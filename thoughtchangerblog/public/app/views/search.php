<?php
/** @var string $q */
$terms = array_filter(preg_split('/\s+/', mb_strtolower($q)), fn($t) => mb_strlen($t) > 1);
$hits = [];
if ($terms) foreach (posts() as $p) {
    $hay = mb_strtolower($p['title'] . ' ' . $p['description']);
    $body = null; $score = 0;
    foreach ($terms as $t) {
        if (str_contains($hay, $t)) $score += 5;
        else { $body ??= mb_strtolower(strip_tags(post_body($p))); if (str_contains($body, $t)) $score += 1; else { $score = 0; break; } }
    }
    if ($score) $hits[] = [$score, $p];
}
usort($hits, fn($a, $b) => $b[0] <=> $a[0]);
view('head', ['meta' => ['title' => 'You searched for ' . $q . ' - ' . SITE_NAME, 'description' => '', 'canonical' => '/?s=' . urlencode($q), 'robots' => 'noindex, follow', 'bodyClass' => 'search']]);
?>
<section class="page-hero">
  <div class="wrap-narrow">
    <h1 class="page-title">Search results</h1>
    <form class="search search-lg" role="search" action="/" method="get">
      <label class="sr-only" for="ss">Search</label>
      <input id="ss" type="search" name="s" value="<?= e($q) ?>" placeholder="Search articles">
      <button type="submit" class="btn btn-accent">Search</button>
    </form>
    <p class="page-lede"><?= count($hits) ?> result<?= count($hits) === 1 ? '' : 's' ?> for “<?= e($q) ?>”</p>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="grid grid-4">
      <?php foreach ($hits as [$s, $p]) view('card', ['p' => $p]); ?>
    </div>
    <?php if (!$hits): ?><p class="center">Nothing matched that search. Try a single word, or <a href="/blog/">browse all articles</a>.</p><?php endif; ?>
  </div>
</section>
<?php view('foot'); ?>
