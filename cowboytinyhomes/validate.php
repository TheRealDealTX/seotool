<?php
// Checks for cowboytinyhomes: plan geometry and copy, the Texas cost table, and that every
// routed page has a template. Run from the repo: php cowboytinyhomes/validate.php
declare(strict_types=1);
require __DIR__ . '/site/inc/config.php';
require __DIR__ . '/site/inc/pages.php';
$problems = [];

$tile = function (string $slug, string $what, array $rooms, float $W, float $D) use (&$problems) {
    $area = 0;
    foreach ($rooms as $i => [$l, $x, $y, $w, $d]) {
        if ($x < 0 || $y < 0 || $x + $w > $W + 1e-6 || $y + $d > $D + 1e-6) $problems[] = "$slug: $what room $l is outside the footprint";
        $area += $w * $d;
        foreach (array_slice($rooms, $i + 1) as [$l2, $x2, $y2, $w2, $d2]) {
            if (min($x + $w, $x2 + $w2) - max($x, $x2) > 1e-6 && min($y + $d, $y2 + $d2) - max($y, $y2) > 1e-6) $problems[] = "$slug: $what rooms $l and $l2 overlap";
        }
    }
    if (abs($area - $W * $D) > 1e-6) $problems[] = "$slug: $what rooms cover $area of " . ($W * $D) . " sq ft";
};
foreach ($PLANS as $slug => $p) {
    $tile($slug, 'main', $p['rooms'], $p['W'], $p['D']);
    if (!empty($p['upper'])) {
        $tile($slug, 'upper', $p['upper'], $p['W'], $p['D']);
        $s1 = array_values(array_filter($p['rooms'], fn($r) => $r[0] === 'STAIR'));
        $s2 = array_values(array_filter($p['upper'], fn($r) => $r[0] === 'STAIR'));
        if (!$s1 || $s1 != $s2) $problems[] = "$slug: the STAIR must be the same rectangle on both floors";
    }
    if (!preg_match('/\b(' . preg_quote(number_format($p['sqft']), '/') . '|' . $p['sqft'] . ') sq ft\b/', $p['intro'])) $problems[] = "$slug: intro does not state {$p['sqft']} sq ft";
    $sleep = 0;
    foreach (array_merge($p['rooms'], $p['upper'] ?? [], $p['loft'] ?? []) as $r) if (preg_match('/BED|PRIMARY|BUNK|STUDIO|LOFT/', $r[0]) && !preg_match('/STORAGE/', $r[0])) $sleep++;
    if ($sleep < $p['beds']) $problems[] = "$slug: {$p['beds']} beds listed but only $sleep sleeping areas drawn";
    if ($p['type'] === 'park-model' && $p['main_sqft'] > 400) $problems[] = "$slug: park model over 400 sq ft";
    if ($p['mobile'] && $p['D'] > 8.5) $problems[] = "$slug: tiny house on wheels wider than 8.5 ft";
    foreach (['name', 'title', 'price', 'intro', 'layout', 'features', 'texas', 'category', 'type', 'styles'] as $k) if (empty($p[$k])) $problems[] = "$slug: missing $k";
    if (!isset(PAGES[$p['url']])) $problems[] = "$slug: no route for {$p['url']}";
}
$profile = json_decode((string)file_get_contents(__DIR__ . '/generator/profile.json'), true);
if ($profile['cost_regions'] != TX_REGIONS) $problems[] = 'TX_REGIONS in config.php does not match generator/profile.json cost_regions';
foreach (PAGES as $path => $m) if (!is_file(__DIR__ . '/site/pages/' . $m['file'] . '.php')) $problems[] = "$path: missing template pages/{$m['file']}.php";
$sets = plan_sets();
foreach ($PLANS as $slug => $p) if (!isset($sets[$slug])) $problems[] = "$slug: not built yet (run generator/build.py)";

echo $problems ? implode("\n", $problems) . "\n" : 'OK: ' . count($PLANS) . " plans, " . count(PAGES) . " routes\n";
exit($problems ? 1 : 0);
