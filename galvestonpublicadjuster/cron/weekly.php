<?php
// Weekly job (run by the host's cron, CLI only):
//   1. Weather: scan the last 8 days of Galveston wind observations for sustained winds or
//      gusts >= WIND_EVENT_MPH and add any new event days to data/weather-events.json.
//   2. Blog: publish the next queued post (or, once the queue is empty and an Anthropic API
//      key is configured, write a new one from the Semrush keyword list).
//
// Usage: php cron/weekly.php [--weather-only|--blog-only] [--backfill=YYYY-MM-DD]
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
require dirname(__DIR__) . '/inc/config.php';
require dirname(__DIR__) . '/inc/content.php';

$opts = getopt('', ['weather-only', 'blog-only', 'backfill:']);
date_default_timezone_set('America/Chicago');

function http_get_json($url) {
    $ctx = stream_context_create(['http' => [
        'timeout' => 30,
        'header'  => "User-Agent: (galvestonpublicadjuster.com, " . LEAD_EMAIL . ")\r\nAccept: application/geo+json, application/json\r\n",
    ]]);
    $raw = @file_get_contents($url, false, $ctx);
    return $raw === false ? null : json_decode($raw, true);
}

function logln($s) { echo '[' . date('c') . "] $s\n"; }

// ---------------------------------------------------------------- weather
function check_weather($backfillFrom = null) {
    $kmh = 0.621371;
    $days = [];   // Y-m-d => ['gust' => mph, 'sustained' => mph, 'source' => ...]
    $note = function ($day, $gust, $sus, $src) use (&$days) {
        $d = $days[$day] ?? ['gust' => 0, 'sustained' => 0, 'sources' => []];
        $d['gust'] = max($d['gust'], round($gust));
        $d['sustained'] = max($d['sustained'], round($sus));
        $d['sources'][$src] = true;
        $days[$day] = $d;
    };

    // 1) Measured: NWS observations at Scholes International Airport (KGLS), last ~7 days.
    $start = gmdate('Y-m-d\TH:i:s\Z', strtotime('-8 days'));
    $obs = http_get_json('https://api.weather.gov/stations/KGLS/observations?start=' . urlencode($start) . '&limit=500');
    $nwsOk = is_array($obs) && isset($obs['features']);
    foreach ($obs['features'] ?? [] as $f) {
        $p = $f['properties'] ?? [];
        $g = $p['windGust']['value'] ?? null;
        $s = $p['windSpeed']['value'] ?? null;
        if ($g === null && $s === null) continue;
        $day = date('Y-m-d', strtotime($p['timestamp']));
        $note($day, ($g ?? 0) * $kmh, ($s ?? 0) * $kmh, 'NWS KGLS (Scholes Intl. Airport)');
    }

    // 2) Modeled daily maximums for Galveston Island (Open-Meteo), covers gaps and backfill.
    $from = $backfillFrom ?: date('Y-m-d', strtotime('-8 days'));
    $to = date('Y-m-d', strtotime('-1 day'));
    $base = strtotime($from) < strtotime('-60 days') ? 'https://archive-api.open-meteo.com/v1/archive' : 'https://api.open-meteo.com/v1/forecast';
    $q = $base . '?latitude=' . GEO_LAT . '&longitude=' . GEO_LNG . "&start_date=$from&end_date=$to"
        . '&daily=wind_gusts_10m_max,wind_speed_10m_max&wind_speed_unit=mph&timezone=America%2FChicago';
    $om = http_get_json($q);
    $omOk = isset($om['daily']['time']);
    foreach ($om['daily']['time'] ?? [] as $i => $day) {
        $note($day, $om['daily']['wind_gusts_10m_max'][$i] ?? 0, $om['daily']['wind_speed_10m_max'][$i] ?? 0, 'Open-Meteo model (Galveston Island)');
    }

    // 3) NWS alerts active for Galveston County (hurricane / tropical storm / high wind).
    $alerts = [];
    $al = http_get_json('https://api.weather.gov/alerts/active?point=' . GEO_LAT . ',' . GEO_LNG);
    foreach ($al['features'] ?? [] as $a) {
        $ev = $a['properties']['event'] ?? '';
        if (preg_match('/Hurricane|Tropical Storm|High Wind|Extreme Wind|Tornado|Severe Thunderstorm/i', $ev)) $alerts[] = $ev;
    }

    $events = read_json(DATA . '/weather-events.json');
    $byDate = [];
    foreach ($events as $i => $e) $byDate[$e['date']] = $i;
    $weekMax = 0; $added = 0;
    ksort($days);
    foreach ($days as $day => $d) {
        $weekMax = max($weekMax, $d['gust'], $d['sustained']);
        if (max($d['gust'], $d['sustained']) < WIND_EVENT_MPH) continue;
        $row = [
            'date' => $day,
            'max_gust_mph' => $d['gust'],
            'max_sustained_mph' => $d['sustained'],
            'sources' => array_keys($d['sources']),
            'alerts' => $alerts,
            'summary' => sprintf('Winds reached %d mph (gusts) / %d mph (sustained) around Galveston on %s. At these speeds, older or 60–70 mph-rated shingles commonly crease, lift or blow off; inspect your roof and document damage before filing a windstorm claim.',
                $d['gust'], $d['sustained'], date('F j, Y', strtotime($day))),
            'detected' => date('Y-m-d'),
        ];
        if (isset($byDate[$day])) {
            $old = $events[$byDate[$day]];
            $row['max_gust_mph'] = max($row['max_gust_mph'], $old['max_gust_mph']);
            $row['max_sustained_mph'] = max($row['max_sustained_mph'], $old['max_sustained_mph']);
            $row['sources'] = array_values(array_unique(array_merge($old['sources'], $row['sources'])));
            $row['detected'] = $old['detected'];
            $events[$byDate[$day]] = $row;
        } else {
            $events[] = $row;
            $added++;
        }
    }
    write_json(DATA . '/weather-events.json', array_values($events));
    write_json(DATA . '/weather-status.json', [
        'last_checked' => date('c'),
        'window' => [$from, $to],
        'max_wind_mph_this_check' => $weekMax,
        'new_events' => $added,
        'nws_ok' => $nwsOk,
        'open_meteo_ok' => $omOk,
        'active_alerts' => $alerts,
    ]);
    logln("weather: max {$weekMax} mph, {$added} new event(s), nws=" . ($nwsOk ? 'ok' : 'fail') . ' om=' . ($omOk ? 'ok' : 'fail'));
}

