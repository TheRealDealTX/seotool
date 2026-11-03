<?php
defined('CPA') or exit;
/* /calculators/federal-income-tax/{amount}/ — programmatic salary pages (router sets $AMOUNT). */
$Y = TAX_YEAR;
$A = $AMOUNT;
$am = money($A);
$S = [];
foreach (['single', 'mfj', 'hoh', 'mfs'] as $s) $S[$s] = salary_breakdown($A, $s);
$b = $S['single'];
$P['title'] = "Federal Income Tax on $am in $Y | CPA Calculator";
$P['description'] = "How much federal tax on $am in $Y? A single filer pays " . money($b['tax']) . " (" . number_format($b['effective'] * 100, 1) . "% effective, " . round($b['marginal'] * 100) . "% bracket). See married, head of household, FICA and take-home pay.";
$P['modified'] = date('Y-m-d', filemtime(__FILE__));
$idx = array_search($A, SALARY_PAGES, true);
$prevA = SALARY_PAGES[$idx - 1] ?? null;
$nextA = SALARY_PAGES[$idx + 1] ?? null;
$y = $TAX['years'][(string) $Y];
?>
<section class="page-hero"><div class="wrap">
  <?= breadcrumbs([['Calculators', '/calculators/'], ['Federal Income Tax Calculator', '/calculators/federal-income-tax/'], ["Tax on $am", $P['path']]]) ?>
  <h1>Federal income tax on <?= $am ?> (<?= $Y ?>)</h1>
  <p class="lede">If you earn <?= $am ?> a year in <?= $Y ?> and file single, your federal income tax is about <strong style="color:#fff"><?= money($b['tax']) ?></strong> — an effective rate of <?= number_format($b['effective'] * 100, 1) ?>% in the <?= round($b['marginal'] * 100) ?>% bracket. After Social Security and Medicare, take-home pay is about <?= money($b['net']) ?> a year, or <?= money($b['net'] / 12) ?> a month, before state tax.</p>
  <div class="badges"><span class="badge"><?= icon('check') ?><?= $Y ?> IRS brackets</span><span class="badge"><?= icon('check') ?>Standard deduction applied</span><span class="badge"><?= icon('check') ?>All 4 filing statuses</span></div>
</div></section>

<section class="tool"><div class="wrap">
  <div class="tool-box" style="grid-template-columns:1fr">
    <div class="tool-form">
      <div class="table-wrap" style="margin:0"><table>
        <caption class="sr-only">Federal tax on <?= $am ?> by filing status</caption>
        <thead><tr><th><?= $am ?> salary, <?= $Y ?></th><th class="n">Single</th><th class="n">Married jointly</th><th class="n">Head of household</th><th class="n">Married separately</th></tr></thead>
        <tbody>
          <tr><td>Standard deduction</td><?php foreach ($S as $r) echo '<td class="n">' . money($r['std']) . '</td>'; ?></tr>
          <tr><td>Taxable income</td><?php foreach ($S as $r) echo '<td class="n">' . money($r['taxable']) . '</td>'; ?></tr>
          <tr><td><strong>Federal income tax</strong></td><?php foreach ($S as $r) echo '<td class="n"><strong>' . money($r['tax']) . '</strong></td>'; ?></tr>
          <tr><td>Effective tax rate</td><?php foreach ($S as $r) echo '<td class="n">' . number_format($r['effective'] * 100, 1) . '%</td>'; ?></tr>
          <tr><td>Marginal bracket</td><?php foreach ($S as $r) echo '<td class="n">' . round($r['marginal'] * 100) . '%</td>'; ?></tr>
          <tr><td>Social Security (6.2%)</td><?php foreach ($S as $r) echo '<td class="n">' . money($r['ss']) . '</td>'; ?></tr>
          <tr><td>Medicare (1.45%<?= $A > 200000 ? ' + 0.9%' : '' ?>)</td><?php foreach ($S as $r) echo '<td class="n">' . money($r['medicare']) . '</td>'; ?></tr>
          <tr><td><strong>Take-home pay (yearly)</strong></td><?php foreach ($S as $r) echo '<td class="n"><strong>' . money($r['net']) . '</strong></td>'; ?></tr>
          <tr><td>Take-home per month</td><?php foreach ($S as $r) echo '<td class="n">' . money($r['net'] / 12) . '</td>'; ?></tr>
          <tr><td>Take-home every two weeks</td><?php foreach ($S as $r) echo '<td class="n">' . money($r['net'] / 26) . '</td>'; ?></tr>
        </tbody>
      </table></div>
      <p class="hint" style="margin:12px 0 0">Assumes all <?= $am ?> is W-2 wages, the standard deduction, no pre-tax contributions and no credits. State and local income tax are not included.</p>
    </div>
  </div>
</div></section>

<section class="tool-content"><div class="wrap"><article class="prose">
  <h2 id="breakdown">How the <?= $am ?> tax is calculated (single filer)</h2>
  <p>Start with <?= $am ?> of gross wages and subtract the <?= $Y ?> standard deduction of <?= money($b['std']) ?>. That leaves <strong><?= money($b['taxable']) ?> of taxable income</strong>, which is taxed in layers:</p>
  <div class="table-wrap"><table><thead><tr><th>Bracket</th><th class="n">Income taxed at this rate</th><th class="n">Tax</th></tr></thead><tbody>
