<?php
/**
 * Live weather from the National Weather Service API (api.weather.gov).
 * No API key is required; NWS asks for an identifying User-Agent.
 *
 * Everything is cached in data/cache/*.json. Pages read the cache; if it is
 * stale, one refresh is attempted with a short timeout. If NWS is down, the
 * last good data is shown with its timestamp, or a fallback message.
 */

declare(strict_types=1);

require_once __DIR__ . '/functions.php';

function http_get_json(string $url, int $timeout = 0, array $headers = []): ?array
{
    $body = http_get($url, $timeout, array_merge(['Accept: application/geo+json, application/json'], $headers));
    if ($body === null) {
        return null;
    }
    $data = json_decode($body, true);
    return is_array($data) ? $data : null;
}

function http_get(string $url, int $timeout = 0, array $headers = []): ?string
{
    $timeout = $timeout ?: (int) cfg('http_timeout', 8);
    $ua = cfg('nws_user_agent');
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS      => 3,
            CURLOPT_CONNECTTIMEOUT => min(5, $timeout),
            CURLOPT_TIMEOUT        => $timeout,
            CURLOPT_USERAGENT      => $ua,
            CURLOPT_HTTPHEADER     => $headers,
            CURLOPT_ENCODING       => '',
        ]);
        $body = curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        $err = curl_error($ch);
        curl_close($ch);
        if ($body === false || $code < 200 || $code >= 300) {
            log_line('http', "GET $url failed ($code) $err");
            return null;
        }
        return (string) $body;
    }
    $ctx = stream_context_create(['http' => [
        'timeout' => $timeout, 'ignore_errors' => true,
        'header' => "User-Agent: $ua\r\n" . implode("\r\n", $headers),
    ]]);
    $body = @file_get_contents($url, false, $ctx);
    $status = isset($http_response_header[0]) ? (int) preg_replace('#^HTTP/\S+\s+(\d+).*#', '$1', $http_response_header[0]) : 0;
    if ($body === false || $status < 200 || $status >= 300) {
        log_line('http', "GET $url failed ($status)");
        return null;
    }
    return $body;
}

/** Cached fetch: returns ['data'=>..., 'fetched'=>ts, 'stale'=>bool] or null. */
function cached_fetch(string $key, int $ttl, callable $fetch, bool $allowRefresh = true): ?array
{
    $file = data_path('cache/' . $key . '.json');
    $cache = read_json_file($file, null);
    $age = $cache ? time() - (int) ($cache['fetched'] ?? 0) : PHP_INT_MAX;
    if ($cache && $age < $ttl && !defined('MPA_FORCE_REFRESH')) {
        $cache['stale'] = false;
        return $cache;
    }
    if ($allowRefresh) {
        // Simple lock so concurrent visitors don't all hit the API.
        $lock = $file . '.lock';
        $locked = is_file($lock) && time() - filemtime($lock) < 30;
        if (!$locked) {
            @touch($lock);
            $data = null;
            try {
                $data = $fetch();
            } catch (Throwable $ex) {
                log_line('weather', $key . ' fetch error: ' . $ex->getMessage());
            }
            @unlink($lock);
            if ($data !== null) {
                $cache = ['fetched' => time(), 'data' => $data];
                write_json_file($file, $cache);
                $cache['stale'] = false;
                return $cache;
            }
        }
    }
    if ($cache) {
        $cache['stale'] = true;
        return $cache;
    }
    return null;
}

/** Grid point metadata for McAllen (rarely changes; cached for 7 days). */
function nws_point(bool $allowRefresh = true): ?array
{
    $c = cached_fetch('nws-point', 86400 * 7, function () {
        $j = http_get_json(sprintf('https://api.weather.gov/points/%.4f,%.4f', cfg('lat'), cfg('lon')));
        if (!$j || empty($j['properties']['forecast'])) {
            return null;
        }
        $p = $j['properties'];
        return [
            'forecast'     => $p['forecast'],
            'gridData'     => $p['forecastGridData'],
            'office'       => $p['gridId'],
            'gridX'        => $p['gridX'],
            'gridY'        => $p['gridY'],
            'zone'         => basename((string) $p['forecastZone']),
            'county'       => basename((string) $p['county']),
        ];
    }, $allowRefresh);
    return $c['data'] ?? null;
}

function c_to_f($c): ?float
{
    return $c === null ? null : $c * 9 / 5 + 32;
}

function kmh_to_mph($k): ?float
{
    return $k === null ? null : $k * 0.621371;
}

