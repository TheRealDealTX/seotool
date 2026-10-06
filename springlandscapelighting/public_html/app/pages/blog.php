<?php defined('SLT') || exit;
$cat = $GLOBALS['CAT'] ?? null; $page = $GLOBALS['PAGE_N'] ?? 1; $per = 9;
$posts = POSTS; uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']) ?: strcmp($a['title'], $b['title']));
if ($cat) $posts = array_filter($posts, fn($p) => $p['cat'] === $cat);
$pages = max(1, (int)ceil(count($posts) / $per));
if ($page > $pages) { not_found(); }
$list = array_slice($posts, ($page - 1) * $per, $per, true);
$base = $cat ? '/category/' . $cat . '/' : '/blog/';
$title = $cat ? CATEGORIES[$cat]['name'] : 'Landscape Lighting Blog';
page_hero(['title' => e($title), 'eyebrow' => $cat ? 'Category' : 'Ideas, guides & tips', 'sub' => $cat ? e(CATEGORIES[$cat]['desc']) : 'Lighting ideas, planning guides, cost advice and maintenance tips for homeowners in Spring, TX, from the Spring Landscape Lighting team.',
    'crumbs' => $cat ? [['Home', '/'], ['Blog', '/blog/'], [CATEGORIES[$cat]['name'], null]] : [['Home', '/'], ['Blog', null]]]);
add_schema(['@type' => 'ItemList', 'itemListElement' => array_values(array_map(fn($k, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url('/' . $k . '/')], array_keys($list), range(0, count($list) - 1)))]);
?>
<section class="sec" style="padding-top:30px">
  <div class="wrap">
    <nav class="cats" aria-label="Categories"><a href="/blog/"<?= !$cat ? ' class="is-on"' : '' ?>>All</a><?php foreach (CATEGORIES as $k => $c) echo '<a href="/category/' . $k . '/"' . ($cat === $k ? ' class="is-on"' : '') . '>' . e($c['name']) . '</a>'; ?></nav>
    <?php $first = true; if (!$cat && $page === 1): $k = array_key_first($list); $p = array_shift($list); ?>
      <div style="margin-bottom:22px"><?= str_replace('class="pcard ', 'class="pcard pcard--feat ', post_card($k, $p)) ?></div>
    <?php endif; ?>
    <div class="grid-3"><?php foreach ($list as $k => $p) echo post_card($k, $p); ?></div>
    <?php if ($pages > 1): ?><nav class="pager" aria-label="Pagination"><?php for ($i = 1; $i <= $pages; $i++) echo $i === $page ? '<span>' . $i . '</span>' : '<a href="' . ($i === 1 ? $base : $base . 'page/' . $i . '/') . '">' . $i . '</a>'; ?></nav><?php endif; ?>
  </div>
</section>
<section class="sec sec--forest">
  <div class="wrap">
    <?php section_head('Free planning tools', 'Run the numbers for your own property'); ?>
    <div class="grid-3"><?php $i = 0; foreach (TOOLS as $k => $t) { if ($i >= 6) break; echo tool_card($k, $t, $i++); } ?></div>
  </div>
</section>
<?php cta_band(); ?>
