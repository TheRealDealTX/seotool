"""Blog posts. The two WordPress-era slugs are kept; both were rewritten and fact-checked."""
import re
from datetime import date
import lib
from lib import (FLOAT_RATE_S, JUDG_RATE_S, RATE_MONTH, FLOAT_RATE, OCCC_RATES, MONTHS, btn, page_hero, faq_block,
                 cta_band, breadcrumbs, article_body, money, interest, esc, sec_head, FIRM)


def _rate(y, m):
    return OCCC_RATES[y][m - 1]


def fl_hist_rows():
    picks = [(2017, 9), (2018, 11), (2019, 2), (2019, 11), (2022, 9), (2022, 12), (2023, 5), (2023, 9), (2024, 11),
             (2025, 2), (2025, 12), (2026, 1), (lib.RATE_Y, lib.RATE_M + 1)]
    seen, rows = set(), []
    for y, m in picks:
        if (y, m) in seen:
            continue
        seen.add((y, m))
        v = _rate(y, m)
        rows.append(f'<tr><td>{MONTHS[m - 1]} {y}</td><td class="num">{v:.2f}%</td><td class="num"><strong>{v + 5:.2f}%</strong></td></tr>')
    return "".join(rows)


def daily_table(rate):
    rows = ""
    for amt in (10000, 25000, 50000, 100000, 250000):
        rows += (f'<tr><td class="num">{money(amt, False)}</td><td class="num">{money(interest(amt, rate, 1))}</td>'
                 f'<td class="num">{money(interest(amt, rate, 30))}</td><td class="num">{money(interest(amt, rate, 90))}</td>'
                 f'<td class="num">{money(interest(amt, rate, 365))}</td></tr>')
    return ('<div class="table-scroll"><table><thead><tr><th>Late amount</th><th>Per day</th><th>30 days</th><th>90 days</th>'
            f'<th>1 year</th></tr></thead><tbody>{rows}</tbody></table></div>')


POSTS = []


def post(slug, title, h1, desc, published, section, prose, faqs, image=None, card=None, tool=None, modified=None):
    POSTS.append(dict(slug=slug, title=title, h1=h1, desc=desc, published=published, section=section, prose=prose,
                      faqs=faqs, image=image, card=card, tool=tool, modified=modified))


# ===================================================================== 1. 18% standard rate
post("18-standard-rate-explained",
     "18% Standard Rate Explained: Texas Late Claim Interest",
     "The 18% standard rate, <em>explained</em>",
     "How the 18% prompt-payment interest rate in Texas Insurance Code §542.060(a) works: when it applies, when it "
     "starts, how to calculate it, partial payments, supplements and attorney's fees.",
     "2026-04-30", "Interest rates", f'''
<p class="lede">Most policyholders focus on getting a claim approved. Texas law also cares about <em>when</em> it is paid.
If a liable insurer misses the payment deadlines in Chapter 542, §542.060(a) adds interest at 18% a year on the late
amount, plus reasonable attorney&rsquo;s fees. Here is exactly how that works.</p>
<div class="keybox"><h2>In short</h2><ul>
<li><strong>Where:</strong> Texas Insurance Code §542.060(a), part of the Prompt Payment of Claims Act.</li>
<li><strong>Rate:</strong> 18% a year, simple interest, as damages &mdash; plus reasonable and necessary attorney&rsquo;s fees.</li>
<li><strong>Applies to:</strong> non-weather claims, and weather claims made before September 1, 2017.</li>
<li><strong>Runs from:</strong> the date payment was required until the amount is paid.</li></ul></div>

<h2>What the 18% standard rate is</h2>
<p>Section 542.060(a) reads, in part: if an insurer &ldquo;that is liable for a claim under an insurance policy is not in
compliance with this subchapter, the insurer is liable to pay the holder of the policy &hellip; in addition to the amount of
the claim, interest on the amount of the claim at the rate of 18 percent a year as damages, together with reasonable and
necessary attorney&rsquo;s fees.&rdquo;</p>
<p>Three details matter:</p>
<ul><li><strong>It is &ldquo;as damages.&rdquo;</strong> The 18% is a statutory consequence of non-compliance, not a
contractual interest term.</li>
<li><strong>It requires liability.</strong> The insurer has to be liable for the claim. A claim found invalid in
arbitration or litigation doesn&rsquo;t trigger it (§542.058(b)).</li>
<li><strong>It is in addition to the claim.</strong> The policy benefits are paid in full; the interest comes on top.</li></ul>

<h2>When does 18% apply instead of the floating rate?</h2>
<p>Since September 1, 2017, Texas has had two rates. The floating rate in §542.060(c) &mdash; the §304.003 judgment rate
plus 5%, currently {FLOAT_RATE_S} &mdash; applies in actions governed by Chapter 542A: claims for damage caused wholly or
partly by forces of nature, made on or after September 1, 2017. Everything else stays at 18%:</p>
<div class="table-scroll"><table><thead><tr><th>Claim</th><th>Rate</th></tr></thead><tbody>
<tr><td>House fire (cooking, electrical, arson)</td><td><strong>18%</strong></td></tr>
<tr><td>Burst pipe, water heater, appliance leak</td><td><strong>18%</strong></td></tr>
<tr><td>Theft, vandalism, vehicle into the house</td><td><strong>18%</strong></td></tr>
<tr><td>Hail, wind, hurricane, tornado, flood &mdash; claim made before 9/1/2017</td><td><strong>18%</strong></td></tr>
<tr><td>Hail, wind, hurricane, tornado, flood &mdash; claim made on/after 9/1/2017</td><td>Floating ({FLOAT_RATE_S})</td></tr>
<tr><td>Wildfire or lightning &mdash; claim made on/after 9/1/2017</td><td>Floating ({FLOAT_RATE_S})</td></tr>
</tbody></table></div>

<h2>When the 18% starts: it isn&rsquo;t always &ldquo;day 61&rdquo;</h2>
<p>You will often read that interest &ldquo;starts on day 61.&rdquo; That is a useful shorthand for §542.058, but the
precise rule is that interest runs from the <strong>date the claim was required to be paid</strong>, which depends on which
deadline was missed:</p>
<ul><li><strong>§542.058:</strong> more than 60 days after the insurer received all the items, statements and forms it
reasonably requested &mdash; not 60 days after you reported the claim.</li>
<li><strong>§542.057:</strong> 5 business days after the insurer notified you it would pay all or part of the claim. That
can be much earlier than 60 days.</li>
<li><strong>Catastrophes:</strong> in a commissioner-declared weather catastrophe the claim-handling deadlines extend by 15
days (§542.059(b)).</li></ul>
<p>The <a href="/tools/claim-deadline-calculator/">claim deadline calculator</a> works these out from your dates.</p>

<h2>How to calculate 18% interest</h2>
<blockquote><p>late amount &times; 0.18 &divide; 365 &times; days late</p><cite>simple interest, accruing daily</cite></blockquote>
{daily_table(18)}
<p>Example: a $30,000 fire claim should have been paid by June 1 and is paid 120 days late. Interest =
$30,000 &times; 0.18 &divide; 365 &times; 120 = <strong>{money(interest(30000, 18, 120))}</strong>, on top of the $30,000.</p>

<h2>Partial payments don&rsquo;t stop the clock</h2>
<p>A partial payment reduces the balance that interest runs on &mdash; from the date it is paid. It doesn&rsquo;t end the
interest on what is still owed. The Texas Supreme Court confirmed in <em>Hinojos v. State Farm Lloyds</em>, 619 S.W.3d 651
(Tex. 2021), that a reasonable payment made within the deadline doesn&rsquo;t shield the insurer from liability on amounts it
owed but hadn&rsquo;t paid when the deadline passed. The <a href="/statutory-damages-calculator/">statutory interest
calculator</a> handles any number of partial payments.</p>

<h2>Supplements, appraisal and the 18% rate</h2>
<p>When the claim grows &mdash; through a supplement for hidden damage, or an appraisal award higher than what was paid
&mdash; the additional money is still money the insurer was liable for. If it was paid after its deadline, the 18% can apply
to it. Paying an appraisal award doesn&rsquo;t, by itself, end prompt-payment liability (<em>Barbara Technologies Corp. v.
State Farm Lloyds</em>, 589 S.W.3d 806 (Tex. 2019)). See <a href="/post-appraisal-interest-recovery/">post-appraisal
interest</a> and <a href="/long-term-claim-supplements/">supplements</a>.</p>

<h2>Attorney&rsquo;s fees</h2>
<p>§542.060(a) also makes the insurer liable for reasonable and necessary attorney&rsquo;s fees, taxed as costs if suit is
filed (§542.060(b)). That fee exposure is a major reason carriers resolve documented prompt-payment issues. (Weather claims
under Chapter 542A have their own fee formula in §542A.007.)</p>

<h2>Is the 18% automatic?</h2>
<p>The liability arises by statute once the conditions are met &mdash; but carriers rarely calculate or pay it unprompted.
In practice it is raised with a documented timeline and a calculation, and if necessary in a lawsuit. That documentation
is what Enforce Interest prepares.</p>

<h2>Protecting your right to the 18%</h2>
<ol><li>Give notice in writing and keep proof of the date.</li><li>Answer every request in writing, and note the date the
insurer received your response.</li><li>Keep every payment letter and check stub.</li><li>Ask in writing what else the
insurer needs.</li><li>Don&rsquo;t assume a check is the final payment &mdash; compare it to your estimate.</li></ol>''',
     [("Is the 18% compounded?", "<p>No. It is simple interest on the late amount.</p>"),
      ("Does the 18% apply to hail claims?", f"<p>Only to hail claims made before September 1, 2017. Later hail claims use the "
       f"floating §542.060(c) rate, currently {FLOAT_RATE_S}.</p>"),
      ("Does partial payment stop the 18%?", "<p>No. It reduces the balance interest runs on from the date of payment.</p>"),
      ("Do I need an attorney to recover it?", "<p>Not always; many carriers resolve it once it is documented. If a suit is "
       "needed, that is a job for a Texas attorney. Enforce Interest is not a law firm.</p>"),
      ("Are attorney&rsquo;s fees included?", "<p>§542.060 adds reasonable and necessary attorney&rsquo;s fees on top of the interest.</p>")],
     image="18-standard-rate-explained", tool=("/statutory-damages-calculator/", "18% interest calculator",
                                                 "Calculate §542.060(a) interest with partial payments."))

