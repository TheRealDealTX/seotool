"""Page builders. build_all(ctx) writes every page through ctx['write']."""
import html
import json

from content import tool_pages

KW = "The Colony Public Adjuster"

HOME_FAQS = [
    ("What does The Colony Public Adjuster do?",
     "The Colony Public Adjuster represents policyholders, not insurance companies. We inspect and document property damage, review your policy and the carrier's estimate, prepare a supported claim and communicate with the insurer on your behalf within a written agreement."),
    ("How is a public adjuster different from the insurance company's adjuster?",
     "The insurance company's adjuster is hired by the carrier. A licensed public adjuster is hired by you, the property owner, and works only for your side of the claim."),
    ("Is the first claim review really free?",
     "Yes. The initial conversation and claim review are free with no obligation. If representation makes sense, the fee arrangement is explained in a written agreement before any work begins."),
    ("Can you help if my claim was already denied or underpaid?",
     "Often, yes. We review the decision letter, policy, estimates and evidence to see whether a supplement or request for reconsideration is supported. No particular outcome is guaranteed."),
    ("What areas do you serve?",
     "The Colony Public Adjuster serves The Colony, Texas and nearby Denton and Collin County communities including Frisco, Little Elm, Lewisville, Plano, Carrollton and Hebron."),
]

GUIDE = {
    "damage": {
        "wind": {"label": "Wind or hail", "url": "/services/wind-hail/", "cta": "Wind & hail claim help",
                 "items": ["Ground-level photos of every elevation, plus gutters, screens and AC fins", "The storm date and when you first noticed each issue"],
                 "safety": "Do not climb a damaged roof. Leave roof access to trained professionals."},
        "water": {"label": "Water damage", "url": "/services/water-damage/", "cta": "Water damage claim help",
                  "items": ["The plumber's written findings about the source", "Mitigation invoices, moisture readings and drying logs"],
                  "safety": "Shut off water and power to affected areas if it is safe, and start drying promptly."},
        "fire": {"label": "Fire or smoke", "url": "/services/fire-smoke/", "cta": "Fire & smoke claim help",
                 "items": ["A room-by-room contents list started from memory", "Receipts for temporary housing, meals and emergency purchases"],
                 "safety": "Wait for clearance from the fire department before entering the property."},
        "home": {"label": "Other home damage", "url": "/services/residential/", "cta": "Residential claim help",
                 "items": ["Room-by-room photos with a short note for each", "Your declarations page and any endorsements"],
                 "safety": "Address immediate hazards first and keep receipts for any temporary repairs."},
        "commercial": {"label": "Commercial property", "url": "/services/commercial/", "cta": "Commercial claim help",
                       "items": ["One contact each for the property, finances and repairs", "Inventory, equipment and business income records"],
                       "safety": "Secure the premises and preserve damaged inventory until it has been documented."},
    },
    "stage": {
        "preparing": {"label": "Preparing to file", "title": "Getting ready to report {d}",
                      "text": "Report the loss promptly as your policy requires, then start a dated record of what you observed. You do not need every answer before you call your insurer.",
                      "items": ["Your policy number and insurer claim line", "A simple timeline started in our claim diary"],
                      "url": "/tools/claim-checklist/", "cta": "Open the claim checklist"},
        "review": {"label": "Under review", "title": "Your {d} claim is being reviewed",
                   "text": "Keep the file organized while the insurer investigates. Texas law sets response deadlines once the insurer has the items it requested.",
                   "items": ["A list of every item the insurer has requested", "Dates you sent each document, and how"],
                   "url": "/tools/texas-claim-deadlines/", "cta": "Check Texas claim deadlines"},
        "offer": {"label": "Estimate or offer received", "title": "You have an estimate for {d}",
                  "text": "Separate the repair scope from the payment math. Compare the areas, quantities and line items before you focus on the total.",
                  "items": ["Every version of the carrier estimate", "Your contractor's scope for side-by-side comparison"],
                  "url": "/tools/claim-payment-calculator/", "cta": "Try the payment calculator"},
        "denied": {"label": "Denied or underpaid", "title": "Your {d} claim was denied or underpaid",
                   "text": "Get the full decision in writing and identify each reason given. Coverage questions and pricing disagreements need different evidence.",
                   "items": ["The complete decision letter and cited policy language", "An issue-by-issue list with supporting photos"],
                   "url": "/blog/denied-underpaid-claim-review/", "cta": "Read the denied claim guide"},
    },
}

GLOSSARY = [
    ("Scope of loss", "The work an estimate describes: locations, materials, quantities and repair steps. Comparing scopes explains why two estimates can have different totals."),
    ("ACV vs. RCV", "Actual cash value subtracts depreciation. Replacement cost value is the cost to repair or replace new. Many policies pay ACV first and the rest after repairs."),
    ("Supplement", "Additional damage or costs submitted after the first estimate, with documentation showing what is new and why it is needed."),
    ("Appraisal", "A process in many Texas policies for resolving disagreements about the amount of loss, using appraisers and an umpire."),
]


def build_all(c):
    home(c); about(c); process(c); services_hub(c)
    for s in c["SERVICES"]:
        service_page(c, s)
    tool_pages.build(c, KW)
    blog_hub(c)
    for p in c["POSTS"]:
        post_page(c, p)
    faqs(c); contact(c); legal(c); sitemap(c); not_found(c)


