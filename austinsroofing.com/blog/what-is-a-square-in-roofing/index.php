<?php
require dirname(__DIR__, 2) . '/includes/layout.php';

$body = <<<'HTML'
<div class="takeaways">
  <p class="takeaways__title">Key takeaways</p>
  <ul>
    <li>One roofing square = 100 square feet of roof surface, which is a 10 ft × 10 ft area.</li>
    <li>Roof area is larger than your home's square footage, and pitch makes the difference bigger. A 6/12 roof has about 12% more surface than its footprint.</li>
    <li>Most standard architectural shingles come 3 bundles to a square. Heavier designer shingles can take 4–5.</li>
    <li>Add 10–15% waste for most roofs. Roofing cost per square is how contractors, suppliers and insurance adjusters all compare prices.</li>
  </ul>
</div>

<p class="lead">What is a square in roofing? A roofing square is 100 square feet of roof surface, an area 10 feet by 10 feet. Roofers, shingle manufacturers, suppliers and insurance adjusters all measure and price roofs in squares, so understanding this one unit is the fastest way to read a roofing estimate and tell whether two quotes really cover the same roof.</p>

<p>This guide explains how to calculate roofing squares yourself. It covers why pitch matters so much, how many bundles of shingles make a square, how much waste to add, and what a square of shingles costs installed. Every example uses real roof shapes common around Austin and Central Texas. If you want to skip the math, the <a href="/roofing-tools/roofing-square-calculator/">roofing square calculator</a> does it for you.</p>

<h2 id="h-understanding-roofing-measurements-and-why-they-matter">Why Roofing Measurements Matter to Homeowners</h2>
<p>Every number on a roofing estimate comes from the measurement: shingles, underlayment, labor, dumpster size, even the ridge vent. If one contractor measures 24 squares and another measures 28, their quotes will differ by thousands of dollars before anyone has picked a shingle. When you know how squares work, you can ask the right question ("How many squares did you measure, and what waste factor did you use?") instead of guessing which quote is padded.</p>

<h2 id="h-what-is-a-square-in-roofing">What Is a Square in Roofing? The Definition</h2>
<p>A roofing square is a unit of area equal to <strong>100 square feet of finished roof surface</strong>. It measures the actual sloped surface that gets covered, not the floor below and not the footprint seen from above. A roof that measures 2,300 square feet of surface is a 23-square roof.</p>

<h3 id="h-visualizing-one-roofing-square">Picturing One Roofing Square</h3>
<p>Picture a 10 ft × 10 ft patch of roof, about the size of a small bedroom floor tipped up onto the slope. A typical single-story Austin ranch house with an attached garage has somewhere between 20 and 30 of those patches on its roof.</p>

<h3 id="h-why-roofers-still-use-squares-instead-of-square-feet">Why Roofers Use Squares Instead of Square Feet</h3>
<p>Squares keep the numbers manageable and line up with how materials are packaged. Shingle manufacturers design their bundles so that a set number covers exactly one square. Saying "26 squares" is easier than "2,600 square feet," and it converts straight to bundles, rolls of underlayment and crew hours.</p>

<h3 id="h-a-short-history-of-roofing-squares">A Short History of the Roofing Square</h3>
<p>The square dates back to when roofs were covered with wood shingles, slate and clay tile. Tradespeople needed a standard unit for ordering and pricing jobs by hand, and 100 square feet was easy to measure and multiply. When asphalt shingles took over in the twentieth century, manufacturers kept the convention and sized their bundles around it. Today the unit is built into estimating software and insurance claim platforms.</p>

<h2 id="h-how-roofing-squares-are-used-in-estimates">How Squares Are Used in Roofing Estimates</h2>
<p>On a typical estimate you will see the roof measured in squares, and then line items priced either per square or per linear foot:</p>
<ul>
  <li><strong>Per square:</strong> tear-off, shingles, underlayment, installation labor.</li>
  <li><strong>Per linear foot:</strong> drip edge, starter strip, ridge cap, valley metal, ridge vent.</li>
  <li><strong>Per unit:</strong> pipe boots, vents, decking sheets.</li>
</ul>
<p>That is why "roofing cost per square" is the most useful comparison number. It rolls materials and labor into one figure you can compare across bids.</p>

