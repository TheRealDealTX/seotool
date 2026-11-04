<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$pct = fn(float $x, int $dp = 1): string => number_format($x * 100, $dp) . '%';
/* Example: online seller reconciling a 1099-K to Schedule C. */
$gross = 28500; $txns = 260; $refunds = 900; $fees = 3100; $ship = 2200;
$beg_inv = 2500; $purch = 9800; $end_inv = 3300;
$cogs = $beg_inv + $purch - $end_inv;
$net_receipts = $gross - $refunds;
$gross_profit = $net_receipts - $cogs;
$net = $gross_profit - $fees - $ship;
$se_base = $net * 0.9235;
$se = min($se_base, $Y['ssWageBase']) * 0.124 + $se_base * 0.029;
/* Personal-items example. */
$pers = 3400; $pers_cost = 7900;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">Form 1099-K reports payments you received through credit card processors, payment apps and online marketplaces such as PayPal, Venmo, Etsy, eBay and Amazon. Getting a 1099-K does not mean you owe tax on every dollar shown, and not getting one does not mean your sales are tax-free. This guide explains who sends a 1099-K for <?= TAX_YEAR ?>, the restored $20,000 and 200-transaction threshold, and how to report business sales, personal items and payments that should never have been on the form.</p>

<div class="callout"><?= icon('receipt') ?><p><strong>Quick answer:</strong> payment apps and marketplaces must file a 1099-K only when your payments for goods or services exceed <?= money(20000) ?> <em>and</em> 200 transactions in a calendar year. Card processors that pay merchants directly report every amount. Business income goes on Schedule C, personal items sold at a gain go on Form 8949 and Schedule D, and personal items sold at a loss or payments reported in error are zeroed out on Schedule 1.</p></div>

<h2 id="what-is-1099-k">What is Form 1099-K?</h2>
<p>Form 1099-K, "Payment Card and Third Party Network Transactions," is an information return filed by payment settlement entities. There are two kinds of filers:</p>
<ul>
<li><strong>Merchant acquiring entities</strong> process credit and debit card payments for businesses (the companies behind your card reader or online checkout). They report all payment card transactions, with no minimum threshold.</li>
<li><strong>Third-party settlement organizations (TPSOs)</strong> are payment apps and marketplaces that settle payments between buyers and sellers: PayPal, Venmo and Cash App business or "goods and services" payments, Etsy, eBay, Amazon, StubHub, Airbnb, rideshare and delivery apps, and similar platforms. They report only when you exceed the threshold.</li>
</ul>
<p>Bank-to-bank services that never hold the money, such as Zelle, generally do not issue Form 1099-K. Income received that way is still taxable if it is business income. The form is due to recipients by January 31, so <?= TAX_YEAR ?> forms arrive in early <?= TAX_YEAR + 1 ?>.</p>

<h2 id="threshold">The 2026 1099-K threshold: $20,000 and 200 transactions</h2>
<p>For years, TPSOs reported only sellers with more than $20,000 in gross payments and more than 200 transactions. A 2021 law would have lowered that to $600 with no transaction minimum, and the IRS delayed it repeatedly, announcing a phase-down of $5,000 for 2024, $2,500 for 2025 and $600 for <?= TAX_YEAR ?>.</p>
<p>The One Big Beautiful Bill Act (OBBBA), signed July 4, 2025, reversed course. It retroactively reinstated the original test, so a TPSO must file a 1099-K only when, for the calendar year, a payee has:</p>
<div class="table-wrap"><table>
<thead><tr><th>Who files</th><th>Federal reporting threshold</th></tr></thead>
<tbody>
<tr><td>Payment apps and online marketplaces (TPSOs)</td><td>More than <?= money(20000) ?> in gross payments <b>and</b> more than 200 transactions</td></tr>
<tr><td>Card processors (merchant acquirers)</td><td>No threshold: all payment card transactions</td></tr>
</tbody></table></div>
<p>Both TPSO conditions must be met. A seller with <?= money(30000) ?> from 150 sales, or <?= money(8000) ?> from 400 sales, should not receive a federal 1099-K from that platform. The threshold applies per platform, so a seller using three marketplaces could fall under each one's threshold while earning far more in total.</p>
<div class="callout warn"><?= icon('shield') ?><p><strong>State thresholds may differ.</strong> Some states require platforms to issue a 1099-K at much lower amounts, in some cases $600, so you may receive a state-driven form even if you are under the federal threshold. And regardless of any form, all business income is taxable.</p></div>

