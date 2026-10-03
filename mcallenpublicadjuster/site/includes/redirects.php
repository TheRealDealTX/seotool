<?php
/**
 * Permanent (301) redirects for legacy WordPress URLs.
 * Every original page and post keeps its exact URL, so these only cover
 * WordPress-generated archives, shortlinks, and sitemaps.
 */
return [
    'paths' => [
        '/home/'                                 => '/',
        '/category/general/'                     => '/blog/',
        '/category/uncategorized/'               => '/blog/',
        '/author/infohoustonpublicadjusting-com/' => '/author/joseph-dittman/',
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
    ],
    // WordPress ?p= and ?page_id= shortlinks (IDs from the original site).
    'ids' => [
        282 => '/public-adjuster-vs-insurance-adjuster-for-hail-claims/',
        275 => '/hail-damage-claim-supplements/',
        267 => '/what-to-do-if-your-hail-claim-was-denied-in-mcallen/',
        258 => '/document-hail-damage-for-an-insurance-claim/',
        252 => '/roof-hail-damage-insurance-claim-mcallen/',
        243 => '/fire-insurance-adjuster/',
        232 => '/claim-changes-knowing-when-to-hire-a-public-adjuster/',
        228 => '/fire-insurance-public-adjuster/',
        30  => '/terms-of-use/',
        28  => '/contact/',
        26  => '/blog/',
        24  => '/services/',
        22  => '/about-us/',
        19  => '/',
        3   => '/privacy-policy/',
    ],
];
