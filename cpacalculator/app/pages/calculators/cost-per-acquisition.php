<?php
defined('CPA') or exit;
$P['title'] = "CPA Formula & Cost Per Acquisition Calculator (Marketing) | CPA Calculator";
$P['description'] = "The CPA formula explained: cost per acquisition = total cost ÷ conversions. Free CPA calculator with CPC, CTR, conversion rate, ROAS, ROI and target CPA.";
$P['scripts'] = ['/assets/js/tools/cost-per-acquisition.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Worked example (same formulas as the JS). */
$ex = ['spend' => 5000, 'conv' => 125, 'impr' => 250000, 'clicks' => 5000, 'rpc' => 90, 'clv' => 150, 'margin' => 0.40];
$ex['cpa'] = $ex['spend'] / $ex['conv'];
$ex['cpc'] = $ex['spend'] / $ex['clicks'];
$ex['ctr'] = $ex['clicks'] / $ex['impr'];
$ex['cvr'] = $ex['conv'] / $ex['clicks'];
$ex['cpm'] = $ex['spend'] / $ex['impr'] * 1000;
$ex['rev'] = $ex['conv'] * $ex['rpc'];
$ex['roas'] = $ex['rev'] / $ex['spend'];
$ex['roi'] = ($ex['rev'] - $ex['spend']) / $ex['spend'];
$ex['tcpa'] = $ex['clv'] * (1 - $ex['margin']);
$ex['maxcpc'] = $ex['tcpa'] * $ex['cvr'];
$pc = fn($x, $dp = 1) => number_format($x * 100, $dp) . '%';

echo tool_hero('cost-per-acquisition', "Cost Per Acquisition (CPA) Calculator &amp; CPA Formula",
  "Calculate your marketing cost per acquisition from ad spend and conversions — plus CPC, CTR, conversion rate, CPM, ROAS and ROI. Then work out a target CPA from customer lifetime value and the maximum cost per click you can afford.",
  ['CPA = cost ÷ conversions', 'CPC, CTR, CPM & conversion rate', 'ROAS & ROI', 'Target CPA & max CPC']);
?>
<section class="tool" aria-label="Cost per acquisition calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="cpa-form" novalidate>
        <div class="field"><span class="lbl">Mode</span><div class="seg" role="radiogroup" aria-label="Calculator mode">
          <label><input type="radio" name="mode" value="actual" checked><span>Calculate CPA from results</span></label>
          <label><input type="radio" name="mode" value="plan"><span>Forecast from budget, CPC &amp; conversion rate</span></label>
        </div></div>
        <fieldset class="fieldset" data-when="actual"><legend>Campaign results</legend>
          <div class="grid-2">
            <?= money_field('spend', 'Ad spend', $ex['spend'], 'Total media cost for the campaign or period (Google Ads, Meta, LinkedIn, etc.).') ?>
            <?= money_field('other', 'Other campaign costs (optional)', '', 'Agency or freelancer fees, creative production, tools. Added to ad spend for a fully loaded CPA.') ?>
          </div>
          <?= money_field('conv', 'Conversions (acquisitions)', $ex['conv'], 'The number of actions you’re paying for: sales, sign-ups, leads, installs or bookings.', '', '') ?>
          <div class="grid-2">
            <?= money_field('impr', 'Impressions (optional)', $ex['impr'], 'Times your ad was shown. Used for CTR and CPM.', '', '') ?>
            <?= money_field('clicks', 'Clicks (optional)', $ex['clicks'], 'Ad clicks. Used for CPC, CTR and conversion rate.', '', '') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset" data-when="plan"><legend>Forecast inputs</legend>
          <?= money_field('budget', 'Ad budget', 5000, 'What you plan to spend for the period.') ?>
          <div class="grid-3">
            <div class="field"><label for="f-cpc">Cost per click <span class="tip" tabindex="0" data-tip="Average CPC you expect to pay. Check your ad platform’s keyword planner or your past campaigns.">?</span></label><div class="inp pre" data-pre="$"><input id="f-cpc" name="cpc" inputmode="decimal" autocomplete="off" data-money value="1.00" placeholder="0"></div></div>
            <?= money_field('ctr', 'Click-through rate', 2, 'Clicks ÷ impressions. Used to estimate impressions and CPM.', '', '%') ?>
            <?= money_field('cvr', 'Conversion rate', 2.5, 'Conversions ÷ clicks, from your analytics or ad platform.', '', '%') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Value of a conversion</legend>
          <div class="grid-2">
            <?= money_field('rpc', 'Revenue per conversion', $ex['rpc'], 'Average order value or first-purchase revenue. Used for ROAS and ROI.') ?>
            <?= money_field('clv', 'Customer lifetime value (profit)', $ex['clv'], 'Gross profit you expect from a customer over the relationship: lifetime revenue × gross margin. Used for target CPA.') ?>
          </div>
          <?= money_field('margin', 'Desired profit margin on that value', 40, 'Share of the customer’s lifetime value you want to keep as profit after paying to acquire them.', '', '%') ?>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Cost per acquisition (CPA)</div>
          <div class="res-big" data-out="cpa">$0</div>
          <div class="res-sub" data-out="sub">—</div>
          <div class="quarters" data-funnel></div>
          <div class="kpis">
            <div class="kpi"><small>CPC</small><b data-out="cpc">—</b></div>
            <div class="kpi"><small>CTR</small><b data-out="ctr">—</b></div>
            <div class="kpi"><small>Conversion rate</small><b data-out="cvr">—</b></div>
            <div class="kpi"><small>CPM</small><b data-out="cpm">—</b></div>
            <div class="kpi"><small>ROAS</small><b data-out="roas">—</b></div>
            <div class="kpi"><small>ROI</small><b data-out="roi">—</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Revenue versus acquisition cost"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note"><span data-out="note">ROI here is on revenue; subtract product costs for profit-based ROI.</span> <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="cpa-formula">The CPA formula</h2>
      <p><strong>Cost per acquisition (CPA)</strong> is what you pay, on average, to win one conversion — a sale, a lead, a sign-up or whatever action your campaign is built around. The formula is simple:</p>
      <div class="formula">CPA = total cost ÷ number of conversions</div>
      <p>If you spend <?= money($ex['spend']) ?> on ads and get <?= $ex['conv'] ?> customers, your CPA is <?= money($ex['spend']) ?> ÷ <?= $ex['conv'] ?> = <strong><?= money($ex['cpa'], 2) ?></strong>. Because conversions come from clicks, and clicks come from impressions, you can write the same CPA calculation in terms of your other ad metrics:</p>
      <div class="formula">CPA = CPC ÷ conversion rate<br>CPA = CPM ÷ (1,000 × CTR × conversion rate)<br>Conversions = budget ÷ CPA</div>
      <p>Those versions are handy for forecasting: at a $1.00 cost per click and a 2.5% conversion rate, CPA = $1.00 ÷ 0.025 = $40.00 before you spend a dollar. Use the “Forecast” mode in the calculator to run that kind of what-if.</p>
      <p><strong>Decide what “total cost” includes.</strong> Most ad platforms report CPA using media spend only. A <em>fully loaded</em> CPA also adds agency fees, creative production and tools — enter those under “Other campaign costs” to see both.</p>

      <h2 id="how-to-use">How to use the CPA calculator</h2>
      <ol>
        <li><strong>Enter ad spend and conversions</strong> for a campaign, channel or month. That alone gives you CPA.</li>
        <li><strong>Add impressions and clicks</strong> (optional) to get CTR, CPC, CPM and conversion rate, plus a simple funnel.</li>
        <li><strong>Enter revenue per conversion</strong> to see return on ad spend (ROAS) and ROI.</li>
        <li><strong>Enter customer lifetime value and your desired margin</strong> to calculate a target CPA and the maximum CPC you can bid while staying on target.</li>
      </ol>

      <h2 id="example">CPA calculation example</h2>
      <p>An online store runs a search campaign for a month:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Metric</th><th>Formula</th><th class="n">Result</th></tr></thead><tbody>
        <tr><td>CPA</td><td><?= money($ex['spend']) ?> ÷ <?= $ex['conv'] ?> conversions</td><td class="n"><?= money($ex['cpa'], 2) ?></td></tr>
        <tr><td>CPC</td><td><?= money($ex['spend']) ?> ÷ <?= number_format($ex['clicks']) ?> clicks</td><td class="n"><?= money($ex['cpc'], 2) ?></td></tr>
        <tr><td>CTR</td><td><?= number_format($ex['clicks']) ?> ÷ <?= number_format($ex['impr']) ?> impressions</td><td class="n"><?= $pc($ex['ctr'], 2) ?></td></tr>
        <tr><td>Conversion rate</td><td><?= $ex['conv'] ?> ÷ <?= number_format($ex['clicks']) ?> clicks</td><td class="n"><?= $pc($ex['cvr'], 2) ?></td></tr>
        <tr><td>CPM</td><td><?= money($ex['spend']) ?> ÷ <?= number_format($ex['impr']) ?> × 1,000</td><td class="n"><?= money($ex['cpm'], 2) ?></td></tr>
        <tr><td>ROAS</td><td><?= money($ex['rev']) ?> revenue ÷ <?= money($ex['spend']) ?></td><td class="n"><?= number_format($ex['roas'], 2) ?>× (<?= $pc($ex['roas'], 0) ?>)</td></tr>
        <tr><td>ROI</td><td>(<?= money($ex['rev']) ?> − <?= money($ex['spend']) ?>) ÷ <?= money($ex['spend']) ?></td><td class="n"><?= $pc($ex['roi'], 0) ?></td></tr>
        <tr><td>Target CPA</td><td><?= money($ex['clv']) ?> CLV × (1 − <?= $pc($ex['margin'], 0) ?>)</td><td class="n"><?= money($ex['tcpa'], 2) ?></td></tr>
        <tr><td>Max CPC</td><td><?= money($ex['tcpa']) ?> target CPA × <?= $pc($ex['cvr'], 1) ?></td><td class="n"><?= money($ex['maxcpc'], 2) ?></td></tr>
      </tbody></table></div>
      <p>The actual CPA of <?= money($ex['cpa']) ?> is well under the <?= money($ex['tcpa']) ?> target, so this campaign has room to scale — bids could rise toward <?= money($ex['maxcpc'], 2) ?> per click before acquisitions stop being profitable at the desired margin. These are the calculator’s default inputs.</p>

      <h2 id="target-cpa">How to set a target CPA</h2>
      <p>A CPA is only “good” or “bad” relative to what a customer is worth to you. Work backward from value:</p>
      <div class="formula">Break-even CPA = customer lifetime value (gross profit)<br>Target CPA = lifetime value × (1 − desired profit margin)<br>Max CPC = target CPA × conversion rate</div>
      <ul>
        <li><strong>Use profit, not revenue.</strong> If a customer spends $500 over their lifetime at a 30% gross margin, they’re worth $150 of gross profit — that’s the most you can pay to acquire them and still break even.</li>
        <li><strong>One-time purchases:</strong> if customers rarely come back, use the gross profit on the first order. The <a href="/calculators/profit-margin/">profit margin calculator</a> gives you that figure.</li>
        <li><strong>Cash flow matters.</strong> A CPA justified by lifetime value may take months to pay back. Make sure the business can carry that gap — the <a href="/calculators/break-even/">break-even calculator</a> helps you see how many customers cover your fixed costs.</li>
      </ul>

      <h2 id="cpa-vs-cpc-cpm-cac">CPA vs CPC vs CPM vs CAC</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Metric</th><th>Formula</th><th>What it tells you</th></tr></thead><tbody>
        <tr><td><strong>CPA</strong> — cost per acquisition (or action)</td><td>Cost ÷ conversions</td><td>What a campaign pays per desired action. Often a campaign- or channel-level metric.</td></tr>
        <tr><td><strong>CPC</strong> — cost per click</td><td>Cost ÷ clicks</td><td>What you pay for traffic. A low CPC means nothing if those clicks don’t convert.</td></tr>
        <tr><td><strong>CPM</strong> — cost per mille</td><td>Cost ÷ impressions × 1,000</td><td>What you pay for 1,000 ad views. Common for awareness and social campaigns.</td></tr>
        <tr><td><strong>CPL</strong> — cost per lead</td><td>Cost ÷ leads</td><td>A CPA where the conversion is a lead, not a sale.</td></tr>
        <tr><td><strong>CAC</strong> — customer acquisition cost</td><td>All sales &amp; marketing costs ÷ new customers</td><td>A company-wide metric including salaries, tools and every channel — usually higher than any single campaign’s CPA.</td></tr>
        <tr><td><strong>ROAS</strong> — return on ad spend</td><td>Revenue ÷ ad spend</td><td>Revenue generated per dollar of ads. Useful when order values vary.</td></tr>
      </tbody></table></div>
      <p>In short: CPC and CPM measure what you pay for attention, CPA measures what you pay for results, and CAC measures what the whole business pays for each new customer.</p>

      <h2 id="good-cpa">What is a good CPA?</h2>
      <p>There’s no universal good CPA. Benchmarks vary widely by industry, channel, country, product price and what counts as a conversion — a newsletter sign-up and a $5,000 software contract can’t be compared. Published industry averages are a rough starting point at best. A more reliable test is your own economics:</p>
      <ul>
        <li>Your CPA should be <strong>below your target CPA</strong> (lifetime gross profit minus the profit you want to keep).</li>
        <li>Compare CPA <strong>across your own channels and campaigns</strong> and shift budget toward the ones that convert most cheaply at acceptable quality.</li>
        <li>Track CPA <strong>over time</strong> — rising CPA with flat conversion rates usually means competition for clicks is increasing.</li>
      </ul>

      <h2 id="lower-cpa">How to lower your cost per acquisition</h2>
      <ol>
        <li><strong>Raise conversion rate.</strong> Faster pages, clearer offers, fewer form fields and stronger social proof lower CPA without touching bids. Doubling conversion rate halves CPA.</li>
        <li><strong>Tighten targeting.</strong> Add negative keywords, exclude poor-performing placements and audiences, and narrow geography or schedule.</li>
        <li><strong>Improve ad relevance.</strong> More relevant ads tend to earn higher CTR, and on auction platforms better quality can lower what you pay per click.</li>
        <li><strong>Raise order value.</strong> Bundles and upsells don’t lower CPA, but they increase ROAS and the CPA you can afford.</li>
        <li><strong>Use the right bid strategy.</strong> Automated target-CPA bidding needs enough conversion data to work well; feed it accurate conversion tracking.</li>
      </ol>

      <h2 id="not-accountant">CPA formula vs Certified Public Accountant</h2>
      <p>“CPA” also stands for <strong>Certified Public Accountant</strong>. This page is about the marketing metric. If you landed here looking for tax help, our other tools are built for that: estimate your bill with the <a href="/calculators/federal-income-tax/">federal income tax calculator</a>, the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> or the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a>, and read our guide to <a href="/blog/quarterly-taxes-101-guide/">quarterly taxes</a>. Marketing costs are generally deductible business expenses, which lowers the after-tax cost of every acquisition.</p>

<?= faq_block([
  ['What is the CPA formula?', '<p>CPA = total cost ÷ number of conversions. For example, ' . money($ex['spend']) . ' of ad spend that produces ' . $ex['conv'] . ' sales gives a CPA of ' . money($ex['cpa'], 2) . '. Equivalently, CPA = cost per click ÷ conversion rate.</p>'],
  ['How do you calculate cost per acquisition in Google Ads or Meta?', '<p>Use the same formula: divide the campaign’s cost by its conversions for the same date range. Ad platforms usually show this as “cost per conversion” or “cost per result,” based on media spend only and on whatever conversions you’ve set up to track.</p>'],
  ['What is a good CPA?', '<p>It depends on your industry, channel and margins, so benchmarks vary widely. A practical rule is that CPA should be lower than the gross profit a customer brings in, minus the profit you want to keep — your target CPA.</p>'],
  ['How do I calculate target CPA?', '<p>Multiply customer lifetime value (in gross profit) by one minus your desired profit margin. With a ' . money($ex['clv']) . ' lifetime value and a ' . $pc($ex['margin'], 0) . ' desired margin, target CPA = ' . money($ex['clv']) . ' × 0.60 = ' . money($ex['tcpa']) . '.</p>'],
  ['What is the difference between CPA and CAC?', '<p>CPA usually measures a specific campaign or channel using ad spend. Customer acquisition cost (CAC) divides all sales and marketing costs — salaries, tools, agencies and every channel — by all new customers, so it’s typically higher.</p>'],
  ['How are CPA and ROAS related?', '<p>ROAS = revenue per conversion ÷ CPA. If each conversion brings ' . money($ex['rpc']) . ' of revenue and CPA is ' . money($ex['cpa']) . ', ROAS is ' . number_format($ex['roas'], 2) . '×.</p>'],
  ['Is this calculator about Certified Public Accountants?', '<p>No — here CPA means cost per acquisition, a marketing metric. For tax estimates, try our federal income tax, 1099 and self-employment tax calculators.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('cost-per-acquisition', ['profit-margin', 'break-even', '1099-tax-calculator', 'depreciation-calculator', 's-corp-tax-savings', 'federal-income-tax']) ?></div>
