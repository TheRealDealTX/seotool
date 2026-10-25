<?php
require __DIR__ . '/../inc/layout.php';

page_start([
    'title' => 'About Monetizing Influencers | Our Mission',
    'description' => 'About Monetizing Influencers: who we are, what we do and how we help creators turn followers into income with guides, free tools and web design.',
    'path' => '/about/',
    'extra_css' => ['/assets/css/pages.css'],
    'schema' => [['@type' => 'AboutPage', 'name' => 'About Monetizing Influencers', 'url' => SITE_URL . '/about/', 'about' => ['@id' => SITE_URL . '/#org']]],
]);

page_hero('About us',
    'About <span class="grad-text">Monetizing Influencers</span>',
    'We believe every creator with an engaged audience deserves to be paid fairly for it. Monetizing Influencers exists to close the gap between influence and income.',
    [['About', '/about/']]);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap split">
    <div>
      <span class="kicker reveal">Our mission</span>
      <h2 class="reveal">Help creators get paid more from their audience</h2>
      <p class="reveal">Too many talented creators build loyal communities and then guess at what to charge, wait for brands that never email, or depend on a single platform that can change the rules overnight. Monetizing Influencers was started to fix that with clear, practical information and tools anyone can use.</p>
      <p class="reveal">Based in Southlake, Texas, we work with creators around the world across niches like fashion, fitness, motocross, mountain biking, luxury, real estate and finance.</p>
    </div>
    <div class="glass-panel reveal">
      <h3>What we do</h3>
      <ul class="check-list">
        <li><strong>Publish guides</strong> on influencer monetization, brand deals, pricing and every major platform.</li>
        <li><strong>Build free tools</strong> like the earnings calculator, media kit builder and email generator.</li>
        <li><strong>Design money sites</strong> for influencers who want to own their audience.</li>
        <li><strong>Publish expert voices</strong> through our <a href="/write-for-us/">write for us</a> program.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap">
    <div class="section-head"><span class="kicker reveal">Who we help</span><h2 class="reveal">Built for creators at every stage</h2></div>
    <div class="card-grid cols-3">
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('sparkles') ?></span><h3>New creators</h3><p>Start earning before you hit big follower numbers with affiliate income, UGC and smart positioning.</p></article>
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('trending') ?></span><h3>Growing influencers</h3><p>Price your content confidently, pitch brands directly and turn one-off deals into retainers.</p></article>
      <article class="card tilt reveal"><span class="ico-badge"><?= icon('rocket') ?></span><h3>Full-time creators</h3><p>Diversify with products, memberships and a website so your business is not at the mercy of one platform.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker reveal">Our values</span><h2 class="reveal">How Monetizing Influencers works</h2></div>
    <div class="card-grid cols-4">
      <div class="card reveal"><span class="ico-badge"><?= icon('shield') ?></span><h3>Honest numbers</h3><p>Our calculators give estimates and say so. We never promise income.</p></div>
      <div class="card reveal"><span class="ico-badge"><?= icon('heart') ?></span><h3>Audience first</h3><p>Monetization should never cost a creator the trust of their community.</p></div>
      <div class="card reveal"><span class="ico-badge"><?= icon('zap') ?></span><h3>Practical over theory</h3><p>Every guide ends with steps you can take today.</p></div>
      <div class="card reveal"><span class="ico-badge"><?= icon('users') ?></span><h3>Free to learn</h3><p>Our guides and tools are free, with no account required.</p></div>
    </div>
  </div>
</section>

<section class="section alt-bg">
  <div class="wrap narrow">
    <div class="glass-panel gradient-border reveal">
      <h2 style="font-size:1.6rem">Contact Monetizing Influencers</h2>
      <ul class="contact-list" style="list-style:none;padding:0">
        <li><?= icon('mail') ?> <a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a></li>
        <li><?= icon('phone') ?> <a href="tel:<?= e(SITE_PHONE_HREF) ?>"><?= e(SITE_PHONE) ?></a></li>
        <li><?= icon('pin') ?> <?= e(SITE_STREET . ', ' . SITE_CITY . ', ' . SITE_REGION . ' ' . SITE_ZIP) ?>, USA</li>
      </ul>
      <a class="btn btn-glow" href="/contact/">Send us a message <?= icon('arrow') ?></a>
    </div>
  </div>
</section>

<?php cta_band(); ?>
<?php page_end();
