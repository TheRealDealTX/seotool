<?php
/**
 * Monetizing Influencers - site-wide constants.
 * Every page includes inc/layout.php, which includes this file.
 */

const SITE_NAME   = 'Monetizing Influencers';
const SITE_URL    = 'https://monetizinginfluencers.com';
const SITE_TAG    = 'Get Paid More From Your Audience';
const SITE_EMAIL  = 'info@monetizinginfluencers.com';
const SITE_PHONE  = '210-903-9471';
const SITE_PHONE_HREF = '+12109039471';
const SITE_STREET = '2140 E Southlake Blvd';
const SITE_CITY   = 'Southlake';
const SITE_REGION = 'TX';
const SITE_ZIP    = '76092';
const ASSET_VER   = '20261025';

/** Primary navigation: label => [url, children[]] */
function site_nav(): array
{
    return [
        'Monetization' => ['/monetization/', [
            'Influencer Monetization Guide' => '/monetization/',
            'Brand Outreach'                => '/monetization/#brand-outreach',
            'Partnership Deals'             => '/monetization/#partnership-deals',
            'Ad Placements'                 => '/monetization/#ad-placements',
            'White Labeling Products'       => '/monetization/#white-labeling',
            'Short Content Distribution'    => '/monetization/#short-content',
        ]],
        'Platforms' => ['/social-platforms/', [
            'All Social Platforms' => '/social-platforms/',
            'YouTube'              => '/social-platforms/youtube/',
            'TikTok'               => '/social-platforms/tiktok/',
            'Instagram'            => '/social-platforms/instagram/',
            'Facebook'             => '/social-platforms/facebook/',
            'Pinterest'            => '/social-platforms/pinterest/',
        ]],
        'Free Tools' => ['/tools/', [
            'All Creator Tools'           => '/tools/',
            'Influencer Earnings Calculator' => '/tools/influencer-earnings-calculator/',
            'Engagement Rate Calculator'  => '/tools/engagement-rate-calculator/',
            'Influencer Email Generator'  => '/tools/influencer-email-generator/',
            'Media Kit Builder'           => '/tools/media-kit-builder/',
            'Income Stream Simulator'     => '/tools/income-stream-simulator/',
            'Monetization Readiness Quiz' => '/tools/monetization-readiness-quiz/',
        ]],
        'Web Design' => ['/website-design/', []],
        'Blog'       => ['/blogs/', []],
        'Write For Us' => ['/write-for-us/', []],
    ];
}

/** Blog posts, newest first. Used by /blogs/, the homepage and related-post cards. */
function site_posts(): array
{
    return [
        ['/how-to-write-to-an-influencer/', 'How to Write to an Influencer (With 7 Copy-Paste Templates)', 'Outreach', '2026-10-25',
            'The exact email and DM structure that gets influencers to reply, plus templates for Instagram, TikTok, YouTube and Facebook creators.'],
        ['/how-much-should-influencers-charge/', 'How Much Should Influencers Charge? 2026 Rate Guide', 'Pricing', '2026-10-25',
            'Per-post rate ranges by platform and follower tier, the formula brands use, and how to raise your rates without losing deals.'],
        ['/how-to-get-brand-deals/', 'How to Get Brand Deals as a Micro-Influencer', 'Brand Deals', '2026-10-25',
            'A step-by-step system for finding, pitching and closing paid brand partnerships when you have 5K to 100K followers.'],
        ['/influencer-media-kit/', 'How to Make an Influencer Media Kit That Wins Deals', 'Brand Deals', '2026-10-25',
            'What to put in a media kit, which numbers brands actually check, and a free builder to make yours in five minutes.'],
        ['/affiliate-marketing-for-influencers/', 'Affiliate Marketing for Influencers: The Complete Playbook', 'Income Streams', '2026-10-25',
            'How creators earn commission on every sale, the best places to put links, and how to disclose them the right way.'],
        ['/how-to-make-money-on-pinterest/', 'How to Make Money on Pinterest as an Influencer', 'Pinterest', '2026-10-25',
            'Idea Pins, affiliate pins, brand collaborations and traffic-to-product funnels: every way Pinterest pays creators.'],
        ['/monetizing-your-brand-the-power-of-influencer-marketing/', 'Monetizing Your Brand: The Power of Influencer Marketing', 'Strategy', '2023-07-07',
            'Brand collaborations, sponsored content, merch, content services and more: the core ways influencers turn a following into a business.'],
    ];
}

/** Escape for HTML output. */
function e(string $s): string
{
    return htmlspecialchars($s, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}
