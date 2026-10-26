<?php
// Site-wide constants for bettersidehustles.com.

const SITE_NAME   = 'Better Side Hustles';
const SITE_URL    = 'https://bettersidehustles.com';
const SITE_TAGLINE = 'Side hustle ideas, city guides and free calculators to help you earn more.';
const SITE_LOGO   = '/wp-content/uploads/2023/07/Better-Side-Hustles-Logo.webp';
const SITE_LOGO_FOOTER = '/wp-content/uploads/2023/07/Better-Side-Hustles-Footer-Logo.webp';
const SITE_ICON   = '/wp-content/uploads/2023/07/Better-Side-Hustles-Site-Icon.webp';
const SITE_IMAGE  = '/wp-content/uploads/2023/07/Better-Side-Hustles-Site-Image.webp';
const SITE_ORG_LOGO = '/wp-content/uploads/2023/07/Better-Side-Hustles-Org-Logo.webp';

// Where the contact form is delivered. Must be a mailbox on this domain (or one
// Hostinger is allowed to send for) so mail() is not rejected as spoofed.
const CONTACT_TO   = 'info@bettersidehustles.com';
const CONTACT_FROM = 'info@bettersidehustles.com';

// Google Analytics 4 measurement ID, loaded on every page by header.php.
const GA_ID = 'G-G882PM8VZ1';

// Amazon Associates tracking ID used on every Amazon link.
const AMAZON_TAG = 'bettersidehustles-20';

// Bumped whenever CSS/JS change so browsers fetch the new files.
const ASSET_VERSION = '2026.10.26b';

// Platform guides: slug => [label, logo, one-liner, icon category]
const PLATFORMS = [
    'fiverr'    => ['Fiverr', '/wp-content/uploads/2023/07/fiverr-logo.webp', 'Sell freelance services as fixed-price gigs.'],
    'lyft-uber' => ['Uber & Lyft', '/wp-content/uploads/2023/07/uber-logo.webp', 'Drive on your own schedule in any city.'],
    'thinkific' => ['Thinkific', '/wp-content/uploads/2023/07/thinkific-logo.webp', 'Sell your own course and keep the students.'],
    'skillshare'=> ['Skillshare', '/wp-content/uploads/2023/07/skillshare-logo.webp', 'Get paid royalties for minutes watched.'],
    'udemy'     => ['Udemy', '/wp-content/uploads/2023/07/udemy-logo.webp', 'Reach millions of students with one course.'],
    'coursera'  => ['Coursera', '/wp-content/uploads/2023/07/coursera-logo.webp', 'Earn certificates that unlock paid skills.'],
    'shopify'   => ['Shopify', '/wp-content/uploads/2023/07/shopify-logo.webp', 'Launch an online store in a weekend.'],
    'semrush'   => ['Semrush', '/wp-content/uploads/2023/07/semrush-logo.webp', 'Earn affiliate commissions and sell SEO.'],
];

// Free tools: slug => [key, name, short description, icon]
const TOOLS = [
    'side-hustle-quiz'              => ['quiz', 'Side Hustle Matcher Quiz', 'Answer 6 questions and get the side hustles that fit your time, skills and goals.', 'target'],
    'income-calculator'             => ['income-calculator', 'Side Hustle Income Calculator', 'See what your hours are worth per month and year — and how fast you hit a savings goal.', 'chart'],
    'gig-earnings-calculator'       => ['gig-calculator', 'Gig Driver Earnings Calculator', 'Uber, Lyft, DoorDash: find your true hourly pay after gas and wear.', 'car'],
    'self-employment-tax-calculator'=> ['tax-estimator', 'Side Hustle Tax Calculator', 'Estimate self-employment and income tax so April never surprises you.', 'receipt'],
    'course-revenue-calculator'     => ['course-calculator', 'Online Course Revenue Calculator', 'Compare what one course earns on Udemy, Skillshare and Thinkific.', 'play'],
    'freelance-rate-calculator'     => ['freelance-rate', 'Freelance Rate Calculator', 'Work out the hourly or gig price you need — including Fiverr\'s 20% fee.', 'briefcase'],
    'product-profit-calculator'     => ['shopify-profit', 'Product Profit Calculator', 'Margin, profit per sale and break-even for Shopify, Etsy or Amazon products.', 'cart'],
    'affiliate-commission-calculator'=> ['affiliate-calculator', 'Affiliate Commission Calculator', 'Project monthly affiliate income from traffic, click-through and conversion rates.', 'link'],
];

const NAV = [
    ['Side Hustles', '#', 'platforms'],
    ['City Guides', '/blog/?cat=city-guides', null],
    ['Free Tools', '/tools/', 'tools'],
    ['Gear', '/side-hustle-gear/', null],
    ['Blog', '/blog/', null],
    ['About', '/about/', null],
    ['Contact', '/contact/', null],
];

// Old WordPress URLs that no longer have their own page.
const REDIRECTS = [
    '/write-for-us/'   => '/contact/',
    '/category/blog/'  => '/blog/',
    '/author/adrian/'  => '/about/',
    '/comments/feed/'  => '/feed/',
    '/home/'           => '/',
    '/side-hustles/'   => '/blog/',
];