# ============================================================== HOME
def home(c):
    SITE, icon, img, A = c["SITE"], c["icon"], c["img"], c["ARROW"]
    options = "".join(f'<option value="{s["short"]}">{s["name"]}</option>' for s in c["SERVICES"])
    guide_dmg = "".join(f'<label><input type="radio" name="damage" value="{k}"{" checked" if i == 0 else ""}><span>{v["label"]}</span></label>' for i, (k, v) in enumerate(GUIDE["damage"].items()))
    guide_stage = "".join(f'<label><input type="radio" name="stage" value="{k}"{" checked" if i == 0 else ""}><span>{v["label"]}</span></label>' for i, (k, v) in enumerate(GUIDE["stage"].items()))
    gloss = "".join(f'<button type="button" class="flip" aria-pressed="false"><span class="flip-inner"><span class="flip-face flip-front"><small>Claim term</small><strong>{t}</strong></span><span class="flip-face flip-back">{d}</span></span></button>' for t, d in GLOSSARY)
    marquee_items = ["Hail damage", "Wind damage", "Roof claims", "Water damage", "Burst pipes", "Slab leaks", "Fire &amp; smoke", "Commercial property", "Denied claims", "Underpaid claims", "Supplements", "Appraisal support"]
    mq = "".join(f"<span>{m}</span>" for m in marquee_items)
    story = [
        ("inspector", "Homeowners talking with a claim professional", "01 · Listen & review", "Tell us what happened.", "We start with a free conversation about the damage, your policy and where the claim stands. If The Colony Public Adjuster is not the right fit, we will tell you."),
        ("roof-inspection", "Inspector on a storm-damaged roof", "02 · Inspect & document", "Every elevation. Every room.", "We inspect the property and build the evidence: dated photo logs, measurements, moisture readings and 3D documentation where it helps, so nothing important is left out."),
        ("estimate", "Reviewing estimate paperwork with a calculator", "03 · Prepare & present", "A claim the carrier can follow.", "We prepare a detailed, Xactimate-format repair estimate and an organized claim package that ties every line item back to the evidence and your policy."),
        ("consultation", "Claim professional shaking hands with a client", "04 · Negotiate & resolve", "We handle the back-and-forth.", "We communicate with the insurer, answer requests, push back on missed items and keep you updated until the claim is resolved."),
    ]
    story_imgs = "".join(img(n, a, cls="on" if i == 0 else "") for i, (n, a, *_r) in enumerate(story))
    story_steps = "".join(f'<div class="story-step{" on" if i == 0 else ""}"><span class="tag">{t}</span><h3 style="font:500 2rem/1.15 Fraunces,serif;margin:10px 0 14px">{h}</h3><p class="lead-p">{p}</p></div>' for i, (_n, _a, t, h, p) in enumerate(story))

    body = f'''
<section class="hero"><div class="hero-media">{img("hero", "Brick and stone family home with a green lawn in a North Texas neighborhood", lazy=False, priority=True)}</div>
<div class="wrap hero-grid">
<div><h1 class="split-words"><span class="kw">{KW}</span>Your property claim deserves a <em>stronger voice.</em></h1>
<p class="lead" data-reveal style="--d:500">{KW} helps homeowners and businesses in The Colony, Texas document damage, understand their policy and present a complete insurance claim. Hail, wind, water, fire, or a claim that was denied or underpaid: we work for you, not the insurance company.</p>
<div class="hero-actions" data-reveal style="--d:650"><a class="button" href="/contact/">Get a free claim review {A}</a><a class="button outline-light" href="tel:{SITE["phone_href"]}">{icon("phone")} {SITE["phone"]}</a></div>
<ul class="hero-ticks" data-reveal style="--d:800"><li>{icon("check")} Licensed Texas public adjusters</li><li>{icon("check")} Free, no-obligation review</li><li>{icon("check")} Homes &amp; businesses</li></ul></div>
<aside class="glass hero-card" aria-label="Start your free review"><h2>Start your free review</h2><p>Tell us what kind of damage you are dealing with. It takes about a minute.</p>
<form class="mini-form" id="quick-start" action="/contact/" method="get"><label class="sr" for="qs-type">Type of damage</label><select id="qs-type" name="type">{options}<option value="Other">Something else</option></select>
<button class="button light" type="submit">Continue {A}</button></form>
<div class="hero-stats"><div><strong data-count="1400" data-suffix="+">1,400+</strong><span>claim files reviewed yearly by our Texas firm</span></div><div><strong>$0</strong><span>for your first claim review</span></div><div><strong>100%</strong><span>on the policyholder's side</span></div></div></aside>
</div></section>

<div class="marquee-wrap" aria-hidden="true"><div class="marquee"><div class="marquee-track"><span>{mq}</span><span>{mq}</span></div></div></div>

<section class="section"><div class="wrap two-col">
<div class="stack" data-reveal="left"><div class="frame tall">{img("inspector", "Claim professional reviewing damage details with homeowners", parallax=".08")}</div>
<div class="frame small">{img("water-damage", "Water-damaged ceiling inside a home")}</div>
<div class="badge-float"><span class="ico" style="margin:0">{icon("shield")}</span><div><strong>TX #3356839</strong><span>Licensed public adjuster</span></div></div></div>
<div data-reveal="right"><span class="eyebrow">Your side of the claim</span><h2>You handle life. <em>We handle the claim.</em></h2>
<p class="lead-p">Property damage is stressful enough. Reading estimates, gathering records and keeping up with an insurance carrier can quickly become a second job.</p>
<p>{KW} brings order to the process. As a licensed public adjuster serving The Colony and Denton County, we inspect the damage, read your policy, prepare a supported claim and keep you informed at every step, so you can focus on your family, your tenants or your business.</p>
<ul class="check-list"><li>Thorough inspection and loss documentation</li><li>Policy and estimate review in plain language</li><li>Detailed, line-by-line repair estimates</li><li>Organized communication and negotiation with your carrier</li></ul>
<a class="button ghost" href="/about/">Meet your claim advocates {A}</a></div>
</div></section>

<section class="section tinted"><div class="wrap">
<div class="section-head center" data-reveal><span class="eyebrow">Claims we handle</span><h2>{KW} services for <em>every kind of loss.</em></h2><p>Every property has its own story. Every claim deserves an approach built around its damage, its policy and its circumstances.</p></div>
{c["service_cards"]()}
<p style="text-align:center;margin-top:40px" data-reveal><a class="button ghost" href="/services/">Compare all claim services {A}</a></p>
</div></section>

<section class="section dark on-dark"><div class="wrap">
<div class="stats" data-stagger>
<div class="stat"><strong data-count="1400" data-suffix="+">1,400+</strong><span>Claim files reviewed each year across our Texas firm</span></div>
<div class="stat"><strong data-count="15">15</strong><span>Days Texas insurers generally have to acknowledge a claim</span></div>
<div class="stat"><strong data-count="6">6</strong><span>Core claim types, residential and commercial</span></div>
<div class="stat"><strong>$0</strong><span>Upfront cost for your initial claim review</span></div>
</div></div></section>

<section class="section"><div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">How we help</span><h2>A clear path, <em>one step at a time.</em></h2><p>{KW} turns photos, estimates and letters into one organized process, from the first conversation to the final payment.</p></div>
<div class="story"><div class="story-media">{story_imgs}</div><div class="story-steps">{story_steps}
<div style="padding-top:20px"><a class="button" href="/our-process/">See our full claim process {A}</a></div></div></div>
</div></section>

<section class="section dark on-dark" id="guide"><div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">Interactive guide</span><h2>Where are you <em style="color:var(--gold-2)">in your claim?</em></h2><p>Pick two answers and {KW} will show you what to gather and what to read next. Nothing you select is sent to us.</p></div>
<div class="guide"><form class="panel" id="claim-guide" data-reveal="left" onsubmit="return false">
<fieldset class="choice-group"><legend>What kind of damage?</legend><div class="chips">{guide_dmg}</div></fieldset>
<fieldset class="choice-group"><legend>Where does your claim stand?</legend><div class="chips">{guide_stage}</div></fieldset>
<p class="small" style="margin:0">An organizational guide only, not a coverage decision or legal advice.</p></form>
<div class="panel guide-out" id="guide-out" data-reveal="right" aria-live="polite"><p>Choose your situation to see a starting plan. <a href="/tools/claim-checklist/">Open the full checklist</a>.</p></div></div>
</div></section>

<section class="section"><div class="wrap two-col">
<div data-reveal="left"><span class="eyebrow">Local claim help</span><h2>Your public adjuster <em>in The Colony, TX.</em></h2>
<p class="lead-p">The Colony sits on the eastern shore of Lewisville Lake in Denton County, squarely in North Texas hail country.</p>
<p>Spring storms that roll across the lake can bring large hail and straight-line winds within minutes, and the occasional hard freeze can burst pipes in homes across the city. {KW} knows these patterns and the claims they create, from Austin Ranch and the neighborhoods near Stewart Creek Park to the businesses around Grandscape and the SH 121 corridor.</p>
<p>We start with the facts of your property: what happened, when the damage was found, which areas are affected and what the insurer has said. Then we work from those facts and your policy, rather than assuming every loss follows the same pattern.</p>
<div class="toolbar"><a class="button" href="/contact/">Request a review in The Colony {A}</a></div>
<p class="small">Also serving Frisco, Little Elm, Lewisville, Plano, Carrollton, Hebron and the rest of Denton and Collin counties.</p></div>
<div class="frame wide" data-reveal="zoom">{img("city", "Aerial view of lakeside homes and docks similar to The Colony on Lewisville Lake", parallax=".1")}</div>
</div></section>

<section class="section tinted"><div class="wrap">
<div class="section-head center" data-reveal><span class="eyebrow">Claim language, explained</span><h2>Tap a term. <em>Get a clear answer.</em></h2><p>Insurance paperwork has its own vocabulary. Here are four terms {KW} explains most often.</p></div>
<div class="glossary" data-stagger>{gloss}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">Free claim tools</span><h2>Good questions. Useful tools. <em>Less guesswork.</em></h2><p>Get organized before your first conversation with seven free tools from {KW}. They run in your browser and nothing is sent to us.</p></div>
{c["tool_cards"](c["TOOLS"][:6])}
<p style="margin-top:34px" data-reveal><a class="button ghost" href="/tools/">See all free tools {A}</a></p>
</div></section>

<section class="section sand"><div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">From the claim journal</span><h2>A more informed <em>next step.</em></h2></div>
<div class="blog-grid" data-stagger>{c["blog_cards"](c["POSTS"][:3])}</div>
<p style="margin-top:34px" data-reveal><a class="button ghost" href="/blog/">Read all claim guides {A}</a></p>
</div></section>

<section class="section"><div class="wrap two-col top">
<div data-reveal="left"><span class="eyebrow">Before your first conversation</span><h2>{KW} <em>questions, answered.</em></h2><p>A clearer picture of representation, preparation and what a free review covers.</p><a class="button ghost" href="/faqs/">Read all FAQs {A}</a></div>
<div>{c["faq_block"](HOME_FAQS)}</div>
</div></section>
{c["cta_band"]()}
<script>window.TC_GUIDE={json.dumps(GUIDE)};</script>'''
    schema = [c["faq_schema"](HOME_FAQS),
              {"@type": "Service", "@id": SITE["origin"] + "/#service", "name": "Public adjusting in The Colony, Texas",
               "serviceType": "Public adjuster - property insurance claim representation", "provider": {"@id": SITE["origin"] + "/#organization"},
               "areaServed": {"@type": "City", "name": "The Colony, TX"}, "url": SITE["origin"] + "/services/"}]
    c["write"]("/", c["render"]("/", "The Colony Public Adjuster | Free Property Claim Review",
                                "The Colony Public Adjuster helps homeowners and businesses in The Colony, TX with hail, wind, water, fire and denied insurance claims. Free claim review.",
                                body, current="/", schema=schema))


