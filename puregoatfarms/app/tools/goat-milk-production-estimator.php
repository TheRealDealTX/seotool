<?php
defined('PGF') || exit;
ob_start(); ?>
<div class="tool__fields tool__fields--row">
  <div class="field"><label for="pe-breed">Breed</label>
    <select id="pe-breed">
      <option value="saanen">Saanen</option><option value="alpine">Alpine</option><option value="toggenburg">Toggenburg</option>
      <option value="lamancha">LaMancha</option><option value="oberhasli">Oberhasli</option><option value="nubian" selected>Nubian</option>
      <option value="mini">Mini dairy (cross)</option><option value="nigerian">Nigerian Dwarf</option>
    </select></div>
  <div class="field"><label for="pe-age">Lactation</label>
    <select id="pe-age"><option value="0.78">First freshener</option><option value="0.9">Second lactation</option><option value="1" selected>Mature doe (3rd+)</option></select></div>
  <div class="field"><label for="pe-dim">Days in milk today <span class="opt">(optional)</span></label><input id="pe-dim" type="number" min="1" max="600" placeholder="e.g. 45" inputmode="numeric"></div>
  <div class="field"><label for="pe-today">Today's milk, lb <span class="opt">(optional)</span></label><input id="pe-today" type="number" min="0.1" max="30" step="0.1" placeholder="e.g. 7.5" inputmode="decimal"></div>
</div>
<div class="tool__chart">
  <svg id="pe-chart" viewBox="0 0 720 300" role="img" aria-label="Projected lactation curve in pounds per day"></svg>
  <div class="chart-tip" id="pe-tip" hidden></div>
</div>
<dl class="out-stats out-stats--4" aria-live="polite">
  <div><dt>Peak</dt><dd id="pe-peak">—</dd></div>
  <div><dt>Average per day</dt><dd id="pe-avg">—</dd></div>
  <div><dt>305-day season</dt><dd id="pe-season">—</dd></div>
  <div><dt>Per week (avg)</dt><dd id="pe-week">—</dd></div>
</dl>
<p class="muted small" id="pe-note">Curve based on typical breed averages for healthy does milked twice daily. Add today's numbers to calibrate it to your doe.</p>
<?php
$widget = ob_get_clean();
return [
    'title' => 'Goat Milk Production Estimator — Milk Per Day by Breed | Pure Goat Farms',
    'desc'  => 'Estimate goat milk production per day and per season by breed. See a full 305-day lactation curve for Saanen, Alpine, Nubian, LaMancha and Nigerian Dwarf goats.',
    'intro' => 'Pick a breed to see a full lactation curve — when your doe will peak, how much milk she gives per day, and what the whole season adds up to. Add today\'s milk weight to calibrate it to your own goat.',
    'widget' => $widget,
    'how' => '<h2>How this goat milk production estimate works</h2>
<p>Goat milk production follows a predictable lactation curve: it climbs after kidding, peaks around six to eight weeks, then slowly declines. This estimator draws that curve using a standard dairy lactation model (Wood\'s curve) scaled to typical 305-day totals for each breed, then adjusts for the doe\'s age — first fresheners usually give about 20% less than mature does.</p>
<p>If you enter how many days your doe has been in milk and what she gave today, the tool rescales the whole curve to match her, so the season total reflects <em>your</em> goat rather than a breed average.</p>
<h2>Typical 305-day totals used</h2>
<figure><table><thead><tr><th>Breed</th><th>Season total</th><th>Average per day</th></tr></thead><tbody>
<tr><td>Saanen</td><td>≈2,700 lb</td><td>≈8.9 lb</td></tr><tr><td>Alpine</td><td>≈2,450 lb</td><td>≈8.0 lb</td></tr><tr><td>Toggenburg</td><td>≈2,250 lb</td><td>≈7.4 lb</td></tr><tr><td>LaMancha</td><td>≈2,200 lb</td><td>≈7.2 lb</td></tr><tr><td>Oberhasli</td><td>≈2,150 lb</td><td>≈7.0 lb</td></tr><tr><td>Nubian</td><td>≈1,900 lb</td><td>≈6.2 lb</td></tr><tr><td>Mini dairy</td><td>≈1,200 lb</td><td>≈3.9 lb</td></tr><tr><td>Nigerian Dwarf</td><td>≈780 lb</td><td>≈2.6 lb</td></tr>
</tbody></table></figure>
<p>For the full breakdown, read <a href="/how-much-milk-does-a-goat-produce-per-day/">how much milk does a goat produce per day</a>.</p>',
    'faq' => [
        ['How much milk does a goat produce per day?', 'Most full-size dairy goats average about 6–9 pounds (0.7–1 gallon) per day over a lactation, with more at peak. Nigerian Dwarfs average about 2–3 pounds a day.'],
        ['When does goat milk production peak?', 'Usually about 6 to 8 weeks after kidding. After the peak, production declines slowly — a few percent per month in a well-managed doe.'],
        ['How long is a goat lactation?', 'A standard dairy lactation is about 305 days, followed by a dry period of roughly 60 days before the next kidding. Some does are milked through for much longer.'],
    ],
    'posts' => ['how-much-milk-does-a-goat-produce-per-day', 'best-dairy-goat-breeds-for-milk', 'how-to-increase-goat-milk-production'],
];
