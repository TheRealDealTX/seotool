<?php defined('LLT') or die(http_response_code(404));
global $AREAS;
$P['eyebrow'] = 'Central Texas · Hill Country';
$P['lead'] = 'Austin landscape lighting designed for limestone, live oaks and long Hill Country evenings, from central Austin bungalows to lake homes above Lake Travis.';
$P['_cities'] = $AREAS['austin'][2];
?>
<section class="section">
  <div class="container">
    <?php split('oak-tree-uplighting', 'Live oak uplighting in a Central Texas yard at night', '
      <p class="eyebrow">Lighting the Hill Country</p>
      <h2 class="section-title">Austin Landscape Lighting With a Sense of Place</h2>
      <p class="lead-p">Good Austin landscape lighting does not try to make a yard look like daytime. It picks out what makes Central Texas properties special: pale limestone, the twisting limbs of a live oak, a view over the hills, a porch you actually use from March to November.</p>
      <p>Landscape Lighting Texas designs and installs low-voltage LED systems for homes across Austin and the surrounding Hill Country. Every plan starts with a walk of your property at dusk, so we can see how your stone, trees and slopes behave as the light fades, then we build a layered design around them.</p>
      <p>The result is warm, balanced light that flatters the architecture, guides guests safely and respects the region’s strong dark-sky culture.</p>
      <p><a class="link-arrow" href="/quote/">Book a free dusk consultation ' . icon('arrow', 16) . '</a></p>
    '); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('What We Light', 'What We Light in Austin', 'Central Texas homes mix rugged materials with outdoor rooms that get used most of the year. These are the features we light most often.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('home') ?></span><h3>Limestone &amp; Austin stone facades</h3><p>Close-set uplights graze the texture of cut limestone and Austin stone, while 2700K color keeps the cream and gold tones warm instead of chalky. See <a href="/services/architectural-uplighting/">architectural uplighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('tree') ?></span><h3>Live oaks &amp; cedar elms</h3><p>Two or three uplights at different angles give a live oak canopy depth, and moonlighting from high limbs throws soft branch shadows across the lawn. See <a href="/services/garden-tree-lighting/">tree and garden lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('path') ?></span><h3>Steps, slopes &amp; paths</h3><p>Hill Country lots rarely sit flat. Step lights and low path lights make terraced walks and stone stairs safe without lighting up the whole hillside.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('patio') ?></span><h3>Porches, decks &amp; outdoor kitchens</h3><p>Downlights in pergolas and dimmable string lights turn a back porch into an evening room. See <a href="/services/patio-outdoor-living-lighting/">patio and outdoor living lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('water') ?></span><h3>Pools &amp; view decks</h3><p>On lake and hillside homes we light the near landscape and keep the view dark, so you can still see the water and the stars. See <a href="/services/pool-water-feature-lighting/">pool lighting</a>.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('smart') ?></span><h3>Smart scenes &amp; curfews</h3><p>Astronomical timers and app control let you run full scenes at dusk, then dim to a quieter late-night level. See <a href="/services/smart-lighting-systems/">smart lighting systems</a>.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Local Design', 'Designing Landscape Lighting for Austin and the Hill Country', '', 'left'); ?>
        <p>Central Texas has its own set of challenges. Shallow soil over limestone means wire cannot always be trenched to the usual depth, so we plan routes around rock shelves and protect cable where it runs through beds and gravel. Native trees like live oaks and cedar elms have wide, shallow roots, so we hand-dig near the trunk instead of cutting through feeder roots.</p>
        <p>Light pollution is a real conversation here too. Dripping Springs became the first International Dark Sky Community in Texas, and several Hill Country towns follow dark-sky lighting principles. Even inside Austin, many neighbors simply prefer quieter nights. We design with that in mind.</p>
      </div>
      <div class="reveal">
        <?= checklist([
            'Shielded fixtures and narrow beam angles aimed at the target, not the sky',
            'Warm 2700K color as our default, with 2200K–2400K options for dark-sky-minded properties',
            'Wire routed around limestone ledges and protected where soil is shallow',
            'Hand-digging near live oak and cedar elm roots, with fixtures set outside the trunk flare',
            'Solid brass or copper fixtures that hold up to heat, hail and irrigation',
            'Multi-tap transformers and 12-gauge cable to handle long runs on large lots',
            'Timers set to dim or switch off zones later in the evening',
        ]) ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Communities Served', 'Austin Area Communities We Serve', 'We work throughout the city and the fast-growing towns around it. Do not see yours? <a href="/quote/">Ask us</a>; nearby areas are usually within reach.'); ?>
    <ul class="pill-list reveal">
      <?php foreach (['Austin', 'Westlake', 'Tarrytown', 'Travis Heights', 'Barton Creek', 'Steiner Ranch', 'Lakeway', 'Bee Cave', 'Spicewood', 'Dripping Springs', 'Round Rock', 'Georgetown', 'Cedar Park', 'Leander', 'Pflugerville', 'Hutto', 'Buda', 'Kyle', 'San Marcos', 'Wimberley'] as $c) echo '<li>' . e($c) . '</li>'; ?>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('Featured Look', 'A Live Oak Canopy, Lit the Hill Country Way', 'Drag the slider to compare. Two uplights at the trunk and a soft wash on the lower limbs give a mature live oak shape and depth without spilling light into the sky.'); ?>
    <?php before_after('oak-tree-uplighting', 'Live oak tree uplighting at night, lit by Landscape Lighting Texas'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
    <?php section_head('Our Process', 'How an Austin Lighting Project Works'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>A designer meets you at your property around sunset, walks the yard as the light fades and talks through what you want to see, use and secure after dark.</p></li>
      <li><h3>Custom design</h3><p>You get a lighting plan and an itemized quote: fixture types, beam angles, color temperature, transformer size and zones. Typical residential projects fall in a planning range of $2,500–$12,000.</p></li>
      <li><h3>Expert installation</h3><p>Our crew installs fixtures, cable and the transformer, working around roots, rock and irrigation, and leaves beds and lawns the way we found them.</p></li>
      <li><h3>Reveal &amp; tune</h3><p>We come back after dark to aim every fixture, balance brightness, set the timer and walk you through your controls. The work is covered by our 5-year workmanship warranty.</p></li>
    </ol>
    <div class="reveal" style="margin-top:2rem"><?= tool_promo('/tools/dusk-timer/') ?></div>
  </div>
</section>

<?php faqs([
    ['Can landscape lighting be dark-sky friendly in Austin and Dripping Springs?', 'Yes. We use fully shielded fixtures, aim light down or tightly onto targets, keep color warm (2700K or lower) and put zones on timers that dim or switch off late at night. That approach suits Dripping Springs and other dark-sky-minded Hill Country communities and still gives you a beautiful, usable yard.'],
    ['How do you run wire in rocky Hill Country soil?', 'Where limestone sits close to the surface, we follow natural soil pockets and bed edges, use protective conduit in vulnerable spots and avoid cutting into tree roots. Planning the route carefully at the design stage is what keeps rocky-lot installs clean and reliable.'],
    ['Will lighting hurt my live oaks?', 'Not when it is installed carefully. We set fixtures outside the trunk flare, hand-dig near roots and use LEDs, which run far cooler than old halogen lamps. Read our guide on <a href="/how-to-light-live-oak-trees/">how to light live oak trees</a> for more detail.'],
    ['What does Austin landscape lighting cost?', 'Most residential projects fall in a planning range of $2,500–$12,000, with starter systems around $2,500–$5,000 and large Hill Country estates sometimes exceeding $20,000. Try our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> for a ballpark, then book a free consultation for an exact quote.'],
]); ?>

<section class="section">
  <div class="container">
    <?php section_head('Statewide', 'Other Areas We Serve', 'Landscape Lighting Texas designs and installs outdoor lighting across the state. <a href="/areas/">See every service area</a>.'); ?>
    <?php area_cards('austin'); ?>
  </div>
</section>

<?php cta_band('Ready to Light Your Austin Home?', 'Book a free dusk consultation. A designer will walk your property at nightfall, show you what is possible and send a clear, itemized quote.'); ?>
