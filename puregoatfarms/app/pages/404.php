<?php
defined('PGF') || exit;

$page = [
    'path'    => '/404/',
    'title'   => 'Page Not Found — Pure Goat Farms',
    'desc'    => 'This page wandered off like a goat through a gap in the fence.',
    'noindex' => true,
];
ob_start();
?>
<section class="page-hero page-hero--404">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
  <div class="container narrow center">
    <p class="big-404" aria-hidden="true">404</p>
    <h1>This page got through the fence.</h1>
    <p class="page-hero__lead">Goats find the one gap in any fence — and this link found one too. Try one of these instead:</p>
    <p class="hero__actions hero__actions--center">
      <a class="btn btn--rust" href="/">Go home</a>
      <a class="btn btn--ghost" href="/blog/">Read the blog</a>
      <a class="btn btn--ghost" href="/tools/">Free tools</a>
    </p>
  </div>
</section>
<section class="section section--tight">
  <div class="container">
    <div class="post-grid post-grid--3">
<?php $i = 0; foreach (posts_sorted() as $s => $p): if ($i++ >= 3) break; ?>
      <?= post_card($s, $p) ?>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
