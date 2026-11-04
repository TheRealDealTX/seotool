<?php
defined('CPA') or exit;
require_once SITE_ROOT . '/app/state-calc.php';
$Y = TAX_YEAR;
$ST = states();
$rank = state_rank_75k();
$none = array_keys(array_filter($ST, fn($s) => $s['type'] === 'none'));
$flat = array_keys(array_filter($ST, fn($s) => $s['type'] === 'flat'));
$prog = array_keys(array_filter($ST, fn($s) => $s['type'] === 'progressive'));
$top = [];
foreach ($ST as $c => $s) if ($s['type'] !== 'none') $top[$c] = st_top_rate($s);
arsort($top);
$hiTop = array_slice($top, 0, 5, true);
$loTop = array_slice(array_reverse($top, true), 0, 5, true);
$taxed = array_filter($rank, fn($v) => $v > 0);
$avg75 = array_sum($taxed) / count($taxed);
$hi75 = array_key_first($rank);
$lo75 = array_key_last($taxed);
$ca = state_calc('CA', ['wages' => 75000, 'status' => 'single']);
$names = fn(array $codes) => implode(', ', array_map(fn($c) => '<a href="/calculators/state-income-tax/' . $ST[$c]['slug'] . '/">' . e($ST[$c]['name']) . '</a>', $codes));

$P['title'] = "State Income Tax Calculator $Y: All 50 States & DC";
$P['description'] = "Free $Y state income tax calculator for all 50 states and DC. Estimate state tax, brackets, effective rate, federal tax, FICA and take-home pay in seconds.";
$P['scripts'] = ['/assets/js/tools/state-tax.js'];
$P['modified'] = date('Y-m-d', max(filemtime(__FILE__), filemtime(SITE_ROOT . '/app/data/states.json')));

echo tool_hero('state-income-tax', "State Income Tax Calculator $Y",
  "Pick any of the 50 states or Washington, DC to estimate your $Y state income tax alongside federal income tax, Social Security and Medicare — with your effective state rate, bracket and take-home pay per year, month and paycheck. Includes NYC and Yonkers tax and an optional local tax rate.",
  ['All 50 states + DC', "Updated for $Y rate cuts", 'Federal + state + FICA', 'NYC & local taxes']);
echo states_data_script();
echo state_form_html('CA', 'State income tax calculator');
?>
<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use the state income tax calculator</h2>
      <p>Choose your state of residence, your filing status and your annual wages. Results update as you type: the big number is your estimated <strong>state income tax</strong>, and the breakdown below adds <strong>federal income tax</strong> and <strong>FICA</strong> (Social Security and Medicare) so you can see total tax and take-home pay in one place.</p>
      <ol>
        <li><strong>Select your state.</strong> Use the state where you live. If you live in one state and work in another, see <a href="#two-states">working in two states</a> below.</li>
        <li><strong>Pick a filing status</strong> and the number of children under 17 — children reduce federal tax through the Child Tax Credit and, in many states, through dependent exemptions or credits.</li>
        <li><strong>Enter income.</strong> Put salary, wages, tips and bonuses in the first box and other ordinary income (interest, unemployment, IRA withdrawals) in the second.</li>
        <li><strong>Add pre-tax 401(k) contributions</strong> to see how much they save. They lower federal and state taxable income everywhere except Pennsylvania.</li>
        <li><strong>Add local taxes</strong> if they apply: tick the New York City or Yonkers box for New York, or type a city, county or school-district rate.</li>
      </ol>
      <p>Each state also has its own page with that state’s brackets, deductions, worked examples and comparisons with its neighbors — links to all 51 are <a href="#state-pages">at the bottom of this page</a>.</p>

      <h2 id="how-it-works">How state income tax works</h2>
      <p>Forty-one states and DC tax wages. Every one of them sets its own rules, but almost all follow the same basic recipe:</p>
      <div class="formula">Federal AGI ± state adjustments = State AGI<br>State AGI − state standard deduction − exemptions = State taxable income<br>State taxable income × state rate(s) − state credits = State income tax</div>
      <ul>
        <li><strong>Starting point.</strong> Most states start from your federal adjusted gross income. Colorado, Idaho, Iowa, Montana, New Mexico and North Dakota effectively start from federal taxable income, so the federal standard deduction carries over. A few states, such as Pennsylvania, ignore the federal return almost entirely and tax specific classes of income.</li>
        <li><strong>Deductions and exemptions.</strong> State standard deductions range from zero (Connecticut, Illinois, Massachusetts, New Jersey, Pennsylvania and others) to the full federal amount (<?= money($ST['CO']['std']['single']) ?> single in states that copy it). Many states also allow a personal exemption per taxpayer and dependent, and some give the exemption as a tax credit instead.</li>
        <li><strong>Rates.</strong> States use one of three structures: no tax on wages, one flat rate, or graduated brackets like the federal system.</li>
        <li><strong>Credits.</strong> State earned-income credits, child credits and credits for taxes paid to other states reduce the bill dollar for dollar.</li>
      </ul>
      <div class="callout"><?= icon('spark') ?><p><strong>Good to know:</strong> state income tax is deductible on your federal return only if you itemize, and only within the SALT cap of <?= money($TAX['years'][(string) $Y]['saltCap']) ?> for <?= $Y ?>. Most people take the standard deduction, so this calculator assumes no federal deduction for state tax.</p></div>

      <h2 id="all-states">State income tax on $75,000 — all 50 states and DC</h2>
      <p>The table shows estimated <?= $Y ?> state income tax for a single filer with $75,000 of W-2 wages, the state standard deduction and no children or local tax. Click a column heading to sort. The average among states that tax wages is <strong><?= money($avg75) ?></strong>; <?= e($ST[$hi75]['name']) ?> is highest at <?= money($rank[$hi75]) ?> and <?= e($ST[$lo75]['name']) ?> lowest at <?= money($rank[$lo75]) ?>.</p>
      <div class="table-wrap"><table data-sortable>
        <caption class="sr-only">State income tax on $75,000 of wages, single filer, <?= $Y ?></caption>
        <thead><tr><th data-sort="text">State</th><th data-sort="text">Type</th><th class="n" data-sort="num">Tax on $75k</th><th class="n" data-sort="num">Effective rate</th><th class="n" data-sort="num">Top rate</th></tr></thead>
        <tbody>
