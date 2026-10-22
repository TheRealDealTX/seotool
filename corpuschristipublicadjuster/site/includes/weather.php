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
    if ($cache && $age < $ttl && !defined('CCPA_FORCE_REFRESH')) {
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

/** Grid point metadata for Corpus Christi (rarely changes; cached for 7 days). */
function nws_point(bool $allowRefresh = true): ?array
{
    $c = cached_fetch('nws-point-v2', 86400 * 7, function () {
        $j = http_get_json(sprintf('https://api.weather.gov/points/%.4f,%.4f', cfg('lat'), cfg('lon')));
        if (!$j || empty($j['properties']['forecast'])) {
            return null;
        }
        $p = $j['properties'];
        return [
            'forecast'     => $p['forecast'],
            'hourly'       => $p['forecastHourly'] ?? '',
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

/** Current observation at Corpus Christi International Airport (KCRP). */
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

/** Active NWS alerts (watches, warnings, advisories) for the Corpus Christi point. */
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

/** Hourly forecast for the next 48 hours (NWS forecastHourly). */
function weather_hourly(bool $allowRefresh = true): ?array
{
    return cached_fetch('wx-hourly', (int) cfg('cache_ttl_forecast'), function () use ($allowRefresh) {
        $pt = nws_point($allowRefresh);
        if (!$pt || empty($pt['hourly'])) {
            return null;
        }
        $j = http_get_json($pt['hourly']);
        $periods = $j['properties']['periods'] ?? null;
        if (!$periods) {
            return null;
        }
        $out = [];
        foreach (array_slice($periods, 0, 48) as $p) {
            $out[] = [
                'start' => $p['startTime'],
                'isDay' => (bool) $p['isDaytime'],
                'temp'  => $p['temperature'],
                'pop'   => $p['probabilityOfPrecipitation']['value'] ?? null,
                'wind'  => trim(($p['windSpeed'] ?? '') . ' ' . ($p['windDirection'] ?? '')),
                'icon'  => $p['icon'] ?? '',
                'short' => $p['shortForecast'] ?? '',
            ];
        }
        return ['updated' => $j['properties']['updateTime'] ?? null, 'periods' => $out];
    }, $allowRefresh);
}

/** NOAA CO-OPS tide stations around Corpus Christi (id => label). */
function tide_stations(): array
{
    return [
        '8775296' => 'Corpus Christi Bay (USS Lexington)',
        '8775792' => 'Packery Channel (Padre Island)',
        '8775237' => 'Port Aransas',
    ];
}

/**
 * Observed water level (last 24 h) and predicted tide (next 48 h) for a station,
 * plus high/low tide times. Source: NOAA Tides & Currents (no key needed).
 */
function tides_data(string $station = '8775296', bool $allowRefresh = true): ?array
{
    if (!isset(tide_stations()[$station])) {
        $station = '8775296';
    }
    return cached_fetch('tides-' . $station, 1800, function () use ($station) {
        $base = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?station=' . $station
            . '&datum=MLLW&units=english&time_zone=lst_ldt&format=json&application=CorpusChristiPublicAdjuster';
        $begin = date('Ymd H:i', time() - 24 * 3600);
        $pred = http_get_json($base . '&product=predictions&interval=30&begin_date=' . rawurlencode($begin) . '&range=72', 10);
        $hilo = http_get_json($base . '&product=predictions&interval=hilo&begin_date=' . date('Ymd') . '&range=72', 10);
        if (empty($pred['predictions'])) {
            return null;
        }
        $obs = http_get_json($base . '&product=water_level&range=24', 10);
        $map = fn($rows) => array_map(fn($r) => [strtotime($r['t']), (float) $r['v']], array_filter($rows ?? [], fn($r) => ($r['v'] ?? '') !== ''));
        $observed = $map($obs['data'] ?? []);
        // Thin six-minute observations to every 30 minutes.
        $observed = array_values(array_filter($observed, fn($r) => (int) date('i', $r[0]) % 30 < 6));
        return [
            'station'   => $station,
            'name'      => tide_stations()[$station],
            'predicted' => $map($pred['predictions']),
            'observed'  => $observed,
            'hilo'      => array_map(fn($r) => ['t' => strtotime($r['t']), 'v' => (float) $r['v'], 'type' => $r['type']], $hilo['predictions'] ?? []),
        ];
    }, $allowRefresh);
}

/** Active tropical cyclones from the National Hurricane Center. */
function tropics_data(bool $allowRefresh = true): ?array
{
    return cached_fetch('nhc-storms', 1800, function () {
        $j = http_get_json('https://www.nhc.noaa.gov/CurrentStorms.json', 10);
        if (!is_array($j) || !array_key_exists('activeStorms', $j)) {
            return null;
        }
        $names = ['TD' => 'Tropical Depression', 'TS' => 'Tropical Storm', 'HU' => 'Hurricane', 'MH' => 'Major Hurricane', 'STD' => 'Subtropical Depression', 'STS' => 'Subtropical Storm', 'PTC' => 'Potential Tropical Cyclone', 'PC' => 'Post-Tropical Cyclone'];
        $storms = [];
        foreach ($j['activeStorms'] as $st) {
            $basin = substr((string) ($st['id'] ?? ''), 0, 2);
            $lat = (float) ($st['latitudeNumeric'] ?? 0);
            $lon = (float) ($st['longitudeNumeric'] ?? 0);
            $storms[] = [
                'id'        => $st['id'] ?? '',
                'name'      => $st['name'] ?? '',
                'class'     => $names[$st['classification'] ?? ''] ?? ($st['classification'] ?? ''),
                'basin'     => $basin === 'al' ? 'Atlantic' : ($basin === 'ep' ? 'Eastern Pacific' : 'Central Pacific'),
                'wind_mph'  => isset($st['intensity']) ? (int) round((float) $st['intensity'] * 1.15078) : null,
                'pressure'  => $st['pressure'] ?? null,
                'lat'       => $lat,
                'lon'       => $lon,
                'movement'  => trim(($st['movementDir'] ?? '') !== '' ? deg_to_compass($st['movementDir']) . ' at ' . (int) round((float) ($st['movementSpeed'] ?? 0) * 1.15078) . ' mph' : ''),
                'miles'     => (int) round(geo_miles((float) cfg('lat'), (float) cfg('lon'), $lat, $lon)),
                'updated'   => $st['lastUpdate'] ?? null,
                'link'      => $st['publicAdvisory']['url'] ?? ('https://www.nhc.noaa.gov/'),
            ];
        }
        usort($storms, fn($a, $b) => $a['miles'] <=> $b['miles']);
        return ['storms' => $storms];
    }, $allowRefresh);
}

function geo_miles(float $lat1, float $lon1, float $lat2, float $lon2): float
{
    $r = 3958.8;
    $dLat = deg2rad($lat2 - $lat1);
    $dLon = deg2rad($lon2 - $lon1);
    $a = sin($dLat / 2) ** 2 + cos(deg2rad($lat1)) * cos(deg2rad($lat2)) * sin($dLon / 2) ** 2;
    return 2 * $r * asin(min(1, sqrt($a)));
}

/** Sunrise/sunset for today in Corpus Christi. */
function sun_times(): array
{
    $i = date_sun_info(time(), (float) cfg('lat'), (float) cfg('lon'));
    return ['rise' => $i['sunrise'] ?? null, 'set' => $i['sunset'] ?? null];
}

/** Days until the Atlantic hurricane season starts, or days left in it. */
function hurricane_season_status(): array
{
    $now = time();
    $y = (int) date('Y');
    $start = strtotime($y . '-06-01');
    $end = strtotime($y . '-11-30 23:59:59');
    if ($now < $start) {
        return ['active' => false, 'days' => (int) ceil(($start - $now) / 86400), 'label' => 'days until hurricane season starts (June 1)'];
    }
    if ($now <= $end) {
        return ['active' => true, 'days' => (int) ceil(($end - $now) / 86400), 'label' => 'days left in hurricane season (ends Nov. 30)'];
    }
    $next = strtotime(($y + 1) . '-06-01');
    return ['active' => false, 'days' => (int) ceil(($next - $now) / 86400), 'label' => 'days until the next hurricane season (June 1)'];
}

/** Simple SVG line chart: $series = [[ts, value], ...]. Returns markup. */
function svg_line_chart(array $series, array $opt = []): string
{
    if (count($series) < 2) {
        return '';
    }
    $w = $opt['w'] ?? 720; $h = $opt['h'] ?? 170; $pad = 28;
    $xs = array_column($series, 0); $ys = array_column($series, 1);
    foreach ($opt['extra'] ?? [] as $ex) { foreach ($ex as $pt) { $ys[] = $pt[1]; $xs[] = $pt[0]; } }
    $x0 = min($xs); $x1 = max($xs); $y0 = min($ys); $y1 = max($ys);
    if ($y1 - $y0 < 0.5) { $y0 -= 0.25; $y1 += 0.25; }
    $X = fn($t) => $pad + ($t - $x0) / max(1, $x1 - $x0) * ($w - 2 * $pad);
    $Y = fn($v) => $h - $pad + 4 - ($v - $y0) / ($y1 - $y0) * ($h - 2 * $pad);
    $path = fn($s) => implode(' ', array_map(fn($p, $i) => ($i ? 'L' : 'M') . round($X($p[0]), 1) . ' ' . round($Y($p[1]), 1), $s, array_keys($s)));
    $cls = $opt['class'] ?? 'tide-chart';
    $grad = $opt['grad'] ?? 'tideGrad';
    $out = '<svg class="' . e($cls) . '" viewBox="0 0 ' . $w . ' ' . $h . '" preserveAspectRatio="none" role="img" aria-label="' . e($opt['label'] ?? 'Chart') . '">';
    $out .= '<defs><linearGradient id="' . e($grad) . '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' . e($opt['color'] ?? '#4a70a9') . '" stop-opacity=".35"/><stop offset="1" stop-color="' . e($opt['color'] ?? '#4a70a9') . '" stop-opacity="0"/></linearGradient></defs>';
    $d = $path($series);
    $out .= '<path class="area" d="' . $d . ' L' . round($X(end($series)[0]), 1) . ' ' . ($h - $pad + 4) . ' L' . round($X($series[0][0]), 1) . ' ' . ($h - $pad + 4) . ' Z"/>';
    $out .= '<path class="line" d="' . $d . '"/>';
    foreach ($opt['extra'] ?? [] as $k => $ex) {
        if (count($ex) > 1) {
            $out .= '<path d="' . $path($ex) . '" fill="none" stroke="' . e($opt['extra_color'] ?? '#ff8a5b') . '" stroke-width="2.5"/>';
        }
    }
    if (!empty($opt['now'])) {
        $nx = round($X(time()), 1);
        $out .= '<line class="now" x1="' . $nx . '" x2="' . $nx . '" y1="8" y2="' . ($h - $pad + 4) . '"/><text x="' . ($nx + 4) . '" y="16">Now</text>';
    }
    foreach ($opt['labels'] ?? [] as [$t, $txt]) {
        $out .= '<text x="' . round($X($t), 1) . '" y="' . ($h - 6) . '" text-anchor="middle">' . e($txt) . '</text>';
    }
    $out .= '<text x="4" y="' . round($Y($y1) + 4, 1) . '">' . e(number_format($y1, 1) . ($opt['unit'] ?? '')) . '</text>';
    $out .= '<text x="4" y="' . round($Y($y0) + 4, 1) . '">' . e(number_format($y0, 1) . ($opt['unit'] ?? '')) . '</text>';
    return $out . '</svg>';
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
