<?php
defined('PGF') || exit;
ob_start(); ?>
<div class="tool__grid">
  <div class="tool__fields">
    <div class="field"><label for="ch-amount">Cheese you want to make</label><input id="ch-amount" type="number" min="0.1" max="500" step="0.1" value="2" inputmode="decimal"></div>
    <div class="field"><label for="ch-unit">Cheese unit</label><select id="ch-unit"><option value="pounds" selected>Pounds</option><option value="ounces">Ounces</option><option value="kilograms">Kilograms</option></select></div>
    <div class="field"><label for="ch-type">Cheese style</label><select id="ch-type"><option value="1.0">Soft chevre or fresh cheese</option><option value="1.5" selected>Semi-soft goat cheese</option><option value="2.0">Firm or aged cheese</option></select></div>
    <div class="field"><label for="ch-yield">Milk per goat per day</label><select id="ch-yield"><option value="0.5">0.5 gallon, low yield</option><option value="0.75" selected>0.75 gallon, average home dairy goat</option><option value="1">1 gallon, strong producer</option><option value="1.5">1.5 gallons, excellent producer</option></select></div>
    <div class="field"><label for="ch-days">Milk collection window</label><select id="ch-days"><option value="1">1 day</option><option value="2" selected>2 days</option><option value="3">3 days</option><option value="7">1 week</option></select></div>
    <div class="field"><label for="ch-kids">Milk reserved for kids</label><select id="ch-kids"><option value="0">None</option><option value="0.25">About 25%</option><option value="0.5">About 50%</option></select></div>
  </div>
  <div class="tool__out" aria-live="polite">
    <p class="out-label">Lactating goats needed</p>
    <p class="out-big" id="ch-goats">—</p>
    <div class="goat-row" id="ch-icons" aria-hidden="true"></div>
    <p class="out-sub" id="ch-detail"></p>
    <dl class="out-stats">
      <div><dt>Milk needed</dt><dd id="ch-milk">—</dd></div>
      <div><dt>Usable per goat</dt><dd id="ch-pergoat">—</dd></div>
      <div><dt>Milk in cups</dt><dd id="ch-cups">—</dd></div>
    </dl>
  </div>
</div>
<?php
$widget = ob_get_clean();
return [
    'title' => 'Goat Cheese Herd Calculator — How Many Goats for Cheese? | Pure Goat Farms',
    'desc'  => 'Free goat cheese herd calculator: work out how many lactating goats you need for a batch of chevre, semi-soft or aged goat cheese, with milk reserved for kids.',
    'intro' => 'Start with the cheese, then the milk, then the goats. Tell us how much cheese you want and how your does produce, and we\'ll estimate how many milking goats you need.',
    'widget' => $widget,
    'how' => '<h2>How the cheese herd calculator works</h2>
<p>Each cheese style needs a different amount of milk per finished pound: about 1 gallon for fresh chevre, 1.5 gallons for semi-soft cheese and around 2 gallons for firm or aged cheese. The calculator multiplies your target by that ratio, then divides by the usable milk each goat produces during your collection window after the kids\' share.</p>
<p>Real yields depend on butterfat, recipe, draining time and season — high-butterfat breeds like Nigerian Dwarfs and Nubians give noticeably more cheese per gallon.</p>
<p>The full planning guide, with sample scenarios, is in <a href="/how-many-goats-do-you-need-to-make-cheese/">how many goats do you need to make cheese</a>.</p>',
    'faq' => [
        ['How much cheese does a gallon of goat milk make?', 'Roughly 1 pound of fresh chevre, or about half to two-thirds of a pound of firm or aged cheese, depending on butterfat and recipe.'],
        ['Can one goat make enough milk for cheese?', 'Yes. One average home dairy doe giving about three-quarters of a gallon a day can supply small weekly batches of soft cheese. Two does make regular cheese-making much easier.'],
    ],
    'posts' => ['how-many-goats-do-you-need-to-make-cheese', 'best-dairy-goat-breeds-for-milk'],
];
