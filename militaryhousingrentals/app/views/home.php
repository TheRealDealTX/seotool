<?php
$all = listings();
$featured = array_values(array_filter($all, fn($l) => $l['featured']));
$recent = newest_listings(8);
$branches = [];
foreach (bases() as $b) foreach (preg_split('#\s*/\s*#', $b['branch']) as $br) $branches[$br] = true;
$states = array_unique(array_map(fn($b) => $b['state'], bases()));

layout_start([
    'full_title' => cfg('name') . ' | ' . cfg('tagline'),
    'title' => cfg('name'),
    'description' => 'Find on-base and military-friendly rental housing near Fort Hood, JBSA, Fort Bragg, Camp Lejeune, JBLM, Camp Pendleton and more. Compare floor plans, amenities and BAH budgets.',
    'path' => '/',
    'body_class' => 'page-home',
    'schema' => [[
        '@type' => 'WebSite', '@id' => abs_url('/#website'), 'url' => abs_url('/'), 'name' => cfg('name'),
        'description' => cfg('tagline'), 'publisher' => ['@id' => abs_url('/#organization')],
        'potentialAction' => ['@type' => 'SearchAction', 'target' => ['@type' => 'EntryPoint', 'urlTemplate' => abs_url('/?s={search_term_string}')], 'query-input' => 'required name=search_term_string'],
    ]],
]);
?>
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><img src="/wp-content/uploads/2025/06/Military-Housing-Rentals-BG-1.webp" alt="" fetchpriority="high"></div>
  <div class="wrap hero-inner">
    <p class="eyebrow"><?= icon('shield') ?> Built for service members &amp; military families</p>
    <h1>Find your next home near <span class="rotator" data-rotate='<?= e(json_encode(array_map(fn($b) => $b['short'], bases()))) ?>'>base</span></h1>
    <p class="lead">Compare on-base housing communities and military-friendly rentals by installation, floor plan and budget, then plan your PCS with free tools.</p>
    <form class="search-panel" action="/properties/" method="get" role="search">
      <label class="field">
        <span>Installation</span>
        <select name="base">
          <option value="">All bases</option>
          <?php foreach (bases() as $b): ?><option value="<?= e($b['slug']) ?>"><?= e($b['name']) ?></option><?php endforeach; ?>
        </select>
      </label>
      <label class="field">
        <span>Bedrooms</span>
        <select name="beds">
          <option value="">Any</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option>
        </select>
      </label>
      <label class="field field-grow">
        <span>Keyword</span>
        <input type="search" name="q" placeholder="Neighborhood, city or amenity" autocomplete="off">
      </label>
      <button class="btn btn-accent btn-lg" type="submit"><?= icon('search') ?> Search</button>
    </form>
    <ul class="stats">
      <li><strong data-count="<?= count($all) ?>"><?= count($all) ?></strong><span>Housing listings</span></li>
      <li><strong data-count="<?= count(bases()) ?>"><?= count(bases()) ?></strong><span>Installations</span></li>
      <li><strong data-count="<?= count($states) ?>"><?= count($states) ?></strong><span>States</span></li>
      <li><strong data-count="<?= count(posts()) ?>"><?= count(posts()) ?></strong><span>Free PCS guides</span></li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="eyebrow">Browse by installation</p>
        <h2>Military bases we cover</h2>
      </div>
      <a class="link-arrow" href="/marine-bases/">All bases <?= icon('arrow') ?></a>
    </div>
    <div class="base-grid">
      <?php foreach (bases() as $b): $n = count(listings_for_base($b['slug'])); ?>
        <a class="base-tile" href="/bases/<?= e($b['slug']) ?>/">
          <span class="base-branch"><?= e($b['branch']) ?></span>
          <strong><?= e($b['name']) ?></strong>
          <span class="muted"><?= e($b['city'] . ', ' . $b['state']) ?></span>
          <span class="base-count"><?= $n ?> listing<?= $n === 1 ? '' : 's' ?> <?= icon('arrow') ?></span>
        </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<?php if ($featured): ?>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Hand-picked</p><h2>Featured properties</h2></div>
      <a class="link-arrow" href="/bases/featured/">View featured <?= icon('arrow') ?></a>
    </div>
    <div class="card-grid"><?php foreach ($featured as $l) echo listing_card($l); ?></div>
  </div>
</section>
<?php endif; ?>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Just added</p><h2>Recently listed properties</h2></div>
      <div class="scroller-ctrl">
        <button class="icon-btn" type="button" data-scroll="-1" aria-label="Scroll left"><?= icon('arrow', 'flip') ?></button>
        <button class="icon-btn" type="button" data-scroll="1" aria-label="Scroll right"><?= icon('arrow') ?></button>
      </div>
    </div>
    <div class="scroller" data-scroller><?php foreach ($recent as $l) echo listing_card($l, 'scroller-item'); ?></div>
    <p class="center"><a class="btn btn-primary btn-lg" href="/properties/">Explore all <?= count($all) ?> listings <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">Free planning tools</p><h2>Plan your move in minutes</h2></div>
    </div>
    <div class="tools-grid">
      <?= widget_bah() ?>
      <?= widget_pcs() ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center-head">
      <div><p class="eyebrow">How it works</p><h2>From orders to keys in three steps</h2></div>
    </div>
    <ol class="steps">
      <li><span class="step-icon"><?= icon('search') ?></span><h3>Search by base</h3><p>Filter communities by installation, bedrooms, square footage and amenities, or explore them on the map.</p></li>
      <li><span class="step-icon"><?= icon('heart') ?></span><h3>Save &amp; compare</h3><p>Tap the heart on any listing to build a shortlist you can come back to on this device.</p></li>
      <li><span class="step-icon"><?= icon('phone') ?></span><h3>Contact the community</h3><p>Call or visit the housing office directly to confirm eligibility, waitlists and move-in dates.</p></li>
    </ol>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <div><p class="eyebrow">From the blog</p><h2>Guides for military families</h2></div>
      <a class="link-arrow" href="/blog/">All articles <?= icon('arrow') ?></a>
    </div>
    <div class="card-grid"><?php foreach (array_slice(posts(), 0, 3) as $p) echo post_card($p); ?></div>
  </div>
</section>

<?= cta_band() ?>
<?php layout_end();