<?php foreach ($ST as $c => $s): $t = $rank[$c]; $tr = $top[$c] ?? 0; ?>
          <tr><td><a href="/calculators/state-income-tax/<?= $s['slug'] ?>/"><?= e($s['name']) ?></a></td><td><?= state_type_label($s) ?></td><td class="n" data-v="<?= round($t) ?>"><?= money($t) ?></td><td class="n" data-v="<?= round($t / 750, 4) ?>"><?= number_format($t / 750, 2) ?>%</td><td class="n" data-v="<?= $tr ?>"><?= $tr ? st_pct($tr) : '—' ?></td></tr>
<?php endforeach; ?>
        </tbody>
      </table></div>
      <p class="hint">Figures use each state’s latest published brackets (<?= $Y ?> where available, otherwise 2025 inflation-adjusted amounts) and exclude local income taxes. Top rate is the highest statutory rate for a single filer, including California’s 1% mental health surcharge and the Massachusetts 4% surtax.</p>

      <h2 id="no-income-tax">The nine states with no income tax on wages</h2>
      <p><?= $names($none) ?> do not tax wages or salaries. Two footnotes: <strong>Washington</strong> taxes long-term capital gains above a large standard deduction (7%, plus 2.9% on gains over $1 million), and <strong>New Hampshire</strong> repealed its Interest &amp; Dividends Tax for 2025 onward, so it now has no individual income tax at all.</p>
      <p>No income tax does not mean low taxes. These states lean harder on sales taxes (Tennessee’s combined rate is among the highest in the country), property taxes (Texas) or severance and tourism taxes (Alaska, Wyoming, Nevada). If you are deciding where to live, compare your whole budget, not just the income tax line.</p>

      <h2 id="flat-tax-states">Flat-tax states</h2>
      <p>These <?= count($flat) ?> states tax wages at a single rate (some with a zero-rate band on the first dollars): <?= $names($flat) ?>. Rates range from <?= st_pct(min(array_map(fn($c) => $top[$c], $flat))) ?> to <?= st_pct(max(array_map(fn($c) => $top[$c], $flat))) ?>.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Flat-tax state</th><th class="n">Rate</th><th class="n">Tax on $75k (single)</th></tr></thead><tbody>
