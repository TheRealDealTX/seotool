<?php
$meta['title'] = 'Contact a Galveston Public Adjuster | Free Claim Review';
$meta['description'] = 'Request a free claim review from a licensed Galveston public adjuster. Call (832) 503-5866 for an expert consultation or send the form.';
$meta['crumb'] = 'Contact';
$meta['schema'][] = ['@type' => 'ContactPage', 'url' => SITE_URL . '/contact/'];
$err = isset($_GET['error']);
?>
<section class="hero hero-sub">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="eyebrow"><?= icon('phone', 18) ?> Free claim review</span>
      <h1>Call for an Expert Consultation</h1>
      <p class="lede">Tell us about your storm, fire, flood or denied claim. <?= AUTHOR ?> will review it and call you back — free, with no obligation.</p>
      <p><?= phone_link('btn btn-cta btn-lg', icon('phone', 22) . ' ' . PHONE) ?></p>
      <ul class="hero-trust"><li><?= icon('check', 18) ?> No recovery, no fee</li><li><?= icon('check', 18) ?> Galveston County</li><li><?= icon('check', 18) ?> <a href="mailto:<?= LEAD_EMAIL ?>" style="color:#fff"><?= LEAD_EMAIL ?></a></li></ul>
    </div>
    <div class="hero-card">
      <h2>Request your free review</h2>
      <?php if ($err): ?><p class="form-status err">Please check your name and phone number and try again, or call <?= e(PHONE) ?>.</p><?php endif ?>
      <?= lead_form('contact') ?>
    </div>
  </div>
  <?= wave_divider() ?>
</section>
<section class="section"><div class="wrap narrow">
  <h2>What to have ready</h2>
  <ul class="checks"><li>Your policy or declarations page (TWIA, homeowners, flood)</li><li>The date of loss and your claim number, if filed</li><li>Photos or video of the damage</li><li>Any estimate, offer or denial letter from the insurer</li></ul>
  <p>Don't have everything? Call anyway — we can help you get it.</p>
</div></section>
