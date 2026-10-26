<?php
require dirname(__DIR__) . '/includes/bootstrap.php';
$crumbs = [['Home', '/'], ['Contact', '/contact/']];
page_start([
    'title'       => 'Contact Bastrop Roofing | (512) 297-7580 | Free Estimate',
    'description' => 'Contact Bastrop Roofing for a free roof inspection and estimate in Bastrop, TX. Call (512) 297-7580, email info@bastroproofs.com or send the online form.',
    'path'        => '/contact/',
    'schema'      => [breadcrumb_schema($crumbs), ['@type' => 'ContactPage', 'url' => abs_url('/contact/'), 'about' => ['@id' => abs_url('/#business')]]],
]);
page_hero('Free estimates', 'Contact Bastrop Roofing', 'Tell us what is happening with your roof. We will schedule a free inspection and give you a clear written estimate.', $crumbs);
?>
<section class="section">
  <div class="container split split-top">
    <div class="split-copy reveal">
      <h2 class="section-title small">Talk With a Bastrop Roofer</h2>
      <p>The fastest way to reach us is by phone. For active leaks and storm damage, call any time — storm calls are answered 24/7.</p>
      <ul class="contact-list dark">
        <li><a href="tel:<?= SITE['phone_href'] ?>"><span class="ci"><?= icon('phone') ?></span><span><small>Call or text</small><?= SITE['phone_display'] ?></span></a></li>
        <li><a href="mailto:<?= SITE['email'] ?>"><span class="ci"><?= icon('mail') ?></span><span><small>Email</small><?= SITE['email'] ?></span></a></li>
        <li><span class="ci"><?= icon('pin') ?></span><span><small>Based in</small>Bastrop, TX <?= SITE['zip'] ?></span></li>
        <li><span class="ci"><?= icon('clock') ?></span><span><small>Hours</small><?= SITE['hours'] ?></span></li>
      </ul>
      <div class="map-embed">
        <iframe title="Map of Bastrop, TX" src="https://www.google.com/maps?q=Bastrop,+TX+78602&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
    <div class="form-card form-card-light reveal">
      <h3>Request Your Free Roof Estimate</h3>
      <?php estimate_form('Contact page'); ?>
    </div>
  </div>
</section>
<?php cta_band('Storm Damage or an Active Leak?', 'Do not wait for a callback. Call now and we will help you protect your home and plan the repair.'); page_end();
