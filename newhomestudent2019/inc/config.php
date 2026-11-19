<?php defined('NHS') || exit;
/* Site-wide settings. Edit here, not in templates. */
const SITE = [
    'name'        => 'New Home Investing Knowledge',
    'short'       => 'New Home Investing Knowledge',
    'tagline'     => 'Training, tools & honest advice for building your dream home',
    'origin'      => 'https://newhomestudent2019.com',
    'email'       => 'info@newhomestudent2019.com',
    'phone'       => '(832) 720-7978',
    'phone_href'  => '+18327207978',
    'author'      => 'Jonathon',
    'region'      => 'Texas',
    'amazon_tag'  => 'newhomestudent2019-20',
    'gtm_id'      => 'GTM-N59TH97L',          // Google Tag Manager container
    'lead_to'     => 'info@newhomestudent2019.com',   // where free-training sign-ups are emailed
    'mail_from'   => 'info@newhomestudent2019.com',
    'per_page'    => 12,
];

const CATEGORIES = [
    'building-tips' => [
        'name' => 'New Home Building Tips',
        'title' => 'New Home Building Tips & Guides for Owner-Builders',
        'description' => 'Step-by-step guides on planning, budgeting, permitting and building a new home in Texas — written for owner-builders and anyone hiring a builder.',
        'intro' => 'Everything we know about planning, budgeting, permitting and building a new home — from picking a lot to the final inspection.',
    ],
    'tips' => [
        'name' => 'Buying, Moving & Homeowner Tips',
        'title' => 'Home Buying, Moving & New Homeowner Tips',
        'description' => 'Practical advice on buying a home in Texas, relocating, moving with pets, and setting up your new house the right way.',
        'intro' => 'Buying instead of building? Moving across Texas? Just got the keys? Start here.',
    ],
    'real-estate-investing' => [
        'name' => 'Real Estate Investing',
        'title' => 'New Home & Rental Property Investing Guides',
        'description' => 'House hacking, off-market deals, appraisals and insurance claims — practical real estate investing guides for new and aspiring investors.',
        'intro' => 'Use what you learn building and owning a home to build long-term wealth through real estate.',
    ],
    'apartment-living' => [
        'name' => 'Renting & Apartment Living',
        'title' => 'Apartment Living Tips for Renters Saving for a Home',
        'description' => 'Apartment guides, renter tips and small-space ideas for Houston, Austin and Texas renters who are saving for, or planning, their own home.',
        'intro' => 'Many of our readers rent while they save for or build a home. These guides help you rent smarter in the meantime.',
    ],
];

/* Old WordPress taxonomy URLs -> new homes (301). */
const LEGACY_REDIRECTS = [
    '/category/uncategorized/' => '/blog/',
    '/tag/miscellaneous/'      => '/blog/',
    '/tag/tiny-homes/'         => '/is-it-worth-building-tiny-homes-in-texas-in-2023-exploring-the-trend-and-practicality/',
    '/tag/house-build/'        => '/category/building-tips/',
    '/tag/real-estate/'        => '/category/real-estate-investing/',
    '/tag/renovation/'         => '/recognizing-the-signs-is-it-time-for-a-full-house-renovation/',
    '/home/'                   => '/',
    '/sitemap_index.xml'       => '/sitemap.xml',
    '/wp-sitemap.xml'          => '/sitemap.xml',
    '/post-sitemap.xml'        => '/sitemap.xml',
    '/page-sitemap.xml'        => '/sitemap.xml',
    '/comments/feed/'          => '/feed/',
];

/* Main navigation. */
const NAV = [
    ['Start Here', '/build-a-home-yourself/'],
    ['Free Training', '/free-training/'],
    ['Blog', '/blog/'],
    ['Recommended Tools', '/our-products/'],
    ['Resources', '/resources/'],
    ['About', '/about-us/'],
];
