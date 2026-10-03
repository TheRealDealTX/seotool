<?php
/**
 * Storm data: NOAA NCEI Storm Events (verified history) and NWS Local Storm
 * Reports (preliminary, near real time). Shared by pages, the JSON API, and cron.
 */

declare(strict_types=1);

require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/weather.php';

const STORM_HISTORY_FILE = 'storm-history.json';
const WEATHER_EVENTS_FILE = 'weather-events.json';

/** Event types we track, grouped into display families. */
function storm_type_family(string $type): string
{
    $t = strtolower($type);
    if (strpos($t, 'hail') !== false) return 'hail';
    if (strpos($t, 'tornado') !== false || strpos($t, 'funnel') !== false) return 'tornado';
    if (strpos($t, 'hurricane') !== false || strpos($t, 'tropical') !== false) return 'tropical';
    if (strpos($t, 'flood') !== false || strpos($t, 'rain') !== false) return 'flood';
    if (strpos($t, 'wind') !== false || strpos($t, 'thunderstorm') !== false) return 'wind';
    if (strpos($t, 'freeze') !== false || strpos($t, 'cold') !== false || strpos($t, 'ice') !== false || strpos($t, 'winter') !== false || strpos($t, 'snow') !== false) return 'winter';
    return 'other';
}

function storm_family_label(string $fam): string
{
    return [
        'hail' => 'Hail', 'wind' => 'Wind', 'tornado' => 'Tornado', 'tropical' => 'Tropical Storm / Hurricane',
        'flood' => 'Flood & Heavy Rain', 'winter' => 'Freeze & Winter', 'other' => 'Other',
    ][$fam] ?? 'Other';
}

function storm_family_icon(string $fam): string
{
    return ['hail' => 'hail', 'wind' => 'wind', 'tornado' => 'storm', 'tropical' => 'hurricane', 'flood' => 'water', 'winter' => 'thermo'][$fam] ?? 'storm';
}

/** NCEI event types kept in the history (heat and drought are excluded). */
function ncei_tracked_types(): array
{
    return [
        'Hail', 'Thunderstorm Wind', 'High Wind', 'Strong Wind', 'Tornado', 'Funnel Cloud',
        'Flash Flood', 'Flood', 'Heavy Rain', 'Tropical Storm', 'Hurricane', 'Hurricane (Typhoon)',
        'Tropical Depression', 'Storm Surge/Tide', 'Lightning', 'Frost/Freeze', 'Extreme Cold/Wind Chill',
        'Cold/Wind Chill', 'Ice Storm', 'Winter Storm', 'Winter Weather', 'Heavy Snow',
    ];
}

function kt_to_mph(?float $kt): ?float
{
    return $kt === null ? null : round($kt * 1.15078);
}

/** Title-case NCEI place names ("MC ALLEN" -> "McAllen"). */
function nice_place(string $s): string
{
    $s = trim($s);
    if ($s === '') {
        return '';
    }
    $s = ucwords(strtolower($s));
    $fix = ['Mc Allen' => 'McAllen', 'Mc Cook' => 'McCook', 'Penitas' => 'Peñitas', '(mfe)miller Intl Arp' => 'McAllen-Miller Intl Airport', 'Muni Arpt' => 'Municipal Airport', 'Mid Vly Arpt' => 'Mid Valley Airport', 'Intl Arpt' => 'Intl Airport', 'Hidalgo County' => 'Hidalgo County'];
    return strtr($s, $fix);
}