function deg_to_compass($deg): string
{
    if ($deg === null) {
        return '';
    }
    $dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
    return $dirs[(int) round(fmod((float) $deg + 360, 360) / 22.5) % 16];
}

/** Current observation at McAllen Miller International Airport (KMFE). */
function weather_current(bool $allowRefresh = true): ?array
{
    return cached_fetch('wx-current', (int) cfg('cache_ttl_current'), function () {
        $j = http_get_json('https://api.weather.gov/stations/' . cfg('nws_station') . '/observations/latest');
        $p = $j['properties'] ?? null;
        if (!$p || !isset($p['timestamp'])) {
            return null;
        }
        $v = fn($k) => $p[$k]['value'] ?? null;
        // Treat observations older than 3 hours as unusable.
        if (strtotime($p['timestamp']) < time() - 3 * 3600) {
            log_line('weather', 'Latest observation too old: ' . $p['timestamp']);
            return null;
        }
        return [
            'time'        => $p['timestamp'],
            'text'        => $p['textDescription'] ?? '',
            'icon'        => $p['icon'] ?? '',
            'temp_f'      => c_to_f($v('temperature')),
            'dewpoint_f'  => c_to_f($v('dewpoint')),
            'humidity'    => $v('relativeHumidity'),
            'wind_mph'    => kmh_to_mph($v('windSpeed')),
            'gust_mph'    => kmh_to_mph($v('windGust')),
            'wind_dir'    => $v('windDirection'),
            'heat_index_f'=> c_to_f($v('heatIndex')),
            'wind_chill_f'=> c_to_f($v('windChill')),
            'pressure_inhg' => $v('barometricPressure') !== null ? $v('barometricPressure') / 3386.389 : null,
            'visibility_mi' => $v('visibility') !== null ? $v('visibility') / 1609.344 : null,
            'station'     => cfg('nws_station'),
        ];
    }, $allowRefresh);
}

/** 7-day forecast (14 day/night periods) plus daily precipitation totals from grid data. */
function weather_forecast(bool $allowRefresh = true): ?array
{
    return cached_fetch('wx-forecast', (int) cfg('cache_ttl_forecast'), function () use ($allowRefresh) {
        $pt = nws_point($allowRefresh);
        if (!$pt) {
            return null;
        }
        $j = http_get_json($pt['forecast']);
        $periods = $j['properties']['periods'] ?? null;
        if (!$periods) {
            return null;
        }
        $out = [];
        foreach ($periods as $p) {
            $out[] = [
                'name'     => $p['name'],
                'start'    => $p['startTime'],
                'isDay'    => (bool) $p['isDaytime'],
                'temp'     => $p['temperature'],
                'unit'     => $p['temperatureUnit'],
                'pop'      => $p['probabilityOfPrecipitation']['value'] ?? null,
                'wind'     => trim(($p['windSpeed'] ?? '') . ' ' . ($p['windDirection'] ?? '')),
                'icon'     => $p['icon'] ?? '',
                'short'    => $p['shortForecast'] ?? '',
                'detailed' => $p['detailedForecast'] ?? '',
            ];
        }
        // Daily QPF (inches) from the raw grid. Optional: forecast still works without it.
        $qpf = [];
        $grid = http_get_json($pt['gridData'], 10);
        foreach ($grid['properties']['quantitativePrecipitation']['values'] ?? [] as $row) {
            [$start, $dur] = array_pad(explode('/', $row['validTime']), 2, 'PT1H');
            $ts = strtotime($start);
            $mm = (float) ($row['value'] ?? 0);
            // Attribute the amount to the local calendar day of the period start.
            $day = date('Y-m-d', $ts);
            $qpf[$day] = ($qpf[$day] ?? 0) + $mm / 25.4;
        }
        return [
            'updated' => $j['properties']['updateTime'] ?? ($j['properties']['generatedAt'] ?? null),
            'periods' => $out,
            'qpf'     => array_map(fn($x) => round($x, 2), $qpf),
            'office'  => $pt['office'],
            'grid'    => $pt['gridX'] . ',' . $pt['gridY'],
        ];
    }, $allowRefresh);
}

