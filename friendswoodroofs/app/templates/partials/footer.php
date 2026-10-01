<?php defined('FR_APP') || exit; // no direct web access (host ignores .htaccess) ?>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a class="brand brand--footer" href="/">
        <?php partial('logo'); ?>
        <span class="brand-text"><span class="brand-name">Friendswood Roofers</span><span class="brand-tag">Friendswood, TX</span></span>
      </a>
      <p>Roof repair, replacement, inspections, storm damage repair and maintenance for homeowners in Friendswood, Texas.</p>
      <p class="footer-phone"><a href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span><?= e(phone_display()) ?></span></a></p>
      <a class="btn btn-accent" href="/contact/#estimate-form">Request an Estimate</a>
    </div>
    <div>
      <h2 class="footer-heading">Services</h2>
      <ul class="footer-links">
        <?php foreach (services() as $slug => $s): ?>
        <li><a href="/services/<?= e($slug) ?>/"><?= e($s['name']) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2 class="footer-heading">Company</h2>
      <ul class="footer-links">
        <li><a href="/about/">About</a></li>
        <li><a href="/service-area/">Service Area</a></li>
        <li><a href="/roofing-project-planner/">Roofing Project Planner</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/faqs/">FAQs</a></li>
        <li><a href="/contact/">Contact Us</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-heading">Weather resources</h2>
      <ul class="footer-links">
        <li><a href="https://www.weather.gov/hgx/" rel="noopener">NWS Houston/Galveston</a></li>
        <li><a href="https://www.nhc.noaa.gov/" rel="noopener">National Hurricane Center</a></li>
      </ul>
      <h2 class="footer-heading">Legal</h2>
      <ul class="footer-links">
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <p>&copy; <?= date('Y') ?> Friendswood Roofers. Serving homeowners in Friendswood, TX.</p>
    </div>
  </div>
</footer>
