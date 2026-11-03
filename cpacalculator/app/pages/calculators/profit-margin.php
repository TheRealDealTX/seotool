<?php
defined('CPA') or exit;
$P['title'] = "Profit Margin Calculator — Margin, Markup & Selling Price | CPA Calculator";
$P['description'] = "Free profit margin calculator: get margin, markup and profit from cost and price, the price for a target margin or markup, plus gross, operating and net margin.";
$P['scripts'] = ['/assets/js/tools/profit-margin.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Worked examples (same formulas as the JS). */
$exCost = 60; $exPrice = 100;
$exProfit = $exPrice - $exCost;
$exMargin = $exProfit / $exPrice; $exMarkup = $exProfit / $exCost;
$exTarget = 0.40; $exTargetPrice = 45 / (1 - $exTarget);
$pl = ['rev' => 500000, 'cogs' => 300000, 'opex' => 120000, 'other' => 25000];
$pl['gross'] = $pl['rev'] - $pl['cogs']; $pl['op'] = $pl['gross'] - $pl['opex']; $pl['net'] = $pl['op'] - $pl['other'];
$pct = fn($x, $dp = 1) => number_format($x * 100, $dp) . '%';

echo tool_hero('profit-margin', "Profit Margin Calculator",
  "Enter a cost and a selling price to get your profit margin, markup and profit — or work backward from a target margin or markup to the price you should charge. Switch to the income-statement mode for gross, operating and net profit margin.",
  ['Margin, markup & profit', 'Price from target margin', 'Gross, operating & net margin', 'Margin vs markup table']);
?>
<section class="tool" aria-label="Profit margin calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="pm-form" novalidate>
        <div class="field"><span class="lbl">What do you want to calculate?</span><div class="seg" role="radiogroup" aria-label="Calculation mode">
          <label><input type="radio" name="mode" value="price" checked><span>Margin from cost &amp; price</span></label>
          <label><input type="radio" name="mode" value="margin"><span>Price from target margin</span></label>
          <label><input type="radio" name="mode" value="markup"><span>Price from markup</span></label>
          <label><input type="radio" name="mode" value="pl"><span>Gross, operating &amp; net margin</span></label>
        </div></div>
        <fieldset class="fieldset" data-when="price margin markup"><legend>Per unit</legend>
          <div class="grid-2">
            <?= money_field('cost', 'Cost per unit', $exCost, 'What one unit costs you: purchase price or materials and direct labor, plus inbound shipping. For services, your direct cost of delivering the job.') ?>
            <div data-when="price"><?= money_field('price', 'Selling price per unit', $exPrice, 'What the customer pays you, before sales tax.') ?></div>
            <div data-when="margin"><?= money_field('tmargin', 'Target profit margin', 40, 'Profit as a percentage of the selling price. Must be below 100%.', '', '%') ?></div>
            <div data-when="markup"><?= money_field('tmarkup', 'Markup', 50, 'Profit as a percentage of cost. 100% markup means doubling your cost.', '', '%') ?></div>
          </div>
          <?= money_field('units', 'Units sold (optional)', '', 'Enter a volume to see total revenue, cost and profit.', '', '') ?>
        </fieldset>
        <fieldset class="fieldset" data-when="pl"><legend>Income statement (any period)</legend>
          <?= money_field('rev', 'Revenue (net sales)', $pl['rev'], 'Total sales after returns, discounts and allowances.') ?>
          <div class="grid-2">
            <?= money_field('cogs', 'Cost of goods sold (COGS)', $pl['cogs'], 'Direct costs of what you sold: inventory, materials, direct labor, freight-in.') ?>
            <?= money_field('opex', 'Operating expenses', $pl['opex'], 'Rent, salaries, marketing, software, insurance, depreciation and other overhead.') ?>
          </div>
          <?= money_field('other', 'Interest, taxes & other expenses', $pl['other'], 'Interest expense, income taxes and any non-operating items (net of other income).') ?>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label" data-out="biglabel">Profit margin</div>
          <div class="res-big" data-out="big">0%</div>
          <div class="res-sub" data-out="sub">—</div>
          <div class="kpis">
            <div class="kpi"><small data-out="k1l">Gross margin</small><b data-out="k1">0%</b></div>
            <div class="kpi"><small data-out="k2l">Markup</small><b data-out="k2">0%</b></div>
            <div class="kpi"><small data-out="k3l">Profit per unit</small><b data-out="k3">$0</b></div>
            <div class="kpi"><small data-out="k4l">Selling price</small><b data-out="k4">$0</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where each sales dollar goes"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note"><span data-out="note">Margin is profit ÷ price; markup is profit ÷ cost.</span> <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use the profit margin calculator</h2>
      <p>Choose one of four modes at the top of the calculator:</p>
      <ul>
        <li><strong>Margin from cost &amp; price</strong> — enter what an item costs you and what you sell it for. You get profit per unit, profit margin and markup.</li>
        <li><strong>Price from target margin</strong> — enter your cost and the margin you want (say 40%). The calculator gives the selling price that delivers exactly that margin.</li>
        <li><strong>Price from markup</strong> — enter your cost and a markup percentage, the way many retailers and contractors price. You’ll see the price and the margin it really produces.</li>
        <li><strong>Gross, operating &amp; net margin</strong> — enter revenue, cost of goods sold, operating expenses and interest/taxes from an income statement to see all three margins for your whole business.</li>
      </ul>
      <p>Add units sold in any of the per-unit modes to see totals, and use “Copy share link” to send the exact scenario to a partner or your accountant.</p>

      <h2 id="formula">Profit margin formulas</h2>
      <div class="formula">Profit = selling price − cost<br>Profit margin = profit ÷ selling price × 100<br>Markup = profit ÷ cost × 100<br>Price for a target margin = cost ÷ (1 − margin)<br>Price for a markup = cost × (1 + markup)</div>
      <p>For a whole business, the same idea applies at three levels of the income statement:</p>
      <div class="formula">Gross margin = (revenue − COGS) ÷ revenue<br>Operating margin = (revenue − COGS − operating expenses) ÷ revenue<br>Net margin = net income ÷ revenue</div>

      <h2 id="example">Profit margin examples</h2>
      <h3 id="example-unit">From cost and price</h3>
      <p>You buy a product for <?= money($exCost, 2) ?> and sell it for <?= money($exPrice, 2) ?>. Profit is <?= money($exProfit, 2) ?>, so the <strong>profit margin is <?= $pct($exMargin) ?></strong> (<?= money($exProfit) ?> ÷ <?= money($exPrice) ?>) and the <strong>markup is <?= $pct($exMarkup) ?></strong> (<?= money($exProfit) ?> ÷ <?= money($exCost) ?>). Same dollars, two very different percentages.</p>
      <h3 id="example-target">Pricing for a target margin</h3>
      <p>A product costs $45 and you want a 40% margin. Divide cost by (1 − 0.40): $45 ÷ 0.60 = <strong><?= money($exTargetPrice, 2) ?></strong>. A common mistake is adding 40% to cost ($45 × 1.4 = $63.00) — that’s a 40% <em>markup</em> and only a <?= $pct((63 - 45) / 63) ?> margin.</p>
      <h3 id="example-pl">Gross, operating and net margin</h3>
      <div class="table-wrap"><table>
        <thead><tr><th>Income statement</th><th class="n">Amount</th><th class="n">% of revenue</th></tr></thead><tbody>
        <tr><td>Revenue</td><td class="n"><?= money($pl['rev']) ?></td><td class="n">100.0%</td></tr>
        <tr><td>Cost of goods sold</td><td class="n">−<?= money($pl['cogs']) ?></td><td class="n"><?= $pct($pl['cogs'] / $pl['rev']) ?></td></tr>
        <tr><td><strong>Gross profit</strong></td><td class="n"><strong><?= money($pl['gross']) ?></strong></td><td class="n"><strong><?= $pct($pl['gross'] / $pl['rev']) ?></strong> gross margin</td></tr>
        <tr><td>Operating expenses</td><td class="n">−<?= money($pl['opex']) ?></td><td class="n"><?= $pct($pl['opex'] / $pl['rev']) ?></td></tr>
        <tr><td><strong>Operating profit</strong></td><td class="n"><strong><?= money($pl['op']) ?></strong></td><td class="n"><strong><?= $pct($pl['op'] / $pl['rev']) ?></strong> operating margin</td></tr>
        <tr><td>Interest &amp; taxes</td><td class="n">−<?= money($pl['other']) ?></td><td class="n"><?= $pct($pl['other'] / $pl['rev']) ?></td></tr>
        <tr><td><strong>Net profit</strong></td><td class="n"><strong><?= money($pl['net']) ?></strong></td><td class="n"><strong><?= $pct($pl['net'] / $pl['rev']) ?></strong> net margin</td></tr>
      </tbody></table></div>

      <h2 id="margin-vs-markup">Margin vs markup</h2>
      <p>Margin and markup both describe the same profit, but measured against different bases. <strong>Margin</strong> compares profit to the selling price, so it can never reach 100%. <strong>Markup</strong> compares profit to cost, so it can be any size — a 300% markup is perfectly possible. Because cost is always smaller than price (when you’re profitable), markup is always the larger number. Use this conversion table to translate between them:</p>
      <div class="table-wrap"><table>
        <thead><tr><th class="n">Profit margin</th><th class="n">Equivalent markup</th><th class="n">Price for a $100 cost</th></tr></thead><tbody>
<?php foreach ([0.10, 0.15, 0.20, 0.25, 1 / 3, 0.40, 0.50, 0.60, 0.70, 0.75] as $m): ?>
        <tr><td class="n"><?= $pct($m) ?></td><td class="n"><?= $pct($m / (1 - $m)) ?></td><td class="n"><?= money(100 / (1 - $m), 2) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <div class="formula">Markup = margin ÷ (1 − margin)<br>Margin = markup ÷ (1 + markup)</div>
      <p>Mixing the two up is one of the most expensive pricing mistakes a small business can make: if you want a 50% margin but add a 50% markup, you actually earn a 33.3% margin.</p>

      <h2 id="good-margin">What is a good profit margin?</h2>
      <p>There’s no single “good” number — margins vary enormously by industry and business model. Grocery stores and distributors often run thin net margins and rely on volume, while software, consulting and other service businesses with few direct costs usually have much higher gross margins. The most useful comparisons are:</p>
      <ul>
        <li><strong>Your own trend.</strong> Is your gross margin rising or slipping as costs change?</li>
        <li><strong>Similar businesses.</strong> Industry associations, trade groups and published financial ratio studies report typical margins for businesses like yours.</li>
        <li><strong>Your break-even point.</strong> Your gross margin needs to cover fixed costs with room to spare — the <a href="/calculators/break-even/">break-even calculator</a> shows how many units that takes.</li>
      </ul>

      <h2 id="improve">How to improve your profit margin</h2>
      <ol>
        <li><strong>Price on margin, not markup.</strong> Set the margin you need, then use the target-margin mode to find the price.</li>
        <li><strong>Know your true cost.</strong> Include freight, packaging, payment processing fees and returns in cost per unit.</li>
        <li><strong>Raise prices selectively.</strong> A small price increase falls straight to profit; at a 30% margin, a 5% price rise lifts profit per unit by roughly 17%.</li>
        <li><strong>Watch acquisition costs.</strong> Marketing spend per customer can quietly erase product margin — compare it with your profit per sale using the <a href="/calculators/cost-per-acquisition/">cost per acquisition calculator</a>.</li>
        <li><strong>Plan for taxes.</strong> Profit isn’t what you keep. Sole proprietors and freelancers can estimate tax on their profit with the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>, and growing businesses can test an <a href="/calculators/s-corp-tax-savings/">S corp election</a>. Equipment purchases reduce taxable profit through <a href="/calculators/depreciation-calculator/">depreciation</a>.</li>
      </ol>

<?= faq_block([
  ['How do I calculate profit margin?', '<p>Subtract cost from the selling price to get profit, divide profit by the selling price, and multiply by 100. For example, an item that costs ' . money($exCost) . ' and sells for ' . money($exPrice) . ' has a ' . money($exProfit) . ' profit and a ' . $pct($exMargin) . ' profit margin.</p>'],
  ['What is the difference between margin and markup?', '<p>Margin is profit as a percentage of the selling price; markup is profit as a percentage of cost. A product that costs $60 and sells for $100 has a 40% margin but a 66.7% markup. Markup is always the larger number.</p>'],
  ['How do I calculate selling price from cost and margin?', '<p>Divide the cost by (1 − the margin as a decimal). For a $45 cost and a 40% target margin: $45 ÷ 0.60 = ' . money($exTargetPrice, 2) . '.</p>'],
  ['What is the formula for a 30% markup?', '<p>Multiply cost by 1.30. A $50 cost with a 30% markup sells for $65, which works out to a ' . $pct(15 / 65) . ' margin.</p>'],
  ['What’s the difference between gross, operating and net profit margin?', '<p>Gross margin subtracts only the cost of goods sold. Operating margin also subtracts operating expenses like rent, salaries and marketing. Net margin subtracts everything, including interest and income taxes, so it shows what the business actually keeps from each dollar of sales.</p>'],
  ['Can a profit margin be more than 100%?', '<p>No. Because margin is measured against the selling price, profit can never exceed the price, so margin tops out just below 100%. Markup has no ceiling.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('profit-margin', ['break-even', 'cost-per-acquisition', 'depreciation-calculator', '1099-tax-calculator', 's-corp-tax-savings', 'self-employment-tax']) ?></div>
