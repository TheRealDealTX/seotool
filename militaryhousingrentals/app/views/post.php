<?php
$p = $post;
$html = post_html($p['slug']);
// Interactive widgets embedded in specific guides
if ($p['slug'] === 'bah-explained-military-housing-allowance') $html = preg_replace('#(<h2[^>]*>A Simple BAH Budgeting Rule</h2>)#', widget_bah() . '$1', $html, 1);
if ($p['slug'] === 'pcs-moving-checklist') $html = preg_replace('#(<h2[^>]*>As Soon as You Have Orders</h2>)#', widget_pcs() . '$1', $html, 1);
// Give every h2 an id for the table of contents
$toc = [];
$html = preg_replace_callback('#<h2([^>]*)>(.*?)</h2>#s', function ($m) use (&$toc) {
    if (preg_match('/id="([^"]+)"/', $m[1], $id)) $slug = $id[1];
    else { $slug = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower(html_entity_decode(strip_tags($m[2])))), '-'); $m[1] .= ' id="' . $slug . '"'; }
    $toc[] = [$slug, html_entity_decode(strip_tags($m[2]))];
    return '<h2' . $m[1] . '>' . $m[2] . '</h2>';
}, $html);
// Yoast FAQ block -> FAQPage schema
$faq = [];
if (preg_match_all('#<strong class="schema-faq-question">(.*?)</strong>\s*<p class="schema-faq-answer">(.*?)</p>#s', $html, $mm, PREG_SET_ORDER)) {
    foreach ($mm as $q) $faq[] = ['@type' => 'Question', 'name' => trim(strip_tags($q[1])), 'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(strip_tags($q[2]))]];
}
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], ['Blog', '/blog/'], [$p['title'], null]]);
$schema = [$crumb_schema, [
    '@type' => 'BlogPosting', 'headline' => $p['title'], 'description' => $p['seo_desc'] ?: $p['excerpt'],
    'datePublished' => $p['date'], 'dateModified' => $p['modified'], 'mainEntityOfPage' => abs_url('/' . $p['slug'] . '/'),
    'image' => abs_url($p['image']['src'] ?? cfg('og_image')), 'author' => ['@type' => 'Organization', 'name' => cfg('name'), 'url' => abs_url('/')],
    'publisher' => ['@id' => abs_url('/#organization')],
]];
if ($faq) $schema[] = ['@type' => 'FAQPage', 'mainEntity' => $faq];
$related = array_values(array_filter(posts(), fn($o) => $o['slug'] !== $p['slug']));
$related = array_slice($related, 0, 3);
layout_start([
    'title' => $p['title'],
    'description' => $p['seo_desc'] ?: $p['excerpt'],
    'path' => '/' . $p['slug'] . '/',
    'image' => $p['image']['src'] ?? null,
    'og_type' => 'article',
    'nav' => '/blog/',
    'progress' => true,
    'head_extra' => '<meta property="article:published_time" content="' . e($p['date']) . '">' . "\n" . '<meta property="article:modified_time" content="' . e($p['modified']) . '">',
    'schema' => $schema,
]);
?>
<article class="post">
  <header class="post-hero">
    <div class="wrap narrow">
      <?= $crumbs ?>
      <h1><?= e($p['title']) ?></h1>
      <p class="post-meta"><?= icon('calendar') ?> <?= e(fmt_date($p['date'])) ?> <span>&middot;</span> <?= icon('clock') ?> <?= reading_time($p['slug']) ?> min read</p>
    </div>
    <?php if (!empty($p['image'])): ?><div class="wrap post-cover"><img src="<?= e($p['image']['src']) ?>" alt="<?= e($p['image']['alt'] ?: $p['title']) ?>" width="1200" height="630" fetchpriority="high"></div><?php endif; ?>
  </header>
  <div class="wrap post-layout">
    <aside class="toc" aria-label="On this page">
      <?php if (count($toc) > 2): ?>
      <details open data-toc>
        <summary><?= icon('list') ?> On this page</summary>
        <ol><?php foreach ($toc as [$id, $t]): ?><li><a href="#<?= e($id) ?>"><?= e($t) ?></a></li><?php endforeach; ?></ol>
      </details>
      <?php endif; ?>
      <div class="share-box">
        <span class="muted small">Share this guide</span>
        <button type="button" class="btn btn-light btn-sm" data-share data-title="<?= e($p['title']) ?>"><?= icon('share') ?> Share</button>
      </div>
    </aside>
    <div class="prose post-body"><?= $html ?></div>
  </div>
</article>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">Keep reading</p><h2>More guides for military families</h2></div><a class="link-arrow" href="/blog/">All articles <?= icon('arrow') ?></a></div>
    <div class="card-grid"><?php foreach ($related as $o) echo post_card($o); ?></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">Ready to look?</p><h2>Recently listed properties</h2></div><a class="link-arrow" href="/properties/">All listings <?= icon('arrow') ?></a></div>
    <div class="card-grid"><?php foreach (newest_listings(3) as $l) echo listing_card($l); ?></div>
  </div>
</section>
<?php layout_end();
