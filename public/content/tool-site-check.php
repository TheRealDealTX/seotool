<?php defined('SCC') || exit;
return [
    'title' => 'Solar Camera Site Check: Will Solar Work at My Spot?',
    'description' => 'Answer 7 quick questions about sun, shade, climate, activity and signal to see if a solar security camera will stay charged where you want to mount it.',
    'h1' => 'Solar Camera Site Check',
    'crumb' => 'Solar Site Check',
    'kicker' => 'Free tool',
    'icon' => 'compass',
    'keyword' => 'will a solar camera work at my house',
    'published' => '2026-11-03', 'updated' => '2026-11-03',
    'image' => 'direct-sunlight', 'image_alt' => 'Solar security camera in direct sunlight',
    'lede' => 'Not every wall is a good home for a solar camera. Answer seven questions about the mounting spot and get a 0–100 suitability score with specific fixes: a bigger panel, a cable to a sunnier spot, a different radio, or a wired camera instead.',
    'body' => <<<'HTML'
<h2>What the score means</h2>
<div class="table-wrap"><table><thead><tr><th>Score</th><th>Verdict</th><th>What to expect</th></tr></thead><tbody>
<tr><td>70–100</td><td>Great solar site</td><td>A standard 3–6 W panel keeps the battery near full most of the year.</td></tr>
<tr><td>45–69</td><td>Workable</td><td>Occasional top-ups in winter unless you upsize the panel or trim triggers.</td></tr>
<tr><td>0–44</td><td>Solar will struggle</td><td>Relocate the panel, add capacity, or use a wired/plug-in camera here.</td></tr>
</tbody></table></div>

<h2>The factors, and why they’re weighted this way</h2>
<p><strong>Direct sun hours</strong> carry the most weight because panel output is roughly proportional to direct sunlight. Diffuse light on an overcast day or in open shade gives only around 10–25% of rated output.</p>
<p><strong>Shade type</strong> matters because winter shade is the killer. A building or hill that blocks the low December sun can stop charging entirely for months, while leafy trees mostly shade in summer, when you have energy to spare.</p>
<p><strong>Orientation and climate</strong> set the ceiling. East or west faces lose roughly 15–25% compared with facing the equator, and grey northern winters can deliver only 1–2 peak sun hours a day.</p>
<p><strong>Activity</strong> sets the demand. A quiet backyard might record ten short clips a day; a camera facing a street can record a hundred or more.</p>
<p><strong>Panel options</strong> can rescue a poor spot: a separate panel on a 10–16 ft cable can sit on a sunny fence or roof edge while the camera stays where it needs to be.</p>
<p><strong>Connectivity</strong> doesn’t change the energy score much, but it changes which camera you should buy. Weak Wi‑Fi makes a camera transmit longer, and 4G radios draw more power than Wi‑Fi.</p>

<div class="callout tip"><strong>How to measure sun hours without tools</strong><p>On a clear day, note when direct sunlight first lands on the spot and when it leaves. Repeat in winter if you can, or picture the sun about 47° lower at noon in December than in June. Free sun-path apps can show the arc against your yard.</p></div>

<h2>Next steps</h2>
<p>Turn the score into numbers with the <a href="/tools/solar-camera-battery-calculator/">battery and power calculator</a>, set the panel angle with the <a href="/tools/solar-panel-angle-calculator/">panel angle calculator</a>, and read <a href="/guides/do-solar-cameras-need-direct-sunlight/">do solar cameras need direct sunlight</a> for shade workarounds.</p>
HTML,
    'faq' => [
        ['How many hours of sun does a solar security camera need?', 'Most need about 2–4 hours of direct sun a day at moderate activity with a 3–6 W panel. Busy locations, 4G models and 4K cameras need more.'],
        ['Will a solar camera work on a north-facing wall?', 'In the northern hemisphere a north-facing wall gets little direct sun, so a panel mounted there will struggle. Mount the camera on the north wall but run the panel’s cable to a south-facing spot, roof edge or pole.'],
        ['Does a solar camera work under trees?', 'Under dense evergreen cover, usually not well. Under deciduous trees it can work, because leaves drop in winter when you need the energy most, but clean fallen leaves off the panel.'],
        ['Is my answer saved anywhere?', 'No. The quiz runs in your browser and nothing is sent to our server.'],
    ],
    'related' => ['/guides/do-solar-cameras-need-direct-sunlight/', '/guides/solar-camera-panel-angle/', '/guides/are-solar-cameras-worth-it/'],
];
