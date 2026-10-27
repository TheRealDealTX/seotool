<?php
// Business details, navigation and the neighborhood/area catalogue.
defined('HA_ROOT') || exit;

const SITE = [
    'name'      => 'Houston Apartments',
    'legal'     => 'TX Rising LLC – Houston Apartments',
    'tagline'   => 'Free Houston apartment locating since 2018',
    'phone'     => '(832) 720-7978',
    'phone_raw' => '+18327207978',
    'email'     => 'info@houstonapartments.com',
    'founded'   => 2018,
    'cashback'  => 500,
    'center'    => [29.7604, -95.3698],
];

const FOUNDER = [
    'name'   => 'Joseph Dittman',
    'title'  => 'Owner, Founder & Lead Apartment Locator',
    'photo'  => '/assets/img/joseph-dittman-houston-apartment-locator.webp',
    'avatar' => '/assets/img/joseph-dittman-avatar.webp',
    'short'  => 'Joseph Dittman founded Houston Apartments in 2018 and still works with renters himself – touring properties, filming them, and tracking which communities have the best deals each week.',
];

const NAV = [
    ['/apartments/', 'Find Apartments'],
    ['/houston-apartments-neighborhoods/', 'Neighborhoods'],
    ['/houston-apartment-tools/', 'Renter Tools'],
    ['/houston-apartments-process/', 'How It Works'],
    ['/houston-apartments-blog/', 'Blog'],
    ['/about-houston-apartments/', 'About'],
];

/*
 * Area landing pages. The keys are the old WordPress page slugs (kept so the
 * URLs never 404); `rise` lists the riseapartments.com "location" term IDs
 * whose listings belong on the page. lat/lng/zoom frame the map.
 */
const AREAS = [
    'houston-heights-apartments'        => ['name' => 'Houston Heights',     'rise' => [46, 51],  'lat' => 29.7980, 'lng' => -95.3980, 'zoom' => 13, 'tag' => 'Historic bungalows, 19th Street boutiques and the Heights Hike & Bike Trail.'],
    'downtown-houston-apartments'       => ['name' => 'Downtown Houston',    'rise' => [34, 47],  'lat' => 29.7560, 'lng' => -95.3650, 'zoom' => 14, 'tag' => 'High-rise living beside Discovery Green, Minute Maid Park and METRORail.'],
    'houston-medical-center-apartments' => ['name' => 'Medical Center',      'rise' => [39],      'lat' => 29.7070, 'lng' => -95.4010, 'zoom' => 14, 'tag' => 'Walk or ride the rail to the world’s largest medical complex.'],
    'montrose-apartments'               => ['name' => 'Montrose',            'rise' => [36],      'lat' => 29.7440, 'lng' => -95.3920, 'zoom' => 14, 'tag' => 'Murals, museums and Houston’s most eclectic dining scene.'],
    'river-oaks-apartments'             => ['name' => 'River Oaks',          'rise' => [43],      'lat' => 29.7500, 'lng' => -95.4200, 'zoom' => 14, 'tag' => 'Tree-lined luxury next to River Oaks District shopping.'],
    'rice-military-apartments'          => ['name' => 'Rice Military',       'rise' => [44],      'lat' => 29.7690, 'lng' => -95.4130, 'zoom' => 14, 'tag' => 'Washington Avenue nightlife minutes from Memorial Park.'],
    'galleria-apartments-houston'       => ['name' => 'Galleria / Uptown',   'rise' => [37],      'lat' => 29.7400, 'lng' => -95.4620, 'zoom' => 13, 'tag' => 'Uptown towers, The Galleria and Post Oak Boulevard dining.'],
    'memorial-city-apartments'          => ['name' => 'Memorial City',       'rise' => [41],      'lat' => 29.7800, 'lng' => -95.5420, 'zoom' => 13, 'tag' => 'CITYCENTRE, Memorial City Mall and quick I-10 access.'],
    'spring-branch-apartments'          => ['name' => 'Spring Branch',       'rise' => [52],      'lat' => 29.8000, 'lng' => -95.5200, 'zoom' => 13, 'tag' => 'Central west-side value with Korea Town eats and Spring Branch ISD.'],
    'apartments-in-katy'                => ['name' => 'Katy',                'rise' => [66],      'lat' => 29.7860, 'lng' => -95.7600, 'zoom' => 12, 'tag' => 'Top-rated Katy ISD schools, master-planned communities and LaCenterra.'],
    'sugar-land-apartments'             => ['name' => 'Sugar Land',          'rise' => [53],      'lat' => 29.6000, 'lng' => -95.6200, 'zoom' => 12, 'tag' => 'Sugar Land Town Square, lakeside parks and Fort Bend ISD.'],
    'apartments-in-richmond-tx'         => ['name' => 'Richmond',            'rise' => [49, 180], 'lat' => 29.5820, 'lng' => -95.7600, 'zoom' => 12, 'tag' => 'Small-town Fort Bend charm with new suburban communities.'],
    'apartments-in-cypress-tx'          => ['name' => 'Cypress',             'rise' => [48],      'lat' => 29.9690, 'lng' => -95.6970, 'zoom' => 12, 'tag' => 'Bridgeland, Towne Lake and Cy-Fair ISD in northwest Harris County.'],
    'the-woodlands-apartments'          => ['name' => 'The Woodlands',       'rise' => [63],      'lat' => 30.1658, 'lng' => -95.4613, 'zoom' => 12, 'tag' => 'Waterway Square, trails and a forested master-planned lifestyle.'],
    'apartments-in-conroe-tx'           => ['name' => 'Conroe',              'rise' => [55],      'lat' => 30.3119, 'lng' => -95.4561, 'zoom' => 12, 'tag' => 'Lake Conroe weekends and a historic downtown square.'],
    'apartments-humble-tx'              => ['name' => 'Humble & Kingwood',   'rise' => [57, 179], 'lat' => 29.9988, 'lng' => -95.2622, 'zoom' => 12, 'tag' => 'Lake Houston living close to Bush Intercontinental Airport.'],
    'baytown-apartments'                => ['name' => 'Baytown',             'rise' => [68],      'lat' => 29.7355, 'lng' => -94.9774, 'zoom' => 12, 'tag' => 'Affordable bayfront living near the east-side refinery corridor.'],
    'apartments-in-galveston'           => ['name' => 'Galveston',           'rise' => [50],      'lat' => 29.2910, 'lng' => -94.8270, 'zoom' => 12, 'tag' => 'Island life on the Seawall with the Strand Historic District.'],
];
