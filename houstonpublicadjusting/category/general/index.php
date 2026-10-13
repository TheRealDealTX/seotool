<?php
require dirname(__DIR__, 2) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Blog', '/blog/'], ['General', '/category/general/']];
$slugs = array_keys(array_filter(POSTS, fn($p) => $p['category'] === 'general'));
page_start([
    'title' => 'General Insurance Claim Articles | Houston Public Adjusters',
    'desc' => 'All general insurance claim articles from Houston Public Adjusters, written by licensed Texas public adjuster Joseph Dittman.',
    'path' => '/category/general/',
    'crumbs' => $crumbs,
    'schema' => [['@type' => 'CollectionPage', 'name' => 'General', 'url' => SITE_URL . '/category/general/']],
]);
echo page_hero('General Claim Articles', 'Every guide in our General category &mdash; hail, roof, fire and denied-claim advice from a licensed Houston public adjuster.', $crumbs, 'Category');
?>
<section class="section"><div class="wrap"><?= post_cards($slugs) ?></div></section>
<?php
page_end();