<h2 id="boxes">Reading your 1099-K, box by box</h2>
<div class="table-wrap"><table>
<thead><tr><th>Box</th><th>What it shows</th></tr></thead>
<tbody>
<tr><td><b>1a</b></td><td>Gross amount of payment card or third-party network transactions: the total before fees, refunds, shipping or chargebacks</td></tr>
<tr><td><b>1b</b></td><td>Card-not-present transactions (online and phone sales)</td></tr>
<tr><td><b>2</b></td><td>Merchant category code describing the type of business</td></tr>
<tr><td><b>3</b></td><td>Number of payment transactions</td></tr>
<tr><td><b>4</b></td><td>Federal income tax withheld (backup withholding, usually because a correct taxpayer ID was not provided)</td></tr>
<tr><td><b>5a–5l</b></td><td>Gross amounts by month, January through December</td></tr>
<tr><td><b>6–8</b></td><td>State, state ID number and state income tax withheld</td></tr>
</tbody></table></div>
<p>The key point is that Box 1a is <strong>gross</strong>. It can include shipping charged to buyers, platform fees, amounts later refunded and, on some platforms, sales tax collected from buyers. You do not pay tax on the gross. You report it and then subtract refunds, cost of goods and expenses so that your return ties back to the form.</p>

<h2 id="personal">Personal payments, reimbursements and gifts</h2>
<p>Money that is not income does not become taxable just because it appears on a 1099-K. Common examples:</p>
<ul>
<li>Splitting rent, utilities, dinner or travel costs with friends or roommates</li>
<li>Reimbursements from family members</li>
<li>Gifts, such as birthday or holiday money (gifts are not income to the recipient)</li>
<li>Moving money between your own accounts</li>
</ul>
<p>Platforms are supposed to exclude these when they are sent as "friends and family" payments, so mark personal transfers that way. If personal payments still end up on a 1099-K, ask the issuer for a corrected form. If you cannot get one, you can report the amount and back it out on Schedule 1 (shown below) and keep records that explain each payment.</p>

<h2 id="selling-personal-items">Selling personal items: gain or loss?</h2>
<p>Selling your own used belongings (clothing, furniture, a bike, electronics) usually produces a loss, because you sell for less than you paid. A loss on personal-use property is not deductible, but it is not taxable either. If you sell an item for more than you paid, such as concert tickets or a collectible, the profit is a capital gain.</p>
<p><strong>Example:</strong> you receive a 1099-K for <?= money($pers) ?> from selling household items that originally cost about <?= money($pers_cost) ?>. You sold everything at a loss, so you owe no tax on it. Report <?= money($pers) ?> on Schedule 1, line 8z ("Form 1099-K personal items sold at a loss") and the same <?= money($pers) ?> on line 24z, so the net effect is zero. Items sold at a gain go on Form 8949 and Schedule D instead.</p>
<p>If you regularly buy items to resell, you are running a business, not selling personal items, and Schedule C applies.</p>

<h2 id="how-to-report">How to report a 1099-K on your tax return</h2>
<div class="table-wrap"><table>
<thead><tr><th>Situation</th><th>Where it goes</th></tr></thead>
<tbody>
<tr><td>Business sales of goods or services (reselling, crafts, freelance work, rideshare)</td><td>Schedule C, line 1 (gross receipts), with refunds on line 2, cost of goods in Part III and fees as expenses; plus Schedule SE</td></tr>
<tr><td>Personal items sold at a gain</td><td>Form 8949 and Schedule D (capital gain)</td></tr>
<tr><td>Personal items sold at a loss</td><td>Schedule 1, line 8z and line 24z, offsetting to zero</td></tr>
<tr><td>Form received in error (personal transfers, reimbursements, gifts)</td><td>Request a correction; otherwise Schedule 1, line 8z and line 24z ("Form 1099-K received in error")</td></tr>
<tr><td>Short-term rental income through a booking platform</td><td>Usually Schedule E; Schedule C if you provide substantial services</td></tr>
</tbody></table></div>
<p>Here is how an online seller with a <?= money($gross) ?> 1099-K (<?= $txns ?> transactions) would reconcile it on Schedule C:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Reconciling a 1099-K to Schedule C</caption>
<tbody>
<tr><td>Line 1: Gross receipts (Box 1a of the 1099-K)</td><td class="n"><?= money($gross) ?></td></tr>
<tr><td>Line 2: Returns and refunds</td><td class="n">−<?= money($refunds) ?></td></tr>
<tr><td>Line 4: Cost of goods sold (<?= money($beg_inv) ?> opening inventory + <?= money($purch) ?> purchases − <?= money($end_inv) ?> closing)</td><td class="n">−<?= money($cogs) ?></td></tr>
<tr><td><b>Line 5/7: Gross profit / gross income</b></td><td class="n"><b><?= money($gross_profit) ?></b></td></tr>
<tr><td>Line 10: Platform and payment processing fees</td><td class="n">−<?= money($fees) ?></td></tr>
<tr><td>Line 27b (Part V): Shipping labels and postage</td><td class="n">−<?= money($ship) ?></td></tr>
<tr><td><b>Line 31: Net profit</b></td><td class="n"><b><?= money($net) ?></b></td></tr>
<tr><td>Self-employment tax on net profit (Schedule SE)</td><td class="n"><?= money($se) ?></td></tr>
</tbody></table></div>
<p>Only the <?= money($net) ?> of profit is taxed, not the <?= money($gross) ?> on the form, though self-employment tax alone is about <?= money($se) ?> before income tax. The <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> adds income tax, the QBI deduction and quarterly payments, and the <a href="/calculators/profit-margin/">profit margin calculator</a> helps price products. Our <a href="/blog/schedule-c-tax-form/">Schedule C tax form guide</a> covers every line.</p>

