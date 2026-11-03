<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "CPA Calculator — Free $Y Tax & Accounting Calculators";
$P['description'] = "CPA Calculator offers free $Y tax calculators built on IRS tables: federal income tax, 1099 and self-employment tax, quarterly estimates, paycheck, refund and business tools.";
$P['scripts'] = ['/assets/js/tools/home.js'];
$P['bodyClass'] = 'home';
$P['schema'][] = ['@type' => 'ItemList', 'name' => 'CPA Calculator tools', 'itemListElement' => array_map(fn($s, $i) => [
  '@type' => 'ListItem', 'position' => $i + 1, 'name' => TOOLS[$s][0], 'url' => SITE_ORIGIN . tool_url($s)], array_keys(TOOLS), array_keys(array_keys(TOOLS)))];
$single = $y['brackets']['single'];
?>
<section class="hero hero-home">
  <div class="floaters" aria-hidden="true">
    <span style="left:6%;top:18%;--s:64px;--k:-.25;--rot:-12deg">%</span>
    <span style="left:44%;top:12%;--s:38px;--k:.35">$</span>
    <span style="left:88%;top:70%;--s:72px;--k:-.15;--rot:10deg">÷</span>
    <span style="left:30%;top:82%;--s:46px;--k:.3">+</span>
    <span style="left:62%;top:88%;--s:34px;--k:-.4">1040</span>
    <span style="left:4%;top:68%;--s:30px;--k:.2">W-2</span>
    <span style="left:92%;top:16%;--s:40px;--k:.25;--rot:-8deg">=</span>
  </div>
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow"><span class="dot"></span>Updated for the <?= $Y ?> tax year · IRS Rev. Proc. 2025-32</span>
      <h1>CPA Calculator: free tax &amp; accounting calculators for <em><?= $Y ?></em></h1>
      <p class="lede">CPA Calculator turns the math a CPA does into plain-English tools anyone can use. Estimate your federal income tax, 1099 self-employment tax, quarterly payments, paycheck and refund in seconds — free, private and built on the current IRS tables.</p>
      <div class="hero-ctas">
        <a class="btn" href="/calculators/federal-income-tax/">Federal tax calculator <?= icon('arrow') ?></a>
        <a class="btn btn-outline" href="/calculators/1099-tax-calculator/">1099 tax calculator</a>
      </div>
      <ul class="hero-ticks">
        <li><?= icon('check') ?>No signup, no ads in your way</li>
        <li><?= icon('check') ?>Runs in your browser</li>
        <li><?= icon('check') ?><?= count(TOOLS) ?> free calculators</li>
      </ul>
    </div>
    <div class="reveal" style="--d:150ms">
      <form class="widget" id="home-calc" aria-label="Quick federal tax estimate">
        <div class="receipt-tape">2026 brackets <b>✓</b><br>std. deduction <b><?= money($y['std']['single']) ?></b></div>
        <div class="widget-h"><strong>What will I owe in federal tax?</strong><span class="live">Live</span></div>
        <div class="grid-2">
          <div class="field"><label for="h-income">Annual income</label><div class="inp pre" data-pre="$"><input id="h-income" name="income" inputmode="decimal" data-money value="75,000"></div></div>
          <div class="field"><label for="h-status">Filing as</label><select id="h-status" name="status"><option value="single">Single</option><option value="mfj">Married, jointly</option><option value="hoh">Head of household</option><option value="mfs">Married, separately</option></select></div>
        </div>
        <div class="field" style="margin-bottom:0"><label for="h-side">Side-hustle / 1099 income <span class="hint">(optional)</span></label><div class="inp pre" data-pre="$"><input id="h-side" name="side" inputmode="decimal" data-money placeholder="0"></div></div>
        <div class="result-big"><small>Estimated <?= $Y ?> federal tax</small><span class="num" data-out="tax">$0</span></div>
        <div class="mini-stats">
          <div><small>Effective</small><b data-out="eff">0%</b></div>
          <div><small>Bracket</small><b data-out="marg">0%</b></div>
          <div><small>Take-home</small><b data-out="take">$0</b></div>
        </div>
        <p class="hint" style="margin:12px 0 0">Full breakdown in the <a href="/calculators/federal-income-tax/">federal income tax calculator</a>.</p>
      </form>
    </div>
  </div>
