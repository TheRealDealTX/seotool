<?php
/** Article index /blog/ and category archives /category/<slug>/ (paginated). */
defined('RT_APP') || exit;

use RT\Db;
use RT\Seo;

$per = 12;
$pageNo = max(1, (int) ($pageNo ?? 1));
$cat = null;
if (!empty($category)) {
    $cat = Db::one('SELECT * FROM categories WHERE slug = ?', [$category]);
    if (!$cat) {
        rt_not_found();
    }
}
$params = [];
$where = "a.status = 'published'";
if ($cat) {
    $where .= ' AND a.id IN (SELECT article_id FROM article_categories WHERE category_id = :cat)';
    $params['cat'] = (int) $cat['id'];
}
$total = (int) Db::val("SELECT COUNT(*) FROM articles a WHERE {$where}", $params);
$pages = max(1, (int) ceil($total / $per));
if ($pageNo > $pages) {
    rt_not_found();
}
$rows = Db::all("SELECT a.* FROM articles a WHERE {$where} ORDER BY a.published_at DESC LIMIT {$per} OFFSET " . (($pageNo - 1) * $per), $params);
$cats = Db::all("SELECT c.slug, c.name, COUNT(ac.article_id) n FROM categories c JOIN article_categories ac ON ac.category_id = c.id JOIN articles a ON a.id = ac.article_id AND a.status = 'published' GROUP BY c.id ORDER BY c.name");
$base = $cat ? '/category/' . $cat['slug'] . '/' : '/blog/';

$page = [
    'title' => ($cat ? $cat['name'] . ' — Rodeo Guides' : 'Rodeo Guide: Articles for Fans & First-Timers') . ($pageNo > 1 ? ' (page ' . $pageNo . ')' : ''),
    'description' => $cat ? 'Rodeo Texas articles filed under ' . $cat['name'] . '.' : 'How rodeo works, how bull riding is scored, what to wear, Texas rodeo history and more.',
    'canonical' => $base . ($pageNo > 1 ? 'page/' . $pageNo . '/' : ''),
    'jsonld' => [Seo::breadcrumbs(array_filter([['Home', '/'], ['Rodeo guide', '/blog/'], $cat ? [$cat['name'], $base] : null]))],
    'head_extra' => ($pageNo > 1 ? '<link rel="prev" href="' . e($base . ($pageNo > 2 ? 'page/' . ($pageNo - 1) . '/' : '')) . '">' : '')
        . ($pageNo < $pages ? '<link rel="next" href="' . e($base . 'page/' . ($pageNo + 1) . '/') . '">' : ''),
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
?>
<div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">›</span> <?= $cat ? '<a href="/blog/">Rodeo guide</a> <span aria-hidden="true">›</span> ' . e($cat['name']) : 'Rodeo guide' ?></nav>
  <h1><?= e($cat ? $cat['name'] : 'Rodeo guide') ?></h1>
  <?php if ($cats): ?>
    <ul class="quick-chips" aria-label="Categories">
      <li><a class="chip<?= !$cat ? ' is-active' : '' ?>" href="/blog/">All</a></li>
      <?php foreach ($cats as $c): ?><li><a class="chip<?= $cat && $cat['slug'] === $c['slug'] ? ' is-active' : '' ?>" href="/category/<?= e($c['slug']) ?>/"><?= e($c['name']) ?> <span class="chip__n"><?= (int) $c['n'] ?></span></a></li><?php endforeach; ?>
    </ul>
  <?php endif; ?>
  <div class="article-grid">
    <?php foreach ($rows as $a): ?>
      <article class="article-tile">
        <?php if ($a['featured_image']): ?>
          <a href="/<?= e($a['slug']) ?>/" tabindex="-1" aria-hidden="true"><img src="<?= e($a['featured_image']) ?>" alt="" width="<?= (int) ($a['featured_width'] ?: 1200) ?>" height="<?= (int) ($a['featured_height'] ?: 800) ?>" loading="lazy" decoding="async"></a>
        <?php endif; ?>
        <div class="article-tile__body">
          <h2><a href="/<?= e($a['slug']) ?>/"><?= e($a['title']) ?></a></h2>
          <p class="muted"><time datetime="<?= e(substr((string) $a['published_at'], 0, 10)) ?>"><?= e(date('F j, Y', strtotime((string) $a['published_at']))) ?></time></p>
          <p><?= e(excerpt($a['excerpt'] ?: strip_tags($a['content_html']), 150)) ?></p>
        </div>
      </article>
    <?php endforeach; ?>
  </div>
  <?php if ($pages > 1): ?>
    <nav class="pager" aria-label="Pages">
      <?php if ($pageNo > 1): ?><a rel="prev" href="<?= e($base . ($pageNo > 2 ? 'page/' . ($pageNo - 1) . '/' : '')) ?>">‹ Newer</a><?php endif; ?>
      <span class="pager__info">Page <?= $pageNo ?> of <?= $pages ?></span>
      <?php if ($pageNo < $pages): ?><a rel="next" href="<?= e($base . 'page/' . ($pageNo + 1) . '/') ?>">Older ›</a><?php endif; ?>
    </nav>
  <?php endif; ?>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
