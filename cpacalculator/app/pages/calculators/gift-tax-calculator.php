<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$excl = $y['giftAnnualExclusion'];
$exempt = $y['estate']['exemption'];
$P['title'] = "Gift Tax Calculator $Y — Annual Exclusion & Form 709 | CPA Calculator";
$P['description'] = "Free $Y gift tax calculator: see what the " . money($excl) . " annual exclusion covers, your taxable gifts, lifetime exemption left and whether you must file Form 709.";
$P['scripts'] = ['/assets/js/tools/gift-tax-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Unified transfer tax (IRC §2001(c)) on a cumulative amount, from tax.json estate.brackets. */
function gt_unified_tax(float $amt, array $br): float {
  $tax = 0; $prev = 0;
  foreach ($br as [$top, $rate]) {
    $top = $top ?? INF;
    if ($amt > $prev) $tax += (min($amt, $top) - $prev) * $rate;
    $prev = $top;
  }
  return $tax;
}
/* Worked example: married parent gives two children $50,000 each and a grandchild $19,000; optional gift splitting. */
function gt_example(array $gifts, bool $split, float $prior = 0): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $ex = $y['giftAnnualExclusion']; $br = $y['estate']['brackets']; $exempt = $y['estate']['exemption'];
  $excl = 0; $taxable = 0;
  foreach ($gifts as $g) { $mine = $split ? $g / 2 : $g; $e = min($mine, $ex); $excl += $e; $taxable += $mine - $e; }
  $credit = gt_unified_tax($exempt, $br);
  $usedPrior = min(gt_unified_tax($prior, $br), $credit);
  $due = max(0, gt_unified_tax($prior + $taxable, $br) - gt_unified_tax($prior, $br) - ($credit - $usedPrior));
  return ['excl' => $excl, 'taxable' => $taxable, 'left' => max(0, $exempt - $prior - $taxable), 'due' => $due, 'credit' => $credit];
}
$gifts = [50000, 50000, $excl];
$exA = gt_example($gifts, false);
$exB = gt_example($gifts, true);
$credit = $exA['credit'];
$nc = $y['giftSpouseNonCitizen'];

echo tool_hero('gift-tax-calculator', "Gift Tax Calculator $Y",
  "Work out how a gift is treated for federal gift tax: how much the " . money($excl) . " annual exclusion covers, what counts as a taxable gift, whether you need to file Form 709, and how much of your " . money($exempt) . " lifetime exemption is left. Add every recipient, split gifts with your spouse, and include tuition or medical bills you paid directly.",
  ["$Y annual exclusion: " . money($excl), 'Gift splitting with a spouse', 'Lifetime exemption tracker', 'Form 709 filing check']);
