<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
/* 2 months and 15 days, counting the first day of the tax year (IRS example: Jan 7 -> Mar 21). */
$due = fn(string $start): string => date('F j, Y', strtotime($start . ' +2 months +14 days'));
$starts = [(TAX_YEAR + 1) . '-01-01', (TAX_YEAR + 1) . '-01-07', (TAX_YEAR + 1) . '-04-01', (TAX_YEAR + 1) . '-09-10'];
/* Simplified payroll-tax comparison: $120,000 profit, $60,000 reasonable salary. */
$profit = 120000; $salary = 60000;
$se_base = $profit * 0.9235;
$se = min($se_base, $Y['ssWageBase']) * 0.124 + $se_base * 0.029;
$payroll = min($salary, $Y['ssWageBase']) * 0.124 + $salary * 0.029;
$saved = $se - $payroll;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">IRS Form 2553, <em>Election by a Small Business Corporation</em>, is the one-time filing that turns a corporation or an LLC into an S corporation for federal tax purposes. Once the election is accepted, the business generally stops paying corporate income tax, and its profits pass through to the owners' personal returns on Schedule K-1. Owners who work in the business can also split their income between salary and distributions, which is where most S corp tax savings come from. This guide covers who qualifies, the deadline, how to fill out and file Form 2553, and how to fix a late election.</p>

<div class="callout"><?= icon('building') ?><p><strong>Should you elect at all?</strong> Before filing, compare your tax as a sole proprietor or LLC with an S corporation paying a reasonable salary. The <a href="/calculators/s-corp-tax-savings/">S corp tax savings calculator</a> does this, including payroll taxes and the extra costs of running payroll.</p></div>

<h2 id="eligibility">Who can file IRS Form 2553</h2>
<p>To make an S election, the business must meet all of these requirements on the day the election is made and the day it takes effect:</p>
<div class="table-wrap"><table>
<caption class="sr-only">S corporation eligibility requirements</caption>
<thead><tr><th>Requirement</th><th>Details</th></tr></thead>
<tbody>
<tr><td><b>Domestic entity</b></td><td>A U.S. corporation, or an LLC or other entity eligible to be taxed as a corporation.</td></tr>
<tr><td><b>100 or fewer shareholders</b></td><td>Members of a family can elect to be treated as a single shareholder, and spouses count as one.</td></tr>
<tr><td><b>Only eligible shareholders</b></td><td>Individuals who are U.S. citizens or residents, estates, and certain trusts and tax-exempt organizations. Partnerships, corporations and nonresident aliens cannot be shareholders.</td></tr>
<tr><td><b>One class of stock</b></td><td>All shares must have identical rights to distributions and liquidation proceeds. Differences in voting rights alone are allowed.</td></tr>
<tr><td><b>Not an ineligible corporation</b></td><td>Certain financial institutions, insurance companies and domestic international sales corporations (DISCs) cannot elect.</td></tr>
</tbody></table></div>
<p>The one-class-of-stock rule trips up more LLCs than any other. An LLC operating agreement that gives members unequal distribution rights, or distributions that are not made in proportion to ownership, can put the election at risk. Review the agreement before filing.</p>

<h2 id="deadline">IRS Form 2553 deadline</h2>
<p>Form 2553 must be filed <strong>no more than 2 months and 15 days after the beginning of the tax year</strong> the election is to take effect, or at any time during the tax year before it. For an existing calendar-year business that wants S status starting January 1, that means by March 15. For a new business, the first tax year begins on the earliest date it has shareholders, acquires assets or begins doing business, which is often earlier than the owner expects.</p>
<div class="table-wrap"><table>
<caption class="sr-only">Form 2553 deadline examples</caption>
<thead><tr><th>Tax year begins</th><th>Form 2553 due by</th></tr></thead>
<tbody>
<?php foreach ($starts as $s): ?>
<tr><td><?= date('F j, Y', strtotime($s)) ?></td><td><?= $due($s) ?></td></tr>
<?php endforeach; ?>
</tbody></table></div>
<p>The period counts the first day of the tax year, so a year that begins on January 7 has a deadline of March 21, matching the IRS's own example. If a deadline falls on a weekend or legal holiday, it moves to the next business day. An election filed after the deadline is generally treated as made for the <em>following</em> tax year, unless you qualify for late election relief.</p>

