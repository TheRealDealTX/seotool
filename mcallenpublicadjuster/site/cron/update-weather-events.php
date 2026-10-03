<?php
/**
 * Collect new storm reports for the coverage area and save them to data/weather-events.json.
 *
 * Sources:
 *   1. National Weather Service API — official Local Storm Report (LSR) products issued by
 *      NWS Brownsville/Rio Grande Valley (BRO): https://api.weather.gov/products/types/LSR/locations/BRO
 *   2. Iowa Environmental Mesonet LSR archive (mirror of the same NWS reports) to backfill
 *      reports that rolled off the NWS API: https://mesonet.agron.iastate.edu/geojson/lsr.php
 *
 * Suggested schedule: every hour.   php cron/update-weather-events.php [--days=30]
 */
declare(strict_types=1);
require __DIR__ . '/_cli.php';

$counties = array_map('strtoupper', (array) cfg('event_counties', [cfg('county_name')]));
$state = cfg('state_abbr');
$days = (int) cli_opt('days', 14);
$file = data_path(WEATHER_EVENTS_FILE);
$store = read_json_file($file, ['events' => [], 'products' => [], 'status' => []]);
$store['products'] = $store['products'] ?? [];
$incoming = [];
$status = [];

// --- 1. NWS API LSR products ----------------------------------------
$list = http_get_json('https://api.weather.gov/products/types/LSR/locations/' . cfg('nws_office'), 15);
if ($list === null) {
    $status['nws'] = 'error';
    out('events', 'NWS product list unavailable');
} else {
    $status['nws'] = 'ok';
    $n = 0;
    foreach ($list['@graph'] ?? [] as $prod) {
        $pid = $prod['id'] ?? '';
        if ($pid === '' || isset($store['products'][$pid])) {
            continue;
        }
        $p = http_get_json('https://api.weather.gov/products/' . rawurlencode($pid), 15);
        if (!$p || empty($p['productText'])) {
            continue;
        }
        $url = 'https://api.weather.gov/products/' . $pid;
        foreach (parse_lsr_text($p['productText'], $url) as $raw) {
            if (strtoupper($raw['state']) === $state && in_array(strtoupper($raw['county']), $counties, true)) {
                $raw['product'] = $pid;
                $rec = lsr_record($raw);
                if ($rec) {
                    $incoming[] = $rec;
                    $n++;
                }
            }
        }
        $store['products'][$pid] = $prod['issuanceTime'] ?? date('c');
    }
    out('events', "NWS API: $n report(s) in coverage area from new products");
}

// --- 2. IEM archive backfill -----------------------------------------
$sts = gmdate('YmdHi', time() - $days * 86400);
$ets = gmdate('YmdHi', time() + 3600);
$iem = http_get_json("https://mesonet.agron.iastate.edu/geojson/lsr.php?sts=$sts&ets=$ets&wfos=" . cfg('nws_office'), 30);
if ($iem === null) {
    $status['iem'] = 'error';
    out('events', 'IEM archive unavailable');
} else {
    $status['iem'] = 'ok';
    $n = 0;
    foreach ($iem['features'] ?? [] as $f) {
        $x = $f['properties'];
        if (strtoupper($x['state'] ?? '') !== $state || !in_array(strtoupper($x['county'] ?? ''), $counties, true)) {
            continue;
        }
        $rec = lsr_record([
            'typetext' => $x['typetext'] ?? '', 'city' => $x['city'] ?? '', 'county' => $x['county'] ?? '',
            'lat' => $x['lat'], 'lon' => $x['lon'], 'valid' => $x['valid'], 'mag' => (string) ($x['magnitude'] ?? ''),
            'unit' => $x['unit'] ?? '', 'source' => $x['source'] ?? '', 'remark' => $x['remark'] ?? '',
            'url' => 'https://mesonet.agron.iastate.edu/p.php?pid=' . rawurlencode((string) ($x['product_id'] ?? '')),
            'product' => $x['product_id'] ?? '',
        ]);
        if ($rec) {
            // Validate: coordinates must fall in/near the county bounding box.
            if ($rec['lat'] < 25.9 || $rec['lat'] > 26.85 || $rec['lon'] < -98.65 || $rec['lon'] > -97.65) {
                continue;
            }
            $incoming[] = $rec;
            $n++;
        }
    }
    out('events', "IEM archive: $n report(s) in coverage area over the last $days day(s)");
}

if ($status['nws'] === 'error' && $status['iem'] === 'error') {
    $store['status'] = ['last_attempt' => date('c'), 'ok' => false, 'sources' => $status] + ($store['status'] ?? []);
    write_json_file($file, $store);
    out('events', 'All sources failed; keeping existing events.');
    exit(1);
}

[$events, $added] = merge_lsr_events($store['events'] ?? [], $incoming);
// Keep three years of reports; forget processed product ids after 60 days.
$cut = date('Y-m-d', strtotime('-3 years'));
$events = array_values(array_filter($events, fn($e) => $e['date'] >= $cut));
$store['products'] = array_filter($store['products'], fn($t) => strtotime($t) > time() - 60 * 86400);
$store['events'] = $events;
$store['updated'] = date('c');
$store['status'] = ['last_attempt' => date('c'), 'last_success' => date('c'), 'ok' => true, 'sources' => $status];
write_json_file($file, $store);
out('events', "Saved " . count($events) . " event(s); $added new.");
exit(0);
