<?php
require dirname(__DIR__) . '/includes/layout.php';

$crumbs = [['Contact Us', '/contact-us/']];
page_start([
    'title' => 'Contact Austin Roofing | Free Roofing Estimate in Austin, TX',
    'description' => 'Contact Austin Roofing for a free roofing estimate or inspection in Austin, TX. Call or text (956) 465-6045, email info@austinsroofing.com — 24/7 emergency service.',
    'path' => '/contact-us/',
    'crumbs' => $crumbs,
    'body_class' => 'page-contact',
]);
add_schema(['@type' => 'ContactPage', 'url' => abs_url('/contact-us/'), 'name' => 'Contact Austin Roofing', 'about' => ['@id' => abs_url('/#business')]]);
page_hero('Contact Austin Roofing', [
    'crumbs' => $crumbs,
    'eyebrow' => 'Free estimates · 24/7 emergencies',
    'lead' => 'Request your free Austin roofing estimate, schedule an inspection or get emergency help. Call, text, email or send the form — a real roofer will get back to you fast.',
    'cta' => false,
]);
?>
<section class="section section--tight">
  <div class="container">
    <div class="contact-cards">
      <a class="contact-card reveal" href="tel:<?= BIZ['phone_href'] ?>"><?= icon('phone') ?><strong>Quick Call</strong><span><?= e(BIZ['phone_display']) ?></span><small>24/7 emergency line</small></a>
      <a class="contact-card reveal" href="sms:<?= BIZ['phone_href'] ?>"><?= icon('mail') ?><strong>Send a Text Message</strong><span><?= e(BIZ['phone_short']) ?></span><small>Send photos of the damage</small></a>
      <a class="contact-card reveal" href="mailto:<?= BIZ['email'] ?>"><?= icon('clipboard') ?><strong>Email Us</strong><span><?= e(BIZ['email']) ?></span><small>We reply quickly</small></a>
    </div>
    <div class="split split--wide-left" style="align-items:start">
      <div id="quote">
        <h2>Request Your Free Roofing Estimate</h2>
        <?php if (isset($_GET['error'])): ?>
        <div class="form-alert form-alert--error" role="alert">Please add your name and a phone number or valid email so we can reach you.</div>
        <?php endif; ?>
        <?php quote_form(false, '/contact-us/'); ?>
      </div>
      <div class="prose">
        <h2>What Happens Next</h2>
        <ol class="steps" style="grid-template-columns:1fr;gap:34px;margin-top:30px">
          <li><h3>We reach out</h3><p>An Austin Roofing team member contacts you to confirm details and schedule a time.</p></li>
          <li><h3>Free inspection</h3><p>We inspect the roof and send photos of everything we find.</p></li>
          <li><h3>Clear, written quote</h3><p>You get honest repair or replacement options — no pressure, no obligation.</p></li>
        </ol>
        <div class="callout callout--warn" style="margin-top:34px"><p><strong>Roof leaking right now?</strong> Don’t wait for a form reply — call <?= phone_link() ?> for 24/7 <a href="/services/emergency-roof-repair/">emergency roof repair</a>.</p></div>
        <p>Serving Austin and Central Texas including <a href="/service-areas/round-rock-tx/">Round Rock</a>, <a href="/service-areas/cedar-park-tx/">Cedar Park</a>, <a href="/service-areas/pflugerville-tx/">Pflugerville</a>, <a href="/service-areas/georgetown-tx/">Georgetown</a>, <a href="/service-areas/kyle-tx/">Kyle</a> and <a href="/service-areas/">more</a>.</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--cream">
  <div class="container" style="max-width:900px">
    <?php faq_block([
        ['How fast will Austin Roofing respond?', '<p>We respond quickly during business hours and offer 24/7 service for emergencies like active leaks and storm damage.</p>'],
        ['Is the estimate really free?', '<p>Yes — inspections and estimates are free with no obligation.</p>'],
        ['Can I text photos of my roof?', '<p>Yes. Text photos to <a href="sms:+19564656045">(956) 465-6045</a> and we can often give you a first read before we visit.</p>'],
        ['Do you give estimates for commercial and multi-family roofs?', '<p>Yes. We provide free assessments and written proposals for commercial buildings, apartment complexes, townhome communities and HOAs.</p>'],
    ], 'Contact FAQs'); ?>
  </div>
</section>
<?php
page_end();
