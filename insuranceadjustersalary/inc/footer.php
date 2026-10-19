</main>
<footer class="site-footer">
  <div class="footer-glow" aria-hidden="true"></div>
  <div class="container footer-grid">
    <div class="footer-brand">
      <a class="brand" href="/">
        <span class="brand-mark"><?= icon('shield', 22) ?></span>
        <span class="brand-text">Insurance Adjuster <em>Salary</em></span>
      </a>
      <p>Independent pay research, calculators and career guides for staff, independent, catastrophe and public insurance adjusters.</p>
      <a class="btn btn-gold btn-sm" href="<?= COURSE_URL ?>" target="_blank" rel="sponsored noopener">Get Certified This Week</a>
      <p class="promo-note">Use <strong class="code-pill" data-copy="<?= PROMO_CODE ?>"><?= PROMO_CODE ?></strong> for 20% off.</p>
    </div>
    <div>
      <h3>Salary Guides</h3>
      <ul>
        <li><a href="<?= BLOG_BASE ?>how-much-do-insurance-adjusters-make/">How Much Adjusters Make</a></li>
        <li><a href="<?= BLOG_BASE ?>claims-adjuster-salary/">Claims Adjuster Salary</a></li>
        <li><a href="<?= BLOG_BASE ?>independent-adjuster-salary/">Independent Adjuster Salary</a></li>
        <li><a href="<?= BLOG_BASE ?>public-adjuster-salary/">Public Adjuster Salary</a></li>
        <li><a href="<?= BLOG_BASE ?>cat-adjuster-salary/">CAT Adjuster Salary</a></li>
        <li><a href="<?= BLOG_BASE ?>property-adjuster-salary/">Property Adjuster Salary</a></li>
      </ul>
    </div>
    <div>
      <h3>Free Tools</h3>
      <ul>
<?php foreach (tools() as $t): ?>
        <li><a href="<?= e($t['path']) ?>"><?= e($t['name']) ?></a></li>
<?php endforeach; ?>
      </ul>
      <h3 class="mt">By State</h3>
      <ul>
        <li><a href="<?= BLOG_BASE ?>insurance-adjuster-salary-texas/">Texas Adjuster Salary</a></li>
        <li><a href="<?= BLOG_BASE ?>insurance-adjuster-salary-florida/">Florida Adjuster Salary</a></li>
      </ul>
    </div>
    <div>
      <h3>Site</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="<?= BLOG_BASE ?>">Insurance Adjuster Advice</a></li>
        <li><a href="/tools/">All Tools</a></li>
        <li><a href="/about/">About</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>Copyright &copy; <?= date('Y') ?> <?= e(SITE_NAME) ?>. Salary figures are estimates for research purposes and are not job offers.</p>
    <a href="#top" class="to-top" aria-label="Back to top"><?= icon('up', 18) ?></a>
  </div>
</footer>
<div class="toast" role="status" aria-live="polite"></div>
<script src="<?= asset('js/main.js') ?>" defer></script>
<?php foreach ($page['scripts'] ?? [] as $s): ?>
<script src="<?= asset('js/' . $s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
