<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "No Tax on Tips Calculator $Y: Tip Tax Savings | CPA Calculator";
$P['description'] = "Free no tax on tips calculator for $Y. See how much the qualified tips deduction saves you, the " . money($y['tipsMax']) . " cap, MAGI phase-out and the FICA still owed.";
$P['scripts'] = ['/assets/js/tools/tips-tax-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

$po = $y['obbbaPhaseOut'];
$max = $y['tipsMax'];
/* Server-side mirror of the calculator for an employee with W-2 wages and reported tips (standard deduction). */
function tips_ex(float $wages, float $tips, string $status = 'single'): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $gross = $wages + $tips;
  $phase = max(0, $gross - $y['obbbaPhaseOut']['start'][$status]) * $y['obbbaPhaseOut']['per1000'] / 1000;
  $ded = $status === 'mfs' ? 0 : max(0, min($tips, $y['tipsMax']) - $phase);
  $std = $y['std'][$status];
  $tw = max(0, $gross - $std);
  $tWith = max(0, $gross - $std - $ded);
  $without = fed_tax($tw, $status)['tax'];
  $with = fed_tax($tWith, $status)['tax'];
  $base = $y['ssWageBase'];
  $fica = (min($gross, $base) - min($wages, $base)) * 0.062 + $tips * 0.0145;
  return compact('status', 'wages', 'tips', 'gross', 'ded', 'std', 'tw', 'tWith', 'without', 'with', 'fica') + ['saved' => $without - $with];
}
$ex = tips_ex(28000, 20000);
$table = array_map(fn($a) => tips_ex($a[0], $a[1], $a[2]), [[25000, 10000, 'single'], [28000, 20000, 'single'], [45000, 30000, 'single'], [60000, 25000, 'mfj'], [140000, 25000, 'single']]);

echo tool_hero('tips-tax-calculator', "No Tax on Tips Calculator $Y",
  "See how much the new deduction for qualified tips saves you. Enter your cash and card tips and your wages to find your deduction (up to " . money($max) . "), the MAGI phase-out, the federal income tax you save, and the Social Security and Medicare you still owe on tips.",
  ['Up to ' . money($max) . ' deduction', 'MAGI phase-out applied', 'Employees & self-employed', 'FICA still owed shown']);
