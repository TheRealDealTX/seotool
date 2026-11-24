<?php defined('APP') || exit;

$st = strtolower($params[0]);
$slug = $params[1];
$filterKey = $params[2] ?? null;
if (!isset(states()[strtoupper($st)])) not_found();
$filters = city_filters();
if ($filterKey !== null && !isset($filters[$filterKey])) not_found();

$guide = city_guide($st, $slug);
$known = known_cities($st)[$st . '/' . $slug] ?? null;
if (!$guide && !$known) {
    // A city nobody has listed in yet and we have no guide for.
    http_response_code(404);
    cache_public();
    $name = ucwords(str_replace('-', ' ', $slug));
    page([
        'title' => 'Sublets in ' . $name . ', ' . strtoupper($st) . ' | The Sublet',
        'robots' => 'noindex, follow',
        'body' => '<div class="wrap narrow section"><h1>No sublets in ' . e($name) . ' yet</h1><p>Be the first to list a furnished room or apartment in ' . e($name) . ', ' . e(state_name($st)) . ' on The Sublet.</p><p><a class="btn" href="/post-a-sublet/">List your place</a> <a class="btn btn-ghost" href="' . e(state_url($st)) . '">Other cities in ' . e(state_name($st)) . '</a></p></div>',
    ]);
    exit;
}
cache_public();
$name = $guide['name'] ?? $known['name'];
$stateName = state_name($st);
$base = city_url($st, $slug);
$preset = $filterKey ? $filters[$filterKey]['where'] : [];
$path = $base . ($filterKey ? $filterKey . '/' : '');
$center = $guide ? [(float)$guide['lat'], (float)$guide['lng'], 12] : null;
$dir = directory_section(['state' => $st, 'city' => $slug], $path, $center, $preset,
    '<h3>Be the first to list ' . ($filterKey ? strtolower(e($filters[$filterKey]['label'])) . ' ' : 'a sublet ') . 'in ' . e($name) . '</h3>'
    . '<p>There are no ' . ($filterKey ? 'matching ' : '') . 'listings here right now — The Sublet only shows places posted by real hosts. Have a furnished room or apartment free for a month or more?</p>'
    . '<p><a class="btn" href="/post-a-sublet/?city=' . e(rawurlencode($name)) . '&amp;state=' . e(strtoupper($st)) . '">List your place in ' . e($name) . '</a></p>');

$h1 = $filterKey ? $filters[$filterKey]['label'] . ' in ' . $name . ', ' . strtoupper($st) : 'Sublets in ' . $name . ', ' . strtoupper($st);
$crumbs = [['The Sublet', '/'], ['Sublets', '/sublets/'], [$stateName, state_url($st)], [$name, $base]];
if ($filterKey) $crumbs[] = [$filters[$filterKey]['short'], $path];

$faqs = $guide['faqs'] ?? [];
if (!$filterKey) {
    $faqs[] = ['q' => 'How do I list my ' . $name . ' sublet on The Sublet?', 'a' => 'Use the “List your place” form. Free listings are reviewed before publishing and keep your email private behind a contact relay; a one-time ' . price_label() . ' verified listing goes live instantly with your contact details and a Verified host badge.'];
}
// Index filtered pages only when they have listings (avoids thin duplicates).
$indexable = !$dir['filtered'] && ($filterKey ? $dir['total'] > 0 : ($guide || $dir['total'] > 0));
$tips = $guide['tips'] ?? [];
$tipLabels = ['interns' => ['💼', 'For interns'], 'nurses' => ['🩺', 'For travel nurses'], 'students' => ['🎓', 'For students'], 'seasonal' => ['📅', 'When demand peaks']];

$cp = photo('city.' . $st . '/' . $slug);
ob_start(); ?>
<section class="page-hero city-hero"<?= $cp ? ' style="--hero:url(\'' . e($cp['file']) . '\')"' : '' ?>>
  <div class="page-hero-bg" aria-hidden="true"></div>
  <div class="wrap page-hero-inner">
    <?= breadcrumbs_html($crumbs) ?>
    <h1 class="reveal"><?= e($h1) ?></h1>
    <p class="lead reveal"><?= $guide ? e(html_entity_decode($guide['tagline'], ENT_QUOTES, 'UTF-8')) : 'Furnished rooms and apartments for 1–12 month stays in ' . e($name) . ', posted by hosts on The Sublet.' ?></p>
  </div>
  <?php if ($cp && !empty($cp['credit'])): ?><span class="photo-credit">Photo: <?= e(strip_tags($cp['credit'])) ?><?= !empty($cp['license']) ? ' · ' . e($cp['license']) : '' ?></span><?php endif; ?>
