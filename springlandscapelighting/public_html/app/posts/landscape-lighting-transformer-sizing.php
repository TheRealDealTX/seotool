<?php defined('SLT') || exit; ?>
<p class="lead">The transformer is the heart of a low-voltage landscape lighting system. Every fixture depends on it, and most of the problems we see on older systems, from dim lights at the end of a run to fixtures that burn out early, trace back to a transformer that was undersized, overloaded or wired without accounting for voltage drop. Here is how to size one properly.</p>

<h2>What the transformer does</h2>
<p>A landscape transformer takes 120-volt household power and steps it down to roughly 12 volts, which is safer to run through shallow-buried cable in planting beds and lawns. A good unit also houses the controls: a timer, a photocell input, sometimes a smart module, and the circuit breakers that protect each output.</p>
<p>Transformers are rated by capacity, usually in watts or volt-amps (VA): 150, 300, 600, 900 and 1200 are common sizes. That rating is the maximum continuous load it can carry, not a target to hit.</p>

<h2>The 80% rule</h2>
<p>Standard practice is to load a transformer to no more than about 80% of its rated capacity. That headroom keeps it running cooler, which matters in a Texas summer when the enclosure is already sitting in 95-degree air, and it leaves room for a few fixtures later.</p>
<p>To find the minimum size, divide your total fixture load by 0.8.</p>
<div class="table-wrap"><table>
<thead><tr><th>System</th><th>Total load</th><th>Load ÷ 0.8</th><th>Sensible choice</th></tr></thead>
<tbody>
<tr><td>24 path and accent lights at 5 W</td><td>120 W</td><td>150 W</td><td>150 W, or 300 W if you plan to expand</td></tr>
<tr><td>Front elevation: 12 uplights at 7 W, 10 path lights at 4 W</td><td>124 W</td><td>155 W</td><td>300 W</td></tr>
<tr><td>Whole property: 40 mixed fixtures, 230 W total</td><td>230 W</td><td>288 W</td><td>300 W tight; 600 W or two units is more comfortable</td></tr>
</tbody>
</table></div>
<div class="callout"><strong>Tip:</strong> Some LED fixtures list a VA rating that is higher than their wattage because their drivers are not purely resistive loads. When the manufacturer gives a VA figure, add up VA rather than watts.</div>
<p>You can run these numbers in the calculator below, including wire gauge and run length.</p>
<?php tool_embed('transformer-sizing-calculator'); ?>

<h2>Multi-tap transformers</h2>
<p>Professional transformers usually offer several output taps, commonly 12, 13, 14 and 15 volts, and sometimes higher. Each tap gives you a slightly higher starting voltage. You connect a long or heavily loaded cable run to a higher tap so that, after the voltage drops along the wire, the fixtures still receive what they need.</p>
<p>A short run near the transformer might sit on the 12 V tap, while a 120-foot run out to the back fence might need 14 or 15 V. Single-tap 12 V transformers from big-box kits cannot make that adjustment, which is one reason those systems look uneven.</p>

<h2>Voltage drop and wire gauge</h2>
<p>Low-voltage systems carry relatively high current, and copper wire has resistance, so voltage falls as it travels. The longer the run, the heavier the load and the thinner the wire, the bigger the drop.</p>
<p>The calculation is:</p>
<p><strong>Voltage drop = current × loop resistance</strong>, where current = watts ÷ volts, and loop resistance = 2 × run length in feet × (ohms per 1,000 ft ÷ 1,000). The factor of 2 accounts for the current going out and back on the two conductors.</p>
<div class="table-wrap"><table>
<thead><tr><th>Cable</th><th>Approx. ohms per 1,000 ft (per conductor)</th><th>Typical use</th></tr></thead>
<tbody>
<tr><td>16/2</td><td>4.02</td><td>Short leads, very light loads</td></tr>
<tr><td>14/2</td><td>2.52</td><td>Short runs with a few fixtures</td></tr>
<tr><td>12/2</td><td>1.59</td><td>The common main-run cable</td></tr>
<tr><td>10/2</td><td>1.00</td><td>Long or heavily loaded runs</td></tr>
</tbody>
</table></div>
<h3>Worked example</h3>
<p>Say you have 100 W of fixtures grouped at the end of a 100-foot run of 12/2:</p>
<ul>
<li>Current: 100 W ÷ 12 V ≈ 8.33 A</li>
<li>Loop resistance: 2 × 100 × 1.59 ÷ 1,000 = 0.318 Ω</li>
<li>Voltage drop: 8.33 × 0.318 ≈ 2.65 V</li>
</ul>
<p>On the 12 V tap the fixtures would see about 9.35 V, too low for many fixtures. On the 14 V tap they would see about 11.35 V, which is right in range. Switch to 10/2 cable and the drop falls to about 1.67 V, so the 13 V tap would do. These numbers assume all the load sits at the end; when fixtures are spread along the run the actual drop is lower, but the last fixture still sees the most.</p>

