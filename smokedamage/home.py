"""Homepage for SmokeDamage.com — the main sales page."""

import html


def esc(s):
    return html.escape(str(s), quote=True)


HOUSE_SVG = """<svg viewBox="0 0 560 420" role="img" aria-labelledby="hd-t hd-d">
<title id="hd-t">How smoke can travel through a house</title>
<desc id="hd-d">Cross-section of a two-level house. Smoke moves from a kitchen fire origin into the adjacent room and hallway, is drawn into an HVAC return, passes through the air handler and ductwork in the attic, and can be distributed to other rooms and onto contents.</desc>
<defs>
<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#FF6D1F"/></marker>
<linearGradient id="smk" x1="0" x2="1"><stop offset="0" stop-color="#FF6D1F" stop-opacity=".30"/><stop offset="1" stop-color="#FF6D1F" stop-opacity=".04"/></linearGradient>
</defs>
<path d="M40 150 L280 30 L520 150" fill="none" stroke="#222" stroke-width="3" stroke-linejoin="round"/>
<rect x="60" y="150" width="440" height="240" fill="#FFFDF7" stroke="#222" stroke-width="3"/>
<path d="M80 150 L280 50 L480 150" fill="#F5E7C6" opacity=".55"/>
<line x1="60" y1="270" x2="500" y2="270" stroke="#222" stroke-width="2"/>
<line x1="200" y1="270" x2="200" y2="390" stroke="#222" stroke-width="2"/>
<line x1="330" y1="270" x2="330" y2="390" stroke="#222" stroke-width="2"/>
<line x1="230" y1="150" x2="230" y2="270" stroke="#222" stroke-width="2"/>
<line x1="370" y1="150" x2="370" y2="270" stroke="#222" stroke-width="2"/>
<rect x="72" y="282" width="118" height="98" rx="6" fill="url(#smk)"/>
<rect x="212" y="282" width="108" height="98" rx="6" fill="#FF6D1F" opacity=".10"/>
<rect x="342" y="282" width="146" height="98" rx="6" fill="#FF6D1F" opacity=".06"/>
<rect x="250" y="96" width="80" height="34" rx="6" fill="#fff" stroke="#222" stroke-width="2"/>
<text x="290" y="117" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="11" font-weight="700" fill="#222">Air handler</text>
<path d="M250 113 H120 V150" fill="none" stroke="#6C665E" stroke-width="6" stroke-linecap="round" opacity=".35"/>
<path d="M330 113 H440 V150" fill="none" stroke="#6C665E" stroke-width="6" stroke-linecap="round" opacity=".35"/>
<path d="M300 130 V150" fill="none" stroke="#6C665E" stroke-width="6" opacity=".35"/>
<text x="340" y="84" font-family="Montserrat,sans-serif" font-size="10" font-weight="700" fill="#6C665E">Attic / ductwork</text>
<path d="M130 330 C 170 320, 190 320, 230 330" fill="none" stroke="#FF6D1F" stroke-width="3" stroke-dasharray="6 5" marker-end="url(#ar)"/>
<path d="M265 300 C 270 260, 285 200, 296 158" fill="none" stroke="#FF6D1F" stroke-width="3" stroke-dasharray="6 5" marker-end="url(#ar)"/>
<path d="M120 152 C 115 190, 130 215, 140 235" fill="none" stroke="#FF6D1F" stroke-width="3" stroke-dasharray="6 5" marker-end="url(#ar)"/>
<path d="M440 152 C 445 190, 430 215, 425 235" fill="none" stroke="#FF6D1F" stroke-width="3" stroke-dasharray="6 5" marker-end="url(#ar)"/>
<path d="M310 340 C 340 336, 360 336, 390 342" fill="none" stroke="#FF6D1F" stroke-width="3" stroke-dasharray="6 5" marker-end="url(#ar)"/>
<circle cx="110" cy="352" r="16" fill="#FF6D1F"/>
<path d="M110 340 c6 7 8 11 2 20 c-2-5-6-6-7-10 c-3 4-3 7-1 10 c-6-3-7-12 6-20z" fill="#fff"/>
<text x="131" y="300" font-family="Montserrat,sans-serif" font-size="11" font-weight="800" fill="#222">1 · Fire origin</text>
<text x="222" y="300" font-family="Montserrat,sans-serif" font-size="11" font-weight="800" fill="#222">2 · Hallway</text>
<text x="262" y="232" font-family="Montserrat,sans-serif" font-size="11" font-weight="800" fill="#222">3 · Return</text>
<text x="352" y="300" font-family="Montserrat,sans-serif" font-size="11" font-weight="800" fill="#222">Adjacent room</text>
<text x="80" y="200" font-family="Montserrat,sans-serif" font-size="11" font-weight="800" fill="#222">Bedroom</text>
<text x="388" y="200" font-family="Montserrat,sans-serif" font-size="11" font-weight="800" fill="#222">Bedroom</text>
<rect x="400" y="340" width="60" height="30" rx="4" fill="#fff" stroke="#222" stroke-width="1.5"/>
<text x="430" y="359" text-anchor="middle" font-family="Montserrat,sans-serif" font-size="9" font-weight="700" fill="#222">Contents</text>
<rect x="150" y="226" width="44" height="32" rx="4" fill="#fff" stroke="#222" stroke-width="1.5"/>
<rect x="400" y="226" width="44" height="32" rx="4" fill="#fff" stroke="#222" stroke-width="1.5"/>
</svg>"""


