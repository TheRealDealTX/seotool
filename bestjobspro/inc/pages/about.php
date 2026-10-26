<?php
$faqs = [
    ['q' => 'Is Best Jobs Pro a staffing agency or a recruiter?', 'a' => 'Both. Best Jobs Pro provides temporary and temp-to-hire staffing, and we also recruit for permanent, direct-hire positions. Employers choose the arrangement that fits each role.'],
    ['q' => 'Which industries does Best Jobs Pro recruit for?', 'a' => 'We recruit for offices and administration, accounting, warehousing and logistics, manufacturing and production, construction and skilled trades, apartment and property maintenance, hospitality, food service and transportation.'],
    ['q' => 'How do I reach Best Jobs Pro?', 'a' => 'Call 210-903-9471 any time, 24/7, email careers@bestjobspro.com, or use the contact form. Our office is at 2140 E Southlake Blvd, Southlake, TX 76092.'],
];
page_start([
    'title'       => 'About Best Jobs Pro | Texas Staffing & Recruiting Agency',
    'description' => 'Meet Best Jobs Pro, the Texas staffing agency and pro recruiters connecting employers with dependable talent and job seekers with the best jobs, fee-free.',
    'path'        => '/about/',
    'crumbs'      => [['About', '/about/']],
    'schema'      => [faq_schema($faqs), ['@type' => 'AboutPage', 'name' => 'About Best Jobs Pro', 'url' => url('/about/'), 'about' => ['@id' => SITE_URL . '/#organization']]],
]);
page_hero('About Best Jobs Pro', 'A Texas staffing agency with one job: put the right people in the right roles, quickly and without fees for job seekers.', [['About', '/about/']], '/assets/img/site/About-Best-Jobs-Pro-Background.webp', 'Who we are');
?>
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Our story</p>
      <h2>Staffing built on the belief that people make the business</h2>
      <p>Best Jobs Pro is a staffing and recruiting agency based in Southlake, Texas. We work with Texas employers that need reliable people, and with job seekers who want work that fits their skills, schedule and goals.</p>
      <p>We started from a conviction every manager eventually learns the hard way: the success of a company is tied to the skill and determination of the people on its team. So we spend our time where it counts, finding and vetting professionals who can do the work and who share your commitment to doing it well.</p>
      <p>Our recruiters understand how different industries hire. A night-shift machine operator, a bilingual receptionist and a certified welder are three very different searches, and we treat them that way.</p>
    </div>
    <div class="split__media reveal">
      <span class="arc-deco" aria-hidden="true"></span>
      <img src="/assets/img/site/Best-Jobs-Pro-Logo-Talent-Interview.webp" alt="Best Jobs Pro recruiter talking with a job candidate" width="739" height="739" loading="lazy">
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head reveal">
      <p class="eyebrow">What drives us</p>
      <h2>Our mission and values</h2>
      <p>Help Texas companies grow by hiring the best available talent, and help Texas workers land jobs where they are valued.</p>
    </div>
    <div class="cards cards--4 stagger">
      <article class="card tilt"><div class="card__ico"><?= icon('zap') ?></div><h3>Urgency</h3><p>When you call, we move. Every hiring request gets priority attention from the moment it reaches our office.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('target') ?></div><h3>Precision</h3><p>We match on skills, experience, schedule and culture, so the person we send is the person you needed.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('shield') ?></div><h3>Integrity</h3><p>No fees for applicants. Honest feedback for both sides. Compliant screening and fair treatment.</p></article>
      <article class="card tilt"><div class="card__ico"><?= icon('heart') ?></div><h3>Respect</h3><p>Your time matters, whether you are a hiring manager or a candidate. We keep you informed at every step.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--wide">
    <div class="reveal">
      <p class="eyebrow">For employers</p>
      <h2>The key to your company's next stage of growth</h2>
      <p>Whether you need to fill a critical leadership seat, strengthen your core operations team, or add customer-facing staff who make a great first impression, Best Jobs Pro has the tools, network and experience to deliver with speed and accuracy.</p>
      <p>As soon as you reach out, our team gets to work: defining the role with you, sourcing candidates, screening and interviewing them, running background checks and drug screens, and presenting only the people who fit your needs and your culture.</p>
      <a class="btn" href="/employers/">Staffing for employers <?= icon('arrow') ?></a>
    </div>
    <div class="reveal">
      <div class="tiles">
        <a class="tile" href="tel:<?= SITE_TEL ?>"><span class="tile__ico"><?= icon('phone') ?></span><span><small>Call 24/7</small><b><?= SITE_PHONE ?></b></span></a>
        <a class="tile" href="mailto:<?= SITE_EMAIL ?>"><span class="tile__ico"><?= icon('mail') ?></span><span><small>Email</small><b><?= SITE_EMAIL ?></b></span></a>
        <a class="tile" href="<?= SITE_MAP ?>" target="_blank" rel="noopener"><span class="tile__ico"><?= icon('pin') ?></span><span><small>Office</small><b><?= SITE_STREET ?>, <?= SITE_CITY ?>, TX</b></span></a>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap"><?= faq_block($faqs, 'About Best Jobs Pro: common questions') ?></div>
</section>
<?= cta_band('Let the right people shape your company\'s future') ?>
<?php page_end();
