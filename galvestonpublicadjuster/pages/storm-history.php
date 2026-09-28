<?php
$meta['title'] = 'Galveston Storm History: Hurricanes from 1900 to Today';
$meta['description'] = 'Galveston hurricane and storm history: the 1900 Storm, 1915, Carla, Alicia, Ike, Harvey, Beryl and more — winds, surge, damage and what each taught us about insurance.';
$meta['crumb'] = 'Galveston Storm History';
$meta['schema'][] = ['@type' => 'Article', 'headline' => 'Galveston Storm History', 'author' => ['@type' => 'Person', 'name' => AUTHOR],
    'publisher' => ['@id' => SITE_URL . '/#business'], 'dateModified' => '2026-09-28'];
// [year, name, css class, category label, wind note, chart mph, body]
$storms = [
    ['1900', 'The Great Galveston Storm', 'c4', 'Category 4', '~120 mph (anemometer failed at 100 mph)', 120, 'Struck September 8, 1900, with a storm surge of about 15.7 feet over an island whose highest point was under 9 feet. Between 6,000 and 8,000 people died in the city — the deadliest natural disaster in U.S. history. Galveston responded by building the Seawall and raising the grade of the entire city.'],
    ['1915', 'The 1915 Galveston Hurricane', 'c4', 'Category 4', 'Sustained ~93 mph, gusts ~120 mph at Galveston', 120, 'On August 16–17, 1915, a surge of about 16 feet tested the new Seawall. The city behind it largely held, a turning point that proved engineering could protect the island.'],
    ['1943', 'The "Surprise" Hurricane', 'c2', 'Category 1–2', '132 mph gust recorded in the Houston area', 132, 'Wartime censorship limited warnings when this July 27, 1943 storm came ashore on Bolivar Peninsula. Nineteen people died.'],
    ['1961', 'Hurricane Carla', 'c4', 'Category 4', 'Gusts estimated to 175 mph near landfall', 175, 'Carla made landfall near Port O\'Connor on September 11, 1961, about 120 miles southwest, yet its size brought surge and a destructive tornado to Galveston.'],
    ['1983', 'Hurricane Alicia', 'c3', 'Category 3', '102 mph gust measured at Galveston', 102, 'Alicia came ashore on the west end of Galveston Island on August 18, 1983, with about 12 feet of surge along Galveston Bay, 21 deaths and roughly $3 billion in damage. Its wind damage helped drive stronger coastal building standards.'],
    ['2001', 'Tropical Storm Allison', 'ts', 'Tropical Storm', 'Winds up to 60 mph', 60, 'A reminder that water, not wind, is often the costlier peril: Allison caused about $5 billion in damage in June 2001, mostly from flooding in the Houston region.'],
    ['2005', 'Hurricane Rita', 'c3', 'Category 3', '120 mph at landfall (Sabine Pass)', 120, 'Rita made landfall at the Texas–Louisiana border on September 24, 2005. Galveston was evacuated, and the massive evacuation itself was deadly.'],
    ['2008', 'Hurricane Ike', 'c2', 'Category 2', '110 mph at landfall on Galveston Island', 110, 'Ike made landfall on the east end of Galveston Island on September 13, 2008, with surge of 10–15 feet on the island and 15–20 feet on Bolivar — far worse than its category suggested. Damage was about $19.3 billion, Texas saw more than 800,000 windstorm-related claims, and TWIA handled tens of thousands of claims; many became disputes over wind vs. flood.'],
    ['2017', 'Hurricane Harvey', 'c4', 'Category 4', '130 mph at landfall near Rockport', 130, 'Harvey stalled over Southeast Texas at the end of August 2017, producing catastrophic rain flooding in Galveston County. Texas insurers reported roughly 670,000 property claims.'],
    ['2021', 'Hurricane Nicholas', 'c1', 'Category 1', '75 mph at landfall on Matagorda Peninsula', 75, 'Nicholas came ashore near Sargent on September 14, 2021, bringing wind, rain and power outages to the upper coast.'],
    ['2024', 'Hurricane Beryl', 'c1', 'Category 1', '80 mph at landfall; 97 mph peak gust in Brazoria County', 97, 'Beryl made landfall near Matagorda on July 8, 2024, knocking out power to millions in the Houston–Galveston area. TWIA reported paying about $336 million to roughly 34,000 policyholders. In 2026 a federal class action alleged TWIA reduced Beryl estimates — allegations that remain unproven.'],
];
echo page_hero(icon('hurricane', 18) . ' 125+ years of storms', 'Galveston Storm History: The Hurricanes That Shaped the Island',
    'From the deadliest disaster in American history to Ike and Beryl, Galveston\'s storms explain why the island has a Seawall, a windstorm code, TWIA — and why claims here are different.', art_hero_house());
