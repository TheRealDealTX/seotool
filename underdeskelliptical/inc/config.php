<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
// Site-wide constants for underdeskelliptical.com. Every other file reads from here.

const SITE_NAME   = 'Under Desk Elliptical';
const SITE_URL    = 'https://underdeskelliptical.com';
const SITE_HOST   = 'underdeskelliptical.com';
const AMAZON_TAG  = 'underdeskellipticaljditt-20';
const GA_ID       = 'G-XZNNQ99Z4G';   // Google Analytics 4, loaded on every HTML page by inc/layout.php
const SITE_EMAIL  = 'hello@underdeskelliptical.com';
const SITE_TAGLINE = 'Honest guides to the best under desk ellipticals, desk bikes and seated workouts';
const SITE_LOGO   = '/wp-content/uploads/2026/04/Under-Desk-Elliptical-Logo.webp';
const SITE_ICON   = '/wp-content/uploads/2026/04/cropped-Under-Desk-Elliptical-Site-Icon-192x192.webp';
const DEFAULT_IMAGE = '/wp-content/uploads/2026/05/What-Is-the-Best-Under-Desk-Elliptical-1.webp';
const AUTHOR_NAME = 'Under Desk Elliptical Editorial Team';

// Last full content refresh; shown as "Updated" on posts that do not set their own date.
const SITE_UPDATED = '2026-10-22';

// Categories live at /topic/<slug>/ and tags at /tag/<slug>/ (the old WordPress URLs).
const CATEGORIES = [
    'top-picks'           => ['Top Picks', 'Our best under desk elliptical picks for every budget, body and workspace.'],
    'reviews'             => ['Reviews', 'In-depth under desk elliptical reviews: Cubii, DeskCycle, Geoneo, Flex Fitness, Yosuda and more.'],
    'compare'             => ['Compare', 'Head-to-head comparisons: under desk elliptical vs walking pad, bike and treadmill.'],
    'guides'              => ['Guides', 'Buying guides that explain how to choose the right under desk elliptical.'],
    'how-to'              => ['How To', 'Step-by-step help for setting up and using an under desk elliptical.'],
    'health-benefits'     => ['Health Benefits', 'What the research says about calories, muscles, steps and circulation.'],
    'desk-exercise'       => ['Desk Exercise', 'Ways to move more while you sit and work.'],
    'home-office-fitness' => ['Home Office Fitness', 'Fitness gear and habits for remote workers and home offices.'],
    'workplace-fitness'   => ['Workplace Fitness', 'Staying active through the workday at the office.'],
    'general'             => ['General', 'Everything else about under desk ellipticals.'],
];

const TAGS = [
    'best-of-2026'          => ['Best of 2026', 'The under desk ellipticals and desk exercisers that stand out this year.'],
    'best-for-seniors'      => ['Best for Seniors', 'Gentle, stable under desk ellipticals for older adults.'],
    'best-budget-options'   => ['Best Budget Options', 'Affordable under desk ellipticals that still work well.'],
    'quietest-models'       => ['Quietest Models', 'Under desk ellipticals quiet enough for calls, offices and shared homes.'],
    'desk-exercise'         => ['Desk Exercise', 'Movement you can do at your desk.'],
    'active-sitting'        => ['Active Sitting', 'Turning sitting time into light activity.'],
    'fitness-while-working' => ['Fitness While Working', 'Exercising during the workday without losing focus.'],
    'remote-work-fitness'   => ['Remote Work Fitness', 'Staying active when you work from home.'],
];

const NAV = [
    ['Best Picks', '/what-is-the-best-under-desk-elliptical/'],
    ['Reviews', '/topic/reviews/'],
    ['Compare', '/topic/compare/'],
    ['Guides', '/topic/guides/'],
    ['Tools', '/tools/'],
    ['Blog', '/blog/'],
];

// Contact form messages are saved to data/messages.php; set an address here to also email them.
const CONTACT_TO = '';
