"""Homepage. Primary keyword: "Alabama Insurance Appraiser" (used 14+ times in body copy)."""

from components import (BIZ, CITIES, IMG, SERVICES, TOOLS, btn, call_btn, card, checklist, contact_form,
                        faq_html, faq_schema, grid, icon, kicker, section_head, steps_html, url, ORG_ID)

KW = "Alabama Insurance Appraiser"

FAQS = [
    ("What does an Alabama Insurance Appraiser do?",
     "<p>An Alabama Insurance Appraiser evaluates the <strong>amount of a property loss</strong> when the policyholder and the insurance company disagree on what it will cost to repair or replace the damage. The work covers the inspection, measurements, repair scope, line-item pricing, competing estimates and the documentation that supports a final number under the policy's appraisal clause.</p>"),
    ("When should I consider insurance appraisal?",
     "<p>Appraisal is worth considering when the carrier has accepted that a loss happened but the two sides are still apart on <em>how much</em> it is worth &mdash; after estimates, supplements and re-inspections have been exchanged. The exact right to appraisal, the deadlines and the procedure come from your policy, so read the appraisal provision first.</p>"),
    ("Does appraisal decide whether my claim is covered?",
     "<p>Generally, no. Appraisal resolves the value of the loss, not every coverage question. If the carrier has denied that the policy covers the damage at all, that is usually a coverage issue that may call for legal advice rather than appraisal alone.</p>"),
    ("How much does an insurance appraiser cost?",
     "<p>Fees depend on the size and complexity of the loss and are agreed in writing before work begins. Under most appraisal clauses each side pays its own appraiser and the two sides split the umpire's fee. Ask any appraiser how the fee is calculated before you sign.</p>"),
    ("Do you handle commercial and multi-family claims?",
     "<p>Yes. Our Alabama Insurance Appraiser services cover single-family homes and condos as well as office, retail, apartment, church, warehouse, industrial and institutional property &mdash; claims where the estimate can run to hundreds of line items.</p>"),
    ("Which estimating platforms do you use?",
     "<p>We write and review estimates in <strong>Xactimate</strong> and <strong>Symbility</strong>, the two platforms most carriers use, and capture properties with <strong>Matterport</strong> 3D scanning when a digital record of rooms, measurements and damage will help.</p>"),
    ("Do you work outside Birmingham?",
     "<p>Yes &mdash; statewide. We take assignments in Huntsville, Montgomery, Mobile, Tuscaloosa, Hoover, Auburn, Dothan, Decatur, Florence, Gadsden and the smaller towns and rural counties in between, from the Tennessee Valley to the Gulf Coast.</p>"),
    ("How long does insurance appraisal take?",
     "<p>A well-documented residential claim can resolve in a few weeks once both appraisers are named; large commercial losses take longer. Inspection scheduling, the number of disputed items and whether an umpire is needed drive the timeline.</p>"),
]


