<?php
require_once __DIR__ . '/data.php';

$faqs = [
    ['q' => 'What is the average insurance adjuster salary?',
     'a' => 'The Bureau of Labor Statistics reports a median of $76,790 a year ($36.92 an hour) for claims adjusters, appraisers, examiners and investigators (May 2024). Most staff adjusters earn between about $52,000 and $92,000 depending on line of business, experience and location.'],
    ['q' => 'How much do insurance adjusters make in their first year?',
     'a' => 'Trainee and entry-level staff adjusters usually start between $45,000 and $60,000 plus benefits. Independent adjusters who land catastrophe deployments can out-earn that in a strong storm season, but first-year IA income is unpredictable.'],
    ['q' => 'Which type of adjuster earns the highest salary?',
     'a' => 'Experienced catastrophe (CAT) and large-loss commercial adjusters have the highest earning ceilings, with busy-year incomes of $150,000 to $250,000 or more. Staff large-loss and complex-claims adjusters commonly earn $85,000 to $120,000 with full benefits.'],
    ['q' => 'How do insurance adjusters get paid?',
     'a' => 'Staff adjusters receive a W-2 salary. Independent adjusters are paid per claim from a fee schedule tied to the size of the loss, or a daily rate, and split the fee with their IA firm. Public adjusters earn a percentage of the policyholder\'s settlement, typically 10% to 20%.'],
    ['q' => 'How long does it take to become an insurance adjuster?',
     'a' => 'Many people complete an online pre-licensing course and pass the state exam within one to two weeks. Texas is a popular license choice because it offers reciprocity with most states that license adjusters.'],
    ['q' => 'Does an insurance adjuster salary vary by state?',
     'a' => 'Yes. Staff pay tracks local wage levels, so states like California, New York, New Jersey and Massachusetts pay more, while catastrophe-prone states like Texas, Florida, Louisiana and Oklahoma offer the most claim volume for independent adjusters.'],
];

$posts = array_slice(all_posts(), 0, 6);

$page = [
    'title'       => 'Insurance Adjuster Salary (2026): How Much Adjusters Make',
    'description' => 'Insurance adjuster salary data for 2026: staff, independent, CAT and public adjuster pay, salary by state, free calculators, and how to get licensed fast.',
    'path'        => '/',
    'body_class'  => 'has-hero',
    'preload'     => 'hero-roof-inspection.webp',
    'scripts'     => ['salary-model.js', 'home.js'],
    'schema'      => [[
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($f) => ['@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']]], $faqs),
    ]],
];
require __DIR__ . '/header.php';
?>

