<?php
/* State income tax engine (PHP mirror of assets/js/tools/state-tax.js — keep the two in sync).
 * Data: app/data/states.json via states(). Simplified W-2 model: wages + other ordinary income,
 * pre-tax 401(k), children, filing status; standard deduction only. */
defined('CPA') or exit;

function st_brackets(array $S, string $st): array {
  $b = $S['brackets'][$st] ?? null;
  if (is_string($b)) $b = $S['brackets'][$b] ?? null;
  return $b ?? ($S['brackets']['single'] ?? [[null, 0]]);
}

function st_bracket_tax(float $taxable, array $br): array {
  $prev = 0; $tax = 0; $marg = $br[0][1] ?? 0; $layers = [];
  $taxable = max(0, $taxable);
  foreach ($br as [$top, $rate]) {
    $top = $top ?? INF;
    $amt = max(0, min($taxable, $top) - $prev);
    $layers[] = ['from' => $prev, 'to' => $top, 'rate' => $rate, 'amount' => $amt, 'tax' => $amt * $rate];
    $tax += $amt * $rate;
    if ($taxable > $prev) $marg = $rate;
    $prev = $top;
  }
  return ['tax' => $tax, 'marginal' => $marg, 'layers' => $layers];
}

/* Federal part: mirrors CPA.estimate() for wages + other income, pre-tax deferrals, kids (CTC), standard deduction. */
function st_federal(float $wages, float $other, string $st, int $kids, float $pretax, int $year = TAX_YEAR): array {
  global $TAX;
  $y = $TAX['years'][(string) $year];
  $gross = $wages + $other;
  $agi = max(0, $gross - $pretax);
  $std = $y['std'][$st];
  $taxable = max(0, $agi - $std);
  $f = fed_tax($taxable, $st, $year);
  $ctc = $kids ? max(0, $kids * $y['ctc']['amount'] - ceil(max(0, $agi - $y['ctc']['phaseStart'][$st]) / 1000) * 50) : 0;
  $it = max(0, $f['tax'] - $ctc);
  $ss = min(max(0, $wages), $y['ssWageBase']) * 0.062;
  $med = max(0, $wages) * 0.0145 + max(0, $wages - $y['addlMedicare'][$st]) * 0.009;
  return ['gross' => $gross, 'agi' => $agi, 'std' => $std, 'taxable' => $taxable, 'tax' => $it, 'marginal' => $f['marginal'], 'fica' => $ss + $med, 'ss' => $ss, 'medicare' => $med];
}

function st_lin(float $v, float $x, float $a, float $b, float $min = 0): float {
  if ($x <= $a) return $v;
  if ($x >= $b) return $min;
  return $v - ($v - $min) * ($x - $a) / ($b - $a);
}

function st_ct_extra(float $agi, string $st): float {
  $c = fn($x, $per) => (int) ceil($x / $per);
  if ($st === 'mfj') {
    $ph = $agi > 100500 ? min(20000, 2000 * $c($agi - 100500, 5000)) * 0.025 : 0;
    $r1 = $agi > 210000 ? min(500, 50 * $c($agi - 210000, 10000)) : 0;
    $r2 = $agi > 400000 ? min(6300, min(5400, 180 * $c($agi - 400000, 10000)) + ($agi > 1000000 ? 100 * $c($agi - 1000000, 10000) : 0)) : 0;
  } elseif ($st === 'hoh') {
    $ph = $agi > 78500 ? min(16000, 1600 * $c($agi - 78500, 5000)) * 0.025 : 0;
    $r1 = $agi > 168000 ? min(400, 40 * $c($agi - 168000, 8000)) : 0;
    $r2 = $agi > 320000 ? min(5040, min(4200, 140 * $c($agi - 320000, 8000)) + ($agi > 800000 ? 80 * $c($agi - 800000, 8000) : 0)) : 0;
  } else {
    $start = $st === 'mfs' ? 50250 : 56500; $step = $st === 'mfs' ? 2500 : 5000;
    $ph = $agi > $start ? min(10000, 1000 * $c($agi - $start, $step)) * 0.025 : 0;
    $r1 = $agi > 105000 ? min(250, 25 * $c($agi - 105000, 5000)) : 0;
    $r2 = $agi > 200000 ? min(3150, 90 * $c(min($agi, 500000) - 200000, 5000) + ($agi > 500000 ? 50 * $c($agi - 500000, 5000) : 0)) : 0;
  }
  return $ph + $r1 + $r2;
}

