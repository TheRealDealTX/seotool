"""Homepage for rooferkaty.com. Primary keyword: "Katy roofer" (plus katy roofing / roofer in Katy / roofers in Katy)."""
import build as B
from build import e, icon, img, TEL, PHONE

HOME_FAQS = [
    {"q": "Is the roof inspection really free?",
     "a": "Yes. Our roof inspections are free for Katy homeowners with no obligation to hire us. You get photos of what we find and an honest recommendation, even if the answer is that your roof is fine."},
    {"q": "How do I know if hail damaged my roof?",
     "a": "Hail damage is rarely visible from the ground. Look for dented gutters, downspouts, AC fins or mailboxes, and granules collecting at downspout outlets. If you see those signs, book a free inspection so a Katy roofer can check the shingles up close and document any bruising."},
    {"q": "Will you help with my insurance claim?",
     "a": "We document storm damage with photos and measurements, explain what we found, and can meet your adjuster on the roof. We are roofers, not public adjusters, and we never waive or rebate deductibles, which is illegal in Texas."},
    {"q": "How long does a roof replacement take in Katy?",
     "a": "Most single-family homes in Katy are torn off and re-roofed in one to two days once materials are delivered. Weather, roof size, steep pitches and decking repairs can add time; we'll give you a schedule up front."},
    {"q": "What does a new roof cost in Katy, TX?",
     "a": "Architectural shingle replacements on typical Katy homes commonly run in the low-to-mid five figures depending on roof size, pitch and material. Try our free roof cost calculator for a planning range, then book a free inspection for an exact written estimate."},
    {"q": "Do you work with HOAs in Cinco Ranch, Cane Island and Elyson?",
     "a": "Yes. Many Katy communities have rules on shingle color and material. We help you choose an approved product and provide the specs your HOA's architectural committee usually asks for."},
    {"q": "Should I repair or replace my roof?",
     "a": "Isolated damage on a roof under about 12 to 15 years old is usually a repair. Widespread hail bruising, curling or brittle shingles, repeated leaks, or a roof near the end of its life usually point to replacement. We'll show you photos and give you both options when both make sense."},
    {"q": "What areas do you serve?",
     "a": "We serve all of Katy (77449, 77450, 77493, 77494) plus Cinco Ranch, Fulshear, Brookshire, Cypress, Richmond and West Houston along the Energy Corridor."},
]


