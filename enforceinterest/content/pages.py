"""Core pages: qualify quiz, FAQ, about, contact, blog index, legal, sitemap, 404."""
import lib
from lib import (FLOAT_RATE_S, JUDG_RATE_S, RATE_MONTH, FLOAT_RATE, EMAIL, FIRM, LICENSE, NAME, btn, page_hero,
                 facts, faq_block, cta_band, breadcrumbs, sec_head, esc, icon, money, interest, with_toc, side_cta)
from content import guides, products


def simple(path, title, desc, crumb, h1, lede, body_html, eyebrow="", schema=None, og=None, noindex=False,
           priority="0.5", h1_plain=None, js=None):
    trail = [("Home", "/"), (crumb, path)]
    _, bc = breadcrumbs(trail)
    import re
    p = {"path": path, "title": title, "desc": desc, "schema": [bc] + (schema or []), "priority": priority,
         "h1_plain": h1_plain or re.sub(r"<[^>]+>", "", h1).replace("&amp;", "&").replace("&rsquo;", "'"),
         "body": page_hero(trail, eyebrow or crumb, h1, lede) + body_html}
    if og:
        p["og"] = og
    if noindex:
        p["noindex"] = True
    if js:
        p["js"] = js
    return p


def build(ctx, post_pages):
    mc = ctx["make_card"]
    out = guides.build(ctx)
    out += [toolkit(mc), qualify(mc), faq(mc), about(mc), contact(mc), blog_index(mc, post_pages, ctx), privacy(), terms(),
            disclaimer(), sitemap_page()]
    return out


# ------------------------------------------------------------------ claim documentation toolkit
def toolkit(mc):
    path = "/claim-documentation-toolkit/"
    trail = [("Home", "/"), ("Claim documentation toolkit", path)]
    _, bc = breadcrumbs(trail)
    groups = {}
    for k, v in products.P.items():
        groups.setdefault(v[1], []).append(k)
    order = ["Documentation", "Inspection", "Water damage", "Freeze", "Storm", "Fire & smoke", "Prevention"]
    secs = "".join(
        f'<div style="margin-bottom:48px" data-reveal><h2 style="font-size:1.6rem">{g}</h2>'
        f'<div class="grid g3" style="margin-top:18px">{"".join(products.card(k) for k in groups[g])}</div></div>'
        for g in order if g in groups)
    faqs = [
        ("Do I need special equipment to file an insurance claim?",
         "<p>No. A phone camera and a written record of dates are the essentials. The tools here make documentation faster "
         "and more convincing, especially for water damage, where moisture readings show how far water spread.</p>"),
        ("Will my insurer reimburse these purchases?",
         "<p>Sometimes. Reasonable costs to protect property from further damage (a tarp, water extraction, drying "
         "equipment) are often covered as part of the claim. Keep receipts and submit them. Documentation gear "
         "you keep, like a scanner, usually isn&rsquo;t reimbursed.</p>"),
        ("How were these products chosen?",
         "<p>For what they add to a claim file: dated readings, clear images, organized records, or protection that "
         "satisfies your policy&rsquo;s duty to prevent further damage. We favor established brands with long review "
         "histories. Check the current price and availability on Amazon before you buy.</p>"),
    ]
    fh, fl = faq_block(faqs)

    def body():
        return (page_hero(trail, "Recommended gear &middot; Amazon", "Claim documentation <em>toolkit</em>",
                          "The tools that make a Texas property claim easier to prove: moisture meters, thermal cameras, "
                          "scanners, storm and freeze protection. Picked by a public adjusting team for what they add to the "
                          "claim file.") +
                f'''<section class="section tight"><div class="wrap">
<div class="callout" style="margin-top:0"><strong>Why gear matters to statutory interest</strong><p>The Chapter 542 clock
starts when the insurer has the items it reasonably requested. Clear photos, moisture readings and organized, dated documents
get those items to the carrier faster and leave less room for repeat requests, so the deadline is easier to prove.</p></div>
<p class="aff-note" style="margin:0 0 36px">{products.DISCLOSURE}</p>
{secs}</div></section>
<section class="section alt"><div class="wrap-narrow">{sec_head("FAQ", "Toolkit questions", center=True)}<div data-reveal>{fh}</div></div></section>''' +
                cta_band())

    p = {"path": path, "title": "Insurance Claim Documentation Toolkit | Enforce Interest",
         "desc": "Recommended tools for documenting a Texas property insurance claim: moisture meters, thermal cameras, "
                 "scanners, tarps and freeze protection.",
         "body": body, "schema": [bc, fl, {"@context": "https://schema.org", "@type": "ItemList", "name": "Claim documentation toolkit",
                                           "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": v[0]}
                                                               for i, v in enumerate(products.P.values())]}],
         "h1_plain": "Claim documentation toolkit", "priority": "0.6", "guide": True}
    p["og"] = mc("claim-documentation-toolkit", "Recommended gear", "Insurance claim documentation toolkit")
    return p