/* $o: wages, otherIncome, status, kids, pretax, nyc, yonkers, localRate (decimal). */
function state_calc(string $code, array $o): array {
  $S = states()[$code];
  $wages = (float) ($o['wages'] ?? 0); $other = (float) ($o['otherIncome'] ?? 0);
  $st = $o['status'] ?? 'single'; $kids = (int) ($o['kids'] ?? 0); $pretax = (float) ($o['pretax'] ?? 0);
  $fed = st_federal($wages, $other, $st, $kids, $pretax);
  $gross = $wages + $other;
  $fedAgi = $fed['agi'];
  $agi = max(0, $gross - (($S['pretaxDeductible'] ?? true) ? $pretax : 0));
  $sp = $S['special'] ?? '';
  $r = ['code' => $code, 'gross' => $gross, 'stateAgi' => $agi, 'std' => 0, 'exemptions' => 0, 'fedTaxDed' => 0, 'taxable' => 0,
        'taxBefore' => 0, 'credits' => 0, 'tax' => 0, 'marginal' => 0, 'topRate' => 0, 'layers' => [], 'nyc' => 0, 'yonkers' => 0, 'local' => 0, 'fed' => $fed];
  if ($S['type'] !== 'none') {
    $persons = $st === 'mfj' ? 2 : 1;
    // Standard deduction (or SC income-adjusted deduction)
    $std = $S['std'][$st] ?? ($S['std']['single'] ?? 0);
    if (isset($S['stdPhase'][$st])) { [$a, $b, $mn] = $S['stdPhase'][$st]; $std = st_lin($std, $agi, $a, $b, $mn); }
    if ($sp === 'mn') {
      [$t1, $t2] = $st === 'mfs' ? [122200, 168900] : [244400, 337800];
      $std -= min(0.8 * $std, 0.03 * max(0, min($agi, $t2) - $t1) + 0.10 * max(0, $agi - $t2));
    }
    // Exemptions
    $ex = $S['exemption'] ?? [];
    $pers = isset($ex['personalByStatus'][$st]) ? $ex['personalByStatus'][$st] : ($ex['personal'] ?? 0) * $persons;
    $dep = ($ex['dependent'] ?? 0) * $kids;
    if ($sp === 'al') $dep = ($agi <= 50000 ? 1000 : ($agi <= 100000 ? 500 : 300)) * $kids;
    if ($sp === 'oh') { $per = $agi <= 40000 ? 2400 : ($agi <= 80000 ? 2150 : ($agi < 500000 ? 1900 : 0)); $pers = $per * $persons; $dep = $per * $kids; }
    if ($sp === 'nm') $dep = 4000 * max(0, $kids - 1);
    if ($sp === 'md') {
      $f = in_array($st, ['mfj', 'hoh'], true) ? ($agi <= 150000 ? 1 : ($agi <= 175000 ? .5 : ($agi <= 200000 ? .25 : 0)))
                                               : ($agi <= 100000 ? 1 : ($agi <= 125000 ? .5 : ($agi <= 150000 ? .25 : 0)));
      $pers *= $f; $dep *= $f;
    }
    if (isset($S['exemptionPhase'][$st])) { [$a, $b] = $S['exemptionPhase'][$st]; $pers = st_lin($pers, $agi, $a, $b); }
    if (isset($S['exemptionCliff'][$st]) && $agi > $S['exemptionCliff'][$st]) { $pers = 0; $dep = 0; }
    if (isset($S['allowancePhase'])) { [$a, $b] = $S['allowancePhase']; $k = st_lin(1, $agi, $a, $b); $std *= $k; $pers *= $k; $dep *= $k; }
    // Federal income tax deduction (AL full; MO partial; OR capped)
    $fd = 0; $fit = $fed['tax'];
    $mode = $S['fedTaxDeduction'] ?? '';
    if ($mode === 'full') $fd = $fit;
    elseif ($mode === 'mo') { $p = $agi <= 25000 ? .35 : ($agi <= 50000 ? .25 : ($agi <= 100000 ? .15 : ($agi <= 125000 ? .05 : 0))); $fd = min($fit * $p, $st === 'mfj' ? 10000 : 5000); }
    elseif ($mode === 'or') {
      $th = $st === 'mfj' ? [250000, 260000, 270000, 280000, 290000] : [125000, 130000, 135000, 140000, 145000];
      $k = $fedAgi < $th[0] ? 1 : ($fedAgi < $th[1] ? .8 : ($fedAgi < $th[2] ? .6 : ($fedAgi < $th[3] ? .4 : ($fedAgi < $th[4] ? .2 : 0))));
      $fd = min($fit, 8500 * $k);
    }
    $taxable = max(0, $agi - $std - $pers - $dep - $fd);
    // Tax
    $br = st_brackets($S, $st);
    $use = (isset($S['lowIncome']) && $taxable <= $S['lowIncome']['max']) ? $S['lowIncome']['brackets'] : $br;
    $bt = st_bracket_tax($taxable, $use);
    $tax = $bt['tax'];
    if (isset($S['addOver']) && $taxable > $S['addOver'][0]) $tax += $S['addOver'][1];
    if ($sp === 'ct') $tax += st_ct_extra($agi, $st);
    if (isset($S['recapture']) && $agi > $S['recapture']['start']) {
      $tax += max(0, $taxable * $bt['marginal'] - $tax) * min(1, ($agi - $S['recapture']['start']) / $S['recapture']['span']);
    }
    if ($sp === 'vt' && $fedAgi > 150000) $tax = max($tax, 0.03 * $fedAgi);
    // Credits
    $cr = 0;
    if (isset($S['credits'])) {
      $pc = $S['credits']['personalCredit'] ?? 0; $dc = $S['credits']['dependentCredit'] ?? 0;
      if ($sp === 'ca') {
        $th = $st === 'mfj' ? 504411 : ($st === 'hoh' ? 378310 : 252203);
        $cut = $fedAgi > $th ? 6 * ceil(($fedAgi - $th) / 2500) : 0;
        $cr = max(0, $pc - $cut) * $persons + max(0, $dc - $cut) * $kids;
      } else $cr = $pc * $persons + $dc * $kids;
      if (isset($S['creditCliff'][$st]) && $fedAgi > $S['creditCliff'][$st]) $cr = 0;
    }
    if ($sp === 'ut') {
      $u = $S['utCredit'];
      $cr += max(0, $u['rate'] * (($u['fedStd'][$st] ?? $u['fedStd']['single']) + $u['depExemption'] * $kids) - $u['phaseRate'] * max(0, $agi - $u['phaseStart'][$st]));
    }
    $r['std'] = $std; $r['exemptions'] = $pers + $dep; $r['fedTaxDed'] = $fd; $r['taxable'] = $taxable;
    $r['taxBefore'] = $tax; $r['credits'] = min($cr, $tax); $r['tax'] = max(0, $tax - $cr);
    $r['marginal'] = $bt['marginal']; $r['topRate'] = end($br)[1]; $r['layers'] = $bt['layers'];
    // Local
    if (!empty($o['nyc']) && isset($S['localTax']['nyc'])) {
      $nb = $S['localTax']['nyc']['brackets'][$st] ?? $S['localTax']['nyc']['brackets']['single'];
      $r['nyc'] = st_bracket_tax($taxable, $nb)['tax'];
    }
    if (!empty($o['yonkers']) && isset($S['localTax']['yonkers'])) $r['yonkers'] = $r['tax'] * $S['localTax']['yonkers']['pctOfState'];
  }
  $lr = (float) ($o['localRate'] ?? 0);
  if ($lr > 0) $r['local'] = (($S['localBase'] ?? '') === 'taxable' ? $r['taxable'] : $gross) * $lr;
  $r['localTotal'] = $r['nyc'] + $r['yonkers'] + $r['local'];
  $r['effective'] = $gross > 0 ? $r['tax'] / $gross : 0;
  $r['total'] = $fed['tax'] + $fed['fica'] + $r['tax'] + $r['localTotal'];
  $r['net'] = $gross - $r['total'] - $pretax;
  return $r;
}

