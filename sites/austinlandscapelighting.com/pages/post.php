<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$p = post($slug);
$body = $p['body'];
// Embedded tools: <!-- TOOL:slug -->
$body = preg_replace_callback('/<!--\s*TOOL:([a-z0-9-]+)\s*-->/', fn($m) => tool_markup($m[1], true), $body);
$hasTool = str_contains($p['body'], '<!-- TOOL:');
[$body, $toc] = with_heading_ids($body);
$crumbs = [['Home', '/'], ['Blog', '/blog/'], [$p['h1'], $p['path']]];
$all = array_values(posts());
$idx = array_search($slug, array_column($all, 'slug'), true);
$prev = $all[$idx + 1] ?? null;   // older
$next = $idx > 0 ? $all[$idx - 1] : null;  // newer
$more = array_values(array_filter($all, fn($x) => $x['slug'] !== $slug));
$more = array_slice($more, 0, 3);
$page = [
    'title' => $p['title'],
    'description' => $p['description'],
    'path' => $p['path'],
    'image' => $p['image'],
    'active' => '/blog/',
    'og_type' => 'article',
    'published' => $p['published'],
    'modified' => $p['modified'] ?? $p['published'],
    'tools_js' => $hasTool,
    'schema' => array_merge([schema_webpage(['title' => $p['title'], 'description' => $p['description'], 'path' => $p['path'], 'image' => $p['image']], 'ItemPage'), schema_breadcrumb($crumbs), schema_article($p)], !empty($p['faqs']) ? [schema_faq($p['faqs'])] : []),
];
$meta = '<div class="post-hero__meta"><span class="tag">' . e($p['category']) . '</span><span>' . icon('clock', 'ico ico--sm') . ' ' . $p['reading'] . ' min read</span><span>Published <time datetime="' . e($p['published']) . '">' . nice_date($p['published']) . '</time></span>' . (($p['modified'] ?? $p['published']) !== $p['published'] ? '<span>Updated ' . nice_date($p['modified']) . '</span>' : '') . '</div>';
ob_start();
echo sub_hero(['eyebrow' => 'Austin Landscape Lighting blog', 'h1' => e($p['h1']), 'intro' => e($p['excerpt']), 'crumbs' => $crumbs, 'meta' => $meta, 'cta' => false]);
?>
<section class="section">
  <div class="container layout">
    <article class="prose" data-reveal>
      <figure class="post-figure"><?= picture($p['image'], $p['image_alt'] ?? $p['h1'], ['eager' => true, 'sizes' => '(max-width: 960px) 100vw, 60vw']) ?></figure>
      <?= $body ?>
      <?php if (!empty($p['faqs'])): ?>
      <h2 id="faq">Frequently asked questions</h2>
      <?= faq_list($p['faqs'], 'post-faq') ?>
      <?php endif; ?>
      <div class="author-box">
        <img src="/assets/img/brand/austin-landscape-lighting-site-icon.webp" alt="Austin Landscape Lighting" width="64" height="64" loading="lazy">
        <p><strong>Written by the design team at Austin Landscape Lighting.</strong> We design, install and maintain low-voltage LED landscape lighting across Austin and the Hill Country. Questions about your property? <a href="/contact/">Book a free dusk consultation</a> or call <a href="<?= BIZ['phone_href'] ?>"><?= e(BIZ['phone_display']) ?></a>.</p>
      </div>
      <nav class="post-nav" aria-label="More articles">
        <?php if ($prev): ?><a href="<?= e($prev['path']) ?>"><small>Older</small><?= e($prev['h1']) ?></a><?php else: ?><span></span><?php endif; ?>
        <?php if ($next): ?><a href="<?= e($next['path']) ?>" style="text-align:right"><small>Newer</small><?= e($next['h1']) ?></a><?php endif; ?>
      </nav>
    </article>
    <?= sidebar(['toc' => $toc, 'links' => array_map(fn($t) => [$t['name'], $t['path']], array_slice(array_values(tools()), 0, 5)), 'links_title' => 'Free planning tools']) ?>
  </div>
</section>
<section class="section section--alt section--tight">
  <div class="container">
    <?= section_head('Keep reading', 'More from the Austin Landscape Lighting blog', '', 'left') ?>
    <div class="blog-grid"><?php foreach ($more as $m) echo post_card($m); ?></div>
  </div>
</section>
<?= cta_band() ?>
<?php
render_page($page, ob_get_clean());
