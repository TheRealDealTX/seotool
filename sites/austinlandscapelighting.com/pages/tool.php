<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$t = tools()[$slug];
$crumbs = [['Home', '/'], ['Tools', '/tools/'], [$t['name'], $t['path']]];

$copy = [
    'fixture-calculator' => [
        'title' => 'How Many Landscape Lights Do I Need? Free Calculator',
        'description' => 'Estimate how many landscape lighting fixtures your Austin home needs for the facade, paths, trees, steps, patio and pool, plus transformer size and budget.',
        'intro' => 'Enter a few measurements and the calculator applies the spacing and coverage rules Austin Landscape Lighting uses on real designs: one uplight per 10 feet of facade, path lights every 6 to 8 feet, two fixtures per mature tree and so on.',
        'faqs' => [
            ['q' => 'How accurate is the fixture calculator?', 'a' => 'It is a planning estimate built from the same spacing rules our designers start with. Real counts move with beam spreads, facade texture, canopy density and how much contrast you want. Most finished designs land within a few fixtures of the estimate.'],
            ['q' => 'Why does a two-story home add fixtures?', 'a' => 'Taller walls need either more fixtures or wider spacing with higher output to carry light to the roofline. We add a modest allowance so the upper story does not fade to black.'],
            ['q' => 'Does more fixtures always mean better?', 'a' => 'No. Over-lighting flattens texture and creates glare. A good design leaves some areas dark on purpose so the lit features stand out.'],
        ],
        'related' => ['/how-many-landscape-lights-do-i-need/', '/tools/cost-estimator/', '/tools/transformer-calculator/'],
    ],
    'cost-estimator' => [
        'title' => 'Landscape Lighting Cost Estimator for Austin Homes',
        'description' => 'Build a planning budget for landscape lighting in Austin from fixture count, fixture grade, controls, zones and site conditions, from Austin Landscape Lighting.',
        'intro' => 'Slide the fixture count and pick a fixture grade to see an installed planning range. The breakdown shows roughly where the money goes: brass fixtures, wire and connectors, transformer, controls, labor and night aiming.',
        'faqs' => [
            ['q' => 'What does a typical Austin system cost?', 'a' => 'Most Austin Landscape Lighting residential projects fall in a planning range of $3,500 to $12,000. A tight entry package is less; an estate with two zones and smart controls is more. Your written estimate is itemized and firm.'],
            ['q' => 'Why do fixture grades differ so much in price?', 'a' => 'Cast brass with integrated LEDs is excellent value. Machined brass with replaceable lamps and adjustable optics costs more up front but is easier to service and re-aim for decades.'],
            ['q' => 'Are design fees extra?', 'a' => 'Design is included when Austin Landscape Lighting installs the system. A stand-alone lighting plan for another contractor or a future phase is priced separately.'],
        ],
        'related' => ['/landscape-lighting-cost-in-austin/', '/tools/fixture-calculator/', '/services/custom-lighting-design/'],
    ],
    'led-savings-calculator' => [
        'title' => 'LED Landscape Lighting Savings Calculator',
        'description' => 'Compare halogen and LED landscape lighting energy use and cost. See annual and 10-year savings for your Austin system with the Austin Landscape Lighting calculator.',
        'intro' => 'Older Austin systems often run 35-watt halogen lamps that draw seven times the power of a modern LED. Enter your fixture count, hours and electricity rate to see what a retrofit saves in energy and lamp replacements.',
        'faqs' => [
            ['q' => 'Can I just swap LED lamps into my halogen fixtures?', 'a' => 'Often yes, if the fixtures are brass and the sockets are sound. We check the transformer taps and voltage at each fixture, because LED loads change the math on long wire runs.'],
            ['q' => 'How long do LED landscape lamps last?', 'a' => 'Quality LED lamps and integrated fixtures are rated for 40,000 to 50,000 hours, roughly 15 to 20 years at six hours a night, compared with about 2,000 hours for halogen.'],
            ['q' => 'Will LED light look cold?', 'a' => 'Not the ones we install. 2700K warm-white LEDs match the color of halogen with better consistency between fixtures.'],
        ],
        'related' => ['/services/led-upgrade-and-retrofit/', '/tools/color-temperature-guide/', '/solar-vs-low-voltage-landscape-lighting/'],
    ],
    'transformer-calculator' => [
        'title' => 'Low-Voltage Transformer Sizing Calculator',
        'description' => 'Size a 12-volt landscape lighting transformer from fixture wattage, apply 25 percent headroom and check voltage drop by wire gauge and run length.',
        'intro' => 'Add your fixtures by type, enter the longest wire run and gauge, and the tool recommends a transformer size, estimates voltage drop and suggests a multi-tap setting. Austin Landscape Lighting confirms every number with a meter during night aiming.',
        'faqs' => [
            ['q' => 'Why leave 25 percent headroom?', 'a' => 'Transformers run cooler and last longer below 80 percent load, and headroom lets you add a few fixtures later without replacing the transformer.'],
            ['q' => 'What is voltage drop and why does it matter?', 'a' => 'Resistance in the wire lowers voltage at the far end of a run. LEDs tolerate some drop, but too much dims fixtures or causes flicker. Heavier wire, shorter runs and multi-tap transformers fix it.'],
            ['q' => 'Can one transformer serve the front and back yard?', 'a' => 'Sometimes, but long runs around a house usually argue for a second transformer or a hub-and-spoke layout. We decide from the wire plan.'],
        ],
        'related' => ['/services/low-voltage-landscape-lighting/', '/tools/fixture-calculator/', '/landscape-lighting-design-guidelines/'],
    ],
    'color-temperature-guide' => [
        'title' => 'Landscape Lighting Color Temperature Guide (Kelvin)',
        'description' => 'Slide from 2000K candlelight to 5000K daylight and see how each color temperature looks on an Austin stone home, with Austin Landscape Lighting recommendations.',
        'intro' => 'Color temperature decides whether a home looks warm and expensive or harsh and commercial. Move the slider to preview each Kelvin value and read what it suits. Austin Landscape Lighting installs 2700K on most homes.',
        'faqs' => [
            ['q' => 'Can I mix color temperatures?', 'a' => 'Keep one temperature across the whole property, with at most a deliberate warmer accent zone on a patio or fire pit. Mixed temperatures look like mismatched bulbs.'],
            ['q' => 'What temperature matches my porch lights?', 'a' => 'Most residential porch lamps are 2700K. Matching the landscape system to them keeps the facade coherent. We can also re-lamp porch sconces as part of a project.'],
            ['q' => 'Is warm light dark-sky friendly?', 'a' => 'Warmer light with less blue content is preferred by dark-sky guidelines. Combined with fully shielded fixtures, 2700K is the responsible choice in the Hill Country.'],
        ],
        'related' => ['/services/custom-lighting-design/', '/modern-landscape-lighting-ideas/', '/tools/lighting-visualizer/'],
    ],
    'lighting-visualizer' => [
        'title' => 'Landscape Lighting Visualizer: Build Your Night Scene',
        'description' => 'Toggle uplighting, path lights, moonlighting, step lights and more on an illustrated Austin home and watch the fixture count and planning range update live.',
        'intro' => 'Every switch adds a technique to the scene and a line to the budget. Use it to decide what matters most to you before Austin Landscape Lighting walks your property at dusk.',
        'faqs' => [
            ['q' => 'Is this what my actual house will look like?', 'a' => 'It is an illustration of the techniques, not a rendering of your home. On the free consultation we can demo fixtures on your actual facade and trees at night.'],
            ['q' => 'Which techniques should I start with?', 'a' => 'Facade uplighting and path lighting deliver the most curb appeal and safety per dollar. Trees and patios are the usual second phase.'],
            ['q' => 'Why does "dark-sky friendly" not add fixtures?', 'a' => 'It is a design choice, not a product. Shielded fixtures aimed at the house rather than the sky cost nothing extra and keep the stars visible.'],
        ],
        'related' => ['/services/architectural-uplighting/', '/services/garden-and-tree-lighting/', '/tools/fixture-calculator/'],
    ],
    'sunset-timer' => [
        'title' => 'Austin Sunset Times & Landscape Lighting Timer Schedule',
        'description' => 'Tonight\'s sunset, civil dusk and sunrise for Austin, TX plus a month-by-month schedule showing when your landscape lights should switch on and off.',
        'intro' => 'Austin sunsets swing from about 5:30 pm in December to 8:40 pm in June. This tool computes tonight\'s times and a year-round schedule so you can see why Austin Landscape Lighting installs astronomic timers or photocells instead of fixed clocks.',
        'faqs' => [
            ['q' => 'Should lights come on at sunset or dusk?', 'a' => 'Civil dusk, about 25 to 30 minutes after sunset, is when the sky is dark enough for landscape lighting to read. Switching on at sunset wastes a little energy but looks fine too.'],
            ['q' => 'What is an astronomic timer?', 'a' => 'A timer that knows your latitude and the date, so it tracks sunset through the year and adjusts for daylight saving automatically. No seasonal resets.'],
            ['q' => 'Photocell or timer?', 'a' => 'A photocell turns lights on at dusk and off at dawn. A timer or smart controller can also turn them off at a set hour. Many Austin Landscape Lighting systems use a photocell for on and a timer for off.'],
        ],
        'related' => ['/services/smart-lighting-systems/', '/services/low-voltage-landscape-lighting/', '/tools/led-savings-calculator/'],
    ],
    'lighting-style-quiz' => [
        'title' => 'What Is Your Landscape Lighting Style? Take the Quiz',
        'description' => 'Eight quick questions match your Austin home to a landscape lighting style, with the services and color temperature Austin Landscape Lighting recommends for it.',
        'intro' => 'Modern minimal, classic estate, Hill Country natural or resort entertainer? Answer eight questions about your architecture, trees and evenings and we will suggest where to start.',
        'faqs' => [
            ['q' => 'What if I am between two styles?', 'a' => 'Most homes are. The quiz points to a starting palette; the design visit refines it to your facade and how you live outdoors.'],
            ['q' => 'Does style change the price?', 'a' => 'Mostly it changes where fixtures go, not how many. Modern designs often use fewer, more precise fixtures; resort designs add controls and zones.'],
            ['q' => 'Can I share my result?', 'a' => 'Mention it when you book a consultation and the Austin Landscape Lighting designer will bring matching fixture samples to demo at night.'],
        ],
        'related' => ['/services/custom-lighting-design/', '/tools/lighting-visualizer/', '/gallery/'],
    ],
][$slug];

