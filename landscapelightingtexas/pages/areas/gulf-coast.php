<?php defined('LLT') or die(http_response_code(404));
global $AREAS;
$P['eyebrow'] = 'Gulf Coast · Coastal Bend · Rio Grande Valley';
$P['lead'] = 'Coastal Texas landscape lighting built for salt air, storms and sandy soil, with marine-tough fixtures lighting palms, pools and raised homes from Galveston to Corpus Christi and the Rio Grande Valley.';
$P['_cities'] = $AREAS['gulf-coast'][2];
?>
<section class="section">
  <div class="container">
    <?php split('pool-lighting', 'Pool and palm landscape lighting at night on a coastal Texas home', '
      <p class="eyebrow">Lighting the Coast</p>
      <h2 class="section-title">Coastal Texas Landscape Lighting That Lasts</h2>
      <p class="lead-p">Life on the Texas coast happens outside: on the deck, by the pool, under the palms with the Gulf breeze coming in. Coastal Texas landscape lighting should make those evenings better, but it also has to stand up to one of the harshest environments for outdoor equipment anywhere in the state.</p>
      <p>Salt air corrodes cheap fixtures, humidity finds weak connections, and tropical storms bring wind and water. Landscape Lighting Texas designs coastal systems around those realities, starting with marine-tough materials and sealed connections and ending with a design that looks right on a beach house, a bay-front home or a palm-lined Valley property.</p>
      <p>Every project begins with a free walk of your property at dusk.</p>
      <p><a class="link-arrow" href="/quote/">Book a free dusk consultation ' . icon('arrow', 16) . '</a></p>
    '); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('What We Light', 'What We Light on the Gulf Coast', 'Coastal homes are built around views, water and outdoor living. These are the features we light most often.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('tree') ?></span><h3>Palms &amp; tropical plantings</h3><p>Narrow uplights graze palm trunks and catch the fronds, while softer light picks out oleander, hibiscus and other coastal plantings. See <a href="/services/garden-tree-lighting/">tree and garden lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('water') ?></span><h3>Pools &amp; outdoor living</h3><p>Pool decks, outdoor kitchens and water features lit in layers for resort-style evenings. See <a href="/services/pool-water-feature-lighting/">pool and water feature lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('home') ?></span><h3>Raised &amp; beach homes</h3><p>Pilings, stairs, porches and the space under raised homes lit for safety and character, without glare off the water. See <a href="/services/architectural-uplighting/">architectural uplighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('patio') ?></span><h3>Decks &amp; balconies</h3><p>Step lights, rail lights and shielded downlights for decks and balconies built for watching the sunset and staying out after. See <a href="/services/patio-outdoor-living-lighting/">patio and deck lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>Walkways &amp; boardwalks</h3><p>Low path lights and in-grade fixtures along walks, dock access paths and drives, placed for sandy soil. See <a href="/services/pathway-driveway-lighting/">pathway lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('wrench') ?></span><h3>Post-storm repair</h3><p>Testing, re-aiming and replacing fixtures and connections after storm season or salt damage, on any brand of system. See <a href="/services/landscape-lighting-maintenance/">maintenance and repair</a>.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Local Design', 'Designing Coastal Texas Landscape Lighting', '', 'left'); ?>
        <p>Material choice matters more on the coast than anywhere else in Texas. Salt spray and salty humidity attack aluminum and steel quickly, causing pitting, flaking paint and seized hardware. Solid brass and copper fixtures develop a natural patina instead, and with stainless or brass hardware they can last for many years even near the water.</p>
        <p>Storms are the other planning factor. We mount transformers high, keep connections sealed, choose low-profile fixtures that do not catch wind and use timers that pick up again after a power interruption. On beachfront property, we also keep light low, shielded and away from the shoreline, since bright lights on the beach can disorient nesting and hatchling sea turtles and some coastal communities have lighting rules to protect them.</p>
      </div>
      <div class="reveal">
        <?= checklist([
            'Solid brass and copper fixtures with stainless or brass hardware for salt air',
            'Sealed LED modules and waterproof wire connections',
            'Transformers mounted high, above likely flood levels, on GFCI-protected circuits',
            'Low-profile fixtures and secure stakes for sandy soil and strong wind',
            'Shielded, warm light kept low and aimed away from beaches and the water',
            'Astronomical timers and smart controls that recover after power outages',
            'Annual rinse, inspection and tune-up to stay ahead of corrosion',
        ]) ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Communities Served', 'Gulf Coast &amp; South Texas Communities We Serve', 'From the upper coast to the Coastal Bend and the Rio Grande Valley. Do not see yours? <a href="/quote/">Ask us</a>; nearby areas are usually within reach.'); ?>
    <ul class="pill-list reveal">
      <?php foreach (['Galveston', 'League City', 'Clear Lake', 'Kemah', 'Seabrook', 'Texas City', 'Freeport', 'Port Aransas', 'Corpus Christi', 'Portland', 'Rockport', 'Port Lavaca', 'Harlingen', 'McAllen', 'Mission', 'Edinburg', 'Brownsville', 'South Padre Island'] as $c) echo '<li>' . e($c) . '</li>'; ?>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('Featured Look', 'A Coastal Pool Deck After Sunset', 'Drag the slider to compare. Palms, plantings and the pool edge lit in layers make a coastal backyard feel like a resort, and keep the deck safe to walk.'); ?>
    <?php before_after('pool-lighting', 'Pool and palm lighting at night, installed by Landscape Lighting Texas'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
    <?php section_head('Our Process', 'How a Coastal Lighting Project Works'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>A designer walks your property at sunset, notes exposure to salt and wind, flood-prone spots and views, and talks through how you use the space at night.</p></li>
      <li><h3>Custom design</h3><p>You receive a plan and itemized quote with coastal-grade fixtures, beam angles, color temperature, transformer placement and zones. Typical residential projects fall in a planning range of $2,500–$12,000.</p></li>
      <li><h3>Expert installation</h3><p>Our crew installs fixtures, cable and transformers with sealed connections and secure mounts suited to sand, decks and pilings.</p></li>
      <li><h3>Reveal &amp; tune</h3><p>We return after dark to aim and balance every light, set timers and show you the controls. Work is backed by our 5-year workmanship warranty.</p></li>
    </ol>
    <div class="reveal" style="margin-top:2rem"><?= tool_promo('/tools/dusk-timer/') ?></div>
  </div>
</section>

<?php faqs([
    ['What landscape lighting fixtures are best near salt water?', 'Solid brass and copper are the best choices for coastal Texas. They develop a protective patina instead of corroding, unlike most aluminum and painted steel fixtures. Pair them with stainless or brass hardware, sealed LEDs and waterproof connections for the longest life.'],
    ['How does landscape lighting handle hurricanes and tropical storms?', 'Low-voltage systems with low-profile fixtures, sealed connections and high-mounted transformers come through storms well in most cases. After a major storm we can test the system, re-aim fixtures and replace anything damaged through our <a href="/services/landscape-lighting-maintenance/">repair service</a>.'],
    ['Can you light a beachfront home without disturbing sea turtles?', 'Yes. We keep beach-facing light low, fully shielded and warm in color, aim it away from the sand and use timers so it is off when it is not needed. We also follow any local coastal lighting rules that apply to your property.'],
    ['How much does coastal landscape lighting cost?', 'Most residential projects fall in a planning range of $2,500–$12,000, with starter systems around $2,500–$5,000. Coastal-grade brass and copper fixtures are an important part of the budget because they last much longer near the water. Try our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> for a ballpark.'],
]); ?>

<section class="section">
  <div class="container">
    <?php section_head('Statewide', 'Other Areas We Serve', 'Landscape Lighting Texas designs and installs outdoor lighting across the state. <a href="/areas/">See every service area</a>.'); ?>
    <?php area_cards('gulf-coast'); ?>
  </div>
</section>

<?php cta_band('Ready to Light Your Coastal Home?', 'Book a free dusk consultation. A designer will walk your property at nightfall, show you what is possible and send a clear, itemized quote.'); ?>
