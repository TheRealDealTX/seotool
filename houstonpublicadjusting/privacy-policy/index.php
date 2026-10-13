<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Privacy Policy', '/privacy-policy/']];
page_start(['title' => 'Privacy Policy | Houston Public Adjusters', 'desc' => 'How Houston Public Adjusters collects, uses and protects the information you share through our website, forms, phone and email.', 'path' => '/privacy-policy/', 'crumbs' => $crumbs]);
?>
<section class="page-hero"><div class="wrap"><?= breadcrumbs_html($crumbs) ?><h1>Privacy Policy</h1><p class="lede">Effective Date: February 6, 2026 &middot; Updated October 13, 2026</p></div></section>
<div class="wrap" style="padding:48px 0 64px"><div class="prose">
<p>Houston Public Adjusters (operated by <?= LEGAL_NAME ?>, &ldquo;we,&rdquo; &ldquo;our,&rdquo; or &ldquo;us&rdquo;) is committed to protecting your privacy. This Privacy Policy explains how we collect, use, store and safeguard your information when you visit our website or contact us through our online forms, phone, text message or email.</p>
<p>By using this website, you consent to the data practices described in this policy.</p>
<h2>Information We Collect</h2>
<p>We may collect both personal and non-personal information depending on how you interact with our website.</p>
<h3>Personal Information You Provide</h3>
<p>When you fill out a contact form, request a consultation, or communicate with us, we may collect:</p>
<ul><li>Name</li><li>Email address</li><li>Phone number</li><li>Property address or ZIP code (if provided)</li><li>Details related to your insurance claim or property damage</li></ul>
<p>You are not required to provide personal information to browse our website, but certain services may not be available without it.</p>
<h3>Non-Personal Information</h3>
<p>We may automatically collect limited technical data, including IP address, browser type, device information, and pages visited and time spent on the site. This information helps us understand how visitors use our website and improve performance and usability.</p>
<h3>Information That Stays in Your Browser</h3>
<p>Our calculators, contents inventory builder and hurricane checklist run entirely in your browser. Anything you type into them is stored only on your device (in your browser&rsquo;s local storage) and is never sent to us. Our live weather tracker requests public data directly from the National Weather Service and NOAA.</p>
<h2>How We Use Your Information</h2>
<p>We use the information collected for legitimate business purposes, including:</p>
<ul><li>Responding to inquiries and consultation requests</li><li>Communicating about your insurance claim or services</li><li>Providing customer support</li><li>Improving website functionality and content</li><li>Maintaining internal records</li><li>Complying with legal and regulatory obligations</li></ul>
<p>We do not sell, rent, or trade your personal information to third parties for marketing purposes. Mobile numbers and text-messaging consent are never shared with third parties or affiliates for marketing purposes.</p>
<h2>How We Protect Your Information</h2>
<p>We take reasonable administrative, technical, and physical measures to safeguard your personal information against unauthorized access, misuse, or disclosure. While no method of data transmission over the internet is 100% secure, we strive to use commercially acceptable means to protect your information and limit access to authorized personnel only.</p>
<h2>Sharing of Information</h2>
<p>We may share your information only under the following circumstances:</p>
<ul><li>With service providers who assist in operating our website or communications, under confidentiality obligations</li><li>When required by law, regulation, or legal process</li><li>To protect our rights, property, or safety, or that of others</li></ul>
<p>We do not disclose your personal information beyond what is necessary to provide our services or comply with legal requirements.</p>
<h2>Cookies and Tracking Technologies</h2>
<p>Our website may use cookies or similar technologies to enhance user experience and analyze site traffic. You can choose to disable cookies through your browser settings. Doing so may affect certain features of the website.</p>
<h2>Third-Party Links</h2>
<p>Our website may contain links to third-party websites for informational purposes. We are not responsible for the privacy practices, policies, or content of those external sites. We encourage users to review the privacy policies of any third-party websites they visit.</p>
<h2>Your Privacy Rights</h2>
<p>Depending on your location, you may have rights regarding your personal information, including the right to request access to the information we hold about you, request corrections to inaccurate information, and request deletion of your personal data, subject to legal obligations. To exercise these rights, please contact us using the information below.</p>
<h2>Children&rsquo;s Privacy</h2>
<p>Our website and services are not intended for individuals under the age of 13. We do not knowingly collect personal information from children. If you believe a child has provided personal information through our website, please contact us so we can promptly remove it.</p>
<h2>Communications</h2>
<p>By submitting your information through our website, you consent to being contacted by Houston Public Adjusters via phone, text message, email, or other reasonable communication methods related to your inquiry or services. Message and data rates may apply. You may opt out of text messages at any time by replying STOP, and out of other non-essential communications by contacting us directly.</p>
<h2>Changes to This Privacy Policy</h2>
<p>We reserve the right to update or modify this Privacy Policy at any time. Changes will be effective immediately upon posting to this page. We encourage you to review this policy periodically to stay informed about how we protect your information.</p>
<h2>Contact Us</h2>
<p>If you have questions about this Privacy Policy or how your information is handled, please contact us:</p>
<p><strong>Houston Public Adjusters</strong> (<?= LEGAL_NAME ?>)<br>Email: <a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a><br>Phone: <a href="tel:<?= PHONE_E164 ?>"><?= PHONE_DISPLAY ?></a></p>
</div></div>
<?php
page_end();
