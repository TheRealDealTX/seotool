<?php defined('APP') || exit;

// "Boston" / "Boston, MA" searches jump straight to the city page
$q = get('q');
if ($q !== '' && count($_GET) <= 4) {
    $needle = strtolower(trim(preg_replace('/\s*,\s*([a-z]{2})$/i', '|$1', $q)));
    [$cname, $cst] = array_pad(explode('|', $needle), 2, null);
    $hits = [];
    foreach (known_cities() as $k => $c) {
        if (strtolower($c['name']) === trim($cname) && (!$cst || strtolower($c['state']) === $cst)) $hits[] = $k;
    }
    if (count($hits) === 1) {
        [$st, $slug] = explode('/', $hits[0]);
        $keep = array_intersect_key($_GET, ['from' => 1, 'max' => 1, 'to' => 1]);
        $keep = array_filter($keep, fn($v) => is_string($v) && $v !== '');
        redirect(city_url($st, $slug) . ($keep ? '?' . http_build_query($keep) : ''), 302);
    }
}

cache_public();
$dir = directory_section([], '/sublets/', [39.5, -98.35, 4], [], null, true);
$states = states();
$byState = [];
foreach (known_cities() as $k => $c) $byState[strtoupper(explode('/', $k)[0])][] = [$k, $c];
$crumbs = [['The Sublet', '/'], ['Sublets', '/sublets/']];

ob_start(); ?>
<div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <header class="page-head">
    <h1>Sublets &amp; short-term rentals across the US</h1>
    <p class="lead">Furnished rooms, apartments and homes for one to twelve months, posted by real hosts on The Sublet. Filter by budget, dates, type and pets — or switch to the map.</p>
  </header>
  <?= $dir['html'] ?>

  <section class="section" id="states">
    <h2>Browse sublets by state</h2>
    <div class="state-grid">
      <?php foreach ($states as $code => $name): $has = !empty($byState[$code]); ?>
        <div class="state-col">
          <a class="state-link<?= $has ? '' : ' is-quiet' ?>" href="<?= e(state_url($code)) ?>"><?= e($name) ?></a>
          <?php if ($has): ?><span class="small muted"><?php echo implode(', ', array_map(fn($x) => '<a href="' . e(city_url(...explode('/', $x[0]))) . '">' . e($x[1]['name']) . '</a>', array_slice($byState[$code], 0, 4))); ?></span><?php endif; ?>
        </div>
      <?php endforeach; ?>
    </div>
  </section>
</div>
<?php
$body = ob_get_clean();
page([
    'title' => 'Sublets & Short-Term Rentals Nationwide | The Sublet',
    'description' => 'Browse furnished sublets and 1–12 month rentals across the US on The Sublet. Filter by price, dates, room type and pets, or view them on a map.',
    'canonical' => '/sublets/',
    'robots' => $dir['filtered'] ? 'noindex, follow' : 'index, follow',
    'body' => $body,
    'h_extra' => leaflet_head(),
    'schema' => array_values(array_filter([schema_breadcrumbs($crumbs), schema_itemlist($dir['cards'], 'Sublets on The Sublet')])),
]);
