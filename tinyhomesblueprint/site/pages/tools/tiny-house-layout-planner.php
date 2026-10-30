<?php
$app = [
    '@context' => 'https://schema.org', '@type' => 'WebApplication',
    'name' => 'Tiny House Layout Planner', 'url' => abs_url($PATH),
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
$presets = ['8.5x20' => '8.5 x 20 ft trailer', '8.5x24' => '8.5 x 24 ft trailer', '8.5x28' => '8.5 x 28 ft trailer', '12x24' => '12 x 24 ft cabin', '16x24' => '16 x 24 ft cottage', '20x38' => '20 x 38 ft (our 700 sq ft plans)'];
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Free tool</p>
    <h1>Tiny House Layout Planner</h1>
    <p class="lead">Sketch a tiny house layout to scale in your browser. Pick a footprint, drop in beds, kitchens, showers and stairs at their real sizes, drag them around a 1 ft grid and see how much open floor you have left. Save it as an image when you are done.</p>
    <ul class="hero-facts">
      <li>Real furniture dimensions</li>
      <li>Snaps to 6 in</li>
      <li>Works with mouse, touch and keyboard</li>
    </ul>
  </div>
</section>

<section class="section tool-sec">
  <div class="wrap planner" id="lp">
    <div class="planner-side">
      <div class="panel">
        <h2>1. Set the footprint</h2>
        <div class="field">
          <label for="lp-preset">Preset size</label>
          <select id="lp-preset">
            <?php foreach ($presets as $v => $l): ?><option value="<?= e($v) ?>"<?= $v === '8.5x24' ? ' selected' : '' ?>><?= e($l) ?></option><?php endforeach; ?>
            <option value="custom">Custom size</option>
          </select>
        </div>
        <div class="dims">
          <label for="lp-w">Width (ft)<input type="number" id="lp-w" min="6" max="30" step="0.5" value="8.5" inputmode="decimal"></label>
          <span class="x" aria-hidden="true">&times;</span>
          <label for="lp-l">Length (ft)<input type="number" id="lp-l" min="8" max="60" step="0.5" value="24" inputmode="decimal"></label>
        </div>
      </div>
      <div class="panel">
        <h2>2. Add rooms &amp; furniture</h2>
        <p class="hint" style="margin-top:-4px">Tap an item to drop it in the plan, then drag it into place. Sizes are width &times; depth in feet.</p>
        <div class="palette" id="lp-palette" role="group" aria-label="Items to add"></div>
      </div>
    </div>

    <div class="planner-main">
      <div class="planner-bar">
        <span class="sel-name" id="lp-sel" aria-live="polite">Nothing selected</span>
        <label class="wall-len" id="lp-wall-wrap" for="lp-wall-len">Length <input type="number" id="lp-wall-len" min="1" max="60" step="0.5" value="6" style="width:80px;padding:.4em .5em"> ft</label>
        <button type="button" class="btn btn-outline" id="lp-rotate" disabled>Rotate <span class="kbd">R</span></button>
        <button type="button" class="btn btn-outline" id="lp-dup" disabled>Duplicate</button>
        <button type="button" class="btn btn-outline" id="lp-del" disabled>Delete</button>
      </div>
      <div class="planner-stage">
        <svg id="lp-svg" xmlns="http://www.w3.org/2000/svg" role="application" aria-label="Tiny house floor plan canvas. Select an item, then use arrow keys to move it, R to rotate and Delete to remove it." aria-describedby="lp-help"></svg>
      </div>
      <div class="planner-stats" aria-live="polite">
        <div><b id="lp-area">204</b><span>sq ft footprint</span></div>
        <div><b id="lp-occ">0%</b><span>floor occupied</span></div>
        <div><b id="lp-open">204</b><span>sq ft open floor</span></div>
        <div id="lp-ov-box"><b id="lp-ov">0</b><span>overlapping items</span></div>
      </div>
      <p class="planner-msg" id="lp-msg" role="status"></p>
      <div class="planner-bar">
        <button type="button" class="btn btn-wood" id="lp-png">Download PNG</button>
        <button type="button" class="btn btn-outline" id="lp-sample">Load sample layout</button>
        <button type="button" class="btn btn-outline" id="lp-clear">Clear all</button>
      </div>
      <p class="hint" id="lp-help">Keyboard: Tab to an item, then use the arrow keys to move it 6 in (hold Shift for 1 ft), <span class="kbd">R</span> to rotate, <span class="kbd">Delete</span> to remove and <span class="kbd">Esc</span> to deselect. Your layout is saved in this browser automatically.</p>
    </div>
  </div>
</section>

<section class="section tool-prose">
  <div class="narrow prose">
    <h2>How to plan a tiny house layout that works</h2>
    <p>A good tiny house layout is mostly about what you leave out. In a 200 sq ft house there is room for every function you need, but only if each one is sized honestly and placed so you are not stepping around it all day. This free planner from Tiny Homes Blueprint lets you test that before you buy a trailer or pour a slab: every item is drawn at its real size on a 1 ft grid, so if a queen bed does not fit across an 8.5 ft trailer with room to walk, you will see it immediately.</p>

    <h2>How the layout planner works</h2>
    <ol>
      <li><strong>Choose a footprint.</strong> Start with a common trailer length like 8.5 x 24 ft or a foundation size like 16 x 24 ft, or type your own width and length. Presets use outside dimensions; on an 8.5 ft trailer the inside is closer to 7.5&ndash;7.8 ft once walls are framed, so leave a little slack.</li>
      <li><strong>Add items.</strong> Each button adds a piece at its real size. Items snap to a 6 in grid and cannot be dragged outside the walls.</li>
      <li><strong>Arrange and check.</strong> Items that overlap turn red. The stats bar shows how much of the floor is covered and how much open floor you have left to move around in.</li>
      <li><strong>Save it.</strong> The plan saves in your browser automatically. Use Download PNG for an image you can print, share or bring to a designer.</li>
    </ol>

    <h3>Item sizes used in the planner</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>Item</th><th class="num">Size (ft)</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>Queen bed</td><td class="num">5 x 6.7</td><td>60 x 80 in mattress; allow 2 ft walkway on at least one side</td></tr>
        <tr><td>Full bed</td><td class="num">4.5 x 6.3</td><td>54 x 75 in mattress</td></tr>
        <tr><td>Galley kitchen counter</td><td class="num">8 x 2</td><td>Standard 24 in deep base cabinets</td></tr>
        <tr><td>Refrigerator</td><td class="num">2.5 x 2.5</td><td>Apartment or 24 in fridge with door clearance</td></tr>
        <tr><td>Shower</td><td class="num">3 x 3</td><td>36 x 36 in, a comfortable minimum; 32 in units exist</td></tr>
        <tr><td>Toilet zone</td><td class="num">2.5 x 4</td><td>30 in wide with clear space in front</td></tr>
        <tr><td>Storage stairs</td><td class="num">8 x 2.5</td><td>Stairs to a loft with drawers and cabinets underneath</td></tr>
        <tr><td>Wood stove with clearance</td><td class="num">3.5 x 3.5</td><td>Small stove plus a typical reduced-clearance zone; follow the stove's listing</td></tr>
      </tbody>
    </table></div>

    <h2>Common tiny house layouts to try</h2>
    <p>Load the sample layout to see the most common arrangement, then try these variations to see which suits the way you live:</p>
    <ul>
      <li><strong>Bath at one end, living at the other.</strong> The classic layout for an 8.5 x 24 ft trailer: bathroom and laundry across one end, a galley kitchen along one long wall, and a sofa and storage stairs at the far end under the loft.</li>
      <li><strong>Kitchen in the middle, two lofts.</strong> On 28 ft and longer trailers, a central kitchen with lofts over both ends gives a couple or a family two separate sleeping areas.</li>
      <li><strong>Main-floor bedroom.</strong> For anyone who would rather not climb, a 12 x 24 ft or wider footprint fits a queen bed on the main floor with a walkway beside it. Try it with the 12 x 24 ft preset.</li>
      <li><strong>Flex room.</strong> On a larger footprint like 20 x 38 ft, a room that switches between dining, office and guest room earns its space. Our 700 sq ft plans use a retractable wall for exactly this.</li>
    </ul>

    <h2>Tiny house layout tips</h2>
    <ul class="check-list">
      <li><strong>Keep a clear path.</strong> Aim for at least 30&ndash;36 in of walkway through the house. On an 8.5 ft trailer that means furniture on one side is limited to about 5 ft deep.</li>
      <li><strong>Stack the wet zones.</strong> Put the kitchen sink, shower, toilet and washer on the same end or wall to keep plumbing short and cheaper.</li>
      <li><strong>Use the ends.</strong> On a long, narrow house, the ends are the only places a full-width room fits. Bathrooms and bedrooms usually go there, with the kitchen and living space between.</li>
      <li><strong>Lofts change the math.</strong> Moving the bed to a loft frees 35&ndash;45 sq ft of floor. Plan stairs or a ladder and read our guide to <a href="/tiny-house-plans-with-loft/">tiny house plans with a loft</a> for headroom rules.</li>
      <li><strong>Watch the open-floor number.</strong> If less than about 35% of the floor is open, the house will feel cramped, no matter how good it looks in a rendering.</li>
    </ul>
    <p>For more ideas, see our <a href="/blog/tiny-house-layout-ideas/">15 tiny house layout ideas</a>. If you are working on a trailer, the <a href="/blog/tiny-house-trailer-size-guide/">trailer size guide</a> explains legal widths and lengths, and the <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a> checks whether your build stays under the trailer rating.</p>

    <h2>From sketch to buildable plan</h2>
    <p>A sketch is the right place to start, but it is not something you can permit or build from. A buildable plan adds wall thicknesses, framing, window sizes, electrical and plumbing layouts and the structural details an inspector checks. Once your layout feels right, price it with the <a href="/tools/tiny-house-cost-calculator/">tiny house cost calculator</a> and compare it with ready-made <a href="/tiny-house-plans/">tiny house floor plans</a>. Tiny Homes Blueprint can also modify one of our plans to match the layout you sketched here.</p>

    <?php faq_block([
        ['What is the best layout for a tiny house?', '<p>For most tiny houses on wheels, the layout that works best puts the bathroom at one end, a galley kitchen along one long wall in the middle, the living area at the other end and the bed in a loft. It keeps plumbing together and leaves a clear walkway down the length of the house.</p>'],
        ['How wide should a walkway be in a tiny house?', '<p>Aim for 30 to 36 inches. You can squeeze to about 24 inches for short runs, such as beside a bed, but main paths through the kitchen should stay at 30 inches or more.</p>'],
        ['Will a queen bed fit in a tiny house on wheels?', '<p>Yes, but usually across the width in a loft or at one end. A queen is 60 x 80 inches, and the inside width of an 8.5 ft wide trailer house is about 7.5 to 7.8 ft after walls, which leaves little room to walk around it on the main floor.</p>'],
        ['Does the planner save my layout?', '<p>Yes. Your layout is saved in this browser automatically, so it will be there when you come back on the same device. Use Download PNG to keep a copy or share it.</p>'],
        ['Can I use my sketch as a construction plan?', '<p>No. The planner is a space-planning sketch. To build, you need a full plan set with framing, structural, electrical and plumbing details that meets your local code. Tiny Homes Blueprint can turn a sketch into a plan modification or custom design.</p>'],
    ]); ?>

    <h2>Related tools and guides</h2>
    <ul class="related-links">
      <li><a href="/tools/how-big-should-my-tiny-house-be/"><?= icon('size') ?> Tiny house size calculator</a></li>
      <li><a href="/tools/tiny-house-cost-calculator/"><?= icon('cost') ?> Cost calculator</a></li>
      <li><a href="/tools/tiny-house-style-quiz/"><?= icon('quiz') ?> Tiny house style quiz</a></li>
      <li><a href="/blog/tiny-house-layout-ideas/"><?= icon('book') ?> Tiny house layout ideas</a></li>
      <li><a href="/tiny-house-on-wheels-plans/"><?= icon('wheels') ?> Tiny house on wheels plans</a></li>
      <li><a href="/tiny-house-plans-with-loft/"><?= icon('loft') ?> Plans with a loft</a></li>
      <li><a href="/shipping-container-home-plans/"><?= icon('container') ?> Shipping container layouts</a></li>
      <li><a href="/plans/plan-12-2417/"><?= icon('file') ?> Plan 12-2417 (700 sq ft)</a></li>
    </ul>
  </div>
</section>

<?php cta_band('Turn your sketch into a real plan', 'Send us your layout and we can suggest a plan that fits, or quote a modification or custom design.', 'Send us your layout', '/contact/'); ?>
<?php page_end(['scripts' => ['/assets/js/tools/layout-planner.js']]); ?>
