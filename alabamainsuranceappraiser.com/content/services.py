"""/services/ hub and one page per service."""

from components import (BIZ, SERVICES, btn, card, checklist, callout, fig, faq_html, faq_schema, grid, icon,
                        related_links, section_head, service_schema, steps_html, table, url)

SVC = {s: (n, b, i) for s, n, b, i in SERVICES}


def sidebar_links(exclude):
    return [(n, f"/services/{s}/") for s, n, _, _ in SERVICES if s != exclude][:8]


# Each entry: title tag, meta description, h1, lead, hero image, service_type, body sections, faqs, related
DATA = {
    "property-insurance-appraisal": dict(
        title="Property Insurance Appraisal Services in Alabama",
        desc="Independent property insurance appraisal in Alabama. We evaluate the disputed amount of loss, compare estimates and support the number.",
        h1="Property Insurance Appraisal in Alabama",
        lead="An independent evaluation of the amount of loss when you and your insurance carrier can't agree on what the damage will cost to repair.",
        img="inspect", stype="Insurance appraisal",
        body=f"""
<p class="lead-p">Property insurance appraisal is a contract-based way to settle a disagreement over the <strong>amount of loss</strong>. Each side names an appraiser, the appraisers evaluate the damage, and any items they can't agree on go to an umpire. When it works, it resolves a valuation dispute faster and at lower cost than litigation.</p>
<p>Alabama Insurance Appraiser handles the appraiser's side of that process for homeowners, commercial property owners, contractors and attorneys anywhere in the state. The job is narrow on purpose: find out exactly why the estimates differ, decide what the loss is actually worth, and support that number with evidence.</p>
<h2>What our appraisal assignment includes</h2>
{checklist(["Review of the policy's appraisal provision, deadlines and umpire procedure",
            "On-site inspection, measurements and photo documentation of the damaged property",
            "Line-by-line comparison of the carrier's estimate and your contractor's estimate",
            "An independent Xactimate or Symbility estimate where one is needed",
            "Analysis of scope, quantities, materials, labor, access, code and matching issues",
            "Negotiation with the opposing appraiser item by item",
            "Umpire-ready submissions for any items left unresolved",
            "A signed appraisal award that itemizes the agreed amount of loss"], "checklist two-col")}
<h2>When appraisal makes sense</h2>
<p>Appraisal fits best when the carrier agrees there is a covered loss but the two sides are still apart on the number after estimates, supplements and re-inspections have been exchanged. Typical examples:</p>
<ul><li>The carrier allows spot repairs to a roof and your contractor says the slope or the whole roof needs replacement.</li>
<li>Both estimates include the same rooms but the drywall, flooring or paint quantities don't match.</li>
<li>The unit prices, labor hours or overhead and profit in the carrier's estimate don't reflect what the work costs in your market.</li>
<li>A commercial estimate omits code-required items, access equipment or repair sequencing.</li></ul>
{callout("<p>Appraisal decides how much a loss is worth. It generally does not decide whether the policy covers the damage in the first place. If the carrier has denied coverage outright, talk to an attorney about that issue.</p>", "warn", "Appraisal is about value, not coverage")}
<h2>How we develop the amount of loss</h2>
{steps_html([("Read the contract", "We start with your policy's appraisal clause: how a demand is made, how quickly appraisers must be named, appraiser qualifications and how costs are split."),
             ("Gather the record", "Estimates, photos, adjuster notes, engineering reports, invoices and correspondence &mdash; everything that explains how each number was built."),
             ("Inspect and measure", "We document the property ourselves, including roof measurements, room dimensions, materials and conditions, often with Matterport capture."),
             ("Build the position", "Each disputed item gets a supported quantity, price and repair method. Totals come last."),
             ("Negotiate and resolve", "We work through the differences with the other appraiser and present anything left to the umpire.")])}
<h2>Why detail wins appraisals</h2>
<p>A $40,000 gap is rarely one $40,000 disagreement. It is usually thirty or forty smaller ones: a missing starter course, a low waste factor, a ceiling left out of the paint scope, a dumpster that never made the estimate. Appraisers who argue over totals end up splitting the difference. Appraisers who argue line items with evidence get the items that belong.</p>
{fig("roof", "Close-up of water flowing across damaged asphalt shingles", "Roof losses are the most common source of appraisal disputes in Alabama.")}
<h2>Who we work with</h2>
<p>Policyholders hire us directly. We also take appraisal and estimating assignments from roofing and restoration contractors, property managers and attorneys who need an independent, documented valuation.</p>
""",
        faqs=[("Who chooses the appraisers?", "<p>Under most policies each side picks its own appraiser, and the two appraisers then choose an umpire. If they can't agree on an umpire, the policy usually lets either side ask a court to appoint one.</p>"),
              ("Is the appraisal award binding?", "<p>That depends on the policy wording. Many clauses say an award signed by any two of the three (two appraisers, or one appraiser and the umpire) sets the amount of loss. Coverage defenses and other policy terms may still apply.</p>"),
              ("Can I be my own appraiser?", "<p>Most policies require a competent and impartial or disinterested appraiser. Even if self-appointment isn't barred, an experienced appraiser who estimates for a living usually gets a better result.</p>")],
        related=["estimate-review", "xactimate-estimates", "residential-property-appraisal", "commercial-property-appraisal"],
    ),
    "residential-property-appraisal": dict(
        title="Residential Insurance Appraisal in Alabama",
        desc="Homeowner insurance appraisal across Alabama for roof, hail, wind, water and fire claims, for houses, condos and rental property.",
        h1="Residential Property Insurance Appraisal",
        lead="For Alabama homeowners whose claim payment doesn't cover the real cost to put the house back the way it was.",
        img="residential", stype="Residential property insurance appraisal",
        body=f"""
<p class="lead-p">Most residential appraisal disputes start the same way: the adjuster's estimate arrives, the contractor's estimate arrives, and the two are thousands of dollars apart. You're left in the middle with a damaged house and two professionals telling you different things.</p>
<p>Alabama Insurance Appraiser evaluates homeowner claims independently. We look at your house, your materials and your repair scope, then put a supported number on the loss so the disagreement can actually be settled.</p>
<h2>Homes and properties we appraise</h2>
{checklist(["Single-family homes", "Townhomes and patio homes", "Condominium units (interior and HO-6 claims)", "Rental houses and duplexes", "Detached garages, shops and other structures", "Fences, decks and outbuildings"], "checklist two-col")}
<h2>Common residential disputes</h2>
<h3>Roof repair vs. replacement</h3>
<p>The single most common fight. Carriers often allow a handful of replaced shingles; contractors point to brittle or discontinued shingles that can't be repaired without damaging the rest of the slope. The answer depends on the shingle, its condition, repairability testing and whether a reasonable match exists.</p>
<h3>Interior water damage scope</h3>
<p>After a roof leak or plumbing failure, estimates often disagree on how far the damage goes &mdash; how many feet of drywall, whether insulation is wet, whether flooring runs continuously into undamaged rooms, and how much paint is needed for a uniform finish.</p>
<h3>Matching and uniform appearance</h3>
<p>Replacing three courses of siding or one room of flooring that no longer matches the rest of the house is a frequent point of disagreement. How it is resolved depends on the policy language and the specific facts.</p>
<h3>Pricing and overhead &amp; profit</h3>
<p>When a job needs several trades, general contractor overhead and profit is often at issue, along with whether the carrier's unit prices reflect your local market.</p>
{fig("residential", "Suburban Alabama home with a modern exterior after a property claim inspection")}
<h2>What to have ready</h2>
<p>Gather your full policy (including the declarations page), every estimate and supplement, photos and video from right after the loss, receipts for emergency repairs, and the adjuster's letters. Our <a href="/tools/appraisal-readiness-checklist/">appraisal readiness checklist</a> walks through each item.</p>
{callout("<p>Many homeowner policies set deadlines for naming an appraiser after a written demand (often 20 days) and time limits for filing suit. Check your policy and calendar the dates.</p>", "tip", "Watch the clock")}
""",
        faqs=[("Will appraisal raise my premium?", "<p>Using a right your policy gives you is not the same as filing a new claim. Premium decisions depend on your carrier and claim history; ask your agent if you're concerned.</p>"),
              ("Can I still use my own contractor?", "<p>Yes. Appraisal sets the amount of loss. Who does the repair is a separate decision.</p>"),
              ("What if my mortgage company is on the check?", "<p>Mortgage companies are commonly named on claim payments, including those that follow an appraisal award. Their disbursement process is separate from the appraisal.</p>")],
        related=["property-insurance-appraisal", "hail-damage-appraisal", "water-damage-appraisal", "estimate-review"],
    ),
    "commercial-property-appraisal": dict(
        title="Commercial Property Insurance Appraisal in Alabama",
        desc="Commercial insurance appraisal for office, retail, multi-family, church and industrial buildings in Alabama. Detailed scope and valuation review.",
        h1="Commercial Property Insurance Appraisal",
        lead="Large-loss appraisal for office, retail, apartment, church, warehouse, industrial and institutional property across Alabama.",
        img="commercial", stype="Commercial property insurance appraisal",
        body=f"""
<p class="lead-p">Commercial claims are where small differences become very large numbers. A low-slope roof measured a few hundred square feet short, a missed tapered insulation layer or an omitted crane day can move a commercial estimate by tens of thousands of dollars.</p>
<p>Alabama Insurance Appraiser takes commercial appraisal and estimating assignments statewide. We are used to estimates that run to hundreds of line items across multiple buildings, and we organize them so every disputed item can be traced and resolved.</p>
<h2>Property types</h2>
{grid([card("Office &amp; professional", "Mid-rise offices, medical and professional buildings, tenant suites.", None, "building"),
       card("Retail &amp; restaurants", "Strip centers, freestanding retail, restaurants and service businesses.", None, "target"),
       card("Multi-family", "Apartment communities, condo associations and student housing.", None, "users"),
       card("Churches &amp; institutions", "Sanctuaries, fellowship halls, schools and nonprofit facilities.", None, "home"),
       card("Industrial &amp; warehouse", "Metal buildings, distribution, manufacturing and flex space.", None, "layers"),
       card("Hospitality", "Hotels, motels and short-term rental portfolios.", None, "map")], 3)}
<h2>What makes commercial appraisal different</h2>
<ul><li><strong>Roof systems.</strong> TPO, EPDM, modified bitumen, built-up and standing-seam metal roofs each have their own components, attachment requirements and code considerations.</li>
<li><strong>Scale and repetition.</strong> An error repeated across 48 apartment units or 12 buildings multiplies fast.</li>
<li><strong>Access and logistics.</strong> Lifts, cranes, staging, protection of occupied spaces, after-hours work and phasing all carry real cost.</li>
<li><strong>Building systems.</strong> Rooftop HVAC units, curbs, electrical and fire protection may be affected by the same event.</li>
<li><strong>Code and ordinance.</strong> Repairs may trigger current code requirements, subject to the policy's ordinance or law coverage.</li></ul>
{fig("commercial", "Modern multi-story commercial building in Alabama at dusk")}
<h2>Our commercial workflow</h2>
{steps_html([("Policy and SOV review", "We review the commercial policy, the appraisal clause, deductibles, and the statement of values."),
             ("Building-by-building documentation", "Matterport capture, roof measurements and component inventories for each structure."),
             ("Comparative estimate matrix", "A side-by-side breakdown of the carrier's and contractor's estimates by building, trade and line item."),
             ("Supported valuation", "An Xactimate or Symbility estimate with the documentation behind each disputed item."),
             ("Appraisal panel", "Negotiation with the opposing appraiser and umpire presentations for whatever remains.")])}
<h2>Working with owners, managers and counsel</h2>
<p>We coordinate with property managers for access, with engineers when structural or roof-system questions require it, and with counsel when a dispute involves both valuation and coverage issues.</p>
""",
        faqs=[("Do you handle multi-building claims?", "<p>Yes. We organize the estimate by building and trade so each structure's disputed items can be tracked separately.</p>"),
              ("Can you work alongside our engineer?", "<p>Yes. Engineering findings often define the scope; we turn that scope into a priced, defensible estimate.</p>"),
              ("How is a percentage wind or hail deductible handled?", "<p>Appraisal sets the amount of loss. Deductibles are applied by the carrier afterward under the policy. Our <a href='/tools/hurricane-deductible-calculator/'>deductible calculator</a> shows how a percentage deductible translates into dollars.</p>")],
        related=["property-insurance-appraisal", "matterport-documentation", "wind-storm-damage-appraisal", "xactimate-estimates"],
    ),
    "estimate-review": dict(
        title="Insurance Claim Estimate Review in Alabama",
        desc="Line-by-line review of carrier and contractor estimates in Alabama. Find missing items, quantity errors and pricing gaps before you invoke appraisal.",
        h1="Insurance Claim Estimate Review",
        lead="Find out exactly where two estimates differ, and which differences are worth fighting for, before you commit to appraisal.",
        img="inspect", stype="Insurance claim estimate review",
        body=f"""
<p class="lead-p">Not every disagreement needs a full appraisal. Sometimes the fastest way forward is a clear, item-by-item explanation of what's missing or mispriced, sent back to the adjuster as a supported supplement.</p>
<p>Our estimate review compares the carrier's estimate with your contractor's estimate (or with what the property actually needs) and turns the result into a plain-English report.</p>
<h2>What the review covers</h2>
{table(["Category", "What we check"], [
    ["Measurements", "Roof squares, pitch, waste factor, wall and ceiling areas, linear footage of trim, gutters and flashing"],
    ["Scope", "Repair vs. replace, missing rooms or elevations, related items such as drip edge, starter, ventilation and underlayment"],
    ["Materials", "Correct grade and type of shingle, siding, flooring or cabinetry; availability and matching"],
    ["Labor &amp; access", "Steep and high charges, additional layers, protection, lifts, phasing"],
    ["Pricing", "Unit costs against the current local price list, minimum charges, taxes"],
    ["Overhead &amp; profit", "Whether the job's complexity and number of trades support general contractor O&amp;P"],
    ["Depreciation", "Age, condition and the depreciation applied to each line"],
])}
<h2>What you receive</h2>
{checklist(["A gap summary showing how much of the difference falls into each category",
            "An annotated list of missing, short or mispriced line items",
            "Supporting photos and measurements for each disputed item",
            "A recommendation: supplement, request re-inspection, or invoke appraisal"])}
{callout("<p>Try our free <a href='/tools/claim-gap-calculator/'>Claim Gap Calculator</a> to see the size of the gap and what it means after deductible and depreciation.</p>", "tip", "Start with the numbers")}
<h2>Who it helps</h2>
<p>Homeowners deciding whether appraisal is worth it, contractors who need a third-party supplement, and attorneys who want an independent read on a disputed estimate.</p>
""",
        faqs=[("How fast is an estimate review?", "<p>Turnaround depends on the size of the estimates and whether an inspection is needed. A desk review of a residential roof claim moves much faster than a multi-building commercial claim.</p>"),
              ("Do I need both estimates?", "<p>The carrier's estimate is essential. A contractor estimate helps, but we can also review the carrier's estimate against what we document at the property.</p>"),
              ("Can the review be used in appraisal later?", "<p>Yes. The same organized documentation becomes the foundation of an appraisal position if the dispute goes that far.</p>")],
        related=["property-insurance-appraisal", "xactimate-estimates", "symbility-estimates", "hail-damage-appraisal"],
    ),
    "xactimate-estimates": dict(
        title="Xactimate Estimates for Insurance Claims in Alabama",
        desc="Detailed Xactimate estimates for Alabama property claims and appraisal: line-item scope, current local pricing, sketches and photo reports.",
        h1="Xactimate Estimates for Alabama Property Claims",
        lead="Detailed, line-item estimates on the platform most insurance carriers already use, priced with the current price list for your area.",
        img="roof", stype="Xactimate estimating",
        body=f"""
<p class="lead-p">Xactimate is the estimating software most property insurers and restoration contractors use. When your estimate speaks the same language as the carrier's &mdash; same line items, same price list, same units &mdash; disagreements become specific and solvable.</p>
<p>Alabama Insurance Appraiser writes Xactimate estimates for appraisal assignments, estimate reviews and supplements, for residential and commercial property.</p>
<h2>What's in our Xactimate estimates</h2>
{checklist(["Sketches with room dimensions and roof diagrams", "Line items for every trade: demolition, framing, roofing, drywall, paint, flooring, finish carpentry, electrical and more",
            "The current Xactimate price list for the property's ZIP code", "Steep, high, additional-layer and access charges where they apply",
            "F9 notes explaining the reasoning behind disputed items", "Photo reports tied to the estimate"], "checklist two-col")}
<h2>Why a carrier-format estimate matters</h2>
<p>An adjuster can compare an Xactimate estimate to theirs line by line. That makes it much easier to show precisely which items are missing or short &mdash; and harder to dismiss the estimate as a contractor's lump-sum bid.</p>
<h2>Common Xactimate gaps we catch</h2>
<ul><li>Missing starter strip, drip edge, ice-and-water shield, ridge cap or valley metal</li>
<li>Waste factors below what the roof's geometry requires</li>
<li>Pipe jacks, vents, satellite detach-and-reset, gutter guards left out</li>
<li>Paint scoped to one wall when the room needs uniform finish</li>
<li>Content manipulation, floor protection and final cleaning omitted</li>
<li>Price list date older than the date of loss</li></ul>
{fig("roof", "Wet asphalt shingle roof showing storm damage that requires a detailed estimate")}
""",
        faqs=[("Is Xactimate pricing accurate for Alabama?", "<p>Xactimate publishes regional price lists by ZIP code and updates them regularly. Whether a specific price fits your job is a fair question to raise in an estimate dispute.</p>"),
              ("Can you convert a contractor bid into Xactimate?", "<p>Yes. We rebuild lump-sum or spreadsheet bids into a line-item Xactimate estimate so they can be compared directly with the carrier's.</p>"),
              ("Do you also write Symbility?", "<p>Yes &mdash; see our <a href='/services/symbility-estimates/'>Symbility estimates</a> page.</p>")],
        related=["symbility-estimates", "estimate-review", "property-insurance-appraisal", "matterport-documentation"],
    ),
    "symbility-estimates": dict(
        title="Symbility Estimates for Insurance Claims | Alabama",
        desc="Symbility (CoreLogic) estimates for Alabama property insurance claims, with structured scope and pricing that line up with carrier estimates.",
        h1="Symbility Estimates for Insurance Claims",
        lead="Structured estimates on the Symbility platform, for carriers and claims that use it instead of Xactimate.",
        img="inspect", stype="Symbility estimating",
        body=f"""
<p class="lead-p">Several insurers and independent adjusting firms write their estimates in Symbility (now part of CoreLogic's claims platform). When the carrier's estimate is in Symbility, answering it in the same format keeps the comparison clean.</p>
<p>Alabama Insurance Appraiser prepares Symbility estimates for appraisal and estimate-review assignments across Alabama.</p>
<h2>What we deliver</h2>
{checklist(["Room-by-room scope with diagrams and measurements", "Pricing on the current regional price list", "Notes supporting repair method and quantities",
            "Photo documentation linked to each area", "A comparison summary against the carrier's estimate"])}
<h2>Symbility vs. Xactimate</h2>
{table(["", "Symbility", "Xactimate"], [
    ["Used by", "A number of carriers and independent adjusting firms", "Most carriers, adjusters and restoration contractors"],
    ["Pricing", "Regional price lists", "ZIP-code price lists updated regularly"],
    ["Diagrams", "Built-in floor plan and roof tools", "Sketch with roof and room tools"],
    ["Our recommendation", "Use when the carrier estimate is in Symbility", "Default for most appraisals and supplements"],
])}
<p>Both tools can produce accurate, defensible estimates. What matters is the scope and the evidence behind it.</p>
""",
        faqs=[("Which carriers use Symbility?", "<p>Usage changes over time and varies by line of business. Your carrier's estimate will show which platform it was written in.</p>"),
              ("Can a Symbility estimate be compared with an Xactimate estimate?", "<p>Yes, though line items don't map one-to-one. We normalize both estimates into a common comparison so differences are clear.</p>"),
              ("Do you charge differently for Symbility?", "<p>No. Fees are based on the size and complexity of the assignment, not the platform.</p>")],
        related=["xactimate-estimates", "estimate-review", "property-insurance-appraisal", "matterport-documentation"],
    ),
    "matterport-documentation": dict(
        title="Matterport 3D Documentation for Insurance Claims | Alabama",
        desc="Matterport 3D scanning for Alabama insurance claims: accurate measurements, floor plans and a permanent visual record of property damage.",
        h1="Matterport 3D Documentation for Insurance Claims",
        lead="A permanent, measurable 3D record of the property and the damage, captured before repairs erase the evidence.",
        img="commercial", stype="Matterport property documentation",
        body=f"""
<p class="lead-p">Photos show what the camera pointed at. A Matterport scan shows everything &mdash; every room, wall, ceiling and transition &mdash; with measurements you can take later, long after the drywall has been replaced.</p>
<p>Alabama Insurance Appraiser uses Matterport capture on appraisal assignments where the layout, extent of damage or quantities are in dispute, and as a standalone documentation service.</p>
<h2>What a Matterport capture gives you</h2>
{grid([card("Immersive 3D walkthrough", "Anyone on the claim can tour the property online without another site visit.", None, "cube"),
       card("Measurements on demand", "Point-to-point measurements of rooms, openings and damaged areas.", None, "ruler"),
       card("Floor plans", "Schematic floor plans that support room dimensions in the estimate.", None, "layers"),
       card("Tagged damage", "Notes and photos pinned to the exact location of each damaged item.", None, "pin")], 2)}
<h2>When it's most useful</h2>
<ul><li>Multi-room or multi-floor water and fire losses</li><li>Commercial buildings and apartment communities with many units</li>
<li>Claims where mitigation or demolition will start before every party can inspect</li><li>Disputes over room sizes, ceiling heights or the extent of affected areas</li></ul>
{callout("<p>Capture before mitigation crews remove materials whenever it is safe to do so. Once the damage is gone, the scan is the record.</p>", "tip", "Timing matters")}
""",
        faqs=[("Who can see the scan?", "<p>You decide. Scans can be shared by private link with the carrier, the other appraiser, the umpire or your attorney.</p>"),
              ("How accurate are Matterport measurements?", "<p>Matterport publishes accuracy figures for each camera. They're well suited to room-level dimensions used in estimates; we verify critical measurements by hand.</p>"),
              ("Can you scan a commercial building?", "<p>Yes. Large buildings are captured in sections and joined into one model.</p>")],
        related=["property-insurance-appraisal", "commercial-property-appraisal", "fire-smoke-damage-appraisal", "water-damage-appraisal"],
    ),
    "hail-damage-appraisal": dict(
        title="Hail Damage Insurance Appraisal in Alabama | Roof &amp; Exterior",
        desc="Hail damage appraisal for Alabama roofs, siding, gutters and soft metals. Independent amount-of-loss review when the hail claim estimate is too low.",
        h1="Hail Damage Insurance Appraisal in Alabama",
        lead="When the carrier calls it cosmetic or allows a few shingles and your roofer says it needs replacement.",
        img="roof", stype="Hail damage insurance appraisal",
        body=f"""
<p class="lead-p">Hail is one of the most frequent causes of property claims in North and Central Alabama, and one of the most argued. The same storm can leave one roof untouched and another needing full replacement, depending on the hailstone size, wind direction, roof age and material.</p>
<h2>What we evaluate on hail claims</h2>
{checklist(["Hail impacts to asphalt, architectural and impact-resistant shingles", "Metal roof panels, standing seam and ridge components",
            "Soft metals: vents, flashing, gutters and downspouts as size and direction indicators", "Siding, window wraps, screens and HVAC fins",
            "Repairability, brittleness and matching of the existing roof", "Collateral damage that helps establish the date and size of hail"], "checklist two-col")}
<h2>The usual hail disputes</h2>
<h3>Functional vs. cosmetic damage</h3>
<p>Some policies, especially on metal roofs, exclude cosmetic hail damage. Whether a dent affects the panel's function or only its appearance can turn on the policy wording and the evidence.</p>
<h3>Test squares and hit counts</h3>
<p>Adjusters often use a 10-by-10 test square on each slope. How the square is chosen, how hits are identified, and how many hits trigger replacement can all be debated.</p>
<h3>Repair vs. replacement</h3>
<p>Brittle shingles that crack when lifted, discontinued products and unavailable colors can make a "repair" impractical. That is a scope question appraisal is designed to resolve.</p>
{fig("roof", "Close view of a storm-damaged asphalt shingle roof surface")}
{callout("<p>Use our <a href='/tools/roof-square-calculator/'>Roof Square Calculator</a> to check the roof size in your estimate against your footprint and pitch.</p>", "tip", "Check the measurements")}
""",
        faqs=[("How long after a hailstorm can I file?", "<p>Your policy sets the notice requirements and any time limits. Report damage promptly, since delay makes it harder to tie damage to a specific storm.</p>"),
              ("Can hail damage show up later as leaks?", "<p>Yes. Bruised shingles can lose granules and fail over time. Early documentation helps connect later leaks to the original storm.</p>"),
              ("Does appraisal work for hail on metal roofs?", "<p>Appraisal can value the damage, but whether cosmetic dents are covered depends on the policy. That coverage question may sit outside appraisal.</p>")],
        related=["wind-storm-damage-appraisal", "residential-property-appraisal", "estimate-review", "xactimate-estimates"],
    ),
    "wind-storm-damage-appraisal": dict(
        title="Wind, Tornado &amp; Hurricane Damage Appraisal | Alabama",
        desc="Insurance appraisal for tornado, straight-line wind and hurricane damage across Alabama. Roof, siding, window, fence and structural loss valuation.",
        h1="Wind, Tornado &amp; Hurricane Damage Appraisal",
        lead="From Dixie Alley tornadoes to Gulf Coast hurricanes, wind claims across Alabama come with complicated scopes and percentage deductibles.",
        img="storm", stype="Wind and storm damage insurance appraisal",
        body=f"""
<p class="lead-p">Alabama gets wind from every direction: spring and late-fall tornado outbreaks, derechos and straight-line wind from summer thunderstorms, and tropical systems that bring hurricane-force gusts to Mobile and Baldwin counties and well inland toward Dothan and Montgomery.</p>
<h2>Wind and storm damage we value</h2>
{grid([card("Roof systems", "Lifted, creased or missing shingles; displaced metal panels; damaged underlayment and decking.", None, "home"),
       card("Building envelope", "Siding, soffit, fascia, windows, doors and garage doors.", None, "layers"),
       card("Trees and debris", "Impact damage from falling trees and windborne debris.", None, "alert"),
       card("Water intrusion", "Interior damage from wind-driven rain through storm-created openings.", None, "droplets"),
       card("Other structures", "Fences, carports, sheds, pool enclosures and detached garages.", None, "building"),
       card("Commercial", "Rooftop units, metal buildings, signage and large roof systems.", None, "target")], 3)}
<h2>Hurricane and named-storm deductibles</h2>
<p>Many Alabama policies, especially near the coast, carry a separate hurricane or named-storm deductible expressed as a percentage of the dwelling limit (Coverage A) &mdash; commonly 1% to 5% or more. On a $350,000 home, a 2% deductible is $7,000 before the carrier pays anything. Use our <a href="/tools/hurricane-deductible-calculator/">hurricane deductible calculator</a> to see yours in dollars.</p>
<h2>Creased shingles and the "repair" problem</h2>
<p>Wind often creases shingles without tearing them off. Creased shingles have lost their seal and bend line strength. Whether a slope can be repaired by replacing individual shingles depends on the shingle's age and whether neighboring shingles can be lifted without breaking.</p>
{fig("storm", "Storm clouds building over Alabama homes ahead of severe wind")}
<h2>FORTIFIED roofs</h2>
<p>If your home has an IBHS FORTIFIED designation, the roof repair or replacement may need to meet FORTIFIED standards to keep the designation and its premium discount. Alabama's Strengthen Alabama Homes program has helped many homeowners retrofit to that standard. Make sure the estimate reflects the roof system you actually have.</p>
""",
        faqs=[("Is tornado damage handled differently from wind?", "<p>Tornado damage is usually treated as windstorm damage under the policy. A separate hurricane deductible typically applies only to named storms as the policy defines them.</p>"),
              ("What about flood water after a hurricane?", "<p>Standard homeowner policies exclude flood. Wind-driven rain through storm openings is treated differently from rising water. Flood claims run through a separate flood policy.</p>"),
              ("Can appraisal resolve wind vs. flood disputes?", "<p>Causation disputes can blur into coverage questions. Some courts let appraisers address causation as part of the amount of loss; others don't. Get advice if this is the core issue.</p>")],
        related=["hail-damage-appraisal", "commercial-property-appraisal", "residential-property-appraisal", "matterport-documentation"],
    ),
    "water-damage-appraisal": dict(
        title="Water Damage Insurance Appraisal in Alabama",
        desc="Water damage appraisal for Alabama plumbing, roof and appliance leaks: drywall, flooring, cabinetry, insulation and mitigation scope review.",
        h1="Water Damage Insurance Appraisal",
        lead="Burst pipes, failed supply lines, roof leaks and appliance failures &mdash; where the real damage is usually larger than what's visible on day one.",
        img="flood", stype="Water damage insurance appraisal",
        body=f"""
<p class="lead-p">Water moves. It wicks up drywall, runs under cabinets, soaks insulation and travels along subfloors into rooms that look fine. Estimates written from a quick walk-through often miss the extent of it.</p>
<h2>What we evaluate</h2>
{checklist(["Moisture mapping and mitigation logs", "Drywall height and linear footage removed and replaced", "Insulation, baseboard, casing and trim",
            "Continuous flooring that runs between rooms", "Cabinets and countertops affected by water at the toe kick", "Ceilings below upper-floor leaks",
            "Paint for uniform appearance", "Content manipulation and pack-out"], "checklist two-col")}
<h2>The flooring problem</h2>
<p>Hardwood, LVP and tile often run continuously through several rooms. If the damaged section can't be matched or isolated at a natural break, replacing only the wet area may leave a visible patch. How that is handled depends on the policy and the specific flooring.</p>
<h2>Sudden vs. long-term leaks</h2>
<p>Most homeowner policies cover sudden and accidental discharge but exclude repeated seepage or long-term leaks. Whether the loss is covered is a coverage question; what the covered portion is worth is an appraisal question.</p>
{callout("<p>Standard homeowner policies exclude surface water and rising flood water. Those losses are handled under a separate flood policy, such as one through the NFIP.</p>", "warn", "Flood is different")}
{fig("flood", "Flooded residential street showing the scale of water damage after a storm")}
""",
        faqs=[("Should I wait for the adjuster before drying out?", "<p>No. Most policies require you to protect the property from further damage. Document thoroughly, keep damaged samples where practical, and start mitigation.</p>"),
              ("Is mold covered?", "<p>Mold coverage is often limited or excluded, with a sublimit in some policies. Check the policy language.</p>"),
              ("Can you review a mitigation invoice?", "<p>Yes. We review drying logs, equipment days and mitigation line items as part of an estimate review.</p>")],
        related=["residential-property-appraisal", "matterport-documentation", "estimate-review", "fire-smoke-damage-appraisal"],
    ),
    "fire-smoke-damage-appraisal": dict(
        title="Fire &amp; Smoke Damage Insurance Appraisal | Alabama",
        desc="Fire and smoke damage appraisal across Alabama. Structural repair, smoke and soot cleaning, demolition, rebuild and contents-related scope valuation.",
        h1="Fire &amp; Smoke Damage Insurance Appraisal",
        lead="Fire losses involve more trades, more judgment calls and more money than almost any other claim. Detail matters at every step.",
        img="residential", stype="Fire and smoke damage insurance appraisal",
        body=f"""
<p class="lead-p">After a fire, the burned area is only part of the loss. Smoke and soot travel through HVAC ducts and wall cavities; heat damages wiring and framing out of sight; water from firefighting adds another layer of damage.</p>
<h2>Scope we evaluate</h2>
{checklist(["Structural framing, sheathing and roof decking", "Electrical, plumbing and HVAC affected by heat and smoke", "Smoke and soot cleaning vs. replacement of finishes",
            "Odor control: sealing, deodorization and duct cleaning", "Demolition, debris removal and haul-off", "Code upgrades triggered by the rebuild",
            "Water damage from fire suppression", "Rebuild sequencing and temporary protection"], "checklist two-col")}
<h2>Clean or replace?</h2>
<p>The biggest fire-claim fights are often over whether smoke-affected materials can be cleaned or must be replaced. The answer depends on the material, the type of smoke residue and whether cleaning actually restores it.</p>
<h2>Code and ordinance</h2>
<p>A rebuild may need to meet current building codes. Whether those costs are covered, and up to what limit, depends on the policy's ordinance or law coverage.</p>
{fig("residential", "Two-story Alabama home representing a residential fire and smoke damage claim")}
""",
        faqs=[("Can you work with my contents inventory?", "<p>Our focus is the building. We coordinate with whoever is handling contents so the building and contents scopes don't overlap or leave gaps.</p>"),
              ("How long do fire appraisals take?", "<p>Larger losses take longer because the scope is bigger and more trades are involved. Good documentation early speeds everything up.</p>"),
              ("What about additional living expenses?", "<p>ALE (Coverage D) disputes are handled under the policy terms. Appraisal can address amount-of-loss disputes on ALE in some policies.</p>")],
        related=["water-damage-appraisal", "matterport-documentation", "residential-property-appraisal", "commercial-property-appraisal"],
    ),
}