<section class="hero">
  <div class="hero-media"><img src="/assets/img/hero-roof-inspection.webp" alt="Insurance adjuster inspecting a residential roof for storm damage" width="1600" height="1067" fetchpriority="high"></div>
  <div class="hero-orb o1" aria-hidden="true"></div>
  <div class="hero-orb o2" aria-hidden="true"></div>
  <div class="container hero-inner">
    <div>
      <span class="eyebrow anim">2026 pay guide &amp; free tools</span>
      <h1 class="anim d1">Insurance Adjuster Salary: What <span class="grad">Adjusters Really Earn</span></h1>
      <p class="hero-lead anim d2">Real numbers on insurance adjuster salary for <span class="typed" data-words="staff adjusters|independent adjusters|CAT adjusters|public adjusters|desk adjusters">staff adjusters</span> &mdash; plus calculators, state-by-state pay and a fast path to your license.</p>
      <div class="hero-actions anim d3">
        <a class="btn btn-gold btn-lg pulse" href="/salary-calculator/"><?= icon('calc', 20) ?> Calculate Your Salary</a>
        <a class="btn btn-ghost btn-lg" href="<?= COURSE_URL ?>" target="_blank" rel="sponsored noopener">Get Certified This Week</a>
      </div>
      <div class="hero-badges anim d4">
        <span><?= icon('check', 18) ?> BLS-anchored data</span>
        <span><?= icon('check', 18) ?> 4 free calculators</span>
        <span><?= icon('check', 18) ?> Licensed in about a week</span>
      </div>
    </div>
    <aside class="glass hero-card anim d3" aria-label="Insurance adjuster salary snapshot">
      <h2>National median pay</h2>
      <p class="sub">Claims adjusters, appraisers, examiners &amp; investigators</p>
      <div class="big-number"><span data-count="<?= BLS_MEDIAN_ANNUAL ?>" data-prefix="$">$0</span><small> /year</small></div>
      <div class="mini-bars">
        <div class="mini-bar"><span>Staff desk</span><span class="track"><span class="fill" data-width="52%"></span></span><b>$65k</b></div>
        <div class="mini-bar"><span>Staff field</span><span class="track"><span class="fill" data-width="61%"></span></span><b>$76k</b></div>
        <div class="mini-bar"><span>Independent</span><span class="track"><span class="fill" data-width="70%"></span></span><b>$88k</b></div>
        <div class="mini-bar"><span>CAT adjuster</span><span class="track"><span class="fill" data-width="88%"></span></span><b>$110k</b></div>
        <div class="mini-bar"><span>Public adjuster</span><span class="track"><span class="fill" data-width="72%"></span></span><b>$90k</b></div>
      </div>
      <p class="src">Median: BLS Occupational Outlook Handbook, May 2024. Role figures: typical mid-career estimates.</p>
    </aside>
  </div>
  <a class="scroll-cue" href="#overview" aria-label="Scroll to content"></a>
</section>

<div class="container stats-wrap">
  <div class="stats reveal">
    <div class="stat"><strong data-count="<?= BLS_MEDIAN_ANNUAL ?>" data-prefix="$">$0</strong><span>Median annual pay</span></div>
    <div class="stat"><strong data-count="<?= BLS_MEDIAN_HOURLY ?>" data-prefix="$" data-decimals="2">$0</strong><span>Median hourly wage</span></div>
    <div class="stat"><strong data-count="365300">0</strong><span>Jobs nationwide</span></div>
    <div class="stat"><strong data-count="7" data-suffix=" days">0</strong><span>To get licensed online</span></div>
  </div>
</div>

<section class="section" id="overview">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">The quick answer</span>
      <h2>What is the average insurance adjuster salary?</h2>
      <p>The typical insurance adjuster salary in the United States is <strong>$76,790 a year</strong>, or about $36.92 an hour, according to the Bureau of Labor Statistics. That figure is a median, so half of adjusters earn more and half earn less.</p>
      <p>Where you land depends on how you work. A staff adjuster on salary trades upside for stability and benefits. An independent or catastrophe adjuster is paid per claim and can double the median in an active storm year &mdash; or fall well short of it in a quiet one. Public adjusters earn a percentage of each settlement they negotiate for policyholders.</p>
      <div class="callout"><strong>Bottom line:</strong> an insurance adjuster salary usually starts in the $45,000&ndash;$60,000 range, climbs to $70,000&ndash;$90,000 within a few years, and can pass six figures for senior, large-loss and CAT adjusters.</div>
      <a class="link-arrow" href="<?= BLOG_BASE ?>how-much-do-insurance-adjusters-make/">How much do insurance adjusters make? Full breakdown <?= icon('arrow', 16) ?></a>
    </div>
    <div class="photo-frame reveal reveal-delay-2">
      <img src="/assets/img/docs-calculator.webp" alt="Adjuster reviewing claim paperwork and a calculator to estimate a payout" width="1200" height="675" loading="lazy">
      <div class="photo-badge"><?= icon('trend', 30) ?><div><strong>6 figures</strong><span>Possible in year one*</span></div></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
