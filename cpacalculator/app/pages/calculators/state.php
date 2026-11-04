<?php
defined('CPA') or exit;
/* /calculators/state-income-tax/{slug}/ — one page per state + DC (router sets $STATE from app/data/states.json). */
require_once SITE_ROOT . '/app/state-calc.php';
$Y = TAX_YEAR;
$ST = states();
$S = $STATE;
$code = $S['code'];
$name = $S['name'];
$isNone = $S['type'] === 'none';
$isFlat = $S['type'] === 'flat';
$url = '/calculators/state-income-tax/' . $S['slug'] . '/';
$slink = fn($c) => '<a href="/calculators/state-income-tax/' . $ST[$c]['slug'] . '/">' . e($ST[$c]['name']) . '</a>';

/* Computed figures */
$r75 = state_calc($code, ['wages' => 75000, 'status' => 'single']);
$EX = [];
foreach ([50000, 75000, 100000] as $amt) foreach (['single', 'mfj'] as $s) $EX[] = [$amt, $s, state_calc($code, ['wages' => $amt, 'status' => $s])];
$rank = state_rank_75k();
$taxedCount = count(array_filter($rank, fn($v) => $v > 0));
$pos = array_search($code, array_keys($rank), true) + 1;
$br1 = st_brackets($S, 'single');
$top = st_top_rate($S);
$low = 0;
foreach ($br1 as $b) if ($b[1] > 0) { $low = $b[1]; break; }
$nBr = count(array_filter($br1, fn($b) => $b[1] > 0));
$eff75 = number_format($r75['effective'] * 100, 2);
$std = $S['std'] ?? [];
$ex = $S['exemption'] ?? [];
$cr = $S['credits'] ?? [];
$k401 = state_calc($code, ['wages' => 75000, 'status' => 'single', 'pretax' => 10000]);
$save401 = $r75['tax'] - $k401['tax'];
$nb = $S['neighbors'] ?? [];
$nbTax = [];
foreach ($nb as $c) $nbTax[$c] = $rank[$c];
asort($nbTax);
$abbr = $code === 'DC' ? 'DC' : $code;

/* Title + description (keep 140–160 chars, unique per state via computed $75k figure). */
if ($isNone) {
  $P['title'] = "$name Paycheck Calculator $Y (No State Income Tax)";
  $cands = [
    "$name has no state income tax: on \$75,000 a single filer keeps about " . money($r75['net']) . " after federal tax and FICA. $Y paycheck calculator; sales tax {$S['salesTax']}%.",
    "$name has no state income tax. On \$75,000 a single filer keeps about " . money($r75['net']) . " after federal tax and FICA. Free $Y $name paycheck calculator.",
    "$name has no state income tax. On \$75,000 a single filer keeps about " . money($r75['net']) . " after federal tax and FICA. Free $Y $name take-home pay calculator.",
    "No state income tax in $name: on \$75,000 a single filer keeps about " . money($r75['net']) . " after federal tax and FICA. Free $Y paycheck calculator.",
  ];
} else {
  $P['title'] = "$name Income Tax Calculator $Y";
  $cands = [
    "Free $Y $name income tax calculator. A single filer earning \$75,000 pays about " . money($r75['tax']) . " in $abbr tax ($eff75% effective). See brackets, deductions and take-home pay.",
    "Free $Y $name income tax calculator. A single filer earning \$75,000 pays about " . money($r75['tax']) . " in $abbr tax ($eff75% effective). See brackets and take-home pay.",
    "$Y $name income tax calculator: a single filer earning \$75,000 pays about " . money($r75['tax']) . " in state tax ($eff75% effective). Brackets, deductions & take-home pay.",
    "$name income tax calculator $Y: \$75,000 single pays about " . money($r75['tax']) . " in $abbr tax ($eff75% effective). See brackets and take-home pay.",
  ];
}
usort($cands, fn($a, $b) => (mb_strlen($a) >= 140 && mb_strlen($a) <= 160 ? 0 : 1) <=> (mb_strlen($b) >= 140 && mb_strlen($b) <= 160 ? 0 : 1));
$P['description'] = $cands[0];
$P['scripts'] = ['/assets/js/tools/state-tax.js'];
$P['modified'] = date('Y-m-d', max(filemtime(__FILE__), filemtime(SITE_ROOT . '/app/data/states.json')));

/* WebApplication schema (tool_schema for the hub, then made state-specific). */
tool_schema('state-income-tax');
$i = count($P['schema']) - 1;
$P['schema'][$i]['name'] = "$name Income Tax Calculator";
$P['schema'][$i]['url'] = SITE_ORIGIN . $url;
$P['schema'][$i]['description'] = $isNone ? "Take-home pay calculator for $name, which has no state income tax." : "Estimate $name state income tax, federal tax, FICA and take-home pay.";

