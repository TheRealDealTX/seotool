"""Homepage. build(g) receives build.py's globals so it can use the shared
layout helpers without a circular import."""

from siteconfig import BIZ, TOOLS, MATERIALS, TEXAS_REGIONS, US_REGIONS

TITLE = "Free Roof Estimate Calculators & Pro Roof Estimates | Roof Estimate Pro"
DESCRIPTION = ("Free roof estimate calculators with Texas 2026 pricing: replacement cost, squares, materials and "
               "insurance claims. Plus pro line-item roof estimates statewide.")

FAQS = [
    ("Are the roof estimate calculators really free?",
     "<p>Yes. All twelve tools are free to use with no sign-up. Your inputs are saved in your own browser so you can "
     "come back to them, and you can print, save as PDF or share any estimate by link.</p>"),
    ("How accurate are the calculators?",
     "<p>They are built the way an estimator prices a job, with line items, waste, labor adjustments for pitch and height, "
     "and regional pricing for Texas. With good measurements most results land within 10–15% of a professional bid. "
     "Every unit price is editable, so contractors can use their own costs.</p>"),
    ("Do you only work in Texas?",
     "<p>Texas is our home market and we cover every region of the state, from DFW and Houston to the Valley and the "
     "Panhandle. We also prepare estimates for properties in other states. Send us the address and we will confirm.</p>"),
    ("What does a professional estimate cost?",
     f"<p>A claim estimate review is ${BIZ['price_claim_review']} per claim and a professional scope of damages is "
     f"${BIZ['price_scope']}. Full line-item estimates are quoted per project based on size and complexity. "
     "<a href=\"/get-estimate/\">Send us the details</a> for a price.</p>"),
    ("Who uses Roof Estimate Pro?",
     "<p>Roofing contractors who need estimates and supplements written, public adjusters and desk adjusters who need a "
     "second set of eyes on a claim, and homeowners and property managers who want to know what a roof should cost "
     "before they talk to a contractor or an insurer.</p>"),
]


def _quick(g):
    mats = "".join(f'<option value="{m["key"]}"{" selected" if m["key"] == "arch" else ""}>{m["name"]}</option>'
                   for m in MATERIALS)
    regs = "".join(f'<option value="{r["key"]}">Texas — {r["name"]}</option>' for r in TEXAS_REGIONS)
    regs += "".join(f'<option value="{r["key"]}">{r["name"].split(" (")[0]}</option>' for r in US_REGIONS)
    pitches = "".join(f'<option value="{p}"{" selected" if p == 6 else ""}>{p}/12</option>' for p in (3, 4, 5, 6, 7, 8, 9, 10, 12))
    icon = g["icon"]
    return f"""<div class="glass quick" id="quick-est" data-reveal style="--d:.15s">
  <svg class="roof-art" viewBox="0 0 160 110" fill="none" stroke="#FCBE8E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M10 70 L80 18 L150 70"/><path d="M26 58 V100 H134 V58"/><path d="M68 100 V78 H92 V100"/>
    <path d="M80 18 V8 M60 4 H100" stroke="#9fd9d5" stroke-dasharray="3 4"/><path d="M8 104 H152" stroke="#9fd9d5"/>
  </svg>
  <div class="quick-head"><h2>Quick roof estimate</h2><span class="live-dot">Live</span></div>
  <div class="q-row"><label for="q-area">Home size (living area) <span class="q-val" id="q-area-out">2,200 sq ft</span></label>
    <input type="range" id="q-area" min="800" max="6000" step="50" value="2200"></div>
  <div class="grid" style="grid-template-columns:1fr 1fr;gap:12px">
    <div class="q-row"><label for="q-stories">Stories</label><select id="q-stories"><option value="1">1 story</option><option value="2">2 stories</option><option value="3">3 stories</option></select></div>
    <div class="q-row"><label for="q-pitch">Roof pitch</label><select id="q-pitch">{pitches}</select></div>
  </div>
  <div class="q-row"><label for="q-mat">Material</label><select id="q-mat">{mats}</select></div>
  <div class="q-row"><label for="q-region">Location</label><select id="q-region">{regs}</select></div>
  <div class="quick-out" aria-live="polite"><small>Estimated replacement cost</small><div class="big">$0</div><small class="sq">—</small></div>
  <div class="quick-foot"><a href="/tools/roof-replacement-cost-calculator/">Get the itemized estimate {icon('arrow')}</a>
    <a href="/get-estimate/">Ask an estimator {icon('arrow')}</a></div>
</div>"""


