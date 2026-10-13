<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
$path = '/terms-of-use/';
$crumbs = [['Home', '/'], ['Terms of Use', $path]];
page_start([
    'title' => 'Terms of Use | Sugar Land Public Adjuster',
    'description' => 'The terms and conditions that govern your use of the Sugar Land Public Adjuster website.',
    'path' => $path,
    'breadcrumbs' => $crumbs,
]);
page_hero('Terms of Use', '', $crumbs);
?>
<section class="section">
  <div class="container narrow prose">
<?= file_get_contents(dirname(__DIR__) . '/content/legal/terms-of-use.html') ?>
  </div>
</section>
<?php page_end(); ?>
