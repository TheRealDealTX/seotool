<?php
defined('SLT') || exit;

/**
 * Night-time house illustration with four switchable lighting layers:
 *   .lt-arch (architectural), .lt-path, .lt-tree, .lt-patio
 * Light color comes from the CSS custom property --lc on the .scene element,
 * overall brightness from --int.
 */
function house_scene(string $id, bool $sky = true, bool $lit = false, string $fit = 'xMidYMax slice'): string {
    $o = $lit ? '' : ' style="opacity:0"';
    $beam = function (float $x, float $base, float $top, float $spread, float $w = 9) use ($id): string {
        return '<polygon class="beam" points="' . ($x - $w) . ',' . $base . ' ' . ($x + $w) . ',' . $base . ' ' . ($x + $spread) . ',' . $top . ' ' . ($x - $spread) . ',' . $top . '" fill="url(#' . $id . '-beam)"/>'
            . '<rect class="fx" x="' . ($x - 5) . '" y="' . ($base - 4) . '" width="10" height="8" rx="2"/>';
    };
    $pool = function (float $x, float $y, float $rx = 70) use ($id): string {
        return '<ellipse cx="' . $x . '" cy="' . ($y + 4) . '" rx="' . $rx . '" ry="' . ($rx * .26) . '" fill="url(#' . $id . '-pool)"/>'
            . '<rect x="' . ($x - 1.5) . '" y="' . ($y - 26) . '" width="3" height="28" fill="#1d2420"/>'
            . '<path d="M' . ($x - 9) . ',' . ($y - 26) . ' h18 l-4,-7 h-10z" fill="#2a322d"/>'
            . '<ellipse class="fx" cx="' . $x . '" cy="' . ($y - 24) . '" rx="7" ry="2.5"/>'
            . '<ellipse cx="' . $x . '" cy="' . ($y - 20) . '" rx="16" ry="12" fill="url(#' . $id . '-dot)"/>';
    };
    ob_start(); ?>
<svg class="scene-svg" viewBox="0 0 1600 700" preserveAspectRatio="<?= $fit ?>" role="img" aria-label="Illustration of a brick home at night with architectural, path, tree and patio landscape lighting">
  <defs>
    <linearGradient id="<?= $id ?>-beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" style="stop-color:var(--lc,#ffc56b)" stop-opacity="1"/><stop offset=".45" style="stop-color:var(--lc,#ffc56b)" stop-opacity=".45"/><stop offset="1" style="stop-color:var(--lc,#ffc56b)" stop-opacity="0"/></linearGradient>
    <radialGradient id="<?= $id ?>-pool"><stop offset="0" style="stop-color:var(--lc,#ffc56b)" stop-opacity=".85"/><stop offset=".5" style="stop-color:var(--lc,#ffc56b)" stop-opacity=".25"/><stop offset="1" style="stop-color:var(--lc,#ffc56b)" stop-opacity="0"/></radialGradient>
    <radialGradient id="<?= $id ?>-dot"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".3" style="stop-color:var(--lc,#ffc56b)" stop-opacity=".6"/><stop offset="1" style="stop-color:var(--lc,#ffc56b)" stop-opacity="0"/></radialGradient>
    <radialGradient id="<?= $id ?>-wash" cx=".5" cy=".85" r=".75"><stop offset="0" style="stop-color:var(--lc,#ffc56b)" stop-opacity=".38"/><stop offset=".6" style="stop-color:var(--lc,#ffc56b)" stop-opacity=".08"/><stop offset="1" style="stop-color:var(--lc,#ffc56b)" stop-opacity="0"/></radialGradient>
    <radialGradient id="<?= $id ?>-canopy" cx=".5" cy=".75" r=".6"><stop offset="0" style="stop-color:var(--lc,#ffc56b)" stop-opacity=".55"/><stop offset=".7" style="stop-color:var(--lc,#ffc56b)" stop-opacity=".1"/><stop offset="1" style="stop-color:var(--lc,#ffc56b)" stop-opacity="0"/></radialGradient>
    <linearGradient id="<?= $id ?>-lawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1a12"/><stop offset="1" stop-color="#040a07"/></linearGradient>
    <linearGradient id="<?= $id ?>-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#02060a"/><stop offset=".7" stop-color="#0a1820"/><stop offset="1" stop-color="#13261f"/></linearGradient>
    <pattern id="<?= $id ?>-brick" width="40" height="16" patternUnits="userSpaceOnUse"><rect width="40" height="16" fill="#1f1714"/><path d="M0 8h40M0 16h40M20 0v8M0 8v8M40 8v8" stroke="#140f0d" stroke-width="1.4"/></pattern>
    <radialGradient id="<?= $id ?>-moon"><stop offset=".35" stop-color="#f4ecd2" stop-opacity=".25"/><stop offset="1" stop-color="#f4ecd2" stop-opacity="0"/></radialGradient>
    <filter id="<?= $id ?>-blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>
  <?php if ($sky): ?>
  <rect width="1600" height="700" fill="url(#<?= $id ?>-sky)"/>
  <g fill="#fff" opacity=".7"><circle cx="120" cy="60" r="1.2"/><circle cx="340" cy="110" r="1"/><circle cx="560" cy="40" r="1.4"/><circle cx="820" cy="90" r="1"/><circle cx="1040" cy="50" r="1.2"/><circle cx="1260" cy="120" r="1"/><circle cx="1450" cy="70" r="1.5"/><circle cx="700" cy="150" r=".9"/><circle cx="1150" cy="170" r=".9"/><circle cx="40" cy="180" r="1"/></g>
  <circle cx="1300" cy="90" r="30" fill="#f4ecd2" opacity=".9"/><circle cx="1300" cy="90" r="80" fill="url(#<?= $id ?>-moon)"/>
  <?php endif; ?>
  <!-- distant tree line -->
  <path d="M0,470 C60,420 110,440 160,410 C220,380 260,430 330,400 C400,370 430,420 500,410 L500,520 L0,520Z M1100,520 L1100,420 C1160,380 1200,410 1260,380 C1320,350 1360,400 1420,370 C1480,345 1540,390 1600,360 L1600,520Z" fill="#06100b"/>
  <!-- lawn -->
  <rect y="515" width="1600" height="185" fill="url(#<?= $id ?>-lawn)"/>

  <!-- house -->
  <g class="house">
    <rect x="540" y="285" width="220" height="235" fill="url(#<?= $id ?>-brick)"/>
    <polygon points="520,292 650,172 780,292" fill="#0e1311"/>
    <polygon points="540,292 650,190 760,292" fill="#191512"/>
    <rect x="760" y="330" width="240" height="190" fill="url(#<?= $id ?>-brick)"/>
    <polygon points="740,334 800,252 1000,252 1042,334" fill="#0e1311"/>
    <rect x="1000" y="384" width="180" height="136" fill="url(#<?= $id ?>-brick)"/>
    <polygon points="985,392 1040,332 1180,332 1196,392" fill="#0e1311"/>
    <rect x="1024" y="420" width="132" height="100" fill="#141917" stroke="#0b0e0d" stroke-width="2"/>
    <path d="M1024 445h132M1024 470h132M1024 495h132" stroke="#0d1110" stroke-width="2"/>
    <!-- chimney -->
    <rect x="890" y="210" width="34" height="60" fill="#1b1512"/>
    <!-- windows -->
    <g class="win-g">
      <rect class="win" x="575" y="318" width="50" height="58" rx="2"/><rect class="win" x="675" y="318" width="50" height="58" rx="2"/>
      <rect class="win" x="575" y="418" width="50" height="62" rx="2"/><rect class="win" x="675" y="418" width="50" height="62" rx="2"/>
      <rect class="win" x="775" y="420" width="40" height="58" rx="2"/><rect class="win" x="952" y="420" width="40" height="58" rx="2"/>
      <path d="M600 318v58M575 347h50M700 318v58M675 347h50M600 418v62M575 449h50M700 418v62M675 449h50M795 420v58M775 449h40M972 420v58M952 449h40" stroke="#0b0e0d" stroke-width="3"/>
    </g>
    <!-- entry -->
    <path d="M858 520v-82a24 24 0 0 1 48 0v82z" fill="#2a1d14"/>
    <circle cx="896" cy="482" r="2.5" fill="#c9a36a"/>
    <polygon points="815,398 882,350 950,398" fill="#0e1311"/>
    <rect x="826" y="398" width="13" height="122" fill="#2a2724"/><rect x="926" y="398" width="13" height="122" fill="#2a2724"/>
    <!-- foundation shrubs -->
    <g fill="#0a1710"><ellipse cx="575" cy="515" rx="42" ry="20"/><ellipse cx="640" cy="518" rx="34" ry="16"/><ellipse cx="715" cy="515" rx="44" ry="21"/><ellipse cx="795" cy="518" rx="30" ry="15"/><ellipse cx="975" cy="518" rx="32" ry="15"/></g>
  </g>

  <!-- driveway + walkway -->
  <polygon points="1024,520 1156,520 1340,700 990,700" fill="#121715"/>
  <path d="M860,520 C852,585 765,622 690,700 L790,700 C850,632 908,585 906,520 Z" fill="#1a1e1b"/>

  <!-- live oak -->
  <g class="tree oak">
    <path d="M250,520 C246,470 240,430 220,395 C205,370 170,350 140,345 M250,470 C262,430 290,400 340,380 C370,368 400,370 420,360 M246,440 C250,400 255,370 268,345" stroke="#0f0d0b" stroke-width="18" fill="none" stroke-linecap="round"/>
    <path d="M250,520 L250,440" stroke="#0f0d0b" stroke-width="30"/>
    <g fill="#08130d"><ellipse cx="170" cy="320" rx="110" ry="62"/><ellipse cx="270" cy="285" rx="130" ry="80"/><ellipse cx="370" cy="325" rx="110" ry="60"/><ellipse cx="225" cy="350" rx="90" ry="40"/><ellipse cx="330" cy="355" rx="80" ry="36"/></g>
  </g>
  <!-- crape myrtle -->
  <g class="tree crape">
    <path d="M470,520 C468,480 455,450 445,425 M470,520 C474,478 488,450 498,425 M470,515 L470,430" stroke="#2a2420" stroke-width="5" fill="none"/>
    <g fill="#0a1510"><ellipse cx="470" cy="405" rx="58" ry="40"/><ellipse cx="440" cy="420" rx="34" ry="24"/><ellipse cx="500" cy="420" rx="34" ry="24"/></g>
  </g>
  <!-- pine -->
  <g class="tree pine">
    <rect x="1494" y="150" width="11" height="372" fill="#100d0b"/>
    <g fill="#07120c"><ellipse cx="1500" cy="160" rx="62" ry="40"/><ellipse cx="1470" cy="210" rx="46" ry="26"/><ellipse cx="1530" cy="240" rx="50" ry="26"/><ellipse cx="1490" cy="120" rx="40" ry="28"/></g>
  </g>
  <!-- pergola + patio -->
  <g class="patio">
    <polygon points="1205,520 1440,520 1470,565 1180,565" fill="#16130f"/>
    <rect x="1225" y="408" width="10" height="135" fill="#1f1a15"/><rect x="1415" y="408" width="10" height="135" fill="#1f1a15"/>
    <rect x="1212" y="400" width="226" height="10" fill="#241e18"/>
    <path d="M1240 400v-8M1270 400v-8M1300 400v-8M1330 400v-8M1360 400v-8M1390 400v-8" stroke="#241e18" stroke-width="6"/>
    <rect x="1290" y="505" width="70" height="6" fill="#2a231c"/><rect x="1300" y="511" width="5" height="26" fill="#2a231c"/><rect x="1345" y="511" width="5" height="26" fill="#2a231c"/>
    <rect x="1262" y="500" width="18" height="38" rx="3" fill="#1d1813"/><rect x="1370" y="500" width="18" height="38" rx="3" fill="#1d1813"/>
  </g>

  <!-- ===== LIGHT LAYERS ===== -->
  <g class="lights">
    <g class="lt lt-arch"<?= $o ?>>
      <ellipse cx="650" cy="420" rx="150" ry="140" fill="url(#<?= $id ?>-wash)"/>
      <ellipse cx="880" cy="430" rx="140" ry="110" fill="url(#<?= $id ?>-wash)"/>
      <ellipse cx="1090" cy="440" rx="110" ry="90" fill="url(#<?= $id ?>-wash)"/>
      <?= $beam(553, 518, 300, 34) ?><?= $beam(650, 518, 250, 46) ?><?= $beam(747, 518, 300, 34) ?>
      <?= $beam(832, 518, 380, 16, 5) ?><?= $beam(932, 518, 380, 16, 5) ?><?= $beam(1010, 518, 380, 28) ?><?= $beam(1172, 518, 380, 26) ?>
    </g>
    <g class="lt lt-path"<?= $o ?>>
      <?= $pool(838, 565, 60) ?><?= $pool(935, 580, 62) ?><?= $pool(770, 625, 70) ?><?= $pool(868, 650, 70) ?><?= $pool(690, 685, 78) ?>
      <?= $pool(1010, 600, 64) ?><?= $pool(1210, 640, 70) ?>
    </g>
    <g class="lt lt-tree"<?= $o ?>>
      <ellipse cx="265" cy="320" rx="230" ry="120" fill="url(#<?= $id ?>-canopy)"/>
      <ellipse cx="470" cy="410" rx="80" ry="58" fill="url(#<?= $id ?>-canopy)"/>
      <ellipse cx="1500" cy="190" rx="90" ry="140" fill="url(#<?= $id ?>-canopy)"/>
      <?= $beam(190, 520, 300, 70) ?><?= $beam(250, 524, 260, 60) ?><?= $beam(330, 520, 310, 70) ?>
      <?= $beam(470, 520, 380, 40) ?><?= $beam(1480, 520, 130, 30) ?>
    </g>
    <g class="lt lt-patio"<?= $o ?>>
      <ellipse cx="1325" cy="540" rx="170" ry="40" fill="url(#<?= $id ?>-pool)"/>
      <ellipse cx="1325" cy="440" rx="140" ry="70" fill="url(#<?= $id ?>-wash)"/>
      <path d="M1230 420 Q1280 452 1325 440 Q1372 452 1420 420" stroke="#3a3328" stroke-width="1.5" fill="none"/>
      <g class="fx"><?php foreach ([[1245, 430], [1265, 439], [1285, 444], [1305, 443], [1325, 440], [1345, 443], [1365, 444], [1385, 439], [1405, 430]] as [$bx, $by]) echo '<circle cx="' . $bx . '" cy="' . $by . '" r="3.2"/><circle cx="' . $bx . '" cy="' . $by . '" r="11" fill="url(#' . $id . '-dot)"/>'; ?></g>
    </g>
  </g>
</svg>
<?php
    return ob_get_clean();
}
