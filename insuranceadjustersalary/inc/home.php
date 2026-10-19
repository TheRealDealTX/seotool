<?php
require_once __DIR__ . '/data.php';

$metros = texas_metros();
$tx = array_values(array_filter(states(), fn($s) => $s['code'] === 'TX'))[0];
$seasons = texas_seasons();

$faqs = [
    ['q' => 'What is the average insurance adjuster salary in Texas?',
     'a' => 'Texas staff adjusters earn about $76,800 a year at the median by our estimate, right in line with the BLS national median of $76,790 (May 2024). Austin, Dallas-Fort Worth and Houston pay roughly $80,000 to $81,000, while El Paso and the Rio Grande Valley pay less.'],
    ['q' => 'How much do insurance adjusters make in Texas in their first year?',
     'a' => 'Trainee and entry-level staff adjusters in Texas usually start between $45,000 and $60,000 plus benefits. Independent adjusters who work Texas hail and Gulf Coast hurricane deployments can out-earn that in a strong storm season, but first-year IA income is unpredictable.'],
    ['q' => 'Why do adjusters in other states get a Texas license?',
     'a' => 'Texas offers reciprocity with every state that licenses adjusters through reciprocity, and residents of states without their own adjuster license can designate Texas as their home state. One Texas all-lines license opens doors nationwide, which is why it is the most popular adjuster license in the country.'],
    ['q' => 'Which type of adjuster earns the highest salary?',
     'a' => 'Experienced catastrophe (CAT) and large-loss commercial adjusters have the highest earning ceilings, with busy-year incomes of $150,000 to $250,000 or more. In Texas, spring hail in Dallas-Fort Worth and hurricane season on the Gulf Coast drive most of that CAT income.'],
    ['q' => 'How do public adjusters get paid in Texas?',
     'a' => 'Public adjusters earn a percentage of the policyholder\'s settlement. Texas caps public adjuster fees at 10% of the settlement, lower than many states, and requires a separate Texas public adjuster license.'],
    ['q' => 'How long does it take to get a Texas adjuster license?',
     'a' => 'Many people complete an online Texas all-lines pre-licensing course and apply for their license within one to two weeks. Use code joe20 for 20% off the AdjustingOnline course.'],
];

$posts = all_posts();
$txPost = $posts['insurance-adjuster-salary-texas'] ?? null;
$posts = array_slice($posts, 0, 6);

$chart = chart_data();
$chart = ['texas' => [
    'label' => 'Texas metros',
    'note'  => 'Estimated staff adjuster salary range by Texas metro (mid-career). Our estimates, anchored to the BLS national median.',
    'rows'  => array_map(fn($m) => [$m['name'], (int) round($m['median'] * .8, -2), (int) round($m['median'] * 1.2, -2)], array_slice($metros, 0, 6)),
]] + $chart;

$page = [
    'title'       => 'Insurance Adjuster Salary in Texas (2026) & Nationwide Pay',
    'description' => 'Insurance adjuster salary data for Texas and every state: staff, independent, CAT and public adjuster pay, Texas metro salaries, free calculators and fast licensing.',
    'path'        => '/',
    'body_class'  => 'has-hero',
    'preload'     => 'hero-roof-inspection.webp',
    'scripts'     => ['salary-model.js', 'home.js'],
    'schema'      => [faq_schema($faqs)],
];
require __DIR__ . '/header.php';
?>

