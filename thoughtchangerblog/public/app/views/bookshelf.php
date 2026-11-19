<?php
$items = bookshelf_items();
view('head', ['meta' => [
    'title' => 'Recommended Reads: Books That Change How You Think - Thought Changer',
    'description' => 'The Thought Changer bookshelf: the books on mindset, meaning, and intentional living we recommend most, gathered from every article.',
    'canonical' => '/recommended-reads/', 'bodyClass' => 'bookshelf',
    'schema' => [['@type' => 'CollectionPage', '@id' => SITE_URL . '/recommended-reads/#webpage', 'url' => SITE_URL . '/recommended-reads/', 'name' => 'Recommended Reads', 'isPartOf' => ['@id' => SITE_URL . '/#website']]],
]]);
$byTheme = ['Mindset' => [], 'Quotes' => [], 'General' => []];
foreach ($items as $it) {
    $p = post_by_slug($it['from'][0]);
    $byTheme[primary_cat($p) === 'Reflections' ? 'General' : primary_cat($p)][] = $it;
}
$labels = ['Mindset' => 'For a Stronger Mindset', 'Quotes' => 'Words Worth Keeping', 'General' => 'Life, Meaning & Perspective'];
?>
<section class="page-hero">
  <div class="wrap-narrow">
    <span class="eyebrow center-block reveal">The Thought Changer Bookshelf</span>
    <h1 class="page-title reveal">Recommended Reads</h1>
    <p class="page-lede reveal">Every book we’ve recommended across the site, in one place. These are the reads that sit behind our articles—the ones that changed how we think about time, attention, purpose, and growth.</p>
  </div>
</section>
<?php foreach ($byTheme as $k => $list): if (!$list) continue; ?>
<section class="band band-tight">
  <div class="wrap">
    <?php view('products', ['products' => $list, 'heading' => $labels[$k], 'intro' => 'Recommended in our ' . ($k === 'General' ? 'reflections' : strtolower($k) . ' articles') . '.', 'showFrom' => true]); ?>
  </div>
</section>
<?php endforeach; ?>
<?php view('foot'); ?>
