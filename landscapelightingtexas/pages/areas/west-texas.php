<?php defined('LLT') or die(http_response_code(404));
global $AREAS;
$P['eyebrow'] = 'West Texas · Permian Basin · Panhandle';
$P['lead'] = 'West Texas landscape lighting built for wind, dust, caliche and big night skies, with desert plantings, long drives and wide-open properties lit the dark-sky way.';
$P['_cities'] = $AREAS['west-texas'][2];
?>
<section class="section">
  <div class="container">
    <?php split('driveway-lighting', 'Driveway lighting at night on a large Texas property', '
      <p class="eyebrow">Lighting Big Country</p>
      <h2 class="section-title">West Texas Landscape Lighting for Wide-Open Properties</h2>
      <p class="lead-p">West of the Hill Country, the landscape opens up and the sky takes over. Good West Texas landscape lighting works with that: it shows off a home, a desert garden and a long drive without washing out one of the darkest night skies in the country.</p>
      <p>Landscape Lighting Texas designs and installs low-voltage LED systems for homes and businesses from El Paso to Midland, Odessa, Lubbock, Amarillo, Abilene and San Angelo. Properties here tend to be bigger and more exposed, so careful fixture selection, sturdy installation and well-planned wiring matter as much as the design itself.</p>
      <p>Every plan starts with a free walk of your property at dusk, when we can see exactly how your land and sky behave as night falls.</p>
      <p><a class="link-arrow" href="/quote/">Book a free dusk consultation ' . icon('arrow', 16) . '</a></p>
    '); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('What We Light', 'What We Light in West Texas', 'Western properties call for a lighter touch and tougher hardware. These are the features we light most.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('leaf') ?></span><h3>Desert &amp; xeriscape gardens</h3><p>Agave, yucca, sotol, cactus and desert willow have strong shapes that look striking with low grazing light and shadows on a wall behind them. See <a href="/services/garden-tree-lighting/">garden lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>Long drives &amp; entries</h3><p>Low bollards and path lights mark long driveways and gates on acreage without throwing light across the land. See <a href="/services/pathway-driveway-lighting/">pathway and driveway lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('home') ?></span><h3>Stucco, stone &amp; adobe-style homes</h3><p>Soft washes and grazing light for stucco, stone and adobe-style walls, with warm color that suits earthy desert palettes. See <a href="/services/architectural-uplighting/">architectural uplighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('tree') ?></span><h3>Mesquites &amp; shade trees</h3><p>Mesquite, live oak and pecan trees around the house are gently uplit to give a yard depth and a focal point. See <a href="/services/garden-tree-lighting/">tree lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('patio') ?></span><h3>Patios &amp; fire pits</h3><p>Shielded downlights and dimmable lighting for patios and fire pits built for cool desert evenings and star-watching. See <a href="/services/patio-outdoor-living-lighting/">patio lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('shield') ?></span><h3>Security &amp; commercial</h3><p>Motion-aware, fully shielded lighting for homes, shops and commercial sites, aimed where it is needed and nowhere else. See <a href="/services/security-lighting/">security lighting</a>.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Local Design', 'Designing Landscape Lighting for West Texas Conditions', '', 'left'); ?>
        <p>Wind and dust are the everyday tests out here. Blowing grit scours finishes and coats lenses, gusts work loose fixtures in soft beds, and big temperature swings between day and night stress seals. Caliche, the cemented layer common under West Texas soil, can make digging slow and trenching difficult, so wire routes need planning before the first shovel goes in.</p>
        <p>Then there is the sky. Big Bend National Park is an International Dark Sky Park, and counties around the McDonald Observatory near Fort Davis have outdoor lighting rules to protect its view of the stars. Even far from those places, many West Texans simply want to keep seeing the Milky Way from the back porch. Dark-sky practice is part of every design we do here.</p>
      </div>
      <div class="reveal">
        <?= checklist([
            'Fully shielded fixtures aimed down or tightly onto their targets, never into the sky',
            'Warm color, 2700K and below, with amber-toned options near observatories',
            'Heavy-wall brass and copper fixtures with glass lenses that resist sand scouring',
            'Stakes and mounts set deep or anchored to stay put in strong wind',
            'Wire routes planned around caliche, with conduit where trenching is shallow',
            'Heavy-gauge cable, multiple home runs and multi-tap transformers for long distances',
            'Timers and motion controls so light runs only when it is useful',
        ]) ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Communities Served', 'West Texas Communities We Serve', 'We take on projects across West Texas, the Permian Basin and the Panhandle, including ranch and rural properties. Do not see yours? <a href="/quote/">Ask us</a> about availability.'); ?>
    <ul class="pill-list reveal">
      <?php foreach (['El Paso', 'Horizon City', 'Midland', 'Odessa', 'Big Spring', 'Lubbock', 'Wolfforth', 'Amarillo', 'Canyon', 'Abilene', 'San Angelo', 'Alpine', 'Fort Davis', 'Marfa'] as $c) echo '<li>' . e($c) . '</li>'; ?>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('Featured Look', 'A Long Drive, Lit Without Losing the Stars', 'Drag the slider to compare. Low, shielded fixtures mark the route and the entry while the land and sky beyond stay dark.'); ?>
    <?php before_after('driveway-lighting', 'Driveway lighting at night, installed by Landscape Lighting Texas'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
    <?php section_head('Our Process', 'How a West Texas Lighting Project Works'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>We walk the property at sunset, note wind exposure, soil and distances, and talk through what you want to light and what you want to keep dark.</p></li>
      <li><h3>Custom design</h3><p>You receive a plan and itemized quote with fixtures, beam angles, color temperature, transformer locations and cable sizing. Typical residential projects fall in a planning range of $2,500–$12,000, while large properties can run higher.</p></li>
      <li><h3>Expert installation</h3><p>Our crew installs fixtures, cable and transformers, working through caliche where needed and anchoring everything for wind.</p></li>
      <li><h3>Reveal &amp; tune</h3><p>We return after dark to aim and shield each fixture, balance the system, set timers and show you the controls. Work is backed by our 5-year workmanship warranty.</p></li>
    </ol>
    <div class="reveal" style="margin-top:2rem"><?= tool_promo('/tools/transformer-calculator/') ?></div>
  </div>
</section>

<?php faqs([
    ['What is dark-sky landscape lighting?', 'Dark-sky lighting puts light only where it is needed. It uses fully shielded fixtures, aims light downward or tightly onto a target, keeps color warm, uses no more brightness than necessary and switches off or dims when the light is not needed. It is the right approach anywhere in West Texas and especially near Big Bend and the McDonald Observatory.'],
    ['How do you deal with caliche when installing lighting?', 'We plan wire routes around the hardest ground where we can, use existing beds and hardscape edges, and protect cable in conduit where we cannot trench to normal depth. Planning this during design keeps installation clean and on schedule.'],
    ['Will fixtures survive West Texas wind and dust?', 'Solid brass and copper fixtures with glass lenses hold up far better than plastic or thin aluminum. We anchor fixtures firmly and recommend an annual cleaning and re-aim, which our <a href="/services/landscape-lighting-maintenance/">maintenance service</a> covers.'],
    ['Can you light a large ranch or rural property?', 'Yes. Long distances mean voltage drop is the main design challenge, so we use heavier cable, multiple runs and transformers placed close to the lights they power. Our <a href="/tools/transformer-calculator/">transformer and voltage drop calculator</a> shows why those choices matter.'],
]); ?>

<section class="section">
  <div class="container">
    <?php section_head('Statewide', 'Other Areas We Serve', 'Landscape Lighting Texas designs and installs outdoor lighting across the state. <a href="/areas/">See every service area</a>.'); ?>
    <?php area_cards('west-texas'); ?>
  </div>
</section>

<?php cta_band('Ready to Light Your West Texas Property?', 'Book a free dusk consultation. A designer will walk your property at nightfall, show you what is possible and send a clear, itemized quote.'); ?>
