<?php
// Geometry checks for inc/plans.php, used by validate.php. Returns a list of problems.
function plan_geometry_problems(array $PLANS): array {
    $out = [];
    foreach ($PLANS as $slug => $p) {
        if (empty($p['rooms'])) continue;
        $W = $p['W']; $D = $p['D']; $area = 0;
        foreach ($p['rooms'] as $i => [$l, $x, $y, $w, $d]) {
            if ($x < 0 || $y < 0 || $x + $w > $W + 1e-6 || $y + $d > $D + 1e-6) $out[] = "$slug: room $l is outside the footprint";
            $area += $w * $d;
            foreach (array_slice($p['rooms'], $i + 1) as [$l2, $x2, $y2, $w2, $d2]) {
                if (min($x + $w, $x2 + $w2) - max($x, $x2) > 1e-6 && min($y + $d, $y2 + $d2) - max($y, $y2) > 1e-6) $out[] = "$slug: rooms $l and $l2 overlap";
            }
        }
        if (abs($area - $W * $D) > 1e-6) $out[] = "$slug: rooms cover $area sq ft of a " . ($W * $D) . " sq ft footprint";
        foreach ($p['loft'] ?? [] as [$l, $x, $y, $w, $d]) if ($x < 0 || $y < 0 || $x + $w > $W + 1e-6 || $y + $d > $D + 1e-6) $out[] = "$slug: loft $l is outside the footprint";
        if ($p['sqft'] !== $p['main_sqft'] + $p['loft_sqft']) $out[] = "$slug: sqft {$p['sqft']} != main + loft";
        if (!preg_match('/\b' . number_format($p['sqft']) . ' sq ft\b|\b' . $p['sqft'] . ' sq ft\b/', $p['intro'])) $out[] = "$slug: intro does not state {$p['sqft']} sq ft";
        $beds = 0; foreach ($p['rooms'] as $r) if (preg_match('/BED|PRIMARY|STUDIO|SLEEP/', $r[0])) $beds++;
        foreach ($p['loft'] ?? [] as $r) if (!preg_match('/STORAGE/', $r[0])) $beds++;
        if ($beds < $p['beds']) $out[] = "$slug: {$p['beds']} beds listed but only $beds sleeping areas drawn";
    }
    return $out;
}
