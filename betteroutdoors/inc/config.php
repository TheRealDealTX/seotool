<?php defined('BO') || exit;
// Better Outdoors - site constants and the content registry.
// Every page and post the site serves is listed here; index.php routes from it.

const SITE_NAME   = 'Better Outdoors';
const SITE_URL    = 'https://betteroutdoors.net';
const SITE_EMAIL  = 'info@betteroutdoors.net';
const AMAZON_TAG  = 'betteroutdoors-20';
const SITE_TAGLINE = 'Archery, Bowhunting & Outdoor Gear Guides';
const UPLOADS     = '/wp-content/uploads/2026/01/';
const ASSET_VER   = '20261026';

// Posts keep their original WordPress slugs so every indexed URL survives.
// 'kw' is the primary keyword (from Search Console), 'image' is the hero.
$POSTS = [
    '2016-pse-draw-length-adjustment' => [
        'title'   => '2016 PSE Draw Length Adjustment: Step-by-Step Guide + Chart',
        'h1'      => '2016 PSE Draw Length Adjustment: The Complete Step-by-Step Guide',
        'desc'    => 'How to do a 2016 PSE draw length adjustment: find your draw length, read the PSE draw length chart, move the modules, and know when to use a bow press.',
        'kw'      => '2016 pse draw length adjustment',
        'image'   => '2016-PSE-Draw-Length-Adjustment.webp',
        'thumb'   => '2016-PSE-Draw-Length-Adjustment-768x512.webp',
        'excerpt' => 'Find your true draw length, decode the PSE draw length chart for your cam, and adjust modules safely, with or without a bow press.',
        'date'    => '2026-01-12',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Tuning',
    ],
    'understanding-mathews-compound-bow-packages' => [
        'title'   => 'Mathews Bow Packages: What Comes in a Mathews Compound Bow Package',
        'h1'      => 'Mathews Compound Bow Packages: What You Get and Who They Fit',
        'desc'    => 'Mathews bow packages explained: what comes in a Mathews compound bow package, RTH vs. bare bow, real costs, and how to choose the right Mathews package for hunting.',
        'kw'      => 'mathews bow packages',
        'image'   => 'Understanding-Mathews-Compound-Bow-Packages-1-1.webp',
        'thumb'   => 'Understanding-Mathews-Compound-Bow-Packages-1-1-768x512.webp',
        'excerpt' => 'Sight, rest, quiver, stabilizer: what a Mathews package really includes, what it costs versus a bare bow, and who should buy one.',
        'date'    => '2026-01-14',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Guides',
    ],
    'bear-archery-bear-paw-grip' => [
        'title'   => 'Bear Paw Grip Guide: Bear Archery Bow Grips Explained',
        'h1'      => 'Bear Archery Bear Paw Grip: Design, Feel, and Performance',
        'desc'    => 'The Bear Paw grip explained: grip shape, wrist angle, torque, how Bear bow grips compare with other grips, and how to pick a grip that fits your hand.',
        'kw'      => 'bear paw grip',
        'image'   => 'Bear-Archery-Bear-Paw-Grip-2-1.webp',
        'thumb'   => 'Bear-Archery-Bear-Paw-Grip-2-1-768x512.webp',
        'excerpt' => 'How grip shape and wrist angle drive torque and accuracy, and how to tell whether a Bear bow grip suits your hand.',
        'date'    => '2026-01-13',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Tuning',
    ],
    'mathews-prima-level-1-package' => [
        'title'   => 'Mathews Prima Specs & Review: Level 1 Package Explained',
        'h1'      => 'Mathews Prima Level 1 Package: Specs, Review, and Who It Fits',
        'desc'    => 'Mathews Prima specs and review: 30" axle-to-axle, 21.5"–27.5" draw, 40–60 lb. What the Prima Level 1 package includes and which archers the Prima bow suits best.',
        'kw'      => 'mathews prima',
        'image'   => 'Mathews-Prima-Level-1-Package-1.webp',
        'thumb'   => 'Mathews-Prima-Level-1-Package-1-768x512.webp',
        'excerpt' => 'Full Mathews Prima specs, what the Level 1 package adds, and why this short-draw bow is a favorite for women and smaller-framed hunters.',
        'date'    => '2026-01-14',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Reviews',
    ],
    'bear-archery-alaskan-xt-rth-compound-bow' => [
        'title'   => 'Bear Alaskan XT RTH Review: Specs, Speed & Package',
        'h1'      => 'Bear Archery Alaskan XT RTH Compound Bow Review',
        'desc'    => 'Bear Alaskan XT RTH review: 335 fps IBO, 33" axle-to-axle, 25"–30" draw, 80% let-off. Full specs, what the RTH package includes, and who the Alaskan XT suits.',
        'kw'      => 'bear alaskan xt',
        'image'   => 'Bear-Archery-Alaskan-XT-RTH-Compound-Bow-1.png',
        'thumb'   => 'Bear-Archery-Alaskan-XT-RTH-Compound-Bow-1-768x512.png',
        'excerpt' => 'A 33-inch, 335 fps ready-to-hunt bow with a forgiving 6.25-inch brace height. Full Bear Alaskan XT specs and field notes.',
        'date'    => '2026-01-14',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Reviews',
    ],
    'bear-archery-persist-compound-bow' => [
        'title'   => 'Bear Persist Review: Specs, Speed & Persist 33 Compared',
        'h1'      => 'Bear Archery Persist Compound Bow: Specs and Review',
        'desc'    => 'Bear Persist review: 340 fps, 31" axle-to-axle, 6.5" brace height, 25"–30" draw, 75–90% let-off. Full Bear Persist bow specs and how it compares with the Persist 33.',
        'kw'      => 'bear persist',
        'image'   => 'Bear-Archery-Persist-Compound-Bow.webp',
        'thumb'   => 'Bear-Archery-Persist-Compound-Bow-768x512.webp',
        'excerpt' => '340 fps in a 31-inch frame with four let-off options. Full Bear Persist specs, setup tips, and Persist vs. Persist 33.',
        'date'    => '2026-01-12',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Reviews',
    ],
    'bear-archery-whitetail-maxx-rth-compound-bow' => [
        'title'   => 'Bear Whitetail Maxx RTH Review: Specs & Package',
        'h1'      => 'Bear Archery Whitetail Maxx RTH Compound Bow Review',
        'desc'    => 'Bear Whitetail Maxx RTH review: up to 339 fps, 31" axle-to-axle, 6.5" brace height, 26"–30" draw, 45–70 lb. Specs, RTH package contents, and treestand performance.',
        'kw'      => 'bear whitetail maxx',
        'image'   => 'Bear-Archery-Whitetail-Maxx-RTH-Compound-Bow-1-2.webp',
        'thumb'   => 'Bear-Archery-Whitetail-Maxx-RTH-Compound-Bow-1-2-768x512.webp',
        'excerpt' => 'A 31-inch, 339 fps whitetail bow that ships ready to hunt. Full Whitetail Maxx specs and what to know before you buy.',
        'date'    => '2026-01-14',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Reviews',
    ],
    '2018-pse-evolve-28' => [
        'title'   => '2018 PSE Evolve 28 Specs & Review: Still Worth It?',
        'h1'      => '2018 PSE Evolve 28: Specs, Review, and Used-Buyer Guide',
        'desc'    => 'PSE Evolve 28 specs and review: 28" axle-to-axle, 7" brace height, up to 335 fps, 24.5"–30" draw. How the Evolve cam works and what to check on a used PSE Evolve 28.',
        'kw'      => 'pse evolve 28',
        'image'   => '2018-pse-evolve-28-1-1.webp',
        'thumb'   => '2018-pse-evolve-28-1-1-768x511.webp',
        'excerpt' => 'A 28-inch blind and treestand bow with a 7-inch brace height. Full PSE Evolve 28 specs and a used-buyer checklist.',
        'date'    => '2026-01-13',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Reviews',
    ],
    'mathews-lift-29-5' => [
        'title'   => 'Mathews Lift 29.5 Specs & Review: IBO Speed, Draw, Weight',
        'h1'      => 'Mathews Lift 29.5: Specs and Review of a Quiet, Stable Hunting Bow',
        'desc'    => 'Mathews Lift 29.5 specs: 29.5" axle-to-axle, 6" brace height, up to 348 fps IBO, 24.5"–30" draw, 3.99 lb. Review of the Lift 29.5 vs. the Lift 33 and Lift X.',
        'kw'      => 'mathews lift 29.5',
        'image'   => 'Mathews-Lift-29.5-1.webp',
        'thumb'   => 'Mathews-Lift-29.5-1-768x512.webp',
        'excerpt' => 'Full Mathews Lift 29.5 specs, what the 29.5-inch platform does well, and how it compares with the Lift 33 and Lift X.',
        'date'    => '2026-01-14',
        'updated' => '2026-10-26',
        'cat'     => 'Bow Reviews',
    ],
];

