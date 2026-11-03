"""Long-form guide pages: the Prompt Payment Act pillar, claim types, appraisal and supplements."""
import lib
from lib import (FLOAT_RATE_S, JUDG_RATE_S, RATE_MONTH, FLOAT_RATE, btn, cite, page_hero, facts, faq_block,
                 cta_band, breadcrumbs, article_body, money, interest, esc, sec_head)


def guide(path, title, desc, crumb, eyebrow, h1, lede, prose, faqs, og, aside=None, tool=None, ctas="",
          priority="0.8", modified=None):
    trail = [("Home", "/"), (crumb, path)]
    _, bc = breadcrumbs(trail)
    fh, fl = faq_block(faqs) if faqs else ("", None)
    import re
    h1_plain = re.sub(r"<[^>]+>", "", h1).replace("&amp;", "&").replace("&rsquo;", "'")

    def body():
        f = (f'<section class="section alt"><div class="wrap-narrow">{sec_head("FAQ", "Frequently asked questions", center=True)}'
             f'<div data-reveal>{fh}</div></div></section>') if faqs else ""
        return (page_hero(trail, eyebrow, h1, lede, ctas=ctas, aside=aside or "") +
                article_body(prose, tool=tool) + f + cta_band())

    art = {"@context": "https://schema.org", "@type": "Article", "headline": h1_plain, "description": desc,
           "mainEntityOfPage": lib.SITE + path, "datePublished": "2026-04-30", "dateModified": modified or lib.BUILD_DATE,
           "author": {"@type": "Organization", "name": lib.NAME, "url": lib.SITE + "/about-us/"},
           "publisher": {"@id": lib.SITE + "/#org"}, "image": lib.SITE + f"/assets/img/{og}.jpg", "inLanguage": "en-US"}
    return {"path": path, "title": title, "desc": desc, "body": body, "schema": [bc, art] + ([fl] if fl else []),
            "og": og, "guide": True, "h1_plain": h1_plain, "priority": priority, "modified": modified or lib.BUILD_DATE}


def ctas_std():
    return btn("/statutory-damages-calculator/", "Calculate interest", "gold") + btn("/contact/", "Free claim review", "ghost", arrow=False)