<h2 id="h-roof-area-vs-home-square-footage-they-are-not-the-same">Roof Area vs. Home Square Footage: Not the Same Number</h2>
<p>Your home's listed square footage counts heated living space. Your roof covers a different area, for several reasons:</p>
<ul class="checklist">
  <li>It covers the garage, porches and other unheated areas that aren't in the living area.</li>
  <li>It extends past the walls as eaves and rake overhangs.</li>
  <li>It is sloped, so its surface is larger than its footprint.</li>
  <li>A two-story home stacks living space, so its roof covers only about half the home's square footage.</li>
</ul>
<p>A 2,000 sq ft single-story home can easily have a 25–28 square roof, while a 2,000 sq ft two-story home might have 13–15 squares.</p>

<h2 id="h-how-to-calculate-roofing-squares-yourself">How to Calculate Roofing Squares Yourself</h2>
<h3 id="h-step-by-step">Step by Step</h3>
<ol class="steps">
  <li><h3>Measure the footprint</h3><p>Measure the outside of the house at ground level, including the garage and covered porches, and add the overhang width on each side (often 1–2 ft). Multiply length × width for each rectangle and add the results.</p></li>
  <li><h3>Find the pitch</h3><p>Pitch is rise over a 12-inch run, such as 6/12. You can measure it from the attic or a ladder, or use our <a href="/roofing-tools/roof-pitch-calculator/">roof pitch calculator</a>.</p></li>
  <li><h3>Apply the pitch multiplier</h3><p>Multiply the footprint by the factor in the table below to get the true surface area.</p></li>
  <li><h3>Divide by 100</h3><p>That gives you the roof size in squares.</p></li>
  <li><h3>Add waste</h3><p>Multiply by 1.10 for a simple gable roof or by 1.15 or more for hips, valleys and dormers. Round up.</p></li>
</ol>

<h3 id="h-example">Worked Example</h3>
<p>A single-story home in Round Rock measures 60 ft × 32 ft including the garage. With 1.5 ft overhangs on every side, the footprint becomes 63 × 35 = 2,205 sq ft. The roof is a 6/12 hip roof.</p>
<div class="table-wrap"><table>
  <thead><tr><th>Step</th><th>Calculation</th><th>Result</th></tr></thead>
  <tbody>
    <tr><td>Footprint with overhangs</td><td>63 × 35</td><td>2,205 sq ft</td></tr>
    <tr><td>Pitch adjustment (6/12)</td><td>2,205 × 1.118</td><td>2,465 sq ft</td></tr>
    <tr><td>Convert to squares</td><td>2,465 ÷ 100</td><td>24.65 squares</td></tr>
    <tr><td>Add 15% waste (hip roof)</td><td>24.65 × 1.15</td><td>28.3 → <strong>29 squares to order</strong></td></tr>
  </tbody>
</table></div>
<p>The roof measures about 24.7 squares, and the order is 29 squares. When quotes list both numbers, make sure you are comparing the same one.</p>

<h2 id="h-why-roof-pitch-changes-everything">Why Roof Pitch Changes Everything</h2>
<p>A steeper roof has more surface over the same footprint, and steep roofs take longer to work on safely. Pitch raises both the material count and the labor rate.</p>
<h3 id="h-common-pitch-impact">Pitch Multiplier Table</h3>
<div class="table-wrap"><table>
  <thead><tr><th>Pitch</th><th>Multiplier</th><th>Extra area vs. flat</th><th>Common on</th></tr></thead>
  <tbody>
    <tr><td>3/12</td><td>1.031</td><td>+3%</td><td>Porches, additions (low-slope limits apply)</td></tr>
    <tr><td>4/12</td><td>1.054</td><td>+5%</td><td>Many 1970s–80s ranch homes</td></tr>
    <tr><td>5/12</td><td>1.083</td><td>+8%</td><td>Tract homes</td></tr>
    <tr><td>6/12</td><td>1.118</td><td>+12%</td><td>Most common in Austin subdivisions</td></tr>
    <tr><td>7/12</td><td>1.158</td><td>+16%</td><td>Newer builds</td></tr>
    <tr><td>8/12</td><td>1.202</td><td>+20%</td><td>Two-story and custom homes</td></tr>
    <tr><td>9/12</td><td>1.250</td><td>+25%</td><td>Custom homes</td></tr>
    <tr><td>10/12</td><td>1.302</td><td>+30%</td><td>Hill Country, steep gables</td></tr>
    <tr><td>12/12</td><td>1.414</td><td>+41%</td><td>Steep, decorative gables</td></tr>
  </tbody>
