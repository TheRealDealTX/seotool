</main>
<footer class="site-footer">
  <div class="footer-wave" aria-hidden="true"><svg viewBox="0 0 1440 80" preserveAspectRatio="none"><path d="M0 40c240 40 480 40 720 0s480-40 720 0v40H0z"/></svg></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="brand brand-light" href="/"><span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 40 40"><rect width="40" height="40" rx="11" fill="#7c6cff"/><text x="20" y="27" text-anchor="middle" font-family="Space Grotesk,Arial" font-weight="700" font-size="18" fill="#fff">A+</text></svg></span><span class="brand-name">Free<b>Grade</b>Calculator</span></a>
      <p>Free, private, no-signup grade, GPA and study calculators for students, parents and teachers. Your numbers never leave your device.</p>
      <a class="footer-mail" href="mailto:<?= e(SITE_EMAIL) ?>"><?= icon('mail') ?> <?= e(SITE_EMAIL) ?></a>
    </div>
    <?php foreach (['grades' => 'Grades', 'gpa' => 'GPA', 'teachers' => 'Teachers'] as $ck => $label): ?>
    <div class="footer-col"><h3><?= e($label) ?></h3><ul>
      <?php foreach (tools() as $s => $t) if ($t[1] === $ck): ?><li><a href="/<?= e($s) ?>"><?= e($t[0]) ?></a></li><?php endif; ?>
    </ul></div>
    <?php endforeach; ?>
    <div class="footer-col"><h3>More</h3><ul>
      <li><a href="/tools">All calculators</a></li>
      <li><a href="/blog">Blog &amp; guides</a></li>
      <li><a href="/study-supplies">Study supplies</a></li>
      <li><a href="/about-us">About us</a></li>
      <li><a href="/contact">Contact</a></li>
      <li><a href="/sitemap">Sitemap</a></li>
    </ul></div>
  </div>
  <div class="wrap footer-bottom">
    <p>© <?= date('Y') ?> <?= e(SITE_NAME) ?>. Results are estimates — always confirm with your school’s official policy.</p>
    <nav aria-label="Legal"><a href="/privacy-policy">Privacy</a><a href="/terms-of-use">Terms</a><a href="/disclaimer">Disclaimer</a><a href="/affiliate-disclosure">Affiliate disclosure</a></nav>
  </div>
</footer>

<nav class="bottom-nav" aria-label="Quick">
  <a href="/" <?= ($GLOBALS['__page']['path'] ?? '') === '/' ? 'aria-current="page"' : '' ?>><?= icon('home') ?><span>Home</span></a>
  <a href="/gpa-calculator"><?= icon('cap') ?><span>GPA</span></a>
  <button type="button" class="bn-search search-open" aria-label="Search tools"><?= icon('search') ?></button>
  <a href="/tools"><?= icon('grid') ?><span>Tools</span></a>
  <a href="/blog"><?= icon('book') ?><span>Blog</span></a>
</nav>

<div class="palette" id="palette" hidden role="dialog" aria-modal="true" aria-label="Search tools and articles">
  <div class="palette-box">
    <div class="palette-input"><?= icon('search') ?><input type="search" id="palette-q" placeholder="Search 29 calculators & guides…" autocomplete="off" aria-label="Search"><kbd>Esc</kbd></div>
    <ul class="palette-results" id="palette-results" role="listbox"></ul>
  </div>
</div>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c6cff"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs></svg>
<button class="to-top" type="button" aria-label="Back to top"><?= icon('arrow') ?></button>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
window.FGC_INDEX = <?= json_encode(array_merge(
    array_map(fn($s, $t) => ['t' => $t[0], 'u' => '/' . $s, 'd' => $t[3], 'k' => 'Tool'], array_keys(tools()), tools()),
    array_values(array_map(fn($a) => ['t' => $a['title'], 'u' => '/blog/' . $a['slug'], 'd' => $a['excerpt'] ?? '', 'k' => 'Guide'], articles()))
), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?>;
</script>
<script src="<?= asset('js/app.js') ?>" defer></script>
<?php if (!empty($GLOBALS['__page']['tools_js'])): ?><script src="<?= asset('js/tools.js') ?>" defer></script><?php endif; ?>
</body>
</html>
