<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Overtime Calculator $Y + No Tax on Overtime | CPA Calculator";
$P['description'] = "Free overtime calculator for $Y: time-and-a-half and double-time pay, plus the no tax on overtime deduction, phase-out and how much federal tax you save.";
$P['scripts'] = ['/assets/js/tools/overtime-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

$po = $y['obbbaPhaseOut'];
$otMax = $y['overtimeMax'];
/* Server-side mirror of the calculator: weekly overtime at 1.5x, standard deduction, no other income. */
function ot_ex(float $rate, float $reg, float $h15, int $otWeeks, string $status = 'single', int $weeks = 52): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $regAnnual = $rate * $reg * $weeks;
  $otAnnual = $rate * 1.5 * $h15 * $otWeeks;
  $annual = $regAnnual + $otAnnual;
  $qual = min($h15, max(0, $reg + $h15 - 40)) * $rate * 0.5 * $otWeeks;
  $phase = max(0, $annual - $y['obbbaPhaseOut']['start'][$status]) * $y['obbbaPhaseOut']['per1000'] / 1000;
  $ded = $status === 'mfs' ? 0 : max(0, min($qual, $y['overtimeMax'][$status]) - $phase);
  $std = $y['std'][$status];
  $without = fed_tax(max(0, $annual - $std), $status);
  $with = fed_tax(max(0, $annual - $std - $ded), $status);
  return compact('rate', 'reg', 'h15', 'otWeeks', 'regAnnual', 'otAnnual', 'annual', 'qual', 'ded', 'std') +
    ['without' => $without['tax'], 'with' => $with['tax'], 'saved' => $without['tax'] - $with['tax'], 'marginal' => $with['marginal']];
}
$ex = ot_ex(28, 40, 8, 50);

echo tool_hero('overtime-calculator', "Overtime Calculator $Y (No Tax on Overtime)",
  "Work out your overtime pay at time-and-a-half and double time, your weekly and yearly gross, and how much the new no tax on overtime deduction lowers your federal income tax. The deduction covers the qualified overtime premium, up to " . money($otMax['single']) . " (" . money($otMax['mfj']) . " joint), for 2025 through 2028.",
  ['1.5x and 2x overtime pay', 'Qualified OT premium', 'Phase-out & caps applied', 'Federal tax saved']);