<section class="hero">
  <div class="hero-media"><img src="/assets/img/hero-roof-inspection.webp" alt="Texas insurance adjuster inspecting a brick home's roof for hail damage" width="1600" height="1067" fetchpriority="high"></div>
  <div class="hero-orb o1" aria-hidden="true"></div>
  <div class="hero-orb o2" aria-hidden="true"></div>
  <div class="container hero-inner">
    <div>
      <span class="eyebrow anim">Texas-focused 2026 pay guide</span>
      <h1 class="anim d1">Insurance Adjuster Salary in Texas: What <span class="grad">Adjusters Really Earn</span></h1>
      <p class="hero-lead anim d2">Real insurance adjuster salary numbers for <span class="typed" data-words="Houston|Dallas-Fort Worth|Austin|San Antonio|Corpus Christi|every Texas metro">Houston</span> &mdash; plus every other state, free calculators and the fastest path to a Texas adjuster license.</p>
      <div class="hero-actions anim d3">
        <a class="btn btn-gold btn-lg pulse" href="/salary-calculator/"><?= icon('calc', 20) ?> Calculate Your Texas Salary</a>
        <?= cert_btn('btn btn-ghost btn-lg') ?>
      </div>
      <div class="hero-badges anim d4">
        <span><?= icon('check', 18) ?> Texas metro pay data</span>
        <span><?= icon('check', 18) ?> 4 free calculators</span>
        <span><?= icon('check', 18) ?> Texas license in about a week</span>
      </div>
    </div>
    <aside class="glass hero-card anim d3" aria-label="Texas insurance adjuster salary snapshot">
      <h2>Texas adjuster pay snapshot</h2>
      <p class="sub">Estimated median staff adjuster salary by metro</p>
      <div class="big-number"><span data-count="<?= $tx['median'] ?>" data-prefix="$">$0</span><small> Texas median</small></div>
      <div class="mini-bars">
<?php foreach (array_slice($metros, 0, 5) as $m): ?>
        <div class="mini-bar"><span><?= e(str_replace('Dallas-Fort Worth', 'Dallas-FW', $m['name'])) ?></span><span class="track"><span class="fill" data-width="<?= round(($m['median'] - 50000) / 35000 * 100) ?>%"></span></span><b>$<?= round($m['median'] / 1000, 1) ?>k</b></div>
<?php endforeach; ?>
      </div>
      <p class="src">U.S. median $<?= number_format(BLS_MEDIAN_ANNUAL) ?> (BLS, May 2024). Texas and metro figures are our estimates.</p>
    </aside>
  </div>
  <a class="scroll-cue" href="#overview" aria-label="Scroll to content"></a>
</section>

<div class="container stats-wrap">
  <div class="stats reveal">
    <div class="stat"><strong data-count="<?= $tx['median'] ?>" data-prefix="$">$0</strong><span>Texas median (est.)</span></div>
    <div class="stat"><strong data-count="<?= $metros[0]['median'] / 1000 ?>" data-prefix="$" data-decimals="1" data-suffix="k">$0</strong><span>Top metro: Austin (est.)</span></div>
    <div class="stat"><strong data-count="10" data-suffix="%">0</strong><span>Texas public adjuster fee cap</span></div>
    <div class="stat"><strong data-count="7" data-suffix=" days">0</strong><span>To get licensed online</span></div>
  </div>
</div>

<section class="section" id="overview">
  <div class="container split">
    <div class="reveal">
      <span class="eyebrow">The quick answer</span>
      <h2>What is the average insurance adjuster salary in Texas?</h2>
      <p>The typical insurance adjuster salary in Texas is about <strong>$76,800 a year</strong> for a staff adjuster, right on top of the national median of $76,790 (about $36.92 an hour) reported by the Bureau of Labor Statistics. Austin, Dallas-Fort Worth and Houston pay closer to $80,000; El Paso and the Rio Grande Valley pay less.</p>
      <p>Where you land depends on how you work. A staff adjuster on salary trades upside for stability and benefits. An independent or catastrophe adjuster is paid per claim and can double the median in a big Texas hail or hurricane year &mdash; or fall short of it in a quiet one. Public adjusters earn a share of each settlement, capped at 10% in Texas.</p>
      <div class="callout"><strong>Bottom line:</strong> an insurance adjuster salary in Texas usually starts in the $45,000&ndash;$60,000 range, climbs to $70,000&ndash;$90,000 within a few years, and can pass six figures for senior, large-loss and CAT adjusters.</div>
      <a class="link-arrow" href="<?= BLOG_BASE ?>insurance-adjuster-salary-texas/">Full Texas insurance adjuster salary guide <?= icon('arrow', 16) ?></a>
    </div>
    <div class="photo-frame reveal reveal-delay-2">
      <img src="/assets/img/brick-home.webp" alt="Brick home in a Texas suburb - residential property claims drive adjuster pay" width="1200" height="675" loading="lazy">
      <div class="photo-badge"><?= icon('trend', 30) ?><div><strong>6 figures</strong><span>Possible in a big storm year*</span></div></div>
    </div>
  </div>
