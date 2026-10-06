<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'App Control, Zones & Scenes';
$P['lead'] = 'Smart landscape lighting puts every zone of your outdoor lighting on your phone: schedules that follow the Texas sunset, dimming, scenes for parties or quiet nights, and integration with the smart home you already have.';
?>
<section class="section">
  <div class="container">
<?php split('garden-pathway-lighting', 'Garden pathway lit by a smart, zoned low-voltage landscape lighting system at night', <<<'HTML'
<p class="eyebrow reveal">Control, not complexity</p>
<h2 class="section-title reveal">What a Smart Landscape Lighting System Actually Does</h2>
<p class="lead-p reveal">A smart landscape lighting system replaces the old plug-in timer and single on/off switch with zones you can schedule, dim and combine into scenes from an app, a wall keypad or your voice assistant. The fixtures stay low-voltage LED; what changes is how intelligently they are run.</p>
<p class="reveal">The practical benefits are simple. Lights come on at dusk year-round without anyone resetting a timer after daylight saving time. The patio can dim at 10pm while the driveway stays on. Uplights on the facade can switch off at midnight while path lights stay on until sunrise. Landscape Lighting Texas designs the zones first and picks the control platform second, so the system fits how you live rather than how a gadget works.</p>
HTML); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
<?php section_head('Features', 'Smart Lighting Features Worth Paying For', 'Not every smart feature earns its place. These are the ones Texas homeowners use every week.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('clock') ?></span><h3>Astronomical timers</h3><p>The controller calculates sunset for your exact location every day, so lights come on at dusk in December and in July without manual adjustment. Offsets let you start a few minutes before or after.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('sliders') ?></span><h3>Zoning</h3><p>Front facade, trees, paths, patio, pool and security lights each get their own zone with its own schedule. Zoning is the foundation of every other smart feature.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('bulb') ?></span><h3>Dimming</h3><p>Dimmable zones or fixture-level dimming let us balance the property after install and let you soften the scene later in the evening, which also reduces energy use.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('spark') ?></span><h3>Scenes</h3><p>“Arrive home,” “Entertaining,” “Late night” and “Away” each set multiple zones at once. One tap changes the whole property.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('sun') ?></span><h3>Tunable white & color</h3><p>Selected fixtures can shift color temperature or, where it suits the design, produce color for holidays and game days, then go back to warm white the next night.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('smart') ?></span><h3>Smart home integration</h3><p>Depending on the platform, lighting can work with popular voice assistants and home automation systems, so a single “goodnight” turns off the patio and arms the security scene.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
<?php section_head('Compare', 'Timer, Smart Transformer or Fixture-Level Control?', 'There are three common ways to control landscape lighting. The best one depends on the size of the property and how much flexibility you want.', 'left'); ?>
    <div class="table-wrap reveal">
      <table>
        <thead><tr><th></th><th>Basic timer / photocell</th><th>Smart transformer (zone control)</th><th>Fixture-level smart control</th></tr></thead>
        <tbody>
          <tr><td>Follows sunset automatically</td><td>Photocell only; timers drift</td><td>Yes, astronomical</td><td>Yes, astronomical</td></tr>
          <tr><td>Independent zones</td><td>No</td><td>Yes, by circuit</td><td>Yes, down to each fixture</td></tr>
          <tr><td>Dimming</td><td>No</td><td>Often, by zone</td><td>Yes, per fixture</td></tr>
          <tr><td>Scenes & app control</td><td>No</td><td>Yes</td><td>Yes</td></tr>
          <tr><td>Color / tunable white</td><td>No</td><td>Limited</td><td>Yes, with compatible fixtures</td></tr>
          <tr><td>Best fit</td><td>Small, simple systems</td><td>Most homes</td><td>Estates, pools, design-forward projects</td></tr>
        </tbody>
      </table>
    </div>
    <p class="reveal">Most of our residential clients are well served by zone control on a smart transformer. Fixture-level control makes sense when you want individual trees, color effects or very fine balancing across a large property.</p>
    <p class="reveal">Whatever the platform, a smart system is only as good as the wiring underneath it. We size transformers with headroom, run 12- or 10-gauge cable in hub layouts to keep voltage even across each zone, and use multi-tap transformers so long runs still get the right voltage. That is what keeps dimmed fixtures matching one another and prevents the flicker that cheaper smart kits are known for. Our <a href="/tools/transformer-calculator/">transformer and voltage drop calculator</a> shows the math.</p>
  </div>
</section>

<section class="section alt">
  <div class="container">
<?php section_head('Scenes in action', 'Before and After: Smart Landscape Lighting Scenes', 'Drag to compare. With zoning and dimming, the same fixtures can deliver a bright welcome at 7pm and a soft, low-glow scene at midnight.'); ?>
<?php before_after('garden-pathway-lighting', 'Garden path shown unlit and then lit by a smart landscape lighting scene'); ?>
    <?= tool_promo('/tools/lighting-design-simulator/') ?>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div>
<?php section_head('Texas conditions', 'Smart Lighting Systems Built for Texas', '', 'left'); ?>
        <p class="reveal">Smart controls add electronics to an outdoor system, so placement and protection matter more here than in milder climates.</p>
        <?= checklist([
          '<strong>Heat:</strong> transformers and controllers mounted out of direct west sun where possible, in enclosures rated for outdoor use.',
          '<strong>Storms and power blips:</strong> systems that keep their schedule after an outage and surge protection on the line side.',
          '<strong>Wi-Fi reach:</strong> we check signal at the transformer location during the consultation and plan for an extender or wired bridge when needed.',
          '<strong>Humidity:</strong> sealed, gel-filled or heat-shrink connections at every splice, because a smart system is only as reliable as its wiring.',
          '<strong>Long season:</strong> different schedules for summer patio nights and winter early dusk, set once and handled automatically.',
        ]) ?>
      </div>
      <div>
<?php section_head('HOA-friendly', 'Smarter Lighting Is Better Neighbor Lighting', '', 'left'); ?>
        <p class="reveal">Many Texas HOAs restrict light trespass and late-night brightness. Smart schedules make compliance easy: uplights off or dimmed at a set hour, warm color temperatures by default and path or security zones kept low and shielded. It also reflects good dark-sky practice, which matters in places like the Hill Country around <a href="/areas/austin/">Austin</a>.</p>
        <p class="reveal">Running fewer fixtures for fewer hours saves energy, too. A whole-property LED system typically costs about $10–$25 a month to run; smart dimming and schedules can bring that lower. Compare scenarios with our <a href="/tools/energy-savings-calculator/">LED energy savings calculator</a>.</p>
        <ul class="pill-list reveal"><li>Facade</li><li>Trees</li><li>Paths</li><li>Driveway</li><li>Patio</li><li>Pool</li><li>Security</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
<?php section_head('How it works', 'From Consultation to First Scene', 'Our four-step process, with controls planned in from day one.'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>We walk the property at nightfall, talk through how you want to use the lighting and check where transformers, Wi-Fi and existing wiring are.</p></li>
      <li><h3>Custom design</h3><p>Your plan shows every fixture, the zone it belongs to and the control platform we recommend, with an itemized quote. Upgrading an existing system to smart control is quoted separately so you can compare.</p></li>
      <li><h3>Expert installation</h3><p>Licensed technicians install fixtures, transformers and controllers, wire each zone on its own run and connect the system to your network and app.</p></li>
      <li><h3>Reveal & tune</h3><p>After dark we set dimming levels, build your scenes and schedules with you and show you how to change them. You leave with a system you can actually operate.</p></li>
    </ol>
    <p class="reveal">Planning a schedule? The <a href="/tools/dusk-timer/">Texas dusk timer</a> shows sunset times by city and month. For wiring basics, see our <a href="/low-voltage-landscape-lighting-guide/">low-voltage landscape lighting guide</a>.</p>
  </div>
</section>

<?php faqs([
  ['Can you make my existing landscape lighting smart?', 'Usually, yes. In many cases we can replace the transformer or add a smart controller and split existing runs into zones. If the system still uses halogen lamps, we often recommend an LED retrofit at the same time; our <a href="/services/landscape-lighting-maintenance/">maintenance and repair team</a> works on any brand.'],
  ['Do I need Wi-Fi for smart landscape lighting?', 'For app and voice control, yes, or a hub that connects to your network. Astronomical schedules typically keep running on the controller itself if your internet goes down, so lights still come on at dusk.'],
  ['Will smart lighting work with my smart home system?', 'Compatibility depends on the control platform. We confirm which assistants and automation systems you use during the consultation and recommend a platform that works with them.'],
  ['Are color-changing landscape lights a good idea?', 'Used sparingly, yes. We design around warm white for everyday use and add color capability to select fixtures for holidays or events. Full-time color tends to look less natural on stone, brick and trees.'],
  ['How much does a smart lighting system cost?', 'It depends on the size of the system and the level of control. As a planning range, most residential landscape lighting projects run $2,500–$12,000, and smart control is one line in that itemized quote. Our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> gives a quick estimate.'],
]); ?>

<section class="section alt">
  <div class="container">
<?php section_head('Keep exploring', 'Explore Other Services', 'Smart control ties every part of your lighting together.'); ?>
<?php service_cards('smart-lighting-systems', 3); ?>
  </div>
</section>

<?php cta_band('Put Your Whole Property on One App', 'Book a free dusk consultation with Landscape Lighting Texas and we’ll show you how zones, schedules and scenes can work on your property.'); ?>
