<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';

$path = '/sugar-land-storm-history/';
$crumbs = [['Home', '/'], ['Storm Center', '/sugar-land-weather/'], ['Storm History', $path]];

// [date label, iso date, title, icon, categories, summary, claim lesson]
$storms = [
    ['July 8, 2024', '2024-07-08', 'Hurricane Beryl', '🌀', ['hurricane'],
     'Beryl made landfall near Matagorda as a Category 1 hurricane and tracked north over the Houston area. Damaging gusts brought down trees and power lines across Fort Bend County, and more than two million CenterPoint Energy customers lost power—many for a week or longer in the July heat.',
     'Tree-impact and roof claims spiked, and so did disputes over spoiled food, generator costs and additional living expenses. Keep receipts for everything you spend because of the outage and the damage.'],
    ['May 16, 2024', '2024-05-16', 'Houston Derecho', '⛈️', ['severe'],
     'A fast-moving line of severe thunderstorms produced hurricane-force straight-line winds, worst in central Houston, shattering windows, toppling trees and transmission towers and knocking out power across the region.',
     'Straight-line wind damage is covered like other wind damage, usually under the wind/hail deductible—not a named-storm deductible, since no named storm was involved. Check which deductible the insurer applied.'],
    ['May 2024', '2024-05-12', 'Brazos River Flooding', '🌊', ['flood'],
     'Heavy rain upstream sent the Brazos River at Richmond above flood stage twice in May 2024, cresting at 45.92 ft on May 12 and 45.78 ft on May 22 according to NOAA gauge records—minor flood stage, flooding low-lying land near the river.',
     'River flooding is excluded from homeowners policies. Only an NFIP or private flood policy pays—and NFIP policies usually take 30 days to go into effect, so they must be bought well before the river rises.'],
    ['September 14, 2021', '2021-09-14', 'Hurricane Nicholas', '🌀', ['hurricane'],
     'Nicholas came ashore on the Matagorda Peninsula as a Category 1 hurricane, bringing heavy rain and gusty winds to the Houston area and widespread power outages.',
     'Even “minor” hurricanes trigger named-storm deductibles. If damage is close to the deductible, a thorough scope decides whether the claim pays anything.'],
    ['February 14–19, 2021', '2021-02-14', 'Winter Storm Uri', '🥶', ['freeze'],
     'An Arctic outbreak brought snow, ice and temperatures in the teens to Sugar Land while the Texas power grid failed. Homes went days without heat, and burst pipes flooded thousands of houses across the Houston region.',
     'Burst-pipe water damage is generally covered as sudden and accidental, but insurers scrutinized whether owners took reasonable steps to maintain heat. Document the outage and every mitigation step.'],
    ['August 25–September 1, 2017', '2017-08-31', 'Hurricane Harvey', '🌀', ['hurricane', 'flood'],
     'Harvey made landfall near Rockport as a Category 4 hurricane, then stalled over Southeast Texas for days, dropping historic rainfall. Upstream rain pushed the Brazos River at Richmond to a record 55.19 ft—the highest crest on record at the gauge—and parts of Fort Bend County along the river were ordered to evacuate.',
     'Harvey made “wind vs. water” the defining claim fight. Damage from rising water needs a flood policy; damage from wind-driven rain through a damaged roof belongs on the homeowners claim. Separate and document them carefully.'],
    ['April–June 2016', '2016-06-02', 'Tax Day Flood & Record Brazos Crest', '🌊', ['flood'],
     'The April 2016 “Tax Day” floods inundated much of the Houston area, and the Brazos at Richmond reached 49.67 ft on April 21. Weeks later, more rain pushed the river to 54.74 ft on June 2—a record at the time—flooding neighborhoods near the river.',
     'Back-to-back floods create overlapping damage. Each date of loss needs its own documentation, and prior repairs (with receipts) protect the next claim.'],
    ['May–June 2015', '2015-06-03', 'Memorial Day Floods', '🌊', ['flood'],
     'Torrential Memorial Day weekend rain flooded parts of the Houston area, and the Brazos at Richmond crested at 50.01 ft on June 3, 2015—major flood stage.',
     'NFIP flood claims run on strict federal deadlines—generally a signed proof of loss within 60 days unless FEMA extends it.'],
    ['September 13, 2008', '2008-09-13', 'Hurricane Ike', '🌀', ['hurricane'],
     'Ike made landfall at Galveston as a large Category 2 hurricane. Its broad wind field swept across the Houston metro, damaging roofs, fences and trees across Fort Bend County and leaving millions of customers in the region without power, some for weeks.',
     'Ike’s claims ran for years. Many were underpaid because of rushed inspections. Hidden roof and attic damage often surfaced months later—one reason reopening and supplementing claims matters.'],
    ['September 2005', '2005-09-24', 'Hurricane Rita', '🌀', ['hurricane'],
     'Weeks after Katrina, Rita threatened the upper Texas coast and triggered one of the largest evacuations in U.S. history from the Houston area before making landfall near the Texas–Louisiana border on September 24.',
     'Evacuation costs and additional living expenses may be covered when a civil authority orders an evacuation. Read the “civil authority” and ALE sections of your policy.'],
    ['June 5–9, 2001', '2001-06-08', 'Tropical Storm Allison', '🌧️', ['flood'],
     'Allison never became a hurricane, but it stalled over Southeast Texas and dumped catastrophic rain on the Houston area, causing billions of dollars in flood damage. Its name was retired.',
     'A tropical storm can do more damage than a hurricane. Flood coverage—not wind coverage—decides these claims.'],
    ['October 1994', '1994-10-21', 'October 1994 Southeast Texas Floods', '🌊', ['flood'],
     'Days of torrential rain flooded rivers across Southeast Texas. The Brazos at Richmond crested at 50.3 ft on October 21, 1994, then one of the highest crests in its history.',
     'Levee improvement districts built since then protect much of Sugar Land, but properties outside them—and anyone with a mortgage in a mapped floodplain—should review flood coverage.'],
    ['Every spring', '2026-04-15', 'Severe Thunderstorm & Hail Season', '🧊', ['severe'],
     'March through June is peak season for severe thunderstorms in Southeast Texas, bringing hail, damaging straight-line winds and occasional tornadoes to Fort Bend County.',
     'Hail damage is easy to miss from the ground and many policies require weather claims to be reported within a set time. Have the roof inspected after any significant hail event.'],
];