# ------------------------------------------------------------------ qualify quiz
def qualify(mc):
    path = "/does-my-claim-qualify/"
    trail = [("Home", "/"), ("Does my claim qualify?", path)]
    _, bc = breadcrumbs(trail)
    qs = [
        ("q1", "What kind of claim is it?", [
            ("prop", "My own property claim (home, rental, business property, contents)", 2),
            ("auto", "My own auto policy (collision/comprehensive)", 1),
            ("excl", "Workers&rsquo; comp, title, mortgage guaranty, bond or marine insurance", -99),
            ("third", "A claim against someone else&rsquo;s insurance", -99)]),
        ("q2", "How has the insurer handled payment?", [
            ("late", "It paid, but well after I sent what it asked for", 3),
            ("partial", "It paid part, and more was paid (or is owed) later", 3),
            ("denied_paid", "It denied the claim, then paid after I pushed back", 3),
            ("pending", "It still hasn&rsquo;t paid or decided", 2),
            ("ontime", "It paid everything promptly", -3),
            ("denied", "It denied the claim and never paid", -1)]),
        ("q3", "Did any of these happen?", [
            ("appraisal", "Appraisal produced a higher award", 3),
            ("supp", "A supplement for more damage was paid slowly", 2),
            ("both", "Both appraisal and supplements", 4),
            ("none", "None of these", 0)]),
        ("q4", "Roughly how long after you sent the requested documents did the money arrive?", [
            ("lt60", "Less than 60 days", -2),
            ("2to6", "2 to 6 months", 2),
            ("6plus", "More than 6 months", 3),
            ("unsure", "I&rsquo;m not sure", 1)]),
        ("q5", "Was any of the delay caused on your side?", [
            ("no", "No &mdash; I responded quickly and gave access", 1),
            ("some", "Some &mdash; I was slow on a few items", 0),
            ("yes", "Mostly &mdash; I didn&rsquo;t provide what was asked for months", -3)]),
        ("q6", "When did the loss happen?", [
            ("recent", "Within the last 2 years", 2),
            ("2to4", "2 to 4 years ago", 0),
            ("old", "More than 4 years ago", -2)]),
    ]
    blocks = []
    for i, (qid, q, opts) in enumerate(qs):
        btns = "".join(f'<button type="button" data-q="{qid}" data-v="{v}" data-score="{s}">{t}</button>' for v, t, s in opts)
        blocks.append(f'<div class="quiz-q{" on" if i == 0 else ""}" data-step="{i}"><span class="tag wine">Question {i + 1} of {len(qs)}</span>'
                      f'<h2 style="margin-top:14px;font-size:1.7rem">{q}</h2><div class="quiz-opts">{btns}</div>'
                      f'{"<button type=button class=quiz-back data-back>&larr; Back</button>" if i else ""}</div>')
    quiz = f'''<div class="quiz" data-tool="quiz"><div class="tool-panel" style="padding:clamp(24px,4vw,44px)">
<div class="quiz-prog"><i></i></div>{"".join(blocks)}
<div class="quiz-q" data-step="result"><div data-verdict></div>
<div class="btn-row" style="margin-top:22px">{btn("/contact/", "Send my file for a free review", "primary")}<button type="button" class="btn btn-ghost" data-restart>Start over</button></div></div>
</div></div>'''
    faqs = [
        ("What makes a Texas insurance claim qualify for statutory interest?",
         "<p>Two things: the insurer is liable for the claim (it was covered and owed), and it failed to comply with a deadline "
         "in Chapter 542, Subchapter B &mdash; most often by paying more than 60 days after receiving the items it reasonably "
         "requested (§542.058).</p>"),
        ("Does a denied claim qualify?",
         "<p>Only if the denial turns out to be wrong &mdash; for example, the insurer later pays or a court or appraisal finds "
         "money was owed. A claim found invalid in arbitration or litigation doesn&rsquo;t qualify (§542.058(b)).</p>"),
        ("Does my claim qualify if I was paid in full?",
         "<p>It can. Interest depends on <em>when</em> payment was made, not on whether you were eventually paid. A claim paid "
         "in full but late can still carry interest for the period of delay.</p>"),
    ]
    fh, fl = faq_block(faqs)

    def body():
        return (page_hero(trail, "Two-minute check &middot; free", "Does my claim <em>qualify</em>?",
                          "Under Texas law the question isn&rsquo;t the type of damage &mdash; it&rsquo;s timing. Answer six "
                          "questions and we&rsquo;ll tell you whether your claim looks worth a closer look.") +
                f'<section class="section tight"><div class="wrap">{quiz}</div></section>' +
                f'''<section class="section alt"><div class="wrap"><div class="prose" style="margin:0 auto">
<h2>The three things that have to be true</h2>
<h3>1. A covered first-party claim</h3>
<p>Your own property policy &mdash; homeowners, landlord, condo, renters or commercial property &mdash; for damage the
policy covers: hail, wind, hurricane, fire, smoke, water, theft and so on. Claims against someone else&rsquo;s insurer,
and the lines excluded by §542.053 (workers&rsquo; comp, title, mortgage guaranty, bonds, marine), don&rsquo;t qualify.</p>
<h3>2. Money that was owed</h3>
<p>Interest applies to amounts the insurer was liable for. That includes underpaid initial estimates, supplements, and
differences resolved through appraisal &mdash; whenever the final amount paid was higher than what was paid by the
deadline.</p>
<h3>3. A missed deadline</h3>
<p>The most common is §542.058: payment more than 60 days after the insurer received everything it reasonably requested.
Others are the 5-business-day payment deadline after acceptance (§542.057) and the decision deadlines in §542.056.</p>
<div class="table-scroll"><table><thead><tr><th>Scenario</th><th>Likely outcome</th></tr></thead><tbody>
<tr><td>Paid quickly and in full</td><td>Unlikely to qualify</td></tr>
<tr><td>Paid in full, but months after documents were sent</td><td>Likely worth a review</td></tr>
<tr><td>Underpaid, then corrected later</td><td>Likely worth a review</td></tr>
<tr><td>Several supplements paid slowly</td><td>Strong candidate</td></tr>
<tr><td>Appraisal award higher than prior payments</td><td>Strong candidate</td></tr>
<tr><td>Denied, then paid after pushback</td><td>Likely worth a review</td></tr>
<tr><td>Denied and never paid</td><td>Depends on whether the denial was wrong</td></tr>
<tr><td>Delay caused by the policyholder</td><td>Weak</td></tr>
</tbody></table></div>
<h2>Why people don&rsquo;t realize they qualify</h2>
<p>Because the claim feels finished. The roof is on, the checks cleared, and the timeline is forgotten. But that timeline
is exactly what decides whether interest is owed. If your quiz result says &ldquo;worth a review,&rdquo; the next step is
the dates: build them in the <a href="/tools/claim-timeline-builder/">claim timeline builder</a>, run the
<a href="/statutory-damages-calculator/">interest calculator</a>, or simply <a href="/contact/">send the file to Enforce
Interest</a>.</p></div></div></section>
<section class="section"><div class="wrap-narrow">{sec_head("FAQ", "Qualification questions", center=True)}<div data-reveal>{fh}</div></div></section>''' +
                cta_band())

    p = {"path": path, "title": "Does My Claim Qualify for 18% Interest? | Enforce Interest",
         "desc": "Free two-minute check: does your Texas insurance claim qualify for prompt-payment statutory interest under "
                 "§542.060? Covered claim, money owed, missed deadline — find out where you stand.",
         "body": body, "schema": [bc, fl], "is_tool": True, "h1_plain": "Does my claim qualify?", "priority": "0.8",
         "js": ["tools.js"]}
    p["og"] = mc("does-my-claim-qualify", "Free 2-minute check", "Does my Texas insurance claim qualify for statutory interest?")
    return p