/** Active NWS alerts (watches, warnings, advisories) for the McAllen point. */
function weather_alerts(bool $allowRefresh = true): ?array
{
    return cached_fetch('wx-alerts', (int) cfg('cache_ttl_alerts'), function () {
        $j = http_get_json(sprintf('https://api.weather.gov/alerts/active?point=%.4f,%.4f', cfg('lat'), cfg('lon')));
        if (!$j || !isset($j['features'])) {
            return null;
        }
        $alerts = [];
        foreach ($j['features'] as $f) {
            $p = $f['properties'];
            // Skip expired alerts even if the feed still lists them.
            if (!empty($p['expires']) && strtotime($p['expires']) < time()) {
                continue;
            }
            $alerts[] = [
                'id'          => $p['id'] ?? '',
                'event'       => $p['event'] ?? 'Weather Alert',
                'severity'    => $p['severity'] ?? 'Unknown',
                'urgency'     => $p['urgency'] ?? '',
                'headline'    => $p['headline'] ?? '',
                'description' => $p['description'] ?? '',
                'instruction' => $p['instruction'] ?? '',
                'area'        => $p['areaDesc'] ?? '',
                'effective'   => $p['effective'] ?? ($p['onset'] ?? ''),
                'expires'     => $p['ends'] ?? ($p['expires'] ?? ''),
                'sender'      => $p['senderName'] ?? 'National Weather Service',
            ];
        }
        return $alerts;
    }, $allowRefresh);
}

/** Map an NWS icon URL to one of our inline SVG weather icons. */
function wx_icon_key(string $iconUrl, ?bool $isDay = null): string
{
    $night = $isDay === false || ($isDay === null && strpos($iconUrl, '/night/') !== false);
    $path = (string) parse_url($iconUrl, PHP_URL_PATH);
    $code = strtok(basename($path), ',?') ?: '';
    // Combined icons like "rain_showers,40/tsra" — use the most significant part.
    if (preg_match('/(tsra|tornado|hurricane|tropical_storm)/', $path)) {
        return 'storm';
    }
    if (preg_match('/(snow|sleet|fzra|blizzard)/', $path)) {
        return 'snow';
    }
    if (preg_match('/(rain|showers)/', $path)) {
        return 'rain';
    }
    if (preg_match('/(fog|haze|smoke|dust)/', $path)) {
        return 'fog';
    }
    if (preg_match('/wind_/', $path)) {
        return 'wind';
    }
    if (preg_match('/(ovc|bkn)/', $code)) {
        return 'cloud';
    }
    if (preg_match('/sct/', $code)) {
        return $night ? 'partly-night' : 'partly';
    }
    return $night ? 'moon' : 'sun';
}

function wx_svg(string $key, string $label = ''): string
{
    $sun = '<circle cx="32" cy="32" r="11" fill="#F5B83D"/><g stroke="#F5B83D" stroke-width="3.5" stroke-linecap="round"><path d="M32 8v6M32 50v6M8 32h6M50 32h6M15 15l4.2 4.2M44.8 44.8 49 49M15 49l4.2-4.2M44.8 19.2 49 15"/></g>';
    $cloud = '<path d="M46 50H20a11 11 0 1 1 2.6-21.7A14 14 0 0 1 49.5 31 9.5 9.5 0 0 1 46 50Z" fill="#DCE4EC" stroke="#9FB1C3" stroke-width="2"/>';
    $smallSun = '<circle cx="24" cy="24" r="9" fill="#F5B83D"/><g stroke="#F5B83D" stroke-width="3" stroke-linecap="round"><path d="M24 7v4M7 24h4M12 12l3 3M36 12l-3 3"/></g>';
    $moon = '<path d="M40 12a18 18 0 1 0 12 30A20 20 0 0 1 40 12Z" fill="#E8D7A6"/>';
    $map = [
        'sun'          => $sun,
        'moon'         => $moon,
        'partly'       => $smallSun . '<path d="M48 52H24a10 10 0 1 1 2.4-19.7A12.5 12.5 0 0 1 50.5 35 8.5 8.5 0 0 1 48 52Z" fill="#DCE4EC" stroke="#9FB1C3" stroke-width="2"/>',
        'partly-night' => '<path d="M30 8a14 14 0 1 0 10 23A16 16 0 0 1 30 8Z" fill="#E8D7A6"/><path d="M48 52H24a10 10 0 1 1 2.4-19.7A12.5 12.5 0 0 1 50.5 35 8.5 8.5 0 0 1 48 52Z" fill="#DCE4EC" stroke="#9FB1C3" stroke-width="2"/>',
        'cloud'        => $cloud,
        'rain'         => '<path d="M46 42H20a11 11 0 1 1 2.6-21.7A14 14 0 0 1 49.5 23 9.5 9.5 0 0 1 46 42Z" fill="#DCE4EC" stroke="#9FB1C3" stroke-width="2"/><g stroke="#3B82C4" stroke-width="3" stroke-linecap="round"><path d="M22 48l-3 7M32 48l-3 7M42 48l-3 7"/></g>',
        'storm'        => '<path d="M46 40H20a11 11 0 1 1 2.6-21.7A14 14 0 0 1 49.5 21 9.5 9.5 0 0 1 46 40Z" fill="#B8C5D3" stroke="#7C90A5" stroke-width="2"/><path d="M33 40l-6 10h7l-4 10 11-14h-7l4-6Z" fill="#F5B83D"/>',
        'snow'         => $cloud . '<g fill="#7FB3E0"><circle cx="22" cy="57" r="2.5"/><circle cx="32" cy="59" r="2.5"/><circle cx="42" cy="57" r="2.5"/></g>',
        'fog'          => '<g stroke="#9FB1C3" stroke-width="4" stroke-linecap="round"><path d="M12 24h40M8 34h44M14 44h38"/></g>',
        'wind'         => '<g fill="none" stroke="#7C90A5" stroke-width="4" stroke-linecap="round"><path d="M8 26h30a7 7 0 1 0-7-7"/><path d="M8 38h40a7 7 0 1 1-7 7"/></g>',
    ];
    $inner = $map[$key] ?? $sun;
    $aria = $label !== '' ? ' role="img" aria-label="' . e($label) . '"' : ' aria-hidden="true"';
    return '<svg class="wx-svg" viewBox="0 0 64 64" width="64" height="64"' . $aria . '>' . $inner . '</svg>';
}

