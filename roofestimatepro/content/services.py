"""Service hub (/services/) and the four service pages (/services/<slug>/).

build(g) is called by build.py with its globals(), so every layout helper
(build_prose, icon, tool_card, faq_html, cta_band, toc, ...) comes from g.
"""


def _checks(items):
    return '<ul class="check-list">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


AREA_SERVED = [{"@type": "State", "name": "Texas"}, {"@type": "Country", "name": "United States"}]


# --------------------------------------------------------------------------
# Service page content
# --------------------------------------------------------------------------

XACT_BODY = """
<h2 id="what-this-estimate-is">A line-item estimate, not a number on a napkin</h2>
<p>A roof replacement priced as "26 squares at $550" tells nobody what is actually on the roof. A line-item estimate
breaks the job into the same pieces an insurance carrier, a lender or a careful homeowner expects to see: tear-off by
layer, the roofing product by the square, starter, hip and ridge cap by the linear foot, drip edge, underlayment,
ice-and-water barrier in the valleys, flashing, pipe jacks, vents, steep and high-roof charges, haul-off and permits.
Each line has a quantity, a unit and a unit price, so anyone reading it can check the math.</p>
<p>We build every estimate from scratch, in the format carriers use: Xactimate-style line items, grouped by roof area
and trade, with the measurements and notes that support each quantity. We do not copy the carrier's estimate and add
to it, and we do not start from a template that assumes every roof is a simple gable.</p>

<h2 id="how-we-build-it">How we build it</h2>
<h3>1. Measurements first</h3>
<p>Quantities come from a measurement report (EagleView, Hover, GAF QuickMeasure, Roofr and similar), a drone or
satellite takeoff, or your own field sketch with pitches and lengths. We reconcile the report against the photos:
a detached garage left off the report, a porch roof at a different pitch or a second layer of shingles changes the
estimate, and we would rather catch it now than in a supplement later.</p>
<h3>2. Waste tied to the geometry</h3>
<p>A flat 10% waste factor is wrong on most roofs. A simple gable might need 8–10%; a cut-up hip roof with dormers and
valleys can run 15% or more. We set waste from the hip, valley and rake lengths on the actual roof and show it as its
own figure, so nobody has to guess whether it is buried in the square count.</p>
<h3>3. The items people forget</h3>
<p>The difference between a thin estimate and a complete one is usually the accessory lines: starter strip at the
eaves and rakes, hip and ridge cap, drip edge where the local code requires it, step and counterflashing at walls,
chimney flashing, replacing (not reusing) pipe jacks and vents, detach-and-reset for satellite dishes, solar,
gutters or gutter guards, and the steep (7/12 and up) and high (two stories and up) labor charges. We list each one
that applies and leave out the ones that do not.</p>
<h3>4. Pricing for the property's market</h3>
<p>Unit prices are set for where the property is, not where we are. Labor and material costs in the Rio Grande Valley
are not the same as Dallas, and both differ from Denver. Overhead and profit appear as a separate line when the job
calls for a general contractor, so the subtotal and the markup can be read on their own.</p>

<h2 id="who-uses-it">Who uses our residential estimates</h2>
<p><strong>Roofing contractors</strong> use them to send a clean, defensible number to the carrier on a claim job, to
back up a supplement request, or to stop spending evenings in estimating software. <strong>Public adjusters</strong>
use them as the estimate behind a claim presentation. <strong>Homeowners</strong> use them to understand whether the
carrier's number or a contractor's bid is in the right range before signing anything. Property managers and
appraisers use them to put several buildings or an appraisal dispute on the same footing.</p>

<h2 id="what-it-is-not">What a professional estimate is, and is not</h2>
<p>Our estimate documents what the roof needs and what that work reasonably costs in that market. It is not a bid to
do the work: we are estimators, not a roofing company, and we don't sell roofs. It is also not a coverage decision.
Whether a carrier pays for a line item depends on the policy, the cause of loss and the facts of the claim, so read
your policy and ask your adjuster or attorney about coverage questions.</p>
<p>If you only need a ballpark, start with the free <a href="/tools/roof-replacement-cost-calculator/">Roof
Replacement Cost Calculator</a>; it uses the same kind of itemized math with Texas 2026 pricing and lets you edit every
unit price. When the number has to hold up in front of a carrier, a lender or a client, <a
href="/get-estimate/">send the roof to us</a>.</p>

<h2 id="texas-notes">Texas notes</h2>
<p>Most of our residential work is hail and wind on asphalt shingle roofs in North, Central and West Texas, plus
hurricane and tropical-storm wind on the Gulf Coast. A few Texas details show up in our estimates again and again:
impact-resistant (Class 4) shingles, which many Texas insurers discount; windstorm inspection requirements for
properties in the coastal counties covered by TWIA; and city permit fees that vary widely from one municipality to the
next. Texas law also bars roofing contractors from paying or waiving an insured's deductible, so we never write a
"deductible credit" into an estimate.</p>
"""

