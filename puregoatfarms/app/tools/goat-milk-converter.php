<?php
defined('PGF') || exit;
ob_start(); ?>
<div class="conv">
  <div class="conv__in">
    <div class="field"><label for="cv-val">Amount</label><input id="cv-val" type="number" min="0" step="any" value="8.6" inputmode="decimal"></div>
    <div class="field"><label for="cv-unit">From</label>
      <select id="cv-unit"><option value="lb" selected>Pounds (lb)</option><option value="kg">Kilograms (kg)</option><option value="oz">Ounces by weight (oz)</option><option value="gal">US gallons</option><option value="qt">US quarts</option><option value="pt">US pints</option><option value="cup">US cups</option><option value="l">Liters</option><option value="ml">Milliliters</option></select></div>
  </div>
  <div class="conv__grid" aria-live="polite" id="cv-out"></div>
</div>
<?php
$widget = ob_get_clean();
return [
    'title' => 'Goat Milk Converter — Pounds to Gallons, Liters & Cups | Pure Goat Farms',
    'desc'  => 'Convert goat milk pounds to gallons, quarts, liters and cups. Goat milk weighs about 8.6 lb per gallon — use this free converter for milk records and recipes.',
    'intro' => 'Dairy records are kept in pounds, recipes use cups and the rest of the world uses liters. Convert any goat milk amount between weight and volume in one step.',
    'widget' => $widget,
    'how' => '<h2>How much does a gallon of goat milk weigh?</h2>
<p>A US gallon of goat milk weighs about <strong>8.6 pounds</strong> (3.9 kg). That is slightly heavier than water (8.34 lb per gallon) because milk contains fat, protein, lactose and minerals. One liter of goat milk weighs about 1.03 kg.</p>
<figure><table><thead><tr><th>Weight</th><th>Volume</th></tr></thead><tbody><tr><td>1 lb</td><td>≈ 1.86 cups / 0.44 L</td></tr><tr><td>2.15 lb</td><td>≈ 1 quart</td></tr><tr><td>4.3 lb</td><td>≈ ½ gallon</td></tr><tr><td>8.6 lb</td><td>≈ 1 gallon / 3.79 L</td></tr></tbody></table></figure>
<p>Weighing milk is the quickest way to track production — see <a href="/how-much-milk-does-a-goat-produce-per-day/">how much milk does a goat produce per day</a>.</p>',
    'faq' => [
        ['How many pounds of goat milk is a gallon?', 'About 8.6 pounds per US gallon.'],
        ['How many liters is a pound of goat milk?', 'About 0.44 liters, or just under 2 cups.'],
    ],
    'posts' => ['how-much-milk-does-a-goat-produce-per-day', 'how-much-milk-can-a-goat-really-give-at-once'],
];