<?php $roles = ['Staff Adjuster', 'Independent Adjuster', 'CAT Adjuster', 'Public Adjuster', 'Desk Adjuster', 'Field Adjuster', 'Auto Appraiser', 'Workers Comp Adjuster', 'Large Loss Adjuster', 'Bodily Injury Adjuster'];
for ($i = 0; $i < 2; $i++) foreach ($roles as $r) echo '    <span>' . e($r) . "</span>\n"; ?>
  </div>
</div>

<section class="section section-soft" id="salary-guide">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Salary by adjuster type</span>
      <h2>Insurance adjuster salary by role</h2>
      <p>The four career paths pay in completely different ways. Here is what each one typically earns and what comes with it.</p>
    </div>
    <div class="grid-4">
      <article class="card pay-card spotlight tilt reveal">
        <div class="icon-wrap"><?= icon('brief', 26) ?></div>
        <h3>Staff adjuster</h3>
        <div class="range">$52k&ndash;$92k</div>
        <div class="range-note">W-2 salary with an insurance carrier</div>
        <ul class="ticks">
          <li><?= icon('check', 16) ?> Health, 401(k) and paid time off</li>
          <li><?= icon('check', 16) ?> Company car for field roles</li>
          <li><?= icon('check', 16) ?> Predictable hours and pay</li>
        </ul>
      </article>
      <article class="card pay-card spotlight tilt reveal reveal-delay-1">
        <div class="icon-wrap"><?= icon('user', 26) ?></div>
        <h3>Independent adjuster</h3>
        <div class="range">$45k&ndash;$130k</div>
        <div class="range-note">1099 contractor paid per claim</div>
        <ul class="ticks">
          <li><?= icon('check', 16) ?> Fee schedule tied to loss size</li>
          <li><?= icon('check', 16) ?> 65&ndash;75% fee split is common</li>
          <li><?= icon('check', 16) ?> You choose your deployments</li>
        </ul>
      </article>
      <article class="card pay-card spotlight tilt reveal reveal-delay-2">
        <div class="icon-wrap"><?= icon('storm', 26) ?></div>
        <h3>CAT adjuster</h3>
        <div class="range">$50k&ndash;$200k+</div>
        <div class="range-note">Deploys after hurricanes, hail &amp; wildfire</div>
        <ul class="ticks">
          <li><?= icon('check', 16) ?> $15k&ndash;$60k+ per deployment</li>
          <li><?= icon('check', 16) ?> 7-day weeks during storms</li>
          <li><?= icon('check', 16) ?> Highest earning ceiling</li>
        </ul>
      </article>
      <article class="card pay-card spotlight tilt reveal reveal-delay-3">
        <div class="icon-wrap"><?= icon('percent', 26) ?></div>
        <h3>Public adjuster</h3>
        <div class="range">$50k&ndash;$150k+</div>
        <div class="range-note">Paid 10&ndash;20% of the settlement</div>
        <ul class="ticks">
          <li><?= icon('check', 16) ?> Works for the policyholder</li>
          <li><?= icon('check', 16) ?> Fees capped in many states</li>
          <li><?= icon('check', 16) ?> Income grows with referrals</li>
        </ul>
      </article>
    </div>
  </div>
</section>

<section class="section section-dark">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Interactive chart</span>
      <h2>Compare insurance adjuster salary ranges</h2>
      <p>Switch views to see how pay changes by adjuster type, line of business and years of experience.</p>
    </div>
    <div class="reveal" data-chart='<?= e(json_encode(chart_data())) ?>'>
      <div class="tabs" role="tablist" aria-label="Chart view"></div>
      <div class="bar-chart" aria-live="polite"></div>
      <p class="chart-note"></p>
    </div>
  </div>
</section>