def build(ctx):
    mc = ctx["make_card"]
    out = []

    # ================================================================ PILLAR
    prose = f'''
<div class="keybox"><h2>Key takeaways</h2><ul>
<li>The Texas Prompt Payment of Claims Act is Chapter 542, Subchapter B of the Texas Insurance Code (§§542.051&ndash;.061).</li>
<li>It sets deadlines to acknowledge (15 days), decide (15 business days), pay after acceptance (5 business days) and pay in any event (60 days after receiving requested items).</li>
<li>An insurer that is liable for a claim and misses a deadline owes interest as damages &mdash; 18% a year, or {FLOAT_RATE_S} for weather claims under §542.060(c) &mdash; plus reasonable attorney&rsquo;s fees.</li>
<li>The statute must be &ldquo;liberally construed to promote the prompt payment of insurance claims&rdquo; (§542.054).</li></ul></div>

<h2>What the Texas Prompt Payment Act is</h2>
<p>Texas first passed a prompt-payment law for insurance claims in 1991, as Article 21.55 of the old Insurance Code.
When the Legislature recodified the Insurance Code, Article 21.55 became <strong>Chapter 542, Subchapter B</strong>
(&ldquo;Prompt Payment of Claims&rdquo;), effective April 1, 2005. Lawyers still call it the TPPCA or simply
&ldquo;542.&rdquo; Its purpose is written into the statute: it &ldquo;shall be liberally construed to promote the prompt
payment of insurance claims&rdquo; (§542.054).</p>
<p>The Act does two things. It imposes a sequence of claim-handling deadlines on insurers, and it attaches a financial
consequence to missing them. That consequence &mdash; statutory interest &ldquo;as damages&rdquo; plus attorney&rsquo;s
fees &mdash; is what Enforce Interest calculates and presents for Texas policyholders.</p>

<h2>Who and what it covers</h2>
<p>Subchapter B applies to essentially every insurer authorized to do business in Texas (§542.052): stock and mutual
companies, Lloyd&rsquo;s plans, reciprocal exchanges, county and farm mutuals, risk retention and purchasing groups,
eligible surplus lines insurers and others. It covers a <strong>&ldquo;claim&rdquo;</strong> as defined in §542.051: a
first-party claim made by an insured, policyholder or named beneficiary that must be paid by the insurer directly to that
person. Homeowners, commercial property, renters, condo and many other first-party claims qualify.</p>
<p>It does <strong>not</strong> apply to (§542.053):</p>
<ul><li>workers&rsquo; compensation insurance;</li><li>mortgage guaranty insurance;</li><li>title insurance;</li>
<li>fidelity, surety or guaranty bonds;</li><li>marine insurance as defined in §1807.001; or</li>
<li>the Texas Title Insurance Guaranty Association.</li></ul>
<p>The Texas Property and Casualty Insurance Guaranty Association is covered by the deadlines but is not subject to the
§542.060 damages. Claims against the Texas Windstorm Insurance Association follow TWIA&rsquo;s own exclusive remedies
in Chapter 2210 (see our <a href="/hurricane-claims/">hurricane claims guide</a>).</p>

<h2>The deadlines, section by section</h2>
<div class="table-scroll"><table><thead><tr><th>Section</th><th>Insurer must&hellip;</th><th>Deadline</th></tr></thead><tbody>
<tr><td>§542.055</td><td>Acknowledge the claim, begin investigating and request all items it reasonably believes it will need</td><td>15 days after notice (surplus lines: 30 business days)</td></tr>
<tr><td>§542.056(a)</td><td>Accept or reject the claim in writing</td><td>15 business days after receiving all items required to secure final proof of loss</td></tr>
<tr><td>§542.056(b)</td><td>Same, when it reasonably suspects arson</td><td>30 days after receiving the items</td></tr>
<tr><td>§542.056(d)</td><td>If it can&rsquo;t decide, say why it needs more time &mdash; then decide</td><td>Within the original window; then within 45 days of that notice</td></tr>
<tr><td>§542.057</td><td>Pay the claim (or the accepted part) after notifying acceptance</td><td>5 business days (surplus lines: 20 business days)</td></tr>
<tr><td>§542.058</td><td>Not delay payment</td><td>60 days after receiving all items reasonably requested, unless another statute sets a period</td></tr>
<tr><td>§542.059(b)</td><td>&mdash;</td><td>All claim-handling deadlines +15 days in a commissioner-declared weather catastrophe</td></tr>
</tbody></table></div>
<p>A &ldquo;business day&rdquo; is any day except Saturday, Sunday or a holiday recognized by Texas (§542.051(1)). The
<a href="/tools/claim-deadline-calculator/">claim deadline calculator</a> applies those rules to your dates.</p>
<h3>§542.055: acknowledgment and the first request</h3>
<p>The first deadline is triggered by &ldquo;notice of claim&rdquo; &mdash; any written notification that reasonably
apprises the insurer of the facts of the claim. Within 15 days the insurer must acknowledge receipt (and if it does so
orally, keep a record of the date, manner and content), start its investigation, and request from the claimant
&ldquo;all items, statements, and forms that the insurer reasonably believes, at that time, will be required.&rdquo;
It may make additional requests later only &ldquo;if during the investigation of the claim the additional requests are
necessary&rdquo; (§542.055(b)).</p>
<h3>§542.056: the decision</h3>
<p>Once the insurer has the items it required to secure final proof of loss, it has 15 business days to accept or reject
the claim in writing. A rejection must give reasons. If the insurer can&rsquo;t decide in time, it must tell the claimant
why within the same period, and it then has 45 days from that notice to decide.</p>
<h3>§542.057: payment after acceptance</h3>
<p>If the insurer accepts all or part of the claim, it must pay within 5 business days of the notice of acceptance, or
within 5 business days after the claimant performs any act the payment was conditioned on (for example, returning a
signed proof of loss).</p>
<h3>§542.058: the 60-day rule</h3>
<p>§542.058 is the backstop. An insurer that, &ldquo;after receiving all items, statements, and forms reasonably requested
and required under Section 542.055, delays payment of the claim for a period exceeding the period specified by other
applicable statutes or, if other statutes do not specify a period, for more than 60 days,&rdquo; must pay the damages in
§542.060. It does not apply if arbitration or litigation finds the claim invalid (§542.058(b)).</p>

<h2>The penalty: §542.060 interest and attorney&rsquo;s fees</h2>
<p>If an insurer &ldquo;that is liable for a claim under an insurance policy is not in compliance with this
subchapter,&rdquo; it must pay, in addition to the claim, <strong>interest on the amount of the claim at 18% a year as
damages, together with reasonable and necessary attorney&rsquo;s fees</strong> (§542.060(a)). If suit is filed, the fees
are taxed as costs (§542.060(b)).</p>
<p>For actions governed by Chapter 542A &mdash; weather and other forces-of-nature claims made on or after September 1,
2017 &mdash; the rate is instead simple interest at the §304.003 judgment rate on the date of judgment plus 5%, accruing
from the date the claim was required to be paid (§542.060(c)). For {RATE_MONTH}, that is {JUDG_RATE_S} + 5% =
<strong>{FLOAT_RATE_S}</strong>. Both subsections preserve prejudgment interest &ldquo;as provided by law,&rdquo; and
§542.061 makes the Act&rsquo;s remedies cumulative with any other remedy.</p>
<div class="callout"><strong>Two conditions, not one</strong><p>Interest is owed when the insurer (1) is <em>liable</em> for
the claim and (2) failed to comply with the subchapter. A late payment of a claim the insurer was never liable for
doesn&rsquo;t trigger it; neither does a timely payment of a claim it was liable for.</p></div>

<h2>How Chapter 542A changed weather claims in 2017</h2>
<p>HB 1774 added Chapter 542A, effective September 1, 2017, for claims arising from damage caused wholly or partly by
forces of nature. It requires a written pre-suit notice at least 61 days before filing (§542A.003), gives the insurer a
right to inspect (§542A.004), lets the insurer abate a suit filed without proper notice (§542A.005) and ties
attorney&rsquo;s fees to how close the judgment comes to the amount demanded in the notice (§542A.007). It also created the
floating rate in §542.060(c). See the <a href="/blog/542a-pre-suit-notice-explained/">542A pre-suit notice guide</a>.</p>

<h2>The cases that shape it today</h2>
<ul>
<li><strong><em>Barbara Technologies Corp. v. State Farm Lloyds</em>, 589 S.W.3d 806 (Tex. 2019)</strong> &mdash;
payment of an appraisal award is not an acknowledgment of liability and does not, as a matter of law, bar TPPCA
damages.</li>
<li><strong><em>Ortiz v. State Farm Lloyds</em>, 589 S.W.3d 127 (Tex. 2019)</strong> &mdash; decided the same day:
paying an appraisal award forecloses breach-of-contract and bad-faith claims for policy benefits absent an independent
injury, but the TPPCA claim could proceed.</li>
<li><strong><em>Alvarez v. State Farm Lloyds</em>, 601 S.W.3d 781 (Tex. 2020)</strong> &mdash; applied <em>Barbara
Technologies</em>.</li>
<li><strong><em>Hinojos v. State Farm Lloyds</em>, 619 S.W.3d 651 (Tex. 2021)</strong> &mdash; an insurer is liable under
the TPPCA for amounts owed but unpaid when the statutory deadline expires, even if it made a reasonable partial payment
on time.</li>
<li><strong><em>Rodriguez v. Safeco Ins. Co. of Indiana</em> (Tex. 2024)</strong> &mdash; in a Chapter 542A case, an
insurer that pays the appraisal award plus all statutory interest that could be owed is not liable for attorney&rsquo;s
fees under §542A.007.</li>
</ul>
<p>Read more in <a href="/blog/hinojos-v-state-farm-lloyds-explained/">Hinojos v. State Farm Lloyds, explained</a>.</p>

<h2>How to use the Act on your own claim</h2>
<ol>
<li><strong>Write everything down.</strong> The date you gave written notice, every request the insurer made and the date
it received each response. The <a href="/tools/claim-timeline-builder/">claim timeline builder</a> keeps this for you.</li>
<li><strong>Find the trigger date.</strong> The 60-day clock starts on the date the insurer had everything it
<em>reasonably</em> requested &mdash; not necessarily the date it says the file was complete.</li>
<li><strong>Compare payments to deadlines.</strong> Any amount paid after its deadline, including amounts later found owed
through appraisal or a supplement, can carry interest.</li>
<li><strong>Run the numbers.</strong> Use the <a href="/statutory-damages-calculator/">statutory interest calculator</a>
with the right rate.</li>
<li><strong>Present it.</strong> A clear, dated timeline with the calculation is often enough for a carrier to resolve
the issue. Enforce Interest does this as part of a public adjusting engagement; disputes that require a lawsuit belong
with a Texas attorney.</li></ol>'''
    faqs = [
        ("Is the Texas Prompt Payment Act the same as Chapter 542?",
         "<p>Yes &mdash; specifically Chapter 542, Subchapter B of the Insurance Code (§§542.051&ndash;.061). Other subchapters of "
         "Chapter 542 deal with unfair claim settlement practices and health-care provider payments.</p>"),
        ("Does the 60-day rule apply to auto insurance?",
         "<p>It applies to first-party claims paid directly to the insured, so it can apply to your own collision or "
         "comprehensive claim. It does not apply to a claim you make against someone else&rsquo;s insurer (a third-party "
         "liability claim).</p>"),
        ("Do I have to ask for the 18% interest?",
         "<p>The liability arises by statute when the conditions are met, but in practice carriers rarely volunteer it. It is "
         "usually raised in a written demand or, failing that, in a lawsuit.</p>"),
        ("Can the insurer extend the deadlines?",
         "<p>Only in the ways the statute allows: the §542.056(d) notice that it needs more time (then 45 days to decide), the "
         "15-day catastrophe extension in §542.059(b), and court-granted extensions for guaranty associations (§542.059(a)). "
         "Additional document requests must be necessary to the investigation (§542.055(b)).</p>"),
    ]
    out.append(guide("/texas-prompt-payment-act/",
                     "Texas Prompt Payment Act (Ch. 542) Explained | Enforce Interest",
                     "The Texas Prompt Payment of Claims Act, section by section: 15-day, 15-business-day, 5-day and 60-day "
                     f"deadlines, 18% and {FLOAT_RATE_S} interest, Chapter 542A and the key court cases.",
                     "Texas Prompt Payment Act", "Tex. Ins. Code §§542.051&ndash;.061",
                     "The Texas Prompt Payment Act, <em>explained</em>",
                     "Every deadline Texas insurers must meet on a first-party claim, what happens when they miss one, and "
                     "how the courts have applied it since 2019.",
                     prose, faqs, mc("texas-prompt-payment-act", "Tex. Ins. Code ch. 542", "The Texas Prompt Payment Act, explained"),
                     aside=facts([("Enacted", "1991 (Art. 21.55)"), ("Codified", "Ch. 542, Subch. B (2005)"),
                                  ("Interest", f"18% / {FLOAT_RATE_S}"), ("Plus", "attorney&rsquo;s fees")]),
                     ctas=ctas_std(), priority="0.9"))

    # ================================================================ HAIL & WIND
    prose = f'''
<h2>Why hail and wind claims stall</h2>
<p>Texas leads the country in hail claims, and a single spring storm across Dallas&ndash;Fort Worth, San Antonio or the
Austin corridor can put tens of thousands of roofs into the claims queue at once. Carriers bring in field adjusters
from out of state, inspections slip, and estimates move through desk review. None of that changes the deadlines in
Chapter 542. In a commissioner-declared catastrophe the claim-handling deadlines extend by 15 days (§542.059(b)); beyond
that, the clock runs.</p>
<h2>Red flags on storm claims</h2>
<ul>
<li><strong>Inspection weeks after notice.</strong> The insurer must acknowledge and begin investigating within 15 days
(§542.055). A first inspection a month or more later is worth noting.</li>
<li><strong>The same document requested twice.</strong> Additional requests are allowed only when the investigation
makes them necessary (§542.055(b)). Duplicates and requests for things the carrier already holds don&rsquo;t move the
60-day trigger in a principled way.</li>
<li><strong>Field estimate cut in desk review.</strong> When the adjuster who walked the roof wrote one number and a
reviewer who didn&rsquo;t wrote another, the first estimate is evidence of scope.</li>
<li><strong>&ldquo;Wear and tear&rdquo; or &ldquo;prior damage&rdquo; denials.</strong> Hail date reports, roof age, and
photographs of fresh fractures and granule loss answer these.</li>
<li><strong>Partial payment, then silence.</strong> Once the carrier accepts part of the claim, §542.057 requires
payment of that part within 5 business days. The rest remains subject to §542.058.</li>
</ul>
<h2>Which interest rate applies to a hail or wind claim?</h2>
<p>Hail and wind are forces of nature, so a lawsuit on a hail or wind claim made on or after September 1, 2017 is an
action governed by Chapter 542A, and the floating rate in §542.060(c) applies: the §304.003 judgment rate plus 5%
&mdash; <strong>{FLOAT_RATE_S}</strong> using the {RATE_MONTH} rate. A storm claim made before that date carries the
standard 18%. (The test in HB 1774 is when the <em>claim was made</em>, not the date of loss.)</p>
<p>On a $40,000 roof claim paid 120 days late, that is {money(interest(40000, FLOAT_RATE, 120))} at {FLOAT_RATE_S},
versus {money(interest(40000, 18, 120))} at 18%.</p>
<h2>The 61-day pre-suit notice</h2>
<p>Before suing over a weather claim, a policyholder must give the insurer written notice at least 61 days in advance
stating the acts or omissions complained of, the specific amount claimed and the attorney&rsquo;s fees incurred
(§542A.003). The insurer can ask to inspect within 30 days (§542A.004). The amount in that notice later caps or scales
attorney&rsquo;s fees (§542A.007). The <a href="/tools/542a-notice-calculator/">542A notice calculator</a> shows the
dates and the fee ratio.</p>
<h2>Roof claims and supplements</h2>
<p>Most hail claims grow after the tear-off: rotted or delaminated decking, code-required drip edge, underlayment or
ventilation, and damaged flashing that wasn&rsquo;t visible from the ground. Each supplement is a new request for payment
and is evaluated on its own timeline. See <a href="/long-term-claim-supplements/">claim supplements</a> for how interest
applies when a supplement is paid late.</p>
<h2>Evidence that moves storm claims</h2>
<ul><li>A hail or wind report for your address and date (several commercial services produce these).</li>
<li>Close-up photos of soft metals &mdash; vents, gutters, downspouts, AC fins &mdash; which dent cleanly in hail.</li>
<li>Test-square photos showing fractured shingle mats and displaced granules.</li>
<li>The roof&rsquo;s installation date (permit, invoice or prior inspection) to rebut age arguments.</li>
<li>Every adjuster estimate, including revisions, with dates.</li></ul>
<h2>Deductibles on Texas storm claims</h2>
<p>Many Texas policies use a percentage wind/hail deductible based on the dwelling limit. Interest is calculated on what
is owed after the deductible. Convert yours with the <a href="/tools/wind-hail-deductible-calculator/">deductible
calculator</a>.</p>'''
    faqs = [
        ("How long does an insurance company have to pay a hail claim in Texas?",
         "<p>Generally 60 days after it receives all the items it reasonably requested (§542.058), or 5 business days after it "
         "notifies you it will pay (§542.057), whichever applies first. In a declared weather catastrophe the claim-handling "
         "deadlines extend by 15 days.</p>"),
        ("How long do I have to file a hail claim in Texas?",
         "<p>Your policy controls the notice requirement &mdash; usually &ldquo;prompt&rdquo; notice, and some policies set a "
         "fixed window such as one year from the storm. TWIA policies require filing within one year (§2210.573). Lawsuit "
         "deadlines are separate; contractual limits can&rsquo;t be shorter than two years (§16.070).</p>"),
        ("Is hail damage interest 18% or the floating rate?",
         f"<p>For hail claims made on or after September 1, 2017, the floating rate &mdash; currently {FLOAT_RATE_S}. For hail "
         "claims made before then, 18%.</p>"),
    ]
    out.append(guide("/hail-wind-claims/",
                     "Texas Hail & Wind Claims: Late Payment Interest | Enforce Interest",
                     "Texas hail and wind insurance claims paid late: deadlines, the 61-day 542A notice, the "
                     f"{FLOAT_RATE_S} floating interest rate, roof supplements and the evidence that moves storm claims.",
                     "Hail &amp; wind claims", "Hail &middot; wind &middot; tornado &middot; Chapter 542A",
                     "Hail &amp; wind claims paid <em>late</em>",
                     "Storm claims are where Texas carriers fall furthest behind. The deadlines don&rsquo;t move &mdash; and when "
                     "they are missed, interest runs at the floating weather rate.",
                     prose, faqs, mc("hail-wind-claims", "Hail · wind · Chapter 542A", "Texas hail and wind claims paid late"),
                     aside=facts([("Interest rate", f"{FLOAT_RATE_S} floating"), ("Pre-suit notice", "61 days"),
                                  ("Inspection request", "30 days"), ("Catastrophe", "+15 days")]),
                     ctas=ctas_std(), tool=("/tools/542a-notice-calculator/", "542A notice calculator",
                                            "Pre-suit notice dates and the attorney-fee ratio.")))

    # ================================================================ HURRICANE
    prose = f'''
<h2>Hurricane claims are three claims in one</h2>
<p>A Gulf Coast hurricane can produce a wind claim, a flood claim and a business-income or living-expense claim from the
same day &mdash; under different policies, from different insurers, with different rules. Disputes over which force
caused which damage are the single biggest source of delay. Knowing which policy pays what, and which deadlines apply
to each, is the first step.</p>
<div class="table-scroll"><table><thead><tr><th>Coverage</th><th>Usually written by</th><th>Deadlines &amp; remedies</th></tr></thead><tbody>
<tr><td>Wind (inland and many coastal homes)</td><td>Private homeowners or commercial insurer</td><td>Chapter 542 deadlines; §542.060(c) floating interest; Chapter 542A notice</td></tr>
<tr><td>Wind and hail in the 14 coastal counties and part of Harris County</td><td>Texas Windstorm Insurance Association (TWIA)</td><td>TWIA&rsquo;s exclusive process in Chapter 2210, Subchapter L-1</td></tr>
<tr><td>Flood / storm surge</td><td>National Flood Insurance Program or a private flood carrier</td><td>Federal rules for NFIP policies; not governed by Chapter 542 for NFIP</td></tr>
</tbody></table></div>

<h2>Private insurers: Chapter 542 and 542A</h2>
<p>For a hurricane wind claim against a private carrier, the full prompt-payment sequence applies, extended by 15 days
when the commissioner has declared a weather catastrophe (§542.059(b)). A claim made on or after September 1, 2017 is
governed by Chapter 542A: interest under §542.060(c) at the §304.003 rate plus 5% (<strong>{FLOAT_RATE_S}</strong> using
{RATE_MONTH}&rsquo;s rate) and a 61-day pre-suit notice.</p>
<h2>TWIA claims follow different rules</h2>
<p>TWIA policies are governed by Insurance Code Chapter 2210, and Subchapter L-1 provides the <em>exclusive</em> remedies
for TWIA claims (§2210.572). Chapter 542A does not apply to TWIA (§542A.002(b)). The key TWIA deadlines:</p>
<ul>
<li><strong>File within one year</strong> of the date of damage (§2210.573(a)); the commissioner can extend this by up to
180 days for good cause (§2210.205(b)).</li>
<li><strong>Accept or deny within 60 days</strong> after TWIA receives the claim or the information it requested
(§2210.573(d)), unless extended by the commissioner.</li>
<li><strong>Pay within 10 days</strong> after notice of acceptance, or after you perform a condition (§2210.5731).</li>
<li><strong>Interest is prejudgment interest</strong> at the Finance Code Chapter 304 rate from the day after payment was
due (§2210.576(b)(2)) &mdash; not the 18% or §542.060(c) rate.</li>
<li><strong>Disputes</strong> over the amount go to appraisal under §2210.574; denied coverage requires notice of intent to
sue and suit within two years of the denial notice (§2210.577).</li>
</ul>
<h2>Named-storm and windstorm deductibles</h2>
<p>Coastal policies commonly carry a percentage deductible for named storms or windstorm. On a home insured for
$400,000, a 5% deductible is $20,000. Run yours through the <a href="/tools/wind-hail-deductible-calculator/">deductible
calculator</a> before deciding how to proceed.</p>
<h2>Wind versus water</h2>
<p>Wind policies exclude flood; flood policies don&rsquo;t cover wind. When a carrier attributes damage to surge or rising
water, ask for the basis in writing, preserve water lines and debris lines with photographs, and document roof and
window openings that let wind-driven rain in. For TWIA, the commissioner publishes guidelines for separating wind from
water damage, and those guidelines are presumed correct in a TWIA dispute (§2210.578(h)).</p>
<h2>Living expenses and temporary repairs</h2>
<p>Additional living expense (ALE) and business income are part of the claim and are paid on the same statutory clock.
Keep receipts, and send them in batches with a cover letter so each batch has a clear date of receipt.</p>
<h2>After the storm: a checklist</h2>
<ol><li>Report the claim in writing and keep proof of the date.</li>
<li>Photograph everything before mitigation, then mitigate (tarps, water extraction) and keep invoices.</li>
<li>Identify every policy: homeowners, TWIA, flood, and any separate contents or business policies.</li>
<li>Log every request and response in the <a href="/tools/claim-timeline-builder/">claim timeline builder</a>.</li>
<li>Check the deadlines with the <a href="/tools/claim-deadline-calculator/">deadline calculator</a> (tick
&ldquo;TWIA&rdquo; if it applies).</li></ol>'''
    faqs = [
        ("How long does TWIA have to pay a claim?",
         "<p>TWIA must accept or deny within 60 days after it receives the claim or requested information, and pay an accepted "
         "claim within 10 days after notice of acceptance (§§2210.573(d), 2210.5731).</p>"),
        ("Does the 18% penalty apply to TWIA?",
         "<p>No. TWIA claims have exclusive remedies in Chapter 2210. A successful claimant can recover the covered loss, "
         "prejudgment interest at the Finance Code rate from the day after payment was due, costs and attorney&rsquo;s fees, "
         "with enhanced damages only for proven intentional misconduct (§2210.576).</p>"),
        ("How long do I have to file a hurricane claim in Texas?",
         "<p>For TWIA, one year from the date of damage (§2210.573). For private insurers, check your policy&rsquo;s notice "
         "condition &mdash; often &ldquo;prompt notice&rdquo; or a fixed period &mdash; and file as soon as you can.</p>"),
    ]
    out.append(guide("/hurricane-claims/",
                     "Texas Hurricane Insurance Claims: Deadlines & Interest | Enforce Interest",
                     "Texas hurricane claims: private insurer deadlines and the floating interest rate, TWIA's one-year "
                     "filing, 60-day decision and 10-day payment rules, named-storm deductibles and wind vs. flood.",
                     "Hurricane claims", "Gulf Coast &middot; TWIA &middot; named storms",
                     "Hurricane claims in <em>Texas</em>",
                     "Wind, flood and TWIA each play by different rules. Here is which deadlines apply to your hurricane "
                     "claim &mdash; and what late payment costs the insurer.",
                     prose, faqs, mc("hurricane-claims", "Gulf Coast · TWIA", "Texas hurricane insurance claims: deadlines and interest"),
                     aside=facts([("Private carrier rate", FLOAT_RATE_S), ("TWIA filing", "1 year"),
                                  ("TWIA decision", "60 days"), ("TWIA payment", "10 days")]),
                     ctas=ctas_std(), tool=("/tools/claim-deadline-calculator/", "Claim deadline calculator",
                                            "Includes TWIA and catastrophe extensions.")))

    # ================================================================ FIRE & SMOKE
    prose = f'''
<h2>Fire claims get the full 18%</h2>
<p>Fire is not a &ldquo;force of nature&rdquo; under Chapter 542A unless it is a wildfire or lightning-caused fire. A
house fire from cooking, wiring, a dryer or arson is governed by the standard §542.060(a) rate: <strong>18% a year</strong>
on whatever was paid late, plus reasonable attorney&rsquo;s fees. On a $150,000 fire claim paid 90 days late, that is
{money(interest(150000, 18, 90))}.</p>
<p>One timing difference: if the insurer has a reasonable basis to believe the loss resulted from arson, it gets 30 days
(instead of 15 business days) after receiving the requested items to accept or reject (§542.056(b)). The 60-day payment
backstop in §542.058 is unchanged.</p>
<h2>Smoke damage: the scope fight</h2>
<p>Smoke and soot travel well beyond the room that burned &mdash; through the HVAC system, into wall cavities and attics,
and onto contents in closed drawers. Carriers often scope cleaning for the visibly affected rooms only. The evidence that
widens scope:</p>
<ul><li><strong>Smoke damage investigations.</strong> An industrial hygienist or environmental consultant samples surfaces
(tape lifts and wipe samples) and air to identify char, soot and ash throughout the structure.</li>
<li><strong>HVAC inspection.</strong> Ductwork and air handlers that ran during or after the fire distribute residue.</li>
<li><strong>Odor testing and contents.</strong> Textiles and porous contents often can&rsquo;t be restored; a contents
specialist documents what can be cleaned and what must be replaced.</li>
<li><strong>Wildfire smoke.</strong> Even without flames on the property, wildfire smoke infiltration can be a covered loss;
wildfire is a force of nature, so those claims fall under Chapter 542A and the floating rate.</li></ul>
<p>Each investigation report is a document the insurer may request. Send it with a dated cover letter: the date the carrier
receives the last reasonably requested item is what starts the 60-day clock. More on this in our guide to
<a href="/blog/smoke-damage-claim-texas/">smoke damage claims in Texas</a>.</p>
<h2>Where fire claims slow down</h2>
<ul>
<li><strong>Cause-and-origin investigations</strong> that run for months with no written explanation of what is still needed.</li>
<li><strong>ACV versus replacement cost.</strong> Depreciation is withheld up front, and the holdback becomes payable only
after rebuilding &mdash; another payment with its own deadline.</li>
<li><strong>Contents inventories</strong> of thousands of items, reviewed line by line.</li>
<li><strong>Code upgrades</strong> (ordinance or law coverage) when the rebuild must meet current code.</li>
<li><strong>Additional living expense</strong> paid in slow, partial increments while the family is displaced.</li>
<li><strong>Examinations under oath and recorded statements</strong> requested late in the claim.</li></ul>
<h2>Total losses and the 72-hour rule</h2>
<p>If the insurer pays, or commits in writing to pay, the policy limit for a total fire loss of real property within 72
hours after the loss is reported, Texas bars a public adjuster from charging a percentage fee on that claim (§4102.104(b)).
That is a consumer protection worth knowing. Most fire claims are not resolved that quickly, and that is where documenting
the timeline matters.</p>
<h2>What to keep after a fire</h2>
<ol><li>The fire department report number and date.</li><li>Photos and video before debris removal.</li>
<li>Every ALE receipt (hotel, rent, meals over normal, mileage).</li><li>The contents list, updated as you remember items.</li>
<li>Copies of all hygienist, contractor and engineer reports with the date each was sent to the carrier.</li></ol>'''
    faqs = [
        ("How long does an insurance company have to pay a fire claim in Texas?",
         "<p>The general rules apply: 15 business days to accept or reject after receiving requested items (30 days if arson is "
         "reasonably suspected), 5 business days to pay after acceptance, and 60 days after receiving requested items in any "
         "event (§§542.056&ndash;.058).</p>"),
        ("What is a smoke damage investigation?",
         "<p>A professional assessment &mdash; usually by an industrial hygienist &mdash; that samples surfaces and air to find "
         "and map soot, char and ash residue, so the cleaning and replacement scope is based on evidence rather than what is "
         "visible.</p>"),
        ("Is fire claim interest 18%?",
         "<p>Yes for most fires. Wildfire and lightning are forces of nature, so those claims (made on or after September 1, "
         f"2017) use the floating rate, currently {FLOAT_RATE_S}.</p>"),
    ]
    out.append(guide("/fire-smoke-damage/",
                     "Texas Fire & Smoke Damage Claims Paid Late | Enforce Interest",
                     "Texas fire and smoke damage insurance claims: the 18% late-payment rate, arson timing rules, smoke "
                     "damage investigations, ACV holdbacks, ALE and contents — and how delays are documented.",
                     "Fire &amp; smoke damage", "18% standard rate &middot; §542.060(a)",
                     "Fire &amp; smoke damage <em>claims</em>",
                     "Non-weather losses carry the full 18% when paid late. Fire claims stall on scope, contents and "
                     "investigations &mdash; here is how to keep the clock on the record.",
                     prose, faqs, mc("fire-smoke-damage", "18% standard rate", "Texas fire and smoke damage claims paid late"),
                     aside=facts([("Interest rate", "18% fixed"), ("Arson decision", "30 days"),
                                  ("Payment backstop", "60 days"), ("Wildfire", f"{FLOAT_RATE_S} (542A)")]),
                     ctas=ctas_std()))

    # ================================================================ WATER
    prose = f'''
<h2>Water claims: sudden versus gradual</h2>
<p>Most homeowners policies cover <strong>sudden and accidental</strong> discharge of water from plumbing, appliances or
HVAC systems, and exclude damage from <strong>continuous or repeated seepage or leakage</strong> over time (often 14 days
or more, depending on the form). Nearly every water-claim dispute turns on which side of that line the loss falls.
Plumber invoices identifying the failed part, moisture mapping and photos of the failure point are the core evidence.</p>
<h2>The rate on water claims</h2>
<p>A burst supply line, failed water heater or leaking dishwasher is not a force of nature, so late payment carries the
standard <strong>18%</strong> under §542.060(a). Water that enters from a storm &mdash; wind-driven rain through a damaged
roof, or a rainstorm &mdash; is weather-related and falls under Chapter 542A and the floating rate
({FLOAT_RATE_S}) for claims made on or after September 1, 2017.</p>
<h2>Where water claims stall</h2>
<ul>
<li><strong>&ldquo;Long-term seepage&rdquo; denials</strong> on what was a sudden failure.</li>
<li><strong>Mitigation versus repair.</strong> Drying is paid; tear-out, rebuild and cabinets are disputed.</li>
<li><strong>Mold.</strong> Many Texas policies limit or exclude mold, but mold resulting from a covered water loss is often
covered up to a sublimit. Testing can stretch a claim for months while the statutory clock keeps running.</li>
<li><strong>Cause-of-loss letters</strong> asking you to procure reports the insurer is responsible for obtaining.</li>
<li><strong>Hidden damage</strong> found behind walls or under floors and labeled a &ldquo;new claim.&rdquo;</li></ul>
<h2>Freeze damage</h2>
<p>Burst pipes from a hard freeze &mdash; as in February 2021 &mdash; are usually covered as sudden and accidental
discharge, but many policies exclude freeze damage to plumbing in a vacant or unheated home unless you used reasonable
care to maintain heat or shut off and drain the water. Freeze claims made during a declared winter-storm catastrophe get
the 15-day extension in §542.059(b). Whether a freeze loss is a &ldquo;force of nature&rdquo; claim under Chapter 542A is
not spelled out in the statute&rsquo;s list (which names snowstorms but not freezes); it can affect the rate and the
pre-suit notice. Read <a href="/blog/how-long-to-file-a-freeze-claim-in-texas/">how long you have to file a freeze claim
in Texas</a>.</p>
<h2>Texas water claims and your claims history</h2>
<p>Texas limits how insurers can use some water-damage history. Insurers can&rsquo;t use a prior appliance-related water
claim to rate, renew or cancel a policy if the damage was properly remediated and the remediation was inspected and certified (§544.353, with exceptions for three or more such claims in three years), and claims caused by natural
causes don&rsquo;t count toward the three-claims nonrenewal rule (§551.107). Don&rsquo;t let fear of a nonrenewal keep you
from reporting a legitimate loss &mdash; and don&rsquo;t delay reporting; late notice is a common defense.</p>
<h2>What to do in the first week</h2>
<ol><li>Stop the water and photograph the source before repair.</li><li>Keep the failed part.</li>
<li>Hire mitigation and keep its moisture logs.</li><li>Report the claim in writing.</li>
<li>Log every request and response in the <a href="/tools/claim-timeline-builder/">claim timeline builder</a>.</li></ol>'''
    faqs = [
        ("Is water damage from a burst pipe covered in Texas?",
         "<p>Usually, as sudden and accidental discharge, subject to the policy&rsquo;s exclusions (for example, continuous "
         "seepage or freezing in an unheated vacant home).</p>"),
        ("What interest applies if my water claim is paid late?",
         f"<p>18% a year under §542.060(a) for plumbing and appliance leaks. Storm-driven water claims made on or after "
         f"September 1, 2017 use the floating rate, currently {FLOAT_RATE_S}.</p>"),
        ("Does mold extend the insurer&rsquo;s deadline?",
         "<p>No. Mold testing may be a legitimate part of the investigation, but the deadlines in Chapter 542 still run from "
         "the events the statute names.</p>"),
    ]
    out.append(guide("/water-plumbing-damage/",
                     "Texas Water & Plumbing Damage Claims Paid Late | Enforce Interest",
                     "Texas water and plumbing damage insurance claims: sudden vs. seepage, mold, freeze losses, the 18% "
                     "late-payment interest rate and how to document a water claim timeline.",
                     "Water &amp; plumbing damage", "18% standard rate &middot; §542.060(a)",
                     "Water &amp; plumbing damage <em>claims</em>",
                     "Burst pipes, failed water heaters and slab leaks are paid at the full 18% when paid late. Here is "
                     "where water claims stall &mdash; and what keeps them moving.",
                     prose, faqs, mc("water-plumbing-damage", "18% standard rate", "Texas water and plumbing damage claims paid late"),
                     aside=facts([("Interest rate", "18% fixed"), ("Storm water", f"{FLOAT_RATE_S}"),
                                  ("Key issue", "sudden vs. seepage"), ("Freeze catastrophe", "+15 days")]),
                     ctas=ctas_std()))

    # ================================================================ POST-APPRAISAL
    ex = interest(176000, FLOAT_RATE, 423)
    prose = f'''
<h2>The pattern</h2>
<p>A claim stalls. The carrier pays a figure well below the contractor&rsquo;s estimate. The policyholder invokes the
appraisal clause; each side names an appraiser, an umpire is chosen, and the panel issues an award &mdash; often far
higher than what was paid. The carrier pays the award and closes the file. No one mentions the months between when the
money was due and when it arrived.</p>
<p>That gap is what Enforce Interest calculates. Appraisal fixes the amount of loss. It doesn&rsquo;t erase the date by
which that amount should have been paid.</p>
<h2>What the Texas Supreme Court has held</h2>
<ul>
<li><strong><em>Barbara Technologies Corp. v. State Farm Lloyds</em>, 589 S.W.3d 806 (Tex. 2019).</strong> Paying an
appraisal award is not an acknowledgment of liability and is not a determination that the insurer complied with the
prompt-payment statute. Payment of the award does not, by itself, bar TPPCA damages.</li>
<li><strong><em>Ortiz v. State Farm Lloyds</em>, 589 S.W.3d 127 (Tex. 2019).</strong> The same day, the Court held that
paying the award <em>does</em> generally foreclose breach-of-contract and bad-faith claims for policy benefits unless the
insured shows an independent injury &mdash; but the prompt-payment claim survives.</li>
<li><strong><em>Alvarez v. State Farm Lloyds</em>, 601 S.W.3d 781 (Tex. 2020).</strong> Applied <em>Barbara
Technologies</em> to reverse a judgment for the insurer.</li>
<li><strong><em>Hinojos v. State Farm Lloyds</em>, 619 S.W.3d 651 (Tex. 2021).</strong> The court of appeals had ruled for
the insurer because it made a reasonable payment within the 60-day window. The Supreme Court reversed: an insurer is liable
for prompt-payment damages on amounts it owed but had not paid when the statutory deadline expired, even if its earlier
partial payment was reasonable and timely.</li>
<li><strong><em>Rodriguez v. Safeco Insurance Co. of Indiana</em> (Tex. Feb. 2, 2024).</strong> In a Chapter 542A weather
case, when the insurer pays the appraisal award <em>and</em> any statutory interest that could be owed, nothing remains to
be awarded on the claim, so §542A.007 permits no attorney&rsquo;s fees.</li></ul>
<div class="callout wine"><strong>What changed after Rodriguez</strong><p>Many carriers now pay the award together with
an interest figure they calculate themselves. That doesn&rsquo;t end the analysis &mdash; it moves it to the math. Did they
start interest on the right date? Use the right rate? Credit each earlier payment on the date it was actually made? A
short-paid interest figure leaves the door open.</p></div>
<h2>How post-appraisal interest is calculated</h2>
<ol><li><strong>Amount owed:</strong> the award under the policy&rsquo;s valuation, less the deductible.</li>
<li><strong>Deadline:</strong> usually the §542.058 date &mdash; 60 days after the insurer received the items it reasonably
requested &mdash; or an earlier §542.057 date for any part it accepted.</li>
<li><strong>Balance at the deadline:</strong> amount owed minus everything paid by the deadline.</li>
<li><strong>Accrual:</strong> interest on that balance at the applicable rate, reduced each time a later payment arrives,
through the date the award was paid.</li></ol>
<h3>Worked example</h3>
<div class="table-scroll"><table><tbody>
<tr><td>Hail claim made</td><td class="num">March 22, 2024</td></tr>
<tr><td>§542.058 deadline (60 days after requested items received)</td><td class="num">May 21, 2024</td></tr>
<tr><td>Paid by the deadline</td><td class="num">$48,000</td></tr>
<tr><td>Appraisal award less $2,500 deductible</td><td class="num">$224,000</td></tr>
<tr><td>Balance paid with the award</td><td class="num">$176,000 on July 18, 2025</td></tr>
<tr><td>Days late</td><td class="num">423</td></tr>
<tr><td>Rate (§542.060(c), {RATE_MONTH})</td><td class="num">{FLOAT_RATE_S}</td></tr>
<tr><td><strong>Statutory interest</strong></td><td class="num"><strong>{money(ex)}</strong></td></tr>
</tbody></table></div>
<p>The same facts on a non-weather claim at 18% produce {money(interest(176000, 18, 423))}. Try your own numbers in the
<a href="/tools/appraisal-interest-calculator/">appraisal interest calculator</a>.</p>
<h2>Common carrier responses &mdash; and the replies</h2>
<h3>&ldquo;We paid the appraisal award, so the claim is closed.&rdquo;</h3>
<p><em>Barbara Technologies</em> and <em>Hinojos</em> answer this directly: payment of an award does not, by itself,
discharge prompt-payment liability.</p>
<h3>&ldquo;Our original payment was reasonable.&rdquo;</h3>
<p>That was the reasoning the Supreme Court rejected in <em>Hinojos</em>. Reasonableness of an earlier payment doesn&rsquo;t
change that the rest of the money owed was unpaid when the deadline expired.</p>
<h3>&ldquo;We never had a complete file, so no clock started.&rdquo;</h3>
<p>This is a real factual issue. The 60-day period runs from receipt of the items the insurer <em>reasonably</em> requested.
The claim file &mdash; what was asked for, when, and what was already in hand &mdash; decides it, which is why the timeline
reconstruction matters.</p>
<h3>&ldquo;We already paid interest.&rdquo;</h3>
<p>Check the calculation line by line. The appraisal calculator has a field for exactly this.</p>
<h2>What to send for a post-appraisal review</h2>
<ul><li>The policy declarations page and the appraisal clause.</li><li>The appraisal demand, appointment letters and the
signed award.</li><li>Every payment letter and check stub, with dates.</li><li>All correspondence with the carrier, including
document requests and your responses.</li><li>Any 542A pre-suit notice, for weather claims.</li></ul>'''
    faqs = [
        ("If the carrier paid the appraisal award, can I still collect interest?",
         "<p>Possibly. Under <em>Barbara Technologies</em> and <em>Hinojos</em>, payment of an award doesn&rsquo;t by itself end "
         "prompt-payment liability. Interest can be owed on amounts unpaid at the statutory deadline through the date they were paid.</p>"),
        ("What is Hinojos v. State Farm Lloyds?",
         "<p>A 2021 Texas Supreme Court decision, 619 S.W.3d 651, holding that an insurer&rsquo;s reasonable, timely partial "
         "payment doesn&rsquo;t shield it from prompt-payment damages on the amounts it owed but hadn&rsquo;t paid by the "
         "deadline. <a href=\"/blog/hinojos-v-state-farm-lloyds-explained/\">Read our explainer</a>.</p>"),
        ("Does Rodriguez v. Safeco mean I can&rsquo;t recover anything after appraisal?",
         "<p>No. <em>Rodriguez</em> concerns attorney&rsquo;s fees in Chapter 542A cases when the insurer has paid the award and "
         "all statutory interest that could be owed. If the interest wasn&rsquo;t paid, or was underpaid, the interest itself "
         "remains owed.</p>"),
        ("Is there a deadline to pursue post-appraisal interest?",
         "<p>Yes. Your policy&rsquo;s suit-limitation clause (not shorter than two years under §16.070) and general limitations "
         "rules apply, and when the claim accrued is a legal question. Don&rsquo;t wait.</p>"),
    ]
    out.append(guide("/post-appraisal-interest-recovery/",
                     "Post-Appraisal Interest in Texas (Hinojos) | Enforce Interest",
                     "Texas insurer paid the appraisal award but not the interest? How Barbara Technologies, Hinojos and "
                     "Rodriguez v. Safeco apply, how post-appraisal interest is calculated, and what to send.",
                     "Post-appraisal interest", "Hinojos v. State Farm Lloyds &middot; 619 S.W.3d 651",
                     "The carrier paid the appraisal. <em>The interest is a separate question.</em>",
                     "Appraisal sets the amount of loss &mdash; not the date it was due. Texas law can still owe you "
                     "interest on every day the underpaid amount sat unpaid.",
                     prose, faqs, mc("post-appraisal-interest", "Hinojos v. State Farm (Tex. 2021)", "Post-appraisal interest recovery in Texas"),
                     aside=facts([("Key case", "Hinojos (2021)"), ("Fees case", "Rodriguez (2024)"),
                                  ("Accrues from", "statutory deadline"), ("Through", "award payment")]),
                     ctas=btn("/tools/appraisal-interest-calculator/", "Appraisal interest calculator", "gold") + btn("/contact/", "Free post-appraisal review", "ghost", arrow=False),
                     tool=("/tools/appraisal-interest-calculator/", "Appraisal interest calculator",
                           "Interest on the gap between pre-appraisal payments and the award, with a shortfall check."),
                     priority="0.9"))

    # ================================================================ SUPPLEMENTS
    s1 = interest(19000, 18, 75)
    prose = f'''
<h2>Why supplements are normal</h2>
<p>An adjuster inspects a loss for an hour or two. The contractor opens the roof or the wall and sees what the adjuster
couldn&rsquo;t: rotted decking under the shingles, water in the subfloor, smoke residue in the ductwork, code requirements
triggered by the permit. A <strong>supplement</strong> is a request for payment of that additional, related scope. It is
a routine part of property claims &mdash; and a routine place for delay.</p>
<h2>Common supplement items</h2>
<div class="grid g2" style="margin:1.5em 0">
<div class="card"><h3>Roof &amp; structure</h3><ul><li>Decking replacement found at tear-off</li><li>Drip edge, underlayment and ventilation required by code</li><li>Flashing, valley metal, pipe jacks</li><li>Truss or rafter damage</li></ul></div>
<div class="card"><h3>Water &amp; mold</h3><ul><li>Subfloor and framing found during demolition</li><li>Mold remediation following a covered water loss</li><li>Cabinets, trim and fixtures</li><li>HVAC contamination</li></ul></div>
<div class="card"><h3>Fire &amp; smoke</h3><ul><li>Whole-structure soot cleaning after testing</li><li>HVAC cleaning or replacement</li><li>Contents that can&rsquo;t be deodorized</li><li>Electrical and life-safety code upgrades</li></ul></div>
<div class="card"><h3>Hurricane &amp; storm</h3><ul><li>Permanent repairs after temporary tarping</li><li>Additional living expense true-ups</li><li>Recoverable depreciation after repairs</li><li>Hidden moisture damage</li></ul></div></div>
<h2>How the prompt-payment rules apply to a supplement</h2>
<p>Chapter 542 doesn&rsquo;t use the word &ldquo;supplement,&rdquo; but its deadlines are written around requests and
receipt of information: the insurer must request what it needs, decide within 15 business days of receiving it, pay
within 5 business days of accepting, and not delay payment more than 60 days after receiving what it reasonably requested.
When a supplement arrives with its documentation, those same events happen again for the supplemental amount. Texas
courts and practitioners therefore analyze a late supplement payment on its own timeline: when did the insurer receive
the supplement and the items it reasonably needed, when was payment due, and when did it pay?</p>
<p>Two principles carry over directly from the Supreme Court&rsquo;s cases:</p>
<ul><li><strong>Partial payment doesn&rsquo;t stop interest on the rest</strong> (<em>Hinojos</em>, 2021). If a carrier pays
part of a supplement and the rest is later found owed, the unpaid part can carry interest from its deadline.</li>
<li><strong>Appraisal doesn&rsquo;t erase the delay</strong> (<em>Barbara Technologies</em>, 2019). A supplement resolved
through appraisal is analyzed the same way as an original claim.</li></ul>
<div class="callout"><strong>Is it a supplement or a new claim?</strong><p>Carriers sometimes tell policyholders that
additional damage is a separate, new claim &mdash; which can mean a second deductible and a fresh set of deadlines. The
deciding question is causation: if the damage flows from the original loss event, it belongs to the original claim.
Contractor letters, dated photos and expert reports tying the new finding to the original cause are the evidence.</p></div>
<h2>How supplement interest adds up</h2>
<p>Because each supplement has its own payment date, interest is calculated per supplement and then added together. A
simple illustration: a roofer finds $19,000 of decking and code items; the carrier receives the supplement with
documentation, the 60-day deadline passes on October 4, and the carrier pays on December 18 &mdash; 75 days late. At 18%,
that delay is worth {money(s1)}; at the {FLOAT_RATE_S} weather rate, {money(interest(19000, FLOAT_RATE, 75))}. Add a
second supplement for mold or living expenses and the periods simply stack.</p>
<p>The <a href="/statutory-damages-calculator/">statutory interest calculator</a> handles this: add each supplement as a
separate component with its own deadline and payments.</p>
<h2>How carriers slow supplements</h2>
<ul><li><strong>&ldquo;We need to re-inspect.&rdquo;</strong> Re-inspection may be legitimate, but it happens on the
insurer&rsquo;s clock.</li>
<li><strong>Serial document requests.</strong> Estimates, then invoices, then photos, then a sworn proof of loss. Additional
requests are allowed only when the investigation makes them necessary (§542.055(b)).</li>
<li><strong>&ldquo;That was included in the original scope.&rdquo;</strong> A line-by-line comparison against the original
estimate answers this.</li>
<li><strong>&ldquo;It&rsquo;s been too long.&rdquo;</strong> Policies limit the time to sue and often to complete repairs for
recoverable depreciation. Track those dates.</li></ul>
<h2>Supplement best practices</h2>
<ol><li>Submit each supplement in writing with all supporting documents at once, and keep proof of the date received.</li>
<li>Ask the adjuster in writing to identify anything else needed.</li>
<li>Record each response in the <a href="/tools/claim-timeline-builder/">claim timeline builder</a>.</li>
<li>Calendar the 15-business-day and 60-day dates with the <a href="/tools/claim-deadline-calculator/">deadline calculator</a>.</li></ol>'''
    faqs = [
        ("Can I file a supplement months after the original payment?",
         "<p>Usually, if the additional damage comes from the same loss and you are within the policy&rsquo;s time limits (for "
         "repairs, recoverable depreciation and suit). Report additional damage promptly once you discover it.</p>"),
        ("When is a supplement payment due?",
         "<p>Apply the same Chapter 542 events to the supplement: decision within 15 business days of receiving what the insurer "
         "needs to evaluate it, payment within 5 business days of acceptance, and in any event within 60 days of receiving the "
         "items it reasonably requested.</p>"),
        ("How is interest calculated when there are several supplements?",
         "<p>Separately for each supplement, from its own deadline to its payment date(s), then added together.</p>"),
    ]
    out.append(guide("/long-term-claim-supplements/",
                     "Insurance Claim Supplements Paid Late in Texas | Enforce Interest",
                     "How Texas prompt-payment deadlines and interest apply to insurance claim supplements: hidden damage, "
                     "code upgrades, new-claim tactics, stacking interest across supplements, best practices.",
                     "Claim supplements", "Supplements &middot; hidden damage &middot; code upgrades",
                     "The repair started. <em>Then they found more damage.</em>",
                     "Supplements are part of almost every serious property claim. When a carrier slow-walks one, the "
                     "statutory clock runs on that money too.",
                     prose, faqs, mc("claim-supplements", "Supplements · hidden damage", "Insurance claim supplements paid late in Texas"),
                     aside=facts([("Each supplement", "own timeline"), ("Interest", f"18% / {FLOAT_RATE_S}"),
                                  ("Partial payment", "doesn&rsquo;t stop it"), ("Appraisal", "doesn&rsquo;t erase it")]),
                     ctas=ctas_std()))
    return out