</section>

<section class="section section-dark" id="texas">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Texas metros</span>
      <h2>Insurance adjuster salary by Texas city</h2>
      <p>Estimated median staff adjuster pay in Texas' biggest claim markets. Independent adjusters follow the storms instead, so their income depends more on the season than the city.</p>
    </div>
    <div class="bar-chart reveal">
<?php $maxM = $metros[0]['median']; foreach ($metros as $m): ?>
      <div class="bar-row"><span class="name"><?= e($m['name']) ?></span><span class="track"><span class="fill" style="width:0" data-width="<?= round($m['median'] / $maxM * 100, 1) ?>%"></span></span><span class="amt">$<?= number_format($m['median']) ?></span></div>
<?php endforeach; ?>
    </div>
    <p class="chart-note">Our estimates: a metro wage index applied to the BLS national median for claims adjusters ($<?= number_format(BLS_MEDIAN_ANNUAL) ?>, May 2024). <a href="/salary-by-state/#TX" style="color:var(--gold-light)">Compare Texas with other states &rarr;</a></p>
  </div>
</section>

<section class="section section-alt" id="why">
  <div class="container">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow">Why Texas</span>
        <h2>Why become an insurance adjuster in Texas?</h2>
        <p>Texas is the best place to start an adjusting career &mdash; and the best license to hold even if you live somewhere else. Constant storm activity, huge carrier hubs in Dallas, Houston, Austin and San Antonio, and nationwide reciprocity keep the Texas insurance adjuster salary market busy year after year.</p>
        <div class="cert-inline"><?= cert_btn('btn btn-dark', 'Get Your Texas License') ?></div>
      </div>
      <div class="photo-frame reveal reveal-delay-1">
        <img src="/assets/img/austin-skyline.webp" alt="Austin, Texas skyline at dusk" width="1200" height="675" loading="lazy">
        <div class="photo-badge"><?= icon('star', 30) ?><div><strong>#1</strong><span>Home-state license choice</span></div></div>
      </div>
    </div>
    <div class="grid-4" style="margin-top:56px">
      <div class="card spotlight reveal"><div class="icon-wrap"><?= icon('star', 24) ?></div><h3>Recognized nationwide</h3><p>Texas has reciprocity with every state that allows licensing through reciprocity, so one license opens doors across the country.</p></div>
      <div class="card spotlight reveal reveal-delay-1"><div class="icon-wrap"><?= icon('book', 24) ?></div><h3>Simple licensing</h3><p>If your home state has no adjuster license of its own, you can designate Texas as your home state for licensing purposes.</p></div>
      <div class="card spotlight reveal reveal-delay-2"><div class="icon-wrap"><?= icon('map', 24) ?></div><h3>Texas is huge</h3><p>Hail, tornadoes, freezes and Gulf hurricanes create steady claim volume. Independent adjusters working Texas storms need a Texas license.</p></div>
      <div class="card spotlight reveal reveal-delay-3"><div class="icon-wrap"><?= icon('bolt', 24) ?></div><h3>Fast to start</h3><p>An online course can have you licensed in about a week, without years of school or student debt.</p></div>
    </div>
  </div>
</section>

<section class="section" id="seasons">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Interactive planner</span>
      <h2>Texas claim seasons: when the money comes</h2>
      <p>Pick a month to see which Texas perils keep adjusters busy. Independent and CAT adjuster income rises and falls with this calendar.</p>
    </div>
    <div class="season reveal" data-seasons='<?= e(json_encode($seasons)) ?>'>
      <div class="season-months" role="tablist" aria-label="Month">
