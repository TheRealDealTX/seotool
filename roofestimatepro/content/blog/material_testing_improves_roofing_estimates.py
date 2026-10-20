INFO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/>'
            '<path d="M12 8h.01"/></svg>')

body = f"""
<p>Most roofing estimates are built from three things: a measurement report, a set of photos and the estimator's
assumptions about what is under the surface. The measurements are usually right. The photos are usually useful. The
assumptions are where the money gets lost. A low-slope roof that turns out to have two layers and wet insulation, or a
shingle roof whose discontinued product cannot be matched, changes the scope far more than a few squares of
measurement error ever will.</p>
<p>Field testing replaces those assumptions with facts. None of the tests below are exotic; most take less than an hour
and cost little next to the price of a wrong scope. This guide covers the tests that actually change an estimate, what
each one tells you, and how to put the result into the line items.</p>

<h2 id="why-testing-changes-the-number">Why testing changes the number, not just the paperwork</h2>
<p>An estimate is a list of quantities multiplied by unit prices. Testing almost never changes the unit prices. It
changes the quantities and, more often, which line items belong on the estimate at all. A few examples of what one
test can move:</p>
<ul>
  <li><strong>Number of existing layers.</strong> On a flat roof, each extra layer of tear-off runs about $1.50 to $3.00
  per square foot. On a 20,000 sf building, one unexpected layer is $30,000 to $60,000 of work that was not in the bid.</li>
  <li><strong>Wet insulation.</strong> Wet board cannot be covered over. If a recover was planned, the scope becomes a
  partial or full tear-off plus new insulation.</li>
  <li><strong>Repairability.</strong> If a shingle cannot be lifted and resealed without breaking, a "repair" estimate
  is not a real option, and the claim discussion shifts toward replacement of the slope or the roof.</li>
  <li><strong>Product availability.</strong> If the installed shingle is discontinued, matching questions come up that
  decide whether one slope or the whole roof is on the estimate.</li>
</ul>
<p>The point is not to run every test on every job. It is to know which unknown is the most expensive one on this roof
and test that one before the number goes out.</p>

<h2 id="low-slope-core-cuts">Core cuts on low-slope roofs</h2>
<p>A core cut is a small sample cut through the roof system down to the deck, usually 2 to 4 inches across, then patched
the same day. It is the single most useful test on a commercial or flat residential roof because it answers the
questions a drone photo cannot.</p>
<h3>What a core cut tells you</h3>
<ul>
  <li><strong>Layer count and type.</strong> A TPO membrane over a gravel BUR over another BUR is a three-layer tear-off,
  and the bottom layers often weigh much more than the top one, which affects disposal and labor.</li>
  <li><strong>Insulation type and thickness.</strong> Polyiso, perlite, wood fiber, EPS or none. Thickness tells you the
  existing R-value (polyiso runs roughly R-5.7 per inch) and whether a replacement will trigger an energy code upgrade.</li>
  <li><strong>Moisture.</strong> Insulation that is damp, crumbly or heavy in the hand is a red flag. Wet perlite and wood
  fiber board lose strength and can no longer hold fasteners well.</li>
  <li><strong>Deck type.</strong> Steel, wood, concrete, gypsum or tectum. The deck decides the fastener type, pull-out
  values and whether mechanical attachment is even possible.</li>
  <li><strong>Attachment of the existing system.</strong> Mopped, adhered or mechanically fastened, which affects
  how hard and how slow the tear-off will be.</li>
</ul>
<h3>Where to cut</h3>
<p>One core cut is a guess with a sample size of one. Take several: near drains, near the worst-looking area, in an
area that looks sound, and on each roof section that may have been built at a different time. Additions and
re-roofed sections often have different layer counts than the original building. Get the owner's permission, patch
each cut properly and photograph the sample next to a tape measure.</p>

<figure><img src="/assets/img/blog/Real-World-Applications-in-Roofing-Projects-1200.webp" alt="Roofing crew inspecting and sampling a commercial low-slope roof before pricing the job" width="1200" height="800" loading="lazy"><figcaption>Sampling several areas of a low-slope roof before pricing catches extra layers and wet insulation that photos miss.</figcaption></figure>

<h2 id="moisture-surveys">Infrared and moisture surveys</h2>
<p>Core cuts tell you what is happening at a point. A moisture survey tells you how much of the roof it is happening
across, which is what you need for a quantity.</p>
<div class="table-wrap"><table>
  <thead><tr><th>Method</th><th>How it works</th><th>Best use</th><th>Limits</th></tr></thead>
  <tbody>
    <tr><td>Infrared (thermal) scan</td><td>Wet insulation holds heat longer after sunset and shows as warm areas</td><td>Fast coverage of large roofs; mapping wet areas</td><td>Needs a clear, sunny day and a dry surface; ballast and reflective membranes can mask readings</td></tr>
    <tr><td>Capacitance / impedance meter</td><td>Measures changes in electrical properties of the roof system on a grid</td><td>Grid surveys of smaller roofs; verifying infrared hits</td><td>Reads only the upper part of the system; surface water and metal affect readings</td></tr>
    <tr><td>Nuclear moisture gauge</td><td>Counts hydrogen in the roof assembly on a grid</td><td>Ballasted or thick systems</td><td>Licensed operators only; slower</td></tr>
    <tr><td>Core cuts (verification)</td><td>Physical sample of suspect and dry areas</td><td>Confirming every survey before it goes in an estimate</td><td>Point data only</td></tr>
  </tbody>
</table></div>
<p>Texas makes infrared work well and badly in the same week. Strong sun loads the roof with heat, which helps the scan,
but Gulf Coast humidity and evening dew can wet the surface and blur the image. Scan on a clear evening after a sunny
day, with no rain in the last day or so, and verify the hot spots with cores.</p>
<p>The output you want is a marked-up roof plan with wet areas outlined and measured. That turns into line items:
remove wet insulation, replace with new board of matching thickness, and either re-cover the dry areas or tear off
everything. Run the dry and wet quantities through the <a href="/tools/flat-roof-calculator/">flat and commercial roof
calculator</a> both ways to see where the recover-versus-replace line falls.</p>

<h2 id="shingle-testing">Shingle brittleness and repairability</h2>
<p>On steep-slope claims, the argument is often not whether a shingle is damaged but whether it can be repaired. A repair
means lifting the shingles above the damaged one, pulling nails, sliding a new shingle in and resealing. On an older or
heat-aged roof, the surrounding shingles may crack or tear when lifted, so the repair causes new damage.</p>
<h3>How a brittleness test is done</h3>
<p>The tester gently lifts the tabs of several undamaged shingles in different areas of the roof, often at a set
temperature range, and records whether the sealant releases cleanly and whether the shingle creases, cracks or tears.
Photos and video of each attempt are what make the result useful. Do it on more than one slope, since a south or west
slope in Texas usually takes far more heat than a north slope and may fail when the north side passes.</p>
<p>A failed test does not automatically mean the carrier owes a full roof. It is evidence that a repair estimate is not
realistic for that area. Combine it with the damage count on each slope and a cost comparison from the
<a href="/tools/roof-repair-cost-calculator/">roof repair cost calculator</a> to show what repair would really involve.</p>

<div class="callout">{INFO_SVG}
<p><strong>Test in the conditions the repair would happen in.</strong> Shingles are more pliable in the afternoon heat
and stiffer on a cool morning. Note the time and temperature of every brittleness test. A result taken at 7 a.m. in
February will be challenged; one taken mid-day on several slopes, with video, is much harder to dismiss.</p></div>

<h2 id="shingle-identification">Shingle identification and availability</h2>
<p>When part of a roof needs replacing, the next question is whether new material can be found that matches the old.
Manufacturers change colors and discontinue lines regularly, and an older three-tab or a discontinued laminate can be
hard or impossible to source.</p>
<p>Material identification services, ITEL is the name most adjusters know, take a physical sample and report the likely
manufacturer, product line and whether a comparable product is still available, sometimes with pricing. On the
contractor side, you can do a basic version yourself: measure the exposure and overall size (metric and English
shingles differ), photograph the back for markings, and call distributors with a sample in hand.</p>
<p>How a mismatch is handled depends on the policy and the carrier. Texas does not have a general statute requiring
insurers to replace undamaged areas for matching; it comes down to policy language, any endorsements and the
adjuster's call. Document the facts either way: what was tested, what was found and which products were checked.
The <a href="/tools/roof-insurance-claim-calculator/">roof insurance claim calculator</a> helps you see what a slope-only
versus full-roof settlement would pay after deductible and depreciation.</p>

<h2 id="deck-and-test-squares">Deck probes and hail test squares</h2>
<h3>Deck condition</h3>
<p>Decking is the most common surprise on residential tear-offs. You can reduce the surprise before tear-off by walking
the roof for soft spots, checking from the attic for stains, delamination and daylight, and probing suspect areas
with an awl or moisture meter from below. Board-by-board certainty is not possible before the shingles come off, so
price decking as a stated allowance (for example, a number of sheets at a per-sheet price) and say so in the estimate.</p>
<h3>Hail test squares</h3>
<p>A test square is a marked 10 ft by 10 ft area on each slope where hail impacts to the shingles are counted. It is how
most field adjusters and engineers measure hail damage consistently, and it is how they decide whether a slope is
repaired or replaced. Mark hits with chalk, photograph the full square and close-ups, and record soft metal impacts
(vents, flashing, gutters) separately, since they help establish hail size and direction.</p>
<p>Some carriers use an internal count of hits per square as a threshold for replacement. That threshold is a guideline,
not policy language, so a well-documented square on each slope matters more than hitting a magic number. Test the
slopes facing the storm direction first, then every other slope, and do not skip a slope because it looks clean
from the ground.</p>

<h2 id="putting-results-in-the-estimate">Putting test results into the estimate</h2>
<p>Testing only helps if the results end up in the line items and the supporting file. A practical layout:</p>
<div class="table-wrap"><table>
  <thead><tr><th>Test</th><th>What it changes</th><th>Typical line items affected</th></tr></thead>
  <tbody>
    <tr><td>Core cuts</td><td>Tear-off layers, insulation scope, fastener type</td><td>Tear-off per layer, insulation board, cover board, fasteners and plates</td></tr>
    <tr><td>Moisture survey</td><td>Wet area quantity; recover vs replace</td><td>Remove and replace wet insulation (sf), membrane over affected area</td></tr>
    <tr><td>Brittleness test</td><td>Repair vs slope or roof replacement</td><td>Shingle replacement by slope, starter, ridge, underlayment</td></tr>
    <tr><td>Material identification</td><td>Matching and availability</td><td>Shingle line and quantity; additional slopes</td></tr>
    <tr><td>Test squares</td><td>Damage per slope</td><td>Slope-by-slope replacement, soft metal items</td></tr>
    <tr><td>Deck probes</td><td>Decking allowance</td><td>Sheathing replacement (sheets or sf)</td></tr>
  </tbody>
</table></div>
<p>Keep the evidence with the estimate: photos with a scale reference, a roof plan showing where each test was taken,
the date and time, and a one-line result for each. When an adjuster or owner asks why a line item is there, the answer
should be one photo away.</p>
<p>If you are building the estimate for a claim, our <a href="/services/xactimate-roof-estimates/">Xactimate-format roof
estimates</a> are built from exactly this kind of field data. If the carrier already wrote an estimate and ignored your
test results, a <a href="/services/insurance-claim-estimate-review/">claim estimate review</a> lays out what is missing.</p>

<h2 id="practical-testing-plan">A testing plan to use on your next bid</h2>
<p>Before you price any roof, write down the one unknown that would hurt most if you guessed wrong, then pick the test
that answers it:</p>
<ol>
  <li><strong>Flat roof, any age:</strong> at least three core cuts, more on larger or multi-section roofs. Add an infrared
  scan if the building has a history of leaks or the cores show any moisture.</li>
  <li><strong>Shingle roof on a hail claim:</strong> a test square on every slope, soft metal documentation, and a
  brittleness test on the slopes where a repair is being proposed.</li>
  <li><strong>Partial replacement or older shingle:</strong> identify the product and check availability before the
  scope is finalized.</li>
  <li><strong>Any tear-off:</strong> an attic check and a written decking allowance.</li>
</ol>
<p>Then put each result into the estimate as a quantity or a line item, attach the photos, and price it. An estimate
built this way is slower by an hour and far less likely to be wrong by a truckload.</p>
"""