/* Lede */
if ($isNone) {
  $lede = "$name does not tax wages or salaries, so your paycheck only loses federal income tax and FICA. On \$75,000 a year, a single filer pays " . money($r75['fed']['tax']) . " of federal income tax and " . money($r75['fed']['fica']) . " of Social Security and Medicare, and takes home about <strong style=\"color:#fff\">" . money($r75['net']) . "</strong> — " . money($r75['net'] / 12) . " a month.";
} elseif ($isFlat) {
  $lede = "$name has a flat " . st_pct($top) . " income tax. A single filer earning \$75,000 in $Y owes about <strong style=\"color:#fff\">" . money($r75['tax']) . "</strong> in $name income tax — an effective rate of $eff75% — and takes home about " . money($r75['net']) . " after federal tax and FICA.";
} else {
  $lede = "$name taxes income in $nBr brackets from " . st_pct($low) . " to " . st_pct($top) . ". A single filer earning \$75,000 in $Y owes about <strong style=\"color:#fff\">" . money($r75['tax']) . "</strong> in $name income tax — an effective rate of $eff75% — and takes home about " . money($r75['net']) . " after federal tax and FICA.";
}
$badges = $isNone ? ['No state income tax', "$Y federal brackets", 'Take-home per paycheck', 'Compare neighbors'] : [($S['year'] == $Y ? "$Y $abbr rates" : "Latest {$S['year']} $abbr brackets"), 'State + federal + FICA', 'All filing statuses', 'Worked examples'];

/* Descriptions used in the prose */
$baseTxt = $S['base'] === 'federal_taxable' ? 'starts from your federal taxable income, so the federal standard deduction (' . money($std['single'] ?? 0) . ' single, ' . money($std['mfj'] ?? 0) . ' joint) is built in'
  : ($code === 'PA' ? 'taxes eight classes of income under its own rules rather than starting from your federal return' : 'starts from your federal adjusted gross income (AGI)');
