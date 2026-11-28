<?php
/** @var array $article */
$a = $article;
[$body, $toc] = add_heading_ids(render_shortcodes($a['body']));
$faqs = $a['faqs'] ?? [];
$url = '/blog/' . $a['slug'];
$crumbs = [['Home', '/'], ['Blog', '/blog'], [$a['title'], $url]];
$schema = [
    ['@type' => 'BlogPosting', 'headline' => $a['title'], 'description' => $a['description'], 'image' => SITE_URL . '/assets/img/photos/' . $a['hero'] . '.webp', 'datePublished' => $a['date'] . 'T08:00:00-05:00', 'dateModified' => ($a['updated'] ?? $a['date']) . 'T08:00:00-05:00', 'author' => ['@type' => 'Organization', 'name' => $a['author'] ?? 'FGC Editorial Team', 'url' => SITE_URL . '/about-us'], 'publisher' => ['@id' => SITE_URL . '/#org'], 'mainEntityOfPage' => abs_url($url), 'wordCount' => word_count($a['body']), 'articleSection' => $a['category'], 'keywords' => $a['keyword'] ?? ''],
    breadcrumb_schema($crumbs),
];
if ($faqs) $schema[] = faq_schema($faqs);
page_start(['title' => $a['meta_title'] ?? $a['title'], 'description' => $a['description'], 'path' => $url, 'schema' => $schema, 'image' => $a['hero'], 'article' => true, 'body_class' => 'page-article']);
$updated = ($a['updated'] ?? $a['date']) !== $a['date'];
?>
<div class="wrap">
  <header class="article-hero">
    <?= breadcrumbs_html([['Home', '/'], ['Blog', '/blog'], [$a['category'], '/blog']]) ?>
    <h1><?= e($a['title']) ?></h1>
    <div class="article-meta">
      <span class="author"><span class="avatar">FGC</span> <?= e($a['author'] ?? 'FGC Editorial Team') ?></span>
      <span><?= $updated ? 'Updated ' . nice_date($a['updated']) : nice_date($a['date']) ?></span>
      <span><?= read_time($a['body']) ?> min read</span>
      <span class="chip"><?= e($a['category']) ?></span>
    </div>
    <div class="article-cover"><?= photo($a['hero'], $a['hero_alt'] ?? $a['title'], '', false, '(max-width: 1180px) 100vw, 1180px') ?></div>
  </header>
  <div class="article-layout">
    <nav class="toc" aria-label="Table of contents"><h2>Contents</h2><ol><?php foreach ($toc as [$id, $t]): ?><li><a href="#<?= e($id) ?>"><?= e($t) ?></a></li><?php endforeach; ?><?php if ($faqs): ?><li><a href="#faq">FAQs</a></li><?php endif; ?></ol>
      <div class="side-card" style="margin-top:20px"><h3>Try the calculator</h3><ul class="side-links"><?php foreach (array_slice($a['related_tools'] ?? [], 0, 3) as $s): $m = tool_meta($s); if (!$m) continue; ?><li><a href="/<?= e($s) ?>"><?= icon($m['icon']) ?> <?= e($m['name']) ?></a></li><?php endforeach; ?></ul></div>
    </nav>
    <div style="min-width:0">
      <details class="toc-mobile"><summary>In this guide (<?= count($toc) ?> sections)</summary><ol><?php foreach ($toc as [$id, $t]): ?><li><a href="#<?= e($id) ?>"><?= e($t) ?></a></li><?php endforeach; ?></ol></details>
      <article class="prose"><?= $body ?></article>
      <?= faqs_html($faqs) ?>
      <div class="author-box"><span class="avatar">FGC</span><div><strong><?= e($a['author'] ?? 'FGC Editorial Team') ?></strong><p>Our editorial team writes practical, fact-checked guides on grades, GPA and test scores for students, parents and teachers. Spotted an error? <a href="/contact">Let us know</a>.</p></div></div>
      <div class="share-row" style="margin-bottom:30px"><button type="button" class="btn btn-ghost btn-sm" data-share><?= icon('copy', 'ic ic-xs') ?> Share this guide</button><button type="button" class="btn btn-ghost btn-sm" data-print><?= icon('print', 'ic ic-xs') ?> Print</button></div>
    </div>
  </div>
</div>
<section class="section section-alt"><div class="wrap">
  <div class="section-head"><span class="kicker">Keep reading</span><h2>Related guides</h2></div>
  <div class="post-grid"><?php
    $more = array_filter(articles(), fn($x) => $x['slug'] !== $a['slug']);
    uasort($more, fn($x, $y) => ($y['category'] === $a['category']) <=> ($x['category'] === $a['category']));
    foreach (array_slice($more, 0, 3) as $a2) { $a = $a2; include ROOT . '/templates/partials/post-card.php'; } ?></div>
</div></section>
<?php page_end();
