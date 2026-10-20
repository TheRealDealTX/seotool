<?php
/** Generic page: hero + article body + optional FAQs. */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
?>
<section class="section section-article">
  <div class="container<?= !empty($page['wide']) ? '' : ' with-sidebar' ?>">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
      <?php if (empty($page['no_cta'])) component('cta-band'); ?>
    </article>
    <?php if (empty($page['wide'])): ?>
    <aside class="sidebar">
      <?php include MPA_ROOT . '/templates/sidebar.php'; ?>
    </aside>
    <?php endif; ?>
  </div>
</section>
