"""/tools/ hub and five interactive claim tools (logic in /assets/js/tools.js)."""

from components import (TOOLS, btn, callout, card, checklist, faq_html, faq_schema, grid, icon, section_head,
                        steps_html, url, ORG_ID)

TOOL = {s: (n, b, i) for s, n, b, i in TOOLS}


def money(name, label, value="", hint=""):
    h = f'<small class="muted">{hint}</small>' if hint else ""
    return (f'<label class="field"><span>{label}</span><div class="input-wrap"><span class="pre">$</span>'
            f'<input class="has-pre" type="number" inputmode="decimal" min="0" step="any" name="{name}" value="{value}"></div>{h}</label>')


def number(name, label, value="", post="", step="any", hint=""):
    h = f'<small class="muted">{hint}</small>' if hint else ""
    pc = f'<span class="post">{post}</span>' if post else ""
    cls = ' class="has-post"' if post else ""
    return (f'<label class="field"><span>{label}</span><div class="input-wrap"><input{cls} type="number" inputmode="decimal" '
            f'min="0" step="{step}" name="{name}" value="{value}">{pc}</div>{h}</label>')


def select(name, label, options, hint=""):
    h = f'<small class="muted">{hint}</small>' if hint else ""
    opts = "".join(f'<option value="{v}"{" selected" if sel else ""}>{t}</option>' for v, t, sel in options)
    return f'<label class="field"><span>{label}</span><select name="{name}">{opts}</select>{h}</label>'


def rows(*items):
    return '<div class="result-rows">' + "".join(f'<div><span>{a}</span><strong data-out="{b}">&mdash;</strong></div>' for a, b in items) + "</div>"


DISCLAIMER = callout("<p>These tools give rough, educational estimates only. They are not an appraisal, an estimate or advice about your policy. Your policy wording and the facts of your claim control. Nothing you type is sent to our servers.</p>", "info", "Planning estimates only")


