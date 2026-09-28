"""Tools section: /tools/, Smoke Damage Scope Calculator, Contents RCV/ACV Calculator."""

import html


def esc(s):
    return html.escape(str(s), quote=True)


SCOPE_DISCLAIMER = ("This tool provides general organizational information only. It is not a coverage determination, "
                    "a remediation recommendation, a health assessment, a structural assessment, a damage valuation, or legal advice.")
CONTENTS_DISCLAIMER = ("This calculator is an organizational and estimating tool. Your insurance policy and carrier's applicable "
                       "claim evaluation determine how replacement cost, depreciation, and actual cash value are handled.")


def radio_group(name, label, options, num, required=False):
    opts = "".join(f'<label class="chip"><input type="radio" name="{name}" value="{esc(o)}"{" required" if required and i == 0 else ""}><span>{esc(o)}</span></label>'
                   for i, o in enumerate(options))
    return f'<fieldset class="q-block"><legend><span class="q-num">{num:02d}</span>{esc(label)}</legend><div class="chips">{opts}</div></fieldset>'


def build(b):
    SITE = b.SITE

    # ------------------------------------------------------------------ /tools/
    idx = {"path": "/tools/", "title": "Smoke & Fire Claim Tools | Free Calculators",
           "description": "Free tools for Texas smoke and fire claims: a documentation scope calculator and a contents replacement cost and depreciation calculator.",
           "h1": "Smoke & Fire Claim Tools", "eyebrow": "Free Tools", "image": "contents-inventory", "kind": "tool",
           "crumbs": [("Home", "/"), ("Tools", "/tools/")], "updated": b.TODAY,
           "lead_html": "Two free, private tools to help you organize a smoke or fire claim before your claim review. Nothing you enter is sent to us unless you choose to send it."}
    idx["schema"] = [b.webpage_schema(idx, "CollectionPage"), b.breadcrumb_schema(idx["crumbs"]),
                     {"@type": "ItemList", "@id": b.url("/tools/") + "#tools", "itemListElement": [
                         {"@type": "ListItem", "position": 1, "url": b.url("/tools/smoke-damage-scope-calculator/"), "name": "Smoke Damage Scope Calculator"},
                         {"@type": "ListItem", "position": 2, "url": b.url("/tools/contents-rcv-acv-calculator/"), "name": "Contents Replacement Cost & Depreciation Calculator"}]}]
    cards = f"""<div class="card-grid" style="grid-template-columns:repeat(auto-fill,minmax(min(100%,440px),1fr))">
<a class="card card-link photo-card" href="/tools/smoke-damage-scope-calculator/"><div class="pc-img">{b.picture("inspection", "(min-width: 1000px) 560px, 100vw", max_w=1200)}</div>
<div class="pc-body"><h2 style="font-size:1.4rem">Smoke Damage Scope Calculator</h2><p>Answer questions about the property, the fire and where the claim stands. Get a customized list of areas to document, records to gather and questions for your claim review. Print it, save it as a PDF or email it to yourself.</p><span class="card-more">Open the scope calculator →</span></div></a>
<a class="card card-link photo-card" href="/tools/contents-rcv-acv-calculator/"><div class="pc-img">{b.picture("contents-inventory", "(min-width: 1000px) 560px, 100vw", max_w=1200)}</div>
<div class="pc-body"><h2 style="font-size:1.4rem">Contents RCV / ACV Calculator</h2><p>Build an unlimited line-item contents inventory with quantity, age, condition, replacement cost, estimated depreciation and estimated actual cash value. Export to CSV or save as a PDF.</p><span class="card-more">Open the contents calculator →</span></div></a>
</div>
<div class="prose" style="max-width:820px;margin-top:40px">
<h2>What these tools are — and aren't</h2>
<p>Both tools are organizational aids. They help you see what may need to be documented and keep a contents inventory in a consistent format. They do not tell you what your policy covers, what your insurer owes, or how any item should be cleaned or replaced.</p>
<p>When you're ready, bring the results to a <a href="/contact/">free claim review</a>, or read more about <a href="/smoke-damage-claims/">smoke damage insurance claims</a> and <a href="/smoke-damaged-contents/">smoke-damaged contents</a>.</p>
</div>"""
    main = b.page_hero(idx) + f'<section class="section-sm"><div class="container">{cards}</div></section>' + b.final_cta()
    b.write(idx["path"], b.render_page(idx, main))
    b.register(idx)

    # --------------------------------------------------------- scope calculator
    sc = {"path": "/tools/smoke-damage-scope-calculator/", "title": "Smoke Damage Scope Calculator | Free Claim Tool",
          "description": "Free Smoke Damage Scope Calculator: see which areas, records and questions to document after a smoke or fire loss in Texas.",
          "h1": "Smoke Damage Scope Calculator", "eyebrow": "Free Tool", "kind": "tool", "image": None,
          "crumbs": [("Home", "/"), ("Tools", "/tools/"), ("Smoke Damage Scope Calculator", "/tools/smoke-damage-scope-calculator/")],
          "updated": b.TODAY,
          "lead_html": "Answer a few questions about the property and the fire. You'll get a customized Smoke Damage Documentation Scope: areas to document, records to gather and questions to discuss during your claim review. This is not a settlement calculator."}
    sc["schema"] = [b.webpage_schema(sc), b.breadcrumb_schema(sc["crumbs"]),
                    {"@type": "WebApplication", "@id": b.url(sc["path"]) + "#app", "name": "Smoke Damage Scope Calculator",
                     "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
                     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": b.ORG_ID},
                     "description": sc["description"]}]
    q = 0
    def nq():
        nonlocal q
        q += 1
        return q
    qs = [
        radio_group("ptype", "Property type", ["Single-family home", "Condo", "Townhome", "Apartment / rental", "Multifamily", "Office", "Retail", "Restaurant", "Warehouse", "Commercial", "Other"], nq()),
        f'<div class="q-block field"><label class="q" for="s-size"><span class="q-num">{nq():02d}</span>Approximate property size (sq ft)</label><input id="s-size" name="size" type="number" min="0" step="50" inputmode="numeric" placeholder="e.g. 2,200" style="max-width:260px"></div>',
        f'<div class="q-block field"><label class="q" for="s-rooms"><span class="q-num">{nq():02d}</span>Number of affected rooms or areas</label><input id="s-rooms" name="rooms" type="number" min="0" max="500" inputmode="numeric" placeholder="e.g. 6" style="max-width:260px"></div>',
        radio_group("origin", "Where did the fire start?", ["Kitchen", "Garage", "Bedroom", "Living area", "Attic", "Electrical", "Fireplace", "Appliance", "Neighboring property", "Wildfire / exterior smoke", "Unknown", "Other"], nq()),
        radio_group("flame", "Was there direct flame damage?", ["Yes", "No", "Unsure"], nq()),
        radio_group("soot", "Visible soot?", ["None", "Light", "Moderate", "Heavy", "Unsure"], nq()),
        radio_group("odor", "Smoke odor?", ["None", "Light", "Moderate", "Heavy", "Unsure"], nq()),
        radio_group("hvac", "Was the HVAC system operating during or after the fire?", ["Yes", "No", "Unsure"], nq()),
        radio_group("vents", "Visible residue around vents or registers?", ["Yes", "No", "Unsure"], nq()),
        radio_group("contents", "Contents affected?", ["None", "Some", "Many", "Most", "Unsure"], nq()),
        radio_group("water", "Water from fire suppression (firefighting or sprinklers)?", ["Yes", "No", "Unsure"], nq()),
        radio_group("status", "Where does the claim stand right now?", ["Not yet reported", "New claim", "Already inspected", "Partially paid", "Denied", "Delayed", "Underpaid", "Closed", "Unsure"], nq()),
    ]
    main = b.page_hero(sc, img=False, buttons=False) + f"""<section class="tool-shell"><div class="container tool-grid">
<div>
<form class="tool-card" id="scope-form" novalidate>
<h2>Tell us about the loss</h2>
<p>Answer what you can — "Unsure" is fine. Your answers stay in your browser.</p>
{''.join(qs)}
<div class="btn-row" style="margin-top:18px"><button class="btn" type="submit">Build my documentation scope</button><button class="btn btn-outline" type="reset">Start over</button></div>
</form>
<div class="result-panel" id="scope-result" hidden tabindex="-1" aria-live="polite"></div>
</div>
<aside class="sidebar no-print"><div class="sidebar-sticky">
<div class="disclaimer-box"><strong>Important</strong>{esc(SCOPE_DISCLAIMER)}</div>
<div class="side-card dark"><h3>Prefer to talk it through?</h3><p>A licensed Texas public adjuster can walk through the scope with you.</p>
<a class="btn" href="/contact/?source=scope-calculator" data-cta="scope-sidebar">{SITE['cta_primary']}</a>
<a class="btn btn-ghost-light" href="{SITE['phone_href']}" data-loc="scope-sidebar">{b.icon('phone')}{SITE['phone_display']}</a></div>
<div class="side-card"><h3>Related</h3><ul class="related-list">
<li><a href="/smoke-damage-claims/">Smoke Damage Insurance Claims</a></li>
<li><a href="/hvac-smoke-damage/">HVAC Smoke Damage</a></li>
<li><a href="/smoke-damaged-contents/">Smoke-Damaged Contents</a></li>
<li><a href="/tools/contents-rcv-acv-calculator/">Contents RCV / ACV Calculator</a></li></ul></div>
</div></aside>
</div></section>
<section class="section-sm section-white"><div class="container-narrow prose">
<h2>How the Smoke Damage Scope Calculator works</h2>
<p>The calculator uses your answers to highlight the building areas, systems, contents and expense categories that commonly need attention after a smoke or fire event with similar characteristics — for example, HVAC components when the system was running, or suppression-water damage when firefighters used water. It does not inspect your property, decide what is damaged or determine what is covered.</p>
<p>Use the results as a checklist while you take photos and gather records, and as a starting point for a conversation with your Smoke Damage Public Adjuster or your insurer. The extent of any smoke damage depends on the specific event and needs to be evaluated and documented on site.</p>
<p class="disclaimer-box"><strong>Disclaimer</strong>{esc(SCOPE_DISCLAIMER)}</p>
</div></section>"""
    sc["scripts"] = f'<script src="/assets/js/scope.js?v={b.ASSET_V}" defer></script>'
    sc["words"] = b.word_count(main)
    b.write(sc["path"], b.render_page(sc, main))
    b.register(sc)

    # ------------------------------------------------------- contents calculator
    cc = {"path": "/tools/contents-rcv-acv-calculator/", "title": "Contents RCV & ACV Calculator | Depreciation Tool",
          "description": "Free contents replacement cost and depreciation calculator. Build a line-item inventory with RCV, depreciation and estimated ACV.",
          "h1": "Contents Replacement Cost & Depreciation Calculator", "eyebrow": "Free Tool · Contents RCV / ACV", "kind": "tool", "image": None,
          "crumbs": [("Home", "/"), ("Tools", "/tools/"), ("Contents RCV / ACV Calculator", "/tools/contents-rcv-acv-calculator/")],
          "updated": b.TODAY,
          "lead_html": "Build a line-item inventory of smoke- or fire-damaged personal property. The calculator totals Replacement Cost Value (RCV), your estimated depreciation and the resulting estimated Actual Cash Value (ACV). Your list is saved in this browser only."}
    cc["schema"] = [b.webpage_schema(cc), b.breadcrumb_schema(cc["crumbs"]),
                    {"@type": "WebApplication", "@id": b.url(cc["path"]) + "#app", "name": "Contents Replacement Cost & Depreciation Calculator",
                     "applicationCategory": "FinanceApplication", "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
                     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "provider": {"@id": b.ORG_ID},
                     "description": cc["description"]}]
    cats = ["Furniture", "Electronics", "Appliances", "Clothing", "Linens & bedding", "Books & media", "Artwork & decor",
            "Collectibles", "Kitchenware", "Children's items", "Office equipment", "Business inventory", "Tools & equipment",
            "Stored property", "Personal care", "Sports & outdoor", "Other"]
    cat_opts = "".join(f'<option value="{esc(c)}">{esc(c)}</option>' for c in cats)
    main = b.page_hero(cc, img=False, buttons=False) + f"""<section class="tool-shell"><div class="container">
<div class="disclaimer-box no-print" style="margin-bottom:22px"><strong>Please read</strong>{esc(CONTENTS_DISCLAIMER)} Calculated ACV is not necessarily what an insurer owes — policies, depreciation methods, recoverable depreciation, limits, exclusions and settlement provisions differ.</div>
<div class="tool-card">
<div class="print-only"><h2>Contents Inventory — Smoke Damage Public Adjuster Worksheet</h2><p id="print-date"></p></div>
<div class="calc-toolbar no-print">
<div class="btn-row"><button class="btn btn-sm" type="button" id="add-row">+ Add item</button>
<button class="btn btn-sm btn-outline" type="button" id="export-csv">Export CSV</button>
<button class="btn btn-sm btn-outline" type="button" id="print-list">Print / Save PDF</button>
<button class="btn btn-sm btn-outline" type="button" id="clear-all">Clear list</button></div>
<div class="btn-row"><div class="field"><label class="sr-only" for="filter">Search items</label><input id="filter" type="search" placeholder="Search items…"></div>
<div class="field"><label class="sr-only" for="sort">Sort</label><select id="sort"><option value="">Sort: as entered</option><option value="category">Sort by category</option><option value="rcv">Sort by RCV (high → low)</option><option value="item">Sort by item name</option></select></div></div>
</div>
<div class="calc-table-wrap"><table class="calc-table" id="calc-table">
<caption class="sr-only">Contents inventory line items</caption>
<thead><tr><th scope="col">Item</th><th scope="col">Category</th><th scope="col">Brand</th><th scope="col">Model</th><th scope="col">Qty</th><th scope="col">Age (yrs)</th><th scope="col">Pre-loss condition</th><th scope="col">Replacement cost / item ($)</th><th scope="col">Est. depreciation %</th><th scope="col">Sales tax %</th><th scope="col">RCV</th><th scope="col">Est. depreciation</th><th scope="col">Est. ACV</th><th scope="col">Notes</th><th scope="col" class="no-print"><span class="sr-only">Actions</span></th></tr></thead>
<tbody id="rows"></tbody></table></div>
<template id="row-tpl"><tr>
<td><input data-k="item" aria-label="Item" maxlength="120"></td>
<td><select data-k="category" aria-label="Category">{cat_opts}</select></td>
<td><input data-k="brand" aria-label="Brand" maxlength="60"></td>
<td><input data-k="model" aria-label="Model" maxlength="60"></td>
<td><input data-k="qty" aria-label="Quantity" type="number" min="0" step="1" value="1" inputmode="numeric" style="width:64px"></td>
<td><input data-k="age" aria-label="Approximate age in years" type="number" min="0" step="0.5" inputmode="decimal" style="width:74px"></td>
<td><select data-k="condition" aria-label="Pre-loss condition"><option>New</option><option>Excellent</option><option selected>Good</option><option>Fair</option><option>Poor</option></select></td>
<td><input data-k="cost" aria-label="Estimated replacement cost per item in dollars" type="number" min="0" step="0.01" inputmode="decimal" style="width:110px"></td>
<td><input data-k="dep" aria-label="Estimated depreciation percent" type="number" min="0" max="100" step="1" inputmode="decimal" style="width:74px"></td>
<td><input data-k="tax" aria-label="Sales tax percent if applicable" type="number" min="0" max="20" step="0.001" inputmode="decimal" style="width:84px"></td>
<td class="num-out" data-out="rcv">$0.00</td><td class="num-out" data-out="depamt">$0.00</td><td class="num-out" data-out="acv">$0.00</td>
<td><input data-k="notes" aria-label="Notes" maxlength="300"></td>
<td class="no-print"><div class="row-actions"><button type="button" class="icon-btn" data-act="dup" title="Duplicate item">Copy</button><button type="button" class="icon-btn" data-act="del" title="Remove item">✕</button></div></td>
</tr></template>
<div class="totals" aria-live="polite">
<div class="total-box"><small>Items / quantity</small><strong id="t-count">0</strong></div>
<div class="total-box"><small>Total Replacement Cost (RCV)</small><strong id="t-rcv">$0.00</strong></div>
<div class="total-box"><small>Total Estimated Depreciation</small><strong id="t-dep">$0.00</strong></div>
<div class="total-box dark"><small>Total Estimated ACV</small><strong id="t-acv">$0.00</strong></div>
</div>
<p class="consent" style="margin-top:14px">RCV = quantity × replacement cost per item (plus sales tax if entered). Estimated depreciation = RCV × your depreciation %. Estimated ACV = RCV − estimated depreciation. {esc(CONTENTS_DISCLAIMER)}</p>
</div>
<div class="cta-banner no-print"><div><p class="cta-title">Want a second set of eyes on your contents claim?</p><p>Bring your inventory to a free claim review with a licensed Texas public adjuster.</p></div>
<div class="btn-row"><a class="btn" href="/contact/?source=contents-calculator&amp;damage=Contents" data-cta="contents-calc">{SITE['cta_primary']}</a><a class="btn btn-outline" href="{SITE['phone_href']}" data-loc="contents-calc">{b.icon('phone')}Call {SITE['phone_display']}</a></div></div>
</div></section>
<section class="section-sm section-white"><div class="container-narrow prose">
<h2>RCV, depreciation and ACV in plain English</h2>
<p><strong>Replacement Cost Value (RCV)</strong> is what it would cost to replace an item with a new one of like kind and quality today. <strong>Depreciation</strong> is a reduction for age, wear and condition. <strong>Actual Cash Value (ACV)</strong> is generally described as replacement cost minus depreciation — but how ACV is calculated, and whether depreciation is later recoverable, depends on your policy and the carrier's claim evaluation.</p>
<p>The depreciation percentage in this calculator is <em>your</em> estimate. Insurers may use different depreciation methods, useful-life tables or condition adjustments, and some policies pay ACV first and release withheld depreciation after items are replaced. Read more in <a href="/smoke-damaged-contents/">smoke-damaged contents</a> and <a href="/smoke-damage-claims/">smoke damage insurance claims</a>, or <a href="/contact/">request a free claim review</a>.</p>
<h3>Tips for a stronger inventory</h3>
<ul><li>Go room by room, and include closets, cabinets, drawers, the garage and storage areas.</li>
<li>Record brand and model wherever you can — photos of labels and serial plates help.</li>
<li>Look for proof of ownership and cost: receipts, credit card and bank statements, online order histories, warranty registrations, photos and videos.</li>
<li>Use current replacement pricing for like kind and quality, and note where you found it.</li>
<li>Don't throw items away before they are documented and you understand the carrier's process.</li></ul>
<p class="disclaimer-box"><strong>Disclaimer</strong>{esc(CONTENTS_DISCLAIMER)}</p>
</div></section>"""
    cc["scripts"] = f'<script src="/assets/js/contents.js?v={b.ASSET_V}" defer></script>'
    cc["words"] = b.word_count(main)
    b.write(cc["path"], b.render_page(cc, main))
    b.register(cc)