// Interactive tools (new pages).
$TOOLS = [
    'draw-length-calculator' => [
        'title' => 'Draw Length Calculator: Find Your Bow Draw Length',
        'h1'    => 'Draw Length Calculator',
        'desc'  => 'Free draw length calculator. Enter your wingspan or height to estimate your compound bow draw length, then check it against the signs of a correct fit.',
        'short' => 'Estimate your draw length from wingspan or height.',
        'icon'  => 'fa-ruler-horizontal',
    ],
    'arrow-speed-calculator' => [
        'title' => 'Arrow Speed Calculator: Real FPS From IBO Rating',
        'h1'    => 'Arrow Speed Calculator',
        'desc'  => 'Convert a bow\'s IBO rating into your real arrow speed. Adjust draw length, draw weight, arrow weight and string accessories to estimate true FPS.',
        'short' => 'Turn an IBO rating into your real-world FPS.',
        'icon'  => 'fa-gauge-high',
    ],
    'kinetic-energy-calculator' => [
        'title' => 'Arrow Kinetic Energy & Momentum Calculator',
        'h1'    => 'Kinetic Energy & Momentum Calculator',
        'desc'  => 'Calculate arrow kinetic energy (ft-lbs) and momentum (slug-ft/s) from speed and arrow weight, and see which game animals your setup is suited for.',
        'short' => 'See if your setup has the energy for your game.',
        'icon'  => 'fa-bolt',
    ],
    'bow-finder' => [
        'title' => 'Bow Finder Quiz: Which Compound Bow Fits You?',
        'h1'    => 'Bow Finder Quiz',
        'desc'  => 'Answer six quick questions about your draw length, budget and hunting style, and the Better Outdoors bow finder matches you with compound bows we have reviewed.',
        'short' => 'Six questions to match you with the right bow.',
        'icon'  => 'fa-bullseye',
    ],
    'bowhunting-checklist' => [
        'title' => 'Bowhunting Gear Checklist (Interactive & Printable)',
        'h1'    => 'Bowhunting Gear Checklist',
        'desc'  => 'An interactive bowhunting gear checklist for treestand, ground blind and backcountry hunts. Tick items off, save your progress and print it before you go.',
        'short' => 'Tick-off pack list for treestand, blind and backcountry.',
        'icon'  => 'fa-list-check',
    ],
];

$NAV = [
    ['Home', '/'],
    ['Bow Reviews', '/blog/'],
    ['Tips', '/category/tips/'],
    ['Tools', '/tools/'],
    ['About Us', '/about-us/'],
    ['Contact Us', '/contact-us/'],
];
