<?php defined('SCC') || (http_response_code(404) && exit);
return [
    'title'       => '360 Degree Solar Camera: What Pan-Tilt Really Covers',
    'description' => 'A 360 degree solar camera pans about 355° but sees one view at a time. See how PTZ, auto-tracking, dual-lens and fisheye compare and where each fits.',
    'h1'          => '360 Degree Solar Camera Guide: Pan-Tilt, Dual-Lens and Fisheye Explained',
    'crumb'       => '360° Solar Cameras',
    'card_title'  => '360 Degree Solar Cameras',
    'card_text'   => 'What “360°” really means on a pan-tilt solar camera, how motors affect battery life, and where one beats two fixed cameras.',
    'kicker'      => 'Guide',
    'icon'        => 'camera',
    'keyword'     => '360 degree solar camera',
    'published'   => '2026-05-12',
    'updated'     => '2026-11-03',
    'image'       => '360-solar-camera',
    'image_alt'   => 'Pan-tilt 360 degree solar security camera with an attached solar panel mounted on the corner of a house',
    'affiliate'   => false,
    'lede'        => 'A <strong>360 degree solar camera</strong> is almost always a pan-tilt (PTZ) camera: a motor can swing the lens around roughly 355° horizontally and about 90° vertically, but at any moment it only sees its lens’s field of view, often 90–120°. That makes it great for following movement across an open yard, and weaker than fixed cameras at watching several spots at once.',
    'takeaways'   => [
        '“360°” on a solar camera usually means it can <strong>rotate</strong> about 355°, not that it records all directions simultaneously.',
        'Auto-tracking and patrol presets run motors, which <strong>draw extra power</strong>; heavy patrol schedules can outrun a small 3–6 W panel in winter.',
        'Dual-lens models pair a wide lens with a zoom or second wide lens to cut blind spots while panning.',
        'Best spots: the middle of a yard, an outside corner of a house, or a farmyard where a single pole sees in many directions.',
        'For doors and gates where you need a constant view, a fixed camera is usually the better choice.',
    ],
    'body' => <<<'HTML'
<h2>What does “360 degree” mean on a solar camera?</h2>
<p>Marketing often blurs two very different technologies. Most products sold as a 360 degree solar camera are <strong>pan-tilt cameras</strong>: the lens sits in a motorized head that rotates left-right (pan) and up-down (tilt). Typical specs read something like 355° pan and 90° tilt. The missing few degrees are a mechanical stop that keeps internal cables from twisting.</p>
<p>The key point is that a pan-tilt camera’s <em>instantaneous</em> view is just its lens’s horizontal field of view, commonly 90–120°. When it looks at the driveway, it is not looking at the back gate. A true simultaneous 360° view requires a <a href="https://en.wikipedia.org/wiki/Fisheye_lens" target="_blank" rel="noopener">fisheye</a> lens (one ultra-wide lens, usually ceiling-mounted, with a distorted circular image) or several lenses stitched together. Those designs are rare in battery-solar form because they need more processing power.</p>
<div class="keyfacts">
<div><b>~355°</b><span>typical horizontal pan range</span></div>
<div><b>~90°</b><span>typical tilt range</span></div>
<div><b>90–120°</b><span>what the lens sees at one moment</span></div>
</div>

<h2>PTZ solar security camera vs fixed vs dual-lens vs fisheye</h2>
<p>Here’s how the main camera styles compare when powered by solar. “PTZ” strictly means <a href="https://en.wikipedia.org/wiki/Pan%E2%80%93tilt%E2%80%93zoom_camera" target="_blank" rel="noopener">pan-tilt-zoom</a>; many solar models only do pan-tilt with digital zoom, so read the spec sheet.</p>
<div class="table-wrap"><table>
<thead><tr><th>Type</th><th>What it sees at once</th><th>Can follow motion?</th><th>Power draw on solar</th><th>Best use</th></tr></thead>
<tbody>
<tr><td>Fixed bullet/box</td><td>One fixed 90–130° view</td><td>No</td><td>Lowest</td><td>Doors, gates, driveways, constant views</td></tr>
<tr><td>Pan-tilt (PTZ)</td><td>One 90–120° view, aimable over ~355°</td><td>Yes, with auto-tracking</td><td>Moderate; spikes when motors run</td><td>Open yards, corners, farmyards</td></tr>
<tr><td>Dual-lens pan-tilt</td><td>Wide view plus a second zoom or wide view</td><td>Yes</td><td>Moderate to higher (two sensors)</td><td>Large areas where detail at distance matters</td></tr>
<tr><td>Dual-lens fixed (back-to-back or split)</td><td>Two fixed views, up to ~180° combined</td><td>No</td><td>Moderate</td><td>Building corners, long fence lines</td></tr>
<tr><td>Fisheye / panoramic</td><td>Full 180–360° at once (distorted)</td><td>Not needed</td><td>Higher; rare on battery solar</td><td>Ceilings, carports, covered patios</td></tr>
</tbody>
</table></div>

<h2>How auto-tracking and patrol presets work</h2>
<p><strong>Auto-tracking</strong> uses motion detection, often combined with on-camera AI that recognizes people, vehicles or animals, to keep a subject centered by nudging the pan and tilt motors. On a battery camera, the trigger is usually the PIR sensor (heat-motion, typical range 8–12 m), which wakes the camera; the image processor then takes over to follow the subject.</p>
<p><strong>Patrol</strong> or <strong>cruise</strong> modes move the camera between saved preset positions on a schedule, for example front gate, then driveway, then side yard, dwelling a set time at each. On a mains-powered PTZ this is free. On solar it’s a power decision.</p>
<h3>Battery impact of motors</h3>
<p>Stepper motors in small pan-tilt heads draw modest current, but they also keep the camera awake: the sensor, processor and often the radio stay on while the head moves. The cost of a patrol isn’t the motor alone; it’s the minutes of “awake” time it creates.</p>
<p>As a rule of thumb, a solar camera that wakes 20–40 times a day for short clips fits comfortably on a typical 3–6 W panel in summer. Add a patrol cycle every 15 minutes and you’ve added 96 wake-ups a day before any motion at all. That can push daily consumption well past what the panel replaces on short winter days with 2–3 peak sun hours. Model your own setup in the <a href="/tools/solar-camera-battery-calculator/">solar camera battery calculator</a>.</p>
<div class="callout tip"><strong>Battery-friendly settings</strong><p>Use auto-tracking instead of timed patrol, limit tracking duration (for example 20–30 seconds), set the home position to the most important view, and disable patrol overnight unless you truly need it. Then check whether your mounting spot gets enough sun with the <a href="/tools/solar-camera-site-check/">site check</a>.</p></div>

<h2>Dual lens solar cameras: why two lenses help a pan-tilt</h2>
<p>A single-lens PTZ has one weakness: while it zooms in on a person at the gate, it loses the wide view of everything else. Dual-lens designs address this in two ways:</p>
<ul>
<li><strong>Wide + telephoto:</strong> one lens stays wide for context while the other zooms optically on the tracked subject. You get a usable face or plate at distance without giving up situational awareness.</li>
<li><strong>Wide + wide (pointed differently):</strong> two fixed fields of view combined into roughly 180° or more, sometimes on a panning head, which shrinks the area hidden behind the camera at any moment.</li>
</ul>
<p>Two image sensors mean more processing and slightly higher energy per event. Dual-lens solar cameras often come with larger integrated panels or a separate panel option for that reason. Read <a href="/how-solar-cameras-work/">how solar cameras work</a> for the power chain behind those trade-offs.</p>

<h2>Where a 360 solar security camera outdoors makes sense</h2>
<p>A pan-tilt camera earns its place where activity can come from many directions and a single mounting point has a clear view all around.</p>
<figure><img src="/assets/img/360-solar-camera-2.webp" alt="360 degree pan-tilt solar camera on a pole in the middle of an open yard with clear sightlines in every direction" width="1200" height="800" loading="lazy"><figcaption>A pole in the middle of an open area is the classic spot for a pan-tilt solar camera.</figcaption></figure>
<ul>
<li><strong>Center of a yard or paddock.</strong> On a pole with nothing blocking any side, the camera can track movement anywhere around it.</li>
<li><strong>Outside corner of a house.</strong> A corner mount covers two walls; a pan-tilt can swing to watch either side, or the yard between them. Wall-mounted, the building itself blocks roughly half the circle, so you’re effectively getting about 270°.</li>
<li><strong>Farm yards and equipment areas.</strong> One camera on a central pole can follow vehicles between barn, fuel tank and gate. See <a href="/use-cases/solar-cameras-for-farms/">solar cameras for farms</a>.</li>
<li><strong>Construction sites.</strong> Layouts change weekly; a PTZ can be re-aimed from the app instead of a ladder. More in <a href="/use-cases/solar-cameras-for-construction-sites/">solar cameras for construction sites</a>.</li>
</ul>
<h3>When fixed cameras are better</h3>
<p>Front doors, gates and driveways need constant, unbroken coverage. If a PTZ is tracking a cat in the back corner when a car pulls in, the car isn’t recorded. For these zones, two fixed cameras often beat one pan-tilt at similar total cost. Use the <a href="/tools/cctv-camera-planner/">CCTV camera planner</a> to see how many fixed views your property needs, and read <a href="/guides/how-many-cctv-cameras-do-i-need/">how many CCTV cameras do I need</a> for zone-by-zone advice.</p>

<h2>How much area can a pan-tilt solar camera cover?</h2>
<p>Coverage has two dimensions: angle and detail. A camera that swings through 355° still only resolves faces at a limited distance. With a typical 2K or 3K sensor and a 100–110° lens, faces are usually identifiable out to only a few meters and recognizable out to perhaps 10–15 m; beyond that you see that someone is there but not who. Optical zoom or a telephoto second lens extends that range in the zoomed direction.</p>
<p>Plug your lens angle, resolution and distance into the calculator below to see the width of the scene and whether you’ll get enough pixels per foot to identify a person.</p>
<!--tool:coverage-->
<p>Run it once for the wide lens and once for the zoom position (if your camera has one) to see the difference. You can also open the full <a href="/tools/camera-coverage-calculator/">camera coverage calculator</a> in its own page.</p>

<h2>Mounting a 360 degree solar camera: upright vs inverted</h2>
<p>Most pan-tilt solar cameras can be mounted two ways:</p>
<ul>
<li><strong>Upright</strong> on a flat surface, fence post top or pole bracket, with the head above the base. This gives the clearest all-around view and is the norm for pole mounts.</li>
<li><strong>Inverted</strong> (upside down) under an eave or soffit. The app usually has an “image flip” setting. This protects the camera from rain, but the eave can shade an integrated solar panel, so you may need a separate panel on a cable placed in the sun.</li>
</ul>
<p>Mount height of about 2.5–3.5 m is a good balance: high enough to deter tampering and see over fences, low enough that faces aren’t just the tops of heads. Pole mounts in open ground can go higher for a broader view. For panel tilt and direction, use the <a href="/tools/solar-panel-angle-calculator/">solar panel angle calculator</a>, and see the general <a href="/solar-camera-installation/">solar camera installation guide</a> for wiring and sealing.</p>
<div class="callout warn"><strong>Check the panel cable length</strong><p>On a pan-tilt camera, the panel cable must not snag as the head turns. Route it from the base, not the moving head, and leave a drip loop so water runs off before reaching the connector.</p></div>

<h2>Privacy masks and pointing rules</h2>
<p>A camera that can turn almost all the way around can also turn toward a neighbor’s window. Most PTZ apps let you draw <strong>privacy masks</strong>, which black out areas of the image, and some let you set pan limits so the head never turns past a certain angle. Masks should stay locked to the scene as the camera pans; check this in the app after setup.</p>
<p>Laws on recording neighboring property vary by state and country. Video of areas visible from public spaces is generally treated differently from views into private spaces, and audio recording is usually stricter because of wiretap and consent laws. Check local rules, and if you rent, read <a href="/guides/rental-property-outdoor-camera-no-subscription/">our guide to outdoor cameras for rental properties</a>.</p>

<h2>Do pan-tilt solar cameras track at night?</h2>
<p>Most do, with limits. In infrared night mode the image is black and white, and AI person or vehicle detection still works on many models, though accuracy drops at the edge of IR range. Built-in IR illuminators on small solar cameras usually reach roughly 8–15 m; beyond that the camera may detect heat-motion with its PIR but have too little light to track a shape. Models with a spotlight can switch to color night vision when triggered, which helps tracking but costs significant battery per event. For more on how solar cameras handle darkness, read <a href="/guides/do-solar-cameras-work-at-night/">do solar cameras work at night</a>.</p>
<p>One quirk specific to pan-tilt models: when the head turns, the IR illuminator turns with it, so areas the camera isn’t pointed at are dark in the footage. A fixed floodlight covering the yard can help any camera, PTZ or not.</p>

<h2>What to check before buying a 360 degree solar camera</h2>
<p>Spec sheets for pan-tilt solar cameras look similar, but a few details separate a good fit from a frustrating one.</p>
<div class="table-wrap"><table>
<thead><tr><th>Spec</th><th>What to look for</th><th>Why it matters</th></tr></thead>
<tbody>
<tr><td>Pan / tilt range</td><td>~355° pan, 90° or more tilt</td><td>Tilt range decides whether it can look down at the base of a pole or up a slope</td></tr>
<tr><td>Zoom type</td><td>Optical zoom or telephoto second lens</td><td>Digital zoom only crops; detail at distance stays limited</td></tr>
<tr><td>Panel</td><td>Integrated plus option for a separate panel</td><td>Lets you mount under an eave and still put the panel in sun</td></tr>
<tr><td>Battery capacity</td><td>Larger is better for heavy tracking</td><td>Motors and longer clips use more energy per event</td></tr>
<tr><td>Tracking controls</td><td>Adjustable tracking time, return-to-home, schedules</td><td>Keeps motor use and battery drain in check</td></tr>
<tr><td>Privacy masks</td><td>Masks that follow the scene as it pans</td><td>Fixed-position masks drift off target when the head moves</td></tr>
<tr><td>Connectivity</td><td>2.4 GHz Wi-Fi or 4G option</td><td>Remote yards often need cellular; see <a href="/guides/do-solar-cameras-need-wifi/">do solar cameras need Wi-Fi</a></td></tr>
</tbody>
</table></div>

<!--products:eufy-s340,go-pt-ultra,argus4pro-->

<h2>Is a 360 degree solar camera worth it?</h2>
<p>A pan-tilt solar camera is worth it when you have one good mounting point with open views in many directions and activity that moves around: yards, farms, job sites. It’s less worth it as your only camera at a front door or gate, where constant coverage matters more than flexibility. Many owners end up with a mix: fixed cameras on entry points and one PTZ watching the open ground in between. For the bigger cost-benefit question, read <a href="/guides/are-solar-cameras-worth-it/">are solar cameras worth it</a>, and compare models in our <a href="/best-solar-security-cameras/">best solar security cameras</a> guide.</p>
HTML,
    'faq' => [
        ['Does a 360 degree solar camera record all directions at once?', 'Usually not. Most are pan-tilt cameras that rotate about 355° but only see their lens’s field of view, often 90–120°, at any moment. Simultaneous 360° recording requires a fisheye or multi-lens panoramic camera, which is uncommon in battery-solar models because of the extra processing power needed.'],
        ['Do pan tilt solar cameras drain the battery faster?', 'They can. The motors themselves use modest power, but every movement keeps the sensor, processor and radio awake. Timed patrol modes add many wake-ups per day. Auto-tracking triggered by motion, with short tracking limits, is much easier on a small solar panel than continuous patrol.'],
        ['What is the difference between PTZ and pan-tilt?', 'PTZ stands for pan-tilt-zoom. A true PTZ has an optical zoom lens that magnifies without losing detail. Many solar models only pan and tilt and offer digital zoom, which crops the image. Some dual-lens cameras add a telephoto lens that acts like optical zoom.'],
        ['Where is the best place to mount a 360 solar security camera?', 'Ideally on a pole or high point with clear views in many directions, such as the center of a yard or farmyard. On a house, an outside corner gives roughly 270° of usable view. Mount around 2.5–3.5 m high and make sure the solar panel gets several hours of direct sun.'],
        ['Is one 360 camera better than two fixed cameras?', 'It depends on the zone. For open areas where activity moves around, one pan-tilt camera can replace two or three fixed views. For doors, gates and driveways that need constant coverage, two fixed cameras are usually more reliable because they never look away.'],
        ['Can I set privacy zones on a pan-tilt solar camera?', 'Most apps support privacy masks that black out parts of the image, and some let you limit how far the head can pan. After setup, pan the camera through its full range to confirm the masks stay aligned with the areas you want hidden.'],
    ],
    'related' => ['/guides/how-many-cctv-cameras-do-i-need/', '/best-solar-security-cameras/', '/use-cases/solar-cameras-for-farms/'],
];
