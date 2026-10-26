<?php
$faqs = [
    ['q' => 'What is Best Jobs Pro?', 'a' => 'Best Jobs Pro is a Texas staffing agency and recruiting firm. We match job seekers with office, warehouse, skilled-trade, driving, food-service and customer-service jobs, and we help employers find, screen and onboard reliable people for temporary, temp-to-hire and direct-hire roles.'],
    ['q' => 'Does Best Jobs Pro charge job seekers a fee?', 'a' => 'No. Best Jobs Pro never charges employment or processing fees to applicants. Applying, interviewing and getting placed are all free for job seekers. Our staffing services are paid for by the employers we recruit for.'],
    ['q' => 'What kinds of jobs can Best Jobs Pro help me find?', 'a' => 'Our recruiters fill roles such as administrative assistants, receptionists, accounting specialists, warehouse packers and stockers, machine operators, welders, carpenters, apartment maintenance techs, CDL drivers, housekeeping and food service. See the Job Postings page for current openings.'],
    ['q' => 'How do I apply for a job through Best Jobs Pro?', 'a' => 'Fill out the online application, choose the job you want and upload your résumé if you have one. A recruiter reviews it, calls you to talk about your goals, and then matches you with employers hiring for your skills. You can also call 210-903-9471 at any hour.'],
    ['q' => 'How fast can Best Jobs Pro fill a position for my company?', 'a' => 'Timing depends on the role, but we start the search as soon as you call. Because we keep a pool of pre-screened candidates and handle sourcing, interviews, background checks and drug screening for you, many positions are filled far faster than a typical in-house hiring process.'],
    ['q' => 'Where is Best Jobs Pro located?', 'a' => 'Our office is at 2140 E Southlake Blvd, Southlake, TX 76092, and we recruit for employers across Texas. Our phone line, 210-903-9471, is answered 24 hours a day, 7 days a week.'],
];

page_start([
    'title'       => 'Best Jobs Pro | Texas Staffing Agency & Pro Recruiters',
    'description' => 'Best Jobs Pro is a Texas staffing agency matching job seekers with the best jobs and employers with pro talent. No fees for applicants. Call 24/7.',
    'path'        => '/',
    'preload'     => '/assets/img/site/Best-Jobs-Pro-Logo-Talent-Interview.webp',
    'body_class'  => 'home',
    'schema'      => [faq_schema($faqs)],
]);
?>
<section class="hero">
  <canvas class="net-canvas" aria-hidden="true"></canvas>
  <div class="arcs" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap hero__in">
    <div class="reveal in">
      <p class="eyebrow">Texas staffing agency &middot; No fees for job seekers</p>
      <h1>Best Jobs Pro: Texas Staffing for the <span class="accent">Best Jobs</span> &amp; Pro Talent</h1>
      <p class="hero__sub">Now matching <strong class="tw" data-typewriter="Welders|Receptionists|CDL Drivers|Warehouse Packers|Accounting Specialists|Skilled Carpenters|Machine Operators">Welders</strong> with Texas employers. Whether you want a better job or need dependable people, Best Jobs Pro connects the right person with the right role, fast.</p>
      <div class="hero__btns">
        <a class="btn" href="/applications/"><?= icon('file') ?> Find a Job</a>
        <a class="btn btn--ghost-light" href="/employers/"><?= icon('users') ?> Hire Talent</a>
      </div>
      <ul class="hero__trust">
        <li><?= icon('shield') ?> $0 employment or processing fees</li>
        <li><?= icon('clock') ?> Phones answered 24/7</li>
        <li><?= icon('usercheck') ?> Screened, job-ready candidates</li>
      </ul>
    </div>
    <div class="hero__visual" aria-hidden="true">
      <div class="hero__ring"></div>
      <img src="/assets/img/site/Best-Jobs-Pro-Logo-Talent-Interview.webp" alt="" width="739" height="739" fetchpriority="high">
      <div class="float-card float-card--1"><span class="fc-ico"><?= icon('wrench') ?></span><span><b>Welder</b><small>Full-time &middot; Texas</small></span><span class="fc-ok"><?= icon('check') ?></span></div>
      <div class="float-card float-card--2"><span class="fc-ico"><?= icon('briefcase') ?></span><span><b>Admin Assistant</b><small>Mon&ndash;Fri &middot; Office</small></span><span class="fc-ok"><?= icon('check') ?></span></div>
      <div class="float-card float-card--3"><span class="fc-ico"><?= icon('truck') ?></span><span><b>CDL Driver</b><small>Class A/B &middot; Routes</small></span><span class="fc-ok"><?= icon('check') ?></span></div>
    </div>
  </div>
  <svg class="hero__wave" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 70h1440V20c-240 40-480 50-720 30S240 0 0 30z"/></svg>