?>
<section class="tool" aria-label="Overtime calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="ot-form" novalidate>
        <div class="grid-2">
          <?= year_field() ?>
          <?= money_field('rate', 'Regular hourly rate', 28, 'Your base hourly rate. Under the FLSA, the “regular rate” also includes non-discretionary bonuses and shift differentials.') ?>
        </div>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Hours per week</legend>
          <div class="grid-3">
            <?= money_field('regHours', 'Regular hours', 40, 'Straight-time hours per week, usually 40.', '', '') ?>
            <?= money_field('ot15', 'OT hours at 1.5×', 8, 'Hours paid at time-and-a-half in a typical overtime week.', '', '') ?>
            <?= money_field('ot2', 'OT hours at 2×', '', 'Hours paid at double time, for example under a union contract or state law.', '', '') ?>
          </div>
          <input type="range" min="0" max="40" step="1" data-range-for="ot15" aria-label="Overtime hours slider">
          <div class="grid-2">
            <?= money_field('weeks', 'Weeks worked per year', 52, 'Weeks you are paid regular hours. Use 50 if you take two unpaid weeks off.', '', '') ?>
            <?= money_field('otWeeks', 'Weeks per year with overtime', 50, 'How many of those weeks include the overtime hours above.', '', '') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>No tax on overtime</legend>
          <?= money_field('magi', 'Modified AGI estimate', '', 'Your household AGI for the year, including a spouse’s income if filing jointly. The deduction shrinks by $100 per $1,000 above ' . money($po['start']['single']) . ' (' . money($po['start']['mfj']) . ' joint).', 'Leave blank to use your annual pay from this calculator.') ?>
          <label class="check"><input type="checkbox" name="flsa" checked> I’m a non-exempt employee paid overtime under the FLSA</label>
          <label class="check"><input type="checkbox" name="dtOver40" checked> My double-time hours are also over 40 in the workweek</label>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Annual overtime pay</div>
          <div class="res-big" data-out="otAnnual">$0</div>
          <div class="res-sub" data-out="otSub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Time-and-a-half rate</small><b data-out="otRate">$0</b></div>
            <div class="kpi"><small>Double-time rate</small><b data-out="dtRate">$0</b></div>
            <div class="kpi"><small>Annual gross pay</small><b data-out="annual">$0</b></div>
            <div class="kpi"><small>Qualified OT premium</small><b data-out="qual">$0</b></div>
          </div>
          <div class="res-label">No tax on overtime: federal tax saved</div>
          <div class="res-big good" data-out="saved">$0</div>
          <div class="res-sub" data-out="savedSub">—</div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Annual pay by type"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note">Estimate only. Assumes W-2 wages, the standard deduction and no other income; overtime hours are hours over 40 in a workweek. State tax not included. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use the overtime calculator</h2>
      <p>This overtime calculator does two jobs. First, it works out your overtime pay: your time-and-a-half and double-time rates, your weekly paycheck and your yearly gross. Second, it works out the <strong>no tax on overtime</strong> deduction created by the One Big Beautiful Bill Act, which lets many hourly workers deduct the premium part of their overtime pay from federal taxable income for 2025 through 2028.</p>
      <ol>
        <li><strong>Enter your hourly rate</strong> and your regular hours per week.</li>
        <li><strong>Add overtime hours</strong> at 1.5× and, if you get it, at 2×.</li>
        <li><strong>Set how many weeks</strong> you work and how many include overtime. Seasonal overtime? Lower the overtime weeks.</li>
        <li><strong>Choose your filing status</strong> and, if your household income is higher than your pay (a working spouse, side income), enter your modified AGI so the phase-out is applied correctly.</li>
      </ol>

      <h2 id="formula">Overtime pay formula</h2>
      <p>The Fair Labor Standards Act (FLSA) requires non-exempt employees to be paid at least 1.5 times their regular rate for hours worked over 40 in a workweek. The math:</p>
      <div class="formula">Overtime rate = hourly rate × 1.5 (double time = × 2)<br>Weekly pay = rate × regular hours + OT rate × OT hours<br>Qualified OT premium = rate × 0.5 × FLSA overtime hours<br>Deduction = min(premium, <?= money($otMax['single']) ?> or <?= money($otMax['mfj']) ?> joint) − $<?= $po['per1000'] ?> per $1,000 of MAGI over the threshold<br>Tax saved = tax without deduction − tax with deduction</div>
      <p>Only the “half” in time-and-a-half is deductible. If you earn $28 an hour, each overtime hour pays $42, but only $14 of it is qualified overtime compensation. The $28 straight-time part is taxed like the rest of your wages, and for double-time hours the extra half beyond 1.5× doesn’t qualify either, because the FLSA only requires time-and-a-half.</p>

      <h2 id="example">Worked example: $<?= $ex['rate'] ?>/hour with <?= $ex['h15'] ?> overtime hours a week</h2>
      <p>A single filer earns $<?= $ex['rate'] ?> an hour, works 40 regular hours plus <?= $ex['h15'] ?> hours of time-and-a-half overtime in <?= $ex['otWeeks'] ?> weeks of <?= $Y ?>, and has no other income:</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Regular pay (40 h × $<?= $ex['rate'] ?> × 52 weeks)</td><td class="n"><?= money($ex['regAnnual']) ?></td></tr>
        <tr><td>Overtime pay (<?= $ex['h15'] ?> h × <?= money($ex['rate'] * 1.5, 2) ?> × <?= $ex['otWeeks'] ?> weeks)</td><td class="n"><?= money($ex['otAnnual']) ?></td></tr>
        <tr><td>Annual gross pay</td><td class="n"><?= money($ex['annual']) ?></td></tr>
        <tr><td>Qualified overtime premium (<?= $ex['h15'] ?> h × <?= money($ex['rate'] * 0.5, 2) ?> × <?= $ex['otWeeks'] ?>)</td><td class="n"><?= money($ex['qual']) ?></td></tr>
        <tr><td>Overtime deduction (under the <?= money($otMax['single']) ?> cap, no phase-out)</td><td class="n"><?= money($ex['ded']) ?></td></tr>
        <tr><td>Federal income tax without the deduction</td><td class="n"><?= money($ex['without']) ?></td></tr>
        <tr><td>Federal income tax with the deduction</td><td class="n"><?= money($ex['with']) ?></td></tr>
        <tr><td><strong>Federal tax saved</strong></td><td class="n"><strong><?= money($ex['saved']) ?></strong></td></tr>
      </tbody></table></div>
      <p>The savings equal the deduction times the worker’s <?= round($ex['marginal'] * 100) ?>% marginal rate. Social Security and Medicare are still due on all <?= money($ex['otAnnual']) ?> of overtime pay, because the deduction only affects federal income tax.</p>

      <h2 id="qualifies">What counts as qualified overtime</h2>
      <p>Qualified overtime compensation is overtime pay <strong>required by section 7 of the FLSA</strong> that exceeds your regular rate. In practice:</p>
      <ul>
        <li><strong>Counts:</strong> the half-time premium for hours over 40 in a workweek for non-exempt employees, including hourly workers and non-exempt salaried staff.</li>
        <li><strong>Doesn’t count:</strong> the straight-time part of overtime pay, the extra premium in double time, daily overtime required only by state law (for example, over 8 hours in a day when the week is under 40), overtime paid under a union contract or company policy beyond what the FLSA requires, and pay for exempt employees who get overtime voluntarily.</li>
        <li><strong>Regular rate matters:</strong> under the FLSA, non-discretionary bonuses and shift differentials are part of your regular rate, so the premium is half of that blended rate.</li>
      </ul>
      <p>Independent contractors aren’t covered by the FLSA’s overtime rules, so 1099 workers can’t claim this deduction. Check the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> instead.</p>

      <h2 id="limits">Deduction limits and phase-out</h2>
      <p>The deduction is capped per return, not per person, and it phases out by $<?= $po['per1000'] ?> for every $1,000 of modified AGI above the threshold:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Filing status</th><th class="n">Maximum deduction</th><th class="n">Phase-out starts</th><th class="n">No deduction at MAGI of</th></tr></thead><tbody>