<h2 id="mismatches">1099-K mismatches and IRS notices</h2>
<p>The IRS matches 1099-K amounts to returns. If the gross on the form does not appear anywhere on your return, you may receive an automated underreporting notice (CP2000) proposing tax on the full amount. Avoid that by:</p>
<ul>
<li><strong>Reporting the gross and subtracting costs,</strong> rather than reporting only net deposits.</li>
<li><strong>Watching for duplicates.</strong> A client who pays through a payment app should not also send you a 1099-NEC for the same payments, because card and app payments are reported on the 1099-K. If both arrive, report the income once and keep records showing the overlap.</li>
<li><strong>Reconciling platform reports.</strong> Download the annual sales, refund and fee reports from each marketplace and keep them with your return.</li>
<li><strong>Fixing wrong forms early.</strong> Contact the issuer (its name and phone number are on the form) for errors in your taxpayer ID, the amount, or payments that were not yours.</li>
</ul>
<p>If you already filed without reporting a 1099-K correctly, an <a href="/blog/amended-tax-return/">amended tax return</a> can fix it.</p>

<h2 id="no-form">Not over the threshold? You may still owe tax</h2>
<p>The restored $20,000 / 200-transaction rule means far fewer casual sellers will get a 1099-K, but it changes only the paperwork. Profit from selling goods or services is taxable, and self-employment tax applies once net self-employment earnings reach $400. Keep your own records of sales, costs and fees. If you expect to owe $1,000 or more, make estimated payments with the <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> or see <a href="/blog/got-a-1099-exactly-what-to-do-next/">Got a 1099? Here is what to do next</a>. Deciding whether side work is a business at all? See <a href="/blog/1099-vs-w2/">1099 vs W-2</a>.</p>

<?= faq_block([
  ['What is the 1099-K threshold for ' . TAX_YEAR . '?', '<p>Payment apps and online marketplaces must issue a federal Form 1099-K only if your payments for goods and services exceed $20,000 and 200 transactions in the calendar year. The One Big Beautiful Bill Act restored this threshold and cancelled the planned drop to $600. Card processors report all card payments, and some states set lower thresholds.</p>'],
  ['Do I have to pay taxes on a 1099-K?', '<p>You pay tax on profit, not on the gross amount in Box 1a. Business income is reduced by refunds, cost of goods and expenses on Schedule C. Personal items sold at a loss and personal payments reported in error are not taxable; you back them out on Schedule 1.</p>'],
  ['Will I get a 1099-K for Venmo or PayPal personal payments?', '<p>You should not. Friends-and-family transfers, gifts and reimbursements are not payments for goods or services and should be excluded. If they show up on a 1099-K, ask for a corrected form or report them on Schedule 1 as received in error and keep records.</p>'],
  ['How do I report a 1099-K for items I sold at a loss?', '<p>Report the 1099-K amount on Schedule 1, line 8z as "Form 1099-K personal items sold at a loss" and the same amount on line 24z, so the net is zero. Items sold at a gain go on Form 8949 and Schedule D.</p>'],
  ['What is the difference between a 1099-K and a 1099-NEC?', '<p>A 1099-NEC is filed by a business that paid you directly for services. A 1099-K is filed by the card processor, app or marketplace that processed the payment. Payments made by card or through a payment app are reported on the 1099-K, not the 1099-NEC, to avoid double reporting.</p>'],
  ['What if I made money selling online but did not get a 1099-K?', '<p>You still report business income. The 1099-K threshold controls only whether the platform files a form; it does not create a tax exemption. Use your platform sales reports to fill out Schedule C.</p>'],
]) ?>
<?= post_close($SLUG, '1099-tax-calculator', ['got-a-1099-exactly-what-to-do-next', 'schedule-c-tax-form', '1099-vs-w2']) ?>