$crests = [
    ['Sept 1, 2017', 'Harvey', 55.19], ['June 2, 2016', '', 54.74], ['Nov 28, 1940', '', 51.40], ['Oct 21, 1994', '', 50.30],
    ['May 5, 1957', '', 50.13], ['June 3, 2015', '', 50.01], ['Jan 1, 1992', '', 49.68], ['Apr 21, 2016', 'Tax Day', 49.67],
    ['May 25, 1965', '', 47.72], ['May 8, 1944', '', 47.70], ['Jan 10, 2019', '', 46.59], ['May 12, 2024', '', 45.92],
];

$items = [];
foreach ($storms as $i => $s) {
    $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $s[2] . ' (' . $s[0] . ')'];
}
page_start([
    'title' => 'Sugar Land Storm History: Hurricanes, Floods & Freezes | Sugar Land Public Adjuster',
    'description' => 'A timeline of major storms that hit Sugar Land and Fort Bend County—Harvey, Ike, Beryl, Uri, Brazos River floods—with record river crests and insurance claim lessons.',
    'path' => $path,
    'breadcrumbs' => $crumbs,
    'schema' => [['@type' => 'ItemList', '@id' => SITE['origin'] . $path . '#storms', 'name' => 'Major storms affecting Sugar Land, TX', 'itemListElement' => $items]],
]);
page_hero('Sugar Land Storm History', 'Hurricanes, floods, freezes and hail have all left their mark on Sugar Land and Fort Bend County. Here is what happened—and what each storm taught us about insurance claims.', $crumbs, 'Storm Center');
?>
<div class="wx-strip" id="wx-strip">
  <div class="container wx-strip-inner">
    <span data-wx><span class="wx-pill">Live Sugar Land weather &amp; NWS alerts</span></span>
    <span><a href="/sugar-land-weather/">Open the live storm tracker &rarr;</a></span>
  </div>