def build(g):
    icon, tool_card, post_card = g["icon"], g["tool_card"], g["post_card"]
    page = {"path": "/", "title": TITLE, "description": DESCRIPTION,
            "preload": ""}
    page["schema"] = [g["webpage_schema"](page), g["faq_schema"](FAQS, "/"),
                      {"@type": "ItemList", "@id": g["url"]("/#tools"), "name": "Free roof estimating tools",
                       "itemListElement": [{"@type": "ListItem", "position": i, "url": g["url"](f"/tools/{t['slug']}/"),
                                            "name": t["name"]} for i, t in enumerate(TOOLS, 1)]}]

    hero = f"""<section class="hero hero-home">{g['hero_bg']()}
  <div class="wrap">
    <div data-reveal>
      <a class="eyebrow-pill" href="/tools/"><b>NEW</b> 12 free roof estimating tools {icon('arrow')}</a>
      <h1>Roof estimates you can <span class="grad-text">check, trust and use.</span></h1>
      <p class="lede">Free calculators for replacement cost, squares, pitch, materials, insurance claims and more, loaded with
      Texas 2026 pricing. When you need a line-item estimate in the format carriers use, our estimators build it for you.</p>
      <div class="btn-row" style="margin-top:28px">
        <a class="btn btn--peach" href="/tools/roof-replacement-cost-calculator/">Start the cost calculator {icon('arrow')}</a>
        <a class="btn btn--ghost-light" href="/get-estimate/">Talk to an estimator</a>
      </div>
      <ul class="hero-badges">
        <li>{icon('check')}Free, no sign-up</li><li>{icon('check')}All of Texas + other states</li><li>{icon('check')}Claim reviews from ${BIZ['price_claim_review']}</li>
      </ul>
    </div>
    {_quick(g)}
  </div>
</section>"""

    tools = f"""<section class="section section--paper" id="tools"><div class="wrap">
  <div class="section-head" data-reveal><span class="kicker">Free tools</span><h2>Every calculator a roof estimate needs</h2>
    <p>Measure it, price it, order it, and check what insurance should pay. Each tool shows its math and lets you edit the unit prices.</p></div>
  <div class="grid grid--3">{''.join(tool_card(t) for t in TOOLS)}</div>
</div></section>"""

    n_sys = len(MATERIALS) + 8
    stats = f"""<section class="section section--dark section--tight"><div class="wrap">
  <div class="stats" data-reveal>
    <div class="stat"><b><span data-count="{len(TOOLS)}">{len(TOOLS)}</span></b><span>free calculators</span></div>
    <div class="stat"><b><span data-count="{n_sys}">{n_sys}</span></b><span>roofing systems priced</span></div>
    <div class="stat"><b><span data-count="254">254</span></b><span>Texas counties covered</span></div>
    <div class="stat"><b><em>$</em>0</b><span>to use any tool</span></div>
  </div>
</div></section>"""

    paths = f"""<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><span class="kicker">Two ways to get your number</span><h2>Do it yourself, or hand it to a pro</h2>
    <p>The tools are complete enough to estimate a roof on their own. When the number has to stand up to a carrier, a bank or a client, send it to us.</p></div>
  <div class="grid grid--2">
    <div class="card" data-reveal><span class="ico">{icon('calc')}</span><h3>Use the free tools</h3>
      <p>For contractors pricing a bid, homeowners sanity-checking a quote, and adjusters running a quick number.</p>
      <ul class="check-list" style="margin-top:18px">
        <li>Itemized results with Texas regional pricing</li><li>Edit every unit price to match your costs</li>
        <li>Print, save as PDF or share a link</li><li>Inputs saved in your browser, no account needed</li></ul>
      <a class="btn btn--ghost" href="/tools/">Browse the tools {icon('arrow')}</a></div>
    <div class="card card--dark" data-reveal style="--d:.08s"><span class="ico">{icon('hardhat')}</span><h3>Get a professional estimate</h3>
      <p>Line-item roof estimates built from scratch from your photos, measurement reports and carrier paperwork.</p>
      <ul class="check-list" style="margin-top:18px;color:#d6e2e0">
        <li>Residential and commercial roofs</li><li>Claim estimate review: <b style="color:#fff">${BIZ['price_claim_review']}</b> per claim</li>
        <li>Scope of damages: <b style="color:#fff">${BIZ['price_scope']}</b> per property</li><li>Texas-wide, plus other states</li></ul>
      <a class="btn btn--peach" href="/get-estimate/">Request an estimate {icon('arrow')}</a></div>
  </div>
</div></section>"""

    who = f"""<section class="section section--paper"><div class="wrap">
  <div class="section-head" data-reveal><span class="kicker">Who it's for</span><h2>Built for everyone who prices a roof</h2></div>
  <div class="grid grid--4">
    <div class="card" data-reveal><span class="ico">{icon('hardhat')}</span><h3>Roofing contractors</h3><p>Bid faster with takeoffs and job costing, or send us the estimates and supplements you don't have time to write.</p></div>
    <div class="card" data-reveal style="--d:.06s"><span class="ico">{icon('briefcase')}</span><h3>Public &amp; desk adjusters</h3><p>Check carrier estimates line by line, run depreciation and ACV, and order a scope when you need one fast.</p></div>
    <div class="card" data-reveal style="--d:.12s"><span class="ico">{icon('house')}</span><h3>Homeowners</h3><p>Know what a fair roof price looks like, and what your claim should pay, before you sign anything.</p></div>
    <div class="card" data-reveal style="--d:.18s"><span class="ico">{icon('building')}</span><h3>Property managers</h3><p>Budget flat and commercial roofs, compare restoration to replacement, and get estimates for every building.</p></div>
  </div>
</div></section>"""

    steps = f"""<section class="section"><div class="wrap">
  <div class="split">
    <div data-reveal>
      <span class="kicker">Professional estimates</span>
      <h2>Estimates that hold up when someone checks them</h2>
      <p class="lede">We build every estimate from measurements and photos, item by item, the way carriers and appraisers
      expect to see it: quantities you can verify, the code items that apply, and nothing padded.</p>
      <div class="steps" style="grid-template-columns:1fr 1fr;margin-top:26px">
        <div class="step"><h3>Send the details</h3><p>Address, photos, measurement report or carrier estimate. Upload or email.</p></div>
        <div class="step"><h3>We measure &amp; scope</h3><p>An estimator reviews the roof and confirms the scope with you.</p></div>
        <div class="step"><h3>Line-item estimate</h3><p>Quantities, materials, labor, code items and O&amp;P, ready to submit.</p></div>
        <div class="step"><h3>Revisions</h3><p>Questions from the carrier or client? We walk through the estimate with you.</p></div>
      </div>
      <p style="margin-top:22px"><a class="btn" href="/how-it-works/">How it works {icon('arrow')}</a></p>
    </div>
    <div data-reveal style="--d:.1s">{g['sample_sheet']()}</div>
  </div>
</div></section>"""

    region_chips = "".join(f'<li>{r["name"]}</li>' for r in TEXAS_REGIONS)
    texas = f"""<section class="section section--dark"><div class="wrap">
  <div class="split">
    <div data-reveal>
      <span class="kicker">Texas first</span>
      <h2>Every corner of Texas, and roofs beyond it</h2>
      <p class="lede" style="color:#a9bbb8">Hail Alley in North Texas, hurricanes on the Gulf Coast, heat that cooks membranes
      in Central and West Texas. Our pricing and estimates are built around Texas roofs, region by region, and we prepare
      estimates for properties in other states too.</p>
      <ul class="city-list" style="margin:18px 0 26px">{region_chips}<li>+ other U.S. states</li></ul>
      <a class="btn btn--peach" href="/areas/">See service areas {icon('arrow')}</a>
    </div>
    <div class="grid grid--2" data-reveal style="--d:.1s">
      <div class="card card--dark"><span class="ico">{icon('bolt')}</span><h3>Storm-ready</h3><p>Hail and wind claim estimates, supplements and reviews when the carrier's numbers come up short.</p></div>
      <div class="card card--dark"><span class="ico">{icon('map')}</span><h3>Regional pricing</h3><p>Labor and tear-off adjusted for seven Texas regions and five U.S. regions.</p></div>
      <div class="card card--dark"><span class="ico">{icon('file')}</span><h3>Remote by design</h3><p>We work from photos, drone shots and measurement reports, so distance is never a problem.</p></div>
      <div class="card card--dark"><span class="ico">{icon('shield')}</span><h3>Claim know-how</h3><p>RCV, ACV, depreciation, deductibles and O&amp;P: we speak the carrier's language.</p></div>
    </div>
  </div>
</div></section>"""

    posts = g["POSTS"][:3]
    blog = ""
    if posts:
        blog = f"""<section class="section"><div class="wrap">
  <div class="section-head" data-reveal><span class="kicker">From the blog</span><h2>Field notes from working estimators</h2></div>
  <div class="grid grid--3">{''.join(post_card(p) for p in posts)}</div>
  <p style="text-align:center;margin-top:32px"><a class="btn btn--ghost" href="/blog/">All articles {icon('arrow')}</a></p>
</div></section>"""

    main = hero + tools + stats + paths + who + steps + texas + blog + g["faq_html"](FAQS) + g["cta_band"]()
    g["write"]("/", g["render"](page, None, main, scripts=f'<script src="/assets/js/data.js?v={g["ASSET_V"]}" defer></script>\n'), priority="1.0")
