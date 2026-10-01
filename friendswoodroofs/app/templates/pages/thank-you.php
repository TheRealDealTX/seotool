<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
$sent = !empty($_SESSION['estimate_sent']);
unset($_SESSION['estimate_sent']);
?>
<section class="page-hero page-hero--center">
  <div class="container narrow page-hero-inner">
    <?php if ($sent): ?>
      <span class="success-mark" aria-hidden="true"><?= icon('check') ?></span>
      <h1>Thank you, your request was sent</h1>
      <p class="lead">We received your estimate request and will contact you using the phone number you provided. If you included an email address, we may reply by email as well.</p>
    <?php else: ?>
      <h1>Thank you for contacting Friendswood Roofers</h1>
      <p class="lead">This page confirms estimate requests sent from our website. If you haven't sent one yet, you can <a href="/contact/#estimate-form">request an estimate</a> or call us.</p>
    <?php endif; ?>
  </div>
</section>
<section class="section">
  <div class="container narrow prose">
    <h2>What happens next</h2>
    <ol>
      <li>We review your request and any details you shared.</li>
      <li>We call you to ask questions and arrange a time to look at your roof.</li>
      <li>After the assessment, you receive a written estimate. There is no obligation.</li>
    </ol>
    <p>If water is coming into your home, move belongings away from the leak, place a container under drips and keep clear of any sagging ceiling. Do not go on the roof. For anything urgent, please call us at <a href="<?= e(phone_href()) ?>"><?= e(phone_display()) ?></a>.</p>
    <h2>While you wait</h2>
    <ul class="link-list">
      <li><a href="/blog/roof-inspection-what-to-expect-friendswood/">What to Expect During a Roof Inspection in Friendswood</a></li>
      <li><a href="/blog/roof-repair-or-replacement-friendswood/">Roof Repair or Replacement? A Guide for Friendswood Homeowners</a></li>
      <li><a href="/faqs/">Roofing FAQs</a></li>
      <li><a href="/">Return to the homepage</a></li>
    </ul>
  </div>
</section>
