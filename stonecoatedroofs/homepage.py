"""Homepage: primary keyword "stone coated steel roofing" (+ Texas). Brand named 14+ times in the main content."""

import json

from siteconfig import BIZ, BRANDS, FEATURED_CITIES

ICONS = {
    "hail": "M7 15a4 4 0 1 1 1-7.9A5 5 0 0 1 18 8a3.5 3.5 0 0 1 0 7M8 19v.01M12 20v.01M16 19v.01",
    "wind": "M3 8h11a3 3 0 1 0-3-3M3 12h15a3 3 0 1 1-3 3M3 16h7",
    "hurricane": "M12 12m-3 0a3 3 0 1 0 6 0 3 3 0 1 0-6 0M12 3c-5 0-8 3-8 6M12 21c5 0 8-3 8-6M4 9c0 4 3 6 8 6M20 15c0-4-3-6-8-6",
    "tornado": "M3 4h18M5 8h14M7 12h10M9 16h6M11 20h2",
    "clock": "M12 12m-9 0a9 9 0 1 0 18 0 9 9 0 1 0-18 0M12 7v5l3 2",
    "shield": "M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6zM9 12l2 2 4-4",
}
REASONS = [
    ("hail", "Hail Damage", "Texas leads the U.S. in hail claims. Granule loss and bruising shorten a shingle roof's life by years even when no leak shows. Class 4 stone coated steel won't dent."),
    ("wind", "Wind Damage", "Sustained Texas winds lift shingle tabs, expose nails and start the slow leak that ruins a deck. Stone coated panels interlock — rated to 120 mph."),
    ("hurricane", "Hurricane Damage", "Beryl, Harvey, Ike — Texas coast roofs take direct hits every few years. Hurricane-rated stone coated systems are uplift-tested for coastal exposure."),
    ("tornado", "Tornado Damage", "North Texas sees more tornadoes than almost anywhere. Stone coated steel resists flying debris and interlocks to stay on the deck where shingles peel away."),
    ("clock", "End of Lifespan", "Most asphalt roofs in Texas last 12–18 years under UV and heat. If yours is 15+ and curling, shedding granules or letting daylight into the attic, it's time."),
    ("shield", "Insurance Non-Renewal", "Texas carriers are dropping homes with aging or storm-damaged roofs. A new stone coated steel roof often restores coverage and can lower premiums."),
]


def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ICONS[name]}"/></svg>'


def reasons_cards():
    return "".join(f'<a class="card tilt rv" style="--d:{i * .06:.2f}s" href="/free-quote/"><span class="ico">{icon(k)}</span><h3>{t}</h3><p>{p}</p><span class="more">Free inspection</span></a>'
                   for i, (k, t, p) in enumerate(REASONS))


CMP = {
    "_rows": ["Lifespan", "Hail rating (UL 2218)", "Wind rating", "Weight (lb / sq ft)", "Fire rating", "Insurance discount"],
    "stone": ["40–70 yrs", "Class 4", "120 mph+", "~2.4", "Class A", "Often yes"],
    "asphalt": ["12–18 yrs in Texas", "Class 3–4 (impact lines)", "60–130 mph", "2.3–4.3", "Class A", "Class 4 lines only"],
    "clay": ["50+ yrs (tiles crack)", "Varies; tiles break", "Varies", "8–12", "Class A", "Sometimes"],
    "concrete": ["30–50 yrs", "Often not rated", "Varies", "9–10", "Class A", "Rarely"],
    "standing": ["40–60 yrs", "Class 4 (can dent)", "High", "0.9–1.5", "Class A", "Often yes"],
    "cedar": ["20–30 yrs", "Not rated", "Moderate", "3–4.5", "Class C–B", "Often surcharged"],
    "_links": {"asphalt": "/stone-coated-vs-asphalt-shingle/", "clay": "/stone-coated-vs-clay-tile/", "concrete": "/stone-coated-vs-concrete-tile/",
               "standing": "/stone-coated-vs-standing-seam-metal/", "cedar": "/stone-coated-vs-cedar-shake/"},
}
CMP_NAMES = [("asphalt", "Asphalt shingle"), ("clay", "Clay tile"), ("concrete", "Concrete tile"), ("standing", "Standing seam"), ("cedar", "Cedar shake")]

