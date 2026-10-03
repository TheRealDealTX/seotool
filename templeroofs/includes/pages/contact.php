<?php
defined('TR_ROOT') || exit;
$crumbs = [['Contact', '/contact/']];
layout_start([
    'title'       => 'Contact Temple Roofers | (512) 297-7580',
    'raw_title'   => true,
    'description' => 'Contact Temple Roofers in Temple, TX. Call (512) 297-7580 or send a message to schedule a free roof inspection or ask a roofing question.',
    'path'        => '/contact/',
    'crumbs'      => $crumbs,
]);
page_hero(['h1' => 'Contact Temple Roofers', 'lead' => 'Call, or send a message and we will get back to you. Free roof inspections for Temple and nearby Bell County communities.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true]);
?>
<section class="section">
  <div class="container contact-grid">
    <div class="contact-info reveal">
      <h2>Talk to a Temple roofer</h2>
      <p>The fastest way to reach us is by phone. If you send the form, include the best time to call and a few details about what you are seeing on your roof or ceiling.</p>
      <a class="contact-tile" href="<?= e(tel_href()) ?>">
        <span class="contact-tile__icon"><?= icon('phone') ?></span>
        <span><span class="contact-tile__label">Phone</span><strong><?= e(cfg('phone_intl')) ?></strong></span>
      </a>
      <a class="contact-tile" href="/free-roof-inspection/">
        <span class="contact-tile__icon"><?= icon('clipboard-check') ?></span>
        <span><span class="contact-tile__label">Free roof inspection</span><strong>Book online</strong></span>
      </a>
      <div class="contact-tile contact-tile--static">
        <span class="contact-tile__icon"><?= icon('map-pin') ?></span>
        <span><span class="contact-tile__label">Based in</span><strong>Temple, Texas</strong><small>Serving Temple and nearby <a href="/service-areas/">Bell County communities</a></small></span>
      </div>
      <div class="callout">
        <strong>Active leak?</strong> Move belongings away from the drip, catch water in a container, and keep clear of any bulging ceiling. Then call us — see <a href="/services/emergency-roof-leak-repair-temple-tx/">emergency roof leak repair</a> for more steps.
      </div>
    </div>
    <div class="contact-form reveal">
      <?php lead_form(['variant' => 'full', 'id' => 'contact', 'title' => 'Send us a message', 'subtitle' => 'Fields marked * are required.', 'button' => 'Send My Request']); ?>
    </div>
  </div>
</section>
<?php layout_end();