/** Convert one NCEI CSV row (assoc) into our normalized event record. */
function ncei_normalize(array $r): ?array
{
    if (!in_array($r['EVENT_TYPE'] ?? '', ncei_tracked_types(), true)) {
        return null;
    }
    // BEGIN_DATE_TIME e.g. "08-MAY-25 13:52:00" (2-digit year) — use BEGIN_YEARMONTH + BEGIN_DAY instead.
    $ym = $r['BEGIN_YEARMONTH'] ?? '';
    $date = sprintf('%s-%s-%02d', substr($ym, 0, 4), substr($ym, 4, 2), (int) ($r['BEGIN_DAY'] ?? 1));
    $time = str_pad((string) ($r['BEGIN_TIME'] ?? '0'), 4, '0', STR_PAD_LEFT);
    $mag = ($r['MAGNITUDE'] ?? '') !== '' ? (float) $r['MAGNITUDE'] : null;
    $type = $r['EVENT_TYPE'];
    $isWind = in_array($type, ['Thunderstorm Wind', 'High Wind', 'Strong Wind'], true);
    $loc = nice_place($r['BEGIN_LOCATION'] ?? '');
    if ($loc === '') {
        $loc = nice_place($r['CZ_NAME'] ?? 'Hidalgo County');
        if (($r['CZ_TYPE'] ?? '') === 'C') {
            $loc .= ' County';
        } elseif (stripos($loc, 'county') === false) {
            $loc .= ' County (zone)';
        }
    }
    $lat = ($r['BEGIN_LAT'] ?? '') !== '' ? round((float) $r['BEGIN_LAT'], 3) : null;
    $lon = ($r['BEGIN_LON'] ?? '') !== '' ? round((float) $r['BEGIN_LON'], 3) : null;
    $narr = trim(preg_replace('/\s+/', ' ', str_replace('|', ' ', ($r['EVENT_NARRATIVE'] ?? '') ?: ($r['EPISODE_NARRATIVE'] ?? ''))));
    if (mb_strlen($narr) > 700) {
        $narr = rtrim(mb_substr($narr, 0, 690), " ,.;") . '…';
    }
    $magType = ['EG' => 'estimated gust', 'MG' => 'measured gust', 'ES' => 'estimated sustained', 'MS' => 'measured sustained'][$r['MAGNITUDE_TYPE'] ?? ''] ?? '';
    return [
        'id'        => 'ncei-' . $r['EVENT_ID'],
        'src'       => 'NCEI',
        'type'      => $type === 'Hurricane (Typhoon)' ? 'Hurricane' : $type,
        'fam'       => storm_type_family($type),
        'date'      => $date,
        'time'      => substr($time, 0, 2) . ':' . substr($time, 2, 2),
        'tz'        => $r['CZ_TIMEZONE'] ?? 'CST-6',
        'loc'       => $loc,
        'area'      => nice_place($r['CZ_NAME'] ?? '') . (($r['CZ_TYPE'] ?? '') === 'C' ? ' County' : ''),
        'lat'       => $lat,
        'lon'       => $lon,
        'hail_in'   => $type === 'Hail' ? $mag : null,
        'wind_kt'   => $isWind ? $mag : null,
        'wind_mph'  => $isWind ? kt_to_mph($mag) : null,
        'mag_type'  => $isWind ? $magType : '',
        'tor_scale' => ($r['TOR_F_SCALE'] ?? '') ?: null,
        'damage'    => ($r['DAMAGE_PROPERTY'] ?? '') ?: null,
        'text'      => $narr,
        'url'       => 'https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=' . $r['EVENT_ID'],
        'episode'   => $r['EPISODE_ID'] ?? '',
    ];
}

function storm_history(): array
{
    static $h = null;
    if ($h === null) {
        $h = read_json_file(data_path(STORM_HISTORY_FILE), ['updated' => null, 'events' => []]);
    }
    return $h;
}

function weather_events_data(): array
{
    static $w = null;
    if ($w === null) {
        $w = read_json_file(data_path(WEATHER_EVENTS_FILE), ['updated' => null, 'events' => []]);
    }
    return $w;
}

/* ------------------------------------------------------------------ */
/* NWS Local Storm Reports                                            */
/* ------------------------------------------------------------------ */