</section>

<section class="stats" aria-label="Best Jobs Pro at a glance">
  <div class="wrap">
    <div class="stats__grid reveal">
      <div class="stat-box"><strong data-count="16">16</strong><span>Job types hiring now</span></div>
      <div class="stat-box"><strong data-count="38">38</strong><span>In-demand skills we place</span></div>
      <div class="stat-box"><strong data-count="24" data-suffix="/7">24/7</strong><span>Phone line, every day</span></div>
      <div class="stat-box"><strong data-count="0" data-prefix="$">$0</strong><span>Fees for job seekers</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">Two ways we help</p>
      <h2>Pro jobs for job seekers. Pro staffing for employers.</h2>
      <p>Best Jobs Pro sits in the middle of the Texas job market. On one side are people who want steady, fairly paid work. On the other are businesses that need people they can count on. We do the matching.</p>
    </div>
    <div class="cards cards--3 stagger" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">
      <article class="card tilt">
        <div class="card__ico"><?= icon('briefcase') ?></div>
        <h3>Land your ideal job</h3>
        <p>Tell us what you are good at and what you want next. A Best Jobs Pro recruiter matches your skills, schedule and pay goals with Texas employers who are hiring, from office and admin roles to warehouse, trades and driving jobs. You never pay a fee.</p>
        <a class="card__link" href="/applications/">Apply now <?= icon('arrow') ?></a>
      </article>
      <article class="card tilt">
        <div class="card__ico"><?= icon('users') ?></div>
        <h3>Find and keep a solid workforce</h3>
        <p>Need one receptionist or a full night-shift crew? Best Jobs Pro sources, screens and onboards reliable people for temporary, temp-to-hire and direct-hire roles, so your team stays productive and your managers stay focused on the business.</p>
        <a class="card__link" href="/employers/">Find the best candidate <?= icon('arrow') ?></a>
      </article>
      <article class="card tilt">
        <div class="card__ico"><?= icon('compass') ?></div>
        <h3>Not sure where you fit?</h3>
        <p>Take our free Job Match Quiz. Six quick questions point you to the kinds of jobs that suit how you like to work, then show the openings that fit. It takes about a minute.</p>
        <a class="card__link" href="/career-tools/job-match-quiz/">Take the quiz <?= icon('arrow') ?></a>
      </article>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap split">
    <div class="split__media reveal">
      <span class="arc-deco" aria-hidden="true"></span>
      <img src="/assets/img/site/Best-Jobs-Pro-Recruitment.webp" alt="Best Jobs Pro recruiter interviewing a job candidate in Texas" width="737" height="737" loading="lazy">
    </div>
    <div class="reveal">
      <p class="eyebrow">Exceptional recruitment &amp; staffing</p>
      <h2>A Texas staffing agency that treats hiring like it matters</h2>
      <p>Best Jobs Pro was built on a simple idea: a company is only as strong as the people who show up for it every day. That is why we put real time into finding professionals who have the skills for the job and the drive to stick with it.</p>
      <p>Our recruiters know Texas industries, from construction and manufacturing to offices, apartment communities and logistics. That knowledge lets us look past keywords on a résumé and find the person who will fit your team, your schedule and your culture.</p>
      <ul class="checks">
        <li>Rigorous screening: skills checks, behavioral interviews and background checks</li>
        <li>Temporary, seasonal, temp-to-hire and direct-hire staffing</li>
        <li>No employment or processing fees for applicants, ever</li>
      </ul>
      <a class="btn" href="/about/">Learn more about Best Jobs Pro <?= icon('arrow') ?></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">What we do best</p>
      <h2>Why employers call Best Jobs Pro first</h2>
      <p>Eight things every client gets from our team, whether you need one hire or fifty.</p>
    </div>
    <div class="cards cards--4 stagger">