# ------------------------------------------------------------------ FAQ
FAQ_GROUPS = [
    ("The 60-day rule", [
        ("What is the Texas 60-day rule for insurance claims?",
         "<p>Texas Insurance Code §542.058 says that once an insurer has received all items, statements and forms it reasonably "
         "requested, it may not delay payment of a covered claim for more than 60 days (unless another statute sets a different "
         "period). If it does, it owes the damages in §542.060.</p>"),
        ("When does the 60-day clock start?",
         "<p>On the date the insurer received the last item it reasonably requested under §542.055 &mdash; not necessarily the date "
         "you filed the claim. If the insurer kept requesting things it didn&rsquo;t need, the clock may have started earlier than "
         "it says; that is a fact question built from the claim file.</p>"),
        ("What other deadlines are there?",
         "<p>15 days to acknowledge, investigate and request items (§542.055); 15 business days after receiving them to accept or "
         "reject (§542.056); 5 business days to pay after accepting (§542.057). Surplus lines insurers get longer on the first and "
         "third, and a declared weather catastrophe adds 15 days (§542.059(b)).</p>"),
        ("Does the rule apply to commercial property claims?",
         "<p>Yes. It applies to first-party claims under most insurance policies, residential or commercial, except the lines "
         "excluded by §542.053.</p>"),
        ("What if the insurer says it needs more time?",
         "<p>Under §542.056(d) it must tell you, within the 15-business-day window, why it needs more time, and then accept or "
         "reject within 45 days of that notice.</p>"),
    ]),
    ("Interest &amp; rates", [
        ("How much interest does a Texas insurer owe for late payment?",
         f"<p>18% a year (simple) under §542.060(a) for most claims. For weather claims made on or after September 1, 2017, in an "
         f"action governed by Chapter 542A, the §304.003 judgment rate plus 5% &mdash; {FLOAT_RATE_S} using the {RATE_MONTH} rate "
         f"of {JUDG_RATE_S}.</p>"),
        ("What is the Act of God floating rate?",
         "<p>The informal name for §542.060(c): interest on weather (&ldquo;forces of nature&rdquo;) claims at the Finance Code "
         "§304.003 rate on the date of judgment plus five percent. Because §304.003 is floored at 5% and capped at 15%, it ranges "
         "from 10% to 20%. <a href=\"/blog/act-of-god-floating-rate/\">Full explanation</a>.</p>"),
        ("Is it the date of loss or the date of the claim that decides the rate?",
         "<p>The date the claim was made. HB 1774, Section 4(b), applies §542.060(c) only to claims made on or after September 1, "
         "2017.</p>"),
        ("Is the interest compounded?",
         "<p>No. It is simple interest on the unpaid amount, accruing daily from the date payment was required.</p>"),
        ("Do I also get attorney&rsquo;s fees?",
         "<p>§542.060 adds reasonable and necessary attorney&rsquo;s fees. In weather cases, Chapter 542A can reduce or eliminate "
         "fees depending on the pre-suit notice and the result (§542A.007).</p>"),
        ("Can I get prejudgment interest too?",
         "<p>The statute says nothing in §542.060 prevents prejudgment interest &ldquo;as provided by law.&rdquo; See our "
         "<a href=\"/texas-prejudgment-interest/\">prejudgment interest guide</a>.</p>"),
    ]),
    ("Appraisal &amp; supplements", [
        ("If the carrier paid the appraisal award, is interest still owed?",
         "<p>It can be. <em>Barbara Technologies</em> (Tex. 2019) and <em>Hinojos</em> (Tex. 2021) hold that paying an award "
         "doesn&rsquo;t by itself end prompt-payment liability; amounts owed but unpaid at the deadline can carry interest until paid.</p>"),
        ("What did Rodriguez v. Safeco decide?",
         "<p>In 2024 the Texas Supreme Court held that in a Chapter 542A case, an insurer that pays the appraisal award plus all "
         "statutory interest that could be owed isn&rsquo;t liable for attorney&rsquo;s fees under §542A.007.</p>"),
        ("Do supplements have their own deadlines?",
         "<p>Each supplement is evaluated on its own timeline &mdash; when the insurer received it and the items reasonably needed, "
         "and when it paid. Interest is calculated per supplement and added up.</p>"),
    ]),
    ("Working with Enforce Interest", [
        ("Are you a law firm?",
         f"<p>No. Enforce Interest is a service of {FIRM}, a Texas-licensed public adjusting firm (license #{LICENSE}). We adjust "
         "and document claims and present them to carriers. We don&rsquo;t give legal advice or file lawsuits.</p>"),
        ("What does it cost?",
         "<p>The review is free. If we take the engagement, our fee is a contingency percentage of the recovery, within the 10% "
         "Texas cap (§4102.104). No recovery, no fee.</p>"),
        ("Will you refer me to an attorney?",
         "<p>Texas law bars public adjusters from soliciting employment for attorneys (§4102.158(d)). If your situation needs a "
         "lawyer, we will tell you so; choosing one is up to you.</p>"),
        ("What should I send for a review?",
         "<p>Your declarations page, claim letters and emails, every payment letter or check stub, estimates, any appraisal "
         "documents and a short description of what happened. Use the <a href=\"/contact/\">contact form</a>.</p>"),
        ("Do you work outside Texas?",
         "<p>No. Enforce Interest works only on Texas claims under Texas law.</p>"),
    ]),
    ("Deadlines to act", [
        ("How long do I have to sue my insurance company in Texas?",
         "<p>Check the policy&rsquo;s &ldquo;suit against us&rdquo; condition &mdash; often two years and one day from when the "
         "cause of action accrues. Texas voids contractual limits shorter than two years (§16.070). Chapter 541 claims have a "
         "two-year limit (§541.162). When a claim accrues is a legal question; talk to an attorney well before any deadline.</p>"),
        ("How long do I have to file a claim?",
         "<p>Policies usually require prompt notice; some set a fixed window. TWIA claims must be filed within one year of the "
         "damage (§2210.573).</p>"),
        ("What is the 542A pre-suit notice?",
         "<p>For weather claims, written notice to the insurer at least 61 days before suit, stating the complaint, the amount "
         "owed and attorney&rsquo;s fees incurred (§542A.003). <a href=\"/blog/542a-pre-suit-notice-explained/\">Details here</a>.</p>"),
    ]),
]


