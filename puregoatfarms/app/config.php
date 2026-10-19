<?php
// Site-wide constants for puregoatfarms.com. Everything else reads from here.
defined('PGF') || exit;

const SITE_NAME   = 'Pure Goat Farms';
const SITE_URL    = 'https://puregoatfarms.com';
const SITE_HOST   = 'puregoatfarms.com';
const SITE_EMAIL  = 'info@puregoatfarms.com';
const SITE_TAGLINE = 'Practical Goat Farming, Health & Dairy Guides';
const GA_ID       = 'G-9578859YFV';
const AMAZON_TAG  = 'josephrayditt-20';

// Original WordPress media library, kept at its old URLs so nothing 404s.
const UPLOADS = '/wp-content/uploads/2026/07/';

const IMG = [
    'logo'      => UPLOADS . 'Pure-Goat-Farms-Logo.webp',
    'logo_wh'   => UPLOADS . 'Pure-Goat-Farms-Logo-Wh.webp',
    'hero'      => UPLOADS . 'Pure-Goat-Farm-BG.webp',
    'hero_768'  => UPLOADS . 'Pure-Goat-Farm-BG-768x768.webp',
    'story'     => UPLOADS . 'Pure-Goat-Farms-Story.webp',
    'story_768' => UPLOADS . 'Pure-Goat-Farms-Story-768x768.webp',
    'og'        => UPLOADS . 'Pure-Goat-Farms-Site-Image.webp',
    'icon'      => UPLOADS . 'cropped-Pure-Goat-Farms-Site-Icon.webp',
];

// Category slugs match the old /category/<slug>/ URLs exactly.
const CATEGORIES = [
    'milking-dairy' => [
        'name' => 'Milking & Dairy',
        'num'  => '01',
        'icon' => 'pail',
        'blurb' => 'Milking routines, butterfat, cheese-making basics, and keeping a dairy line productive.',
        'intro' => 'Everything we have learned on the milking stand: how much milk a goat really gives, how often to milk, how to plan cheese batches, and how to keep a dairy doe productive season after season.',
    ],
    'farm-life' => [
        'name' => 'Farm Life',
        'num'  => '02',
        'icon' => 'barn',
        'blurb' => 'Fencing, shelter, pasture rotation, and the daily rhythm of running a goat farm.',
        'intro' => 'The day-to-day side of keeping goats: chores, shelter, pasture, and the routines that make a small goat farm run smoothly through every season.',
    ],
    'goat-breeds' => [
        'name' => 'Goat Breeds',
        'num'  => '03',
        'icon' => 'goat',
        'blurb' => 'Nubians, Boers, Nigerian Dwarfs and more — build & temperament for every purpose.',
        'intro' => 'Breed-by-breed notes on milk volume, butterfat, size, temperament and climate fit, so you can pick goats that suit your goals instead of fighting them.',
    ],
    'health-care' => [
        'name' => 'Health & Care',
        'num'  => '04',
        'icon' => 'heart',
        'blurb' => 'Vaccination schedules, hoof trimming, parasite control, and reading the signs of illness early.',
        'intro' => 'Health, nutrition and reproduction notes from our own herd: feeding for milk, freshening and dry periods, and catching problems before they become emergencies.',
    ],
];

const TOOLS = [
    'goat-milk-yield-calculator' => [
        'name'  => 'Goat Milk Yield Calculator',
        'short' => 'Milk per milking',
        'icon'  => 'pail',
        'desc'  => 'Split a goat\'s daily yield into what you will actually collect at each milking, in liters, gallons, pounds or cups.',
        'kw'    => 'goat milk yield calculator',
    ],
    'goat-milk-production-estimator' => [
        'name'  => 'Goat Milk Production Estimator',
        'short' => 'Season & lactation curve',
        'icon'  => 'chart',
        'desc'  => 'Pick a breed and see a full 305-day lactation curve: peak day, milk per day, per week and per season.',
        'kw'    => 'goat milk production per day',
    ],
    'goat-cheese-herd-calculator' => [
        'name'  => 'Goat Cheese Herd Calculator',
        'short' => 'Goats needed for cheese',
        'icon'  => 'cheese',
        'desc'  => 'Work backward from the cheese you want to make to the number of milking does you need.',
        'kw'    => 'how many goats do you need to make cheese',
    ],
    'goat-gestation-calculator' => [
        'name'  => 'Goat Gestation & Kidding Date Calculator',
        'short' => 'Kidding date & timeline',
        'icon'  => 'calendar',
        'desc'  => 'Enter a breeding date to get the due date window plus a dry-off, booster and kidding-prep timeline.',
        'kw'    => 'goat gestation calculator',
    ],
    'goat-feed-calculator' => [
        'name'  => 'Goat Feed & Hay Calculator',
        'short' => 'Hay, grain & water',
        'icon'  => 'hay',
        'desc'  => 'Estimate daily and monthly hay, grain and water for your herd, with an optional feed cost.',
        'kw'    => 'goat feed calculator',
    ],
    'dairy-goat-breed-finder' => [
        'name'  => 'Dairy Goat Breed Finder',
        'short' => '60-second breed quiz',
        'icon'  => 'goat',
        'desc'  => 'Answer five quick questions and get the dairy breeds that best fit your space, climate and milk goals.',
        'kw'    => 'best dairy goat breed',
    ],
    'goat-milk-converter' => [
        'name'  => 'Goat Milk Unit Converter',
        'short' => 'Pounds ↔ gallons ↔ liters',
        'icon'  => 'scale',
        'desc'  => 'Convert milk weights from the scale into gallons, quarts, liters and cups using goat-milk density.',
        'kw'    => 'goat milk pounds to gallons',
    ],
];

// Main navigation. Children render as dropdowns.
function nav_items(): array
{
    $blog = [['All Articles', '/blog/']];
    foreach (CATEGORIES as $slug => $c) {
        $blog[] = [$c['name'], "/category/$slug/"];
    }
    $tools = [['All Tools', '/tools/']];
    foreach (TOOLS as $slug => $t) {
        $tools[] = [$t['name'], "/tools/$slug/"];
    }
    return [
        ['Home', '/', []],
        ['About', '/about/', []],
        ['Blog', '/blog/', $blog],
        ['Tools', '/tools/', $tools],
        ['Start Here', '/start-here/', []],
        ['FAQ', '/faq/', []],
    ];
}
