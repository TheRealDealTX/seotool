<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Paths, Drives & Steps';
$P['lead'] = 'Pathway and driveway lighting in Texas that guides guests from the curb to the door: soft, even pools of light from path lights, bollards and in-grade fixtures, spaced for safety and designed to stay out of everyone\'s eyes.';
?>
<section class="section">
  <div class="container">
    <?php split('driveway-lighting', 'Driveway lined with low bollard lights leading to a Texas home at night', '
      <p class="eyebrow">Why it matters</p>
      <h2>Pathway and Driveway Lighting in Texas</h2>
      <p class="lead-p">Pathway and driveway lighting is the most practical light on a property: it shows where to walk, where the edges are and where the steps begin.</p>
      <p>It is also the easiest to get wrong. Too many fixtures in a straight line turns a front walk into a runway. Bright, unshielded lamps blind people at eye level so they see less, not more. Fixtures placed at the edge of a driveway get clipped by tires and mowers.</p>
      <p>Landscape Lighting Texas designs paths and drives as part of the whole scene: overlapping pools of light at walking level, staggered so they follow the curve of the path, with surrounding beds and trees lit softly so the walk feels open rather than tunnel-like.</p>
    ', false); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Techniques', 'How We Light Paths, Drives and Steps', 'The goal is visible footing and a clear route, with fixtures that look good by day and nearly disappear at night.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>Staggered path lights</h3><p>Shielded path lights placed alternately on each side of a walk, typically 6–10 feet apart, so pools of light overlap softly. Staggering avoids the runway look and follows curves naturally.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('beam') ?></span><h3>Driveway bollards</h3><p>Low bollards or path lights set back from the edge mark the drive's borders and entry. On long rural drives we light the entrance, curves and the arrival court rather than every few feet.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('spark') ?></span><h3>In-grade &amp; flush lights</h3><p>Drive-over rated fixtures set flush into pavers or concrete where a raised fixture would be hit. Useful for gate columns, narrow drives and the edges of motor courts.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('home') ?></span><h3>Step &amp; riser lights</h3><p>Small louvered fixtures set into risers or retaining walls light each tread. Steps are where most nighttime trips happen, so they get priority in every design.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('moon') ?></span><h3>Moonlighting from above</h3><p>Where a walk passes under a large tree, a downlight high in the canopy can light the path with dappled leaf shadows and no fixtures at ground level at all.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('leaf') ?></span><h3>Bed-edge lighting</h3><p>Lighting the planting along a path widens the lit area and gives the walk context, so you see the garden on the way in, not just the pavement.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    <?php section_head('See the difference', 'Curb to Front Door, Before and After', 'Drag the slider to compare the approach with and without driveway lighting.'); ?>
    <?php before_after('driveway-lighting', 'Before and after driveway and pathway lighting at a Texas home'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Specifications', 'Typical Path &amp; Driveway Fixtures', 'Low outputs are deliberate: at walking level, less light with good shielding looks better and works better than bright, glaring fixtures.'); ?>
    <div class="table-wrap reveal">
      <table>
        <thead><tr><th>Fixture</th><th>Typical output</th><th>Beam / spread</th><th>Color temp</th><th>Materials &amp; notes</th></tr></thead>
        <tbody>
          <tr><td>Path light (18–24 in tall)</td><td>80–200 lm</td><td>Downward, 6–10 ft pool</td><td>2700K</td><td>Brass or copper with hat shield; lamp hidden from view</td></tr>
          <tr><td>Bollard</td><td>150–300 lm</td><td>Downward or 360°</td><td>2700–3000K</td><td>Brass, copper or powder-coated; set back from the drive edge</td></tr>
          <tr><td>In-grade / drive-over light</td><td>100–300 lm</td><td>Flush, 25–60°</td><td>2700K</td><td>Drive-over rated, sealed for wet locations, drainage base</td></tr>
          <tr><td>Step / riser light</td><td>40–120 lm</td><td>Louvered, downward</td><td>2700K</td><td>Brass faceplate, recessed into stone or block</td></tr>
          <tr><td>Wall / hardscape light</td><td>60–150 lm</td><td>Downward wash</td><td>2700K</td><td>Mounted under wall caps or in retaining walls</td></tr>
          <tr><td>Power on long runs</td><td colspan="4">12V multi-tap transformer, 10-gauge cable or split runs on long drives to control voltage drop. Run the numbers with the <a href="/tools/transformer-calculator/">transformer &amp; voltage drop calculator</a>.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Texas considerations', 'Driveway Lighting for Texas Properties', '', 'left'); ?>
        <?= checklist([
            '<strong>Long drives:</strong> Hill Country and acreage properties can have drives hundreds of feet long. Heavier wire, multiple runs or a second transformer keep the last fixture as bright as the first.',
            '<strong>Clay and caliche:</strong> path lights are set on long, sturdy stakes or concrete footings so they stay plumb as soil shrinks and swells.',
            '<strong>Mowers, trimmers and tires:</strong> fixtures sit far enough inside beds to avoid damage, and solid brass shrugs off knocks that bend aluminum.',
            '<strong>Limestone and flagstone walks:</strong> step lights can be set into stone risers and retaining walls for a clean, built-in look.',
            '<strong>Coastal salt:</strong> on the Gulf Coast we specify brass, copper and stainless hardware throughout.',
        ]) ?>
      </div>
      <div class="reveal">
        <?php section_head('Glare &amp; neighbors', 'Light the Ground, Not the Eyes', '', 'left'); ?>
        <p>Path and drive lights sit right at eye level for anyone walking or driving past, so glare control matters more here than anywhere else. We use hat-style shields that hide the LED, keep outputs modest and aim light down onto the walking surface.</p>
        <p>The result is friendlier to neighbors and HOA rules, and better for dark-sky communities around the Hill Country. It also makes the house safer: your eyes adapt to a softly lit path far better than to a few bright points.</p>
        <ul class="pill-list"><li>Shielded optics</li><li>Staggered spacing</li><li>Warm 2700K</li><li>Dusk-to-late timers</li></ul>
        <p>Want the path lights on at dusk every night, year-round? Check your city's sunset times by month.</p>
        <?= tool_promo('/tools/dusk-timer/') ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
    <?php section_head('Our process', 'How a Path &amp; Driveway Project Works'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>We walk the route from the street and the driveway to the door as it gets dark, note steps, edges and level changes, and talk through how you and your guests arrive.</p></li>
      <li><h3>Custom design</h3><p>You get a layout showing fixture spacing, styles and wire runs, with an itemized quote. Paths often share a transformer with <a href="/services/architectural-uplighting/">facade uplighting</a> and <a href="/services/garden-tree-lighting/">tree lighting</a>.</p></li>
      <li><h3>Expert installation</h3><p>Licensed, insured installers trench narrow cable runs, bore under walks where needed, and set fixtures plumb and secure. Most front-walk projects finish in a day.</p></li>
      <li><h3>Reveal &amp; tune</h3><p>After dark we walk the route with you, adjust heights and outputs, and set timers. Work is covered by our 5-year workmanship warranty.</p></li>
    </ol>
  </div>
</section>

<?php faqs([
    ['How far apart should path lights be?', 'Typically 6–10 feet, staggered on alternating sides of the walk so the pools of light overlap slightly. The exact spacing depends on fixture height, output and how wide the walk is.'],
    ['Can you put lights in an existing concrete driveway?', 'Yes. We can core-drill for drive-over in-grade fixtures, and bore under existing walks and drives to run cable without cutting the slab.'],
    ['Will path lights be too bright for my neighbors or HOA?', 'Not with shielded fixtures at modest output. Path lights are usually 80–200 lumens with the light directed down onto the walk. If your HOA requires approval, we provide a plan for submission.'],
    ['How do you keep long driveways evenly lit?', 'By managing voltage drop: heavier 10-gauge cable, splitting the load into several runs, using multi-tap transformer settings and, on very long drives, a second transformer. Every fixture is checked with a meter during installation.'],
    ['Are solar path lights a good alternative?', 'Solar lights are inexpensive but usually dim, short-lived and inconsistent after cloudy days. A professional low-voltage LED system gives reliable, adjustable light every night. See our <a href="/low-voltage-landscape-lighting-guide/">low-voltage lighting guide</a> for how these systems work.'],
]); ?>

<section class="section alt">
  <div class="container">
    <?php section_head('Keep exploring', 'Explore Other Services', 'Combine the approach with the house and garden for a full Landscape Lighting Texas design.'); ?>
    <?php service_cards('pathway-driveway-lighting', 3); ?>
  </div>
</section>

<?php cta_band('Ready to Light the Way Home?'); ?>