# ===================================================================== 2. Act of God floating rate
post("act-of-god-floating-rate",
     f"Act of God Floating Rate: Texas §542.060(c) ({FLOAT_RATE_S})",
     "The Act of God floating rate, <em>explained</em>",
     f"The Texas 'Act of God' floating interest rate on weather insurance claims: §542.060(c), how it's set ({JUDG_RATE_S} + "
     f"5% = {FLOAT_RATE_S}), which claims it covers, the 2017 cutoff and how it compares with 18%.",
     "2026-04-30", "Interest rates", f'''
<p class="lede">&ldquo;Act of God floating rate&rdquo; is shorthand for one sentence in the Texas Insurance Code: the
interest rate on late-paid weather insurance claims under §542.060(c). It isn&rsquo;t about loans or force-majeure clauses.
It decides how much a Texas insurer owes when it pays a hail, wind, hurricane or flood claim late.</p>
<div class="keybox"><h2>In short</h2><ul>
<li><strong>Formula:</strong> Finance Code §304.003 judgment rate + 5%, simple interest.</li>
<li><strong>Today:</strong> {JUDG_RATE_S} ({RATE_MONTH}) + 5% = <strong>{FLOAT_RATE_S}</strong>.</li>
<li><strong>Range:</strong> 10% to 20%, because §304.003 has a 5% floor and 15% ceiling.</li>
<li><strong>Applies to:</strong> forces-of-nature claims made on or after September 1, 2017, in actions governed by Chapter 542A.</li></ul></div>

<h2>Where the floating rate comes from</h2>
<p>Until 2017, every late-paid Texas claim carried 18%. House Bill 1774 (85th Legislature), effective September 1, 2017,
added Chapter 542A for weather-related property claims and added subsection (c) to §542.060:</p>
<blockquote><p>&ldquo;In an action to which Chapter 542A applies, if an insurer that is liable for a claim under an insurance
policy is not in compliance with this subchapter, the insurer is liable to pay the holder of the policy, in addition to the
amount of the claim, simple interest on the amount of the claim as damages each year at the rate determined on the date of
judgment by adding five percent to the interest rate determined under Section 304.003, Finance Code, together with reasonable
and necessary attorney&rsquo;s fees.&rdquo;</p><cite>Tex. Ins. Code §542.060(c)</cite></blockquote>
<p>The subsection adds that interest &ldquo;accrues beginning on the date the claim was required to be paid.&rdquo;</p>

<h2>Which claims are &ldquo;Act of God&rdquo; claims?</h2>
<p>Chapter 542A defines its claims as first-party claims under a policy covering real property or improvements, paid
directly to the insured, arising from damage &ldquo;caused, wholly or partly, by forces of nature, including an earthquake or
earth tremor, a wildfire, a flood, a tornado, lightning, a hurricane, hail, wind, a snowstorm, or a rainstorm&rdquo;
(§542A.001(2)). Note &ldquo;wholly or partly&rdquo; &mdash; a loss with a mixed cause can qualify. The list is not
exhaustive (&ldquo;including&rdquo;); freeze damage, for example, isn&rsquo;t named, and whether a particular loss qualifies
can be disputed.</p>
<p>Chapter 542A does not apply to actions against the Texas Windstorm Insurance Association (§542A.002(b)), which has its
own remedies.</p>

<h2>The September 1, 2017 cutoff: date of claim, not date of loss</h2>
<p>HB 1774&rsquo;s transition section is specific. Chapter 542A applies to actions filed on or after September 1, 2017, and
&ldquo;Section 542.060(c) &hellip; applies only to a claim &hellip; made on or after the effective date of this Act&rdquo;
(HB 1774, §4). So a weather claim <em>made</em> before that date keeps the 18% rate, even if the dispute was litigated
later. For a storm that hit in August 2017 but was reported in September, the floating rate would apply.</p>

<h2>How the rate is set</h2>
<p>The §304.003 rate is set monthly by the Texas Office of Consumer Credit Commissioner: on the 15th, it takes the prime
rate published by the Federal Reserve Board, floored at 5% and capped at 15%, and that becomes the rate for judgments
rendered the following month. Selected months:</p>
<div class="table-scroll"><table><thead><tr><th>Month</th><th>§304.003 rate</th><th>§542.060(c) rate</th></tr></thead>
<tbody>{fl_hist_rows()}</tbody></table></div>
<p>The full table is on our <a href="/texas-judgment-interest-rate/">Texas judgment interest rate</a> page.</p>
<h3>&ldquo;Determined on the date of judgment&rdquo;</h3>
<p>In a lawsuit, one rate &mdash; the rate in effect on the date the judgment is signed &mdash; applies to the entire
period of delay. It is not averaged across the months the claim sat unpaid. Before judgment, a demand or settlement uses the
current month&rsquo;s rate as the best estimate.</p>

<h2>18% versus the floating rate: what it means in dollars</h2>
<div class="table-scroll"><table><thead><tr><th>Late amount &amp; delay</th><th>At 18%</th><th>At {FLOAT_RATE_S}</th></tr></thead><tbody>
<tr><td>$25,000 &times; 90 days</td><td class="num">{money(interest(25000, 18, 90))}</td><td class="num">{money(interest(25000, FLOAT_RATE, 90))}</td></tr>
<tr><td>$50,000 &times; 180 days</td><td class="num">{money(interest(50000, 18, 180))}</td><td class="num">{money(interest(50000, FLOAT_RATE, 180))}</td></tr>
<tr><td>$100,000 &times; 1 year</td><td class="num">{money(interest(100000, 18, 365))}</td><td class="num">{money(interest(100000, FLOAT_RATE, 365))}</td></tr>
<tr><td>$176,000 &times; 423 days</td><td class="num">{money(interest(176000, 18, 423))}</td><td class="num">{money(interest(176000, FLOAT_RATE, 423))}</td></tr>
</tbody></table></div>

<h2>Why Texas moved to a floating rate</h2>
<p>When HB 1774 was debated, Texas was coming off a wave of hail litigation, and market interest rates had been near zero
for years. Supporters, including insurers and tort-reform groups, argued that a fixed 18% had drifted far above market
rates and encouraged weather-claim lawsuits; tying the penalty to the judgment rate, they said, would keep it meaningful
without being a windfall. Opponents, including consumer advocates, argued that a lower penalty would weaken insurers&rsquo;
incentive to pay storm claims promptly. The compromise kept a penalty at least five points above the judgment rate, with a
10% floor.</p>

<h2>What the floating rate didn&rsquo;t change</h2>
<ul><li>The deadlines in §§542.055&ndash;.058 are the same for weather claims.</li>
<li>Interest still accrues from the date payment was required, and it is still simple interest.</li>
<li>Partial payments and appraisal awards are treated the same way (<em>Hinojos</em>, <em>Barbara Technologies</em>).</li>
<li>Attorney&rsquo;s fees remain available, but subject to Chapter 542A&rsquo;s notice and fee formula.</li></ul>''',
     [("What is the current Texas Act of God floating rate?",
       f"<p>{FLOAT_RATE_S}: the {RATE_MONTH} §304.003 rate of {JUDG_RATE_S} plus 5%.</p>"),
      ("Does the floating rate apply to freeze claims?",
       "<p>Freeze isn&rsquo;t in §542A.001&rsquo;s list of examples (snowstorm is). Whether a freeze loss is a forces-of-nature "
       "claim can be argued either way and affects both the rate and the pre-suit notice requirement.</p>"),
      ("Can the floating rate be higher than 18%?",
       "<p>Yes, in principle: if prime were above 13%, §304.003 plus 5% would exceed 18%, up to a 20% maximum.</p>"),
      ("Is the floating rate set when the claim is late or at judgment?",
       "<p>At judgment. §542.060(c) uses the rate &ldquo;determined on the date of judgment.&rdquo;</p>")],
     image="act-of-god-floating-rate", tool=("/texas-judgment-interest-rate/", "Judgment rate tracker",
                                             "Every monthly §304.003 rate and the matching §542.060(c) rate."))