/** Map LSR event text (NWS or IEM "typetext") to our type names. Returns null to skip. */
function lsr_type(string $raw): ?string
{
    $t = strtoupper(trim($raw));
    $map = [
        'HAIL' => 'Hail', 'TSTM WND GST' => 'Thunderstorm Wind', 'TSTM WND DMG' => 'Thunderstorm Wind',
        'NON-TSTM WND GST' => 'High Wind', 'NON-TSTM WND DMG' => 'High Wind', 'HIGH SUST WINDS' => 'High Wind',
        'TORNADO' => 'Tornado', 'FUNNEL CLOUD' => 'Funnel Cloud', 'WATERSPOUT' => null,
        'FLASH FLOOD' => 'Flash Flood', 'FLOOD' => 'Flood', 'HEAVY RAIN' => 'Heavy Rain',
        'TROPICAL STORM' => 'Tropical Storm', 'HURRICANE' => 'Hurricane', 'STORM SURGE' => 'Storm Surge/Tide',
        'LIGHTNING' => 'Lightning', 'DOWNBURST' => 'Thunderstorm Wind', 'FREEZE' => 'Frost/Freeze',
        'EXTREME COLD' => 'Extreme Cold/Wind Chill', 'ICE STORM' => 'Ice Storm', 'SNOW' => 'Heavy Snow',
        'HEAVY SNOW' => 'Heavy Snow', 'SLEET' => 'Winter Weather', 'FREEZING RAIN' => 'Ice Storm',
    ];
    return $map[$t] ?? null;
}

/** Normalize one LSR into our record. $mag like "E1.75 INCH" / "M62 MPH" / "1.75". */
function lsr_record(array $x): ?array
{
    $type = lsr_type($x['typetext']);
    if ($type === null) {
        return null;
    }
    $fam = storm_type_family($type);
    $magRaw = strtoupper(trim((string) ($x['mag'] ?? '')));
    $num = null;
    $qual = '';
    if (preg_match('/^([EMU])?\s*([\d.]+)/', $magRaw, $m)) {
        $num = (float) $m[2];
        $qual = ['E' => 'estimated', 'M' => 'measured', 'U' => 'unknown'][$m[1] ?? ''] ?? '';
    } elseif (is_numeric($magRaw)) {
        $num = (float) $magRaw;
    }
    $isWind = $fam === 'wind';
    $unit = $x['unit'] ?? (strpos($magRaw, 'MPH') !== false ? 'MPH' : (strpos($magRaw, 'KT') !== false ? 'KT' : ''));
    $windMph = null;
    if ($isWind && $num !== null) {
        $windMph = strtoupper((string) $unit) === 'KT' || strtoupper((string) $unit) === 'KTS' ? kt_to_mph($num) : round($num);
    }
    $ts = strtotime($x['valid']);
    if (!$ts) {
        return null;
    }
    $text = trim(preg_replace('/\s+/', ' ', (string) ($x['remark'] ?? '')));
    $key = gmdate('YmdHi', $ts) . '|' . $type . '|' . round((float) $x['lat'], 2) . '|' . round((float) $x['lon'], 2);
    return [
        'id'       => 'lsr-' . substr(sha1($key), 0, 16),
        'src'      => 'NWS LSR',
        'type'     => $type,
        'fam'      => $fam,
        'date'     => date('Y-m-d', $ts),
        'time'     => date('H:i', $ts),
        'iso'      => date('c', $ts),
        'loc'      => str_ireplace('Mcallen', 'McAllen', trim((string) $x['city'])),
        'area'     => trim((string) $x['county']) . ' County',
        'lat'      => round((float) $x['lat'], 3),
        'lon'      => round((float) $x['lon'], 3),
        'hail_in'  => $fam === 'hail' ? $num : null,
        'wind_mph' => $windMph,
        'mag_type' => $isWind && $qual ? $qual . ' gust' : ($qual ?: ''),
        'reporter' => trim((string) ($x['source'] ?? '')),
        'text'     => mb_substr($text, 0, 700),
        'url'      => $x['url'],
        'product'  => $x['product'] ?? '',
        'verified' => date('c'),
        'correction' => stripos($text, 'corrects previous') !== false,
    ];
}