POST = {
    "slug": "material-testing-improves-roofing-estimates",
    "title": "Roof Material Testing for Better Estimates | Roof Estimate Pro",
    "h1": "How Material Testing Makes Roofing Estimates More Accurate",
    "description": "Core cuts, moisture scans, brittleness tests, shingle ID and hail test squares: the field tests that change a roofing estimate and how to use the results.",
    "published": "2026-04-17T08:24:56-05:00",
    "modified": "2026-10-20",
    "category": "Estimating",
    "image": "How-Material-Testing-Improves-Roofing-Estimates-and-Helps-Contractors-Avoid-Costly-Errors",
    "image_alt": "Roofer examining roofing material samples on a job site before preparing an estimate",
    "excerpt": "Core cuts, moisture surveys, brittleness tests and shingle ID turn roofing guesses into quantities. Here is which test to run and how it changes the estimate.",
    "lede": "The tests that find extra layers, wet insulation, unrepairable shingles and unmatched products before they blow up your scope.",
    "body": body,
    "faqs": [
        ("How many core cuts does a flat roof need before an estimate?",
         "<p>There is no fixed rule, but one is rarely enough. Take at least three on a small roof, and more on larger roofs or "
         "buildings with additions or sections re-roofed at different times. Cut near drains, in suspect areas and in sound "
         "areas, and patch each cut the same day.</p>"),
        ("Can I re-cover a flat roof if the insulation is wet?",
         "<p>No. Building codes and manufacturers do not allow a recover over wet or deteriorated insulation, and most codes "
         "also limit recovers when two or more roof layers already exist. Wet areas have to be removed and replaced. Check "
         "the code your city has adopted and the manufacturer's requirements for the new system.</p>"),
        ("Does a failed brittleness test mean insurance must replace the whole roof?",
         "<p>Not automatically. It is evidence that repairs are not practical in the tested areas. Coverage still depends "
         "on the policy, the storm damage found and the adjuster's review. Document tests on several slopes with video, "
         "time and temperature.</p>"),
        ("What is an ITEL report on a roofing claim?",
         "<p>It is a material identification report. A shingle sample is sent in, and the report gives the likely "
         "manufacturer and product line, whether it is still available and what comparable products exist. Adjusters use "
         "it to decide matching and pricing questions.</p>"),
        ("What is a hail test square?",
         "<p>A marked 10 ft by 10 ft area on each roof slope where hail hits are counted and photographed. It gives a "
         "consistent damage measurement per slope, which drives whether the slope is repaired or replaced.</p>"),
    ],
    "related_tools": ["flat-roof-calculator", "roof-repair-cost-calculator", "roof-insurance-claim-calculator"],
}
