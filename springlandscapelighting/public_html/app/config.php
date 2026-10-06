<?php
defined('SLT') || exit;

const SITE_URL   = 'https://springlandscapelighting.com';
const BRAND      = 'Spring Landscape Lighting';
const PHONE      = '(281) 704-7210';
const PHONE_TEL  = '+12817047210';
const EMAIL      = 'info@springlandscapelighting.com';
const LEAD_TO    = 'info@springlandscapelighting.com';
const ASSET_VER  = '20261006b';

// ---------------------------------------------------------------------------
// Services  (/services/{slug}/)
// ---------------------------------------------------------------------------
const SERVICES = [
    'architectural-lighting' => [
        'name'  => 'Architectural Lighting',
        'short' => 'Architectural',
        'icon'  => 'house',
        'title' => 'Architectural Lighting in Spring, TX | Spring Landscape Lighting',
        'desc'  => 'Architectural landscape lighting in Spring, TX: uplighting, wall washing and grazing that brings brick, stone, columns and rooflines to life after dark.',
        'blurb' => 'Bring dimension to brick, stone, columns, rooflines and entry features with carefully placed uplights, washes and grazing light.',
        'kw'    => 'architectural lighting Spring TX',
    ],
    'pathway-driveway-lighting' => [
        'name'  => 'Pathway & Driveway Lighting',
        'short' => 'Pathways',
        'icon'  => 'footprints',
        'title' => 'Pathway & Driveway Lighting in Spring, TX | Spring Landscape Lighting',
        'desc'  => 'Low-glare pathway, step and driveway lighting for Spring, TX homes. Safer arrivals, softer light and fixtures placed to avoid the runway look.',
        'blurb' => 'Low-glare light along walks, steps and driveways that makes arrivals safer and feels welcoming, never like a runway.',
        'kw'    => 'pathway lighting Spring TX',
    ],
    'tree-garden-lighting' => [
        'name'  => 'Tree & Garden Lighting',
        'short' => 'Trees & Gardens',
        'icon'  => 'trees',
        'title' => 'Tree & Garden Lighting in Spring, TX | Spring Landscape Lighting',
        'desc'  => 'Tree uplighting, moonlighting and garden accent lighting for live oaks, pines, palms and planting beds in Spring, TX.',
        'blurb' => 'Showcase live oaks, pines and planting beds with uplighting, moonlighting, silhouetting and soft accent light.',
        'kw'    => 'tree lighting Spring TX',
    ],
    'patio-pool-lighting' => [
        'name'  => 'Patio & Pool Lighting',
        'short' => 'Patio & Pool',
        'icon'  => 'waves',
        'title' => 'Patio, Pool & Outdoor Living Lighting in Spring, TX | Spring Landscape Lighting',
        'desc'  => 'Patio, pool, pergola and outdoor kitchen lighting in Spring, TX. Comfortable, glare-free light for cooking, entertaining and relaxing after sunset.',
        'blurb' => 'Comfortable light for patios, kitchens, pergolas, pools and fire features, so your outdoor rooms stay open after dark.',
        'kw'    => 'patio lighting Spring TX',
    ],
    'smart-lighting-controls' => [
        'name'  => 'Smart Lighting Controls',
        'short' => 'Smart Controls',
        'icon'  => 'smartphone',
        'title' => 'Smart Landscape Lighting Controls in Spring, TX | Spring Landscape Lighting',
        'desc'  => 'Astronomical timers, photocells, zoning, dimming and app control for landscape lighting in Spring, TX. Lights that run themselves.',
        'blurb' => 'Astronomical timers, zones, dimming and app control, so the right lights come on at the right time without you thinking about it.',
        'kw'    => 'smart landscape lighting controls',
    ],
    'landscape-lighting-repair' => [
        'name'  => 'Repairs & Upgrades',
        'short' => 'Repairs & Upgrades',
        'icon'  => 'wrench',
        'title' => 'Landscape Lighting Repair & LED Upgrades in Spring, TX | Spring Landscape Lighting',
        'desc'  => 'Landscape lighting repair in Spring, TX: dim or dead fixtures, cut wires, failed transformers, halogen-to-LED conversions and full redesigns.',
        'blurb' => 'Fix dim or dead fixtures, damaged wire and tired transformers, or convert an old halogen system to efficient LED.',
        'kw'    => 'landscape lighting repair Spring TX',
    ],
];