<?php $fl = $flat; usort($fl, fn($a, $b) => $top[$a] <=> $top[$b]); foreach ($fl as $c): ?>
          <tr><td><a href="/calculators/state-income-tax/<?= $ST[$c]['slug'] ?>/"><?= e($ST[$c]['name']) ?></a></td><td class="n"><?= st_pct($top[$c]) ?></td><td class="n"><?= money($rank[$c]) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <p>A flat rate is not the whole story: Illinois has a high rate but taxes no retirement income, Pennsylvania has a low rate but no standard deduction and adds local earned-income taxes, and Ohio exempts the first $26,050 entirely.</p>

      <h2 id="highest-lowest">Highest and lowest top income tax rates</h2>
      <p>The remaining <?= count($prog) ?> jurisdictions use graduated brackets. The highest top rates belong to <?= implode(', ', array_map(fn($c) => e($ST[$c]['name']) . ' (' . st_pct($hiTop[$c]) . ')', array_keys($hiTop))) ?>. The lowest top rates among states that tax wages are <?= implode(', ', array_map(fn($c) => e($ST[$c]['name']) . ' (' . st_pct($loTop[$c]) . ')', array_keys($loTop))) ?>.</p>
      <p>Top rates grab headlines, but they often apply only to very high incomes — California’s 13.3% starts above $1 million. For most households the bottom and middle brackets, the size of the standard deduction and local taxes matter more, which is why the $75,000 table above is a better guide to what you will actually pay.</p>

      <h2 id="example">Worked example: $75,000 in California</h2>
      <p>A single California resident earning $75,000 of wages subtracts the <?= money($ca['std']) ?> California standard deduction, leaving <?= money($ca['taxable']) ?> of taxable income. The brackets work out like this:</p>
      <ul>
<?php foreach ($ca['layers'] as $l): if ($l['amount'] <= 0) continue; ?>
        <li><?= st_pct($l['rate']) ?> on <?= money($l['amount']) ?> = <?= money($l['tax'], 2) ?></li>
<?php endforeach; ?>
        <li>Tax before credits <?= money($ca['taxBefore']) ?>, minus the <?= money($ca['credits']) ?> personal exemption credit = <strong><?= money($ca['tax']) ?></strong> of California tax (<?= number_format($ca['effective'] * 100, 2) ?>% effective).</li>
        <li>Add federal income tax of <?= money($ca['fed']['tax']) ?> and FICA of <?= money($ca['fed']['fica']) ?>: take-home pay is about <strong><?= money($ca['net']) ?></strong> a year, or <?= money($ca['net'] / 12) ?> a month.</li>
      </ul>

      <h2 id="changes"><?= $Y ?> state income tax changes</h2>
      <p>State income taxes are falling in much of the country. Changes reflected in the calculator for <?= $Y ?> include:</p>
      <ul>
        <li><strong>Rate cuts effective January 1:</strong> Indiana (2.95%), Kentucky (3.5%), Mississippi (4%), Montana (5.65% top), Nebraska (4.55% top), North Carolina (3.99%), Oklahoma (three brackets, 4.5% top) and Ohio, which moved to a single 2.75% rate above $26,050.</li>
        <li><strong>Cuts enacted in 2026 and made retroactive:</strong> Georgia (4.99%, with a bigger standard deduction), Utah (4.45%), West Virginia (every rate down 5%, top 4.58%), Arkansas (3.7% top) and South Carolina, which replaced its 6% top rate with a 1.99% / 5.21% structure and a new income-adjusted deduction.</li>
        <li><strong>Bigger deductions:</strong> Hawaii roughly doubled its standard deduction to $8,000 single, and Arizona re-conformed to the larger federal standard deduction.</li>
        <li><strong>New York</strong> trimmed its five lowest rates for <?= $Y ?>, and <strong>Massachusetts</strong> raised its surtax threshold to $1,107,750.</li>
      </ul>

      <h2 id="local">Local income taxes</h2>
      <p>In about a dozen states, cities, counties or school districts add their own income tax. The biggest are New York City (3.078%–3.876%), Maryland’s counties (2.25%–3.3%), Pennsylvania’s local earned-income taxes (Philadelphia about 3.74%), Ohio’s municipal taxes (often 2%–2.5%), Michigan’s city taxes (Detroit 2.4%), Kentucky’s occupational taxes, Indiana’s county taxes and the Portland, Oregon metro taxes on high earners. Use the NYC checkbox or the local rate box to include them — local tax can add 1% to 4% of income.</p>

      <h2 id="two-states">Living in one state and working in another</h2>
      <p>Generally your <strong>home state taxes all of your income</strong>, the state where you work taxes the wages earned there, and your home state gives you a credit for tax paid to the work state so you aren’t taxed twice on the same dollars. You end up paying roughly the higher of the two states’ taxes. Some neighboring states have <strong>reciprocity agreements</strong> — for example Pennsylvania with New Jersey, Maryland, Ohio, Indiana, Virginia and West Virginia — under which you pay only your home state. Remote workers should also watch for “convenience of the employer” rules in states such as New York, which can tax remote days worked for a New York employer.</p>

      <h2 id="lower">How to lower your state income tax</h2>
      <ul>
        <li><strong>Contribute pre-tax to a 401(k), 403(b) or HSA.</strong> Traditional contributions reduce state taxable income in every income-tax state except Pennsylvania (and California and New Jersey tax HSA contributions).</li>
        <li><strong>Check state-only deductions and credits</strong> — 529 plan deductions, renter’s credits, state earned-income credits and retirement-income exclusions are common.</li>
        <li><strong>Mind your residency.</strong> Moving to a lower-tax state only works if you truly change your domicile; keep records of where you live and work.</li>
        <li><strong>Plan the timing of big income</strong> such as bonuses, Roth conversions or asset sales, especially in states with steep top brackets or surtaxes.</li>
      </ul>
      <p>For the federal side, see the <a href="/calculators/federal-income-tax/">federal income tax calculator</a>, or model your per-check withholding with the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>.</p>

      <h2 id="state-pages">State income tax calculators by state</h2>
      <ul class="pill-links">