def faq(mc):
    path = "/faq/"
    trail = [("Home", "/"), ("FAQ", path)]
    _, bc = breadcrumbs(trail)
    all_items = [it for _, items in FAQ_GROUPS for it in items]
    _, fl = faq_block(all_items)
    secs = ""
    nav = ""
    for g, items in FAQ_GROUPS:
        sid = lib.slugify(g)
        fh, _ = faq_block(items)
        nav += f'<a href="#{sid}" class="tag" style="text-decoration:none">{g}</a> '
        secs += f'<div id="{sid}" style="margin-bottom:56px" data-reveal><h2 style="font-size:1.7rem">{g}</h2>{fh}</div>'
    body = (page_hero(trail, "Texas prompt-payment law", "Frequently asked <em>questions</em>",
                      "Straight answers about the Texas 60-day rule, 18% and floating-rate interest, appraisal, supplements "
                      "and how Enforce Interest works.") +
            f'<section class="section"><div class="wrap-narrow"><div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:40px">{nav}</div>{secs}</div></section>' +
            cta_band())
    p = {"path": path, "title": "Texas 60-Day Rule & Claim Interest FAQ | Enforce Interest",
         "desc": "Answers on the Texas 60-day rule, 18% and floating-rate prompt-payment interest, appraisal awards, supplements, "
                 "deadlines to sue and how Enforce Interest's free claim review works.",
         "body": body, "schema": [bc, fl], "h1_plain": "Frequently asked questions", "priority": "0.7"}
    p["og"] = mc("faq", "FAQ", "Texas 60-day rule and claim interest: frequently asked questions")
    return p


