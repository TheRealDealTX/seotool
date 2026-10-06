<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Facade & Home Lighting';
$P['lead'] = 'Architectural uplighting in Texas, designed at dusk and aimed by hand: grazed limestone, lit columns and entries, and balanced facades that give your home presence after dark without glare or hot spots.';
?>
<section class="section">
  <div class="container">
    <?php split('architectural-uplighting', 'Texas stone home with architectural uplighting on the facade and columns at dusk', '
      <p class="eyebrow">Why it matters</p>
      <h2>Architectural Uplighting in Texas, Done With Restraint</h2>
      <p class="lead-p">Architectural uplighting is the craft of placing small, low-voltage fixtures at the base of a house and aiming light up its walls, columns and gables so the architecture reads clearly at night.</p>
      <p>Done well, the house looks the way it does in late-afternoon sun: textured, three-dimensional and welcoming. Done poorly, it looks like a row of scallops with bright spots at the bottom and dark gaps in between. The difference is design, not wattage.</p>
      <p>At Landscape Lighting Texas we start by asking what makes your home distinctive. On a Hill Country house it might be rough-cut Austin stone; on a Dallas Tudor, steep gables and a stone chimney; on a Houston traditional, tall columns and a deep porch. We light those features and let the rest fall into soft shadow.</p>
    ', false); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Techniques', 'How We Light a Facade', 'Each wall surface and feature calls for a different technique. Most homes use three or four of these together.'); ?>
    <div class="grid-3">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('beam') ?></span><h3>Grazing</h3><p>A fixture placed 6–12 inches from a textured wall and aimed nearly straight up. The steep angle throws shadow from every stone edge, which is what makes limestone, fieldstone and brick look rich at night. It is the signature look for Texas stone homes.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('sun') ?></span><h3>Washing</h3><p>Wider-beam fixtures set farther back (often 2–3 feet) to spread even light across a smooth surface. Washing suits stucco, painted siding and modern facades, where grazing would exaggerate every small imperfection.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('home') ?></span><h3>Column &amp; feature spotlighting</h3><p>Narrow 15–25° beams placed tight to columns, pilasters and chimneys. Light travels the full height without spilling onto windows, and repeating it on each column gives the facade rhythm.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('moon') ?></span><h3>Shadowing &amp; silhouetting</h3><p>Lighting a shrub or small tree in front of a wall casts its shadow across the facade, or backlights it as a dark shape against a lit surface. A subtle way to soften large blank walls.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('bulb') ?></span><h3>Entry &amp; eave downlighting</h3><p>Small downlights tucked into soffits or porch ceilings light the front door, house numbers and steps from above, so guests can see faces and footing without anyone staring into a bulb.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('spark') ?></span><h3>Balancing the composition</h3><p>The center of the house (usually the entry) should be slightly brighter than the wings, with corners defined but not glaring. We tune each fixture's output on site until the whole elevation reads as one picture from the street.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    <?php section_head('See the difference', 'The Same Home, Before and After', 'Drag the slider. Without lighting, the house is a dark shape behind a porch light. With uplighting, the stone, columns and roofline come forward.'); ?>
    <?php before_after('architectural-uplighting', 'Before and after architectural uplighting on a Texas home'); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Specifications', 'Typical Fixtures for Facade Lighting', 'Starting points we refine on site. Final output and beam angle depend on wall height, texture and how close the fixture can sit.'); ?>
    <div class="table-wrap reveal">
      <table>
        <thead><tr><th>Fixture</th><th>Typical output</th><th>Beam angle</th><th>Color temp</th><th>Materials &amp; notes</th></tr></thead>
        <tbody>
          <tr><td>Grazing uplight (single-story wall)</td><td>150–300 lm</td><td>25–36°</td><td>2700K</td><td>Solid brass or copper, glare cowl</td></tr>
          <tr><td>Grazing / wash uplight (two-story wall)</td><td>300–600 lm</td><td>36–60°</td><td>2700K</td><td>Brass or copper, adjustable knuckle</td></tr>
          <tr><td>Column &amp; chimney spot</td><td>200–450 lm</td><td>10–25°</td><td>2700K</td><td>Narrow optic or snoot to control spill</td></tr>
          <tr><td>In-grade well light</td><td>200–500 lm</td><td>25–60°</td><td>2700K</td><td>Composite or brass housing, drain gravel, rated for wet locations</td></tr>
          <tr><td>Eave / soffit downlight</td><td>100–250 lm</td><td>36–60°</td><td>2700K</td><td>Small aluminum or brass housing, recessed or surface</td></tr>
          <tr><td>Wiring &amp; power</td><td colspan="4">12V multi-tap transformer, 12- or 10-gauge direct-burial cable, hub layout for even voltage. Check sizing with our <a href="/tools/transformer-calculator/">transformer calculator</a>.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Texas considerations', 'Uplighting for Texas Homes and Weather', '', 'left'); ?>
        <p>Texas architecture and weather shape every design decision we make.</p>
        <?= checklist([
            '<strong>Limestone and Austin stone</strong> reward grazing; we often shift slightly warmer (2700K) to bring out the cream and honey tones.',
            '<strong>Brick</strong> benefits from a slightly wider beam so mortar lines do not turn into harsh stripes.',
            '<strong>Hail and foot traffic:</strong> solid brass bodies and tempered glass lenses survive impacts that crack plastic fixtures.',
            '<strong>Clay and caliche soil:</strong> fixtures are set on sturdy stakes or mounting blocks so shrink-swell cycles do not tilt them off aim.',
            '<strong>Summer heat and irrigation:</strong> sealed fittings and waterproof connectors keep sprinkler water and humidity out of connections.',
            '<strong>Coastal homes:</strong> near the Gulf, brass and copper are the right call because aluminum fixtures corrode in salt air.',
        ]) ?>
      </div>
      <div class="reveal">
        <?php section_head('Neighbors &amp; HOAs', 'Bright Enough, Never Glaring', '', 'left'); ?>
        <p>Many Texas neighborhoods have HOA rules on outdoor lighting, and some communities near the Hill Country follow dark-sky practices. Architectural uplighting fits easily within both when it is designed properly.</p>
        <ul class="pill-list"><li>Shielded fixtures</li><li>Aimed at walls, not sky</li><li>Warm 2700K color</li><li>Timers that shut off late</li><li>No light into windows</li></ul>
        <p>We keep beams on the structure, add cowls or louvers where a lamp could be seen from the street, and set timers so the facade dims or switches off at a reasonable hour. If your HOA needs a lighting plan for approval, we provide one.</p>
        <p>Choosing between warm and neutral white? See how they look on stone with the tool below, or read our <a href="/landscape-lighting-color-temperature-guide/">color temperature guide</a>.</p>
        <?= tool_promo('/tools/color-temperature-visualizer/') ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container narrow">
    <?php section_head('Our process', 'From Dusk Walkthrough to Final Reveal'); ?>
    <ol class="steps">
      <li><h3>Free dusk consultation</h3><p>A designer visits as the sun goes down, studies the facade from the street and the driveway, and may set up a few demo fixtures so you can see grazing versus washing on your own walls.</p></li>
      <li><h3>Custom design</h3><p>You receive a plan showing every fixture location, beam angle, output and color temperature, with an itemized quote. Facade lighting is often paired with <a href="/services/garden-tree-lighting/">tree lighting</a> and <a href="/services/pathway-driveway-lighting/">path lighting</a> on the same transformer.</p></li>
      <li><h3>Expert installation</h3><p>Licensed, insured installers set the transformer, run cable in narrow slit trenches and place fixtures with minimal disturbance to beds and turf. Most homes are installed in a day or two.</p></li>
      <li><h3>Reveal &amp; tune</h3><p>We come back after dark, walk the property with you, and fine-tune aim and intensity until the facade is balanced. The work is covered by our 5-year workmanship warranty.</p></li>
    </ol>
  </div>
