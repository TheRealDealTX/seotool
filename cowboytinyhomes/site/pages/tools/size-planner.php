<?php
$GLOBALS['scripts'][] = 'tools.js';
hero([
    'eyebrow' => 'Free Tool',
    'h1'      => 'Tiny House Size Planner: How Many Square Feet Do You Need?',
    'lead'    => 'Add the rooms you want and watch the square footage add up. The planner shows your total size, which tiny home types fit, and a rough budget range.',
    'image'   => '4.webp',
    'cta'     => false,
]);
// [key, label, hint, sq ft, default, max, kind]
$rooms = [
    ['bedroom',   'Bedroom',            '~120 sq ft, fits a queen bed',      120, 1, 4, ''],
    ['loft',      'Sleeping loft',      '~80 sq ft, above the main floor',     80, 1, 2, 'loft'],
    ['fullbath',  'Full bathroom',      '~45 sq ft with shower',               45, 1, 3, ''],
    ['halfbath',  'Half bath',          '~20 sq ft, toilet and sink',          20, 0, 2, ''],
    ['kitchen-c', 'Compact kitchen',    '~60 sq ft galley',                    60, 1, 1, ''],
    ['kitchen-f', 'Full kitchen',       '~110 sq ft with island or bar',      110, 0, 1, ''],
    ['living',    'Living area',        '~110 sq ft sofa and TV',             110, 1, 2, ''],
    ['dining',    'Dining nook',        '~40 sq ft for 2–4 seats',             40, 0, 1, ''],
    ['office',    'Office nook',        '~35 sq ft desk space',                35, 0, 2, ''],
    ['laundry',   'Laundry',            '~20 sq ft stacked washer/dryer',      20, 0, 1, ''],
    ['storage',   'Storage / closets',  '~25 sq ft per closet',                25, 1, 6, ''],
    ['mudroom',   'Entry / mudroom',    '~30 sq ft',                           30, 0, 1, ''],
    ['porch',     'Covered porch',      '~80 sq ft, outdoor',                  80, 0, 2, 'porch'],
];
?>
<section class="section">
  <div class="wrap">
    <div class="tool" data-tool="size-planner">
      <div class="tool-panel">
        <h2>Choose Your Rooms</h2>
        <p class="tool-note">Use + and − to add rooms. Lofts and porches are shown separately because they do not count toward heated floor area.</p>
        <div class="room-list">
<?php foreach ($rooms as [$key, $label, $hint, $sqft, $def, $max, $kind]): ?>
          <div class="room" data-room="<?= $key ?>" data-sqft="<?= $sqft ?>" data-max="<?= $max ?>"<?= $kind ? ' data-kind="' . $kind . '"' : '' ?>>
            <div><b><?= e($label) ?></b><small><?= e($hint) ?></small></div>
            <div class="stepper">
              <button type="button" data-step="-" aria-label="Remove <?= e($label) ?>">−</button>
              <output aria-label="<?= e($label) ?> count" value="<?= $def ?>"><?= $def ?></output>
              <button type="button" data-step="+" aria-label="Add <?= e($label) ?>">+</button>
            </div>
          </div>
