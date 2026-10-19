<?php
defined('PGF') || exit;
ob_start(); ?>
<div class="tool__grid">
  <div class="tool__fields">
    <div class="field"><label for="my-daily">Daily milk yield</label><input id="my-daily" type="number" min="0.1" max="40" step="0.1" value="3" inputmode="decimal"></div>
    <div class="field"><label for="my-unit">Unit</label>
      <select id="my-unit"><option value="liters">Liters</option><option value="gallons">US gallons</option><option value="pounds">Pounds</option></select></div>
    <div class="field"><span class="field__label" id="my-milkings-l">Milkings per day</span>
      <div class="seg" role="radiogroup" aria-labelledby="my-milkings-l">
        <button type="button" role="radio" aria-checked="false" data-v="1">Once</button>
        <button type="button" role="radio" aria-checked="true" class="is-on" data-v="2">Twice</button>
        <button type="button" role="radio" aria-checked="false" data-v="3">Three times</button>
      </div></div>
    <div class="field"><label for="my-share">Milk reserved for kids: <output id="my-share-out">0%</output></label><input id="my-share" type="range" min="0" max="75" step="5" value="0"></div>
  </div>
  <div class="tool__out" aria-live="polite">
    <p class="out-label">You can expect to collect</p>
    <p class="out-big" id="my-per">—</p>
    <p class="out-sub" id="my-cups">per milking</p>
    <div class="day-split" id="my-split" aria-hidden="true"></div>
    <dl class="out-stats">
      <div><dt>Kept per day</dt><dd id="my-kept">—</dd></div>
      <div><dt>To the kids</dt><dd id="my-kids">—</dd></div>
      <div><dt>Per week</dt><dd id="my-week">—</dd></div>
    </dl>
  </div>
</div>
<?php
$widget = ob_get_clean();
return [
    'title' => 'Goat Milk Yield Calculator — Milk Per Milking | Pure Goat Farms',
    'desc'  => 'Free goat milk yield calculator: split a goat\'s daily milk into what you collect per milking, in liters, gallons, pounds and cups, with milk reserved for kids.',
    'intro' => 'How much milk will you actually get in the pail each time? Enter your goat\'s daily yield and milking schedule to see the amount per milking, per day and per week.',
    'widget' => $widget,
    'how' => '<h2>How the goat milk yield calculator works</h2>
<p>The calculator takes your goat\'s total daily production, removes the share you leave for nursing kids, and divides the rest by the number of milkings. It then converts the result between liters, US gallons, pounds and cups using goat milk\'s weight of about 8.6 pounds per gallon.</p>
<p>For example, a doe giving 3 liters a day, milked twice with no kids nursing, gives about 1.5 liters (just over 6 cups) per milking.</p>
<h2>Typical daily yields to try</h2>
<ul><li><strong>Nigerian Dwarf:</strong> about 1–1.5 liters (2–3 lb) a day</li><li><strong>Nubian:</strong> about 2.5–3 liters (5–7 lb)</li><li><strong>Alpine or Saanen:</strong> about 3.5–4.5 liters (7–10 lb)</li></ul>
<p>Not sure what your goat produces? See <a href="/how-much-milk-can-a-goat-really-give-at-once/">how much milk a goat can really give at once</a> or estimate her full season with the <a href="/tools/goat-milk-production-estimator/">Goat Milk Production Estimator</a>.</p>',
    'faq' => [
        ['How much milk does a goat give per milking?', 'Most dairy goats milked twice a day give about 2–4 pounds (roughly 1–2 quarts) per milking. Nigerian Dwarfs typically give 1–1.5 pounds and top Saanens can give 5–6 pounds at peak.'],
        ['Does milking once a day give more milk per milking?', 'Yes, each milking is larger because milk has built up for 24 hours, but total daily milk is usually 15–25% lower than with twice-a-day milking.'],
        ['How many cups are in a gallon of goat milk?', 'A US gallon holds 16 cups. A doe giving a gallon a day on twice-daily milking gives about 8 cups per milking.'],
    ],
    'posts' => ['how-much-milk-can-a-goat-really-give-at-once', 'how-often-do-you-milk-a-goat'],
];
