<?php
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
?>
<section class="section section-alt">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">16 claim services</p><h2>Property Insurance Claim Services</h2><p>Choose a claim type to learn about documentation, common insurer disputes, and how a public adjuster can help.</p></div>
    <?php component('services-grid'); ?>
  </div>
</section>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
      <?php component('cta-band'); ?>
    </article>
    <aside class="sidebar"><?php include MPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
