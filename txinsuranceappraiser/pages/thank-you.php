<?php
ob_start(); ?>
<section class="hero hero-sm">
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">Request received</span>
      <h1 class="anim">Thank you — we’ll be in touch shortly</h1>
      <p class="lead anim">Joseph or a member of the TX Insurance Appraiser team will reach out, usually the same business day. Need us sooner? Call <?= e(SITE['phone']) ?>.</p>
      <div class="hero-actions anim">
        <a class="btn btn-gold btn-lg" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 20) ?> Call now</a>
        <a class="btn btn-ghost-light btn-lg" href="/tools/claim-documentation-checklist/">Start your documentation checklist</a>
      </div>
    </div>
  </div>
</section>
<?php
render_page([
    'title' => 'Thank You | TX Insurance Appraiser',
    'description' => 'Thanks for contacting TX Insurance Appraiser.',
    'path' => '/thank-you/',
    'noindex' => true,
], (string) ob_get_clean());