COMM_BODY = """
<h2 id="commercial-is-different">Commercial roofs need a different kind of takeoff</h2>
<p>On a house, squares, pitch and a handful of linear measurements carry most of the estimate. On a commercial
building the field of the roof is often the easy part. The money is in the perimeter and the details: parapet walls
and their height, coping and edge metal, curbs for rooftop units, pipe and conduit penetrations, drains and scuppers,
crickets and tapered insulation, expansion joints, and the terminations where the membrane meets walls and equipment.
Miss a 3-foot parapet around a 40,000 sq ft building and the estimate can be off by thousands of square feet of
flashing membrane.</p>
<p>We build commercial estimates line by line, in the format carriers use, from the roof plan, aerial or drone
measurements, core-cut data and photos. Each line is tied to a measured quantity so a property manager, owner,
carrier or appraiser can see where the number came from.</p>

<h2 id="systems">Systems we estimate</h2>
<h3>Low-slope</h3>
<p>TPO (mechanically attached and fully adhered), PVC, EPDM, two-ply modified bitumen, built-up roofing, and fluid-applied
silicone and acrylic coatings. For reference, typical 2026 installed ranges at the Dallas–Fort Worth baseline, before
tear-off and insulation, run about $7.00–$10.00/sf for mechanically attached 60-mil TPO, $9.00–$13.00/sf for 60-mil PVC,
$7.50–$11.00/sf for two-ply mod-bit and $3.50–$6.00/sf for a silicone restoration. Tear-off adds about $1.50–$3.00/sf per
layer, and polyiso insulation about $0.90–$1.30/sf per inch.</p>
<h3>Steep-slope and metal</h3>
<p>Plenty of commercial property is steep-slope: apartment complexes, retail mansards, churches, offices built like
large houses, and metal buildings. We estimate shingle, tile, standing seam and exposed-fastener metal on commercial
buildings with the same per-building detail as the low-slope work, which matters on a multi-building apartment claim
where every building has different damage.</p>

<h2 id="restore-or-replace">Restoration, recover or replacement</h2>
<p>The biggest decision on most low-slope roofs is whether to coat, recover or tear off. The answer depends on what is
under the membrane:</p>
<ul>
<li><strong>Coating restoration</strong> can make sense when the membrane is aged but the insulation is dry and the
deck is sound. Many coating manufacturers will not warranty a restoration over wet insulation, so a moisture survey
(infrared or core cuts) should come first.</li>
<li><strong>Recover</strong> means a new membrane over the existing roof, usually with a cover board. Building codes
generally do not allow a recover where the roof already has two layers, and wet insulation has to come out either way.</li>
<li><strong>Full replacement</strong> is the answer when insulation is saturated, the deck is damaged, or the drainage
is wrong and needs tapered insulation to fix.</li>
</ul>
<p>When you ask, we price more than one option side by side so the owner or carrier can see the cost difference and
the expected service life of each: coatings typically 10–15 years (renewable), TPO 20–25, PVC and EPDM 25–30.</p>

<h2 id="claims-and-budgets">For insurance claims and for budgets</h2>
<p>On hail and wind claims we document the damage by roof section and system, scope the repair or replacement the
damage supports, and include the items low-slope claims often leave out: wet insulation replacement, edge metal and
coping, re-flashing curbs and walls, temporary repairs, and detach-and-reset of rooftop equipment where the work
requires it. For owners and managers who are not on a claim, the same takeoff becomes a capital budget or a way to
compare contractor bids on equal terms.</p>
<p>Want to rough out the numbers first? The free <a href="/tools/flat-roof-calculator/">Flat &amp; Commercial Roof
Calculator</a> handles membrane rolls, insulation boards, fasteners and cost for each system, and the <a
href="/tools/metal-roof-calculator/">Metal Roof Calculator</a> covers panels, trim and fasteners.</p>

<h2 id="what-we-are-not">What we are, and are not</h2>
<p>We are estimators. We prepare estimates, takeoffs and scopes; we don't sell or install roofs, and we don't
perform engineering, moisture testing or code inspections ourselves. When a project needs an engineer's report or a
moisture survey, we build the estimate from that report and say so in the notes.</p>
"""

REVIEW_BODY = """
<h2 id="why-review">Why carrier estimates come up short</h2>
<p>Most carrier roof estimates are not wrong on purpose. They are written fast, often after a storm when one adjuster
has dozens of claims, from a measurement that may or may not match the roof, using a template that assumes a simple
roof. The result is an estimate that has the big lines (tear-off, shingles) but misses the smaller ones that add up:
starter, ridge cap on the hips, drip edge, valley treatment, flashing, steep and high charges, vents and pipe jacks.
On a typical house, those lines can be a meaningful share of the total.</p>
<p>Our claim estimate review costs $50 per claim. You upload the carrier's estimate and your photos, and an estimator
compares the two line by line and tells you, in writing, what is missing or under-scoped.</p>

<h2 id="what-we-check">What we check</h2>
<h3>Quantities</h3>
<p>We compare the squares, waste, eave, rake, hip, ridge and valley lengths in the estimate against the measurement
report or the photos. A roof measured at 31 squares and paid at 26 is the most common and the most expensive gap.</p>
<h3>Missing line items</h3>
<p>We look for every component the photos show and the estimate leaves out: starter course, hip and ridge cap, drip
edge, underlayment, ice-and-water barrier in valleys, step flashing, counterflashing, chimney flashing, pipe jacks,
exhaust and ridge vents, satellite or solar detach-and-reset, gutter and guard work, and permits.</p>
<h3>Labor charges</h3>
<p>Steep charges (7/12 and up, with higher tiers above 9/12 and 12/12) and high-roof charges (two stories and up) are
easy to leave off and easy to prove from photos. We also note when an additional layer of shingles was not included in
the tear-off.</p>
<h3>Code items and overhead and profit</h3>
<p>We point out code-required items commonly left off and flag whether overhead and profit was included when the
job involves several trades. Whether a carrier owes code upgrades or O&amp;P depends on your policy and the claim, so we
note the item and the reason, not a coverage conclusion.</p>

<h2 id="what-you-get">What you get back</h2>
<p>A written list of the missing and under-scoped items, each with the quantity and unit the roof supports and a short
note on why it applies, plus any photo references that back it up. It is written to be easy to forward: a contractor
can attach it to a supplement request, a homeowner can send it to the desk adjuster, and a public adjuster can fold it
into the claim file.</p>
<p>If the review shows the carrier's estimate is far off, a review is not enough. In that case we can write a complete
<a href="/services/xactimate-roof-estimates/">line-item roof estimate</a> from scratch for the claim.</p>

<h2 id="before-you-submit">Before you submit</h2>
<ul>
<li>Get the full carrier estimate, not just the summary page. PDF is fine; an ESX file is better if you have it.</li>
<li>Gather photos of every slope, plus close-ups of flashing, vents, pipe jacks, valleys, drip edge and any
second layer at the edge.</li>
<li>If you have a measurement report, include it. If you don't, the <a
href="/tools/roof-square-footage-calculator/">Roof Square Footage Calculator</a> and <a
href="/tools/roof-pitch-calculator/">Roof Pitch Calculator</a> will get you close enough to sanity-check the
squares.</li>
<li>Run the carrier's numbers through the <a href="/tools/roof-insurance-claim-calculator/">Roof Insurance Claim
Calculator</a> to see how RCV, depreciation and the deductible become your first check.</li>
</ul>

<h2 id="what-a-review-is-not">What a review is, and is not</h2>
<p>A claim estimate review compares an estimate to the roof. It is not legal advice, a coverage opinion or an
appraisal award, and we don't contact the carrier or negotiate on anyone's behalf. Coverage questions belong with your
policy, your agent, a licensed public adjuster or an attorney. What the review gives you is a clear, item-by-item list
you can use in those conversations.</p>
"""

