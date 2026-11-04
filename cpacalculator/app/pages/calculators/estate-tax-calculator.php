<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$exempt = $y['estate']['exemption'];
$exM = '$' . rtrim(rtrim(number_format($exempt / 1e6, 2), '0'), '.') . 'M';
$P['title'] = "Estate Tax Calculator $Y — $exM Federal Exemption | CPA Calculator";
$P['description'] = "Free $Y estate tax calculator. Estimate federal estate tax on your taxable estate under the " . money($exempt) . " exemption, portability (DSUE) and the 40% top rate.";
$P['scripts'] = ['/assets/js/tools/estate-tax-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Unified transfer tax (IRC §2001(c)) from tax.json estate.brackets. */
function et_unified_tax(float $amt, array $br): float {
  $tax = 0; $prev = 0;
  foreach ($br as [$top, $rate]) {
    $top = $top ?? INF;
    if ($amt > $prev) $tax += (min($amt, $top) - $prev) * $rate;
    $prev = $top;
  }
  return $tax;
}
function et_estate(float $gross, float $deductions, float $gifts, float $dsue = 0): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $br = $y['estate']['brackets'];
  $taxableEstate = max(0, $gross - $deductions);
  $base = $taxableEstate + $gifts;
  $tentative = et_unified_tax($base, $br);
  $credit = et_unified_tax($y['estate']['exemption'] + $dsue, $br);
  $tax = max(0, $tentative - $credit);
  return compact('taxableEstate', 'base', 'tentative', 'credit', 'tax') + ['eff' => $gross > 0 ? $tax / $gross : 0];
}
$exAssets = ['Home' => 1200000, 'Investment accounts' => 8000000, 'Retirement accounts' => 3000000, 'Life insurance (owned by decedent)' => 2000000, 'Business interest' => 4000000, 'Other property' => 300000];
$exGross = array_sum($exAssets);
$exDebts = 500000; $exExp = 200000; $exGifts = 1000000;
$ex = et_estate($exGross, $exDebts + $exExp, $exGifts);
$exSp = et_estate($exGross, $exDebts + $exExp, $exGifts, $exempt); // same estate if a full DSUE were available
$creditBase = et_unified_tax($exempt, $y['estate']['brackets']);

echo tool_hero('estate-tax-calculator', "Estate Tax Calculator $Y",
  "Estimate the federal estate tax on what you leave behind. List your assets, subtract debts, expenses and bequests to a spouse or charity, add back lifetime taxable gifts, and see your taxable estate, the tentative tax on the unified rate schedule, the " . money($exempt) . " exemption credit and what — if anything — is owed.",
  [money($exempt) . " exemption ($Y)", 'Portability / DSUE', 'Unified 18%–40% rate schedule', 'Marital & charitable deductions']);