</section>

<div class="wrap">
  <div class="stats">
    <div class="stat reveal"><b data-count="<?= count(TOOLS) ?>">0</b><span>free CPA Calculator tools</span></div>
    <div class="stat reveal" style="--d:80ms"><b data-count="<?= $Y ?>" data-plain>0</b><span>IRS brackets &amp; limits loaded</span></div>
    <div class="stat reveal" style="--d:160ms"><b data-count="<?= count(SALARY_PAGES) ?>">0</b><span>salary-by-salary tax breakdowns</span></div>
    <div class="stat reveal" style="--d:240ms"><b data-count="0" data-suf=" sign-ups">0</b><span>your numbers never leave your device</span></div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <div class="sec-head center reveal">
      <span class="kicker">Start here</span>
      <h2>What’s your tax situation?</h2>
      <p>Pick the one that sounds like you and CPA Calculator will point you to the right tools and guides.</p>
    </div>
    <div class="paths">
      <a class="path reveal" href="/calculators/paycheck-calculator/">
        <span class="tag">Most common</span>
        <h3>I have a regular job (W-2)</h3>
        <p class="muted">See your federal tax, check your paycheck withholding and find out if you’ll get a refund.</p>
        <ul><li><?= icon('check') ?>Federal income tax</li><li><?= icon('check') ?>Paycheck &amp; take-home pay</li><li><?= icon('check') ?>Tax refund estimator</li></ul>
      </a>
      <a class="path reveal" style="--d:100ms" href="/calculators/1099-tax-calculator/">
        <span class="tag">Trending</span>
        <h3>I freelance or have a 1099</h3>
        <p class="muted">Uber, Etsy, Upwork, consulting or locums — see what you owe, what you can write off and what to pay each quarter.</p>
        <ul><li><?= icon('check') ?>1099 &amp; self-employment tax</li><li><?= icon('check') ?>Quarterly estimated tax</li><li><?= icon('check') ?>Mileage &amp; home office</li></ul>
      </a>
      <a class="path reveal" style="--d:200ms" href="/calculators/s-corp-tax-savings/">
        <span class="tag">Business</span>
        <h3>I run a small business</h3>
        <p class="muted">Decide on an S corp, price for profit, find your break-even point and depreciate equipment.</p>
        <ul><li><?= icon('check') ?>S corp vs LLC savings</li><li><?= icon('check') ?>Profit margin &amp; break-even</li><li><?= icon('check') ?>Depreciation (MACRS)</li></ul>
      </a>
    </div>
  </div>
</section>

<section class="section section-alt" id="calculators">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">Every CPA Calculator tool</span>
      <h2>Free calculators for taxes, payroll and business math</h2>
      <p>Each CPA Calculator tool shows its work: the formula, the IRS figures it used and a line-by-line breakdown you can print or share with your accountant.</p>
    </div>
    <?= tool_cards(array_keys(TOOLS)) ?>
  </div>
</section>

<section class="section section-dark">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">How brackets really work</span>
      <h2>Your income climbs the <?= $Y ?> tax brackets one step at a time</h2>
      <p>The biggest tax myth is that a raise pushes <em>all</em> your income into a higher bracket. It doesn’t. Each step below is taxed only on the dollars that land on it — which is why your effective rate is always lower than your bracket. CPA Calculator draws this staircase for your exact income in the federal tax calculator.</p>
      <p>For a single filer in <?= $Y ?>, the first <?= money($single[0][0]) ?> of taxable income is taxed at 10%, income up to <?= money($single[1][0]) ?> at 12%, and so on up to 37% above <?= money($single[5][0]) ?>.</p>
      <a class="btn" href="/calculators/federal-income-tax/#brackets">See all <?= $Y ?> brackets <?= icon('arrow') ?></a>
    </div>
    <div class="stairs" aria-label="<?= $Y ?> federal tax rates for single filers">
