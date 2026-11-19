<?php
/** @var string $q */
$hits = search_posts($q);
$total = count($hits);
view('head', ['meta' => ['title' => ($q === '' ? 'Search' : 'You searched for ' . $q) . ' - ' . SITE_NAME, 'description' => '', 'canonical' => '/?s=' . urlencode($q), 'robots' => 'noindex, follow', 'bodyClass' => 'search-page']]);
$terms = search_terms($q);
$hl = function (string $text) use ($terms): string {
    $out = e($text);
    foreach ($terms as $t) $out = preg_replace('/(' . preg_quote(e($t), '/') . ')/iu', '<mark>$1</mark>', $out);
    return $out;
};
?>
<section class="page-hero">
  <div class="wrap-narrow">
    <span class="eyebrow center-block">Search</span>
    <h1 class="page-title"><?= $q === '' ? 'Search the blog' : 'Results for “' . e($q) . '”' ?></h1>
    <form class="sbox js-suggest" role="search" action="/" method="get" autocomplete="off">
      <label class="sr-only" for="ss">Search articles</label>
      <svg class="sbox-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M10 2a8 8 0 0 1 6.32 12.9l5.39 5.4-1.41 1.4-5.4-5.39A8 8 0 1 1 10 2Zm0 2a6 6 0 1 0 0 12 6 6 0 0 0 0-12Z"/></svg>
      <input id="ss" type="search" name="s" value="<?= e($q) ?>" placeholder="Try “fleeting”, “mindset”, “quotes”…" aria-autocomplete="list" aria-controls="ss-list" aria-expanded="false">
      <button type="submit" class="btn btn-accent">Search</button>
      <div class="suggest" id="ss-list" role="listbox" hidden></div>
    </form>
    <?php if ($q !== ''): ?><p class="result-count"><?= $total ?> article<?= $total === 1 ? '' : 's' ?> found</p><?php endif; ?>
    <div class="chips"><span class="chips-label">Popular:</span><?php foreach (['life is fleeting', 'level up', 'quotes', 'mindset', 'gratitude', 'boundaries', 'island time'] as $c): ?><a href="/?s=<?= urlencode($c) ?>"><?= e($c) ?></a><?php endforeach; ?></div>
  </div>
</section>
<section class="band band-tight">
  <div class="wrap-narrow">
    <?php if ($hits): ?>
    <ol class="results">
      <?php foreach ($hits as $p): ?>
      <li class="result reveal">
        <a href="/<?= e($p['slug']) ?>/">
          <img src="<?= e(str_replace('-768x512', '-300x200', thumb($p['image']))) ?>" width="300" height="200" alt="" loading="lazy" decoding="async">
          <span class="result-body">
            <span class="card-tag"><?= e(primary_cat($p)) ?></span>
            <strong><?= $hl($p['title']) ?></strong>
            <span class="result-desc"><?= $hl($p['description']) ?></span>
            <span class="card-meta"><?= reading_time($p) ?> min read</span>
          </span>
        </a>
      </li>
      <?php endforeach; ?>
    </ol>
    <?php else: ?>
      <div class="empty-state">
        <p><?= $q === '' ? 'Type a word or phrase above to search every article.' : 'Nothing matched “' . e($q) . '”. Try a single word, or start with one of these:' ?></p>
      </div>
      <div class="grid grid-3">
        <?php foreach (array_slice(featured_posts(), 0, 3) as $p) view('card', ['p' => $p]); ?>
      </div>
    <?php endif; ?>
  </div>
</section>
<?php view('foot'); ?>
