<?php
$title = 'Contact TX Insurance Appraiser | Free Insurance Claim Review';
$desc  = 'Contact TX Insurance Appraiser for a free insurance claim review. Call or text (254) 421-5412 or email us. Serving Austin, Waco, Dallas, Houston and all of Texas.';
$err = isset($_GET['error']);
ob_start(); ?>
<section class="hero hero-sm">
  <div class="hero-bg" style="background-image:url(/assets/img/site/TX-Insurance-Appraiser-Site-Image.webp)"></div>
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">Contact us · Reach us 24/7</span>
      <h1 class="anim">Contact TX Insurance Appraiser</h1>
      <p class="lead anim">Tell us about your claim. We’ll review the carrier’s estimate free and call you back — first thing in the morning if you reach us after hours.</p>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap split" style="align-items:start">
    <div class="reveal-l">
      <h2>Get your free claim review</h2>
      <p style="color:var(--ink-2)">The more you share, the faster we can help: your carrier’s estimate, photos of the damage, and where the claim stands today.</p>
      <?php if ($err): ?><p class="form-msg err">Please complete the required fields and try again.</p><?php endif; ?>
      <div class="tool" style="padding:28px"><?= lead_form('full', 'contact-page') ?></div>
    </div>
    <div class="reveal-r">
      <h2>Reach us directly</h2>
      <div class="contact-cards">
        <a class="contact-card" href="tel:<?= SITE['phone_href'] ?>"><span class="ic-badge ic-gold" style="margin:0;width:52px;height:52px"><?= icon('phone', 24) ?></span><span><b>Quick call</b><?= e(SITE['phone']) ?></span></a>
        <a class="contact-card" href="sms:<?= SITE['phone_href'] ?>"><span class="ic-badge" style="margin:0;width:52px;height:52px"><?= icon('chat', 24) ?></span><span><b>Send a text message</b>Text photos and questions to <?= e(SITE['phone_short']) ?></span></a>
        <a class="contact-card" href="mailto:<?= SITE['email'] ?>"><span class="ic-badge" style="margin:0;width:52px;height:52px"><?= icon('mail', 24) ?></span><span><b>Email</b><?= e(SITE['email']) ?></span></a>
        <div class="contact-card"><span class="ic-badge" style="margin:0;width:52px;height:52px"><?= icon('clock', 24) ?></span><span><b>Office hours</b><?= e(SITE['hours']) ?> · messages answered 24/7</span></div>
      </div>
      <h3 style="margin-top:34px">Regional hubs</h3>
      <div class="grid g2" style="gap:14px">
        <?php foreach (['austin' => 'Austin-TX.webp', 'waco' => 'Waco-TX.webp', 'dallas' => 'Dallas-TX.webp', 'houston' => null] as $slug => $im): $c = cities()[$slug]; ?>
        <a class="fc" style="aspect-ratio:16/10" href="<?= city_url($slug) ?>"><img src="<?= $im ? '/assets/img/site/' . $im : city_image($c) ?>" alt="<?= e($c['name']) ?>, TX" width="500" height="265" loading="lazy"><span><?= e($c['name']) ?>, TX</span></a>
        <?php endforeach; ?>
      </div>
      <p style="margin-top:20px;color:var(--ink-2)">We serve property owners in <a href="/areas/">288 Texas cities</a> — wherever your property is, we’ll come to you.</p>
    </div>
  </div>
</section>
<?php
$content = (string) ob_get_clean();
render_page([
    'title' => $title, 'description' => $desc, 'path' => '/contact-us/',
    'crumbs' => [['Home', '/'], ['Contact Us', '/contact-us/']],
    'schema' => [schema_webpage('ContactPage', $title, $desc, '/contact-us/')],
], $content);