// ---------------------------------------------------------------- blog
function api_key() {
    foreach ([PRIVATE_DIR . '/config.php', DATA . '/private/config.php'] as $f) {
        if (is_file($f)) { $c = include $f; if (!empty($c['anthropic_api_key'])) return $c['anthropic_api_key']; }
    }
    return getenv('ANTHROPIC_API_KEY') ?: null;
}

function generate_post() {
    $key = api_key();
    if (!$key) { logln('blog: queue empty and no API key configured — nothing published'); return null; }
    $keywords = read_json(DATA . '/keywords.json');
    $used = array_map(fn($p) => strtolower($p['keyword'] ?? ''), all_post_sources());
    $pick = null;
    foreach ($keywords as $k) if (!in_array(strtolower($k['keyword']), $used, true)) { $pick = $k; break; }
    if (!$pick) { logln('blog: keyword list exhausted'); return null; }

    $prompt = "Write a blog post for galvestonpublicadjuster.com, a licensed Texas public adjusting firm serving Galveston Island and Galveston County (TWIA windstorm, hurricane, fire, flood, denied or underpaid property claims). Author: " . AUTHOR . ". Phone: " . PHONE . ".\n\n"
        . "Primary keyword: \"{$pick['keyword']}\" (topic cluster: {$pick['topic']}).\n"
        . "Requirements: high buyer intent and genuinely helpful; specific to Galveston / the Texas coast / TWIA where relevant; 1100-1400 words; practical steps and checklists; no invented statistics, case results, testimonials or statute numbers; never promise outcomes. Use the keyword in the title, first paragraph and one H2. Include 2 internal links chosen from: /twia-claims-expert/, /galveston-fire-claims/, /calculators/, /texas-windstorm-rules/, /galveston-local-code/, /galveston-storm-history/, /contact/. End with a CTA paragraph offering a free consultation at <a href=\"tel:" . PHONE_TEL . "\">" . PHONE . "</a>.\n\n"
        . "Return ONLY a JSON object with keys: slug, title (<=65 chars), description (140-160 chars), keyword, category (one of: TWIA & Windstorm | Fire & Smoke | Flood & Water | Denied & Underpaid | Claim Process), read_minutes (int), html (body only: p, h2, h3, ul, ol, li, strong, a, blockquote — no h1, no styles), faq (array of 3 {q, a}).";
    $req = json_encode(['model' => 'claude-sonnet-5', 'max_tokens' => 8000, 'messages' => [['role' => 'user', 'content' => $prompt]]]);
    $ctx = stream_context_create(['http' => ['method' => 'POST', 'timeout' => 180, 'ignore_errors' => true,
        'header' => "content-type: application/json\r\nx-api-key: $key\r\nanthropic-version: 2023-06-01\r\n", 'content' => $req]]);
    $res = json_decode((string)@file_get_contents('https://api.anthropic.com/v1/messages', false, $ctx), true);
    $text = $res['content'][0]['text'] ?? '';
    if (!preg_match('/\{.*\}/s', $text, $m) || !($post = json_decode($m[0], true)) || empty($post['slug']) || empty($post['html'])) {
        logln('blog: generation failed: ' . substr(json_encode($res), 0, 300));
        return null;
    }
    $post['slug'] = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($post['slug'])), '-');
    $post['keyword'] = $pick['keyword'];
    $post['html'] = strip_tags($post['html'], '<p><h2><h3><ul><ol><li><strong><em><a><blockquote>');
    write_json(DATA . '/posts-generated/' . date('Ymd') . '-' . $post['slug'] . '.json', $post);
    return $post;
}

function publish_weekly_post() {
    $pub = read_json(DATA . '/published.json');
    $today = date('Y-m-d');
    // Idempotent: one post per 6 days even if cron fires twice.
    if ($pub && max($pub) > date('Y-m-d', strtotime('-6 days'))) { logln('blog: already published this week'); return; }
    $post = next_queued_post() ?? generate_post();
    if (!$post) return;
    $pub[$post['slug']] = $today;
    write_json(DATA . '/published.json', $pub);
    logln("blog: published {$post['slug']}");
}

if (!isset($opts['blog-only'])) check_weather($opts['backfill'] ?? null);
if (!isset($opts['weather-only'])) publish_weekly_post();
