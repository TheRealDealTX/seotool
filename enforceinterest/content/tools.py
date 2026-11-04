"""Free tool pages. Interactive logic lives in assets/js/tools.js (data-tool="...")."""
import lib
from lib import (FLOAT_RATE_S, JUDG_RATE_S, RATE_MONTH, FLOAT_RATE, OCCC_RATES, MONTHS, btn, cite, icon, page_hero,
                 faq_block, cta_band, breadcrumbs, facts, esc, money, interest, sec_head)

TOOL_LIST = [
    {"path": "/statutory-damages-calculator/", "short": "Statutory interest calculator", "icon": "calc",
     "blurb": "§542.060 interest on late payments, partial payments and supplements, at 18% or the floating rate."},
    {"path": "/tools/claim-deadline-calculator/", "short": "Claim deadline calculator", "icon": "calendar",
     "blurb": "Every Chapter 542 deadline from your notice date, with business days and Texas holidays."},
    {"path": "/tools/appraisal-interest-calculator/", "short": "Appraisal interest calculator", "icon": "scale",
     "blurb": "Hinojos-style interest on the gap between what was paid and the appraisal award."},
    {"path": "/does-my-claim-qualify/", "short": "Does my claim qualify?", "icon": "check",
     "blurb": "A two-minute check of whether your claim timeline is worth a closer look."},
    {"path": "/texas-judgment-interest-rate/", "short": "Judgment interest rate tracker", "icon": "chart",
     "blurb": f"Every OCCC §304.003 rate since 2005 and the matching §542.060(c) rate ({FLOAT_RATE_S} now)."},
    {"path": "/texas-prejudgment-interest/", "short": "Prejudgment interest calculator", "icon": "percent",
     "blurb": "Texas Finance Code ch. 304 accrual dates and interest for property damage claims."},
    {"path": "/tools/542a-notice-calculator/", "short": "542A notice &amp; fee calculator", "icon": "doc",
     "blurb": "61-day pre-suit notice dates, the insurer&rsquo;s inspection window and the attorney-fee ratio."},
    {"path": "/tools/claim-timeline-builder/", "short": "Claim timeline builder", "icon": "list",
     "blurb": "Log every claim event, see which deadlines passed and print a status-request letter."},
    {"path": "/tools/public-adjuster-fee-calculator/", "short": "Public adjuster fee calculator", "icon": "shield",
     "blurb": "What a Texas public adjuster can charge (10% cap) and what you net."},
    {"path": "/tools/depreciation-calculator/", "short": "ACV &amp; depreciation calculator", "icon": "layers",
     "blurb": "Replacement cost, actual cash value and recoverable depreciation, line by line."},
    {"path": "/tools/wind-hail-deductible-calculator/", "short": "Wind &amp; hail deductible calculator", "icon": "wind",
     "blurb": "Percentage deductibles in dollars, and what a storm claim actually pays."},
]


# ------------------------------------------------------------------ form helpers
def f_date(name, label, help_="", req=False, value=""):
    h = f'<span class="help">{help_}</span>' if help_ else ""
    r = " required" if req else ""
    v = f' value="{value}"' if value else ""
    return f'<div class="field"><label for="{name}">{label}</label><input type="date" id="{name}" name="{name}"{r}{v}>{h}</div>'


def f_money(name, label, help_="", value="", ph=""):
    h = f'<span class="help">{help_}</span>' if help_ else ""
    v = f' value="{value}"' if value else ""
    p = f' placeholder="{ph}"' if ph else ""
    return (f'<div class="field"><label for="{name}">{label}</label><div class="money"><input type="number" inputmode="decimal" '
            f'min="0" step="0.01" id="{name}" name="{name}"{v}{p}></div>{h}</div>')


def f_num(name, label, help_="", value="", step="1", suffix=""):
    h = f'<span class="help">{help_}</span>' if help_ else ""
    wrap_o, wrap_c = ('<div class="pct">', '</div>') if suffix == "%" else ("", "")
    return (f'<div class="field"><label for="{name}">{label}</label>{wrap_o}<input type="number" inputmode="decimal" step="{step}" '
            f'min="0" id="{name}" name="{name}" value="{value}">{wrap_c}{h}</div>')


def f_text(name, label, ph="", help_=""):
    h = f'<span class="help">{help_}</span>' if help_ else ""
    return f'<div class="field"><label for="{name}">{label}</label><input type="text" id="{name}" name="{name}" placeholder="{ph}" autocomplete="off">{h}</div>'


def f_select(name, label, options, help_="", selected=None):
    h = f'<span class="help">{help_}</span>' if help_ else ""
    opts = "".join(f'<option value="{v}"{" selected" if v == selected else ""}>{t}</option>' for v, t in options)
    return f'<div class="field"><label for="{name}">{label}</label><select id="{name}" name="{name}">{opts}</select>{h}</div>'


def seg(name, label, options, checked=0):
    o = "".join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if i == checked else ""}><span>{t}{f"<small>{s}</small>" if s else ""}</span></label>'
                for i, (v, t, s) in enumerate(options))
    return f'<div class="field"><span class="lab">{label}</span><div class="seg">{o}</div></div>'


def chk(name, label, checked=False):
    return f'<label class="chk"><input type="checkbox" name="{name}"{" checked" if checked else ""}><span>{label}</span></label>'


def rate_month_select(name="rateMonth", label="§304.003 rate month"):
    opts = []
    for y in sorted(OCCC_RATES, reverse=True):
        if y < 2017:
            continue
        for m in range(len(OCCC_RATES[y]) - 1, -1, -1):
            v = OCCC_RATES[y][m]
            opts.append((f"{y}-{m + 1:02d}", f"{MONTHS[m]} {y} &mdash; {v:.2f}% (&rarr; {v + 5:.2f}%)"))
    return f_select(name, label, opts, "For the floating rate. In court it is fixed on the date of judgment; for an estimate use the latest month.")


def results_shell(inner, actions=True):
    act = ('<div class="result-actions no-print"><button type="button" data-act="copy">Copy summary</button>'
           '<button type="button" data-act="print">Print / save PDF</button><button type="button" data-act="csv">Download CSV</button>'
           '<button type="button" data-act="link">Copy shareable link</button></div>') if actions else ""
    return f'<aside class="results"><div class="result-card" aria-live="polite">{inner}{act}<div class="result-note" data-note></div></div></aside>'


def related(paths):
    items = [t for t in TOOL_LIST if t["path"] in paths]
    cards = "".join(f'<a class="card" href="{t["path"]}"><div class="ico">{icon(t["icon"])}</div><h3>{t["short"]}</h3><p>{t["blurb"]}</p><span class="more">Open tool</span></a>' for t in items)
    return f'<section class="section tight alt"><div class="wrap"><h2 style="font-size:1.6rem">Related tools</h2><div class="grid g3" style="margin-top:22px" data-stagger>{cards}</div></div></section>'


def app_schema(name, path, desc):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "url": lib.SITE + path,
            "description": desc, "applicationCategory": "FinanceApplication", "operatingSystem": "Any (web browser)",
            "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "publisher": {"@id": lib.SITE + "/#org"}}


def tool_page(path, title, desc, crumb, eyebrow, h1, lede, tool_html, content_html, faqs, rel, h1_plain, og_kicker,
              aside="", priority="0.8", schema_name=None):
    trail = [("Home", "/"), ("Tools", "/tools/"), (crumb, path)] if path.startswith("/tools/") else [("Home", "/"), ("Tools", "/tools/"), (crumb, path)]
    _, bc = breadcrumbs(trail)
    fh, fl = faq_block(faqs) if faqs else ("", None)

    def body():
        faq_sec = (f'<section class="section"><div class="wrap-narrow">{sec_head("FAQ", "Questions about this tool", center=True)}'
                   f'<div data-reveal>{fh}</div></div></section>') if faqs else ""
        return (page_hero(trail, eyebrow, h1, lede, aside=aside) +
                f'<section class="section tight"><div class="wrap">{tool_html}</div></section>' +
                f'<section class="section alt"><div class="wrap"><div class="prose" style="margin:0 auto">{content_html}</div></div></section>' +
                faq_sec + related(rel) + cta_band())

    schema = [bc, app_schema(schema_name or h1_plain, path, desc)] + ([fl] if fl else [])
    return {"path": path, "title": title, "desc": desc, "body": body, "schema": schema, "is_tool": True,
            "h1_plain": h1_plain, "priority": priority, "js": ["rates.js", "tools.js"], "og_kicker": og_kicker}