FAQ = [
    {"q": "What is stone coated steel roofing?", "a": "Stone coated steel roofing is a steel panel protected by an aluminum-zinc coating, then finished with acrylic-bonded stone granules. Pressed into shingle, shake, tile or slate profiles, it looks like a traditional roof but weighs about 2.4 lb per sq ft and carries Class 4 hail and Class A fire ratings. <a href=\"/what-is-stone-coated-steel-roofing/\">Read the full guide</a>."},
    {"q": "How much does stone coated steel roofing cost in Texas?", "a": "Plan on roughly $10–$18 per square foot installed, depending on profile, pitch, tear-off and brand. Try the <a href=\"/tools/stone-coated-roof-cost-calculator/\">stone coated roof cost calculator</a> for a range on your home, or request a free estimate from Stone Coated Roofs."},
    {"q": "What are the problems with stone coated steel roofing?", "a": "The real problems are installation-driven: leaks at poorly flashed penetrations, granule shedding on cheap products, and scuffing from careless foot traffic. Higher upfront cost is the main trade-off. A specialist installer avoids most of them — see <a href=\"/stone-coated-steel-roof-problems/\">stone coated steel roofing problems</a>."},
    {"q": "Is stone coated steel the best roof material for hail?", "a": "For most Texas homes, yes. It carries the top UL 2218 Class 4 impact rating, and because the steel flexes rather than fractures, large hail usually leaves no functional damage. Compare options in our <a href=\"/best-roofing-material-for-hailstorms-in-texas/\">best roof material for hail</a> guide."},
    {"q": "Are stone coated roofs hurricane resistant?", "a": "Interlocking stone coated panels are wind-rated to 120 mph and higher, and foam-set or high-wind fastening schedules push uplift resistance further for the Gulf Coast. See <a href=\"/hurricane-resistant-roofing-systems/\">hurricane resistant roofing systems</a>."},
    {"q": "Will a stone coated roof lower my insurance?", "a": "Many Texas carriers discount Class 4 roofs — commonly 5% to 25% — and some restore coverage on homes they'd otherwise non-renew. Estimate yours with the <a href=\"/tools/insurance-discount-estimator/\">insurance discount estimator</a>."},
    {"q": "Is a stone coated steel roof loud in the rain?", "a": "No. The stone granules and the air gap of a batten install break up the sound, so rain sounds much like it does on shingles."},
    {"q": "Where does Stone Coated Roofs work?", "a": "Statewide — Houston, Dallas–Fort Worth, Austin, San Antonio, Corpus Christi, El Paso, Lubbock, East Texas and everywhere between. <a href=\"/service-area/\">Find your city</a>."},
]


