"""Homepage for missouricityroofs.com. Primary keyword: "Missouri City roofers" (14+ uses in the main content)."""
import build as B
from build import e, icon, img, TEL, PHONE

HOME_FAQS = [
    {"q": "Is the roof inspection really free?",
     "a": "Yes. Inspections are free for Missouri City homeowners with no obligation to hire us. You get photos of what we find and an honest recommendation, even when the answer is that your roof is fine."},
    {"q": "How do I know if hail hit my roof?",
     "a": "Hail damage is rarely visible from the street. Look for dents on gutters, downspouts, AC fins and mailboxes, and granules collecting at downspout outlets. If you see any of that, book a free inspection so a roofer can check the shingles up close and document what's there."},
    {"q": "Will you help with my insurance claim?",
     "a": "We photograph and measure storm damage, explain what we found and can meet your adjuster on the roof. We are roofers, not public adjusters, and we never waive or rebate deductibles, which is illegal in Texas."},
    {"q": "How long does a roof replacement take?",
     "a": "Most single-family homes in Missouri City are torn off and re-roofed in one to two days once materials arrive. Steep pitches, rotten decking and weather can add time, and you'll get a schedule up front."},
    {"q": "What does a new roof cost in Missouri City, TX?",
     "a": "Architectural shingle replacements on typical Missouri City homes commonly land in the low-to-mid five figures, depending on roof size, pitch and material. Try the estimator on this page for a planning range, then book a free inspection for an exact written price."},
    {"q": "Do you work with HOAs in Sienna and Riverstone?",
     "a": "Yes. Sienna, Riverstone and many other communities have rules on shingle color and material. We help you pick an approved product and put together the specs the architectural review committee usually asks for."},
    {"q": "My Quail Valley home has an older roof. Repair or replace?",
     "a": "Isolated damage on a roof under about 12 to 15 years old is usually a repair. Brittle or curling shingles, repeated leaks or widespread hail bruising usually point to replacement. We'll show you photos and price both when both make sense."},
    {"q": "Which ZIP codes do you serve?",
     "a": "All of Missouri City (77459 and 77489) plus Sienna, Sugar Land, Stafford, Pearland, Fresno and Richmond."},
]

SEASONS = [
    ("Jan", "cold", "Cold fronts & rare freezes", "Wind behind cold fronts lifts tired shingles. A hard freeze like Winter Storm Uri in 2021 can split pipe boots and back water up at the eaves.", "Clear gutters; check pipe boots and attic for stains."),
    ("Feb", "cold", "Late freezes, gusty fronts", "Gusty north winds test ridge caps and loose flashing on older Quail Valley and Hunters Glen roofs.", "Schedule a pre-spring inspection while crews are available."),
    ("Mar", "hail", "Hail season starts", "Spring storm lines build along the Gulf moisture boundary. Hail and straight-line wind are the main roof threats through June.", "Photograph your roof now so you have a 'before' record."),
    ("Apr", "hail", "Peak hail & severe storms", "The busiest month for hail reports around Fort Bend County. Damage often hides until the next heavy rain.", "Inspect after every hail report, even if nothing looks wrong."),
    ("May", "hail", "Severe storms & derechos", "Fast-moving wind storms like the May 2024 derecho can peel shingles across whole neighborhoods in minutes.", "Trim limbs over the roof; secure patio items."),
    ("Jun", "storm", "Hurricane season opens", "Tropical moisture brings flooding rain. Gutters and valleys get tested hard.", "Pre-season inspection; fix loose shingles before named storms."),
    ("Jul", "storm", "Tropical storms & heat", "Hurricane Beryl (July 2024) showed how wind and fallen trees can hit Fort Bend County. Attic heat peaks too.", "Check ventilation, sealants and trees near the house."),
    ("Aug", "storm", "Peak heat & tropics", "Long, hot days bake shingles from below and dry out sealant. The tropics stay active.", "Watch for curling shingles and cracked pipe boots."),
    ("Sep", "storm", "Peak hurricane season", "Historically the most active month for Gulf storms. Heavy rain finds every weak spot.", "Keep a tarp plan and our number handy."),
    ("Oct", "calm", "Best window for projects", "Milder temperatures and fewer storms make fall the best time for replacements and repairs.", "Book replacements and repairs before winter."),
    ("Nov", "calm", "Leaf season", "Leaves from mature oaks clog gutters and valleys, and trapped debris holds moisture against shingles.", "Clean gutters and valleys; look for algae streaks."),
    ("Dec", "cold", "Holiday lull, first fronts", "Quieter weather, but the first strong fronts arrive. A good time to plan next year's roof work.", "Get estimates and insurance questions sorted early."),
]


