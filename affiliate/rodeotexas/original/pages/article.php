<?php
/** Single article at its original WordPress URL: /<slug>/ */
defined('RT_APP') || exit;

use RT\Db;
use RT\EventRepo;
use RT\Seo;
use RT\View;

$a = $article;
$cats = Db::all('SELECT c.slug, c.name FROM categories c JOIN article_categories ac ON ac.category_id = c.id WHERE ac.article_id = ? ORDER BY c.name', [$a['id']]);
$more = Db::all("SELECT slug, title FROM articles WHERE status = 'published' AND id <> ? ORDER BY published_at DESC LIMIT 5", [$a['id']]);
$upcoming = EventRepo::upcoming(3);

$page = [
    'title' => $a['seo_title'] ?: $a['title'],
    'description' => $a['meta_description'] ?: excerpt($a['excerpt'] ?: strip_tags($a['content_html']), 158),
    'canonical' => '/' . $a['slug'] . '/',
    'og_type' => 'article',
    'og_image' => $a['featured_image'] ?: '/assets/img/og-default.png',
    'og_image_alt' => $a['featured_alt'] ?: $a['title'],
    'jsonld' => [Seo::article($a), Seo::breadcrumbs([['Home', '/'], ['Rodeo guide', '/blog/'], [$a['title'], '/' . $a['slug'] . '/']])],
    'head_extra' => '<meta property="article:published_time" content="' . e(gmdate('c', strtotime($a['published_at'] . ' UTC'))) . '">'
        . '<meta property="article:modified_time" content="' . e(gmdate('c', strtotime($a['updated_at'] . ' UTC'))) . '">',
    'body_class' => 'page-article',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
?>
<article class="wrap article">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">›</span> <a href="/blog/">Rodeo guide</a> <span aria-hidden="true">›</span> <span><?= e($a['title']) ?></span></nav>
  <header class="article__head">
    <h1><?= e($a['title']) ?></h1>
    <p class="muted">
      <time datetime="<?= e(substr((string) $a['published_at'], 0, 10)) ?>"><?= e(date('F j, Y', strtotime((string) $a['published_at']))) ?></time>
      <?php foreach ($cats as $c): ?> · <a href="/category/<?= e($c['slug']) ?>/"><?= e($c['name']) ?></a><?php endforeach; ?>
    </p>
  </header>
  <?php if ($a['featured_image']): ?>
    <img class="article__hero" src="<?= e($a['featured_image']) ?>" alt="<?= e($a['featured_alt']) ?>" width="<?= (int) ($a['featured_width'] ?: 1200) ?>" height="<?= (int) ($a['featured_height'] ?: 800) ?>" fetchpriority="high" decoding="async">
  <?php endif; ?>
  <div class="article__layout">
    <div class="prose article__body">
      <?= $a['content_html'] /* trusted HTML written by site administrators */ ?>
    </div>
    <aside class="article__side">
      <?php if ($upcoming): ?>
        <div class="side-card"><h2>Upcoming Texas rodeos</h2>
          <div class="event-list event-list--compact"><?php foreach ($upcoming as $ev) { echo View::eventCard($ev, true); } ?></div>
          <p><a class="link-more" href="/rodeos/">See the full schedule →</a></p></div>
      <?php endif; ?>
      <?php if ($more): ?>
        <div class="side-card"><h2>More rodeo guides</h2><ul class="link-list"><?php foreach ($more as $m): ?><li><a href="/<?= e($m['slug']) ?>/"><?= e($m['title']) ?></a></li><?php endforeach; ?></ul></div>
      <?php endif; ?>
    </aside>
  </div>
</article>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
