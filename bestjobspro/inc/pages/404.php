<?php
page_start([
    'title'       => 'Page Not Found | Best Jobs Pro',
    'description' => 'The page you were looking for could not be found. Browse Best Jobs Pro job postings, career tools and articles.',
    'path'        => $path ?? '/',
    'robots'      => 'noindex, follow',
]);
?>
<section class="hero" style="min-height:60vh">
  <canvas class="net-canvas" aria-hidden="true"></canvas>
  <div class="arcs" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap" style="padding:110px 22px;text-align:center;position:relative">
    <p class="eyebrow" style="justify-content:center">Error 404</p>
    <h1>This position has been filled.</h1>
    <p class="hero__sub" style="margin:0 auto">Well, the page you were after isn't here. Try one of these instead:</p>
    <div class="hero__btns" style="justify-content:center">
      <a class="btn" href="/job-postings/"><?= icon('briefcase') ?> Job postings</a>
      <a class="btn btn--ghost-light" href="/">Home</a>
      <a class="btn btn--ghost-light" href="/blog/">Blog</a>
      <a class="btn btn--ghost-light" href="/contact-us/">Contact us</a>
    </div>
  </div>
</section>
<?php page_end();
