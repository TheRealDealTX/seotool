<?php
require __DIR__ . '/../inc/layout.php';

page_start([
    'title' => 'Terms of Use | Monetizing Influencers',
    'description' => 'The terms of use for the Monetizing Influencers website, free creator tools, guest post submissions and web design services.',
    'path' => '/terms/',
    'extra_css' => ['/assets/css/pages.css'],
]);

page_hero('Legal', 'Terms of Use', 'Please read these terms before using the Monetizing Influencers website, tools and services.', [['Terms of Use', '/terms/']]);
?>
<section class="section" style="padding-top:10px">
  <div class="wrap narrow prose legal">
    <p class="updated">Last updated: October 25, 2026</p>

    <h2>Acceptance of these terms</h2>
    <p>By using monetizinginfluencers.com (the "site"), operated by Monetizing Influencers, you agree to these terms. If you do not agree, please do not use the site.</p>

    <h2>Informational content only</h2>
    <p>The guides, articles and examples on this site are for general information and education. They are not legal, tax, financial or professional advice. Rules for platforms, sponsorship disclosure and taxes change and vary by country, so check current requirements or speak to a qualified professional before acting.</p>

    <h2>Estimates are not guarantees</h2>
    <p>Rate ranges, income figures and the results of our free tools (including the earnings calculator, engagement rate calculator, income stream simulator and readiness quiz) are estimates based on general benchmarks and the information you enter. They are not promises or guarantees of income. Actual results depend on your audience, niche, content, market conditions and many other factors.</p>

    <h2>Use of the site</h2>
    <p>You agree not to misuse the site, including by attempting to break its security, sending spam through our forms, scraping it in a way that harms its performance, or using it for unlawful purposes. Content and tools you generate with our tools (for example emails and media kits) are yours to use.</p>

    <h2>Intellectual property</h2>
    <p>The site design, text, graphics, logo and code are owned by Monetizing Influencers or used with permission, and are protected by copyright and trademark law. You may share links to our pages and quote short excerpts with attribution. Please do not copy whole articles or tools without written permission.</p>

    <h2>Guest posts</h2>
    <p>By submitting an article through our <a href="/write-for-us/">write for us</a> program you confirm it is your original, unpublished work and does not infringe anyone else's rights. If we accept and publish it, you grant Monetizing Influencers exclusive publishing rights as described in our guidelines, and we may edit it for grammar, SEO, clarity and length. We may decline any submission.</p>

    <h2>Web design services</h2>
    <p>Our <a href="/website-design/">web design for influencers</a> service is provided under the scope, timeline and price agreed with you in writing before work begins. Unless agreed otherwise, the advertised one-time price covers the inclusions listed on that page. You are responsible for the accuracy and rights of the content, images and brand assets you supply.</p>

    <h2>Third-party links and platforms</h2>
    <p>The site links to and discusses third-party websites and platforms. We do not control them and are not responsible for their content, policies or changes to their monetization programs.</p>

    <h2>Disclaimer and limitation of liability</h2>
    <p>The site and tools are provided "as is" without warranties of any kind. To the fullest extent permitted by law, Monetizing Influencers is not liable for any indirect, incidental or consequential loss, or for any loss of income, arising from your use of the site or reliance on its content. Where liability cannot be excluded, it is limited to the amount you paid us, if any, for the service concerned.</p>

    <h2>Governing law</h2>
    <p>These terms are governed by the laws of the State of Texas, USA, without regard to its conflict of law rules. Any dispute will be handled in the state or federal courts located in Tarrant County, Texas.</p>

    <h2>Changes</h2>
    <p>We may update these terms at any time. The "last updated" date shows when they were last changed, and continued use of the site means you accept the updated terms.</p>

    <h2>Contact</h2>
    <p>Questions? Email <a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a> or call <?= e(SITE_PHONE) ?>.</p>
  </div>
</section>
<?php page_end();