$stdTxt = function () use ($S, $std, $code) {
  if ($S['base'] === 'federal_taxable') return '';
  if ($code === 'UT') return 'Instead of a standard deduction, Utah gives a nonrefundable taxpayer credit worth 6% of the federal standard deduction (plus $2,111 per dependent), which phases out as income rises.';
  if (($std['single'] ?? 0) == 0) return "There is no standard deduction in $S[name].";
  $t = ($code === 'SC' ? 'The South Carolina income-adjusted deduction' : 'The standard deduction') . ' is ' . money($std['single']) . ' for single filers and ' . money($std['mfj']) . ' for married couples filing jointly' . (isset($std['hoh']) ? ' (' . money($std['hoh']) . ' head of household)' : '') . '.';
  if (isset($S['stdPhase'])) $t .= ' It phases ' . (($S['stdPhase']['single'][2] ?? 0) > 0 ? 'down' : 'out') . ' between ' . money($S['stdPhase']['single'][0]) . ' and ' . money($S['stdPhase']['single'][1]) . ' of income for single filers.';
  return $t;
};
$exTxt = function () use ($S, $ex, $cr, $code) {
  $p = [];
  if (!empty($ex['personalByStatus'])) $p[] = 'a personal exemption of ' . money($ex['personalByStatus']['single']) . ' (' . money($ex['personalByStatus']['mfj']) . ' joint)';
  elseif (!empty($ex['personal'])) $p[] = 'a personal exemption of ' . money($ex['personal']) . ' per taxpayer';
  if (!empty($ex['dependent'])) $p[] = ($code === 'NM' ? 'a $4,000 deduction for each dependent after the first' : 'a dependent exemption of ' . money($ex['dependent']) . ($code === 'AL' ? ' (reduced at higher incomes)' : '') . ' per dependent');
  if (!empty($cr['personalCredit'])) $p[] = 'a personal exemption credit of ' . money($cr['personalCredit']) . ' per taxpayer';
  if (!empty($cr['dependentCredit'])) $p[] = 'a credit of ' . money($cr['dependentCredit']) . ' per dependent';
  return $p ? 'You also get ' . implode(', ', array_slice($p, 0, -1)) . (count($p) > 1 ? ' and ' : '') . end($p) . '.' : '';
};
$special = [];
if (($S['fedTaxDeduction'] ?? '') === 'full') $special[] = "Unusually, $name lets you deduct the federal income tax you paid, which lowers taxable income substantially — on \$75,000 that deduction is worth " . money($r75['fedTaxDed']) . '.';
if (($S['fedTaxDeduction'] ?? '') === 'mo') $special[] = "Missouri lets you deduct a percentage of your federal income tax (35% at low incomes, falling to 0% above \$125,000 of AGI); on \$75,000 that is " . money($r75['fedTaxDed']) . '.';
if (($S['fedTaxDeduction'] ?? '') === 'or') $special[] = "Oregon lets you subtract federal income tax up to about \$8,500, phased out between \$125,000 and \$145,000 of AGI (\$250,000–\$290,000 joint); on \$75,000 the subtraction is " . money($r75['fedTaxDed']) . '.';
if (($S['pretaxDeductible'] ?? true) === false) $special[] = 'Employee 401(k) and 403(b) contributions are <strong>not</strong> deductible for Pennsylvania tax, so the calculator ignores them for the state line.';
if (isset($S['recapture'])) $special[] = 'Once AGI passes ' . money($S['recapture']['start']) . ', New York phases out the benefit of the lower brackets, so the tax approaches your top marginal rate times all taxable income (simplified here over a ' . money($S['recapture']['span']) . ' range).';
if (isset($S['lowIncome'])) $special[] = 'If your net income is ' . money($S['lowIncome']['max']) . ' or less, a separate low-income table applies with a 0% bottom bracket.';
if (isset($S['addOver'])) $special[] = 'Income up to ' . money($S['addOver'][0]) . ' is tax-free; above that the tax is ' . money($S['addOver'][1]) . ' plus ' . st_pct($br1[count($br1) - 1][1]) . ' of the excess, so crossing the threshold adds a ' . money($S['addOver'][1]) . ' step.';
if (isset($S['exemptionPhase'])) $special[] = 'The personal exemption phases out between ' . money($S['exemptionPhase']['single'][0]) . ' and ' . money($S['exemptionPhase']['single'][1]) . ' of AGI for single filers.';
if (isset($S['exemptionCliff'])) $special[] = 'Exemptions are lost entirely once AGI exceeds ' . money($S['exemptionCliff']['single']) . ' (' . money($S['exemptionCliff']['mfj']) . ' joint).';
if (isset($S['allowancePhase'])) $special[] = 'The standard deduction and exemptions phase out between ' . money($S['allowancePhase'][0]) . ' and ' . money($S['allowancePhase'][1]) . ' of income.';
if (isset($S['creditCliff'])) $special[] = 'The exemption credit is not allowed once federal AGI exceeds ' . money($S['creditCliff']['single']) . ' (' . money($S['creditCliff']['mfj']) . ' joint).';
if (($S['special'] ?? '') === 'vt') $special[] = 'If federal AGI is over $150,000 you pay the greater of the regular tax or 3% of AGI.';
if (($S['special'] ?? '') === 'ct') $special[] = 'Above about $56,500 of AGI ($100,500 joint) the 2% bracket is phased out and recapture amounts are added; the calculator models both.';
if (($S['special'] ?? '') === 'md') $special[] = 'Personal exemptions are halved and then eliminated as AGI rises above $100,000 ($150,000 joint).';
if (($S['special'] ?? '') === 'oh') $special[] = 'Ohio’s exemption is $2,400 per person up to $40,000 of income, $2,150 up to $80,000 and $1,900 below $500,000.';

/* Formula line */
$formula = $isNone ? '' : (($code === 'UT') ? 'Federal AGI × ' . st_pct($top) . ' − taxpayer credit = Utah income tax'
  : (($S['pretaxDeductible'] ?? true) ? 'Federal AGI' : 'Gross compensation') . (($std['single'] ?? 0) || $S['base'] === 'federal_taxable' ? ' − ' . ($code === 'SC' ? 'SC income-adjusted deduction' : 'standard deduction') : '') .
    ((!empty($ex['personal']) || !empty($ex['dependent']) || !empty($ex['personalByStatus'])) ? ' − exemptions' : '') . (isset($S['fedTaxDeduction']) ? ' − federal tax deduction' : '') .
    ' = ' . $name . ' taxable income<br>' . ($isFlat ? 'Taxable income × ' . st_pct($top) : 'Tax from the ' . $name . ' brackets') . (($cr['personalCredit'] ?? 0) || ($cr['dependentCredit'] ?? 0) ? ' − credits' : '') . ' = ' . $name . ' income tax');

$mfjSame = json_encode(st_brackets($S, 'mfj')) === json_encode($br1);
$hohOwn = isset($S['brackets']['hoh']) && is_array($S['brackets']['hoh']);
$hohRef = isset($S['brackets']['hoh']) && is_string($S['brackets']['hoh']) ? $S['brackets']['hoh'] : null;
?>
<section class="page-hero"><div class="wrap">
  <?= breadcrumbs([['Calculators', '/calculators/'], ['State Income Tax', '/calculators/state-income-tax/'], [$name, $url]]) ?>
  <h1><?= e($isNone ? "$name Paycheck & Income Tax Calculator $Y" : "$name Income Tax Calculator $Y") ?></h1>
  <p class="lede"><?= $lede ?></p>
  <div class="badges"><?php foreach ($badges as $b) echo '<span class="badge">' . icon('check') . e($b) . '</span>'; ?></div>
