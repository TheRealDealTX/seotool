<?php defined('BO') || exit;
$crumbs = [['Home', '/'], ['Privacy Policy', '/privacy-policy/']];
page_head(['title' => 'Privacy Policy & Affiliate Disclosure | Better Outdoors', 'desc' => 'How Better Outdoors collects, uses and protects information, how cookies and Amazon affiliate links work, and your privacy choices.', 'path' => '/privacy-policy/', 'schema' => [breadcrumb_schema($crumbs)]]);
?>
<section class="page-hero"><div class="wrap"><?= breadcrumbs_html($crumbs) ?><h1>Privacy Policy</h1><p>Last updated <?= fmt_date('2026-10-26') ?></p></div></section>
<div class="page-body prose">
<p>This Privacy Policy explains how Better Outdoors (&ldquo;we,&rdquo; &ldquo;us&rdquo;) at betteroutdoors.net handles information when you visit our website, use our tools or contact us.</p>
<h2 id="information-we-collect">Information We Collect</h2>
<ul>
  <li><strong>Information you give us.</strong> If you use our contact form or email us, we receive your name, email address and message. We use it only to respond.</li>
  <li><strong>Automatically collected data.</strong> Like most websites, our hosting provider logs technical data such as IP address, browser type, pages visited and the time of each request, for security and performance.</li>
  <li><strong>Tool data.</strong> Our calculators and checklist run in your browser. Settings such as your checklist ticks or last draw length are saved in your browser&rsquo;s local storage and never sent to us.</li>
</ul>
<h2 id="how-we-use-information">How We Use Information</h2>
<p>We use information to operate and secure the site, answer messages, understand which guides are helpful, and improve our content. We do not sell your personal information.</p>
<h2 id="cookies">Cookies and Third-Party Services</h2>
<p>Better Outdoors loads fonts from Google Fonts and icons from Cloudflare&rsquo;s cdnjs, which may receive your IP address when delivering those files. When you click an Amazon link, Amazon may set cookies to attribute purchases. Third-party sites have their own privacy policies, which we encourage you to review.</p>
<h2 id="affiliate-disclosure">Affiliate Disclosure</h2>
<p>Better Outdoors is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. <strong>As an Amazon Associate, we earn from qualifying purchases.</strong></p>
<p>This means that if you click a product link and make a purchase, we may earn a commission at no additional cost to you. Affiliate relationships never influence our verdicts or which products we cover. Amazon may use cookies to track purchases; we never receive your personal or payment details from these transactions.</p>
<h2 id="data-retention">Data Retention and Security</h2>
<p>Contact messages are kept only as long as needed to respond and for reasonable record-keeping. We use HTTPS and reputable hosting to protect data in transit, though no method of transmission is 100% secure.</p>
<h2 id="your-rights">Your Choices and Rights</h2>
<p>You can block or delete cookies in your browser and clear local storage at any time. Depending on where you live (for example under GDPR or CCPA), you may have the right to access, correct or delete personal information we hold. Email us to make a request.</p>
<h2 id="children">Children&rsquo;s Privacy</h2>
<p>Better Outdoors is not directed at children under 13, and we do not knowingly collect their personal information.</p>
<h2 id="changes">Changes to This Policy</h2>
<p>We may update this policy from time to time. The date at the top shows the latest revision.</p>
<h2 id="contact">Contact</h2>
<p>Questions about privacy? Email <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a> or use our <a href="/contact-us/">contact form</a>.</p>
</div>
<?php page_foot(false); ?>