// ---------------------------------------------------------------------------
// Service areas  (/service-areas/{slug}/)
// ---------------------------------------------------------------------------
const AREAS = [
    'spring-tx'          => ['name' => 'Spring, TX',          'short' => 'Spring'],
    'klein-tx'           => ['name' => 'Klein, TX',           'short' => 'Klein'],
    'champion-forest'    => ['name' => 'Champion Forest',     'short' => 'Champion Forest'],
    'gleannloch-farms'   => ['name' => 'Gleannloch Farms',    'short' => 'Gleannloch Farms'],
    'augusta-pines'      => ['name' => 'Augusta Pines',       'short' => 'Augusta Pines'],
    'the-woodlands-tx'   => ['name' => 'The Woodlands, TX',   'short' => 'The Woodlands'],
];

// ---------------------------------------------------------------------------
// Tools  (/tools/{slug}/)
// ---------------------------------------------------------------------------
const TOOLS = [
    'lighting-visualizer' => [
        'name' => 'Landscape Lighting Visualizer',
        'icon' => 'sparkles',
        'desc' => 'Switch lighting layers on and off, change color temperature and brightness, and see how a home transforms after dark.',
        'title'=> 'Landscape Lighting Visualizer | Spring Landscape Lighting',
        'meta' => 'Interactive landscape lighting visualizer. Toggle architectural, path, tree and patio lighting, adjust color temperature and brightness, and preview the effect.',
    ],
    'energy-cost-calculator' => [
        'name' => 'Energy Cost Calculator',
        'icon' => 'calculator',
        'desc' => 'Estimate the nightly, monthly and yearly electricity cost of any landscape lighting system.',
        'title'=> 'Landscape Lighting Energy Cost Calculator | Spring Landscape Lighting',
        'meta' => 'Free landscape lighting energy cost calculator. Enter fixtures, watts, hours and your electricity rate to estimate monthly and yearly operating cost.',
    ],
    'fixture-estimator' => [
        'name' => 'Fixture Count Estimator',
        'icon' => 'clipboard-list',
        'desc' => 'Describe your property and get a planning-level estimate of how many fixtures each area typically needs.',
        'title'=> 'Landscape Lighting Fixture Estimator | Spring Landscape Lighting',
        'meta' => 'Estimate how many path lights, uplights and accent fixtures your property needs, plus total wattage and a suggested transformer size.',
    ],
    'transformer-sizing-calculator' => [
        'name' => 'Transformer & Voltage Drop Calculator',
        'icon' => 'plug',
        'desc' => 'Size a low-voltage transformer and check voltage drop on a wire run before you buy or troubleshoot.',
        'title'=> 'Landscape Lighting Transformer & Voltage Drop Calculator | Spring Landscape Lighting',
        'meta' => 'Size a low-voltage landscape lighting transformer with the 80% rule and calculate voltage drop by wire gauge, run length and load.',
    ],
    'led-savings-calculator' => [
        'name' => 'Halogen to LED Savings Calculator',
        'icon' => 'zap',
        'desc' => 'Compare an existing halogen system with an LED retrofit: energy, cost and lamp replacements per year.',
        'title'=> 'Halogen to LED Landscape Lighting Savings Calculator | Spring Landscape Lighting',
        'meta' => 'See how much an LED landscape lighting upgrade saves over halogen: watts, kWh, yearly cost and payback, using your own numbers.',
    ],
    'color-temperature-guide' => [
        'name' => 'Color Temperature Explorer',
        'icon' => 'palette',
        'desc' => 'Slide from candle-warm 2200K to cool 5000K and see which light color flatters brick, stone, foliage and water.',
        'title'=> 'Landscape Lighting Color Temperature Explorer (2200K–5000K) | Spring Landscape Lighting',
        'meta' => 'Interactive guide to landscape lighting color temperature. Compare 2200K, 2700K, 3000K, 4000K and 5000K on brick, stone, plants and water.',
    ],
    'sunset-timer-planner' => [
        'name' => 'Sunset & Timer Planner',
        'icon' => 'sunset',
        'desc' => 'Month-by-month sunset times for Spring, TX, with suggested timer settings and yearly run-hours.',
        'title'=> 'Sunset Times & Landscape Lighting Timer Planner for Spring, TX | Spring Landscape Lighting',
        'meta' => 'Sunset times for Spring, TX by month, with recommended landscape lighting timer schedules and estimated annual run-hours.',
    ],
];