</div></section>
<?= states_data_script() ?>
<?= state_form_html($code, "$name income tax calculator") ?>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
<?php if ($isNone): ?>
      <h2 id="overview">Does <?= e($name) ?> have a state income tax?</h2>
      <p>No. <?= e($S['notes']) ?></p>
      <p>That makes <?= e($name) ?> one of nine states — with <?= implode(', ', array_map($slink, array_values(array_diff(array_keys(array_filter($ST, fn($s) => $s['type'] === 'none')), [$code])))) ?> — where wages are free of state income tax. Your paycheck still has federal income tax withheld, plus Social Security (6.2% up to <?= money($TAX['years'][(string) $Y]['ssWageBase']) ?>) and Medicare (1.45%, plus 0.9% on high wages).</p>
      <div class="table-wrap"><table>
        <caption class="sr-only"><?= e($name) ?> taxes at a glance</caption>
        <tbody>
          <tr><td>State income tax on wages</td><td class="n"><strong>None</strong></td></tr>
          <tr><td>State sales tax rate</td><td class="n"><?= $S['salesTax'] ?>%<?= $S['salesTax'] ? ' plus local' : '' ?></td></tr>
          <tr><td>Local income taxes</td><td class="n"><?= str_starts_with($S['local'], 'No') ? 'None' : 'See below' ?></td></tr>
          <tr><td>Take-home on $75,000 (single)</td><td class="n"><?= money($r75['net']) ?></td></tr>
        </tbody>
      </table></div>

      <h2 id="examples">Take-home pay in <?= e($name) ?>: $50,000, $75,000 and $100,000</h2>
      <p>Because there is no state income tax, take-home pay in <?= e($name) ?> depends only on federal income tax and FICA. These <?= $Y ?> figures assume W-2 wages, the federal standard deduction and no pre-tax deductions.</p>
<?php else: ?>
      <h2 id="overview"><?= e($name) ?> income tax at a glance</h2>
      <p><?= e($S['notes']) ?></p>
      <div class="table-wrap"><table>
        <caption class="sr-only"><?= e($name) ?> income tax at a glance</caption>
        <tbody>
          <tr><td>Tax structure</td><td class="n"><?= $isFlat ? 'Flat ' . st_pct($top) : $nBr . ' brackets, ' . st_pct($low) . ' – ' . st_pct($top) ?></td></tr>
          <tr><td>Figures for tax year</td><td class="n"><?= $S['year'] ?></td></tr>
          <tr><td>Starting point</td><td class="n"><?= $S['base'] === 'federal_taxable' ? 'Federal taxable income' : ($code === 'PA' ? 'PA classes of income' : 'Federal AGI') ?></td></tr>
          <tr><td>Standard deduction (single / joint)</td><td class="n"><?= ($std['single'] ?? 0) ? money($std['single']) . ' / ' . money($std['mfj']) : ($code === 'UT' ? 'Credit instead' : 'None') ?></td></tr>
          <tr><td>Tax on $75,000 (single)</td><td class="n"><strong><?= money($r75['tax']) ?></strong> (<?= $eff75 ?>%)</td></tr>
          <tr><td>Rank at $75,000</td><td class="n"><?= $pos ?><?= ['th', 'st', 'nd', 'rd'][($pos % 100 >= 11 && $pos % 100 <= 13) ? 0 : min($pos % 10, 4) % 4] ?? 'th' ?> highest of <?= $taxedCount ?></td></tr>
          <tr><td>Local income taxes</td><td class="n"><?= str_starts_with($S['local'], 'No') ? 'None' : 'Yes — see below' ?></td></tr>
          <tr><td>State sales tax</td><td class="n"><?= $S['salesTax'] ?>%</td></tr>
        </tbody>
      </table></div>

      <h2 id="how-calculated">How <?= e($name) ?> calculates your income tax</h2>
      <p><?= e($name) ?> <?= $baseTxt ?>. <?= $stdTxt() ?> <?= $exTxt() ?></p>
<?php if ($special): ?>
      <ul>
<?php foreach ($special as $sp): ?>
        <li><?= $sp ?></li>
<?php endforeach; ?>
      </ul>
<?php endif; ?>
      <div class="formula"><?= $formula ?></div>

      <h2 id="brackets"><?= e($name) ?> income tax <?= $isFlat ? 'rate' : 'brackets' ?> (<?= $S['year'] ?>)</h2>
<?php if ($isFlat && $nBr === 1 && count($br1) === 1): ?>
      <p><?= e($name) ?> applies a single <?= st_pct($top) ?> rate to all taxable income for every filing status. There are no brackets to climb: each extra $1,000 of taxable income adds <?= money($top * 1000) ?> of state tax.</p>