TOOLS_DATA = {
    "claim-gap-calculator": dict(
        title="Insurance Claim Gap Calculator | Compare Two Estimates",
        desc="Free claim gap calculator: compare the insurance estimate with your contractor's and see the real gap after deductible and depreciation.",
        h1="Insurance Claim Gap Calculator",
        lead="Compare the carrier's estimate with your contractor's estimate and see how big the gap really is after deductible and depreciation.",
        ui=f'''<form class="tool-shell" data-tool="gap" onsubmit="return false">
  <div class="tool-inputs"><h2>Your estimates</h2>
    {money("carrier", "Insurance company estimate (RCV)", "18500", "Replacement cost value on the carrier's estimate")}
    {money("contractor", "Contractor / your estimate (RCV)", "31200")}
    {money("deductible", "Deductible", "2500")}
    {money("dep", "Depreciation withheld by carrier", "4200", "Shown as depreciation or holdback on the estimate")}
    {select("policy", "Policy settles at", [("rcv", "Replacement cost (depreciation recoverable)", True), ("acv", "Actual cash value only", False)])}
  </div>
  <div class="tool-out" aria-live="polite"><h2>Results</h2>
    <div><div class="result-label">Gap between estimates</div><div class="result-big" data-out="gap">&mdash;</div></div>
    <div class="bars"><div><label><span>Carrier</span><span data-out="carrierFmt"></span></label><div class="bar"><span data-bar="carrier"></span></div></div>
      <div><label><span>Contractor</span><span data-out="contractorFmt"></span></label><div class="bar"><span data-bar="contractor"></span></div></div></div>
    {rows(("Gap as % of carrier estimate", "gapPct"), ("Carrier's first payment (ACV less deductible)", "firstPay"), ("Recoverable depreciation (after repairs)", "recov"), ("Total from carrier estimate", "carrierNet"), ("Total if contractor scope were agreed", "contractorNet"))}
    <p class="result-note" data-out="advice"></p>
  </div>
</form>''',
        how=[("Enter both estimates", "Use the replacement cost value (RCV) totals from the carrier's estimate and from your contractor's estimate."),
             ("Add deductible and depreciation", "Copy the deductible and the depreciation the carrier withheld. Both appear on most estimate summaries."),
             ("Read the gap", "The calculator shows the dollar gap, the percentage gap and what you'd receive under each scope.")],
        body='''<h2>Why the size of the gap matters</h2>
<p>Appraisal costs money and time, so the gap has to be worth it. A $1,500 difference on a roof claim is often better handled with a supplement and supporting photos. A $15,000 difference with clear missing scope may justify appraisal. The calculator doesn't make that decision for you, but it frames it.</p>
<h2>RCV, ACV and recoverable depreciation</h2>
<p>Most homeowner policies pay the <strong>actual cash value</strong> first &mdash; replacement cost minus depreciation, minus the deductible &mdash; then release the withheld <strong>recoverable depreciation</strong> after repairs are completed. ACV-only policies never pay that depreciation back, which makes the gap more painful. See our <a href="/glossary/">glossary</a> for definitions.</p>''',
        faqs=[("What counts as a big gap?", "<p>There's no fixed threshold. Consider the dollar amount, how much of it is supported by clear evidence, and the cost of appraisal relative to the gap.</p>"),
              ("Does the calculator know my policy?", "<p>No. It uses only what you type. Check your declarations page for your deductible and loss settlement terms.</p>")],
    ),
    "depreciation-calculator": dict(
        title="Insurance Depreciation Calculator | Estimate ACV &amp; Holdback",
        desc="Free insurance depreciation calculator. Estimate actual cash value, depreciation and recoverable holdback for roofs, siding, flooring, HVAC and more.",
        h1="Depreciation &amp; Actual Cash Value Calculator",
        lead="See roughly how much depreciation an adjuster might apply to a damaged item, and what that means for actual cash value.",
        ui=f'''<form class="tool-shell" data-tool="dep" onsubmit="return false">
  <div class="tool-inputs"><h2>Item details</h2>
    {select("item", "Item type", [("20", "3-tab asphalt shingles (≈20 yr)", False), ("30", "Architectural shingles (≈30 yr)", True), ("50", "Metal roofing (≈50 yr)", False), ("30", "Vinyl siding (≈30 yr)", False), ("15", "HVAC system (≈15 yr)", False), ("12", "Water heater (≈12 yr)", False), ("10", "Carpet (≈10 yr)", False), ("25", "Laminate / LVP flooring (≈25 yr)", False), ("50", "Hardwood flooring (≈50 yr)", False), ("7", "Interior paint (≈7 yr)", False), ("custom", "Custom life expectancy", False)])}
    {number("life", "Life expectancy", "30", "yrs", "1")}
    {money("rcv", "Replacement cost of the item", "14000")}
    {number("age", "Age of the item", "8", "yrs", "0.5")}
    {select("cond", "Condition before the loss", [("0.85", "Excellent (less wear)", False), ("1", "Average", True), ("1.15", "Below average (more wear)", False)])}
    {number("cap", "Maximum depreciation", "80", "%", "1", "Many estimates cap depreciation well below 100%")}
  </div>
  <div class="tool-out" aria-live="polite"><h2>Results</h2>
    <div><div class="result-label">Estimated actual cash value</div><div class="result-big" data-out="acv">&mdash;</div></div>
    <div class="bars"><div><label><span>Depreciated</span><span data-out="pct"></span></label><div class="bar"><span data-bar="dep"></span></div></div></div>
    {rows(("Replacement cost (RCV)", "rcvFmt"), ("Estimated depreciation", "depAmt"), ("Remaining useful life", "remain"))}
    <p class="result-note">If your policy pays replacement cost, the depreciation shown is usually recoverable once the repair is completed and documented. ACV-only policies don't return it.</p>
  </div>
</form>''',
        how=[("Pick the item", "Choose a common building component or enter a custom life expectancy."),
             ("Enter cost and age", "Use the replacement cost from your estimate and the item's age at the date of loss."),
             ("Adjust for condition", "Better-than-average upkeep generally means less depreciation; neglect means more.")],
        body='''<h2>How adjusters calculate depreciation</h2>
<p>Most estimates use straight-line depreciation: age divided by expected life, times replacement cost, often with a maximum cap and a condition adjustment. Life expectancies vary by carrier and software settings, and some carriers depreciate labor as well as materials &mdash; a practice whose treatment varies by state and policy language.</p>
<h2>Where depreciation disputes come from</h2>
<ul><li>A life expectancy that's too short for the material (for example, treating architectural shingles as 20-year shingles)</li>
<li>Age taken from a guess instead of permits, receipts or the home's records</li>
<li>Depreciation applied to items that aren't subject to wear, or labor depreciated where the policy doesn't support it</li></ul>
<p>Depreciation is part of the amount of loss, so it can be addressed in appraisal.</p>''',
        faqs=[("Is depreciation always recoverable?", "<p>Only under a replacement cost policy, and usually only after repairs are completed within the time the policy allows.</p>"),
              ("Can labor be depreciated in Alabama?", "<p>Practices vary and the answer can turn on policy language. If labor depreciation is significant on your claim, ask an attorney or an appraiser to review it.</p>")],
    ),
    "roof-square-calculator": dict(
        title="Roof Square Calculator | Roof Area, Pitch &amp; Waste Factor",
        desc="Free roof square calculator: turn footprint and pitch into roof area, squares, waste factor and bundles to check your insurance estimate.",
        h1="Roof Square Calculator",
        lead="Turn a building footprint and roof pitch into roof area, squares and bundles &mdash; then compare it with the roof measurements on your estimate.",
        ui=f'''<form class="tool-shell" data-tool="roof" onsubmit="return false">
  <div class="tool-inputs"><h2>Your roof</h2>
    {number("len", "Building length", "60", "ft")}
    {number("wid", "Building width", "36", "ft")}
    {number("over", "Eave &amp; rake overhang", "12", "in", "1")}
    {select("pitch", "Roof pitch (rise per 12 in.)", [(str(x), f"{x}/12" + (" (low slope)" if x <= 3 else " (common)" if x in (6, 7) else " (steep)" if x >= 8 else ""), x == 6) for x in range(2, 13)])}
    <fieldset class="field" style="border:0;padding:0;margin:0"><span>Roof style</span><div class="seg">
      <label><input type="radio" name="style" value="10" checked><span>Simple gable</span></label>
      <label><input type="radio" name="style" value="14"><span>Hip roof</span></label>
      <label><input type="radio" name="style" value="18"><span>Complex / cut-up</span></label></div></fieldset>
    {number("stories", "Stories", "1", "", "1")}
  </div>
  <div class="tool-out" aria-live="polite"><h2>Results</h2>
    <div><div class="result-label">Squares to order (with waste)</div><div class="result-big" data-out="sqWaste">&mdash;</div></div>
    {rows(("Footprint incl. overhang", "foot"), ("Pitch multiplier", "mult"), ("Roof surface area", "area"), ("Roof squares (no waste)", "sq"), ("Suggested waste factor", "waste"), ("Shingle bundles (3 per square)", "bundles"))}
    <p class="result-note" data-out="steep"></p>
  </div>
</form>''',
        how=[("Measure the footprint", "Use the outside length and width of the house, or of each roof section separately for L-shaped homes."),
             ("Choose the pitch", "Pitch is the rise in inches per 12 inches of run. Most Alabama homes fall between 5/12 and 8/12."),
             ("Compare with your estimate", "Look for the roof squares and waste on the carrier's estimate and compare.")],
        body='''<h2>What is a roofing square?</h2>
<p>One square is 100 square feet of roof surface. Shingles are sold in bundles, usually three per square. Insurance estimates list roof area in squares and add a waste percentage for cutting at hips, valleys and rakes.</p>
<h2>Why waste factor matters</h2>
<p>A simple gable roof might need about 10% waste. Hip roofs and cut-up roofs with dormers and valleys often need 14&ndash;20% or more. An estimate that uses 10% waste on a complex roof leaves material out. Waste is one of the most common roof-estimate disputes we see.</p>
<h2>Steep and high charges</h2>
<p>Roofs steeper than about 7/12 typically carry steep-slope labor charges, and two-story roofs often carry high-roof charges. Check that your estimate includes them where they apply.</p>''',
        faqs=[("How accurate is this?", "<p>It's a quick check for simple roofs. Complex roofs should be measured on site or with aerial measurement reports, which is what appraisers use.</p>"),
              ("What if my house is L-shaped?", "<p>Calculate each rectangle separately and add the squares together.</p>")],
    ),
    "hurricane-deductible-calculator": dict(
        title="Hurricane Deductible Calculator Alabama | Wind &amp; Named Storm",
        desc="Free hurricane deductible calculator for Alabama homeowners: turn a percentage wind deductible into dollars and see what a claim may pay.",
        h1="Hurricane &amp; Wind Deductible Calculator",
        lead="Percentage deductibles are figured on your dwelling limit, not on the damage. See yours in dollars before the next storm.",
        ui=f'''<form class="tool-shell" data-tool="hurr" onsubmit="return false">
  <div class="tool-inputs"><h2>Your policy</h2>
    {money("covA", "Dwelling coverage (Coverage A)", "350000", "From your declarations page")}
    <fieldset class="field" style="border:0;padding:0;margin:0"><span>Hurricane / named-storm deductible</span><div class="seg">
      <label><input type="radio" name="pct" value="1"><span>1%</span></label>
      <label><input type="radio" name="pct" value="2" checked><span>2%</span></label>
      <label><input type="radio" name="pct" value="5"><span>5%</span></label>
      <label><input type="radio" name="pct" value="10"><span>10%</span></label></div></fieldset>
    {number("custom", "Or enter a custom percentage", "", "%", "0.5")}
    {money("aop", "All-other-perils deductible (for comparison)", "1000")}
    {money("loss", "Estimated storm damage", "24000")}
  </div>
  <div class="tool-out" aria-live="polite"><h2>Results</h2>
    <div><div class="result-label">Your hurricane deductible</div><div class="result-big" data-out="ded">&mdash;</div></div>
    {rows(("Deductible percentage", "pctFmt"), ("Estimated claim payment (before depreciation)", "pay"), ("Same loss with your AOP deductible", "payAop"), ("Extra out-of-pocket from % deductible", "extra"))}
    <p class="result-note" data-out="note"></p>
  </div>
</form>''',
        how=[("Find Coverage A", "Your dwelling limit is on the declarations page, usually listed as Coverage A."),
             ("Pick the percentage", "Look for a hurricane, named-storm or windstorm deductible stated as a percentage."),
             ("Add a damage estimate", "See what portion of a loss would be paid after the deductible.")],
        body='''<h2>How percentage deductibles work in Alabama</h2>
<p>Many Alabama homeowner policies, especially in Mobile and Baldwin counties, carry a separate hurricane or named-storm deductible stated as a percentage of Coverage A. On a $350,000 dwelling limit, a 2% deductible is $7,000 &mdash; even if the damage is only $9,000. Some policies apply a percentage deductible to all wind and hail losses.</p>
<p>When the deductible applies depends on how the policy defines the triggering event &mdash; for example, a storm named by the National Hurricane Center, or a hurricane watch or warning issued for any part of Alabama. Read your policy's definition carefully.</p>
<h2>Ways Alabama homeowners lower wind risk</h2>
<p>Alabama law requires insurers to offer premium discounts for homes built or retrofitted to IBHS FORTIFIED standards, and the state's Strengthen Alabama Homes program has offered grants toward FORTIFIED roofs. Ask your agent how a FORTIFIED roof would affect your premium and deductible options.</p>''',
        faqs=[("Does the deductible apply per storm or per year?", "<p>Policies differ. Some apply the hurricane deductible per event, others once per hurricane season. Check your policy.</p>"),
              ("Does appraisal change my deductible?", "<p>No. Appraisal sets the amount of loss; the deductible is then applied under the policy.</p>")],
    ),
    "appraisal-readiness-checklist": dict(
        title="Insurance Appraisal Checklist for Alabama Claims",
        desc="Free interactive checklist of the policy documents, estimates, photos and records to gather before invoking appraisal on an Alabama claim.",
        h1="Appraisal Readiness Checklist",
        lead="Check off each document as you gather it. Your progress saves in this browser, and you can print the list for your file.",
        ui="CHECKLIST",
        how=[("Work through each group", "Start with the policy, then the estimates, then photos and records."),
             ("Check items as you go", "Progress saves automatically in this browser only."),
             ("Print or share", "Print the list and bring it to your consultation.")],
        body='''<h2>Why preparation matters</h2>
<p>An appraiser can only argue what the record supports. Claims with organized policies, estimates, photos and correspondence move faster and resolve better. Missing records slow everything down and leave gaps the other side will use.</p>''',
        faqs=[("Do I need everything on the list?", "<p>No. Gather what you have. The essentials are the full policy, the carrier's estimate and your photos.</p>"),
              ("Is my checklist stored on your server?", "<p>No. Progress is saved only in your browser's local storage.</p>")],
    ),
}

