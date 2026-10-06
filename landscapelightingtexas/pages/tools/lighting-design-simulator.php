<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Interactive simulator';
$P['lead'] = 'Switch lighting zones on a real Texas home, dim them, change color temperature and try smart scenes — the same layering decisions a lighting designer makes on site.';
$P['tools_js'] = true;
$P['hero_no_cta'] = true;
?>
<section class="section">
  <div class="container reveal"><?php widget_simulator(); ?></div>
</section>
<section class="section alt">
  <div class="container narrow prose reveal">
<h2>What the Simulator Shows</h2>
<p>Professional landscape lighting is built in layers. Each button in the simulator controls one layer on a real stone home photographed at night:</p>
<ul>
<li><strong>Facade uplights</strong> graze the stone and columns, giving the house shape and texture. This is the layer that creates curb appeal from the street.</li>
<li><strong>Tree uplights</strong> frame the home and add depth. Large trees usually need two or three fixtures so the canopy does not look flat.</li>
<li><strong>Path &amp; beds</strong> light the walk and planting beds — the safety layer and the one guests notice first.</li>
<li><strong>Entry &amp; windows</strong> warm the front door so the home reads as welcoming rather than spotlit.</li>
<li><strong>Shrub accents</strong> fill the middle ground so there are no black holes between the house and the street.</li>
</ul>
<p>Try switching on only the facade, then add the trees and the paths. Notice how the scene goes from &ldquo;lit house&rdquo; to &ldquo;lit property.&rdquo; That balance — not brightness — is what makes a design look expensive.</p>
<h2>Scenes, Dimming and Color Temperature</h2>
<p>The scene buttons mimic what a <a href="/services/smart-lighting-systems/">smart lighting system</a> can do on your phone: a bright <em>Entertaining</em> scene for guests, a <em>Late night</em> scene that keeps only the path on at low output, and a <em>Security</em> scene that brightens entries and walks. The dimmer shows how much atmosphere you gain by running lights at 60–80% instead of full power, and the color temperature slider shows why most Texas homes look best at 2700K. Read more in our <a href="/landscape-lighting-color-temperature-guide/">color temperature guide</a>.</p>
<h2>From Simulator to Your Home</h2>
<p>The fixture and wattage readout is a rough guide for a home of this size. Your property will be different — which is why every Landscape Lighting Texas design starts with a free dusk consultation. Use the <a href="/landscape-lighting-cost-calculator/">cost calculator</a> to turn the fixture count into a planning budget.</p>

  </div>
</section>
<?php faqs([
    ['Is the simulator accurate for my home?', 'It shows how lighting layers work together on a typical Texas stone home. Your design will be tailored to your architecture, trees and sightlines during the dusk consultation.'],
    ['How many fixtures does a typical home need?', 'Front-yard designs often use 12–20 fixtures; full front-and-back designs commonly run 20–40. Large estates use more.'],
    ['Can I really control scenes from my phone?', 'Yes. Smart transformers and controllers let you schedule, dim and switch zones and scenes from an app, and many integrate with smart-home platforms.'],
]); ?>
<section class="section">
  <div class="container">
    <?php section_head('More free tools', 'Keep Planning Your Project'); tool_cards('/tools/lighting-design-simulator/'); ?>
  </div>
</section>
<?php cta_band();
