<?php
require __DIR__ . '/inc/layout.php';
http_response_code(404);
page_start(['title' => 'Page Not Found | Houston Public Adjusters', 'desc' => 'The page you were looking for could not be found.', 'path' => '/404/', 'noindex' => true]);
?>
<section class="page-hero"><div class="wrap"><h1>Page not found</h1><p class="lede">The page you&rsquo;re looking for has moved or doesn&rsquo;t exist. Here are some good places to start.</p></div></section>
<section class="section"><div class="wrap">
  <div class="card-grid">
    <a class="card tool-card" href="/"><h3>Home</h3><p>Houston Public Adjusters</p></a>
    <a class="card tool-card" href="/services/"><h3>Services</h3><p>Claims we handle</p></a>
    <a class="card tool-card" href="/tools/"><h3>Claim tools</h3><p>Calculators and checklists</p></a>
    <a class="card tool-card" href="/blog/"><h3>Blog</h3><p>Claim guides</p></a>
    <a class="card tool-card" href="/contact/"><h3>Contact</h3><p>Free claim review</p></a>
  </div>
</div></section>
<?php
page_end();
