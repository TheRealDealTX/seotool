<?php
/**
 * Live Temple, TX weather.
 *
 *  - Current conditions + 7-day forecast: Open-Meteo (https://open-meteo.com, no key needed)
 *  - Active alerts: U.S. National Weather Service API (https://api.weather.gov)
 *
 * Responses are cached in /storage/cache. If a service is down, the most
 * recent cached copy (up to weather_max_stale seconds old) is returned and
 * explicitly flagged as cached with its timestamp — never as live data.
 */
defined('TR_ROOT') || exit;

const WMO_CODES = [
    0 => ['Clear sky', 'sun'], 1 => ['Mainly clear', 'sun'], 2 => ['Partly cloudy', 'cloud-sun'], 3 => ['Overcast', 'cloud'],
    45 => ['Fog', 'cloud-fog'], 48 => ['Freezing fog', 'cloud-fog'],
    51 => ['Light drizzle', 'cloud-drizzle'], 53 => ['Drizzle', 'cloud-drizzle'], 55 => ['Heavy drizzle', 'cloud-drizzle'],
    56 => ['Freezing drizzle', 'cloud-drizzle'], 57 => ['Freezing drizzle', 'cloud-drizzle'],
    61 => ['Light rain', 'cloud-rain'], 63 => ['Rain', 'cloud-rain'], 65 => ['Heavy rain', 'cloud-rain'],
    66 => ['Freezing rain', 'cloud-rain'], 67 => ['Heavy freezing rain', 'cloud-rain'],
    71 => ['Light snow', 'cloud-snow'], 73 => ['Snow', 'cloud-snow'], 75 => ['Heavy snow', 'cloud-snow'], 77 => ['Snow grains', 'cloud-snow'],
    80 => ['Rain showers', 'cloud-rain'], 81 => ['Rain showers', 'cloud-rain'], 82 => ['Violent rain showers', 'cloud-rain'],
    85 => ['Snow showers', 'cloud-snow'], 86 => ['Heavy snow showers', 'cloud-snow'],
    95 => ['Thunderstorms', 'cloud-lightning'], 96 => ['Thunderstorms with hail', 'cloud-hail'], 99 => ['Severe thunderstorms with hail', 'cloud-hail'],
];

function wmo(int $code): array
{
    return WMO_CODES[$code] ?? ['Unknown', 'cloud'];
}

/** GET a JSON URL with a short timeout. Returns decoded array or null. */
function http_json(string $url, array $headers = []): ?array
{
    $ua = 'TempleRoofersWebsite/1.0 (' . cfg('base_url') . '/contact/)';
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS      => 3,
            CURLOPT_CONNECTTIMEOUT => 4,
            CURLOPT_TIMEOUT        => 8,
            CURLOPT_USERAGENT      => $ua,
            CURLOPT_HTTPHEADER     => $headers,
        ]);
        $body = curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
    } else {
        $ctx = stream_context_create(['http' => ['timeout' => 8, 'header' => implode("\r\n", array_merge(["User-Agent: $ua"], $headers))]]);
        $body = @file_get_contents($url, false, $ctx);
        $code = $body === false ? 0 : 200;
    }
    if ($body === false || $code < 200 || $code >= 300) {
        return null;
    }
    $data = json_decode((string) $body, true);
    return is_array($data) ? $data : null;
}

/**
 * Cached fetch. Returns ['status' => live|cached|unavailable, 'fetched_at' => int|null, 'data' => array|null].
 * "live" means fetched within the normal TTL; "cached" means a fresh fetch failed and an older copy is shown.
 */
