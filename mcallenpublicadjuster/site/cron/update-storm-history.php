<?php
/**
 * Update the historical storm list (data/storm-history.json) from the NOAA NCEI
 * Storm Events Database bulk CSV files:
 *   https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/
 *
 * By default only the current and previous year are re-downloaded (NCEI revises
 * recent months). Use --full to rebuild every year since 1950 (slow, ~1 GB download).
 *
 * Suggested schedule: weekly.   php cron/update-storm-history.php [--full] [--years=2024,2025]
 */
declare(strict_types=1);
require __DIR__ . '/_cli.php';

$base = 'https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/';
$index = http_get($base, 30);
if ($index === null) {
    out('history', 'NCEI index unavailable; keeping existing data.');
    exit(1);
}
preg_match_all('/StormEvents_details-ftp_v1\.0_d(\d{4})_c(\d{8})\.csv\.gz/', $index, $m, PREG_SET_ORDER);
$files = [];
foreach ($m as $row) {
    $files[$row[1]] = $row[0]; // year => file (latest creation date wins because names sort)
}
ksort($files);
if (!$files) {
    out('history', 'No NCEI detail files found; keeping existing data.');
    exit(1);
}

if (cli_opt('full')) {
    $years = array_keys($files);
} elseif ($y = cli_opt('years')) {
    $years = array_filter(array_map('trim', explode(',', (string) $y)));
} else {
    $years = [(string) date('Y'), (string) (date('Y') - 1)];
}

$store = read_json_file(data_path(STORM_HISTORY_FILE), ['events' => [], 'files' => []]);
$byId = [];
foreach ($store['events'] ?? [] as $e) {
    $byId[$e['id']] = $e;
}
$store['files'] = $store['files'] ?? [];
$state = cfg('state_name');
$county = strtoupper(cfg('county_name'));
$tmp = data_path('cache/ncei-download.csv.gz');
$changed = 0;

foreach ($years as $year) {
    if (!isset($files[$year])) {
        continue;
    }
    $fname = $files[$year];
    if (($store['files'][$year] ?? '') === $fname && !cli_opt('force')) {
        out('history', "$year unchanged ($fname)");
        continue;
    }
    if (!http_download($base . $fname, $tmp, 600)) {
        out('history', "Download failed for $fname");
        continue;
    }
    $gz = gzopen($tmp, 'rb');
    if (!$gz) {
        out('history', "Could not open $fname");
        continue;
    }
    $header = fgetcsv($gz, 0, ',', '"', '');
    $yearIds = [];
    $count = 0;
    while (($row = fgetcsv($gz, 0, ',', '"', '')) !== false) {
        if (count($row) !== count($header)) {
            continue;
        }
        $r = array_combine($header, $row);
        if ($r['STATE'] !== $state || strpos(strtoupper($r['CZ_NAME']), $county) === false) {
            continue;
        }
        $rec = ncei_normalize($r);
        if ($rec) {
            $yearIds[$rec['id']] = true;
            $byId[$rec['id']] = $rec;
            $count++;
        }
    }
    gzclose($gz);
    @unlink($tmp);
    // Remove records NCEI deleted from this year's file.
    foreach ($byId as $id => $e) {
        if (substr($e['date'], 0, 4) === (string) $year && !isset($yearIds[$id])) {
            unset($byId[$id]);
        }
    }
    $store['files'][$year] = $fname;
    $changed++;
    out('history', "$year: $count tracked event(s) from $fname");
}

$events = array_values($byId);
usort($events, fn($a, $b) => strcmp($b['date'] . $b['time'], $a['date'] . $a['time']));
$store['events'] = $events;
$store['updated'] = date('c');
$store['source'] = 'NOAA National Centers for Environmental Information (NCEI) Storm Events Database';
$store['coverage'] = 'Hidalgo County, Texas (county and NWS forecast zone entries)';
ksort($store['files']);
write_json_file(data_path(STORM_HISTORY_FILE), $store);
out('history', 'Saved ' . count($events) . " event(s); $changed year file(s) processed.");
exit(0);