SCOPE_BODY = """
<h2 id="what-is-a-scope">What a scope of damages is</h2>
<p>A scope of damages is the itemized record of what a loss damaged and what each damaged item needs: remove and
replace, repair, clean, or detach and reset, with quantities. It is the foundation every estimate sits on. A carrier
adjuster writes one at the inspection; an appraiser, a contractor or a public adjuster may write their own. When two
scopes disagree, the claim usually turns on which one is better documented.</p>
<p>Put simply: the scope is the list, and an estimate puts prices on the list. A clear scope makes the pricing
conversation shorter, because both sides are arguing about the same items.</p>

<h2 id="two-ways">Two ways to get one</h2>
<h3>Order a professional scope: $200</h3>
<p>Send us the property address, the type of damage, the cause of loss and your photos and measurements through the
<a href="/get-a-scope/">scope order form</a>. An estimator works through the property slope by slope (and room by room
for interior water damage), lists every damaged component with its quantity and repair method, and notes the cause of
loss and the code items that apply. The fee is $200 per property, collected by secure Stripe checkout after you submit.</p>
<h3>Build a DIY scope on PAscope.com</h3>
<p>Prefer a hands-on approach? You can document and submit the property damage yourself through <a
href="https://pascope.com/" rel="noopener" target="_blank">PAscope.com</a> for a fast, low-cost evaluation. It suits
people who are comfortable on the property, taking methodical photos and describing what they see.</p>

<h2 id="what-we-cover">What a scope covers</h2>
<ul>
<li><strong>Roof:</strong> each slope and roof area, the roofing system, layers, pitch, the damaged components and
whether repair is possible or replacement is needed.</li>
<li><strong>Roof and exterior:</strong> adds gutters and downspouts, siding, trim, fascia and soffit, windows and screens,
fences and outbuildings that the same storm hit.</li>
<li><strong>Interior water damage:</strong> room by room, the ceilings, walls, insulation, flooring and contents areas
affected by a roof leak.</li>
<li><strong>Whole property:</strong> all of the above for a single loss.</li>
</ul>

<h2 id="documentation">Documentation that makes a scope stronger</h2>
<p>A remote scope is only as good as the photos behind it. The most useful sets have:</p>
<ul>
<li>An overview of every elevation of the building and every slope of the roof.</li>
<li>Close-ups of hail or wind damage with something for scale (a chalk circle, a coin or a tape measure).</li>
<li>Soft metals: vents, gutters, downspouts, AC fins and window wraps often show hail size and direction better
than shingles do.</li>
<li>Edges and layers: a photo at the eave or rake showing how many layers of shingles are on the roof and whether drip
edge is present.</li>
<li>Interior stains and wet areas, with the room shown wide first and then close.</li>
<li>Any measurement report (EagleView, Hover and similar) and the date of loss.</li>
</ul>

<h2 id="when-to-scope">When a scope helps most</h2>
<p>Order a scope before the carrier inspection if you want your own record of the damage going in; after the
inspection if the carrier's scope left items out; or before appraisal, when both sides need a clean list to compare.
Contractors use our scopes to document a job before work starts so nothing is lost when the old roof comes off.
Public adjusters use them as a starting point for the claim estimate.</p>
<p>If you already have the carrier's estimate and just want to know what is missing from it, the $50 <a
href="/services/insurance-claim-estimate-review/">claim estimate review</a> is the faster, cheaper option. If you need
the scope priced out, ask for a full <a href="/services/xactimate-roof-estimates/">line-item estimate</a>.</p>

<h2 id="limits">What a scope is, and is not</h2>
<p>Our scope documents physical damage and the repair it needs, based on the photos, measurements and information you
provide. It is not a coverage determination, an engineering report or legal advice, and we don't act as anyone's
adjuster. The <a href="/tools/roof-repair-cost-calculator/">Roof Repair Cost Calculator</a> is a good way to put rough
numbers on a small repair scope yourself.</p>
"""

