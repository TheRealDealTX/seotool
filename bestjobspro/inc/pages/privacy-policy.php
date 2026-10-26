<?php
page_start([
    'title'       => 'Privacy Policy | Best Jobs Pro',
    'description' => 'How Best Jobs Pro collects, uses and protects the information you share through our website, job applications, résumés and contact forms.',
    'path'        => '/privacy-policy/',
    'crumbs'      => [['Privacy Policy', '/privacy-policy/']],
]);
page_hero('Privacy Policy', 'Last updated October 26, 2026', [['Privacy Policy', '/privacy-policy/']], '/assets/img/site/best-jobs-pro-policy.webp');
?>
<section class="section">
  <div class="wrap prose" style="max-width:860px">
    <p class="lead">This policy explains what information Best Jobs Pro ("we," "us") collects through <a href="/">bestjobspro.com</a>, how we use it and the choices you have. If you have questions, email <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a> or call <?= SITE_PHONE ?>.</p>

    <h2 id="who-we-are">Who we are</h2>
    <p>Best Jobs Pro is a staffing and recruiting agency located at <?= SITE_STREET ?>, <?= SITE_CITY ?>, <?= SITE_REGION ?> <?= SITE_ZIP ?>, USA. Our website address is <?= SITE_URL ?>.</p>

    <h2 id="what-we-collect">Information we collect</h2>
    <ul>
      <li><strong>Job applications:</strong> your name, phone number, email address, the job you are interested in, how you heard about us, any message you include and your résumé or CV if you upload one.</li>
      <li><strong>Contact form messages:</strong> your name, email, phone number, whether you are a job seeker or employer, and your message.</li>
      <li><strong>Technical data:</strong> like most websites, our hosting provider records basic server logs (IP address, browser type, pages requested and time) for security and troubleshooting.</li>
    </ul>
    <p>Our career tools (paycheck, tax, rate and résumé calculators and the job quiz) run entirely in your browser. What you type into them is not sent to us or stored.</p>

    <h2 id="how-we-use-it">How we use your information</h2>
    <ul>
      <li>To review your application, contact you about job opportunities and match you with employers.</li>
      <li>To share your application details with prospective employers for roles you have expressed interest in.</li>
      <li>To respond to questions and staffing requests.</li>
      <li>To keep the website secure and working properly.</li>
    </ul>
    <p>We do not sell your personal information, and we never charge job seekers employment or processing fees.</p>

    <h2 id="sharing">Who we share it with</h2>
    <p>We share applicant information with employers only in connection with job opportunities. We also use service providers that help us operate, such as our web host and email provider, who process data on our behalf. With your consent, and where the law allows, we may use third-party providers for background checks or drug screening as part of a hiring process. We may disclose information if required by law.</p>

    <h2 id="cookies">Cookies</h2>
    <p>This website does not use advertising or tracking cookies. Embedded content, such as the Google Map on our contact page, may set its own cookies according to that provider's policies.</p>

    <h2 id="retention">How long we keep it</h2>
    <p>Applications and résumés are kept as long as needed to consider you for current and future roles, unless you ask us to delete them. Contact messages are kept as long as needed to respond and for reasonable business records.</p>

    <h2 id="your-rights">Your choices and rights</h2>
    <p>You can ask us to access, correct or delete the personal information you sent us, or to stop contacting you, by emailing <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a>. We may keep information we are required to retain for legal, administrative or security reasons.</p>

    <h2 id="security">Security</h2>
    <p>Our site uses HTTPS encryption, and form submissions are delivered by email to our team rather than stored in a public database. No method of transmission is perfectly secure, so please do not include sensitive information such as Social Security numbers in forms or résumés.</p>

    <h2 id="links">Links to other websites</h2>
    <p>Articles on this site may link to other websites. We are not responsible for their content or privacy practices.</p>

    <h2 id="changes">Changes to this policy</h2>
    <p>We may update this policy from time to time. The date at the top shows when it last changed.</p>
  </div>
</section>
<?php page_end();