CHECK_GROUPS = [
    ("Policy documents", [
        ("Full certified policy", "Request a certified copy from your carrier or agent, including all endorsements."),
        ("Declarations page", "Coverage limits, deductibles (including hurricane / wind), loss settlement."),
        ("Appraisal provision located", "Note the demand method, deadlines and umpire procedure."),
        ("Notice and time-limit dates", "Date of loss, date reported, and any suit-limitation period."),
    ]),
    ("Estimates & payments", [
        ("Carrier's estimate(s)", "Every version, including supplements and revised estimates."),
        ("Contractor estimate(s)", "Detailed line items, not just a total."),
        ("Payment letters & checks", "What has been paid, what was withheld as depreciation."),
        ("Denial or partial-denial letters", "Any reason given for items not paid."),
    ]),
    ("Photos & documentation", [
        ("Photos and video right after the loss", "Wide shots and close-ups of every damaged area."),
        ("Before-loss photos", "Real estate listings, old photos, Google Street View captures."),
        ("Weather data", "Storm date, hail size or wind reports for your address."),
        ("Damaged samples kept", "Shingles, flooring or materials removed during mitigation."),
    ]),
    ("Reports & records", [
        ("Adjuster and engineer reports", "Request copies of every inspection report."),
        ("Mitigation invoices & drying logs", "Water-extraction and dry-out records."),
        ("Receipts for emergency repairs", "Tarps, board-up, temporary repairs, hotel stays."),
        ("Correspondence log", "Emails, letters and a log of phone calls with dates and names."),
    ]),
]