</section>

<?php faqs([
    ['How many uplights does a typical Texas home need?', 'A single-story home often needs 6–12 facade fixtures; a larger two-story home, 12–25. The number depends on wall length, the number of columns and gables, and how much of the facade you want to feature. Our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> gives a planning estimate.'],
    ['Will uplighting shine into my windows?', 'Not when it is designed properly. We place fixtures between windows, use narrow beams on columns, and add glare shields where needed so light stays on the masonry and out of bedrooms.'],
    ['What color temperature is best for a stone or brick house?', 'Most Texas homes look best at 2700K. It brings out the warmth of limestone, Austin stone and red brick. Cooler 4000K and above tends to make stone look gray and flat, so we rarely use it on facades.'],
    ['How much does it cost to run facade lighting?', 'Very little. LED landscape fixtures use roughly 75–80% less energy than halogen, and a whole-property LED system typically costs about $10–$25 a month to run. Facade lighting alone is usually at the low end of that range.'],
    ['Can you light a two-story home without lights on the roof?', 'Yes. Ground-mounted fixtures with the right output and beam angle can reach a two-story gable. For deep overhangs we may add small soffit downlights, which are hidden from view.'],
]); ?>

<section class="section alt">
  <div class="container">
    <?php section_head('Keep exploring', 'Explore Other Services', 'Facade lighting looks best as part of a full plan from Landscape Lighting Texas.'); ?>
    <?php service_cards('architectural-uplighting', 3); ?>
  </div>
</section>

<?php cta_band('Ready to See Your Home in a New Light?'); ?>
