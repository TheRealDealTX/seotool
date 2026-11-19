<?php
/** @var string $kind blog|Mindset|Quotes|General  @var int $page */
$cfg = [
    'blog'    => ['base' => '/blog/', 'h1' => 'All Articles', 'title' => 'Blog', 'desc' => 'Every Thought Changer article in one place—reflections on mindset, meaning, quotes, and intentional living, one thought at a time.', 'intro' => 'Reflections on the everyday moments, phrases, and metaphors that shape how we think. Start anywhere—each piece stands on its own.'],
    'Mindset' => ['base' => '/mindset/', 'h1' => 'Mindset', 'title' => 'Mindset', 'desc' => 'Mindset shapes how we interpret everything—what we notice, how we respond, and what we carry forward.', 'intro' => 'Mindset shapes how we interpret everything—what we notice, how we respond, and what we carry forward. The posts collected here explore the subtle patterns of thought that influence daily choices and long-term direction. Not to offer answers, but to invite awareness.'],
    'Quotes'  => ['base' => '/quotes/', 'h1' => 'Quotes', 'title' => 'Quotes', 'desc' => 'The quotes collected here aren’t meant to rush you forward, but to pause you—offering subtle shift in how you see something familiar.', 'intro' => 'Words have a way of finding us when we’re ready. The quotes collected here aren’t meant to rush you forward, but to pause you—offering perspective, clarity, or a subtle shift in how you see something familiar. Read slowly. Let one line stay with you longer than the rest.'],
    'General' => ['base' => '/category/general/', 'h1' => 'General', 'title' => 'General Archives', 'desc' => 'General reflections from Thought Changer on life, meaning, perspective, and the small shifts that change how we live.', 'intro' => 'Reflections on life, meaning, and perspective—the everyday lessons that don’t fit neatly in one box.'],
][$kind];
$list = $kind === 'blog' ? posts() : posts_in($kind);
$per = 60;
$pages = max(1, (int) ceil(count($list) / $per));
if ($page > $pages) { http_response_code(404); view('404'); return; }
$items = array_slice($list, ($page - 1) * $per, $per);
$url = $cfg['base'] . ($page > 1 ? 'page/' . $page . '/' : '');
$title = $cfg['title'] . ($page > 1 ? " - Page $page of $pages" : '') . ' - ' . SITE_NAME;
view('head', ['meta' => [
    'title' => $title, 'description' => $cfg['desc'], 'canonical' => $url, 'bodyClass' => 'archive',
    'prev' => $page > 1 ? ($page === 2 ? $cfg['base'] : $cfg['base'] . 'page/' . ($page - 1) . '/') : null,
    'next' => $page < $pages ? $cfg['base'] . 'page/' . ($page + 1) . '/' : null,
    'schema' => [
        ['@type' => 'CollectionPage', '@id' => SITE_URL . $url . '#webpage', 'url' => SITE_URL . $url, 'name' => $title,
         'isPartOf' => ['@id' => SITE_URL . '/#website'],
         'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => array_map(fn($p, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => SITE_URL . '/' . $p['slug'] . '/'], $items, array_keys($items))]],
        ['@type' => 'BreadcrumbList', 'itemListElement' => [
            ['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => SITE_URL . '/'],
            ['@type' => 'ListItem', 'position' => 2, 'name' => $cfg['h1']]]],
    ],
]]);
?>
<section class="page-hero">
  <div class="wrap-narrow">
    <h1 class="page-title reveal"><?= e($cfg['h1']) ?></h1>
    <?php if ($page === 1): ?><p class="page-lede reveal"><?= e($cfg['intro']) ?></p><?php endif; ?>
    <?php if ($kind !== 'Mindset' && $kind !== 'Quotes'): ?>
    <div class="chips reveal"><a href="/blog/"<?= $kind === 'blog' ? ' aria-current="page"' : '' ?>>All</a><a href="/mindset/">Mindset</a><a href="/quotes/">Quotes</a><a href="/category/general/"<?= $kind === 'General' ? ' aria-current="page"' : '' ?>>General</a></div>
    <?php else: ?>
    <div class="chips reveal"><a href="/blog/">All</a><a href="/mindset/"<?= $kind === 'Mindset' ? ' aria-current="page"' : '' ?>>Mindset</a><a href="/quotes/"<?= $kind === 'Quotes' ? ' aria-current="page"' : '' ?>>Quotes</a><a href="/category/general/">General</a></div>
    <?php endif; ?>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="grid grid-4">
      <?php foreach ($items as $i => $p) view('card', ['p' => $p, 'eager' => $i < 4]); ?>
    </div>
    <?php if ($pages > 1): ?>
    <nav class="pager" aria-label="Pagination">
      <?php for ($i = 1; $i <= $pages; $i++): $h = $i === 1 ? $cfg['base'] : $cfg['base'] . 'page/' . $i . '/'; ?>
        <a href="<?= $h ?>"<?= $i === $page ? ' aria-current="page"' : '' ?>><?= $i ?></a>
      <?php endfor; ?>
    </nav>
    <?php endif; ?>
  </div>
</section>
<?php view('foot'); ?>