<?php else: ?>
      <p><?= $mfjSame ? 'The same brackets apply to single filers and married couples filing jointly' . ($hohOwn ? '' : ' (and to heads of household)') . '.' : 'Married couples filing jointly get their own, wider brackets.' ?> Rates apply only to the slice of taxable income inside each bracket.</p>
      <h3 id="brackets-single"><?= $mfjSame ? 'All filers' : 'Single filers' ?></h3>
      <?= state_bracket_table($S, 'single') ?>
<?php if (!$mfjSame): ?>
      <h3 id="brackets-mfj">Married filing jointly</h3>
      <?= state_bracket_table($S, 'mfj') ?>
<?php endif; ?>
<?php if ($hohOwn): ?>
      <h3 id="brackets-hoh">Head of household</h3>
      <?= state_bracket_table($S, 'hoh') ?>
<?php elseif ($hohRef === 'mfj' && !$mfjSame): ?>
      <p>Heads of household use the married-filing-jointly brackets in <?= e($name) ?>.</p>
<?php endif; ?>
<?php endif; ?>

      <h2 id="deductions"><?= e($name) ?> standard deduction and exemptions</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Filing status</th><th class="n"><?= $code === 'SC' ? 'Income-adjusted deduction' : 'Standard deduction' ?></th><th class="n">Personal exemption</th><th class="n">Per dependent</th></tr></thead><tbody>
<?php foreach (['single', 'mfj', 'hoh'] as $s):
  $sd = $code === 'UT' ? 'Credit' : money($std[$s] ?? ($std['single'] ?? 0));
  $pe = !empty($ex['personalByStatus']) ? money($ex['personalByStatus'][$s]) : (!empty($ex['personal']) ? money($ex['personal'] * ($s === 'mfj' ? 2 : 1)) : (!empty($cr['personalCredit']) ? money($cr['personalCredit'] * ($s === 'mfj' ? 2 : 1)) . ' credit' : '—'));
  $de = $code === 'NM' ? '$4,000 (after the first)' : (!empty($ex['dependent']) ? money($ex['dependent']) : (!empty($cr['dependentCredit']) ? money($cr['dependentCredit']) . ' credit' : '—')); ?>
          <tr><td><?= status_label($s) ?></td><td class="n"><?= $sd ?></td><td class="n"><?= $pe ?></td><td class="n"><?= $de ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <p class="hint">Amounts before any income-based phase-outs. <?= $S['base'] === 'federal_taxable' ? 'Because ' . e($name) . ' starts from federal taxable income, these equal the ' . $Y . ' federal standard deduction.' : '' ?></p>

      <h2 id="examples"><?= e($name) ?> income tax on $50,000, $75,000 and $100,000</h2>
      <p>Estimated <?= $Y ?> tax for W-2 wages with the standard deduction, no children and no pre-tax deductions. Change any of these in the calculator above.</p>
<?php endif; ?>
      <div class="table-wrap"><table>
        <thead><tr><th>Wages</th><th>Filing status</th><?php if (!$isNone): ?><th class="n"><?= e($abbr) ?> tax</th><th class="n">Effective</th><?php endif; ?><th class="n">Federal tax</th><th class="n">FICA</th><th class="n">Take-home</th><th class="n">Monthly</th></tr></thead><tbody>
<?php foreach ($EX as [$amt, $s, $x]): ?>
          <tr><td><?= money($amt) ?></td><td><?= $s === 'mfj' ? 'Married jointly' : 'Single' ?></td><?php if (!$isNone): ?><td class="n"><strong><?= money($x['tax']) ?></strong></td><td class="n"><?= number_format($x['effective'] * 100, 2) ?>%</td><?php endif; ?><td class="n"><?= money($x['fed']['tax']) ?></td><td class="n"><?= money($x['fed']['fica']) ?></td><td class="n"><?= money($x['net']) ?></td><td class="n"><?= money($x['net'] / 12) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
<?php if (!$isNone): ?>

      <h2 id="step-by-step">Step by step: $75,000 single filer in <?= e($name) ?></h2>
      <ul>
        <li>Gross wages: <strong>$75,000</strong></li>
<?php if ($r75['std']): ?>        <li><?= $code === 'SC' ? 'Income-adjusted deduction' : 'Standard deduction' ?>: −<?= money($r75['std']) ?></li>
<?php endif; if ($r75['exemptions']): ?>        <li>Exemptions: −<?= money($r75['exemptions']) ?></li>
<?php endif; if ($r75['fedTaxDed']): ?>        <li>Federal income tax deduction: −<?= money($r75['fedTaxDed']) ?></li>
<?php endif; ?>
        <li><?= e($name) ?> taxable income: <strong><?= money($r75['taxable']) ?></strong></li>
