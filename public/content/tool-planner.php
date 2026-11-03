<?php defined('SCC') || (http_response_code(404) && exit);
return [
    'title' => 'How Many CCTV Cameras Do I Need? Free Camera Planner',
    'description' => 'Free CCTV camera planner: choose your property and zones to see how many security cameras you need, which types, where solar fits and a typical budget.',
    'h1' => 'CCTV Camera Planner: How Many Cameras Do I Need?',
    'crumb' => 'CCTV Camera Planner',
    'kicker' => 'Free tool',
    'icon' => 'map',
    'keyword' => 'how many cctv cameras do i need calculator',
    'published' => '2026-11-03', 'updated' => '2026-11-03',
    'image' => 'how-many-cctv-cameras', 'image_alt' => 'Security cameras covering the zones around a house',
    'lede' => 'Tick the areas you want covered and pick a coverage level. The planner turns that into a camera count, the right camera type for each zone, which spots suit solar power, and a realistic hardware budget you can copy or print.',
    'body' => <<<'HTML'
<h2>How the planner decides</h2>
<p>Every zone carries a priority. Entry points that burglars actually use (front door, back door, driveway) are priority one. Side passages, garages, yards and the indoor entry hall are priority two. Outbuildings, gates, patios, fence lines and other indoor rooms are priority three. Your coverage level decides how deep the plan goes:</p>
<div class="table-wrap"><table><thead><tr><th>Coverage level</th><th>Includes</th><th>Typical detached house</th></tr></thead><tbody>
<tr><td>Essential</td><td>Priority-one entry points</td><td>3 cameras</td></tr>
<tr><td>Balanced</td><td>Entry points + blind spots</td><td>4–6 cameras</td></tr>
<tr><td>Complete</td><td>Every ticked zone; 2–3 cameras on big yards, fence lines and long driveways</td><td>6–10 cameras</td></tr>
</tbody></table></div>

<h2>Camera type per zone</h2>
<ul>
<li><strong>Front door:</strong> a video doorbell sees faces and packages at close range in a head-to-toe view.</li>
<li><strong>Driveway and gates:</strong> a dual-lens or 4K camera keeps enough pixels on vehicles and plates at distance. Check the numbers with the <a href="/tools/camera-coverage-calculator/">coverage calculator</a>.</li>
<li><strong>Back door and garage:</strong> a floodlight camera lights the area and deters, but needs more power. On solar, pick a model with a large panel.</li>
<li><strong>Yards and fence lines:</strong> wide-angle cameras on normal lots, pan-tilt (360°) cameras on large ones.</li>
<li><strong>Remote sheds and gates without Wi‑Fi:</strong> 4G LTE solar cameras.</li>
</ul>

<h2>Where solar makes sense</h2>
<p>The planner marks a zone as a solar candidate when it is outdoors and power outlets are scarce or the spot is far from the house (gate, shed, fence line). Before buying, check each solar spot with the <a href="/tools/solar-camera-site-check/">Solar Site Check</a>. Walls that face away from the sun or sit under deep eaves may suit a wired or plug-in camera better.</p>

<h2>Placement rules that apply to every plan</h2>
<ol class="steps">
<li><strong>Height 7–10 ft (2.1–3 m)</strong><p>High enough to be hard to reach, low enough to see faces rather than the tops of heads.</p></li>
<li><strong>Overlap fields of view</strong><p>Each camera should see a little of its neighbour’s area so nobody can pass between them unseen.</p></li>
<li><strong>Watch approaches, not just doors</strong><p>A camera aimed down a path catches a face walking toward it; one aimed at the door catches the back of a head.</p></li>
<li><strong>Respect neighbours’ privacy</strong><p>Use privacy masks for windows and gardens that are not yours.</p></li>
</ol>
<p>Want the reasoning in more depth? Read <a href="/guides/how-many-cctv-cameras-do-i-need/">how many CCTV cameras do I need</a>.</p>
HTML,
    'faq' => [
        ['How many security cameras does an average house need?', 'Most detached houses are well covered with four to six cameras: front door, driveway, back door and one or two covering the yard and side passages. Apartments often need one or two, and acreage or farms eight or more.'],
        ['Is one camera enough for a house?', 'One camera can cover the main entrance, but it leaves the back door and sides unwatched, which is where most forced entries happen. Two cameras (front and back) are a sensible minimum.'],
        ['Should indoor cameras be part of my plan?', 'An indoor camera in the entry hall catches anyone who gets past the outdoor cameras. Choose one with a physical privacy shutter or a scheduled privacy mode, and never place cameras where people expect privacy.'],
        ['Are the budget figures accurate?', 'They are typical US retail ranges for consumer cameras in late 2026, excluding installation and monitoring. Prices vary widely by brand and sales.'],
    ],
    'related' => ['/guides/how-many-cctv-cameras-do-i-need/', '/best-solar-security-cameras/', '/solar-camera-installation/'],
];
