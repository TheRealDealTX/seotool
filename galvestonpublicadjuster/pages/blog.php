<?php
$meta['title'] = 'Galveston Insurance Claim Guides | Public Adjuster Blog';
$meta['description'] = 'Weekly guides for Galveston property owners on TWIA, hurricane, fire, flood and denied insurance claims — written by licensed public adjuster ' . AUTHOR . '.';
$meta['crumb'] = 'Blog';
$posts = blog_posts();
$meta['schema'][] = ['@type' => 'Blog', 'name' => SITE_NAME . ' Blog', 'url' => SITE_URL . '/blog/', 'author' => ['@type' => 'Person', 'name' => AUTHOR],
    'blogPost' => array_map(fn($p) => ['@type' => 'BlogPosting', 'headline' => $p['title'], 'url' => SITE_URL . '/blog/' . $p['slug'] . '/', 'datePublished' => $p['date']], $posts)];
// Group the guides by topic, in the order the categories are defined, so each topic can point at
// the hub pages behind it. Categories without a published post yet are skipped.
$groups = [];
foreach (array_keys(CATEGORY_HUBS) as $cat) $groups[$cat] = [];
foreach ($posts as $p) $groups[$p['category']][] = $p;
$groups = array_filter($groups);
echo page_hero(icon('file', 18) . ' New guide every week', 'Insurance Claim Guides for Galveston Property Owners',
    'Practical, no-nonsense help with TWIA, hurricane, fire, flood and denied claims — written by <a href="/about/" style="color:#fff">' . AUTHOR . '</a>, licensed Texas public adjuster.');
?>
<section class="section" style="padding-top:40px">
  <div class="wrap">
    <?php if (!$posts): ?><p class="center muted">The first guide is on its way.</p><?php endif ?>
    <?php if (count($groups) > 1): ?>
    <p class="center blog-jump"><strong>Jump to:</strong> <?= implode(' · ', array_map(fn($c) => '<a href="#' . e(strtolower(preg_replace('/[^a-z]+/i', '-', $c))) . '">' . e($c) . '</a>', array_keys($groups))) ?></p>
    <?php endif ?>
    <?php foreach ($groups as $cat => $list): $id = strtolower(preg_replace('/[^a-z]+/i', '-', $cat)); ?>
    <div class="blog-group" id="<?= e($id) ?>">
      <div class="blog-group-head"><h2><?= e($cat) ?></h2><p class="small muted">Related: <?= category_hub_links($cat) ?></p></div>
      <div class="grid g3"><?php foreach ($list as $i => $p) echo post_card($p, $i); ?></div>
    </div>
    <?php endforeach ?>
    <?= banner('Have a question about your claim? Call for an expert consultation.', 'Free, no-obligation review with ' . AUTHOR . '.') ?>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Start here</span><h2>Tools and references behind the guides</h2><p>Everything we use on real claims, published for you.</p></div>
    <div class="grid g3"><?php foreach (['twia', 'fire', 'calculators', 'windstorm-rules', 'local-code', 'weather-events'] as $k) echo hub_card($k); ?></div>
  </div>
</section>
