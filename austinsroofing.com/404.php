<?php
require __DIR__ . '/includes/layout.php';
http_response_code(404);
page_start([
    'title' => 'Page Not Found | Austin Roofing',
    'description' => 'The page you were looking for could not be found. Browse Austin Roofing services, tools and guides.',
    'path' => '/404/', 'noindex' => true,
]);
?>
<section class="not-found">
  <div class="container">
    <p class="not-found__code">404</p>
    <h1>This Page Blew Off the Roof</h1>
    <p class="lead">The page you are looking for has moved or no longer exists. Try one of these instead:</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn--red" href="/">Austin Roofing Home</a>
      <a class="btn btn--outline" href="/services/">Our Services</a>
      <a class="btn btn--outline" href="/blog/">Roofing Blog</a>
      <a class="btn btn--outline" href="/contact-us/">Contact Us</a>
    </div>
  </div>
</section>
<?php page_end();
