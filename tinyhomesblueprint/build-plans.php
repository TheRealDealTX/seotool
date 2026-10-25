<?php
// Regenerate the plan drawings in assets/plans/ from inc/plans.php:
//   php build-plans.php
require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/plan-svg.php';

$dir = __DIR__ . '/assets/plans';
if (!is_dir($dir)) mkdir($dir, 0755, true);
foreach (glob("$dir/*.svg") as $old) unlink($old);
$n = 0;
foreach ($PLANS as $slug => $p) {
    if (empty($p['rooms'])) continue;
    file_put_contents("$dir/$slug-floor-plan.svg", plan_floor_svg($p));
    file_put_contents("$dir/$slug-elevation.svg", plan_elevation_svg($p));
    $n++;
}
echo "wrote drawings for $n plans to assets/plans/\n";
