<?php
/**
 * External weekly import runner (used by the scheduled Claude Code routine, or any machine with PHP 8 + cURL).
 *
 *   RODEOTEXAS_IMPORT_TOKEN=… php tools/external-import.php [--site=https://rodeotexas.org]
 *        [--research=research.json] [--only=slug,slug] [--dry-run]
 *
 * 1. GET  {site}/api/import/sources/  → which sources to fetch and their adapter configuration
 * 2. fetch each source here with the same adapters the server uses (robots.txt + Crawl-delay honoured)
 * 3. POST {site}/api/import/          → {"source": slug, "records": [...]}   (or {"error": "..."} if fetching failed)
 * 4. optional: POST the research file (JSON array of records found on official organizer pages) to the
 *    "weekly-research" source — those are always held for admin review.
 *
 * The server applies every rule (Texas-only, dedupe, admin locks, explicit-only cancellations, review queue).
 * A source that fails here is reported as failed and its existing events stay untouched.
 * Exit code: 0 all OK, 1 any failure.
 */
declare(strict_types=1);

putenv('RT_CONFIG=' . __DIR__ . '/runner-config.php');
define('RT_PUBLIC', dirname(__DIR__) . '/public_html');
require dirname(__DIR__) . '/app/bootstrap.php';

use RT\Http;

$opts = getopt('', ['site::', 'research::', 'only::', 'dry-run']);
$site = rtrim((string) ($opts['site'] ?? (getenv('RODEOTEXAS_SITE') ?: 'https://rodeotexas.org')), '/');
$token = (string) getenv('RODEOTEXAS_IMPORT_TOKEN');
$dry = isset($opts['dry-run']);
$only = isset($opts['only']) ? array_filter(explode(',', (string) $opts['only'])) : null;
if ($token === '' && !$dry) {
    fwrite(STDERR, "RODEOTEXAS_IMPORT_TOKEN is not set. Create a token in Admin → Account and add it to the environment settings.\n");
    exit(1);
}
if (!str_starts_with($site, 'https://') && !str_starts_with($site, 'http://127.0.0.1') && !str_starts_with($site, 'http://localhost')) {
    fwrite(STDERR, "Refusing to send the token over plain HTTP.\n");
    exit(1);
}

function api(string $method, string $url, string $token, ?array $body = null): array
{
    $ch = curl_init($url);
    $headers = ['Accept: application/json', 'Authorization: Bearer ' . $token, 'X-Import-Token: ' . $token];
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 300, CURLOPT_CONNECTTIMEOUT => 20,
        CURLOPT_USERAGENT => 'RodeoTexas-ExternalRoutine/1.0', CURLOPT_CUSTOMREQUEST => $method]);
    if ($body !== null) {
        $headers[] = 'Content-Type: application/json';
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE));
    }
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    $raw = curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    $err = curl_error($ch);
    curl_close($ch);
    return [$code, is_string($raw) ? (json_decode($raw, true) ?? ['raw' => substr($raw, 0, 300)]) : ['error' => $err]];
}

/** POST with retries for transient server errors (408/429/5xx). A 409 means an import is already running. */
function post(string $site, string $token, array $body): array
{
    for ($i = 1; $i <= 4; $i++) {
        [$code, $resp] = api('POST', $site . '/api/import/', $token, $body);
        if ($code === 200 || ($code >= 400 && $code < 500 && !in_array($code, [408, 409, 429], true))) {
            return [$code, $resp];
        }
        sleep(min(60, 5 * 2 ** $i));
    }
    return [$code, $resp];
}

$ok = true;
$summary = [];
if ($dry) {
    $sources = ['fetch' => [], 'push_only' => []];
    echo "Dry run: no token used, nothing sent.\n";
} else {
    [$code, $sources] = api('GET', $site . '/api/import/sources/', $token);
    if ($code !== 200 || !isset($sources['fetch'])) {
        fwrite(STDERR, "Could not load the source list (HTTP {$code}): " . json_encode($sources) . "\n");
        exit(1);
    }
}
$map = ['tribe_rest' => RT\Adapters\TribeRestAdapter::class, 'ical' => RT\Adapters\IcalAdapter::class, 'jsonld' => RT\Adapters\JsonLdAdapter::class];
foreach ($sources['fetch'] as $s) {
    if ($only !== null && !in_array($s['slug'], $only, true)) {
        continue;
    }
    $cls = $map[$s['adapter']] ?? null;
    if ($cls === null) {
        continue;
    }
    $adapter = new $cls(['slug' => $s['slug'], 'name' => $s['name'], 'config' => json_encode($s['config'])],
        static function (string $level, string $msg) use ($s): void { echo "  [{$s['slug']}] {$level}: {$msg}\n"; });
    echo "Fetching {$s['name']}…\n";
    try {
        $records = $adapter->fetch();
        $body = ['source' => $s['slug'], 'records' => $records];
        echo '  fetched ' . count($records) . " record(s)\n";
    } catch (\Throwable $e) {
        $body = ['source' => $s['slug'], 'error' => $e->getMessage()];
        echo '  FETCH FAILED: ' . $e->getMessage() . "\n";
        $ok = false;
    }
    [$code, $resp] = post($site, $token, $body);
    echo "  server: HTTP {$code} " . ($resp['message'] ?? json_encode($resp)) . "\n";
    $summary[$s['slug']] = ['http' => $code, 'status' => $resp['status'] ?? null, 'message' => $resp['message'] ?? null];
    if ($code !== 200 || ($resp['status'] ?? '') === 'failed') {
        $ok = false;
    }
}

// Research results: JSON array of records (see app/adapters/Adapter.php for the record format).
if (!empty($opts['research'])) {
    $file = (string) $opts['research'];
    $recs = json_decode((string) @file_get_contents($file), true);
    if (!is_array($recs) || !array_is_list($recs)) {
        fwrite(STDERR, "Research file {$file} is not a JSON array.\n");
        $ok = false;
    } else {
        $clean = [];
        foreach ($recs as $r) {
            if (!is_array($r) || empty($r['title']) || empty($r['start_date']) || empty($r['source_url'])) {
                echo '  skipped research record without title/start_date/source_url: ' . json_encode($r) . "\n";
                continue;
            }
            $r['uid'] = $r['uid'] ?? ('research:' . sha1(strtolower((string) $r['source_url']) . '|' . $r['start_date'] . '|' . strtolower((string) $r['title'])));
            $r += ['end_date' => $r['start_date'], 'performances' => [], 'venue' => [], 'categories' => [], 'status' => null];
            $clean[] = $r;
        }
        echo 'Research: ' . count($clean) . " record(s)\n";
        if ($dry) {
            echo json_encode($clean, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . "\n";
        } elseif ($clean) {
            [$code, $resp] = post($site, $token, ['source' => 'weekly-research', 'records' => $clean]);
            echo "  server: HTTP {$code} " . ($resp['message'] ?? json_encode($resp)) . "\n";
            $summary['weekly-research'] = ['http' => $code, 'status' => $resp['status'] ?? null, 'message' => $resp['message'] ?? null];
            if ($code !== 200) {
                $ok = false;
            }
        }
    }
}
echo "\nSUMMARY " . json_encode($summary, JSON_UNESCAPED_SLASHES) . "\n";
exit($ok ? 0 : 1);