<?php foreach (['single', 'hoh', 'mfj'] as $s): ?>
        <tr><td><?= status_label($s) ?></td><td class="n"><?= money($otMax[$s]) ?></td><td class="n"><?= money($po['start'][$s]) ?></td><td class="n"><?= money($po['start'][$s] + $otMax[$s] / ($po['per1000'] / 1000)) ?></td></tr>
<?php endforeach; ?>
        <tr><td>Married filing separately</td><td class="n" colspan="3">Not allowed: you must file jointly</td></tr>
      </tbody></table></div>
      <p>You also need a Social Security number valid for employment on the return. The deduction is available whether you take the standard deduction or itemize, but it doesn’t lower your AGI, so it won’t help with AGI-based limits elsewhere on the return.</p>

      <h2 id="reporting">W-2 reporting and Schedule 1-A</h2>
      <p>You claim the deduction on <strong>Schedule 1-A</strong>, the new schedule for the tips, overtime, car loan interest and senior deductions, which flows to Form 1040. The amount comes from your employer:</p>
      <ul>
        <li><strong>For <?= $Y ?> and later,</strong> employers report qualified overtime compensation separately on Form W-2, so the number you need is printed for you.</li>
        <li><strong>For 2025,</strong> employers weren’t required to report it separately. The IRS allowed workers to use a reasonable method, such as adding up the overtime premium shown on pay stubs, or a separate statement from the employer.</li>
      </ul>
      <p>If you expect a large overtime deduction, you can reduce your paycheck withholding by entering it as a deduction in Step 4(b) of Form W-4. The <a href="/calculators/paycheck-calculator/">paycheck calculator</a> and <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> help you check the result.</p>

      <h2 id="still-taxed">What no tax on overtime doesn’t cover</h2>
      <ul>
        <li><strong>FICA:</strong> Social Security (6.2% up to <?= money($y['ssWageBase']) ?>) and Medicare (1.45%) still apply to every overtime dollar.</li>
        <li><strong>State income tax:</strong> states decide for themselves whether to follow the federal deduction, and many don’t. Your state may tax all of your overtime.</li>
        <li><strong>Withholding:</strong> your employer still withholds federal tax on overtime as usual; the savings show up as a lower tax bill or bigger refund when you file.</li>
      </ul>
      <div class="callout"><?= icon('spark') ?><p><strong>Tip:</strong> keep your final pay stub for each year through 2028. It shows total overtime hours and pay, which makes it easy to check the W-2 figure.</p></div>
      <p>Want to compare hourly and salaried offers? The <a href="/calculators/salary-to-hourly/">salary to hourly calculator</a> converts between the two, and the <a href="/calculators/tips-tax-calculator/">no tax on tips calculator</a> handles the companion tips deduction.</p>