def build(b, locations, posts, events):
    SITE = b.SITE
    icon = b.icon
    picture = b.picture
    phone = SITE["phone_display"]
    tel = SITE["phone_href"]

    faqs = [
        ("What does a Smoke Damage Public Adjuster do?",
         "<p>It is a licensed public adjuster hired by the policyholder — not the insurance company — to help with a smoke or fire property claim. We document the damage, review the policy and the carrier's estimate, organize supporting records such as photos, inventories and invoices, prepare the claim presentation and communicate with the insurer on your behalf. We do not perform repairs, cleaning or restoration.</p>"),
        ("Does homeowners insurance cover smoke damage?",
         "<p>Many property policies address smoke damage, but whether a specific loss is covered depends on the policy language, any exclusions or limitations, and the facts of the loss. That is why documentation and a careful policy review matter. See <a href=\"/smoke-damage-claims/\">smoke damage insurance claims</a> for more detail.</p>"),
        ("Can a public adjuster review my claim after the insurance company has already inspected?",
         "<p>Yes. Many people contact us after an inspection, a partial payment, or a denial letter. We can compare the documented conditions with the carrier's estimate and correspondence to see whether items deserve further attention. No result is guaranteed.</p>"),
        ("Do you serve all of Texas?",
         "<p>Yes. As a Texas Smoke Damage Public Adjuster, we represent residential and commercial policyholders statewide — from Houston and Dallas–Fort Worth to Austin, San Antonio, El Paso, the Rio Grande Valley, West Texas and the Panhandle. See our <a href=\"/texas/\">Texas service areas</a>.</p>"),
        ("Do you work for the insurance company?",
         "<p>No. We represent policyholders only. The insurance company has its own adjusters, who work for or on behalf of the insurer. A public adjuster is hired by the insured under a written contract.</p>"),
        ("How are public adjusters paid in Texas?",
         "<p>Public adjusters in Texas are generally paid a percentage of the claim settlement under a written contract, and Texas law regulates both the contract and the compensation. Our <a href=\"/texas-public-adjuster-rules/\">Texas public adjuster rules</a> page explains the requirements in plain English. The initial claim review is free.</p>"),
    ]
    faq_html = "".join(f'<details class="faq-item"><summary><span>{esc(q)}</span></summary><div class="faq-answer">{a}</div></details>' for q, a in faqs)

    complications = [
        ("Smoke migration", "Smoke can move well beyond the room where a fire started — through doorways, hallways, stairwells and gaps in the building."),
        ("Soot deposition", "Fine residue can settle on walls, ceilings, cabinetry and contents in rooms that show little visible damage at first glance."),
        ("Odor", "Persistent odor may point to residue in porous materials, but it needs to be documented and, where appropriate, evaluated by qualified specialists."),
        ("HVAC contamination", "If a system ran during or after the fire, smoke may have been drawn into returns, filters, ductwork and the air handler."),
        ("Attics, insulation & wall cavities", "Smoke and heat can reach concealed spaces that are not visible during a quick walkthrough."),
        ("Cabinetry, flooring & upholstery", "Different materials react differently to heat, soot and odor, which drives cleaning-versus-replacement questions."),
        ("Electronics & appliances", "Residue on and inside electronics raises questions that may need technical input and careful documentation."),
        ("Clothing & contents", "Personal property claims often involve hundreds of items that each need a description, age, condition and value."),
        ("Firefighting water", "Water used to put out the fire can damage drywall, insulation, flooring and contents in addition to the fire itself."),
        ("Temporary living expenses", "When a home is not livable, additional living expenses may be addressed under the policy — records matter."),
        ("Business interruption", "Commercial policies may address lost business income or extra expense, depending on the policy and the facts."),
    ]
    comp_cards = "".join(f'<div class="mini-card"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>' for t, d in complications)

    doc_groups = [
        ("The structure", ["Direct Fire Damage", "Heat Damage", "Smoke Residue", "Soot", "Odor", "Ceilings", "Walls", "Flooring", "Cabinetry", "Insulation", "HVAC Systems", "Fire Suppression Water Damage", "Debris"]),
        ("Contents & property", ["Personal Property", "Furniture", "Clothing", "Electronics", "Business Equipment", "Inventory"]),
        ("Expenses & records", ["Additional Living Expenses", "Commercial Loss Documentation", "Carrier Estimates", "Invoices & Receipts", "Photos & Video", "Correspondence"]),
    ]
    doc_html = "".join(
        f'<div class="doc-group"><h3>{esc(g)}</h3><ul class="doc-grid">' + "".join(f'<li><span class="dot" aria-hidden="true"></span>{esc(x)}</li>' for x in items) + "</ul></div>"
        for g, items in doc_groups)

    claims = [
        ("Residential Smoke Damage", "Houses, condos, townhomes and rental properties affected by smoke, soot and odor.", "/residential-smoke-damage-claims/", "texas-home"),
        ("Commercial Smoke Damage", "Offices, retail, restaurants, warehouses, multifamily, churches and associations.", "/commercial-smoke-damage-claims/", "commercial-fire"),
        ("Fire + Smoke Combination Claims", "Direct flame, heat, smoke, suppression water and debris in one loss.", "/fire-damage-claims/", "burned-house"),
        ("Soot Damage", "Visible and fine residue on surfaces, materials, systems and contents.", "/soot-damage-claims/", "soot-ceiling"),
        ("Contents Claims", "Itemized inventories for furniture, electronics, clothing, inventory and more.", "/smoke-damaged-contents/", "contents-damage"),
        ("HVAC Smoke Damage", "Returns, filters, ductwork, registers and air handlers affected by smoke.", "/hvac-smoke-damage/", "hvac-vent"),
        ("Smoke Odor Claims", "Documenting persistent odor and the materials involved.", "/smoke-odor-claims/", "smoke-hallway"),
        ("Denied Claims", "A structured second look at a denial letter and the claim file.", "/denied-smoke-damage-claims/", "paperwork-review"),
        ("Delayed Claims", "Organizing the file and communication when a claim has stalled.", "/delayed-smoke-damage-claims/", "inspection"),
        ("Underpaid Claims", "Comparing the carrier's estimate with the documented damage.", "/underpaid-smoke-damage-claims/", "adjuster-documenting"),
    ]
    claim_cards = "".join(
        f'<a class="card card-link photo-card" href="{href}"><div class="pc-img">{picture(img, "(min-width: 1100px) 280px, (min-width: 700px) 45vw, 100vw", max_w=800)}</div>'
        f'<div class="pc-body"><span class="num">{i:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="card-more">Learn more →</span></div></a>'
        for i, (t, d, href, img) in enumerate(claims, 1))

    path_steps = [
        ("Fire origin", "Where the fire started — often a kitchen, garage, electrical source or appliance."),
        ("Adjacent room", "Heat and smoke move into the next space through open doors and shared walls."),
        ("Hallway", "Hallways and stairwells can channel smoke toward the rest of the home or building."),
        ("HVAC return", "If the system is running, return vents can draw smoke into the system."),
        ("HVAC system", "Filters, the air handler and ductwork may carry residue through the building."),
        ("Other rooms", "Supply registers can distribute residue and odor to rooms far from the fire."),
        ("Attic & building cavities", "Smoke and heat can reach concealed spaces, insulation and wall cavities."),
        ("Contents", "Furniture, clothing, electronics and stored items may be affected throughout."),
    ]
    path_html = "".join(f'<li><span class="sp-dot">{i:02d}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>' for i, (t, d) in enumerate(path_steps, 1))

    steps = [
        ("Initial Claim Review", "We discuss what happened and where your insurance claim currently stands — no policy or claim number needed to start."),
        ("Property Inspection", "We document observable smoke, soot, fire, contents and related property damage, room by room."),
        ("Policy & Claim File Review", "We review available policy documents, carrier estimates, correspondence, reports, invoices, inventories and supporting records."),
        ("Damage Documentation", "We organize photographs, room-by-room conditions, contents, estimates, invoices, scopes and relevant records."),
        ("Claim Presentation", "We prepare a documented claim position based on the available facts and the policy provisions."),
        ("Carrier Communication", "We communicate and negotiate with the insurer regarding the documented property claim."),
    ]
    steps_html = "".join(f'<li><span class="t-num">{i:02d}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for i, (t, d) in enumerate(steps, 1))

    have = {l["city"]: l["path"] for l in locations}
    city_items = "".join(
        (f'<li><a href="{have[c]}">{esc(c)}</a></li>' if c in have else f"<li><span>{esc(c)}</span></li>") for c in b.MARKETS)

    latest = ""
    items = posts[:3]
    if items:
        cards = "".join(b.post_card(p, f'{esc(p.get("category") or "Guide")} · {b.fmt_date(p["published"])}') for p in items)
        latest = f"""<section class="section"><div class="container">
<div class="section-head"><p class="eyebrow">Resource Center</p><h2>Guides for Texas smoke and fire claims</h2>
<p>Plain-English articles on documentation, coverage questions and the claim process. <a href="/blog/" style="color:var(--orange-deep);font-weight:700">View all articles →</a></p></div>
<div class="post-grid">{cards}</div></div></section>"""

    page = {
        "path": "/",
        "kind": "home",
        "title": "Smoke Damage Public Adjuster | Texas Smoke & Fire Claims",
        "description": "Texas Smoke Damage Public Adjuster representing homeowners and businesses in smoke, soot and fire insurance claims. Free claim review.",
        "h1": "Texas Smoke Damage Public Adjuster Representing Policyholders",
        "image": "hero-fire-house",
        "updated": b.TODAY,
    }
    page["crumbs"] = [("Home", "/")]
    page["schema"] = [
        b.webpage_schema(page),
        {"@type": "Service", "@id": b.url("/") + "#service", "name": "Smoke Damage Public Adjuster",
         "serviceType": "Public adjusting — smoke and fire property insurance claims",
         "provider": {"@id": b.ORG_ID}, "areaServed": {"@type": "State", "name": "Texas"},
         "description": page["description"],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Smoke & fire claim services", "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "url": b.url(h)}} for t, _, h, _ in claims]}},
        b.faq_schema("/", [(q, a) for q, a in faqs]),
    ]
    v = b.IMG_VARIANTS.get("hero-fire-house")
    if v:
        w = [x for x in v["widths"] if x <= 1200]
        page["preload"] = (f'<link rel="preload" as="image" type="image/avif" imagesrcset="' +
                           ", ".join(f"/assets/img/hero-fire-house-{x}.avif {x}w" for x in w) +
                           '" imagesizes="(min-width: 980px) 520px, 100vw" fetchpriority="high">\n')

    main = f"""<section class="hero"><div class="container hero-grid">
<div class="hero-copy">
<p class="eyebrow">Texas Smoke &amp; Fire Claim Specialists</p>
<h1>Texas <span>Smoke Damage</span> Public Adjuster Representing Policyholders</h1>
<p class="hero-lead">Your smoke damage claim deserves a closer look. Smoke Damage Public Adjuster represents Texas homeowners and businesses after smoke and fire property losses — documenting smoke, soot, odor, contents and related fire damage so the claim is presented with organized supporting information. We work for you, not the insurance company.</p>
<div class="btn-row"><a class="btn" href="/contact/" data-cta="home-hero">{SITE['cta_primary']}</a>
<a class="btn btn-outline" href="{tel}" data-loc="home-hero">{icon('phone')}Call {phone}</a></div>
<ul class="proof-list">
<li>Licensed Texas Public Adjusting Company</li>
<li>Residential &amp; Commercial Claims</li>
<li>Serving All of Texas</li>
</ul>
</div>
<div class="hero-visual">
<div class="hero-photo">{picture("hero-fire-house", "(min-width: 980px) 520px, 100vw", eager=True, max_w=1200)}</div>
<span class="hero-tag">Policyholder representation</span>
<div class="license-card"><p class="lc-label">Licensed Texas public adjuster</p><p class="lc-name">{esc(SITE['company'])}</p><p class="lc-num">TDI License #{SITE['license_number']}</p></div>
</div>
</div></section>

<div class="trust-bar"><div class="container">
<ul>
<li>{icon('shield')}Texas Licensed</li>
<li>{icon('user')}Policyholder Representation</li>
<li>{icon('home')}Residential Claims</li>
<li>{icon('building')}Commercial Claims</li>
<li>{icon('map')}Statewide Texas</li>
<li>{icon('flame')}Smoke &amp; Fire Claim Focus</li>
</ul>
<p class="trust-legal">{esc(SITE['company'])} &middot; {esc(SITE['license_label'])}</p>
</div></div>

<section class="section"><div class="container">
<div class="split">
<div class="sticky-col reveal">
<p class="eyebrow">Why smoke claims become complicated</p>
<h2>What you can't easily see can still affect the claim.</h2>
<p>Fire damage is usually obvious. Smoke damage often isn't. Smoke can travel beyond the room where the fire began, settle on surfaces and contents, enter HVAC pathways and create cleaning-or-replacement questions that need careful documentation.</p>
<p>A Smoke Damage Public Adjuster helps organize those details into a documented claim instead of relying only on what is visible during a first walkthrough.</p>
<div class="image-frame" style="aspect-ratio:4/3;margin-top:24px">{picture("smoke-interior", "(min-width: 980px) 460px, 100vw", max_w=1200)}</div>
</div>
<div class="mini-grid reveal">{comp_cards}</div>
</div></div></section>

<section class="section section-dark"><div class="container">
<div class="section-head"><p class="eyebrow">What we document</p>
<h2>Build the claim around evidence — not assumptions.</h2>
<p>As your Smoke Damage Public Adjuster, we document the property, the contents and the expenses tied to the loss, then organize everything so the carrier can see what was affected and why.</p></div>
<div class="doc-groups">{doc_html}</div>
</div></section>

<section class="section"><div class="container">
<div class="section-head"><p class="eyebrow">Claims we handle</p>
<h2>Smoke Damage Public Adjuster services for every part of the loss</h2>
<p>SmokeDamage.com is built around one specialty: helping policyholders with smoke and fire-related property insurance claims — from the first report to an underpaid or denied claim.</p></div>
<div class="claims-grid">{claim_cards}</div>
</div></section>

<section class="section section-white"><div class="container">
<div class="path-wrap">
<div class="reveal">
<p class="eyebrow">Smoke damage is not always obvious</p>
<h2>How smoke can travel through a property</h2>
<p>Smoke doesn't always stay where the fire was. Depending on the event, it may follow a path like the one below. Not every fire affects every area — the extent of damage depends on the specific event and has to be evaluated and documented.</p>
<ol class="smoke-path">{path_html}</ol>
</div>
<figure class="house-diagram reveal">{HOUSE_SVG}<figcaption>Illustration only. The actual extent of smoke and soot damage depends on the fire, the building, ventilation, HVAC operation and how quickly the property was secured.</figcaption></figure>
</div></div></section>

<section class="section"><div class="container">
<div class="section-head"><p class="eyebrow">The claim process</p>
<h2>A clear path from first call to claim presentation</h2>
<p>Every claim is different, but the work follows the same disciplined steps. <a href="/smoke-damage-claim-process/" style="color:var(--orange-deep);font-weight:700">See the full claim process →</a></p></div>
<ol class="timeline-h">{steps_html}</ol>
</div></section>

<section class="section section-sand"><div class="container">
<div class="section-head center"><p class="eyebrow">Insurance companies have adjusters</p>
<h2>Who does each adjuster work for?</h2>
<p>Both roles are part of the claim process. The difference is who they represent.</p></div>
<div class="compare">
<div class="compare-col"><span class="tag">Insurance company adjuster</span>
<h3>Works for or on behalf of the insurance company.</h3>
<ul><li>May be a staff adjuster, an independent adjuster or a firm hired by the carrier.</li>
<li>Investigates and evaluates the claim for the insurer.</li>
<li>Prepares the carrier's estimate and communicates the carrier's position.</li></ul></div>
<div class="compare-col us"><span class="tag">Public adjuster</span>
<h3>Is hired by the policyholder to assist with the property insurance claim.</h3>
<ul><li>Licensed by the Texas Department of Insurance and bound by Texas rules on contracts and fees.</li>
<li>Documents the loss, reviews the policy and prepares the claim presentation for the insured.</li>
<li>Communicates and negotiates with the insurer on the policyholder's behalf.</li></ul></div>
</div>
<p style="text-align:center;margin-top:26px">Public adjusters are not attorneys and do not give legal advice. <a href="/texas-public-adjuster-rules/" style="color:var(--orange-deep);font-weight:700">How Texas regulates public adjusters →</a></p>
</div></section>

<section class="section"><div class="container">
<div class="section-head"><p class="eyebrow">Free claim tools</p><h2>Get organized before the claim review</h2>
<p>Two free tools help you see what to document and how contents values are usually organized. They're organizational aids — not settlement or coverage calculators.</p></div>
<div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(min(100%,420px),1fr))">
<a class="card card-link photo-card" href="/tools/smoke-damage-scope-calculator/"><div class="pc-img">{picture("inspection", "(min-width: 1000px) 560px, 100vw", max_w=1200)}</div><div class="pc-body"><h3>Smoke Damage Scope Calculator</h3><p>Answer a few questions about the fire and get a customized list of areas to document, records to gather and questions to discuss.</p><span class="card-more">Build my documentation scope →</span></div></a>
<a class="card card-link photo-card" href="/tools/contents-rcv-acv-calculator/"><div class="pc-img">{picture("contents-inventory", "(min-width: 1000px) 560px, 100vw", max_w=1200)}</div><div class="pc-body"><h3>Contents RCV / ACV Calculator</h3><p>Build a line-item contents inventory with replacement cost, estimated depreciation and estimated ACV — then export it to CSV or PDF.</p><span class="card-more">Start my inventory →</span></div></a>
</div></div></section>

<section class="section section-white"><div class="container tx-wrap">
<div class="tx-map reveal">{b.texas_map_svg(locations)}</div>
<div>
<p class="eyebrow">Texas statewide</p>
<h2>A Texas Smoke Damage Public Adjuster for the whole state</h2>
<p>From Gulf Coast refineries and Houston-area neighborhoods to Hill Country homes, Panhandle ranches and El Paso businesses, we represent policyholders with smoke and fire claims in every corner of Texas.</p>
<ul class="city-cloud">{city_items}</ul>
<h3 style="font-size:1.35rem">Need Help With a Smoke Damage Claim Anywhere in Texas?</h3>
<div class="btn-row"><a class="btn" href="{tel}" data-loc="home-texas">{icon('phone')}Call {phone}</a><a class="btn btn-outline" href="/texas/">View Texas service areas</a></div>
</div>
</div></section>

<section class="section"><div class="container split reverse">
<div>
<p class="eyebrow">How we work</p>
<h2>Documentation first. Clear communication throughout.</h2>
<p>We don't publish testimonials we can't verify or promise results no one can promise. What we can tell you is how we approach every smoke and fire claim:</p>
<div class="mini-grid" style="margin-top:22px">
<div class="mini-card"><h3>We represent you</h3><p>Our only client in the claim is the policyholder.</p></div>
<div class="mini-card"><h3>We don't do repairs</h3><p>We don't clean, remediate, demolish or rebuild property on claims we adjust.</p></div>
<div class="mini-card"><h3>We show our work</h3><p>Room-by-room documentation, organized records and a written claim presentation.</p></div>
<div class="mini-card"><h3>We explain the policy</h3><p>What the carrier's estimate includes, what it leaves out, and what the policy says.</p></div>
</div>
</div>
<div class="image-frame" style="aspect-ratio:4/3.2">{picture("adjuster-documenting", "(min-width: 980px) 560px, 100vw", max_w=1200)}</div>
</div></section>

{latest}

<section class="section section-white"><div class="container-narrow">
<div class="section-head center"><p class="eyebrow">FAQ</p><h2>Questions about working with a Smoke Damage Public Adjuster</h2></div>
<div class="faq-list">{faq_html}</div>
<p style="text-align:center"><a href="/faq/" style="color:var(--orange-deep);font-weight:700">See all smoke and fire claim FAQs →</a></p>
</div></section>

<section class="section section-sand cta-final"><div class="container">
<p class="eyebrow">Free Claim Review</p>
<h2>Talk with a Texas Smoke Damage Public Adjuster about your claim</h2>
<p>Tell us what happened and where the claim stands. We'll review it with you and explain whether and how we may be able to help. No policy or claim number is needed to start.</p>
<div class="btn-row"><a class="btn" href="/contact/" data-cta="home-final">{SITE['cta_primary']}</a>
<a class="btn btn-dark" href="{tel}" data-loc="home-final">{icon('phone')}Call {phone}</a></div>
</div></section>"""
    b.write("/", b.render_page(page, main, current="/"))
    page["words"] = b.word_count(main)
    b.register(page)
