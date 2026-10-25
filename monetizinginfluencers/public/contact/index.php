<?php
require __DIR__ . '/../inc/layout.php';

page_start([
    'title' => 'Contact Monetizing Influencers',
    'description' => 'Contact Monetizing Influencers about brand deals, monetization plans, web design for influencers or guest posts. Email, phone or send a message.',
    'path' => '/contact/',
    'extra_css' => ['/assets/css/pages.css'],
    'schema' => [['@type' => 'ContactPage', 'name' => 'Contact Monetizing Influencers', 'url' => SITE_URL . '/contact/', 'about' => ['@id' => SITE_URL . '/#org']]],
]);

page_hero('Contact',
    'Contact <span class="grad-text">Monetizing Influencers</span>',
    'Questions about monetizing your channel, our web design package or writing for us? Send a message and we will reply within 1-2 business days.',
    [['Contact', '/contact/']]);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap">
    <div class="card-grid cols-3">
      <div class="card info-card tilt reveal"><span class="ico-badge"><?= icon('mail') ?></span><h3>Email</h3><p><a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a></p></div>
      <div class="card info-card tilt reveal"><span class="ico-badge"><?= icon('phone') ?></span><h3>Phone</h3><p><a href="tel:<?= e(SITE_PHONE_HREF) ?>"><?= e(SITE_PHONE) ?></a></p></div>
      <div class="card info-card tilt reveal"><span class="ico-badge"><?= icon('pin') ?></span><h3>Address</h3><p><?= e(SITE_STREET) ?><br><?= e(SITE_CITY . ', ' . SITE_REGION . ' ' . SITE_ZIP) ?>, USA</p></div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap split" style="align-items:start">
    <div>
      <h2 class="reveal">Send us a message</h2>
      <p class="reveal">Pick the topic that fits best so your message reaches the right person faster.</p>
      <ul class="check-list reveal">
        <li>Looking for a free plan? Use <a href="/get-started/">Get Started</a>.</li>
        <li>Want a website? See <a href="/website-design/">web design for influencers</a>.</li>
        <li>Pitching an article? Read <a href="/write-for-us/">write for us</a>.</li>
      </ul>
    </div>
    <div class="glass-panel gradient-border reveal" id="contact">
      <?= form_flash('contact') ?>
      <form class="form js-form" action="/api/form.php" method="post">
        <?= form_guard('contact', '/contact/') ?>
        <div class="form-row">
          <div class="field"><label for="ct-name">Name *</label><input id="ct-name" type="text" name="name" required autocomplete="name"></div>
          <div class="field"><label for="ct-email">Email *</label><input id="ct-email" type="email" name="email" required autocomplete="email"></div>
        </div>
        <div class="field"><label for="ct-subject">Subject</label>
          <select id="ct-subject" name="subject"><option>General question</option><option>Monetization help</option><option>Web design</option><option>Guest post / write for us</option><option>Partnership or advertising</option><option>Something else</option></select></div>
        <div class="field"><label for="ct-message">Message *</label><textarea id="ct-message" name="message" required></textarea></div>
        <button class="btn btn-glow btn-lg" type="submit"><?= icon('mail') ?> Send message</button>
      </form>
    </div>
  </div>
</section>
<?php page_end();