<?php endforeach; ?>
        </div>
      </div>
      <div class="result-panel" aria-live="polite">
        <h2>Your Tiny House Size</h2>
        <div class="result-big" data-out="total">—</div>
        <p class="result-sub" data-out="detail"></p>
        <ul class="result-rows">
          <li><span>Sleeping loft</span><b data-out="loft">—</b></li>
          <li><span>Porch</span><b data-out="porch">—</b></li>
          <li><span>Rough budget (standard finishes)</span><b data-out="budget">—</b></li>
        </ul>
        <h3>Which home types fit?</h3>
        <ul class="fit-list" data-out="fit"></ul>
        <a class="btn btn--gold" data-out="link" href="/contact-us/">Design This Floor Plan</a>
        <a class="btn btn--ghost" data-out="calc" href="/tools/tiny-home-cost-calculator/">Price It in Detail</a>
        <p class="disclaimer">Room sizes are typical planning areas for small homes. Real layouts vary with ceiling height, stairs and furniture. Budget excludes land and site work.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--narrow prose">
    <h2>How Big Should a Tiny House Be?</h2>
    <p>Most tiny houses fall between 150 and 400 square feet, while "small homes" and ADUs commonly run from 400 to 1,200 square feet. The right size is not a number you pick first — it is the sum of the rooms you genuinely need. This tiny house size planner works the way our designers do: start with the spaces, add an allowance for walls and circulation, and then see which kinds of homes can hold the result.</p>
    <p>For one person, a well-designed 200 to 300 square feet with a sleeping loft can feel surprisingly roomy. Couples tend to be most comfortable between 300 and 500 square feet with a real bedroom. A family of three or four usually needs 600 square feet or more with two bedrooms, plenty of closet space and a laundry area.</p>

    <h2>How the Planner Calculates Square Footage</h2>
    <p>Each room uses a typical planning area for small homes — a bedroom that fits a queen bed with walking space is about 120 square feet, a full bathroom with a shower is about 45, and a compact galley kitchen is about 60. The planner adds them together, then adds <strong>15% for walls, hallways and stairs</strong>. In a tiny house that allowance is lower than in a standard home because good small-home design eliminates hallways wherever possible.</p>
    <p><strong>Sleeping lofts</strong> are listed separately. In a tiny home on wheels or park model, a loft adds valuable space without adding to the footprint. In a foundation home built under the International Residential Code, lofts must meet specific rules for ceiling height, guards and access (see IRC Appendix Q where adopted), and they may or may not count toward the home's official square footage. <strong>Porches</strong> are outdoor space, so they are excluded from the total — but in the Texas climate, a covered porch often functions as a second living room for much of the year.</p>

    <h2>Reading the "Which Home Types Fit" List</h2>
    <ul>
      <li><strong>Tiny home on wheels</strong> — road-legal towable homes are generally limited to about 8.5 feet wide, so larger plans need a long trailer (often 30 to 40 feet) or a gooseneck. Above roughly 300 square feet the planner flags this.</li>
      <li><strong>Park model home</strong> — typically capped just under 400 square feet of floor area, which is why many park models rely on a loft.</li>
      <li><strong>ADU / casita</strong> — usually 300 to 1,200 square feet, but local zoning often caps ADU size as a fixed number or as a percentage of the main house. Confirm your city's limit.</li>
      <li><strong>Custom home on a foundation</strong> — no practical upper limit for a small home, though minimum-size rules in some cities and subdivisions can set a floor.</li>
    </ul>
    <p>The budget range applies Texas 2026 per-square-foot planning costs at standard finishes to every home type that fits. For a full estimate with site work, utilities and add-ons, send your size to the <a href="/tools/tiny-home-cost-calculator/">tiny home cost calculator</a>. To see real layouts, browse our <a href="/home-designs/">tiny house plans and designs</a> or the featured <a href="/gonzales-modern-living/">Gonzales Modern Living</a> plan.</p>
  </div>
</section>

<?php faq_section([
    ['What is the minimum size for a tiny house in Texas?',
     '<p>Texas has no single statewide minimum. The International Residential Code requires at least one habitable room of 70 square feet or more, and IRC Appendix Q (where a city adopts it) defines a tiny house as 400 square feet or less. Some cities and subdivisions set their own minimum home sizes, so check your local rules.</p>'],
    ['Do lofts count as square footage?',
     '<p>It depends on the home type and local code. For tiny homes on wheels and park models, lofts are usually extra space beyond the floor area. In foundation homes, a loft that meets habitable-space requirements may be counted. The planner shows loft area separately so you can see both numbers.</p>'],
    ['How many square feet do two people need in a tiny house?',
     '<p>Most couples are comfortable between about 300 and 500 square feet, especially with a separate bedroom or a well-designed loft, plenty of storage and a covered porch for outdoor living.</p>'],
    ['Can Cowboy Tiny Homes design a floor plan from my planner results?',
     '<p>Yes. Click "Design This Floor Plan" and your room list is sent with your contact request. Our designers turn it into a dimensioned floor plan, elevations and 3D renderings as part of our <a href="/tiny-house-design-services/">tiny house design services</a>.</p>'],
], 'Tiny House Size FAQs'); ?>

<?php related([
    '/home-designs/',
    '/tools/tiny-home-cost-calculator/',
    '/tiny-house-design-services/',
    '/tools/which-tiny-home-is-right-for-me/',
], 'Keep Planning Your Tiny House'); ?>

<?php cta_band('Ready to Turn Your Room List Into a Floor Plan?'); ?>
