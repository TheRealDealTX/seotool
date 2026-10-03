<?php
defined('TR_ROOT') || exit;
$crumbs = [['Roofing Tools', '/tools/'], [$tool['name'], '/tools/' . $toolSlug . '/']];
$faqs = [
    ['q' => 'What does a roof pitch like 6/12 mean?', 'a' => 'It means the roof rises 6 inches vertically for every 12 inches of horizontal run. Pitch is usually written as rise over a 12-inch run.'],
    ['q' => 'What is the slope multiplier?', 'a' => 'It is the factor that converts flat (plan-view) area into actual sloped roof surface: √(1 + (rise ÷ run)²). Multiply the footprint area by it to get roof area.'],
    ['q' => 'How many bundles of shingles are in a square?', 'a' => 'Most standard and architectural asphalt shingles are packaged three bundles per square (100 sq ft), but some heavier products use four or five. Check the specific product, and remember ridge cap and starter strips are usually ordered separately.'],
    ['q' => 'Can I measure pitch without going on the roof?', 'a' => 'Yes. You can measure from inside the attic against a rafter, or at a gable end with a level and tape from a ladder at the eave — never on the roof surface. Many smartphone apps can also estimate pitch from a photo. If in doubt, a free inspection includes accurate measurements.'],
];
layout_start([
    'title' => 'Roof Pitch & Area Calculator — Squares & Bundles', 'description' => 'Free roof pitch calculator: convert rise/run to pitch, angle and slope multiplier, then estimate roof area, squares and shingle bundles.',
    'path' => '/tools/' . $toolSlug . '/', 'crumbs' => $crumbs, 'schema' => [schema_faq($faqs)], 'scripts' => ['js/tools.js'], 'body_class' => 'page-tool',
]);
page_hero(['h1' => 'Roof Pitch & Area Calculator', 'lead' => 'Work out roof pitch, slope angle and multiplier, then turn your home\'s footprint into roof area, squares and shingle bundles.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true, 'eyebrow' => 'Free roofing tool']);
?>
<section class="section section--tight">
  <div class="container tool-layout" data-tool="pitch">
    <form class="tool-panel" novalidate data-pitch-form>
      <h2 class="tool-panel__title"><?= icon('ruler') ?> 1. Roof pitch</h2>
      <fieldset class="seg" data-pitch-mode>
        <legend class="sr-only">Enter pitch as</legend>
        <label><input type="radio" name="mode" value="rise" checked> Rise &amp; run</label>
        <label><input type="radio" name="mode" value="angle"> Angle (degrees)</label>
      </fieldset>
      <div class="form-grid" data-mode-panel="rise">
        <div class="field">
          <label for="p-rise">Rise (inches)</label>
          <input type="number" id="p-rise" name="rise" min="0" max="48" step="0.25" value="6" inputmode="decimal" aria-describedby="p-rise-err">
          <p class="field__error" id="p-rise-err" hidden></p>
        </div>
        <div class="field">
          <label for="p-run">Run (inches)</label>
          <input type="number" id="p-run" name="run" min="1" max="48" step="0.25" value="12" inputmode="decimal" aria-describedby="p-run-err">
          <p class="field__error" id="p-run-err" hidden></p>
        </div>
      </div>
      <div class="form-grid" data-mode-panel="angle" hidden>
        <div class="field field--wide">
          <label for="p-angle">Roof angle (degrees)</label>
          <input type="number" id="p-angle" name="angle" min="0" max="75" step="0.1" value="26.6" inputmode="decimal" aria-describedby="p-angle-err">
          <p class="field__error" id="p-angle-err" hidden></p>
        </div>
      </div>

      <h2 class="tool-panel__title"><?= icon('home') ?> 2. Roof area</h2>
      <fieldset class="seg" data-area-mode>
        <legend class="sr-only">Measure area by</legend>
        <label><input type="radio" name="amode" value="dims" checked> Footprint dimensions</label>
        <label><input type="radio" name="amode" value="flat"> Footprint area</label>
      </fieldset>
      <div class="form-grid" data-area-panel="dims">
        <div class="field">
          <label for="p-length">Building length (ft)</label>
          <input type="number" id="p-length" name="length" min="1" max="500" step="0.5" value="60" inputmode="decimal" aria-describedby="p-length-err">
          <p class="field__error" id="p-length-err" hidden></p>
        </div>
        <div class="field">
          <label for="p-width">Building width (ft)</label>
          <input type="number" id="p-width" name="width" min="1" max="500" step="0.5" value="35" inputmode="decimal" aria-describedby="p-width-err">
          <p class="field__error" id="p-width-err" hidden></p>
        </div>
        <div class="field field--wide">
          <label for="p-overhang">Overhang on each side (inches)</label>
          <input type="number" id="p-overhang" name="overhang" min="0" max="48" step="1" value="12" inputmode="numeric" aria-describedby="p-overhang-err">
          <p class="field__error" id="p-overhang-err" hidden></p>
        </div>
      </div>
      <div class="form-grid" data-area-panel="flat" hidden>
        <div class="field field--wide">
          <label for="p-flat">Footprint area incl. overhangs (sq ft)</label>
          <input type="number" id="p-flat" name="flat" min="10" max="100000" step="1" value="2200" inputmode="numeric" aria-describedby="p-flat-err">
          <p class="field__error" id="p-flat-err" hidden></p>
        </div>
      </div>
      <div class="form-grid">
        <div class="field">
          <label for="p-waste">Waste allowance (%)</label>
          <input type="number" id="p-waste" name="waste" min="0" max="30" step="1" value="10" inputmode="numeric" aria-describedby="p-waste-err">
          <p class="field__error" id="p-waste-err" hidden></p>
        </div>
        <div class="field">
          <label for="p-bundles">Bundles per square</label>
          <select id="p-bundles" name="bundles"><option value="3" selected>3 (most asphalt shingles)</option><option value="4">4</option><option value="5">5</option></select>
        </div>
      </div>
    </form>

    <div class="tool-results" aria-live="polite">
      <figure class="pitch-diagram">
        <svg viewBox="0 0 372 190" role="img" aria-labelledby="pd-title" data-pitch-svg>
          <title id="pd-title">Roof pitch diagram</title>
          <line x1="20" y1="160" x2="300" y2="160" class="pd-base"/>
          <polygon points="20,160 300,160 300,90" class="pd-tri" data-pd-tri/>
          <line x1="300" y1="160" x2="300" y2="90" class="pd-rise" data-pd-rise/>
          <text x="160" y="180" class="pd-label" text-anchor="middle" data-pd-run>Run 12"</text>
          <text x="306" y="128" class="pd-label" data-pd-risetxt>Rise 6"</text>
          <path d="M70 160 A50 50 0 0 0 68 148" class="pd-arc" data-pd-arc/>
          <text x="78" y="152" class="pd-label pd-label--gold" data-pd-angle>26.6°</text>
        </svg>
        <figcaption>Rise is measured vertically for every unit of horizontal run.</figcaption>
      </figure>
      <div class="result-stats result-stats--2">
        <div><span data-out="pitch">—</span><small>Pitch (rise / 12)</small></div>
        <div><span data-out="angle">—</span><small>Slope angle</small></div>
        <div><span data-out="multiplier">—</span><small>Slope multiplier</small></div>
        <div><span data-out="grade">—</span><small>Grade (rise ÷ run)</small></div>
        <div><span data-out="footprint">—</span><small>Footprint (sq ft)</small></div>
        <div><span data-out="area">—</span><small>Roof area (sq ft)</small></div>
        <div><span data-out="squares">—</span><small>Squares incl. waste</small></div>
        <div><span data-out="bundles">—</span><small>Shingle bundles</small></div>
      </div>
      <p class="pitch-class" data-out="class"></p>
      <a class="btn btn--gold btn--block" href="/free-roof-inspection/">Get Exact Measurements — Free Inspection</a>
      <p class="tool-disclaimer"><?= icon('info') ?> Assumes a simple roof where all planes share one pitch. Ridge cap, starter strip and extra waste for many valleys are not included.</p>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow prose">
    <h2>The Math Behind the Calculator</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th scope="col">Value</th><th scope="col">Formula</th><th scope="col">Units</th></tr></thead>
        <tbody>
          <tr><td>Pitch (x/12)</td><td>rise ÷ run × 12</td><td>inches of rise per 12 in. of run</td></tr>
          <tr><td>Slope angle</td><td>arctan(rise ÷ run)</td><td>degrees</td></tr>
          <tr><td>Rise from angle</td><td>tan(angle) × 12</td><td>inches per 12 in.</td></tr>
          <tr><td>Grade</td><td>rise ÷ run × 100</td><td>percent</td></tr>
          <tr><td>Slope multiplier</td><td>√(1 + (rise ÷ run)²)</td><td>unitless</td></tr>
          <tr><td>Footprint</td><td>(length + 2 × overhang) × (width + 2 × overhang)</td><td>sq ft (overhang converted from in. to ft ÷ 12)</td></tr>
          <tr><td>Roof area</td><td>footprint × slope multiplier</td><td>sq ft</td></tr>
          <tr><td>Squares</td><td>roof area × (1 + waste %) ÷ 100</td><td>1 square = 100 sq ft</td></tr>
          <tr><td>Bundles</td><td>squares × bundles per square, rounded up</td><td>bundles</td></tr>
        </tbody>
      </table>
    </div>
    <h3>Common pitches at a glance</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th scope="col">Pitch</th><th scope="col">Angle</th><th scope="col">Multiplier</th><th scope="col">Typical use</th></tr></thead>
        <tbody>
          <?php foreach ([2 => 'Low-slope; needs special underlayment or membrane', 4 => 'Lowest common for shingles (with extra underlayment)', 6 => 'Very common on Central Texas homes', 8 => 'Steeper; more labor and safety equipment', 10 => 'Steep; specialty staging', 12 => '45°; very steep'] as $r => $use): $m = sqrt(1 + ($r / 12) ** 2); ?>
          <tr><td><?= $r ?>/12</td><td><?= number_format(rad2deg(atan($r / 12)), 1) ?>°</td><td><?= number_format($m, 3) ?></td><td><?= e($use) ?></td></tr>
          <?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <div class="callout callout--warn"><strong>Measure safely:</strong> take pitch measurements from inside the attic or from a ladder at the gable end — never by walking the roof. A free inspection includes professional measurements.</div>
    <p>Ready to turn your measurements into a budget? Try the <a href="/tools/roof-replacement-cost-calculator/">roof replacement cost calculator</a>, or read about <a href="/services/asphalt-shingle-roofing-temple-tx/">asphalt shingle</a> and <a href="/services/metal-roofing-temple-tx/">metal roofing</a> options.</p>
    <?= faq_html($faqs, 'Roof Pitch FAQs') ?>
  </div>
</section>
<?php final_cta('Want Exact Roof Measurements? Book a Free Inspection.', '', '/tools/' . $toolSlug . '/'); ?>
<?php layout_end();
