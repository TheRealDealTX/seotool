<?php
/** @var array $tool */
$copy = load_content('tools', $tool['slug']) ?? [];
$h1 = $copy['h1'] ?? $tool['name'];
[$body, $toc] = add_heading_ids(render_shortcodes($copy['body'] ?? ''));
$faqs = $copy['faqs'] ?? [];
$cat = tool_categories()[$tool['cat']];
$crumbs = [['Home', '/'], ['Tools', '/tools'], [$cat[0], '/tools#' . $tool['cat']], [$tool['name'], '/' . $tool['slug']]];
$schema = [
    ['@type' => 'WebApplication', 'name' => $h1, 'url' => abs_url('/' . $tool['slug']), 'applicationCategory' => 'EducationalApplication', 'operatingSystem' => 'Any (web browser)', 'browserRequirements' => 'Requires JavaScript', 'description' => $copy['description'] ?? $tool['short'], 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'publisher' => ['@id' => SITE_URL . '/#org']],
    breadcrumb_schema($crumbs),
];
if ($faqs) $schema[] = faq_schema($faqs);
$picks = [
  'grades' => ['ti-30xs', 'academic-planner'], 'gpa' => ['academic-planner', 'straight-a-book'], 'teachers' => ['teacher-gradebook', 'grading-pens'],
  'test-prep' => ['sat-study-guide', 'act-prep-guide'], 'math' => ['ti-84-plus-ce', 'casio-fx-991ex'], 'study' => ['visual-timer', 'noise-cancelling-headphones'],
][$tool['cat']];
page_start([
    'title' => $copy['meta_title'] ?? ($tool['name'] . ' | ' . SITE_NAME),
    'description' => $copy['description'] ?? $tool['short'],
    'path' => '/' . $tool['slug'], 'schema' => $schema, 'tools_js' => true, 'body_class' => 'page-tool',
]);
?>
<section class="page-hero">
  <div class="hero-bg" aria-hidden="true"><div class="blob blob-1"></div><div class="blob blob-2"></div></div>
  <div class="wrap">
    <?= breadcrumbs_html($crumbs) ?>
    <span class="chip"><?= icon($tool['icon'], 'ic ic-xs') ?> <?= e($cat[0]) ?></span>
    <h1 style="margin-top:12px"><?= e($h1) ?></h1>
    <?php if (!empty($copy['lead'])): ?><p class="lead"><?= e($copy['lead']) ?></p><?php endif; ?>
  </div>
</section>
<div class="wrap tool-layout">
  <div class="tool-main">
    <div class="reveal in"><?php $tag = 'h2'; include ROOT . '/widgets/' . $tool['slug'] . '.php'; ?></div>
    <p class="note" style="display:flex;gap:8px;align-items:center"><?= icon('shield', 'ic ic-xs') ?> Private by design: calculations run in your browser and entries are saved only on this device.</p>
    <?php if ($toc): ?>
    <details class="toc-mobile" style="margin-top:28px"><summary>On this page</summary><ol><?php foreach ($toc as [$id, $t]): ?><li><a href="#<?= e($id) ?>"><?= e($t) ?></a></li><?php endforeach; ?></ol></details>
    <?php endif; ?>
    <article class="prose" style="margin-top:20px"><?= $body ?></article>
    <?= faqs_html($faqs) ?>
  </div>
  <aside class="sidebar" aria-label="Related">
    <div class="side-card"><h3>Related calculators</h3><ul class="side-links">
      <?php foreach (tool_related($tool['slug'], 6) as $s): $m = tool_meta($s); ?><li><a href="/<?= e($s) ?>"><?= icon($m['icon']) ?> <?= e($m['name']) ?></a></li><?php endforeach; ?>
    </ul></div>
    <div class="side-card"><h3>Share this tool</h3><div class="share-row"><button type="button" class="btn btn-ghost btn-sm" data-share><?= icon('copy', 'ic ic-xs') ?> Share / copy link</button><button type="button" class="btn btn-ghost btn-sm" data-print><?= icon('print', 'ic ic-xs') ?> Print</button></div></div>
    <div class="side-card"><h3>Student picks</h3><?= product_grid([$picks[0]]) ?></div>
  </aside>
</div>
<?php
$rel = array_filter(articles(), fn($a) => in_array($tool['slug'], $a['related_tools'] ?? []));
if ($rel): ?>
<section class="section section-alt" style="padding-top:50px"><div class="wrap">
  <div class="section-head"><span class="kicker">Learn more</span><h2>Guides for this calculator</h2></div>
  <div class="post-grid"><?php foreach (array_slice($rel, 0, 3) as $a) include ROOT . '/templates/partials/post-card.php'; ?></div>
</div></section>
<?php endif;
page_end();