<?php foreach ($b['layers'] as $l): if ($l['amount'] <= 0) continue; ?>
    <tr><td><?= round($l['rate'] * 100) ?>%</td><td class="n"><?= money($l['amount']) ?></td><td class="n"><?= money($l['tax']) ?></td></tr>
<?php endforeach; ?>
    <tr><td><strong>Total</strong></td><td class="n"><?= money($b['taxable']) ?></td><td class="n"><strong><?= money($b['tax']) ?></strong></td></tr>
  </tbody></table></div>
  <p>Because only the top slice is taxed at <?= round($b['marginal'] * 100) ?>%, your <strong>effective federal rate is <?= number_format($b['effective'] * 100, 1) ?>%</strong>. Each additional $1,000 of salary adds about <?= money($b['marginal'] * 1000) ?> of federal income tax<?= $A < $y['ssWageBase'] ? ' plus $76.50 of FICA' : '' ?>.</p>

  <h2 id="married">Federal tax on <?= $am ?> if you’re married</h2>
  <p>Married couples filing jointly get double the standard deduction (<?= money($S['mfj']['std']) ?>) and brackets twice as wide, so <?= $am ?> of combined income produces only <strong><?= money($S['mfj']['tax']) ?></strong> of federal income tax (<?= number_format($S['mfj']['effective'] * 100, 1) ?>% effective). Filing separately, each spouse’s tax is figured on their own income using the single-width brackets — on <?= $am ?> that’s <?= money($S['mfs']['tax']) ?>. A head of household filer with <?= $am ?> owes about <?= money($S['hoh']['tax']) ?>.</p>

  <h2 id="lower">How to pay less tax on <?= $am ?></h2>
  <ul>
<?php $k = min($y['k401'], $A * 0.1); $k_tax = salary_breakdown($A - $k, 'single')['tax']; ?>
    <li><strong>Contribute to a traditional 401(k).</strong> Putting <?= money($k) ?> (<?= $A * 0.1 >= $y['k401'] ? 'the ' . $Y . ' limit' : '10% of pay' ?>) into a pre-tax 401(k) cuts a single filer’s federal tax from <?= money($b['tax']) ?> to about <?= money($k_tax) ?> — saving <?= money($b['tax'] - $k_tax) ?>.</li>
    <li><strong>Use an HSA</strong> if you have a high-deductible health plan (<?= money($y['hsa']['self']) ?> self-only limit for <?= $Y ?>).</li>
    <li><strong>Claim credits.</strong> Each qualifying child under 17 is worth up to <?= money($y['ctc']['amount']) ?> through the Child Tax Credit.</li>
    <li><strong>Check the new deductions</strong> for qualified tips (up to <?= money($y['tipsMax']) ?>) and overtime premium pay (up to $12,500).</li>
  </ul>
  <p>Model any of these in the full <a href="/calculators/federal-income-tax/?wages=<?= $A ?>">federal income tax calculator</a>, or see your per-paycheck amount in the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>.</p>
  <?php if ($A <= 120000): ?><div class="callout"><?= icon('spark') ?><p>Is your <?= $am ?> from freelance or 1099 work instead of a W-2 job? You’ll also owe about <?= money($A * 0.9235 * 0.153) ?> of self-employment tax. Run it in the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>.</p></div><?php endif; ?>

  <h2 id="other-salaries">Federal tax on other salaries</h2>
  <ul class="pill-links">
<?php foreach (SALARY_PAGES as $o): ?>
    <li><a href="/calculators/federal-income-tax/<?= $o ?>/"<?= $o === $A ? ' aria-current="page"' : '' ?>><?= money($o) ?></a></li>
<?php endforeach; ?>
  </ul>
  <p><?php if ($prevA): ?>← <a href="/calculators/federal-income-tax/<?= $prevA ?>/">Federal tax on <?= money($prevA) ?></a><?php endif; ?><?php if ($prevA && $nextA) echo ' · '; ?><?php if ($nextA): ?><a href="/calculators/federal-income-tax/<?= $nextA ?>/">Federal tax on <?= money($nextA) ?></a> →<?php endif; ?></p>

<?= faq_block([
  ["How much federal tax do I pay on $am?", "<p>A single filer pays about " . money($b['tax']) . " in $Y federal income tax on $am of W-2 wages after the " . money($b['std']) . " standard deduction. Married filing jointly it's " . money($S['mfj']['tax']) . " and head of household " . money($S['hoh']['tax']) . ".</p>"],
  ["What tax bracket is $am in?", "<p>For a single filer, $am of salary falls in the " . round($b['marginal'] * 100) . "% federal bracket for $Y (based on taxable income of " . money($b['taxable']) . "). For married couples filing jointly it is the " . round($S['mfj']['marginal'] * 100) . "% bracket.</p>"],
  ["What is $am after taxes?", "<p>About " . money($b['net']) . " a year (" . money($b['net'] / 12) . " a month) for a single filer after federal income tax and FICA, before any state or local income tax, retirement contributions or benefits.</p>"],
  ["How much is $am a month before tax?", "<p>$am a year is " . money($A / 12) . " a month, " . money($A / 26) . " every two weeks, or about " . money($A / 2080, 2) . " an hour based on 2,080 working hours. See the <a href=\"/calculators/salary-to-hourly/\">salary to hourly calculator</a>.</p>"],
]) ?>
</article></div></section>
<div class="wrap"><?= related_tools('federal-income-tax', ['federal-income-tax', 'paycheck-calculator', 'tax-refund-calculator', 'salary-to-hourly']) ?></div>
