<?php
defined('PGF') || exit;

$crumbs = [['Home', '/'], ['Privacy Policy', '/privacy-policy/']];
$page = [
    'path'   => '/privacy-policy/',
    'title'  => 'Privacy Policy — Pure Goat Farms',
    'desc'   => 'How Pure Goat Farms collects, uses and protects your information, including analytics, cookies, affiliate links and your privacy rights.',
    'crumbs' => $crumbs,
];
ob_start();
?>
<section class="page-hero page-hero--slim">
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>Privacy Policy</h1>
    <p class="page-hero__lead">Effective Date: July 2026</p>
  </div>
</section>
<section class="section section--tight">
  <div class="container narrow prose">
    <p>Pure Goat Farms respects your privacy and is committed to protecting the personal information you share when visiting our website, <a href="/">https://puregoatfarms.com/</a>. This Privacy Policy explains how we collect, use, store, and protect your information when you browse our website, contact us, subscribe to updates, or interact with our content.</p>
    <p>By using this website, you agree to the terms of this Privacy Policy.</p>
    <h2>Information We Collect</h2>
    <p>We may collect personal information that you voluntarily provide when you contact us, submit a form, subscribe to a newsletter, leave a comment, or communicate with us through the website.</p>
    <p>This information may include your name, email address, phone number, message details, and any other information you choose to provide.</p>
    <p>We may also collect non-personal information automatically, including your browser type, device type, IP address, pages visited, time spent on the website, referring website, and general usage data.</p>
    <h2>How We Use Your Information</h2>
    <p>Pure Goat Farms may use the information collected to respond to inquiries, provide website content, improve user experience, send updates when requested, monitor website performance, prevent spam or security issues, and understand how visitors use our website.</p>
    <p>We do not sell, rent, or trade your personal information to third parties.</p>
    <h2>Cookies and Tracking Technologies</h2>
    <p>Our website may use cookies and similar tracking technologies to improve functionality, analyze website traffic, remember user preferences, and provide a better browsing experience.</p>
    <p>Cookies are small files stored on your device. You can choose to disable cookies through your browser settings. However, some parts of the website may not function properly if cookies are disabled.</p>
    <h2>Analytics</h2>
    <p>Pure Goat Farms may use third-party analytics tools, such as Google Analytics or similar services, to understand visitor behavior and improve website performance. These tools may collect information such as pages visited, session duration, browser type, device information, and general location data.</p>
    <p>This information is used for website improvement and does not personally identify individual visitors.</p>
    <h2>Affiliate Links and Advertising</h2>
    <p>Some pages on Pure Goat Farms may include affiliate links, sponsored content, or advertising links. If you click on an affiliate link and make a purchase, we may earn a small commission at no additional cost to you.</p>
    <p>Third-party advertisers or affiliate partners may use cookies or tracking technologies according to their own privacy policies. Pure Goat Farms is not responsible for the privacy practices of third-party websites.</p>
    <h2>Third-Party Links</h2>
    <p>Our website may contain links to external websites, resources, tools, or services. Once you leave Pure Goat Farms, we are not responsible for the privacy practices, content, or policies of those third-party websites.</p>
    <p>We encourage you to review the privacy policies of any external websites you visit.</p>
    <h2>Comments and User Content</h2>
    <p>If comments are enabled on the website, visitors may submit comments or other user-generated content. Information submitted in public comment areas may be visible to other users.</p>
    <p>We reserve the right to moderate, remove, or block comments that are spam, offensive, inappropriate, or harmful.</p>
    <h2>Email Communications</h2>
    <p>If you subscribe to our newsletter or provide your email address, we may send you updates, articles, resources, promotions, or other relevant communications.</p>
    <p>You may unsubscribe from email communications at any time by clicking the unsubscribe link in the email or contacting us directly.</p>
    <h2>Data Protection</h2>
    <p>We take reasonable steps to protect your personal information from unauthorized access, misuse, disclosure, alteration, or destruction. However, no method of online transmission or electronic storage is completely secure.</p>
    <p>While we work to protect your information, we cannot guarantee absolute security.</p>
    <h2>Children’s Privacy</h2>
    <p>Pure Goat Farms does not knowingly collect personal information from children under the age of 13. If we become aware that personal information from a child has been collected without parental consent, we will take steps to delete that information.</p>
    <p>Parents or guardians who believe their child has provided personal information may contact us to request removal.</p>
    <h2>Your Privacy Rights</h2>
    <p>Depending on your location, you may have the right to access, update, correct, or delete your personal information. You may also request that we stop sending marketing communications or limit how your information is used.</p>
    <p>To make a privacy-related request, please contact us using the details below.</p>
    <h2>California Privacy Rights</h2>
    <p>If you are a California resident, you may have additional rights under the California Consumer Privacy Act, including the right to know what personal information is collected, request deletion of personal information, and opt out of certain data-sharing practices.</p>
    <p>Pure Goat Farms does not sell personal information.</p>
    <h2>GDPR Privacy Rights</h2>
    <p>If you are located in the European Economic Area, you may have rights under the General Data Protection Regulation, including the right to access, correct, delete, restrict processing, object to processing, and request a copy of your personal data.</p>
    <p>You may contact us to exercise these rights.</p>
    <h2>Data Retention</h2>
    <p>We retain personal information only for as long as necessary to fulfill the purposes described in this Privacy Policy, comply with legal obligations, resolve disputes, and maintain website security.</p>
    <h2>Changes to This Privacy Policy</h2>
    <p>Pure Goat Farms may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated effective date.</p>
    <p>We encourage visitors to review this page regularly to stay informed about how we protect personal information.</p>
    <h2>Contact Us</h2>
    <p>If you have any questions about this Privacy Policy or how your information is handled, please contact us:</p>
    <p>Pure Goat Farms<br>Website: <a href="/">https://puregoatfarms.com/</a><br>Email: <a href="mailto:info@puregoatfarms.com">info@puregoatfarms.com</a></p>
    <h2>Amazon Associates</h2>
    <p>Pure Goat Farms is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. When you click a product link on our site, Amazon may set cookies in your browser to record that the visit came from us. We may earn a commission on qualifying purchases at no extra cost to you. We do not receive any personal information about you or what you buy.</p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
