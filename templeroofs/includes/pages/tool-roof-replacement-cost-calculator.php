<?php
defined('TR_ROOT') || exit;
$costs = require TR_INC . '/calculator-costs.php';
$crumbs = [['Roofing Tools', '/tools/'], [$tool['name'], '/tools/' . $toolSlug . '/']];
$faqs = [
    ['q' => 'How accurate is this roof replacement cost calculator?', 'a' => 'It is a planning tool. It uses your inputs and clearly labeled illustrative Central Texas cost assumptions to produce a range. Real prices depend on the exact roof measurements, materials chosen, decking condition, access, code requirements and current supplier pricing, which only an on-site inspection can confirm.'],
    ['q' => 'Why does the calculator ask for floor area instead of roof area?', 'a' => 'Most homeowners know their home\'s square footage but not their roof area. The calculator converts floor area to a roof footprint (adding a typical overhang), then applies a slope multiplier for your pitch to estimate the actual roof surface. If you know your roof area, use the Roof Pitch & Area Calculator for a more direct measurement.'],
    ['q' => 'What is a roofing square?', 'a' => 'A square is 100 square feet of roof surface. Roofing materials and labor are usually priced per square.'],
    ['q' => 'Does the estimate include insurance or my deductible?', 'a' => 'No. The calculator estimates a total project cost only. If a replacement is part of an insurance claim, your insurer determines what is covered, and Texas law requires you to pay your deductible.'],
];
layout_start([
    'title' => 'Roof Replacement Cost Calculator — Temple, TX', 'description' => 'Estimate roof replacement cost in Temple, TX: roof area, squares, materials, labor, tear-off and decking. Free planning calculator.',
    'path' => '/tools/' . $toolSlug . '/', 'crumbs' => $crumbs, 'schema' => [schema_faq($faqs)], 'scripts' => ['js/tools.js'], 'body_class' => 'page-tool',
]);
page_hero(['h1' => 'Temple Roof Replacement Cost Calculator', 'lead' => 'Estimate a planning range for a new roof based on your home size, pitch, material and roof complexity. Results update instantly.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true, 'eyebrow' => 'Free roofing tool']);
?>
<script type="application/json" id="cost-config"><?= json_encode($costs, JSON_HEX_TAG | JSON_HEX_AMP) ?></script>
<section class="section section--tight">
  <div class="container tool-layout" data-tool="cost">
    <form class="tool-panel" novalidate data-cost-form>
      <h2 class="tool-panel__title"><?= icon('home') ?> Your home &amp; roof</h2>
      <div class="form-grid">
        <div class="field">
          <label for="c-area">Home floor area (sq ft) <span class="req">*</span></label>
          <input type="number" id="c-area" name="area" min="400" max="20000" step="10" value="2000" inputmode="numeric" required aria-describedby="c-area-help c-area-err">
          <p class="field__help" id="c-area-help">Total heated/living area, all floors.</p>
          <p class="field__error" id="c-area-err" hidden></p>
        </div>
        <div class="field">
          <label for="c-stories">Number of stories</label>
          <select id="c-stories" name="stories"><option value="1" selected>1 story</option><option value="2">2 stories</option><option value="3">3 stories</option></select>
        </div>
        <div class="field">
          <label for="c-pitch">Estimated roof pitch</label>
          <select id="c-pitch" name="pitch">
            <?php foreach ([3 => 'Low (3/12)', 4 => 'Low (4/12)', 5 => 'Moderate (5/12)', 6 => 'Moderate (6/12) — common', 7 => 'Moderate-steep (7/12)', 8 => 'Steep (8/12)', 9 => 'Steep (9/12)', 10 => 'Very steep (10/12)', 12 => 'Very steep (12/12)'] as $v => $l): ?>
            <option value="<?= $v ?>"<?= $v === 6 ? ' selected' : '' ?>><?= e($l) ?></option>
            <?php endforeach; ?>
          </select>
          <p class="field__help">Not sure? Use the <a href="/tools/roof-pitch-calculator/">pitch calculator</a>.</p>
        </div>
        <div class="field">
          <label for="c-material">Roofing material</label>
          <select id="c-material" name="material">
            <?php foreach ($costs['materials'] as $k => $m): ?><option value="<?= e($k) ?>"<?= $k === 'architectural' ? ' selected' : '' ?>><?= e($m['label']) ?></option><?php endforeach; ?>
          </select>
        </div>
        <div class="field">
          <label for="c-layers">Existing roofing layers to remove</label>
          <select id="c-layers" name="layers"><option value="0">None (new deck / already removed)</option><option value="1" selected>1 layer</option><option value="2">2 layers</option><option value="3">3 layers</option></select>
        </div>
        <div class="field">
          <label for="c-complexity">Roof complexity</label>
          <select id="c-complexity" name="complexity">
            <?php foreach ($costs['complexity'] as $k => $c): ?><option value="<?= e($k) ?>"<?= $k === 'moderate' ? ' selected' : '' ?>><?= e($c['label']) ?></option><?php endforeach; ?>
          </select>
        </div>
        <div class="field">
          <label for="c-decking">Estimated decking replacement: <output id="c-decking-out" for="c-decking">10%</output></label>
          <input type="range" id="c-decking" name="decking" min="0" max="100" step="5" value="10">
          <p class="field__help">Share of the roof deck that may need new sheathing. Unknown until tear-off; 0–15% is common on sound roofs.</p>
        </div>
        <div class="field">
          <label for="c-waste">Waste allowance (%)</label>
          <input type="number" id="c-waste" name="waste" min="0" max="30" step="1" placeholder="Auto" inputmode="numeric" aria-describedby="c-waste-help c-waste-err">
          <p class="field__help" id="c-waste-help">Leave blank to use the default for your roof complexity.</p>
          <p class="field__error" id="c-waste-err" hidden></p>
        </div>
      </div>
      <button type="button" class="btn btn--ghost btn--sm" data-reset>Reset to defaults</button>
    </form>

    <div class="tool-results" aria-live="polite" data-cost-results>
      <div class="result-hero">
        <p class="result-hero__label">Estimated project range</p>
        <p class="result-hero__value" data-out="total">—</p>
        <p class="result-hero__sub" data-out="material-label"></p>
      </div>
      <div class="result-stats">
        <div><span data-out="roof-area">—</span><small>Est. roof surface (sq ft)</small></div>
        <div><span data-out="squares">—</span><small>Roofing squares (incl. waste)</small></div>
        <div><span data-out="per-square">—</span><small>Approx. cost per square</small></div>
      </div>
      <div class="table-wrap">
        <table class="breakdown">
          <thead><tr><th scope="col">Cost line</th><th scope="col">Low</th><th scope="col">High</th></tr></thead>
          <tbody data-breakdown></tbody>
        </table>
      </div>
      <div class="bar-chart" data-bars aria-hidden="true"></div>
      <a class="btn btn--gold btn--block" href="/free-roof-inspection/?concern=replacement"><?= icon('clipboard-check') ?> Get an Accurate Quote — Free Roof Inspection</a>
      <p class="tool-disclaimer"><?= icon('info') ?> Planning estimate only — not a quote or binding estimate. Based on illustrative Central Texas assumptions last reviewed <?= e($costs['last_reviewed']) ?>. An on-site inspection is required for actual pricing.</p>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="container container--narrow prose">
    <h2>How the Calculator Works</h2>
    <p>Every number above is calculated from your inputs using the formulas below. Nothing is hard-coded.</p>
    <ol>
      <li><strong>Roof footprint</strong> = floor area ÷ stories × <?= e($costs['overhang_factor']) ?> (adds roughly 10% for eave and rake overhangs).</li>
      <li><strong>Slope multiplier</strong> = √(1 + (rise ÷ 12)²). A 6/12 roof has a multiplier of about 1.118.</li>
      <li><strong>Roof surface area</strong> = footprint × slope multiplier.</li>
      <li><strong>Squares ordered</strong> = roof area × (1 + waste %) ÷ 100.</li>
      <li><strong>Materials</strong> = squares ordered × (material cost + accessories cost per square).</li>
      <li><strong>Labor</strong> = (roof area ÷ 100) × labor per square × pitch factor × story factor × complexity factor.</li>
      <li><strong>Tear-off &amp; disposal</strong> = (roof area ÷ 100) × layers × tear-off cost per square.</li>
      <li><strong>Decking</strong> = roof area × decking % ÷ 32 sq ft per sheet × cost per sheet.</li>
    </ol>
    <h3>Current assumptions (illustrative)</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th scope="col">Material</th><th scope="col">Material / square</th><th scope="col">Labor / square</th></tr></thead>
        <tbody>
          <?php foreach ($costs['materials'] as $m): ?>
          <tr><td><?= e($m['label']) ?></td><td>$<?= e($m['material'][0]) ?>–$<?= e($m['material'][1]) ?></td><td>$<?= e($m['labor'][0]) ?>–$<?= e($m['labor'][1]) ?></td></tr>
          <?php endforeach; ?>
          <tr><td>Accessories (underlayment, drip edge, ridge, flashing, vents)</td><td colspan="2">$<?= e($costs['accessories_per_square'][0]) ?>–$<?= e($costs['accessories_per_square'][1]) ?> per square</td></tr>
          <tr><td>Tear-off &amp; disposal</td><td colspan="2">$<?= e($costs['tearoff_per_square_per_layer'][0]) ?>–$<?= e($costs['tearoff_per_square_per_layer'][1]) ?> per square, per layer</td></tr>
          <tr><td>Decking replacement</td><td colspan="2">$<?= e($costs['decking_per_sheet'][0]) ?>–$<?= e($costs['decking_per_sheet'][1]) ?> per 4×8 sheet installed</td></tr>
          <tr><td>Pitch labor factor</td><td colspan="2">×1.00 below 7/12, ×1.10 at 7–8/12, ×1.22 at 9–10/12, ×1.35 at 11/12+</td></tr>
          <tr><td>Story labor factor</td><td colspan="2">×1.00 one story, ×1.10 two stories, ×1.20 three stories</td></tr>
        </tbody>
      </table>
    </div>
    <h3>What is not included</h3>
    <ul>
      <li>Permits or inspection fees, if your jurisdiction or HOA requires them.</li>
      <li>Structural repairs beyond deck sheathing (rafters, trusses, fascia boards).</li>
      <li>Gutters, skylights, chimney rebuilding, solar panel removal and reinstallation.</li>
      <li>Attic ventilation upgrades beyond standard vents, and insulation work.</li>
      <li>Insurance deductibles, financing costs and taxes.</li>
    </ul>
    <div class="callout">Building codes generally limit roofs to two layers, and most quality replacements remove all existing layers. If you have three layers, expect a full tear-off. See <a href="/services/roof-replacement-temple-tx/">roof replacement in Temple</a> for more on the process.</div>
    <?= faq_html($faqs, 'Cost Calculator FAQs') ?>
  </div>
</section>
<?php final_cta('Get an Accurate Quote — Free Roof Inspection', 'Calculators estimate; inspections measure. We will measure your roof, check the decking and ventilation, and give you a written estimate with no obligation.', '/tools/' . $toolSlug . '/'); ?>
<?php layout_end();
