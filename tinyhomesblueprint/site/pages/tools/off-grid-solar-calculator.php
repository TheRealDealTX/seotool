<?php
$app = [
    '@context' => 'https://schema.org', '@type' => 'WebApplication',
    'name' => 'Off-Grid Solar Calculator for Tiny Houses', 'url' => abs_url($PATH),
    'description' => $ROUTE['description'],
    'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any',
    'browserRequirements' => 'Requires JavaScript',
    'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
    'publisher' => ['@id' => SITE_URL . '/#org'],
];
page_start([
    'breadcrumbs' => [['Home', '/'], ['Free Tools', '/tools/'], [$ROUTE['nav'], null]],
    'styles' => ['/assets/css/tools.css'],
    'schema' => [$app],
]);
if (!function_exists('tool_seg')) { function tool_seg(string $name, array $opts, string $checked): void {
    foreach ($opts as $v => $l) echo '<label><input type="radio" name="' . e($name) . '" value="' . e($v) . '"' . ((string)$v === $checked ? ' checked' : '') . '><span>' . e($l) . '</span></label>';
} }
$regions = [
    '6'   => 'Desert Southwest (AZ, NM, NV, inland SoCal)',
    '5.5' => 'Mountain West (CO, UT, ID high desert)',
    '5'   => 'Texas, Oklahoma, California coast',
    '4.5' => 'Southeast and Florida',
    '4'   => 'Midwest and Mid-Atlantic',
    '3.5' => 'Northeast, Great Lakes, Pacific Northwest',
    '3'   => 'Alaska or heavily shaded sites',
];
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Free tool</p>
    <h1>Off-Grid Solar Calculator for Tiny Houses</h1>
    <p class="lead">Size a tiny house solar system from the ground up. List your appliances, choose your sun hours, backup days and battery type, and get your daily energy use, solar array size, number of panels, battery bank, inverter and a rough budget.</p>
    <ul class="hero-facts">
      <li>Editable appliance list</li>
      <li>LiFePO4 or lead-acid batteries</li>
      <li>12, 24 or 48 V systems</li>
    </ul>
  </div>
</section>

