<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Service Areas', '/service-areas/']];
$notes = [
    'Houston' => 'Every neighborhood inside and outside the Loop, from the Heights and Montrose to Meyerland, Kingwood, Clear Lake and Alief.',
    'Katy' => 'Fast-growing west-side subdivisions exposed to spring hail and Cypress Creek and Brazos-area flooding.',
    'Sugar Land' => 'Fort Bend County homes and businesses facing wind, hail and Brazos River flood risks.',
    'The Woodlands' => 'Tree-heavy lots where wind events and falling limbs drive roof and structure claims.',
    'Cypress' => 'Northwest Harris County, hit hard by the 2016 Tax Day Flood and frequent spring hail.',
    'Spring' => 'Spring Creek and Cypress Creek watersheds; wind, hail and plumbing claims.',
    'Pearland' => 'Brazoria County homes exposed to Gulf hurricanes, Clear Creek flooding and hail.',
    'Pasadena' => 'East Harris County residential and industrial-adjacent properties near the Ship Channel.',
    'Humble' => 'Northeast Harris County, flooded by Harvey and Imelda along the San Jacinto River.',
    'Kingwood' => 'Lake Houston-area homes with major flood and wind claim history.',
    'League City' => 'Clear Lake and Galveston County communities with direct hurricane exposure.',
    'Baytown' => 'Bayfront homes and businesses facing surge, wind and flood risk.',
    'Missouri City' => 'Fort Bend County neighborhoods with hail, wind and freeze claims.',
    'Friendswood' => 'Clear Creek watershed homes with a long flood and hurricane history.',
    'Bellaire' => 'Inner-loop city on Brays Bayou next to Meyerland, which flooded three years running from 2015 to 2017.',
    'Tomball' => 'Northwest Harris County homes and acreage with hail and wind exposure.',
    'Conroe' => 'Montgomery County homes and businesses facing tornado, hail and Lake Conroe-area flooding.',
    'Galveston' => 'Island properties with TWIA windstorm policies and surge exposure.',
];
page_start([
    'title' => 'Public Adjuster Service Areas Around Houston, TX | Houston Public Adjusters',
    'desc' => 'Houston Public Adjusters serve Houston, Katy, Sugar Land, The Woodlands, Cypress, Spring, Pearland, Pasadena, Humble, League City, Baytown, Galveston and more.',
    'path' => '/service-areas/',
    'crumbs' => $crumbs,
]);
echo page_hero('Public Adjuster Service Areas Around Houston', 'Our licensed public adjusters serve homeowners and businesses across Harris, Fort Bend, Montgomery, Brazoria, Galveston and Chambers counties. If you&rsquo;re in Greater Houston, we can inspect your property.', $crumbs);
?>
<section class="section">
  <div class="wrap">
    <div class="area-grid">
<?php foreach (AREAS as $a): ?>
      <div class="area"><h3>Public adjuster in <?= e($a[0]) ?>, TX</h3><p><strong><?= e($a[3]) ?> County.</strong> <?= e($notes[$a[0]] ?? '') ?></p></div>
<?php endforeach; ?>
    </div>
    <p class="section-lede" style="margin-top:36px">Don&rsquo;t see your city? We handle claims throughout Southeast Texas and, through TX Public Adjusting, statewide. Call <a href="tel:<?= PHONE_E164 ?>"><?= PHONE_DISPLAY ?></a>.</p>
  </div>
</section>
<section class="section alt">
  <div class="wrap two-col">
    <div class="prose">
      <h2>Local claims need local knowledge</h2>
      <p>A roof in Katy, a slab home in Meyerland and a beach house on Galveston Island are insured, damaged and priced differently. Houston public adjusters who work this market know which neighborhoods flood, which carriers write TWIA wind coverage, what local contractors charge after a storm, and how insurers handle each type of loss.</p>
      <p>Check conditions in your city with our <a href="/houston-weather/">live weather tracker</a>, or see how past storms hit each area in our <a href="/houston-storm-history/">Houston storm history</a>.</p>
    </div>
    <div class="side-card"><?= lead_form('lead-areas', 'Free claim review in your area', '', true) ?></div>
  </div>
</section>
<?php
page_end();
