<?php
// Business details, navigation and shared lists. Loaded by index.php only.
defined('LLT') or die(http_response_code(404));

const SITE_NAME   = 'Landscape Lighting Texas';
const SITE_ORIGIN = 'https://landscapelightingtexas.com';
const SITE_HOST   = 'landscapelightingtexas.com';
const PHONE       = '+1 (281) 704-7210';
const PHONE_HREF  = 'tel:+12817047210';
const EMAIL       = 'info@landscapelightingtexas.com';
const HOURS       = 'Mon–Fri 8am–6pm CT';
const ASSET_VER   = '20261006b';

// Where quote requests are emailed. The form also keeps a copy on the server
// (storage/), so nothing is lost if mail delivery is not configured.
const QUOTE_TO = EMAIL;

// Main navigation. Children render as a dropdown on desktop.
$NAV = [
    ['label' => 'Services', 'href' => '/services/', 'children' => 'services'],
    ['label' => 'Areas',    'href' => '/areas/',    'children' => 'areas'],
    ['label' => 'Tools',    'href' => '/tools/',    'children' => 'tools'],
    ['label' => 'Gallery',  'href' => '/gallery/'],
    ['label' => 'About',    'href' => '/about-us/'],
    ['label' => 'Blog',     'href' => '/blog/'],
];

// Services: slug => [name, short blurb, image, icon]
$SERVICES = [
    'architectural-uplighting'   => ['Architectural Uplighting', 'Grazed stone, lit columns and balanced facades that give your home presence after dark.', 'architectural-uplighting', 'home'],
    'garden-tree-lighting'       => ['Garden & Tree Lighting', 'Moonlit live oaks, glowing crape myrtles and planting beds with real depth.', 'oak-tree-uplighting', 'tree'],
    'pathway-driveway-lighting'  => ['Pathway & Driveway Lighting', 'Soft pools of light that guide guests from the curb to the door, safely.', 'driveway-lighting', 'path'],
    'pool-water-feature-lighting'=> ['Pool & Water Feature Lighting', 'Resort-style pools, fountains and patios that come alive at sunset.', 'pool-lighting', 'water'],
    'patio-outdoor-living-lighting' => ['Patio & Outdoor Living Lighting', 'Bistro strings, step lights and downlights for porches, kitchens and pergolas.', 'patio-lighting', 'patio'],
    'smart-lighting-systems'     => ['Smart Lighting Systems', 'App-controlled zones, astronomical timers, dimming and color scenes.', 'garden-pathway-lighting', 'smart'],
    'security-lighting'          => ['Security & Floodlighting', 'Motion-aware, glare-free lighting that protects without looking like a parking lot.', 'landscape-lighting-texas-home', 'shield'],
    'landscape-lighting-maintenance' => ['Maintenance & Repair', 'Annual tune-ups, re-aiming, LED retrofits and repairs for any brand of system.', 'garden-pathway-lighting', 'wrench'],
];

// Regions with their own pages: slug => [name, region label, cities]
$AREAS = [
    'austin'            => ['Austin', 'Central Texas', ['Austin', 'Round Rock', 'Georgetown', 'Cedar Park', 'Lakeway', 'Dripping Springs', 'Pflugerville', 'San Marcos']],
    'houston'           => ['Houston', 'Southeast Texas', ['Houston', 'Sugar Land', 'The Woodlands', 'Katy', 'Pearland', 'Cypress', 'Kingwood', 'Friendswood']],
    'dallas-fort-worth' => ['Dallas–Fort Worth', 'North Texas', ['Dallas', 'Fort Worth', 'Plano', 'Frisco', 'McKinney', 'Southlake', 'Arlington', 'Denton']],
    'san-antonio'       => ['San Antonio', 'South Central Texas', ['San Antonio', 'New Braunfels', 'Boerne', 'Schertz', 'Helotes', 'Fair Oaks Ranch', 'Alamo Heights', 'Seguin']],
    'west-texas'        => ['West Texas', 'West Texas & Panhandle', ['El Paso', 'Midland', 'Odessa', 'Lubbock', 'Amarillo', 'Abilene', 'San Angelo']],
    'gulf-coast'        => ['Gulf Coast', 'Gulf Coast & South Texas', ['Corpus Christi', 'Galveston', 'League City', 'Rockport', 'McAllen', 'Brownsville', 'Edinburg']],
];

// Interactive tools: slug => [name, blurb, icon]. The cost calculator lives at
// its original post URL, so it is listed with an absolute path.
$TOOLS = [
    '/landscape-lighting-cost-calculator/'       => ['Cost Calculator', 'Estimate fixtures, installation, transformer size and running cost.', 'calc'],
    '/tools/lighting-design-simulator/'          => ['Lighting Design Simulator', 'Switch lighting zones on a Texas home, dim them and try scenes.', 'sliders'],
    '/tools/color-temperature-visualizer/'       => ['Color Temperature Visualizer', 'Drag from candle-warm 2200K to cool 5000K and see the difference.', 'sun'],
    '/tools/transformer-calculator/'             => ['Transformer & Voltage Drop', 'Size a low-voltage transformer and check voltage drop by wire gauge.', 'bolt'],
    '/tools/beam-spread-calculator/'             => ['Beam Spread Calculator', 'Find the beam angle that covers a tree, wall or column perfectly.', 'beam'],
    '/tools/dusk-timer/'                         => ['Texas Dusk Timer', 'Sunset and dusk times for your city, with timer settings by month.', 'clock'],
    '/tools/energy-savings-calculator/'          => ['LED Energy Savings', 'Compare halogen and LED running costs at Texas electricity rates.', 'leaf'],
    '/tools/lighting-style-quiz/'                => ['Lighting Style Quiz', 'Six quick questions to match your home with a lighting plan.', 'spark'],
];

// Cities shown on the homepage marquee and Texas map: name => [lon, lat]
$CITY_POINTS = [
    'Austin' => [-97.74, 30.27], 'Houston' => [-95.37, 29.76], 'Dallas' => [-96.80, 32.78],
    'San Antonio' => [-98.49, 29.42], 'Fort Worth' => [-97.33, 32.75], 'El Paso' => [-106.49, 31.76],
    'Corpus Christi' => [-97.40, 27.80], 'Lubbock' => [-101.85, 33.58], 'Amarillo' => [-101.83, 35.22],
    'Midland' => [-102.08, 32.00], 'Plano' => [-96.70, 33.02], 'Frisco' => [-96.82, 33.15],
    'The Woodlands' => [-95.49, 30.17], 'Galveston' => [-94.80, 29.30], 'McAllen' => [-98.23, 26.20],
    'Waco' => [-97.15, 31.55], 'Georgetown' => [-97.68, 30.63], 'New Braunfels' => [-98.12, 29.70],
    'Abilene' => [-99.73, 32.45], 'Tyler' => [-95.30, 32.35], 'Laredo' => [-99.51, 27.53],
    'Brownsville' => [-97.50, 25.90], 'Beaumont' => [-94.10, 30.08], 'San Angelo' => [-100.44, 31.46],
];
