<?php defined('LLT') or die(http_response_code(404)); ?>
<p class="lead-p">Nearly every residential outdoor lighting system in Texas is low-voltage landscape lighting: a transformer steps household 120-volt power down to about 12 volts, and buried cable carries that safer, lower voltage to each fixture. It is simple in concept, but the details (transformer size, wire gauge, voltage drop and how the wire is laid out) decide whether every light glows evenly for years or the far end of the yard looks dim and fixtures fail early. This guide explains how a 12V system works, from the outlet to the last path light.</p>

<p>Whether you are planning a new system, troubleshooting an old one or weighing a DIY kit against a professional install, understanding these basics will help you ask the right questions, whether you hire Landscape Lighting Texas or another installer.</p>

<h2>How a 12-Volt Landscape Lighting System Works</h2>

<p>A low-voltage system has four main parts:</p>

<ol>
<li><strong>Power source:</strong> a dedicated outdoor GFCI outlet, or a hardwired connection made by an electrician.</li>
<li><strong>Transformer:</strong> converts 120V AC to roughly 12–15V AC, and usually houses the timer, photocell or smart controller.</li>
<li><strong>Low-voltage cable:</strong> direct-burial, two-conductor stranded copper cable that runs from the transformer to the fixtures.</li>
<li><strong>Fixtures:</strong> uplights, path lights, well lights, downlights and hardscape lights, each connected to the cable with a waterproof connection.</li>
</ol>

<p>Because the cable carries only about 12 volts, the shock risk is far lower than line voltage, the cable can be buried shallowly, and fixtures can be moved as plants grow. That flexibility is the reason low voltage became the standard for residential landscape lighting.</p>

<?= figure('garden-pathway-lighting', 'Low-voltage path lights along a garden walk at a Texas home', 'Path lights on a 12V system: low shock risk, shallow cable, and fixtures that can move as the garden grows.') ?>

<h2>Transformers: The Heart of the System</h2>

<h3>What the transformer does</h3>
<p>A landscape lighting transformer takes 120V from the house and delivers low voltage to one or more output circuits. Professional units are typically magnetic (a toroidal or laminated core) in a stainless steel or powder-coated case, with built-in breakers or fuses on each circuit. Larger transformers divide their capacity into several circuits, commonly around 300 watts each, so one wire problem does not take down the whole yard.</p>

<h3>Multi-tap transformers</h3>
<p>A multi-tap transformer offers several output terminals, typically 12, 13, 14 and 15 volts (some go higher). Longer or heavier-loaded cable runs lose voltage along the way, so you connect them to a higher tap to compensate. The goal is for every fixture to receive the voltage it was designed for, usually around 11–12 volts for halogen, or within the stated range for LED (many LED fixtures accept roughly 9–15V, but always check the specification).</p>

<h3>Sizing at 80% load</h3>
<p>Add up the wattage of every fixture (use the lamp or fixture rating, not the halogen equivalent). Then choose a transformer so that total is no more than about 80% of its rating. That headroom keeps the transformer cooler, which matters in a Texas garage or on a sunny wall in July, and leaves capacity to add fixtures later.</p>

<div class="table-wrap"><table>
<thead><tr><th>Total fixture load</th><th>Minimum transformer at 80%</th><th>Common size to choose</th></tr></thead>
<tbody>
<tr><td>100W (about 20 LED path lights at 5W)</td><td>125W</td><td>150W–200W</td></tr>
<tr><td>240W</td><td>300W</td><td>300W</td></tr>
<tr><td>400W</td><td>500W</td><td>600W</td></tr>
<tr><td>700W</td><td>875W</td><td>900W–1,200W</td></tr>
</tbody>
</table></div>

<?= tool_promo('/tools/transformer-calculator/') ?>

<h2>Wire Gauge: 16, 14, 12 and 10 AWG</h2>

<p>Low-voltage cable is sold by American Wire Gauge (AWG); the smaller the number, the thicker the copper and the lower its resistance. Because 12V systems run relatively high current for their wattage (100W at 12V is over 8 amps), wire size matters much more than it does on household circuits.</p>

<div class="table-wrap"><table>
<thead><tr><th>Gauge</th><th>Approx. resistance per 1,000 ft (per conductor)</th><th>Typical use</th></tr></thead>
<tbody>
<tr><td>16 AWG</td><td>About 4.0 Ω</td><td>Short leads and very small, close-in loads; common in DIY kits</td></tr>
<tr><td>14 AWG</td><td>About 2.5 Ω</td><td>Short runs with light LED loads</td></tr>
<tr><td>12 AWG</td><td>About 1.6 Ω</td><td>The professional workhorse for most residential runs</td></tr>
<tr><td>10 AWG</td><td>About 1.0 Ω</td><td>Long runs, heavier loads and feeds to a hub</td></tr>
</tbody>
</table></div>