# ------------------------------------------------------------------ pages
def ledger_tool():
    comp_tpl = f'''<template id="tpl-component"><div class="component" data-component>
  <div class="component-head"><input type="text" data-c="label" aria-label="Component name" value="Original claim">
    <button type="button" class="icon-btn" data-remove-component aria-label="Remove this component" title="Remove">&times;</button></div>
  <div class="seg" style="margin-bottom:14px"><label><input type="radio" data-c="mode" value="due" checked><span>I know the payment deadline</span></label><label><input type="radio" data-c="mode" value="items"><span>Compute it from the items-received date</span></label></div>
  <div class="row2">
    <div class="field" data-show="due"><label>Date payment was required</label><input type="date" data-c="due"><span class="help">The deadline that was missed (e.g. §542.057 or §542.058).</span></div>
    <div class="field" data-show="items" hidden><label>Date insurer received all requested items</label><input type="date" data-c="items"><span class="help">Deadline = this date + 60 days (§542.058).</span></div>
    <div class="field"><label>Amount owed on this component</label><div class="money"><input type="number" min="0" step="0.01" inputmode="decimal" data-c="amount" placeholder="50000"></div><span class="help">Final amount owed (e.g. agreed or appraised figure, less deductible).</span></div>
  </div>
  <label class="chk" data-show="items" hidden><input type="checkbox" data-c="cat"><span>Declared weather catastrophe: add 15 days (§542.059(b))</span></label>
  <div class="lab" style="font:600 .86rem var(--sans);margin:6px 0 8px">Payments on this component</div>
  <div class="pay-list" data-pays></div>
  <button type="button" class="add-btn" data-add-pay>+ Add a payment</button>
</div></template>
<template id="tpl-pay"><div class="pay-row" data-pay>
  <div class="field"><label>Payment date</label><input type="date" data-p="date"></div>
  <div class="field"><label>Amount paid</label><div class="money"><input type="number" min="0" step="0.01" inputmode="decimal" data-p="amount"></div></div>
  <button type="button" class="icon-btn" data-remove-pay aria-label="Remove payment">&times;</button>
</div></template>'''
    return f'''<div class="tool-shell" data-tool="ledger">
<form class="tool-form" onsubmit="return false" novalidate>
  <div class="tool-panel">
    <h2><span class="n">I</span>Claim particulars</h2><p class="hint">Optional &mdash; used only to label your printed memo. Nothing leaves your browser.</p>
    <div class="row3">{f_text("insured", "Insured", "Policyholder")}{f_text("carrier", "Carrier", "Insurance company")}{f_text("claimref", "Claim no.", "Optional")}</div>
  </div>
  <div class="tool-panel">
    <h2><span class="n">II</span>Which rate applies?</h2><p class="hint">§542.060(c) applies to weather claims made on or after Sept. 1, 2017 (HB 1774, §4(b)); everything else uses 18%.</p>
    {seg("cause", "What caused the damage?", [("weather", "Forces of nature", "hail, wind, storm, flood&hellip;"), ("other", "Something else", "fire, water, theft&hellip;")], 1)}
    {f_date("claimMade", "Date the claim was made", "When you first reported the claim to the insurer.")}
    {seg("regime", "Rate", [("auto", "Auto", "from the answers above"), ("std", "18%", "§542.060(a)"), ("float", "Floating", "§542.060(c)")])}
    <div data-float-only hidden>{rate_month_select()}</div>
    <div class="callout" data-regime-note style="margin:6px 0 0;font-size:.9rem"></div>
  </div>
  <div class="tool-panel">
    <h2><span class="n">III</span>Amounts, deadlines &amp; payments</h2><p class="hint">Add the original claim and each supplement separately &mdash; each has its own deadline. Payments made on or before the deadline reduce the amount interest runs on.</p>
    <div data-components></div>
    <button type="button" class="add-btn" data-add-component>+ Add a supplement / separate component</button>
  </div>
  <div class="tool-panel">
    <h2><span class="n">IV</span>Accrue through</h2>
    {f_date("through", "Calculate interest through", "Unpaid balances accrue to this date. Defaults to today.")}
  </div>
  {comp_tpl}
</form>
{results_shell(f"""<span class="result-label">Statutory interest (estimate)</span>
  <div class="result-big gold" data-out="total">$0.00</div>
  <div class="result-sub" data-out="sub">Enter a deadline and an amount to begin.</div>
  <div class="result-rows">
    <div><span>Rate applied</span><b data-out="rate">&mdash;</b></div>
    <div><span>Amount paid late or still unpaid</span><b data-out="late">&mdash;</b></div>
    <div><span>Longest delay</span><b data-out="days">&mdash;</b></div>
    <div><span>Still accruing per day</span><b data-out="perday">&mdash;</b></div>
    <div class="total"><span>Claim + interest owed</span><b data-out="grand">&mdash;</b></div>
  </div>
  <div class="tbl-wrap"><table class="mini-table" data-out="table"><thead><tr><th>Period</th><th>Balance</th><th>Days</th><th>Interest</th></tr></thead><tbody></tbody></table></div>""")}
</div>'''


