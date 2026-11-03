<?php
defined('CPA') or exit;
$P['title'] = "Break Even Calculator — Break-Even Point in Units & Sales | CPA Calculator";
$P['description'] = "Free break even calculator. Find your break-even point in units and sales dollars, contribution margin, target-profit units and margin of safety, with a chart.";
$P['scripts'] = ['/assets/js/tools/break-even.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Worked example (same formulas as the JS). */
$ex = ['fixed' => 30000, 'price' => 50, 'var' => 20, 'target' => 15000, 'expected' => 1500];
$ex['cm'] = $ex['price'] - $ex['var'];
$ex['cmr'] = $ex['cm'] / $ex['price'];
$ex['beu'] = $ex['fixed'] / $ex['cm'];
$ex['ber'] = $ex['fixed'] / $ex['cmr'];
$ex['tu'] = ($ex['fixed'] + $ex['target']) / $ex['cm'];
$ex['mos'] = $ex['expected'] - $ex['beu'];
$ex['profit'] = $ex['expected'] * $ex['cm'] - $ex['fixed'];

echo tool_hero('break-even', "Break Even Calculator",
  "Find out how many units you need to sell — and how much revenue you need — to cover your fixed costs. Add a profit goal and your sales forecast to see the units required, your margin of safety and a break-even chart.",
  ['Break-even units & revenue', 'Contribution margin & ratio', 'Target profit & margin of safety', 'Interactive break-even chart']);
?>
<section class="tool" aria-label="Break-even calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="be-form" novalidate>
        <fieldset class="fieldset"><legend>Costs &amp; price</legend>
          <?= money_field('fixed', 'Fixed costs (for the period)', $ex['fixed'], 'Costs that don’t change with sales volume over the period you’re analyzing (e.g. a month or a year): rent, salaries, insurance, software, loan payments, depreciation.') ?>
          <input type="range" min="0" max="250000" step="500" data-range-for="fixed" aria-label="Fixed costs slider">
          <div class="grid-2">
            <?= money_field('price', 'Selling price per unit', $ex['price'], 'Average price a customer pays per unit, net of discounts.') ?>
            <?= money_field('var', 'Variable cost per unit', $ex['var'], 'Costs that rise with each unit sold: materials, direct labor, packaging, shipping, payment processing and sales commissions.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Goals (optional)</legend>
          <div class="grid-2">
            <?= money_field('target', 'Target profit', $ex['target'], 'The profit you want to earn for the period, before income tax.') ?>
            <?= money_field('expected', 'Expected sales (units)', $ex['expected'], 'Your forecast for the period. Used for the margin of safety and projected profit.', '', '') ?>
          </div>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Break-even point</div>
          <div class="res-big" data-out="units">0</div>
          <div class="res-sub" data-out="sub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Break-even revenue</small><b data-out="rev">$0</b></div>
            <div class="kpi"><small>Contribution margin</small><b data-out="cm">$0</b></div>
            <div class="kpi"><small>CM ratio</small><b data-out="cmr">0%</b></div>
            <div class="kpi"><small>Units for target profit</small><b data-out="tu">0</b></div>
            <div class="kpi"><small>Margin of safety</small><b data-out="mos">—</b></div>
            <div class="kpi"><small>Profit at expected sales</small><b data-out="profit">—</b></div>
          </div>
          <svg data-chart viewBox="0 0 420 270" role="img" aria-label="Break-even chart: revenue and total cost lines" style="width:100%;height:auto;display:block;background:#fff;border:1px solid var(--line);border-radius:12px;margin-bottom:18px"></svg>
          <ul class="rows" data-rows></ul>
          <p class="note"><span data-out="note">Assumes price and variable cost per unit stay constant across volumes.</span> <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use the break even calculator</h2>
      <ol>
        <li><strong>Pick a period</strong> — a month or a year — and enter your <strong>fixed costs</strong> for that period.</li>
        <li><strong>Enter your selling price and variable cost per unit.</strong> A “unit” can be a product, a billable hour, a meal, a subscription or an average order.</li>
        <li><strong>Optionally add a target profit</strong> to see the sales needed to hit it, and your <strong>expected sales</strong> to see how much cushion you have above break-even.</li>
      </ol>
      <p>The results update as you type. The chart plots revenue against total cost: where the lines cross is your break-even point, the shaded area to the right is profit and the area to the left is loss.</p>

      <h2 id="formula">The break-even formula</h2>
      <p>Every unit you sell contributes its price minus its variable cost toward paying your fixed costs. That amount is the <strong>contribution margin</strong>. Once enough units have been sold to cover all fixed costs, every additional unit is profit.</p>
      <div class="formula">Contribution margin per unit = price − variable cost<br>Contribution margin ratio = contribution margin ÷ price<br>Break-even units = fixed costs ÷ contribution margin per unit<br>Break-even sales ($) = fixed costs ÷ contribution margin ratio<br>Units for target profit = (fixed costs + target profit) ÷ contribution margin<br>Margin of safety = expected sales − break-even sales</div>

      <h2 id="example">Break-even example</h2>
      <p>A small business has <?= money($ex['fixed']) ?> a month in fixed costs. It sells its product for <?= money($ex['price']) ?> and each unit costs <?= money($ex['var']) ?> in materials, packaging and payment fees.</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Contribution margin per unit (<?= money($ex['price']) ?> − <?= money($ex['var']) ?>)</td><td class="n"><?= money($ex['cm']) ?></td></tr>
        <tr><td>Contribution margin ratio (<?= money($ex['cm']) ?> ÷ <?= money($ex['price']) ?>)</td><td class="n"><?= round($ex['cmr'] * 100, 1) ?>%</td></tr>
        <tr><td>Break-even units (<?= money($ex['fixed']) ?> ÷ <?= money($ex['cm']) ?>)</td><td class="n"><?= number_format(ceil($ex['beu'])) ?> units</td></tr>
        <tr><td>Break-even revenue (<?= money($ex['fixed']) ?> ÷ <?= round($ex['cmr'] * 100) ?>%)</td><td class="n"><?= money($ex['ber']) ?></td></tr>
        <tr><td>Units to earn <?= money($ex['target']) ?> profit</td><td class="n"><?= number_format(ceil($ex['tu'])) ?> units</td></tr>
        <tr><td>Margin of safety at <?= number_format($ex['expected']) ?> expected units</td><td class="n"><?= number_format($ex['mos']) ?> units (<?= round($ex['mos'] / $ex['expected'] * 100, 1) ?>%)</td></tr>
        <tr><td>Profit at expected sales</td><td class="n"><?= money($ex['profit']) ?></td></tr>
      </tbody></table></div>
      <p>Sales could fall by a third before the business starts losing money. Those are the default numbers in the calculator above, so you can change one input at a time and watch the break-even point move.</p>

      <h2 id="what-if">How price and costs move your break-even point</h2>
      <p>Small changes to price have an outsized effect because they flow straight into contribution margin. Using the example’s <?= money($ex['fixed']) ?> of fixed costs and <?= money($ex['var']) ?> variable cost:</p>
      <div class="table-wrap"><table>
        <thead><tr><th class="n">Price</th><th class="n">Contribution margin</th><th class="n">Break-even units</th><th class="n">Break-even revenue</th></tr></thead><tbody>
<?php foreach ([35, 40, 45, 50, 55, 60, 70] as $p): $cm = $p - $ex['var']; ?>
        <tr><td class="n"><?= money($p) ?></td><td class="n"><?= money($cm) ?></td><td class="n"><?= number_format(ceil($ex['fixed'] / $cm)) ?></td><td class="n"><?= money(ceil($ex['fixed'] / $cm) * $p) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <p>Cutting the price from $50 to $40 doesn’t lower break-even by a fifth — it raises it by half, from 1,000 to 1,500 units. That’s why discounting is so risky for businesses with modest contribution margins. You can lower your break-even point three ways:</p>
      <ul>
        <li><strong>Raise prices</strong> (or shift your mix toward higher-margin products).</li>
        <li><strong>Reduce variable costs</strong> — better supplier pricing, lower shipping, cheaper payment processing.</li>
        <li><strong>Reduce fixed costs</strong> — renegotiate rent, cut unused subscriptions, outsource instead of hiring.</li>
      </ul>

      <h2 id="fixed-vs-variable">Fixed costs vs variable costs</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Fixed costs (per period)</th><th>Variable costs (per unit)</th></tr></thead><tbody>
        <tr><td>Rent and utilities for your space</td><td>Raw materials and inventory</td></tr>
        <tr><td>Salaried staff and owner pay</td><td>Hourly production labor</td></tr>
        <tr><td>Insurance, licenses, accounting fees</td><td>Packaging and shipping</td></tr>
        <tr><td>Software subscriptions and website</td><td>Credit card and marketplace fees</td></tr>
        <tr><td>Loan payments, equipment leases, depreciation</td><td>Sales commissions</td></tr>
      </tbody></table></div>
      <p>Some costs are mixed — a phone plan with a base fee plus usage, for example. Split them into their fixed and variable parts for the most accurate answer. Equipment is a fixed cost spread over its life; the <a href="/calculators/depreciation-calculator/">depreciation calculator</a> gives you the annual figure.</p>

      <h2 id="margin-of-safety">Margin of safety and operating leverage</h2>
      <p>The <strong>margin of safety</strong> tells you how far sales can fall before you hit break-even. Expressed as a percentage of expected sales, it’s a quick risk gauge: a thin margin of safety means a slow month could put you in the red.</p>
      <p><strong>Operating leverage</strong> measures how sensitive profit is to sales. The degree of operating leverage (DOL) equals total contribution margin divided by operating profit. In the example, DOL is <?= number_format($ex['expected'] * $ex['cm'] / $ex['profit'], 1) ?>, so a 10% increase in sales would lift profit by about <?= round($ex['expected'] * $ex['cm'] / $ex['profit'] * 10) ?>% — and a 10% drop would cut it by the same amount. Businesses with high fixed costs have high operating leverage.</p>

      <h2 id="limits">Limitations of break-even analysis</h2>
      <ul>
        <li>It assumes price and variable cost per unit stay constant. In reality, volume discounts, price changes and overtime can bend the lines.</li>
        <li>Fixed costs are only fixed within a range — adding a second location or shift creates a new, higher break-even point.</li>
        <li>For multiple products, use a weighted-average contribution margin based on your sales mix.</li>
        <li>Break-even is before income tax. To hit an after-tax profit goal, divide it by (1 − your tax rate) before entering it as the target. Self-employed owners can estimate that rate with the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>.</li>
      </ul>
      <p>Pair this tool with the <a href="/calculators/profit-margin/">profit margin calculator</a> to set prices, and the <a href="/calculators/cost-per-acquisition/">cost per acquisition calculator</a> to check that your marketing cost per customer leaves room for contribution margin.</p>

<?= faq_block([
  ['How do you calculate the break-even point?', '<p>Divide fixed costs by the contribution margin per unit (selling price minus variable cost per unit). With ' . money($ex['fixed']) . ' of fixed costs, a ' . money($ex['price']) . ' price and a ' . money($ex['var']) . ' variable cost, break-even is ' . money($ex['fixed']) . ' ÷ ' . money($ex['cm']) . ' = ' . number_format(ceil($ex['beu'])) . ' units.</p>'],
  ['How do I calculate break-even in sales dollars?', '<p>Divide fixed costs by the contribution margin ratio (contribution margin ÷ price). In the example, ' . money($ex['fixed']) . ' ÷ ' . round($ex['cmr'] * 100) . '% = ' . money($ex['ber']) . ' of revenue.</p>'],
  ['What is contribution margin?', '<p>Contribution margin is what each sale leaves over after variable costs, available to cover fixed costs and then profit. Per unit it’s price minus variable cost; as a ratio it’s that amount divided by price.</p>'],
  ['How many units do I need to sell to make a profit?', '<p>Add your target profit to fixed costs, then divide by contribution margin per unit. To earn ' . money($ex['target']) . ' in the example: (' . money($ex['fixed']) . ' + ' . money($ex['target']) . ') ÷ ' . money($ex['cm']) . ' = ' . number_format(ceil($ex['tu'])) . ' units.</p>'],
  ['What is a good margin of safety?', '<p>It depends on how predictable your sales are. A larger margin of safety gives more protection against a slow period; businesses with volatile or seasonal sales generally want more cushion than those with steady recurring revenue.</p>'],
  ['Does break-even include taxes?', '<p>Standard break-even analysis is pre-tax: at break-even there’s no profit, so no income tax. When planning for a target profit, convert an after-tax goal to pre-tax by dividing by (1 − tax rate).</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('break-even', ['profit-margin', 'cost-per-acquisition', 'depreciation-calculator', '1099-tax-calculator', 's-corp-tax-savings', 'home-office-deduction']) ?></div>