def page():
    p = {
        "path": "/",
        "title": "Alabama Insurance Appraiser | Property Claim Appraisal &amp; Estimates",
        "og_title": "Alabama Insurance Appraiser — Independent Property Claim Appraisal",
        "description": "Alabama Insurance Appraiser: independent property insurance appraisal, Xactimate estimates and claim documentation for home and business claims statewide.",
        "crumbs": [("Home", "/")],
        "hero_img": "home",
        "layout": "raw",
        "nav_active": "/",
        "body_class": "home",
        "preload": '<link rel="preload" as="image" href="/assets/img/alabama-insurance-appraiser-home.webp" fetchpriority="high">\n',
        "priority": "1.0",
        "changefreq": "weekly",
    }
    p["schema"] = [faq_schema(p, FAQS), {
        "@type": "ItemList", "@id": url("/#services"), "name": "Alabama Insurance Appraiser services",
        "itemListElement": [{"@type": "ListItem", "position": n, "url": url(f"/services/{s}/"), "name": nm}
                            for n, (s, nm, _, _) in enumerate(SERVICES, 1)]}]

    svc_cards = [card(n, b, f"/services/{s}/", i) for s, n, b, i in SERVICES[:6]]
    tool_cards = [card(n, b, f"/tools/{s}/", i, link_label="Open tool") for s, n, b, i in TOOLS[:4]]
    cities = "".join(f'<a class="city" href="/service-areas/{s}/"><span>{c}<small>Insurance appraisal</small></span>{icon("arrow", "ico ico-sm")}</a>'
                     for c, s in CITIES)
    cities += f'<a class="city city-statewide" href="/service-areas/"><span>All of Alabama<small>67 counties served</small></span>{icon("map", "ico ico-sm")}</a>'
    marquee_items = ["Hail damage", "Tornado &amp; wind", "Hurricane losses", "Water damage", "Fire &amp; smoke",
                     "Commercial roofs", "Multi-family", "Churches", "Xactimate", "Symbility", "Matterport", "Umpire-ready reports"]
    mq = "".join(f"<span>{m}</span>" for m in marquee_items) * 2

    p["body"] = f'''
<section class="hero">
  <div class="hero-bg" style="background-image:url('/assets/img/{IMG["home"][0]}')" aria-hidden="true"></div>
  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="container hero-inner">
    <div>
      {kicker("Independent property claim appraisal &middot; Statewide")}
      <h1 data-split>Alabama Insurance Appraiser <span class="grad-text">for Disputed Property Claims</span></h1>
      <p class="hero-lead">When your insurance company's number and your contractor's number don't match, Alabama Insurance Appraiser finds out why. We inspect, measure, estimate and document the real amount of loss for homeowners, commercial owners, contractors and attorneys across Alabama.</p>
      <div class="hero-actions">{btn("Speak with an appraiser", "tel:" + BIZ["phone_href"], "primary", "phone")}{btn("Explore services", "/services/", "ghost-light")}</div>
      <p class="hero-note">{icon("shield", "ico ico-xs")} Appraisal rights, deadlines and procedures depend on the wording of your insurance policy.</p>
    </div>
    <div class="hero-badges" aria-label="Highlights">
      <div class="hero-badge glass">{'<span class="card-ico">' + icon("scale") + '</span>'}<div><strong>Insurance Appraisal</strong><span>Independent amount-of-loss review</span></div></div>
      <div class="hero-badge glass">{'<span class="card-ico">' + icon("file") + '</span>'}<div><strong>Xactimate &amp; Symbility</strong><span>Line-item estimating</span></div></div>
      <div class="hero-badge glass">{'<span class="card-ico">' + icon("cube") + '</span>'}<div><strong>Matterport 3D</strong><span>Digital property documentation</span></div></div>
      <div class="hero-badge glass">{'<span class="card-ico">' + icon("building") + '</span>'}<div><strong>Residential + Commercial</strong><span>All 67 Alabama counties</span></div></div>
    </div>
  </div>
  <span class="scroll-cue" aria-hidden="true"></span>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}</div></div>

<section class="section section-white" style="padding-top:0;padding-bottom:0">
  <div class="container">
    <div class="stats">
      <div class="stat reveal"><strong><span data-count="67">67</span></strong><span>Alabama counties covered, from the Shoals to the Gulf Coast</span></div>
      <div class="stat reveal"><strong><span data-count="11">11</span><em>+</em></strong><span>Core appraisal, estimating and documentation services</span></div>
      <div class="stat reveal"><strong><span data-count="3">3</span></strong><span>Platforms: Xactimate, Symbility and Matterport</span></div>
      <div class="stat reveal"><strong><span data-count="5">5</span></strong><span>Free claim tools and calculators on this site</span></div>
    </div>
  </div>
</section>

<section class="section section-white" id="about">
  <div class="container split">
    <div class="reveal reveal-left">
      {kicker("Why property owners call us")}
      <h2>An Alabama Insurance Appraiser who looks behind the bottom line</h2>
      <p class="lead-big">Two estimates can be $30,000 apart and still agree on most of the house. The difference usually hides in a few dozen line items.</p>
      <p>Comparing two totals tells you almost nothing. As an independent Alabama Insurance Appraiser, we break each estimate down to the measurements, materials, quantities, labor, access, repair method and code items behind it, then build a supported amount-of-loss position you can actually defend.</p>
      <p>That focus stays on the <strong>amount of loss</strong> and on the appraisal procedure your policy sets out &mdash; not on reopening the whole claim.</p>
      {checklist(["Roof, siding and exterior storm damage", "Interior water and plumbing losses", "Fire, smoke and soot restoration scope", "Commercial and multi-family buildings"], "checklist two-col")}
      <div class="hero-actions">{btn("About our approach", "/about-us/", "ghost")}{btn("How appraisal works", "/insurance-appraisal-process/", "soft", "list")}</div>
    </div>
    <div class="frame reveal reveal-right">
      <div class="img-zoom"><img src="/assets/img/roof-water-damage-appraisal.webp" srcset="/assets/img/roof-water-damage-appraisal-720.webp 720w, /assets/img/roof-water-damage-appraisal.webp 1500w" sizes="(max-width: 760px) 100vw, 560px" width="1500" height="1000" alt="Water running off damaged roof shingles during an Alabama storm" loading="lazy"></div>
      <div class="frame-badge"><span class="card-ico">{icon("search")}</span>Property-specific documentation, not generic repair figures</div>
    </div>
  </div>
</section>

<section class="section section-aqua" id="services">
  <div class="container">
    {section_head("Appraisal &amp; estimating services", "What Alabama Insurance Appraiser does for your claim", "Every service is built to make a valuation disagreement easier to understand &mdash; and easier to resolve.", True)}
    {grid(svc_cards, 3)}
    <p class="center" style="margin-top:36px">{btn("View all 11 services", "/services/", "primary")}</p>
  </div>
</section>

<section class="section section-white">
  <div class="container split flip">
    <div class="reveal reveal-right">
      {kicker("Storm season in Alabama")}
      <h2>Storm damage may look obvious. The cost to repair it rarely is.</h2>
      <p>Alabama sees spring tornado outbreaks across Dixie Alley, large hail in the Tennessee Valley and the Birmingham metro, and hurricane-force wind on the Gulf Coast. The damage is easy to photograph; the repair scope behind it is not.</p>
      <p>Roof systems, flashing, ventilation, gutters, siding, windows, interior water intrusion, code upgrades, matching, access and repair sequencing all change the number. An Alabama Insurance Appraiser reviews the <em>complete</em> scope, not just the headline damage.</p>
      {btn("Wind &amp; storm damage appraisal", "/services/wind-storm-damage-appraisal/", "ghost")}
    </div>
    <div class="frame reveal reveal-left">
      <div class="img-zoom"><img src="/assets/img/storm-damage-alabama-homes.webp" srcset="/assets/img/storm-damage-alabama-homes-720.webp 720w, /assets/img/storm-damage-alabama-homes.webp 1600w" sizes="(max-width: 760px) 100vw, 560px" width="1600" height="1066" alt="Dark storm clouds over Alabama homes before a severe weather event" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section section-dark" id="process">
  <div class="container split" style="align-items:start">
    <div class="reveal">
      {section_head("The appraisal process", "How insurance appraisal usually unfolds in Alabama", "Every policy is different, but when an appraisal clause applies and is properly invoked, most claims follow a similar path.")}
      <p>Alabama courts treat appraisal as a contract process that is separate from arbitration, which is why the exact wording of your policy matters so much. An experienced Alabama Insurance Appraiser starts there &mdash; with the appraisal provision itself.</p>
      {btn("Read the full process guide", "/insurance-appraisal-process/", "light")}
    </div>
    {steps_html([
        ("Review the policy language", "Confirm the appraisal provision, the written-demand requirement, deadlines and how an umpire is chosen."),
        ("Identify the disputed amount", "Line up the estimates, photos, measurements and correspondence to pin down exactly where the numbers differ."),
        ("Appraisers evaluate the loss", "Each side's appraiser inspects, measures and builds a supported position on the amount of loss."),
        ("Resolve remaining differences", "Items the appraisers can't agree on go to the umpire under the policy's procedure, and an award is signed."),
    ])}
  </div>
</section>

<section class="section section-sand">
  <div class="container">
    {section_head("Property claim types", "Losses an Alabama Insurance Appraiser evaluates", "Residential and commercial claims involve very different scopes, so the valuation approach adapts to the building and the damage.", True)}
    {grid([
        card("Hail Damage", "Roof coverings, soft metals, gutters, siding, screens and exterior finishes.", "/services/hail-damage-appraisal/", "hail"),
        card("Wind, Tornado &amp; Hurricane", "Roofing, windows, doors, fences and the building envelope.", "/services/wind-storm-damage-appraisal/", "wind"),
        card("Water Losses", "Drywall, flooring, cabinetry, insulation and hidden moisture.", "/services/water-damage-appraisal/", "droplets"),
        card("Fire &amp; Smoke", "Structure, cleaning, demolition, rebuild and repair sequencing.", "/services/fire-smoke-damage-appraisal/", "flame"),
        card("Residential Property", "Single-family homes, townhomes, condos and rental houses.", "/services/residential-property-appraisal/", "home"),
        card("Commercial &amp; Multi-Family", "Office, retail, apartments, churches, warehouses and schools.", "/services/commercial-property-appraisal/", "building"),
    ], 3)}
  </div>
</section>

<section class="section section-white" id="tools">
  <div class="container">
    {section_head("Free claim tools", "Run the numbers before you call", "Free calculators and checklists our Alabama Insurance Appraiser team built for policyholders. Nothing to download, nothing stored on our servers.", True)}
    {grid(tool_cards, 4)}
    <p class="center" style="margin-top:36px">{btn("See all tools", "/tools/", "ghost", "calculator")}</p>
  </div>
</section>

<section class="section section-aqua" id="areas">
  <div class="container">
    {section_head("Serving the state of Alabama", "Alabama Insurance Appraiser service areas", "From North Alabama to the Gulf Coast &mdash; metro areas, growing suburbs, small towns and rural property.", True)}
    <div class="city-grid">{cities}</div>
  </div>
</section>

<section class="section section-white">
  <div class="container">
    {section_head("Why this approach works", "Clear documentation makes valuation differences easier to resolve", "", True)}
    {grid([
        card("Detailed, not generic", "Repair cost depends on the actual materials, measurements, configuration, access and conditions at your property &mdash; not a broad damage category.", None, "target"),
        card("Differences get organized", "Line-item comparison separates disagreements over quantity, scope, labor, material, pricing and method so each can be resolved on its own.", None, "compare"),
        card("Evidence supports the number", "Photos, measurements, Xactimate or Symbility estimates and Matterport scans make an Alabama Insurance Appraiser's position easy to follow.", None, "camera"),
    ], 3)}
  </div>
</section>

<section class="section section-sand" id="faq">
  <div class="container split" style="align-items:start">
    <div class="reveal">
      {section_head("Frequently asked questions", "Insurance appraisal questions, answered", "Straight answers from an Alabama Insurance Appraiser. For more, see the full FAQ.")}
      <div class="hero-actions">{btn("All FAQs", "/faq/", "ghost", "help")}{btn("Claim glossary", "/glossary/", "soft", "book")}</div>
    </div>
    {faq_html(FAQS)}
  </div>
</section>

<section class="section section-white">
  <div class="container">
    {section_head("Guides &amp; resources", "Learn before you invoke appraisal", "", True)}
    {grid([
        card("What Does an Insurance Appraiser Do?", "The appraiser's role, what gets inspected, how the amount of loss is decided and what appraisal can't do.", "/what-does-an-insurance-appraiser-do/", "book", link_label="Read guide"),
        card("How to Invoke Appraisal in Alabama", "Written demand, deadlines, choosing your appraiser and what happens next.", "/how-to-invoke-the-appraisal-clause-in-alabama/", "file", link_label="Read guide"),
        card("Appraisal vs. Public Adjuster vs. Attorney", "Who does what on a disputed claim, and when each one makes sense.", "/insurance-appraiser-vs-public-adjuster-vs-attorney/", "users", link_label="Read guide"),
    ], 3)}
  </div>
</section>

<section class="section section-dark" id="contact">
  <div class="container split" style="align-items:start">
    <div class="reveal">
      {kicker("Discuss your property claim")}
      <h2>Looking for an Alabama Insurance Appraiser?</h2>
      <p class="section-lead" style="margin-bottom:26px">Share the property location, the type of loss and a few details about the disagreement. We'll tell you which appraisal, estimating or documentation service fits &mdash; or if appraisal isn't the right tool.</p>
      <div class="contact-cards">
        <a class="contact-card" href="tel:{BIZ['phone_href']}"><span class="card-ico">{icon("phone")}</span><span><small>Call or text</small><strong>{BIZ['phone_display']}</strong></span></a>
        <a class="contact-card" href="mailto:{BIZ['email']}"><span class="card-ico">{icon("mail")}</span><span><small>Email</small><strong>{BIZ['email']}</strong></span></a>
        <div class="contact-card"><span class="card-ico">{icon("map")}</span><span><small>Service area</small><strong>Statewide &mdash; all of Alabama</strong></span></div>
      </div>
    </div>
    <div class="form-shell reveal">{contact_form(compact=True)}</div>
  </div>
</section>
'''
    return p