SERVICE_PAGES = {
    "xactimate-roof-estimates": {
        "title": "Xactimate Roof Estimates, Built from Scratch | Roof Estimate Pro",
        "description": "Line-item residential roof estimates in the format carriers use, built from measurements and photos for contractors, public adjusters and homeowners.",
        "h1": "Xactimate-style roof estimates, built from scratch",
        "kicker": "Residential estimates",
        "lede": "Line-item roof estimates in the format carriers use, with every quantity tied to a measurement and every accessory that belongs on the roof. For contractors, public adjusters and homeowners in Texas and across the U.S.",
        "icon": "house",
        "service_type": "Roof estimating",
        "price_label": "Quoted per project",
        "order_href": "/get-estimate/",
        "order_label": "Request an estimate",
        "badges": ["Line items carriers recognize", "Built from your measurements", "Texas and other states"],
        "body": XACT_BODY,
        "included": [
            "Tear-off by layer and roof area, with disposal",
            "Roofing product by the square with waste tied to the roof geometry",
            "Starter, hip and ridge cap, drip edge, underlayment and valley treatment",
            "Step, counter and chimney flashing; pipe jacks; exhaust and ridge vents",
            "Steep and high-roof labor charges where the pitch and height call for them",
            "Detach-and-reset items: satellite, solar, gutters and guards",
            "Permits, overhead and profit as separate lines",
            "Notes explaining any quantity that is not obvious from the report",
        ],
        "need": [
            "Property address and the roof type (or your best guess)",
            "A measurement report, drone takeoff or a sketch with pitches and lengths",
            "Photos of every slope, plus close-ups of flashing, vents and edges",
            "The carrier's estimate, if this is an insurance claim",
            "What the estimate is for and any deadline you are working to",
        ],
        "deliverable": "A PDF line-item estimate organized by roof area and trade: quantities, units, unit prices, subtotals, overhead and profit, and a summary page, with notes on measurements and assumptions. Need it in a different layout or file type? Ask when you order.",
        "who": [
            "<strong>Roofing contractors</strong> sending claim pricing or supplements",
            "<strong>Public adjusters</strong> who need the estimate behind a claim",
            "<strong>Homeowners</strong> checking a carrier number or a bid",
            "<strong>Property managers and appraisers</strong> comparing several roofs",
        ],
        "tools": ["roof-replacement-cost-calculator", "roof-square-footage-calculator", "roof-pitch-calculator", "shingle-calculator"],
        "faqs": [
            ("Do you use Xactimate?",
             "<p>We build estimates with Xactimate-style line items, in the format carriers use, so a desk adjuster sees familiar line descriptions, units and organization. If your carrier or client needs a specific file type, tell us when you order and we will confirm what we can provide.</p>"),
            ("How much does a full roof estimate cost?",
             "<p>Full estimates are quoted per project, because a single-story gable and a three-building complex are very different jobs. Send the details through the <a href=\"/get-estimate/\">estimate request form</a> and we will quote it before any work starts.</p>"),
            ("Can you estimate a roof without visiting it?",
             "<p>Yes. All of our work is remote. A measurement report or accurate sketch gives us the quantities, and good photos show the materials, layers, flashing and damage. If something can't be confirmed from what you send, we say so in the estimate notes.</p>"),
            ("How long does it take?",
             "<p>It depends on the size of the roof and how complete the files are. We confirm a delivery time when you order, before you commit.</p>"),
            ("Will the carrier have to accept your estimate?",
             "<p>No estimate binds a carrier. A well-documented line-item estimate gives the adjuster specific items and quantities to respond to, which is usually far more productive than arguing over a total. What a policy covers is a separate question for your policy, adjuster or attorney.</p>"),
        ],
        "cta": ("Have a roof that needs a real number?", "Send the measurements and photos. We will quote the estimate first, then build it line by line in the format carriers use."),
    },
    "commercial-roof-estimates": {
        "title": "Commercial Roof Estimates: TPO, PVC, Mod-Bit & Metal | Roof Estimate Pro",
        "description": "Commercial roof estimates and takeoffs for TPO, PVC, EPDM, mod-bit, coatings and metal, including restoration vs. replacement options, in Texas and beyond.",
        "h1": "Commercial roof estimates and takeoffs",
        "kicker": "Commercial estimates",
        "lede": "Low-slope and steep-slope commercial roofs estimated line by line: membrane, insulation, edge metal, curbs, drains and every termination. For owners, property managers, contractors and adjusters.",
        "icon": "building",
        "service_type": "Commercial roof estimating",
        "price_label": "Quoted per project",
        "order_href": "/get-estimate/",
        "order_label": "Request a commercial estimate",
        "badges": ["TPO, PVC, EPDM, mod-bit, BUR", "Coatings and metal", "Restore vs. replace options"],
        "body": COMM_BODY,
        "included": [
            "Field takeoff by roof section and system, with layers to remove",
            "Insulation and cover board, including tapered systems and crickets",
            "Perimeter detail: parapets, coping, edge metal, gutters and scuppers",
            "Curbs, penetrations, drains, expansion joints and walkway pads",
            "Temporary repairs and detach-and-reset of rooftop equipment when required",
            "Side-by-side pricing for coating, recover and replacement on request",
            "Steep-slope and metal buildings on the same property, priced per building",
        ],
        "need": [
            "Address, building count and the roof system on each building",
            "Roof plan, aerial or drone measurements, or a dimensioned sketch",
            "Photos of the field, perimeter, parapets, curbs, drains and damage",
            "Core-cut or moisture-survey results, if you have them",
            "The carrier's estimate or engineer's report on a claim",
        ],
        "deliverable": "A PDF line-item estimate organized by building and roof section, with measured quantities, unit prices, subtotals and notes on system assumptions. When options are requested, each option is priced on its own page so they can be compared.",
        "who": [
            "<strong>Owners and property managers</strong> budgeting or comparing bids",
            "<strong>Commercial roofing contractors</strong> who need takeoff help",
            "<strong>Public and independent adjusters</strong> on commercial claims",
            "<strong>Appraisers and attorneys</strong> who need a documented number",
        ],
        "tools": ["flat-roof-calculator", "metal-roof-calculator", "roofing-bid-calculator"],
        "faqs": [
            ("What size commercial roofs do you estimate?",
             "<p>From a single strip-center roof to multi-building apartment and industrial properties. Larger projects simply take longer to measure and document, and we confirm a delivery time when you order.</p>"),
            ("Can you price a coating against a replacement?",
             "<p>Yes. Ask for options and we price coating restoration, recover and full replacement side by side. Moisture-survey or core-cut data matters here, because a coating over wet insulation is rarely a good investment.</p>"),
            ("Do you do moisture surveys or core cuts?",
             "<p>No. We are estimators and work remotely from the data you send. If a moisture survey or core cuts have been done, we build the estimate from those results and note it.</p>"),
            ("Do you estimate metal buildings?",
             "<p>Yes: exposed-fastener and standing seam metal roofs, including panel replacement, fasteners, trim and retrofit options. The free <a href=\"/tools/metal-roof-calculator/\">Metal Roof Calculator</a> is a good first look.</p>"),
            ("Is pricing different outside Texas?",
             "<p>Yes. We price for the property's market, so labor and material costs reflect where the building is. Our free tools use the same idea, with regional factors for Texas and other U.S. regions.</p>"),
        ],
        "cta": ("Need a commercial roof priced line by line?", "Send the roof plan, photos and any core-cut data. We will quote the takeoff first, with restoration and replacement options if you want them."),
    },
    "insurance-claim-estimate-review": {
        "title": "Roof Claim Estimate Review: $50 Per Claim | Roof Estimate Pro",
        "description": "Send the carrier's roof estimate and your photos. For $50 an estimator checks it line by line and lists the missing items, quantities and labor charges.",
        "h1": "Claim estimate review: what is the carrier's estimate missing?",
        "kicker": "$50 per claim",
        "lede": "Upload the carrier's estimate and your photos. An estimator compares them line by line and sends back a written list of everything missing or under-scoped, ready to forward to the desk adjuster.",
        "icon": "search",
        "service_type": "Insurance claim estimate review",
        "price": 50,
        "price_label": "$50 per claim",
        "order_href": "/claim/",
        "order_label": "Submit a claim for review",
        "badges": ["$50 flat per claim", "Line-by-line comparison", "Written list you can forward"],
        "body": REVIEW_BODY,
        "included": [
            "Squares, waste and linear quantities checked against the measurements",
            "Missing components: starter, ridge cap, drip edge, valley treatment, flashing",
            "Pipe jacks, vents, satellite and solar detach-and-reset, gutter items",
            "Steep and high-roof charges and additional tear-off layers",
            "Code items commonly left off, noted with the reason",
            "Overhead and profit flagged where several trades are involved",
        ],
        "need": [
            "The full carrier estimate (PDF or ESX), not just the summary",
            "Claim number, carrier, date of loss and property address",
            "Photos of every slope and close-ups of the details",
            "Measurement report, if you have one",
            "A short note on what was paid, denied or disputed",
        ],
        "deliverable": "A written list of missing and under-scoped items, each with the quantity and unit the roof supports, a short reason and photo references, plus a summary you can send to the desk adjuster or attach to a supplement.",
        "who": [
            "<strong>Homeowners</strong> who think the check looks low",
            "<strong>Roofing contractors</strong> preparing a supplement",
            "<strong>Public adjusters</strong> who want a second set of eyes",
            "<strong>Property managers</strong> handling several claims at once",
        ],
        "tools": ["roof-insurance-claim-calculator", "roof-depreciation-calculator", "roof-square-footage-calculator"],
        "faqs": [
            ("What does the $50 review include?",
             "<p>A line-by-line comparison of the carrier's roof estimate against your photos and measurements, and a written list of the items and quantities that are missing or short, with the reason for each. Payment is collected by secure Stripe checkout after you <a href=\"/claim/\">submit the claim</a>.</p>"),
            ("Will you talk to the insurance company for me?",
             "<p>No. We prepare the review for you to use. You, your contractor or your licensed public adjuster can send it to the carrier. We don't negotiate claims or give coverage or legal advice.</p>"),
            ("What if the carrier's estimate is completely wrong?",
             "<p>If the gaps are large, a list of missing items is not the best tool. We will tell you, and we can write a complete <a href=\"/services/xactimate-roof-estimates/\">line-item estimate</a> from scratch instead.</p>"),
            ("Do you review estimates from any carrier and any state?",
             "<p>Yes. The review works the same way for any carrier's estimate, for properties in Texas and other states.</p>"),
            ("Can you review a denied claim?",
             "<p>If there is no carrier estimate, there is nothing to compare. A <a href=\"/services/scope-of-damages/\">scope of damages</a> documents the damage instead, which is often the better first step after a denial. Questions about the denial itself belong with your policy, a public adjuster or an attorney.</p>"),
        ],
        "cta": ("Think the carrier's estimate is short?", "For $50 an estimator checks it against the roof and lists exactly what is missing. Submit the claim and upload the estimate and photos."),
        "cta_href": "/claim/", "cta_label": "Submit a claim",
    },
    "scope-of-damages": {
        "title": "Scope of Damages for Roof & Property Claims: $200 | Roof Estimate Pro",
        "description": "Order a professional scope of damages for $200, built from your photos and measurements, or document the damage yourself with a DIY scope on PAscope.com.",
        "h1": "Scope of damages, professional or DIY",
        "kicker": "$200 per property",
        "lede": "An itemized record of what the loss damaged and what each item needs, with quantities, cause-of-loss notes and code items. Order one from our estimators, or build your own on PAscope.com.",
        "icon": "clip",
        "service_type": "Scope of damages",
        "price": 200,
        "price_label": "$200 per property",
        "order_href": "/get-a-scope/",
        "order_label": "Order a scope",
        "badges": ["$200 per property", "Roof, exterior and interior", "DIY option on PAscope.com"],
        "body": SCOPE_BODY,
        "included": [
            "Slope-by-slope roof scope: system, layers, pitch and damaged components",
            "Room-by-room interior scope for leak damage when needed",
            "Exterior items hit by the same storm: gutters, siding, trim, screens, fences",
            "Repair method for each item: replace, repair, clean or detach and reset",
            "Quantities tied to the measurements and photos",
            "Cause-of-loss notes and the code items that apply",
        ],
        "need": [
            "Property address, type of damage and cause of loss",
            "Date of loss and the carrier, if a claim is open",
            "Photos of every elevation and slope, with close-ups of the damage",
            "Measurement reports (EagleView, Hover or similar) if available",
            "Access notes or anything you have already been told about the loss",
        ],
        "deliverable": "A written scope of damages organized by roof area, elevation and room, listing every damaged item with its quantity and repair method, plus cause-of-loss notes. It is ready to hand to the carrier, an appraiser or the estimator who will price it.",
        "who": [
            "<strong>Homeowners</strong> who want their own record before or after the inspection",
            "<strong>Contractors</strong> documenting a job before tear-off",
            "<strong>Public adjusters</strong> who need a starting scope",
            "<strong>Appraisers and attorneys</strong> preparing for appraisal or a dispute",
        ],
        "tools": ["roof-repair-cost-calculator", "roof-insurance-claim-calculator", "gutter-calculator"],
        "faqs": [
            ("What is the difference between a scope and an estimate?",
             "<p>A scope lists what was damaged and what each item needs, with quantities. An estimate puts unit prices on that list. If you need both, ask for a <a href=\"/services/xactimate-roof-estimates/\">line-item estimate</a>, which includes the scope.</p>"),
            ("What does the $200 scope cover?",
             "<p>One property and one loss: the roof, and the exterior and interior items affected by the same event if you choose that damage type on the <a href=\"/get-a-scope/\">order form</a>. Payment is collected by secure Stripe checkout after you submit.</p>"),
            ("What is the DIY option?",
             "<p>On <a href=\"https://pascope.com/\" rel=\"noopener\" target=\"_blank\">PAscope.com</a> you document and submit the property damage yourself for a fast, low-cost evaluation. It suits people who are comfortable photographing the property methodically.</p>"),
            ("Do you inspect the property in person?",
             "<p>No. Scopes are prepared remotely from your photos, measurements and notes. That is why the photo checklist on this page matters: the better the photos, the more complete the scope.</p>"),
            ("Is the scope a coverage opinion?",
             "<p>No. It documents physical damage and the repair it needs. Whether a policy covers it is a separate question for your policy, adjuster or attorney.</p>"),
        ],
        "cta": ("Want the damage documented properly?", "Order a $200 professional scope from your photos and measurements, or build your own on PAscope.com."),
        "cta_href": "/get-a-scope/", "cta_label": "Order a scope",
    },
}