<?php foreach ($r75['layers'] as $l): if ($l['amount'] <= 0) continue; ?>
        <li><?= st_pct($l['rate']) ?> on <?= money($l['amount']) ?> = <?= money($l['tax'], 2) ?></li>
<?php endforeach; ?>
<?php if (abs($r75['taxBefore'] - array_sum(array_column($r75['layers'], 'tax'))) > 0.5): ?>        <li>Adjustments (<?= isset($S['addOver']) ? 'base amount' : (isset($S['recapture']) ? 'recapture' : 'phase-outs and recapture') ?>): +<?= money($r75['taxBefore'] - array_sum(array_column($r75['layers'], 'tax'))) ?></li>
<?php endif; if ($r75['credits']): ?>        <li>Credits: −<?= money($r75['credits']) ?></li>
<?php endif; ?>
        <li><?= e($name) ?> income tax: <strong><?= money($r75['tax']) ?></strong> — <?= $eff75 ?>% of gross pay, with a marginal state rate of <?= st_pct($r75['marginal']) ?>.</li>
        <li>With <?= money($r75['fed']['tax']) ?> of federal income tax and <?= money($r75['fed']['fica']) ?> of FICA, total tax is <?= money($r75['total']) ?> and take-home pay is about <strong><?= money($r75['net']) ?></strong> (<?= money($r75['net'] / 26) ?> every two weeks).</li>
      </ul>
<?php endif; ?>

      <h2 id="local">Local income taxes in <?= e($name) ?></h2>
      <p><?= e($S['local']) ?></p>
<?php if (isset($S['localTax']['nyc'])): $nyc75 = state_calc($code, ['wages' => 75000, 'status' => 'single', 'nyc' => true]); ?>
      <p>For a single New York City resident earning $75,000, city tax adds about <strong><?= money($nyc75['nyc']) ?></strong> on top of <?= money($nyc75['tax']) ?> of state tax, for a combined <?= money($nyc75['nyc'] + $nyc75['tax']) ?> (<?= number_format(($nyc75['nyc'] + $nyc75['tax']) / 750, 2) ?>% of pay). Tick “I live in New York City” in the calculator to include it.</p>
      <div class="table-wrap"><table><thead><tr><th>NYC taxable income (single)</th><th class="n">NYC rate</th></tr></thead><tbody>
<?php $pv = 0; foreach ($S['localTax']['nyc']['brackets']['single'] as [$t, $rt]): ?>
        <tr><td><?= $t === null ? 'Over ' . money($pv) : money($pv) . ' – ' . money($t) ?></td><td class="n"><?= st_pct($rt, 3) ?></td></tr>
<?php $pv = $t; endforeach; ?>
      </tbody></table></div>
<?php elseif (!str_starts_with($S['local'], 'No')): ?>
      <p>To include a local tax, type its rate in the “Other local / city income tax rate” box in the calculator<?= ($S['localBase'] ?? '') === 'taxable' ? ' — it is applied to ' . e($name) . ' taxable income, the base used by county taxes' : '' ?>. At a 1% local rate, $75,000 of wages would add about <?= money((($S['localBase'] ?? '') === 'taxable' ? $r75['taxable'] : 75000) * 0.01) ?> a year.</p>
<?php endif; ?>

      <h2 id="sales-tax">Sales tax and other <?= e($name) ?> taxes</h2>
<?php if ($S['salesTax'] > 0): ?>
      <p>The <?= e($name) ?> state sales tax rate is <strong><?= $S['salesTax'] ?>%</strong><?= in_array($code, ['DC'], true) ? '' : ', and local governments may add their own rates on top' ?>. Spending $30,000 a year on taxable goods would cost roughly <?= money(30000 * $S['salesTax'] / 100) ?> in state sales tax alone<?= $isNone ? ' — a big part of how the state funds itself without an income tax' : '' ?>.</p>
<?php else: ?>
      <p><?= e($name) ?> has <strong>no statewide sales tax</strong><?= $code === 'AK' ? ', though many Alaska boroughs and cities levy local sales taxes' : '' ?>. <?= $isNone ? 'With neither a broad income tax nor a state sales tax, ' . e($name) . ' relies on other sources such as resource revenue and property taxes.' : 'It makes up the difference with its income tax, which is why the income tax rates are relatively high.' ?></p>
<?php endif; ?>