function cached_fetch(string $name, int $ttl, callable $fetch): array
{
    $file = TR_STORAGE . '/cache/' . $name . '.json';
    $cache = is_file($file) ? json_decode((string) @file_get_contents($file), true) : null;
    $now = time();
    if (is_array($cache) && isset($cache['fetched_at']) && $now - $cache['fetched_at'] < $ttl) {
        return ['status' => 'live', 'fetched_at' => $cache['fetched_at'], 'data' => $cache['data']];
    }
    // One request at a time refreshes the cache; others wait briefly on the lock.
    $lock = @fopen($file . '.lock', 'c');
    if ($lock) {
        flock($lock, LOCK_EX);
        $again = is_file($file) ? json_decode((string) @file_get_contents($file), true) : null;
        if (is_array($again) && isset($again['fetched_at']) && $now - $again['fetched_at'] < $ttl) {
            flock($lock, LOCK_UN);
            fclose($lock);
            return ['status' => 'live', 'fetched_at' => $again['fetched_at'], 'data' => $again['data']];
        }
    }
    $fresh = $fetch();
    if ($fresh !== null) {
        storage_write($file, json_encode(['fetched_at' => $now, 'data' => $fresh]));
        $result = ['status' => 'live', 'fetched_at' => $now, 'data' => $fresh];
    } elseif (is_array($cache) && isset($cache['fetched_at']) && $now - $cache['fetched_at'] < (int) cfg('weather_max_stale', 21600)) {
        $result = ['status' => 'cached', 'fetched_at' => $cache['fetched_at'], 'data' => $cache['data']];
    } else {
        $result = ['status' => 'unavailable', 'fetched_at' => null, 'data' => null];
    }
    if ($lock) {
        flock($lock, LOCK_UN);
        fclose($lock);
    }
    return $result;
}

function fetch_forecast(): ?array
{
    $q = http_build_query([
        'latitude'           => cfg('lat'),
        'longitude'          => cfg('lng'),
        'current'            => 'temperature_2m,apparent_temperature,relative_humidity_2m,is_day,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation,uv_index',
        'hourly'             => 'precipitation_probability',
        'daily'              => 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max,uv_index_max,sunrise,sunset',
        'temperature_unit'   => 'fahrenheit',
        'wind_speed_unit'    => 'mph',
        'precipitation_unit' => 'inch',
        'timezone'           => cfg('timezone'),
        'forecast_days'      => 7,
    ]);
    $raw = http_json('https://api.open-meteo.com/v1/forecast?' . $q);
    if (!$raw || empty($raw['current']) || empty($raw['daily']['time'])) {
        return null;
    }
    $c = $raw['current'];
    // Precipitation probability for the current hour.
    $pop = null;
    $hourKey = substr((string) $c['time'], 0, 13) . ':00';
    $idx = array_search($hourKey, $raw['hourly']['time'] ?? [], true);
    if ($idx !== false) {
        $pop = $raw['hourly']['precipitation_probability'][$idx] ?? null;
    }
    [$label, $icon] = wmo((int) $c['weather_code']);
    if (!$c['is_day'] && in_array($icon, ['sun', 'cloud-sun'], true)) {
        $icon = $icon === 'sun' ? 'moon' : 'cloud-moon';
    }
    $current = [
        'time'        => $c['time'],
        'temp'        => round((float) $c['temperature_2m']),
        'feels'       => round((float) $c['apparent_temperature']),
        'humidity'    => (int) $c['relative_humidity_2m'],
        'wind'        => round((float) $c['wind_speed_10m']),
        'wind_dir'    => compass((float) $c['wind_direction_10m']),
        'gust'        => round((float) $c['wind_gusts_10m']),
        'precip'      => (float) $c['precipitation'],
        'pop'         => $pop,
        'uv'          => isset($c['uv_index']) ? round((float) $c['uv_index'], 1) : null,
        'code'        => (int) $c['weather_code'],
        'label'       => $label,
        'icon'        => $icon,
        'is_day'      => (bool) $c['is_day'],
    ];
    $d = $raw['daily'];
    $days = [];
    foreach ($d['time'] as $i => $date) {
        $code = (int) $d['weather_code'][$i];
        [$dl, $di] = wmo($code);
        $day = [
            'date'    => $date,
            'code'    => $code,
            'label'   => $dl,
            'icon'    => $di,
            'hi'      => round((float) $d['temperature_2m_max'][$i]),
            'lo'      => round((float) $d['temperature_2m_min'][$i]),
            'pop'     => $d['precipitation_probability_max'][$i] ?? null,
            'rain'    => round((float) ($d['precipitation_sum'][$i] ?? 0), 2),
            'wind'    => round((float) $d['wind_speed_10m_max'][$i]),
            'gust'    => round((float) $d['wind_gusts_10m_max'][$i]),
            'uv'      => isset($d['uv_index_max'][$i]) ? round((float) $d['uv_index_max'][$i], 1) : null,
            'storm'   => $code >= 95,
            'sunrise' => $d['sunrise'][$i] ?? null,
            'sunset'  => $d['sunset'][$i] ?? null,
        ];
        $day['risk'] = roof_risk($day);
        $days[] = $day;
    }
    return ['current' => $current, 'days' => $days];
}