def build(ctx):
    mc = ctx["make_card"]
    out = []

    # 1. Main statutory interest calculator (existing URL) -------------------------
    content = f'''
<h2>How the Texas statutory interest calculator works</h2>
<p>Texas Insurance Code §542.060 makes an insurer that is liable for a claim, and that did not comply with the
prompt-payment subchapter, pay the policyholder interest on the amount of the claim &ldquo;as damages,&rdquo; together
with reasonable and necessary attorney&rsquo;s fees. This calculator does the interest part of that sentence:</p>
<blockquote><p>interest = late amount &times; annual rate &divide; 365 &times; days late</p><cite>Simple interest, accruing daily</cite></blockquote>
<p>It works on <strong>components</strong>. The original claim is one component; each supplement or separately
submitted item is another, because each one has its own payment deadline. For every component it starts on the date
payment was required, subtracts anything paid on or before that date, and then charges interest on the remaining
balance until each later payment reduces it. If a balance is still unpaid, it accrues through the date you choose.</p>
<h3>Choosing the rate</h3>
<ul>
<li><strong>18% a year</strong> &mdash; §542.060(a). Applies to non-weather claims (fire, smoke, plumbing leaks,
theft, vandalism) and to weather claims made before September 1, 2017.</li>
<li><strong>Floating rate</strong> &mdash; §542.060(c). In an action governed by Chapter 542A, the rate is the
Finance Code §304.003 judgment rate plus 5%. Chapter 542A covers claims for damage caused wholly or partly by forces
of nature, and the 2017 law that created it (HB 1774) applies the new rate to claims <em>made</em> on or after
September 1, 2017. The {RATE_MONTH} §304.003 rate is {JUDG_RATE_S}, so the floating rate is {FLOAT_RATE_S}.
Because §304.003 is floored at 5% and capped at 15%, the floating rate is always between 10% and 20%.</li>
</ul>
<div class="callout"><strong>Why the date the claim was made matters</strong><p>The old site and many online summaries
say the floating rate turns on the <em>date of loss</em>. The bill text says otherwise: Section 4(b) of HB 1774 applies
§542.060(c) &ldquo;only to a claim &hellip; made on or after&rdquo; September 1, 2017. For nearly every claim today the
answer is the same, but for a 2017 storm reported late it can change the rate.</p></div>
<h3>Finding the deadline</h3>
<p>The date payment was required depends on which part of Chapter 542 the insurer missed:</p>
<div class="table-scroll"><table><thead><tr><th>Provision</th><th>Deadline</th><th>Measured from</th></tr></thead><tbody>
<tr><td>§542.057(a)</td><td>5 business days (20 for surplus lines)</td><td>Notice that the insurer will pay all or part of the claim</td></tr>
<tr><td>§542.057(b)</td><td>5 business days</td><td>Performance of an act the payment was conditioned on</td></tr>
<tr><td>§542.058(a)</td><td>60 days (unless another statute sets a period)</td><td>Receipt of all items, statements and forms reasonably requested</td></tr>
<tr><td>§542.059(b)</td><td>+15 days to each claim-handling deadline</td><td>A weather catastrophe or major natural disaster declared by the commissioner</td></tr>
</tbody></table></div>
<p>If you aren&rsquo;t sure, use the <a href="/tools/claim-deadline-calculator/">claim deadline calculator</a> first,
then bring the result back here.</p>
<h3>What the calculator does not decide</h3>
<ul>
<li><strong>Whether the insurer is liable for the claim.</strong> §542.060 applies only if it is. If arbitration or
litigation finds a claim invalid, §542.058(a) does not apply (§542.058(b)).</li>
<li><strong>Whether a document request was reasonable.</strong> The 60-day clock runs from receipt of items the
insurer <em>reasonably</em> requested; whether a request qualified is a fact question.</li>
<li><strong>Attorney&rsquo;s fees and prejudgment interest.</strong> Both can be awarded in addition to §542.060
interest in a lawsuit; see the <a href="/texas-prejudgment-interest/">prejudgment interest calculator</a>.</li>
</ul>
<p>Payments are applied to the claim balance, not to accrued interest first. That is the conservative approach and
the one most demand letters use; a court could allocate differently.</p>'''
    faqs = [
        ("Is Texas prompt-payment interest simple or compound?",
         "<p>Simple. §542.060(c) says &ldquo;simple interest&rdquo; outright, and the 18% in §542.060(a) is likewise "
         "calculated as simple annual interest on the unpaid amount.</p>"),
        ("Do partial payments stop the interest?",
         "<p>No. A payment reduces the balance the interest runs on from the date it is made. Interest continues on "
         "whatever remains unpaid. The Texas Supreme Court made this point in <em>Hinojos v. State Farm Lloyds</em> (2021): "
         "a reasonable partial payment made on time does not shield the insurer from interest on amounts it owed but "
         "had not paid when the deadline expired.</p>"),
        ("Why does the calculator divide by 365?",
         "<p>An annual rate applied daily is conventionally divided by 365. In a leap year the difference is a fraction "
         "of a percent of the interest.</p>"),
        ("Can I use this for a commercial property claim?",
         "<p>Yes. Subchapter B of Chapter 542 applies to first-party claims under most insurance policies, residential "
         "or commercial. It does not apply to workers&rsquo; compensation, mortgage guaranty, title insurance, fidelity, "
         "surety or guaranty bonds, or marine insurance (§542.053).</p>"),
        ("Is the result a legal opinion?",
         "<p>No. It is an estimate from the dates and amounts you enter. Enforce Interest is a public adjusting service, "
         "not a law firm.</p>"),
    ]
    p = tool_page("/statutory-damages-calculator/",
                  "Texas Statutory Interest Calculator (§542.060) | Enforce Interest",
                  "Free Texas prompt-payment interest calculator. Compute §542.060 statutory damages at 18% or the "
                  f"{FLOAT_RATE_S} floating rate, with partial payments, supplements and a printable memo.",
                  "Statutory interest calculator", "Tex. Ins. Code §542.060 &middot; free calculator",
                  "Texas statutory interest <em>calculator</em>",
                  "Calculate the prompt-payment interest a Texas insurer owes on a late-paid claim &mdash; with partial "
                  "payments, supplements, the 18% or floating rate, and a memo you can print or share.",
                  ledger_tool(), content, faqs,
                  ["/tools/claim-deadline-calculator/", "/tools/appraisal-interest-calculator/", "/texas-judgment-interest-rate/"],
                  "Texas statutory interest calculator", "Free calculator &middot; §542.060",
                  aside=facts([("Standard rate", "18.00%"), ("Floating rate", f"{FLOAT_RATE_S}"),
                               ("Judgment rate", f"{JUDG_RATE_S} &middot; {RATE_MONTH[:3]} {lib.RATE_Y}"),
                               ("Formula", "simple, daily")]),
                  priority="0.9", schema_name="Texas Prompt Payment Interest Calculator")
    p["og"] = mc("tool-statutory-interest", "Free calculator · §542.060", "Texas statutory interest calculator")
    out.append(p)

    # 2. Claim deadline calculator ------------------------------------------------
    tool = f'''<div class="tool-shell" data-tool="deadlines">
<form class="tool-form" onsubmit="return false" novalidate>
  <div class="tool-panel">
    <h2><span class="n">I</span>Key dates</h2><p class="hint">Enter what you know. Leave a date blank and the steps that depend on it are estimated or skipped.</p>
    <div class="row2">{f_date("loss", "Date of loss")}{f_date("notice", "Date you gave written notice of the claim", "", True)}</div>
    <div class="row2">{f_date("items", "Date the insurer received the last requested item", "Starts the §542.056 and §542.058 clocks.")}{f_date("accept", "Date the insurer said it would pay", "Starts the §542.057 clock.")}</div>
    {f_date("extension", "Date the insurer said it needed more time (if any)", "§542.056(d): it must then decide within 45 days of that notice.")}
  </div>
  <div class="tool-panel">
    <h2><span class="n">II</span>Circumstances</h2>
    {chk("surplus", "The insurer is an eligible <strong>surplus lines</strong> insurer")}
    {chk("cat", "The loss is part of a <strong>declared weather catastrophe</strong> or major natural disaster (+15 days, §542.059(b))")}
    {chk("arson", "The insurer has a reasonable basis to suspect <strong>arson</strong> (30 days to decide)")}
    {chk("twia", "This is a <strong>TWIA</strong> windstorm policy (one-year claim filing deadline)")}
    {chk("weather", "The damage was caused by <strong>weather / forces of nature</strong> (Chapter 542A notice applies)", True)}
    {f_select("limit", "Suit limitation in your policy", [("2y1d", "2 years and 1 day from accrual (common)"), ("2y", "2 years (the shortest Texas allows)"), ("4y", "4 years (general contract statute)")], "Check the &ldquo;Suit Against Us&rdquo; condition in your policy. §16.070 voids anything shorter than two years.")}
  </div>
</form>
{results_shell('''<span class="result-label">Your Chapter 542 timeline</span>
  <div class="result-big" data-out="headline" style="font-size:1.7rem;font-family:var(--serif)">Enter your notice date</div>
  <div class="result-sub" data-out="sub">Business days skip weekends and Texas national and state holidays (Gov&rsquo;t Code §662.003).</div>
  <ol class="tl" data-out="tl"></ol>''')}
</div>'''
    content = f'''
<h2>Every deadline in the Texas prompt-payment statute</h2>
<p>Chapter 542, Subchapter B of the Texas Insurance Code sets a sequence of deadlines for first-party claims. Each is
measured from a specific event, and two of them count <strong>business days</strong> &mdash; days other than
Saturdays, Sundays and holidays recognized by Texas (§542.051(1)). This calculator applies those rules to your dates.</p>
<div class="table-scroll"><table><thead><tr><th>Step</th><th>Statute</th><th>Standard insurer</th><th>Surplus lines insurer</th></tr></thead><tbody>
<tr><td>Acknowledge, begin investigation, request items</td><td>§542.055(a)</td><td>15 days after notice</td><td>30 business days</td></tr>
<tr><td>Accept or reject in writing</td><td>§542.056(a)</td><td>15 business days after receiving all items</td><td>15 business days</td></tr>
<tr><td>Accept or reject &mdash; arson suspected</td><td>§542.056(b)</td><td>30 days after receiving items</td><td>30 days</td></tr>
<tr><td>Decide after notice that more time is needed</td><td>§542.056(d)</td><td>45 days after that notice</td><td>45 days</td></tr>
<tr><td>Pay after acceptance</td><td>§542.057</td><td>5 business days</td><td>20 business days</td></tr>
<tr><td>Pay in any event</td><td>§542.058(a)</td><td>60 days after receiving all items</td><td>60 days</td></tr>
<tr><td>Declared weather catastrophe</td><td>§542.059(b)</td><td colspan="2">Claim-handling deadlines extended 15 days</td></tr>
</tbody></table></div>
<h3>Beyond Chapter 542</h3>
<ul>
<li><strong>Chapter 542A pre-suit notice.</strong> For weather claims, written notice must be given at least 61 days
before suit is filed (§542A.003). The insurer can ask to inspect within 30 days of receiving it (§542A.004). Use the
<a href="/tools/542a-notice-calculator/">542A notice calculator</a> for detail.</li>
<li><strong>TWIA policies.</strong> A Texas Windstorm Insurance Association claim must be filed within one year of the
date of damage (§2210.573(a)); the commissioner can extend that up to 180 days for good cause (§2210.205(b)).</li>
<li><strong>Lawsuit limitations.</strong> Many policies require suit within two years and one day after the cause of
action accrues. Texas will not enforce a contractual limit shorter than two years (Civ. Prac. &amp; Rem. Code §16.070).
Claims under Insurance Code Chapter 541 have a two-year limit (§541.162). When accrual happens is a legal question
&mdash; the date shown here is measured from the date of loss as a cautious planning date only.</li>
</ul>
<div class="callout wine"><strong>Holidays</strong><p>The calculator skips the national holidays in Government Code
§662.003(a) and the state holidays in §662.003(b) (Confederate Heroes Day, Texas Independence Day, San Jacinto Day,
Emancipation Day, LBJ Day, the day after Thanksgiving, December 24 and 26). Optional holidays are counted as business
days. Holidays that fall on a weekend are not moved.</p></div>'''
    faqs = [
        ("Does the 60-day clock start when I file the claim?",
         "<p>Not usually. §542.058 measures 60 days from the date the insurer received all items, statements and forms "
         "it reasonably requested under §542.055. If the insurer never asked for anything, the claim notice itself may be "
         "the starting point &mdash; a fact-specific question.</p>"),
        ("What is a business day under the Texas Insurance Code?",
         "<p>A day other than a Saturday, Sunday or holiday recognized by Texas (§542.051(1)).</p>"),
        ("Do catastrophe extensions apply automatically?",
         "<p>Only when the Texas commissioner of insurance has declared a weather-related catastrophe or major natural "
         "disaster. Then the claim-handling deadlines in the subchapter are extended by 15 days (§542.059(b)).</p>"),
    ]
    p = tool_page("/tools/claim-deadline-calculator/",
                  "Texas Insurance Claim Deadline Calculator | Enforce Interest",
                  "Calculate every Texas Insurance Code Chapter 542 claim deadline from your notice date: 15-day "
                  "acknowledgment, 15 business days, 5 business days, 60 days, 542A notice and limitations.",
                  "Claim deadline calculator", "Chapter 542 &middot; business days &middot; Texas holidays",
                  "Texas claim <em>deadline</em> calculator",
                  "Turn your notice date into the full set of statutory deadlines &mdash; acknowledgment, acceptance, "
                  "payment, the 60-day backstop, 542A notice and suit limitations &mdash; and see which have passed.",
                  tool, content, faqs,
                  ["/statutory-damages-calculator/", "/tools/542a-notice-calculator/", "/tools/claim-timeline-builder/"],
                  "Texas insurance claim deadline calculator", "Free tool · Chapter 542 deadlines")
    p["og"] = mc("tool-claim-deadlines", "Free tool · Chapter 542 deadlines", "Texas insurance claim deadline calculator")
    out.append(p)

    # 3. Appraisal interest calculator ------------------------------------------
    ex = interest(176000, FLOAT_RATE, 423)
    tool = f'''<div class="tool-shell" data-tool="appraisal">
<form class="tool-form" onsubmit="return false" novalidate>
  <div class="tool-panel">
    <h2><span class="n">I</span>The award</h2>
    <div class="row2">{f_money("award", "Appraisal award (amount the policy owes before deductible)", "", "", "224000")}{f_money("deductible", "Deductible", "", "", "2500")}</div>
    {f_date("awardPaid", "Date the award was paid", "", True)}
  </div>
  <div class="tool-panel">
    <h2><span class="n">II</span>When payment was due</h2>
    {seg("mode", "Deadline", [("due", "I know the date", ""), ("items", "Items received + 60 days", "")])}
    <div data-show="due">{f_date("due", "Date payment was required", "Often the §542.058 date: 60 days after the insurer received the items it requested.")}</div>
    <div data-show="items" hidden>{f_date("items", "Date insurer received all requested items")}{chk("cat", "Declared weather catastrophe (+15 days)")}</div>
  </div>
  <div class="tool-panel">
    <h2><span class="n">III</span>What the carrier paid before the award</h2><p class="hint">Every check issued before the award was paid, with its date.</p>
    <div class="pay-list" data-pays></div>
    <button type="button" class="add-btn" data-add-pay>+ Add a payment</button>
  </div>
  <div class="tool-panel">
    <h2><span class="n">IV</span>Rate</h2>
    {seg("regime", "Claim type", [("float", "Weather claim", "made on/after 9/1/2017"), ("std", "18% claim", "non-weather or pre-2017")])}
    <div data-float-only>{rate_month_select()}</div>
    {f_money("paidInterest", "Interest the carrier already paid (if any)", "Since Rodriguez v. Safeco (2024), carriers often pay award + interest. Enter it to check for a shortfall.")}
  </div>
  <template id="tpl-pay"><div class="pay-row" data-pay>
    <div class="field"><label>Payment date</label><input type="date" data-p="date"></div>
    <div class="field"><label>Amount paid</label><div class="money"><input type="number" min="0" step="0.01" inputmode="decimal" data-p="amount"></div></div>
    <button type="button" class="icon-btn" data-remove-pay aria-label="Remove payment">&times;</button>
  </div></template>
</form>
{results_shell('''<span class="result-label">Interest on the underpaid amount</span>
  <div class="result-big gold" data-out="total">$0.00</div>
  <div class="result-sub" data-out="sub">Enter the award, the payments and the dates.</div>
  <div class="result-rows">
    <div><span>Owed under the award (after deductible)</span><b data-out="owed">&mdash;</b></div>
    <div><span>Paid by the deadline</span><b data-out="ontime">&mdash;</b></div>
    <div><span>Paid late (incl. award payment)</span><b data-out="late">&mdash;</b></div>
    <div><span>Rate</span><b data-out="rate">&mdash;</b></div>
    <div><span>Interest already paid</span><b data-out="paidInt">&mdash;</b></div>
    <div class="total"><span>Interest shortfall</span><b data-out="short">&mdash;</b></div>
  </div>
  <div class="tbl-wrap"><table class="mini-table" data-out="table"><thead><tr><th>Period</th><th>Balance</th><th>Days</th><th>Interest</th></tr></thead><tbody></tbody></table></div>''')}
</div>'''
    content = f'''
<h2>Why appraisal doesn&rsquo;t automatically end the interest</h2>
<p>Appraisal settles one thing: the <em>amount of loss</em>. It does not decide whether that amount was paid on time.
Three Texas Supreme Court decisions put that distinction into law:</p>
<ul>
<li><strong><em>Barbara Technologies Corp. v. State Farm Lloyds</em>, 589 S.W.3d 806 (Tex. 2019)</strong> &mdash; an
insurer&rsquo;s payment of an appraisal award is not an acknowledgment of liability and does not, by itself, bar a
claim for prompt-payment damages.</li>
<li><strong><em>Alvarez v. State Farm Lloyds</em>, 601 S.W.3d 781 (Tex. 2020)</strong> &mdash; applied the same rule.</li>
<li><strong><em>Hinojos v. State Farm Lloyds</em>, 619 S.W.3d 651 (Tex. 2021)</strong> &mdash; a reasonable payment made
within the statutory deadline does not protect the insurer from interest on the amounts it owed but had not paid when
the deadline expired.</li>
</ul>
<p>So the calculation is: what did the policy owe (the award, less the deductible), what had been paid by the
deadline, and how long did the rest take? Interest runs on the unpaid balance from the deadline until each later
payment &mdash; usually the award payment &mdash; brings it down.</p>
<h3>A worked example</h3>
<p>A weather claim is made in 2024. The carrier receives what it requested and its §542.058 deadline passes on
May 21, 2024. It has paid $48,000. Appraisal awards $226,500 and the deductible is $2,500, so the policy owed
$224,000. The carrier pays the remaining $176,000 on July 18, 2025 &mdash; 423 days late. At {FLOAT_RATE_S}, the
interest on $176,000 for 423 days is <strong>{money(ex)}</strong>. At 18% it would be {money(interest(176000, 18, 423))}.</p>
<h3>What changed in 2024: <em>Rodriguez v. Safeco</em></h3>
<p>In <em>Rodriguez v. Safeco Insurance Co. of Indiana</em> (Tex. Feb. 2, 2024), the Texas Supreme Court held that in a
Chapter 542A weather case, an insurer that pays the appraisal award <em>plus any statutory interest that could be
owed</em> leaves nothing to be &ldquo;awarded in the judgment&rdquo; on the claim, so the formula in §542A.007(a)(3)
allows no attorney&rsquo;s fees. Since then many carriers pay an interest figure along with the award. That makes the
calculation itself the issue: was the right deadline used? The right rate? Were the earlier partial payments credited
on the right dates? Enter what they paid in the &ldquo;interest already paid&rdquo; box to see whether it falls short.</p>
<div class="callout"><strong>Deductible and holdback</strong><p>Enter the award as the amount of loss under the
policy&rsquo;s valuation (replacement cost or actual cash value, as the award states). If the award separates
recoverable depreciation that only becomes payable after repairs, that portion may have a different due date &mdash;
model it as a separate component in the <a href="/statutory-damages-calculator/">main calculator</a>.</p></div>'''
    faqs = [
        ("Does Hinojos apply to weather claims under Chapter 542A?",
         "<p>Yes. The holding concerns §542.058 and §542.060, which apply to weather claims too; Chapter 542A changes the "
         "rate (to the floating §542.060(c) rate) and adds notice and attorney-fee rules.</p>"),
        ("The carrier paid the award with interest. Is there anything left?",
         "<p>Possibly not &mdash; but check the math. A different start date, the wrong rate, or partial payments credited "
         "too early can all understate the interest. If the payment fully covered every possible dollar of statutory "
         "interest, <em>Rodriguez</em> means attorney&rsquo;s fees under §542A.007 are unlikely in a weather case.</p>"),
        ("My appraisal was years ago. Is it too late?",
         "<p>Limitations depends on the policy&rsquo;s suit clause and when the claim for interest accrued; it is a legal "
         "question for an attorney. Contractual limits can&rsquo;t be shorter than two years in Texas (§16.070).</p>"),
    ]
    p = tool_page("/tools/appraisal-interest-calculator/",
                  "Appraisal Interest Calculator (Texas, Hinojos) | Enforce Interest",
                  "Calculate Texas prompt-payment interest on the gap between pre-appraisal payments and the appraisal "
                  "award, per Hinojos v. State Farm. Checks interest the carrier paid for shortfalls.",
                  "Appraisal interest calculator", "Hinojos v. State Farm Lloyds &middot; 619 S.W.3d 651",
                  "Appraisal <em>interest</em> calculator",
                  "The award was higher than what the carrier paid. Calculate the statutory interest on that gap &mdash; "
                  "and check whether the interest the carrier sent was enough.",
                  tool, content, faqs,
                  ["/statutory-damages-calculator/", "/tools/542a-notice-calculator/", "/texas-judgment-interest-rate/"],
                  "Appraisal interest calculator", "Free tool · post-appraisal interest")
    p["og"] = mc("tool-appraisal-interest", "Free tool · Hinojos interest", "Texas appraisal interest calculator")
    out.append(p)

    # 4. 542A notice calculator -------------------------------------------------
    tool = f'''<div class="tool-shell" data-tool="notice542a">
<form class="tool-form" onsubmit="return false" novalidate>
  <div class="tool-panel">
    <h2><span class="n">I</span>Notice dates</h2>
    {f_date("noticeDate", "Date the insurer received the pre-suit notice", "", True)}
    {f_date("suitDate", "Planned filing date (optional)", "We will check it is at least 61 days after notice.")}
  </div>
  <div class="tool-panel">
    <h2><span class="n">II</span>Fee ratio (§542A.007)</h2><p class="hint">Compares what the judgment awards on the claim with the amount demanded in the notice.</p>
    <div class="row2">{f_money("demand", "Amount alleged owed in the notice", "", "80000")}{f_money("judgment", "Amount awarded on the claim", "", "60000")}</div>
    {f_money("fees", "Reasonable &amp; necessary attorney&rsquo;s fees found", "", "30000")}
  </div>
</form>
{results_shell('''<span class="result-label">Chapter 542A dates</span>
  <div class="result-big" data-out="headline" style="font-size:1.7rem;font-family:var(--serif)">Enter the notice date</div>
  <ol class="tl" data-out="tl"></ol>
  <div class="result-rows">
    <div><span>Award &divide; notice demand</span><b data-out="ratio">&mdash;</b></div>
    <div><span>Fee rule that applies</span><b data-out="rule">&mdash;</b></div>
    <div class="total"><span>Fees recoverable (estimate)</span><b data-out="fee">&mdash;</b></div>
  </div>''')}
</div>'''
    content = '''
<h2>What Chapter 542A requires before a weather-claim lawsuit</h2>
<p>Chapter 542A was added to the Insurance Code in 2017 (HB 1774). It applies to lawsuits on first-party property
claims for damage caused wholly or partly by forces of nature &mdash; earthquake, wildfire, flood, tornado,
lightning, hurricane, hail, wind, snowstorm, rainstorm &mdash; filed on or after September 1, 2017. It does not apply
to suits against the Texas Windstorm Insurance Association, which has its own procedure in Chapter 2210.</p>
<h3>The notice (§542A.003)</h3>
<p>At least <strong>61 days</strong> before filing suit, the claimant must give the insurer written notice stating:</p>
<ol><li>the acts or omissions giving rise to the claim;</li>
<li>the specific amount alleged to be owed on the claim for damage to or loss of covered property; and</li>
<li>the reasonable and necessary attorney&rsquo;s fees incurred so far, calculated from contemporaneous time records.</li></ol>
<p>If an attorney or other representative gives the notice, they must send the claimant a copy and say so in the
notice. Notice isn&rsquo;t required if there&rsquo;s a reasonable basis to believe limitations will expire first, or if the
claim is a counterclaim.</p>
<h3>The insurer&rsquo;s inspection (§542A.004)</h3>
<p>Within 30 days after receiving the notice, the insurer may ask in writing to inspect, photograph or evaluate the
property. If reasonably possible, that must be done within 60 days after it received the notice.</p>
<h3>The fee formula (§542A.007)</h3>
<p>Recoverable attorney&rsquo;s fees are the least of: the fees proved at trial; fees available under other law; or the
fees multiplied by the ratio of the amount awarded on the claim to the amount demanded in the notice. If that ratio is
<strong>0.8 or more</strong>, the full fees are awarded (if otherwise recoverable). If it is <strong>below 0.2</strong>,
no fees. If the insurer proves it was entitled to notice and didn&rsquo;t get one at least 61 days before suit, no fees
incurred after it files that plea are recoverable.</p>
<div class="callout wine"><strong>Why the number in the notice matters</strong><p>Overstating the demand can shrink or
erase a fee award; understating it can cap the case. And after <em>Rodriguez v. Safeco</em> (Tex. 2024), an insurer that
pays an appraisal award plus all possible statutory interest can reduce the &ldquo;amount awarded&rdquo; to zero. This
tool illustrates the formula; drafting a 542A notice is a job for a Texas attorney.</p></div>'''
    p = tool_page("/tools/542a-notice-calculator/",
                  "542A Pre-Suit Notice & Attorney Fee Calculator | Enforce Interest",
                  "Texas Insurance Code Chapter 542A calculator: 61-day pre-suit notice dates, the 30-day inspection "
                  "request window and the §542A.007 attorney-fee ratio (0.2 and 0.8 thresholds).",
                  "542A notice calculator", "Tex. Ins. Code ch. 542A &middot; weather claims",
                  "542A notice &amp; <em>fee</em> calculator",
                  "For weather claims: when suit can be filed after pre-suit notice, the insurer&rsquo;s inspection window, "
                  "and how the notice amount drives the attorney-fee formula.",
                  tool, content, [],
                  ["/tools/claim-deadline-calculator/", "/tools/appraisal-interest-calculator/", "/statutory-damages-calculator/"],
                  "542A notice and attorney fee calculator", "Free tool · Chapter 542A")
    p["og"] = mc("tool-542a", "Free tool · Chapter 542A", "542A pre-suit notice and attorney fee calculator")
    out.append(p)

    # 5. Claim timeline builder -------------------------------------------------
    tool = '''<div class="tool-shell" data-tool="timeline">
<form class="tool-form" onsubmit="return false" novalidate>
  <div class="tool-panel">
    <h2><span class="n">I</span>Claim details</h2>
    <div class="row3"><div class="field"><label for="tl-ins">Your name</label><input id="tl-ins" data-meta="insured" type="text"></div>
    <div class="field"><label for="tl-car">Insurance company</label><input id="tl-car" data-meta="carrier" type="text"></div>
    <div class="field"><label for="tl-no">Claim number</label><input id="tl-no" data-meta="claimno" type="text"></div></div>
    <div class="row2"><div class="field"><label for="tl-loss">Date of loss</label><input id="tl-loss" data-meta="loss" type="date"></div>
    <div class="field"><label for="tl-addr">Property address</label><input id="tl-addr" data-meta="address" type="text"></div></div>
  </div>
  <div class="tool-panel">
    <h2><span class="n">II</span>Add an event</h2><p class="hint">Saved in this browser only (localStorage). Add events in any order; they are sorted by date.</p>
    <div class="row2"><div class="field"><label for="ev-type">What happened</label><select id="ev-type">
      <option value="notice">I reported the claim (notice)</option><option value="ack">Insurer acknowledged the claim</option>
      <option value="request">Insurer requested documents/information</option><option value="sent">I sent requested documents</option>
      <option value="inspect">Inspection took place</option><option value="extension">Insurer said it needs more time</option>
      <option value="accept">Insurer accepted (all or part)</option><option value="deny">Insurer denied (all or part)</option>
      <option value="payment">Payment received</option><option value="supplement">Supplement submitted</option>
      <option value="appraisal">Appraisal demanded</option><option value="award">Appraisal award issued</option>
      <option value="call">Phone call / email</option><option value="other">Other</option></select></div>
    <div class="field"><label for="ev-date">Date</label><input id="ev-date" type="date"></div></div>
    <div class="row2"><div class="field"><label for="ev-amt">Amount (if any)</label><div class="money"><input id="ev-amt" type="number" min="0" step="0.01"></div></div>
    <div class="field"><label for="ev-note">Note</label><input id="ev-note" type="text" placeholder="e.g. requested contractor estimate"></div></div>
    <div class="btn-row"><button type="button" class="btn btn-primary btn-sm" data-add-event>Add event</button><button type="button" class="add-btn" data-demo>Load an example</button><button type="button" class="add-btn" data-clear>Clear all</button></div>
  </div>
  <div class="tool-panel">
    <h2><span class="n">III</span>Status-request letter</h2><p class="hint">A plain, polite letter asking the carrier for a written status, the items it still needs and its payment date. Edit before sending.</p>
    <div class="field"><textarea data-letter rows="14" aria-label="Generated letter"></textarea></div>
    <div class="btn-row"><button type="button" class="add-btn" data-copy-letter>Copy letter</button></div>
  </div>
</form>
<aside class="results"><div class="result-card" aria-live="polite">
  <span class="result-label">Your claim timeline</span>
  <div class="result-big" data-out="headline" style="font-size:1.6rem;font-family:var(--serif)">No events yet</div>
  <div class="result-sub" data-out="sub">Add your first event, or load the example.</div>
  <ol class="tl" data-out="tl"></ol>
  <div class="result-actions no-print"><button type="button" data-act="print">Print timeline</button><button type="button" data-act="csv">Download CSV</button></div>
  <div class="result-note">Deadlines shown are estimates under Tex. Ins. Code §§542.055&ndash;.058 based on the events you log.</div>
</div></aside>
</div>'''
    content = '''
<h2>Why a claim diary is the most valuable document you&rsquo;ll keep</h2>
<p>Every deadline in Chapter 542 is triggered by an event: written notice, a request for information, the day the
insurer receives the last item it asked for, a notice of acceptance. If the dates of those events aren&rsquo;t written
down, the deadlines can&rsquo;t be proved &mdash; and the statutory interest that depends on them can&rsquo;t be calculated.</p>
<p>This builder keeps a dated log and reads it the way the statute does. Log the day you reported the claim and it
shows the §542.055 acknowledgment deadline. Log the day you sent the documents the adjuster requested and it shows the
§542.056 decision date and the §542.058 60-day payment date. Log payments and it flags which arrived after a deadline.</p>
<h3>What to record</h3>
<ul><li>Every written request from the insurer &mdash; what was asked for and the date you received the request.</li>
<li>Every response &mdash; what you sent, how (email, portal, certified mail) and the date it was received.</li>
<li>Inspections, re-inspections and engineer or contractor visits.</li>
<li>Every acceptance, partial denial and payment, with amounts.</li>
<li>Supplements and the documents supporting them.</li></ul>
<p>Keep copies. When you are ready, send the log to Enforce Interest with your documents for a
<a href="/contact/">free review</a>.</p>'''
    p = tool_page("/tools/claim-timeline-builder/",
                  "Insurance Claim Timeline Builder & Letter | Enforce Interest",
                  "Log your Texas insurance claim events, see the Chapter 542 deadlines they trigger, flag late payments "
                  "and generate a claim status-request letter. Free, private, in your browser.",
                  "Claim timeline builder", "Claim diary &middot; Chapter 542 deadlines",
                  "Claim <em>timeline</em> builder",
                  "Keep a dated log of your claim, see which statutory deadlines each event triggered, and print a "
                  "polite status-request letter for your carrier.",
                  tool, content, [],
                  ["/tools/claim-deadline-calculator/", "/statutory-damages-calculator/", "/does-my-claim-qualify/"],
                  "Claim timeline builder", "Free tool · claim diary")
    p["og"] = mc("tool-timeline", "Free tool · claim diary", "Insurance claim timeline builder and status letter")
    out.append(p)

    # 6. Public adjuster fee calculator -----------------------------------------
    tool = f'''<div class="tool-shell" data-tool="pafee">
<form class="tool-form" onsubmit="return false" novalidate>
  <div class="tool-panel">
    <h2><span class="n">I</span>The numbers</h2>
    {f_money("offer", "What the insurer had offered / paid before hiring a PA", "Optional. Used to compare outcomes.", "40000")}
    {f_money("settle", "Total settlement after the PA&rsquo;s work", "", "75000")}
    {f_num("pct", "Contingency fee", "Texas caps total PA compensation at 10% of the settlement on the claim.", "10", "0.5", "%")}
    {chk("feeOnTotal", "Fee is charged on the whole settlement (uncheck if only on new money above the prior offer)", True)}
  </div>
</form>
{results_shell('''<span class="result-label">What you net</span>
  <div class="result-big gold" data-out="net">$0.00</div>
  <div class="result-sub" data-out="sub">After the public adjuster&rsquo;s fee.</div>
  <div class="result-rows">
    <div><span>Public adjuster fee</span><b data-out="fee">&mdash;</b></div>
    <div><span>Effective fee on the settlement</span><b data-out="eff">&mdash;</b></div>
    <div><span>Gain over the prior offer, after fee</span><b data-out="gain">&mdash;</b></div>
    <div class="total"><span>Break-even settlement</span><b data-out="be">&mdash;</b></div>
  </div><div data-out="warn"></div>''', actions=False)}
</div>'''
    content = '''
<h2>How public adjuster fees work in Texas</h2>
<p>Public adjusters are licensed by the Texas Department of Insurance under Insurance Code Chapter 4102. Section
4102.104 lets a license holder be paid by the hour, by flat rate, by a percentage of what the insurer pays, or another
method &mdash; but <strong>the total commission may not exceed 10 percent of the amount of the insurance settlement on
the claim</strong>.</p>
<ul>
<li><strong>The 72-hour policy-limits exception.</strong> If, within 72 hours after the loss is reported, the insurer pays
or commits in writing to pay the policy limit under §862.053 (total loss of real property by fire), a percentage fee
isn&rsquo;t allowed; the adjuster is limited to reasonable compensation for time and expenses.</li>
<li><strong>You stay on the check.</strong> Every claim payment must name the insured as a payee and require the
insured&rsquo;s endorsement; a public adjuster may not endorse a check on your behalf (§4102.104(c)&ndash;(e)).</li>
<li><strong>No repair work.</strong> A public adjuster may not take part in repairing the property on a claim they adjust
or take money from contractors who get that work (§4102.158).</li>
</ul>
<p>Enforce Interest&rsquo;s fee is contingency-based and within the statutory cap; the review is free and there is no fee
if nothing is recovered. Ask any adjuster for the fee in writing before you sign.</p>'''
    p = tool_page("/tools/public-adjuster-fee-calculator/",
                  "Texas Public Adjuster Fee Calculator (10% Cap) | Enforce Interest",
                  "Calculate a Texas public adjuster fee under the 10% cap in Insurance Code §4102.104, what you net, "
                  "and the settlement you need to break even against the insurer's offer.",
                  "Public adjuster fee calculator", "Tex. Ins. Code §4102.104 &middot; 10% cap",
                  "Public adjuster <em>fee</em> calculator",
                  "See what a Texas public adjuster can charge, what you keep, and how much the settlement has to "
                  "improve for hiring one to make sense.",
                  tool, content, [],
                  ["/tools/depreciation-calculator/", "/tools/wind-hail-deductible-calculator/", "/statutory-damages-calculator/"],
                  "Texas public adjuster fee calculator", "Free tool · PA fees")
    p["og"] = mc("tool-pa-fee", "Free tool · §4102.104", "Texas public adjuster fee calculator")
    out.append(p)

    # 7. Depreciation calculator -----------------------------------------------
    presets = [("20", "3-tab asphalt shingles (~20 yrs)"), ("30", "Architectural shingles (~30 yrs)"),
               ("50", "Standing-seam metal roof (~50 yrs)"), ("40", "Clay / concrete tile (~40+ yrs)"),
               ("10", "Carpet (~10 yrs)"), ("25", "Hardwood / LVP flooring (~25 yrs)"), ("8", "Interior paint (~8 yrs)"),
               ("15", "HVAC system (~15 yrs)"), ("10", "Water heater (~10 yrs)"), ("25", "Cabinets (~25 yrs)"),
               ("30", "Wood fence (~15&ndash;30 yrs)"), ("custom", "Custom life expectancy")]
    tool = f'''<div class="tool-shell" data-tool="depr">
<form class="tool-form" onsubmit="return false" novalidate>
  <div class="tool-panel">
    <h2><span class="n">I</span>The item</h2>
    {f_select("preset", "Item", presets, "Typical useful lives used in estimates. Carriers&rsquo; tables vary; use the life in your estimate if you have it.", "30")}
    <div class="row2">{f_num("life", "Life expectancy (years)", "", "30", "1")}{f_num("age", "Age at time of loss (years)", "", "8", "0.5")}</div>
    <div class="row2">{f_money("rcv", "Replacement cost (RCV)", "", "24000")}{f_num("cap", "Maximum depreciation", "Some estimates cap depreciation (e.g. 80%).", "100", "1", "%")}</div>
  </div>
  <div class="tool-panel">
    <h2><span class="n">II</span>Policy</h2>
    {seg("policy", "How does your policy value this item?", [("rcv", "Replacement cost", "depreciation recoverable"), ("acv", "Actual cash value", "e.g. ACV roof endorsement")])}
    {f_money("ded", "Deductible applied to this claim", "", "2000")}
  </div>
</form>
{results_shell('''<span class="result-label">First check (ACV less deductible)</span>
  <div class="result-big gold" data-out="first">$0.00</div>
  <div class="result-sub" data-out="sub"></div>
  <div class="result-rows">
    <div><span>Depreciation</span><b data-out="dep">&mdash;</b></div>
    <div><span>Actual cash value</span><b data-out="acv">&mdash;</b></div>
    <div><span>Recoverable depreciation (after repair)</span><b data-out="rec">&mdash;</b></div>
    <div class="total"><span>Total policy benefit</span><b data-out="total">&mdash;</b></div>
  </div>''', actions=False)}
</div>'''
    content = '''
<h2>RCV, ACV and recoverable depreciation, explained</h2>
<p><strong>Replacement cost value (RCV)</strong> is what it costs today to repair or replace damaged property with
materials of like kind and quality. <strong>Actual cash value (ACV)</strong> is usually RCV minus depreciation for age
and wear. Most Texas replacement-cost homeowners policies pay ACV first and the withheld depreciation &mdash;
&ldquo;recoverable depreciation&rdquo; or the &ldquo;holdback&rdquo; &mdash; once the work is completed, within the time
the policy allows. Policies or endorsements that value roofs at ACV never pay that depreciation back.</p>
<h3>The straight-line method</h3>
<blockquote><p>depreciation = RCV &times; (age &divide; life expectancy), up to any cap</p></blockquote>
<p>Estimating software applies depreciation line by line, and carriers often depreciate labor as well as materials. If
your estimate depreciates items that don&rsquo;t wear out, uses a life expectancy far shorter than the material&rsquo;s
real life, or applies depreciation to code-upgrade items, those are worth questioning.</p>
<h3>Where interest comes in</h3>
<p>Recoverable depreciation becomes payable when the policy&rsquo;s conditions are met &mdash; usually proof the repairs
were done. If the carrier then sits on it, that is another payment with a deadline. Model it as its own component in
the <a href="/statutory-damages-calculator/">statutory interest calculator</a>.</p>'''
    p = tool_page("/tools/depreciation-calculator/",
                  "ACV vs RCV Depreciation Calculator | Enforce Interest",
                  "Calculate depreciation, actual cash value and recoverable depreciation on an insurance claim, with "
                  "typical life expectancies for roofs, flooring, HVAC and more. Free Texas claim tool.",
                  "Depreciation calculator", "Replacement cost &middot; actual cash value",
                  "ACV &amp; <em>depreciation</em> calculator",
                  "See how depreciation turns replacement cost into your first check, and how much should come back "
                  "once repairs are done.",
                  tool, content, [],
                  ["/tools/wind-hail-deductible-calculator/", "/tools/public-adjuster-fee-calculator/", "/statutory-damages-calculator/"],
                  "ACV and depreciation calculator", "Free tool · depreciation")
    p["og"] = mc("tool-depreciation", "Free tool · ACV & RCV", "ACV vs RCV depreciation calculator")
    out.append(p)

    # 8. Deductible calculator --------------------------------------------------
    tool = f'''<div class="tool-shell" data-tool="deduct">
<form class="tool-form" onsubmit="return false" novalidate>
  <div class="tool-panel">
    <h2><span class="n">I</span>Your policy</h2>
    {f_money("covA", "Dwelling coverage (Coverage A) limit", "On your declarations page.", "350000")}
    {seg("dtype", "Wind/hail or named-storm deductible", [("pct", "Percentage", "of Coverage A"), ("flat", "Flat dollar", "")])}
    <div data-show="pct">{f_select("pct", "Percentage", [("0.5", "0.5%"), ("1", "1%"), ("2", "2%"), ("3", "3%"), ("5", "5%"), ("10", "10%")], "", "2")}</div>
    <div data-show="flat" hidden>{f_money("flat", "Deductible amount", "", "2500")}</div>
  </div>
  <div class="tool-panel">
    <h2><span class="n">II</span>The loss</h2>
    {f_money("loss", "Estimated covered damage (before deductible)", "Use the replacement-cost total of your estimate.", "18000")}
    {f_money("dep", "Depreciation withheld (if any)", "Optional; affects the first check, not the total.", "0")}
  </div>
</form>
{results_shell('''<span class="result-label">Your deductible</span>
  <div class="result-big" data-out="ded">$0</div>
  <div class="result-sub" data-out="sub"></div>
  <div class="result-rows">
    <div><span>Covered damage</span><b data-out="loss">&mdash;</b></div>
    <div><span>First payment (after deductible and depreciation)</span><b data-out="first">&mdash;</b></div>
    <div class="total"><span>Total payable after deductible</span><b data-out="pay">&mdash;</b></div>
  </div><div data-out="warn"></div>''', actions=False)}
</div>'''
    content = '''
<h2>Percentage deductibles on Texas storm claims</h2>
<p>Many Texas homeowners policies use a separate deductible for wind and hail &mdash; and on the coast, for named
storms &mdash; written as a percentage of the dwelling (Coverage A) limit rather than a flat amount. A 2% deductible on a
home insured for $350,000 is $7,000, regardless of the size of the loss. That is why storm claims that look large can
pay surprisingly little, and why some small roof claims are not worth filing.</p>
<ul><li><strong>Check the declarations page.</strong> It lists the all-other-perils deductible and any separate wind/hail
or named-storm deductible.</li>
<li><strong>The deductible comes off once per occurrence</strong>, typically from the replacement-cost total.</li>
<li><strong>TWIA policies</strong> on the coast carry their own windstorm deductible options.</li>
<li><strong>Interest is calculated on the amount owed after the deductible.</strong> Use the result here as the
&ldquo;amount owed&rdquo; in the <a href="/statutory-damages-calculator/">statutory interest calculator</a>.</li></ul>'''
    p = tool_page("/tools/wind-hail-deductible-calculator/",
                  "Wind & Hail Deductible Calculator (Texas) | Enforce Interest",
                  "Convert a percentage wind/hail or named-storm deductible into dollars and see what a Texas storm claim "
                  "pays after the deductible and depreciation. Free calculator.",
                  "Wind &amp; hail deductible calculator", "Percentage deductibles &middot; storm claims",
                  "Wind &amp; hail <em>deductible</em> calculator",
                  "A 2% deductible isn&rsquo;t 2% of the damage. See your deductible in dollars and what your storm claim "
                  "actually pays.",
                  tool, content, [],
                  ["/tools/depreciation-calculator/", "/statutory-damages-calculator/", "/tools/public-adjuster-fee-calculator/"],
                  "Wind and hail deductible calculator", "Free tool · storm deductibles")
    p["og"] = mc("tool-deductible", "Free tool · storm deductibles", "Texas wind and hail deductible calculator")
    out.append(p)

    # 9. Judgment interest rate tracker (guide + lookup) -------------------------
    out.append(judgment_rate_page(mc))
    # 10. Prejudgment interest (guide + calculator) ------------------------------
    out.append(prejudgment_page(mc))
    # 11. Tools hub -------------------------------------------------------------
    out.append(hub(mc))
    return out


