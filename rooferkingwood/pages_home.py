"""Homepage for rooferkingwood.com. Primary keyword: "Kingwood roofers" (14+ uses in the main content)."""
import build as B
from build import e, icon, img, TEL, PHONE

HOME_FAQS = [
    {"q": "Is the roof inspection really free?",
     "a": "Yes. Our inspections are free for Kingwood homeowners with no obligation to hire us. You get photos of what we find and an honest recommendation, even when the answer is that your roof is fine."},
    {"q": "A pine limb hit my roof. What should I do first?",
     "a": "Stay off the roof and away from any downed lines. If water is coming in, move valuables and catch the drip, photograph the damage from the ground, then call us. We can tarp the opening and document everything for your insurance company."},
    {"q": "Do I need village association approval for a new roof in Kingwood?",
     "a": "Most Kingwood village associations require architectural approval before a re-roof, usually for shingle color and material. Rules differ from village to village, so check your deed restrictions. We help you pick a product and gather the specs your committee asks for."},
    {"q": "Will you help with my insurance claim?",
     "a": "We document storm and tree damage with photos and measurements, explain what we found and can meet your adjuster on the roof. We are roofers, not public adjusters, and we never waive or rebate deductibles, which is illegal in Texas."},
    {"q": "How long does a roof replacement take in Kingwood?",
     "a": "Most single-family Kingwood homes are torn off and re-roofed in one to two days once materials arrive. Steep pitches, heavy tree cover over the driveway, decking repairs and weather can add time; you get a schedule up front."},
    {"q": "What does a new roof cost in Kingwood, TX?",
     "a": "Architectural shingle replacements on typical Kingwood homes commonly land in the low-to-mid five figures depending on roof size, pitch and material. Use our free roof cost calculator for a planning range, then book a free inspection for an exact written estimate."},
    {"q": "Why do so many Kingwood roofs get black streaks?",
     "a": "Shade and humidity under the tree canopy feed algae (often Gloeocapsa magma) that leaves dark streaks, and moss can grow where needles collect. Algae-resistant shingles and zinc or copper strips help; pressure-washing a shingle roof does more harm than good."},
    {"q": "What areas do you serve?",
     "a": "All of Kingwood (77339, 77345 and the Kingwood part of 77346) plus Atascocita, Humble, Porter, New Caney, Huffman and Crosby around Lake Houston."},
]


