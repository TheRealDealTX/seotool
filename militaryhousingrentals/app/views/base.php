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
    $seo = $b['seo'] ?? [];
    // Optional long-form guide for this installation (app/data/guides/{name}.html)
    $guide = !empty($b['guide']) ? guide_html($b['guide']) : '';
    $toc = $faq = [];
    if ($guide) [$guide, $toc, $faq] = article_prepare($guide);
    $guide_id = 'housing-guide';
    $guide_title = $b['name'] . ' housing guide (' . date('Y') . ')';
    $guide_updated = $b['guide_updated'] ?? '2026-10-16';
    $schema = [];
    if ($guide) {
        $schema[] = [
            '@type' => 'Article', '@id' => abs_url("/bases/$slug/#$guide_id"), 'headline' => $guide_title,
            'description' => $seo['description'] ?? '', 'datePublished' => $guide_updated, 'dateModified' => $guide_updated,
            'mainEntityOfPage' => abs_url("/bases/$slug/"), 'image' => abs_url($b['image']['src'] ?? cfg('og_image')),
            'about' => ['@type' => 'Place', 'name' => $b['name']],
            'author' => ['@type' => 'Organization', 'name' => cfg('name'), 'url' => abs_url('/')], 'publisher' => ['@id' => abs_url('/#organization')],
        ];
        if ($faq) $schema[] = ['@type' => 'FAQPage', 'mainEntity' => $faq];
    }
    ob_start(); ?>
<section class="section section-tight">
  <div class="wrap base-facts">
    <div class="fact"><span class="muted">Branch</span><strong><?= e($b['branch']) ?></strong></div>
    <div class="fact"><span class="muted">Nearest city</span><strong><?= e($b['city'] . ', ' . $b['state']) ?></strong></div>
    <div class="fact"><span class="muted">Listings</span><strong><?= count($items) ?></strong></div>
    <div class="fact fact-wide"><span class="muted">About</span><p><?= e($b['blurb']) ?><?php if ($guide): ?> <a href="#<?= e($guide_id) ?>">Read the housing guide &darr;</a><?php elseif (!empty($b['guide_url'])): ?> <a href="<?= e($b['guide_url']) ?>">Read the housing guide &rarr;</a><?php endif; ?></p></div>
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
        <?php if ($guide): ?><li><?= icon('check') ?> <a href="#<?= e($guide_id) ?>"><?= e($guide_title) ?></a></li><?php endif; ?>
        <?php if (!$guide && !empty($b['guide_url'])): ?><li><?= icon('check') ?> <a href="<?= e($b['guide_url']) ?>"><?= e($b['guide_label'] ?? $b['short'] . ' housing guide') ?></a></li><?php endif; ?>
        <li><?= icon('check') ?> <a href="/pcs-moving-checklist/">PCS moving checklist</a></li>
        <li><?= icon('check') ?> <a href="/what-is-base-housing/">What is base housing?</a></li>
        <li><?= icon('check') ?> <a href="/how-to-find-off-base-housing/">How to find off-base housing</a></li>
        <li><?= icon('check') ?> <a href="/pcs-with-pets-military-housing/">PCSing with pets</a></li>
      </ul>
      <?php if ($others): ?>
        <p class="muted">Other <?= e($b['state']) ?> installations: <?php foreach ($others as $i => $o) echo ($i ? ', ' : '') . '<a href="/bases/' . e($o['slug']) . '/">' . e($o['name']) . '</a>'; ?></p>
      <?php endif; ?>
      <p class="muted">See what's new across every base on the <a href="/feed/">latest listings &amp; guides</a> page.</p>
    </div>
    <?= widget_bah() ?>
  </div>
</section>
<?php if ($guide): ?>
<section class="section guide" id="<?= e($guide_id) ?>">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Housing guide</p><h2><?= e($guide_title) ?></h2></div>
      <a class="link-arrow" href="#main">Back to listings <?= icon('arrow', 'flip') ?></a>
    </div>
    <p class="guide-meta"><span><?= icon('calendar') ?> Updated <?= e(fmt_date($guide_updated)) ?></span><span><?= icon('clock') ?> <?= max(1, (int)round(str_word_count(strip_tags($guide)) / 225)) ?> min read</span><span><?= icon('pin') ?> <?= e($b['city'] . ', ' . $b['state']) ?></span></p>
    <?php if (count($toc) > 2): ?>
    <nav aria-label="Guide sections" data-toc><ul class="jump-links"><?php foreach ($toc as [$id, $t]): ?><li><a href="#<?= e($id) ?>"><?= e($t) ?></a></li><?php endforeach; ?></ul></nav>
    <?php endif; ?>
    <div class="two-col">
      <div class="prose guide-body"><?= $guide ?></div>
      <div>
        <?php if ($items): ?>
        <div class="card side-card">
          <h3><?= e($b['short']) ?> housing listings</h3>
          <ul class="mini-list">
          <?php foreach ($items as $l): $img = listing_image($l); ?>
            <li><a href="/properties/<?= e($l['slug']) ?>/"><img src="<?= e($img['src']) ?>" alt="" width="64" height="64" loading="lazy"><span><strong><?= e($l['title']) ?></strong><small><?= e(price_label($l)) ?> &middot; <?= e(($l['beds_range'] ?: fmt_num($l['beds'])) . ' bd') ?></small></span></a></li>
          <?php endforeach; ?>
          </ul>
          <a class="btn btn-outline btn-block" href="#main">Compare on the map</a>
        </div>
        <?php endif; ?>
        <div class="card side-card">
          <h3>Keep reading</h3>
          <ul class="mini-list">
          <?php foreach (newest_posts(3) as $p): ?>
            <li><a href="/<?= e($p['slug']) ?>/"><img src="<?= e($p['image']['src'] ?? cfg('og_image')) ?>" alt="" width="64" height="64" loading="lazy"><span><strong><?= e($p['title']) ?></strong><small><?= e(fmt_date($p['date'])) ?></small></span></a></li>
          <?php endforeach; ?>
          </ul>
          <a class="btn btn-outline btn-block" href="/feed/">Latest listings &amp; guides</a>
        </div>
      </div>
    </div>
  </div>
</section>
<?php endif;
    $after = ob_get_clean();
    $archive = [
        'path' => "/bases/$slug/",
        'title' => $b['name'] . ' Military Housing Rentals',
        'full_title' => $seo['full_title'] ?? null,
        'h1' => $seo['h1'] ?? $b['name'] . ' housing',
        'eyebrow' => $b['branch'] . ' · ' . $b['city'] . ', ' . $b['state'],
        'intro' => $seo['intro'] ?? 'On-base family housing communities and rentals at ' . $b['name'] . ' near ' . $b['city'] . ', ' . $b['state'] . '. Compare neighborhoods, floor plans and amenities, then contact the community directly.',
        'description' => $seo['description'] ?? 'Military housing rentals at ' . $b['name'] . ' (' . $b['city'] . ', ' . $b['state'] . '): on-base family housing neighborhoods, floor plans, amenities and leasing office contacts.',
        'items' => $items,
        'base' => $slug,
        'image' => $b['image']['src'] ?? null,
        'hero_img' => $b['image']['src'] ?? null,
        'crumbs' => [['Home', '/'], ['Military Bases', '/marine-bases/'], [$b['name'], null]],
        'before' => $before,
        'after' => $after,
        'schema' => $schema,
    ];
}
require __DIR__ . '/properties.php';
