<?php
defined('RT_APP') || exit;

$page = [
    'title' => 'Privacy Policy',
    'description' => 'How Rodeo Texas collects, uses and protects information.',
    'canonical' => '/privacy-policy/',
];
require_once RT_PUBLIC . '/includes/head.php';
require_once RT_PUBLIC . '/includes/header.php';
?>
<div class="wrap narrow prose">
  <h1>Privacy Policy</h1>
  <p><em>Last updated: September 29, 2026</em></p>
  <p>At Rodeo Texas, your privacy matters to us. This policy explains what information we collect, how we use it, and the choices you have.</p>

  <h2>Information you give us</h2>
  <p>When you use our contact form, submit an event, or report a correction, we collect the information you enter — such as your name, e-mail address, phone number and message. We use it only to respond to you and to review and publish accurate event listings. Your e-mail address and phone number are never published.</p>

  <h2>Favorites saved in your browser</h2>
  <p>Events you save as favorites are stored only in your own browser (local storage). They are not sent to us, and you can clear them at any time from the Favorites page or your browser settings.</p>

  <h2>Analytics and cookies</h2>
  <p>We use Google Analytics to understand how visitors use the site, for example which pages are popular. Google Analytics uses cookies and collects information such as pages visited, approximate location and device type. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google Analytics opt-out browser add-on</a> or by blocking cookies in your browser.</p>
  <p>To protect our forms from spam, we keep a one-way, non-reversible fingerprint of the network address used to submit a form for a limited time.</p>

  <h2>Maps</h2>
  <p>Map views load map images from OpenStreetMap's tile servers, which receive your network address in order to deliver those images. See the <a href="https://osmfoundation.org/wiki/Privacy_Policy" rel="noopener">OpenStreetMap Foundation privacy policy</a>.</p>

  <h2>Sharing</h2>
  <p>We do not sell, rent, or share your personal information with third parties, except service providers that host the site and deliver e-mail on our behalf.</p>

  <h2>Third-party links</h2>
  <p>Our website links to other websites, such as rodeo organizers and ticket sellers. Once you leave our site, their privacy practices apply.</p>

  <h2>Data security</h2>
  <p>We take reasonable steps to protect your information. However, no method of online transmission or storage is 100% secure.</p>

  <h2>Updates to this policy</h2>
  <p>We may update this policy occasionally. Changes will be posted on this page with a new “last updated” date.</p>

  <h2>Contact us</h2>
  <p>If you have questions about this policy, please <a href="/contact/">contact us</a>.</p>
</div>
<?php
require_once RT_PUBLIC . '/includes/footer.php';
require_once RT_PUBLIC . '/includes/scripts.php';