<section class="section" id="estimator">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Free tool</span>
      <h2>Quick insurance adjuster salary estimator</h2>
      <p>Move the sliders to estimate your pay. For state, designation and benefits adjustments, open the full calculator.</p>
    </div>
    <div class="tool-shell reveal">
      <form class="tool-form" id="quick-est" onsubmit="return false">
        <div class="field">
          <span class="label">Adjuster type</span>
          <div class="seg">
            <input type="radio" name="role" id="qr-desk" value="desk" checked><label for="qr-desk">Staff desk</label>
            <input type="radio" name="role" id="qr-field" value="field"><label for="qr-field">Staff field</label>
            <input type="radio" name="role" id="qr-ind" value="independent"><label for="qr-ind">Independent</label>
            <input type="radio" name="role" id="qr-cat" value="cat"><label for="qr-cat">CAT</label>
          </div>
        </div>
        <div class="field">
          <label for="q-line">Line of business</label>
          <select id="q-line" name="line">
            <option value="property">Property (homeowners)</option>
            <option value="auto">Auto / material damage</option>
            <option value="wc">Workers compensation</option>
            <option value="casualty">Bodily injury / casualty</option>
            <option value="commercial">Commercial / large loss</option>
          </select>
        </div>
        <div class="field">
          <label for="q-years">Years of experience <output id="q-years-out">3</output></label>
          <input type="range" id="q-years" name="years" min="0" max="20" value="3">
        </div>
        <a class="btn btn-dark" href="/salary-calculator/">Open the full salary calculator <?= icon('arrow', 16) ?></a>
      </form>
      <div class="tool-result" aria-live="polite">
        <h3>Estimated annual pay</h3>
        <div class="result-big" id="q-mid">$0</div>
        <div class="result-sub" id="q-label">Staff desk adjuster</div>
        <div class="range-viz">
          <div class="track"><span class="band" id="q-band"></span><span class="pin" id="q-pin"></span></div>
          <div class="labels"><span>$30k</span><span>$130k</span><span>$230k</span></div>
        </div>
        <ul class="result-list">
          <li><span>Typical range</span><b id="q-range">-</b></li>
          <li><span>Hourly equivalent</span><b id="q-hour">-</b></li>
          <li><span>Monthly (gross)</span><b id="q-month">-</b></li>
        </ul>
        <p class="tool-disclaimer">Estimates only, anchored to the BLS national median. Not a job offer.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt" id="why">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Why Texas</span>
        <h2>Why become an insurance adjuster in Texas?</h2>
        <p>Texas is one of the best places to start an adjusting career &mdash; and one of the best licenses to hold even if you live somewhere else. It is a big reason the Texas insurance adjuster salary market stays so active year after year.</p>
        <a class="link-arrow" href="<?= BLOG_BASE ?>insurance-adjuster-salary-texas/">Insurance adjuster salary in Texas <?= icon('arrow', 16) ?></a>
      </div>
      <div class="photo-frame reveal reveal-delay-1">
        <img src="/assets/img/austin-skyline.webp" alt="Austin, Texas skyline at dusk" width="1200" height="675" loading="lazy">
      </div>
    </div>
    <div class="grid-4" style="margin-top:56px">
      <div class="card spotlight reveal"><div class="icon-wrap"><?= icon('star', 24) ?></div><h3>Recognized nationwide</h3><p>Texas has reciprocity with every state that allows licensing through reciprocity, so one license opens doors across the country.</p></div>
      <div class="card spotlight reveal reveal-delay-1"><div class="icon-wrap"><?= icon('book', 24) ?></div><h3>Simple licensing</h3><p>If your home state has no adjuster license of its own, you can designate Texas as your home state for licensing purposes.</p></div>
      <div class="card spotlight reveal reveal-delay-2"><div class="icon-wrap"><?= icon('map', 24) ?></div><h3>Texas is huge</h3><p>Hail, tornadoes, freezes and Gulf hurricanes create steady claim volume. Independent adjusters working Texas storms need a Texas license.</p></div>
      <div class="card spotlight reveal reveal-delay-3"><div class="icon-wrap"><?= icon('bolt', 24) ?></div><h3>Fast to start</h3><p>An online course and exam can have you licensed in about a week, without years of school or student debt.</p></div>
    </div>
  </div>
