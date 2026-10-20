<?php
/**
 * Permanent (301) redirects for legacy WordPress URLs.
 * Every original page and post keeps its exact URL, so these only cover
 * WordPress-generated archives, shortlinks, and sitemaps.
 */
return [
    'paths' => [
        '/home/'                                  => '/',
        '/category/general/'                      => '/blog/',
        '/category/uncategorized/'                => '/blog/',
        '/author/infohoustonpublicadjusting-com/' => '/author/joseph-dittman/',
        '/author/admin/'                          => '/author/joseph-dittman/',
        '/comments/feed/'                         => '/feed/',
        '/category/general/feed/'                 => '/feed/',
        '/sitemap_index.xml'                      => '/sitemap.xml',
        '/wp-sitemap.xml'                         => '/sitemap.xml',
        '/post-sitemap.xml'                       => '/sitemap.xml',
        '/page-sitemap.xml'                       => '/sitemap.xml',
        '/category-sitemap.xml'                   => '/sitemap.xml',
        '/author-sitemap.xml'                     => '/sitemap.xml',
        '/contact-us/'                            => '/contact/',
        '/about/'                                 => '/about-us/',
        '/claim-tools/claim-calculator/'          => '/claim-calculator/',
        '/tools/'                                 => '/claim-tools/',
        '/building-codes/'                        => '/local-building-codes/',
        '/free-claim-review-form/'                => '/free-claim-review/',
        '/faqs/'                                  => '/faq/',
        '/areas-we-serve/'                        => '/service-areas/',
        '/category/general/page/2/'               => '/blog/',
        '/what-is-a-public-adjuster/'             => '/what-is-a-public-claims-adjuster/',
        '/when-to-call-a-public-adjuster/'        => '/knowing-when-to-call-a-public-adjuster/',
        '/hail-damage-claim-supplements-what-carriers-miss-in-their-scope-xactimate-insights/' => '/hail-damage-claim-supplements-what-carriers-miss-in-their-scope/',
    ],
    // WordPress ?p= and ?page_id= shortlinks (IDs from the original site).
    'ids' => [
        243 => '/public-adjuster-vs-insurance-adjuster-for-hail-claims-in-texas/',
        236 => '/hail-damage-claim-supplements-what-carriers-miss-in-their-scope/',
        229 => '/what-to-do-if-your-hail-claim-was-denied-in-texas/',
        222 => '/document-hail-damage-for-an-insurance-claim/',
        216 => '/hail-damage-roof-insurance-claim-how-to-protect-your-roof/',
        208 => '/fire-insurance-adjuster/',
        197 => '/knowing-when-to-call-a-public-adjuster/',
        190 => '/what-is-a-public-claims-adjuster/',
        30  => '/terms-of-use/',
        28  => '/contact/',
        26  => '/blog/',
        24  => '/services/',
        22  => '/about-us/',
        19  => '/',
        3   => '/privacy-policy/',
    ],
];