<?php foreach ($ST as $c => $s): ?>
        <li><a href="/calculators/state-income-tax/<?= $s['slug'] ?>/"><?= e($s['name']) ?></a></li>
<?php endforeach; ?>
      </ul>

<?= faq_block([
  ['Which states have no state income tax?', '<p>Nine states don’t tax wages: ' . strip_tags($names($none)) . '. Washington does tax large long-term capital gains, and New Hampshire’s interest and dividends tax ended after 2024.</p>'],
  ['Which state has the highest income tax?', '<p>California has the highest top rate at 13.3% (including the 1% mental health surcharge on income over $1 million), followed by ' . implode(', ', array_map(fn($c) => e($ST[$c]['name']) . ' (' . st_pct($hiTop[$c]) . ')', array_slice(array_keys($hiTop), 1, 3))) . '. On a typical $75,000 salary, though, ' . e($ST[$hi75]['name']) . ' takes the most at about ' . money($rank[$hi75]) . ' for a single filer.</p>'],
  ['How much state tax will I pay on $75,000?', '<p>Anywhere from $0 in the nine no-tax states to about ' . money($rank[$hi75]) . ' in ' . e($ST[$hi75]['name']) . ' for a single filer. The average among states with an income tax is about ' . money($avg75) . ', an effective rate near ' . number_format($avg75 / 750, 1) . '%. Use the calculator for your exact state and filing status.</p>'],
  ['Is state income tax calculated on gross or taxable income?', '<p>On state taxable income: most states start from federal adjusted gross income (gross pay minus pre-tax 401(k), HSA and similar contributions), then subtract a state standard deduction and exemptions before applying their rates. Pennsylvania is a notable exception that taxes 401(k) contributions.</p>'],
  ['Does this include city and local income taxes?', '<p>Yes, optionally. For New York you can add New York City resident tax or the Yonkers surcharge with a checkbox, and for any state you can enter a local rate — for example a Pennsylvania earned-income tax, an Ohio municipal tax or a Maryland county rate.</p>'],
  ['How accurate is this state income tax calculator?', '<p>It uses each state’s published ' . $Y . ' brackets, standard deductions and exemptions (or the latest 2025 indexed amounts where ' . $Y . ' figures aren’t out yet), and models the main phase-outs. It does not include every state credit, itemized deductions or special income types, so treat it as a planning estimate and confirm with your state return or a tax professional.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('state-income-tax', ['federal-income-tax', 'paycheck-calculator', 'salary-to-hourly', 'tax-refund-calculator', 'bonus-tax-calculator', '1099-tax-calculator']) ?></div>
