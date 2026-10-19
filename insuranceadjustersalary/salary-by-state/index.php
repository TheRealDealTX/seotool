<?php
require dirname(__DIR__) . '/inc/config.php';
require SITE_ROOT . '/inc/data.php';

$states = states();
$byMedian = $states;
usort($byMedian, fn($a, $b) => $b['median'] <=> $a['median']);
$top = array_slice($byMedian, 0, 10);
$maxMedian = $top[0]['median'];
$catLabel = ['H' => 'High', 'M' => 'Moderate', 'L' => 'Low'];
$catClass = ['H' => 'tier-high', 'M' => 'tier-mid', 'L' => 'tier-low'];

$faqs = [
    ['q' => 'Which state pays insurance adjusters the most?',
     'a' => 'For staff adjusters, high-wage areas such as the District of Columbia, California, Massachusetts, New York and New Jersey pay the most. For independent and CAT adjusters, storm-heavy states like Texas, Florida, Louisiana and Oklahoma usually generate the most income because of claim volume.'],
    ['q' => 'What is the insurance adjuster salary in Texas?',
     'a' => 'Texas staff adjuster pay sits close to the national median of about $76,800, with Houston and Dallas-Fort Worth running slightly higher. Texas also has some of the heaviest hail and hurricane claim volume in the country, which lifts independent adjuster income.'],
    ['q' => 'What is the insurance adjuster salary in Florida?',
     'a' => 'Florida staff pay runs close to the national median, while hurricane seasons create large earning opportunities for independent and catastrophe adjusters with a Florida 6-20 or emergency license.'],
    ['q' => 'Where do these state salary figures come from?',
     'a' => 'They are estimates. We apply a regional wage index to the BLS national median for claims adjusters ($76,790, May 2024). They are useful for comparing states, but official BLS state data and real job postings should guide salary negotiations.'],
];

$page = [
    'title' => 'Insurance Adjuster Salary by State (2026): All 50 States',
    'description' => 'Compare insurance adjuster salary by state. Search and sort estimated median pay, salary ranges, hourly wages and catastrophe claim demand for all 50 states.',
    'path' => '/salary-by-state/',
    'image' => 'miami-skyline.webp',
    'scripts' => ['tools.js'],
    'schema' => [tool_schema('Insurance Adjuster Salary by State Explorer', '/salary-by-state/', 'Searchable, sortable estimates of insurance adjuster pay in every state.'), faq_schema($faqs)],
];
require SITE_ROOT . '/inc/header.php';
echo page_hero('Interactive explorer', 'Insurance Adjuster Salary by State', 'Search, sort and filter estimated adjuster pay for all 50 states and D.C. &mdash; plus where catastrophe claim demand is strongest for independent adjusters.', 'miami-skyline.webp', ['Tools' => '/tools/', 'Salary by State' => null]);
?>
<section class="section section-dark">
  <div class="container">
    <div class="section-head reveal">
      <span class="eyebrow">Top 10</span>
      <h2>Highest-paying states for staff adjusters</h2>
    </div>
    <div class="bar-chart reveal">
<?php foreach ($top as $s): ?>
      <div class="bar-row"><span class="name"><?= e($s['name']) ?></span><span class="track"><span class="fill" style="width:0" data-width="<?= round($s['median'] / $maxMedian * 100, 1) ?>%"></span></span><span class="amt">$<?= number_format($s['median']) ?></span></div>
<?php endforeach; ?>
    </div>
    <p class="chart-note">Estimated median staff adjuster salary. Regional wage index applied to the BLS national median.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="state-tools reveal">
      <div class="field">
        <label for="st-search">Search states</label>
        <input type="search" id="st-search" placeholder="e.g. Georgia or GA" autocomplete="off">
      </div>
      <div class="field" style="flex:0 1 240px">
        <label for="st-cat">Catastrophe demand</label>
        <select id="st-cat">
          <option value="">All states</option>
          <option value="H">High</option>
          <option value="M">Moderate</option>
          <option value="L">Low</option>
        </select>
      </div>
    </div>
    <div class="table-wrap reveal" style="margin-top:0">
      <table class="data-table" id="state-table">
        <thead>
          <tr>
            <th><button type="button" data-sort="name">State</button></th>
            <th><button type="button" data-sort="median">Est. median salary</button></th>
            <th>Typical range</th>
            <th><button type="button" data-sort="hourly">Hourly</button></th>
            <th><button type="button" data-sort="cat">CAT demand</button></th>
          </tr>
        </thead>
        <tbody>
<?php foreach ($states as $s): ?>
          <tr id="<?= $s['code'] ?>" data-name="<?= e($s['name']) ?>" data-code="<?= $s['code'] ?>" data-median="<?= $s['median'] ?>" data-hourly="<?= $s['hourly'] ?>" data-cat="<?= $s['cat'] ?>">
            <td><strong><?= e($s['name']) ?></strong></td>
            <td><div class="bar-cell">$<?= number_format($s['median']) ?><span class="mini"><i style="width:<?= round(($s['median'] - 60000) / 35000 * 100) ?>%"></i></span></div></td>
            <td>$<?= number_format($s['low'] / 1000) ?>k &ndash; $<?= number_format($s['high'] / 1000) ?>k</td>
            <td>$<?= number_format($s['hourly'], 2) ?></td>
            <td><span class="tier <?= $catClass[$s['cat']] ?>"><?= $catLabel[$s['cat']] ?></span></td>
          </tr>
<?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <p class="chart-note" id="st-count"></p>
  </div>
</section>

<section class="section section-soft">
  <div class="container narrow prose reveal">
    <h2>How insurance adjuster salary changes by state</h2>
    <p>For <strong>staff adjusters</strong>, pay follows the local labor market. Carriers in high-cost metros &mdash; Washington D.C., the Bay Area, Boston, New York and northern New Jersey &mdash; pay well above the national median of $<?= number_format(BLS_MEDIAN_ANNUAL) ?>, while much of the South and rural Midwest pays somewhat less, often with a lower cost of living to match.</p>
    <p>For <strong>independent and CAT adjusters</strong>, the map looks different. Fee schedules are mostly national, so income follows claim volume. States with a <em>High</em> catastrophe rating see regular hurricanes, hail, tornadoes or wildfires, and that is where deployments happen. Many independent adjusters live in a low-cost state and travel to the storms.</p>
    <p>Dig into the two biggest markets: <a href="<?= BLOG_BASE ?>insurance-adjuster-salary-texas/">insurance adjuster salary in Texas</a> and <a href="<?= BLOG_BASE ?>insurance-adjuster-salary-florida/">insurance adjuster salary in Florida</a>. Or personalize your estimate with the <a href="/salary-calculator/">salary calculator</a>.</p>
    <div class="callout"><strong>About this data:</strong> state figures are our estimates, made by applying a regional wage index to the BLS national median for claims adjusters, appraisers, examiners and investigators (May 2024). For official state wages, see the <a href="https://www.bls.gov/oes/" target="_blank" rel="noopener">BLS Occupational Employment and Wage Statistics</a> program.</div>
    <h2 id="faq">State salary FAQs</h2>
    <?= faq_html($faqs) ?>
  </div>
</section>
<?= other_tools('/salary-by-state/') ?>
<?= course_cta() ?>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