/* Convenience: state tax only (single W-2 earner, no extras). */
function state_tax_on(string $code, float $wages, string $status = 'single', int $kids = 0): float {
  return state_calc($code, ['wages' => $wages, 'status' => $status, 'kids' => $kids])['tax'];
}

function st_pct(float $r, int $dp = 2): string { return rtrim(rtrim(number_format($r * 100, $dp), '0'), '.') . '%'; }

/* Bracket table for one state/status. */
function state_bracket_table(array $S, string $st): string {
  $br = st_brackets($S, $st);
  $h = '<div class="table-wrap"><table><caption class="sr-only">' . e($S['name']) . ' ' . $S['year'] . ' income tax brackets — ' . e(status_label($st)) . '</caption><thead><tr><th>Rate</th><th>Taxable income</th><th class="n">Tax owed</th></tr></thead><tbody>';
  $prev = 0; $cum = 0;
  foreach ($br as [$top, $rate]) {
    $range = $top === null ? 'Over ' . money($prev) : ($prev === 0 ? '$0' : money($prev + 1)) . ' – ' . money($top);
    $owed = $prev === 0 ? st_pct($rate) . ' of taxable income' : money($cum) . ' + ' . st_pct($rate) . ' over ' . money($prev);
    $h .= '<tr><td><b>' . st_pct($rate) . '</b></td><td>' . $range . '</td><td class="n">' . $owed . '</td></tr>';
    if ($top !== null) { $cum += ($top - $prev) * $rate; $prev = $top; }
  }
  return $h . '</tbody></table></div>';
}

