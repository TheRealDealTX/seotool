<?php
/**
 * Read-only JSON used by the map view and the favorites page.
 *   /api/events.json?<same filters as /rodeos/>
 *   /api/events.json?slugs=a,b,c
 */
defined('RT_APP') || exit;

use RT\Dates;
use RT\EventRepo;
use RT\View;

header('Cache-Control: public, max-age=300');
header('X-Robots-Tag: noindex');

if (isset($_GET['slugs'])) {
    $rows = EventRepo::bySlugs(explode(',', (string) $_GET['slugs']));
} else {
    $rows = EventRepo::mapPoints(EventRepo::filtersFrom($_GET));
}
$out = [];
foreach ($rows as $e) {
    $s = Dates::status($e);
    $out[] = [
        'slug' => $e['slug'],
        'title' => $e['title'],
        'url' => '/rodeos/' . $e['slug'] . '/',
        'start_date' => $e['start_date'],
        'end_date' => $e['end_date'],
        'dates' => Dates::range($e['start_date'], $e['end_date']),
        'status' => $s['key'],
        'status_label' => $s['label'],
        'place' => View::place($e),
        'lat' => $e['lat'] !== null ? (float) $e['lat'] : null,
        'lng' => $e['lng'] !== null ? (float) $e['lng'] : null,
        'precise' => $e['location_precision'] === 'address',
        'association' => $e['assoc_abbr'],
        'type' => $e['type_name'],
    ];
}
json_out(['count' => count($out), 'events' => $out]);