</section>

<section class="section" id="comparison">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Cost comparison</span>
      <h2>Entry into insurance adjusting is relatively easy</h2>
      <p>Doctors and lawyers spend years in school and often carry six-figure debt before they earn a professional income. A strong insurance adjuster salary is within reach without either.</p>
    </div>
    <div class="compare reveal">
      <div class="compare-col college">
        <h3>4-year college degree</h3>
        <div class="compare-row"><span class="label">How many days will it take?</span><span class="val"><span data-count="1460">0</span>+</span></div>
        <div class="compare-row"><span class="label">How much will it cost me?</span><span class="val">$<span data-count="100">0</span>k+</span></div>
        <div class="compare-row"><span class="label">Earning while you train?</span><span class="val no">Rarely</span></div>
        <div class="compare-row"><span class="label">Flexibility</span><span class="val no">NO</span></div>
      </div>
      <div class="compare-col adjuster">
        <h3>Becoming an adjuster</h3>
        <div class="compare-row"><span class="label">How many days will it take?</span><span class="val"><span data-count="7">0</span></span></div>
        <div class="compare-row"><span class="label">How much will it cost me?</span><span class="val">Under $<span data-count="1">0</span>k</span></div>
        <div class="compare-row"><span class="label">Earning while you train?</span><span class="val yes">YES</span></div>
        <div class="compare-row"><span class="label">Flexibility</span><span class="val yes">YES</span></div>
      </div>
    </div>
    <p class="chart-note" style="text-align:center">Adjuster costs include a typical online pre-licensing course, exam and license fees. College figure reflects four years of tuition, fees and housing at a public university.</p>
  </div>
</section>

<section class="section section-dark" id="how-much">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">How it works</span>
      <h2>How much do insurance adjusters make &mdash; and how do they get paid?</h2>
      <p>From license to first paycheck, here is the path most new adjusters follow.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><h3>Get licensed</h3><p>Complete a pre-licensing course, pass the exam and apply for your license. Texas is a popular choice for reciprocity.</p></div>
      <div class="step reveal reveal-delay-1"><h3>Choose your path</h3><p>Apply for staff trainee programs with carriers, or join independent adjusting firm rosters for deployments.</p></div>
      <div class="step reveal reveal-delay-2"><h3>Work claims</h3><p>Inspect losses, write estimates in tools like Xactimate, and settle claims for property, auto or casualty.</p></div>
      <div class="step reveal reveal-delay-3"><h3>Get paid</h3><p>Staff adjusters draw a salary. Independents bill per claim or per day. Public adjusters take a share of the settlement.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split flip">
    <div class="reveal">
      <span class="eyebrow">What moves the number</span>
      <h2>6 factors that drive insurance adjuster salary</h2>
      <div class="grid-2" style="margin-top:24px">
        <div><h3>1. Employment type</h3><p>W-2 staff roles pay steadily; 1099 work pays per claim with far more variance.</p></div>
        <div><h3>2. Line of business</h3><p>Commercial, large loss and casualty pay more than auto material damage.</p></div>
        <div><h3>3. Experience</h3><p>Pay rises roughly 30&ndash;40% between trainee and senior adjuster.</p></div>
        <div><h3>4. Storm activity</h3><p>Hurricane and hail seasons decide most independent and CAT incomes.</p></div>
        <div><h3>5. Location</h3><p>High-wage states pay staff adjusters 10&ndash;15% above the national median.</p></div>
        <div><h3>6. Credentials</h3><p>AIC, CPCU, Xactimate certification and bilingual skills earn premiums.</p></div>
      </div>
    </div>
    <div class="photo-frame reveal reveal-delay-1">
      <img src="/assets/img/brick-home.webp" alt="Suburban brick home - property claims drive much of adjuster pay" width="1200" height="675" loading="lazy">
      <div class="photo-badge"><?= icon('home', 30) ?><div><strong>$62k&ndash;$90k</strong><span>Field property adjusters</span></div></div>
    </div>
  </div>
