<?php
$meta['title'] = 'Galveston Insurance Claim Guides | Public Adjuster Blog';
$meta['description'] = 'Weekly guides for Galveston property owners on TWIA, hurricane, fire, flood and denied insurance claims — written by licensed public adjuster ' . AUTHOR . '.';
$meta['crumb'] = 'Blog';
$posts = blog_posts();
$meta['schema'][] = ['@type' => 'Blog', 'name' => SITE_NAME . ' Blog', 'url' => SITE_URL . '/blog/', 'author' => ['@type' => 'Person', 'name' => AUTHOR],
    'blogPost' => array_map(fn($p) => ['@type' => 'BlogPosting', 'headline' => $p['title'], 'url' => SITE_URL . '/blog/' . $p['slug'] . '/', 'datePublished' => $p['date']], $posts)];
echo page_hero(icon('file', 18) . ' New guide every week', 'Insurance Claim Guides for Galveston Property Owners',
    'Practical, no-nonsense help with TWIA, hurricane, fire, flood and denied claims — written by ' . AUTHOR . ', licensed Texas public adjuster.');
?>
<section class="section">
  <div class="wrap">
    <?php if ($posts): ?>
    <div class="grid g3"><?php foreach ($posts as $i => $p) echo post_card($p, $i); ?></div>
    <?php else: ?><p class="center muted">The first guide is on its way.</p><?php endif ?>
    <?= banner('Have a question about your claim? Call for an expert consultation.', 'Free, no-obligation review with ' . AUTHOR . '.') ?>
  </div>
</section>
