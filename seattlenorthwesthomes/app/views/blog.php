<?php defined('SNW') || (http_response_code(404) && exit);
$crumbs = [['Blog', '/blog/']];
if ($category) $crumbs[] = [$heading, ''];
partial('page-hero', ['title' => $heading . ($page > 1 ? ' — Page ' . $page : ''), 'crumbs' => $crumbs,
    'lead' => $category ? categories()[$category]['description'] : 'Local advice on buying, selling and living in Seattle — plus our archive of home, renting and Texas market guides.']); ?>
<section class="section tight">
  <div class="wrap">
    <nav class="tag-list cats" aria-label="Blog categories">
      <a href="/blog/"<?= !$category ? ' aria-current="page"' : '' ?>>All</a>
<?php foreach (categories() as $s => $c): ?>
      <a href="/blog/category/<?= $s ?>/"<?= $category === $s ? ' aria-current="page"' : '' ?>><?= e($c['name']) ?></a>
<?php endforeach ?>
    </nav>
    <div class="grid-3">
<?php foreach ($items as $p) partial('post-card', ['p' => $p]); ?>
    </div>
<?php if ($pages > 1): ?>
    <nav class="pager" aria-label="Pagination">
<?php for ($i = 1; $i <= $pages; $i++): $href = $i === 1 ? $base : $base . 'page/' . $i . '/'; ?>
      <a href="<?= $href ?>"<?= $i === $page ? ' aria-current="page"' : '' ?>><?= $i ?></a>
<?php endfor ?>
    </nav>
<?php endif ?>
  </div>
</section>