# ===================================================================== 3. Hinojos
post("hinojos-v-state-farm-lloyds-explained",
     "Hinojos v. State Farm Lloyds Explained (Tex. 2021)",
     "<em>Hinojos v. State Farm Lloyds</em>, explained",
     "What the Texas Supreme Court decided in Hinojos v. State Farm Lloyds, 619 S.W.3d 651 (2021), how it builds on Barbara "
     "Technologies, and what it means for appraisal and partial payments.",
     "2026-10-13", "Case law", f'''
<p class="lede">In March 2021 the Texas Supreme Court decided <em>Hinojos v. State Farm Lloyds</em>, 619 S.W.3d 651. It
answered a question that comes up in almost every disputed property claim: if an insurer pays something on time, and more
is owed later, is the insurer liable for prompt-payment interest on the rest?</p>
<div class="keybox"><h2>The holding in one sentence</h2><p style="margin:0">An insurer is liable under the Texas Prompt
Payment of Claims Act for amounts it owed but had not paid when the statutory deadline expired &mdash; even if it made a
reasonable payment within the deadline and later paid the rest through appraisal.</p></div>

<h2>Background: appraisal and the prompt-payment statute</h2>
<p>Most Texas property policies contain an <strong>appraisal clause</strong>: if the insurer and policyholder disagree on
the amount of loss, each appoints an appraiser, the appraisers choose an umpire, and an agreed or umpire-approved figure
becomes binding on the amount. For years, insurers argued that paying an appraisal award ended the claim &mdash; including
any claim that payment was late.</p>
<p>In 2019 the Supreme Court began rejecting that argument:</p>
<ul><li><strong><em>Barbara Technologies Corp. v. State Farm Lloyds</em>, 589 S.W.3d 806 (Tex. 2019):</strong> paying an
appraisal award is neither an acknowledgment of liability nor a determination that the insurer complied with the statute;
it does not, by itself, bar TPPCA damages.</li>
<li><strong><em>Ortiz v. State Farm Lloyds</em>, 589 S.W.3d 127 (Tex. 2019):</strong> paying the award generally
forecloses breach-of-contract and bad-faith claims for policy benefits (absent an independent injury) &mdash; but not the
TPPCA claim.</li>
<li><strong><em>Alvarez v. State Farm Lloyds</em>, 601 S.W.3d 781 (Tex. 2020):</strong> applied <em>Barbara
Technologies</em>.</li></ul>

<h2>What happened in Hinojos</h2>
<p>Hinojos made a wind and hail claim. State Farm investigated and paid an amount within the statutory period; Hinojos
disputed it and invoked appraisal; the award was higher, and State Farm paid it. Hinojos sued under the TPPCA for interest
on the late-paid amount. The court of appeals sided with State Farm, reasoning that State Farm had made a reasonable
payment on the claim within the sixty-day statutory limit. The Supreme Court reversed and sent the case back.</p>

<h2>The Court&rsquo;s reasoning</h2>
<p>The statute&rsquo;s text drove the result. §542.058 makes an insurer that &ldquo;delays payment of the claim&rdquo; for more
than the allowed period liable under §542.060. The &ldquo;claim&rdquo; is the amount the insurer is liable for under the
policy &mdash; not the amount the insurer chose to pay. So if the insurer was liable for more than it paid by the deadline,
it delayed payment of part of the claim. A good-faith, reasonable estimate doesn&rsquo;t change that, because §542.058 is
a timing statute, and the Act must be &ldquo;liberally construed to promote the prompt payment of insurance claims&rdquo;
(§542.054). Interest is measured on the amount owed but unpaid when the deadline passed.</p>

<h2>What Hinojos means in practice</h2>
<ol><li><strong>Partial payments don&rsquo;t end the analysis.</strong> They reduce the unpaid balance from the date paid.</li>
<li><strong>The appraisal award is evidence of what was owed.</strong> The difference between the award (less deductible)
and what was paid by the deadline is the starting balance for interest.</li>
<li><strong>The deadline still has to be proved.</strong> <em>Hinojos</em> doesn&rsquo;t say when the 60 days started. That
still depends on when the insurer received the items it reasonably requested &mdash; a fact question.</li>
<li><strong>It applies to weather claims.</strong> For Chapter 542A claims the rate is the §542.060(c) floating rate
({FLOAT_RATE_S} using the {RATE_MONTH} rate), but the principle is the same.</li></ol>
<h3>Example</h3>
<p>Deadline: May 21, 2024. Paid by then: $48,000. Award less deductible: $224,000. The $176,000 balance is paid July 18,
2025 &mdash; 423 days later. At {FLOAT_RATE_S}: {money(interest(176000, FLOAT_RATE, 423))}. At 18%:
{money(interest(176000, 18, 423))}.</p>

<h2>After Hinojos: Rodriguez v. Safeco (2024)</h2>
<p>Insurers adapted. In <em>Rodriguez v. Safeco Insurance Co. of Indiana</em> (Tex. Feb. 2, 2024), the Court answered a
certified question from the Fifth Circuit: in a Chapter 542A case, when the insurer pays the appraisal award plus any
statutory interest that could be owed, the insured can&rsquo;t recover attorney&rsquo;s fees under §542A.007, because nothing
remains to be awarded on the claim. The practical result is that many carriers now pay an interest figure with the award.
<em>Hinojos</em> tells you interest is owed; <em>Rodriguez</em> makes it essential to check whether what was paid was
enough &mdash; the right start date, the right rate, every payment credited on the right day.</p>
<p>The <a href="/tools/appraisal-interest-calculator/">appraisal interest calculator</a> has a field for the interest the
carrier already paid and shows any shortfall.</p>''',
     [("What is the citation for Hinojos?", "<p><em>Hinojos v. State Farm Lloyds</em>, 619 S.W.3d 651 (Tex. 2021).</p>"),
      ("Does Hinojos apply if the insurer paid within 60 days?",
       "<p>Yes &mdash; that was the point of the case. A timely, reasonable partial payment doesn&rsquo;t protect the insurer "
       "from liability on amounts it owed but hadn&rsquo;t paid by the deadline.</p>"),
      ("Did Hinojos change the 60-day trigger?",
       "<p>No. When the deadline started is still determined by when the insurer received the items it reasonably requested.</p>")],
     card=("Case law · Tex. 2021", "Hinojos v. State Farm Lloyds, explained"),
     tool=("/tools/appraisal-interest-calculator/", "Appraisal interest calculator", "Apply Hinojos to your own award and payments."))