# ------------------------------------------------------------------ about
def about(mc):
    path = "/about-us/"
    body_html = f'''
<section class="section"><div class="wrap split">
<div data-reveal="left"><span class="eyebrow">Our focus</span><h2>The work most policyholders never realize they&rsquo;re owed.</h2>
<p class="lede">Insurance claims don&rsquo;t just get delayed. They get underpaid, re-inspected, supplemented and dragged out
&mdash; sometimes for months, sometimes for years.</p>
<p>What most policyholders never hear is that in Texas, delay isn&rsquo;t only an inconvenience. Under Chapter 542 of the
Insurance Code it creates a financial liability for the carrier. Enforce Interest exists to identify that liability and
document it so it can be recovered.</p>
<p>We are not a general-purpose claims shop. Enforce Interest is a service of {FIRM}, a Texas Department of
Insurance&ndash;licensed public adjusting firm (license #{LICENSE}) based in Austin, and it concentrates on one question:
<strong>when should the carrier have paid, and when did it actually pay?</strong></p></div>
<div data-reveal="right">{facts([("Firm", FIRM), ("License", f"TDI #{LICENSE}"), ("Based in", "Austin, Texas"), ("Service area", "All of Texas"), ("Contact", EMAIL)])}</div>
</div></section>
<section class="section alt"><div class="wrap">
{sec_head("What we do", "Timeline-driven claim analysis.", "Every Enforce Interest engagement follows the same disciplined process.")}
<div class="steps-h" data-stagger>
<div class="step-h"><h3>Review the history</h3><p>Policy, claim letters, inspections, estimates, payments, supplements and appraisal &mdash; everything with a date on it.</p></div>
<div class="step-h"><h3>Find the triggers</h3><p>When notice was given, what was requested, when each item arrived and when each payment was due.</p></div>
<div class="step-h"><h3>Calculate</h3><p>Interest on each late amount at the right rate, period by period, with every figure traceable.</p></div>
<div class="step-h"><h3>Present &amp; recover</h3><p>A clear written presentation to the carrier, and follow-through until the claim is resolved.</p></div>
</div></div></section>
<section class="section"><div class="wrap">
{sec_head("How interest builds", "Each phase of a claim can carry its own consequences.")}
<div class="table-scroll" data-reveal><table><thead><tr><th>Scenario</th><th>What happens</th><th>Why it matters</th></tr></thead><tbody>
<tr><td>Late initial payment</td><td>Carrier pays after its §542.057 or §542.058 deadline</td><td>Interest on the late amount for each day of delay</td></tr>
<tr><td>Underpayment corrected later</td><td>More money is paid months afterwards</td><td>Interest on the difference from the original deadline (<em>Hinojos</em>)</td></tr>
<tr><td>Supplement delay</td><td>Additional damage submitted; payment stalls</td><td>The supplement is evaluated on its own timeline</td></tr>
<tr><td>Appraisal award</td><td>Carrier pays the award after the dispute</td><td>Paying the award doesn&rsquo;t by itself end prompt-payment liability</td></tr>
</tbody></table></div></div></section>
<section class="section dark"><div class="wrap split">
<div data-reveal="left"><span class="eyebrow">Who we help</span><h2>Homeowners and businesses with claims that took too long.</h2>
<ul class="check" style="color:rgba(255,255,255,.85)"><li>Homeowners with delayed or underpaid claims</li><li>Property owners dealing with supplements</li>
<li>Policyholders who went through appraisal</li><li>Commercial property claimants with complex, multi-payment timelines</li></ul></div>
<div data-reveal="right"><div class="card dark-card" style="padding:30px"><h3>What we hear most</h3>
<p>&ldquo;My insurance paid &mdash; but it took months.&rdquo;</p><p>&ldquo;They sent more money later and never explained why.&rdquo;</p>
<p>&ldquo;We had to file supplement after supplement.&rdquo;</p><p>&ldquo;We won appraisal, and that was it.&rdquo;</p>
<p style="color:var(--gold-2)">If that sounds familiar, the interest was probably never addressed.</p></div></div>
</div></section>
<section class="section"><div class="wrap grid g3" data-stagger>
<div class="card"><div class="ico">{icon("scale")}</div><h3>Built for Texas law</h3><p>Our work is grounded in Chapter 542, Chapter 542A, the Texas Supreme Court&rsquo;s appraisal decisions and current OCCC rates &mdash; not generic claim advice.</p></div>
<div class="card"><div class="ico">{icon("shield")}</div><h3>Licensed and accountable</h3><p>Public adjusters in Texas are licensed and regulated by TDI under Chapter 4102. Our fees are contingent and within the 10% statutory cap.</p></div>
<div class="card"><div class="ico">{icon("doc")}</div><h3>Honest about limits</h3><p>We are not a law firm and don&rsquo;t give legal advice. If a claim needs litigation, we&rsquo;ll say so plainly.</p></div>
</div></section>
<section class="section alt"><div class="wrap-narrow center" data-reveal>
<span class="eyebrow">Our perspective</span><h2>Claims are treated like transactions. They&rsquo;re really timelines.</h2>
<p class="lede">And timelines create obligations. Every day past a statutory deadline has a value set by Texas law. Most people
never calculate it. Enforce Interest does.</p></div></section>''' + cta_band()
    p = simple(path, "About Enforce Interest | Rise Public Adjusting, Texas",
               f"Enforce Interest is a {FIRM} service (TDI license #{LICENSE}) focused on Texas prompt-payment statutory interest "
               "for late-paid property insurance claims. Who we are and how we work.",
               "About us", "About <em>Enforce Interest</em>",
               "A Texas-licensed public adjusting service built around one part of the Insurance Code: the deadlines insurers "
               "must meet, and the interest they owe when they don&rsquo;t.", body_html, eyebrow=f"A {FIRM} service",
               schema=[{"@context": "https://schema.org", "@type": "AboutPage", "url": lib.SITE + path, "name": "About Enforce Interest",
                        "about": {"@id": lib.SITE + "/#org"}}], priority="0.6")
    p["og"] = mc("about", f"A {FIRM} service", "About Enforce Interest")
    return p