# Hub card copy, per service slug.
HUB_CARDS = {
    "xactimate-roof-estimates": ("Residential line-item estimates",
        "Replacement and repair estimates built from scratch in the format carriers use, with every accessory, labor charge and quantity documented."),
    "commercial-roof-estimates": ("Commercial roof estimates",
        "TPO, PVC, EPDM, mod-bit, BUR, coatings and metal. Takeoffs by section with parapets, curbs and drains, and restore-vs-replace options."),
    "insurance-claim-estimate-review": ("Claim estimate review",
        "Send the carrier's estimate and photos. We compare them line by line and list what is missing or short, ready to forward."),
    "scope-of-damages": ("Scope of damages",
        "An itemized record of what the loss damaged and how each item should be repaired. Order one from us, or go DIY on PAscope.com."),
}


# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------


def service_schema(g, s, d, path):
    sch = {"@type": "Service", "@id": g["url"](path) + "#service", "name": s["name"],
           "serviceType": d["service_type"], "description": d["description"],
           "provider": {"@id": g["ORG_ID"]}, "areaServed": AREA_SERVED, "url": g["url"](path)}
    if d.get("price"):
        sch["offers"] = {"@type": "Offer", "price": str(d["price"]), "priceCurrency": "USD",
                         "url": g["url"](d["order_href"])}
    return sch