<?php
$best = [
    ['target', 'Strategic talent sourcing', 'We actively recruit people with the skills, experience and attitude your roles need, including candidates who are not scrolling job boards.'],
    ['layers', 'Customized recruiting', 'One executive assistant or a whole production line: we build the search around your requirements, budget and timeline.'],
    ['building', 'Industry expertise', 'Office, industrial, trades, hospitality and logistics. We know what good looks like in each and screen for it.'],
    ['clipboard', 'Assessment & screening', 'Skills tests, structured interviews and background checks mean you only meet qualified, reliable people.'],
    ['usercheck', 'Onboarding support', 'We help new hires start strong with paperwork, expectations and first-week check-ins that improve retention.'],
    ['repeat', 'Flexible staffing', 'Scale up for a busy season or a project, then scale back, without cutting corners on quality.'],
    ['link', 'Long-term partnership', 'The more we learn about your business, the better and faster every future match becomes.'],
    ['zap', 'Prompt, responsive service', 'Hiring is urgent. We pick up the phone 24/7 and start working your order the same day.'],
];
foreach ($best as $i => [$ic, $t, $d]): ?>
      <article class="card card--num tilt" data-n="<?= sprintf('%02d', $i + 1) ?>">
        <div class="card__ico"><?= icon($ic) ?></div>
        <h3><?= e($t) ?></h3>
        <p><?= e($d) ?></p>
      </article>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section--dark">
  <canvas class="net-canvas" aria-hidden="true"></canvas>
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow" style="color:#ffb3b3">How it works</p>
      <h2>From application to first day in four steps</h2>
      <p>The Best Jobs Pro process is simple, quick and free for job seekers.</p>
    </div>
    <ol class="timeline">
      <li><div class="timeline__dot"><?= icon('file') ?></div><h3>1. Apply online</h3><p>Send your details and résumé in about five minutes, or call us any time.</p></li>
      <li><div class="timeline__dot"><?= icon('headset') ?></div><h3>2. Talk with a recruiter</h3><p>We learn your skills, goals, schedule and the pay you are looking for.</p></li>
      <li><div class="timeline__dot"><?= icon('search') ?></div><h3>3. Get matched</h3><p>We introduce you to Texas employers whose openings fit you, and prep you for the interview.</p></li>
      <li><div class="timeline__dot"><?= icon('star') ?></div><h3>4. Start working</h3><p>Accept the offer and start. We stay in touch to make sure the job is a good fit.</p></li>
    </ol>
  </div>
</section>

<div class="marquee" aria-label="In-demand skills">
  <div class="marquee__track">
<?php
$skills = ['Accountant', 'ACDL Driver', 'Apartment Leasing', 'Assembly Crews', 'Bookkeeper', 'Carpenter', 'Clerical', 'Construction', 'Customer Service Rep', 'Data Entry Operator', 'Electrician', 'Executive Secretary', 'Food Service', 'Forklift', 'General Labor', 'Heavy Equipment Operator', 'Janitorial Staff', 'Machinist', 'Maintenance', 'Painter', 'Payroll Clerk', 'Receptionist', 'Sales & Marketing', 'Shipping & Receiving', 'Warehouse', 'Welder'];
foreach (array_merge($skills, $skills) as $i => $s): ?>
    <span<?= $i >= count($skills) ? ' aria-hidden="true"' : '' ?>><?= e($s) ?></span>
<?php endforeach; ?>
  </div>
</div>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">Supplementary services</p>
      <h2>Everything you need to hire with confidence</h2>
      <p>Beyond recruiting, Best Jobs Pro handles the checks and extras that keep your workplace safe and your workforce dependable.</p>
    </div>
    <div class="cards stagger" style="grid-template-columns:repeat(auto-fit,minmax(210px,1fr))">
      <article class="card tilt"><div class="card__ico"><?= icon('clock') ?></div><h3>24/7 workforce support</h3><p>Business does not stop at 5 p.m., and neither do we. Call any hour for coverage or a replacement.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('shield') ?></div><h3>Background checks</h3><p>Thorough, compliant background screening so every hiring decision is a well-informed one.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('flask') ?></div><h3>Drug screening</h3><p>Pre-employment drug testing that helps you keep a safe, productive and trusted team.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('search') ?></div><h3>Intensive recruiting</h3><p>Proactive outreach that finds strong candidates for hard-to-fill and specialized roles.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('gauge') ?></div><h3>Skills assessment</h3><p>Hands-on and written tests that confirm strengths, spot gaps and match people to the right work.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">Hiring now</p>
      <h2>Open job postings across Texas</h2>
      <p>A sample of the roles Best Jobs Pro is recruiting for right now. Every application is free.</p>
    </div>
    <div class="jobs stagger">
