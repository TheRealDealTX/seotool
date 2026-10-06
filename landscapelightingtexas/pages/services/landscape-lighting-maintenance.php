<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Repair, Retrofits & Annual Care';
$P['lead'] = 'Landscape lighting repair and maintenance for any brand of system: we find out why lights are dark or flickering, fix the wiring and transformers, retrofit old halogen fixtures to LED and keep everything aimed and clean year after year.';
?>
<section class="section">
  <div class="container">
<?php split('garden-pathway-lighting', 'Restored garden pathway lighting after landscape lighting repair and re-aiming', <<<'HTML'
<p class="eyebrow reveal">Any system, any installer</p>
<h2 class="section-title reveal">Landscape Lighting Repair That Finds the Real Problem</h2>
<p class="lead-p reveal">When landscape lighting fails, the symptom is rarely the cause. A dark run of path lights might be a nicked cable under a flower bed; dim fixtures at the end of a run point to voltage drop; a whole system that goes out after rain usually means a failing connection or a tripped GFCI. Good landscape lighting repair and maintenance starts with testing, not guessing.</p>
<p class="reveal">Landscape Lighting Texas services systems we installed and systems we didn’t, from any manufacturer. We check the transformer, measure voltage at the fixtures, trace and repair wiring, replace broken fixtures, and put the design back the way it was meant to look, or better.</p>
HTML); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
<?php section_head('What we fix', 'Common Landscape Lighting Problems We Repair', 'Texas weather, growing landscapes and time are hard on outdoor lighting. These are the issues we see most.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('bolt') ?></span><h3>Whole system out</h3><p>Tripped GFCI outlets, failed transformers, blown fuses or breakers, a dead photocell or a timer that lost its program after a power outage.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>One run dark</h3><p>Usually a cut or corroded cable, often from aeration, edging, new plantings or a fence post. We locate the break and repair it with sealed, direct-burial splices.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('bulb') ?></span><h3>Dim or uneven lights</h3><p>Voltage drop on long or undersized runs, an overloaded transformer or daisy-chained wiring. Fixes include re-tapping, hub wiring or heavier 12- or 10-gauge cable.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('spark') ?></span><h3>Flickering fixtures</h3><p>Loose or corroded connections, failing lamps or incompatible LED drivers. Humidity and irrigation make Texas connections a frequent culprit.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('tree') ?></span><h3>Lights aimed wrong</h3><p>Fixtures knocked by mowers, buried by mulch or swallowed by shrubs, and uplights that no longer fit a tree that has grown several feet. We re-aim and relocate.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('shield') ?></span><h3>Storm & hail damage</h3><p>Cracked lenses, broken stakes and bent fixtures after storms. We replace what is damaged and recommend tougher brass or copper fixtures where hail is common.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
<?php section_head('LED retrofits', 'Upgrading Halogen Landscape Lighting to LED', 'If your system still uses halogen lamps, an LED retrofit is usually the single best upgrade you can make.'); ?>
    <div class="grid-2">
      <div>
        <p class="reveal">LED landscape lighting uses roughly 75–80% less energy than halogen, runs much cooler and lasts far longer between lamp changes. For many older systems, that means lower running costs, less maintenance and a more consistent look across the property.</p>
        <p class="reveal">There are two ways to retrofit. Where the existing fixtures are solid brass or copper and in good condition, we can often install LED replacement lamps in the original housings. Where fixtures are worn, corroded or plastic, replacing them with integrated LED fixtures gives better optics and longer life. Either way, we check the transformer, recalculate the load and re-tap so the new lamps get the right voltage.</p>
        <p class="reveal">See what you might save with the <a href="/tools/energy-savings-calculator/">LED energy savings calculator</a>, or read <a href="/led-vs-halogen-landscape-lighting/">LED vs halogen landscape lighting</a> for the full comparison.</p>
      </div>
      <div>
        <div class="table-wrap reveal">
          <table>
            <thead><tr><th></th><th>Halogen system</th><th>After LED retrofit</th></tr></thead>
            <tbody>
              <tr><td>Energy use</td><td>Baseline</td><td>About 75–80% less</td></tr>
              <tr><td>Lamp changes</td><td>Frequent</td><td>Far less often</td></tr>
              <tr><td>Heat at the fixture</td><td>High</td><td>Low</td></tr>
              <tr><td>Transformer load</td><td>Often near capacity</td><td>Room to add fixtures</td></tr>
              <tr><td>Color options</td><td>Fixed warm white</td><td>2700K, 3000K, tunable or color</td></tr>
              <tr><td>Smart control</td><td>Limited</td><td>Ready for zoning and dimming</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
<?php section_head('See the difference', 'Before and After: A Restored Lighting System', 'Drag the slider. Many properties already have the fixtures; they just need repair, cleaning and re-aiming to look right again.'); ?>
<?php before_after('garden-pathway-lighting', 'Garden path with a dark, neglected lighting system compared to the restored system'); ?>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div>
<?php section_head('Annual maintenance plan', 'What an Annual Landscape Lighting Maintenance Visit Covers', '', 'left'); ?>
        <p class="reveal">Landscapes grow, mulch piles up and Texas weather wears on connections. A yearly visit keeps the system performing the way it did on reveal night. A typical maintenance visit includes:</p>
        <?= checklist([
          'Testing every zone and measuring voltage at the transformer and at the fixtures',
          'Cleaning lenses of dust, hard-water spots from irrigation and debris',
          'Re-aiming and re-leveling fixtures, and moving uplights as trees grow',
          'Trimming foliage away from fixtures and clearing mulch and soil',
          'Inspecting and resealing connections, and replacing failed lamps',
          'Resetting timers and astronomical schedules, and checking smart controls',
          'A short report on anything that needs attention before it fails',
        ]) ?>
        <p class="reveal">Plan pricing depends on the size of the system and is quoted after an initial evaluation. Prefer to handle some of it yourself? Use our <a href="/landscape-lighting-maintenance-checklist/">seasonal maintenance checklist</a>.</p>
      </div>
      <div>
<?php section_head('Texas conditions', 'Why Texas Systems Need Regular Care', '', 'left'); ?>
        <ul class="pill-list reveal"><li>Heat</li><li>Hail</li><li>Storms</li><li>Humidity</li><li>Salt air</li><li>Clay soil</li><li>Caliche</li><li>Fast growth</li></ul>
        <p class="reveal"><strong>Heat</strong> breaks down plastic housings and cheap connectors. <strong>Hail and storms</strong> crack lenses and knock fixtures over. <strong>Humidity and coastal salt</strong> corrode exposed splices, especially around Houston and the <a href="/areas/gulf-coast/">Gulf Coast</a>. Expanding <strong>clay soil</strong> and rocky <strong>caliche</strong> shift stakes and pull on wires, so fixtures drift out of aim. And a long growing season means shrubs can bury a path light in a single summer.</p>
        <p class="reveal">If your HOA has rules on outdoor lighting, a maintenance visit is also a good time to make sure fixtures are still shielded and aimed where they should be.</p>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
<?php section_head('How it works', 'Our Repair & Maintenance Process', 'The same four steps as a new project, adapted for an existing system.'); ?>
    <ol class="steps">
      <li><h3>Free dusk evaluation</h3><p>We see the system running at night, note what is dark, dim or misaimed, and talk through what you want it to look like.</p></li>
      <li><h3>Diagnosis & plan</h3><p>We test the transformer, circuits and fixtures, find the causes and give you an itemized quote for repairs, retrofits or an annual plan.</p></li>
      <li><h3>Expert repair</h3><p>Licensed, insured technicians repair wiring, replace failed components, retrofit to LED and correct voltage problems, protecting your plantings as they work.</p></li>
      <li><h3>Reveal & tune</h3><p>We return after dark to re-aim, balance brightness and reset your schedule, so the whole system looks finished again.</p></li>
    </ol>
    <?= tool_promo('/tools/transformer-calculator/') ?>
  </div>
</section>

<?php faqs([
  ['Do you repair landscape lighting systems you didn’t install?', 'Yes. We service landscape lighting from any brand and any installer. We test the system, explain what we find and recommend the most practical fix, whether that is a repair, an upgrade or a partial redesign.'],
  ['Why are only some of my landscape lights out?', 'When one section is dark, the cause is usually a damaged cable or a failed connection on that run. If lights are on but dim toward the end of a run, voltage drop is the likely cause. Our <a href="/low-voltage-landscape-lighting-guide/">low-voltage lighting guide</a> explains how runs are wired.'],
  ['Is it worth converting halogen landscape lighting to LED?', 'In most cases, yes. LEDs use about 75–80% less energy, need far fewer lamp changes and run cooler. If your fixtures are in good condition, LED replacement lamps can be a cost-effective path; worn fixtures are often better replaced with integrated LED models.'],
  ['How often should landscape lighting be maintained?', 'We recommend a professional check at least once a year, with quick homeowner checks each season: clean lenses, pull back mulch and plants and confirm the timer after power outages or time changes.'],
  ['Can you add fixtures or smart controls during a repair visit?', 'Yes. Repairs and retrofits are a good time to extend coverage or add <a href="/services/smart-lighting-systems/">smart controls</a>. An LED retrofit often frees up transformer capacity for new fixtures.'],
]); ?>

<section class="section alt">
  <div class="container">
<?php section_head('Keep exploring', 'Explore Other Services', 'Ready to expand once your system is working again?'); ?>
<?php service_cards('landscape-lighting-maintenance', 3); ?>
  </div>
</section>

<?php cta_band('Get Your Lights Back On', 'Tell Landscape Lighting Texas what’s happening with your system. We’ll evaluate it at dusk and send a clear, itemized repair or retrofit quote.'); ?>