# ------------------------------------------------------------------ judgment rate
def rate_chart():
    pts = []
    for y in sorted(OCCC_RATES):
        if y < 2005:
            continue
        for m, v in enumerate(OCCC_RATES[y]):
            if v is not None:
                pts.append((y + m / 12, v))
    W, H, L, R, T, B = 760, 300, 44, 16, 16, 34
    x0, x1 = pts[0][0], pts[-1][0] + 1 / 12
    ymin, ymax = 0, 22

    def X(x):
        return L + (x - x0) / (x1 - x0) * (W - L - R)

    def Y(v):
        return T + (1 - (v - ymin) / (ymax - ymin)) * (H - T - B)
    grid = "".join(f'<line x1="{L}" x2="{W - R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/><text x="{L - 8}" y="{Y(v) + 4:.1f}" text-anchor="end">{v}%</text>' for v in (0, 5, 10, 15, 20))
    years = "".join(f'<text x="{X(y):.1f}" y="{H - 12}" text-anchor="middle">{y}</text>' for y in range(2006, int(x1) + 1, 4))
    l1 = " ".join(f"{X(x):.1f},{Y(v):.1f}" for x, v in pts)
    l2 = " ".join(f"{X(x):.1f},{Y(v + 5):.1f}" for x, v in pts if x >= 2017 + 8 / 12)
    area = f"M{X(pts[0][0]):.1f},{Y(0):.1f} L" + " L".join(f"{X(x):.1f},{Y(v):.1f}" for x, v in pts) + f" L{X(pts[-1][0]):.1f},{Y(0):.1f} Z"
    ann = f'<line x1="{X(2017 + 8 / 12):.1f}" x2="{X(2017 + 8 / 12):.1f}" y1="{T}" y2="{H - B}" stroke="#a07c2c" stroke-dasharray="3 3"/><text x="{X(2017 + 8 / 12) + 6:.1f}" y="{T + 12}" style="fill:#a07c2c">HB 1774 (9/1/2017)</text>'
    return (f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Texas postjudgment interest rate and §542.060(c) rate, 2005 to {lib.RATE_Y}">'
            f'<defs><linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6f1818" stop-opacity=".18"/><stop offset="1" stop-color="#6f1818" stop-opacity="0"/></linearGradient></defs>'
            f'<g class="grid">{grid}</g>{years}<path class="area" d="{area}"/><polyline class="l1" points="{l1}"/><polyline class="l2" points="{l2}"/>{ann}</svg>')


