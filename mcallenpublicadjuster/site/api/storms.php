<?php
/**
 * JSON feed of storm events for the Storm History, Weather Events and Storm Lookup tools.
 *   /api/storms.php?set=history   NOAA NCEI Storm Events (verified)
 *   /api/storms.php?set=events    NWS Local Storm Reports (preliminary)
 *   /api/storms.php?set=all       both
 */
declare(strict_types=1);
define('MPA_ROOT', dirname(__DIR__));
require_once MPA_ROOT . '/includes/config.php';
require_once MPA_ROOT . '/includes/functions.php';
require_once MPA_ROOT . '/includes/storms.php';

header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');
header('Cache-Control: public, max-age=1800');

$set = $_GET['set'] ?? 'all';
$out = ['updated' => [], 'events' => []];
$fields = ['id', 'src', 'type', 'fam', 'date', 'time', 'loc', 'area', 'lat', 'lon', 'hail_in', 'wind_mph', 'mag_type', 'tor_scale', 'damage', 'text', 'url', 'reporter', 'verified'];
$add = function (array $data, string $key) use (&$out, $fields) {
    $out['updated'][$key] = $data['updated'] ?? null;
    foreach ($data['events'] ?? [] as $e) {
        $row = [];
        foreach ($fields as $f) {
            if (isset($e[$f]) && $e[$f] !== null && $e[$f] !== '') {
                $row[$f] = $e[$f];
            }
        }
        $out['events'][] = $row;
    }
};
if ($set === 'history' || $set === 'all') {
    $add(storm_history(), 'history');
}
if ($set === 'events' || $set === 'all') {
    $add(weather_events_data(), 'events');
}
usort($out['events'], fn($a, $b) => strcmp(($b['date'] ?? '') . ($b['time'] ?? ''), ($a['date'] ?? '') . ($a['time'] ?? '')));
$etag = '"' . md5(json_encode($out['updated']) . $set) . '"';
header('ETag: ' . $etag);
if (($_SERVER['HTTP_IF_NONE_MATCH'] ?? '') === $etag) {
    http_response_code(304);
    exit;
}
echo json_encode($out, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