<section class="section tool-sec">
  <div class="wrap">
    <form class="tool-shell solar-shell" id="sol" novalidate>
      <div class="panel">
        <h2>1. What will you power?</h2>
        <p class="panel-intro">Edit watts, hours per day and quantity to match your appliances. For fridges, enter the hours the compressor actually runs, not 24.</p>
        <div class="table-wrap mt-0" style="border:0;overflow:visible">
          <table class="appl-table">
            <thead><tr><th class="c-name" scope="col">Appliance</th><th class="c-w num" scope="col">Watts</th><th class="c-h num" scope="col">Hrs/day</th><th class="c-q num" scope="col">Qty</th><th class="c-wh" scope="col">Wh/day</th><th class="c-x" scope="col"><span class="sr">Remove</span></th></tr></thead>
            <tbody id="sol-rows"></tbody>
          </table>
        </div>
        <div class="appl-total"><span>Daily total</span><span id="sol-sum">0 Wh</span></div>
        <div class="appl-add">
          <label for="sol-preset" class="sr">Appliance to add</label>
          <select id="sol-preset"></select>
          <button type="button" class="btn btn-outline btn-sm" id="sol-add">Add appliance</button>
          <button type="button" class="btn btn-outline btn-sm" id="sol-custom">Add custom row</button>
        </div>

        <h2 class="mt-2">2. Your site and system</h2>
        <div class="field">
          <label for="sol-region">Region</label>
          <select id="sol-region">
            <?php foreach ($regions as $v => $l): ?><option value="<?= e($v) ?>"<?= $v === '4.5' ? ' selected' : '' ?>><?= e($l) ?> &ndash; <?= e($v) ?> h</option><?php endforeach; ?>
            <option value="custom">Custom</option>
          </select>
        </div>
        <div class="field">
          <label for="sol-psh">Peak sun hours per day: <span class="range-out" id="sol-psh-out">4.5</span></label>
          <input type="range" id="sol-psh" name="psh" min="3" max="6" step="0.25" value="4.5" aria-describedby="sol-psh-h">
          <small id="sol-psh-h">Annual averages. For year-round living in the north, size for winter, which can be half these figures.</small>
        </div>
        <div class="field">
          <label for="sol-days">Days of autonomy (cloudy-day backup): <span class="range-out" id="sol-days-out">2</span></label>
          <input type="range" id="sol-days" name="days" min="1" max="5" step="1" value="2">
          <div class="range-ends" aria-hidden="true"><span>1 day</span><span>5 days</span></div>
        </div>
        <div class="field-row">
          <div class="field">
            <span class="label" id="sol-bat-l">Battery type</span>
            <div class="seg seg-sm" role="radiogroup" aria-labelledby="sol-bat-l"><?php tool_seg('bat', ['lfp' => 'LiFePO4', 'lead' => 'Lead-acid'], 'lfp'); ?></div>
          </div>
          <div class="field">
            <span class="label" id="sol-v-l">System voltage</span>
            <div class="seg seg-sm" role="radiogroup" aria-labelledby="sol-v-l"><?php tool_seg('volt', ['12' => '12 V', '24' => '24 V', '48' => '48 V'], '24'); ?></div>
          </div>
        </div>
      </div>

      <div class="panel result-panel">
        <p class="result-label">Daily energy use</p>
        <div aria-live="polite" aria-atomic="true">
          <p class="result-big" id="sol-wh">1,850 Wh/day</p>
          <p class="result-sub" id="sol-sub">About 55 kWh per month</p>
        </div>
        <div class="mini-stats">
          <div><b id="sol-array">1,600 W</b><span id="sol-array-l">solar array (4 x 400 W panels)</span></div>
          <div><b id="sol-batt">9.2 kWh</b><span id="sol-batt-l">battery bank (385 Ah at 24 V)</span></div>
          <div><b id="sol-inv">1,000 W</b><span id="sol-inv-l">inverter (peak load x 1.25)</span></div>
          <div><b id="sol-cc">60 A</b><span id="sol-cc-l">MPPT charge controller</span></div>
        </div>
        <ul class="result-rows">
          <li><span>Equipment (DIY install)</span><b id="sol-cost">-</b></li>
          <li><span>Professionally installed</span><b id="sol-cost-pro">-</b></li>
        </ul>
        <ul class="flag-list" id="sol-flags"></ul>
        <p class="result-note">Rough sizing for planning. A solar installer or electrician should confirm wire sizes, breakers and code compliance for your system.</p>
      </div>
    </form>
  </div>
</section>