# ------------------------------------------------------------------ contact
def contact(mc):
    path = "/contact/"
    radios = lambda name, opts: '<div class="radio-row">' + "".join(
        f'<label><input type="radio" name="{name}" value="{v}"><span>{v}</span></label>' for v in opts) + '</div>'
    form = f'''<form class="form-card" id="claim-form" action="/contact.php" method="post" enctype="multipart/form-data" novalidate data-reveal>
<h2 style="font-size:1.6rem">Free claim review</h2>
<p class="muted" style="font-size:.94rem">Tell us about the claim. The more dates you can give, the faster we can answer. Fields marked * are required.</p>
<div class="row2"><div class="field"><label for="f-name">Full name *</label><input id="f-name" name="name" required autocomplete="name"></div>
<div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="(512) 555-0100"></div></div>
<div class="row2"><div class="field"><label for="f-email">Email *</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="f-ins">Insurance company</label><input id="f-ins" name="insurer"></div></div>
<div class="row3"><div class="field"><label for="f-type">Type of claim</label><select id="f-type" name="claim_type"><option>Hail / wind</option><option>Hurricane</option><option>Fire / smoke</option><option>Water / plumbing</option><option>Freeze</option><option>Other</option></select></div>
<div class="field"><label for="f-dol">Date of loss</label><input id="f-dol" name="date_of_loss" type="date"></div>
<div class="field"><label for="f-claim">Claim number</label><input id="f-claim" name="claim_number"></div></div>
<div class="row2"><div class="field"><span class="lab">Any supplements filed?</span>{radios("supplements", ["Yes", "No"])}</div>
<div class="field"><span class="lab">Did the claim go to appraisal?</span>{radios("appraisal", ["Yes", "No"])}</div></div>
<div class="row2"><div class="field"><span class="lab">Denied, then later paid?</span>{radios("denied_then_paid", ["Yes", "No"])}</div>
<div class="field"><span class="lab">Do you believe it was underpaid?</span>{radios("underpaid", ["Yes", "No", "Not sure"])}</div></div>
<div class="row2"><div class="field"><label for="f-amt">Approximate total paid so far</label><div class="money"><input id="f-amt" name="amount_paid" type="number" min="0" step="1"></div></div>
<div class="field"><label for="f-county">Property city / county (Texas)</label><input id="f-county" name="location"></div></div>
<div class="field"><label for="f-msg">What happened? *</label><textarea id="f-msg" name="message" required placeholder="Key dates: when you reported it, what the insurer asked for, when you sent it, when each payment arrived."></textarea></div>
<div class="field"><span class="lab">Documents (optional): PDF, JPG or PNG, up to 5 files, 10 MB total</span>
<label class="file-drop" id="file-drop"><input type="file" name="files[]" multiple accept=".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png"><span data-file-label>Drop or choose claim letters, payment stubs, estimates</span></label>
<span class="help">Please don&rsquo;t upload privileged attorney&ndash;client communications.</span></div>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
<input type="hidden" name="t" value="">
<label class="chk"><input type="checkbox" name="consent" value="yes" required><span>I agree to be contacted about my claim review. *</span></label>
<button class="btn btn-primary" type="submit">Analyze my claim{lib.ARROW}</button>
<div class="form-status" role="status" aria-live="polite"></div>
</form>'''
    aside = f'''<div class="contact-aside">
<div class="card" data-reveal><div class="ico">{icon("mail")}</div><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a><br>We usually reply within one business day.</p></div>
<div class="card" data-reveal><div class="ico">{icon("doc")}</div><h3>What to have ready</h3><ul><li>Declarations page</li><li>Claim letters and emails</li><li>Payment letters / check stubs</li><li>Estimates and supplements</li><li>Appraisal award, if any</li></ul></div>
<div class="card" data-reveal><div class="ico">{icon("shield")}</div><h3>No cost, no pressure</h3><p>The review is free. If there&rsquo;s something to recover, we&rsquo;ll show you where. If not, you&rsquo;ll know that too.</p></div>
<div class="card" data-reveal><div class="ico">{icon("pin")}</div><h3>{FIRM}</h3><p>Texas public adjuster license #{LICENSE}<br>Austin, Texas &middot; serving all of Texas</p></div>
</div>'''
    body_html = (f'<section class="section"><div class="wrap" style="display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:32px" id="contact-grid">'
                 f'{form}{aside}</div></section><style>@media (max-width:900px){{#contact-grid{{grid-template-columns:minmax(0,1fr)!important}}}}</style>')
    p = simple(path, "Free Claim Review | Contact Enforce Interest",
               "Send your Texas insurance claim to Enforce Interest for a free review. We rebuild the timeline, calculate "
               "§542.060 statutory interest and tell you whether anything is owed. No upfront cost.",
               "Contact", "Let&rsquo;s find out what you&rsquo;re <em>owed</em>",
               "If your claim felt slow, complicated or paid in pieces, send us the details. We&rsquo;ll look at the timeline, "
               "the payments and where interest may apply &mdash; no assumptions, no pressure.", body_html,
               eyebrow="Free claim review &middot; Texas only",
               schema=[{"@context": "https://schema.org", "@type": "ContactPage", "url": lib.SITE + path,
                        "name": "Contact Enforce Interest", "about": {"@id": lib.SITE + "/#org"}}], priority="0.7")
    p["og"] = mc("contact", "Free claim review", "Let's find out what you're owed")
    return p


