<?php
/** Blog index with search, category filter, and pagination (?pg=2, ?q=, ?cat=). */
$all = all_content('posts');
$q = trim((string) ($_GET['q'] ?? ''));
$cat = trim((string) ($_GET['cat'] ?? ''));
$cats = [];
foreach ($all as $p) { $c = $p['category'] ?? 'Insurance Claims'; $cats[$c] = ($cats[$c] ?? 0) + 1; }
ksort($cats);
$list = array_values(array_filter($all, function ($p) use ($q, $cat) {
    if ($cat !== '' && ($p['category'] ?? '') !== $cat) return false;
    if ($q !== '') {
        $hay = mb_strtolower($p['title'] . ' ' . ($p['description'] ?? '') . ' ' . strip_tags($p['body'] ?? ''));
        foreach (preg_split('/\s+/', mb_strtolower($q)) as $w) { if ($w !== '' && mb_strpos($hay, $w) === false) return false; }
    }
    return true;
}));
$per = 9;
$pages = max(1, (int) ceil(count($list) / $per));
$pg = min($pages, max(1, (int) ($_GET['pg'] ?? 1)));
$featured = ($q === '' && $cat === '' && $pg === 1 && $list) ? array_shift($list) : null;
$slice = array_slice($list, ($pg - 1) * $per, $per);
$qs = function (array $extra) use ($q, $cat) { $a = array_filter(['q' => $q, 'cat' => $cat] + []); return '?' . http_build_query(array_merge($a, $extra)); };
component('page-hero', ['page' => $page]);
?>
<section class="section">
  <div class="container">
    <form class="blog-search" action="/blog/" method="get" role="search">
      <label class="sr-only" for="blog-q">Search articles</label>
      <input id="blog-q" type="search" name="q" value="<?= e($q) ?>" placeholder="Search articles: hail, denied claim, appraisal…">
      <button class="btn btn-gold" type="submit">Search</button>
    </form>
    <div class="chip-list chip-list-center" aria-label="Categories">
      <a class="chip" href="/blog/"<?= $cat === '' ? ' aria-current="page" style="background:var(--navy);color:#fff"' : '' ?>>All (<?= count($all) ?>)</a>
      <?php foreach ($cats as $c => $n): ?><a class="chip" href="/blog/?cat=<?= e(rawurlencode($c)) ?>"<?= $cat === $c ? ' aria-current="page" style="background:var(--navy);color:#fff"' : '' ?>><?= e($c) ?> (<?= $n ?>)</a><?php endforeach; ?>
    </div>
    <?php if ($q !== ''): ?><p class="center muted"><?= count($list) ?> result<?= count($list) === 1 ? '' : 's' ?> for &ldquo;<?= e($q) ?>&rdquo; &middot; <a href="/blog/">Clear search</a></p><?php endif; ?>
    <?php if ($featured): ?>
    <article class="featured-post reveal">
      <a class="featured-post-media" href="<?= e($featured['path']) ?>" tabindex="-1" aria-hidden="true"><?= img($featured['image'] ?? '', '', ['sizes' => '(max-width: 860px) 100vw, 660px']) ?></a>
      <div class="featured-post-body">
        <p class="post-card-meta"><span><?= e($featured['category'] ?? '') ?></span> <time datetime="<?= e(iso_date($featured['date'])) ?>"><?= e(format_date($featured['date'])) ?></time></p>
        <h2><a href="<?= e($featured['path']) ?>" style="color:var(--navy);text-decoration:none"><?= e($featured['title']) ?></a></h2>
        <p class="muted"><?= e($featured['excerpt'] ?? $featured['description'] ?? '') ?></p>
        <p class="small muted">By Joseph Dittman, Public Adjuster</p>
        <a class="btn btn-gold" href="<?= e($featured['path']) ?>">Read the article</a>
      </div>
    </article>
    <?php endif; ?>
    <?php if ($slice): ?>
    <div class="card-grid card-grid-posts"><?php foreach ($slice as $post) component('post-card', ['post' => $post]); ?></div>
    <?php elseif (!$featured): ?>
    <p class="center">No articles found. Try another search or <a href="/blog/">browse all articles</a>.</p>
    <?php endif; ?>
    <?php if ($pages > 1): ?>
    <nav class="pager" aria-label="Blog pages">
      <?php for ($i = 1; $i <= $pages; $i++): ?><a href="/blog/<?= e($i > 1 ? $qs(['pg' => $i]) : ($q !== '' || $cat !== '' ? $qs([]) : '')) ?>"<?= $i === $pg ? ' aria-current="page"' : '' ?>><?= $i ?></a><?php endfor; ?>
    </nav>
    <?php endif; ?>
    <?php component('cta-band'); ?>
  </div>
</section>
