INFO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/>'
            '<path d="M12 8h.01"/></svg>')

body = f"""
<p>A flat roof is not really flat. A well-built low-slope roof drains at a quarter inch per foot or more, sheds water
through drains, scuppers or gutters, and is held together by a membrane that is only as good as its edges and
penetrations. Most failures start at the details, not in the open field of the roof.</p>
<p>This guide walks through a low-slope installation in the order it happens on site, and at each step points out what
it does to the estimate. Whether you are pricing a job, comparing bids or reviewing a scope, these are the decisions that
move the number.</p>

<h2 id="assessment-and-deck">Step 1: Assess the existing roof and the deck</h2>
<p>Every installation starts with knowing what is already there. Before a price goes out, someone should confirm:</p>
<ul>
  <li><strong>How many layers exist.</strong> Core cuts at several spots show the full build-up down to the deck.</li>
  <li><strong>Whether the insulation is dry.</strong> Wet board cannot stay. An infrared scan on larger roofs maps the
  wet areas so they can be measured.</li>
  <li><strong>Deck type and condition.</strong> Steel decks rust at drains and along old leak lines; wood decks rot; light
  concrete and gypsum decks limit which fasteners can be used.</li>
  <li><strong>Drainage.</strong> Ponding that lasts more than about 48 hours after rain points to deck deflection, clogged
  drains or not enough slope, and the new system should correct it.</li>
</ul>
<p>Deck repairs are hard to quantify before tear-off. Price them as a stated allowance, such as a set number of square
feet of steel deck or sheets of plywood at a unit price, so the owner knows what is included and what is extra.</p>

<h2 id="tear-off-or-recover">Step 2: Decide on tear-off or recover</h2>
<p>A recover installs a new system over the existing roof, usually with a cover board or new insulation between them.
It saves tear-off and disposal and keeps the building dry during the work. It is only allowed when the conditions are
right.</p>
<h3>When a recover is not allowed</h3>
<p>The International Building Code, which most Texas cities adopt with local amendments, does not allow a recover when
the existing roof or insulation is water-soaked or deteriorated, or when the roof already has two or more applications
of roof covering. Manufacturers add their own requirements before they will warranty a recover. Always check the code
edition your city has adopted and the manufacturer's recover guidelines.</p>
<h3>What it does to the price</h3>
<p>Tear-off runs about $1.50 to $3.00 per square foot per layer, before disposal surprises like heavy gravel BUR. A
recover avoids that, but usually adds a cover board and still requires removing any wet areas. On a roof with one dry
layer, recovering often saves money. On a roof with two layers, there is no choice: it is a full tear-off.</p>

<figure><img src="/assets/img/blog/Flat-Roof-Installation-2-1200.webp" alt="Crew removing an old flat roof down to the deck before installing a new membrane" width="1000" height="666" loading="lazy"><figcaption>A full tear-off exposes the deck so damaged areas can be repaired before new insulation goes down.</figcaption></figure>

<h2 id="insulation-and-taper">Step 3: Insulation and tapered systems</h2>
<p>Insulation does two jobs on a low-slope roof: it provides the thermal value the energy code asks for, and in a
tapered system it creates the slope that moves water to the drains.</p>
<h3>Flat insulation</h3>
<p>Polyiso is the most common board in Texas, at roughly R-5.7 per inch. It is usually installed in two layers with
staggered joints so heat cannot bypass the seams. Installed cost is about $0.90 to $1.30 per square foot per inch of
thickness.</p>
<h3>Energy code</h3>
<p>When a roof is replaced and the insulation sits entirely above the deck, the energy code adopted by many Texas
jurisdictions can require the new roof to meet current insulation levels, which in recent IECC editions is often in the
R-25 to R-30 continuous range for Texas climate zones (2 through 4). A building that had one inch of old board may need three to
five inches of new polyiso. That can be the single largest line item after the membrane, and it also raises the roof
edge, so edge metal, curbs and door thresholds may need to be built up. Confirm the requirement with the local building
department.</p>
<h3>Tapered insulation</h3>
<p>Tapered polyiso is manufactured in sloped panels, laid out by a designer to move water toward drains, with crickets
between drains and behind curbs. It is priced by average thickness, so a tapered system that averages 3.5 inches costs
roughly what 3.5 inches of flat board would, plus design and the crickets. It costs more than flat board, but it fixes
ponding instead of covering it.</p>

<h2 id="attachment-methods">Step 4: Attachment method</h2>
<p>How the insulation and membrane are held down affects cost, wind rating and noise on occupied buildings.</p>
<div class="table-wrap"><table>
  <thead><tr><th>Method</th><th>How it works</th><th>Strengths</th><th>Trade-offs</th></tr></thead>
  <tbody>
    <tr><td>Mechanically attached (MA)</td><td>Membrane fastened with screws and plates in the seam laps, insulation fastened separately</td><td>Lowest installed cost for TPO and PVC; fast on steel decks</td><td>Membrane can flutter in high wind; needs a deck with good pull-out values</td></tr>
    <tr><td>Fully adhered (FA)</td><td>Membrane glued to a cover board or insulation with bonding adhesive</td><td>Smooth finish, better wind performance, quieter</td><td>More labor and adhesive; adhesives are temperature sensitive</td></tr>
    <tr><td>Induction welded</td><td>Plates fastened under the membrane, then heat-bonded to its underside with an induction tool</td><td>No seam fastening; good uplift resistance; fewer penetrations through the sheet</td><td>Specialized equipment; not every installer offers it</td></tr>
    <tr><td>Ballasted</td><td>Loose membrane held down with stone or pavers</td><td>Low material cost on large roofs</td><td>Heavy; requires structural capacity; harder to find leaks</td></tr>
  </tbody>
</table></div>
<p>Wind design matters in Texas, especially along the Gulf Coast. Corners and perimeters see higher uplift than the
field, so the fastening pattern tightens there. Ask which wind uplift rating the system is designed to and confirm the
fastening pattern in the bid, not just "per manufacturer."</p>

<h2 id="membrane-and-flashing">Step 5: Membrane, flashing and drains</h2>
<p>With insulation down, the membrane is rolled out, seamed and flashed. On TPO and PVC, seams are hot-air welded and
should be probed by the installer. EPDM seams use tape; mod-bit and BUR use heat, hot asphalt or cold adhesive.</p>
<h3>The details that leak</h3>
<ul>
  <li><strong>Perimeter edge.</strong> Edge metal, gravel stop or coping holds the membrane at the edge, where wind uplift
  starts. Edge metal is priced per linear foot and is easy to leave off a quick estimate.</li>
  <li><strong>Walls and parapets.</strong> Membrane runs up the wall, is terminated with a bar and counterflashed or
  covered by coping. Every linear foot of wall is extra flashing labor.</li>
  <li><strong>Curbs and penetrations.</strong> HVAC units, vents, pipes and conduits each need a curb wrap, pipe boot or
  pitch pocket. Count them; they add up fast on retail and restaurant roofs.</li>
  <li><strong>Drains and scuppers.</strong> Old drain bowls are often replaced or fitted with new inserts, clamping rings
  and strainers. Overflow scuppers may be required by code.</li>
</ul>
<p>When perimeter water leaves through gutters, size them for Texas downpours. The
<a href="/tools/gutter-calculator/">gutter and downspout calculator</a> checks gutter size and downspout count for the
roof area and rainfall.</p>

<figure><img src="/assets/img/blog/Flat-Roof-Installation-3-1200.webp" alt="Installer welding a single-ply membrane seam near a rooftop detail" width="1000" height="666" loading="lazy"><figcaption>Seams and flashings are where most low-slope leaks begin, so they deserve most of the inspection time.</figcaption></figure>

<div class="callout">{INFO_SVG}
<p><strong>Count details before you price the field.</strong> Walk the roof with a notepad and count every curb, pipe,
drain, scupper and linear foot of wall and edge. On small commercial roofs the details can cost as much as the
membrane, and they are the items most often missing from a low bid.</p></div>

<h2 id="installed-costs">What a flat roof installation costs in Texas</h2>
<p>These are installed price ranges for 2026 with a DFW baseline, including labor and contractor overhead and profit.
They exclude tear-off and insulation, which are listed separately so you can build the full number.</p>
<div class="table-wrap"><table>
  <thead><tr><th>System or item</th><th>Installed price</th><th>Typical service life</th></tr></thead>
  <tbody>
    <tr><td>TPO 60-mil, mechanically attached</td><td>$7.00 to $10.00 per sf</td><td>20 to 25 years</td></tr>
    <tr><td>TPO 60-mil, fully adhered</td><td>$8.00 to $11.50 per sf</td><td>20 to 25 years</td></tr>
    <tr><td>PVC 60-mil</td><td>$9.00 to $13.00 per sf</td><td>25 to 30 years</td></tr>
    <tr><td>EPDM 60-mil, fully adhered</td><td>$7.00 to $10.50 per sf</td><td>25 to 30 years</td></tr>
    <tr><td>Modified bitumen, 2-ply</td><td>$7.50 to $11.00 per sf</td><td>15 to 20 years</td></tr>
    <tr><td>Built-up roof (BUR)</td><td>$7.50 to $11.50 per sf</td><td>20 to 30 years</td></tr>
    <tr><td>Tear-off, per layer</td><td>$1.50 to $3.00 per sf</td><td>n/a</td></tr>
    <tr><td>Polyiso insulation, per inch</td><td>$0.90 to $1.30 per sf</td><td>Life of the roof if kept dry</td></tr>
  </tbody>
</table></div>
<p>Put together, a single-layer tear-off with 2 inches of new polyiso and mechanically attached TPO comes to roughly
$10.30 to $15.60 per square foot before edge metal, drains, curbs and deck repair. Houston, Austin and San Antonio prices
run close to DFW; remote West Texas jobs carry extra travel and mobilization. The
<a href="/tools/flat-roof-calculator/">flat and commercial roof calculator</a> uses these same ranges, and the
<a href="/tools/roofing-bid-calculator/">roofing bid calculator</a> checks whether your markup and margin hold up once
labor and materials are in.</p>

<h2 id="inspections-and-warranties">Step 6: Inspections, closeout and warranties</h2>
<p>Most cities require a permit for a commercial re-roof and some inspect at completion. Separate from the city,
manufacturers inspect before issuing a system warranty.</p>
<ul>
  <li><strong>Contractor warranty</strong> covers workmanship, often for two years or so; terms vary by contractor.</li>
  <li><strong>Material warranty</strong> covers the membrane itself, usually not labor.</li>
  <li><strong>No-dollar-limit (NDL) system warranty</strong> covers materials and labor for leaks caused by the system
  for a set term, such as 15, 20 or 30 years. It requires an approved installer, a manufacturer inspection and
  specified components, and costs more. Longer terms usually require thicker membrane, more fasteners or more insulation.</li>
</ul>
<p>At closeout, ask for the warranty documents, a roof plan showing drains and penetrations, product data sheets and the
fastening pattern used. Those make future claims and repairs much easier to price.</p>

<h2 id="before-you-sign">Checklist before you sign or send a flat roof bid</h2>
<ol>
  <li>Core cuts confirm the layer count, insulation and deck, and wet areas are measured.</li>
  <li>The scope says tear-off or recover, and why the choice meets code.</li>
  <li>Insulation thickness and R-value are written down, with tapered layout if ponding exists.</li>
  <li>Attachment method and wind rating are named.</li>
  <li>Edge metal, wall flashing, curbs, pipes, drains and scuppers are counted as separate quantities.</li>
  <li>Deck repair is a stated allowance with a unit price.</li>
  <li>The warranty type and term are spelled out.</li>
</ol>
<p>If any item is missing, the bid is not comparable to the next one. For a full line-item number on a commercial
building, our <a href="/services/commercial-roof-estimates/">commercial roof estimates</a> are built from your
measurements and photos, or you can <a href="/get-estimate/">request an estimate</a> directly.</p>
"""

