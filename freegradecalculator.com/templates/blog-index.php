<?php
$all = articles(); $first = reset($all); $rest = array_slice($all, 1);
$cats = array_values(array_unique(array_map(fn($a) => $a['category'], $all)));
page_start(['title' => 'Grade & GPA Blog – Guides for Students and Teachers', 'description' => 'Step-by-step guides on calculating grades, GPA, weighted vs unweighted scales, SAT scores, curving and standards-based grading — with worked examples.', 'path' => '/blog', 'schema' => [breadcrumb_schema([['Home', '/'], ['Blog', '/blog']])], 'image' => $first['hero'] ?? null]);
?>
<section class="page-hero"><div class="hero-bg" aria-hidden="true"><div class="blob blob-1"></div><div class="blob blob-2"></div></div>
  <div class="wrap"><?= breadcrumbs_html([['Home', '/'], ['Blog', '/blog']]) ?><h1>Grades, GPA &amp; study guides</h1><p class="lead">Plain-English explanations with formulas, worked examples and free calculators to check your work.</p></div>
</section>
<div class="wrap" style="padding-bottom:30px">
  <?php if ($first): ?>
  <a class="post-feature reveal in" href="/blog/<?= e($first['slug']) ?>"><?= photo($first['hero'], $first['hero_alt'] ?? '', '', false, '(max-width: 860px) 100vw, 640px') ?>
    <div class="pc-body"><div class="pc-meta"><span class="chip">Latest · <?= e($first['category']) ?></span><span><?= nice_date($first['date']) ?></span></div><h2><?= e($first['title']) ?></h2><p><?= e($first['excerpt'] ?? '') ?></p><span class="btn btn-primary btn-sm" style="align-self:flex-start">Read guide <?= icon('arrow', 'ic ic-xs') ?></span></div></a>
  <?php endif; ?>
  <div class="filter-bar" role="group" aria-label="Filter by topic"><button type="button" data-cat="all" aria-pressed="true">All topics</button><?php foreach ($cats as $c): ?><button type="button" data-cat="<?= e(slugify($c)) ?>" aria-pressed="false"><?= e($c) ?></button><?php endforeach; ?></div>
  <div class="post-grid">
    <?php foreach ($rest as $a): ?><div data-tool-card data-cat="<?= e(slugify($a['category'])) ?>" style="display:flex"><?php include ROOT . '/templates/partials/post-card.php'; ?></div><?php endforeach; ?>
  </div>
</div>
<?php page_end();
