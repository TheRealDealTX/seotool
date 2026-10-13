<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Terms of Use', '/terms-of-use/']];
page_start(['title' => 'Terms of Use | Houston Public Adjusters', 'desc' => 'The terms and conditions that govern your use of the Houston Public Adjusters website, its calculators and its content.', 'path' => '/terms-of-use/', 'crumbs' => $crumbs]);
?>
<section class="page-hero"><div class="wrap"><?= breadcrumbs_html($crumbs) ?><h1>Terms of Use</h1><p class="lede">Effective Date: February 6, 2026 &middot; Updated October 13, 2026</p></div></section>
<div class="wrap" style="padding:48px 0 64px"><div class="prose">
<p>Welcome to the Houston Public Adjusters website, operated by <?= LEGAL_NAME ?> (&ldquo;we,&rdquo; &ldquo;our,&rdquo; or &ldquo;us&rdquo;). By accessing or using this website, you agree to be bound by the terms and conditions outlined below. If you do not agree with these Terms of Use, please do not use this website.</p>
<p>These terms govern your use of our website only and do not create a public adjuster-client relationship.</p>
<h2>Website Purpose</h2>
<p>The information provided on this website is for <strong>general informational purposes only</strong>. It is intended to explain our services as public adjusters and provide general insight into the insurance claims process. Nothing on this website should be interpreted as legal advice, insurance coverage advice specific to your policy, or a guarantee of claim outcome. Each insurance claim is unique and depends on policy language, damage conditions, and insurer responses.</p>
<h2>Calculators, Tools and Weather Data</h2>
<p>Our calculators and tools provide estimates for planning purposes only. Results depend entirely on the figures you enter and on general assumptions, and they are not an appraisal, a coverage determination or a promise of any settlement amount. Weather information is provided by the National Weather Service and NOAA as-is and may be delayed or unavailable; always follow official guidance for safety decisions.</p>
<h2>No Professional Relationship Established</h2>
<p>Use of this website, including submitting a contact form or sending an email, does <strong>not</strong> create a public adjuster-client relationship. Such a relationship is only established after a written agreement is signed by both parties. You should not rely on information on this website as a substitute for professional advice specific to your situation.</p>
<h2>User Responsibilities</h2>
<p>By using this website, you agree that you will provide accurate and truthful information when submitting forms, will not use the website for unlawful or fraudulent purposes, and will not attempt to disrupt, damage, or interfere with the website or its functionality. We reserve the right to restrict or terminate access to the website if these terms are violated.</p>
<h2>Intellectual Property Rights</h2>
<p>All content on this website &mdash; including text, graphics, logos, layout, and design &mdash; is the property of Houston Public Adjusters unless otherwise stated and is protected by applicable intellectual property laws. You may view and print pages for personal, non-commercial use. You may not copy, reproduce, modify, or distribute website content without prior written permission, or use our content for commercial purposes without authorization.</p>
<h2>Third-Party Links</h2>
<p>This website may include links to third-party websites for informational purposes. These links do not constitute endorsement or control over third-party content. We are not responsible for the content or accuracy of third-party websites or their privacy practices or terms of use. Accessing third-party websites is at your own risk.</p>
<h2>Website Availability</h2>
<p>We strive to keep this website accurate and accessible, but we do not guarantee continuous or uninterrupted access, or that content is always current or error-free. We may update, modify, or remove content at any time without notice.</p>
<h2>Limitation of Liability</h2>
<p>To the fullest extent permitted by law, Houston Public Adjusters shall not be liable for any damages arising from your use or inability to use this website; reliance on information, calculators or weather data provided on the website; or errors, omissions, or inaccuracies in website content. This includes direct, indirect, incidental, or consequential damages.</p>
<h2>Indemnification</h2>
<p>You agree to indemnify and hold harmless Houston Public Adjusters from any claims, liabilities, damages, or expenses arising out of your use of the website, your violation of these Terms of Use, or your misuse of website content.</p>
<h2>Governing Law</h2>
<p>These Terms of Use are governed by and interpreted in accordance with the laws of the <strong>State of Texas</strong>, without regard to conflict-of-law principles. Any disputes related to these terms or use of this website shall be subject to the exclusive jurisdiction of the courts located in Texas.</p>
<h2>Changes to These Terms</h2>
<p>We reserve the right to update or revise these Terms of Use at any time. Changes become effective immediately upon posting to this page. Your continued use of the website constitutes acceptance of any revised terms.</p>
<h2>Contact Information</h2>
<p>If you have questions about these Terms of Use, please contact us:</p>
<p><strong>Houston Public Adjusters</strong> (<?= LEGAL_NAME ?>)<br>Email: <a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a><br>Phone: <a href="tel:<?= PHONE_E164 ?>"><?= PHONE_DISPLAY ?></a></p>
</div></div>
<?php
page_end();