<h2 id="late-election">Late election relief (Rev. Proc. 2013-30)</h2>
<p>Missing the deadline is common, and the IRS provides a simplified fix in Revenue Procedure 2013-30. You can usually get relief if:</p>
<ul>
<li>You file within <strong>3 years and 75 days</strong> of the date the election was meant to take effect;</li>
<li>The business intended to be an S corporation as of that date and failed to qualify only because the form was not filed on time;</li>
<li>You have <strong>reasonable cause</strong> for the late filing and acted diligently to correct it once you discovered it; and</li>
<li>All shareholders reported their income consistently with S corporation status (or will, by amending).</li>
</ul>
<p>To request relief, write "FILED PURSUANT TO REV. PROC. 2013-30" at the top of Form 2553 and explain the reasonable cause in the space provided on the form. In some cases, a late Form 2553 can be attached to a timely filed Form 1120-S, and relief is available beyond 3 years and 75 days for corporations that meet additional conditions. If you do not qualify for the simplified procedure, the alternative is a private letter ruling, which is slower and carries a user fee.</p>

<div class="callout warn"><?= icon('shield') ?><p><strong>Do not wait for the acceptance letter to start acting like an S corp.</strong> If you elect for the current year, the owner-employee's reasonable salary should run through payroll from the effective date. Paying no salary and taking only distributions is one of the most common S corporation problems the IRS looks for.</p></div>

<h2 id="fill-out">How to fill out Form 2553</h2>
<p>The form is four pages, and most small businesses only need Part I:</p>
<ol>
<li><strong>Part I, Election Information:</strong> the corporation's name, address, EIN, date and state of incorporation, the tax year the election takes effect, and the name and title of an officer or legal representative the IRS may contact. An authorized officer signs here.</li>
<li><strong>Shareholder information and consents:</strong> each shareholder's name, address, shares or ownership percentage, the date acquired, Social Security number or EIN, and tax year end. <strong>Every shareholder must sign</strong> a consent, either on the form or on an attached statement.</li>
<li><strong>Part II, Selection of Fiscal Tax Year:</strong> only if the business wants a tax year other than the calendar year, which requires a business purpose or a Section 444 election.</li>
<li><strong>Part III, Qualified Subchapter S Trust (QSST) election:</strong> only if a trust holds shares.</li>
<li><strong>Part IV, Late Corporate Classification Election:</strong> for an entity that also needs late relief for its corporate classification.</li>
</ol>
<h3 id="consents">Shareholder and spouse consents</h3>
<p>The consent requirement is strict. Everyone who is a shareholder when the election is made must consent, and for an election that takes effect earlier in the same year, anyone who owned shares earlier that year must also consent. In the community property states (Arizona, California, Idaho, Louisiana, Nevada, New Mexico, Texas, Washington and Wisconsin), a spouse with a community property interest in the shares must sign a consent too, even if the spouse's name is not on the stock certificate or LLC records. A missing spouse consent is a frequent reason an election is rejected or later found invalid.</p>

<h2 id="llc">Form 2553 for an LLC</h2>
<p>An LLC with one owner is taxed as a sole proprietorship by default, and an LLC with two or more owners as a partnership. To be taxed as an S corporation, the LLC must be classified as a corporation and then elect S status. You do <strong>not</strong> need to file Form 8832 first: under the IRS regulations, an eligible entity that files a timely Form 2553 is treated as having also elected to be classified as a corporation. Filing Form 2553 alone is enough.</p>
<p>The LLC keeps its legal form under state law. Only its federal tax treatment changes: it files Form 1120-S, issues K-1s to owners (see our <a href="/blog/k1-tax-form/">K-1 tax form guide</a>) and runs payroll for owners who work in the business, instead of reporting profit on <a href="/blog/schedule-c-tax-form/">Schedule C</a>.</p>

<h2 id="where-to-file">Where to file Form 2553</h2>
<p>Form 2553 is filed by <strong>mail or fax</strong> with the IRS service center assigned to the state where the business has its principal office. The correct address and fax number are listed on the IRS "Where to File Your Taxes for Form 2553" page and in the form instructions, and they change from time to time, so check the current page before sending. Keep proof of filing: a fax confirmation or certified mail receipt can save the election if the IRS says it never received it.</p>
<p>A few states require their own S election as well; New York, for example, uses Form CT-6. Check your state's rules when you file the federal form.</p>