<?php
$catIcon = ['office' => 'briefcase', 'labor' => 'package', 'trades' => 'wrench', 'customer' => 'headset', 'driving' => 'truck'];
foreach (array_slice(JOBS, 0, 6) as [$name, $cat, $type, $desc]): ?>
      <article class="job-card">
        <div class="job-card__top"><span class="job-card__ico"><?= icon($catIcon[$cat]) ?></span><h3><?= e($name) ?></h3></div>
        <p><?= e($desc) ?></p>
        <div class="job-card__tags"><span class="tag tag--brand"><?= e(JOB_CATEGORIES[$cat]) ?></span><span class="tag"><?= e($type) ?></span><span class="tag">Texas</span></div>
        <a class="more" href="/applications/?job=<?= urlencode($name) ?>#apply-form">Apply for this job <?= icon('arrow') ?></a>
      </article>
<?php endforeach; ?>
    </div>
    <p style="text-align:center;margin-top:34px"><a class="btn btn--outline" href="/job-postings/">See all job postings <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">Free career tools</p>
      <h2>Job search pro tools, built by Best Jobs Pro</h2>
      <p>Plan your pay, sharpen your résumé and price your freelance work with free calculators that run right in your browser.</p>
    </div>
    <div class="cards cards--3 tool-cards stagger">
<?php foreach (TOOLS as $slug => [$title, $desc, $ic]): ?>
      <article class="card tilt">
        <div class="card__ico"><?= icon($ic) ?></div>
        <h3><?= e($title) ?></h3>
        <p><?= e($desc) ?></p>
        <a class="card__link" href="/career-tools/<?= $slug ?>/">Use the tool <?= icon('arrow') ?></a>
      </article>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--wide">
    <div class="reveal">
      <p class="eyebrow">Why job seekers choose us</p>
      <h2>The best jobs, a pro recruiter in your corner, and zero fees</h2>
      <p>Searching on your own means hundreds of listings, dozens of applications and a lot of silence. With Best Jobs Pro, a real recruiter reviews your background, tells you which openings fit, and puts your name in front of the hiring manager.</p>
      <ul class="checks checks--2">
        <li>Free for applicants</li>
        <li>Office, labor, trades &amp; driving</li>
        <li>Full-time, part-time &amp; shifts</li>
        <li>Temp, temp-to-hire &amp; direct hire</li>
        <li>Résumé and interview help</li>
        <li>Phones answered 24/7</li>
      </ul>
      <p>Limited experience? That is fine. Many of the employers who work with Best Jobs Pro will train the right person, and we will help you show them why that person is you.</p>
      <a class="btn" href="/applications/">Submit your application <?= icon('arrow') ?></a>
    </div>
    <div class="reveal">
      <div class="scan-visual" aria-hidden="true">
        <i class="h"></i><i></i><i class="k"></i><i></i><i></i><i class="k"></i><i></i><i></i><i></i><i class="k"></i><i></i><i></i><i></i><i class="k"></i><i></i>
      </div>
      <p style="text-align:center;margin-top:18px;font-weight:600">Is your résumé job-ready? <a href="/career-tools/resume-keyword-checker/">Scan it free</a>.</p>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">From the blog</p>
      <h2>Career advice from the Best Jobs Pro team</h2>
    </div>
    <div class="posts">
<?php foreach (array_slice(all_posts(), 0, 3) as $p) echo post_card($p); ?>
    </div>
    <p style="text-align:center;margin-top:34px"><a class="btn btn--outline" href="/blog/">Read more articles <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <?= faq_block($faqs, 'Best Jobs Pro FAQs') ?>
  </div>
</section>

<?= cta_band('Your next job or your next great hire is one call away', 'Call Best Jobs Pro at ' . SITE_PHONE . ' any time, day or night, or apply online in five minutes. No fees for job seekers.') ?>
<?php page_end();
