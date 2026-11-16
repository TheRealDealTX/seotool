<?php
ob_start(); ?>
<section class="hero hero-sm">
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">Error 404</span>
      <h1 class="anim">We couldn’t find that page</h1>
      <p class="lead anim">The page may have moved. Try one of the links below, or call us — we’re happy to help with your claim.</p>
      <div class="hero-actions anim">
        <a class="btn btn-gold btn-lg" href="/">Go to the homepage</a>
        <a class="btn btn-ghost-light btn-lg" href="/areas/">Find your city</a>
        <a class="btn btn-ghost-light btn-lg" href="/blog/">Read the blog</a>
      </div>
    </div>
  </div>
</section>
<?php
render_page([
    'title' => 'Page Not Found | TX Insurance Appraiser',
    'description' => 'Page not found. Explore TX Insurance Appraiser’s appraisal services, Texas service areas and insurance claim guides.',
    'path' => '/404/',
    'noindex' => true,
], (string) ob_get_clean());