</section>

<section class="section section-soft" id="tools">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Free interactive tools</span>
      <h2>Calculate your insurance adjuster salary</h2>
      <p>Built for adjusters and career changers. No sign-up, no email &mdash; just answers.</p>
    </div>
    <div class="grid-4">
<?php foreach (tools() as $i => $t): ?>
      <a class="card tool-card spotlight tilt reveal reveal-delay-<?= $i ?>" href="<?= e($t['path']) ?>">
        <div class="icon-wrap"><?= icon($t['icon'], 26) ?></div>
        <h3><?= e($t['name']) ?></h3>
        <p><?= e($t['blurb']) ?></p>
        <span class="link-arrow">Open tool <?= icon('arrow', 16) ?></span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section" id="state">
  <div class="container split">
    <div class="photo-frame reveal">
      <img src="/assets/img/miami-skyline.webp" alt="Miami skyline at sunset - Florida is a major market for hurricane adjusters" width="1200" height="675" loading="lazy">
      <div class="photo-badge"><?= icon('map', 30) ?><div><strong>51</strong><span>States + D.C. covered</span></div></div>
    </div>
    <div class="reveal reveal-delay-1">
      <span class="eyebrow">Location matters</span>
      <h2>Insurance adjuster salary by state</h2>
      <p>Staff pay follows local wages, so an insurance adjuster salary in California or New York runs well above the national median while much of the South runs slightly below. Independent pay works differently: fee schedules are national, and the money follows the storms &mdash; which is why Texas, Florida, Louisiana and Oklahoma stay at the top of every CAT adjuster's list.</p>
      <div class="keyword-cloud" style="margin:22px 0">
        <a href="<?= BLOG_BASE ?>insurance-adjuster-salary-texas/">Texas</a>
        <a href="<?= BLOG_BASE ?>insurance-adjuster-salary-florida/">Florida</a>
        <a href="/salary-by-state/#CA">California</a>
        <a href="/salary-by-state/#NY">New York</a>
        <a href="/salary-by-state/#GA">Georgia</a>
        <a href="/salary-by-state/#LA">Louisiana</a>
        <a href="/salary-by-state/#OK">Oklahoma</a>
      </div>
      <a class="btn btn-dark" href="/salary-by-state/">Explore all 50 states <?= icon('arrow', 16) ?></a>
    </div>
  </div>
</section>

<?php if ($posts): ?>
<section class="section section-soft">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Insurance adjuster advice</span>
      <h2>Latest salary guides</h2>
      <p>Deep dives on pay, licensing and career moves for every kind of adjuster.</p>
    </div>
    <div class="post-grid">
<?php foreach ($posts as $p) echo post_card($p); ?>
    </div>
    <p style="text-align:center;margin-top:40px"><a class="btn btn-dark" href="<?= BLOG_BASE ?>">View all guides <?= icon('arrow', 16) ?></a></p>
  </div>
</section>
<?php endif; ?>

<section class="section" id="faq">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">FAQ</span>
      <h2>Insurance adjuster salary questions, answered</h2>
    </div>
    <div class="faq reveal">
<?php foreach ($faqs as $i => $f): ?>
      <details<?= $i === 0 ? ' open' : '' ?>><summary><?= e($f['q']) ?></summary><div class="faq-a"><p><?= e($f['a']) ?></p></div></details>
<?php endforeach; ?>
    </div>
    <p class="chart-note" style="text-align:center;margin-top:30px">*Six-figure first-year earnings are most realistic for independent adjusters during heavy catastrophe seasons. Sources: <a href="<?= BLS_URL ?>" target="_blank" rel="noopener">BLS Occupational Outlook Handbook</a>; role ranges are industry estimates.</p>
  </div>
</section>

<?= course_cta() ?>

<?php require __DIR__ . '/footer.php'; ?>
