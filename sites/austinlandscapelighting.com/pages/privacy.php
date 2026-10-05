<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Privacy Policy', '/privacy-policy/']];
$page = [
    'title' => 'Privacy Policy | Austin Landscape Lighting',
    'description' => 'How Austin Landscape Lighting collects, uses and protects the information you share through austinlandscapelighting.com, including estimate requests and analytics.',
    'path' => '/privacy-policy/',
    'robots' => 'noindex, follow',
    'schema' => [schema_webpage(['title' => 'Privacy Policy', 'description' => 'Privacy policy.', 'path' => '/privacy-policy/']), schema_breadcrumb($crumbs)],
];
ob_start();
echo sub_hero(['eyebrow' => 'Legal', 'h1' => 'Privacy Policy', 'intro' => 'Last updated October 5, 2026. This policy explains what information Austin Landscape Lighting collects on this website and how it is used.', 'crumbs' => $crumbs, 'cta' => false]);
?>
<section class="section">
  <div class="container container--narrow prose" data-reveal>
    <h2>Who we are</h2>
    <p>Austin Landscape Lighting ("we", "us") operates austinlandscapelighting.com. We design, install and maintain landscape lighting in Austin, Texas and surrounding communities. You can reach us at <a href="mailto:<?= e(BIZ['email']) ?>"><?= e(BIZ['email']) ?></a> or <a href="<?= BIZ['phone_href'] ?>"><?= e(BIZ['phone_display']) ?></a>.</p>
    <h2>Information we collect</h2>
    <p><strong>Information you give us.</strong> When you request an estimate or contact us, we collect the details you enter: name, email address, phone number, city, the service you are interested in and your message. We use this information to respond to your request, schedule consultations and provide our services.</p>
    <p><strong>Information collected automatically.</strong> Our web server records standard access logs (IP address, browser type, pages visited, referring page and timestamps) for security and troubleshooting. We may use privacy-respecting analytics to understand how the site is used in aggregate. This site sets no advertising cookies.</p>
    <h2>How we use information</h2>
    <ul>
      <li>To reply to inquiries and schedule and perform lighting consultations, installations and service.</li>
      <li>To send estimates, invoices, appointment reminders and warranty information.</li>
      <li>To improve the website and our services.</li>
      <li>To comply with legal obligations and protect against fraud or abuse.</li>
    </ul>
    <p>We do not sell your personal information. We do not share it with third parties except service providers who help us operate (for example email hosting), and only as needed for them to perform those services.</p>
    <h2>Text messages and calls</h2>
    <p>If you provide a phone number, we may call or text you about your request. Message and data rates may apply. Reply STOP to any text to opt out.</p>
    <h2>Data retention and security</h2>
    <p>We keep inquiry and project records for as long as needed to serve you and meet legal, accounting and warranty obligations. We use reasonable technical and organizational measures to protect your information, though no method of transmission over the internet is completely secure.</p>
    <h2>Your choices</h2>
    <p>You may ask us to access, correct or delete the personal information we hold about you by emailing <a href="mailto:<?= e(BIZ['email']) ?>"><?= e(BIZ['email']) ?></a>. We will respond within a reasonable time.</p>
    <h2>Third-party links</h2>
    <p>This site may link to third-party websites such as Google. Their privacy practices are governed by their own policies.</p>
    <h2>Children</h2>
    <p>This website is not directed to children under 13 and we do not knowingly collect information from them.</p>
    <h2>Changes</h2>
    <p>We may update this policy from time to time. The date at the top reflects the latest revision. Continued use of the site after changes means you accept the updated policy.</p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