/* Inline the data for state-tax.js. */
function states_data_script(): string {
  return '<script>window.STATES=' . json_encode(states(), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . ';</script>';
}

/* Shared calculator markup for the hub and the 51 state pages (#state-form, wired by state-tax.js). */
function state_form_html(string $code, string $aria): string {
  $S = states()[$code];
  ob_start(); ?>
<section class="tool" aria-label="<?= e($aria) ?>">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="state-form" novalidate>
        <div class="grid-2">
          <div class="field"><label for="f-state">State</label><select id="f-state" name="state">
<?php foreach (states() as $c => $s): ?>
            <option value="<?= $c ?>"<?= $c === $code ? ' selected' : '' ?>><?= e($s['name']) ?></option>
<?php endforeach; ?>
          </select><span class="hint"><a href="/calculators/state-income-tax/<?= e($S['slug']) ?>/" data-state-link><?= e($S['name']) ?> income tax guide →</a></span></div>
          <div class="field"><label for="f-kids">Children under 17</label><select id="f-kids" name="kids"><?php for ($i = 0; $i <= 6; $i++) echo "<option value=\"$i\">$i</option>"; ?></select></div>
        </div>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Income</legend>
          <?= money_field('wages', 'Wages, salary & tips (W-2)', 75000, 'Your expected annual gross pay before any deductions, including bonuses.') ?>
          <input type="range" min="0" max="500000" step="1000" data-range-for="wages" aria-label="Wages slider">
          <div class="grid-2">
            <?= money_field('otherIncome', 'Other taxable income', '', 'Interest, ordinary dividends, unemployment, IRA distributions, rental or other ordinary income.') ?>
            <?= money_field('pretax', 'Pre-tax 401(k) / 403(b)', '', 'Traditional (not Roth) payroll contributions. Deductible for federal tax and in every state except Pennsylvania.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Local taxes</legend>
          <div data-nyc<?= isset($S['localTax']) ? '' : ' hidden' ?>>
            <label class="check"><input type="checkbox" name="nyc"> I live in New York City (add NYC resident income tax)</label>
            <label class="check"><input type="checkbox" name="yonkers"> I live in Yonkers (add 16.75% resident surcharge)</label>
          </div>
          <?= money_field('localRate', 'Other local / city income tax rate', '', 'Optional. For example a Pennsylvania EIT, Ohio municipal tax, Michigan city tax, Kentucky occupational tax, or a Maryland or Indiana county rate.', 'Optional — applied to gross income (to taxable income for Maryland and Indiana counties).', '%') ?>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Estimated <span data-out="stateName"><?= e($S['name']) ?></span> income tax</div>
          <div class="res-big" data-out="tax">$0</div>
          <div class="res-sub"><span data-out="summary">—</span></div>
          <div class="kpis">
            <div class="kpi"><small>Effective state rate</small><b data-out="eff">0%</b></div>
            <div class="kpi"><small>Your state bracket</small><b data-out="marg">0%</b></div>
            <div class="kpi"><small>Top state rate</small><b data-out="top">0%</b></div>
            <div class="kpi"><small>Total tax (all levels)</small><b data-out="total">$0</b></div>
          </div>
          <div class="kpis">
            <div class="kpi"><small>Take-home / year</small><b data-out="netYear">$0</b></div>
            <div class="kpi"><small>Per month</small><b data-out="netMonth">$0</b></div>
            <div class="kpi"><small>Every two weeks</small><b data-out="netBiweekly">$0</b></div>
            <div class="kpi"><small>Federal income tax</small><b data-out="fedTax">$0</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your income goes"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <div class="res-label" style="margin-bottom:6px">Your income across the state brackets</div>
          <div data-brackets></div>
          <p class="note">Estimate for W-2 income using the standard deduction. Excludes state credits not listed, itemized deductions and payroll taxes such as SDI or paid-leave premiums. See <a href="/our-methodology/">our methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>
<?php
  return ob_get_clean();
}

/* $75,000 single tax for every state, sorted high → low, with rank. */
function state_rank_75k(): array {
  static $r;
  if ($r) return $r;
  $r = [];
  foreach (states() as $c => $S) $r[$c] = state_tax_on($c, 75000);
  arsort($r);
  return $r;
}

function state_type_label(array $S): string {
  return ['none' => 'No income tax', 'flat' => 'Flat', 'progressive' => 'Graduated'][$S['type']] ?? $S['type'];
}

function st_top_rate(array $S, string $st = 'single'): float { $b = st_brackets($S, $st); return $S['type'] === 'none' ? 0 : (float) $b[count($b) - 1][1]; }
