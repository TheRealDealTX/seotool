<?php
$faqs = [
    ['q' => 'What staffing services does Best Jobs Pro offer?', 'a' => 'Temporary staffing, temp-to-hire, direct-hire recruiting, seasonal and project staffing, plus background checks, drug screening, skills assessments and onboarding support.'],
    ['q' => 'What is the difference between temp, temp-to-hire and direct hire?', 'a' => 'Temporary staff work for a set period or project. Temp-to-hire lets you try a worker on the job before offering a permanent position. Direct hire means we recruit and screen, and the candidate joins your payroll from day one.'],
    ['q' => 'Do you help people with little work experience?', 'a' => 'Yes. Many entry-level warehouse, food-service, housekeeping and general-labor roles do not need experience, and our recruiters help you present your strengths to employers who are willing to train.'],
];
page_start([
    'title'       => 'Staffing & Recruiting Services in Texas | Best Jobs Pro',
    'description' => 'Temp, temp-to-hire and direct-hire staffing in Texas, plus background checks, drug screening and skills testing. See every Best Jobs Pro service.',
    'path'        => '/our-services/',
    'crumbs'      => [['Our Services', '/our-services/']],
    'schema'      => [faq_schema($faqs), ['@type' => 'Service', 'serviceType' => 'Staffing and recruiting', 'provider' => ['@id' => SITE_URL . '/#organization'], 'areaServed' => 'Texas', 'url' => url('/our-services/')]],
]);
page_hero('Staffing &amp; Recruiting Services in Texas', 'Find your perfect match, whether that is a new job or a new team member. Best Jobs Pro guides employers and job seekers through every step of hiring.', [['Our Services', '/our-services/']], '/assets/img/site/best-jobs-pro-services-copy.webp', 'Our services');
?>
<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">Staffing options</p>
      <h2>Flexible staffing that fits the way you hire</h2>
      <p>Every role is different. Choose the arrangement that makes sense, and switch as your needs change.</p>
    </div>
    <div class="cards cards--4 stagger">
      <article class="card tilt"><div class="card__ico"><?= icon('clock') ?></div><h3>Temporary staffing</h3><p>Cover vacations, leave, peak seasons and special projects with ready-to-work people.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('repeat') ?></div><h3>Temp-to-hire</h3><p>See how someone performs on the job before you make a permanent offer.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('usercheck') ?></div><h3>Direct hire</h3><p>We recruit, screen and present finalists. You hire them onto your payroll.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('users') ?></div><h3>Volume &amp; project staffing</h3><p>Crews for production lines, warehouses, construction and event work.</p></article>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap split">
    <div class="split__media reveal">
      <span class="arc-deco" aria-hidden="true"></span>
      <img src="/assets/img/site/Best-Jobs-Pro-Recruitment.webp" alt="Best Jobs Pro recruitment service for Texas employers" width="737" height="737" loading="lazy">
    </div>
    <div class="reveal">
      <p class="eyebrow">For employers</p>
      <h2>Finding the right candidates</h2>
      <p>Our talent solutions connect Texas businesses with candidates who are qualified, screened and ready. Every potential hire goes through a structured process so only the strongest people reach your desk.</p>
      <ul class="checks">
        <li>Role intake: duties, schedule, pay range and culture</li>
        <li>Sourcing from our candidate pool and active outreach</li>
        <li>Skills assessment and structured interviews</li>
        <li>Background checks and drug screening</li>
        <li>Shortlist, interviews, offer and onboarding support</li>
      </ul>
      <a class="btn" href="/employers/">Request candidates <?= icon('arrow') ?></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">For job seekers</p>
      <h2>Finding the right job</h2>
      <p>Your skills, education and background are worth more than a résumé buried in an inbox. Our recruiters take time to understand what you want, help you present yourself well, and introduce you to employers looking for exactly that.</p>
      <p>Just starting out or decades in? Limited experience should never stop you from landing a good position, especially with Best Jobs Pro on your side. And you will never pay us a fee.</p>
      <div class="hero__btns" style="margin:0"><a class="btn" href="/applications/">Submit your application <?= icon('arrow') ?></a><a class="btn btn--outline" href="/career-tools/resume-keyword-checker/">Check your résumé</a></div>
    </div>
    <div class="split__media reveal">
      <span class="arc-deco" aria-hidden="true"></span>
      <img src="/assets/img/site/Best-Jobs-Pro-Job-Applicant.webp" alt="Job applicant working with Best Jobs Pro to find the right job" width="737" height="737" loading="lazy">
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">Supplementary services</p>
      <h2>Screening and support included</h2>
    </div>
    <div class="cards stagger" style="grid-template-columns:repeat(auto-fit,minmax(210px,1fr))">
      <article class="card tilt"><div class="card__ico"><?= icon('shield') ?></div><h3>Background checks</h3><p>Verify history and credentials before anyone starts.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('flask') ?></div><h3>Drug screening</h3><p>Pre-employment testing for safer, more reliable teams.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('gauge') ?></div><h3>Skills assessment</h3><p>Typing, software, trade and aptitude testing matched to the role.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('search') ?></div><h3>Intensive recruiting</h3><p>Targeted searches for specialized and hard-to-fill jobs.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('headset') ?></div><h3>24/7 support</h3><p>Call-outs and urgent orders handled day or night.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">In-demand skills</p>
      <h2>Positions we staff every day</h2>
      <p>If your role is not listed, call us. Our recruiters fill a wide range of Texas jobs.</p>
    </div>
    <div class="skills reveal">
<?php foreach (['Accountant', 'ACDL Driver', 'Apartment Leasing', 'Assembly Crews', 'Bookkeeper', 'Carpenter', 'Clerical', 'Construction', 'Credit & Collection Staff', 'Customer Service Rep', 'Demonstrator', 'Secretary', 'File Clerk', 'Data Entry Operator', 'Electrician', 'Executive Secretary', 'Food Service', 'Framers', 'General Labor', 'General Office', 'Heavy Equipment Operator', 'Industrial', 'Insurance Clerk', 'Inventory Staff', 'Janitorial Staff', 'Machinist', 'Maintenance Work', 'Painter', 'Payroll Clerk', 'Production', 'Receptionist', 'Sales & Marketing', 'Shipping and Receiving', 'Telemarketer', 'Trimmers', 'Typist', 'Warehouse Work', 'Welder'] as $s): ?>
      <span><?= e($s) ?></span>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap"><?= faq_block($faqs, 'Staffing services FAQs') ?></div>
</section>
<?= cta_band() ?>
<?php page_end();