def build(g):
    B = g["BRAND"]
    page, faq_html, post_card, lead_form, city_grid, tx_map = g["page"], g["faq_html"], g["post_card"], g["lead_form"], g["city_grid"], g["tx_map"]
    AREA, POSTS, faq_ld, E = g["AREA"], g["POSTS"], g["faq_ld"], g["E"]
    phone, ph = BIZ["phone_display"], BIZ["phone_href"]

    brands_mq = "".join(f"<span>{b[0]}</span>" for b in BRANDS) * 2
    brand_cards = "".join(
        (f'<a class="card brand tilt rv" style="--d:{i * .04:.2f}s" href="{h}">' if h else f'<div class="card brand rv" style="--d:{i * .04:.2f}s">')
        + f'<div class="bn">{n}<small>{tier}</small></div><p>{blurb}</p><div class="w">{w}</div>' + ("</a>" if h else "</div>")
        for i, (n, blurb, w, tier, h) in enumerate(BRANDS))
    styles = [("Slate", "The look of natural slate, without the 800 lb per square.", "/slate-roof/", "/wp-content/uploads/2026/05/Slate-Roof.webp"),
              ("Wood Shake", "Cedar-shake texture with a Class A fire rating.", "/wood-shake-roof/", "/wp-content/uploads/2026/05/Wood-Shake-Roof.webp"),
              ("Tile", "Mediterranean and Spanish profiles — terracotta that never cracks.", "/tile-roofs/", "/wp-content/uploads/2026/05/Tile-Roofs.webp"),
              ("Shingle", "Dimensional shingle look with five-decade durability.", "/shingle-roofs/", "/wp-content/uploads/2026/05/Shingle-Roofs.webp")]
    style_cards = "".join(f'<a class="icard rv" style="--d:{i * .08:.2f}s" href="{u}"><img src="{img}" alt="Stone coated steel {n.lower()} roof" width="900" height="600" loading="lazy"><div class="in-c"><span class="tag" style="color:#fff;background:rgba(255,255,255,.15)">Profile 0{i + 1}</span><h3>{n}</h3><p>{p}</p></div></a>'
                          for i, (n, p, u, img) in enumerate(styles))
    cmp_rows = "".join(f"<tr><td>{r}</td><td>{CMP['stone'][i]}</td><td>{CMP['asphalt'][i]}</td></tr>" for i, r in enumerate(CMP["_rows"]))
    cmp_btns = "".join(f'<button type="button" data-k="{k}" aria-pressed="{str(i == 0).lower()}">{n}</button>' for i, (k, n) in enumerate(CMP_NAMES))
    cmp_json = E(json.dumps({k: v for k, v in CMP.items() if k not in ("_rows", "stone")}))
    feat_cities = city_grid(FEATURED_CITIES + ["frisco", "mckinney", "denton", "southlake", "grand-prairie", "irving"], fid="home-cities")
    guides = [p for p in POSTS if p["slug"] in ("stone-coated-steel-roof-problems", "storm-damage-roof-replacement", "best-roofing-material-for-hailstorms-in-texas",
                                                 "hurricane-resistant-roofing-systems", "roof-types-for-insurance", "stone-coated-roofing-cost-texas")]
    methods = [("M.01", "Batten", "Horizontal battens fastened across the deck; panels hook onto them. A ventilated air space beneath gives the best thermal performance — the most common residential system.", "M5 70h150M5 50h150M20 50v20M60 50v20M100 50v20M140 50v20M5 50l20-14h40l20 14M85 50l20-14h40l10 7"),
               ("M.02", "Direct-to-Deck", "Panels fastened straight through the deck with no batten layer. Lower install cost and simpler detailing — popular on lower pitches.", "M5 70h150M5 60h150M5 60l20-14h40l20 14M85 60l20-14h40l10 7M30 60v10M70 60v10M110 60v10"),
               ("M.03", "Foam-Set", "Adhesive foam bonds panels to the underlayment without penetrating the deck. Exceptional wind-uplift performance — the choice for high-wind coastal homes.", "M5 70h150M5 62h150M5 62l20-14h40l20 14M85 62l20-14h40l10 7M25 62c5-6 10-6 15 0M65 62c5-6 10-6 15 0M105 62c5-6 10-6 15 0")]
    method_cards = "".join(f'<div class="card method rv" style="--d:{i * .08:.2f}s"><div class="mn">{m}</div><svg viewBox="0 0 160 80" aria-hidden="true"><path d="{d}"/></svg><h3>{n}</h3><p>{p}</p></div>'
                           for i, (m, n, p, d) in enumerate(methods))
    quotes = [("Took a direct hit from softball-sized hail in 2024. Asphalt neighbors filed total losses. Our Decra had not a single visible dent from the ground.", "M. Whitfield", "Plano · 9 yrs in"),
              ("Quietest roof I've ever lived under. The myth about metal roofs being loud in rain just doesn't apply to stone coated. The granular coating kills the noise.", "J. Reyes", "Belton · 4 yrs in"),
              ("The premium hurt — until our home insurance dropped over $800 a year and stayed there. The roof pays for itself in slow motion.", "K. Albright", "Houston · 6 yrs in")]
    quote_cards = "".join(f'<figure class="card quote rv" style="--d:{i * .08:.2f}s;margin:0"><div class="stars" aria-label="5 stars">★★★★★</div><blockquote>“{q}”</blockquote><figcaption><cite>— {n} · {w}</cite></figcaption></figure>'
                          for i, (q, n, w) in enumerate(quotes))
    meters = lambda rows: "".join(f'<div class="meter{" dim" if dim else ""}"><label><span>{n}</span><span>{lab}</span></label><div class="bar"><i data-w="{w}"></i></div></div>' for n, lab, w, dim in rows)  # noqa: E731
    tabs = [
        ("Hail", "Best roof material for hail", f"Hail is the number-one reason Texans replace roofs. Stone coated steel carries the top UL 2218 <strong>Class 4</strong> rating — a 2-inch steel ball dropped from 20 feet without cracking. The steel flexes; the granules hide minor marks. That's why {B} recommends it as the best roof for Texas hail storms.",
         [("Stone coated steel", "Class 4", 96, 0), ("Class 4 impact shingle", "Class 4*", 72, 1), ("Standard asphalt", "Class 1–3", 38, 1), ("Concrete tile", "Often cracks", 30, 1)],
         "/best-roofing-material-for-hailstorms-in-texas/", "/wp-content/uploads/2026/06/hail-resistant-roofing-texas-2.webp"),
        ("Hurricane &amp; wind", "Hurricane resistant roofing", "Interlocking panels mechanically lock to each other and the deck, so there's no seal strip for wind to peel. Standard systems are rated to 120 mph; foam-set and enhanced fastening schedules are used for hurricane-proof roofing on the Texas coast.",
         [("Stone coated (foam-set)", "Coastal high-wind", 95, 0), ("Stone coated (batten)", "120 mph+", 85, 0), ("Architectural asphalt", "60–130 mph", 55, 1), ("3-tab asphalt", "60 mph", 30, 1)],
         "/hurricane-resistant-roofing-systems/", "/wp-content/uploads/2026/07/hurricane-resistant-roofing-systems-2.webp"),
        ("Heat &amp; UV", "Built for Texas sun", "Asphalt bakes, curls and sheds granules in Texas heat. Steel doesn't soften, and a batten install leaves a vented air space that reduces attic heat gain. Ceramic-coated stone holds its color for decades.",
         [("Stone coated steel", "40–70 yrs", 92, 0), ("Clay tile", "50+ yrs", 80, 1), ("Architectural asphalt", "12–18 yrs TX", 32, 1), ("Wood shake", "20–30 yrs", 40, 1)],
         "/stone-coated-steel-roof-lifespan/", "/wp-content/uploads/2026/06/How-Long-Does-Stone-Coated-Steel-Roofing-Really-Last-2.webp"),
        ("Fire", "Class A fire rating", "A non-combustible steel substrate earns Class A — the highest fire rating — which matters for insurers and HOAs, especially where cedar shake is common.",
         [("Stone coated steel", "Class A", 95, 0), ("Concrete / clay tile", "Class A", 90, 1), ("Asphalt shingle", "Class A", 70, 1), ("Untreated cedar shake", "Class C", 20, 1)],
         "/stone-coated-vs-cedar-shake/", "/wp-content/uploads/2026/05/Wood-Shake-Roof.webp"),
    ]
    tab_btns = "".join(f'<button role="tab" type="button" aria-selected="{str(i == 0).lower()}" id="tb{i}" aria-controls="tp{i}">{t[0]}</button>' for i, t in enumerate(tabs))
    tab_panels = "".join(f'<div role="tabpanel" id="tp{i}" aria-labelledby="tb{i}" class="tabpanel{" on" if i == 0 else ""}"><div><h3 style="font-size:1.8rem">{t[1]}</h3><p style="color:#d6ccbf">{t[2]}</p><div class="reveal-group">{meters(t[3])}</div><p class="mt"><a class="btn btn-ghost btn-sm" href="{t[4]}">Read the guide <span class="arr">→</span></a></p></div><img src="{t[5]}" alt="{t[1]} — stone coated steel roofing" width="900" height="600" loading="lazy"></div>'
                         for i, t in enumerate(tabs))
    problems = [("Leaks at flashings", "Almost every stone coated leak traces to a penetration — chimney, skylight, pipe boot — flashed like a shingle roof. We use the manufacturer's own trim and flashing details."),
                ("Granule loss", "A little loose stone after install is normal. Ongoing shedding signals a cheap product or foot traffic damage. We install only tier-one lines and walk panels correctly."),
                ("Dents &amp; scuffs", "Hail rarely dents stone coated steel, but careless installers do. Specialist crews step on the panel's strong points, not the middle."),
                ("Noise myths", "Installed over solid decking and underlayment, it's no louder than shingles in rain."),
                ("Higher upfront cost", "It costs more on day one — and less over 40 years. Run the lifetime calculator to see your break-even."),
                ("Finding a real installer", "Most roofers install stone coated a few times a year. Stone Coated Roofs installs nothing else.")]
    prob_cards = "".join(f'<div class="card lift rv" style="--d:{i * .05:.2f}s"><span class="tag">Problem 0{i + 1}</span><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate(problems))
    storm = [("Inspect &amp; document", "Free roof-level inspection with photos of every hit, dent and lifted panel."),
             ("File the claim", "We give you the documentation your carrier asks for and meet the adjuster on site."),
             ("Review the scope", "We check the insurer's estimate line by line against what the roof actually needs."),
             ("Upgrade, don't repeat", "Apply the claim toward Class 4 stone coated steel so the next storm isn't another claim."),
             ("Install &amp; register", "Installed by specialists, registered for the manufacturer warranty, documented for your discount.")]
    storm_html = "".join(f'<div class="step rv" style="--d:{i * .08:.2f}s"><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(storm))

    body = f"""
<section class="hero"><canvas class="hail" aria-hidden="true"></canvas>
<div class="wrap">
<div>
<span class="eyebrow">Stone Coated Roofs · Texas statewide</span>
<h1 class="split-words">Stone coated steel roofing, <em class="it">built for Texas weather.</em></h1>
<p class="lede rv" style="--d:.5s">Stone Coated Roofs is Texas's specialist installer of stone coated steel roofing. Residential and commercial, every leading brand — Decra, Tilcor, TEK, Roser and more — and statewide service. One Class 4 roof, installed once, for the life of the building.</p>
<div class="ctas rv" style="--d:.65s"><a class="btn mag" href="/free-quote/" data-open-quote>Get a free estimate <span class="arr">→</span></a><a class="btn btn-ghost" href="tel:{ph}">Call {phone}</a></div>
<div class="hero-badges rv" style="--d:.8s"><span class="chip"><b>Class 4</b> hail rated</span><span class="chip"><b>120 mph+</b> wind</span><span class="chip"><b>Class A</b> fire</span><span class="chip"><b>50-yr–lifetime</b> warranties</span></div>
</div>
<div class="hero-visual rv rv-r" style="--d:.3s"><div class="frame"><img src="/wp-content/uploads/2026/05/What-Is-Stone-Coated-Steel-Roofing.webp" width="900" height="600" alt="Charcoal stone coated steel tile roof installed by Stone Coated Roofs" fetchpriority="high"></div>
<div class="float-card a"><small>Lifespan</small><strong>40–70 yrs</strong></div>
<div class="float-card b"><small>Weight</small><strong>2.4 lb/sf</strong></div>
<div class="float-card c"><small>Insurance</small><strong>Class 4 discount</strong></div></div>
</div><span class="scroll-cue" aria-hidden="true"></span></section>

<div class="marquee" aria-label="Brands installed by Stone Coated Roofs"><div class="track">{brands_mq}</div></div>

<section class="section tight"><div class="wrap">
<h2 class="sr">Stone coated steel roofing performance</h2>
<div class="stats">
<div class="stat"><div class="v"><span data-count="70">0</span><sup>yrs</sup></div><p>Service life a stone coated steel roof can reach — about three asphalt roofs.</p></div>
<div class="stat"><div class="v">Class&nbsp;<span data-count="4">0</span></div><p>Highest UL 2218 impact rating — the one Texas insurers reward.</p></div>
<div class="stat"><div class="v"><span data-count="120">0</span><sup>mph</sup></div><p>Standard wind rating; coastal systems go higher.</p></div>
<div class="stat"><div class="v"><span data-count="2.4">0</span><sup>lb/sf</sup></div><p>Roughly a quarter the weight of concrete tile — no structural upgrade.</p></div>
</div></div></section>

<section class="section"><div class="wrap two">
<div class="layers rv" aria-hidden="true"><div class="layer" style="--z:0">Steel core</div><div class="layer" style="--z:0">Aluminum-zinc coating</div><div class="layer" style="--z:0">Acrylic basecoat</div><div class="layer" style="--z:0">Stone granules</div><div class="layer" style="--z:0">Clear overglaze</div></div>
<div><span class="eyebrow">01 · What it is</span><h2 class="split-words">What is stone coated <span class="it">steel roofing?</span></h2>
<p class="lead-p">Stone coated steel roofing is a steel panel sealed in an aluminum-zinc alloy and finished with real stone granules. It looks like slate, shake, tile or shingle — and performs like steel.</p>
<ol class="layer-list"><li><b>Steel core</b><span>Structural strength that flexes under hail instead of cracking.</span></li><li><b>Aluminum-zinc coating</b><span>Corrosion protection on both faces of the steel.</span></li><li><b>Stone granules</b><span>Color, texture and sound damping — bonded in acrylic.</span></li><li><b>Overglaze</b><span>Locks the stone in and keeps the finish from fading.</span></li></ol>
<p class="mt"><a href="/what-is-stone-coated-steel-roofing/">Stone Coated Roofs' complete guide to stone coated steel →</a></p></div>
</div></section>

<section class="section sand"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">02 · Why replace</span><h2>Reasons to <span class="it">replace your roof.</span></h2></div><p>If any of these apply, your roof is overdue. Stone Coated Roofs inspects for free and documents everything for your insurance carrier. <a href="/why-replace/">See all the warning signs →</a></p></div>
<div class="grid g3">{reasons_cards()}</div>
</div></section>

<section class="section dark"><div class="wrap" data-tabs>
<div class="sec-head"><div><span class="eyebrow">03 · Performance</span><h2>Storm resistant roofs for <span class="it">every Texas threat.</span></h2></div><p>Hail in DFW, hurricanes on the Gulf, heat everywhere. Here's how stone coated steel roofing compares where it counts.</p></div>
<div class="tabs" role="tablist" aria-label="Performance">{tab_btns}</div>{tab_panels}
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">04 · Honest answers</span><h2>Stone coated steel roofing problems <span class="it">— and how we prevent them.</span></h2></div><p>Every roof has weak points. Most stone coated complaints come from installers who don't specialize. Here's what goes wrong and how Stone Coated Roofs avoids it. <a href="/stone-coated-steel-roof-problems/">Full problems guide →</a></p></div>
<div class="grid g3">{prob_cards}</div>
</div></section>

<section class="section sand"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">05 · Free tools</span><h2>Price your roof <span class="it">in 30 seconds.</span></h2></div><p>Move the sliders for a planning range on a stone coated steel roof for your home — then try the lifetime cost, insurance and hail tools from Stone Coated Roofs.</p></div>
{g["tools"].cost_tool("h", compact=True)}
<div class="grid g3 mt tool-cards">{g["TOOL_CARDS_SMALL"]}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">06 · Compare</span><h2>How it stacks up <span class="it">against everything else.</span></h2></div><p>Pick a material to compare against stone coated steel on lifespan, hail, wind, weight, fire and insurance.</p></div>
<div class="cmp rv" data-cmp="{cmp_json}"><div class="cmp-pick">{cmp_btns}</div>
<div class="table-wrap" style="margin:0;border:0;border-radius:0"><table><thead><tr><th>Factor</th><th>Stone coated steel</th><th>Asphalt shingle</th></tr></thead><tbody>{cmp_rows}</tbody></table></div>
<p style="padding:16px 20px;margin:0"><a class="cmp-link" href="/stone-coated-vs-asphalt-shingle/">Read: stone coated vs asphalt shingle →</a> · <a href="/topic/compare/">All comparisons</a></p></div>
</div></section>

<section class="section dark"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">07 · Brands</span><h2>Certified to install <span class="it">every leading brand.</span></h2></div><p>Stone Coated Roofs recommends the right system for your home — not whatever's in the warehouse.</p></div>
<div class="grid g3">{brand_cards}</div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">08 · Profiles</span><h2>Steel that looks <span class="it">like anything.</span></h2></div><p>Stone coated steel can be pressed and finished to mimic almost any traditional roof — at a fraction of the weight. <a href="/topic/roof-styles/">Explore styles →</a></p></div>
<div class="grid g4">{style_cards}</div>
</div></section>

<section class="section sand"><div class="wrap two" style="align-items:start">
<div><span class="eyebrow">09 · Insurance</span><h2>Roof types for insurance: <span class="it">why Class 4 wins.</span></h2>
<p class="lead-p">Texas underwriters look hard at roof age, material and impact rating. A Class 4 stone coated steel roof checks every box — and often earns a premium discount or keeps a policy from non-renewal.</p>
<ul class="layer-list"><li><b>UL 2218 Class 4 impact rating</b><span>The rating behind most Texas impact-resistant roof discounts.</span></li><li><b>Class A fire, 120 mph+ wind</b><span>Fewer claims for wind and fire underwriting.</span></li><li><b>Documentation from Stone Coated Roofs</b><span>Product approvals and install certificate for your agent.</span></li></ul>
<p class="mt" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="/tools/insurance-discount-estimator/">Estimate my discount <span class="arr">→</span></a><a class="btn btn-ghost" href="/roof-types-for-insurance/">Roof types for insurance</a></p></div>
<div><span class="eyebrow">10 · Storm damage</span><h2>Storm damage roof <span class="it">replacement, start to finish.</span></h2>
<div class="steps" style="grid-template-columns:1fr">{storm_html}</div>
<p class="mt"><a href="/storm-damage-roof-replacement/">Storm damage roof replacement guide →</a> · <a href="/roof-replacement-after-hail-storm/">Hail damage roof replacement →</a></p></div>
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">11 · Commercial</span><h2>Built for commercial <span class="it">properties, too.</span></h2></div><p>Sloped or mansard roof? Stone coated steel makes it permanent — apartments, hotels, retail, churches, senior living and HOAs. <a href="/commercial/">Commercial roofing →</a></p></div>
<div class="grid g4">{g["commercial_cards"]()}</div>
</div></section>

<section class="section dark"><div class="wrap two">
<div><span class="eyebrow">12 · Service area</span><h2>We serve <span class="it">every Texas city.</span></h2><p style="color:#b8ada1">From the Panhandle to the Gulf, Stone Coated Roofs dispatches crews statewide with city-specific knowledge of local code, climate and HOA rules.</p>{feat_cities}<p class="mt"><a class="btn btn-ghost" href="/service-area/">Browse all Texas cities <span class="arr">→</span></a></p></div>
{tx_map()}
</div></section>

<section class="section"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">13 · Install methods</span><h2>How it gets <span class="it">on the roof.</span></h2></div><p>Three install systems, each with trade-offs in cost, performance and deck compatibility. We pick the right one for your building.</p></div>
<div class="grid g3 dark" style="background:none">{method_cards}</div>
</div></section>

<section class="section dark"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">14 · Field reports</span><h2>What the roof looks like, <span class="it">years in.</span></h2></div><p>Texas property owners on life under stone coated steel.</p></div>
<div class="grid g3">{quote_cards}</div>
</div></section>

<section class="section sand"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">15 · Guides</span><h2>Stone Coated Roofs <span class="it">guides.</span></h2></div><p>Plain-English answers on cost, problems, hail, hurricanes and insurance. <a href="/blog/">All guides →</a></p></div>
<div class="grid g3">{"".join(post_card(p) for p in guides)}</div>
</div></section>

{faq_html(FAQ, "Stone coated steel roofing FAQ")}

<section class="section dark" id="estimate"><div class="wrap two">
<div><span class="eyebrow">Free estimate</span><h2>One roof. <span class="it">One time.</span></h2><p style="color:#d6ccbf;font-size:1.1rem">Tell Stone Coated Roofs about your property and we'll schedule a free inspection, walk you through every brand and profile, and give you a written estimate — no pressure.</p>
<p style="color:#d6ccbf">Prefer the phone? <a href="tel:{ph}" style="color:#f2c4a6;font-weight:600">{phone}</a></p></div>
<div class="quote-box rv">{lead_form("home", "Request your free estimate")}</div>
</div></section>
"""
    graph = [faq_ld(FAQ), {"@type": "WebPage", "@id": f"{g['ORIGIN']}/#webpage", "url": f"{g['ORIGIN']}/", "name": "Stone Coated Roofs — Stone Coated Steel Roofing in Texas",
                           "about": {"@id": f"{g['ORIGIN']}/#business"}, "isPartOf": {"@id": f"{g['ORIGIN']}/#website"}}]
    page("/", "Stone Coated Roofs | Stone Coated Steel Roofing in Texas",
         "Stone Coated Roofs is Texas's specialist in stone coated steel roofing — Class 4 hail, 120 mph wind, every leading brand, residential & commercial, statewide.",
         body, graph=graph, scripts=("site", "tools"),
         extra_head='<link rel="preload" as="image" href="/wp-content/uploads/2026/05/What-Is-Stone-Coated-Steel-Roofing.webp">')
