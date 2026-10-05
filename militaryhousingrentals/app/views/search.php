<?php
$q = trim(mb_substr((string)($_GET['s'] ?? ''), 0, 100));
$terms = array_filter(preg_split('/\s+/', mb_strtolower($q)));
$match = function ($text) use ($terms) { $t = mb_strtolower($text); foreach ($terms as $w) if (!str_contains($t, $w)) return false; return (bool)$terms; };
$ls = array_values(array_filter(listings(), fn($l) => $match($l['title'] . ' ' . $l['address'] . ' ' . strip_tags($l['description']) . ' ' . (base($l['base'])['name'] ?? '') . ' ' . implode(' ', $l['amenities']))));
$ps = array_values(array_filter(posts(), fn($p) => $match($p['title'] . ' ' . $p['excerpt'] . ' ' . strip_tags(post_html($p['slug'])))));
layout_start(['title' => $q !== '' ? 'Search results for "' . $q . '"' : 'Search', 'description' => 'Search military housing listings and guides.', 'path' => '/', 'robots' => 'noindex, follow']);
?>
<section class="page-hero page-hero-sm">
  <div class="wrap">
    <h1><?= $q !== '' ? 'Results for “' . e($q) . '”' : 'Search' ?></h1>
    <form class="inline-search" action="/" method="get" role="search"><input type="search" name="s" value="<?= e($q) ?>" placeholder="Search listings and guides" aria-label="Search"><button class="btn btn-primary" type="submit"><?= icon('search') ?> Search</button></form>
  </div>
</section>
<section class="section section-tight">
  <div class="wrap">
    <h2><?= count($ls) ?> listing<?= count($ls) === 1 ? '' : 's' ?></h2>
    <?php if ($ls): ?><div class="card-grid"><?php foreach ($ls as $l) echo listing_card($l); ?></div><?php else: ?><p class="muted">No listings matched. <a href="/properties/">Browse all listings</a>.</p><?php endif; ?>
    <h2 class="mt"><?= count($ps) ?> article<?= count($ps) === 1 ? '' : 's' ?></h2>
    <?php if ($ps): ?><div class="card-grid"><?php foreach ($ps as $p) echo post_card($p); ?></div><?php else: ?><p class="muted">No articles matched. <a href="/blog/">Browse the blog</a>.</p><?php endif; ?>
  </div>
</section>
<?php layout_end();