# ------------------------------------------------------------------ blog index
def blog_index(mc, post_pages, ctx):
    path = "/blog/"
    trail = [("Home", "/"), ("Blog", path)]
    _, bc = breadcrumbs(trail)
    posts = sorted(post_pages, key=lambda p: p["published"], reverse=True)
    sections = []
    for p in posts:
        if p["section"] not in sections:
            sections.append(p["section"])

    def body():
        pic = ctx["pic"]
        cards = "".join(
            f'<a class="card post-card" href="{p["path"]}" data-cat="{lib.slugify(p["section"])}"><div class="pc-img">{pic(p["og"], p["h1_plain"])}</div>'
            f'<div class="pc-body"><span class="tag wine">{p["section"]}</span><h3 style="margin-top:12px">{p["h1"]}</h3>'
            f'<p>{esc(p["desc"])}</p><span class="meta">{p["date_h"]} &middot; {p["read"]} min read</span></div></a>' for p in posts)
        filt = '<button type="button" aria-pressed="true" data-filter="all">All</button>' + "".join(
            f'<button type="button" aria-pressed="false" data-filter="{lib.slugify(s)}">{s}</button>' for s in sections)
        return (page_hero(trail, "Guides &middot; case law &middot; deadlines", "The Enforce Interest <em>blog</em>",
                          "Plain-English guides to Texas prompt-payment law, claim deadlines, appraisal and the interest insurers "
                          "owe when they pay late.") +
                f'<section class="section"><div class="wrap"><div class="filters" data-filters>{filt}</div>'
                f'<div class="grid g3" data-posts>{cards}</div></div></section>' + cta_band())
    p = {"path": path, "title": "Texas Insurance Claim Interest Blog | Enforce Interest",
         "desc": "Guides to Texas prompt-payment interest: the 18% rate, the floating weather rate, Hinojos, 542A notice, "
                 "freeze claims, smoke damage, claim deadlines and policy cancellation rules.",
         "body": body, "priority": "0.7", "freq": "weekly", "h1_plain": "The Enforce Interest blog",
         "schema": [bc, {"@context": "https://schema.org", "@type": "Blog", "name": f"{NAME} blog", "url": lib.SITE + path,
                         "publisher": {"@id": lib.SITE + "/#org"},
                         "blogPost": [{"@type": "BlogPosting", "headline": p["h1_plain"], "url": lib.SITE + p["path"],
                                       "datePublished": p["published"]} for p in posts]}]}
    p["og"] = mc("blog", "Enforce Interest blog", "Guides to Texas insurance claim interest")
    return p


# ------------------------------------------------------------------ legal
def legal(path, title, desc, h1, prose):
    prose, toc = with_toc(prose)
    body = (f'<section class="section"><div class="wrap article-wrap"><article class="prose">{prose}</article>'
            f'<aside class="article-side">{toc}{side_cta()}</aside></div></section>')
    return simple(path, title, desc, h1, h1, f"Last updated {lib.BUILD_DATE}.", body, eyebrow="Legal", priority="0.3")


def privacy():
    return legal("/privacy-policy/", "Privacy Policy | Enforce Interest",
                 "How Enforce Interest collects, uses and protects information you submit through enforceinterest.com, "
                 "including claim review requests and documents.", "Privacy policy", f'''
<h2>Who we are</h2><p>enforceinterest.com is operated by {FIRM} (&ldquo;we,&rdquo; &ldquo;us&rdquo;), a Texas public adjusting
firm. Questions about this policy: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>What we collect</h2><ul>
<li><strong>Information you send us</strong> through the claim review form or by email: name, contact details, insurer,
claim details, and any documents you upload.</li>
<li><strong>Technical information</strong> our web host records automatically in server logs, such as IP address, browser
type, pages requested and time of request.</li></ul>
<h2>Calculators and tools</h2><p>Our calculators run entirely in your browser. The figures you enter are not sent to us. The
claim timeline builder stores your entries in your own browser&rsquo;s local storage so they are there when you return; you
can clear them at any time with the &ldquo;Clear all&rdquo; button or your browser settings.</p>
<h2>How we use information</h2><ul><li>To review your claim and respond to you.</li><li>To provide public adjusting services if you
engage us.</li><li>To keep our website secure and working.</li><li>To comply with legal and licensing obligations.</li></ul>
<p>We do not sell personal information, and we do not share it with third parties for their marketing.</p>
<h2>Cookies</h2><p>The site does not use advertising or analytics cookies. Fonts are loaded from Google Fonts, which may log
your IP address when delivering them.</p>
<h2>Retention and security</h2><p>We keep claim information as long as needed to evaluate and handle the claim and to meet
record-keeping requirements, and we use reasonable safeguards to protect it. No method of transmission over the internet
is completely secure.</p>
<h2>Your choices</h2><p>You may ask us to access, correct or delete personal information you have sent us by emailing
{EMAIL}.</p>
<h2>Changes</h2><p>We may update this policy and will change the date above when we do.</p>''')


