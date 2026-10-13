<?php
require dirname(__DIR__) . '/inc/layout.php';

$crumbs = [['Home', '/'], ['Houston Storm History', '/houston-storm-history/']];

// [year, name, date, types, summary, claim lesson]
$storms = [
    [2024, 'Hurricane Beryl', 'July 8, 2024', ['hurricane', 'wind'], 'Beryl made landfall near Matagorda as a Category 1 hurricane and tracked directly over the Houston area. Roughly 2.2 million CenterPoint customers lost power, many for more than a week in July heat. Fallen trees, roof damage and power-outage food and equipment losses were widespread.', 'Named-storm deductibles applied to many Beryl claims. Tree-on-roof, fence and spoilage claims were frequently underpaid or missed entirely.'],
    [2024, 'Houston Derecho', 'May 16, 2024', ['wind'], 'A fast-moving line of severe thunderstorms produced straight-line winds the National Weather Service estimated near 100 mph in downtown Houston, blowing out high-rise windows, toppling transmission towers and leaving close to a million customers without power.', 'Derecho damage is wind damage, not a hurricane, so the standard (not the hurricane) deductible usually applies — a detail carriers sometimes get wrong.'],
    [2021, 'Hurricane Nicholas', 'September 14, 2021', ['hurricane', 'flood'], 'Nicholas came ashore on the Matagorda Peninsula as a Category 1 hurricane, knocking out power to roughly half a million Houston-area customers and dropping heavy rain across the region.', 'Smaller storms still create real claims. Interior water from wind-driven rain is a covered loss under many policies.'],
    [2021, 'Winter Storm Uri', 'February 2021', ['freeze'], 'Days of sub-freezing temperatures and the ERCOT grid failure left millions of Texans without power or heat. Frozen and burst pipes flooded homes and businesses across Houston, and plumbers and materials were scarce for weeks.', 'Burst-pipe water damage is typically covered; the pipe repair itself sometimes is not. Delayed repairs led to mold disputes that needed careful documentation.'],
    [2019, 'Tropical Storm Imelda', 'September 17–19, 2019', ['flood'], 'Imelda stalled over Southeast Texas and dumped more than 40 inches of rain in parts of Jefferson County, with severe flooding in northeast Harris County, Kingwood and Humble.', 'Rising water is excluded from homeowners policies. Flood insurance (NFIP or private) and wind-driven rain coverage had to be separated claim by claim.'],
    [2017, 'Hurricane Harvey', 'August 25 – September 1, 2017', ['hurricane', 'flood'], 'Harvey made landfall near Rockport as a Category 4 hurricane, then stalled over Southeast Texas. Parts of Harris County received more than 40 inches of rain and roughly 150,000 Harris County homes flooded. With an estimated $125 billion in damage it remains one of the costliest disasters in U.S. history.', 'Harvey showed why wind versus water causation matters: the same house could have a wind claim, a flood claim and contents claims under different policies.'],
    [2016, 'Tax Day Flood', 'April 17–18, 2016', ['flood'], 'Training thunderstorms dropped more than 15 inches of rain in parts of northwest Harris County overnight, flooding thousands of homes and apartments in Cypress, Jersey Village and along Cypress Creek.', 'Many renters and homeowners outside mapped flood zones learned they had no flood coverage. A flood policy has a 30-day waiting period, so buy it before the season.'],
    [2015, 'Memorial Day Flood', 'May 25–26, 2015', ['flood'], 'Torrential rain over the Brays Bayou watershed sent the bayou out of its banks, flooding thousands of homes in Meyerland and southwest Houston.', 'Repeat-flood neighborhoods face tighter underwriting. Documenting pre-loss condition and prior repairs protects later claims.'],
    [2008, 'Hurricane Ike', 'September 13, 2008', ['hurricane', 'wind', 'flood'], 'Ike made landfall at Galveston as a large Category 2 hurricane with a catastrophic storm surge on Bolivar Peninsula and Galveston Island. More than 2 million CenterPoint customers lost power and wind damage stretched across the entire metro, including blown-out windows downtown.', 'Ike produced years of underpaid-roof litigation in Texas and helped shape today’s windstorm claim rules, including deadlines and pre-suit notice requirements.'],
    [2005, 'Hurricane Rita', 'September 24, 2005', ['hurricane'], 'Weeks after Katrina, Rita triggered one of the largest evacuations in U.S. history as millions left the Houston–Galveston area. The storm turned east and made landfall near the Texas–Louisiana border.', 'Evacuation costs can fall under Additional Living Expense (ALE) coverage when a civil authority orders an evacuation. Keep receipts.'],
    [2001, 'Tropical Storm Allison', 'June 5–9, 2001', ['flood'], 'Allison never reached hurricane strength but stalled over Houston for days, producing more than 35 inches of rain in parts of Harris County. The Texas Medical Center and downtown tunnels flooded and tens of thousands of homes were damaged.', 'A tropical storm can be more destructive than a hurricane. Flood and mold claims from Allison helped change how Texas insurers handle mold.'],
    [1983, 'Hurricane Alicia', 'August 18, 1983', ['hurricane', 'wind'], 'Alicia made landfall southwest of Galveston as a Category 3 hurricane and passed directly over Houston, shattering windows in downtown skyscrapers and causing billions of dollars in damage across the region.', 'Alicia led directly to stronger building codes along the Texas coast. Code-upgrade (ordinance or law) coverage pays to rebuild to today’s standards.'],
];

