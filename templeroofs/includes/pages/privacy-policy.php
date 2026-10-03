<?php
defined('TR_ROOT') || exit;
$crumbs = [['Privacy Policy', '/privacy-policy/']];
layout_start([
    'title' => 'Privacy Policy', 'description' => 'How Temple Roofers collects, uses and protects the information you share through templeroofs.com.',
    'path' => '/privacy-policy/', 'crumbs' => $crumbs,
]);
page_hero(['h1' => 'Privacy Policy', 'lead' => 'Effective October 3, 2026. This policy explains what information templeroofs.com collects and how it is used.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true]);
?>
<div class="container container--narrow">
  <article class="prose legal">
    <p>Temple Roofers ("we", "us") operates templeroofs.com. We respect your privacy and collect only the information needed to respond to your roofing requests and run this website.</p>
    <h2>Information you give us</h2>
    <p>When you submit an inspection request or contact form, we receive the details you enter: your name, phone number, and optionally your email address, property address or ZIP code, the type of roofing concern, your preferred contact method and time, and any additional details you write. We also record the date and time of the submission and the page you sent it from.</p>
    <h2>How we use it</h2>
    <ul>
      <li>To contact you about your request, schedule an inspection and provide estimates.</li>
      <li>To keep a record of our communication with you.</li>
      <li>To protect the website from spam and abuse.</li>
    </ul>
    <p>We do not sell, rent or trade your personal information, and we do not use it for unrelated marketing without your permission.</p>
    <h2>How submissions are handled</h2>
    <p>Form submissions are processed on our web server and delivered to our team by email. If email delivery temporarily fails, the submission is saved in a protected, non-public location on the server so your request is not lost, and is deleted once it has been handled. Form submissions are sent over an encrypted (HTTPS) connection.</p>
    <h2>Information collected automatically</h2>
    <ul>
      <li><strong>Server logs:</strong> like most websites, our hosting provider records standard technical data such as IP address, browser type and pages requested, for security and troubleshooting.</li>
      <li><strong>Spam protection:</strong> to limit abuse of our forms, we keep a short-lived, one-way hashed (not readable) version of the submitting IP address and the time of the submission. These records expire automatically.</li>
      <li><strong>Cookies:</strong> this site does not use advertising or analytics cookies. If you submit a form without JavaScript enabled and need to correct an error, a temporary session cookie is used to redisplay your entries; it is deleted when you close your browser.</li>
    </ul>
    <h2>Third-party services</h2>
    <p>Weather information on this site is retrieved by our server from <a href="https://open-meteo.com/" rel="noopener">Open-Meteo</a> and the <a href="https://www.weather.gov/" rel="noopener">National Weather Service</a>. Your browser does not connect to those services directly and no personal information is shared with them. Fonts and images are hosted on our own server.</p>
    <h2>Data retention and security</h2>
    <p>We keep inquiry information only as long as needed to respond to you and maintain reasonable business records. We use reasonable technical measures to protect it, but no method of transmission or storage is completely secure.</p>
    <h2>Your choices</h2>
    <p>You may ask us to update or delete the information you submitted, or to stop contacting you, by calling <a href="<?= e(tel_href()) ?>"><?= e(cfg('phone_display')) ?></a>.</p>
    <h2>Children</h2>
    <p>This website is intended for adults. We do not knowingly collect information from children under 13.</p>
    <h2>Changes to this policy</h2>
    <p>We may update this policy from time to time. The effective date above shows when it was last revised.</p>
    <h2>Contact</h2>
    <p>Questions about this policy? Call Temple Roofers at <a href="<?= e(tel_href()) ?>"><?= e(cfg('phone_intl')) ?></a> or use our <a href="/contact/">contact form</a>.</p>
  </article>
</div>
<?php layout_end();
