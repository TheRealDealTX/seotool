<?php
// /bases/{slug}/ — one installation, or the "featured" collection.
if ($slug === 'featured') {
    $archive = [
        'path' => '/bases/featured/', 'title' => 'Featured Military Housing Rentals', 'h1' => 'Featured properties',
        'eyebrow' => 'Hand-picked',
        'intro' => 'Our featured military housing communities: complete listings with photos, floor plans and amenities.',
        'description' => 'Featured military housing rentals and on-base family housing communities, with photos, floor plans and amenities.',
        'items' => array_values(array_filter(listings(), fn($l) => $l['featured'])),
        'base' => 'featured',
        'crumbs' => [['Home', '/'], ['Military Bases', '/marine-bases/'], ['Featured', null]],
    ];
} else {
    $b = base($slug);
    $items = listings_for_base($slug);
    $others = array_values(array_filter(bases(), fn($o) => $o['slug'] !== $slug && $o['state'] === $b['state']));
    ob_start(); ?>
<section class="section section-tight">
  <div class="wrap base-facts">
    <div class="fact"><span class="muted">Branch</span><strong><?= e($b['branch']) ?></strong></div>
    <div class="fact"><span class="muted">Nearest city</span><strong><?= e($b['city'] . ', ' . $b['state']) ?></strong></div>
    <div class="fact"><span class="muted">Listings</span><strong><?= count($items) ?></strong></div>
    <div class="fact fact-wide"><span class="muted">About</span><p><?= e($b['blurb']) ?></p></div>
  </div>
</section>
<?php
    $before = ob_get_clean();
    ob_start(); ?>
<section class="section section-alt">
  <div class="wrap two-col">
    <div>
      <h2>Moving to <?= e($b['short']) ?>?</h2>
      <p>Contact the installation housing office as soon as you have orders. They manage the waitlist for on-base housing and can help with off-base referrals. Privatized communities set rent to your BAH, so it helps to <a href="/bah-explained-military-housing-allowance/">know how BAH works</a> before you compare options.</p>
      <ul class="checks">
        <li><?= icon('check') ?> <a href="/pcs-moving-checklist/">PCS moving checklist</a></li>
        <li><?= icon('check') ?> <a href="/what-is-base-housing/">What is base housing?</a></li>
        <li><?= icon('check') ?> <a href="/how-to-find-off-base-housing/">How to find off-base housing</a></li>
        <li><?= icon('check') ?> <a href="/pcs-with-pets-military-housing/">PCSing with pets</a></li>
      </ul>
      <?php if ($others): ?>
        <p class="muted">Other <?= e($b['state']) ?> installations: <?php foreach ($others as $i => $o) echo ($i ? ', ' : '') . '<a href="/bases/' . e($o['slug']) . '/">' . e($o['name']) . '</a>'; ?></p>
      <?php endif; ?>
    </div>
    <?= widget_bah() ?>
  </div>
</section>
<?php
    $after = ob_get_clean();
    $archive = [
        'path' => "/bases/$slug/",
        'title' => $b['name'] . ' Military Housing Rentals',
        'h1' => $b['name'] . ' housing',
        'eyebrow' => $b['branch'] . ' · ' . $b['city'] . ', ' . $b['state'],
        'intro' => 'On-base family housing communities and rentals at ' . $b['name'] . ' near ' . $b['city'] . ', ' . $b['state'] . '. Compare neighborhoods, floor plans and amenities, then contact the community directly.',
        'description' => 'Military housing rentals at ' . $b['name'] . ' (' . $b['city'] . ', ' . $b['state'] . '): on-base family housing neighborhoods, floor plans, amenities and leasing office contacts.',
        'items' => $items,
        'base' => $slug,
        'image' => $b['image']['src'] ?? null,
        'hero_img' => $b['image']['src'] ?? null,
        'crumbs' => [['Home', '/'], ['Military Bases', '/marine-bases/'], [$b['name'], null]],
        'before' => $before,
        'after' => $after,
    ];
}
require __DIR__ . '/properties.php';
