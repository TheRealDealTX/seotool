</main>
<section class="newsletter reveal" id="subscribe" aria-labelledby="nl-h">
  <div class="wrap newsletter-inner">
    <div>
      <h2 id="nl-h">One thought, delivered.</h2>
      <p>A short, reflective note when something new is published. No noise. Unsubscribe anytime.</p>
    </div>
    <?php view('form-subscribe'); ?>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-about">
      <a href="/" class="footer-logo"><img src="<?= LOGO_WHITE ?>" width="756" height="114" alt="Thought Changer" loading="lazy"></a>
      <p><strong>Thought Changer</strong> is a space for reflection and growth, shining light on the quiet moments and metaphors that reshape how we think, act, and evolve—one thought at a time.</p>
      <p><a href="mailto:<?= SITE_EMAIL ?>" class="footer-mail"><svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm9 7.2L4 7.3V17h16V7.3l-8 4.9Zm7.1-5.2H4.9L12 11.3 19.1 7Z"/></svg><?= SITE_EMAIL ?></a></p>
    </div>
    <div>
      <h3>Quick Links</h3>
      <ul>
        <li><a href="/">Home</a></li><li><a href="/about-us/">About Us</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact-us/">Contact Us</a></li>
      </ul>
    </div>
    <div>
      <h3>Popular</h3>
      <ul>
        <li><a href="/quotes/">Quotes</a></li><li><a href="/mindset/">Mindset</a></li><li><a href="/recommended-reads/">Recommended Reads</a></li>
        <li><a href="/life-is-fleeting-5-ways-to-slow-it-down/">Life Is Fleeting</a></li><li><a href="/heres-what-it-means-to-level-up/">What It Means to Level Up</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-legal">
    <p class="affiliate-note">As an Amazon Associate, Thought Changer earns from qualifying purchases. <a href="/affiliate-disclosure/">Affiliate disclosure</a>.</p>
    <p><a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms-of-use/">Terms of Use</a></p>
    <p>© <?= date('Y') ?> Thought Changer. All Rights Reserved.</p>
  </div>
</footer>
<a href="#top" class="to-top" aria-label="Back to top"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 7.6 4.7 15l1.4 1.4 5.9-5.9 5.9 5.9 1.4-1.4L12 7.6Z"/></svg></a>
<script src="/assets/js/site.js?v=<?= ASSET_VER ?>" defer></script>
</body>
</html>
