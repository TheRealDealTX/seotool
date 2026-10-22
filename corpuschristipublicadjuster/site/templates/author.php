<?php
$toc = [];
$body = prepared_body($page, $toc);
$posts = all_content('posts');
?>
<section class="page-hero">
  <?php component('aurora'); ?>
  <div class="container page-hero-inner" style="max-width:var(--container)">
    <?php component('breadcrumbs', ['page' => $page]); ?>
    <div class="author-hero">
      <img src="/assets/img/joseph-dittman.webp" alt="Joseph Dittman, Texas public adjuster" width="220" height="220" fetchpriority="high">
      <div>
        <p class="eyebrow eyebrow-gold">Author &amp; Public Adjuster</p>
        <h1><?= e($page['h1'] ?? $page['title']) ?></h1>
        <p class="page-hero-lead"><?= e($page['lead'] ?? 'Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness.') ?></p>
        <div class="hero-actions"><a class="btn btn-gold" href="/free-claim-review/">Request a Free Claim Review</a><a class="btn btn-outline-light" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_short')) ?></a><a class="btn btn-outline-light" href="mailto:<?= e(cfg('author_email')) ?>"><?= icon('mail', 'icon icon-sm') ?> Email Joseph directly</a></div>
        <p class="small" style="margin-top:14px;color:#b9c6d3">Direct email: <a href="mailto:<?= e(cfg('author_email')) ?>" style="color:var(--gold)"><?= e(cfg('author_email')) ?></a></p>
      </div>
    </div>
  </div>
  <?php component('waves'); ?>
</section>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
    </article>
    <aside class="sidebar"><?php include CCPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Articles by Joseph Dittman (<?= count($posts) ?>)</h2>
    <div class="card-grid card-grid-posts"><?php foreach ($posts as $post) component('post-card', ['post' => $post]); ?></div>
  </div>
</section>