# ===================================================================== 4. Deadlines
post("texas-insurance-claim-deadlines",
     "Texas Insurance Claim Deadlines: Every Clock in One Place",
     "Texas insurance claim <em>deadlines</em>: every clock in one place",
     "Every Texas insurance claim deadline: reporting the claim, Chapter 542's 15-day, 15-business-day, 5-day and 60-day "
     "rules, catastrophes, TWIA, the 61-day 542A notice and limitations to sue.",
     "2026-10-20", "Deadlines", f'''
<p class="lede">A Texas property claim runs on several clocks at once &mdash; some on the insurer, some on you. Missing one
of yours can cost coverage or the right to sue. Missing one of theirs can cost the insurer statutory interest. Here they
all are, in order.</p>

<h2>Your deadlines: reporting the claim</h2>
<ul><li><strong>Private insurers:</strong> the policy controls. Most require notice &ldquo;promptly&rdquo; or &ldquo;as
soon as practicable,&rdquo; and some Texas policies set a fixed period for weather claims. Read the &ldquo;Duties After
Loss&rdquo; section.</li>
<li><strong>TWIA:</strong> file within one year of the date of damage (§2210.573(a)). The commissioner can extend by up to
180 days for good cause (§2210.205(b)).</li>
<li><strong>Proof of loss:</strong> if the insurer requests a sworn proof of loss, the policy usually sets a deadline (often
60 days from the request).</li></ul>

<h2>The insurer&rsquo;s deadlines: Chapter 542</h2>
<div class="table-scroll"><table><thead><tr><th>Deadline</th><th>Statute</th><th>Trigger</th></tr></thead><tbody>
<tr><td>Acknowledge, start investigating, request items: 15 days (surplus lines 30 business days)</td><td>§542.055</td><td>Written notice of claim</td></tr>
<tr><td>Accept or reject in writing: 15 business days (30 days if arson suspected)</td><td>§542.056</td><td>Receipt of all items required for proof of loss</td></tr>
<tr><td>Decide after a &ldquo;need more time&rdquo; notice: 45 days</td><td>§542.056(d)</td><td>The insurer&rsquo;s notice</td></tr>
<tr><td>Pay: 5 business days (surplus lines 20)</td><td>§542.057</td><td>Notice of acceptance, or performance of a condition</td></tr>
<tr><td>Pay in any event: 60 days</td><td>§542.058</td><td>Receipt of all items reasonably requested</td></tr>
<tr><td>+15 days to each claim-handling deadline</td><td>§542.059(b)</td><td>Commissioner-declared weather catastrophe</td></tr>
</tbody></table></div>
<p>&ldquo;Business day&rdquo; excludes weekends and Texas holidays (§542.051(1)). Use the
<a href="/tools/claim-deadline-calculator/">claim deadline calculator</a> to get exact dates.</p>

<h2>TWIA&rsquo;s deadlines</h2>
<p>TWIA has its own sequence in Chapter 2210: it may request information within 30 days after the claim is filed;
it must accept or deny within 60 days after receiving the claim or the requested information (§2210.573); and it must pay
an accepted claim within 10 days of notice of acceptance (§2210.5731). A suit over denied coverage must be filed within two
years of the denial notice (§2210.577).</p>

<h2>Before you sue: Chapter 542A</h2>
<p>For weather claims, written pre-suit notice at least <strong>61 days</strong> before filing (§542A.003). The insurer may
request an inspection within <strong>30 days</strong> of receiving it, to be completed if reasonably possible within
<strong>60 days</strong> (§542A.004). The <a href="/tools/542a-notice-calculator/">542A calculator</a> does the arithmetic.</p>

<h2>Deadlines to sue</h2>
<ul><li><strong>The policy&rsquo;s suit clause.</strong> Commonly two years and one day after the cause of action accrues.
Texas voids any contractual limit shorter than two years (Civ. Prac. &amp; Rem. Code §16.070).</li>
<li><strong>Insurance Code Chapter 541</strong> (unfair or deceptive practices): two years from the act or its discovery,
extendable 180 days in limited circumstances (§541.162).</li>
<li><strong>Breach of contract:</strong> four years under the general statute, unless a valid policy clause shortens it.</li></ul>
<div class="callout wine"><strong>When does a claim &ldquo;accrue&rdquo;?</strong><p>Often when the insurer denies or
underpays the claim, not the date of loss &mdash; but that is a legal question with real consequences. If a deadline might be
close, talk to a Texas attorney now.</p></div>

<h2>Policy deadlines people forget</h2>
<ul><li><strong>Recoverable depreciation:</strong> many policies require repairs to be completed within a set time (often 180
days to two years) to collect the holdback.</li>
<li><strong>Appraisal:</strong> some policies set a time to name an appraiser after a demand (often 20 days).</li>
<li><strong>Additional living expense:</strong> usually limited to the time reasonably needed to repair, sometimes capped.</li></ul>
<p>Keep all of these in one place with the <a href="/tools/claim-timeline-builder/">claim timeline builder</a>.</p>''',
     [("How long does an insurance company have to pay a claim in Texas?",
       "<p>Five business days after accepting it (§542.057), and in any case no more than 60 days after receiving all items it "
       "reasonably requested (§542.058), plus 15 days in a declared weather catastrophe.</p>"),
      ("How long do I have to sue my insurance company in Texas?",
       "<p>Check your policy; two years and one day from accrual is common, and nothing shorter than two years is enforceable "
       "(§16.070). Chapter 541 claims have a two-year limit.</p>"),
      ("How long do I have to file a TWIA claim?", "<p>One year from the date of damage (§2210.573(a)).</p>")],
     card=("Deadlines · Ch. 542 · 542A · TWIA", "Texas insurance claim deadlines: every clock in one place"),
     tool=("/tools/claim-deadline-calculator/", "Claim deadline calculator", "Your dates, every statutory deadline."))

