<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['FAQ', '/faq/']];
$faqs = site_faqs();
$extra = [
    ['q' => 'Do I need a permit for landscape lighting in Austin?', 'a' => 'Low-voltage (12-volt) landscape lighting does not require an electrical permit in most Central Texas jurisdictions. The transformer plugs into an existing exterior GFCI outlet. If a new 120-volt circuit or outlet is needed, a licensed electrician handles that portion with any required permit.'],
    ['q' => 'Can you work with my existing system?', 'a' => 'Yes. Austin Landscape Lighting repairs, retrofits and expands existing systems, including older halogen installs from other companies. We start with a system audit: transformer load, wire condition, fixture health and voltage at each fixture.'],
    ['q' => 'Will installation damage my landscaping?', 'a' => 'Low-voltage wire is buried a few inches deep in mulch or turf with a flat spade, not a trencher. Beds are returned to how we found them, and we route around roots and irrigation lines.'],
    ['q' => 'How do smart controls work?', 'a' => 'A Wi-Fi or Bluetooth controller replaces the simple timer. From an app you can set schedules tied to sunset, dim zones, create scenes for entertaining and turn everything off from bed. Voice assistants are supported on most systems.'],
    ['q' => 'Do you offer maintenance plans?', 'a' => 'Yes. Seasonal tune-ups include re-aiming fixtures that have shifted, trimming growth that blocks beams, cleaning lenses, checking connections and transformer settings, and replacing any lamps under warranty.'],
    ['q' => 'What happens on the free consultation?', 'a' => 'A designer walks the property with you, ideally at dusk, listens to how you use your outdoor space and notes the features worth lighting. Within a few days you receive a fixture-by-fixture plan and a written, itemized estimate.'],
];
$all = array_merge($faqs, $extra);
$page = [
    'title' => 'Landscape Lighting FAQ | Austin Landscape Lighting',
    'description' => 'Answers to common landscape lighting questions in Austin: cost, timelines, LED vs halogen, color temperature, warranties, permits, smart controls and maintenance.',
    'path' => '/faq/',
    'active' => '/faq/',
    'schema' => [schema_webpage(['title' => 'FAQ', 'description' => 'Landscape lighting FAQ.', 'path' => '/faq/'], 'FAQPage'), schema_breadcrumb($crumbs), schema_faq($all)],
];
ob_start();
echo sub_hero(['eyebrow' => 'FAQ', 'h1' => 'Landscape Lighting Questions, Answered', 'intro' => 'Everything Austin homeowners ask Austin Landscape Lighting before a project: what it costs, how long it takes, which fixtures and color temperatures we use and what the warranty covers.', 'crumbs' => $crumbs, 'cta' => false]);
?>
<section class="section">
  <div class="container container--narrow"><?= faq_list($all, 'all-faq') ?></div>
</section>
<section class="section section--alt section--tight">
  <div class="container">
    <?= section_head('Still curious?', 'Run the numbers yourself', '', 'left') ?>
    <div class="grid grid--4"><?php foreach (array_slice(array_values(tools()), 0, 4) as $i => $t) echo tool_card($t, $i); ?></div>
  </div>
</section>
<?= contact_section('Ask us anything', 'Have a question we did not cover?') ?>
<?php
render_page($page, ob_get_clean());
