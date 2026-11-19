<?php defined('SNW') || (http_response_code(404) && exit);
partial('page-hero', ['title' => 'Privacy Policy', 'crumbs' => [['Privacy Policy', '']]]); ?>
<section class="section tight">
  <div class="wrap prose narrow">
    <p><em>Last updated: November 19, 2026</em></p>
    <h2>Who we are</h2>
    <p><?= e(cfg('name')) ?> operates <?= e(parse_url(cfg('url'), PHP_URL_HOST)) ?>. Questions about this policy can be sent to <a href="mailto:<?= e(cfg('email')) ?>"><?= e(cfg('email')) ?></a>.</p>
    <h2>Information we collect</h2>
    <p>When you submit a form on this site (for example to ask about a home, share what you're looking for, request a home value review or subscribe to updates), we collect the details you enter — such as your name, email address, phone number, property details and message — along with the page you submitted from, the time and your IP address for spam prevention.</p>
    <p>Like most websites, our hosting provider records standard server logs (IP address, browser type, pages requested). We do not use advertising cookies, and this site does not set cookies of its own.</p>
    <h2>How we use your information</h2>
    <ul>
      <li>To respond to your inquiry and provide the real estate services you request</li>
      <li>To send listing updates or market news you have asked for (you can unsubscribe at any time)</li>
      <li>To protect the site from spam and abuse</li>
    </ul>
    <h2>Sharing</h2>
    <p>We do not sell your personal information. We may share it with service providers who help us operate (such as email and hosting providers) and, with your permission, with professionals involved in your transaction such as lenders, inspectors or escrow companies, or when required by law.</p>
    <h2>Embedded content and links</h2>
    <p>Articles may link to or embed content from other websites. Those sites have their own privacy practices, which we encourage you to review.</p>
    <h2>Retention and your choices</h2>
    <p>We keep inquiry records only as long as needed to serve you and meet legal obligations. You may ask us to access, correct or delete your information at any time by emailing <a href="mailto:<?= e(cfg('email')) ?>"><?= e(cfg('email')) ?></a>.</p>
    <h2>Changes</h2>
    <p>We may update this policy from time to time; the date above shows the latest revision.</p>
  </div>
</section>
