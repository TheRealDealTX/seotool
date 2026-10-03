<?php /** @var array $page */ ?>
</main>
<footer class="site-footer">
  <div class="footer-cta">
    <div class="container footer-cta-inner reveal">
      <div>
        <p class="eyebrow eyebrow-gold">Property damage in the Rio Grande Valley?</p>
        <h2>Talk with a McAllen Public Adjuster before you settle.</h2>
        <p>A Free Claim Review helps you understand your policy, your insurer's estimate, and your options. No obligation.</p>
      </div>
      <div class="footer-cta-actions">
        <a class="btn btn-gold btn-lg" href="/free-claim-review/">Get a Free Claim Review</a>
        <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_display')) ?></a>
      </div>
    </div>
  </div>
  <div class="container footer-grid">
    <div class="footer-col footer-about">
      <a class="brand brand-footer" href="/" aria-label="McAllen Public Adjuster home">
        <img src="/assets/img/logo-mark.svg" alt="" width="44" height="44" loading="lazy">
        <span class="brand-text"><span class="brand-name">McAllen</span><span class="brand-sub">Public Adjuster</span></span>
      </a>
      <p>McAllen Public Adjuster represents policyholders&mdash;not insurance companies&mdash;on residential and commercial property insurance claims.</p>
      <p class="footer-legal-name"><strong><?= e(cfg('site_name')) ?></strong><br><?= e(cfg('company')) ?><br>Texas Department of Insurance License #<?= e(cfg('license')) ?></p>
    </div>
    <div class="footer-col">
      <h2 class="footer-heading">Contact</h2>
      <ul class="footer-contact">
        <li><?= icon('phone', 'icon icon-sm') ?> <a href="<?= e(tel_link()) ?>"><?= e(cfg('phone_display')) ?></a></li>
        <li><?= icon('chat', 'icon icon-sm') ?> <a href="sms:<?= e(cfg('phone_e164')) ?>">Text <?= e(cfg('phone_short')) ?></a></li>
        <li><?= icon('mail', 'icon icon-sm') ?> <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a></li>
        <li><?= icon('map', 'icon icon-sm') ?> Serving McAllen, Hidalgo County, and surrounding Rio Grande Valley communities.</li>
      </ul>
      <a class="btn btn-gold btn-sm" href="/free-claim-review/">Free Claim Review</a>
    </div>
    <div class="footer-col">
      <h2 class="footer-heading">Navigation</h2>
      <ul class="footer-links footer-links-2col">
        <?php foreach (footer_nav() as [$l, $h]): ?>
        <li><a href="<?= e($h) ?>"><?= e($l) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <div class="footer-col">
      <h2 class="footer-heading">Claim Services</h2>
      <ul class="footer-links">
        <li><a href="/services/hail-damage-claims/">Hail Damage Claims</a></li>
        <li><a href="/services/wind-damage-claims/">Wind Damage Claims</a></li>
        <li><a href="/services/hurricane-damage-claims/">Hurricane Damage Claims</a></li>
        <li><a href="/services/fire-damage-claims/">Fire Damage Claims</a></li>
        <li><a href="/services/water-damage-claims/">Water Damage Claims</a></li>
        <li><a href="/services/commercial-property-claims/">Commercial Property Claims</a></li>
        <li><a href="/services/denied-insurance-claims/">Denied Insurance Claims</a></li>
        <li><a href="/services/underpaid-insurance-claims/">Underpaid Insurance Claims</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <p class="footer-disclaimer">McAllen Public Adjuster is a public adjusting service of <?= e(cfg('company')) ?>, licensed by the Texas Department of Insurance (License #<?= e(cfg('license')) ?>). Public adjusters represent policyholders in property insurance claims; we are not attorneys and do not provide legal advice. Information on this website is general and educational, is not a guarantee of coverage or of any claim outcome, and does not create a client relationship. Every claim depends on the specific policy, facts, and insurer.</p>
      <p class="footer-copy">&copy; <?= date('Y') ?> <?= e(cfg('site_name')) ?>. All rights reserved. &middot; <a href="/privacy-policy/">Privacy Policy</a> &middot; <a href="/terms-of-use/">Terms of Use</a> &middot; <a href="/sitemap/">Sitemap</a></p>
    </div>
  </div>
</footer>
<div class="mobile-bar" role="region" aria-label="Quick contact">
  <a class="mobile-bar-call" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> Call Now</a>
  <a class="mobile-bar-review" href="/free-claim-review/"><?= icon('clipboard', 'icon icon-sm') ?> Free Claim Review</a>
</div>
<script src="/assets/js/site.js?v=<?= e(asset_version('js/site.js')) ?>" defer></script>
<?php foreach ($page['scripts'] ?? [] as $s): ?>
<script src="<?= e($s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
