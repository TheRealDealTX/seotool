<?php
declare(strict_types=1);

namespace RT;

/**
 * Outbound HTTP for importers and link checks.
 *  - identifies itself with the configured User-Agent
 *  - honours robots.txt (Disallow + Crawl-delay) for the source host
 *  - retries network errors, 429 and 5xx with exponential backoff
 */
final class Http
{
    /** @var array<string,array{disallow:string[],allow:string[],delay:float}> */
    private static array $robots = [];
    /** @var array<string,float> last request time per host */
    private static array $lastHit = [];

    public static int $retries = 3;
    public static int $backoffBase = 2;       // seconds: 2, 4, 8
    public static bool $respectRobots = true;

    public static function userAgent(): string
    {
        return (string) cfg('import.user_agent', 'RodeoTexasBot/1.0');
    }

    /**
     * @return array{status:int, body:string, final_url:string, content_type:string}
     * @throws \RuntimeException after retries are exhausted or when robots.txt disallows
     */
    public static function get(string $url, array $opts = []): array
    {
        if (!preg_match('~^https?://~i', $url)) {
            throw new \RuntimeException('Refusing non-http URL: ' . $url);
        }
        $host = strtolower((string) parse_url($url, PHP_URL_HOST));
        if (self::$respectRobots && empty($opts['skip_robots'])) {
            if (!self::allowedByRobots($url)) {
                throw new \RuntimeException('Blocked by robots.txt: ' . $url);
            }
            self::politeWait($host, max((float) ($opts['min_delay'] ?? 1), self::$robots[$host]['delay'] ?? 0));
        }
        $attempts = max(1, (int) ($opts['retries'] ?? self::$retries));
        $lastErr = '';
        for ($i = 1; $i <= $attempts; $i++) {
            $r = self::once($url, $opts);
            self::$lastHit[$host] = microtime(true);
            if ($r['error'] === '' && $r['status'] < 500 && $r['status'] !== 429) {
                return $r;
            }
            $lastErr = $r['error'] !== '' ? $r['error'] : 'HTTP ' . $r['status'];
            if ($i < $attempts) {
                $wait = self::$backoffBase ** $i;
                if ($r['status'] === 429 && $r['retry_after'] > 0) {
                    $wait = min(60, $r['retry_after']);
                }
                sleep($wait);
            }
        }
        throw new \RuntimeException("Request failed after {$attempts} attempts ({$lastErr}): {$url}");
    }

    /** One request, no retry. Never throws. */
    public static function once(string $url, array $opts = []): array
    {
        $ch = curl_init($url);
        $respHeaders = [];
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS      => 5,
            CURLOPT_PROTOCOLS      => CURLPROTO_HTTP | CURLPROTO_HTTPS,
            CURLOPT_REDIR_PROTOCOLS => CURLPROTO_HTTP | CURLPROTO_HTTPS,
            CURLOPT_CONNECTTIMEOUT => 10,
            CURLOPT_TIMEOUT        => (int) ($opts['timeout'] ?? 30),
            CURLOPT_USERAGENT      => self::userAgent(),
            CURLOPT_ENCODING       => '',
            CURLOPT_HTTPHEADER     => $opts['headers'] ?? ['Accept: application/json, text/calendar, text/html;q=0.9, */*;q=0.5'],
            CURLOPT_NOBODY         => !empty($opts['head']),
            CURLOPT_HEADERFUNCTION => static function ($ch, $line) use (&$respHeaders) {
                $p = strpos($line, ':');
                if ($p !== false) {
                    $respHeaders[strtolower(trim(substr($line, 0, $p)))] = trim(substr($line, $p + 1));
                }
                return strlen($line);
            },
        ]);
        $body = curl_exec($ch);
        $err = $body === false ? curl_error($ch) : '';
        $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        $final = (string) curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
        $ctype = (string) curl_getinfo($ch, CURLINFO_CONTENT_TYPE);
        curl_close($ch);
        $max = (int) ($opts['max_bytes'] ?? 20_000_000);
        $body = is_string($body) ? $body : '';
        if (strlen($body) > $max) {
            $body = substr($body, 0, $max);
        }
        return [
            'status' => $status, 'body' => $body, 'final_url' => $final, 'content_type' => $ctype,
            'error' => $err, 'retry_after' => (int) ($respHeaders['retry-after'] ?? 0),
        ];
    }

    public static function allowedByRobots(string $url): bool
    {
        $p = parse_url($url);
        $host = strtolower($p['host'] ?? '');
        if (!isset(self::$robots[$host])) {
            self::$robots[$host] = ['disallow' => [], 'allow' => [], 'delay' => 0.0];
            $r = self::once(($p['scheme'] ?? 'https') . '://' . $host . '/robots.txt', ['timeout' => 15]);
            if ($r['error'] === '' && $r['status'] === 200) {
                self::$robots[$host] = self::parseRobots($r['body'], self::userAgent());
            }
        }
        $path = ($p['path'] ?? '/') . (isset($p['query']) ? '?' . $p['query'] : '');
        $rules = self::$robots[$host];
        $best = ''; $allowed = true;
        foreach ($rules['disallow'] as $d) {
            if ($d !== '' && str_starts_with($path, $d) && strlen($d) > strlen($best)) {
                $best = $d; $allowed = false;
            }
        }
        foreach ($rules['allow'] as $a) {
            if ($a !== '' && str_starts_with($path, $a) && strlen($a) >= strlen($best)) {
                $best = $a; $allowed = true;
            }
        }
        return $allowed;
    }

    /** Parse robots.txt for the group matching our UA token, else '*'. */
    public static function parseRobots(string $txt, string $ua): array
    {
        $token = strtolower(strtok($ua, '/ ') ?: '*');
        $groups = [];
        $inAgents = false;
        foreach (preg_split('/\r?\n/', $txt) as $line) {
            $line = trim(preg_replace('/#.*/', '', $line) ?? '');
            if ($line === '' || strpos($line, ':') === false) {
                continue;
            }
            [$k, $v] = array_map('trim', explode(':', $line, 2));
            $k = strtolower($k);
            if ($k === 'user-agent') {
                if (!$inAgents) {
                    $groups[] = ['agents' => [], 'rules' => []];
                }
                $groups[count($groups) - 1]['agents'][] = strtolower($v);
                $inAgents = true;
                continue;
            }
            $inAgents = false;
            if ($groups) {
                $groups[count($groups) - 1]['rules'][] = [$k, $v];
            }
        }
        $pick = static function (string $want) use ($groups): ?array {
            $out = null;
            foreach ($groups as $g) {
                if (in_array($want, $g['agents'], true)) {
                    $out = array_merge($out ?? [], $g['rules']);
                }
            }
            return $out;
        };
        $rules = $pick($token) ?? $pick('*') ?? [];
        $res = ['disallow' => [], 'allow' => [], 'delay' => 0.0];
        foreach ($rules as [$k, $v]) {
            if ($k === 'disallow') {
                $res['disallow'][] = $v;
            } elseif ($k === 'allow') {
                $res['allow'][] = $v;
            } elseif ($k === 'crawl-delay') {
                $res['delay'] = min(30.0, (float) $v);
            }
        }
        return $res;
    }

    private static function politeWait(string $host, float $delay): void
    {
        if ($delay <= 0 || !isset(self::$lastHit[$host])) {
            return;
        }
        $wait = $delay - (microtime(true) - self::$lastHit[$host]);
        if ($wait > 0) {
            usleep((int) ($wait * 1_000_000));
        }
    }
}