def build_service(g, s):
    d = SERVICE_PAGES[s["slug"]]
    icon, esc, BIZ = g["icon"], g["esc"], g["BIZ"]
    path = f"/services/{s['slug']}/"
    trail = [("Home", "/"), ("Services", "/services/"), (s["name"], None)]
    body = g["ensure_h2_ids"](d["body"])
    badges = "".join(f"<li>{icon('check')}{b}</li>" for b in d["badges"])
    hero_extra = (f'<div class="btn-row"><a class="btn btn--peach" href="{d["order_href"]}">{d["order_label"]} {icon("arrow")}</a>'
                  f'<a class="btn btn--ghost-light" href="tel:{BIZ["phone_href"]}">{icon("phone")}{BIZ["phone_display"]}</a></div>'
                  f'<ul class="hero-badges">{badges}</ul>')
    tools = [g["TOOL_BY_SLUG"][t] for t in d["tools"] if t in g["TOOL_BY_SLUG"]]
    tool_lis = "".join(f'<li><a href="/tools/{t["slug"]}/">{icon(t["icon"])}{esc(t["short"])}</a></li>' for t in tools)
    others = "".join(f'<li><a href="/services/{o["slug"]}/">{icon("arrow")}{esc(o["name"])}</a></li>'
                     for o in g["SERVICES"] if o["slug"] != s["slug"])
    side = (f'<div class="side-card side-card--cta"><h3>{esc(s["name"])}</h3>'
            f'<p><span class="price-tag"><b>{d["price_label"].split(" ", 1)[0]}</b>{(" " + d["price_label"].split(" ", 1)[1]) if " " in d["price_label"] else ""}</span></p>'
            f'<p>Remote, from your photos, measurements and documents. Texas and other states.</p>'
            f'<a class="btn btn--peach btn--sm" href="{d["order_href"]}">{d["order_label"]}</a></div>'
            f'<div class="side-card"><h3>Free tools for this job</h3><ul>{tool_lis}</ul></div>'
            f'<div class="side-card"><h3>Other services</h3><ul>{others}</ul></div>')
    related = "".join(g["tool_card"](t, tag=False) for t in tools[:3])
    faqs = d["faqs"]
    main = f"""<section class="section"><div class="wrap"><div class="article-layout">
  <article class="prose">{g['toc'](body)}{body}</article>
  <aside class="article-side">{side}</aside>
</div></div></section>
<section class="section section--paper"><div class="wrap">
  <div class="section-head"><span class="kicker">The details</span><h2>What's included and what we need from you</h2>
    <p>Everything below is done remotely. The more complete the files, the more complete the result.</p></div>
  <div class="grid grid--2">
    <div class="card" data-reveal><span class="ico">{icon('check')}</span><h3>What's included</h3>{_checks(d['included'])}</div>
    <div class="card" data-reveal style="--d:.08s"><span class="ico">{icon('clip')}</span><h3>What we need from you</h3>{_checks(d['need'])}
      <p>Files too large for the form? Email them to <a href="mailto:{BIZ['email']}">{BIZ['email']}</a>.</p></div>
    <div class="card" data-reveal><span class="ico">{icon('file')}</span><h3>What you get</h3><p>{d['deliverable']}</p>
      <p style="margin-top:16px"><span class="price-tag"><b>{d['price_label'].split(' ', 1)[0]}</b>{(' ' + d['price_label'].split(' ', 1)[1]) if ' ' in d['price_label'] else ''}</span></p></div>
    <div class="card" data-reveal style="--d:.08s"><span class="ico">{icon('user')}</span><h3>Who it's for</h3>{_checks(d['who'])}</div>
  </div>
</div></section>
<section class="section related-section"><div class="wrap">
  <div class="section-head"><span class="kicker">Free tools</span><h2>Run the numbers yourself first</h2>
    <p>Our calculators use the same itemized approach, with Texas 2026 pricing you can edit. <a href="/tools/">See all 12 tools</a>.</p></div>
  <div class="related">{related}</div>
</div></section>
{g['faq_html'](faqs, heading=f"{esc(s['name'])}: common questions")}"""
    cta_t, cta_x = d["cta"]
    cta = g["cta_band"](cta_t, cta_x)
    if d.get("cta_href"):
        cta = cta.replace('href="/get-estimate/">Talk to an estimator', f'href="{d["cta_href"]}">{d["cta_label"]}')
    main += cta
    g["build_prose"]({
        "path": path, "title": d["title"], "description": d["description"], "h1": d["h1"], "lede": d["lede"],
        "kicker": d["kicker"], "trail": trail, "active": "/services/", "priority": "0.8",
        "html": main, "no_cta": True, "hero_extra": hero_extra,
        "extra_schema": [service_schema(g, s, d, path), g["faq_schema"](faqs, path)],
    })


