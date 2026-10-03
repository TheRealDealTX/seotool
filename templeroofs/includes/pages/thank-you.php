<?php
defined('TR_ROOT') || exit;
layout_start([
    'title'       => 'Thank You — Request Received',
    'description' => 'Thanks for contacting Temple Roofers. We received your request and will be in touch soon.',
    'path'        => '/thank-you/',
    'noindex'     => true,
]);
?>
<section class="section status-page">
  <div class="container container--narrow status-page__inner">
    <span class="status-page__icon status-page__icon--ok"><?= icon('check') ?></span>
    <h1>Thank you — we received your request</h1>
    <p class="lead">Your details were sent to the Temple Roofers team. We will contact you by your preferred method, usually by the next business day, to confirm a time for your free roof inspection.</p>
    <div class="status-page__box">
      <h2>While you wait</h2>
      <ul class="check-list">
        <li><?= icon('check') ?><span>If water is coming in, move belongings away and catch drips in a container.</span></li>
        <li><?= icon('check') ?><span>Take photos of any interior stains and anything you can see from the ground.</span></li>
        <li><?= icon('check') ?><span>Please stay off the roof — we will handle the up-close inspection safely.</span></li>
      </ul>
      <p>Need us sooner? Call <a href="<?= e(tel_href()) ?>"><strong><?= e(cfg('phone_intl')) ?></strong></a>.</p>
    </div>
    <div class="btn-row btn-row--center">
      <a class="btn btn--navy" href="/">Back to home</a>
      <a class="btn btn--ghost" href="/weather/">Check Temple weather</a>
      <a class="btn btn--ghost" href="/blog/">Read roofing guides</a>
    </div>
  </div>
</section>
<?php layout_end();
