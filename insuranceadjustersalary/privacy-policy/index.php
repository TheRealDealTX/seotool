<?php
require dirname(__DIR__) . '/inc/config.php';
$page = ['title' => 'Privacy Policy | ' . SITE_NAME, 'description' => 'Privacy policy for Insurance Adjuster Salary: what we collect when you use our adjuster salary guides and calculators, cookies, analytics and affiliate links.', 'path' => '/privacy-policy/', 'image' => 'laptop-notes.webp'];
require SITE_ROOT . '/inc/header.php';
echo page_hero('Legal', 'Privacy Policy', 'Last updated October 19, 2026.', 'laptop-notes.webp', ['Privacy Policy' => null]);
?>
<section class="section"><div class="container narrow prose legal">
  <p>This policy explains how <?= e(SITE_NAME) ?> (&ldquo;we&rdquo;, &ldquo;us&rdquo;) handles information when you visit this website.</p>
  <h2>Information we collect</h2>
  <p>We do not require accounts and we do not ask for your name or email to use our calculators. Calculator inputs are processed entirely in your browser and are never sent to our servers.</p>
  <p>Like most websites, our hosting provider automatically records standard server logs, such as IP address, browser type, pages requested and the date and time of each request. These logs are used for security and to keep the site running.</p>
  <h2>Cookies and analytics</h2>
  <p>We may use privacy-respecting analytics to understand which pages are useful. These tools may set cookies. You can block or delete cookies in your browser settings.</p>
  <h2>Third-party links</h2>
  <p>Our pages link to third-party sites, including online adjuster course providers. Some of these links may be affiliate or sponsored links. Their privacy practices are governed by their own policies.</p>
  <h2>Children</h2>
  <p>This site is intended for adults researching careers and is not directed to children under 13.</p>
  <h2>Changes</h2>
  <p>We may update this policy from time to time. The date at the top of this page shows when it last changed.</p>
</div></section>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
