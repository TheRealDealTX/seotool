<?php
/**
 * Permanent (301) redirects for legacy WordPress URLs.
 * Every original page and post keeps its exact URL (including /category/general/),
 * so these only cover WordPress-generated feeds, shortlinks, and sitemaps.
 */
return [
    'paths' => [
        '/home/'                                 => '/',
        '/category/uncategorized/'               => '/category/general/',
        '/author/admin/'                         => '/author/joseph-dittman/',
        '/comments/feed/'                        => '/feed/',
        '/category/general/feed/'                => '/feed/',
        '/sitemap_index.xml'                     => '/sitemap.xml',
        '/wp-sitemap.xml'                        => '/sitemap.xml',
        '/post-sitemap.xml'                      => '/sitemap.xml',
        '/page-sitemap.xml'                      => '/sitemap.xml',
        '/category-sitemap.xml'                  => '/sitemap.xml',
        '/author-sitemap.xml'                    => '/sitemap.xml',
        '/contact-us/'                           => '/contact/',
        '/about/'                                => '/about-us/',
        '/claim-tools/claim-calculator/'         => '/claim-calculator/',
        '/tools/'                                => '/claim-tools/',
        '/building-codes/'                       => '/local-building-codes/',
        '/free-claim-review-form/'               => '/free-claim-review/',
        '/hurricane-tracker-port-arthur/'        => '/hurricane-tracker/',
        '/faqs/'                                 => '/faq/',
    ],
    // WordPress ?p= and ?page_id= shortlinks (IDs from the original site).
    'ids' => [
        251 => '/are-insurance-adjusters-honest/',
        30  => '/terms-of-use/',
        28  => '/contact/',
        26  => '/blog/',
        24  => '/services/',
        22  => '/about-us/',
        19  => '/',
        3   => '/privacy-policy/',
    ],
];
