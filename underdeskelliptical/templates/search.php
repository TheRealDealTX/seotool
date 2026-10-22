<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
$q = trim(mb_substr((string) ($_GET['s'] ?? ''), 0, 80));
$terms = array_filter(preg_split('/\s+/', mb_strtolower($q)));
$hits = [];
foreach (all_posts() as $p) {
    $hay = mb_strtolower($p['h1'] . ' ' . $p['keyword'] . ' ' . $p['description'] . ' ' . strip_tags($p['body']));
    $score = 0;
    foreach ($terms as $t) {
        $score += substr_count($hay, $t) + 20 * substr_count(mb_strtolower($p['h1']), $t);
    }
    if ($score) {
        $hits[] = [$score, $p];
    }
}
usort($hits, fn($a, $b) => $b[0] <=> $a[0]);
page_start(['title' => 'Search results for "' . $q . '" | ' . SITE_NAME, 'description' => 'Search ' . SITE_NAME, 'noindex' => true, 'path' => '/']);
?>
<section class="page-hero"><div class="wrap">
  <h1>Search results for “<?= e($q) ?>”</h1>
  <form action="/" method="get" class="big-search" role="search"><input type="search" name="s" value="<?= e($q) ?>" aria-label="Search"><button class="btn">Search</button></form>
</div></section>
<div class="wrap">
  <p><?= count($hits) ?> results.</p>
  <div class="grid grid-3"><?php foreach (array_slice($hits, 0, 24) as [, $p]) echo post_card($p, 2); ?></div>
</div>
<?php page_end();
