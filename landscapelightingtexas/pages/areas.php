<?php defined('LLT') or die(http_response_code(404));
global $AREAS;
$P['eyebrow'] = 'Landscape Lighting Across Texas';
$P['lead'] = 'Landscape Lighting Texas designs and installs custom outdoor lighting for homes and businesses across the Lone Star State, from Austin, Houston, Dallas–Fort Worth and San Antonio to the Gulf Coast, West Texas and the growing communities in between.';

// City directory: every city in $AREAS, plus nearby cities from the original
// directory that belong to the same region.
$extraCities = [
    'dallas-fort-worth' => ['Garland', 'Irving', 'Grand Prairie', 'Mesquite'],
    'austin'            => ['Waco', 'Killeen', 'Temple'],
    'houston'           => ['Pasadena'],
    'san-antonio'       => ['Laredo'],
];
$dirOrder = ['dallas-fort-worth', 'austin', 'houston', 'san-antonio', 'gulf-coast', 'west-texas'];
?>
<section class="section">
  <div class="container">
    <?php section_head('Statewide Service', 'Texas Outdoor Lighting Designed for Your Property'); ?>
    <div class="container narrow prose reveal">
      <p class="lead-p">No two Texas properties are alike. A limestone home in the Hill Country, a shaded Houston garden, a brick estate in North Texas and a beach house on the Gulf each bring different architecture, plantings, weather and nighttime needs.</p>
      <p>That is why every system we install starts with the property itself, not a fixture package. Our designers walk your yard at dusk, then build a plan around what deserves attention: the facade, the oldest trees, the path to the door, the pool and the places you actually gather. We pair professional-grade LED fixtures with low-voltage 12V wiring, measured beam angles and warm 2700K–3000K color, then aim everything on-site after dark so the result looks refined and keeps working through Texas summers.</p>
      <p>Wherever you live in Texas, you get the same process, the same fixture standards and the same 5-year workmanship warranty.</p>
    </div>
    <?php stats([['1400', '+', 'Projects completed'], ['5', '+', 'Years serving Texas'], ['5', '-Year', 'Workmanship warranty'], ['6', '', 'Texas regions served']]); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Major Markets', 'Landscape Lighting in Texas’s Largest Metro Areas', 'We serve homeowners and businesses throughout the state’s major metropolitan areas and the communities around them. Choose your region to see how we approach local homes, landscapes and weather.'); ?>
    <?php area_cards(); ?>
  </div>
</section>

<section class="section" id="city-directory">
  <div class="container">
    <?php section_head('City Directory', 'Find Your City', 'Search for your city or browse by region. Nearby towns are often within reach even when they are not listed.'); ?>
    <div class="city-search reveal"><input type="search" placeholder="Search your city…" aria-label="Search service areas" data-city-search></div>
    <div class="city-dir" data-city-dir>
<?php foreach ($dirOrder as $slug):
    [$name, $region, $cities] = $AREAS[$slug];
    $all = array_values(array_unique(array_merge($cities, $extraCities[$slug] ?? []))); ?>
      <div class="city-group"><h3><?= e($region) ?></h3><ul>
<?php foreach ($all as $city): ?>
        <li><a href="/areas/<?= $slug ?>/"><?= e($city) ?></a></li>
<?php endforeach; ?>
      </ul></div>
<?php endforeach; ?>
    </div>
    <p class="city-empty" data-city-empty hidden>That city is not listed, but we may still serve your area. <a href="/quote/">Contact our team</a> for availability.</p>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="grid-2">
      <div class="reveal">
        <?php section_head('Built for the Environment', 'Landscape Lighting Made for Texas Conditions', '', 'left'); ?>
        <p>Outdoor lighting in Texas has to survive more than a pretty first night. Fixtures sit through 100-degree afternoons, Gulf humidity, hail, flash floods, daily irrigation, shifting clay and caliche soil, West Texas wind and an outdoor season that runs most of the year. We plan for the conditions around your property, not just how it looks at the reveal.</p>
        <p>The result is a system that still looks right years later, with fewer service calls and no surprises on your electric bill. A whole-property LED system typically costs around $10–$25 a month to run.</p>
      </div>
      <div class="reveal">
        <?= checklist([
            'Weather-resistant, professional-grade LED fixtures in brass, copper or marine-grade finishes',
            'Low-voltage 12V systems with multi-tap transformers sized for efficiency and future expansion',
            'Heavy 12- or 10-gauge cable and hub wiring to keep voltage drop in check on long runs',
            'Careful wire routing around tree roots, lawns, irrigation and hardscape',
            'Shielded fixtures and measured beam angles that limit glare and light spill toward neighbors',
            'Nighttime aiming, balancing and astronomical timer setup on installation day',
            'A 5-year workmanship warranty, wherever your property is in Texas',
        ]) ?>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('What We Install', 'Outdoor Lighting Services Available Across Texas', 'Choose a focused upgrade or a complete plan for the whole property. <a href="/services/">See all services</a>.'); ?>
    <?php service_cards('', 6); ?>
  </div>
</section>

<?php faqs([
    ['Do you provide landscape lighting throughout Texas?', 'Yes. Landscape Lighting Texas serves residential and commercial clients statewide, including Austin, Houston, Dallas–Fort Worth, San Antonio, West Texas and the Gulf Coast, along with many surrounding communities. Availability can depend on location and project scope, so <a href="/quote/">contact us</a> if your city is not listed.'],
    ['Do you take projects outside the major metro areas?', 'Yes. We regularly consider projects beyond the big metros, including ranches, Hill Country estates, lake homes, hospitality properties and commercial sites. Scheduling depends on the property’s location and the size of the project, and we will tell you up front what is possible.'],
    ['Do you install both residential and commercial outdoor lighting?', 'Yes. We light homes and estates as well as multifamily communities, hospitality spaces, offices, retail centers and other commercial properties that need professional exterior lighting. See <a href="/services/security-lighting/">security and floodlighting</a> for commercial-focused work.'],
    ['How do I confirm you serve my address?', 'Send us your city or ZIP code, the type of property and a short description of what you want to light through our <a href="/quote/">quote form</a>, or call ' . PHONE . '. We will confirm availability and set up your free dusk consultation.'],
    ['Can you expand or upgrade an existing lighting system?', 'In many cases, yes. We evaluate existing systems of any brand, replace failing or halogen fixtures with LED, fix voltage drop, improve coverage, add smart controls or design an expansion around new landscaping. Learn more about <a href="/services/landscape-lighting-maintenance/">maintenance, repair and LED retrofits</a>.'],
], 'Questions About Our Texas Coverage'); ?>

<?php cta_band('Is Your City Not Listed?', 'There is a good chance we can still help. Tell us where your property is and what you want to light, and our team will confirm availability and schedule a free dusk consultation.'); ?>