?>
<section class="tool" aria-label="Gift tax calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="gift-form" novalidate>
        <?= year_field() ?>
        <fieldset class="fieldset"><legend>Gifts to individuals this year</legend>
          <p class="hint" style="margin-top:0" data-out="exhint">Each recipient can receive up to <?= money($excl) ?> from you this year tax-free and without a Form 709.</p>
          <?php for ($i = 1; $i <= 10; $i++): ?>
          <div class="grid-2" data-row="<?= $i ?>"<?= $i > 3 ? ' hidden' : '' ?>>
            <?= money_field('g' . $i, 'Recipient ' . $i . ' — total gifts', [50000, 50000, $excl][$i - 1] ?? '', $i === 1 ? 'Total of everything you gave this person during the year: cash, checks, stock (at fair market value), forgiven loans, a share of property, 529 contributions.' : '') ?>
            <div class="field"><label for="f-t<?= $i ?>">Gift type</label><select id="f-t<?= $i ?>" name="t<?= $i ?>">
              <option value="present">Present interest (cash, stock)</option>
              <option value="future">Future interest — no exclusion</option>
              <option value="529">529 plan, 5-year election</option>
            </select></div>
          </div>
          <?php endfor; ?>
          <button type="button" class="btn-ghost" data-addrow>+ Add another recipient</button>
        </fieldset>
        <fieldset class="fieldset"><legend>Married?</legend>
          <label class="check"><input type="checkbox" name="split" value="1"> Split gifts with my spouse (both spouses consent on Form 709)</label>
          <div class="grid-2">
            <div class="field"><label for="f-spouse">Your spouse is</label><select id="f-spouse" name="spouse">
              <option value="citizen">A US citizen (unlimited)</option>
              <option value="noncitizen">Not a US citizen</option>
            </select></div>
            <?= money_field('sg', 'Amount given to spouse', '', 'Outright gifts to a US-citizen spouse are fully covered by the marital deduction. A non-citizen spouse has a higher annual exclusion instead (' . money($nc) . ' for ' . $Y . ').') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Excluded payments &amp; prior gifts</legend>
          <?= money_field('edmed', 'Tuition or medical bills paid directly', '', 'Paid straight to a school (tuition only) or a medical provider or insurer on someone’s behalf. These are excluded without limit and don’t use your annual exclusion.') ?>
          <?= money_field('prior', 'Taxable gifts in earlier years', '', 'Total taxable gifts reported on your prior Forms 709 (after annual exclusions). This is the part of your lifetime exemption already used.') ?>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Gift tax due this year</div>
          <div class="res-big good" data-out="due">$0</div>
          <div class="res-sub" data-out="summary">—</div>
          <div class="kpis">
            <div class="kpi"><small>Annual exclusion used</small><b data-out="excl">$0</b></div>
            <div class="kpi"><small>Taxable gifts</small><b data-out="taxable">$0</b></div>
            <div class="kpi"><small>Lifetime exemption used</small><b data-out="used">$0</b></div>
            <div class="kpi"><small>Exemption remaining</small><b data-out="left">$0</b></div>
          </div>
          <div class="res-label" style="margin-bottom:4px">Lifetime exemption</div>
          <div class="meter" data-meter role="img" aria-label="Share of lifetime exemption used"></div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="How your gifts are treated"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note" data-out="note">Federal gift tax only. Connecticut is the one state with its own gift tax. Not legal advice — complex gifts (trusts, business interests, real estate) need an appraisal and a professional.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-gift-tax-works">How the federal gift tax works</h2>
      <p>The gift tax applies when you give money or property to someone without getting full value in return. It is paid by the <strong>giver</strong>, not the recipient — the person receiving a gift owes no federal income tax or gift tax on it. In practice almost nobody pays it, because two generous allowances come first:</p>
      <ul>
        <li><strong>The annual exclusion:</strong> <?= money($excl) ?> per recipient for <?= $Y ?>. You can give that much to as many people as you like each year. A married couple can give <?= money($excl * 2) ?> to each person.</li>
        <li><strong>The lifetime exemption:</strong> gifts above the annual exclusion are “taxable gifts,” but they simply use up part of your <?= money($exempt) ?> lifetime exemption. It is unified with the estate tax exemption — whatever you use during life reduces what is left at death. Under the One Big Beautiful Bill Act it is <?= money($exempt) ?> per person for <?= $Y ?> and indexed for inflation from 2027.</li>
      </ul>
      <p>Only once you’ve given away more than the lifetime exemption in taxable gifts does actual tax start, at rates that reach 40% almost immediately.</p>

      <h2 id="how-to-use">How to use the gift tax calculator</h2>
      <ol>
        <li>Pick the year of the gift — the annual exclusion and exemption change with inflation.</li>
        <li>Enter the total you gave each person during the year. Add rows for more recipients. Choose “future interest” for gifts the recipient can’t use right away (most trusts without withdrawal rights), which don’t qualify for the exclusion.</li>
        <li>If you’re married, tick <strong>gift splitting</strong> to treat each gift as made half by you and half by your spouse.</li>
        <li>Add gifts to your spouse, tuition or medical bills you paid directly, and any taxable gifts from earlier years.</li>
      </ol>

      <h2 id="formula">Gift tax formula</h2>
      <div class="formula">Taxable gift (per recipient) = gift − annual exclusion (<?= money($excl) ?>)<br>Taxable gifts this year = Σ taxable gifts − marital &amp; charitable deductions<br>Tax = unified tax(prior + this year) − unified tax(prior) − unused credit<br>Applicable credit = unified tax on <?= money($exempt) ?> = <?= money($credit) ?></div>
      <p>Tuition paid directly to a school and medical payments made directly to a provider are left out entirely. Outright gifts to a US-citizen spouse are fully deductible; a non-citizen spouse gets a special annual exclusion of <?= money($nc) ?> instead.</p>

      <h2 id="example">Example: gifts to children and a grandchild</h2>
      <p>A parent gives $50,000 to each of two adult children and <?= money($excl) ?> to a grandchild in <?= $Y ?>, with no prior taxable gifts.</p>
      <div class="table-wrap"><table>
        <thead><tr><th></th><th class="n">Without splitting</th><th class="n">With gift splitting (each spouse)</th></tr></thead><tbody>
        <tr><td>Total given</td><td class="n"><?= money(array_sum($gifts)) ?></td><td class="n"><?= money(array_sum($gifts) / 2) ?></td></tr>
        <tr><td>Annual exclusions used</td><td class="n"><?= money($exA['excl']) ?></td><td class="n"><?= money($exB['excl']) ?></td></tr>
        <tr><td>Taxable gifts</td><td class="n"><?= money($exA['taxable']) ?></td><td class="n"><?= money($exB['taxable']) ?></td></tr>
        <tr><td>Lifetime exemption remaining</td><td class="n"><?= money($exA['left']) ?></td><td class="n"><?= money($exB['left']) ?></td></tr>
        <tr><td>Gift tax due</td><td class="n"><?= money($exA['due']) ?></td><td class="n"><?= money($exB['due']) ?></td></tr>
        <tr><td>Form 709 required?</td><td class="n">Yes</td><td class="n">Yes — both spouses</td></tr>
      </tbody></table></div>
      <p>Without splitting, <?= money($exA['taxable']) ?> of the gifts exceed the exclusion. No tax is due — the amount is simply subtracted from the lifetime exemption — but a Form 709 must be filed. With gift splitting, each spouse is treated as giving $25,000 to each child and <?= money($excl / 2) ?> to the grandchild, so only <?= money($exB['taxable']) ?> per spouse is taxable. Splitting still requires a Form 709 to make the election.</p>

      <h2 id="form-709">When you must file Form 709</h2>
      <p>You need to file Form 709 (United States Gift and Generation-Skipping Transfer Tax Return) for a year in which you:</p>
      <ul>
        <li>gave any one person (other than your US-citizen spouse) more than the annual exclusion;</li>
        <li>made any gift of a future interest, regardless of size;</li>
        <li>want to split gifts with your spouse;</li>
        <li>elect to spread a large 529 plan contribution over five years; or</li>
        <li>gave a non-citizen spouse more than <?= money($nc) ?>.</li>
      </ul>
      <p>Form 709 is due April 15 of the following year. An extension of your income tax return (Form 4868) also extends Form 709; otherwise use Form 8892. Late filing carries no penalty when no tax is due, but filing on time starts the statute of limitations on the gift’s value — a good reason to file for hard-to-value assets.</p>

      <h2 id="limits">Gift tax limits by year</h2>
      <div class="table-wrap"><table><thead><tr><th>Year</th><th class="n">Annual exclusion</th><th class="n">Non-citizen spouse</th><th class="n">Lifetime exemption</th></tr></thead><tbody>
      <?php $yrs = array_keys($TAX['years']); rsort($yrs); foreach ($yrs as $yr): $d = $TAX['years'][$yr]; ?>
        <tr><td><?= $yr ?></td><td class="n"><?= money($d['giftAnnualExclusion']) ?></td><td class="n"><?= money($d['giftSpouseNonCitizen']) ?></td><td class="n"><?= money($d['estate']['exemption']) ?></td></tr>
      <?php endforeach; ?>
      </tbody></table></div>

      <h2 id="tips">Planning tips</h2>
      <ul>
        <li><strong>Use the exclusion every year.</strong> It doesn’t carry over. A couple giving <?= money($excl * 2) ?> a year to three children moves <?= money($excl * 2 * 3 * 10) ?> out of their estate over ten years without touching the lifetime exemption.</li>
        <li><strong>Pay tuition and medical bills directly.</strong> A grandparent who writes the tuition check to the university can still give the grandchild the full annual exclusion on top.</li>
        <li><strong>Superfund a 529.</strong> You can contribute up to five years of exclusions (<?= money($excl * 5) ?> per beneficiary, double for couples) at once and elect to spread it over five years on Form 709.</li>
        <li><strong>Think about basis.</strong> Gifted property keeps your cost basis, while inherited property generally gets a step-up to market value at death. Gifting highly appreciated stock can increase the recipient’s eventual <a href="/calculators/capital-gains-tax/">capital gains tax</a>.</li>
        <li><strong>Large lifetime gifts are safe.</strong> IRS regulations prevent a “clawback” if the exemption is ever lowered after you’ve used it.</li>
      </ul>
      <p>To see how lifetime gifts interact with what you leave at death, run the <a href="/calculators/estate-tax-calculator/">estate tax calculator</a> — taxable gifts are added back as “adjusted taxable gifts.”</p>