<?= faq_block([
  ['How do I calculate overtime pay?', "<p>Multiply your hourly rate by 1.5 to get your overtime rate, then multiply by your overtime hours. At \$" . $ex['rate'] . " an hour, overtime pays " . money($ex['rate'] * 1.5, 2) . " an hour, so " . $ex['h15'] . " overtime hours add " . money($ex['rate'] * 1.5 * $ex['h15'], 2) . " to a week’s pay. Double time is your rate times 2.</p>"],
  ['Is overtime tax-free in ' . $Y . '?', "<p>Partly. For 2025 through 2028, you can deduct the qualified overtime premium (the half in time-and-a-half) up to " . money($otMax['single']) . ", or " . money($otMax['mfj']) . " on a joint return. The straight-time part is still taxable, and Social Security, Medicare and usually state tax still apply.</p>"],
  ['How much will no tax on overtime save me?', "<p>Your savings equal the deduction times your marginal federal rate. In the example above, " . money($ex['qual']) . " of qualified premium saves a single filer in the " . round($ex['marginal'] * 100) . "% bracket about " . money($ex['saved']) . ". Enter your hours above for your own figure.</p>"],
  ['Who qualifies for the no tax on overtime deduction?', "<p>Employees who receive overtime pay required by the FLSA, have a valid Social Security number and, if married, file jointly. The deduction shrinks by \$" . $po['per1000'] . " per \$1,000 of modified AGI over " . money($po['start']['single']) . " (" . money($po['start']['mfj']) . " joint).</p>"],
  ['Does double time qualify for the overtime deduction?', '<p>Only the first half-time premium does, and only for hours over 40 in the workweek. If you earn double time for an FLSA overtime hour, the 0.5× premium qualifies but the extra 0.5× does not. Double time paid under state law or a contract for hours that aren’t FLSA overtime doesn’t qualify.</p>'],
  ['Does the overtime deduction reduce Social Security and Medicare taxes?', '<p>No. It’s an income tax deduction only. FICA is withheld on all overtime pay, and your Social Security earnings record still includes it.</p>'],
  ['Where do I claim the overtime deduction?', '<p>On Schedule 1-A, attached to Form 1040. Use the qualified overtime amount your employer reports on your W-2 (or, for 2025, a reasonable figure from your pay stubs if your employer didn’t provide one).</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('overtime-calculator', ['tips-tax-calculator', 'paycheck-calculator', 'salary-to-hourly', 'tax-refund-calculator', 'federal-income-tax', 'bonus-tax-calculator']) ?></div>