# ===================================================================== 5. Freeze claim
post("how-long-to-file-a-freeze-claim-in-texas",
     "How Long Do I Have to File a Freeze Claim in Texas?",
     "How long do I have to file a <em>freeze claim</em> in Texas?",
     "Texas freeze and burst-pipe claims: how long you have to report the claim and to sue, freeze exclusions, catastrophe "
     "extensions, which interest rate applies and how to document the loss.",
     "2026-10-27", "Deadlines", f'''
<p class="lede">There is no single Texas statute that says &ldquo;you have X days to file a freeze claim.&rdquo; The answer
comes from your policy, and the policy usually says &ldquo;promptly.&rdquo; Here is what that means in practice, the other
deadlines that matter, and how freeze claims are paid.</p>
<div class="keybox"><h2>Short answer</h2><ul>
<li><strong>Report it as soon as you discover the damage</strong> &mdash; most policies require prompt notice.</li>
<li>Some policies set a fixed reporting window; check the &ldquo;Duties After Loss&rdquo; section.</li>
<li>The deadline to <em>sue</em> is separate &mdash; commonly two years and one day after the claim accrues, and never less than two years (§16.070).</li></ul></div>

<h2>Reporting deadline: what &ldquo;prompt notice&rdquo; means</h2>
<p>Homeowners policies typically require you to give the insurer &ldquo;prompt notice&rdquo; of a loss. That isn&rsquo;t a
fixed number of days; it means reasonably soon given the circumstances. After a widespread freeze like February 2021, a
delay of days or a few weeks while repairs are arranged is common. Months of unexplained delay invite a late-notice defense,
and late notice can make it hard to prove what the freeze caused. Report in writing, even if you can&rsquo;t get an
adjuster out yet.</p>
<p>Some policies now include a fixed outer limit for reporting certain claims. If yours does, that date controls.</p>

<h2>Deadline to sue</h2>
<p>Most policies limit the time to sue to two years and one day after the cause of action accrues; Texas won&rsquo;t enforce
anything shorter than two years (Civ. Prac. &amp; Rem. Code §16.070). Claims under Insurance Code Chapter 541 have a two-year
limit (§541.162). Accrual is often tied to the insurer&rsquo;s denial or underpayment, but get legal advice if you&rsquo;re
anywhere near two years from the freeze.</p>

<h2>Is freeze damage covered?</h2>
<p>Usually, yes &mdash; a pipe that bursts in a freeze is the classic &ldquo;sudden and accidental discharge&rdquo; of water.
Watch for these limits:</p>
<ul><li><strong>Freezing exclusion for unheated or vacant homes.</strong> Many policies exclude freeze damage to plumbing
unless you used reasonable care to maintain heat, or shut off the water and drained the system. During a statewide power
outage, &ldquo;reasonable care&rdquo; is judged against what was possible.</li>
<li><strong>The pipe itself.</strong> Some policies pay for the water damage but not the cost of repairing the pipe or
appliance that froze.</li>
<li><strong>Mold sublimits</strong> if water sat before mitigation.</li>
<li><strong>Flood policies don&rsquo;t cover burst pipes</strong>, and TWIA covers wind and hail only.</li></ul>

<h2>How fast must the insurer pay a freeze claim?</h2>
<p>Chapter 542 applies: acknowledge within 15 days, decide within 15 business days of receiving what it requested, pay
within 5 business days of accepting, and no later than 60 days after receiving requested items. If the commissioner
declared the freeze a weather-related catastrophe, each claim-handling deadline gets 15 more days (§542.059(b)).</p>

<h2>Which interest rate applies to a late freeze claim?</h2>
<p>This is genuinely unsettled. The floating rate in §542.060(c) applies to claims under Chapter 542A, which covers damage
&ldquo;caused, wholly or partly, by forces of nature,&rdquo; listing examples including a snowstorm but not a freeze. An
insurer may argue a winter storm loss is a forces-of-nature claim (floating rate, currently {FLOAT_RATE_S}, plus the 61-day
pre-suit notice); a policyholder may argue a burst pipe is a plumbing loss (18%). The answer can depend on the facts and the
pleadings. When we calculate freeze-claim interest, we show both.</p>
<p>On a $35,000 freeze claim paid 150 days late: {money(interest(35000, 18, 150))} at 18%, or
{money(interest(35000, FLOAT_RATE, 150))} at {FLOAT_RATE_S}.</p>

<h2>Documenting a freeze loss</h2>
<ol><li>Photograph the burst pipe and water damage before repairs; keep the failed section of pipe.</li>
<li>Note the outside temperatures and any power outage dates (utility notices are good evidence).</li>
<li>Keep plumber and mitigation invoices; plumbers&rsquo; notes on the cause are valuable.</li>
<li>Report the claim in writing and log every request and response in the <a href="/tools/claim-timeline-builder/">timeline builder</a>.</li>
<li>Keep receipts for hotels and extra costs if the home was unlivable.</li></ol>''',
     [("How long do I have to file a freeze claim in Texas?",
       "<p>Your policy controls &mdash; usually &ldquo;prompt notice,&rdquo; meaning as soon as reasonably possible after you "
       "discover the damage, and some policies set a fixed outer limit. Report in writing right away.</p>"),
      ("Can I still file a claim for the February 2021 freeze?",
       "<p>Reporting that late will face a late-notice defense, and the time to sue under most policies has likely run. Talk to "
       "a Texas attorney about your specific situation.</p>"),
      ("Does TWIA cover freeze damage?", "<p>No. TWIA policies cover wind and hail. Freeze damage is a homeowners-policy claim.</p>")],
     card=("Deadlines · freeze & burst pipes", "How long do I have to file a freeze claim in Texas?"),
     tool=("/tools/claim-deadline-calculator/", "Claim deadline calculator", "Includes catastrophe extensions."))

