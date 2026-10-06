<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Patios, Pergolas & Outdoor Kitchens';
$P['lead'] = 'Patio and outdoor living lighting designed for the way Texans actually use their backyards: long evenings at the grill, late dinners under the pergola and conversations that run well past dark. Warm, glare-free light where you need it, and nothing where you don’t.';
?>
<section class="section">
  <div class="container">
<?php split('patio-lighting', 'Covered patio and pergola lit with warm string lights and downlights at dusk in Texas', <<<'HTML'
<p class="eyebrow reveal">Outdoor living, after dark</p>
<h2 class="section-title reveal">Patio Lighting That Makes Evenings Outside Feel Like an Extra Room</h2>
<p class="lead-p reveal">Good patio and outdoor living lighting is not one bright fixture on the back wall. It is three or four quiet layers working together: soft downlight on the table, task light at the grill, safe light on every step and a gentle glow in the surrounding garden so the yard doesn’t turn into a black wall the moment the sun goes down.</p>
<p class="reveal">In Texas, the patio is where life happens from March to November, and often longer. Landscape Lighting Texas designs outdoor living lighting around how you use the space: where people sit, where the cook stands, where kids run and where guests will look when they step outside. Every fixture is low-voltage LED, warm in color and aimed so you see the space, not the bulb.</p>
HTML); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
<?php section_head('Techniques & fixtures', 'The Layers of Great Outdoor Living Lighting', 'Each layer has a job. Together they let you dim the patio for a quiet night or bring it up for a crowd without ever reaching for a floodlight.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('patio') ?></span><h3>Bistro & string lights</h3><p>Commercial-grade, low-wattage LED strings run on catenary cable between posts, pergola beams or the eave. Dimmed to 30–50%, they set the mood without blinding anyone seated underneath.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('bulb') ?></span><h3>Pergola & ceiling downlights</h3><p>Small, shielded downlights tucked into beams or porch ceilings put a soft pool of light on the table and seating. Narrow optics keep light on the surface and out of eyes.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>Step & riser lights</h3><p>Low-profile brick, riser and deck-post lights mark every change in level. They are the single biggest safety upgrade for a raised patio, pool deck or stone stair.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('spark') ?></span><h3>Outdoor kitchen task light</h3><p>Under-counter and hood-area fixtures at a slightly higher output so you can actually see whether the brisket is done, with a separate zone that dims down after the meal.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('tree') ?></span><h3>Perimeter & garden glow</h3><p>A few uplights on nearby trees, a grazed wall or a lit planting bed give the eye somewhere to land beyond the patio edge, which makes the whole space feel larger and calmer.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('sun') ?></span><h3>Fire pit & seating accents</h3><p>Around a fire feature we keep light low and indirect, often a hardscape strip under a seat wall cap, so the flames stay the focal point and faces stay comfortable.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
<?php section_head('See the difference', 'Before and After: A Patio Built for Nighttime', 'Drag the slider. The structure is the same; what changes is whether the space invites you to stay outside after sunset.'); ?>
<?php before_after('patio-lighting', 'Texas patio with layered string lights and downlights compared to the same patio unlit'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
<?php section_head('Planning guide', 'Patio Lighting Fixtures Compared', 'The right mix depends on how the space is built and how you use it. These are the fixture types we specify most often, with typical settings.', 'left'); ?>
    <div class="table-wrap reveal">
      <table>
        <thead><tr><th>Fixture</th><th>Best for</th><th>Typical color</th><th>Notes</th></tr></thead>
        <tbody>
          <tr><td>LED string / bistro lights</td><td>Open patios, pergolas, courtyards</td><td>2200K–2700K</td><td>Hung on steel catenary cable; on a dimmer or dimmable smart zone</td></tr>
          <tr><td>Recessed or surface downlights</td><td>Porch ceilings, pergola beams</td><td>2700K</td><td>Narrow optic and glare shield; aim at the table, not the chairs</td></tr>
          <tr><td>Step / riser lights</td><td>Stairs, raised decks, pool coping</td><td>2700K–3000K</td><td>Low output; louvered faces throw light down onto the tread</td></tr>
          <tr><td>Hardscape strip lights</td><td>Seat walls, counters, bar overhangs</td><td>2700K</td><td>Mounted under the cap so only the wall face glows</td></tr>
          <tr><td>Under-counter task lights</td><td>Grill stations, outdoor kitchens</td><td>3000K</td><td>Separate zone so cooking light can be turned down after dinner</td></tr>
          <tr><td>Accent uplights</td><td>Nearby trees, walls, planters</td><td>2700K–3000K</td><td>Frame the space so the yard beyond the patio doesn’t go black</td></tr>
        </tbody>
      </table>
    </div>
    <p class="reveal">Not sure whether candle-warm or crisper light suits your stone and cushions? Try both in our <a href="/tools/color-temperature-visualizer/">color temperature visualizer</a>, or read the <a href="/landscape-lighting-color-temperature-guide/">2700K vs 3000K guide</a>.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div>
<?php section_head('Built for Texas', 'Outdoor Living Lighting That Holds Up to Texas Weather', '', 'left'); ?>
        <p class="reveal">A patio light in Texas works harder than one almost anywhere else. It runs most nights of the year, bakes under afternoon sun on a west-facing slab, takes wind-driven rain and, in much of the state, hail. We design for that from the start.</p>
        <?= checklist([
          '<strong>Heat:</strong> LED drivers rated for high ambient temperatures and fixtures with real heat sinks, never sealed plastic housings that cook in July.',
          '<strong>Hail and storms:</strong> brass, copper or heavy cast fixtures, commercial string lights on tensioned steel cable and sockets rated for wet locations.',
          '<strong>Humidity and coastal salt:</strong> sealed, IP-rated connections and solid brass hardware near Houston and the <a href="/areas/gulf-coast/">Gulf Coast</a>.',
          '<strong>Clay and caliche:</strong> cable routed in conduit under slabs and pavers, and direct-burial wire laid where expanding clay won’t pull connections apart.',
          '<strong>HOAs:</strong> warm, shielded light that stays on your property, which is what most deed restrictions and neighbors care about.',
        ]) ?>
      </div>
      <div>
<?php section_head('Long season', 'Designed for Nine-Plus Months Outdoors', '', 'left'); ?>
        <p class="reveal">Because Texans use their patios for most of the year, we set lighting up in zones on a smart transformer or astronomical timer. Patio strings and downlights can come on at dusk and dim at 10pm, while path and step lights stay on later for safety.</p>
        <p class="reveal">Mosquito season matters too. Warm LEDs at 2200K–2700K are generally less attractive to many night-flying insects than cool white light, which is one more reason we keep patio color temperatures low.</p>
        <ul class="pill-list reveal">
          <li>Covered patios</li><li>Pergolas & arbors</li><li>Outdoor kitchens</li><li>Decks & stairs</li><li>Fire pits</li><li>Courtyards</li><li>Pool decks</li><li>Porches</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
<?php section_head('How it works', 'Our Four-Step Patio Lighting Process', 'The same process we use on every project, tuned for spaces where people sit, cook and gather.'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>We visit as the sun sets, sit where you sit and look at where light is missing, where glare would bother you and where power and transformers can go. No pressure, just a walk-through.</p></li>
      <li><h3>Custom design</h3><p>You receive a lighting plan with fixture locations, zones, color temperatures and an itemized quote. Patio-focused projects often land within our starter range of roughly $2,500–$5,000; larger outdoor living spaces combined with landscape lighting run higher.</p></li>
      <li><h3>Expert installation</h3><p>Licensed, insured technicians mount fixtures cleanly on beams and walls, run 12- or 10-gauge cable in hub layouts to keep voltage even and conceal wiring wherever it can be hidden.</p></li>
      <li><h3>Reveal & tune</h3><p>We return after dark to adjust aim, dimming levels and timer settings with you, so the patio looks right from the chair, the kitchen and the house.</p></li>
    </ol>
    <?= tool_promo('/tools/lighting-design-simulator/') ?>
    <p class="reveal">Want a ballpark first? Our <a href="/landscape-lighting-cost-calculator/">landscape lighting cost calculator</a> estimates fixtures, installation and running cost. Many homeowners pair patio lighting with <a href="/services/pool-water-feature-lighting/">pool and water feature lighting</a> or <a href="/services/smart-lighting-systems/">smart controls</a> to light the whole backyard as one design.</p>
  </div>
</section>

<?php faqs([
  ['How bright should patio lighting be?', 'Brighter than most people expect at the grill and dimmer than most people expect everywhere else. We typically aim for soft, low-level light at seating, focused light on the table and a separate, brighter task zone in the outdoor kitchen. Dimmable zones let you adjust on the night rather than guessing at install.'],
  ['Can you install string lights without posts?', 'Often, yes. Strings can run from the eave to a pergola, between trees using protective straps, or across a courtyard on tensioned steel cable. Where there is nothing to attach to, we install sturdy posts set in concrete. Open spans in Texas need cable support to survive storms and wind.'],
  ['Will patio lighting attract bugs?', 'All light attracts some insects, but warm color temperatures (2200K–2700K) tend to draw fewer than cool white light. Keeping fixtures shielded and aiming light down at surfaces, rather than out into the yard, helps further.'],
  ['Can patio lighting run on the same system as my landscape lights?', 'Yes. We usually put patio, step and landscape fixtures on one low-voltage system with separate zones, so the patio can dim or switch off independently. If you have an existing system, we can evaluate its transformer capacity and add to it. Our <a href="/services/landscape-lighting-maintenance/">maintenance and repair team</a> services any brand.'],
  ['How long does a patio lighting installation take?', 'Most residential projects are completed in one day. Larger outdoor living spaces or projects combined with full landscape lighting may take two to three days.'],
]); ?>

<section class="section alt">
  <div class="container">
<?php section_head('Keep exploring', 'Explore Other Services', 'Patio lighting works best as part of a whole-property plan.'); ?>
<?php service_cards('patio-outdoor-living-lighting', 3); ?>
  </div>
</section>

<?php cta_band('Make Your Patio the Best Room in the House', 'Book a free dusk consultation with Landscape Lighting Texas. We’ll sit where you sit, show you what’s possible and send a clear, itemized quote.'); ?>