HUB_FAQS = [
    ("How much do your services cost?",
     "<p>A <a href=\"/services/insurance-claim-estimate-review/\">claim estimate review</a> is $50 per claim and a professional <a href=\"/services/scope-of-damages/\">scope of damages</a> is $200 per property. Full residential and commercial estimates are quoted per project before any work starts. The 12 <a href=\"/tools/\">calculators</a> are free.</p>"),
    ("Do you come out to the property?",
     "<p>No. Everything is done remotely from photos, measurement reports, drone images, carrier estimates and your notes. That is how we can serve every part of Texas and other states.</p>"),
    ("Are you a roofing contractor?",
     "<p>No. We prepare estimates and scopes; we don't sell or install roofs. That keeps the estimate about the roof, not about a sale.</p>"),
    ("Which service should I start with?",
     "<p>If you have a carrier estimate and think it is short, start with the $50 review. If there is no estimate yet, or the claim was denied, start with a scope. If you need a priced number for a bid, a claim or a budget, ask for a full estimate. Not sure? <a href=\"/get-estimate/\">Tell us what you have</a> and we will point you to the right one.</p>"),
]


def build_hub(g):
    icon, esc, BIZ = g["icon"], g["esc"], g["BIZ"]
    path = "/services/"
    trail = [("Home", "/"), ("Services", None)]
    cards = []
    for i, s in enumerate(g["SERVICES"]):
        d = SERVICE_PAGES[s["slug"]]
        h, txt = HUB_CARDS[s["slug"]]
        p1, _, p2 = d["price_label"].partition(" ")
        cards.append(
            f'<div class="card" data-reveal style="--d:{i % 2 * 0.08:.2f}s"><span class="ico">{icon(d["icon"])}</span>'
            f'<h3>{h}</h3><p>{txt}</p>'
            f'<p style="margin-top:16px"><span class="price-tag"><b>{p1}</b> {p2}</span></p>'
            f'<div class="btn-row" style="margin-top:18px"><a class="btn btn--sm" href="/services/{s["slug"]}/">Learn more {icon("arrow")}</a>'
            f'<a class="btn btn--ghost btn--sm" href="{d["order_href"]}">{d["order_label"]}</a></div></div>')
    who = [
        ("hardhat", "Roofing contractors", "Claim pricing, supplements and bids without spending your evenings in estimating software. Send the report and photos; get back a line-item estimate you can put your name behind."),
        ("briefcase", "Public adjusters", "The estimate behind the claim presentation, a second look at a carrier estimate, or a scope to start the file. You run the claim; we build the numbers."),
        ("clip", "Desk and independent adjusters", "Overflow estimating after a storm, or an independent check on a contractor's estimate, in the line-item format your file needs."),
        ("house", "Homeowners", "Find out whether the carrier's check or a contractor's bid is in the right range, in plain language, before you sign anything."),
        ("building", "Property managers and owners", "Several buildings, several roofs, one consistent method. Budget numbers, bid comparisons and claim documentation."),
        ("file", "Attorneys and appraisers", "Documented, itemized estimates and scopes for appraisal and disputes, with every quantity traceable to a measurement or photo."),
    ]
    who_html = "".join(
        f'<div class="card" data-reveal style="--d:{i % 3 * 0.06:.2f}s"><span class="ico">{icon(ic)}</span><h3>{h}</h3><p>{t}</p></div>'
        for i, (ic, h, t) in enumerate(who))
    send = _checks([
        "Photos of every slope and elevation, plus close-ups of damage and details",
        "Measurement reports: EagleView, Hover, GAF QuickMeasure, Roofr or a drone takeoff",
        "Carrier estimates as PDF or ESX, engineer reports, core-cut data",
        "A field sketch with pitches and lengths if there is no report",
        "The address, the deadline and what the number is for",
    ])
    get = _checks([
        "Line items in the format carriers use, with quantities, units and unit prices",
        "Waste, steep and high charges shown as their own figures",
        "Notes that explain every quantity that isn't obvious",
        "Pricing for the property's market, not ours",
        "A PDF you can forward to a carrier, client, lender or appraiser",
    ])
    tools = "".join(g["tool_card"](t) for t in g["TOOLS"][:6])
    main = f"""<section class="section section--paper"><div class="wrap">
  <div class="section-head"><span class="kicker">What we do</span><h2>Four ways we can help</h2>
    <p>Each service is done remotely by an estimator, for properties anywhere in Texas and in other states.</p></div>
  <div class="grid grid--2">{''.join(cards)}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><span class="kicker">Who we work with</span><h2>Built for the people who live in roof estimates</h2>
    <p>Most of our work comes from people who need a number that holds up in front of someone else: a carrier, a client, an appraiser or a judge.</p></div>
  <div class="grid grid--3">{who_html}</div>
</div></section>
<section class="section section--dark"><div class="wrap">
  <div class="section-head"><span class="kicker">The exchange</span><h2>What you send us, and what you get back</h2>
    <p>No site visit, no software to buy. If you have more than the form can carry, email it to {BIZ['email']}.</p></div>
  <div class="grid grid--2">
    <div class="card card--dark" data-reveal><span class="ico">{icon('mail')}</span><h3>You send</h3>{send}</div>
    <div class="card card--dark" data-reveal style="--d:.08s"><span class="ico">{icon('file')}</span><h3>You get</h3>{get}</div>
  </div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><span class="kicker">How an order works</span><h2>From files to finished estimate</h2></div>
  <div class="steps">
    <div class="step" data-reveal><h3>Send the details</h3><p>Use the <a href="/get-estimate/">estimate form</a>, the <a href="/claim/">claim form</a> or the <a href="/get-a-scope/">scope form</a>, and attach what you have.</p></div>
    <div class="step" data-reveal style="--d:.06s"><h3>We confirm scope</h3><p>We review the files, ask for anything missing, and confirm the price and a delivery time.</p></div>
    <div class="step" data-reveal style="--d:.12s"><h3>We build it</h3><p>Measurements reconciled, every line item written and priced for the property's market.</p></div>
    <div class="step" data-reveal style="--d:.18s"><h3>You review</h3><p>Questions and corrections are part of the job. <a href="/how-it-works/">See the full process</a>.</p></div>
  </div>
</div></section>
<section class="section section--paper"><div class="wrap">
  <div class="section-head"><span class="kicker">Free tools</span><h2>Or run the numbers yourself</h2>
    <p>Twelve free calculators with Texas 2026 pricing, editable unit prices and printable results. <a href="/tools/">Browse all tools</a>.</p></div>
  <div class="grid grid--3">{tools}</div>
</div></section>
{g['faq_html'](HUB_FAQS, heading="Questions about our services")}"""
    main += g["cta_band"]()
    g["build_prose"]({
        "path": path,
        "title": "Roof Estimating Services for Texas & Beyond | Roof Estimate Pro",
        "description": "Line-item residential and commercial roof estimates, $50 claim estimate reviews and $200 scopes of damages, prepared remotely for Texas and other states.",
        "h1": "Roof estimating services",
        "kicker": "Professional services",
        "lede": "When a free calculator is not enough, our estimators build the estimate for you: line-item residential and commercial estimates in the format carriers use, claim estimate reviews and scopes of damages. All remote, for every part of Texas and other states.",
        "hero_extra": (f'<div class="btn-row"><a class="btn btn--peach" href="/get-estimate/">Request an estimate {icon("arrow")}</a>'
                       f'<a class="btn btn--ghost-light" href="/claim/">Submit a claim for review</a></div>'),
        "trail": trail, "active": "/services/", "priority": "0.8", "html": main, "no_cta": True,
        "extra_schema": [
            {"@type": "ItemList", "@id": g["url"](path) + "#services", "itemListElement": [
                {"@type": "ListItem", "position": i, "url": g["url"](f"/services/{s['slug']}/"), "name": s["name"]}
                for i, s in enumerate(g["SERVICES"], 1)]},
            g["faq_schema"](HUB_FAQS, path)],
    })


def build(g):
    build_hub(g)
    for s in g["SERVICES"]:
        build_service(g, s)
