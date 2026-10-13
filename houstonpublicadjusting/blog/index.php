<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Blog', '/blog/']];
page_start([
    'title' => 'Insurance Claim Blog | Houston Public Adjusters',
    'desc' => 'Insurance claim guides from Houston public adjuster Joseph Dittman: hail and roof claims, fire claims, denied claims, supplements and when to hire a public adjuster.',
    'path' => '/blog/',
    'crumbs' => $crumbs,
    'schema' => [[
        '@type' => 'Blog', 'name' => 'Houston Public Adjusters Blog', 'url' => SITE_URL . '/blog/',
        'author' => ['@id' => SITE_URL . '/#joseph-dittman'], 'publisher' => ['@id' => SITE_URL . '/#business'],
        'blogPost' => array_map(fn($s) => ['@type' => 'BlogPosting', 'headline' => POSTS[$s]['h1'], 'url' => SITE_URL . '/' . $s . '/', 'datePublished' => POSTS[$s]['published'], 'author' => ['@id' => SITE_URL . '/#joseph-dittman']], array_keys(POSTS)),
    ]],
]);
echo page_hero('Insurance Claim Blog', 'Straight talk on property insurance claims from Joseph Dittman, licensed Texas public adjuster with Houston Public Adjusters. Learn how claims really work before you settle.', $crumbs);
?>
<section class="section">
  <div class="wrap">
    <?= post_cards(array_keys(POSTS)) ?>
  </div>
</section>
<?php
page_end();