$hazards = [
    'Hurricane / tropical' => [0, 0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0],
    'Hail &amp; severe storms' => [1, 2, 3, 3, 3, 2, 1, 0, 0, 1, 1, 1],
    'Flash flooding' => [1, 1, 1, 2, 3, 2, 1, 2, 3, 2, 1, 1],
    'Freeze' => [3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
];
$months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

$events = [];
foreach ($storms as $s) {
    $events[] = ['@type' => 'Event', 'name' => $s[1] . ' (' . $s[0] . ')', 'startDate' => (string)$s[0], 'description' => $s[4],
        'location' => ['@type' => 'Place', 'name' => 'Houston, Texas']];
}

page_start([
    'title' => 'Houston Storm History: Hurricanes, Floods, Hail & Freezes',
    'desc' => 'Houston storm history from Hurricane Alicia to Harvey, Uri, the 2024 derecho and Beryl — what each storm did and what it taught policyholders about insurance claims.',
    'path' => '/houston-storm-history/',
    'crumbs' => $crumbs,
    'schema' => [['@type' => 'ItemList', 'name' => 'Major Houston storms', 'itemListElement' => array_map(fn($e, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'item' => $e], $events, array_keys($events))]],
]);
echo page_hero('Houston Storm History', 'Four decades of hurricanes, floods, derechos and freezes &mdash; and the insurance claim lessons each one left behind. Houston Public Adjusters have seen how carriers handle every type of Gulf Coast loss.', $crumbs, 'Hurricanes &middot; Floods &middot; Wind &middot; Freeze');
?>
<section class="section">
  <div class="wrap">
    <h2 class="section-title">Major storms that shaped Houston insurance claims</h2>
    <p class="section-lede">Filter by hazard. Every storm here produced thousands of property insurance claims across Harris County and the surrounding area.</p>
    <div class="filters" role="group" aria-label="Filter storms">
      <button type="button" data-filter="all" aria-pressed="true">All storms</button>
      <button type="button" data-filter="hurricane" aria-pressed="false">Hurricanes</button>
      <button type="button" data-filter="flood" aria-pressed="false">Floods</button>
      <button type="button" data-filter="wind" aria-pressed="false">Wind</button>
      <button type="button" data-filter="freeze" aria-pressed="false">Freeze</button>
    </div>
    <ol class="storm-timeline">
<?php foreach ($storms as $s): ?>
      <li class="storm" data-types="<?= e(implode(' ', $s[3])) ?>">
        <span class="yr"><?= $s[0] ?></span><span class="dot" aria-hidden="true"></span>
        <div class="storm-card">
          <h3><?= e($s[1]) ?></h3>
          <div class="tags"><span class="pill"><?= e($s[2]) ?></span><?php foreach ($s[3] as $t): ?><span class="pill <?= $t === 'hurricane' ? 'red' : '' ?>"><?= ucfirst($t) ?></span><?php endforeach; ?></div>
          <p><?= e($s[4]) ?></p>
          <p class="lesson"><strong>Claim lesson:</strong> <?= e($s[5]) ?></p>
        </div>
      </li>
<?php endforeach; ?>
    </ol>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2 class="section-title">When Houston&rsquo;s damaging weather usually hits</h2>
    <p class="section-lede">A seasonal guide to the hazards behind most Houston property claims. Darker cells mean that hazard is most common that month.</p>
    <div class="table-wrap">
      <table class="season-table">
        <thead><tr><th>Hazard</th><?php foreach ($months as $m): ?><th><?= $m ?></th><?php endforeach; ?></tr></thead>
        <tbody>
<?php foreach ($hazards as $name => $row): ?>
          <tr><td><strong><?= $name ?></strong></td><?php foreach ($row as $v): ?><td style="background:<?= ['#fff', '#fde3c8', '#f9b773', '#f5861f'][$v] ?>" title="<?= ['Rare', 'Possible', 'Common', 'Peak'][$v] ?>"><span class="sr"><?= ['Rare', 'Possible', 'Common', 'Peak'][$v] ?></span></td><?php endforeach; ?></tr>
<?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <p class="tool-note">Legend: white = rare, light = possible, medium = common, orange = peak. Atlantic hurricane season officially runs June 1 to November 30 and peaks from mid-August through September. Flooding can happen in any month in Houston.</p>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div class="prose">
      <h2>What Houston&rsquo;s storm history means for your claim</h2>
      <p>Insurance companies study these storms too. After every major event, carriers bring in out-of-town adjusters with heavy caseloads, apply their own pricing and look hard for exclusions: <em>flood, not wind</em>; <em>wear and tear, not hail</em>; <em>long-term leak, not sudden damage</em>. Knowing how past claims played out is how Houston public adjusters push back.</p>
      <ul class="checklist">
        <li><strong>Causation decides coverage.</strong> Wind and wind-driven rain are usually covered; rising water needs flood insurance. We document which damage came from which force.</li>
        <li><strong>Deductibles differ by storm.</strong> A named hurricane can trigger a 1%&ndash;5% windstorm deductible; a derecho or hailstorm usually doesn&rsquo;t. <a href="/tools/hurricane-deductible-calculator/">Check yours</a>.</li>
        <li><strong>Deadlines are real.</strong> Texas policies and the Insurance Code set notice and lawsuit deadlines. <a href="/tools/claim-deadline-calculator/">Map your timeline</a>.</li>
        <li><strong>Old claims can be reopened.</strong> Hidden damage found during repairs can often be supplemented. <a href="/services/#reopen">Learn about reopened claims</a>.</li>
      </ul>
      <p>Want to look up a specific storm on your street? The <a href="https://www.ncei.noaa.gov/access/storm-events-database/" target="_blank" rel="noopener">NOAA Storm Events Database</a> lists reported hail, wind and flood events by county and date &mdash; useful evidence for a date of loss.</p>
    </div>
    <div>
      <div class="side-card sticky">
        <?= lead_form('lead-storms', 'Was your storm claim underpaid?', 'Houston Public Adjusters review storm claims for free &mdash; including older claims that may still be reopened.') ?>
      </div>
    </div>
  </div>
</section>
<script>
document.querySelectorAll('[data-filter]').forEach(function (b) {
  b.addEventListener('click', function () {
    var f = b.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    document.querySelectorAll('.storm').forEach(function (s) { s.hidden = f !== 'all' && s.dataset.types.split(' ').indexOf(f) < 0; });
  });
});
</script>
<?php
page_end();
