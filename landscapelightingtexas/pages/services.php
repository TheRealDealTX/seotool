<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Design · Installation · Care';
$P['lead'] = 'Landscape lighting services in Texas built around one idea: light the things worth seeing, and hide the fixtures doing the work. From a single lit live oak to a fully zoned estate, every Landscape Lighting Texas system is designed at dusk, installed on professional low-voltage LED hardware and backed by a 5-year workmanship warranty.';
?>
<section class="section">
  <div class="container">
    <?php section_head('What we do', 'Eight Services, <span class="highlight">One Lighting Plan</span>', 'Most properties need more than one kind of light. A facade looks best with a lit tree beside it; a pool feels safer with the path to it lit. We design all of it as one system on shared transformers and controls, so it works together and grows with you.'); ?>
    <?php service_cards(); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('How we design', 'Lighting Design That Starts <span class="highlight">After Sunset</span>', 'Daylight tells you very little about how a property will look at night. That is why our process starts at dusk, on your lawn, with fixtures in hand.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('moon') ?></span><h3>Layers, not floodlight</h3><p>Good landscape lighting is built in layers: accent light on focal points (a facade, a specimen tree), ambient light that gives the yard depth, and task light on paths and steps. Balancing the three is what makes a property look composed rather than simply bright.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('beam') ?></span><h3>The right beam for each target</h3><p>A narrow 15–25° spot reaches up a tall column or a palm trunk; a 36–60° flood washes a wide stone wall or a crape myrtle canopy. We pick beam angles and output per object, not one fixture for everything, and add glare shields where a lamp could catch an eye.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('sun') ?></span><h3>Warm, consistent color</h3><p>Most Texas homes look their best at 2700K, which flatters brick, limestone and stucco. Foliage sometimes gets 3000K for crisper greens. Whatever we choose, we keep it consistent across the property so the whole scene reads as one.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('bolt') ?></span><h3>Engineered wiring</h3><p>Systems run on 12V low-voltage power from multi-tap transformers, with 12- or 10-gauge direct-burial cable laid out in hub runs so every fixture sees even voltage. That is how you avoid the dim-at-the-end problem common in DIY kits.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('shield') ?></span><h3>Built for Texas weather</h3><p>Solid brass and copper bodies that will not rust, sealed fittings rated for wet locations, and LEDs that tolerate a Texas summer. Fixtures go into caliche and clay with proper stakes or mounts so they stay aimed through storms.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('smart') ?></span><h3>Controls that think for you</h3><p>Astronomical timers follow sunset through the year, zones let the pool area run late while the facade turns off at midnight, and optional app control adds dimming and scenes. See <a href="/services/smart-lighting-systems/">smart lighting systems</a>.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('Find your fit', 'What Each Landscape Lighting Service Solves', 'Not sure where to start? Match the problem you notice at night with the service built to fix it.'); ?>
    <div class="table-wrap reveal">
      <table>
        <thead><tr><th>Service</th><th>Solves</th><th>Typical fixtures</th><th>Best for</th></tr></thead>
        <tbody>
          <tr><td><a href="/services/architectural-uplighting/">Architectural Uplighting</a></td><td>A house that disappears after dark; flat, unflattering porch light</td><td>Wall-wash and spot uplights, in-grade wells</td><td>Stone, brick and stucco facades, columns, entries</td></tr>
          <tr><td><a href="/services/garden-tree-lighting/">Garden &amp; Tree Lighting</a></td><td>A yard that ends at the patio; no depth or focal points</td><td>Adjustable uplights, downlights in trees, bed lights</td><td>Live oaks, crape myrtles, palms, planting beds</td></tr>
          <tr><td><a href="/services/pathway-driveway-lighting/">Pathway &amp; Driveway Lighting</a></td><td>Trip hazards, unclear routes, hard-to-find entries</td><td>Path lights, bollards, in-grade and step lights</td><td>Front walks, long driveways, garden paths, steps</td></tr>
          <tr><td><a href="/services/pool-water-feature-lighting/">Pool &amp; Water Feature Lighting</a></td><td>A dark backyard that only works in daylight</td><td>Submersible fixtures, deck and wall lights, accents</td><td>Pools, fountains, ponds, waterfalls</td></tr>
          <tr><td><a href="/services/patio-outdoor-living-lighting/">Patio &amp; Outdoor Living</a></td><td>Outdoor rooms that are too dark or too harsh to enjoy</td><td>String lights, downlights, step and under-cap lights</td><td>Pergolas, porches, outdoor kitchens, decks</td></tr>
          <tr><td><a href="/services/smart-lighting-systems/">Smart Lighting Systems</a></td><td>Timers that drift, all-or-nothing switching</td><td>Smart transformers, zone controllers, app control</td><td>Any new or existing system</td></tr>
          <tr><td><a href="/services/security-lighting/">Security &amp; Floodlighting</a></td><td>Dark corners and side yards; glaring floodlights</td><td>Shielded floods, motion zones, eave downlights</td><td>Side yards, gates, garages, commercial sites</td></tr>
          <tr><td><a href="/services/landscape-lighting-maintenance/">Maintenance &amp; Repair</a></td><td>Dead fixtures, failing transformers, old halogen</td><td>LED retrofits, new wire, re-aiming</td><td>Any brand of existing system</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Packages', 'Three Ways to Light a Texas Property', 'These are <strong>planning ranges</strong> to help you budget, not quotes. Your real number depends on fixture count, wire runs, materials and controls, and it comes as an itemized quote after a free dusk consultation.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card">
        <span class="info-icon"><?= icon('bulb') ?></span>
        <h3>Starter</h3>
        <p><span class="highlight">Planning range: $2,500–$5,000</span></p>
        <p>The front of the house, done properly. Ideal for a first system or a smaller lot.</p>
        <?= checklist([
            'About 8–15 fixtures',
            'Facade uplighting on key features',
            'One feature tree or bed',
            'Front walk path lighting',
            'Transformer with astronomical timer',
        ]) ?>
      </div>
      <div class="info-card reveal glow-card">
        <span class="info-icon"><?= icon('spark') ?></span>
        <h3>Signature</h3>
        <p><span class="highlight">Planning range: $5,000–$12,000</span></p>
        <p>Front and back yard as one design. The range most Texas homes fall into.</p>
        <?= checklist([
            'About 15–35 fixtures',
            'Full facade and entry lighting',
            'Multiple trees, beds and hardscape',
            'Driveway, path or step lighting',
            'Patio or pool-area accents',
            'Two or more zones with timer or app control',
        ]) ?>
      </div>
      <div class="info-card reveal glow-card">
        <span class="info-icon"><?= icon('award') ?></span>
        <h3>Estate</h3>
        <p><span class="highlight">Planning range: $12,000–$20,000+</span></p>
        <p>Large lots, long drives and complete outdoor living areas, lit as one composed scene.</p>
        <?= checklist([
            '35+ fixtures across the property',
            'Moonlighting in mature trees',
            'Pool, water feature and outdoor kitchen',
            'Long driveway and perimeter lighting',
            'Multiple transformers, smart zones and scenes',
        ]) ?>
      </div>
    </div>
    <p class="reveal" style="text-align:center;margin-top:2rem">As a rule of thumb, professionally installed fixtures run roughly $250–$450 each. Try the <a href="/landscape-lighting-cost-calculator/">cost calculator</a> for a fixture-by-fixture estimate, or read about <a href="/led-vs-halogen-landscape-lighting/">LED vs halogen running costs</a>.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Every project includes', 'What You Get From Landscape Lighting Texas', '', 'left'); ?>
        <?= checklist([
            'A free dusk consultation at your property',
            'A written lighting plan with fixture locations, beam angles and color temperature',
            'Transparent, itemized pricing with no surprises',
            'Licensed and insured Texas installers',
            'Night-time aiming and tuning with you on site',
            'A 5-year workmanship warranty',
        ]) ?>
      </div>
      <div class="reveal">
        <?php section_head('Where we work', 'Statewide Service', 'We design and install across Texas, from Hill Country limestone to Gulf Coast salt air.', 'left'); ?>
        <ul class="pill-list">
          <li><a href="/areas/austin/">Austin</a></li>
          <li><a href="/areas/houston/">Houston</a></li>
          <li><a href="/areas/dallas-fort-worth/">Dallas–Fort Worth</a></li>
          <li><a href="/areas/san-antonio/">San Antonio</a></li>
          <li><a href="/areas/west-texas/">West Texas</a></li>
          <li><a href="/areas/gulf-coast/">Gulf Coast</a></li>
        </ul>
        <p style="margin-top:1rem">Want to explore ideas first? Try the <a href="/tools/lighting-design-simulator/">lighting design simulator</a> or the <a href="/tools/lighting-style-quiz/">lighting style quiz</a>.</p>
      </div>
    </div>
  </div>
</section>

<?php faqs([
    ['Which landscape lighting service should I start with?', 'Most homeowners start with the front of the house: facade uplighting, one feature tree and the front walk. It gives the biggest change in curb appeal for the budget, and a well-sized transformer leaves room to add the backyard later.'],
    ['Can you combine several services in one project?', 'Yes, and we recommend it. Designing the facade, trees, paths and pool together lets us share transformers and wire runs, keep color temperature consistent and set up zones so each area can run on its own schedule.'],
    ['Are the package prices fixed?', 'No. Starter, Signature and Estate are planning ranges to help you budget. Your quote is itemized after a free dusk consultation and depends on fixture count, wire distances, fixture materials and controls.'],
    ['Do you work on systems another company installed?', 'Yes. Our <a href="/services/landscape-lighting-maintenance/">maintenance and repair service</a> covers any brand: troubleshooting, re-aiming, transformer and wire repair, and LED retrofits of older halogen systems.'],
]); ?>

<?php cta_band(); ?>
