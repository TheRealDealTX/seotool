<?php
require __DIR__ . '/../inc/layout.php';

page_start([
    'title' => 'Privacy Policy | Monetizing Influencers',
    'description' => 'How Monetizing Influencers collects, uses and protects the information you share through our forms and tools, and how to request access or deletion.',
    'path' => '/privacy-policy/',
    'extra_css' => ['/assets/css/pages.css'],
]);

page_hero('Legal', 'Privacy Policy', 'Your privacy matters to us. This policy explains what information Monetizing Influencers collects, why, and the choices you have.', [['Privacy Policy', '/privacy-policy/']]);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap narrow prose legal">
    <p class="updated">Last updated: October 25, 2026</p>

    <h2>Who we are</h2>
    <p>This website, <a href="/">monetizinginfluencers.com</a>, is operated by Monetizing Influencers, <?= e(SITE_STREET . ', ' . SITE_CITY . ', ' . SITE_REGION . ' ' . SITE_ZIP) ?>, USA ("we", "us", "our"). You can contact us at <a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a>.</p>

    <h2>Information we collect</h2>
    <p><strong>Information you give us.</strong> When you use a form on this site (contact, get started, newsletter, web design quote or write for us), we collect the details you enter, such as your name, email address, social media handles, website, niche, follower range, country and your message or pitch.</p>
    <p><strong>Information collected automatically.</strong> Like most websites, our server records basic technical data with each request, such as your IP address, browser type, the page requested and the date and time. When you submit a form we record your IP address with the submission to help prevent spam and abuse.</p>
    <p><strong>Free tools.</strong> Our calculators, generators and quiz run in your browser. The numbers and text you enter into them are not sent to us unless you choose to submit a form.</p>
    <p>We do not run user accounts, and we do not knowingly collect payment card details on this website.</p>

    <h2>How we use your information</h2>
    <ul>
      <li>To reply to your message, quote request or guest post pitch.</li>
      <li>To prepare the monetization outline you request through Get Started.</li>
      <li>To send our newsletter if you subscribe (you can unsubscribe at any time).</li>
      <li>To keep the website secure and prevent spam or misuse.</li>
      <li>To understand how the website is used and improve it.</li>
    </ul>
    <p>Form submissions are emailed to our inbox and a copy is stored on our web server, which is not publicly accessible. We do not sell or rent your personal information.</p>

    <h2>Cookies and analytics</h2>
    <p>This website does not set advertising or tracking cookies of its own. We may use Google Analytics to understand how visitors use the site; if enabled, Google Analytics uses cookies to collect information such as pages visited and time on site, and that data is processed by Google under its own <a href="https://policies.google.com/privacy" rel="noopener">privacy policy</a>. You can opt out with Google's browser add-on or your browser's cookie settings.</p>

    <h2>Third-party services</h2>
    <p>Our pages load fonts from Google Fonts, which means your browser connects to Google's servers and shares your IP address with Google. Our hosting provider processes server data on our behalf. Links to other websites are provided for convenience; we are not responsible for their content or privacy practices.</p>

    <h2>How long we keep information</h2>
    <p>We keep form submissions for as long as needed to respond and for our business records, normally no longer than three years, unless you ask us to delete them sooner. Newsletter subscriptions are kept until you unsubscribe.</p>

    <h2>Your rights</h2>
    <p>Depending on where you live (for example under the GDPR in the EU and UK or the CCPA in California), you may have the right to access, correct, delete or receive a copy of your personal information, to object to or restrict certain processing, and to withdraw consent. To make a request, email <a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a>. We will respond within a reasonable time and will not discriminate against you for exercising your rights.</p>

    <h2>Security</h2>
    <p>The site is served over HTTPS and stored submissions are kept outside the public web directory. No method of transmission or storage is completely secure, but we take reasonable steps to protect your information.</p>

    <h2>Children</h2>
    <p>This website is intended for adults and is not directed at children under 13. We do not knowingly collect personal information from children. If you believe a child has sent us information, please contact us and we will delete it.</p>

    <h2>Changes to this policy</h2>
    <p>We may update this policy from time to time. The "last updated" date above shows when it was last changed.</p>

    <h2>Contact</h2>
    <p>Questions about this policy? Email <a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a>, call <?= e(SITE_PHONE) ?> or write to us at <?= e(SITE_STREET . ', ' . SITE_CITY . ', ' . SITE_REGION . ' ' . SITE_ZIP) ?>, USA.</p>
  </div>
</section>
<?php page_end();
