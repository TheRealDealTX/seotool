<?php
defined('PGF') || exit;
ob_start(); ?>
<div class="feed-groups">
  <fieldset class="feed-group"><legend>Milking does</legend>
    <div class="field"><label for="fd-m-n">How many</label><input id="fd-m-n" type="number" min="0" max="500" value="2" inputmode="numeric"></div>
    <div class="field"><label for="fd-m-w">Avg weight (lb)</label><input id="fd-m-w" type="number" min="30" max="300" value="140" inputmode="numeric"></div>
    <div class="field"><label for="fd-m-milk">Milk each, lb/day</label><input id="fd-m-milk" type="number" min="0" max="25" step="0.5" value="7" inputmode="decimal"></div>
  </fieldset>
  <fieldset class="feed-group"><legend>Dry does &amp; wethers</legend>
    <div class="field"><label for="fd-d-n">How many</label><input id="fd-d-n" type="number" min="0" max="500" value="1" inputmode="numeric"></div>
    <div class="field"><label for="fd-d-w">Avg weight (lb)</label><input id="fd-d-w" type="number" min="30" max="300" value="130" inputmode="numeric"></div>
  </fieldset>
  <fieldset class="feed-group"><legend>Bucks</legend>
    <div class="field"><label for="fd-b-n">How many</label><input id="fd-b-n" type="number" min="0" max="100" value="0" inputmode="numeric"></div>
    <div class="field"><label for="fd-b-w">Avg weight (lb)</label><input id="fd-b-w" type="number" min="30" max="350" value="180" inputmode="numeric"></div>
  </fieldset>
  <fieldset class="feed-group feed-group--opt"><legend>Prices <span class="opt">(optional)</span></legend>
    <div class="field"><label for="fd-bale">Bale weight (lb)</label><input id="fd-bale" type="number" min="10" max="1500" value="50" inputmode="numeric"></div>
    <div class="field"><label for="fd-bale-p">Price per bale ($)</label><input id="fd-bale-p" type="number" min="0" step="0.5" value="12" inputmode="decimal"></div>
    <div class="field"><label for="fd-bag-p">Grain, per 50-lb bag ($)</label><input id="fd-bag-p" type="number" min="0" step="0.5" value="22" inputmode="decimal"></div>
  </fieldset>
</div>
<div class="feed-out" aria-live="polite">
  <div class="feed-tile"><span class="feed-tile__icon"><?= icon('hay') ?></span><p class="out-label">Hay per day</p><p class="out-big" id="fd-hay">—</p><p class="out-sub" id="fd-hay-m"></p></div>
  <div class="feed-tile"><span class="feed-tile__icon"><?= icon('leaf') ?></span><p class="out-label">Grain per day</p><p class="out-big" id="fd-grain">—</p><p class="out-sub" id="fd-grain-m"></p></div>
  <div class="feed-tile"><span class="feed-tile__icon"><?= icon('pail') ?></span><p class="out-label">Water per day</p><p class="out-big" id="fd-water">—</p><p class="out-sub">Keep it clean and unlimited</p></div>
  <div class="feed-tile feed-tile--dark"><span class="feed-tile__icon"><?= icon('chart') ?></span><p class="out-label">Est. monthly feed cost</p><p class="out-big" id="fd-cost">—</p><p class="out-sub" id="fd-cost-s"></p></div>
</div>
<?php
$widget = ob_get_clean();
return [
    'title' => 'Goat Feed Calculator — Hay, Grain & Water Per Day | Pure Goat Farms',
    'desc'  => 'Free goat feed calculator: estimate how much hay, grain and water your goats need per day and per month — milking does, dry does, wethers and bucks — plus feed cost.',
    'intro' => 'How much hay does a goat eat? Enter your herd and get a daily and monthly estimate for hay, grain and water, with an optional monthly feed budget.',
    'widget' => $widget,
    'how' => '<h2>How much hay does a goat eat per day?</h2>
<p>Goats eat roughly <strong>2.5–4% of their body weight in dry matter</strong> each day. This calculator uses about 2.5% for dry does, wethers and bucks, and about 3.5% for milking does, whose appetite rises with production. A 140-lb milker therefore eats around 5 lb of hay a day, a 130-lb wether a little over 3 lb. Allow extra for waste — goats are notoriously picky.</p>
<h2>How much grain does a milking goat need?</h2>
<p>A common rule of thumb is <strong>1 lb of dairy ration for every 3 lb of milk</strong>, split across milkings. Dry does, wethers and bucks on good forage usually need little or no grain, except in late pregnancy, breeding season or cold weather. Introduce grain changes gradually.</p>
<h2>How much water does a goat drink?</h2>
<p>About 1 gallon per 100 lb of body weight for a dry goat, plus roughly 1.5 gallons of extra water for every gallon of milk produced. Milkers in hot weather can drink 3–4 gallons a day or more.</p>
<p>Feeding for milk? Read <a href="/how-to-increase-goat-milk-production/">how to increase goat milk production</a>.</p>',
    'faq' => [
        ['How much hay does a goat eat per day?', 'Most goats eat about 2.5–4% of body weight in hay or equivalent forage per day — roughly 3–5 lb for a full-size goat. Milking does eat at the top of that range.'],
        ['How much does it cost to feed a goat per month?', 'It varies widely by region and hay price, but a full-size goat on purchased hay commonly costs about $20–$50 per month in hay, plus grain for milkers. Use the calculator with your local prices.'],
        ['How many bales of hay does a goat need for winter?', 'A full-size goat eating about 4 lb a day needs around 120 lb a month — two to three small 50-lb square bales per month, more with waste.'],
    ],
    'posts' => ['how-to-increase-goat-milk-production', 'how-much-milk-does-a-goat-produce-per-day'],
];