def build_home():
    svc_rows = "".join(
        f"""<li class="svc-row" data-reveal><a href="/services/{s['slug']}/"><span class="svc-n">{i + 1:02d}</span>
<span class="svc-ico">{icon(s.get('icon', 'home'))}</span><span class="svc-t"><b>{e(s['name'])}</b><span>{e(s['short'])}</span></span>
<span class="svc-go">{icon('arrow')}</span></a></li>""" for i, s in enumerate(B.SERVICES))

    posts = "".join(
        f"""<article class="post-card" data-reveal><a class="pc-img" href="/blog/{p['slug']}/" tabindex="-1" aria-hidden="true">{img(p['image'], p.get('image_alt', p['h1']))}</a>
<div class="pc-body"><div class="pc-meta"><span class="tag">{e(p.get('category', 'Guide'))}</span><span>{B.fmt_date(p['date'])}</span></div>
<h3><a href="/blog/{p['slug']}/">{e(p['h1'])}</a></h3><p>{e(p['excerpt'])}</p></div></article>""" for p in B.POSTS[:3])

    areas = "".join(f'<li><a href="/areas/{a["slug"]}/"><b>{e(a["name"])}</b><span>{e(a.get("drive", ""))}</span>{icon("arrow")}</a></li>' for a in B.AREAS)

    months = "".join(f'<button type="button" class="m m-{k}" data-month="{i}" aria-pressed="{"true" if i == 0 else "false"}">{m}</button>'
                     for i, (m, k, *_rest) in enumerate(SEASONS))
    season_data = "".join(f'<div class="season" data-season="{i}"{"" if i == 0 else " hidden"}><span class="s-tag s-{k}">{e(t)}</span><p>{e(d)}</p><p class="s-do">{icon("check-circle")} <b>Do this:</b> {e(do)}</p></div>'
                          for i, (m, k, t, d, do) in enumerate(SEASONS))

    main = f"""
<section class="hero">
<div class="wrap hero-grid">
<div class="hero-text">
<span class="kicker" data-reveal>{icon('pin')} Missouri City, TX · Fort Bend County</span>
<h1 data-reveal>Missouri City Roofers who show you the damage <em>before</em> they quote the job</h1>
<p class="lead" data-reveal>We are Missouri City roofers for homeowners who want proof, not pressure: a free inspection with photos of every problem, a written estimate you can actually read, and repairs or replacements built for Gulf Coast heat, hail and hurricanes.</p>
<div class="actions" data-reveal><a class="btn" href="/free-roof-inspection/">Book a free inspection {icon('arrow')}</a>
<a class="btn btn-line" href="tel:{TEL}">{icon('phone')} {PHONE}</a></div>
<ul class="hero-points" data-reveal><li>{icon('camera')} Photo report on every visit</li><li>{icon('file-check')} Itemized written estimates</li><li>{icon('shield')} No deductible games, ever</li></ul>
</div>
<div class="hero-media" data-reveal>
<div class="hm-frame">{img('hero-home', 'Brick two-story home with an architectural shingle roof in Missouri City, Texas', eager=True)}</div>
<div class="wx-chip" data-wx-chip><span class="dot"></span><span>Missouri City weather loading…</span></div>
<div class="hm-badge"><b>$0</b><span>roof inspections for Missouri City homeowners</span></div>
</div>
</div>
<div class="wrap">{B.quote_bar()}</div>
</section>

<section class="proof">
<div class="wrap proof-grid">
<div data-reveal><b>$<em data-count="0">0</em></b><span>Cost of a roof inspection</span></div>
<div data-reveal><b><em data-count="2">0</em></b><span>Missouri City ZIP codes: 77459 &amp; 77489</span></div>
<div data-reveal><b><em data-count="7">0</em></b><span>Communities served in Fort Bend &amp; beyond</span></div>
<div data-reveal><b><em data-count="3">0</em></b><span>Free homeowner tools, plus live Storm Watch</span></div>
</div>
</section>

<section class="section">
<div class="wrap intro-grid">
<div class="intro-img" data-reveal>{img('roofer-work', 'Missouri City roofers working on the shingle roof of a brick home')}<span class="img-cap">Every job starts on the roof, not in a sales pitch.</span></div>
<div data-reveal>
<span class="kicker">Local Missouri City roofing</span>
<h2>Roofs here take a beating. Missouri City roofers should know why.</h2>
<p>Missouri City sits in the path of almost everything the Gulf Coast can throw at a roof. Summer attics hit punishing temperatures, humidity feeds algae and soft decking, spring storm lines drop hail across Fort Bend County, and hurricane season brings wind that finds every loose shingle. Experienced Missouri City roofers plan a roof around all of it, not just the next rain.</p>
<p>The housing stock matters too. Many homes in Quail Valley, Hunters Glen and Fondren Park were built in the 1970s through the 1990s and are on their second or third roof, often under big shade trees. Newer homes in Sienna and Riverstone come with HOA rules on shingle color and style. We know the difference, and we size every estimate to the house in front of us.</p>
<p>What homeowners tell us they want from Missouri City roofers is simple: answer the phone, show up when promised, and don't inflate the job. That's the standard on every roof we touch.</p>
<a class="link-arrow" href="/about/">How we work {icon('arrow')}</a>
</div>
</div>
</section>

<section class="section sec-cream">
<div class="wrap svc-wrap">
<div class="sec-head sticky" data-reveal><span class="kicker">Services</span><h2>What our Missouri City roofers do</h2>
<p>One leak or a full tear-off after a hailstorm, every job starts with a free inspection and a photo report.</p>
<a class="btn" href="/free-roof-inspection/">Start with a free inspection {icon('arrow')}</a></div>
<ol class="svc-list">{svc_rows}</ol>
</div>
</section>

<section class="section storm" id="storm-watch">
<div class="wrap storm-grid">
<div data-reveal>
<span class="kicker light">{icon('cloud-rain')} Storm Watch</span>
<h2>Live Missouri City weather, read by a roofer</h2>
<p>Current conditions and a 3-day look ahead for Missouri City, with a plain-English roof-risk rating for hail and high wind. Open Storm Watch for National Weather Service alerts and the full 7-day forecast.</p>
<div class="wx-panel" data-wx-mini><p>Loading current conditions…</p></div>
</div>
<div class="season-box" data-reveal data-seasons>
<h3>Missouri City roof calendar</h3>
<p class="muted-light">Tap a month to see what it does to your roof.</p>
<div class="months" role="group" aria-label="Choose a month">{months}</div>
{season_data}
<div class="legend"><span class="s-hail">Hail</span><span class="s-storm">Tropical</span><span class="s-cold">Fronts / freeze</span><span class="s-calm">Project window</span></div>
</div>
</div>
</section>

<section class="section">
<div class="wrap check-grid">
<div data-reveal>
<span class="kicker">Free roof inspections</span>
<h2>The 6-point inspection our Missouri City roofers run on every home</h2>
<p>Most roof damage can't be seen from the driveway. Hail bruises, lifted tabs, cracked pipe boots and failing flashing hide until water shows up on a ceiling. Our inspection puts a roofer on every slope with a camera, so you see exactly what we see.</p>
<a class="btn" href="/free-roof-inspection/">Schedule my free inspection {icon('arrow')}</a>
</div>
<ol class="check-list-6" data-reveal>
<li>{icon('cloud-hail')}<div><b>Shingles &amp; surface</b><span>Hail bruising, granule loss, creases and lifted tabs</span></div></li>
<li>{icon('layers')}<div><b>Flashing &amp; valleys</b><span>Walls, chimneys, valleys, exposed nails and sealant</span></div></li>
<li>{icon('wind')}<div><b>Ridge, vents &amp; boots</b><span>Ridge caps, turbines, box vents and pipe boots</span></div></li>
<li>{icon('droplets')}<div><b>Gutters &amp; soft metals</b><span>Dents that confirm hail size; clogs and fascia rot</span></div></li>
<li>{icon('thermo')}<div><b>Attic &amp; ventilation</b><span>Moisture, daylight, decking condition and airflow</span></div></li>
<li>{icon('leaf')}<div><b>Trees &amp; algae</b><span>Overhanging limbs, debris traps and black streaks</span></div></li>
</ol>
</div>
</section>

<section class="section sec-sage">
<div class="wrap est-grid">
<div data-reveal>
<span class="kicker">Quick estimator</span>
<h2>What might a new roof cost on your home?</h2>
<p>Slide to your home's size and pick a material for a 2026 planning range for the Missouri City market. For pitch, layers and decking, open the <a href="/tools/roof-cost-calculator/">full roof cost calculator</a>.</p>
<ul class="tool-links">
<li><a href="/tools/roof-cost-calculator/">{icon('calculator')} Roof Cost Calculator {icon('arrow')}</a></li>
<li><a href="/tools/roof-pitch-calculator/">{icon('ruler')} Roof Pitch &amp; Area Calculator {icon('arrow')}</a></li>
<li><a href="/tools/storm-damage-checklist/">{icon('clipboard')} Storm Damage Self-Check {icon('arrow')}</a></li>
</ul>
</div>
<form class="mini-est" data-tool="mini" onsubmit="return false" data-reveal>
<label for="mini-sqft">Home living area <output for="mini-sqft"></output></label>
<input type="range" id="mini-sqft" name="sqft" min="1200" max="5000" step="50" value="2500" data-fmt=" sq ft">
<label>Stories</label>
<div class="seg"><label><input type="radio" name="stories" value="1"><span>1 story</span></label><label><input type="radio" name="stories" value="2" checked><span>2 stories</span></label></div>
<label>Material</label>
<div class="seg"><label><input type="radio" name="material" value="arch" checked><span>Architectural</span></label><label><input type="radio" name="material" value="class4"><span>Class 4 impact</span></label><label><input type="radio" name="material" value="metal"><span>Standing-seam metal</span></label></div>
<div class="mini-out" aria-live="polite"><small>Planning range</small><b data-out="range">—</b><span data-out="note"></span></div>
<a class="btn btn-block" href="/free-roof-inspection/">Get an exact written quote, free {icon('arrow')}</a>
</form>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="sec-head center" data-reveal><span class="kicker">How it works</span><h2>From first call to final walkthrough</h2>
<p>Hiring Missouri City roofers shouldn't feel like a gamble. Here's exactly what happens, start to finish.</p></div>
<ol class="timeline">
<li data-reveal><span>1</span><h3>Call or book online</h3><p>Tell us about the leak, the storm or the aging roof. We set a time that suits you.</p></li>
<li data-reveal><span>2</span><h3>Free inspection</h3><p>Roof, flashing, vents, gutters and attic, all photographed, good and bad.</p></li>
<li data-reveal><span>3</span><h3>Written options</h3><p>An itemized estimate in plain English. Storm damage? We explain the claim process.</p></li>
<li data-reveal><span>4</span><h3>Built right</h3><p>Tear-off, decking repair, synthetic underlayment, new flashing and balanced ventilation.</p></li>
<li data-reveal><span>5</span><h3>Walkthrough</h3><p>Completion photos, a magnetic nail sweep and care tips for your new roof.</p></li>
</ol>
</div>
</section>

<section class="section sec-cream">
<div class="wrap rr-grid">
<div data-reveal><span class="kicker">Repair or replace?</span><h2>The honest answer depends on your roof</h2>
<p>We'll always tell you when a repair will do. Flip between the two to see how we think about it.</p>
<div class="rr-switch" role="tablist" aria-label="Repair or replace">
<button type="button" role="tab" aria-selected="true" aria-controls="rr-repair" id="rr-t1" data-rr="repair">{icon('hammer')} Usually a repair</button>
<button type="button" role="tab" aria-selected="false" aria-controls="rr-replace" id="rr-t2" data-rr="replace">{icon('home')} Usually a replacement</button></div></div>
<div class="rr-panels" data-reveal>
<div class="rr-panel" id="rr-repair" role="tabpanel" aria-labelledby="rr-t1"><ul class="ticks">
<li>{icon('check')} A few missing or lifted shingles after wind</li><li>{icon('check')} One leak at a pipe boot, vent or chimney</li>
<li>{icon('check')} Roof under about 12 years old with localized damage</li><li>{icon('check')} Flashing or sealant failure in one area</li></ul>
<a class="link-arrow" href="/services/roof-repair-missouri-city-tx/">Roof repair in Missouri City {icon('arrow')}</a></div>
<div class="rr-panel" id="rr-replace" role="tabpanel" aria-labelledby="rr-t2" hidden><ul class="ticks">
<li>{icon('check')} Hail bruising across several slopes</li><li>{icon('check')} Curling, cracking or brittle shingles; heavy granule loss</li>
<li>{icon('check')} Recurring leaks or soft, sagging decking</li><li>{icon('check')} Roof 18+ years old, or an approved insurance claim</li></ul>
<a class="link-arrow" href="/services/roof-replacement-missouri-city-tx/">Roof replacement in Missouri City {icon('arrow')}</a></div>
</div>
</div>
</section>

<section class="section">
<div class="wrap vs-wrap">
<div class="sec-head" data-reveal><span class="kicker">Why local matters</span><h2>Local Missouri City roofers vs. storm chasers</h2>
<p>After every big storm, out-of-town crews flood Fort Bend County with door-knockers and yard signs. Here's how to tell the difference.</p></div>
<div class="vs-table" data-reveal role="table" aria-label="Local roofers compared with storm chasers">
<div class="vs-row vs-head" role="row"><span role="columnheader"></span><span role="columnheader">{icon('home')} Us</span><span role="columnheader">{icon('alert')} Typical storm chaser</span></div>
<div class="vs-row" role="row"><span role="rowheader">After the job</span><span role="cell">Same phone number, still here next season</span><span role="cell">Gone when the storms move on</span></div>
<div class="vs-row" role="row"><span role="rowheader">Proof of damage</span><span role="cell">Photo report before any recommendation</span><span role="cell">"Trust me, you need a new roof"</span></div>
<div class="vs-row" role="row"><span role="rowheader">Your deductible</span><span role="cell">Paid by you, as Texas law requires</span><span role="cell">"We'll cover it" (illegal in Texas)</span></div>
<div class="vs-row" role="row"><span role="rowheader">Estimate</span><span role="cell">Itemized: underlayment, flashing, vents, decking</span><span role="cell">One number on a napkin</span></div>
<div class="vs-row" role="row"><span role="rowheader">Pressure</span><span role="cell">Take your time; the inspection is free</span><span role="cell">"Sign today or lose the price"</span></div>
</div>
<p data-reveal>That's the case for hiring Missouri City roofers you can find again. Read <a href="/blog/how-to-hire-a-roofer-in-missouri-city/">how to hire a roofer in Missouri City</a> before you sign anything.</p>
</div>
</section>

<section class="section sec-green">
<div class="wrap area-grid">
<div data-reveal>
<span class="kicker light">Service area</span>
<h2>Missouri City first, then the rest of Fort Bend</h2>
<p>We're Missouri City roofers first: Quail Valley, Lake Olympia, Vicksburg, Lexington Village, Colony Lakes, Hunters Glen, Sienna and Riverstone. From Texas Parkway to the Fort Bend Parkway and down to the Brazos River, we cover the whole city and the communities around it.</p>
<p class="zips">ZIP codes: 77459 · 77489 · 77479 · 77477 · 77478 · 77545 · 77406 · 77407 · 77469 · 77584</p>
<a class="btn btn-brass" href="/areas/">All service areas {icon('arrow')}</a>
</div>
<ul class="area-list" data-reveal><li><a href="/"><b>Missouri City</b><span>Home base: 77459 &amp; 77489</span>{icon('arrow')}</a></li>{areas}</ul>
</div>
</section>

<section class="section">
<div class="wrap">
<div class="sec-head row" data-reveal><div><span class="kicker">From the blog</span><h2>Roofing guides for Missouri City homeowners</h2></div>
<a class="btn btn-line" href="/blog/">All articles {icon('arrow')}</a></div>
<div class="post-grid">{posts}</div>
</div>
</section>

{B.faq_html(HOME_FAQS, "Questions homeowners ask Missouri City roofers")}

<section class="section">
<div class="wrap intro-grid flip">
<div data-reveal>
<span class="kicker">Our promise</span>
<h2>Four things you can hold us to</h2>
<ul class="promise">
<li><b>Photo-first honesty.</b> You see every issue before we recommend anything.</li>
<li><b>No deductible games.</b> We follow Texas law and never waive or "cover" deductibles.</li>
<li><b>Itemized estimates.</b> Materials, underlayment, flashing, vents and decking, line by line.</li>
<li><b>Clean job sites.</b> Tarps over landscaping and a magnetic nail sweep before we leave.</li>
</ul>
<p>Quick leak repair or complete re-roof, the first step with these Missouri City roofers is always the same: a free inspection and an honest answer.</p>
</div>
<div class="intro-img" data-reveal>{img('tear-off', 'Roofing crew tearing off old shingles before installing a new roof')}<span class="img-cap">Tear-off down to the deck, so we can see and fix what's underneath.</span></div>
</div>
</section>

{B.final_cta("Ready for Missouri City roofers who tell it straight?")}
"""
    faq = B.faq_schema(HOME_FAQS)
    html = B.page("/", "Missouri City Roofers | Roof Repair & Replacement | (512) 297-7580",
                  "Missouri City Roofers: local roof repair, roof replacement and storm damage help in Missouri City, TX. Free photo-documented inspections. Call (512) 297-7580.",
                  main, active="/", schema=[faq], scripts=("weather", "tools"))
    B.add("/", html, priority="1.0")
