<?php defined('LLT') or die(http_response_code(404));
global $AREAS;
$P['eyebrow'] = 'South Central Texas · Alamo City';
$P['lead'] = 'San Antonio landscape lighting for historic homes, Spanish and Mediterranean architecture, Hill Country estates and the patios where the city spends its evenings.';
$P['_cities'] = $AREAS['san-antonio'][2];
?>
<section class="section">
  <div class="container">
    <?php split('patio-lighting', 'Patio and outdoor living lighting at night on a South Texas home', '
      <p class="eyebrow">Lighting the Alamo City</p>
      <h2 class="section-title">San Antonio Landscape Lighting With Character</h2>
      <p class="lead-p">San Antonio has some of the most distinctive residential architecture in Texas: Victorian and revival homes in King William, stately houses in Alamo Heights and Monte Vista, Spanish and Mediterranean styles with stucco and tile roofs, and limestone ranch homes heading into the Hill Country. Thoughtful San Antonio landscape lighting respects that character.</p>
      <p>Landscape Lighting Texas designs low-voltage LED systems that highlight what makes each home special: arches, courtyards, porches, old trees and the patios where families gather once the heat breaks. Every plan begins with a free walk of your property at dusk.</p>
      <p>From there, we build a layered design that feels warm, balanced and at home in its neighborhood.</p>
      <p><a class="link-arrow" href="/quote/">Book a free dusk consultation ' . icon('arrow', 16) . '</a></p>
    '); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('What We Light', 'What We Light in San Antonio', 'South Central Texas homes are built around shade and outdoor gathering. These are the features we light most often.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('home') ?></span><h3>Historic &amp; Spanish-style facades</h3><p>Soft washes on stucco, grazed limestone, and lit arches, columns and porches, scaled so older homes look graceful rather than floodlit. See <a href="/services/architectural-uplighting/">architectural uplighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('patio') ?></span><h3>Patios, courtyards &amp; pergolas</h3><p>Downlights, wall lights and dimmable strings for courtyards and covered patios built for long evenings. See <a href="/services/patio-outdoor-living-lighting/">patio and outdoor living lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('tree') ?></span><h3>Live oaks &amp; pecans</h3><p>Mature live oaks and pecans get layered uplighting and moonlighting that shows their structure. See <a href="/services/garden-tree-lighting/">tree and garden lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('water') ?></span><h3>Pools &amp; fountains</h3><p>Pool surrounds, tiled fountains and courtyard water features lit for reflection and calm. See <a href="/services/pool-water-feature-lighting/">pool and water feature lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>Walkways &amp; long drives</h3><p>Path lights and low bollards for front walks in the city and long, dark drives on Hill Country acreage. See <a href="/services/pathway-driveway-lighting/">pathway and driveway lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('wrench') ?></span><h3>Upgrades &amp; retrofits</h3><p>Older halogen systems converted to LED, repaired and re-aimed, often on homes that already have good bones. See <a href="/services/landscape-lighting-maintenance/">maintenance and repair</a>.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Local Design', 'Designing Landscape Lighting for San Antonio Homes', '', 'left'); ?>
        <p>Historic and character homes reward restraint. Too much light washes out detail and makes old materials look flat, while a few well-placed fixtures make a porch or arch glow. We favor warm color, concealed fixtures and lower output on older facades, and we keep equipment discreet so it does not distract from the architecture in daylight.</p>
        <p>Heading north and west into Boerne, Helotes and Fair Oaks Ranch, the challenges change: rocky limestone ground, bigger lots, native oaks and darker skies. There we plan longer wire runs, use shielded fixtures and keep the view out from the porch dark.</p>
      </div>
      <div class="reveal">
        <?= checklist([
            'Warm 2700K light (or 2400K on older stone and stucco) to bring out natural tones',
            'Low-profile fixtures concealed in beds so they disappear by day',
            'Soft, even washes on stucco walls to avoid scalloped hot spots',
            'Solid brass and copper fixtures that weather well in South Texas heat',
            'Careful wire routing through rocky Hill Country soil and around oak roots',
            'Shielded, downward-aimed light on rural and Hill Country properties',
            'Smart zones so patio scenes, security lighting and late-night levels can run separately',
        ]) ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Communities Served', 'San Antonio Area Communities We Serve', 'From historic neighborhoods inside Loop 410 to the Hill Country and the I-35 corridor. Do not see yours? <a href="/quote/">Ask us</a>; nearby areas are usually within reach.'); ?>
    <ul class="pill-list reveal">
      <?php foreach (['San Antonio', 'King William', 'Alamo Heights', 'Olmos Park', 'Terrell Hills', 'Monte Vista', 'Stone Oak', 'The Dominion', 'Shavano Park', 'Helotes', 'Leon Valley', 'Fair Oaks Ranch', 'Boerne', 'Bulverde', 'Timberwood Park', 'New Braunfels', 'Schertz', 'Cibolo', 'Universal City', 'Seguin'] as $c) echo '<li>' . e($c) . '</li>'; ?>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('Featured Look', 'An Evening Patio, Lit for Lingering', 'Drag the slider to compare. Dimmable overhead light, glowing plantings and softly lit steps turn a patio into a room you will use well into the night.'); ?>
    <?php before_after('patio-lighting', 'Patio lighting at night, installed by Landscape Lighting Texas'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
    <?php section_head('Our Process', 'How a San Antonio Lighting Project Works'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>A designer visits around sunset to walk the property, study the architecture as daylight fades and talk through how you entertain outdoors.</p></li>
      <li><h3>Custom design</h3><p>You receive a plan and itemized quote with fixtures, beam angles, color temperature, transformer size and zones. Typical residential projects fall in a planning range of $2,500–$12,000.</p></li>
      <li><h3>Expert installation</h3><p>Our crew installs fixtures, cable and the transformer with care around old plantings, stonework and irrigation.</p></li>
      <li><h3>Reveal &amp; tune</h3><p>We return after dark to aim and balance each light, set your timer and walk you through the controls. Work is backed by our 5-year workmanship warranty.</p></li>
    </ol>
    <div class="reveal" style="margin-top:2rem"><?= tool_promo('/tools/color-temperature-visualizer/') ?></div>
  </div>
</section>

<?php faqs([
    ['Can you light a historic home without changing its character?', 'Yes. We use small, concealed fixtures, warm color and modest output, and we place equipment in beds and behind plants rather than mounting it on historic surfaces. If your home is in a historic district, we can provide fixture details for any review your neighborhood requires.'],
    ['What color temperature suits stucco and limestone?', 'Warm light works best. We usually recommend 2700K, or 2400K on older cream limestone and earthy stucco, to bring out warm tones. Cooler light can make these materials look gray. Try our <a href="/tools/color-temperature-visualizer/">color temperature visualizer</a> or read the <a href="/landscape-lighting-color-temperature-guide/">color temperature guide</a>.'],
    ['Do you work on Hill Country acreage around Boerne and Helotes?', 'Yes. Larger rural lots usually need longer wire runs, heavier cable and careful transformer placement to avoid voltage drop. We also use shielded fixtures to keep the night sky dark, which most Hill Country homeowners value.'],
    ['How much does San Antonio landscape lighting cost?', 'Most residential projects fall in a planning range of $2,500–$12,000, with starter systems around $2,500–$5,000 and estates sometimes exceeding $20,000. Use our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> for a ballpark before your free consultation.'],
]); ?>

<section class="section">
  <div class="container">
    <?php section_head('Statewide', 'Other Areas We Serve', 'Landscape Lighting Texas designs and installs outdoor lighting across the state. <a href="/areas/">See every service area</a>.'); ?>
    <?php area_cards('san-antonio'); ?>
  </div>
</section>

<?php cta_band('Ready to Light Your San Antonio Home?', 'Book a free dusk consultation. A designer will walk your property at nightfall, show you what is possible and send a clear, itemized quote.'); ?>
