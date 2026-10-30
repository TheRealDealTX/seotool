<?php
// Blueprint-style SVG drawings generated from a plan's geometry in inc/plans.php.
// plan_floor_svg() draws the dimensioned main floor (plus lofts and porch);
// plan_elevation_svg() draws an 800 x 430 front elevation used as the plan's card image.
// build-plans.php writes both to assets/plans/.

const SVG_BG = '#0d3c48', SVG_LINE = '#e8f2f2', SVG_TXT = '#cfe3e3', SVG_ACC = '#f2c58d', SVG_AQUA = '#9fe0dc';

function svg_fmt(float $v): string { return rtrim(rtrim(number_format($v, 2, '.', ''), '0'), '.'); }

function svg_ft(float $v): string {
    $f = (int)floor($v + 1e-9); $in = (int)round(($v - $f) * 12);
    if ($in === 12) { $f++; $in = 0; }
    return $in ? "$f'-$in\"" : "$f'-0\"";
}

function svg_text(float $x, float $y, string $t, float $size, string $fill = SVG_TXT, string $extra = ''): string {
    return sprintf('<text x="%s" y="%s" font-size="%s" fill="%s"%s>%s</text>', svg_fmt($x), svg_fmt($y), svg_fmt($size), $fill, $extra, htmlspecialchars($t, ENT_QUOTES | ENT_XML1));
}

function svg_open(float $w, float $h, string $title): string {
    $id = 'g' . substr(md5($title), 0, 6);
    return sprintf('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" aria-label="%s" font-family="Inter, Helvetica, Arial, sans-serif" text-anchor="middle">',
            svg_fmt($w), svg_fmt($h), svg_fmt($w), svg_fmt($h), htmlspecialchars($title, ENT_QUOTES | ENT_XML1))
        . "<title>" . htmlspecialchars($title, ENT_QUOTES | ENT_XML1) . "</title>"
        . "<defs><pattern id=\"$id\" width=\"24\" height=\"24\" patternUnits=\"userSpaceOnUse\"><path d=\"M24 0H0V24\" fill=\"none\" stroke=\"#ffffff\" stroke-opacity=\".06\"/></pattern></defs>"
        . sprintf('<rect width="%s" height="%s" fill="%s"/><rect width="%s" height="%s" fill="url(#%s)"/>', svg_fmt($w), svg_fmt($h), SVG_BG, svg_fmt($w), svg_fmt($h), $id);
}

// Horizontal or vertical dimension line with ticks and a centered label.
function svg_dim(float $x1, float $y1, float $x2, float $y2, string $label): string {
    $o = sprintf('<g stroke="%s" stroke-width="1"><line x1="%s" y1="%s" x2="%s" y2="%s"/>', SVG_AQUA, svg_fmt($x1), svg_fmt($y1), svg_fmt($x2), svg_fmt($y2));
    if ($y1 == $y2) {
        $o .= sprintf('<line x1="%1$s" y1="%2$s" x2="%1$s" y2="%3$s"/><line x1="%4$s" y1="%2$s" x2="%4$s" y2="%3$s"/></g>', svg_fmt($x1), svg_fmt($y1 - 6), svg_fmt($y1 + 6), svg_fmt($x2));
        $o .= svg_text(($x1 + $x2) / 2, $y1 - 8, $label, 12, SVG_AQUA);
    } else {
        $o .= sprintf('<line x1="%2$s" y1="%1$s" x2="%3$s" y2="%1$s"/><line x1="%2$s" y1="%4$s" x2="%3$s" y2="%4$s"/></g>', svg_fmt($y1), svg_fmt($x1 - 6), svg_fmt($x1 + 6), svg_fmt($y2));
        $cy = ($y1 + $y2) / 2;
        $o .= svg_text($x1 + 16, $cy, $label, 12, SVG_AQUA, sprintf(' transform="rotate(90 %s %s)"', svg_fmt($x1 + 16), svg_fmt($cy)));
    }
    return $o;
}