</section>
<div class="wrap">
  <nav class="filter-links" aria-label="<?= e($name) ?> sublet types">
    <a href="<?= e($base) ?>"<?= !$filterKey ? ' aria-current="page"' : '' ?>>All</a>
    <?php foreach ($filters as $fk => $fd): ?><a href="<?= e($base . $fk . '/') ?>"<?= $fk === $filterKey ? ' aria-current="page"' : '' ?>><?= e($fd['short']) ?></a><?php endforeach; ?>
  </nav>
  <?= $dir['html'] ?>

  <?php if ($guide && !$filterKey): ?>
  <article class="city-guide">
    <section class="section-sm narrow">
      <h2>Subletting in <?= e($name) ?></h2>
      <?= $guide['intro'] ?>
    </section>
    <?php if (!empty($guide['neighborhoods'])): ?>
    <section class="section-sm">
      <h2>Neighborhoods to know</h2>
      <div class="grid hoods">
        <?php foreach ($guide['neighborhoods'] as $n): ?>
          <div class="hood"><h3><?= e(html_entity_decode($n['name'], ENT_QUOTES, 'UTF-8')) ?></h3><p><?= $n['blurb'] ?></p></div>
        <?php endforeach; ?>
      </div>
    </section>
    <?php endif; ?>
    <section class="section-sm split">
      <div><h2>What sublets cost in <?= e($name) ?></h2><?= $guide['prices'] ?><p class="small muted">Price ranges are rough, cautious guidance only — not data from listings on The Sublet. Use the <a href="/tools/cost-calculator/">cost calculator</a> to budget.</p></div>
      <div><h2>Getting around</h2><?= $guide['transit'] ?></div>
    </section>
    <?php if ($tips): ?>
    <section class="section-sm">
      <h2>Tips for your stay in <?= e($name) ?></h2>
      <div class="grid two tips">
        <?php foreach ($tipLabels as $tk => [$ico, $lbl]): if (empty($tips[$tk])) continue; ?>
          <div class="tip"><h3><span aria-hidden="true"><?= $ico ?></span> <?= e($lbl) ?></h3><p><?= $tips[$tk] ?></p></div>
        <?php endforeach; ?>
      </div>
    </section>
    <?php endif; ?>
  </article>
  <?php elseif ($filterKey && $guide): ?>
  <section class="section-sm narrow">
    <p>Looking for more context? Read the full <a href="<?= e($base) ?>"><?= e($name) ?> sublet guide</a> — neighborhoods, transit and tips for interns, travel nurses and students.</p>
  </section>
  <?php endif; ?>

  <section class="section-sm narrow">
    <?= faq_html($faqs, $name . ' sublet FAQs') ?>
    <div class="note"><strong>Hosts:</strong> follow your lease and <?= e($name) ?>’s short-term-rental, registration and tax rules. Listings must comply with fair housing laws. <a href="/fair-housing/">Learn more</a>.</div>
  </section>
  <?php $nearby = array_slice(array_filter(known_cities($st), fn($k) => $k !== $st . '/' . $slug, ARRAY_FILTER_USE_KEY), 0, 12, true); if ($nearby): ?>
  <section class="section-sm">
    <h2 class="h3">More cities in <?= e($stateName) ?></h2>
    <p class="chips"><?php foreach ($nearby as $k => $c): [$s2, $sl2] = explode('/', $k); ?><a href="<?= e(city_url($s2, $sl2)) ?>"><?= e($c['name']) ?></a><?php endforeach; ?></p>
  </section>
  <?php endif; ?>
</div>
<?php
$body = ob_get_clean();
$title = $filterKey ? seo_title($filters[$filterKey]['label'] . ' in ' . $name . ', ' . strtoupper($st))
    : seo_title($name . ', ' . strtoupper($st) . ' Sublets & Furnished Rentals');
$desc = $filterKey
    ? $filters[$filterKey]['label'] . ' in ' . $name . ', ' . $stateName . '. Browse 1–12 month furnished rentals posted by real hosts on The Sublet, with live filters and a map.'
    : 'Sublets in ' . $name . ', ' . strtoupper($st) . ': furnished rooms and apartments for 1–12 months, plus neighborhood, price and transit tips for interns and nurses.';
page([
    'title' => $title,
    'description' => $desc,
    'canonical' => $path,
    'robots' => $indexable ? 'index, follow' : 'noindex, follow',
    'body' => $body,
    'h_extra' => leaflet_head(),
    'og_image' => $cp ? base_url($cp['file']) : null,
    'schema' => array_values(array_filter([schema_breadcrumbs($crumbs), schema_itemlist($dir['cards'], $h1), schema_faq($faqs)])),
]);