</table></div>
<p>The multiplier is the square root of (rise² + 12²) divided by 12. For 8/12, that's √(64 + 144) ÷ 12 = 1.202. Most asphalt shingles need at least a 2/12 slope, with extra underlayment required below 4/12, so very low-slope sections usually get a different roofing system.</p>

<h2 id="h-roofing-squares-and-materials">Roofing Squares and Materials</h2>
<h3 id="h-asphalt-shingles">Asphalt Shingles: How Much Is a Square of Shingles?</h3>
<p>Most standard 3-tab and architectural shingles are packaged <strong>3 bundles per square</strong>. Some heavier designer or luxury shingles take 4 or 5 bundles. Check the wrapper, because it states the coverage per bundle. Ridge cap and starter shingles are sold separately by the linear foot.</p>
<p>So how much is a square of shingles? As a typical planning range, the shingles alone cost roughly $100–$175 per square for 3-tab, $120–$220 for architectural, and $200–$450 or more for premium and impact-resistant lines. Installed, with tear-off, underlayment, accessories and labor, the square of shingles cost is more like $375–$700 for standard products, and higher on steep or complex roofs. Our breakdown of the <a href="/blog/cost-of-asphalt-shingles-per-square/">cost of asphalt shingles per square</a> goes deeper.</p>

<h3 id="h-other-materials">Other Materials</h3>
<ul>
  <li><strong>Synthetic underlayment</strong> comes in rolls that typically cover about 4–10 squares. See <a href="/blog/roofing-underlayment-material-types/">underlayment types</a>.</li>
  <li><strong>Metal panels</strong> are ordered by panel length and coverage width, but jobs are still priced per square.</li>
  <li><strong>Tile</strong> is counted in pieces per square, which varies by profile.</li>
  <li><strong>Self-adhered membrane</strong> rolls usually cover around 1.5–2 squares each.</li>
</ul>

<h2 id="h-waste-factor-the-part-everyone-underestimates">Waste Factor: The Part Everyone Underestimates</h2>
<p>Shingles get cut wherever the roof changes direction, and offcuts from hips and valleys often can't be reused. Typical waste allowances:</p>
<div class="table-wrap"><table>
  <thead><tr><th>Roof type</th><th>Typical waste</th></tr></thead>
  <tbody>
    <tr><td>Simple gable, few penetrations</td><td>10%</td></tr>
    <tr><td>Hip roof or a few valleys</td><td>12–15%</td></tr>
    <tr><td>Cut-up roof with dormers, turrets, many valleys</td><td>15–20%</td></tr>
  </tbody>
</table></div>
<p>Ordering too little means a second delivery, and possibly a slightly different shingle color lot. Ordering a reasonable amount extra is cheaper than stopping a crew mid-job.</p>

<h2 id="h-roofing-squares-and-labor-costs">Roofing Squares and Labor Costs</h2>
<p>Crews are generally paid per square, with add-ons for steep pitch (often starting around 7/12 or 8/12), second stories, extra tear-off layers and difficult access. A 25-square roof at 10/12 can cost noticeably more in labor than a 25-square roof at 5/12, because crews need roof jacks, harnesses and more time on every course.</p>

<h2 id="h-roofing-squares-vs-square-footage-a-clear-comparison">Roofing Squares vs. Square Footage: A Clear Comparison</h2>
<div class="table-wrap"><table>
  <thead><tr><th></th><th>Roofing square</th><th>Home square footage</th></tr></thead>
  <tbody>
    <tr><td>What it measures</td><td>Sloped roof surface</td><td>Heated interior floor area</td></tr>
    <tr><td>Includes garage/porches</td><td>Yes, if under the roof</td><td>No</td></tr>
    <tr><td>Includes overhangs</td><td>Yes</td><td>No</td></tr>
    <tr><td>Affected by pitch</td><td>Yes</td><td>No</td></tr>
    <tr><td>Used for</td><td>Roofing materials, labor, insurance estimates</td><td>Listings, appraisals, HVAC sizing</td></tr>
  </tbody>
