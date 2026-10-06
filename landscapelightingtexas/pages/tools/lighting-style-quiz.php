<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Style quiz';
$P['lead'] = 'Answer six quick questions about your home, yard and priorities and get a landscape lighting plan matched to your style, controls and budget.';
$P['tools_js'] = true;
$P['hero_no_cta'] = true;
?>
<section class="section">
  <div class="container reveal"><?php widget_quiz(); ?></div>
</section>
<section class="section alt">
  <div class="container narrow prose reveal">
<h2>The Six Lighting Styles</h2>
<p>Most great landscape lighting designs lean toward one of a few styles, then borrow from the others:</p>
<ul>
<li><strong>The Architectural Statement</strong> — the home is the hero, with grazed stone and lit columns. See <a href="/services/architectural-uplighting/">architectural uplighting</a>.</li>
<li><strong>The Moonlit Canopy</strong> — big trees, uplit and moonlit, creating drama and shadow. See <a href="/services/garden-tree-lighting/">garden &amp; tree lighting</a>.</li>
<li><strong>The Backyard Resort</strong> — pools, patios and outdoor kitchens layered for entertaining. See <a href="/services/pool-water-feature-lighting/">pool lighting</a> and <a href="/services/patio-outdoor-living-lighting/">patio lighting</a>.</li>
<li><strong>The Garden Gallery</strong> — texture and depth from accent lights on plants and sculpture.</li>
<li><strong>The Safe Arrival</strong> — paths, steps and drives lit evenly and glare-free. See <a href="/services/pathway-driveway-lighting/">pathway lighting</a>.</li>
<li><strong>The Hill Country Night</strong> — subtle, warm and dark-sky friendly, so the stars stay bright.</li>
</ul>
<p>Your result is a starting point. During a free dusk consultation, a Landscape Lighting Texas designer blends the right styles for your property and budget.</p>

  </div>
</section>
<?php faqs([
    ['Is the quiz result a quote?', 'No — it suggests a style, scope and controls. For pricing, try the cost calculator or request a free quote.'],
    ['Can I combine styles?', 'Absolutely. Most homes mix two or three, such as architectural lighting in front and a resort-style backyard.'],
    ['What if I am not sure about budget?', 'Choose "Not sure yet" and we will suggest a mid-range scope that can be phased in over time.'],
]); ?>
<section class="section">
  <div class="container">
    <?php section_head('More free tools', 'Keep Planning Your Project'); tool_cards('/tools/lighting-style-quiz/'); ?>
  </div>
</section>
<?php cta_band();