<section class="section tool-prose">
  <div class="narrow prose">
    <h2>How to size tiny house solar</h2>
    <p>Off-grid solar sizing starts with one number: how many watt-hours you use per day. Everything else, from the number of panels to the size of the battery bank, follows from it. A frugal tiny house with LED lights, a 12 V fridge, laptops and a water pump might use 1 to 2 kWh a day. Add a mini-split, induction cooking or an electric water heater and that can jump to 5 to 15 kWh, which changes the system from a modest DIY project into a serious investment. This off-grid solar calculator from Tiny Homes Blueprint shows you where your energy goes, so you can decide what to power with the sun and what to run on propane or wood.</p>

    <h2>How the calculator works</h2>
    <ol>
      <li><strong>Daily energy:</strong> each appliance's watts &times; hours per day &times; quantity, added together.</li>
      <li><strong>Solar array:</strong> daily energy &divide; peak sun hours &divide; 0.75, allowing about 25% for real-world losses from heat, wiring, charge controller and inverter efficiency, dust and panel angle. The result is rounded up to whole 400 W panels.</li>
      <li><strong>Battery bank:</strong> daily energy &times; days of autonomy &divide; usable depth of discharge, shown in kWh and in amp-hours at your system voltage.</li>
      <li><strong>Inverter:</strong> your peak load &times; 1.25, rounded up to a common inverter size. Peak load assumes all smaller loads can run together, plus your single largest heavy appliance.</li>
    </ol>
    <div class="table-wrap"><table>
      <thead><tr><th>Assumption</th><th>Value used</th></tr></thead>
      <tbody>
        <tr><td>System losses</td><td>~25% (array sized at daily use &divide; sun hours &divide; 0.75)</td></tr>
        <tr><td>Panel size</td><td>400 W</td></tr>
        <tr><td>LiFePO4 usable depth of discharge</td><td>80% (rated 80&ndash;90%; we use the conservative end)</td></tr>
        <tr><td>Lead-acid usable depth of discharge</td><td>50%</td></tr>
        <tr><td>Inverter headroom</td><td>Peak load &times; 1.25</td></tr>
        <tr><td>Charge controller</td><td>Array watts &divide; battery voltage &times; 1.25</td></tr>
        <tr><td>Equipment prices</td><td>Panels $0.50&ndash;0.90/W, LiFePO4 $250&ndash;450/kWh, lead-acid $150&ndash;300/kWh, inverter $0.35&ndash;0.75/W, plus $800&ndash;2,500 for controller, wiring and racking</td></tr>
        <tr><td>Professional installation</td><td>About 1.6&ndash;2.2&times; equipment cost</td></tr>
      </tbody>
    </table></div>
    <p>For a typical full-time tiny house, an installed off-grid system usually lands somewhere around $8,000 to $30,000, which is the range our <a href="/tools/tiny-house-cost-calculator/">tiny house cost calculator</a> uses.</p>

    <h3>Typical daily use for off-grid tiny houses</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>Household type</th><th class="num">Daily use</th><th>What it usually runs</th></tr></thead>
      <tbody>
        <tr><td>Weekend cabin</td><td class="num">0.5&ndash;1 kWh</td><td>Lights, phones, a fan and a water pump</td></tr>
        <tr><td>Frugal full-time</td><td class="num">1&ndash;2.5 kWh</td><td>Adds a 12 V fridge, laptops, Wi-Fi and a TV</td></tr>
        <tr><td>Comfortable full-time</td><td class="num">3&ndash;6 kWh</td><td>Adds a washer, microwave and some mini-split use</td></tr>
        <tr><td>All-electric</td><td class="num">8&ndash;15+ kWh</td><td>Induction cooking, daily heating or cooling, electric hot water</td></tr>
      </tbody>
    </table></div>

    <h2>How to use your result</h2>
    <ul>
      <li><strong>Cut loads before adding panels.</strong> Every 1,000 Wh you remove from your daily use saves roughly 300&ndash;350 W of panels and 2.5 kWh or more of battery. Heavy heating loads are the first place to look.</li>
      <li><strong>Size for your worst month.</strong> If you live there year-round, rerun the calculator with winter sun hours (often 2&ndash;3 in the northern US). Many off-grid homes add a small generator for long cloudy spells instead of oversizing the battery.</li>
      <li><strong>Choose the voltage early.</strong> 12 V suits small systems under about 1,500 W of inverter. 24 V or 48 V keeps current and wire sizes manageable for anything larger.</li>
      <li><strong>Plan the roof.</strong> A 400 W panel is roughly 3.7 x 5.6 ft. A tiny house roof may only fit 4 to 8 panels, so larger arrays often go on a ground mount. Check your design against our <a href="/tiny-house-on-wheels-plans/">tiny house on wheels plans</a> or <a href="/small-cabin-plans/">small cabin plans</a>.</li>
    </ul>

    <h2>Tips for an efficient off-grid tiny house</h2>
    <ul class="check-list">
      <li><strong>Heat water and food with propane.</strong> A propane tankless water heater and cooktop remove the two biggest resistive loads from your solar budget.</li>
      <li><strong>Insulate and air-seal well.</strong> A tight, well-insulated shell needs far less heating and cooling. 2x6 walls or SIPs help, though they add weight on a trailer; check with the <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a>.</li>
      <li><strong>Buy efficient appliances.</strong> A DC compressor fridge, LED lighting and a laptop instead of a desktop can halve a typical daily load.</li>
      <li><strong>Pick LiFePO4 if you can.</strong> Lithium iron phosphate batteries cost more up front but last several times as many cycles as lead-acid, need no maintenance and can be discharged deeper.</li>
      <li><strong>Mind the water.</strong> A 12 V pump uses little power, but a deep well pump can be one of the biggest surge loads in the house.</li>
    </ul>
    <p>Building on rural land? Read our guide to <a href="/blog/how-to-build-a-tiny-house/">building a tiny house</a> for how utilities fit into the build sequence, and see the <a href="/a-frame-house-plans/">A-frame</a> and <a href="/small-farmhouse-plans/">small farmhouse</a> pages for off-grid-friendly designs.</p>

    <?php faq_block([
        ['How many solar panels does a tiny house need?', '<p>Most off-grid tiny houses need about 4 to 10 400 W panels (1,600 to 4,000 W). A frugal home using about 1.5 kWh a day in a sunny region may get by with 2 or 3 panels, while one running a mini-split or induction cooktop may need 10 or more.</p>'],
        ['How much battery storage does an off-grid tiny house need?', '<p>Multiply your daily use by the number of cloudy days you want to ride through, then divide by the usable depth of discharge. For 2 kWh a day and 2 days of backup on LiFePO4, that is about 5 kWh of battery.</p>'],
        ['Can I run air conditioning on solar in a tiny house?', '<p>Yes, an efficient mini-split can run on solar, but cooling and heating are usually the largest loads in an off-grid house. Expect to need a bigger array, a larger battery and a 24 V or 48 V system.</p>'],
        ['Should I use a 12 V, 24 V or 48 V system?', '<p>12 V is simple and fine for small systems with inverters under about 1,500 W. For larger systems, 24 V or 48 V cut the current in half or by three-quarters, which means thinner cables, less heat and better efficiency.</p>'],
        ['How much does an off-grid solar system cost for a tiny house?', '<p>Equipment for a small system can start around $3,000 to $6,000 if you install it yourself. A professionally installed system sized for full-time living typically runs about $8,000 to $30,000 depending on loads and battery size.</p>'],
    ]); ?>

    <h2>Related tools and guides</h2>
    <ul class="related-links">
      <li><a href="/tools/tiny-house-cost-calculator/"><?= icon('cost') ?> Tiny house cost calculator</a></li>
      <li><a href="/tools/tiny-house-trailer-weight-calculator/"><?= icon('weight') ?> Trailer weight calculator</a></li>
      <li><a href="/tools/how-big-should-my-tiny-house-be/"><?= icon('size') ?> Size calculator</a></li>
      <li><a href="/tiny-house-on-wheels-plans/"><?= icon('wheels') ?> Tiny house on wheels plans</a></li>
      <li><a href="/small-cabin-plans/"><?= icon('cabin') ?> Small cabin plans</a></li>
      <li><a href="/shipping-container-home-plans/"><?= icon('container') ?> Shipping container homes</a></li>
      <li><a href="/blog/how-much-does-a-tiny-house-cost/"><?= icon('book') ?> How much a tiny house costs</a></li>
      <li><a href="/blog/tiny-house-zoning-laws/"><?= icon('shield') ?> Tiny house zoning laws</a></li>
    </ul>
  </div>
</section>

<?php cta_band('Designing an off-grid tiny home?', 'Tiny Homes Blueprint plans can be adapted for solar, propane and composting systems. Ask us about your site.', 'Ask about an off-grid plan', '/contact/'); ?>
<?php page_end(['scripts' => ['/assets/js/tools/solar-calculator.js']]); ?>
