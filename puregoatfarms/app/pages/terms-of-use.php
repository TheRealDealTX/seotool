<?php
defined('PGF') || exit;

$crumbs = [['Home', '/'], ['Terms of Use', '/terms-of-use/']];
$page = [
    'path'   => '/terms-of-use/',
    'title'  => 'Terms of Use — Pure Goat Farms',
    'desc'   => 'The terms that govern your use of Pure Goat Farms, including our animal care disclaimer, affiliate links, website tools and calculators.',
    'crumbs' => $crumbs,
];
ob_start();
?>
<section class="page-hero page-hero--slim">
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>Terms of Use</h1>
    <p class="page-hero__lead">Effective Date: July 2026</p>
  </div>
</section>
<section class="section section--tight">
  <div class="container narrow prose">
    <p>Welcome to Pure Goat Farms. These Terms of Use govern your access to and use of <a href="/">https://puregoatfarms.com/</a> and any content, articles, tools, resources, or services available through the website.</p>
    <p>By using this website, you agree to these Terms of Use. If you do not agree, please stop using the website.</p>
    <h2>Use of This Website</h2>
    <p>Pure Goat Farms provides educational and informational content related to goat care, goat farming, homesteading, livestock management, farm tools, and related topics.</p>
    <p>You agree to use this website only for lawful purposes. You must not use the website in any way that could damage the site, interfere with other users, attempt to gain unauthorized access, or violate any applicable law or regulation.</p>
    <h2>Informational Purposes Only</h2>
    <p>The content on Pure Goat Farms is provided for general informational and educational purposes only. While we aim to provide useful and accurate information, we do not guarantee that all content is complete, current, or free from errors.</p>
    <p>Information on this website should not replace professional veterinary, agricultural, legal, financial, or business advice. Always consult a qualified professional before making decisions that affect animal health, farm operations, or business matters.</p>
    <h2>Animal Care Disclaimer</h2>
    <p>Pure Goat Farms may publish information about goat health, feeding, kidding, fencing, milk production, parasite control, and general livestock care. This information is not a substitute for advice from a licensed veterinarian or qualified livestock professional.</p>
    <p>If an animal appears sick, injured, distressed, or in need of urgent care, contact a veterinarian immediately.</p>
    <h2>Intellectual Property</h2>
    <p>All content on this website, including text, articles, images, graphics, logos, page layouts, downloadable materials, and other website elements, is owned by Pure Goat Farms or used with permission unless otherwise stated.</p>
    <p>You may view, share, and print content for personal, non-commercial use only. You may not copy, reproduce, republish, distribute, modify, sell, or exploit website content without written permission from Pure Goat Farms.</p>
    <h2>User Comments and Submissions</h2>
    <p>If the website allows comments, messages, or other submissions, you are responsible for the content you submit. You agree not to post content that is unlawful, abusive, defamatory, misleading, spammy, obscene, threatening, harmful, or infringes on another person’s rights.</p>
    <p>By submitting content to the website, you grant Pure Goat Farms a non-exclusive right to use, display, edit, remove, and publish that content as needed for website operation and moderation.</p>
    <p>We reserve the right to remove comments or submissions at our discretion.</p>
    <h2>Affiliate Links and Sponsored Content</h2>
    <p>Pure Goat Farms may include affiliate links, advertising links, sponsored content, product mentions, or recommendations. If you click an affiliate link and make a purchase, we may earn a commission at no additional cost to you.</p>
    <p>We may recommend products, tools, or services based on usefulness, relevance, or experience. However, you are responsible for reviewing product details, warranties, safety instructions, and seller terms before making a purchase.</p>
    <h2>Third-Party Links</h2>
    <p>This website may contain links to third-party websites, products, resources, or services. These links are provided for convenience and informational purposes only.</p>
    <p>Pure Goat Farms does not control third-party websites and is not responsible for their content, privacy practices, accuracy, availability, products, or services. Visiting third-party websites is done at your own risk.</p>
    <h2>Website Tools and Calculators</h2>
    <p>Pure Goat Farms may provide calculators, charts, checklists, or other tools for educational purposes. These tools are intended to provide general estimates only and should not be treated as professional advice or guaranteed results.</p>
    <p>You are responsible for verifying any information before relying on it for animal care, farm planning, costs, feeding schedules, breeding decisions, or other practical uses.</p>
    <h2>No Guarantees</h2>
    <p>Pure Goat Farms does not guarantee specific results from using the website, following recommendations, purchasing suggested products, or applying information found in articles or resources.</p>
    <p>Farm conditions, animal health, climate, feed quality, management practices, and local regulations vary widely. Therefore, results may differ from one situation to another.</p>
    <h2>Limitation of Liability</h2>
    <p>To the fullest extent permitted by law, Pure Goat Farms and its owners, writers, contributors, partners, and affiliates are not liable for any direct, indirect, incidental, consequential, special, or punitive damages arising from your use of the website.</p>
    <p>This includes, but is not limited to, losses related to animal health, farm operations, product purchases, business decisions, data loss, website interruptions, or reliance on website content.</p>
    <h2>Indemnification</h2>
    <p>You agree to defend, indemnify, and hold harmless Pure Goat Farms, its owners, writers, contributors, affiliates, and partners from any claims, damages, losses, liabilities, costs, or expenses arising from your use of the website, your violation of these Terms of Use, or your submission of content.</p>
    <h2>Website Availability</h2>
    <p>We aim to keep the website available and functioning properly. However, we do not guarantee uninterrupted access. The website may be unavailable due to maintenance, technical issues, updates, security concerns, or circumstances beyond our control.</p>
    <h2>Changes to the Website</h2>
    <p>Pure Goat Farms may update, modify, remove, or discontinue any part of the website at any time without notice. We may also update content, tools, resources, or features as needed.</p>
    <h2>Changes to These Terms</h2>
    <p>We may revise these Terms of Use from time to time. Any changes will be posted on this page with an updated effective date.</p>
    <p>Continued use of the website after changes are posted means you accept the updated Terms of Use.</p>
    <h2>Governing Law</h2>
    <p>These Terms of Use shall be governed by and interpreted according to the laws of the United States and the state in which Pure Goat Farms operates, without regard to conflict of law principles.</p>
    <p>Any disputes related to these Terms or your use of the website shall be handled in the courts with jurisdiction where Pure Goat Farms operates, unless otherwise required by law.</p>
    <h2>Contact Information</h2>
    <p>If you have questions about these Terms of Use, please contact us:</p>
    <p>Pure Goat Farms<br>Website: <a href="/">https://puregoatfarms.com/</a><br>Email: <a href="mailto:info@puregoatfarms.com">info@puregoatfarms.com</a></p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
