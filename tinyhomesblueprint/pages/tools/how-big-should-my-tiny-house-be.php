<?php
$app = [
    '@context' => 'https://schema.org', '@type' => 'WebApplication',
    'name' => 'Tiny House Size Calculator', 'url' => abs_url($PATH),
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
// Style data for the suggestions (names, URLs and icons come from the route registry).
$styleData = [];
foreach ($ROUTES as $p => $r) if ($r['type'] === 'style') $styleData[basename($p)] = ['name' => $r['nav'], 'url' => $p, 'icon' => icon($r['icon'] ?? 'cabin')];
if (!function_exists('tool_seg')) { function tool_seg(string $name, array $opts, string $checked): void {
    foreach ($opts as $v => $l) echo '<label><input type="radio" name="' . e($name) . '" value="' . e($v) . '"' . ((string)$v === $checked ? ' checked' : '') . '><span>' . e($l) . '</span></label>';
} }
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Free tool</p>
    <h1>How Big Should My Tiny House Be?</h1>
    <p class="lead">Tell us who lives there and how you live, and this tiny house square footage calculator recommends a size range, breaks it down by zone and shows how it compares with trailer homes, the IRC tiny house limit and typical ADUs.</p>
    <ul class="hero-facts">
      <li>9 lifestyle questions</li>
      <li>Zone-by-zone breakdown</li>
      <li>Footprint &amp; style suggestions</li>
    </ul>
  </div>
</section>

<section class="section tool-sec">
  <div class="wrap">
    <form class="tool-shell" id="sz" novalidate>
      <div class="panel">
        <h2>Your household</h2>
        <p class="panel-intro">The result updates as you answer.</p>
        <div class="field-row">
          <div class="field">
            <label for="sz-adults">Adults</label>
            <div class="stepper"><button type="button" data-step="-1" data-for="sz-adults" aria-label="Fewer adults">&minus;</button><input type="number" id="sz-adults" name="adults" min="1" max="6" value="2" inputmode="numeric"><button type="button" data-step="1" data-for="sz-adults" aria-label="More adults">+</button></div>
          </div>
          <div class="field">
            <label for="sz-kids">Children</label>
            <div class="stepper"><button type="button" data-step="-1" data-for="sz-kids" aria-label="Fewer children">&minus;</button><input type="number" id="sz-kids" name="kids" min="0" max="6" value="0" inputmode="numeric"><button type="button" data-step="1" data-for="sz-kids" aria-label="More children">+</button></div>
          </div>
        </div>
        <div class="field">
          <span class="label" id="sz-pets-l">Pets</span>
          <div class="seg" role="radiogroup" aria-labelledby="sz-pets-l"><?php tool_seg('pets', ['0' => 'None', '1' => 'One', '2' => 'Two or more'], '1'); ?></div>
        </div>
        <div class="field">
          <span class="label" id="sz-wfh-l">Work from home</span>
          <div class="seg" role="radiogroup" aria-labelledby="sz-wfh-l"><?php tool_seg('wfh', ['none' => 'No', 'some' => 'Occasionally', 'full' => 'Full-time'], 'some'); ?></div>
        </div>

        <p class="group-title">How you live</p>
        <div class="field">
          <span class="label" id="sz-cook-l">Cooking style</span>
          <div class="seg" role="radiogroup" aria-labelledby="sz-cook-l"><?php tool_seg('cook', ['light' => 'Simple meals', 'daily' => 'Cook most days', 'serious' => 'Serious cook / bake'], 'daily'); ?></div>
        </div>
        <div class="field">
          <span class="label" id="sz-store-l">Stuff and storage</span>
          <div class="seg" role="radiogroup" aria-labelledby="sz-store-l"><?php tool_seg('store', ['min' => 'Minimalist', 'avg' => 'Average', 'lots' => 'Lots of gear / hobbies'], 'avg'); ?></div>
        </div>
        <div class="field">
          <span class="label" id="sz-guest-l">Overnight guests</span>
          <div class="seg" role="radiogroup" aria-labelledby="sz-guest-l"><?php tool_seg('guests', ['rare' => 'Rarely', 'some' => 'A few times a year', 'often' => 'Often'], 'some'); ?></div>
        </div>
        <div class="field">
          <span class="label" id="sz-occ-l">How often you live there</span>
          <div class="seg" role="radiogroup" aria-labelledby="sz-occ-l"><?php tool_seg('occ', ['full' => 'Full-time', 'part' => 'Part-time / weekends'], 'full'); ?></div>
        </div>
        <div class="field">
          <span class="label" id="sz-mob-l">Wheels or foundation?</span>
          <div class="seg" role="radiogroup" aria-labelledby="sz-mob-l"><?php tool_seg('mob', ['wheels' => 'On wheels', 'foundation' => 'On a foundation'], 'wheels'); ?></div>
        </div>
      </div>

      <div class="panel result-panel">
        <p class="result-label">Recommended size</p>
        <div aria-live="polite" aria-atomic="true">
          <p class="result-big" id="sz-total">260 - 420 sq ft</p>
          <p class="result-sub" id="sz-sub">Total living space, including any lofts</p>
        </div>
        <div class="mini-stats">
          <div><b id="sz-fp">8.5 x 28 ft</b><span id="sz-fp-l">suggested footprint</span></div>
          <div><b id="sz-main">-</b><span id="sz-main-l">main floor + loft</span></div>
        </div>
        <ul class="zone-list" id="sz-zones"></ul>
        <ul class="flag-list" id="sz-flags"></ul>
        <p class="result-note">A planning guide based on typical space needs, not a code minimum. Check local zoning for minimum dwelling sizes.</p>
      </div>
    </form>

    <div class="two-panels">
      <div class="panel">
        <h2 class="panel-title">How your size compares</h2>
        <p class="panel-intro">Your range against common tiny house reference sizes.</p>
        <div class="compare" id="sz-compare"></div>
        <div class="compare-axis" id="sz-axis" aria-hidden="true"></div>
      </div>
      <div class="panel">
        <h2 class="panel-title">Styles that fit this size</h2>
        <p class="panel-intro">Tiny house styles that work well at your size and setup.</p>
        <div class="style-picks" id="sz-styles" style="grid-template-columns:1fr"></div>
      </div>
    </div>
  </div>
</section>
<script type="application/json" id="sz-style-data"><?= json_encode($styleData, JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) ?></script>

<section class="section tool-prose">
  <div class="narrow prose">
    <h2>How big should a tiny house be?</h2>
    <p>For one person, a well-designed tiny house can work at 150 to 250 sq ft. Most couples living full-time are comfortable at 250 to 400 sq ft, and a family with children usually needs 400 to 700 sq ft or more. The right tiny house square footage depends less on a magic number than on how you live: whether you work from home, how much you cook, how much gear you own and how often people stay over. This calculator from Tiny Homes Blueprint turns those answers into a size range you can design around.</p>

    <h2>How the size calculator works</h2>
    <p>Instead of guessing a single number, the calculator adds up the space each part of daily life needs, then adds about 10% for walls and circulation. Each zone has a low and high allowance, which is why you get a range rather than one figure.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Zone</th><th class="num">Starting allowance</th><th>What changes it</th></tr></thead>
      <tbody>
        <tr><td>Sleeping</td><td class="num">45&ndash;100 sq ft</td><td>Number of adults; +30&ndash;55 sq ft per child</td></tr>
        <tr><td>Kitchen</td><td class="num">25&ndash;90 sq ft</td><td>Cooking style and household size</td></tr>
        <tr><td>Bathroom</td><td class="num">30&ndash;45 sq ft</td><td>Grows to 45&ndash;70 sq ft for four or more people</td></tr>
        <tr><td>Living &amp; dining</td><td class="num">40&ndash;70 sq ft</td><td>Household size, guests and pets</td></tr>
        <tr><td>Work</td><td class="num">0&ndash;60 sq ft</td><td>None, a fold-down desk or a full-time office nook</td></tr>
        <tr><td>Storage</td><td class="num">15&ndash;90 sq ft</td><td>How much you own; reduced for part-time use</td></tr>
        <tr><td>Walls &amp; circulation</td><td class="num">+10%</td><td>Added to the total of all zones</td></tr>
      </tbody>
    </table></div>
    <p>If you choose a house on wheels, the calculator assumes the adults sleep in a loft, which is how most tiny houses on wheels fit a real bed. It shows that loft space separately from the main floor, because a trailer limits the main floor to 8.5 ft wide.</p>

    <h3>Reference sizes used in the comparison</h3>
    <ul>
      <li><strong>8.5 x 24 ft tiny house on wheels: about 204 sq ft.</strong> A common trailer length; lofts add usable space above.</li>
      <li><strong>IRC Appendix AQ tiny house: 400 sq ft or less</strong>, not counting lofts. Where adopted, this appendix relaxes ceiling height, loft and stair rules for small homes.</li>
      <li><strong>Typical ADU: about 400&ndash;800 sq ft.</strong> Many cities cap backyard units somewhere in this range; check your local limit.</li>
      <li><strong>Tiny Homes Blueprint plans: 700 sq ft.</strong> Our current plans, <a href="/plans/plan-12-2418/">Plan 12-2418</a> and <a href="/plans/plan-12-2417/">Plan 12-2417</a>, are both 700 sq ft on a 20 x 38 ft footprint.</li>
    </ul>

    <h3>Typical tiny house square footage by household</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>Household</th><th class="num">Typical range</th><th>Common setup</th></tr></thead>
      <tbody>
        <tr><td>One person, part-time</td><td class="num">120&ndash;200 sq ft</td><td>Shed conversion or small cabin, sleeping loft</td></tr>
        <tr><td>One person, full-time</td><td class="num">150&ndash;250 sq ft</td><td>16&ndash;24 ft tiny house on wheels</td></tr>
        <tr><td>Couple, full-time</td><td class="num">250&ndash;400 sq ft</td><td>24&ndash;30 ft trailer with loft, or a 16 x 24 ft cottage</td></tr>
        <tr><td>Couple, both working from home</td><td class="num">320&ndash;480 sq ft</td><td>Foundation home with an office nook</td></tr>
        <tr><td>Family of four</td><td class="num">450&ndash;750 sq ft</td><td>Two or three bedrooms, or one bedroom plus kids' loft</td></tr>
      </tbody>
    </table></div>

    <h2>How to use your result</h2>
    <ol>
      <li><strong>Design to the low end, budget for the high end.</strong> Every square foot you cut saves money to build, heat and cool. Start near the bottom of your range and only add space where a layout feels tight.</li>
      <li><strong>Test it on paper.</strong> Draw your footprint in the <a href="/tools/tiny-house-layout-planner/">tiny house layout planner</a> and drop in your actual bed, sofa and kitchen to see whether the space works.</li>
      <li><strong>Price it.</strong> Plug the size into the <a href="/tools/tiny-house-cost-calculator/">tiny house cost calculator</a> to see what it will cost to build.</li>
      <li><strong>Check the rules.</strong> Some counties set a minimum house size, and ADUs often have a maximum. Our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning guide</a> explains what to ask.</li>
    </ol>

    <h2>Tips for getting more from less space</h2>
    <ul class="check-list">
      <li><strong>Go up, not out.</strong> A sleeping loft can add 60&ndash;100 sq ft of usable space without enlarging the footprint. See <a href="/tiny-house-plans-with-loft/">tiny house plans with a loft</a>.</li>
      <li><strong>Make rooms do two jobs.</strong> A dining table that doubles as a desk, or a flex room with a retractable wall like the one in our 700 sq ft plans, beats adding a dedicated room.</li>
      <li><strong>Build storage into everything.</strong> Stairs with drawers, benches with lids and toe-kick drawers often hold more than a closet.</li>
      <li><strong>Plan for the next five years.</strong> A couple planning children, or someone who will need single-level living later, should size for that now. Moving walls in a tiny house is harder than it sounds.</li>
      <li><strong>Mind the weight on wheels.</strong> Every extra foot of trailer adds roughly 400&ndash;600 lb once finished. Check yours with the <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a>.</li>
    </ul>

    <?php faq_block([
        ['What is the average size of a tiny house?', '<p>Most tiny houses on wheels are between about 150 and 300 sq ft of main floor, plus loft space. Tiny houses on foundations tend to be larger, commonly 300 to 600 sq ft. The IRC defines a tiny house as 400 sq ft or less, excluding lofts.</p>'],
        ['How many square feet does one person need in a tiny house?', '<p>A single person can live comfortably in 150 to 250 sq ft with a well-planned layout and a sleeping loft. Add space if you work from home full-time or own a lot of gear.</p>'],
        ['Is 400 sq ft too small for a family?', '<p>It can work for a family of three or four with lofts and very efficient storage, but most families are more comfortable at 500 to 700 sq ft, especially with two bedrooms. Use the calculator above with your household to check.</p>'],
        ['Do lofts count toward tiny house square footage?', '<p>Usually not. Building codes, including IRC Appendix AQ, typically measure habitable floor area without lofts, so a 250 sq ft house with a 100 sq ft loft is still treated as 250 sq ft. Lofts still count as living space in daily use, which is why this calculator shows them separately.</p>'],
        ['What size trailer do I need for a tiny house?', '<p>Divide your main-floor size by 8.5 to get the trailer length. For example, 204 sq ft needs a 24 ft trailer. Most tiny house trailers run 16 to 32 ft. See the <a href="/blog/tiny-house-trailer-size-guide/">tiny house trailer size guide</a> for weight and height limits.</p>'],
    ]); ?>

    <h2>Related tools and guides</h2>
    <ul class="related-links">
      <li><a href="/tools/tiny-house-layout-planner/"><?= icon('layout') ?> Layout planner</a></li>
      <li><a href="/tools/tiny-house-cost-calculator/"><?= icon('cost') ?> Cost calculator</a></li>
      <li><a href="/tools/tiny-house-style-quiz/"><?= icon('quiz') ?> Tiny house style quiz</a></li>
      <li><a href="/tiny-cottage-plans/"><?= icon('cottage') ?> Tiny cottage plans</a></li>
      <li><a href="/adu-plans/"><?= icon('adu') ?> ADU plans</a></li>
      <li><a href="/tiny-house-on-wheels-plans/"><?= icon('wheels') ?> Tiny house on wheels plans</a></li>
      <li><a href="/blog/tiny-house-layout-ideas/"><?= icon('book') ?> Tiny house layout ideas</a></li>
      <li><a href="/tiny-house-plans/"><?= icon('file') ?> All tiny house plans</a></li>
    </ul>
  </div>
</section>

<?php cta_band('Found your size? Find your plan.', 'Tiny Homes Blueprint plans are drawn around real furniture and clearances. Browse the plans or ask us to resize one for your household.'); ?>
<?php page_end(['scripts' => ['/assets/js/tools/size-calculator.js']]); ?>
