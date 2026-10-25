<?php
$app = [
    '@context' => 'https://schema.org', '@type' => 'WebApplication',
    'name' => 'Tiny House Trailer Weight Calculator', 'url' => abs_url($PATH),
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
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Free tool</p>
    <h1>Tiny House Trailer Weight Calculator</h1>
    <p class="lead">How much does a tiny house weigh? Pick your trailer length, framing, siding, roof and interior, add water and belongings, and get an estimated total weight checked against common trailer GVWR ratings, with tongue weight and tow vehicle guidance.</p>
    <ul class="hero-facts">
      <li>Component-by-component estimate</li>
      <li>7,000 to 21,000 lb GVWR check</li>
      <li>Tongue and pin weight</li>
    </ul>
  </div>
</section>

<section class="section tool-sec">
  <div class="wrap">
    <form class="tool-shell" id="tw" novalidate>
      <div class="panel">
        <h2>Your build</h2>
        <p class="panel-intro">Change any option to update the weight estimate.</p>
        <div class="field">
          <label for="tw-len">Trailer deck length: <span class="range-out" id="tw-len-out">24</span> ft</label>
          <input type="range" id="tw-len" name="len" min="16" max="32" step="1" value="24">
          <div class="range-ends" aria-hidden="true"><span>16 ft</span><span>32 ft</span></div>
        </div>
        <div class="field">
          <span class="label" id="tw-type-l">Trailer type</span>
          <div class="seg" role="radiogroup" aria-labelledby="tw-type-l"><?php tool_seg('type', ['bumper' => 'Bumper pull', 'gooseneck' => 'Gooseneck'], 'bumper'); ?></div>
        </div>

        <p class="group-title">Construction</p>
        <div class="field">
          <span class="label" id="tw-frame-l">Wall framing</span>
          <div class="seg" role="radiogroup" aria-labelledby="tw-frame-l"><?php tool_seg('frame', ['2x4' => 'Wood 2x4', '2x6' => 'Wood 2x6', 'steel' => 'Steel stud', 'sips' => 'SIPs'], '2x4'); ?></div>
        </div>
        <div class="field">
          <span class="label" id="tw-siding-l">Siding</span>
          <div class="seg" role="radiogroup" aria-labelledby="tw-siding-l"><?php tool_seg('siding', ['vinyl' => 'Vinyl', 'wood' => 'Wood / cedar', 'metal' => 'Metal', 'fiber' => 'Fiber cement'], 'wood'); ?></div>
        </div>
        <div class="field-row">
          <div class="field">
            <span class="label" id="tw-roof-l">Roofing</span>
            <div class="seg" role="radiogroup" aria-labelledby="tw-roof-l"><?php tool_seg('roof', ['metal' => 'Metal', 'shingle' => 'Shingle'], 'metal'); ?></div>
          </div>
          <div class="field">
            <span class="label" id="tw-int-l">Interior walls</span>
            <div class="seg" role="radiogroup" aria-labelledby="tw-int-l"><?php tool_seg('interior', ['pine' => 'Pine T&G', 'drywall' => 'Drywall'], 'pine'); ?></div>
          </div>
        </div>
        <div class="field">
          <span class="label" id="tw-loft-l">Lofts</span>
          <div class="seg" role="radiogroup" aria-labelledby="tw-loft-l"><?php tool_seg('lofts', ['0' => 'None', '1' => 'One loft', '2' => 'Two lofts'], '1'); ?></div>
        </div>

        <p class="group-title">Payload</p>
        <div class="field">
          <label for="tw-water">Fresh water carried: <span class="range-out" id="tw-water-out">0</span> gallons</label>
          <input type="range" id="tw-water" name="water" min="0" max="100" step="5" value="0" aria-describedby="tw-water-h">
          <small id="tw-water-h">Water weighs 8.34 lb per gallon. Most people tow with tanks empty.</small>
        </div>
        <div class="field">
          <label for="tw-contents">Belongings and furniture: <span class="range-out" id="tw-contents-out">1,000</span> lb</label>
          <input type="range" id="tw-contents" name="contents" min="0" max="4000" step="100" value="1000" aria-describedby="tw-contents-h">
          <small id="tw-contents-h">Clothes, kitchenware, books, loose furniture and tools. 1,000&ndash;2,000 lb is typical for full-time living.</small>
        </div>
      </div>

      <div class="panel result-panel">
        <p class="result-label">Estimated total weight</p>
        <div aria-live="polite" aria-atomic="true">
          <p class="result-big" id="tw-total">12,800 lb</p>
          <p class="result-sub" id="tw-sub">Likely range 11,500 - 14,100 lb</p>
        </div>
        <div class="gauge" aria-hidden="true">
          <div class="gauge-track" id="tw-gauge"></div>
        </div>
        <div class="mini-stats">
          <div><b id="tw-plf">530 lb</b><span>per linear foot of trailer</span></div>
          <div><b id="tw-tongue">1,300 - 1,900 lb</b><span id="tw-tongue-l">tongue weight (10-15%)</span></div>
        </div>
        <ul class="flag-list" id="tw-flags"></ul>
        <p class="result-note">An estimate for planning only. Weigh the finished house at a certified truck scale before towing, and never exceed the trailer, axle, tire or hitch ratings.</p>
      </div>
    </form>

    <div class="two-panels">
      <div class="panel">
        <h2 class="panel-title">Trailer GVWR check</h2>
        <p class="panel-intro">Margin is how much of each rating would be left at your estimated weight. Aim for at least 10&ndash;15% to spare.</p>
        <div class="table-wrap mt-0">
          <table class="gvwr-table">
            <thead><tr><th scope="col">GVWR</th><th scope="col">Typical setup</th><th scope="col" class="num">Margin</th></tr></thead>
            <tbody id="tw-gvwr"></tbody>
          </table>
        </div>
      </div>
      <div class="panel">
        <h2 class="panel-title">Where the weight comes from</h2>
        <p class="panel-intro">Midpoint estimate by component.</p>
        <ul class="weight-bk" id="tw-bk"></ul>
      </div>
    </div>
  </div>
</section>

<section class="section tool-prose">
  <div class="narrow prose">
    <h2>How much does a tiny house weigh?</h2>
    <p>A finished tiny house on wheels typically weighs about <strong>400 to 600 lb per linear foot</strong> of trailer, including the trailer itself. That puts a 20 ft house around 9,000 to 12,000 lb and a 24 ft house around 10,000 to 14,000 lb. Light materials and a minimalist load can come in under that; drywall, fiber cement siding, full water tanks and a houseful of belongings can push it well over. Because tiny house trailer weight is the number that decides which trailer, axles and truck you need, it is worth estimating early. This calculator from Tiny Homes Blueprint does exactly that.</p>

    <h2>How the weight calculator works</h2>
    <p>Rather than one flat rule of thumb, the calculator adds up each major component using typical material weights, scaled by trailer length. Then it gives a range of plus or minus 10% to account for differences in design, window count and finishes.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Component</th><th>Assumption used</th></tr></thead>
      <tbody>
        <tr><td>Trailer</td><td>About 125 lb per ft + 300 lb (bumper pull); 140 lb per ft + 700 lb (gooseneck)</td></tr>
        <tr><td>Floor system</td><td>Insulated floor framing and subfloor, about 35 lb per ft</td></tr>
        <tr><td>Wall framing</td><td>Including sheathing and insulation: steel stud 50, 2x4 70, SIPs 85, 2x6 90 lb per ft</td></tr>
        <tr><td>Siding</td><td>Vinyl 14, metal 25, wood or cedar 40, fiber cement 70 lb per ft</td></tr>
        <tr><td>Roof</td><td>Framing and sheathing plus metal (about 1 lb/sq ft) or shingles (about 2.7 lb/sq ft)</td></tr>
        <tr><td>Interior finish</td><td>Pine tongue and groove about 40, drywall about 60 lb per ft</td></tr>
        <tr><td>Kitchen, bath and systems</td><td>Cabinets, fixtures, appliances, wiring, plumbing and water heater, about 1,250 lb + 28 lb per ft</td></tr>
        <tr><td>Lofts</td><td>About 450 lb each for framing, decking and stairs or ladder</td></tr>
        <tr><td>Water and belongings</td><td>Water at 8.34 lb per gallon, plus your contents allowance</td></tr>
      </tbody>
    </table></div>

    <h2>What GVWR means and how to read your result</h2>
    <p><strong>GVWR (gross vehicle weight rating)</strong> is the maximum the loaded trailer may weigh, including the trailer itself. It is set by the weakest link: axles, tires, frame or coupler. Your finished, loaded tiny house must stay under it. The table above shows how much margin each common rating would leave and highlights the smallest rating that keeps at least 10% to spare at the high end of your estimate.</p>
    <ul>
      <li><strong>7,000 lb</strong> &ndash; tandem 3,500 lb axles. Rarely enough for a finished, furnished tiny house; better suited to shells, very light builds or trailers under 16 ft.</li>
      <li><strong>10,000 lb</strong> &ndash; tandem 5,200 lb axles. Workable for 16&ndash;20 ft houses built with light materials.</li>
      <li><strong>14,000 lb</strong> &ndash; tandem 7,000 lb axles. A common choice for 24&ndash;28 ft houses.</li>
      <li><strong>16,000 lb</strong> &ndash; tandem 8,000 lb or triple 5,200 lb axles, for longer or heavier builds.</li>
      <li><strong>21,000 lb</strong> &ndash; triple 7,000 lb axles, usually on gooseneck trailers for 30 ft and up.</li>
    </ul>
    <p>Also check tongue weight. A bumper-pull trailer should carry roughly 10&ndash;15% of its weight on the hitch, and a gooseneck puts roughly 15&ndash;25% on the pin in the truck bed. Too little tongue weight can cause dangerous sway.</p>

    <h2>Choosing a tow vehicle</h2>
    <p>Tow ratings vary widely by make, model, engine, axle ratio, cab and bed configuration, so treat any general guidance as a starting point only. Check the owner's manual and the door-jamb sticker for the towing capacity, gross combined weight rating (GCWR), payload and hitch rating of the exact truck you plan to use. Many owners hire a professional tiny house mover for long trips rather than buying a heavy-duty truck they rarely need. Some states also require a special license for heavy combinations, so check your state's rules before you tow.</p>

    <h2>Tips to keep a tiny house light</h2>
    <ul class="check-list">
      <li><strong>Choose light skins.</strong> Metal roofing and metal or vinyl siding can save 1,000 lb or more over shingles and fiber cement on a 24 ft house.</li>
      <li><strong>Skip drywall.</strong> Thin pine or plywood paneling is lighter and handles road vibration without cracking.</li>
      <li><strong>Tow empty.</strong> A full 50 gallon tank adds about 420 lb. Fill up at your destination.</li>
      <li><strong>Plan the layout for balance.</strong> Put heavy items like the kitchen and bathroom near the axles. Sketch it in the <a href="/tools/tiny-house-layout-planner/">layout planner</a>.</li>
      <li><strong>Buy the trailer last.</strong> Finalize materials, then order a trailer rated with margin to spare. Our <a href="/blog/tiny-house-trailer-size-guide/">tiny house trailer size guide</a> covers lengths, widths and heights.</li>
    </ul>
    <p>Ready to plan a mobile build? Browse <a href="/tiny-house-on-wheels-plans/">tiny house on wheels plans</a>, estimate the budget with the <a href="/tools/tiny-house-cost-calculator/">cost calculator</a>, or ask Tiny Homes Blueprint about adapting a design for a trailer.</p>

    <?php faq_block([
        ['How much does a 24 ft tiny house weigh?', '<p>A typical finished 24 ft tiny house on wheels weighs about 10,000 to 14,000 lb including the trailer, depending on materials, lofts and how much you carry. That is why a 24 ft build usually needs at least a 14,000 lb GVWR trailer, and heavier builds a 16,000 lb one.</p>'],
        ['How much does a tiny house trailer weigh by itself?', '<p>An empty purpose-built tiny house trailer usually weighs about 2,000 to 5,000 lb depending on length, axle rating and steel. Goosenecks are heavier for their length because of the neck.</p>'],
        ['What happens if my tiny house is over the trailer GVWR?', '<p>Overloading a trailer can cause tire blowouts, bent axles, brake failure and frame damage, and it may void insurance. If your estimate is close to or over the GVWR, reduce weight or choose a higher-rated trailer before you build.</p>'],
        ['Can a half-ton truck tow a tiny house?', '<p>Some can tow small, light tiny houses, but many tiny houses are heavier than a half-ton truck is rated to tow. Check the exact truck\'s towing capacity, payload and GCWR in the owner\'s manual and compare them with your estimated weight and tongue weight.</p>'],
        ['How accurate is this tiny house weight estimate?', '<p>It is a planning estimate based on typical material weights, so a real house can vary by 10% or more. The only way to know the true weight is to weigh the finished, loaded house at a certified scale.</p>'],
    ]); ?>

    <h2>Related tools and guides</h2>
    <ul class="related-links">
      <li><a href="/blog/tiny-house-trailer-size-guide/"><?= icon('book') ?> Tiny house trailer size guide</a></li>
      <li><a href="/tiny-house-on-wheels-plans/"><?= icon('wheels') ?> Tiny house on wheels plans</a></li>
      <li><a href="/tiny-house-plans-with-loft/"><?= icon('loft') ?> Plans with a loft</a></li>
      <li><a href="/tools/tiny-house-cost-calculator/"><?= icon('cost') ?> Cost calculator</a></li>
      <li><a href="/tools/how-big-should-my-tiny-house-be/"><?= icon('size') ?> Size calculator</a></li>
      <li><a href="/tools/off-grid-solar-calculator/"><?= icon('solar') ?> Off-grid solar calculator</a></li>
      <li><a href="/blog/how-to-build-a-tiny-house/"><?= icon('book') ?> How to build a tiny house</a></li>
      <li><a href="/blog/tiny-house-zoning-laws/"><?= icon('shield') ?> Tiny house zoning laws</a></li>
    </ul>
  </div>
</section>

<?php cta_band('Planning a tiny house on wheels?', 'Tiny Homes Blueprint can help you adapt a plan for a trailer and keep the weight in check. Tell us about your build.', 'Talk to us about your build', '/contact/'); ?>
<?php page_end(['scripts' => ['/assets/js/tools/trailer-weight.js']]); ?>