// Fit a label inside a box: returns font size, or 0 if it cannot fit legibly.
function svg_fit(string $t, float $boxW, float $max = 13): float {
    $fs = min($max, ($boxW - 6) / max(1, strlen($t) * 0.64));
    return $fs >= 6.5 ? $fs : 0;
}

function plan_floor_svg(array $p): string {
    $W = $p['W']; $D = $p['D'];
    $porch = $p['porch'] ?? null;
    // Extent of drawing in feet, including a porch outside the footprint.
    $minX = 0; $minY = 0; $maxX = $W; $maxY = $D;
    if ($porch) { $minX = min($minX, $porch[0]); $minY = min($minY, $porch[1]); $maxX = max($maxX, $porch[0] + $porch[2]); $maxY = max($maxY, $porch[1] + $porch[3]); }
    $s = min(28, 820 / ($maxX - $minX), 460 / ($maxY - $minY));   // px per foot
    $padL = 40; $padT = 56; $padR = 56; $padB = 56;
    $ox = $padL - $minX * $s; $oy = $padT - $minY * $s;
    $vw = $padL + ($maxX - $minX) * $s + $padR; $vh = $padT + ($maxY - $minY) * $s + $padB;
    $X = function ($ft) use ($ox, $s) { return $ox + $ft * $s; };
    $Y = function ($ft) use ($oy, $s) { return $oy + $ft * $s; };

    $o = svg_open($vw, $vh, $p['name'] . ' floor plan, ' . $p['width'] . ' x ' . $p['depth'] . ', ' . number_format($p['sqft']) . ' sq ft');
    if ($porch) {
        [$px, $py, $pw, $pd] = $porch;
        $o .= sprintf('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"/>', svg_fmt($X($px)), svg_fmt($Y($py)), svg_fmt($pw * $s), svg_fmt($pd * $s), SVG_ACC);
        $lbl = (strpos($p['roof_type'] ?? '', 'aframe') !== false) ? 'DECK' : 'COVERED PORCH';
        $fs = svg_fit($lbl, $pw * $s, 12) ?: svg_fit('PORCH', $pw * $s, 12);
        if ($fs) $o .= svg_text($X($px + $pw / 2), $Y($py + $pd / 2) + 4, $fs < 7 ? 'PORCH' : $lbl, $fs, SVG_ACC);
    }
    // Loft labels sit along the top of each loft outline; room labels move out of their way.
    $bands = [];
    foreach ($p['loft'] ?? [] as [$label, $x, $y, $w, $d]) {
        $t = $label . ' ABOVE (' . (int)round($w * $d) . ' SF)';
        $fs = svg_fit($t, $w * $s - 8, 10);
        if (!$fs) { $t = $label . ' ABOVE'; $fs = svg_fit($t, $w * $s - 8, 10); }
        if ($fs) $bands[] = ['t' => $t, 'fs' => $fs, 'x1' => $X($x), 'x2' => $X($x + $w), 'y1' => $Y($y) + 4, 'y2' => $Y($y) + 6 + $fs + 8, 'cx' => $X($x + $w / 2), 'ty' => $Y($y) + 6 + $fs + 3];
    }
    $lab = '';
    foreach ($p['rooms'] as [$label, $x, $y, $w, $d]) {
        $o .= sprintf('<rect x="%s" y="%s" width="%s" height="%s" fill="#ffffff" fill-opacity=".03" stroke="%s" stroke-width="1.6"/>', svg_fmt($X($x)), svg_fmt($Y($y)), svg_fmt($w * $s), svg_fmt($d * $s), SVG_LINE);
        $cx = $X($x + $w / 2); $cy = $Y($y + $d / 2);
        $words = [$label];
        $fs = svg_fit($label, $w * $s);
        if (!$fs && strpos($label, ' ') !== false) {   // try two lines
            $words = preg_split('/\s+(?=\S+$)|\s+\/\s+|\s+\+\s+/', $label, 2);
            $fs = min(svg_fit($words[0], $w * $s), svg_fit($words[1] ?? '', $w * $s));
        }
        if (!$fs) continue;
        $dims = svg_ft($w) . ' x ' . svg_ft($d);
        $lines = count($words);
        $showDims = $d * $s >= ($lines + 1) * ($fs + 4) + 6 && svg_fit($dims, $w * $s, 10);
        $total = $lines * ($fs + 3) + ($showDims ? 12 : 0);
        $top = $cy - $total / 2;
        foreach ($bands as $bd) {
            if ($X($x + $w) <= $bd['x1'] || $X($x) >= $bd['x2']) continue;
            if ($top < $bd['y2'] && $top + $total > $bd['y1']) $top = max($top, $bd['y2'] + 4);
        }
        if ($top + $total > $Y($y + $d) - 2) {           // no room below the band: drop the size line
            $showDims = false; $total = $lines * ($fs + 3);
            $top = min($top, $Y($y + $d) - $total - 2);
        }
        $ty = $top + $fs;
        foreach ($words as $wd) { $lab .= svg_text($cx, $ty, $wd, $fs, SVG_TXT, ' font-weight="600"'); $ty += $fs + 3; }
        if ($showDims) $lab .= svg_text($cx, $ty + 8, $dims, min(10, svg_fit($dims, $w * $s, 10)), SVG_AQUA);
    }
    // Exterior walls drawn last so they sit over the room outlines.
    $o .= sprintf('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="5"/>', svg_fmt($X(0)), svg_fmt($Y(0)), svg_fmt($W * $s), svg_fmt($D * $s), SVG_LINE);
    foreach ($p['loft'] ?? [] as [$label, $x, $y, $w, $d]) {
        $o .= sprintf('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" fill-opacity=".08" stroke="%s" stroke-width="1.5" stroke-dasharray="3 4"/>', svg_fmt($X($x) + 3), svg_fmt($Y($y) + 3), svg_fmt($w * $s - 6), svg_fmt($d * $s - 6), SVG_AQUA, SVG_AQUA);
    }
    $o .= '<g stroke="' . SVG_BG . '" stroke-width="4" paint-order="stroke" stroke-linejoin="round">' . $lab;
    foreach ($bands as $bd) $o .= svg_text($bd['cx'], $bd['ty'], $bd['t'], $bd['fs'], SVG_AQUA, ' font-weight="600"');
    $o .= '</g>';
    $o .= svg_dim($X(0), $Y($minY) - 22, $X($W), $Y($minY) - 22, svg_ft($W));
    $o .= svg_dim($X($maxX) + 22, $Y(0), $X($maxX) + 22, $Y($D), svg_ft($D));
    $o .= svg_text($vw / 2, $vh - 18, strtoupper($p['name']) . '  ·  MAIN FLOOR ' . number_format($p['main_sqft']) . ' SF' . ($p['loft_sqft'] ? '  ·  LOFT ' . $p['loft_sqft'] . ' SF' : ''), 12, SVG_ACC, ' font-weight="600" letter-spacing="1"');
    return $o . '</svg>';
}

