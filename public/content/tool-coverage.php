<?php defined('SCC') || exit;
return [
    'title' => 'Security Camera Coverage Calculator: FOV & Pixel Density',
    'description' => 'Calculate how wide a security camera sees at any distance and whether it can detect, recognize or identify faces and plates, using DORI pixel density.',
    'h1' => 'Security Camera Coverage & Detail Calculator',
    'crumb' => 'Coverage Calculator',
    'kicker' => 'Free tool',
    'icon' => 'eye',
    'keyword' => 'security camera coverage calculator',
    'published' => '2026-11-03', 'updated' => '2026-11-03',
    'image' => 'driveway-camera', 'image_alt' => 'Solar camera covering a long driveway',
    'lede' => 'A wide lens sees more but each person or plate gets fewer pixels. Enter your camera’s resolution and field of view to see how wide the scene is at any distance, and the maximum range at which it can still identify a face or read a plate.',
    'body' => <<<'HTML'
<h2>Field of view vs detail: the trade-off</h2>
<p>Every camera spreads a fixed number of horizontal pixels across the scene. At 30 ft, a 2K camera with a 110° lens covers a strip roughly 86 ft wide, so each foot gets about 30 pixels. Narrow the lens to 45° and the same camera covers about 25 ft with about 100 pixels per foot: far less area, far more detail.</p>
<p>That is why driveway and gate cameras often use telephoto or dual-lens designs, while yard cameras use wide lenses.</p>

<h2>DORI: detect, observe, recognize, identify</h2>
<div class="table-wrap"><table><thead><tr><th>Level</th><th>Pixels per meter</th><th>Pixels per foot</th><th>What you can do</th></tr></thead><tbody>
<tr><td>Detect</td><td>25</td><td>≈ 8</td><td>Tell that a person or vehicle is present</td></tr>
<tr><td>Observe</td><td>62</td><td>≈ 19</td><td>See clothing colours and what someone is doing</td></tr>
<tr><td>Recognize</td><td>125</td><td>≈ 38</td><td>Recognize someone you already know</td></tr>
<tr><td>Identify</td><td>250</td><td>≈ 76</td><td>Identify a stranger beyond reasonable doubt; read plates</td></tr>
</tbody></table></div>
<p>These thresholds come from the IEC/EN 62676-4 video surveillance standard and are widely used by camera makers to quote “DORI distances”. Real footage is usually somewhat worse than the math because of compression, motion blur and night mode.</p>

<h2>Practical tips</h2>
<ul>
<li><strong>Use the horizontal FOV.</strong> Spec sheets sometimes quote diagonal FOV, which is bigger and flatters the coverage.</li>
<li><strong>Plates need identify-level detail</strong> and a shallow angle. A plate seen from 45° to the side is much harder to read.</li>
<li><strong>Night halves your range.</strong> Infrared footage is softer, so plan identify-distance with daylight figures and expect less after dark.</li>
<li><strong>Mount height adds distance.</strong> A camera 10 ft up looking at a point 20 ft away is actually about 22 ft from the target.</li>
</ul>
<p>Pair this with the <a href="/tools/cctv-camera-planner/">CCTV camera planner</a> to decide which zones need detail and which just need coverage. For pan-tilt models, see <a href="/guides/360-degree-solar-camera/">360-degree solar cameras</a>.</p>
HTML,
    'faq' => [
        ['How far can a security camera identify a face?', 'It depends on resolution and lens. A 2K camera with a typical 105–110° wide lens has an identify range of only about 2–3 m (7–10 ft); a 4K camera with a 45° telephoto lens can identify at roughly 9 m (30 ft). Use the calculator for your exact camera.'],
        ['What field of view should a security camera have?', 'For general coverage of a yard, 100–130°. For driveways, gates or a door you need faces at, 40–80° or a dual-lens camera that combines a wide and a telephoto view.'],
        ['Is 4K worth it for security cameras?', '4K gives about 50% more horizontal pixels than 2K, extending identify range by roughly 50% at the same field of view. On solar cameras it also uses more battery and storage, so it matters most where you need distance.'],
        ['What does px/m mean?', 'Pixels per meter of scene width at the target distance. It measures how much detail lands on the subject: higher is better.'],
    ],
    'related' => ['/guides/solar-camera-driveway-alert-phone/', '/guides/solar-gate-camera/', '/guides/360-degree-solar-camera/'],
];