?>
<section class="tool" aria-label="No tax on tips calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="tips-form" novalidate>
        <?= year_field() ?>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Tips &amp; wages for the year</legend>
          <div class="grid-2">
            <?= money_field('cashTips', 'Cash tips', 6000, 'Tips received in cash and reported to your employer (or recorded, if self-employed).') ?>
            <?= money_field('cardTips', 'Card & app tips', 14000, 'Tips paid by credit or debit card, check or a payment app. These count as “cash tips” under the law.') ?>
          </div>
          <?= money_field('wages', 'Wages, not counting tips', 28000, 'Your hourly or salary pay for the year without tips. Include a spouse’s wages if filing jointly.') ?>
          <?= money_field('magi', 'Modified AGI estimate', '', 'Total household AGI. The deduction drops by $100 per $1,000 over ' . money($po['start']['single']) . ' (' . money($po['start']['mfj']) . ' joint).', 'Leave blank to use wages + tips.') ?>
        </fieldset>
        <fieldset class="fieldset"><legend>Eligibility</legend>
          <label class="check"><input type="checkbox" name="occupation" checked> I work in an occupation that customarily received tips (on the IRS list)</label>
          <label class="check"><input type="checkbox" name="ssn" checked> I have a Social Security number valid for employment</label>
          <label class="check"><input type="checkbox" name="selfEmployed"> My tips are self-employment income (1099 / own business)</label>
          <div data-se-only hidden>
            <?= money_field('seExp', 'Business expenses for the tipped work', '', 'Self-employed: the deduction can’t exceed your net income from the business that earned the tips.') ?>
          </div>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Federal income tax saved by the tips deduction</div>
          <div class="res-big good" data-out="saved">$0</div>
          <div class="res-sub" data-out="savedSub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Total tips</small><b data-out="tips">$0</b></div>
            <div class="kpi"><small>Deduction allowed</small><b data-out="ded">$0</b></div>
            <div class="kpi"><small data-out="payrollLabel">Social Security &amp; Medicare on tips</small><b data-out="payroll">$0</b></div>
            <div class="kpi"><small>Income tax still on tips</small><b data-out="incOnTips">$0</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your tip money goes"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note">Estimate only. Assumes the standard deduction and no other income or credits; state income tax not included. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-it-works">How the no tax on tips deduction works</h2>
      <p>The One Big Beautiful Bill Act created a federal income tax deduction for <strong>qualified tips</strong> for tax years 2025 through 2028. It isn’t a full exemption: tips are still reported as income and still subject to Social Security and Medicare tax. Instead, you subtract up to <?= money($max) ?> of qualified tips when figuring your taxable income, which lowers your federal income tax. This no tax on tips calculator shows how much that’s worth for you, after the cap and the income phase-out.</p>
      <ol>
        <li><strong>Enter your tips for the year,</strong> split between cash and card or app tips. Both qualify.</li>
        <li><strong>Enter your wages without tips,</strong> plus your modified AGI if your household has other income.</li>
        <li><strong>Confirm eligibility:</strong> a tipped occupation, a valid Social Security number, and whether your tips come from self-employment.</li>
      </ol>

      <h2 id="formula">Tip tax deduction formula</h2>
      <div class="formula">Deduction = min(qualified tips, <?= money($max) ?>) − $<?= $po['per1000'] ?> × (MAGI − <?= money($po['start']['single']) ?>) ÷ $1,000<br>(<?= money($po['start']['mfj']) ?> threshold if married filing jointly; $0 if married filing separately)<br>Self-employed: deduction ≤ net income from the tipped business<br>Tax saved = income tax without deduction − income tax with deduction</div>
      <p>The cap is <?= money($max) ?> per return, even if both spouses earn tips. The deduction is fully phased out at <?= money($po['start']['single'] + $max / ($po['per1000'] / 1000)) ?> of MAGI for single and head-of-household filers and <?= money($po['start']['mfj'] + $max / ($po['per1000'] / 1000)) ?> for joint filers.</p>

      <h2 id="example">Worked example: <?= money($ex['tips']) ?> of tips on <?= money($ex['wages']) ?> of wages</h2>
      <p>A single server earns <?= money($ex['wages']) ?> in wages and <?= money($ex['tips']) ?> in reported tips in <?= $Y ?>:</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Wages + tips (W-2 Box 1)</td><td class="n"><?= money($ex['gross']) ?></td></tr>
        <tr><td>Standard deduction</td><td class="n">−<?= money($ex['std']) ?></td></tr>
        <tr><td>Taxable income without the tips deduction</td><td class="n"><?= money($ex['tw']) ?></td></tr>
        <tr><td>Tips deduction (no phase-out at this income)</td><td class="n">−<?= money($ex['ded']) ?></td></tr>
        <tr><td>Taxable income with the deduction</td><td class="n"><?= money($ex['tWith']) ?></td></tr>
        <tr><td>Federal income tax without / with the deduction</td><td class="n"><?= money($ex['without']) ?> / <?= money($ex['with']) ?></td></tr>
        <tr><td><strong>Federal income tax saved</strong></td><td class="n"><strong><?= money($ex['saved']) ?></strong></td></tr>
        <tr><td>Social Security and Medicare still owed on tips (7.65%)</td><td class="n"><?= money($ex['fica']) ?></td></tr>
      </tbody></table></div>
      <p>The deduction pulls this server’s taxable income from the 12% bracket down into the 10% bracket, so the savings come to <?= money($ex['saved']) ?>, about <?= round($ex['saved'] / $ex['tips'] * 100, 1) ?>% of tips. Payroll taxes on tips are unchanged.</p>

      <h3 id="examples-table">Estimated savings at other incomes</h3>
      <div class="table-wrap"><table>
        <thead><tr><th>Filing status</th><th class="n">Wages</th><th class="n">Tips</th><th class="n">Deduction</th><th class="n">Tax saved</th></tr></thead><tbody>