<p>LED fixtures draw far less current than halogen, so modern systems can do more with 12 AWG than older ones could. Our <a href="/led-vs-halogen-landscape-lighting/">LED vs halogen comparison</a> shows how much the switch reduces load.</p>

<h2>Voltage Drop: The Formula and a Worked Example</h2>

<p>Every foot of wire has resistance, and current flowing through it loses voltage as heat. Too much drop and the far fixtures look dim (halogen also turns yellow) or LED drivers misbehave. Here is the calculation using Ohm's law:</p>

<ul>
<li><strong>Current (amps)</strong> = total watts on the run ÷ 12</li>
<li><strong>Loop resistance (Ω)</strong> = run length in feet × 2 × (resistance per 1,000 ft ÷ 1,000). The × 2 accounts for the trip out and back on both conductors.</li>
<li><strong>Voltage drop</strong> = amps × loop resistance</li>
</ul>

<h3>Worked example</h3>
<p>A group of ten 6W LED uplights (60W total) sits at the back of a lot, 150 feet from the transformer.</p>

<div class="table-wrap"><table>
<thead><tr><th>Step</th><th>12 AWG cable</th><th>10 AWG cable</th></tr></thead>
<tbody>
<tr><td>Current</td><td>60 ÷ 12 = 5 A</td><td>60 ÷ 12 = 5 A</td></tr>
<tr><td>Loop resistance</td><td>150 × 2 × 0.0016 = 0.48 Ω</td><td>150 × 2 × 0.0010 = 0.30 Ω</td></tr>
<tr><td>Voltage drop</td><td>5 × 0.48 = 2.4 V</td><td>5 × 0.30 = 1.5 V</td></tr>
<tr><td>Voltage at fixtures on the 12V tap</td><td>9.6 V (too low for many fixtures)</td><td>10.5 V</td></tr>
<tr><td>Tap to use</td><td>14V tap → about 11.6 V</td><td>13V tap → about 11.5 V</td></tr>
</tbody>
</table></div>

<p>This treats the whole load as if it sits at the end of the run, which is conservative and is exactly how a hub layout behaves. Once the system is running, a professional confirms the result by measuring voltage at the fixtures with a meter rather than trusting the math alone.</p>

<?= callout('<p>Do not just crank every run to the highest tap. Fixtures near the transformer on an over-boosted run get too much voltage, and both halogen and LED lamps fail early when overdriven. Balance the layout so all fixtures on a run see similar voltage.</p>', 'warn') ?>

<h2>Wiring Methods: Daisy Chain, T, Loop and Hub</h2>

<h3>Daisy chain (straight run)</h3>
<p>One cable runs past fixture after fixture. It is the simplest and most common DIY method, but the first fixture gets the highest voltage and the last gets the lowest. It works for short runs with light LED loads.</p>

<h3>T method</h3>
<p>A home-run cable carries power out to the middle of a group, then splits in two directions. Because the fixtures are spread evenly on either side of the split, they receive more even voltage than on a long daisy chain.</p>

<h3>Loop method</h3>
<p>The cable runs past the fixtures and returns to the transformer, connected at both ends. Feeding from both ends evens out voltage. It takes more wire and careful polarity, so it is less common today.</p>

<h3>Hub method</h3>
<p>A heavier home-run cable goes to a central hub (a buried junction point), and each fixture is fed from the hub with its own lead of equal or similar length. Every fixture sees nearly identical voltage, connections are concentrated in one serviceable spot, and adding a fixture later is easy. Hub wiring is the approach most professional installers prefer for groups of fixtures, such as several uplights around one large tree.</p>

<?= figure('architectural-uplighting', 'Evenly lit stone facade with matched uplights on a Texas home', 'Even brightness across a facade comes from balanced wiring, not just matching fixtures.') ?>

<h2>Burial, Conduit and Connections</h2>

<h3>Burial depth</h3>
<p>Low-voltage landscape cable is rated for direct burial. The National Electrical Code generally allows landscape lighting circuits of 30 volts or less to be buried about 6 inches deep, and that is the common practice. In beds, cable is often tucked under mulch and soil; in lawns, it is laid in a narrow trench cut by hand or with a cable-laying tool. In caliche or heavy clay, a proper trench is worth the effort, because shallow cable gets cut by aerators, edgers and new plantings.</p>

<h3>Under hardscape</h3>
<p>Never bury cable directly under a driveway, walkway or patio. Run it through a PVC sleeve or conduit so it is protected and replaceable. The best time to place sleeves is before concrete or pavers go in; if you are building a patio or pool deck, ask your contractor to lay empty sleeves where future lighting may cross. Existing slabs can often be crossed by boring underneath.</p>

