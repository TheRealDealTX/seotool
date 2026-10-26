</main>
<section class="cta-band">
  <canvas class="coin-canvas" data-density="0.5" aria-hidden="true"></canvas>
  <div class="wrap cta-inner reveal">
    <h2>Ready to start your side hustle?</h2>
    <p>Take the free 60-second quiz and get three side hustles matched to your schedule, skills and income goal.</p>
    <div class="btn-row">
      <a class="btn btn-green btn-lg" href="/tools/side-hustle-quiz/"><?= icon('target') ?>Find my side hustle</a>
      <a class="btn btn-ghost btn-lg" href="/tools/"><?= icon('chart') ?>Browse free tools</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a href="/"><img src="<?= SITE_LOGO_FOOTER ?>" alt="<?= e(SITE_NAME) ?>" width="190" height="63" loading="lazy"></a>
      <p><?= e(SITE_NAME) ?> helps you find, start and grow a side hustle that fits your life — with honest guides, city-by-city ideas and free calculators.</p>
    </div>
    <div>
      <h3>Side Hustles</h3>
      <ul>
<?php foreach (PLATFORMS as $slug => [$name]): ?>
        <li><a href="/<?= $slug ?>/"><?= e($name) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h3>Free Tools</h3>
      <ul>
<?php foreach (TOOLS as $slug => [, $name]): ?>
        <li><a href="/tools/<?= $slug ?>/"><?= e($name) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h3>Explore</h3>
      <ul>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/blog/?cat=city-guides">City Guides</a></li>
        <li><a href="/side-hustle-gear/">Side Hustle Gear</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>&copy; <?= date('Y') ?> <?= e(SITE_NAME) ?>. All rights reserved.</p>
    <p class="disclosure">As an Amazon Associate, <?= e(SITE_NAME) ?> earns from qualifying purchases. Earnings figures are estimates, not guarantees.</p>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top"><?= icon('arrow') ?></button>
<script src="<?= asset('/assets/js/site.js') ?>" defer></script>
<?php if (!empty($GLOBALS['uses_tools'])): ?>
<script src="<?= asset('/assets/js/tools.js') ?>" defer></script>
<?php endif; ?>
</body>
</html>
