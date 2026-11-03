<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Self Employment Tax Calculator $Y — Schedule SE Estimator | CPA Calculator";
$P['description'] = "Free $Y self employment tax calculator. Get your Social Security and Medicare tax, the W-2 wage base interaction, Additional Medicare and ½ SE deduction.";
$P['scripts'] = ['/assets/js/tools/self-employment-tax.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Server-side mirror of the JS Schedule SE math so the worked examples match the calculator. */
function se_example(float $net, float $w2, string $status = 'single'): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $base = max(0, $net) * 0.9235;
  if ($base < 400) return ['base' => $base, 'room' => 0, 'ss' => 0, 'med' => 0, 'addl' => 0, 'se' => 0, 'half' => 0];
  $room = max(0, $y['ssWageBase'] - $w2);
  $ss = min($base, $room) * 0.124;
  $med = $base * 0.029;
  $addl = max(0, $base - max(0, $y['addlMedicare'][$status] - $w2)) * 0.009;
  return ['base' => $base, 'room' => $room, 'ss' => $ss, 'med' => $med, 'addl' => $addl, 'se' => $ss + $med, 'half' => ($ss + $med) / 2];
}
$ex = se_example(80000, 0);
$ex2 = se_example(50000, 170000);
$maxSs = $y['ssWageBase'] * 0.124;

echo tool_hero('self-employment-tax', "Self-Employment Tax Calculator $Y",
  "Work out your $Y self-employment tax exactly the way Schedule SE does: 92.35% of net earnings, 12.4% Social Security up to the " . money($y['ssWageBase']) . " wage base (reduced by any W-2 wages), 2.9% Medicare, the 0.9% Additional Medicare Tax and your deductible half.",
  ['Schedule SE line by line', 'W-2 wage base interaction', 'Additional Medicare (Form 8959)', '½ SE tax deduction value']);