?>
<section class="tool" aria-label="Estate tax calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="estate-form" novalidate>
        <div class="field"><label for="f-year">Year of death</label><select id="f-year" name="year">
          <?php $yrs = array_keys($TAX['years']); rsort($yrs); foreach ($yrs as $yr) echo '<option value="' . $yr . '"' . ((int) $yr === $Y ? ' selected' : '') . '>' . $yr . ' — exemption ' . money($TAX['years'][$yr]['estate']['exemption']) . '</option>'; ?>
        </select></div>
        <fieldset class="fieldset"><legend>Gross estate (fair market value)</legend>
          <div class="grid-2">
            <?= money_field('home', 'Home & other real estate', 1200000, 'Full market value of real estate you own. For property owned jointly with a spouse, generally half is included.') ?>
            <?= money_field('invest', 'Bank & investment accounts', 8000000, 'Checking, savings, brokerage accounts, stocks, bonds, mutual funds, crypto.') ?>
          </div>
          <div class="grid-2">
            <?= money_field('retire', 'Retirement accounts', 3000000, '401(k), IRA, Roth IRA, pensions with a survivor value. Included at full balance even though heirs may also owe income tax on withdrawals.') ?>
            <?= money_field('life', 'Life insurance you own', 2000000, 'Death benefit of policies you owned or controlled. Policies held by an irrevocable life insurance trust (ILIT) for over three years are excluded.') ?>
          </div>
          <div class="grid-2">
            <?= money_field('biz', 'Business interests', 4000000, 'Value of a business, partnership or LLC interest. Valuation discounts and special-use valuation can reduce this — get an appraisal.') ?>
            <?= money_field('other', 'Other assets', 300000, 'Vehicles, art, jewelry, collectibles, money owed to you, other property.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Deductions</legend>
          <div class="grid-2">
            <?= money_field('debts', 'Debts & mortgages', 500000, 'Mortgages, loans, credit cards and taxes owed at death.') ?>
            <?= money_field('expenses', 'Funeral & administration costs', 200000, 'Funeral, executor commissions, attorney, appraisal and probate fees.') ?>
          </div>
          <label class="check"><input type="checkbox" name="allSpouse" value="1"> Everything (after charity) passes to my US-citizen spouse</label>
          <div class="grid-2">
            <?= money_field('marital', 'Marital deduction (to US-citizen spouse)', '', 'Property passing outright to a surviving spouse who is a US citizen, or to a QTIP trust. A non-citizen spouse requires a qualified domestic trust (QDOT).') ?>
            <?= money_field('charity', 'Charitable bequests', '', 'Gifts in your will or beneficiary designations to qualified charities — fully deductible.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Lifetime gifts &amp; portability</legend>
          <div class="grid-2">
            <?= money_field('gifts', 'Adjusted taxable gifts', 1000000, 'Taxable gifts made after 1976 (amounts above the annual exclusion reported on Form 709), not already included in the estate.') ?>
            <?= money_field('dsue', 'DSUE from a deceased spouse', '', 'Deceased spousal unused exclusion — the exemption your last deceased spouse didn’t use, if their executor elected portability on a Form 706.') ?>
          </div>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Federal estate tax</div>
          <div class="res-big" data-out="tax">$0</div>
          <div class="res-sub" data-out="summary">—</div>
          <div class="kpis">
            <div class="kpi"><small>Gross estate</small><b data-out="gross">$0</b></div>
            <div class="kpi"><small>Taxable estate</small><b data-out="taxable">$0</b></div>
            <div class="kpi"><small>Effective rate</small><b data-out="eff">0%</b></div>
            <div class="kpi"><small data-out="kpi4l">Exemption available</small><b data-out="kpi4">$0</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where the gross estate goes"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note">Federal estate tax only; ignores state estate/inheritance tax, gift tax paid on prior gifts, GST tax and valuation discounts. Not legal advice. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-estate-tax-works">How the federal estate tax works</h2>
      <p>The federal estate tax is a tax on the transfer of property at death. It is calculated on the <strong>taxable estate</strong> — everything the person owned or controlled, minus debts, expenses and bequests to a spouse or charity — and is paid by the estate before heirs receive their shares. Each person has a lifetime exemption, called the basic exclusion amount, that shelters transfers up to that level from tax.</p>
      <p>The <strong>One Big Beautiful Bill Act (OBBBA)</strong>, signed in July 2025, set the exemption at <strong>$15 million per person for 2026</strong> — <?= money($exempt * 2) ?> for a married couple using portability — and indexes it for inflation each year after 2026. That replaced the scheduled “sunset” that would have roughly halved the exemption. The top rate stays at 40%. As a result, only a very small share of estates owe any federal estate tax, though many more owe state estate or inheritance tax.</p>

      <h2 id="how-to-use">How to use the estate tax calculator</h2>
      <ol>
        <li><strong>List assets at fair market value</strong> on the date of death: real estate, investments, retirement accounts, life insurance you own, business interests and other property.</li>
        <li><strong>Subtract debts and expenses</strong> — mortgages, loans, funeral costs, executor and legal fees.</li>
        <li><strong>Add the marital and charitable deductions.</strong> Everything left to a US-citizen spouse or a qualified charity is deductible without limit. Tick the box to leave the entire net estate to a spouse.</li>
        <li><strong>Add adjusted taxable gifts</strong> — taxable lifetime gifts (above the annual exclusion) reported on Form 709. Our <a href="/calculators/gift-tax-calculator/">gift tax calculator</a> works these out.</li>
        <li><strong>Enter any DSUE</strong> inherited from a deceased spouse whose executor elected portability.</li>
      </ol>

      <h2 id="formula">Estate tax formula</h2>
      <div class="formula">Gross estate − debts &amp; expenses − marital − charitable = Taxable estate<br>Tax base = taxable estate + adjusted taxable gifts<br>Tentative tax = unified rate schedule (18%–40%) on tax base<br>Applicable credit = unified tax on (exemption + DSUE)<br>Estate tax = tentative tax − applicable credit (not below $0)</div>
      <p>For <?= $Y ?>, the applicable credit on a <?= money($exempt) ?> exemption is <?= money($creditBase) ?>. Because the first $1 million of the rate schedule is fully absorbed by the credit, every dollar above the exemption is effectively taxed at 40%.</p>

      <h2 id="rates">Unified estate and gift tax rates</h2>
      <div class="table-wrap"><table><thead><tr><th>Taxable amount</th><th class="n">Rate</th><th class="n">Tax on amounts below</th></tr></thead><tbody>
      <?php $prev = 0; $cum = 0; foreach ($y['estate']['brackets'] as [$top, $rate]): ?>
        <tr><td><?= $top === null ? 'Over ' . money($prev) : money($prev) . ' – ' . money($top) ?></td><td class="n"><?= round($rate * 100) ?>%</td><td class="n"><?= money($cum) ?></td></tr>
      <?php if ($top !== null) { $cum += ($top - $prev) * $rate; $prev = $top; } endforeach; ?>
      </tbody></table></div>

      <h2 id="example">Worked example</h2>
      <p>An unmarried person dies in <?= $Y ?> owning <?= money($exGross) ?> of assets, owing <?= money($exDebts) ?>, with <?= money($exExp) ?> of funeral and administration costs and <?= money($exGifts) ?> of taxable lifetime gifts:</p>
      <div class="table-wrap"><table><tbody>
        <?php foreach ($exAssets as $k => $v): ?><tr><td><?= e($k) ?></td><td class="n"><?= money($v) ?></td></tr><?php endforeach; ?>
        <tr><td><strong>Gross estate</strong></td><td class="n"><strong><?= money($exGross) ?></strong></td></tr>
        <tr><td>Debts, funeral &amp; administration</td><td class="n">−<?= money($exDebts + $exExp) ?></td></tr>
        <tr><td>Taxable estate</td><td class="n"><?= money($ex['taxableEstate']) ?></td></tr>
        <tr><td>+ Adjusted taxable gifts</td><td class="n"><?= money($exGifts) ?></td></tr>
        <tr><td>Tax base</td><td class="n"><?= money($ex['base']) ?></td></tr>
        <tr><td>Tentative tax</td><td class="n"><?= money($ex['tentative']) ?></td></tr>
        <tr><td>Applicable credit (<?= money($exempt) ?> exemption)</td><td class="n">−<?= money($ex['credit']) ?></td></tr>
        <tr><td><strong>Federal estate tax</strong></td><td class="n"><strong><?= money($ex['tax']) ?></strong></td></tr>
        <tr><td>Effective rate on gross estate</td><td class="n"><?= number_format($ex['eff'] * 100, 1) ?>%</td></tr>
      </tbody></table></div>
      <p>The tax equals 40% of the <?= money($ex['base'] - $exempt) ?> by which the tax base exceeds the exemption. Had this person been a surviving spouse with a full <?= money($exempt) ?> DSUE from a late husband or wife, the combined <?= money($exempt * 2) ?> of exemption would reduce the tax to <?= money($exSp['tax']) ?>.</p>

      <h2 id="portability">Portability and the marital deduction</h2>
      <p>Married couples have two powerful tools. The <strong>unlimited marital deduction</strong> means nothing is taxed at the first death if everything passes to a US-citizen spouse. <strong>Portability</strong> then lets the surviving spouse add the deceased spouse’s unused exemption (DSUE) to their own. To claim it, the executor must file a Form 706 and elect portability — even when no tax is due. Estates not otherwise required to file can make a late election up to five years after death under Rev. Proc. 2022-32. DSUE comes only from the <em>last</em> deceased spouse, and unlike the basic exclusion it is not indexed for inflation.</p>

      <h2 id="filing">Form 706 filing and deadlines</h2>
      <p>An estate must file Form 706 if the gross estate plus adjusted taxable gifts exceeds the basic exclusion amount for the year of death. It is due <strong>nine months after the date of death</strong>, with an automatic six-month extension to file available on Form 4768 (the tax itself is still due at nine months). Heirs generally receive a stepped-up cost basis equal to the date-of-death value, which can wipe out built-in <a href="/calculators/capital-gains-tax/">capital gains</a> — one reason large estates weigh lifetime gifts against holding assets until death.</p>

      <h2 id="state">State estate and inheritance taxes</h2>
      <p>State taxes often matter more than the federal tax, because state exemptions are usually much lower. As of 2026:</p>
      <ul>
        <li><strong>Estate taxes:</strong> Connecticut, Hawaii, Illinois, Maine, Maryland, Massachusetts, Minnesota, New York, Oregon, Rhode Island, Vermont, Washington and the District of Columbia. Exemptions range from about $1 million (Oregon) to the federal amount (Connecticut).</li>
        <li><strong>Inheritance taxes</strong> (paid by heirs, with close relatives often exempt): Kentucky, Maryland, Nebraska, New Jersey and Pennsylvania. Iowa’s inheritance tax ended for deaths after 2024.</li>
      </ul>
      <p>State rules change frequently — check your state’s revenue department or an estate attorney for current exemptions and rates.</p>

      <div class="callout warn"><?= icon('shield') ?><p><strong>This is an estimate.</strong> Real estates involve appraisals, valuation discounts, jointly owned property rules, gift tax paid on earlier gifts, the generation-skipping transfer tax and state law. Work with an estate planning attorney before relying on any number.</p></div>

<?= faq_block([
  ['What is the federal estate tax exemption for ' . $Y . '?', '<p>' . money($exempt) . ' per person, set by the One Big Beautiful Bill Act and indexed for inflation after 2026. A married couple can shelter ' . money($exempt * 2) . ' using portability. The ' . ($Y - 1) . ' exemption was ' . money($TAX['years'][(string) ($Y - 1)]['estate']['exemption']) . '.</p>'],
  ['How much is the estate tax rate?', '<p>The unified rate schedule runs from 18% to 40%, but because the applicable credit covers the exemption amount, the tax effectively applies at a flat 40% on the taxable estate (plus adjusted taxable gifts) above the exemption.</p>'],
  ['Do heirs pay estate tax?', '<p>No — the estate pays federal estate tax before assets are distributed. Heirs don’t owe income tax on an inheritance either, though they may owe income tax when withdrawing inherited traditional IRA or 401(k) money, and some states charge a separate inheritance tax to heirs.</p>'],
  ['Is life insurance included in my estate?', '<p>Yes, if you owned the policy or held incidents of ownership such as the right to change the beneficiary. Policies owned by an irrevocable life insurance trust (held more than three years) or by another person are generally excluded.</p>'],
  ['What is portability (DSUE)?', '<p>Portability lets a surviving spouse use the deceased spouse’s unused exemption on top of their own. The executor must elect it on a timely Form 706, even if no estate tax is owed.</p>'],
  ['Do lifetime gifts reduce my estate tax exemption?', '<p>Yes. The gift and estate tax share one unified exemption. Taxable gifts above the annual exclusion are added back as “adjusted taxable gifts” when figuring estate tax, so they use up exemption that would otherwise shelter your estate.</p>'],
  ['Which states have an estate or inheritance tax?', '<p>Twelve states plus DC have an estate tax, and five states have an inheritance tax (Maryland has both). State exemptions are often far below the federal amount, so check your state’s current rules.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('estate-tax-calculator', ['gift-tax-calculator', 'capital-gains-tax', 'federal-income-tax', 's-corp-tax-savings', 'state-income-tax']) ?></div>