# ===================================================================== 6. Smoke damage
post("smoke-damage-claim-texas",
     "Smoke Damage Claims in Texas: Investigations & Payment",
     "Smoke damage claims in Texas: <em>investigations</em>, scope and payment",
     "How smoke damage insurance claims work in Texas: what a smoke damage investigation is, why scope gets disputed, "
     "wildfire smoke, contents and HVAC, and the deadlines and interest when payment is late.",
     "2026-11-02", "Claim types", f'''
<p class="lede">A smoke claim is one of the hardest property claims to see and one of the easiest to under-scope. Soot and
odor travel far beyond the flames &mdash; through returns and ducts, into attics and closed cabinets. Here is how smoke damage
claims are investigated, where they get disputed, and what Texas law says about paying them on time.</p>

<h2>What counts as a smoke claim</h2>
<ul><li><strong>Fire in the home</strong> &mdash; the burned area plus smoke and soot elsewhere in the structure.</li>
<li><strong>Puff-back</strong> from a furnace or water heater that spreads soot through the house.</li>
<li><strong>Neighboring fire</strong> &mdash; an apartment, adjoining unit or nearby building.</li>
<li><strong>Wildfire smoke</strong> &mdash; residue and odor without flames ever reaching the property.</li></ul>
<p>Most homeowners policies cover smoke as part of the fire peril (often excluding smoke from agricultural smudging or
industrial operations). Check your form&rsquo;s exact wording.</p>

<h2>What a smoke damage investigation is</h2>
<p>Because smoke residue is often invisible, the scope of a smoke claim should be based on testing rather than on what looks
dirty. A smoke damage investigation typically includes:</p>
<ul><li><strong>Surface sampling</strong> (tape lifts and wipe samples) analyzed by a lab for soot, char and ash particles.</li>
<li><strong>Mapping</strong> &mdash; samples from rooms near and far from the fire, the attic, wall cavities and HVAC components,
to show how far residue traveled.</li>
<li><strong>HVAC inspection</strong> of the air handler, coils and ducts.</li>
<li><strong>Odor assessment</strong> and a contents evaluation: what can be cleaned and deodorized, and what can&rsquo;t.</li>
<li><strong>A written protocol</strong> describing the cleaning, sealing or replacement each area requires.</li></ul>
<p>Investigations are usually performed by industrial hygienists or environmental consultants. Some insurers hire their
own; policyholders can too. Either way, the report becomes central evidence.</p>

<h2>Why smoke claims get disputed</h2>
<ul><li><strong>Room-by-room scoping.</strong> The carrier pays to clean the fire room and the adjoining hallway; residue in
the rest of the house is called &ldquo;not affected.&rdquo;</li>
<li><strong>Clean versus replace.</strong> Porous materials &mdash; insulation, upholstery, carpet pad, clothing &mdash;
often can&rsquo;t be fully deodorized.</li>
<li><strong>HVAC.</strong> Ducts that circulated smoke may need cleaning or replacement.</li>
<li><strong>Wildfire smoke causation.</strong> Without visible damage, carriers question whether residue is from the fire at
all, which is exactly what lab analysis answers.</li></ul>

<h2>Deadlines and interest on smoke claims</h2>
<p>The Chapter 542 deadlines apply to smoke claims like any other: 15 days to acknowledge and request items, 15 business
days to decide after receiving them (30 days if arson is reasonably suspected), 5 business days to pay after accepting, and
no more than 60 days after receiving the items reasonably requested.</p>
<p>Two practical points:</p>
<ol><li><strong>The investigation report is often the last &ldquo;item&rdquo;.</strong> Send it with a dated cover letter and
ask the adjuster in writing whether anything else is needed. The date the insurer receives the last reasonably requested
item starts the §542.058 clock.</li>
<li><strong>Know the rate.</strong> A house fire or puff-back is a non-weather loss: <strong>18%</strong> a year if paid late.
Wildfire smoke is a forces-of-nature loss under Chapter 542A: the floating rate, currently <strong>{FLOAT_RATE_S}</strong>,
for claims made on or after September 1, 2017.</li></ol>
<p>On a $60,000 smoke supplement paid 100 days late: {money(interest(60000, 18, 100))} at 18%;
{money(interest(60000, FLOAT_RATE, 100))} at {FLOAT_RATE_S}.</p>

<h2>Documenting a smoke claim</h2>
<ol><li>Photograph and video every room, closet and the attic before cleaning starts.</li>
<li>Keep a contents list with photos; set aside items that still smell after cleaning.</li>
<li>Ask for the insurer&rsquo;s testing results if it performs any, and get your own if scope is disputed.</li>
<li>Keep every ALE receipt while the home is uninhabitable.</li>
<li>Log requests and responses in the <a href="/tools/claim-timeline-builder/">claim timeline builder</a>.</li></ol>
<p>More on fire losses in our <a href="/fire-smoke-damage/">fire and smoke damage guide</a>.</p>''',
     [("What is a smoke damage investigation?",
       "<p>A professional assessment, usually by an industrial hygienist, that samples surfaces and air throughout the property "
       "to identify and map soot, char and ash, so the repair scope is based on evidence.</p>"),
      ("Is wildfire smoke damage covered in Texas?",
       "<p>Often, as part of the fire or smoke peril, depending on the policy wording. Wildfire is a forces-of-nature cause, so "
       "Chapter 542A&rsquo;s notice rules and the floating interest rate apply to those claims.</p>"),
      ("How long does an insurer have to pay a smoke claim?",
       "<p>The standard Chapter 542 deadlines apply: 5 business days after acceptance, and no more than 60 days after it receives "
       "the items it reasonably requested.</p>")],
     card=("Claim types · smoke & soot", "Smoke damage claims in Texas: investigations and payment"))