<h2 id="acceptance">After you file: CP261 and what comes next</h2>
<p>When the IRS accepts the election, it mails <strong>Notice CP261</strong> confirming the S corporation status and the effective date. The form instructions say you should be notified within 60 days of filing (or 90 days if you also requested a fiscal year). If you have not heard back within that window, call the IRS Business and Specialty Tax Line at 800-829-4933 to check. Keep the CP261 permanently, since banks, lenders and future buyers may ask for it.</p>
<p>Once the election is in place:</p>
<ul>
<li><strong>File Form 1120-S</strong> each year by March 15 for calendar-year corporations, and give each shareholder a Schedule K-1.</li>
<li><strong>Pay a reasonable salary</strong> through payroll to owners who provide services, with income tax withholding and FICA. The salary should reflect what the business would pay someone else for the same work.</li>
<li><strong>Plan for estimated tax.</strong> Salary has withholding, but K-1 profit and distributions do not, so many owners make quarterly payments on their share of the profit. The <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> helps size them.</li>
<li><strong>Keep the election valid</strong> by avoiding ineligible shareholders and disproportionate distributions.</li>
<li><strong>Revoking</strong> requires the consent of shareholders holding more than half the shares. After a revocation or termination, the business generally must wait five years to elect again without IRS consent.</li>
</ul>

<h2 id="savings">Why owners file Form 2553: the payroll tax math</h2>
<p>The main federal saving comes from self-employment tax. A sole proprietor or single-member LLC pays 15.3% self-employment tax on most of its profit (up to the Social Security wage base of <?= money($Y['ssWageBase']) ?> for <?= TAX_YEAR ?>, plus 2.9% above it). An S corporation owner pays the same 15.3% only on salary, while distributions are not subject to payroll tax.</p>
<div class="table-wrap"><table>
<caption class="sr-only">Simplified S corporation payroll tax comparison</caption>
<thead><tr><th><?= money($profit) ?> of profit</th><th class="n">Sole prop / LLC</th><th class="n">S corp, <?= money($salary) ?> salary</th></tr></thead>
<tbody>
<tr><td>Earnings subject to Social Security and Medicare</td><td class="n"><?= money($se_base) ?></td><td class="n"><?= money($salary) ?></td></tr>
<tr><td>Self-employment or payroll tax (both halves)</td><td class="n"><?= money($se) ?></td><td class="n"><?= money($payroll) ?></td></tr>
<tr class="total"><td><b>Difference before other costs</b></td><td class="n" colspan="2"><b><?= money($saved) ?></b></td></tr>
</tbody></table></div>
<p>This is a simplified illustration. It ignores the income tax effects (the deductible half of self-employment tax, the employer's payroll tax deduction and the qualified business income deduction, which can shrink when profit is paid as salary), state taxes, unemployment taxes, and the cost of payroll services and an 1120-S return. A salary that is set unreasonably low to boost the savings invites IRS scrutiny. The <a href="/calculators/s-corp-tax-savings/">S corp calculator</a> includes more of these factors, and the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a> shows your current self-employment tax. For the employee vs contractor side of the question, see <a href="/blog/1099-vs-w2/">1099 vs W-2</a>.</p>

<?= faq_block([
  ['What is IRS Form 2553?', '<p>IRS Form 2553, Election by a Small Business Corporation, is the form a corporation or eligible LLC files to be taxed as an S corporation. Once accepted, profits pass through to the shareholders\' personal returns and the business generally does not pay federal corporate income tax.</p>'],
  ['When is Form 2553 due?', '<p>No more than 2 months and 15 days after the beginning of the tax year the election is to take effect, or any time in the prior tax year. For a calendar-year business electing for January 1, that is March 15 (or the next business day). Late elections may qualify for relief under Rev. Proc. 2013-30 within 3 years and 75 days.</p>'],
  ['Do I need to file Form 8832 before Form 2553?', '<p>No. An LLC that files a timely Form 2553 is automatically treated as having elected corporate classification, so a separate Form 8832 is not required.</p>'],
  ['How long does it take for Form 2553 to be approved?', '<p>The IRS instructions say you should be notified within 60 days of filing, or 90 days if you requested a fiscal tax year. Approval comes as Notice CP261. If you have not received it, call the Business and Specialty Tax Line at 800-829-4933.</p>'],
  ['Can I file Form 2553 online?', '<p>Form 2553 is generally filed by mail or fax to the IRS address for your state, listed on the IRS "Where to File Your Taxes for Form 2553" page. Check that page for the current address, fax number and any newer filing options before sending.</p>'],
  ['Who has to sign Form 2553?', '<p>An authorized officer signs the election, and every shareholder must sign a consent. In community property states, a spouse with a community interest in the shares must consent too. For an election effective earlier in the year, anyone who held shares during that part of the year must also consent.</p>'],
]) ?>
<?= post_close($SLUG, 's-corp-tax-savings', ['k1-tax-form', 'schedule-c-tax-form', '1099-vs-w2']) ?>