<?php if ($nb): $cheap = array_key_first($nbTax); $dear = array_key_last($nbTax); ?>
      <h2 id="neighbors">Compare <?= e($name) ?> with neighboring states</h2>
      <p>State income tax on $75,000 of wages for a single filer in <?= e($name) ?> and <?= count($nb) > 1 ? 'its neighbors' : 'its neighbor' ?>. <?php if ($nbTax[$cheap] < $r75['tax']): ?>Moving to <?= e($ST[$cheap]['name']) ?> would cut state income tax on this salary by about <?= money($r75['tax'] - $nbTax[$cheap]) ?> a year<?php else: ?><?= e($name) ?> is the cheapest in its area on this salary<?php endif; ?><?php if ($nbTax[$dear] > $r75['tax']): ?>, while <?= e($ST[$dear]['name']) ?> would cost about <?= money($nbTax[$dear] - $r75['tax']) ?> more<?php endif; ?>.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>State</th><th>Type</th><th class="n">Top rate</th><th class="n">Tax on $75k</th><th class="n">vs <?= e($abbr) ?></th></tr></thead><tbody>
          <tr><td><strong><?= e($name) ?></strong></td><td><?= state_type_label($S) ?></td><td class="n"><?= $isNone ? '—' : st_pct($top) ?></td><td class="n"><strong><?= money($r75['tax']) ?></strong></td><td class="n">—</td></tr>
<?php foreach ($nb as $c): $d = $rank[$c] - $r75['tax']; ?>
          <tr><td><?= $slink($c) ?></td><td><?= state_type_label($ST[$c]) ?></td><td class="n"><?= $ST[$c]['type'] === 'none' ? '—' : st_pct(st_top_rate($ST[$c])) ?></td><td class="n"><?= money($rank[$c]) ?></td><td class="n"><?= abs($d) < 1 ? 'same' : ($d > 0 ? '+' : '−') . money(abs($d)) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <p>If you live in one of these states and work in another, you generally file a non-resident return in the work state and claim a credit at home for the tax paid<?php $recip = ['PA' => 'NJ, MD, OH, IN, VA and WV', 'NJ' => 'Pennsylvania', 'MD' => 'DC, PA, VA and WV', 'VA' => 'DC, KY, MD, PA and WV', 'WV' => 'KY, MD, OH, PA and VA', 'OH' => 'IN, KY, MI, PA and WV', 'IN' => 'KY, MI, OH, PA and WI', 'KY' => 'IL, IN, MI, OH, VA, WV and WI', 'MI' => 'IL, IN, KY, MN, OH and WI', 'IL' => 'IA, KY, MI and WI', 'WI' => 'IL, IN, KY and MI', 'MN' => 'Michigan and North Dakota', 'ND' => 'Minnesota and Montana', 'MT' => 'North Dakota', 'IA' => 'Illinois', 'DC' => 'every state (non-residents never pay DC income tax)']; echo isset($recip[$code]) ? '. ' . e($name) . ' has reciprocity with ' . e($recip[$code]) . ', so residents of those states working here (and vice versa) usually pay only their home state' : ''; ?>.</p>
<?php endif; ?>

<?php if (!$isNone): ?>
      <h2 id="lower">How to lower your <?= e($name) ?> income tax</h2>
      <ul>
<?php if ($save401 > 0.5): ?>        <li><strong>Pre-tax retirement savings.</strong> Putting $10,000 into a traditional 401(k) on a $75,000 salary cuts <?= e($name) ?> tax by about <?= money($save401) ?> on top of the federal savings.</li>
<?php else: ?>        <li><strong>Know what isn’t deductible.</strong> <?= $code === 'PA' ? 'Pennsylvania does not exempt 401(k) deferrals, but most retirement distributions are not taxed later.' : 'Pre-tax contributions save little here at this income level because of how the deductions interact.' ?></li>
<?php endif; ?>
        <li><strong>Claim state credits.</strong> Check the <?= e($name) ?> return for earned-income, child, education and renter or property-tax credits that this estimate doesn’t include.</li>
        <li><strong>Watch residency and work location.</strong> Days worked in another state and the date you move in or out change how much each state can tax.</li>
        <li><strong>Time large income.</strong> Bonuses, stock sales and Roth conversions all land on your state return too<?= $top >= 0.08 ? ' — with a ' . st_pct($top) . ' top rate, timing can matter a lot' : '' ?>.</li>
      </ul>
<?php else: ?>
      <h2 id="moving">Moving to <?= e($name) ?>?</h2>
      <p>Becoming a <?= e($name) ?> resident ends state income tax on your wages from the day you move, but your former state can still tax income earned before the move and, in some cases, retirement or deferred compensation tied to work done there. Keep proof of your new domicile — a driver’s license, voter registration, lease or deed and where you spend your time. If you keep working remotely for an employer in a state with a “convenience of the employer” rule, such as New York, that state may still tax your wages.</p>
