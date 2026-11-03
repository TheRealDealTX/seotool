<?php
defined('SCC') || exit;
return [
    'panel-angle' => ['name' => 'Solar Panel Angle Calculator', 'short' => 'Panel Angle Calculator', 'path' => '/tools/solar-panel-angle-calculator/', 'icon' => 'angle',
        'blurb' => 'Best tilt and direction for your solar camera panel, by latitude and season.'],
    'battery' => ['name' => 'Solar Camera Battery & Power Calculator', 'short' => 'Battery & Solar Calculator', 'path' => '/tools/solar-camera-battery-calculator/', 'icon' => 'battery',
        'blurb' => 'Daily energy budget, panel size and days of runtime without sun.'],
    'planner' => ['name' => 'CCTV Camera Planner: How Many Cameras Do I Need?', 'short' => 'CCTV Camera Planner', 'path' => '/tools/cctv-camera-planner/', 'icon' => 'map',
        'blurb' => 'Pick your zones and get a camera count, lens types and a printable plan.'],
    'site-check' => ['name' => 'Solar Camera Site Check', 'short' => 'Solar Site Check', 'path' => '/tools/solar-camera-site-check/', 'icon' => 'compass',
        'blurb' => 'Six questions to find out if solar will keep up at your mounting spot.'],
    'data' => ['name' => '4G Data & microSD Storage Calculator', 'short' => '4G Data & Storage', 'path' => '/tools/4g-data-and-storage-calculator/', 'icon' => 'sd',
        'blurb' => 'Monthly SIM data use and how many days of clips fit on your card.'],
    'coverage' => ['name' => 'Camera Coverage & Detail Calculator', 'short' => 'Coverage Calculator', 'path' => '/tools/camera-coverage-calculator/', 'icon' => 'eye',
        'blurb' => 'Field-of-view width and pixel density: can you detect, recognise or identify?'],
    'cost' => ['name' => 'Solar vs Wired Security Camera Cost Calculator', 'short' => 'Solar vs Wired Cost', 'path' => '/tools/solar-vs-wired-cost-calculator/', 'icon' => 'dollar',
        'blurb' => 'Compare 5-year total cost: hardware, trenching, electrician and plans.'],
];