/**
 * Parse an NWS LSR text product (fixed-width format) into raw report arrays.
 * Handles the standard 2-line report blocks followed by indented remarks.
 */
function parse_lsr_text(string $text, string $productUrl): array
{
    $lines = preg_split('/\r?\n/', $text);
    // Time zone from the issuance line, e.g. "1038 PM CDT Thu Oct 1 2026".
    $tzAbbr = 'CDT';
    foreach ($lines as $l) {
        if (preg_match('/^\d{3,4} (AM|PM) ([A-Z]{3}) /', trim($l), $m)) {
            $tzAbbr = $m[2];
            break;
        }
    }
    $offset = ['CDT' => '-05:00', 'CST' => '-06:00', 'MDT' => '-06:00', 'MST' => '-07:00'][$tzAbbr] ?? '-06:00';
    $out = [];
    $n = count($lines);
    for ($i = 0; $i < $n - 1; $i++) {
        $l1 = $lines[$i];
        $l2 = $lines[$i + 1];
        if (!preg_match('/^(\d{3,4}) (AM|PM)\s/', $l1, $tm) || !preg_match('#^(\d{2})/(\d{2})/(\d{4})#', $l2, $dm)) {
            continue;
        }
        $event = trim(substr($l1, 12, 17));
        $city = trim(substr($l1, 29, 24));
        $latlon = trim(substr($l1, 53));
        $mag = trim(substr($l2, 12, 17));
        $county = trim(substr($l2, 29, 19));
        $state = trim(substr($l2, 48, 4));
        $source = trim(substr($l2, 53));
        if (!preg_match('/([\d.]+)N\s+([\d.]+)W/', $latlon, $ll)) {
            continue;
        }
        $hhmm = str_pad($tm[1], 4, '0', STR_PAD_LEFT);
        $h = (int) substr($hhmm, 0, 2) % 12 + ($tm[2] === 'PM' ? 12 : 0);
        $iso = sprintf('%s-%s-%sT%02d:%s:00%s', $dm[3], $dm[1], $dm[2], $h, substr($hhmm, 2, 2), $offset);
        $remarks = [];
        for ($j = $i + 2; $j < $n; $j++) {
            $r = $lines[$j];
            if (trim($r) === '') {
                if ($remarks) {
                    break;
                }
                continue;
            }
            if (preg_match('/^\s{6,}\S/', $r)) {
                $remarks[] = trim($r);
            } else {
                break;
            }
        }
        $unit = '';
        if (preg_match('/(MPH|KT|KTS|INCH|INCHES|IN)\b/i', $mag, $um)) {
            $unit = strtoupper($um[1]);
        }
        $out[] = [
            'typetext' => $event, 'city' => $city, 'county' => $county, 'state' => $state,
            'lat' => (float) $ll[1], 'lon' => -(float) $ll[2], 'valid' => $iso, 'mag' => $mag, 'unit' => $unit,
            'source' => $source, 'remark' => implode(' ', $remarks), 'url' => $productUrl,
        ];
    }
    return $out;
}

/** Merge new LSR records into the list, applying NWS corrections and de-duplicating. */
function merge_lsr_events(array $existing, array $incoming): array
{
    $byId = [];
    foreach ($existing as $e) {
        $byId[$e['id']] = $e;
    }
    $added = 0;
    foreach ($incoming as $e) {
        if (!isset($byId[$e['id']])) {
            $added++;
        } else {
            $e['verified'] = date('c'); // seen again: refresh verification time
        }
        $byId[$e['id']] = array_merge($byId[$e['id']] ?? [], $e);
    }
    // A correction supersedes earlier reports of the same type and time within ~3 km.
    foreach ($byId as $cid => $c) {
        if (empty($c['correction'])) {
            continue;
        }
        foreach ($byId as $id => $old) {
            if ($id !== $cid && empty($old['correction']) && $old['type'] === $c['type'] && $old['date'] === $c['date']
                && $old['time'] === $c['time'] && abs($old['lat'] - $c['lat']) < 0.03 && abs($old['lon'] - $c['lon']) < 0.03) {
                unset($byId[$id]);
            }
        }
    }
    $list = array_values($byId);
    usort($list, fn($a, $b) => strcmp(($b['date'] . $b['time']), ($a['date'] . $a['time'])));
    return [$list, $added];
}