def checklist_ui():
    groups = []
    n = 0
    for g, items in CHECK_GROUPS:
        lis = []
        for t, h in items:
            n += 1
            lis.append(f'<label class="check-item"><input type="checkbox" data-check="c{n}"><span>{t}<small>{h}</small></span></label>')
        groups.append(f'<div class="check-group reveal"><h3>{g} <small data-group-count></small></h3>{"".join(lis)}</div>')
    return (f'<div data-tool="checklist"><div class="check-progress"><div class="ring" data-ring><b data-out="pct">0%</b></div>'
            f'<div><strong data-out="done">0 of {n} gathered</strong><br><small style="color:#b6cbd6">Saved in this browser</small></div>'
            f'<button type="button" class="btn btn-light" data-print>{icon("print", "ico ico-sm")}<span>Print</span></button>'
            f'<button type="button" class="btn btn-ghost-light" data-reset><span>Reset</span></button></div>'
            + "".join(groups) + "</div>")


def tool_page(slug):
    d = TOOLS_DATA[slug]
    name, blurb, ico = TOOL[slug]
    path = f"/tools/{slug}/"
    p = {
        "path": path, "title": d["title"], "description": d["desc"], "h1": d["h1"], "lead": d["lead"],
        "kicker": "Free claim tool", "hero_img": "inspect", "nav_active": "/tools/", "layout": "wide",
        "crumbs": [("Home", "/"), ("Tools", "/tools/"), (name, path)], "scripts": ["/assets/js/tools.js"],
        "hero_actions": "", "priority": "0.7",
    }
    ui = checklist_ui() if d["ui"] == "CHECKLIST" else d["ui"]
    others = [card(n, b, f"/tools/{s}/", i, link_label="Open tool") for s, n, b, i in TOOLS if s != slug]
    p["body"] = f'''
<section class="section section-white" style="padding-top:60px"><div class="container" style="max-width:1080px">
  {ui}
  {DISCLAIMER}
</div></section>
<section class="section section-aqua"><div class="container split" style="align-items:start">
  <div class="reveal">{section_head("How to use it", f"Using the {name}")}{steps_html(d["how"])}</div>
  <div class="prose reveal">{d["body"]}</div>
</div></section>
<section class="section section-white"><div class="container" style="max-width:900px">
  {section_head("Questions", "Frequently asked questions", "", True)}{faq_html(d["faqs"])}
</div></section>
<section class="section section-sand"><div class="container">
  {section_head("More free tools", "Keep going", "", True)}{grid(others, 4)}
</div></section>'''
    p["schema"] = [{
        "@type": "WebApplication", "@id": url(path) + "#app", "name": name, "url": url(path),
        "description": d["desc"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any (web browser)",
        "browserRequirements": "Requires JavaScript", "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": ORG_ID},
    }, faq_schema(p, d["faqs"]), {
        "@type": "HowTo", "@id": url(path) + "#howto", "name": f"How to use the {name}",
        "step": [{"@type": "HowToStep", "position": n, "name": t, "text": b} for n, (t, b) in enumerate(d["how"], 1)],
    }]
    return p