// ---------------------------------------------------------------------------
// Blog  (posts live at /{slug}/ to keep the original WordPress permalinks)
// ---------------------------------------------------------------------------
const CATEGORIES = [
    'general'      => ['name' => 'General',      'desc' => 'Practical answers about owning, running and budgeting for outdoor lighting.'],
    'design-ideas' => ['name' => 'Design Ideas', 'desc' => 'Techniques, color, placement and inspiration for lighting a home and landscape.'],
    'guides'       => ['name' => 'Guides',       'desc' => 'Step-by-step planning guides for low-voltage landscape lighting systems.'],
    'maintenance'  => ['name' => 'Maintenance',  'desc' => 'Keeping a landscape lighting system bright and reliable through Texas weather.'],
];

const POSTS = [
    'electricity-landscape-lighting-use' => [
        'title' => 'How Much Electricity Does Landscape Lighting Use?',
        'seo'   => 'How Much Electricity Does Landscape Lighting Use? (+ Calculator)',
        'desc'  => 'How much electricity landscape lighting uses, how to calculate monthly cost, LED vs halogen, and a free calculator to test your own system.',
        'date'  => '2026-07-21', 'updated' => '2026-10-06', 'cat' => 'general',
        'img'   => 'How-Much-Electricity-Does-Landscape-Lighting-Use.webp',
        'excerpt' => 'Most LED systems cost less to run each month than a streaming subscription. Here is the math, a calculator, and how to keep it low.',
    ],
    'landscape-lighting-cost-spring-tx' => [
        'title' => 'How Much Does Landscape Lighting Cost in Spring, TX?',
        'seo'   => 'Landscape Lighting Cost in Spring, TX: What Drives the Price',
        'desc'  => 'What landscape lighting costs in Spring, TX and why: fixture count, fixture quality, wire runs, transformers, controls and the design itself.',
        'date'  => '2026-10-06', 'cat' => 'guides', 'img' => 'Spring-Landscape-Lighting-BG-1.webp',
        'excerpt' => 'Price follows the plan, not the other way around. These are the factors that actually move a landscape lighting quote up or down.',
    ],
    'landscape-lighting-techniques' => [
        'title' => '12 Landscape Lighting Techniques (and Where Each One Works)',
        'seo'   => '12 Landscape Lighting Techniques Explained | Uplighting, Moonlighting & More',
        'desc'  => 'Uplighting, downlighting, moonlighting, grazing, washing, silhouetting, shadowing and more: what each landscape lighting technique does and where to use it.',
        'date'  => '2026-10-06', 'cat' => 'design-ideas', 'img' => 'Spring-Landscape-Lighting-BG-2.webp',
        'excerpt' => 'Good lighting design is a vocabulary. Learn the twelve techniques designers combine to give a property depth, drama and calm.',
    ],
    'warm-white-vs-cool-white-landscape-lighting' => [
        'title' => 'Warm White vs. Cool White: Choosing a Color Temperature for Landscape Lighting',
        'seo'   => '2700K vs 3000K vs 4000K Landscape Lighting: Choosing a Color Temperature',
        'desc'  => 'How to choose a color temperature for landscape lighting: 2700K vs 3000K vs 4000K on brick, stone, plants and water, and why mixing matters.',
        'date'  => '2026-10-06', 'cat' => 'design-ideas', 'img' => 'Spring-Landscape-Lighting-BG-1.webp',
        'excerpt' => '2700K, 3000K or 4000K? The right color of white depends on what you are lighting. Here is how to choose.',
    ],
    'path-light-spacing' => [
        'title' => 'How Far Apart Should Path Lights Be?',
        'seo'   => 'How Far Apart Should Path Lights Be? Spacing Guide for Walkways',
        'desc'  => 'Path light spacing explained: typical distances, staggering, beam spread, fixture height and how to avoid the runway look on walkways and driveways.',
        'date'  => '2026-10-06', 'cat' => 'design-ideas', 'img' => 'How-Much-Electricity-Does-Landscape-Lighting-Use.webp',
        'excerpt' => 'Too close and it looks like an airport. Too far and you walk through dark gaps. Here is how to space path lights properly.',
    ],
    'tree-uplighting-guide' => [
        'title' => 'How to Uplight Trees: Live Oaks, Pines, Palms and Crape Myrtles',
        'seo'   => 'How to Uplight Trees: A Guide for Live Oaks, Pines & Palms',
        'desc'  => 'How to uplight trees the right way: fixture count, placement, beam angles and techniques for live oaks, pines, palms and crape myrtles.',
        'date'  => '2026-10-06', 'cat' => 'design-ideas', 'img' => 'Spring-Landscape-Lighting-BG-1.webp',
        'excerpt' => 'Mature trees are the best thing many Spring properties have going for them at night. Here is how to light them well.',
    ],
    'landscape-lighting-transformer-sizing' => [
        'title' => 'How to Size a Landscape Lighting Transformer',
        'seo'   => 'How to Size a Low-Voltage Landscape Lighting Transformer (80% Rule)',
        'desc'  => 'How to size a low-voltage landscape lighting transformer: the 80% rule, multi-tap transformers, voltage drop and wire gauge, with worked examples.',
        'date'  => '2026-10-06', 'cat' => 'guides', 'img' => 'Spring-Landscape-Lighting-BG-2.webp',
        'excerpt' => 'The transformer is the heart of a low-voltage system. Size it right and plan for voltage drop, and everything downstream behaves.',
    ],
    'halogen-to-led-landscape-lighting' => [
        'title' => 'Should You Convert Halogen Landscape Lighting to LED?',
        'seo'   => 'Converting Halogen Landscape Lighting to LED: Costs, Savings & Pitfalls',
        'desc'  => 'Should you convert halogen landscape lighting to LED? Energy savings, retrofit lamps vs integrated fixtures, transformer and wiring checks, and pitfalls.',
        'date'  => '2026-10-06', 'cat' => 'guides', 'img' => 'How-Much-Electricity-Does-Landscape-Lighting-Use.webp',
        'excerpt' => 'An LED conversion can cut lighting energy by roughly three quarters. But a swap is not always as simple as changing bulbs.',
    ],
    'landscape-lighting-maintenance-checklist' => [
        'title' => 'Landscape Lighting Maintenance Checklist for Texas Homes',
        'seo'   => 'Landscape Lighting Maintenance Checklist for Texas Homes',
        'desc'  => 'A seasonal landscape lighting maintenance checklist for Texas: cleaning lenses, re-aiming, trimming, checking connections, timers and storm prep.',
        'date'  => '2026-10-06', 'cat' => 'maintenance', 'img' => 'Spring-Landscape-Lighting-BG-2.webp',
        'excerpt' => 'Heat, humidity, storms and fast-growing plants all work against an outdoor system. A short seasonal routine keeps it looking new.',
    ],
    'landscape-lighting-for-home-security' => [
        'title' => 'Does Landscape Lighting Improve Home Security?',
        'seo'   => 'Does Landscape Lighting Improve Home Security? What Actually Helps',
        'desc'  => 'How landscape lighting supports home security: visibility, eliminating hiding spots, glare control, timers and pairing with cameras, without floodlighting.',
        'date'  => '2026-10-06', 'cat' => 'general', 'img' => 'Spring-Landscape-Lighting-BG-1.webp',
        'excerpt' => 'Brighter is not automatically safer. Thoughtful lighting improves visibility without the glare that helps nobody.',
    ],
];

// ---------------------------------------------------------------------------
// Navigation
// ---------------------------------------------------------------------------
const NAV = [
    ['Services',      '/services/',      'services'],
    ['Our Process',   '/our-process/',   null],
    ['Tools',         '/tools/',         'tools'],
    ['Inspiration',   '/inspiration/',   null],
    ['Service Areas', '/service-areas/', 'areas'],
    ['Blog',          '/blog/',          null],
    ['About Us',      '/about-us/',      null],
];