/** Describe the severity of an event in plain words. */
function storm_severity(array $e): string
{
    if (!empty($e['hail_in'])) {
        $in = (float) $e['hail_in'];
        $label = hail_size_label($in);
        return rtrim(rtrim(number_format($in, 2), '0'), '.') . '" hail' . ($label ? ' (' . $label . ')' : '');
    }
    if (!empty($e['wind_mph'])) {
        return (int) $e['wind_mph'] . ' mph' . (!empty($e['mag_type']) ? ' ' . $e['mag_type'] : ' wind');
    }
    if (!empty($e['tor_scale'])) {
        return $e['tor_scale'] . ' tornado';
    }
    return '';
}

function hail_size_label(float $in): string
{
    $sizes = [[4.5, 'softball+'], [4.0, 'softball'], [2.75, 'baseball'], [2.5, 'tennis ball'], [2.0, 'hen egg'], [1.75, 'golf ball'], [1.5, 'ping pong ball'], [1.25, 'half dollar'], [1.0, 'quarter'], [0.88, 'nickel'], [0.75, 'penny'], [0.5, 'marble']];
    foreach ($sizes as [$min, $label]) {
        if ($in >= $min) {
            return $label;
        }
    }
    return 'pea';
}

/** Summary statistics from the verified NCEI history (used for counters). */
function storm_stats(): array
{
    $h = storm_history();
    $s = ['hail' => 0, 'hail_175' => 0, 'max_hail' => 0, 'max_hail_ev' => null, 'wind' => 0, 'max_wind' => 0, 'max_wind_ev' => null,
          'tornado' => 0, 'flood' => 0, 'tropical' => 0, 'first_year' => null, 'last_year' => null, 'total' => count($h['events'] ?? []),
          'by_month_hail' => array_fill(1, 12, 0), 'by_month_wind' => array_fill(1, 12, 0)];
    foreach ($h['events'] ?? [] as $e) {
        $y = (int) substr($e['date'], 0, 4);
        $m = (int) substr($e['date'], 5, 2);
        $s['first_year'] = $s['first_year'] === null ? $y : min($s['first_year'], $y);
        $s['last_year'] = $s['last_year'] === null ? $y : max($s['last_year'], $y);
        switch ($e['fam']) {
            case 'hail':
                $s['hail']++;
                $s['hail_first'] = isset($s['hail_first']) ? min($s['hail_first'], $y) : $y;
                $s['by_month_hail'][$m]++;
                if (($e['hail_in'] ?? 0) >= 1.75) $s['hail_175']++;
                if (($e['hail_in'] ?? 0) > $s['max_hail']) { $s['max_hail'] = $e['hail_in']; $s['max_hail_ev'] = $e; }
                break;
            case 'wind':
                if ($e['type'] === 'Thunderstorm Wind') { $s['wind']++; $s['by_month_wind'][$m]++; }
                if (($e['wind_mph'] ?? 0) > $s['max_wind']) { $s['max_wind'] = $e['wind_mph']; $s['max_wind_ev'] = $e; }
                break;
            case 'tornado':
                if ($e['type'] === 'Tornado') $s['tornado']++;
                break;
            case 'flood':
                if (in_array($e['type'], ['Flash Flood', 'Flood'], true)) $s['flood']++;
                break;
            case 'tropical':
                $s['tropical']++;
                break;
        }
    }
    return $s;
}