function plan_elevation_svg(array $p): string {
    $type = $p['roof_type'] ?? 'gable';
    $VW = 800; $VH = 430; $ground = 360;
    $W = $p['W']; $D = $p['D'];
    $end = in_array($type, ['aframe', 'gambrel'], true);   // drawn from the gable end
    $len = $end ? $D : $W;
    $porch = $p['porch'] ?? null;
    $sidePorch = $porch && $porch[0] >= $W ? $porch[2] : 0;
    $mobile = in_array($type, ['thow', 'shed-thow', 'gooseneck'], true);
    $base = $mobile ? 2.2 : 1.2;                            // trailer deck / foundation height in ft
    $wall = ['thow' => 9.5, 'shed-thow' => 10.5, 'gooseneck' => 9.5, 'container' => 9.5, 'container-double' => 9.5, 'shed' => 9, 'gable' => 9, 'gable-steep' => 9][$type] ?? 9;
    $roofH = ['thow' => 1.8, 'gooseneck' => 1.8, 'shed-thow' => 0.6, 'container' => 0, 'container-double' => 1.6, 'shed' => 1.6,
              'gable' => $D / 2 * 0.5, 'gable-steep' => $D / 2 * 0.95, 'aframe' => $D * 1.15, 'gambrel' => $D * 0.62][$type] ?? 3;
    $totalH = $base + ($end ? $roofH + ($type === 'gambrel' ? 6.5 : 0) : $wall + $roofH);
    $s = min(560 / ($len + $sidePorch + 2), 290 / $totalH);
    $x0 = ($VW - ($len + $sidePorch) * $s) / 2;
    $X = function ($ft) use ($x0, $s) { return $x0 + $ft * $s; };
    $Y = function ($ft) use ($ground, $s) { return $ground - $ft * $s; };
    $line = SVG_LINE; $acc = SVG_ACC;
    $poly = function (array $pts, string $stroke, float $sw = 2, string $fill = 'none', string $extra = '') {
        return sprintf('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>', implode(' ', array_map(function ($q) { return svg_fmt($q[0]) . ',' . svg_fmt($q[1]); }, $pts)), $fill, $stroke, svg_fmt($sw), $extra);
    };
    $rect = function ($x, $y, $w, $h, $stroke, $sw = 1.5, $fill = 'none', $extra = '') {
        return sprintf('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>', svg_fmt($x), svg_fmt($y), svg_fmt($w), svg_fmt($h), $fill, $stroke, svg_fmt($sw), $extra);
    };
    $window = function ($fx, $fy, $fw, $fh) use ($X, $Y, $s, $rect) {
        $o = $rect($X($fx), $Y($fy + $fh), $fw * $s, $fh * $s, SVG_LINE, 1.5, '#9fe0dc', ' fill-opacity=".18"');
        return $o . sprintf('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1"/>', svg_fmt($X($fx + $fw / 2)), svg_fmt($Y($fy + $fh)), svg_fmt($X($fx + $fw / 2)), svg_fmt($Y($fy)), SVG_LINE);
    };
    $door = function ($fx, $fy, $fw = 3, $fh = 6.8, $glass = false) use ($X, $Y, $s, $rect) {
        $o = $rect($X($fx), $Y($fy + $fh), $fw * $s, $fh * $s, SVG_ACC, 2, $glass ? '#9fe0dc' : 'none', $glass ? ' fill-opacity=".15"' : '');
        return $o . sprintf('<circle cx="%s" cy="%s" r="2" fill="%s"/>', svg_fmt($X($fx + $fw - 0.4)), svg_fmt($Y($fy + 3.4)), SVG_ACC);
    };

    $o = svg_open($VW, $VH, $p['name'] . ' front elevation: ' . $p['title']);
    $o .= sprintf('<line x1="30" y1="%1$s" x2="770" y2="%1$s" stroke="%2$s" stroke-width="2"/>', $ground, SVG_AQUA);

    if ($end) {
        // Gable-end view: A-frame triangle or gambrel barn profile.
        $L = $X(0); $R = $X($len); $B = $Y($base); $mid = $X($len / 2);
        $o .= $rect($L - 4, $B, ($R - $L) + 8, $base * $s, $line, 1.5);
        if ($type === 'aframe') {
            $top = $Y($base + $roofH);
            $o .= $poly([[$L - 0.8 * $s, $B], [$mid, $top - 0.6 * $s], [$R + 0.8 * $s, $B]], $line, 3);
            $o .= $poly([[$L + 1.4 * $s, $B], [$mid, $top + 1.6 * $s], [$R - 1.4 * $s, $B]], $line, 1.5);
            for ($i = 1; $i < 5; $i++) { $yy = $B - ($B - $top - 1.6 * $s) * $i / 5; $hw = ($R - $L - 2.8 * $s) / 2 * (1 - $i / 5);
                $o .= sprintf('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="1"/>', svg_fmt($mid - $hw), svg_fmt($yy), svg_fmt($mid + $hw), svg_fmt($yy), $line); }
            $o .= sprintf('<line x1="%1$s" y1="%2$s" x2="%1$s" y2="%3$s" stroke="%4$s" stroke-width="1"/>', svg_fmt($mid), svg_fmt($B), svg_fmt($top + 1.6 * $s), $line);
            $o .= $door($len / 2 - 3, $base, 6, 7, true);
            if ($porch) $o .= $rect($X(-1), $B - 0.25 * $s, ($len + 2) * $s, 0.5 * $s, $acc, 1.5);
        } else { // gambrel
            $wallH = 6.5; $eave = $Y($base + $wallH); $knee = $Y($base + $wallH + $roofH * 0.55); $peak = $Y($base + $wallH + $roofH);
            $o .= $poly([[$L, $B], [$L, $eave], [$L + $len * 0.16 * $s, $knee], [$mid, $peak], [$R - $len * 0.16 * $s, $knee], [$R, $eave], [$R, $B]], $line, 3);
            $o .= $door($len / 2 - 3, $base, 3, 6.5) . $door($len / 2, $base, 3, 6.5);
            $o .= $window($len / 2 - 1.5, $base + $wallH + 1, 3, 2.4);
            $o .= $window(1, $base + 3, 2, 2.5) . $window($len - 3, $base + 3, 2, 2.5);
        }
    } else {
        // Long-side view.
        $L = $X(0); $R = $X($len); $B = $Y($base); $T = $Y($base + $wall);
        if ($mobile) {
            $o .= $rect($L - 0.3 * $s, $Y($base), ($len + 0.6) * $s, 0.6 * $s, $line, 1.5);
            $axle = $len * 0.58;
            foreach ([$axle - 1.6, $axle + 1.6] as $wx) $o .= sprintf('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="2"/><circle cx="%1$s" cy="%2$s" r="%6$s" fill="none" stroke="%5$s"/>', svg_fmt($X($wx)), svg_fmt($Y(1.15)), svg_fmt(1.15 * $s), SVG_BG, $line, svg_fmt(0.5 * $s));
            if ($type === 'gooseneck') $o .= $poly([[$X($len), $Y($base + 0.6)], [$X($len + 3), $Y($base + 0.6)], [$X($len + 3), $Y($base + 2.2)], [$X($len), $Y($base + 2.2)]], $line, 1.5);
            else $o .= sprintf('<path d="M%s %s L%s %s" stroke="%s" stroke-width="2"/>', svg_fmt($L), svg_fmt($Y($base - 0.3)), svg_fmt($X(-3)), svg_fmt($Y(1.4)), $line);
        } else {
            $o .= $rect($L - 2, $B, ($R - $L) + 4, $base * $s, $line, 1.5);
        }
        if ($type === 'gooseneck') {
            $o .= $poly([[$L, $B], [$L, $T], [$X($len - 8), $T], [$X($len - 8), $Y($base + $wall + 0.01)], [$R, $Y($base + $wall)], [$R, $Y($base + 2.6)], [$X($len - 8), $Y($base + 2.6)], [$X($len - 8), $B]], $line, 3);
        } elseif (strpos($type, 'container') === 0) {
            $o .= $rect($L, $T, $len * $s, $wall * $s, $line, 3);
            for ($cx = 0.5; $cx < $len; $cx += 1) $o .= sprintf('<line x1="%1$s" y1="%2$s" x2="%1$s" y2="%3$s" stroke="%4$s" stroke-opacity=".35" stroke-width="1"/>', svg_fmt($X($cx)), svg_fmt($T + 3), svg_fmt($B - 3), $line);
        } else {
            $o .= $rect($L, $T, $len * $s, $wall * $s, $line, 3);
        }
        // Roof
        if ($roofH > 0) {
            $ov = 1.2; $rt = $Y($base + $wall + $roofH);
            if (in_array($type, ['shed', 'shed-thow', 'container-double'], true)) {
                $o .= $poly([[$X(-$ov), $T], [$X(-$ov), $T - 0.5 * $s], [$X($len + $ov), $rt], [$X($len + $ov), $T]], $line, 2.5);
                if ($type !== 'container-double') for ($cx = 2; $cx < $len - 2; $cx += 4) $o .= $window($cx, $base + $wall - 1.6, 2.6, 1.2);
            } else {
                $o .= $poly([[$X(-$ov), $T], [$X(0.6), $rt], [$X($len - 0.6), $rt], [$X($len + $ov), $T]], $line, 2.5);
                for ($cx = 1; $cx < $len; $cx += 1.5) $o .= sprintf('<line x1="%1$s" y1="%2$s" x2="%3$s" y2="%4$s" stroke="%5$s" stroke-opacity=".3"/>', svg_fmt($X($cx)), svg_fmt($T - 1), svg_fmt($X($cx)), svg_fmt($rt + 1), $line);
            }
        }
        // Front porch roof and posts
        if ($porch && $porch[1] < 0) {
            $pl = max(0, $porch[0]); $pr = min($len, $porch[0] + $porch[2]);
            $pt = $Y($base + 8.2);
            $o .= $poly([[$X($pl - 0.6), $pt], [$X($pl - 0.6), $pt - 1.1 * $s], [$X($pr + 0.6), $pt - 1.1 * $s], [$X($pr + 0.6), $pt]], $acc, 2, SVG_BG);
            $n = max(2, (int)round(($pr - $pl) / 8) + 1);
            for ($i = 0; $i < $n; $i++) { $px = $pl + 0.3 + ($pr - $pl - 0.6) * $i / ($n - 1);
                $o .= sprintf('<line x1="%1$s" y1="%2$s" x2="%1$s" y2="%3$s" stroke="%4$s" stroke-width="3"/>', svg_fmt($X($px)), svg_fmt($pt), svg_fmt($B), $acc); }
        }
        if ($sidePorch) {
            $pt = $Y($base + 8.2);
            $o .= $poly([[$R, $pt - 0.8 * $s], [$X($len + $sidePorch + 0.6), $pt - 0.2 * $s], [$X($len + $sidePorch + 0.6), $pt + 0.4 * $s], [$R, $pt + 0.4 * $s - 0.4 * $s]], $acc, 2, SVG_BG);
            foreach ([$len + $sidePorch - 0.3] as $px) $o .= sprintf('<line x1="%1$s" y1="%2$s" x2="%1$s" y2="%3$s" stroke="%4$s" stroke-width="3"/>', svg_fmt($X($px)), svg_fmt($pt), svg_fmt($B), $acc);
            $o .= $rect($R, $B - 0.3 * $s, $sidePorch * $s, 0.3 * $s, $acc, 1.5);
        }
        // Door and windows along the wall
        $doorX = $porch && $porch[1] < 0 ? max($porch[0] + 1.5, min($porch[0] + $porch[2] - 4.5, $porch[0] + $porch[2] / 2 - 1.5)) : min(3, $len * 0.15);
        if (strpos($type, 'container') === 0) $doorX = $len - 6.5;
        $glass = strpos($type, 'container') === 0;
        $o .= $door($doorX, $base, $glass ? 5.5 : 3, $glass ? 7.5 : 6.8, $glass);
        $limit = $type === 'gooseneck' ? $len - 9 : $len - 1;
        for ($wx = 1.5; $wx + 3 <= $limit; $wx += 5.5) {
            if ($wx + 3 > $doorX - 0.8 && $wx < $doorX + ($glass ? 6.3 : 3.8)) continue;
            $o .= $window($wx, $base + 3, 3, 4);
        }
        if ($type === 'gooseneck') $o .= $window($len - 6, $base + 3.4, 3, 3);
    }
    $o .= svg_text($VW / 2, 398, strtoupper($p['name']) . '  ·  ' . number_format($p['sqft']) . ' SQ FT  ·  ' . $p['beds'] . ' BED  ·  ' . $p['baths'] . ' BATH', 14, SVG_ACC, ' font-weight="600" letter-spacing="1.5"');
    $o .= svg_text($VW / 2, 418, $end ? 'GABLE END ELEVATION' : 'FRONT ELEVATION', 10, SVG_AQUA, ' letter-spacing="2"');
    return $o . '</svg>';
}