def service_page(slug):
    d = DATA[slug]
    name, blurb, ico = SVC[slug]
    path = f"/services/{slug}/"
    p = {
        "path": path, "title": d["title"], "description": d["desc"], "h1": d["h1"], "lead": d["lead"],
        "kicker": "Alabama Insurance Appraiser services", "hero_img": d["img"], "nav_active": "/services/",
        "crumbs": [("Home", "/"), ("Services", "/services/"), (name, path)],
        "sidebar_links": sidebar_links(slug), "sidebar_title": "Other services", "priority": "0.8",
        "schema_type": "WebPage",
    }
    rel = related_links("Related services", [(SVC[s][0], f"/services/{s}/") for s in d["related"]])
    p["body"] = d["body"] + f'<h2>Frequently asked questions</h2>{faq_html(d["faqs"])}' + rel
    p["schema"] = [service_schema(p, name, d["stype"]), faq_schema(p, d["faqs"])]
    return p


def hub():
    p = {
        "path": "/services/",
        "title": "Insurance Appraisal &amp; Estimating Services in Alabama",
        "description": "Claim appraisal, estimate review, Xactimate and Symbility estimates, Matterport scans, and hail, wind, water and fire appraisal across Alabama.",
        "h1": "Property Insurance Appraisal Services in Alabama",
        "lead": "Independent appraisal, detailed estimating and property documentation for residential and commercial insurance claims, statewide.",
        "kicker": "Property loss support statewide", "hero_img": "storm", "nav_active": "/services/",
        "crumbs": [("Home", "/"), ("Services", "/services/")], "layout": "wide", "priority": "0.9",
        "schema_type": "CollectionPage",
    }
    core = [card(n, b, f"/services/{s}/", i) for s, n, b, i in SERVICES[:7]]
    loss = [card(n, b, f"/services/{s}/", i) for s, n, b, i in SERVICES[7:]]
    p["body"] = f'''
<section class="section section-white"><div class="container">
  {section_head("Core services", "Appraisal, estimating and documentation", "Every assignment focuses on the scope, measurements, pricing and evidence behind the amount of loss.", True)}
  {grid(core[:3], 3)}<div style="height:24px"></div>{grid(core[3:], 4)}
</div></section>
<section class="section section-aqua"><div class="container">
  {section_head("By type of loss", "Appraisal for the claims Alabama sees most", "Hail in the Tennessee Valley, tornadoes across Dixie Alley, hurricanes on the Gulf Coast, and the water and fire losses that happen everywhere.", True)}
  {grid(loss, 4)}
</div></section>
<section class="section section-white"><div class="container split">
  <div class="reveal">
    {section_head("Core appraisal service", "Independent evaluation of the amount of loss")}
    <p>When estimates differ, a useful appraisal looks beyond the totals to the scope, quantity, pricing and repair-method differences behind them. The assignment can include review of the damaged property, measurements, photographs, competing estimates, repair sequencing, materials, labor and access.</p>
    {checklist(["Review of the applicable appraisal provision", "Inspection and property-specific loss documentation", "Comparison of competing repair scopes and estimates", "A supported position on the amount of loss"])}
    {btn("Property insurance appraisal", "/services/property-insurance-appraisal/", "primary")}
  </div>
  <div class="frame reveal"><div class="img-zoom"><img src="/assets/img/insurance-appraiser-inspecting-roof.webp" width="1000" height="667" alt="Insurance appraiser with a clipboard inspecting a storm-damaged roof" loading="lazy"></div></div>
</div></section>
<section class="section section-dark"><div class="container">
  {section_head("How we work", "From first call to signed award", "", True)}
  {steps_html([("Free consultation", "Tell us about the property, the loss and where the claim stands. We'll say plainly whether appraisal fits."),
               ("Engagement", "A written agreement covering scope and fees before any work begins."),
               ("Documentation", "Inspection, measurements, photos, Matterport capture where useful, and a full record review."),
               ("Valuation", "An Xactimate or Symbility estimate and an item-by-item comparison with the carrier's numbers."),
               ("Resolution", "Negotiation with the other appraiser, umpire submissions if needed, and a signed award.")])}
</div></section>'''
    p["schema"] = [{"@type": "ItemList", "@id": url("/services/#list"), "name": "Insurance appraisal services",
                    "itemListElement": [{"@type": "ListItem", "position": n, "url": url(f"/services/{s}/"), "name": nm}
                                        for n, (s, nm, _, _) in enumerate(SERVICES, 1)]}]
    return p


def pages():
    return [hub()] + [service_page(s) for s, _, _, _ in SERVICES]