</div>

<div class="container content-layout">
  <div>
    <div class="filter-bar" role="group" aria-label="Filter storms">
      <button type="button" class="on" data-filter="all">All events</button>
      <button type="button" data-filter="hurricane">Hurricanes</button>
      <button type="button" data-filter="flood">Floods</button>
      <button type="button" data-filter="severe">Severe storms &amp; hail</button>
      <button type="button" data-filter="freeze">Freezes</button>
    </div>
    <ol class="storm-timeline">
<?php foreach ($storms as [$label, $iso, $name, $icon, $cats, $sum, $lesson]): ?>
      <li class="storm" data-cats="<?= e(implode(' ', $cats)) ?>">
        <span class="storm-dot" aria-hidden="true"><?= $icon ?></span>
        <p class="storm-date mb-0"><time datetime="<?= e($iso) ?>"><?= e($label) ?></time></p>
        <h2 class="h3"><?= e($name) ?></h2>
        <ul class="storm-tags"><?php foreach ($cats as $c): ?><li><?= e(ucfirst($c)) ?></li><?php endforeach; ?></ul>
        <p><?= e($sum) ?></p>
        <p class="storm-lesson"><strong>Claim lesson:</strong> <?= e($lesson) ?></p>
      </li>
<?php endforeach; ?>
    </ol>

    <section class="prose">
      <h2>Highest Brazos River crests at Richmond</h2>
      <p>The NOAA river gauge on the Brazos at Richmond (RMOT2) is the number Fort Bend County watches during major rain events. Minor flood stage is 45 ft, moderate 48 ft and major 50 ft. These are the highest crests on record:</p>
      <div class="crest-chart" aria-label="Bar chart of the highest Brazos River crests at Richmond">
<?php foreach ($crests as [$d, $n, $ft]): ?>
        <div class="crest-row<?= $ft >= 50 ? ' major' : '' ?>"><span><?= e($d) ?><?= $n ? ' <small>(' . e($n) . ')</small>' : '' ?></span><div class="b" style="width:<?= round(($ft - 40) / 16 * 100, 1) ?>%"></div><strong><?= number_format($ft, 2) ?> ft</strong></div>
<?php endforeach; ?>
      </div>
      <p class="small muted">Source: NOAA National Water Prediction Service historic crests for the Brazos River at Richmond. Bars start at 40 ft. Purple bars are major flood stage (50 ft+).</p>

      <h2>What Sugar Land’s storm history means for your insurance</h2>
      <ul class="checklist purple">
        <li><strong>Wind and flood are separate coverages.</strong> Your homeowners policy covers wind; only flood insurance covers rising water.</li>
        <li><strong>Deductibles change by peril.</strong> Named-storm and wind/hail deductibles are often a percentage of your dwelling limit. <a href="/tools/hurricane-deductible-calculator/">Calculate yours</a>.</li>
        <li><strong>Outages cost money.</strong> Food spoilage, hotels and other additional living expenses can be claimable.</li>
        <li><strong>Hidden damage appears later.</strong> Supplements and reopened claims are common after big storms. See <a href="/services/denied-underpaid-claims/">denied &amp; underpaid claims</a>.</li>
      </ul>
      <p>If a storm damaged your property—whether last week or a few months ago—a Sugar Land public adjuster can review the claim for free. Also see our <a href="/hurricane-insurance-claim-guide-sugar-land/">hurricane claim guide</a> and <a href="/services/flood-damage-claims/">flood claim help</a>.</p>
    </section>
  </div>
  <?php sidebar_cta(); ?>
</div>
<?php
$js = <<<'JS'
<script>
document.querySelectorAll('[data-filter]').forEach(function(b){b.addEventListener('click',function(){
var f=b.getAttribute('data-filter');document.querySelectorAll('[data-filter]').forEach(function(x){x.classList.toggle('on',x===b)});
document.querySelectorAll('.storm').forEach(function(s){s.hidden=!(f==='all'||s.getAttribute('data-cats').split(' ').indexOf(f)>-1)});});});
</script>
JS;
page_end(['scripts' => $js]);
