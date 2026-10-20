<?php
/** Blog article. */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
$related = [];
foreach (all_content('posts') as $p) {
    if ($p['path'] !== $page['path']) {
        $related[] = $p;
    }
}
// Prefer explicitly related posts, then same category, then newest.
$pref = $page['related'] ?? [];
usort($related, function ($a, $b) use ($pref, $page) {
    $sa = (in_array($a['path'], $pref, true) ? 2 : 0) + (($a['category'] ?? '') === ($page['category'] ?? '') ? 1 : 0);
    $sb = (in_array($b['path'], $pref, true) ? 2 : 0) + (($b['category'] ?? '') === ($page['category'] ?? '') ? 1 : 0);
    return $sb <=> $sa ?: strcmp($b['date'], $a['date']);
});
$related = array_slice($related, 0, 3);
?>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?php if (!empty($page['image'])): ?>
      <figure class="post-featured"><?= img($page['image'], $page['image_alt'] ?? $page['title'], ['eager' => true, 'sizes' => '(max-width: 900px) 100vw, 760px']) ?></figure>
      <?php endif; ?>
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
      <?php if (!empty($page['sources'])): ?>
      <section class="sources">
        <h2 id="sources">Sources and further reading</h2>
        <ul>
          <?php foreach ($page['sources'] as [$label, $href]): ?><li><a href="<?= e($href) ?>" target="_blank" rel="noopener"><?= e($label) ?></a></li><?php endforeach; ?>
        </ul>
      </section>
      <?php endif; ?>
      <?php component('cta-band'); ?>
      <?php component('author-box'); ?>
      <p class="post-disclaimer">This article is general information about property insurance claims in Texas, not legal advice, and not a promise of any coverage or outcome. Your policy language and the facts of your loss control your claim.</p>
    </article>
    <aside class="sidebar">
      <?php include MPA_ROOT . '/templates/sidebar.php'; ?>
    </aside>
  </div>
</section>
<?php if ($related): ?>
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Related articles</h2>
    <div class="card-grid card-grid-posts">
      <?php foreach ($related as $post) component('post-card', ['post' => $post]); ?>
    </div>
  </div>
</section>
<?php endif; ?>