<?php endif; ?>
      <p>See all states side by side in the <a href="/calculators/state-income-tax/">state income tax calculator</a>, or check the federal side with the <a href="/calculators/federal-income-tax/">federal income tax calculator</a> and your per-check withholding in the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>.</p>

      <h2 id="sources">Sources and updates</h2>
      <p><?= $isNone ? '' : 'Rates, brackets and deductions are for tax year ' . $S['year'] . '. ' ?>Source: <a href="<?= e($S['source']) ?>" rel="nofollow noopener" target="_blank">official <?= e($name) ?> tax agency page</a>, cross-checked with the Tax Foundation’s <?= $Y ?> state income tax tables and <?= $Y ?> state legislation. Data last reviewed <?= fmt_date(json_decode(file_get_contents(SITE_ROOT . '/app/data/states.json'), true)['updated']) ?>.</p>

<?php
$faq = [];
if ($isNone) {
  $nbTaxed = array_values(array_filter($nb, fn($c) => $ST[$c]['type'] !== 'none'));
  $faq[] = ["Does $name have a state income tax?", "<p>No. " . e($S['notes']) . "</p>"];
  $faq[] = ["How much is \$75,000 after taxes in $name?", "<p>About " . money($r75['net']) . " a year (" . money($r75['net'] / 12) . " a month) for a single filer in $Y: " . money($r75['fed']['tax']) . " of federal income tax and " . money($r75['fed']['fica']) . " of Social Security and Medicare, and \$0 of state income tax. A married couple earning \$75,000 keeps about " . money($EX[3][2]['net']) . ".</p>"];
  $faq[] = ["What taxes do $name residents pay instead?", "<p>" . ($S['salesTax'] > 0 ? "$name charges a {$S['salesTax']}% state sales tax plus local rates" : "$name has no state sales tax, though local sales taxes may apply") . ", and residents pay local property taxes. Federal income tax and FICA apply exactly as in every other state.</p>"];
  if ($nbTaxed) $faq[] = ["How much do I save in $name versus neighboring states?", "<p>On \$75,000 of wages a single filer saves about " . implode(', ', array_map(fn($c) => money($rank[$c]) . ' compared with ' . $ST[$c]['name'], $nbTaxed)) . " in state income tax each year.</p>"];
  else $faq[] = ["Do I owe tax if I work in another state?", "<p>Usually yes — the state where you physically work can tax wages earned there, even though $name won’t. Since $name has no income tax there is no home-state credit to claim; you simply pay the work state.</p>"];
  $faq[] = ["Will $name withhold state tax from my paycheck?", "<p>No — employers in $name withhold only federal income tax and FICA" . ($code === 'WA' ? ', plus WA Cares and paid family leave premiums' : '') . ". If you work in another state, that state’s tax may be withheld instead.</p>"];
} else {
  $faq[] = ["What is the $name state income tax rate?", "<p>" . ($isFlat ? "$name has a flat " . st_pct($top) . " rate for $Y" . ($low < $top || count($br1) > 1 ? ' on income above a zero-rate band' : '') . "." : "$name has $nBr brackets ranging from " . st_pct($low) . " to " . st_pct($top) . " (figures for {$S['year']}). The top rate starts at " . money($br1[count($br1) - 2][0] ?? 0) . " of taxable income for single filers.") . " A single filer earning \$75,000 pays an effective rate of about $eff75%.</p>"];
  $faq[] = ["How much $name income tax do I pay on \$75,000?", "<p>About " . money($r75['tax']) . " for a single filer and " . money($EX[3][2]['tax']) . " for a married couple filing jointly, using the standard deduction. Including federal income tax and FICA, a single filer takes home about " . money($r75['net']) . " a year.</p>"];
  $faq[] = ["What is the $name standard deduction?", "<p>" . ($code === 'UT' ? 'Utah has no standard deduction; it gives a taxpayer credit of 6% of the federal standard deduction instead, phased out as income rises.' : (($std['single'] ?? 0) ? strip_tags($stdTxt()) : "$name has no standard deduction.") . ' ' . strip_tags($exTxt())) . "</p>"];
  $faq[] = ["Does $name have local income taxes?", "<p>" . e($S['local']) . "</p>"];
  $faq[] = ["Is $name a high-tax state?", "<p>On a \$75,000 salary $name ranks " . $pos . " of the $taxedCount jurisdictions that tax wages (1 = highest)" . ($pos <= 10 ? ', near the top of the list' : ($pos >= $taxedCount - 10 ? ', among the lowest' : ', in the middle of the pack')) . ". " . ($nb ? 'Among its neighbors, ' . $ST[array_key_first($nbTax)]['name'] . ' is cheapest at ' . money($nbTax[array_key_first($nbTax)]) . '.' : '') . "</p>"];
}
echo faq_block($faq, "$name income tax FAQ");
?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('state-income-tax', ['federal-income-tax', 'paycheck-calculator', 'salary-to-hourly', 'tax-refund-calculator', 'bonus-tax-calculator', 'overtime-calculator']) ?></div>