<h3>Waterproof connectors</h3>
<p>Connections are where most low-voltage systems fail. Twist connectors or pierce-type clips left bare in the soil let water wick into the copper, which turns green and adds resistance until the light dims or quits. Professional installs use gel- or grease-filled waterproof connectors, or crimped and heat-shrink-sealed splices, so moisture cannot reach the conductors. In humid Houston and the salty air of the Gulf Coast, this detail makes the biggest difference in how long a system lasts.</p>

<h2>Controls: Photocells, Timers and Smart Controllers</h2>

<ul>
<li><strong>Photocell:</strong> turns lights on at dusk and off at dawn, or pairs with a timer for "on at dusk, off after six hours." Keep it out of the glow of its own fixtures and away from porch lights.</li>
<li><strong>Mechanical or digital timer:</strong> simple, but it needs resetting with the seasons and after daylight saving time changes or power outages.</li>
<li><strong>Astronomical timer:</strong> calculates sunset and sunrise for your location every day, so the schedule tracks the seasons automatically.</li>
<li><strong>Smart controller:</strong> app control, multiple zones, dimming and scenes. See our <a href="/services/smart-lighting-systems/">smart lighting systems</a> service.</li>
</ul>

<?= tool_promo('/tools/dusk-timer/') ?>

<h2>Power, Permits and the GFCI Outlet</h2>

<p>Most plug-in transformers connect to a 120V outdoor receptacle that must be GFCI protected and fitted with a weather-resistant, in-use ("bubble") cover so the plug stays protected while in use. Large transformers are often hardwired to a dedicated circuit instead.</p>

<p>The low-voltage side of the system is generally straightforward. The line-voltage side is not. Adding a new outdoor receptacle, running a new circuit or hardwiring a transformer is 120V electrical work, which in Texas is generally performed by a licensed electrician, and many cities require a permit for it. Rules vary by city, so check with your local building department and your HOA before work begins.</p>

<?= callout('<p>Before anyone digs, call 811 (Texas811) a few days ahead to have public utility lines marked. Private lines such as irrigation, gas to a grill or pool, and wiring to outbuildings are not marked by 811, so locate those separately.</p>', 'note') ?>

<h2>Professional Install vs a DIY Kit</h2>

<p>Box-store kits come with a small transformer, thin cable and plastic or light aluminum fixtures. They can work for a short run of path lights near an outlet. They tend to fall short on a full property for predictable reasons:</p>

<ul>
<li><strong>Transformer:</strong> single-tap and undersized, so long runs cannot be compensated.</li>
<li><strong>Cable:</strong> often 16 AWG, which limits run length and load.</li>
<li><strong>Connectors:</strong> pierce-type clips that corrode in wet soil.</li>
<li><strong>Fixtures:</strong> plastic or thin finishes that fade and crack in Texas sun and hail.</li>
<li><strong>Design:</strong> lights placed in rows rather than aimed to shape trees, walls and paths at night.</li>
</ul>

<p>A professional-grade system uses solid brass, copper or heavy aluminum fixtures, a multi-tap transformer sized with headroom, 12 or 10 AWG cable laid out with voltage drop in mind, sealed connections and an on-site aiming session after dark. For typical pricing, professional installation commonly runs about $250–$450 per installed fixture as a planning range; our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> builds a fuller estimate, and the <a href="/landscape-lighting-complete-guide/">complete landscape lighting guide</a> covers design techniques.</p>

<?= figure('oak-tree-uplighting', 'Live oak tree uplit by a professionally wired low-voltage system', 'Large trees often need several uplights on a single hub so each one gets the same voltage.') ?>

<h2>Frequently Asked Questions</h2>

<h3>How deep should low-voltage landscape wire be buried?</h3>
<p>About 6 inches is the common standard for landscape lighting circuits of 30 volts or less. Run cable through a sleeve or conduit wherever it passes under concrete, pavers or other hardscape, and go deeper where aerators or future planting could reach it.</p>

<h3>What size transformer do I need?</h3>
<p>Add up the actual wattage of all fixtures and choose a transformer so that total is no more than about 80% of its rating. For example, a 240W load calls for at least a 300W transformer. A multi-tap model lets you compensate for voltage drop on longer runs.</p>

<h3>Is 12 gauge or 10 gauge wire better for landscape lighting?</h3>
<p>12 AWG handles most residential runs, especially with LED fixtures. Use 10 AWG for long runs, heavier loads or the home run to a hub. Calculate voltage drop for each run rather than guessing.</p>

<h3>Do I need an electrician to install low-voltage landscape lighting?</h3>
<p>The 12V cable and fixtures generally do not require an electrician. Adding an outdoor GFCI outlet, a new circuit or a hardwired transformer is line-voltage work that should be done by a licensed electrician, and it may need a city permit.</p>

<p>Want a low-voltage system designed and wired right the first time? Landscape Lighting Texas provides free consultations and estimates statewide, backed by a 5-year workmanship warranty. <a href="/quote/">Request your free quote</a> to get started.</p>