?>
<section class="tool" aria-label="Self-employment tax calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="se-form" novalidate>
        <?= year_field() ?>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Self-employment earnings</legend>
          <?= money_field('profit', 'Schedule C net profit', 80000, 'Line 31 of Schedule C: gross receipts minus business expenses. Enter a loss with a minus sign.') ?>
          <input type="range" min="0" max="400000" step="1000" data-range-for="profit" aria-label="Net profit slider">
          <div class="grid-2">
            <?= money_field('farm', 'Schedule F farm net profit', '', 'Net farm profit or loss (Schedule F line 34). Combined with your other self-employment earnings.') ?>
            <?= money_field('k1', 'Partnership SE earnings (K-1 Box 14A)', '', 'General partners and LLC members taxed as partnerships: net earnings from self-employment reported in Box 14, code A.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>W-2 wages (if you also have a job)</legend>
          <div class="grid-2">
            <?= money_field('wages', 'Social Security wages (W-2 Box 3 + 7)', '', 'Wages already taxed for Social Security use up part of the ' . money($y['ssWageBase']) . ' wage base, so less of your self-employment income is hit by the 12.4%.') ?>
            <?= money_field('medWages', 'Medicare wages (W-2 Box 5)', '', 'Used for the 0.9% Additional Medicare Tax threshold. Leave blank to use the same amount as Box 3.') ?>
          </div>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Self-employment tax (Schedule SE)</div>
          <div class="res-big" data-out="se">$0</div>
          <div class="res-sub" data-out="sub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Social Security (12.4%)</small><b data-out="ss">$0</b></div>
            <div class="kpi"><small>Medicare (2.9%)</small><b data-out="med">$0</b></div>
            <div class="kpi"><small>Deductible half</small><b data-out="half">$0</b></div>
            <div class="kpi"><small>Rate on net profit</small><b data-out="eff">0%</b></div>
          </div>
          <div class="res-label" style="margin-bottom:0">Social Security wage base used (<span data-out="wb"><?= money($y['ssWageBase']) ?></span>)</div>
          <div class="meter" data-meter role="img" aria-label="Share of the Social Security wage base used by W-2 wages and self-employment earnings"></div>
          <ul class="legend" data-meter-legend style="margin-bottom:16px"></ul>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your self-employment profit goes"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note">Federal only. Income tax is figured separately — see the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>. Church employee income and the optional methods are not modeled; see below. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="what-is-se-tax">What is self-employment tax?</h2>
      <p>Self-employment tax is the Social Security and Medicare tax for people who work for themselves. An employee splits these taxes with an employer — 7.65% each. When you’re a sole proprietor, independent contractor, freelancer or general partner, you pay both halves: <strong>15.3%</strong> in total, figured on Schedule SE and added to your Form 1040.</p>
      <p>It’s separate from income tax. Even if the standard deduction wipes out your income tax, you still owe self-employment tax once your net earnings from self-employment reach $400. For many freelancers earning under about $100,000, it is actually the bigger of the two taxes.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Component (<?= $Y ?>)</th><th class="n">Rate</th><th>Applies to</th></tr></thead><tbody>
        <tr><td>Social Security (OASDI)</td><td class="n">12.4%</td><td>Net SE earnings up to <?= money($y['ssWageBase']) ?>, minus W-2 Social Security wages</td></tr>
        <tr><td>Medicare (HI)</td><td class="n">2.9%</td><td>All net SE earnings — no cap</td></tr>
        <tr><td>Additional Medicare Tax</td><td class="n">0.9%</td><td>Combined wages + SE earnings above <?= money($y['addlMedicare']['single']) ?> single/HOH, <?= money($y['addlMedicare']['mfj']) ?> joint, <?= money($y['addlMedicare']['mfs']) ?> separate (Form 8959)</td></tr>
      </tbody></table></div>

      <h2 id="how-to-use">How to use this self employment tax calculator</h2>
      <ol>
        <li><strong>Pick the tax year and filing status.</strong> Filing status only matters for the Additional Medicare Tax threshold; the 15.3% itself is the same for everyone.</li>
        <li><strong>Enter your net profit.</strong> Use Schedule C line 31 — your 1099 and other business income minus deductible expenses — not gross receipts. Add farm profit or partnership self-employment earnings if you have them; a loss in one business offsets profit in another.</li>
        <li><strong>Add W-2 wages if you also have a job.</strong> This is the step most simple calculators skip. Social Security wages already taxed at your job count against the same wage base, so they can reduce or eliminate the 12.4% on your side income.</li>
      </ol>
      <p>The results show the Schedule SE tax, how it splits between Social Security and Medicare, the half you can deduct, how much of the wage base you’ve used, and any Additional Medicare Tax that goes on Form 8959.</p>

      <h2 id="formula">The self-employment tax formula</h2>
      <p>Schedule SE doesn’t apply 15.3% to your full profit. It first multiplies net profit by 92.35% — that removes the “employer half” of the tax, mirroring the fact that an employer’s share of FICA isn’t counted as an employee’s wages.</p>
      <div class="formula">Net SE earnings = net profit × 92.35%<br>Social Security = 12.4% × min(net SE earnings, <?= money($y['ssWageBase']) ?> − W-2 Social Security wages)<br>Medicare = 2.9% × net SE earnings<br>SE tax = Social Security + Medicare<br>Deduction = ½ × SE tax (Schedule 1, line 15)</div>
      <p>The maximum Social Security portion anyone can pay through self-employment in <?= $Y ?> is <?= money($maxSs, 2) ?> (12.4% × <?= money($y['ssWageBase']) ?>). Medicare has no ceiling.</p>

      <h2 id="example">Worked example: $80,000 net profit</h2>
      <p>A single freelance designer with $80,000 of Schedule C net profit and no W-2 job in <?= $Y ?>:</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Net profit</td><td class="n">$80,000</td></tr>
        <tr><td>Net SE earnings ($80,000 × 92.35%)</td><td class="n"><?= money($ex['base'], 2) ?></td></tr>
        <tr><td>Social Security (12.4%)</td><td class="n"><?= money($ex['ss'], 2) ?></td></tr>
        <tr><td>Medicare (2.9%)</td><td class="n"><?= money($ex['med'], 2) ?></td></tr>
        <tr><td><strong>Self-employment tax</strong></td><td class="n"><strong><?= money($ex['se'], 2) ?></strong></td></tr>
        <tr><td>Deductible half (reduces AGI)</td><td class="n"><?= money($ex['half'], 2) ?></td></tr>
      </tbody></table></div>
      <p>That’s <?= number_format($ex['se'] / 80000 * 100, 2) ?>% of net profit — the effective SE rate below the wage base is always 14.13% (92.35% × 15.3%). The deductible half lowers taxable income, so in the 12% bracket it saves roughly <?= money($ex['half'] * 0.12) ?> of income tax.</p>

      <h2 id="w2-wage-base">How W-2 wages interact with the Social Security wage base</h2>
      <p>The <?= money($y['ssWageBase']) ?> Social Security wage base is a single cap on <em>all</em> your earnings — wages and self-employment combined. Your employer has already withheld Social Security on your W-2 wages, so Schedule SE line 8 subtracts them before applying the 12.4%.</p>
      <p>Example: a hospital employee with $170,000 of W-2 wages and $50,000 of net profit from consulting (single filer):</p>
      <ul>
        <li>Net SE earnings: $50,000 × 92.35% = <?= money($ex2['base']) ?></li>
        <li>Wage base room left: <?= money($y['ssWageBase']) ?> − $170,000 = <?= money($ex2['room']) ?>, so Social Security is only 12.4% × <?= money($ex2['room']) ?> = <strong><?= money($ex2['ss'], 2) ?></strong></li>
        <li>Medicare on all of it: 2.9% × <?= money($ex2['base']) ?> = <?= money($ex2['med'], 2) ?></li>
        <li>Additional Medicare: wages + SE earnings exceed $200,000 by <?= money(170000 + $ex2['base'] - 200000) ?>, so 0.9% = <strong><?= money($ex2['addl'], 2) ?></strong> on Form 8959</li>
      </ul>
      <p>Without the W-2 adjustment the Social Security piece would be <?= money($ex2['base'] * 0.124, 2) ?> — an overstatement of <?= money($ex2['base'] * 0.124 - $ex2['ss']) ?>. If your wages alone exceed the wage base, you pay only the 2.9% Medicare (plus any Additional Medicare) on self-employment income.</p>
      <div class="callout"><?= icon('spark') ?><p><strong>Two jobs, too much withheld?</strong> If two or more <em>employers</em> together withheld Social Security on more than <?= money($y['ssWageBase']) ?>, the excess comes back as a credit on Schedule 3. That’s different from the self-employment adjustment above, which happens automatically on Schedule SE.</p></div>

      <h2 id="additional-medicare">The 0.9% Additional Medicare Tax</h2>
      <p>High earners pay an extra 0.9% Medicare tax on combined wages and self-employment earnings above the threshold for their filing status. It’s calculated on Form 8959, not Schedule SE, so it is <strong>not</strong> part of the deductible half. When you have wages, the threshold for self-employment income is reduced by your Medicare wages (W-2 Box 5) — which is why this calculator asks for Box 5 separately.</p>

      <h2 id="half-deduction">The deduction for half of self-employment tax</h2>
      <p>You can deduct 50% of your Schedule SE tax as an adjustment to income on Schedule 1. It reduces your AGI — and therefore your income tax — but not the self-employment tax itself or your Schedule C profit. When figuring the 20% QBI deduction, the deductible half is subtracted from qualified business income, so it trims that deduction slightly. The calculator estimates how much income tax the deduction saves at your bracket.</p>

      <h2 id="special-cases">Special cases: church employees, farm and nonfarm optional methods</h2>
      <ul>
        <li><strong>Church employee income.</strong> If you work for a church or qualified church-controlled organization that elected out of FICA, wages of $108.28 or more are subject to SE tax and go on Schedule SE line 5a without the $400 threshold. Ministers have their own rules for housing allowances and exemptions (Form 4361).</li>
        <li><strong>Farm optional method.</strong> Farmers with gross farm income of up to a set limit, or small net farm profits, can elect to report a larger amount of net earnings (up to an annually indexed cap) to earn Social Security credits in a low-profit year. It raises SE tax on purpose.</li>
        <li><strong>Nonfarm optional method.</strong> Available up to five times in a lifetime when net nonfarm profit is small relative to gross income. It can help you qualify for Social Security coverage or a larger earned income credit.</li>
        <li><strong>Statutory employees and notaries.</strong> Statutory employee income on Schedule C and notary fees are not subject to SE tax.</li>
      </ul>
      <p>These are rare, so the calculator leaves them out. Check the Schedule SE instructions or a tax professional if one applies.</p>

      <h2 id="lower-se-tax">Legal ways to lower self-employment tax</h2>
      <ol>
        <li><strong>Claim every business expense.</strong> SE tax is based on net profit, so mileage (<?= ($y['mileage'] * 100) ?>¢ per mile in <?= $Y ?>), a <a href="/calculators/home-office-deduction/">home office</a>, software, equipment and fees all cut it. Each $1,000 of expenses saves about $141 of SE tax before income tax savings. Try the <a href="/calculators/mileage-deduction/">mileage deduction calculator</a>.</li>
        <li><strong>Consider an S corporation.</strong> Once profit is well above a reasonable salary, an S corp pays FICA only on wages, not distributions. Compare with the <a href="/calculators/s-corp-tax-savings/">S corp tax savings calculator</a>.</li>
        <li><strong>Know what doesn’t help.</strong> SEP-IRA and Solo 401(k) contributions and self-employed health insurance lower income tax but not SE tax, because they are deducted on Schedule 1, not Schedule C.</li>
      </ol>
      <p>Self-employment tax is paid through <a href="/calculators/quarterly-estimated-tax/">quarterly estimated taxes</a> along with your income tax. New to it? Read <a href="/blog/quarterly-taxes-101-guide/">Quarterly Taxes 101</a> and <a href="/blog/got-a-1099-exactly-what-to-do-next/">what to do after you get a 1099</a>.</p>

<?= faq_block([
  ['How do I calculate self-employment tax?', "<p>Multiply net profit by 92.35% to get net earnings from self-employment. Apply 12.4% Social Security to that amount up to " . money($y['ssWageBase']) . " (minus any W-2 Social Security wages) and 2.9% Medicare to all of it. For \$80,000 of profit with no W-2 job, that’s " . money($ex['se'], 2) . " for $Y.</p>"],
  ["What is the self-employment tax rate for $Y?", "<p>15.3% — 12.4% Social Security and 2.9% Medicare — applied to 92.35% of net profit, so the effective rate on profit is about 14.13%. Social Security stops at the " . money($y['ssWageBase']) . " wage base; Medicare continues, and an extra 0.9% applies above \$200,000 (\$250,000 married filing jointly).</p>"],
  ['Do I pay self-employment tax if I also have a W-2 job?', '<p>Yes, on your self-employment profit — but your W-2 Social Security wages reduce the wage base available for the 12.4% portion. If your wages already exceed ' . money($y['ssWageBase']) . ', you only owe the 2.9% Medicare portion (plus any Additional Medicare Tax) on your side income.</p>'],
  ['Is self-employment tax deductible?', '<p>Half of it is. The deduction for one-half of self-employment tax is an adjustment to income on Schedule 1, which lowers your AGI and income tax. The 0.9% Additional Medicare Tax is not part of the deductible amount.</p>'],
  ['Do I have to pay self-employment tax if I made less than $400?', '<p>No. If your net earnings from self-employment (net profit × 92.35%) are under $400, you owe no SE tax, although the income is still subject to income tax. Church employee income is the exception: SE tax applies once it reaches $108.28.</p>'],
  ['Why is self-employment tax so high compared to a W-2 job?', '<p>Employees pay 7.65% and the employer pays another 7.65% behind the scenes. Self-employed people pay both halves. The 92.35% adjustment and the deduction for half of SE tax soften the difference, but your out-of-pocket payroll tax is still roughly double an employee’s.</p>'],
  ['When is self-employment tax paid?', '<p>Through quarterly estimated payments using Form 1040-ES, combined with your income tax, then reconciled on Schedule SE when you file. For ' . $Y . ' the due dates are ' . implode(', ', $y['quarterlyDue']) . '.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('self-employment-tax', ['1099-tax-calculator', 'quarterly-estimated-tax', 's-corp-tax-savings', 'mileage-deduction', 'home-office-deduction', 'federal-income-tax']) ?></div>