$page = [
    'title' => $copy['title'],
    'description' => $copy['description'],
    'path' => $t['path'],
    'image' => 'landscape-lighting-design-tool-2',
    'active' => '/tools/',
    'body_class' => 'tool-page',
    'tools_js' => true,
    'schema' => [schema_webpage(['title' => $copy['title'], 'description' => $copy['description'], 'path' => $t['path']]), schema_breadcrumb($crumbs), schema_tool($t), schema_faq($copy['faqs'])],
];
$relatedLinks = [];
foreach ($copy['related'] as $r) {
    $label = $r;
    if (preg_match('#^/services/([a-z0-9-]+)/$#', $r, $m) && ($s = service($m[1]))) $label = $s['name'];
    elseif (preg_match('#^/tools/([a-z0-9-]+)/$#', $r, $m)) $label = TOOLS[$m[1]][0];
    elseif (preg_match('#^/([a-z0-9-]+)/$#', $r, $m) && ($pp = post($m[1]))) $label = $pp['h1'];
    elseif ($r === '/gallery/') $label = 'Project gallery';
    $relatedLinks[] = [$label, $r];
}
ob_start();
echo sub_hero(['eyebrow' => 'Free tool', 'h1' => e($t['name']), 'intro' => e($copy['intro']), 'crumbs' => $crumbs, 'cta' => false]);
?>
<section class="section section--tight">
  <div class="container" data-reveal="scale"><?= tool_markup($slug) ?></div>
</section>
<section class="section">
  <div class="container layout">
    <article class="prose" data-reveal>
      <h2 id="faq">About this tool</h2>
      <?= faq_list($copy['faqs'], 'tool-faq') ?>
    </article>
    <?= sidebar(['links' => $relatedLinks, 'links_title' => 'Go deeper']) ?>
  </div>
</section>
<section class="section section--alt section--tight">
  <div class="container">
    <?= section_head('More tools', 'Keep planning', '', 'left') ?>
    <div class="grid grid--4"><?php $i = 0; foreach (tools() as $o) { if ($o['slug'] === $slug) continue; if ($i++ >= 4) break; echo tool_card($o, $i); } ?></div>
  </div>
</section>
<?= cta_band() ?>
<?php
render_page($page, ob_get_clean());