<?php foreach ($table as $r): ?>
        <tr><td><?= status_label($r['status']) ?></td><td class="n"><?= money($r['wages']) ?></td><td class="n"><?= money($r['tips']) ?></td><td class="n"><?= money($r['ded']) ?></td><td class="n"><?= money($r['saved']) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <p>Lower earners save less because much of their income already falls under the standard deduction or in the 10% bracket; earners above the phase-out threshold see the deduction shrink.</p>

      <h2 id="qualified-tips">What counts as qualified tips</h2>
      <ul>
        <li><strong>Voluntary payments.</strong> The customer decides whether to tip and how much. Mandatory service charges and automatic gratuities added to a bill don’t qualify.</li>
        <li><strong>“Cash tips” includes cards.</strong> Tips paid in cash, by check, by credit or debit card, or through an app all count. Non-cash tips, like tickets or goods, don’t.</li>
        <li><strong>Tipped occupations only.</strong> The work must be in an occupation that customarily and regularly received tips on or before December 31, 2024, as listed by the Treasury Department. The list covers jobs such as bartenders, wait staff, hairstylists, nail technicians, rideshare and delivery drivers, hotel staff and many entertainment, home service and personal service roles.</li>
        <li><strong>Reported tips.</strong> Tips must be reported on a W-2, a Form 1099 or Form 4137. Unreported tips you never put on your return can’t be deducted.</li>
        <li><strong>Tip pools count.</strong> Tips you receive through a tip-sharing arrangement qualify for you.</li>
        <li><strong>Some businesses are excluded.</strong> Tips earned in certain specified service businesses (the fields defined for the QBI deduction) don’t qualify.</li>
      </ul>

      <h2 id="still-taxed">Taxes you still pay on tips</h2>
      <ul>
        <li><strong>Social Security and Medicare.</strong> Employees owe 7.65% on reported tips (6.2% Social Security up to the <?= money($y['ssWageBase']) ?> wage base, plus 1.45% Medicare). The deduction doesn’t change this, which also means your tips still count toward Social Security benefits.</li>
        <li><strong>Self-employment tax.</strong> If you’re self-employed, your tips are part of your business income and carry 15.3% SE tax. The tips deduction is also limited to your net income from that business. See the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a>.</li>
        <li><strong>State income tax.</strong> Each state decides whether to adopt the federal deduction. In many states your tips remain fully taxable.</li>
        <li><strong>Withholding.</strong> Employers still withhold income tax on tips you report. You can claim the expected deduction on Form W-4, Step 4(b), to lower withholding.</li>
      </ul>

      <h2 id="claiming">How to claim the tips deduction</h2>
      <p>You claim it on <strong>Schedule 1-A</strong> with Form 1040, and it’s available whether you itemize or take the standard deduction. Starting with <?= $Y ?> Forms W-2, employers report qualified tips and your occupation separately. For 2025, the IRS let workers use reasonable figures such as the Social Security tips in W-2 Box 7. Self-employed workers use their Form 1099 amounts and their own records. Married couples must file jointly, and the return must include a Social Security number valid for employment for the person who earned the tips.</p>
      <div class="callout"><?= icon('spark') ?><p><strong>Tip:</strong> record your tips daily (Form 4070A or an app) and report them to your employer each month. Accurate reporting is what makes your tips deductible.</p></div>
      <p>Earn overtime too? The <a href="/calculators/overtime-calculator/">overtime calculator</a> handles the companion overtime deduction. For your full return, use the <a href="/calculators/federal-income-tax/">federal income tax calculator</a> or check your refund with the <a href="/calculators/tax-refund-calculator/">tax refund calculator</a>.</p>

<?= faq_block([
  ['How does no tax on tips work?', "<p>For 2025 through 2028, you can deduct up to " . money($max) . " of qualified tips from your federal taxable income on Schedule 1-A. Tips are still income, still reported, and still subject to Social Security, Medicare and (usually) state income tax.</p>"],
  ['How much will I save with no tax on tips?', "<p>Your savings equal the deduction times your federal tax rate on the income it removes. In our example, " . money($ex['tips']) . " of tips on " . money($ex['wages']) . " of wages saves a single filer about " . money($ex['saved']) . ". Use the calculator for your own numbers.</p>"],
  ['Do I still pay Social Security and Medicare on tips?', '<p>Yes. The deduction only affects federal income tax. Employees still owe 7.65% FICA on reported tips, and self-employed workers owe 15.3% self-employment tax.</p>'],
  ['Do credit card tips count for no tax on tips?', '<p>Yes. The law refers to “cash tips,” which includes tips paid in cash, by check, by credit or debit card, or electronically. Non-cash tips such as gifts or tickets don’t qualify.</p>'],
  ['Is there an income limit for the tips deduction?', "<p>Yes. The deduction drops by \$" . $po['per1000'] . " for every \$1,000 of modified AGI over " . money($po['start']['single']) . " (" . money($po['start']['mfj']) . " for joint filers) and disappears entirely at " . money($po['start']['single'] + $max / ($po['per1000'] / 1000)) . " (" . money($po['start']['mfj'] + $max / ($po['per1000'] / 1000)) . " joint).</p>"],
  ['Can married couples filing separately deduct tips?', '<p>No. Married taxpayers must file a joint return to claim the deduction, and the ' . money($max) . ' cap applies to the joint return as a whole.</p>'],
  ['Are automatic gratuities and service charges deductible?', '<p>No. Mandatory charges added to a bill, such as an automatic 18% gratuity for large parties, are treated as wages rather than tips and don’t qualify for the deduction.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('tips-tax-calculator', ['overtime-calculator', 'paycheck-calculator', 'tax-refund-calculator', 'federal-income-tax', 'self-employment-tax', 'salary-to-hourly']) ?></div>
