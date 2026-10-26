<?php
page_start([
    'title'       => 'Terms of Use | Best Jobs Pro',
    'description' => 'Terms for using the Best Jobs Pro website, job postings, online application and free career tools.',
    'path'        => '/terms-of-use/',
    'crumbs'      => [['Terms of Use', '/terms-of-use/']],
]);
page_hero('Terms of Use', 'Last updated October 26, 2026', [['Terms of Use', '/terms-of-use/']], '/assets/img/site/best-jobs-pro-policy.webp');
?>
<section class="section">
  <div class="wrap prose" style="max-width:860px">
    <p class="lead">By using bestjobspro.com you agree to these terms. If you do not agree, please do not use the site.</p>
    <h2 id="services">Our services</h2>
    <p>Best Jobs Pro is a staffing and recruiting agency. Job postings on this site describe roles we are recruiting for; availability changes often and a posting is not an offer of employment. Submitting an application does not guarantee placement. We never charge job seekers employment or processing fees.</p>
    <h2 id="tools">Career tools and articles</h2>
    <p>Our calculators, quiz and articles are for general information only. Tax, pay and cost figures are estimates and are not tax, legal or financial advice. Check official sources or a qualified professional before making decisions.</p>
    <h2 id="your-info">Information you submit</h2>
    <p>You agree that information you submit is accurate and that you have the right to share it. Please do not submit sensitive data such as Social Security numbers through website forms. Our <a href="/privacy-policy/">Privacy Policy</a> explains how we handle your information.</p>
    <h2 id="use">Acceptable use</h2>
    <p>Do not misuse the site, attempt to disrupt it, submit spam or false applications, or copy its content for commercial use without permission.</p>
    <h2 id="ip">Content ownership</h2>
    <p>The Best Jobs Pro name, logo and site content belong to Best Jobs Pro. Linking to our pages is welcome.</p>
    <h2 id="liability">Limitation of liability</h2>
    <p>The site is provided "as is." To the extent permitted by law, Best Jobs Pro is not liable for losses arising from use of the site or reliance on its content.</p>
    <h2 id="contact">Contact</h2>
    <p>Questions? Email <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a> or call <?= SITE_PHONE ?>.</p>
  </div>
</section>
<?php page_end();