?>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Peak winds</span><h2>Peak wind by storm</h2><p>Highest reported or estimated wind associated with each storm (units: mph; sources vary by era).</p></div>
    <div class="bars reveal" style="max-width:900px;margin:0 auto">
      <?php foreach ($storms as $s): ?><div class="bar-row"><span><strong><?= $s[0] ?></strong> <?= e(explode(' ', $s[1])[count(explode(' ', $s[1])) - 1]) ?></span><div class="bar-track"><div class="bar-fill" data-w="<?= round($s[5] / 180 * 100) ?>"></div></div><b><?= $s[5] ?></b></div><?php endforeach ?>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="wrap narrow">
    <div class="section-head"><span class="kicker">Timeline</span><h2>Major storms affecting Galveston</h2></div>
    <ol class="timeline">
      <?php foreach ($storms as $s): ?>
      <li class="reveal"><span class="yr <?= $s[2] ?>"><?= $s[0] ?></span><div class="card"><h3><?= e($s[1]) ?></h3><div class="meta-row"><span class="tag hot"><?= e($s[3]) ?></span><span class="tag"><?= e($s[4]) ?></span></div><p><?= e($s[6]) ?></p></div></li>
      <?php endforeach ?>
      <li class="reveal"><span class="yr ts">2025</span><div class="card"><h3>A quiet year for Texas</h3><p>No tropical cyclone made landfall in Texas in 2025. Quiet seasons are the best time to review coverage, photograph your property and get a WPI-8 in order.</p></div></li>
    </ol>
    <?= banner('Storm damage — past or present? Call for an expert consultation.', 'Many policies allow claims to be reopened or supplemented when more damage is found.') ?>
  </div>
</section>
<section class="section">
  <div class="wrap grid g3">
    <div class="card reveal"><div class="badge-ico"><?= icon('water', 28) ?></div><h3>Lesson 1: Surge is the killer</h3><p>From 1900 to Ike, water — not wind — did the most damage. That's why flood insurance is separate, and why wind vs. flood is the most common Galveston claim dispute.</p></div>
    <div class="card reveal"><div class="badge-ico"><?= icon('wind', 28) ?></div><h3>Lesson 2: Category isn't everything</h3><p>Ike was "only" Category 2. Beryl was Category 1. Both produced massive claim volume. Roof damage starts well below hurricane strength — see our <a href="/calculators/">shingle wind calculator</a>.</p></div>
    <div class="card reveal"><div class="badge-ico"><?= icon('file', 28) ?></div><h3>Lesson 3: Claims pile up</h3><p>After big storms, adjusters are overloaded and estimates get rushed. Documentation and deadlines decide who gets paid in full. We track <a href="/weather-events/">every 70+ mph wind day</a>.</p></div>
  </div>
</section>
<section class="section alt"><div class="wrap narrow"><p class="small muted">Sources: National Park Service; Texas State Historical Association; Galveston &amp; Texas History Center; NOAA/NHC Tropical Cyclone Reports (Ike AL092008, Nicholas AL142021, Beryl AL022024); NWS Houston/Galveston; TDI Harvey data call; TWIA 2024 season review; Insurance Journal. Figures from early storms are historical estimates.</p></div></section>