<?php foreach (['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] as $i => $mo): ?>
        <button type="button" class="season-month" data-m="<?= $i ?>" aria-selected="false"><?= $mo ?><span class="heat"></span></button>
<?php endforeach; ?>
      </div>
      <div class="season-body">
        <div class="season-rows"></div>
        <div class="season-summary"><h3 class="season-title"></h3><p class="season-text"></p><a class="link-arrow" href="/cat-deployment-calculator/">Estimate a Texas deployment <?= icon('arrow', 16) ?></a></div>
      </div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
<?php $roles = ['Houston', 'Staff Adjuster', 'Dallas-Fort Worth', 'Independent Adjuster', 'Austin', 'CAT Adjuster', 'San Antonio', 'Public Adjuster', 'Corpus Christi', 'Field Adjuster', 'Lubbock', 'Desk Adjuster'];
for ($i = 0; $i < 2; $i++) foreach ($roles as $r) echo '    <span>' . e($r) . "</span>\n"; ?>
  </div>
</div>

<section class="section section-soft" id="salary-guide">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Salary by adjuster type</span>
      <h2>Insurance adjuster salary by role</h2>
      <p>The four career paths pay in completely different ways. Here is what each one typically earns in Texas and nationwide.</p>
    </div>
    <div class="grid-4">
      <article class="card pay-card spotlight tilt reveal">
        <div class="icon-wrap"><?= icon('brief', 26) ?></div>
        <h3>Staff adjuster</h3>
        <div class="range">$52k&ndash;$92k</div>
        <div class="range-note">W-2 salary with a carrier &middot; big hubs in DFW &amp; Houston</div>
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
          <li><?= icon('check', 16) ?> Texas license = national roster</li>
        </ul>
      </article>
      <article class="card pay-card spotlight tilt reveal reveal-delay-2">
        <div class="icon-wrap"><?= icon('storm', 26) ?></div>
        <h3>CAT adjuster</h3>
        <div class="range">$50k&ndash;$200k+</div>
        <div class="range-note">Texas hail, Gulf hurricanes &amp; freezes</div>
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
        <div class="range-note">Fee capped at 10% in Texas</div>
        <ul class="ticks">
          <li><?= icon('check', 16) ?> Works for the policyholder</li>
          <li><?= icon('check', 16) ?> Separate Texas PA license</li>
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
      <p>Switch views to see how pay changes by Texas metro, adjuster type, line of business and years of experience.</p>
    </div>
    <div class="reveal" data-chart='<?= e(json_encode($chart)) ?>'>
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
      <h2>Quick Texas insurance adjuster salary estimator</h2>
      <p>Pick your Texas metro and role. For credentials and every other state, open the full calculator.</p>
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
        <div class="two-col">
          <div class="field">
            <label for="q-metro">Texas metro</label>
            <select id="q-metro" name="metro">
              <option value="1">Texas (statewide)</option>
<?php foreach ($metros as $m): ?>
              <option value="<?= $m['index'] ?>"><?= e($m['name']) ?></option>
<?php endforeach; ?>
            </select>
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

<section class="section section-soft" id="comparison">
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
        <h3>Becoming a Texas adjuster</h3>
        <div class="compare-row"><span class="label">How many days will it take?</span><span class="val"><span data-count="7">0</span></span></div>
        <div class="compare-row"><span class="label">How much will it cost me?</span><span class="val">Under $<span data-count="1">0</span>k</span></div>
        <div class="compare-row"><span class="label">Earning while you train?</span><span class="val yes">YES</span></div>
        <div class="compare-row"><span class="label">Flexibility</span><span class="val yes">YES</span></div>
      </div>
    </div>
    <p class="chart-note" style="text-align:center">Adjuster costs include a typical online pre-licensing course and license fees. College figure reflects four years of tuition, fees and housing at a public university.</p>
    <p style="text-align:center;margin-top:26px"><?= cert_btn('btn btn-gold btn-lg') ?></p>
  </div>
</section>

<section class="section section-dark" id="how-much">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">How it works</span>
      <h2>How much do insurance adjusters make &mdash; and how do they get paid?</h2>
      <p>From Texas license to first paycheck, here is the path most new adjusters follow.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><h3>Get your Texas license</h3><p>Complete a Texas all-lines pre-licensing course and apply through the Texas Department of Insurance. Use joe20 for 20% off the course.</p></div>
      <div class="step reveal reveal-delay-1"><h3>Choose your path</h3><p>Apply for staff trainee programs at carriers in DFW, Houston or Austin, or join independent adjusting firm rosters.</p></div>
      <div class="step reveal reveal-delay-2"><h3>Work claims</h3><p>Inspect hail, wind and water losses, write estimates in tools like Xactimate, and settle property, auto or casualty claims.</p></div>
      <div class="step reveal reveal-delay-3"><h3>Get paid</h3><p>Staff adjusters draw a salary. Independents bill per claim or per day. Public adjusters take up to 10% of the settlement in Texas.</p></div>
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
        <div><h3>4. Texas storm activity</h3><p>Spring hail and Gulf hurricane seasons decide most independent and CAT incomes.</p></div>
        <div><h3>5. Location</h3><p>Austin, DFW and Houston pay staff adjusters about 4&ndash;6% above the national median.</p></div>
        <div><h3>6. Credentials</h3><p>AIC, CPCU, Xactimate certification and Spanish fluency earn premiums in Texas.</p></div>
      </div>
    </div>
    <div class="photo-frame reveal reveal-delay-1">
      <img src="/assets/img/tornado-storm.webp" alt="Tornado over open Texas farmland - storms drive catastrophe adjuster pay" width="1600" height="900" loading="lazy">
      <div class="photo-badge"><?= icon('storm', 30) ?><div><strong>$15k&ndash;$60k+</strong><span>Per CAT deployment</span></div></div>
    </div>
  </div>
</section>

<section class="section section-soft" id="tools">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Free interactive tools</span>
      <h2>Calculate your insurance adjuster salary</h2>
      <p>Built for Texas adjusters and career changers everywhere. No sign-up, no email &mdash; just answers.</p>
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
      <img src="/assets/img/miami-skyline.webp" alt="Miami skyline at sunset - Florida is the second big hurricane market after Texas" width="1200" height="675" loading="lazy">
      <div class="photo-badge"><?= icon('map', 30) ?><div><strong>51</strong><span>States + D.C. covered</span></div></div>
    </div>
    <div class="reveal reveal-delay-1">
      <span class="eyebrow">Beyond Texas</span>
      <h2>Insurance adjuster salary by state</h2>
      <p>Most adjusters start with a Texas license, then add more as they chase storms. Staff pay follows local wages, so an insurance adjuster salary in California or New York runs above the national median while much of the South runs slightly below. Independent pay follows claim volume &mdash; which keeps Texas, Florida, Louisiana and Oklahoma at the top of every CAT adjuster's list.</p>
      <div class="keyword-cloud" style="margin:22px 0">
        <a href="<?= BLOG_BASE ?>insurance-adjuster-salary-texas/">Texas</a>
        <a href="<?= BLOG_BASE ?>insurance-adjuster-salary-florida/">Florida</a>
        <a href="/salary-by-state/#LA">Louisiana</a>
        <a href="/salary-by-state/#OK">Oklahoma</a>
        <a href="/salary-by-state/#CA">California</a>
        <a href="/salary-by-state/#GA">Georgia</a>
        <a href="/salary-by-state/#NY">New York</a>
      </div>
      <a class="btn btn-dark" href="/salary-by-state/">Compare all 50 states <?= icon('arrow', 16) ?></a>
    </div>
  </div>
</section>

<?php if ($posts): ?>
<section class="section section-soft">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Insurance adjuster advice</span>
      <h2>Latest salary guides</h2>
      <p>Deep dives on pay, Texas licensing and career moves for every kind of adjuster.</p>
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
      <h2>Texas insurance adjuster salary questions, answered</h2>
    </div>
    <div class="faq reveal">
<?php foreach ($faqs as $i => $f): ?>
      <details<?= $i === 0 ? ' open' : '' ?>><summary><?= e($f['q']) ?></summary><div class="faq-a"><p><?= e($f['a']) ?></p></div></details>
<?php endforeach; ?>
    </div>
    <p class="chart-note" style="text-align:center;margin-top:30px">*Six-figure earnings are most realistic for independent adjusters during heavy catastrophe seasons. Sources: <a href="<?= BLS_URL ?>" target="_blank" rel="noopener">BLS Occupational Outlook Handbook</a>; Texas, metro and role figures are our estimates.</p>
  </div>
</section>

<?= course_cta() ?>

<?php require __DIR__ . '/footer.php'; ?>