def terms():
    return legal("/terms-of-use/", "Terms of Use | Enforce Interest",
                 "Terms governing use of enforceinterest.com, its calculators and educational content, provided by Rise "
                 "Public Adjusting.", "Terms of use", f'''
<h2>Acceptance</h2><p>By using enforceinterest.com you agree to these terms. If you don&rsquo;t agree, please don&rsquo;t use the site.</p>
<h2>No legal advice</h2><p>{NAME} is a service of {FIRM}, a licensed public adjusting firm. We are not a law firm. Content and
tools on this site are general information about Texas insurance law and claim handling; they are not legal advice and don&rsquo;t
create an attorney&ndash;client or adjuster&ndash;client relationship. A public adjusting engagement begins only when you sign a
written contract with us.</p>
<h2>Calculators</h2><p>Calculator results are estimates based on the information you enter and on the statutes and published
rates they cite as of the date shown. Whether interest is actually owed depends on facts, policy language and law that a
calculator can&rsquo;t evaluate. Verify important dates and rates independently.</p>
<h2>Accuracy</h2><p>We work to keep the site accurate and current, but laws, rates and court decisions change. We make no
warranty that the content is complete, current or error-free.</p>
<h2>Intellectual property</h2><p>Site content, design and code are owned by {FIRM} unless stated otherwise. You may share links
and quote brief excerpts with attribution.</p>
<h2>Limitation of liability</h2><p>To the extent permitted by law, {FIRM} is not liable for any damages arising from use of this
site or reliance on its content or tools.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of the State of Texas.</p>
<h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p>''')


def disclaimer():
    return legal("/disclaimer/", "Disclaimer | Enforce Interest",
                 "Enforce Interest is a public adjusting service, not a law firm. Important information about the educational "
                 "content, calculators and licensing on this site.", "Disclaimer", f'''
<h2>Public adjuster, not a law firm</h2><p>{NAME} is a service of {FIRM}, a public adjusting firm licensed by the Texas
Department of Insurance (license #{LICENSE}). We are not attorneys, and nothing on this site is legal advice. Our services are
limited to public adjusting: investigating, documenting, estimating and presenting first-party property insurance claims on
behalf of policyholders, including the statutory interest that may be owed on them.</p>
<h2>Attorney referrals</h2><p>Under Texas Insurance Code §4102.158, a public adjuster may not solicit employment for an attorney
or contract with an insured primarily to refer them to one. We don&rsquo;t receive anything for recommending a lawyer.</p>
<h2>Fees</h2><p>Public adjuster compensation in Texas may not exceed 10% of the insurance settlement on the claim (§4102.104).
Any engagement with us is in writing and states the fee.</p>
<h2>Affiliate links</h2><p>Some pages recommend products through Amazon links. As an Amazon Associate, Enforce Interest
earns from qualifying purchases, at no extra cost to you. Affiliate links are marked as sponsored, and we don&rsquo;t accept payment
from manufacturers for recommendations.</p>
<h2>Educational content</h2><p>Articles, examples and calculators explain general principles of Texas law as of the date
published. Examples are illustrations, not predictions; outcomes depend on the facts of each claim, the policy and the
carrier&rsquo;s conduct. Past results don&rsquo;t guarantee future results.</p>
<h2>Rates</h2><p>The floating interest rate under Insurance Code §542.060(c) depends on the Finance Code §304.003 rate on the
date of judgment. Rates shown on this site come from the Office of Consumer Credit Commissioner and are updated when the site
is rebuilt; confirm the current rate with the OCCC.</p>
<h2>Texas only</h2><p>Our services and content concern Texas claims and Texas law only.</p>''')


def sitemap_page():
    trail = [("Home", "/"), ("Sitemap", "/sitemap/")]
    _, bc = breadcrumbs(trail)
    return {"path": "/sitemap/", "title": "Sitemap | Enforce Interest", "desc": "Every page on enforceinterest.com: guides, claim types, free tools and blog articles.",
            "schema": [bc], "priority": "0.3", "h1_plain": "Sitemap",
            "body": page_hero(trail, "All pages", "Site<em>map</em>", "Every guide, tool and article on Enforce Interest.") +
            '<section class="section"><div class="wrap grid g2"><!--SITEMAP--></div></section>'}


def not_found():
    return {"path": "/404/", "title": "Page not found | Enforce Interest", "desc": "That page doesn't exist on Enforce Interest.",
            "noindex": True, "h1_plain": "Page not found",
            "body": f'''<section class="page-hero dark"><div class="hero-sect" aria-hidden="true">§</div><div class="wrap">
<span class="eyebrow">Error 404</span><h1>This page missed its <em>deadline</em>.</h1>
<p class="lede">The page you were looking for doesn&rsquo;t exist or has moved. Try one of these instead.</p>
<div class="btn-row">{btn("/", "Home", "gold")}{btn("/statutory-damages-calculator/", "Interest calculator", "ghost", arrow=False)}{btn("/blog/", "Blog", "ghost", arrow=False)}</div></div></section>'''}