# ===================================================================== 7. 542A notice
post("542a-pre-suit-notice-explained",
     "Texas 542A Pre-Suit Notice Explained (61-Day Rule)",
     "The Texas 542A pre-suit notice, <em>explained</em>",
     "What Texas Insurance Code Chapter 542A requires before a weather-claim lawsuit: the 61-day notice, what it must say, "
     "the inspection window, abatement and the attorney-fee formula.",
     "2026-10-06", "Deadlines", f'''
<p class="lede">Since September 1, 2017, a policyholder who wants to sue over a hail, wind, hurricane or other
forces-of-nature claim in Texas must first send a specific written notice and wait 61 days. Get it wrong and the suit can be
abated and attorney&rsquo;s fees reduced or lost.</p>

<h2>Which claims need a 542A notice</h2>
<p>Chapter 542A applies to actions on first-party claims under policies covering real property or improvements, for damage
caused &ldquo;wholly or partly, by forces of nature&rdquo; &mdash; earthquake or tremor, wildfire, flood, tornado, lightning,
hurricane, hail, wind, snowstorm, rainstorm (§542A.001). It covers breach-of-contract, negligence, misrepresentation and
fraud claims, Insurance Code Chapter 541 and 542 claims and DTPA claims (§542A.002(a)). It doesn&rsquo;t apply to the Texas
Windstorm Insurance Association (§542A.002(b)).</p>

<h2>What the notice must say (§542A.003)</h2>
<ol><li>A statement of the acts or omissions giving rise to the claim.</li>
<li>The specific amount alleged to be owed by the insurer on the claim for damage to or loss of covered property.</li>
<li>The reasonable and necessary attorney&rsquo;s fees incurred, calculated from hours actually worked (per contemporaneous
time records) times a customary hourly rate.</li></ol>
<p>It must be given in writing at least 61 days before suit. If an attorney or representative gives it, they must send the
claimant a copy and say so in the notice. It can be combined with other required notices, and it is admissible in evidence.</p>
<p>No notice is required if there&rsquo;s a reasonable basis to believe limitations will expire before notice could be given,
or the claim is a counterclaim (§542A.003(d)).</p>

<h2>The insurer&rsquo;s inspection (§542A.004)</h2>
<p>Within 30 days of receiving the notice, the insurer may ask in writing to inspect, photograph or evaluate the property.
If reasonably possible, the inspection must be completed within 60 days of when it received the notice.</p>

<h2>Abatement (§542A.005)</h2>
<p>If the insurer didn&rsquo;t get a compliant notice, or asked to inspect and wasn&rsquo;t given a reasonable opportunity, it
can file a plea in abatement within 30 days of answering. A verified plea that isn&rsquo;t controverted by affidavit abates the
case automatically on the 11th day. Abatement lasts until the 60th day after a compliant notice is served or the inspection
is allowed.</p>

<h2>The attorney-fee formula (§542A.007)</h2>
<p>Fees are limited to the least of (1) the fees proved at trial, (2) fees allowed under other law, or (3) the fees
multiplied by a ratio: <strong>amount awarded on the claim &divide; amount demanded in the notice</strong>.</p>
<ul><li>Ratio <strong>0.8 or higher</strong>: full fees (if otherwise recoverable).</li>
<li>Ratio <strong>below 0.2</strong>: no fees.</li>
<li>In between: fees scaled by the ratio.</li>
<li>No proper notice at least 61 days before suit, pleaded and proved by the insurer: no fees incurred after that plea.</li></ul>
<p>Try the formula in the <a href="/tools/542a-notice-calculator/">542A notice &amp; fee calculator</a>.</p>
<div class="callout"><strong>Appraisal and Rodriguez</strong><p>In <em>Rodriguez v. Safeco</em> (Tex. 2024), the Supreme Court
held that when an insurer pays the appraisal award plus any statutory interest that could be owed, the amount
&ldquo;awarded in the judgment&rdquo; on the claim is zero, so §542A.007 permits no fees. The 542A notice and the appraisal
clause now interact closely.</p></div>

<h2>Interest under 542A cases</h2>
<p>In an action governed by Chapter 542A, prompt-payment interest is the floating rate in §542.060(c): the §304.003 rate on
the date of judgment plus 5% &mdash; {FLOAT_RATE_S} using {RATE_MONTH}&rsquo;s {JUDG_RATE_S}. It applies to claims made on or
after September 1, 2017.</p>
<p>The 542A notice is a legal document with consequences for fees and timing. Enforce Interest is not a law firm; we prepare
the claim documentation and interest calculations that support it, and a Texas attorney should draft and send it.</p>''',
     [("How many days before suing must a 542A notice be sent?", "<p>At least 61 days (§542A.003(a)).</p>"),
      ("What happens if I don&rsquo;t send a 542A notice?",
       "<p>The insurer can abate the suit until 60 days after a compliant notice, and may cut off attorney&rsquo;s fees incurred "
       "after it pleads the missing notice (§§542A.005, 542A.007(d)).</p>"),
      ("Does 542A apply to TWIA claims?", "<p>No (§542A.002(b)). TWIA claims follow Chapter 2210.</p>")],
     card=("Deadlines · Chapter 542A", "The Texas 542A pre-suit notice, explained"),
     tool=("/tools/542a-notice-calculator/", "542A notice calculator", "Notice dates and the attorney-fee ratio."))