<h2>Target voltage at the fixture</h2>
<p>The traditional target for 12 V landscape lighting is about 10.5 to 12 volts at each fixture. Below that, halogen lamps go yellow and dim. Above 12 V, they run hot and fail early.</p>
<p>Many LED fixtures accept a wider input range, often something like 9 to 15 volts, and some are more forgiving than others. Always check the spec sheet. Overvolting an LED driver can shorten its life just as surely as overvolting a halogen lamp. A professional installer measures actual voltage at the fixtures with a meter after everything is connected, rather than trusting the math alone.</p>

<h2>Hub, daisy chain and T-method wiring</h2>
<p>How you lay out the cable matters as much as which gauge you choose.</p>
<div class="grid-cards">
<div class="mini-card"><h3>Daisy chain</h3><p>One cable runs past each fixture in turn. Simple and cheap, but the first fixture gets the most voltage and the last gets the least. Fine for short runs with light loads.</p></div>
<div class="mini-card"><h3>T-method</h3><p>A home-run cable carries power to the middle of a group, then splits both ways. Fixtures on either side see similar voltage. Good for long beds and path runs.</p></div>
<div class="mini-card"><h3>Hub</h3><p>A home run feeds a central junction, and each fixture connects with its own lead of equal length. Every fixture gets nearly the same voltage. It is the most even and the most work.</p></div>
</div>
<p>In practice, a good design mixes these. Hubs suit clusters like a group of uplights on a <a href="/services/architectural-lighting/">brick or stone elevation</a>, while a T works well along a long front walk lit with <a href="/services/pathway-driveway-lighting/">path lights</a>.</p>

<?php cta_box('Dim lights at the end of the run?', 'Uneven brightness is usually a transformer or wiring problem, not a bulb problem. Spring Landscape Lighting can measure your system and correct taps, cable and layout.'); ?>

<h2>Installation details that matter</h2>
<ul>
<li><strong>Enclosure.</strong> A stainless steel or similarly corrosion-resistant enclosure holds up far better in Gulf Coast humidity than painted steel.</li>
<li><strong>GFCI outlet with an in-use cover.</strong> The transformer should plug into a GFCI-protected outdoor receptacle with a bubble-style cover that stays weatherproof while the plug is in it. Receptacle work is a job for a licensed electrician.</li>
<li><strong>Mounting height and location.</strong> Mount it off the ground, away from sprinkler spray and above areas that pond during heavy rain. Keep it accessible for adjustments.</li>
<li><strong>Photocell and timer.</strong> Place the photocell where it sees open sky, not under an eave or next to a porch light that will fool it. A photocell-on, timer-off setup, or an astronomical timer, avoids all-night running. Our guide to <a href="/services/smart-lighting-controls/">smart lighting controls</a> covers app-based options.</li>
</ul>
<div class="callout callout--warn"><strong>Note:</strong> Fire ants like the warmth inside transformer housings in this part of Texas. Keep gaps sealed and check inside the cover a few times a year.</div>

<h2>When to split into two transformers</h2>
<p>One large transformer is not always better than two smaller ones. Consider splitting when:</p>
<ul>
<li>The front and back yards are far apart and cable runs to one location would be very long</li>
<li>You want completely independent schedules or controls for different areas</li>
<li>The total load pushes past what one unit can carry at 80%</li>
<li>A pool or outdoor living area is being added on the far side of the house</li>
</ul>
<p>Two transformers placed closer to their loads mean shorter runs, less voltage drop and lighter cable. They also mean one failure does not take the whole property dark.</p>
<p>When Spring Landscape Lighting designs a system, transformer location and capacity are planned alongside the fixture layout, not added at the end. If you want a rough fixture count first, try the <a href="/tools/fixture-estimator/">fixture estimator</a>, then see how that load translates to energy with the <a href="/tools/energy-cost-calculator/">energy cost calculator</a>.</p>

<?php faq_block([
    ['What size transformer do I need for landscape lighting?', 'Add up the wattage (or VA, if listed) of every fixture, then divide by 0.8. A 120-watt load needs at least a 150-watt transformer. Many homeowners choose the next size up to allow for future fixtures.'],
    ['Why should a transformer only be loaded to 80 percent?', 'Running below full capacity keeps the transformer cooler and extends its life, which matters in hot Texas summers. It also leaves room to add fixtures later without replacing the unit.'],
    ['What voltage should my landscape lights receive?', 'The traditional target is about 10.5 to 12 volts at each fixture. Many LED fixtures accept a wider range, so check the manufacturer\'s spec sheet and measure with a meter after installation.'],
    ['What wire gauge should I use for landscape lighting?', '12/2 cable is the common choice for main runs. Use 10/2 for long or heavily loaded runs, and keep 14/2 or 16/2 for short leads and light loads. The right gauge depends on load and distance.'],
    ['What are the taps on a landscape transformer for?', 'Multi-tap transformers offer outputs such as 12, 13, 14 and 15 volts. Longer or heavier runs connect to higher taps so that, after voltage drop, fixtures still receive the right voltage.'],
    ['Can I use an oversized transformer?', 'Yes. A larger transformer with a light load is fine and leaves room to grow. The main tradeoffs are cost and, on some older units, slightly higher idle losses.'],
]); ?>
