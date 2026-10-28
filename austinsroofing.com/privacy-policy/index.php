<?php
require dirname(__DIR__) . '/includes/layout.php';
$crumbs = [['Privacy Policy', '/privacy-policy/']];
page_start([
    'title' => 'Privacy Policy | Austin Roofing',
    'description' => 'How Austin Roofing collects, uses and protects information submitted through austinsroofing.com, including quote requests, analytics and cookies.',
    'path' => '/privacy-policy/', 'crumbs' => $crumbs, 'body_class' => 'page-legal',
]);
page_hero('Privacy Policy', ['crumbs' => $crumbs, 'cta' => false]);
?>
<div class="container layout-sidebar">
  <article class="prose legal">
    <?php readfile(AR_ROOT . '/includes/legal/privacy.html'); ?>
    <h2>Interactive Tools</h2>
    <p>The roofing calculators and quizzes on this website run entirely in your browser. The numbers you enter into them are not sent to or stored by Austin Roofing unless you choose to submit a quote request form.</p>
  </article>
  <?php sidebar(); ?>
</div>
<?php page_end();
