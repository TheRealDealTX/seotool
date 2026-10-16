<?php
// /feed/ — the HTML "what's new" page: newest listings, newest guides, every
// installation, and the Fort Hood housing guide (the site's top search topic).
// The RSS feed that used to live here is now /feed.xml.
$new_listings = newest_listings(6);
$new_posts = newest_posts(3);
$guide_id = 'fort-hood-housing-guide';
$guide_title = 'Fort Hood Housing Guide: On-Post Neighborhoods, 2026 BAH and Off-Post Options';
$guide_updated = FEED_GUIDE_UPDATED;
[$guide, $toc, $faq] = article_prepare(guide_html('fort-hood-housing'));
$hood = base('fort-cavazos');
$hood_listings = listings_for_base('fort-cavazos');
$last_listing = $new_listings[0]['date'] ?? date('Y-m-d');
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], ['Latest listings & guides', null]]);

$schema = [$crumb_schema, [
    '@type' => 'CollectionPage', '@id' => abs_url('/feed/#page'), 'url' => abs_url('/feed/'),
    'name' => 'Latest military housing listings and guides',
    'dateModified' => max($last_listing, $guide_updated),
    'mainEntity' => ['@type' => 'ItemList', 'numberOfItems' => count($new_listings), 'itemListElement' => array_map(fn($l, $i) => [
        '@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url('/properties/' . $l['slug'] . '/'), 'name' => $l['title'],
    ], $new_listings, array_keys($new_listings))],
], [
    '@type' => 'Article', '@id' => abs_url('/feed/#' . $guide_id), 'headline' => $guide_title,
    'description' => 'Where Soldiers and families live at Fort Hood, Texas: Cavalry Family Housing neighborhoods, the housing office and waitlist, 2026 Killeen BAH rates and off-post options in Killeen, Harker Heights and Copperas Cove.',
    'datePublished' => '2026-10-16', 'dateModified' => $guide_updated, 'mainEntityOfPage' => abs_url('/feed/'),
    'image' => abs_url($hood['image']['src']), 'about' => ['@type' => 'Place', 'name' => 'Fort Hood', 'url' => abs_url('/bases/fort-cavazos/')],
    'author' => ['@type' => 'Organization', 'name' => cfg('name'), 'url' => abs_url('/')], 'publisher' => ['@id' => abs_url('/#organization')],
]];
if ($faq) $schema[] = ['@type' => 'FAQPage', 'mainEntity' => $faq];

layout_start([
    'title' => 'Latest Military Housing Listings & Fort Hood Housing Guide',
    'full_title' => 'Latest Military Housing Listings & Fort Hood Housing Guide (2026) | ' . cfg('name'),
    'description' => 'New on-base housing listings and PCS guides from Military Housing Rentals, plus our 2026 Fort Hood housing guide: Cavalry Family Housing neighborhoods, Killeen BAH rates, the housing office and off-post options.',
    'path' => '/feed/',
    'image' => $hood['image']['src'],
    'nav' => '/properties/',
    'schema' => $schema,
]);
?>
<section class="page-hero">
  <div class="wrap">
    <?= $crumbs ?>
    <p class="eyebrow"><?= icon('bolt') ?> Updated <?= e(fmt_date(max($last_listing, $guide_updated))) ?></p>
    <h1>Latest military housing listings &amp; guides</h1>
    <p class="lead">Everything new on Military Housing Rentals in one place: the newest on-base communities and military-friendly rentals, the latest PCS guides, every installation we cover, and our in-depth <a href="#<?= e($guide_id) ?>">Fort Hood housing guide</a>, the most-searched base on the site.</p>
    <p class="feed-note"><?= icon('share') ?> Prefer a reader? Subscribe to the <a href="/feed.xml">RSS feed</a>. <span>&middot;</span> Own a rental near a base? <a href="/submit-property/">Submit a property</a>.</p>
  </div>
</section>

<section class="section section-tight">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Just listed</p><h2>Newest housing listings</h2></div>
      <a class="link-arrow" href="/properties/">All <?= count(listings()) ?> listings <?= icon('arrow') ?></a>
    </div>
    <div class="card-grid"><?php foreach ($new_listings as $l) echo listing_card($l); ?></div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">New guides</p><h2>Latest articles for military families</h2></div>
      <a class="link-arrow" href="/blog/">All articles <?= icon('arrow') ?></a>
    </div>
    <div class="card-grid"><?php foreach ($new_posts as $p) echo post_card($p); ?></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Browse by installation</p><h2>Housing by military base</h2></div>
      <a class="link-arrow" href="/marine-bases/">All bases <?= icon('arrow') ?></a>
    </div>
    <ul class="base-list">
      <?php foreach (bases() as $b): $n = count(listings_for_base($b['slug'])); ?>
        <li><a href="/bases/<?= e($b['slug']) ?>/"><?= e($b['name']) ?> housing</a><span class="muted"><?= e($b['city'] . ', ' . $b['state']) ?> &middot; <?= $n ?> listing<?= $n === 1 ? '' : 's' ?></span></li>
      <?php endforeach; ?>
    </ul>
  </div>
</section>

<section class="section section-alt guide" id="<?= e($guide_id) ?>">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Featured guide</p><h2><?= e($guide_title) ?></h2></div>
      <a class="link-arrow" href="/bases/fort-cavazos/">Fort Hood listings <?= icon('arrow') ?></a>
    </div>
    <p class="guide-meta"><span><?= icon('calendar') ?> Updated <?= e(fmt_date($guide_updated)) ?></span><span><?= icon('clock') ?> <?= max(1, (int)round(str_word_count(strip_tags($guide)) / 225)) ?> min read</span><span><?= icon('pin') ?> Killeen, TX</span></p>
    <?php if (count($toc) > 2): ?>
    <nav aria-label="Guide sections" data-toc><ul class="jump-links"><?php foreach ($toc as [$id, $t]): ?><li><a href="#<?= e($id) ?>"><?= e($t) ?></a></li><?php endforeach; ?></ul></nav>
    <?php endif; ?>
    <div class="two-col">
      <div class="prose guide-body"><?= $guide ?></div>
      <div>
        <?php if ($hood_listings): ?>
        <div class="card side-card">
          <h3>Fort Hood housing listings</h3>
          <ul class="mini-list">
          <?php foreach ($hood_listings as $l): $img = listing_image($l); ?>
            <li><a href="/properties/<?= e($l['slug']) ?>/"><img src="<?= e($img['src']) ?>" alt="" width="64" height="64" loading="lazy"><span><strong><?= e($l['title']) ?></strong><small><?= e(price_label($l)) ?> &middot; <?= e(($l['beds_range'] ?: fmt_num($l['beds'])) . ' bd') ?></small></span></a></li>
          <?php endforeach; ?>
          </ul>
          <a class="btn btn-outline btn-block" href="/bases/fort-cavazos/">All Fort Hood listings</a>
        </div>
        <?php endif; ?>
        <?= widget_bah() ?>
      </div>
    </div>
  </div>
</section>

<?= cta_band() ?>
<?php layout_end();
