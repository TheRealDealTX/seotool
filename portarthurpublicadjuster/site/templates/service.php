<?php
/** Insurance claim service page. */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
$others = array_filter(service_cards(), fn($c) => $c[0] !== $page['path']);
$relatedPosts = [];
foreach ($page['related_posts'] ?? [] as $rp) {
    $p = find_content($rp);
    if ($p) {
        $relatedPosts[] = $p;
    }
}
?>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?php if (!empty($page['image'])): ?>
      <figure class="post-featured"><?= img($page['image'], $page['image_alt'] ?? $page['title'], ['eager' => true, 'sizes' => '(max-width: 900px) 100vw, 760px']) ?></figure>
      <?php endif; ?>
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
      <?php component('cta-band', ['heading' => $page['cta_heading'] ?? null]); ?>
    </article>
    <aside class="sidebar">
      <?php include MPA_ROOT . '/templates/sidebar.php'; ?>
    </aside>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Free Claim Review</h2>
    <div class="split split-form">
      <div class="split-copy">
        <p class="lead">Tell us about your <?= e(strtolower($page['service_name'] ?? 'property')) ?> claim. A licensed public adjuster will review your situation and explain your options&mdash;there is no cost and no obligation.</p>
        <ul class="check-list">
          <li><?= icon('check', 'icon icon-sm') ?> Review of the policy, estimate, and insurer letters</li>
          <li><?= icon('check', 'icon icon-sm') ?> Plain-English explanation of what may be missing</li>
          <li><?= icon('check', 'icon icon-sm') ?> Honest answer on whether a public adjuster can help</li>
        </ul>
        <?php if ($relatedPosts): ?>
        <h3>Related reading</h3>
        <ul class="link-list">
          <?php foreach ($relatedPosts as $rp): ?><li><a href="<?= e($rp['path']) ?>"><?= e($rp['title']) ?></a></li><?php endforeach; ?>
        </ul>
        <?php endif; ?>
      </div>
      <div class="form-card"><?php component('claim-form', ['context' => $page['title']]); ?></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <h2 class="section-title">Other claim services</h2>
    <div class="chip-list">
      <?php foreach ($others as [$href, $label]): ?><a class="chip" href="<?= e($href) ?>"><?= e($label) ?></a><?php endforeach; ?>
    </div>
  </div>
</section>