function compass(float $deg): string
{
    $dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    return $dirs[(int) round($deg / 22.5) % 16];
}

/**
 * Informational roof-weather indicator (NOT an official alert). Rules:
 *  High:     gusts >= 58 mph (NWS severe-wind threshold) or thunderstorms with hail in the forecast
 *  Elevated: gusts 40-57 mph, thunderstorms, rain >= 1.5 in, or high >= 100 F
 *  Low:      none of the above
 */
function roof_risk(array $day): array
{
    $level = 'low';
    $reasons = [];
    if ($day['gust'] >= 58) {
        $level = 'high';
        $reasons[] = 'Gusts near ' . $day['gust'] . ' mph can lift or tear shingles';
    } elseif ($day['gust'] >= 40) {
        $level = 'elevated';
        $reasons[] = 'Gusts to ' . $day['gust'] . ' mph may loosen weak shingles and debris';
    }
    if (in_array($day['code'], [96, 99], true)) {
        $level = 'high';
        $reasons[] = 'Thunderstorms with possible hail in the forecast';
    } elseif ($day['code'] === 95) {
        $level = $level === 'high' ? 'high' : 'elevated';
        $reasons[] = 'Thunderstorms possible';
    }
    if ($day['rain'] >= 1.5) {
        $level = $level === 'high' ? 'high' : 'elevated';
        $reasons[] = 'Heavy rain (' . $day['rain'] . ' in) can expose leaks and overflow gutters';
    }
    if ($day['hi'] >= 100) {
        $level = $level === 'high' ? 'high' : 'elevated';
        $reasons[] = 'Extreme heat (' . $day['hi'] . '°F) stresses shingles and attic ventilation';
    }
    return ['level' => $level, 'reasons' => $reasons];
}

function fetch_alerts(): ?array
{
    $raw = http_json(
        'https://api.weather.gov/alerts/active?point=' . cfg('lat') . ',' . cfg('lng'),
        ['Accept: application/geo+json']
    );
    if (!$raw || !isset($raw['features']) || !is_array($raw['features'])) {
        return null;
    }
    $items = [];
    foreach ($raw['features'] as $f) {
        $p = $f['properties'] ?? [];
        if (($p['status'] ?? 'Actual') !== 'Actual') {
            continue;
        }
        $items[] = [
            'event'       => (string) ($p['event'] ?? 'Weather alert'),
            'severity'    => (string) ($p['severity'] ?? 'Unknown'),
            'urgency'     => (string) ($p['urgency'] ?? ''),
            'headline'    => (string) ($p['headline'] ?? ''),
            'area'        => (string) ($p['areaDesc'] ?? ''),
            'effective'   => $p['onset'] ?? $p['effective'] ?? null,
            'ends'        => $p['ends'] ?? $p['expires'] ?? null,
            'description' => mb_substr((string) ($p['description'] ?? ''), 0, 1200),
            'instruction' => mb_substr((string) ($p['instruction'] ?? ''), 0, 800),
            'sender'      => (string) ($p['senderName'] ?? 'National Weather Service'),
            'url'         => (string) ($p['@id'] ?? $f['id'] ?? ''),
        ];
    }
    return $items;
}

/** Combined payload for /api/weather/. */
function weather_payload(): array
{
    $fc = cached_fetch('forecast', (int) cfg('weather_ttl', 600), 'fetch_forecast');
    $al = cached_fetch('alerts', (int) cfg('alerts_ttl', 300), 'fetch_alerts');
    $iso = fn ($t) => $t ? (new DateTimeImmutable('@' . $t))->setTimezone(new DateTimeZone(cfg('timezone')))->format('c') : null;
    return [
        'location' => 'Temple, TX',
        'timezone' => cfg('timezone'),
        'forecast' => ['status' => $fc['status'], 'fetched_at' => $iso($fc['fetched_at'])] + ($fc['data'] ?? []),
        'alerts'   => ['status' => $al['status'], 'fetched_at' => $iso($al['fetched_at']), 'items' => $al['data'] ?? []],
        'links'    => [
            'nws'    => 'https://forecast.weather.gov/MapClick.php?lat=' . cfg('lat') . '&lon=' . cfg('lng'),
            'source' => 'https://open-meteo.com/',
        ],
    ];
}
