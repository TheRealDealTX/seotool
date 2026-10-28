<?php
require dirname(__DIR__) . '/includes/layout.php';
$crumbs = [['Terms of Service', '/terms-of-service/']];
page_start([
    'title' => 'Terms of Service | Austin Roofing',
    'description' => 'Terms of Service for austinsroofing.com: website use, free roofing quotes, service agreements, warranties, calculators and Texas governing law.',
    'path' => '/terms-of-service/', 'crumbs' => $crumbs, 'body_class' => 'page-legal',
]);
page_hero('Terms of Service', ['crumbs' => $crumbs, 'cta' => false]);
?>
<div class="container layout-sidebar">
  <article class="prose legal">
    <?php readfile(AR_ROOT . '/includes/legal/terms.html'); ?>
    <h2>Calculators and Cost Estimates</h2>
    <p>Cost ranges, roofing calculators, quizzes and other tools on this website provide general planning information only. They are not quotes, offers or professional assessments of any specific roof. Pricing for your project is provided only in a written estimate after an inspection.</p>
  </article>
  <?php sidebar(); ?>
</div>
<?php page_end();
