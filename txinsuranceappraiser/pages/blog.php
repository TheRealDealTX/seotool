<?php
$title = 'Texas Insurance Claim & Appraisal Blog | TX Insurance Appraiser';
$desc  = 'Expert guides on Texas insurance appraisal, roof and hail claims, Xactimate estimates, depreciation and commercial property claims.';
$P = posts();
ob_start(); ?>
<section class="hero hero-sm">
  <div class="hero-bg" style="background-image:url(/assets/img/site/TX-Insurance-Appraiser-Background.webp)"></div>
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">Insurance claim blog</span>
      <h1 class="anim">Texas Insurance Claim &amp; Appraisal Guides</h1>
      <p class="lead anim"><?= count($P) ?> in-depth articles on appraisal, roof claims, estimating and Texas weather — written for property owners who want to understand their claim.</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:56px">
  <div class="wrap">
    <div class="search-box"><?= icon('search', 20) ?><input type="search" placeholder="Search articles…" aria-label="Search articles" data-search></div>
    <div class="filters" role="group" aria-label="Filter by category">
      <button class="on" data-cat="all">All</button>
      <?php foreach (BLOG_CATEGORIES as $cat): ?><button data-cat="<?= e($cat) ?>"><?= e($cat) ?></button><?php endforeach; ?>
    </div>
    <div class="grid g3" data-posts>
      <?php foreach ($P as $p): ?>
      <article class="card card-img post-card reveal" data-cat="<?= e($p['category'] ?? '') ?>">
        <a class="ci-media" href="/<?= $p['slug'] ?>/"><img src="<?= post_image($p) ?>" alt="<?= e($p['h1']) ?>" width="700" height="394" loading="lazy"></a>
        <div class="ci-body">
          <span class="pill"><?= e($p['category'] ?? '') ?></span>
          <h2 style="font-size:1.15rem"><a href="/<?= $p['slug'] ?>/" style="text-decoration:none;color:inherit"><?= e($p['h1']) ?></a></h2>
          <p><?= e($p['excerpt'] ?? '') ?></p>
          <p class="meta"><?= e(nice_date($p['published'] ?? '')) ?> · <?= reading_minutes($p['body_html']) ?> min read</p>
        </div>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?= cta_band() ?>
<?php
$content = (string) ob_get_clean();
$items = [];
$i = 0;
foreach ($P as $p) {
    $items[] = ['@type' => 'ListItem', 'position' => ++$i, 'url' => abs_url('/' . $p['slug'] . '/'), 'name' => $p['h1']];
}
render_page([
    'title' => $title, 'description' => $desc, 'path' => '/blog/',
    'crumbs' => [['Home', '/'], ['Blog', '/blog/']],
    'schema' => [schema_webpage('CollectionPage', $title, $desc, '/blog/'), ['@type' => 'ItemList', 'itemListElement' => $items]],
], $content);
