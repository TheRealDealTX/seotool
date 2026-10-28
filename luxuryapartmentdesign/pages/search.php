<?php
$q = trim((string) ($_GET['q'] ?? ''));
$results = [];
if ($q !== '') {
    $terms = array_filter(preg_split('/\s+/', mb_strtolower($q)));
    foreach (articles() as $a) {
        $hay = mb_strtolower($a['title'] . ' ' . $a['h1'] . ' ' . $a['keyword'] . ' ' . implode(' ', $a['secondary_keywords'] ?? []) . ' ' . $a['excerpt']);
        $body = mb_strtolower(strip_tags(article_body($a['slug'])));
        $score = 0;
        foreach ($terms as $t) {
            $score += substr_count($hay, $t) * 5 + min(substr_count($body, $t), 10);
        }
        if ($score > 0) $results[] = [$score, 'a', $a];
    }
    foreach (TOOLS as $s => $t) {
        $hay = mb_strtolower($t['name'] . ' ' . $t['short']);
        $score = 0;
        foreach ($terms as $term) $score += substr_count($hay, $term) * 6;
        if ($score > 0) $results[] = [$score, 't', $s];
    }
    usort($results, fn($x, $y) => $y[0] <=> $x[0]);
}
page_head([
    'title' => $q !== '' ? 'Search results for “' . $q . '”' : 'Search',
    'description' => 'Search Luxury Apartment Design guides and tools.',
    'path' => '/search/',
    'robots' => 'noindex, follow',
]);
?>
<section class="page-hero">
  <div class="container container--narrow">
    <h1>Search</h1>
    <form class="search-form" action="/search/" method="get">
      <label class="sr-only" for="q">Search</label>
      <input id="q" type="search" name="q" value="<?= e($q) ?>" placeholder="Try “rug size” or “small bathroom”">
      <button class="btn btn--gold" type="submit">Search</button>
    </form>
    <?php if ($q !== ''): ?><p class="page-hero__lead"><?= count($results) ?> result<?= count($results) === 1 ? '' : 's' ?> for “<?= e($q) ?>”</p><?php endif; ?>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3">
      <?php foreach ($results as [$s, $type, $item]) echo $type === 'a' ? article_card($item) : tool_card($item); ?>
    </div>
    <?php if ($q !== '' && !$results): ?><p class="empty-state">Nothing matched. Browse <a href="/blogs/">all articles</a> or our <a href="/tools/">free design tools</a>.</p><?php endif; ?>
  </div>
</section>
<?php page_foot(); ?>