# ===================================================================== 8. Cancellation 60-day
post("texas-homeowners-insurance-cancellation-rules",
     "Texas Homeowners Policy Cancellation: The Other 60-Day Rule",
     "How long must a Texas policy be in force before it can&rsquo;t be <em>canceled</em>?",
     "In Texas, how long must a homeowners policy be in force? The 60-day cancellation rule in Insurance Code §551.104, "
     "allowed reasons to cancel, notice periods, nonrenewal and the three-claims rule.",
     "2026-11-03", "Policyholder rights", '''
<p class="lede">Texas has more than one &ldquo;60-day rule.&rdquo; Besides the 60-day claim payment deadline in §542.058,
the Insurance Code limits when an insurer can cancel your homeowners policy &mdash; and the line is drawn at 60 days in
force. Here is how it works.</p>
<div class="keybox"><h2>Short answer</h2><ul>
<li><strong>Homeowners and personal auto:</strong> once the policy has been in effect 60 days, the insurer can cancel only
for the reasons listed in §551.104 (for example, nonpayment or a fraudulent claim).</li>
<li><strong>Most other policies:</strong> the free-cancellation window is 90 days (§551.104(g)).</li>
<li><strong>Notice:</strong> a permitted cancellation doesn&rsquo;t take effect until the 10th day after the insurer mails notice (§551.104(e)).</li></ul></div>

<h2>The first 60 days</h2>
<p>A new homeowners policy that has been in effect <strong>less than 60 days</strong> can be canceled if (§551.104(g)):</p>
<ul><li>the insurer identifies a condition that creates an increased risk of hazard, wasn&rsquo;t disclosed in the
application, and isn&rsquo;t the subject of a prior claim; or</li>
<li>before the policy&rsquo;s effective date, the insurer doesn&rsquo;t accept a copy of a required inspection report from a
TREC-licensed or otherwise authorized inspector, dated within 90 days before the effective date. (An inspection report is
considered accepted if the insurer doesn&rsquo;t reject it within 10 days of receiving it, §551.104(h).)</li></ul>
<p>Personal auto policies in effect less than 60 days, and other policies (not auto or homeowners) in effect less than 90
days, can be canceled more freely under the same subsection.</p>

<h2>After 60 days: the only reasons to cancel</h2>
<p>Once past the initial period, an insurer may cancel only if (§551.104(b)&ndash;(c)):</p>
<ol><li>the named insured doesn&rsquo;t pay any part of the premium when due;</li>
<li>the insured submits a fraudulent claim;</li>
<li>the Texas Department of Insurance determines that continuing the policy would violate the Insurance Code or other
insurance law; or</li>
<li>(for policies other than personal auto) there is an increase in the hazard, within the insured&rsquo;s control, that
would raise the premium rate.</li></ol>
<p>Filing a legitimate claim is not on the list. Under §551.103, &ldquo;cancellation&rdquo; also includes refusing coverage
you&rsquo;re entitled to or reducing coverage by endorsement mid-term without your consent.</p>

<h2>Nonrenewal is different</h2>
<p>An insurer can decline to renew at the end of the term, but it must mail written notice of nonrenewal at least
<strong>60 days</strong> before the policy expires; otherwise it must renew at your request (§551.105).</p>
<h3>The three-claims rule</h3>
<p>For standard fire, homeowners and farm and ranch owners policies, an insurer may refuse to renew if you filed three or
more claims in a three-year period &mdash; but only if it warned you in writing after the second claim (§551.107). Claims
caused by natural causes, claims filed but not paid, and certain properly remediated appliance-related water claims
don&rsquo;t count. The insurer may also add an actuarially based surcharge at renewal after two or more claims in three
policy years.</p>

<h2>Why this matters for claims</h2>
<p>Fear of losing coverage keeps some policyholders from reporting legitimate losses or pushing back on underpayments. The
cancellation rules mean a policy in force more than 60 days can&rsquo;t be canceled mid-term for filing a claim, and weather
claims don&rsquo;t count toward the three-claims nonrenewal rule. Report losses promptly and document them well.</p>
<p>And if your claim was paid late, the other 60-day rule may owe you interest. <a href="/does-my-claim-qualify/">Check
whether your claim qualifies</a>.</p>''',
     [("In Texas, how long must a homeowners policy be in force before it can only be canceled for specific reasons?",
       "<p>60 days. After that, cancellation is limited to the reasons in §551.104(b)&ndash;(c), such as nonpayment or fraud.</p>"),
      ("Can my insurer cancel my policy because I filed a claim?",
       "<p>Not mid-term for a legitimate claim once the policy has been in force 60 days. Claims history can affect renewal "
       "under §551.107, but natural-cause claims don&rsquo;t count.</p>"),
      ("How much notice must a Texas insurer give before nonrenewal?", "<p>At least 60 days before expiration (§551.105).</p>")],
     card=("Policyholder rights · §551.104", "Texas homeowners policy cancellation: the other 60-day rule"))


def read_minutes(html):
    words = len(re.sub(r"<[^>]+>", " ", html).split())
    return max(3, round(words / 230))


def build(ctx):
    mc = ctx["make_card"]
    out = []
    for p in POSTS:
        path = f"/blog/{p['slug']}/"
        trail = [("Home", "/"), ("Blog", "/blog/"), (re.sub(r"<[^>]+>", "", p["h1"]).replace("&rsquo;", "'"), path)]
        _, bc = breadcrumbs(trail)
        h1_plain = re.sub(r"<[^>]+>", "", p["h1"]).replace("&rsquo;", "'").replace("&amp;", "&")
        if p["image"]:
            og = p["image"]
        else:
            og = mc("post-" + p["slug"], p["card"][0], p["card"][1], size=(1200, 800))
        fh, fl = faq_block(p["faqs"]) if p["faqs"] else ("", None)
        modified = p["modified"] or lib.BUILD_DATE
        d = date.fromisoformat(p["published"])
        date_h = f"{MONTHS[d.month - 1]} {d.day}, {d.year}"
        mins = read_minutes(p["prose"])

        def make_body(p=p, trail=trail, og=og, fh=fh, date_h=date_h, mins=mins, modified=modified, path=path):
            pic = ctx["pic"]
            md = date.fromisoformat(modified)
            meta = (f'<div class="article-meta"><span>{p["section"]}</span><span>Published {date_h}</span>'
                    f'<span>Updated {MONTHS[md.month - 1]} {md.day}, {md.year}</span><span>{mins} min read</span></div>')
            others = [q for q in POSTS if q["slug"] != p["slug"]][:3]
            rel = "".join(f'<li><a href="/blog/{q["slug"]}/">{re.sub(r"<[^>]+>", "", q["h1"])}</a></li>' for q in others)
            author = (f'<div class="author-box">{lib.MARK_SVG}<div><strong>Enforce Interest editorial team</strong>'
                      f'<p>Written by the claims team at {FIRM} (Texas public adjuster license #{lib.LICENSE}). Statutes are quoted '
                      f'from the Texas Insurance Code; rates from the OCCC. Educational only &mdash; not legal advice.</p></div></div>'
                      f'<div class="related"><h2 style="font-size:1.4rem">Keep reading</h2><ul>{rel}</ul></div>')
            faq_html = (f'<h2 id="faq">Frequently asked questions</h2>{fh}') if fh else ""
            return (page_hero(trail, p["section"], p["h1"], esc(p["desc"]), meta=meta) +
                    f'<div class="wrap"><div class="article-hero-img" data-reveal>{pic(og, h1_plain, eager=True)}</div></div>' +
                    article_body(p["prose"] + faq_html + author, tool=p["tool"]) + cta_band())

        schema = [bc, {"@context": "https://schema.org", "@type": "BlogPosting", "headline": h1_plain,
                       "description": p["desc"], "datePublished": p["published"], "dateModified": modified,
                       "mainEntityOfPage": lib.SITE + path, "image": lib.SITE + f"/assets/img/{og}.jpg",
                       "articleSection": p["section"], "inLanguage": "en-US",
                       "author": {"@type": "Organization", "name": f"{lib.NAME} editorial team", "url": lib.SITE + "/about-us/"},
                       "publisher": {"@id": lib.SITE + "/#org"}}]
        if fl:
            schema.append(fl)
        out.append({"path": path, "title": p["title"] + " | Enforce Interest" if len(p["title"]) < 44 else p["title"],
                    "desc": p["desc"], "body": make_body, "schema": schema, "type": "article", "og": og,
                    "published": p["published"], "modified": modified, "section": p["section"], "h1": p["h1"],
                    "h1_plain": h1_plain, "read": mins, "date_h": date_h, "priority": "0.7"})
    return out