<?= faq_block([
  ['How much can you gift tax-free in ' . $Y . '?', '<p>' . money($excl) . ' per recipient under the annual exclusion, or ' . money($excl * 2) . ' if you and your spouse split gifts. Above that, gifts use your ' . money($exempt) . ' lifetime exemption, so tax is only owed after cumulative taxable gifts pass that amount.</p>'],
  ['Who pays gift tax — the giver or the receiver?', '<p>The giver. The recipient doesn’t report a gift as income and owes no gift tax. If the giver fails to pay a gift tax that is due, the IRS can collect from the recipient, but that is rare.</p>'],
  ['Do I have to pay tax if I give more than the annual exclusion?', '<p>Usually not. You file Form 709 to report the taxable portion, and it reduces your lifetime exemption. Tax is due only after your lifetime taxable gifts exceed ' . money($exempt) . '.</p>'],
  ['Is there a gift tax between spouses?', '<p>No, if your spouse is a US citizen — the marital deduction is unlimited for outright gifts. If your spouse is not a US citizen, the annual exclusion for gifts to them is ' . money($nc) . ' in ' . $Y . '; anything above that is a taxable gift.</p>'],
  ['Does paying someone’s tuition count as a gift?', '<p>Not if you pay the school directly. Tuition paid straight to a qualifying educational institution and medical expenses paid straight to a provider are excluded without limit. Room, board, books and reimbursements to the student don’t qualify.</p>'],
  ['What is the gift tax rate?', '<p>The same unified rate schedule as the estate tax: 18% on the first $10,000 rising to 40% above $1 million of taxable transfers. Because the applicable credit (' . money($credit) . ') covers the first ' . money($exempt) . ', any gift tax actually paid is effectively at 40%.</p>'],
  ['Do I need to file Form 709 if I split gifts?', '<p>Yes. Gift splitting is elected on Form 709, and in most cases both spouses file their own return. It is due April 15 of the year after the gift.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('gift-tax-calculator', ['estate-tax-calculator', 'capital-gains-tax', 'federal-income-tax', 'tax-refund-calculator', 's-corp-tax-savings']) ?></div>