def rate_table():
    rows = []
    for y in sorted(OCCC_RATES, reverse=True):
        if y < 2005:
            continue
        cells = "".join(f'<td class="num">{v:.2f}</td>' if v is not None else "<td></td>" for v in OCCC_RATES[y])
        cells += "<td></td>" * (12 - len(OCCC_RATES[y]))
        rows.append(f"<tr><th>{y}</th>{cells}</tr>")
    head = "".join(f"<th>{m[:3]}</th>" for m in MONTHS)
    return f'<div class="table-scroll"><table><thead><tr><th>Year</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def judgment_rate_page(mc):
    path = "/texas-judgment-interest-rate/"
    trail = [("Home", "/"), ("Tools", "/tools/"), ("Texas judgment interest rate", path)]
    _, bc = breadcrumbs(trail)
    prev = OCCC_RATES[lib.RATE_Y][lib.RATE_M - 1] if lib.RATE_M else OCCC_RATES[lib.RATE_Y - 1][-1]
    faqs = [
        ("What is the Texas postjudgment interest rate right now?",
         f"<p>For judgments rendered in {RATE_MONTH} it is {JUDG_RATE_S}, as published by the Office of Consumer Credit "
         f"Commissioner. The previous month&rsquo;s rate was {prev:.2f}%.</p>"),
        ("How is the Texas judgment interest rate set?",
         "<p>On the 15th of each month the consumer credit commissioner sets the rate for judgments rendered the following "
         "month. It equals the prime rate published by the Federal Reserve Board on that date, but never less than 5% or "
         "more than 15% (Finance Code §304.003).</p>"),
        ("What is the floating interest rate on a Texas weather insurance claim?",
         f"<p>The §304.003 rate plus 5% (Insurance Code §542.060(c)). With the {RATE_MONTH} rate at {JUDG_RATE_S}, that is "
         f"{FLOAT_RATE_S}. In a lawsuit the rate is the one in effect on the date of judgment.</p>"),
        ("Is prejudgment interest the same rate?",
         "<p>In wrongful death, personal injury and property damage cases, the prejudgment rate equals the postjudgment rate "
         "applicable at the time of judgment (Finance Code §304.103). See our <a href=\"/texas-prejudgment-interest/\">prejudgment "
         "interest guide</a>.</p>"),
    ]
    fh, fl = faq_block(faqs)
    tool = f'''<div class="tool-shell" data-tool="ratelookup">
<form class="tool-form" onsubmit="return false" novalidate><div class="tool-panel">
  <h2><span class="n">I</span>Look up a month</h2><p class="hint">Rates apply to judgments rendered during the month.</p>
  <div class="row2">{f_select("y", "Year", [(str(y), str(y)) for y in sorted(OCCC_RATES, reverse=True) if y >= 1983], "", str(lib.RATE_Y))}
  {f_select("m", "Month", [(f"{i + 1:02d}", MONTHS[i]) for i in range(12)], "", f"{lib.RATE_M + 1:02d}")}</div>
  {f_money("amt", "Optional: judgment or claim amount", "Shows the daily interest at each rate.", "100000")}
</div></form>
{results_shell('''<span class="result-label">§304.003 postjudgment rate</span>
  <div class="result-big" data-out="rate">&mdash;</div>
  <div class="result-sub" data-out="sub"></div>
  <div class="result-rows">
    <div><span>§542.060(c) weather-claim rate</span><b data-out="float">&mdash;</b></div>
    <div><span>§542.060(a) standard rate</span><b>18.00%</b></div>
    <div><span>Daily interest at §304.003</span><b data-out="d1">&mdash;</b></div>
    <div><span>Daily interest at §542.060(c)</span><b data-out="d2">&mdash;</b></div>
    <div class="total"><span>Daily interest at 18%</span><b data-out="d3">&mdash;</b></div>
  </div>''', actions=False)}
</div>'''

    def body():
        return (page_hero(trail, f"OCCC &middot; Tex. Fin. Code §304.003 &middot; updated {RATE_MONTH}",
                          "Texas judgment interest rate: <em>" + JUDG_RATE_S + "</em>",
                          f"The Texas postjudgment interest rate for {RATE_MONTH} is {JUDG_RATE_S}. Add 5% and you have the "
                          f"§542.060(c) floating rate on weather insurance claims: {FLOAT_RATE_S}. Look up any month since 1983.",
                          aside=facts([("Postjudgment rate", JUDG_RATE_S), ("Weather-claim rate", FLOAT_RATE_S),
                                       ("Floor / ceiling", "5% / 15%"), ("Source", "OCCC")])) +
                f'<section class="section tight"><div class="wrap">{tool}</div></section>' +
                f'''<section class="section alt"><div class="wrap">
<div class="sec-head" data-reveal><span class="eyebrow">Rate history</span><h2>Texas §304.003 rate, 2005&ndash;{lib.RATE_Y}</h2>
<p class="lede">Solid line: postjudgment rate. Dashed: the §542.060(c) weather-claim rate it produces (from September 2017).</p></div>
<div data-reveal>{rate_chart()}<div class="legend"><span><i style="background:#6f1818"></i>§304.003 postjudgment rate</span><span><i style="background:#a07c2c"></i>§542.060(c) = §304.003 + 5%</span></div></div>
<div data-reveal style="margin-top:36px">{rate_table()}</div>
<p class="muted" style="font-size:.86rem">Source: Office of Consumer Credit Commissioner, Historical Table of Postjudgment Interest Rates
(rev. 9/17/2026) and Texas Credit Letter of 10/21/2026. Earlier years (1983&ndash;2004) are in the lookup above. Always confirm against
the <a href="https://occc.texas.gov/publications/interest-rates/" rel="noopener" target="_blank">OCCC&rsquo;s current publication</a>.</p>
</div></section>
<section class="section"><div class="wrap"><div class="prose" style="margin:0 auto">
<h2>How the Texas judgment rate works</h2>
<p>Finance Code §304.003 governs interest on Texas money judgments when the underlying contract doesn&rsquo;t set a rate.
On the 15th of each month the consumer credit commissioner determines the rate for judgments rendered in the following
calendar month: the prime rate published by the Federal Reserve Board on that day, with a floor of 5% and a ceiling of
15%. The rate in effect when a judgment is signed stays with that judgment.</p>
<p>From mid-2008 until late 2018, prime sat below 5%, so the Texas rate stayed pinned at the 5% floor. It edged up to
5.50% in 2018&ndash;2019, fell back to the floor from November 2019 to August 2022, then climbed with the Federal
Reserve&rsquo;s increases to 8.50% from September 2023. It eased to 7.00% by December 2025, held at 6.75% for most of
2026 and is {JUDG_RATE_S} for {RATE_MONTH}.</p>
<h2>Why insurance claims care about this number</h2>
<p>Since HB 1774 took effect on September 1, 2017, Insurance Code §542.060(c) sets prompt-payment interest on weather
claims at the §304.003 rate &ldquo;determined on the date of judgment&rdquo; plus five percent. Because §304.003 runs from
5% to 15%, the weather-claim rate runs from 10% to 20%. Non-weather claims (and weather claims made before September 1,
2017) still carry a flat 18% under §542.060(a).</p>
<p>Two practical consequences:</p>
<ul><li><strong>Before judgment the rate is an estimate.</strong> A demand letter or settlement uses the current month&rsquo;s
rate; a court uses the rate on the day it signs the judgment.</li>
<li><strong>The rate applies to the whole delay.</strong> It isn&rsquo;t a blend of monthly rates over the period of delay;
one rate applies to the whole accrual period.</li></ul>
<p>Prejudgment interest in property damage cases also uses the postjudgment rate at the time of judgment
(§304.103). For the accrual rules, see the <a href="/texas-prejudgment-interest/">Texas prejudgment interest guide</a>.</p>
</div></div></section>
<section class="section alt"><div class="wrap-narrow">{sec_head("FAQ", "Texas judgment interest rate questions", center=True)}<div data-reveal>{fh}</div></div></section>''' +
                related(["/statutory-damages-calculator/", "/texas-prejudgment-interest/", "/tools/appraisal-interest-calculator/"]) + cta_band())

    p = {"path": path, "title": f"Texas Judgment Interest Rate ({RATE_MONTH}: {JUDG_RATE_S}) | Enforce Interest",
         "desc": f"Texas postjudgment interest rate for {RATE_MONTH} is {JUDG_RATE_S} (OCCC, Fin. Code §304.003). See the full "
                 f"monthly history and the {FLOAT_RATE_S} §542.060(c) rate for weather insurance claims.",
         "body": body, "schema": [bc, fl, app_schema("Texas judgment interest rate lookup", path, "Monthly Texas §304.003 rates")],
         "is_tool": True, "guide": True, "h1_plain": f"Texas judgment interest rate: {JUDG_RATE_S}", "priority": "0.8",
         "freq": "monthly", "js": ["rates.js", "tools.js"]}
    p["og"] = mc("texas-judgment-interest-rate", f"OCCC · {RATE_MONTH}", f"Texas judgment interest rate: {JUDG_RATE_S}", motif="bars")
    return p