<?php $h = [18, 28, 42, 54, 68, 82, 100]; $prev = 0; foreach ($single as $i => [$top, $rate]): ?>
      <div class="stair"><b><?= round($rate * 100) ?>%</b><i style="--h:<?= $h[$i] ?>%;--d:<?= $i * 120 ?>ms"></i><small><?= $top ? 'to ' . money($top / 1000) . 'k' : 'over ' . money($prev / 1000) . 'k' ?></small></div>
<?php $prev = $top ?? $prev; endforeach; ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker"><?= $Y ?> tax calendar</span>
      <h2>Quarterly estimated tax deadlines</h2>
      <p>Self-employed, investing or earning on the side? The IRS expects tax four times a year. Use the CPA Calculator <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> to work out each payment.</p>
    </div>
    <div class="timeline">
<?php foreach ($y['quarterlyDue'] as $i => $dte): ?>
      <div class="tl-item reveal" style="--d:<?= $i * 150 ?>ms"><b><?= e(preg_replace('/,.*$/', '', $dte)) ?></b><span>Q<?= $i + 1 ?> payment · <?= ['Jan – Mar income', 'Apr – May income', 'Jun – Aug income', 'Sep – Dec income'][$i] ?></span></div>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">Why people trust CPA Calculator</span>
      <h2>CPA-level accuracy, explained like a friend would</h2>
      <p>Most free tax calculators either oversimplify or bury you in jargon. CPA Calculator sits in between: the same order of operations a tax professional uses on Form 1040 and Schedule SE, with every assumption written out.</p>
      <ul class="checks">
        <li><?= icon('check') ?><span><strong>Current IRS data.</strong> <?= $Y ?> and <?= $Y - 1 ?> brackets, standard deductions, Social Security wage base (<?= money($y['ssWageBase']) ?>), mileage rate and contribution limits.</span></li>
        <li><?= icon('check') ?><span><strong>New <?= $Y ?> rules included.</strong> Deductions for tips, overtime and seniors, the <?= money($y['ctc']['amount']) ?> Child Tax Credit and the <?= money($y['saltCap']) ?> SALT cap.</span></li>
        <li><?= icon('check') ?><span><strong>Shows its work.</strong> Every result breaks down AGI, deductions, taxable income and tax by bracket.</span></li>
        <li><?= icon('check') ?><span><strong>Private by design.</strong> Calculations run in your browser; CPA Calculator never stores what you type.</span></li>
      </ul>
      <a href="/our-methodology/">Read how we build and test every calculator →</a>
    </div>
    <div class="reveal" style="--d:120ms">
      <div class="tool-box" style="grid-template-columns:1fr">
        <div class="tool-out" style="border:0">
          <div class="res-label">Example · single filer · $90,000 salary</div>
<?php $ex = salary_breakdown(90000, 'single'); ?>
          <div class="res-big"><?= money($ex['tax']) ?></div>
          <div class="res-sub">federal income tax · <?= number_format($ex['effective'] * 100, 1) ?>% effective · 22% bracket</div>
          <ul class="rows">
            <li><span>Gross wages</span><b><?= money(90000) ?></b></li>
            <li><span>Standard deduction</span><b>−<?= money($ex['std']) ?></b></li>
            <li><span>Taxable income</span><b><?= money($ex['taxable']) ?></b></li>
            <li><span>Social Security + Medicare</span><b><?= money($ex['fica']) ?></b></li>
            <li class="total"><span>Take-home before state tax</span><b><?= money($ex['net']) ?></b></li>
          </ul>
          <a class="btn btn-dark btn-sm" href="/calculators/federal-income-tax/90000/">See the $90k breakdown</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">Federal tax by salary</span>
      <h2>How much federal tax on your salary?</h2>
      <p>Pre-calculated <?= $Y ?> breakdowns for every filing status — federal income tax, FICA, effective rate and take-home pay.</p>
    </div>
    <ul class="pill-links reveal">