def build_home():
    svc_rows = "".join(
        f"""<li><a href="/services/{s['slug']}/"><span class="n">{i + 1:02d}</span><span><b>{e(s['name'])}</b><span class="s">{e(s['short'])}</span></span>
<span class="go">{icon('arrow')}</span></a></li>""" for i, s in enumerate(B.SERVICES))

    posts = "".join(
        f"""<article class="post-row" data-reveal><div class="img">{img(p['image'], p.get('image_alt', p['h1']))}</div>
<div><div class="meta"><span class="cat">{e(p.get('category', 'Guide'))}</span><span>{B.fmt_date(p['date'])}</span><span>{p.get('read_minutes', 6)} min read</span></div>
<h3><a href="/blog/{p['slug']}/">{e(p['h1'])}</a></h3><p>{e(p['excerpt'])}</p><span class="link-arrow">Read the guide {icon('arrow')}</span></div></article>"""
        for p in B.POSTS[:3])

    area_cards = "".join(f'<a class="area-card" href="/areas/{a["slug"]}/"><small>{e(a.get("county", ""))} County</small><b>{e(a["name"])}</b><p>{e(a["short"])}</p></a>'
                         for a in B.AREAS)
    villages = "".join(f"<span>{e(v)}</span>" for v in B.VILLAGES)

    seg = lambda name, opts, checked: '<div class="seg">' + "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{e(l)}</span></label>' for v, l in opts) + "</div>"

    main = f"""
<section class="hero">
<div class="wrap">
<div>
<span class="kicker" data-reveal>Kingwood, TX · The Livable Forest</span>
<h1 data-reveal style="--d:.08s">Kingwood roofers who know what <em>tall pines</em> and Gulf storms do to a roof</h1>
<p class="lead" data-reveal style="--d:.16s">We are the Kingwood roofers homeowners call for leaks, hail, fallen limbs and full replacements. Every job starts with a free inspection, a photo report and a straight answer about what your roof needs, and what it doesn't.</p>
<div class="hero-actions" data-reveal style="--d:.24s"><a class="btn" href="/free-roof-inspection/">Book a free inspection {icon('arrow')}</a>
<a class="btn btn-line" href="tel:{TEL}">{icon('phone')} {PHONE}</a></div>
<div class="proofs" data-reveal style="--d:.32s">
<div>{icon('camera')}<span><b>Photo report</b>Every issue documented</span></div>
<div>{icon('tree')}<span><b>Tree &amp; storm ready</b>Tarps, limbs, claims</span></div>
<div>{icon('file-check')}<span><b>ACC paperwork</b>Village approval help</span></div>
</div>
</div>
<div class="arch" data-reveal style="--d:.2s">
<div class="frame">{img('hero-pines', 'Two-story Kingwood home surrounded by tall pine trees, the kind of roof Kingwood roofers inspect every week', eager=True)}</div>
<div class="stamp"><span><b>$0</b>Roof inspection</span></div>
<a class="wx-chip" href="/weather/" data-wx-chip><span class="ic">⛅</span><span><small><span class="pulse"></span>Live in Kingwood</small><b>--°F</b><small>Loading conditions…</small></span></a>
</div>
</div>
</section>

<section class="quickbar"><div class="wrap">
<h2>Free inspection request <small>We call back to schedule. No obligation.</small></h2>
{B.quick_form()}
</div></section>

<section class="section">
<div class="wrap">
<div class="head" data-reveal><span class="kicker">Field notes</span><h2>Why roofs in Kingwood wear out <em>differently</em></h2>
<p>Most Kingwood roofers will tell you the same thing: this isn't an open-prairie suburb. Four local conditions shape every roof we touch here.</p></div>
<div class="notes">
<div class="note" data-reveal><span class="n">i.</span><h3>The canopy</h3><p>Pine needles pack valleys and gutters, shade feeds algae and moss, and limbs come down in every strong storm. Roofs here need more cleaning and closer inspection than roofs in treeless subdivisions.</p></div>
<div class="note" data-reveal style="--d:.08s"><span class="n">ii.</span><h3>Village rules</h3><p>Most of Kingwood's villages have deed restrictions and architectural review. The right Kingwood roofers handle color and material approval before a single shingle is ordered.</p></div>
<div class="note" data-reveal style="--d:.16s"><span class="n">iii.</span><h3>Gulf storms</h3><p>Spring hail, summer thunderstorms and hurricane season all reach Lake Houston. Wind lifts shingle edges and throws debris; hail bruises what the trees don't shade.</p></div>
<div class="note" data-reveal style="--d:.24s"><span class="n">iv.</span><h3>Older homes</h3><p>Much of Kingwood was built from the 1970s to the 1990s. Many roofs are on their second or third replacement, often with tired decking, old vents and undersized attic ventilation.</p></div>
</div>
</div>
</section>

<section class="section bg-cream">
<div class="wrap cols cols-5-7 top">
<div class="sticky" data-reveal>
<span class="kicker">Services</span>
<h2>Everything Kingwood roofers should handle, under one phone number</h2>
<p>From one cracked pipe boot to a full tear-off after a hailstorm, the work starts the same way: a free inspection with photos, then a written plan.</p>
<div class="photo offset-frame" style="margin-top:28px">{img('roofer-work', 'Roofer installing new asphalt shingles on a home near Kingwood, TX')}</div>
</div>
<div data-reveal style="--d:.1s">
<ul class="svc-list"><li><a href="/free-roof-inspection/"><span class="n">00</span><span><b>Free Roof Inspection</b><span class="s">Every slope, valley, vent and gutter checked, with a photo report you keep. No cost, no obligation.</span></span><span class="go">{icon('arrow')}</span></a></li>
{svc_rows}</ul>
</div>
</div>
</section>

<section class="section">
<div class="wrap cols">
<div class="photo tall offset-frame" data-reveal>{img('shingles', 'Close-up of asphalt shingles checked for hail bruising and granule loss')}<div class="cap">Hail bruises and lifted tabs rarely show from the driveway.</div></div>
<div data-reveal style="--d:.1s">
<span class="kicker">Free roof inspections</span>
<h2>See your roof the way we see it</h2>
<p>A roof under a pine canopy can look fine from the street while needles rot the valley underlayment and a cracked boot drips into the attic. Our inspection puts a roofer on every slope with a camera, so you see exactly what we see.</p>
<ul class="ticks">
<li>{icon('check')}<span><strong>Shingles:</strong> hail bruising, granule loss, creased or missing tabs, algae and moss</span></li>
<li>{icon('check')}<span><strong>Valleys &amp; debris:</strong> needle build-up, trapped water and worn underlayment</span></li>
<li>{icon('check')}<span><strong>Flashing &amp; penetrations:</strong> chimneys, walls, skylights, pipe boots and vents</span></li>
<li>{icon('check')}<span><strong>Gutters &amp; attic:</strong> overflow, fascia rot, decking stains and airflow</span></li>
</ul>
<p>It's the same inspection Kingwood roofers should give every homeowner: thorough, documented and free of sales pressure.</p>
<a class="btn" href="/free-roof-inspection/">Schedule my free inspection {icon('arrow')}</a>
</div>
</div>
</section>

<section class="section bg-pine">
<div class="wrap">
<div class="head" data-reveal style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;max-width:none">
<div style="max-width:640px"><span class="kicker light">Kingwood storm desk</span><h2>Live Kingwood weather, read by roofers</h2>
<p>Current conditions and a 5-day outlook for Kingwood, with a roof-risk rating for hail, thunderstorms and the gusts that bring pine limbs down.</p></div>
<a class="btn btn-brass" href="/weather/">Full forecast &amp; alerts {icon('arrow')}</a></div>
<div class="desk" data-wx-desk data-reveal>
<div class="desk-now"><span class="kicker light">Right now</span><p class="loading">Loading current Kingwood conditions…</p></div>
<div class="desk-days">{''.join('<div class="desk-day loading">·</div>' for _ in range(5))}</div>
<div class="desk-foot"><span data-wx-alertline>Checking National Weather Service alerts for Kingwood…</span><a href="/tools/storm-damage-checklist/">After a storm? Run the damage self-check</a></div>
</div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="head center" data-reveal><span class="kicker">How it works</span><h2>Five steps from first call to final walkthrough</h2>
<p>Hiring Kingwood roofers shouldn't feel like a gamble. Here's exactly what happens after you call.</p></div>
<div class="process">
<div class="pstep" data-reveal><div class="dot">1</div><h3>Call or book online</h3><p>Leak, storm, fallen limb or an aging roof. Pick a time that suits you.</p></div>
<div class="pstep" data-reveal style="--d:.08s"><div class="dot">2</div><h3>Free inspection</h3><p>Roof, flashing, gutters and attic, photographed from top to bottom.</p></div>
<div class="pstep" data-reveal style="--d:.16s"><div class="dot">3</div><h3>Written options</h3><p>An itemized estimate in plain English, plus claim guidance if storms caused it.</p></div>
<div class="pstep" data-reveal style="--d:.24s"><div class="dot">4</div><h3>Approval &amp; install</h3><p>Village ACC paperwork, then tear-off, decking, underlayment, flashing and vents.</p></div>
<div class="pstep" data-reveal style="--d:.32s"><div class="dot">5</div><h3>Walkthrough</h3><p>Completion photos, a magnetic nail sweep and care tips for your new roof.</p></div>
</div>
</div>
</section>

<section class="section bg-sand">
<div class="wrap">
<div class="head" data-reveal><span class="kicker">Try it now</span><h2>Plan your roof before anyone knocks on your door</h2>
<p>Two quick calculators to get you started. Nothing you enter is stored or sent.</p></div>
<div class="estimator" data-reveal>
<div class="est-tabs" role="tablist">
<button type="button" role="tab" aria-selected="true" aria-controls="est-cost" id="tab-cost">{icon('calculator')} Replacement cost</button>
<button type="button" role="tab" aria-selected="false" aria-controls="est-life" id="tab-life">{icon('hourglass')} Roof life left</button>
</div>
<form class="est-panel" id="est-cost" role="tabpanel" aria-labelledby="tab-cost" data-tool="quickcost" onsubmit="return false">
<div class="est-inputs">
<div class="field-row"><label for="q-sqft">Home size (living area) <output for="q-sqft"></output></label><input type="range" id="q-sqft" name="sqft" min="1200" max="6000" step="100" value="2800" data-fmt=" sq ft"></div>
<div class="field-row"><span class="lbl">Stories</span>{seg('stories', [('1', '1 story'), ('2', '2 stories')], '2')}</div>
<div class="field-row"><span class="lbl">Material</span>{seg('material', [('arch', 'Architectural'), ('class4', 'Class 4 impact'), ('metal', 'Standing-seam metal')], 'arch')}</div>
</div>
<div class="est-out" aria-live="polite"><span class="kicker light">Planning range</span><div class="big" data-out="range">—</div>
<span data-out="note"></span>
<a class="btn btn-brass" href="/tools/roof-cost-calculator/">Detailed calculator {icon('arrow')}</a>
<small>2026 Houston-area planning range, not a quote. Pitch, layers, decking and roof complexity change the price.</small></div>
</form>
<form class="est-panel" id="est-life" role="tabpanel" aria-labelledby="tab-life" data-tool="quicklife" onsubmit="return false" hidden>
<div class="est-inputs">
<div class="field-row"><label for="q-year">Year the roof was installed <output for="q-year"></output></label><input type="range" id="q-year" name="year" min="1995" max="2026" step="1" value="2012"></div>
<div class="field-row"><span class="lbl">Material</span>{seg('lmat', [('3tab', '3-tab'), ('arch', 'Architectural'), ('metal', 'Metal')], 'arch')}</div>
<div class="field-row"><span class="lbl">Tree cover over the roof</span>{seg('trees', [('0', 'Open sun'), ('1', 'Some shade'), ('2', 'Heavy canopy')], '1')}</div>
</div>
<div class="est-out" aria-live="polite"><span class="kicker light">Estimated life left</span><div class="big" data-out="left">—</div>
<div class="life-bar"><span class="used" data-out="used"></span><span class="left" data-out="leftbar"></span></div>
<span data-out="advice"></span>
<a class="btn btn-brass" href="/tools/roof-age-estimator/">Full roof age estimator {icon('arrow')}</a></div>
</form>
</div>
<p style="margin-top:22px" data-reveal>More free tools: <a href="/tools/roof-pitch-calculator/">roof pitch &amp; area calculator</a> · <a href="/tools/storm-damage-checklist/">storm damage self-check</a> · <a href="/weather/">live storm desk</a></p>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="head center" data-reveal><span class="kicker">Repair or replace?</span><h2>The honest answer depends on your roof</h2>
<p>Good Kingwood roofers will tell you when a repair is enough. Here's how we decide.</p></div>
<div class="versus">
<div class="vs-col" data-reveal><h3>{icon('hammer')} Usually a repair</h3><ul class="ticks">
<li>{icon('check')}<span>A few shingles lifted or torn off by wind</span></li>
<li>{icon('check')}<span>One leak at a pipe boot, vent, skylight or chimney</span></li>
<li>{icon('check')}<span>A limb puncture in an otherwise healthy roof</span></li>
<li>{icon('check')}<span>Roof under about 12 years old with local damage</span></li></ul>
<a class="link-arrow" href="/services/roof-repair-kingwood-tx/">Roof repair in Kingwood {icon('arrow')}</a></div>
<div class="vs-seal">vs</div>
<div class="vs-col" data-reveal style="--d:.1s"><h3>{icon('home')} Usually a replacement</h3><ul class="ticks">
<li>{icon('check')}<span>Hail bruising across several slopes</span></li>
<li>{icon('check')}<span>Brittle, curling or granule-bare shingles</span></li>
<li>{icon('check')}<span>Repeated leaks or soft decking under the valleys</span></li>
<li>{icon('check')}<span>Roof 18+ years old, or an approved insurance claim</span></li></ul>
<a class="link-arrow" href="/services/roof-replacement-kingwood-tx/">Roof replacement in Kingwood {icon('arrow')}</a></div>
</div>
</div>
</section>

<section class="section bg-pine">
<div class="wrap cols top">
<div data-reveal>
<span class="kicker light">Service area</span>
<h2>Kingwood roofers for every village, and the towns around Lake Houston</h2>
<p>We work across all of Kingwood's villages, from the older streets of Kingwood Forest and Trailwood to Kings Mill and Royal Shores on the newer edges. We know which villages are strict about shingle colors and which streets lose power and limbs first when a storm rolls up the San Jacinto.</p>
<p style="font-size:.92rem;opacity:.85">ZIP codes: 77339 · 77345 · 77346 · 77338 · 77396 · 77365 · 77357 · 77336 · 77532</p>
</div>
<div class="villages" data-reveal style="--d:.1s">{villages}</div>
</div>
<div class="wrap" style="margin-top:44px"><div class="area-cards" data-reveal>{area_cards}</div></div>
</section>

<section class="section">
<div class="wrap">
<div class="head" data-reveal style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;max-width:none">
<div style="max-width:660px"><span class="kicker">From the blog</span><h2>Roofing guides written for Kingwood homes</h2><p>Costs, claims, HOA approvals, tree damage and storm prep, written by local Kingwood roofers.</p></div>
<a class="btn btn-line" href="/blog/">All articles {icon('arrow')}</a></div>
<div>{posts}</div>
</div>
</section>

<section class="section bg-cream">
<div class="wrap cols">
<div data-reveal>
<span class="kicker">Why homeowners choose us</span>
<h2>The difference local Kingwood roofers make</h2>
<p>After every big storm, out-of-town crews flood Kingwood with yard signs and door-knockers. Many are gone before the first warranty question. Hiring Kingwood roofers means hiring people who will still answer the phone next hurricane season.</p>
<ul class="ticks">
<li>{icon('check')}<span><strong>Photos first:</strong> you see every problem before we recommend anything</span></li>
<li>{icon('check')}<span><strong>No deductible games:</strong> we follow Texas law and never waive or "cover" deductibles</span></li>
<li>{icon('check')}<span><strong>Itemized estimates:</strong> underlayment, flashing, vents, decking and disposal spelled out</span></li>
<li>{icon('check')}<span><strong>Respect for your yard:</strong> tarps over beds, careful work around trees and a magnetic nail sweep</span></li>
</ul>
<p>Whether you need a quick leak repair or a complete re-roof, your first step with these Kingwood roofers is the same: a free inspection and an honest answer.</p>
</div>
<div class="photo offset-frame" data-reveal style="--d:.1s">{img('forest-home', 'Home among tall trees in a wooded neighborhood like those served by Kingwood roofers')}</div>
</div>
</section>

{B.faq_html(HOME_FAQS, "Questions homeowners ask Kingwood roofers", bg="")}

{B.closer("Ready for Kingwood roofers who tell it straight?")}
"""
    faq = B.faq_schema(HOME_FAQS)
    html = B.page("/", "Kingwood Roofers | Roofing in Kingwood, TX | (512) 297-7580",
                  "Kingwood Roofers: local roofing company in Kingwood, TX for roof repair, replacement, storm and tree damage. Free roof inspections. Call (512) 297-7580.",
                  main, active="/", schema=[faq], preload="hero-pines", scripts=("weather", "tools"))
    B.add("/", html, priority="1.0")
