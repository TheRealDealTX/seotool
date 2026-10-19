<?php
$page = [
    'title' => 'Page Not Found | ' . SITE_NAME,
    'description' => 'The page you were looking for has moved. Explore insurance adjuster salary guides, calculators and career advice.',
    'path' => '/404/',
];
require __DIR__ . '/header.php';
?>
<section class="page-hero">
  <div class="container">
    <span class="eyebrow">Error 404</span>
    <h1>This claim could not be located</h1>
    <p>The page you requested has moved or never existed. Try one of these instead.</p>
    <div class="hero-actions">
      <a class="btn btn-gold" href="/">Insurance adjuster salary guide <?= icon('arrow', 18) ?></a>
      <a class="btn btn-ghost" href="/salary-calculator/">Salary calculator</a>
      <a class="btn btn-ghost" href="<?= BLOG_BASE ?>">Read the advice blog</a>
    </div>
  </div>
</section>
<?php require __DIR__ . '/footer.php'; ?>