</table></div>

<h2 id="h-how-many-squares-are-on-an-average-roof">How Many Squares Are on an Average Roof?</h2>
<p>Most single-family homes in the Austin metro fall between about 15 and 35 squares. A 1,500 sq ft single-story home usually lands around 17–22 squares, and large two-story homes in Cedar Park or Georgetown often run 30–40 once you count garages and complex rooflines. See how that converts to dollars in our guide on <a href="/blog/how-much-does-it-cost-to-replace-a-roof/">what it costs to replace a roof on a 1,500 sq ft house</a>.</p>

<h2 id="h-roofing-squares-in-insurance-claims">Roofing Squares in Insurance Claims</h2>
<p>After a Central Texas hailstorm, the insurance adjuster's estimate will also be written in squares, usually with a waste percentage and separate line items for ridge, drip edge and accessories. If the adjuster measures fewer squares than your roofer, the payout may fall short. Austin Roofing provides photo-documented measurements and can meet your adjuster on the roof so both sides are working from the same numbers. We do not act as a public adjuster. Learn more on our <a href="/services/roof-insurance-claims/">insurance documentation</a> page.</p>

<h2 id="h-diy-vs-professional-square-calculations">DIY vs. Professional Square Calculations</h2>
<p>A footprint-and-pitch estimate is fine for budgeting and usually lands within about 10% of the true number. Professionals use aerial measurement reports or measure on the roof, accounting for every facet, valley and penetration. Before you sign a contract, rely on a professional measurement. For a first look, use the <a href="/roofing-tools/roofing-square-calculator/">roofing square calculator</a>, and stay off steep or hot roofs yourself, because Austin shingles can pass 150°F in summer sun.</p>

<h2 id="h-common-questions-about-roofing-squares">Common Questions About Roofing Squares</h2>
<p>Homeowners most often ask whether quotes should be compared per square (yes, but only when the square counts match), whether the waste factor is padding (a reasonable 10–15% isn't), and whether ridge cap is included in the squares (usually not, since it is priced by the linear foot). Check the FAQ below for quick answers.</p>

<h2 id="h-why-this-one-term-saves-you-money">Why Understanding Squares Saves You Money</h2>
<p>When you know your roof's square count, you can spot an inflated measurement, compare cost per square across bids, and check an insurance estimate against reality. If you would like a professional measurement and a clear written quote, <a href="/contact-us/">contact Austin Roofing</a> for a free inspection anywhere in Austin and Central Texas.</p>
HTML;

render_post([
    'slug' => 'what-is-a-square-in-roofing',
    'body' => $body,
    'faqs' => [
        ['What is a square in roofing?', '<p>A roofing square is 100 square feet of roof surface, a 10 ft × 10 ft area. A roof with 2,500 sq ft of surface is a 25-square roof.</p>'],
        ['How many bundles of shingles are in a square?', '<p>Most standard 3-tab and architectural shingles take 3 bundles per square. Some heavier designer shingles need 4 or 5 bundles, so check the coverage printed on the wrapper.</p>'],
        ['How much is a square of shingles?', '<p>As a typical planning range, shingles alone run roughly $100–$220 per square for standard 3-tab and architectural products, and more for premium lines. Installed with tear-off, underlayment and labor, expect roughly $375–$700 per square for standard shingles.</p>'],
        ['How do I calculate roofing squares from my home’s square footage?', '<p>Use the roof footprint (including garage, porches and overhangs), not the living area. Multiply by the pitch factor (for example 1.118 for 6/12), divide by 100, then add 10–15% for waste.</p>'],
        ['How many squares is a 2,000 sq ft house?', '<p>A single-story 2,000 sq ft home often needs about 24–28 squares including the garage, overhangs and waste. A two-story home of the same size may need only 13–16.</p>'],
        ['What waste factor should a roofing estimate include?', '<p>About 10% for a simple gable roof, 12–15% for hip roofs, and up to 20% for roofs with many valleys and dormers.</p>'],
    ],
    'related' => service_links(['roof-replacement', 'shingle-roofing', 'roof-inspection', 'roof-insurance-claims']),
]);