/** Group forecast periods into days: [['name','date','hi','lo','pop','icon','short','detailed', 'qpf']] */
function forecast_days(array $fc): array
{
    $days = [];
    foreach ($fc['periods'] as $p) {
        $date = date('Y-m-d', strtotime($p['start']));
        if (!isset($days[$date])) {
            $days[$date] = ['date' => $date, 'name' => $p['isDay'] ? $p['name'] : date('D', strtotime($p['start'])), 'hi' => null, 'lo' => null, 'pop' => null, 'icon' => null, 'short' => '', 'detailed' => [], 'isDay' => $p['isDay']];
        }
        $d = &$days[$date];
        if ($p['isDay']) {
            $d['hi'] = $p['temp'];
            $d['icon'] = $p['icon'];
            $d['short'] = $p['short'];
            $d['isDay'] = true;
            $d['name'] = $p['name'];
        } else {
            $d['lo'] = $p['temp'];
            if ($d['icon'] === null) {
                $d['icon'] = $p['icon'];
                $d['short'] = $p['short'];
            }
        }
        if ($p['pop'] !== null) {
            $d['pop'] = max((int) $d['pop'], (int) $p['pop']);
        }
        $d['detailed'][] = $p['name'] . ': ' . $p['detailed'];
        unset($d);
    }
    foreach ($days as $date => &$d) {
        $d['qpf'] = $fc['qpf'][$date] ?? null;
        if (in_array($d['name'], ['This Afternoon', 'Today', 'Tonight', 'Overnight'], true)) {
            $d['name'] = 'Today';
        }
    }
    unset($d);
    return array_slice(array_values($days), 0, 7);
}

function fmt_num($v, int $dec = 0, string $suffix = ''): string
{
    return $v === null ? '—' : number_format((float) $v, $dec) . $suffix;
}

function time_ago(int $ts): string
{
    $d = time() - $ts;
    if ($d < 90) {
        return 'just now';
    }
    if ($d < 3600) {
        return round($d / 60) . ' minutes ago';
    }
    if ($d < 86400 * 2) {
        $h = (int) round($d / 3600);
        return $h . ' hour' . ($h === 1 ? '' : 's') . ' ago';
    }
    return round($d / 86400) . ' days ago';
}

/** Stream a (large) remote file to disk. Returns true on success. */
function http_download(string $url, string $dest, int $timeout = 600): bool
{
    if (!function_exists('curl_init')) {
        $body = http_get($url, $timeout);
        return $body !== null && @file_put_contents($dest, $body) !== false;
    }
    $fp = @fopen($dest, 'wb');
    if (!$fp) {
        return false;
    }
    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_FILE => $fp, CURLOPT_FOLLOWLOCATION => true, CURLOPT_CONNECTTIMEOUT => 15,
        CURLOPT_TIMEOUT => $timeout, CURLOPT_USERAGENT => cfg('nws_user_agent'),
    ]);
    $ok = curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
    curl_close($ch);
    fclose($fp);
    if (!$ok || $code !== 200) {
        log_line('http', "Download $url failed ($code)");
        @unlink($dest);
        return false;
    }
    return true;
}