def hub():
    p = {
        "path": "/tools/",
        "title": "Free Insurance Claim Tools &amp; Calculators | Alabama",
        "description": "Free claim calculators for Alabama property owners: claim gap, depreciation, roof squares, hurricane deductible and an appraisal checklist.",
        "h1": "Free Insurance Claim Tools &amp; Calculators",
        "lead": "Practical calculators and checklists for policyholders who want to understand their numbers before talking to anyone.",
        "kicker": "Free tools", "hero_img": "inspect", "nav_active": "/tools/", "layout": "wide",
        "crumbs": [("Home", "/"), ("Tools", "/tools/")], "hero_actions": "", "priority": "0.8",
        "schema_type": "CollectionPage",
    }
    cards = [card(n, b, f"/tools/{s}/", i, link_label="Open tool") for s, n, b, i in TOOLS]
    p["body"] = f'''
<section class="section section-white"><div class="container">
  {section_head("Calculators &amp; checklists", "Pick a tool", "Everything runs in your browser. Nothing you enter is sent to us or stored on our servers.", True)}
  {grid(cards[:3], 3)}<div style="height:24px"></div>{grid(cards[3:], 2)}
  <div style="max-width:880px;margin:40px auto 0">{DISCLAIMER}</div>
</div></section>'''
    p["schema"] = [{"@type": "ItemList", "@id": url("/tools/#list"), "name": "Free insurance claim tools",
                    "itemListElement": [{"@type": "ListItem", "position": n, "url": url(f"/tools/{s}/"), "name": nm}
                                        for n, (s, nm, _, _) in enumerate(TOOLS, 1)]}]
    return p


def pages():
    return [hub()] + [tool_page(s) for s, _, _, _ in TOOLS]
