<?php defined('LLT') or die(http_response_code(404));
global $AREAS;
$P['eyebrow'] = 'Southeast Texas · Greater Houston';
$P['lead'] = 'Houston landscape lighting built for humidity, downpours and lush yards, with pools, patios, live oaks and pines lit for long, warm evenings from Katy to Kingwood.';
$P['_cities'] = $AREAS['houston'][2];
?>
<section class="section">
  <div class="container">
    <?php split('pool-lighting', 'Pool and backyard landscape lighting at night in a Houston-area home', '
      <p class="eyebrow">Made for the Bayou City</p>
      <h2 class="section-title">Houston Landscape Lighting That Handles the Weather</h2>
      <p class="lead-p">Houston yards are green, shaded and used almost year-round. Good Houston landscape lighting makes the most of that: a pool that glows after sunset, live oaks and pines with real depth, a covered patio that stays comfortable long after dinner.</p>
      <p>It also has to survive the climate. Heavy humidity, sudden downpours, standing water and storm season are hard on cheap fixtures and sloppy wire connections. Landscape Lighting Texas designs every Houston system around those conditions, using sealed, professional-grade LED fixtures and connections that are made to stay dry.</p>
      <p>Every project starts with a free walk of your property at dusk, so the plan fits your yard rather than a catalog.</p>
      <p><a class="link-arrow" href="/quote/">Book a free dusk consultation ' . icon('arrow', 16) . '</a></p>
    '); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('What We Light', 'What We Light in Houston', 'Greater Houston homes are built for outdoor living. These are the spaces and features homeowners ask us to light most.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('water') ?></span><h3>Pools &amp; outdoor living</h3><p>Pool surrounds, cabanas and water features lit in layers so the backyard feels like a resort, not a stadium. See <a href="/services/pool-water-feature-lighting/">pool and water feature lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('tree') ?></span><h3>Live oaks, pines &amp; palms</h3><p>Wide oak canopies, tall loblolly pines in the northern suburbs and palms around the pool each need different beam angles and placement. See <a href="/services/garden-tree-lighting/">tree and garden lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('home') ?></span><h3>Brick &amp; stone facades</h3><p>Balanced uplighting for brick traditionals, stone-front new builds and modern homes, aimed to avoid hot spots on windows. See <a href="/services/architectural-uplighting/">architectural uplighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('patio') ?></span><h3>Covered patios &amp; kitchens</h3><p>Downlights, step lights and dimmable strings for the patios and outdoor kitchens Houstonians use most months of the year. See <a href="/services/patio-outdoor-living-lighting/">patio lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>Walks &amp; driveways</h3><p>Path lights and bollards that guide guests from the curb and help in the early dark of winter evenings. See <a href="/services/pathway-driveway-lighting/">pathway and driveway lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('shield') ?></span><h3>Security lighting</h3><p>Well-lit entries, side yards and garages that improve visibility without glaring into neighbors’ windows. See <a href="/services/security-lighting/">security lighting</a>.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Local Design', 'Designing Landscape Lighting for Houston’s Climate', '', 'left'); ?>
        <p>Water is the main enemy of outdoor lighting on the Gulf side of Texas. Moisture finds its way into weak wire splices, low spots hold standing water after a storm and humid air works on cheap aluminum housings. A system that looks fine on day one can start flickering within a season if those details are ignored.</p>
        <p>We plan around it from the start. Transformers are mounted above expected water levels, connections are sealed, and fixtures are chosen for wet locations. Lush planting also grows fast here, so we place fixtures where they can be maintained and expect to re-aim as beds fill in.</p>
      </div>
      <div class="reveal">
        <?= checklist([
            'Solid brass and copper fixtures that resist corrosion in heavy humidity',
            'Waterproof, gel-filled or sealed wire connections instead of cheap pierce-type clips',
            'Transformers mounted high and on dedicated GFCI-protected outlets',
            'Fixture placement that avoids low spots and drainage paths where water collects',
            'Sealed LED fixtures with appropriate IP ratings for wet locations',
            'Timers and smart controls that keep running after storm-related power blips',
            'Layouts planned for fast-growing beds, palms and shade trees',
        ]) ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Communities Served', 'Houston Area Communities We Serve', 'From inner-loop neighborhoods to the master-planned suburbs. Do not see yours? <a href="/quote/">Ask us</a>; nearby areas are usually within reach.'); ?>
    <ul class="pill-list reveal">
      <?php foreach (['Houston', 'River Oaks', 'Memorial', 'The Heights', 'Bellaire', 'West University Place', 'Tanglewood', 'Katy', 'Cinco Ranch', 'Cypress', 'Bridgeland', 'The Woodlands', 'Spring', 'Kingwood', 'Humble', 'Sugar Land', 'Missouri City', 'Richmond', 'Pearland', 'Friendswood', 'Clear Lake', 'Pasadena'] as $c) echo '<li>' . e($c) . '</li>'; ?>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('Featured Look', 'A Houston Backyard After Dark', 'Drag the slider to compare. Layered light around the pool, the plantings and the patio gives the yard depth and makes the edges of the water easy to see.'); ?>
    <?php before_after('pool-lighting', 'Pool and landscape lighting at night, installed by Landscape Lighting Texas'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
    <?php section_head('Our Process', 'How a Houston Lighting Project Works'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>A designer visits around sunset to walk the yard, note drainage and low spots, and talk through how you use the space after dark.</p></li>
      <li><h3>Custom design</h3><p>You receive a plan and itemized quote covering fixtures, beam angles, color temperature, transformer location and zones. Typical residential projects fall in a planning range of $2,500–$12,000.</p></li>
      <li><h3>Expert installation</h3><p>Our crew installs cable, fixtures and the transformer with sealed connections, working carefully around irrigation, roots and finished beds.</p></li>
      <li><h3>Reveal &amp; tune</h3><p>We return after dark to aim, balance and set the timer, then show you the controls. Work is backed by our 5-year workmanship warranty.</p></li>
    </ol>
    <div class="reveal" style="margin-top:2rem"><?= tool_promo('/tools/dusk-timer/') ?></div>
  </div>
</section>

<?php faqs([
    ['Will landscape lighting hold up to Houston rain and flooding?', 'A well-built low-voltage system handles heavy rain well. The key details are sealed fixtures, waterproof connections, a transformer mounted above likely water levels and fixtures kept out of drainage paths. If a yard does flood, we can inspect and test the system afterward as part of our <a href="/services/landscape-lighting-maintenance/">maintenance service</a>.'],
    ['What fixtures work best in Houston humidity?', 'Solid brass and copper fixtures are our first choice because they develop a protective patina instead of corroding. Many painted aluminum fixtures flake and pit in sustained humidity. Combined with sealed LED modules, they give the longest life in Southeast Texas.'],
    ['Can you light palms and tall pines?', 'Yes. Palms usually look best with one or two narrow uplights grazing the trunk and catching the fronds. Tall pines in areas like The Woodlands and Kingwood often need higher-output fixtures with narrow beams to reach the canopy without glare.'],
    ['How much does Houston landscape lighting cost?', 'Most homes fall in a planning range of $2,500–$12,000, with starter systems around $2,500–$5,000. Large estates with pools and extensive grounds can exceed $20,000. Use our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> for a ballpark before your free consultation.'],
]); ?>

<section class="section">
  <div class="container">
    <?php section_head('Statewide', 'Other Areas We Serve', 'Landscape Lighting Texas designs and installs outdoor lighting across the state. <a href="/areas/">See every service area</a>.'); ?>
    <?php area_cards('houston'); ?>
  </div>
</section>

<?php cta_band('Ready to Light Your Houston Home?', 'Book a free dusk consultation. A designer will walk your property at nightfall, show you what is possible and send a clear, itemized quote.'); ?>
