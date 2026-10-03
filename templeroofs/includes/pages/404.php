<?php
defined('TR_ROOT') || exit;
layout_start([
    'title'       => 'Page Not Found',
    'description' => 'The page you were looking for could not be found.',
    'path'        => '/404/',
    'noindex'     => true,
    'status'      => 404,
]);
?>
<section class="section status-page">
  <div class="container container--narrow status-page__inner">
    <p class="status-page__code" aria-hidden="true">404</p>
    <h1>We could not find that page</h1>
    <p class="lead">The link may be outdated or the address mistyped. Here are some helpful places to start:</p>
    <div class="link-tiles">
      <a href="/"><?= icon('home') ?> Home</a>
      <a href="/services/"><?= icon('wrench') ?> Roofing services</a>
      <a href="/free-roof-inspection/"><?= icon('clipboard-check') ?> Free roof inspection</a>
      <a href="/tools/"><?= icon('calculator') ?> Roofing tools</a>
      <a href="/weather/"><?= icon('cloud-sun') ?> Temple weather</a>
      <a href="/blog/"><?= icon('book') ?> Roofing blog</a>
    </div>
    <p>Or call us at <a href="<?= e(tel_href()) ?>"><?= e(cfg('phone_display')) ?></a>.</p>
  </div>
</section>
<?php layout_end();