# ============================================================== ABOUT
def about(c):
    SITE, icon, img, A = c["SITE"], c["icon"], c["img"], c["ARROW"]
    values = [("users", "Focused on your interests", "We represent the policyholder, never the insurer. Our role is to develop and present your claim within the terms of your policy and our written agreement."),
              ("camera", "Evidence before assumptions", "Photos, measurements, moisture readings, estimates and records explain what happened and what the repair actually requires."),
              ("message", "Communication that makes sense", "You should always know what has been requested, what has been submitted and which questions still need answers."),
              ("scale", "Honest expectations", "We tell you what the evidence appears to support, including when representation is unlikely to help. No outcome is ever guaranteed."),
              ("pin", "Local knowledge", "We know North Texas storm patterns, local building practices and the kinds of claims homes and businesses in The Colony face."),
              ("shield", "Licensed and accountable", f"{KW} is a service of {SITE['company']}, a Texas-licensed public adjusting firm (License #{SITE['license']}).")]
    tiles = "".join(f'<div class="tile"><span class="ico">{icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i, t, d in values)
    body = c["page_hero"]("An advocate for your property. <em>A partner through the claim.</em>",
                          f"{KW} helps policyholders understand, document and navigate property insurance claims, with the attention to detail your claim deserves.",
                          "about", "Two professionals collaborating at a desk", [("Home", "/"), ("About us", "/about/")])
    body += f'''<section class="section"><div class="wrap two-col">
<div data-reveal="left"><span class="eyebrow">Who we are</span><h2>Good representation <em>starts with listening.</em></h2>
<p class="lead-p">{KW} is a local service of {SITE["company"]}, Texas public adjuster license #{SITE["license"]}. Our work is centered entirely on the property owner's side of the insurance claim.</p>
<p>Our parent firm, <a class="text-link" href="{SITE["parent_site"]}" rel="noopener">TX Public Adjusting</a>, reviews more than 1,400 claim files a year for homeowners and businesses across Texas, from Dallas and Fort Worth to Houston, Austin and San Antonio. {KW} brings that experience to The Colony, Frisco, Little Elm, Lewisville and the surrounding communities.</p>
<p>Before we can explain a claim, we need to understand the property, the damage and your concerns. That first conversation gives us a starting point for a careful review. From homeowners to business owners and property managers, we organize the facts so the claim can be presented clearly and supported by documentation.</p>
<a class="button" href="/contact/">Start a conversation {A}</a></div>
<div class="frame tall" data-reveal="zoom">{img("consultation", "Claim professional shaking hands with a client across a desk", parallax=".08")}</div>
</div></section>
<section class="section tinted"><div class="wrap"><div class="section-head center" data-reveal><span class="eyebrow">What you can expect</span><h2>A careful approach. <em>A clear conversation.</em></h2></div>
<div class="tiles" data-stagger>{tiles}</div></div></section>
<section class="section"><div class="wrap two-col">
<div class="frame wide" data-reveal="left">{img("inspector", "Claim professional with a tablet talking with homeowners", parallax=".08")}</div>
<div data-reveal="right"><span class="eyebrow">Public adjuster vs. insurance adjuster</span><h2>Know who works <em>for whom.</em></h2>
<p>The adjuster your insurance company sends is hired by the carrier. A licensed public adjuster is hired by you. That is the core difference, and it shapes everything from how damage is documented to how disagreements are handled.</p>
<ul class="check-list"><li>Inspects and documents the loss for your side</li><li>Reads your policy for the coverages that apply</li><li>Prepares an independent repair estimate</li><li>Negotiates with the carrier on your behalf</li></ul>
<p class="small">Public adjusters do not provide legal advice. Legal questions may call for an attorney.</p></div>
</div></section>
{c["cta_band"]()}'''
    c["write"]("/about/", c["render"]("/about/", "About Us | The Colony Public Adjuster",
                                      "Meet The Colony Public Adjuster, a licensed Texas public adjusting service representing homeowners and businesses in property insurance claims.",
                                      body, current="/about/", schema=[c["breadcrumb_schema"]([("Home", "/"), ("About us", "/about/")])]))


# ============================================================== PROCESS
PROCESS = [
    ("Free review", "Tell us what happened. We review the claim status, the policy and your concerns, and explain whether representation is likely to help. No cost, no obligation."),
    ("Inspect & document", "We inspect the property and organize photographs, measurements, moisture readings and 3D imaging where useful, building a complete record of the loss."),
    ("Prepare the claim", "We prepare a detailed repair estimate in industry-standard software such as Xactimate and compile the photos, reports and records that support it."),
    ("Negotiate", "We present the claim, answer the carrier's requests and follow up on missed or undervalued items, keeping you informed throughout."),
    ("Resolution", "When the claim is resolved, we walk you through the payment, recoverable depreciation and any remaining steps as you rebuild."),
]


def process(c):
    SITE, icon, img, A = c["SITE"], c["icon"], c["img"], c["ARROW"]
    steps = "".join(f'<div class="step"><span class="dot">{i:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PROCESS, 1))
    body = c["page_hero"]("A considered process. <em>A clearer next step.</em>",
                          f"Here is what working with {KW} looks like, from the first conversation through the final payment.",
                          "inspector", "Claim professional reviewing details with homeowners", [("Home", "/"), ("Our process", "/our-process/")])
    body += f'''<section class="section"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Five steps</span><h2>From damage <em>to resolution.</em></h2></div>
<div class="timeline five">{steps}</div></div></section>
<section class="section tinted"><div class="wrap two-col top">
<div data-reveal="left"><span class="eyebrow">Before representation begins</span><h2>Clear terms, <em>in writing.</em></h2>
<p>We discuss the scope of work, the fee arrangement and your questions before you sign anything. Texas law requires a written contract for public adjusting services and sets rules for how fees work. An initial review does not create a client relationship or guarantee a claim payment.</p>
<h3 style="margin-top:30px">Bring what you already have</h3><p>Your policy, a carrier estimate, a decision letter and photographs are all useful starting points. We will tell you which other documents would help. Please do not send sensitive documents through the general contact form.</p></div>
<div data-reveal="right"><h3>Stay involved and informed</h3><p>You may need to provide access to the property, review information or supply records. We explain the purpose of every request so you understand how it fits into the claim.</p>
<h3 style="margin-top:30px">Every claim follows its own timeline</h3><p>Inspections, document requests, policy questions and carrier review all affect timing. Texas prompt-payment rules set insurer deadlines once requested items are received, and our <a class="text-link" href="/tools/texas-claim-deadlines/">Texas claim deadline calculator</a> maps them out. We discuss the circumstances of your file rather than promise a fixed completion date.</p>
<div class="frame wide" style="margin-top:26px">{img("roof-inspection", "Inspector documenting roof damage on a brick home", parallax=".06")}</div></div>
</div></section>
{c["cta_band"]("Ready for step one?", f"Your free review with {KW} starts with a short conversation. Tell us what happened and we will take it from there.")}'''
    schema = [c["breadcrumb_schema"]([("Home", "/"), ("Our process", "/our-process/")]),
              {"@type": "ItemList", "name": "The Colony Public Adjuster claim process",
               "itemListElement": [{"@type": "ListItem", "position": i, "name": t, "description": d} for i, (t, d) in enumerate(PROCESS, 1)]}]
    c["write"]("/our-process/", c["render"]("/our-process/", "Our Claim Process | The Colony Public Adjuster",
                                            "See how The Colony Public Adjuster moves a property claim from free review to inspection, estimate, negotiation and resolution.",
                                            body, current="/our-process/", schema=schema))


# ============================================================== SERVICES
def services_hub(c):
    SITE, icon, img, A = c["SITE"], c["icon"], c["img"], c["ARROW"]
    body = c["page_hero"]("The right support <em>for your kind of loss.</em>",
                          f"From a hail-damaged roof to a complex commercial loss, {KW} brings the documentation and the conversation together.",
                          "storm", "Storm clouds gathering over a suburban street", [("Home", "/"), ("Services", "/services/")])
    body += f'''<section class="section"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Claim services</span><h2>Six ways {KW} <em>can help.</em></h2><p>Choose the service closest to your situation. Not sure which fits? A free review will sort it out.</p></div>
{c["service_cards"]()}</div></section>
<section class="section tinted"><div class="wrap"><div class="section-head center" data-reveal><span class="eyebrow">In every claim</span><h2>What our representation <em>includes.</em></h2></div>
<div class="tiles four" data-stagger>
<div class="tile"><span class="ico">{icon("search")}</span><h3>Policy review</h3><p>Coverages, limits, deductibles, endorsements and exclusions, in plain language.</p></div>
<div class="tile"><span class="ico">{icon("camera")}</span><h3>Documentation</h3><p>Photo logs, measurements, moisture readings and 3D imaging where it helps.</p></div>
<div class="tile"><span class="ico">{icon("calculator")}</span><h3>Estimating</h3><p>Detailed, line-by-line repair estimates in industry-standard software.</p></div>
<div class="tile"><span class="ico">{icon("message")}</span><h3>Negotiation</h3><p>Carrier communication, follow-up and supplements until the claim is resolved.</p></div>
</div></div></section>
{c["cta_band"]()}'''
    schema = [c["breadcrumb_schema"]([("Home", "/"), ("Services", "/services/")]),
              {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": SITE["origin"] + f"/services/{s['slug']}/", "name": s["name"]} for i, s in enumerate(c["SERVICES"], 1)]}]
    c["write"]("/services/", c["render"]("/services/", "Property Claim Services | The Colony Public Adjuster",
                                         "Residential, commercial, hail, wind, water, fire and denied claim services from The Colony Public Adjuster in The Colony, Texas.",
                                         body, current="/services/", schema=schema))


def service_page(c, s):
    SITE, icon, img, A = c["SITE"], c["icon"], c["img"], c["ARROW"]
    path = f"/services/{s['slug']}/"
    crumbs = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
    org = "".join(f"<li>{x}</li>" for x in s["organize"])
    disputes = "".join(f'<div class="tile"><h3>{t}</h3><p>{d}</p></div>' for t, d in s["disputes"])
    steps = "".join(f'<div class="step"><span class="dot">{i:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PROCESS[:4], 1))
    related = [c["POST_BY_SLUG"][x] for x in s["blog"]]
    others = [x for x in c["SERVICES"] if x["slug"] != s["slug"]][:3]
    body = c["page_hero"](s["h1"], s["lead"], s["img"], s["img_alt"], crumbs)
    body += f'''<section class="section"><div class="wrap two-col">
<div data-reveal="left"><span class="eyebrow">Our approach</span><h2>{s["intro_h"]}</h2>{"".join(f"<p>{p}</p>" for p in s["intro"])}
<a class="button" href="/contact/?type={html.escape(s["short"])}#request">Discuss your {s["short"].lower()} claim {A}</a></div>
<div class="frame tall" data-reveal="zoom">{img(s["img2"], s["img2_alt"], parallax=".08")}</div>
</div></section>
<section class="section dark on-dark"><div class="wrap two-col top">
<div data-reveal="left"><span class="eyebrow">What we document</span><h2>What {KW} <em style="color:var(--gold-2)">helps organize.</em></h2><p>A strong {s["name"].lower()} claim is built from specific, well-organized evidence. Here is what we gather and present on your behalf.</p></div>
<ul class="check-list" data-stagger>{org}</ul>
</div></section>
<section class="section"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Common sticking points</span><h2>{s["disputes_h"]}</h2></div>
<div class="tiles two" data-stagger>{disputes}</div></div></section>
<section class="section tinted"><div class="wrap two-col top">
<div data-reveal="left"><span class="eyebrow">A useful first step</span><h2>{s["first_h"]}</h2><p class="lead-p">{s["first"]}</p>
<div class="callout"><p>Representation, services and fees are set out in a written agreement. Coverage and outcomes depend on your policy and the facts of the loss.</p></div>
<div class="toolbar"><a class="button ghost" href="/tools/claim-checklist/">Open the claim checklist {A}</a></div></div>
<div><h3 style="margin-bottom:18px">{s["name"]} claim FAQs</h3>{c["faq_block"](s["faqs"])}</div>
</div></section>
<section class="section"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">What happens next</span><h2>From questions <em>to a clearer file.</em></h2></div>
<div class="timeline">{steps}</div></div></section>
<section class="section sand"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Keep reading</span><h2>Related claim guides</h2></div>
<div class="blog-grid" data-stagger>{c["blog_cards"](related)}<a class="tool-card" href="/services/"><span class="ico">{icon("list")}</span><span class="kicker">Other services</span><h3>More ways we help</h3><p>{" · ".join(o["name"] for o in others)}</p><span class="text-link">All services {A}</span></a></div></div></section>
{c["cta_band"](f"Talk with {KW} about your {s['short'].lower()} claim.")}'''
    schema = [c["breadcrumb_schema"](crumbs), c["faq_schema"](s["faqs"]),
              {"@type": "Service", "name": s["name"] + " claims in The Colony, TX", "serviceType": "Public adjuster - " + s["name"].lower() + " insurance claims",
               "description": s["desc"], "provider": {"@id": SITE["origin"] + "/#organization"},
               "areaServed": {"@type": "City", "name": "The Colony, TX"}, "url": SITE["origin"] + path}]
    c["write"](path, c["render"](path, s["title"], s["desc"], body, current="/services/", schema=schema,
                                 og_image="og-image.jpg"))


# ============================================================== BLOG
def blog_hub(c):
    cats = sorted({p["category"] for p in c["POSTS"]})
    btns = '<button type="button" data-filter="All" aria-pressed="true">All</button>' + "".join(f'<button type="button" data-filter="{x}" aria-pressed="false">{x}</button>' for x in cats)
    body = c["page_hero"]("Practical guidance <em>for the moments that matter.</em>",
                          f"Plain-language claim guides from {KW} to help property owners in The Colony document damage, read estimates and ask better questions.",
                          "estimate", "Reviewing claim paperwork", [("Home", "/"), ("Blog", "/blog/")], actions=False)
    body += f'''<section class="section"><div class="wrap">
<div class="filters" data-reveal><label class="sr" for="blog-search">Search the guides</label><input id="blog-search" type="search" placeholder="Search claim guides…">{btns}</div>
<p class="small" id="article-count" aria-live="polite">{len(c["POSTS"])} guides</p>
<div class="blog-grid" data-stagger>{c["blog_cards"](c["POSTS"])}</div>
<p id="filter-empty" hidden>No guides match your search. Try another keyword or select All.</p>
</div></section>
<section class="section tinted"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Put the guides to work</span><h2>Free tools <em>to go with them.</em></h2></div>{c["tool_cards"](c["TOOLS"][:3])}</div></section>
{c["cta_band"]()}'''
    schema = [c["breadcrumb_schema"]([("Home", "/"), ("Blog", "/blog/")]),
              {"@type": "Blog", "name": "The Colony Public Adjuster claim journal", "url": c["SITE"]["origin"] + "/blog/",
               "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": c["SITE"]["origin"] + f"/blog/{p['slug']}/", "datePublished": p["date"]} for p in c["POSTS"]]}]
    c["write"]("/blog/", c["render"]("/blog/", "Property Claim Guides & Blog | The Colony Public Adjuster",
                                     "Claim guides from The Colony Public Adjuster: hail damage, water damage, reading estimates, denied claims and home inventories for Texas property owners.",
                                     body, current="/blog/", schema=schema))


def _slugify(t):
    import re
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def post_page(c, p):
    SITE, icon, img, A = c["SITE"], c["icon"], c["img"], c["ARROW"]
    path = f"/blog/{p['slug']}/"
    crumbs = [("Home", "/"), ("Blog", "/blog/"), (p["category"], path)]
    words = sum(len(" ".join(b).split()) for _h, b in p["sections"])
    mins = max(3, round(words / 220))
    toc = "".join(f'<li><a href="#{_slugify(h)}">{h}</a></li>' for h, _b in p["sections"])
    secs = "".join(f'<h2 id="{_slugify(h)}">{h}</h2>' + "".join(b) for h, b in p["sections"])
    tk = "".join(f"<li>{t}</li>" for t in p["takeaways"])
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in p["faqs"])
    related = [x for x in c["POSTS"] if x["slug"] != p["slug"]][:3]
    byline = (f'<div class="byline" data-reveal style="--d:200"><span>{icon("users")} {KW} team</span>'
              f'<span>{icon("calendar")} <time datetime="{p["date"]}">{c["fmt_date"](p["date"])}</time></span><span>{icon("clock")} {mins} min read</span></div>')
    body = c["page_hero"](p["h1"][0].upper() + p["h1"][1:], p["excerpt"], p["img"], p["img_alt"], crumbs, actions=False, extra=byline)
    src_t, src_u = p["source"]
    body += f'''<section class="section"><div class="wrap article-layout">
<aside class="toc no-print"><strong>In this guide</strong><ol>{toc}<li><a href="#faq">FAQs</a></li></ol>
<div style="margin-top:20px;padding-top:18px;border-top:1px solid var(--line)"><p class="small">Need help with your claim?</p><a class="button small" href="/contact/">Free claim review</a></div></aside>
<article class="prose">
<div class="key-takeaways"><h2>Key takeaways</h2><ul class="check-list" style="margin:0">{tk}</ul></div>
<figure>{img(p["img"], p["img_alt"])}</figure>
{secs}
<h2 id="faq">Frequently asked questions</h2>{faq_html}
<div class="callout"><p><strong>Continue preparing.</strong> Use our <a href="/tools/">free claim tools</a> or <a href="/contact/">request a free review from {KW}</a> to talk through your next step.</p></div>
<p class="small">Further reading: <a href="{src_u}" rel="noopener" target="_blank">{src_t}</a>. This article is general educational information from {KW}. Your policy and circumstances govern your claim, and this is not legal advice.</p>
</article></div></section>
<section class="section sand"><div class="wrap"><div class="section-head" data-reveal><span class="eyebrow">Keep reading</span><h2>More claim guides</h2></div><div class="blog-grid" data-stagger>{c["blog_cards"](related)}</div></div></section>
{c["cta_band"]()}'''
    schema = [c["breadcrumb_schema"](crumbs), c["faq_schema"](p["faqs"]),
              {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "datePublished": p["date"],
               "dateModified": c["TODAY"], "image": SITE["origin"] + f"/assets/img/{p['img']}.webp",
               "author": {"@type": "Organization", "name": KW, "url": SITE["origin"] + "/"},
               "publisher": {"@id": SITE["origin"] + "/#organization"}, "mainEntityOfPage": SITE["origin"] + path,
               "articleSection": p["category"], "wordCount": words}]
    c["write"](path, c["render"](path, p["title"], p["desc"], body, current="/blog/", schema=schema, og_type="article"))


# ============================================================== FAQS
ALL_FAQS = [
    ("About public adjusters", [
        ("What does a public adjuster do?", "A public adjuster represents the policyholder in a property insurance claim. Depending on the agreement, that can include inspecting the damage, documenting the loss, reviewing the policy and the insurer's estimate, preparing the claim and communicating with the insurance company."),
        ("Who does The Colony Public Adjuster represent?", "We represent insured property owners: homeowners, landlords, businesses, associations and property managers. We never act as the insurance company's adjuster."),
        ("How is a public adjuster different from my insurance company's adjuster?", "The company adjuster is hired by the insurer. A public adjuster is hired by you and works only for your side of the claim."),
        ("Is a public adjuster an attorney or a contractor?", "No. These are different roles. Public adjusting concerns the insurance claim within the authorized scope of representation. We are not a law firm and do not give legal advice, and we do not perform repairs."),
        ("Are public adjusters licensed in Texas?", "Yes. Public adjusters in Texas must be licensed by the Texas Department of Insurance. The Colony Public Adjuster is a service of Rise Public Adjusting LLC, license #3356839."),
    ]),
    ("Getting started", [
        ("When should I contact you?", "Any time: right after you discover damage, during an active claim, or after you receive an estimate or decision that concerns you. Do not delay any notice your policy requires while waiting for a consultation."),
        ("Is the initial review free?", "Yes. The initial claim review is free and there is no obligation. We explain any proposed representation and fee arrangement before a written agreement is signed."),
        ("What should I have ready for a review?", "Your policy or declarations page, claim number, estimates, decision letters, photographs and a short timeline if you have them. Start by sharing only basic details through the contact form; we will arrange a secure way to receive documents."),
        ("Should I wait for you before preventing further damage?", "No. Do not leave an unsafe situation unaddressed. Call emergency services when needed and appropriate professionals for urgent work. Document conditions and keep records of the reasonable steps you take."),
        ("Do you serve areas outside The Colony?", "Yes. We also serve Frisco, Little Elm, Lewisville, Plano, Carrollton, Hebron and other communities in Denton and Collin counties. Our parent firm serves property owners across Texas."),
    ]),
    ("Fees and outcomes", [
        ("How much does representation cost?", "Fees and how they are calculated are explained in the proposed written agreement, subject to Texas requirements for public adjuster contracts. Ask which payments the fee applies to before signing."),
        ("Can you guarantee a larger settlement?", "No. The facts, documentation, policy terms and claim circumstances determine what can be supported. No particular payment or outcome is guaranteed."),
        ("How long will my claim take?", "There is no single timeline. Inspections, document requests, the extent of damage and coverage questions all play a part. Texas prompt-payment rules set insurer response deadlines once requested items are received."),
    ]),
    ("Claim types", [
        ("Can you review a denied or underpaid claim?", "Yes. We review the written decision, policy, estimates and evidence to identify questions that may need further attention. A review does not guarantee a denial will change or that more will be paid."),
        ("Do you handle residential and commercial claims?", "Yes. We handle homes, rentals, condos and townhomes as well as offices, retail, restaurants, warehouses, churches and multifamily properties."),
        ("Do you handle hail and roof claims?", "Yes. Hail and wind claims are among the most common we see in North Texas, including roofs, gutters, siding, windows, fences and interior leaks."),
        ("Can you help with water damage from a burst pipe or slab leak?", "Yes. We document the source, the spread, mitigation and repairs for plumbing and appliance water losses."),
    ]),
]


def faqs(c):
    flat = [qa for _g, items in ALL_FAQS for qa in items]
    groups = "".join(f'<div style="margin-bottom:50px"><h2 style="font-size:1.8rem" data-reveal>{g}</h2>{c["faq_block"](items, open_first=False)}</div>' for g, items in ALL_FAQS)
    body = c["page_hero"]("Good questions. <em>Straightforward answers.</em>",
                          f"Everything you might want to know about {KW}, public adjusting and what to expect before your first conversation.",
                          "consultation", "Claim professional greeting a client", [("Home", "/"), ("FAQs", "/faqs/")])
    body += f'''<section class="section"><div class="wrap" style="max-width:900px">{groups}</div></section>{c["cta_band"]("Still have a question?", "Call or send a message. A short conversation is often the fastest way to get a clear answer about your claim.")}'''
    c["write"]("/faqs/", c["render"]("/faqs/", "Public Adjuster FAQs | The Colony Public Adjuster",
                                     "Answers to common questions about The Colony Public Adjuster: what public adjusters do, fees, free claim reviews, timelines and denied claims.",
                                     body, current="/faqs/", schema=[c["breadcrumb_schema"]([("Home", "/"), ("FAQs", "/faqs/")]), c["faq_schema"](flat)]))


# ============================================================== CONTACT
def contact(c):
    SITE, icon, img, A = c["SITE"], c["icon"], c["img"], c["ARROW"]
    types = "".join(f'<option value="{s["short"]}">{s["name"]}</option>' for s in c["SERVICES"]) + '<option value="Other">Other</option>'
    body = c["page_hero"]("Tell us what happened. <em>We'll help you find a starting point.</em>",
                          f"Request a free initial claim review from {KW}. Share a few details about the damage and where your claim stands.",
                          "contact", "Smiling claim professional on a phone call", [("Home", "/"), ("Contact", "/contact/")], actions=False)
    body += f'''<section class="section"><div class="wrap two-col top">
<div data-reveal="left"><span class="eyebrow">Start a conversation</span><h2>Real questions deserve <em>a thoughtful review.</em></h2>
<p>Reach {KW} by phone, email or the form. We will talk through the property, the damage and the documents that would help, and whether public adjuster representation makes sense for you.</p>
<div class="contact-cards">
<a class="contact-card" href="tel:{SITE["phone_href"]}"><span class="ico">{icon("phone")}</span><span><strong>{SITE["phone"]}</strong><span>Call for a free claim review</span></span></a>
<a class="contact-card" href="mailto:{SITE["email"]}"><span class="ico">{icon("mail")}</span><span><strong>{SITE["email"]}</strong><span>Email us anytime</span></span></a>
<div class="contact-card"><span class="ico">{icon("pin")}</span><span><strong>Serving The Colony, Texas</strong><span>{SITE["county"]} &middot; Frisco, Little Elm, Lewisville, Plano &amp; Carrollton</span></span></div>
<div class="contact-card"><span class="ico">{icon("shield")}</span><span><strong>{SITE["company"]}</strong><span>Texas Public Adjuster License #{SITE["license"]}</span></span></div>
</div>
<h3>What happens after you reach out?</h3><p>We review your information and contact you to discuss the property, the damage and any documents that would help us understand the claim.</p>
<p class="small">For an immediate threat to life or property, call 911. This form is not monitored as an emergency service.</p></div>
<div class="panel" id="request" data-reveal="right"><h2 style="font-size:2rem">Request your free review</h2><p class="small">Fields marked * are required.</p>
<form id="contact-form" action="/send-mail.php" method="post" novalidate>
<div class="hp" aria-hidden="true"><label for="website">Leave this field empty</label><input id="website" name="website" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="csrf" value=""><input type="hidden" name="ts" value="">
<div class="form-grid">
<div class="field"><label for="name">Full name *</label><input id="name" name="name" required autocomplete="name" maxlength="100"></div>
<div class="field"><label for="phone">Phone number *</label><input id="phone" name="phone" type="tel" required autocomplete="tel" maxlength="40"></div>
<div class="field"><label for="email">Email address *</label><input id="email" name="email" type="email" required autocomplete="email" maxlength="160"></div>
<div class="field"><label for="city">Property city</label><input id="city" name="city" value="The Colony" autocomplete="address-level2" maxlength="80"></div>
<div class="field"><label for="claim_type">Claim type *</label><select id="claim_type" name="claim_type" required><option value="">Select claim type</option>{types}</select></div>
<div class="field"><label for="claim_status">Claim status</label><select id="claim_status" name="claim_status"><option>Not filed yet</option><option>Filed, awaiting review</option><option>Estimate or offer received</option><option>Claim denied</option><option>Underpaid / partially paid</option><option>Other / unsure</option></select></div>
<div class="field full"><label for="message">What happened? *</label><textarea id="message" name="message" required maxlength="3000" placeholder="For example: hail on April 12, roof and gutters damaged, insurer estimate received last week…"></textarea><span class="hint">Please do not include policy numbers, financial information or sensitive documents.</span></div>
<label class="check-label field full"><input type="checkbox" name="consent" value="1" required><span>I agree to be contacted about this request and have read the <a class="text-link" href="/privacy-policy/">Privacy Policy</a>. *</span></label>
</div>
<button class="button" type="submit" style="margin-top:20px;width:100%">Request my free claim review {A}</button>
<div class="form-status" id="form-status" role="status" tabindex="-1"></div>
<p class="small" style="margin-top:14px">Submitting this form does not create a public adjuster-client relationship.</p>
<noscript><p class="small">JavaScript is off. The form will still send, or call {SITE["phone"]}.</p></noscript>
</form></div>
</div></section>
<script>(function(){{var q=new URLSearchParams(location.search),s=document.getElementById('form-status');if(!s)return;if(q.get('sent')){{s.className='form-status ok';s.textContent='Thank you. Your request was sent and we will contact you shortly.';}}else if(q.get('error')){{s.className='form-status err';s.textContent='Your request could not be sent. Please call {SITE["phone"]}.';}}}})();</script>'''
    schema = [c["breadcrumb_schema"]([("Home", "/"), ("Contact", "/contact/")]),
              {"@type": "ContactPage", "url": SITE["origin"] + "/contact/", "mainEntity": {"@id": SITE["origin"] + "/#organization"}}]
    c["write"]("/contact/", c["render"]("/contact/", "Contact The Colony Public Adjuster | Free Claim Review",
                                        "Call (832) 503-5866 or send a message to request a free property claim review from The Colony Public Adjuster in The Colony, TX.",
                                        body, current="/contact/", schema=schema))


# ============================================================== LEGAL
def legal(c):
    SITE = c["SITE"]
    privacy = [
        ("Information you choose to provide", f"When you contact {KW}, we receive the name, phone number, email address, city, claim category, claim status and message you submit. We use this information to respond, discuss services and keep relevant business records. Please do not include sensitive documents or policy, financial or identity numbers in the general form."),
        ("Service providers and disclosures", "Website hosting and email providers process the information needed to run the site and deliver inquiries. Information may also be disclosed where required by law or to protect rights and security. Submitting an inquiry does not sign you up for marketing emails."),
        ("Cookies and browser storage", "The contact form uses a temporary session cookie to help protect submissions. Our free tools (checklist, home inventory, claim diary and depreciation worksheet) save your entries in local storage on your own device only; they are never sent to us. You can clear them with each tool's clear button or your browser's site data settings. The calculators run entirely in your browser. This website loads fonts from Google Fonts and does not use advertising trackers."),
        ("Technical records and retention", "Our hosting provider may keep access and security logs. The form stores a one-way hashed network address in temporary rate-limit records to reduce spam. We keep inquiries and related correspondence as needed to respond, provide services, meet obligations and resolve issues."),
        ("Your choices", "You can contact us to ask about your information, request a correction or deletion, or raise a privacy concern. We may need to verify a request and may keep some information where required or permitted by law."),
        ("Security and external links", "We use reasonable safeguards, but no internet transmission or storage method is completely secure. External sites have their own privacy practices. This site is intended for adult property owners and business representatives."),
        ("Contact and updates", f"Email {SITE['email']} or call {SITE['phone']} with questions. This policy may be updated as our practices change. Effective October 1, 2026."),
    ]
    terms = [
        ("Educational information", "This website provides general information about property claims and public adjusting. It is not a substitute for reading your policy or getting advice about your specific circumstances. We are not a law firm and do not provide legal advice."),
        ("No representation or guaranteed outcome", "Visiting this site, using a tool or submitting a form does not create a public adjuster-client relationship. Representation begins only with a signed written agreement. No recovery, payment amount, coverage decision or claim timeline is guaranteed."),
        ("Tools and examples", "Our calculators illustrate arithmetic using the numbers you enter. They do not determine coverage, payments, fees or the deductible your policy requires. The Texas claim deadline calculator summarizes general statutory timeframes and is not legal advice; deadlines can differ by policy, insurer type and circumstances. The checklist and organizers are aids, not a complete statement of policy duties or legal requirements."),
        ("Your submissions", "Provide accurate contact information and avoid sending sensitive personal data through the general form. Do not use the website to send spam, malicious content or material you do not have permission to share."),
        ("Content and third-party resources", "Website materials are provided for informational use. Photographs are used under the Unsplash License. Links to external resources do not guarantee their accuracy or availability."),
        ("Availability and questions", f"We aim to keep information useful and current, but content may contain errors or become outdated. Contact {SITE['email']} about an apparent error or a question. Effective October 1, 2026."),
    ]
    for path, name, lead, items, desc in [
        ("/privacy-policy/", "Privacy Policy", f"How {KW} collects, uses and protects information on this website.", privacy,
         "Privacy Policy for The Colony Public Adjuster: what information we collect, how the contact form and free tools handle data, and your choices."),
        ("/terms-of-use/", "Terms of Use", f"The terms that apply when you use the {KW} website and free tools.", terms,
         "Terms of Use for The Colony Public Adjuster website, including educational content, free claim tools and no-guarantee disclosures."),
    ]:
        secs = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in items)
        body = c["page_hero"](name, lead, "tools", "Calculator and notepad on a desk", [("Home", "/"), (name, path)], actions=False)
        body += f'<section class="section"><div class="wrap"><div class="prose">{secs}</div></div></section>'
        c["write"](path, c["render"](path, f"{name} | {KW}", desc, body, schema=[c["breadcrumb_schema"]([("Home", "/"), (name, path)])]))


def sitemap(c):
    groups = [
        ("Main pages", [("Home", "/"), ("About us", "/about/"), ("Our process", "/our-process/"), ("FAQs", "/faqs/"), ("Contact", "/contact/")]),
        ("Services", [("All services", "/services/")] + [(s["name"], f"/services/{s['slug']}/") for s in c["SERVICES"]]),
        ("Free tools", [("All tools", "/tools/")] + [(t["name"], f"/tools/{t['slug']}/") for t in c["TOOLS"]]),
        ("Claim guides", [("Blog", "/blog/")] + [(p["h1"][0].upper() + p["h1"][1:], f"/blog/{p['slug']}/") for p in c["POSTS"]]),
        ("Legal", [("Privacy Policy", "/privacy-policy/"), ("Terms of Use", "/terms-of-use/")]),
    ]
    cols = "".join(f'<div class="tile"><h3>{g}</h3><ul style="padding-left:18px;margin:0">' + "".join(f'<li><a class="text-link" href="{u}">{n}</a></li>' for n, u in items) + "</ul></div>" for g, items in groups)
    body = c["page_hero"]("Sitemap", f"Every page on the {KW} website.", "city", "Lakeside homes from above", [("Home", "/"), ("Sitemap", "/sitemap/")], actions=False)
    body += f'<section class="section"><div class="wrap"><div class="tiles" data-stagger>{cols}</div></div></section>'
    c["write"]("/sitemap/", c["render"]("/sitemap/", f"Sitemap | {KW}", "A complete list of pages on The Colony Public Adjuster website: services, free claim tools, guides and contact.", body,
                                        schema=[c["breadcrumb_schema"]([("Home", "/"), ("Sitemap", "/sitemap/")])]))


def not_found(c):
    A = c["ARROW"]
    body = f'''<section class="page-hero"><div class="bg">{c["img"]("storm", "Storm clouds over a street", lazy=False)}</div><div class="wrap">
<h1>This page blew away <em>in the storm.</em></h1><p class="lead">The page you are looking for has moved or no longer exists. Try one of these instead.</p>
<div class="hero-actions"><a class="button light" href="/">Back to the homepage {A}</a><a class="button outline-light" href="/contact/">Request a free claim review</a></div></div></section>
<section class="section"><div class="wrap">{c["service_cards"]()}</div></section>'''
    html_out = c["render"]("/404.html", f"Page not found | {KW}", "The page you requested could not be found.", body, noindex=True)
    c["write"]("/404.html", html_out)