<?php foreach (SALARY_PAGES as $amt): ?>
      <li><a href="/calculators/federal-income-tax/<?= $amt ?>/">Tax on <?= money($amt) ?></a></li>
<?php endforeach; ?>
    </ul>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">Two kinds of CPA</span>
      <h2>Looking for the CPA formula used in marketing?</h2>
      <p>In advertising, CPA means <strong>cost per acquisition</strong>: total campaign cost divided by the number of conversions. If that’s the CPA calculation you came for, the CPA Calculator <a href="/calculators/cost-per-acquisition/">cost per acquisition calculator</a> works out CPA, target CPA, ROAS and the maximum CPC you can afford.</p>
      <div class="formula">CPA = Total ad spend ÷ Conversions</div>
      <p>Everywhere else on CPA Calculator, “CPA” refers to the work of a Certified Public Accountant — taxes, payroll, deductions and business finance.</p>
    </div>
    <div class="reveal" style="--d:120ms"><?= tool_cards(['cost-per-acquisition', 'profit-margin', 'break-even'], 'mini') ?></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="kicker">Plain-English guides</span>
      <h2>Tax guides from the CPA Calculator team</h2>
      <p>Step-by-step explanations that pair with each calculator.</p>
    </div>
    <?= post_cards(array_slice(array_keys(POSTS), 0, 6)) ?>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap" style="max-width:900px">
    <?= faq_block([
      ['What is CPA Calculator?', '<p>CPA Calculator (cpacalculator.com) is a free collection of tax and accounting calculators for employees, freelancers and small-business owners. Each tool applies the current IRS tables the way a Certified Public Accountant would and explains the result in plain English.</p>'],
      ['Is CPA Calculator really free?', '<p>Yes. Every CPA Calculator tool is free with no account, no email and no paywall. You can share or print any result.</p>'],
      ['How accurate is CPA Calculator?', "<p>The calculators use the official $Y IRS brackets, standard deductions, Social Security wage base, mileage rate and contribution limits, and follow the same order of operations as Form 1040 and Schedule SE. For common W-2 and 1099 situations results typically land within a few dollars of tax software. AMT, state taxes and some phase-outs are simplified, so complex returns should be reviewed by a CPA.</p>"],
      ['Is CPA Calculator a substitute for a real CPA?', '<p>No. CPA Calculator is an educational planning tool, not tax advice. It is a great first step — to understand your numbers, set aside the right amount or prepare questions — but a licensed CPA or enrolled agent should review your actual return, especially if you own a business, sold property or received an IRS notice.</p>'],
      ['Does CPA Calculator store my financial information?', '<p>No. The math runs in your web browser. Nothing you type into a CPA Calculator tool is sent to or stored on our servers.</p>'],
      ['Which CPA Calculator tool should I start with?', '<p>Employees should start with the <a href="/calculators/federal-income-tax/">federal income tax calculator</a> or the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>. Freelancers and contractors should start with the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>, then plan payments with the <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a>.</p>'],
    ], 'CPA Calculator FAQ') ?>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta-band reveal">
      <span class="kicker">Ready when you are</span>
      <h2>Know your number before the IRS tells you.</h2>
      <p>Run a free estimate with CPA Calculator in under a minute — then decide what to set aside, adjust your withholding or bring a clear set of numbers to your accountant.</p>
      <div class="hero-ctas" style="margin-bottom:0">
        <a class="btn" href="/calculators/federal-income-tax/">Estimate my federal tax <?= icon('arrow') ?></a>
        <a class="btn btn-outline" href="/calculators/">Browse all calculators</a>
      </div>
    </div>
  </div>
</section>