# ------------------------------------------------------------------ prejudgment
def prejudgment_page(mc):
    path = "/texas-prejudgment-interest/"
    trail = [("Home", "/"), ("Tools", "/tools/"), ("Texas prejudgment interest", path)]
    _, bc = breadcrumbs(trail)
    faqs = [
        ("When does prejudgment interest start in Texas?",
         "<p>In wrongful death, personal injury and property damage cases, on the earlier of the 180th day after the defendant "
         "receives written notice of the claim or the date suit is filed, ending the day before judgment (Finance Code §304.104).</p>"),
        ("What is the Texas prejudgment interest rate?",
         f"<p>The postjudgment rate applicable at the time of judgment (§304.103) &mdash; {JUDG_RATE_S} for judgments rendered "
         f"in {RATE_MONTH}. It is simple interest.</p>"),
        ("Can I get both §542.060 interest and prejudgment interest?",
         "<p>The statute expressly allows it: both §542.060(a) and (c) say nothing in them prevents an award of prejudgment "
         "interest &ldquo;as provided by law.&rdquo; How the two interact for the same period is argued case by case; insurers "
         "commonly object to a double recovery.</p>"),
        ("Does prejudgment interest apply to breach of an insurance contract?",
         "<p>Texas courts award prejudgment interest on contract damages under common law. In <em>Johnson &amp; Higgins of "
         "Texas, Inc. v. Kenneco Energy, Inc.</em>, 962 S.W.2d 507 (Tex. 1998), the Texas Supreme Court adopted the statutory "
         "accrual rules and rate for those cases too.</p>"),
    ]
    fh, fl = faq_block(faqs)
    tool = f'''<div class="tool-shell" data-tool="prejudgment">
<form class="tool-form" onsubmit="return false" novalidate><div class="tool-panel">
  <h2><span class="n">I</span>Dates &amp; amount</h2>
  {f_money("amt", "Amount of the judgment (damages subject to interest)", "", "75000")}
  <div class="row2">{f_date("notice", "Date the defendant received written notice of the claim")}{f_date("suit", "Date suit was filed")}</div>
  {f_date("judg", "Date of judgment (or estimated)", "Interest ends the day before.")}
  {rate_month_select("rateMonth", "Postjudgment rate to use")}
</div>
<div class="tool-panel"><h2><span class="n">II</span>Settlement offer (optional)</h2><p class="hint">§304.105: interest does not accrue on the amount of a rejected offer during the period it could have been accepted.</p>
  {f_money("offer", "Defendant&rsquo;s settlement offer")}
  <div class="row2">{f_date("offerFrom", "Offer made")}{f_date("offerTo", "Offer expired / rejected")}</div>
</div></form>
{results_shell('''<span class="result-label">Prejudgment interest (estimate)</span>
  <div class="result-big gold" data-out="total">$0.00</div>
  <div class="result-sub" data-out="sub"></div>
  <div class="result-rows">
    <div><span>Accrual starts</span><b data-out="start">&mdash;</b></div>
    <div><span>Accrual ends</span><b data-out="end">&mdash;</b></div>
    <div><span>Days</span><b data-out="days">&mdash;</b></div>
    <div><span>Rate</span><b data-out="rate">&mdash;</b></div>
    <div class="total"><span>Postjudgment interest per day</span><b data-out="post">&mdash;</b></div>
  </div>''', actions=False)}
</div>'''

    def body():
        return (page_hero(trail, "Tex. Fin. Code ch. 304 &middot; Subchapter B",
                          "Texas <em>prejudgment interest</em>: rules &amp; calculator",
                          "When prejudgment interest starts, what rate applies and how it sits alongside the 18% prompt-payment "
                          "interest on insurance claims &mdash; with a calculator for property damage cases.",
                          aside=facts([("Rate", f"{JUDG_RATE_S} ({RATE_MONTH[:3]} {lib.RATE_Y})"), ("Type", "simple"),
                                       ("Starts", "earlier of notice + 180 days or suit"), ("Ends", "day before judgment")])) +
                f'<section class="section tight"><div class="wrap">{tool}</div></section>' +
                f'''<section class="section alt"><div class="wrap"><div class="prose" style="margin:0 auto">
<h2>What prejudgment interest is</h2>
<p>Prejudgment interest compensates a plaintiff for the time between the injury (or notice of the claim) and the
judgment &mdash; the lost use of money that should have been paid earlier. In Texas it comes from two sources:</p>
<ul><li><strong>Statute.</strong> Finance Code §§304.101&ndash;.108 apply to wrongful death, personal injury and
<strong>property damage</strong> cases. A judgment in those cases earns prejudgment interest (§304.102).</li>
<li><strong>Common law.</strong> For other claims, such as breach of contract, Texas courts award prejudgment interest as
a matter of equity. In <em>Johnson &amp; Higgins v. Kenneco Energy</em> (Tex. 1998) the Texas Supreme Court held that
those awards should follow the statutory accrual rules and rate.</li></ul>
<h2>The statutory rules</h2>
<div class="table-scroll"><table><thead><tr><th>Rule</th><th>What it says</th><th>Source</th></tr></thead><tbody>
<tr><td>Rate</td><td>Equal to the postjudgment rate applicable at the time of judgment ({JUDG_RATE_S} in {RATE_MONTH})</td><td>§304.103</td></tr>
<tr><td>Start</td><td>Earlier of the 180th day after the defendant receives written notice of a claim, or the date suit is filed</td><td>§304.104</td></tr>
<tr><td>End</td><td>The day before judgment is rendered</td><td>§304.104</td></tr>
<tr><td>Method</td><td>Simple interest; does not compound</td><td>§304.104</td></tr>
<tr><td>Settlement offers</td><td>No accrual on a rejected offer&rsquo;s amount while the offer could have been accepted</td><td>§304.105</td></tr>
</tbody></table></div>
<h2>Prejudgment interest on insurance claims</h2>
<p>When a Texas insurer pays a claim late, the policyholder&rsquo;s main remedy is the §542.060 statutory interest
&mdash; 18% a year, or the floating rate for weather claims. That interest is labeled &ldquo;damages,&rdquo; and the
statute adds: &ldquo;Nothing in this subsection prevents the award of prejudgment interest on the amount of the claim,
as provided by law.&rdquo; So prejudgment interest is available in principle on top of §542.060 interest. In practice,
insurers argue that both should not be awarded on the same dollars for the same days, and courts have handled the overlap
in different ways. Keep both numbers separate when you present a claim.</p>
<div class="callout"><strong>Example</strong><p>A $75,000 property damage judgment is signed on {MONTHS[lib.RATE_M]} 15, {lib.RATE_Y}. The
defendant received written notice on March 1, 2025 and suit was filed on January 10, 2026. Day 180 after notice is
August 28, 2025, which is earlier than the filing date, so interest runs from then to the day before judgment, at the
{JUDG_RATE_S} rate in effect at judgment.</p></div>
<p>Postjudgment interest then runs on the whole judgment &mdash; including court costs and prejudgment interest &mdash;
at the same §304.003 rate until it is paid (§304.003(a)).</p>
</div></div></section>
<section class="section"><div class="wrap-narrow">{sec_head("FAQ", "Texas prejudgment interest questions", center=True)}<div data-reveal>{fh}</div></div></section>''' +
                related(["/texas-judgment-interest-rate/", "/statutory-damages-calculator/", "/tools/appraisal-interest-calculator/"]) + cta_band())

    p = {"path": path, "title": "Texas Prejudgment Interest: Rules & Calculator | Enforce Interest",
         "desc": f"How Texas prejudgment interest works (Fin. Code §§304.101–.108): 180-day accrual rule, {JUDG_RATE_S} rate, "
                 "settlement offers and how it combines with §542.060 insurance interest. Free calculator.",
         "body": body, "schema": [bc, fl, app_schema("Texas prejudgment interest calculator", path, "Fin. Code ch. 304 calculator")],
         "is_tool": True, "guide": True, "h1_plain": "Texas prejudgment interest: rules & calculator", "priority": "0.8",
         "js": ["rates.js", "tools.js"]}
    p["og"] = mc("texas-prejudgment-interest", "Tex. Fin. Code ch. 304", "Texas prejudgment interest: rules and calculator", motif="bars")
    return p