def build_home():
    services = "".join(
        f"""<article class="card" data-reveal style="--d:{(i % 4) * 0.08:.2f}s"><div class="ico">{icon(s.get('icon', 'home'))}</div>
<h3><a class="card-link" href="/services/{s['slug']}/" style="color:inherit;text-decoration:none">{e(s['name'])}</a></h3><p>{e(s['short'])}</p>
<span class="more">Learn more {icon('arrow')}</span></article>""" for i, s in enumerate(B.SERVICES))
    services = (f"""<article class="card" data-reveal style="background:linear-gradient(135deg,var(--brand),var(--brand-2));color:#fff;border:0">
<div class="ico" style="background:rgba(255,255,255,.2);color:#fff">{icon('clipboard')}</div>
<h3 style="color:#fff"><a class="card-link" href="/free-roof-inspection/" style="color:inherit;text-decoration:none">Free Roof Inspection</a></h3>
<p style="color:#fff">A full roof check with photos and a written report. No cost, no obligation, no pressure.</p>
<span class="more" style="color:#fff">Book yours {icon('arrow')}</span></article>""" + services)

    posts = "".join(
        f"""<article class="card img-card" style="--d:{i * 0.1:.1f}s"><div class="img">{img(p['image'], p.get('image_alt', p['h1']))}</div>
<div class="body"><span class="tag">{e(p.get('category', 'Guide'))}</span><div class="meta-row"><span>{B.fmt_date(p['date'])}</span><span>{p.get('read_minutes', 6)} min read</span></div>
<h3><a class="card-link" href="/blog/{p['slug']}/" style="color:inherit;text-decoration:none">{e(p['h1'])}</a></h3><p>{e(p['excerpt'])}</p>
<span class="more">Read article {icon('arrow')}</span></div></article>""" for i, p in enumerate(B.POSTS[:3]))

    areas = "".join(f'<a href="/areas/{a["slug"]}/">{e(a["name"])}</a>' for a in B.AREAS)
    marquee_items = ["Free roof inspections", "Hail & wind damage", "Insurance claim documentation", "Roof replacement", "Leak repair",
                     "Metal roofing", "Gutters & drainage", "Cinco Ranch", "Fulshear", "Cane Island", "Elyson", "Cross Creek Ranch", "Grand Lakes"]
    marquee = "".join(f"<span>{e(m)}</span>" for m in marquee_items) * 2

    main = f"""
<section class="hero hero-home">
<div class="hero-bg" style="background-image:url(/assets/img/hero-roofer.webp)"></div>
<div class="wrap">
<div>
<div data-reveal><span class="eyebrow"><span class="dot"></span> Free roof inspections in Katy, TX</span></div>
<h1 data-reveal style="--d:.1s">The <span class="hl">Katy Roofer</span> your neighbors call after the storm</h1>
<p class="lead" data-reveal style="--d:.2s">Roof repair, roof replacement and hail damage help from a local Katy roofer who documents everything with photos, explains it in plain English and never pushes you into a roof you don't need.</p>
<div class="hero-actions" data-reveal style="--d:.3s"><a class="btn" href="/free-roof-inspection/">Book a free inspection {icon('arrow')}</a>
<a class="btn btn-outline-light" href="tel:{TEL}">{icon('phone')} {PHONE}</a></div>
<div class="hero-trust" data-reveal style="--d:.4s"><span>{icon('check-circle')} $0 inspection</span><span>{icon('camera')} Photo report</span><span>{icon('shield')} Insurance-claim savvy</span></div>
</div>
<div class="form-card" data-reveal="zoom" style="--d:.25s">{B.lead_form('hero-form', heading='Get your free roof inspection', sub='Takes 30 seconds. A local Katy roofer will call to schedule.')}</div>
</div>
<div class="scroll-cue" aria-hidden="true"></div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>

<section class="section" style="padding-top:90px">
<div class="wrap">
<div class="stats">
<div class="stat" data-reveal><b>$<em data-count="0">0</em></b><span>Cost of your roof inspection, always</span></div>
<div class="stat" data-reveal style="--d:.08s"><b><em data-count="3">0</em></b><span>Counties covered: Harris, Fort Bend &amp; Waller</span></div>
<div class="stat" data-reveal style="--d:.16s"><b><em data-count="7">0</em>+</b><span>Communities served around Katy</span></div>
<div class="stat" data-reveal style="--d:.24s"><b><em data-count="7">0</em>-day</b><span>Live Katy forecast on our weather page</span></div>
</div>
</div>
</section>

<section class="section" style="padding-top:0">
<div class="wrap split">
<div data-reveal="left">
<span class="eyebrow">Local Katy roofing</span>
<h2>A Katy roofer who knows what Gulf Coast weather does to a roof</h2>
<p>Katy roofs work harder than most. Summer attic temperatures bake shingles from below, Gulf humidity feeds algae and wood rot, spring storms throw hail across Fort Bend and Harris counties, and every hurricane season brings the chance of a Beryl-style wind event. A good Katy roofer plans for all of it, not just the next rain.</p>
<p>That's how we approach Katy roofing: the right underlayment for humidity, ventilation sized for Texas heat, and shingles or metal rated for the wind and hail we actually get. Whether you live in an older home near Old Town Katy or a newer build in Cane Island, Elyson or Cross Creek Ranch, you'll get a straight answer about what your roof needs and what it doesn't.</p>
<p>Homeowners looking for a roofer in Katy usually want three things: someone who answers the phone, someone who shows up when they said they would, and someone who doesn't inflate the job. That's the standard we hold ourselves to on every roof.</p>
<a class="btn btn-ghost" href="/about/">Why homeowners choose us {icon('arrow')}</a>
</div>
<div data-reveal="right"><div class="wx-mini" data-wx-mini><div class="eyebrow" style="color:var(--gold)"><span class="dot"></span>Live in Katy, TX</div><p style="color:#aab8cb">Loading current conditions…</p></div></div>
</div>
</section>

<section class="section section-soft">
<div class="wrap">
<div class="section-head center" data-reveal><span class="eyebrow">Services</span><h2>Katy roofing services, start to finish</h2>
<p>Need a roofer in Katy for a single leak or a full replacement after a hailstorm? Every job starts with a free inspection and a photo report.</p></div>
<div class="grid g4">{services}</div>
</div>
</section>

<section class="section">
<div class="wrap split">
<div class="media">{img('roofer-shingles', 'Katy roofer in a safety harness inspecting asphalt shingles during a free roof inspection')}
<div class="media-badge"><span class="ico">{icon('check')}</span><span>Every inspection includes a photo report you keep</span></div></div>
<div data-reveal="right">
<span class="eyebrow">Free roof inspections</span>
<h2>Free roof inspections. Real photos. No pressure.</h2>
<p>Most roof damage in Katy can't be seen from the driveway. Hail bruises, lifted shingles, cracked pipe boots and failing flashing all hide in plain sight until water shows up on a ceiling. Our free roof inspection puts a trained Katy roofer on your roof with a camera, so you see exactly what we see.</p>
<ul class="checks">
<li>{icon('check-circle')}<span><strong>Shingles &amp; surface:</strong> hail bruising, granule loss, creases, lifted tabs and wind damage</span></li>
<li>{icon('check-circle')}<span><strong>Flashing &amp; penetrations:</strong> chimneys, walls, valleys, pipe boots and vents</span></li>
<li>{icon('check-circle')}<span><strong>Gutters &amp; soft metals:</strong> dents that confirm hail size and direction</span></li>
<li>{icon('check-circle')}<span><strong>Attic &amp; ventilation:</strong> moisture, daylight, decking condition and airflow</span></li>
</ul>
<a class="btn" href="/free-roof-inspection/">Schedule my free inspection {icon('arrow')}</a>
</div>
</div>
</section>

<section class="section section-dark">
<div class="wrap split" style="align-items:start">
<div class="sticky" data-reveal="left">
<span class="eyebrow">How it works</span>
<h2>Five steps from first call to final walkthrough</h2>
<p>Hiring roofers in Katy shouldn't feel like a gamble. Here's exactly what happens when you call us, so there are no surprises.</p>
<a class="btn" href="tel:{TEL}">{icon('phone')} Call {PHONE}</a>
</div>
<div class="steps"><span class="line" aria-hidden="true"></span>
<div class="step" data-n="1" data-reveal><h3>Call or book online</h3><p>Tell us what's going on: a leak, a recent storm, an aging roof or a home you're buying. We'll set a time that works for you.</p></div>
<div class="step" data-n="2" data-reveal><h3>Free roof inspection</h3><p>We check the roof surface, flashing, vents, gutters and attic, and photograph everything we find, good and bad.</p></div>
<div class="step" data-n="3" data-reveal><h3>Clear, written options</h3><p>You get an itemized estimate in plain English. If there's storm damage, we explain how claims work and can meet your adjuster.</p></div>
<div class="step" data-n="4" data-reveal><h3>Installation done right</h3><p>Tear-off, decking repairs, synthetic underlayment, ice-and-water at valleys, new flashing and ventilation. Your yard gets magnet-swept for nails.</p></div>
<div class="step" data-n="5" data-reveal><h3>Final walkthrough</h3><p>We walk the finished job with you, share completion photos and make sure you know how to care for your new roof.</p></div>
</div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">Katy weather vs. your roof</span><h2>What actually damages roofs in Katy</h2>
<p>Every Katy roofer sees the same four culprits. Knowing them helps you spot problems early and choose the right materials.</p></div>
<div class="grid g4">
<div class="card" data-reveal><div class="ico">{icon('cloud-hail')}</div><h3>Spring hail</h3><p>March through June storms can drop hail across Katy that bruises shingles and knocks off the granules protecting them from UV. Damage often shows up as leaks months later.</p></div>
<div class="card" data-reveal style="--d:.08s"><div class="ico">{icon('wind')}</div><h3>Hurricane &amp; straight-line wind</h3><p>Tropical systems and derechos peel back shingle edges and ridge caps. Once the seal strip breaks, the next storm finishes the job.</p></div>
<div class="card" data-reveal style="--d:.16s"><div class="ico">{icon('sun')}</div><h3>Heat &amp; UV</h3><p>Long Texas summers dry out asphalt, crack pipe boots and shorten roof life, especially on poorly ventilated attics.</p></div>
<div class="card" data-reveal style="--d:.24s"><div class="ico">{icon('droplets')}</div><h3>Humidity &amp; heavy rain</h3><p>Gulf moisture feeds algae streaks and rots decking around failed flashing. Clogged gutters send water under the roof edge.</p></div>
</div>
<p style="margin-top:28px" data-reveal>Keep an eye on the sky with our <a href="/weather/">live Katy weather page and 7-day forecast</a>, including a daily roof-risk rating.</p>
</div>
</section>

<section class="section section-soft">
<div class="wrap">
<div class="section-head center" data-reveal><span class="eyebrow">Repair or replace?</span><h2>The honest answer depends on your roof</h2>
<p>We'll always tell you if a repair will do. Here's how we think about it.</p></div>
<div class="compare">
<div class="card" data-reveal="left"><h3>{icon('hammer')} Usually a repair</h3><ul class="checks" style="margin:0">
<li>{icon('check')}<span>A few missing or lifted shingles after wind</span></li>
<li>{icon('check')}<span>A leak at one pipe boot, vent or chimney</span></li>
<li>{icon('check')}<span>Roof under about 12 years old with localized damage</span></li>
<li>{icon('check')}<span>Flashing or sealant failure in one area</span></li></ul>
<a class="more" href="/services/roof-repair-katy-tx/" style="margin-top:18px">Roof repair in Katy {icon('arrow')}</a></div>
<div class="card" data-reveal="right"><h3>{icon('home')} Usually a replacement</h3><ul class="checks" style="margin:0">
<li>{icon('check')}<span>Hail bruising across multiple slopes</span></li>
<li>{icon('check')}<span>Curling, cracking or brittle shingles; heavy granule loss</span></li>
<li>{icon('check')}<span>Recurring leaks or soft, sagging decking</span></li>
<li>{icon('check')}<span>Roof 18+ years old, or an approved insurance claim</span></li></ul>
<a class="more" href="/services/roof-replacement-katy-tx/" style="margin-top:18px">Roof replacement in Katy {icon('arrow')}</a></div>
</div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head" data-reveal><span class="eyebrow">Free homeowner tools</span><h2>Plan your roof project before anyone knocks on your door</h2>
<p>Run the numbers yourself. These calculators are free and nothing you enter is stored.</p></div>
<div class="grid g3">
<a class="card" href="/tools/roof-cost-calculator/" style="text-decoration:none;color:inherit" data-reveal><div class="ico">{icon('calculator')}</div><h3>Roof Cost Calculator</h3><p>Estimate a replacement range for your Katy home by size, pitch and material, from 3-tab to standing-seam metal.</p><span class="more">Estimate my roof {icon('arrow')}</span></a>
<a class="card" href="/tools/roof-pitch-calculator/" style="text-decoration:none;color:inherit;--d:.08s" data-reveal><div class="ico">{icon('ruler')}</div><h3>Roof Pitch &amp; Area Calculator</h3><p>Convert pitch to degrees, get the slope multiplier, roof squares and how many shingle bundles to order.</p><span class="more">Calculate pitch {icon('arrow')}</span></a>
<a class="card" href="/tools/storm-damage-checklist/" style="text-decoration:none;color:inherit;--d:.16s" data-reveal><div class="ico">{icon('clipboard')}</div><h3>Storm Damage Self-Check</h3><p>After hail or high wind, tick what you see from the ground and get a likelihood score and next steps.</p><span class="more">Check my roof {icon('arrow')}</span></a>
</div>
</div>
</section>

<section class="section section-dark">
<div class="wrap split">
<div data-reveal="left">
<span class="eyebrow">Service area</span>
<h2>Roofers in Katy and across the west Houston suburbs</h2>
<p>We're roofers in Katy first, which means we know the HOA color rules in Cinco Ranch, the newer roofs going up in Elyson and Jordan Ranch, and the older homes off Avenue D that need a little more care. From the Grand Parkway to the Energy Corridor, if you're near I-10 west of Houston, we cover you.</p>
<div class="chips" style="margin:22px 0"><a href="/">Katy, TX</a>{areas}</div>
<p style="font-size:.95rem">ZIP codes: 77449 · 77450 · 77493 · 77494 · 77441 · 77423 · 77433 · 77406 · 77469 · 77077 · 77084 · 77094</p>
</div>
<div class="media">{img('brick-homes', 'Brick two-story homes with asphalt shingle roofs in a Katy, Texas subdivision')}</div>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="section-head" data-reveal style="display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;max-width:none">
<div style="max-width:700px"><span class="eyebrow">From the blog</span><h2>Katy roofing guides for homeowners</h2><p>Straight talk on costs, claims, materials and storm prep, written for Katy homes.</p></div>
<a class="btn btn-ghost" href="/blog/">All articles {icon('arrow')}</a></div>
<div class="grid g3">{posts}</div>
</div>
</section>

{B.faq_html(HOME_FAQS, "Questions homeowners ask their Katy roofer")}

<section class="section">
<div class="wrap split">
<div data-reveal="left">
<span class="eyebrow">Why choose us</span>
<h2>The difference a local Katy roofer makes</h2>
<p>After every big storm, out-of-town crews flood Katy with door-knockers and yard signs. Many are gone before the first warranty question comes up. Choosing a Katy roofer means choosing someone who will still be here next storm season.</p>
<ul class="checks">
<li>{icon('check-circle')}<span><strong>Photo-first honesty:</strong> you see every issue we find before we recommend anything</span></li>
<li>{icon('check-circle')}<span><strong>No deductible games:</strong> we follow Texas law and never waive or "cover" deductibles</span></li>
<li>{icon('check-circle')}<span><strong>Itemized estimates:</strong> materials, underlayment, flashing, vents and decking spelled out</span></li>
<li>{icon('check-circle')}<span><strong>Clean job sites:</strong> tarps over landscaping and a magnetic nail sweep at the end</span></li>
</ul>
<p>Whether you need a quick leak repair or a complete re-roof, the first step with this Katy roofer is always the same: a free inspection and an honest answer.</p>
</div>
<div class="media">{img('home-porch', 'Two-story home with a new roof in Katy, TX')}</div>
</div>
</section>

{B.final_cta("Ready for a Katy roofer who tells it straight?")}
"""
    faq = B.faq_schema(HOME_FAQS)
    html = B.page("/", "Katy Roofer | Free Roof Inspections & Roofing in Katy, TX",
                  "Katy Roofer: local roofer in Katy, TX for roof repair, replacement and hail damage. Free roof inspections with photo reports. Call (512) 297-7580.",
                  main, active="/", schema=[faq], preload="hero-roofer", scripts=("weather",))
    B.add("/", html, priority="1.0")
