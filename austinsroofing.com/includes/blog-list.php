<?php
// Shared body for /blog/ and /category/general/ (all posts are in "General").
function blog_list(string $h1, string $path, array $crumbs, string $title, string $desc, string $lead): void
{
    page_start(['title' => $title, 'description' => $desc, 'path' => $path, 'crumbs' => $crumbs, 'body_class' => 'page-blog']);
    $items = []; $i = 1;
    $posts = POSTS;
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    foreach ($posts as $slug => $p) {
        $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => abs_url('/blog/' . $slug . '/'), 'name' => $p['h1']];
    }
    add_schema(['@type' => 'CollectionPage', 'url' => abs_url($path), 'name' => $h1, 'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => $items]]);
    page_hero($h1, ['crumbs' => $crumbs, 'eyebrow' => 'Austin Roofing Blog', 'lead' => $lead, 'cta' => false]);
    ?>
<section class="section section--tight">
  <div class="container">
    <?php post_cards(count(POSTS)); ?>
  </div>
</section>
<section class="section section--cream">
  <div class="container">
    <h2 class="section-title">Run the Numbers With Our Free Roofing Tools</h2>
    <?php tool_cards(); ?>
  </div>
</section>
<?php
    cta_band();
    page_end();
}
