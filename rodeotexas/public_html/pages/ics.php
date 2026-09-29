<?php
/** Downloadable calendar entry: /rodeos/<slug>/calendar.ics */
defined('RT_APP') || exit;

use RT\EventRepo;
use RT\Ics;

$e = EventRepo::bySlug($slug);
if (!$e) {
    rt_not_found();
}
header('Content-Type: text/calendar; charset=utf-8');
header('Content-Disposition: attachment; filename="' . $e['slug'] . '.ics"');
header('Cache-Control: public, max-age=3600');
echo Ics::forEvent($e, EventRepo::performances((int) $e['id']));
