<?php
defined('SCC') || exit;
if (!function_exists('page_head')) require ROOT . '/inc/layout.php';
page_head(['title' => 'Page not found | Solar CCTV Camera', 'description' => 'This page could not be found.', 'path' => $_SERVER['REQUEST_URI'] ?? '/', 'noindex' => true]);
?>
<section class="err-page"><div class="wrap">
  <div class="code">404</div>
  <h1>This page went dark</h1>
  <p>The page you were looking for doesn’t exist or has moved. Try one of these instead:</p>
  <p class="hero-ctas" style="justify-content:center">
    <a class="btn btn-sun" href="/">Home</a>
    <a class="btn btn-ghost" href="/solar-camera-guides/">All guides</a>
    <a class="btn btn-ghost" href="/tools/">Free tools</a>
  </p>
</div></section>
<?php page_foot();