# ------------------------------------------------------------------ hub
def hub(mc):
    path = "/tools/"
    trail = [("Home", "/"), ("Tools", path)]
    _, bc = breadcrumbs(trail)

    def body():
        cards = "".join(f'<a class="card" href="{t["path"]}"><div class="ico">{icon(t["icon"])}</div><h3>{t["short"]}</h3><p>{t["blurb"]}</p><span class="more">Open tool</span></a>' for t in TOOL_LIST)
        return (page_hero(trail, "Free &middot; no sign-up &middot; runs in your browser", "Free Texas insurance claim <em>tools</em>",
                          "Calculators and checklists built on the Texas Insurance Code, the Finance Code and current OCCC rates. "
                          "Every tool cites its authority and nothing you type leaves your device.") +
                f'<section class="section"><div class="wrap"><h2 class="sr-only">All tools</h2><div class="grid g3" data-stagger>{cards}</div></div></section>' +
                '''<section class="section alt"><div class="wrap"><div class="prose" style="margin:0 auto">
<h2>Which tool should I start with?</h2>
<ul><li><strong>Not sure anything is owed?</strong> Start with <a href="/does-my-claim-qualify/">Does my claim qualify?</a></li>
<li><strong>Know your dates but not your deadlines?</strong> Use the <a href="/tools/claim-deadline-calculator/">claim deadline calculator</a>.</li>
<li><strong>Know the deadline and the payments?</strong> Go straight to the <a href="/statutory-damages-calculator/">statutory interest calculator</a>.</li>
<li><strong>Went through appraisal?</strong> Use the <a href="/tools/appraisal-interest-calculator/">appraisal interest calculator</a>.</li>
<li><strong>Claim still open?</strong> Keep a log in the <a href="/tools/claim-timeline-builder/">claim timeline builder</a>.</li></ul>
<p>The tools give estimates from the information you enter. They are not legal advice. For a review of your actual claim
file, <a href="/contact/">send it to Enforce Interest</a>.</p></div></div></section>''' + cta_band())

    p = {"path": path, "title": "Free Texas Insurance Claim Calculators & Tools | Enforce Interest",
         "desc": "Free Texas insurance claim tools: statutory interest calculator, Chapter 542 deadline calculator, appraisal "
                 "interest, judgment rates, prejudgment interest, 542A notice, PA fees and depreciation.",
         "body": body, "schema": [bc, {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "url": lib.SITE + t["path"], "name": t["short"].replace("&amp;", "&")}
             for i, t in enumerate(TOOL_LIST)]}],
         "h1_plain": "Free Texas insurance claim tools", "priority": "0.8"}
    p["og"] = mc("tools-hub", "Free · no sign-up", "Free Texas insurance claim calculators and tools")
    return p