POST = {
    "slug": "flat-roof-installation-a-complete-guide",
    "title": "Flat Roof Installation Guide: Steps & Costs | Roof Estimate Pro",
    "h1": "Flat Roof Installation: A Complete Guide for Estimating",
    "description": "How a flat roof is installed, step by step: deck prep, tear-off vs recover, insulation, attachment, flashing, warranties and 2026 Texas installed costs.",
    "published": "2026-01-12T22:04:58-05:00",
    "modified": "2026-10-20",
    "category": "Commercial Roofing",
    "image": "Flat-Roof-Installation-1",
    "image_alt": "New single-ply membrane being installed on a commercial flat roof",
    "excerpt": "A step-by-step look at flat roof installation, from deck and tear-off decisions to insulation, attachment, flashing and warranties, with Texas costs.",
    "lede": "Every step of a low-slope installation, in the order it happens on site, and what each decision does to the price.",
    "body": body,
    "faqs": [
        ("How much does a new flat roof cost in Texas?",
         "<p>For 2026, installed membranes run about $7.00 to $13.00 per square foot depending on the system, before "
         "tear-off ($1.50 to $3.00 per sf per layer) and insulation (about $0.90 to $1.30 per sf per inch of polyiso). "
         "A typical tear-off with new insulation and TPO lands around $10 to $16 per sf before details and deck repair.</p>"),
        ("Can a new flat roof go over the old one?",
         "<p>Sometimes. A recover is generally allowed only when the existing roof is dry and sound and there is only one "
         "existing layer. If there are two or more layers or the insulation is wet, building codes require a tear-off. "
         "Check your local code and the manufacturer's recover rules.</p>"),
        ("How much slope does a flat roof need?",
         "<p>Codes and manufacturers generally call for at least 1/4 inch per foot for most low-slope membranes, so "
         "water drains instead of ponding. Tapered insulation is the usual way to add slope on a flat deck.</p>"),
        ("Is mechanically attached or fully adhered TPO better?",
         "<p>Mechanically attached costs less and installs faster. Fully adhered resists wind flutter better and is quieter, "
         "and costs about $1 to $1.50 more per square foot. The right choice depends on wind exposure, deck type and budget.</p>"),
        ("What is an NDL roof warranty?",
         "<p>A no-dollar-limit warranty from the manufacturer covers both materials and labor for leaks caused by the roof "
         "system for a set term. It requires an approved installer, specified components and a manufacturer inspection.</p>"),
    ],
    "related_tools": ["flat-roof-calculator", "roofing-bid-calculator", "gutter-calculator"],
}
