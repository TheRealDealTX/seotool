<?php
declare(strict_types=1);

/** Regional peril profiles used by city pages. */
const REGIONS = [
    'Houston & Upper Gulf Coast' => [
        'perils' => ['storm' => 'Hurricanes & tropical storms', 'drop' => 'Flooding & wind-driven rain', 'wind' => 'Derecho & straight-line wind', 'hail' => 'Spring hail', 'snow' => 'Freeze & burst pipes', 'flame' => 'Fire & smoke'],
        'season' => 'Atlantic hurricane season runs June 1 through November 30, and spring squall lines bring hail and damaging straight-line winds.',
        'focus' => 'named-storm and windstorm deductibles, wind-versus-water causation questions, and roofs and interiors damaged by wind-driven rain',
    ],
    'Golden Triangle (Southeast Texas)' => [
        'perils' => ['storm' => 'Hurricanes & storm surge', 'drop' => 'Flooding & wind-driven rain', 'wind' => 'Tropical-force wind', 'hail' => 'Hail', 'snow' => 'Freeze damage', 'flame' => 'Fire & smoke'],
        'season' => 'Hurricane season (June–November) is the dominant risk, with heavy tropical rainfall and spring thunderstorms adding to it.',
        'focus' => 'hurricane deductibles, wind-versus-flood causation, and full roof and envelope replacement after tropical systems',
    ],
    'Dallas–Fort Worth Metroplex' => [
        'perils' => ['hail' => 'Large hail', 'wind' => 'Tornadoes & straight-line wind', 'storm' => 'Severe thunderstorms', 'snow' => 'Ice storms & freezes', 'drop' => 'Water & plumbing losses', 'flame' => 'Fire & smoke'],
        'season' => 'Peak hail and tornado season typically runs from March through June, with a secondary fall severe-weather season and winter ice events.',
        'focus' => 'hail-damaged composition and metal roofs, repair-versus-replacement disputes, matching of siding and roofing, and percentage wind/hail deductibles',
    ],
    'North Texas & Red River' => [
        'perils' => ['wind' => 'Tornadoes', 'hail' => 'Large hail', 'storm' => 'Severe thunderstorms', 'snow' => 'Ice & winter storms', 'flame' => 'Wildfire & structure fire', 'drop' => 'Water damage'],
        'season' => 'Spring brings the most active tornado and hail days along the Red River corridor, while winter storms can bring ice and freezing temperatures.',
        'focus' => 'wind and hail roof claims, tornado structural damage, and freeze-related water losses',
    ],
    'Central Texas' => [
        'perils' => ['hail' => 'Hail', 'drop' => 'Flash flooding & water', 'wind' => 'Wind & tornadoes', 'snow' => 'Ice storms & freezes', 'flame' => 'Wildfire & fire', 'storm' => 'Severe thunderstorms'],
        'season' => 'Spring hail and wind, flash-flood-prone terrain along the Balcones Escarpment, and periodic winter ice storms shape the claim calendar.',
        'focus' => 'hail and wind roof claims, water losses from storms and freezes, and tree-fall damage after ice storms',
    ],
    'San Antonio & Hill Country' => [
        'perils' => ['hail' => 'Large hail', 'drop' => 'Flash flooding', 'wind' => 'Straight-line wind', 'flame' => 'Wildfire', 'snow' => 'Freeze damage', 'storm' => 'Severe storms'],
        'season' => 'Spring hailstorms and Hill Country flash floods are the biggest property risks, with occasional winter freezes.',
        'focus' => 'hail damage to roofs, skylights and siding, flood-adjacent water claims, and tile and metal roof disputes',
    ],
    'Coastal Bend & South Texas' => [
        'perils' => ['storm' => 'Hurricanes', 'wind' => 'High wind', 'drop' => 'Flooding & wind-driven rain', 'hail' => 'Hail', 'snow' => 'Freeze damage', 'flame' => 'Fire'],
        'season' => 'The Gulf hurricane season (June–November) drives most large losses, along with spring storms and occasional hard freezes.',
        'focus' => 'hurricane and windstorm deductibles, roof and envelope replacement, and coordination with windstorm coverage',
    ],
    'Rio Grande Valley' => [
        'perils' => ['storm' => 'Hurricanes & tropical storms', 'drop' => 'Flooding & heavy rain', 'wind' => 'High wind', 'hail' => 'Hail', 'snow' => 'Freeze damage', 'flame' => 'Fire'],
        'season' => 'Tropical systems from June through November and intense spring storms account for most property claims in the Valley.',
        'focus' => 'wind and water damage after tropical systems, stucco and tile roof repairs, and hurricane deductibles',
    ],
    'East Texas' => [
        'perils' => ['wind' => 'Tornadoes & wind', 'storm' => 'Tree-fall from storms', 'hail' => 'Hail', 'drop' => 'Heavy rain & water', 'snow' => 'Ice storms', 'flame' => 'Fire'],
        'season' => 'Spring and fall severe-weather seasons, remnants of Gulf tropical systems, and winter ice storms bring heavy tree-fall and wind damage.',
        'focus' => 'tree-impact and wind claims, roof replacement disputes, and water intrusion after heavy rain',
    ],
    'West Texas & Permian Basin' => [
        'perils' => ['hail' => 'Large hail', 'wind' => 'High wind & dust storms', 'storm' => 'Severe thunderstorms', 'flame' => 'Wildfire', 'snow' => 'Freeze damage', 'drop' => 'Water damage'],
        'season' => 'Late-spring supercells bring large hail and destructive winds, while dry, windy conditions raise wildfire risk.',
        'focus' => 'hail damage to roofs, siding and HVAC units, wind-lifted roofing, and commercial and industrial property losses',
    ],
    'Panhandle & South Plains' => [
        'perils' => ['hail' => 'Giant hail', 'wind' => 'Tornadoes & high wind', 'flame' => 'Wildfire', 'snow' => 'Blizzards & freezes', 'storm' => 'Severe thunderstorms', 'drop' => 'Water damage'],
        'season' => 'The Panhandle and South Plains see some of the most frequent large-hail days in the country each spring, plus wildfire and blizzard risk.',
        'focus' => 'repeat hail claims, full roof and siding replacement, and wildfire and smoke losses',
    ],
    'El Paso & Far West Texas' => [
        'perils' => ['drop' => 'Monsoon flooding', 'wind' => 'High wind', 'hail' => 'Hail', 'snow' => 'Hard freezes', 'flame' => 'Fire', 'storm' => 'Severe storms'],
        'season' => 'Summer monsoon storms bring flash flooding, hail and microbursts, and spring winds and occasional hard freezes add to the risk.',
        'focus' => 'flat and stucco roof water intrusion, wind damage, and freeze-related plumbing losses',
    ],
];

const PERIL_TEXT = [
    'hail'  => 'Hail bruises shingles, fractures tile, dents metal and cracks skylights and HVAC fins — damage carriers often underscope.',
    'wind'  => 'Wind lifts and creases shingles, peels flashing and topples trees; tornadoes can cause structural damage that needs full replacement.',
    'storm' => 'Severe storms combine wind, rain and debris, damaging the roof, envelope and interior at the same time.',
    'drop'  => 'Sudden water damage hides behind walls and under floors, and scope disputes over drying and replacement are common.',
    'snow'  => 'Freezes burst pipes and cause sudden water losses throughout the home, often discovered days later.',
    'flame' => 'Fire and smoke require detailed scopes for structural repair, cleaning, deodorization and contents.',
];
