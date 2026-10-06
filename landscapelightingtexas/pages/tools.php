<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Free tools';
$P['tools_js'] = true;
$P['lead'] = 'Plan smarter before you spend a dollar. Estimate costs, preview lighting effects, size a transformer, check beam spread and time your lights to Texas sunsets.';
?>
<section class="section">
  <div class="container">
    <?php section_head('Calculators &amp; simulators', 'Eight Free Landscape Lighting Tools'); tool_cards(); ?>
  </div>
</section>
<section class="section alt">
  <div class="container">
    <?php section_head('Try it here', 'The Lighting Design Simulator', 'Turn on facade, tree, path and entry lighting, then try a scene. It is the fastest way to understand layered lighting.'); ?>
    <div class="reveal"><?php widget_simulator(true); ?></div>
  </div>
</section>
<section class="section">
  <div class="container narrow prose reveal">
    <h2>How to Use These Tools</h2>
    <p>Start with the <a href="/tools/lighting-style-quiz/">lighting style quiz</a> to find the look that suits your home, then play with the <a href="/tools/lighting-design-simulator/">simulator</a> and <a href="/tools/color-temperature-visualizer/">color temperature visualizer</a> to refine it. When you have an idea of how many fixtures you want, the <a href="/landscape-lighting-cost-calculator/">cost calculator</a> gives a planning budget, and the <a href="/tools/transformer-calculator/">transformer calculator</a> and <a href="/tools/beam-spread-calculator/">beam spread calculator</a> cover the technical side.</p>
    <p>Every result is a planning estimate. Real projects depend on wiring distances, soil, existing hardscape and the final design — which is why every Landscape Lighting Texas quote starts with a free dusk consultation at your property.</p>
  </div>
</section>
<?php cta_band();
