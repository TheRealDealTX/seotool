<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
$path = '/privacy-policy/';
$crumbs = [['Home', '/'], ['Privacy Policy', $path]];
page_start([
    'title' => 'Privacy Policy | Sugar Land Public Adjuster',
    'description' => 'How Sugar Land Public Adjuster collects, uses, stores and safeguards information submitted through this website, forms, phone or email.',
    'path' => $path,
    'breadcrumbs' => $crumbs,
]);
page_hero('Privacy Policy', '', $crumbs);
?>
<section class="section">
  <div class="container narrow prose">
<?= file_get_contents(dirname(__DIR__) . '/content/legal/privacy-policy.html') ?>
  </div>
</section>
<?php page_end(); ?>
