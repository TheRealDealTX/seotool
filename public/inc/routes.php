<?php
/**
 * URL registry. Every public page is listed here exactly once; the router,
 * the hubs, the related-links blocks and sitemap.xml all read from it.
 *
 *   path => [kind, source, section]
 *   kind:    'article' (content/<source>.php rendered by render_article)
 *            'page'    (pages/<source>.php renders itself)
 *            'tool'    (pages/tools/<source>.php)
 *   section: used for hubs, breadcrumbs and schema
 */
defined('SCC') || exit;

const SECTIONS = [
    'pillar'          => ['Essentials',      '/solar-camera-guides/#essentials'],
    'guides'          => ['Guides',          '/solar-camera-guides/#guides'],
    'use-cases'       => ['Use Cases',       '/solar-camera-guides/#use-cases'],
    'how-to'          => ['How-To',          '/solar-camera-guides/#how-to'],
    'reviews'         => ['Reviews',         '/solar-camera-guides/#reviews'],
    'compare'         => ['Comparisons',     '/solar-camera-guides/#how-to'],
    'troubleshooting' => ['Troubleshooting', '/solar-camera-guides/#how-to'],
    'tools'           => ['Tools',           '/tools/'],
    'site'            => ['',                '/'],
];

function routes(): array
{
    return [
        '/'                                   => ['page', 'home', 'site'],
        // Pillars
        '/best-solar-security-cameras/'       => ['article', 'best-solar-security-cameras', 'pillar'],
        '/how-solar-cameras-work/'            => ['article', 'how-solar-cameras-work', 'pillar'],
        '/solar-camera-installation/'         => ['article', 'solar-camera-installation', 'pillar'],
        '/compare/solar-vs-wired/'            => ['article', 'solar-vs-wired', 'compare'],
        // Guides
        '/guides/solar-camera-panel-angle/'               => ['article', 'solar-camera-panel-angle', 'guides'],
        '/guides/do-solar-cameras-work-at-night/'         => ['article', 'do-solar-cameras-work-at-night', 'guides'],
        '/guides/do-solar-cameras-need-wifi/'             => ['article', 'do-solar-cameras-need-wifi', 'guides'],
        '/guides/do-solar-cameras-need-direct-sunlight/'  => ['article', 'do-solar-cameras-need-direct-sunlight', 'guides'],
        '/guides/do-solar-cameras-work-in-winter/'        => ['article', 'do-solar-cameras-work-in-winter', 'guides'],
        '/guides/solar-camera-battery-life-no-sun/'       => ['article', 'solar-camera-battery-life-no-sun', 'guides'],
        '/guides/how-many-solar-cameras-can-one-panel-power/' => ['article', 'how-many-solar-cameras-can-one-panel-power', 'guides'],
        '/guides/how-many-cctv-cameras-do-i-need/'        => ['article', 'how-many-cctv-cameras-do-i-need', 'guides'],
        '/guides/are-solar-cameras-worth-it/'             => ['article', 'are-solar-cameras-worth-it', 'guides'],
        '/guides/360-degree-solar-camera/'                => ['article', '360-degree-solar-camera', 'guides'],
        '/guides/solar-camera-driveway-alert-phone/'      => ['article', 'solar-camera-driveway-alert-phone', 'guides'],
        '/guides/solar-gate-camera/'                      => ['article', 'solar-gate-camera', 'guides'],
        '/guides/solar-street-light-with-cctv-camera-price/' => ['article', 'solar-street-light-with-cctv-camera-price', 'guides'],
        '/guides/rental-property-outdoor-camera-no-subscription/' => ['article', 'rental-property-outdoor-camera-no-subscription', 'guides'],
        // Use cases
        '/use-cases/solar-cameras-for-farms/'             => ['article', 'solar-cameras-for-farms', 'use-cases'],
        '/use-cases/solar-cameras-rural-property/'        => ['article', 'solar-cameras-rural-property', 'use-cases'],
        '/use-cases/solar-cameras-for-rvs/'               => ['article', 'solar-cameras-for-rvs', 'use-cases'],
        '/use-cases/solar-cameras-for-construction-sites/' => ['article', 'solar-cameras-for-construction-sites', 'use-cases'],
        '/guides/remote-cabin-solar-camera/'              => ['article', 'remote-cabin-solar-camera', 'use-cases'],
        '/guides/portable-solar-camera-camping/'          => ['article', 'portable-solar-camera-camping', 'use-cases'],
        // Reviews / how-to / troubleshooting
        '/reviews/solar-cctv-camera-with-sim-card/'       => ['article', 'solar-cctv-camera-with-sim-card', 'reviews'],
        '/how-to/install-without-drilling/'               => ['article', 'install-without-drilling', 'how-to'],
        '/how-to/reset-solar-camera/'                     => ['article', 'reset-solar-camera', 'how-to'],
        '/troubleshooting/not-charging/'                  => ['article', 'not-charging', 'troubleshooting'],
        // Tools
        '/tools/'                                         => ['page', 'tools-hub', 'site'],
        '/tools/solar-panel-angle-calculator/'            => ['tool', 'panel-angle', 'tools'],
        '/tools/solar-camera-battery-calculator/'         => ['tool', 'battery', 'tools'],
        '/tools/cctv-camera-planner/'                     => ['tool', 'planner', 'tools'],
        '/tools/solar-camera-site-check/'                 => ['tool', 'site-check', 'tools'],
        '/tools/4g-data-and-storage-calculator/'          => ['tool', 'data', 'tools'],
        '/tools/camera-coverage-calculator/'              => ['tool', 'coverage', 'tools'],
        '/tools/solar-vs-wired-cost-calculator/'          => ['tool', 'cost', 'tools'],
        // Hubs and company pages
        '/solar-camera-guides/'                           => ['page', 'guides-hub', 'site'],
        '/about-us/'                                      => ['page', 'about', 'site'],
        '/contact/'                                       => ['page', 'contact', 'site'],
        '/affiliate-disclosure/'                          => ['page', 'affiliate-disclosure', 'site'],
        '/privacy-policy/'                                => ['page', 'privacy-policy', 'site'],
        '/terms-of-use/'                                  => ['page', 'terms-of-use', 'site'],
        '/sitemap/'                                       => ['page', 'html-sitemap', 'site'],
    ];
}

/**
 * Old WordPress URLs -> new home. Consolidates duplicate articles, thin
 * category/tag archives and pages that were deleted in June 2026 but still
 * had search impressions.
 */
function redirects(): array
{
    return [
        '/guides/how-does-solar-camera-work/'                 => '/how-solar-cameras-work/',
        '/reviews/are-solar-powered-cctv-cameras-any-good/'   => '/guides/are-solar-cameras-worth-it/',
        '/reviews/are-solar-powered-security-cameras-any-good/' => '/guides/are-solar-cameras-worth-it/',
        '/guides/solar-camera-for-barn/'                      => '/use-cases/solar-cameras-for-farms/',
        '/guides/cattle-ranch-security-camera-solar/'         => '/use-cases/solar-cameras-for-farms/',
        '/guides/solar-cctv-for-pasture/'                     => '/use-cases/solar-cameras-for-farms/',
        '/guides/camper-security-camera-solar/'               => '/use-cases/solar-cameras-for-rvs/',
        '/guides/solar-driveway-camera/'                      => '/guides/solar-camera-driveway-alert-phone/',
        '/guides/off-grid-security-camera-solar/'             => '/use-cases/solar-cameras-rural-property/',
        '/guides/solar-camera-no-internet/'                   => '/guides/do-solar-cameras-need-wifi/',
        '/guides/tenant-proof-camera/'                        => '/guides/rental-property-outdoor-camera-no-subscription/',
        '/guides/construction-site-cctv-solar/'               => '/use-cases/solar-cameras-for-construction-sites/',
        '/guides/solar-powered-security-camera-for-construction-site/' => '/use-cases/solar-cameras-for-construction-sites/',
        '/guides/temporary-solar-camera-job-site/'            => '/use-cases/solar-cameras-for-construction-sites/',
        '/guides/solar-security-camera-with-floodlight/'      => '/best-solar-security-cameras/',
        '/guides/best-outdoor-wireless-security-camera-system-solar-powered/' => '/best-solar-security-cameras/',
        '/guides/are-solar-cameras-reliable-year-round/'      => '/guides/do-solar-cameras-work-in-winter/',
        '/category/guides/'          => '/solar-camera-guides/',
        '/category/use-cases/'       => '/solar-camera-guides/',
        '/category/reviews/'         => '/solar-camera-guides/',
        '/category/how-to/'          => '/solar-camera-installation/',
        '/category/troubleshooting/' => '/troubleshooting/not-charging/',
        '/category/compare/'         => '/compare/solar-vs-wired/',
        '/tag/rv-camera/'            => '/use-cases/solar-cameras-for-rvs/',
        '/tag/rural-property/'       => '/use-cases/solar-cameras-rural-property/',
        '/tag/off-grid/'             => '/use-cases/solar-cameras-rural-property/',
        '/tag/farm-security/'        => '/use-cases/solar-cameras-for-farms/',
        '/tag/construction-site/'    => '/use-cases/solar-cameras-for-construction-sites/',
        '/tag/rental-property/'      => '/guides/rental-property-outdoor-camera-no-subscription/',
        '/tag/no-subscription/'      => '/guides/rental-property-outdoor-camera-no-subscription/',
        '/tag/4g-cellular/'          => '/reviews/solar-cctv-camera-with-sim-card/',
        '/tag/no-wifi/'              => '/guides/do-solar-cameras-need-wifi/',
        '/tag/night-vision/'         => '/guides/do-solar-cameras-work-at-night/',
        '/tag/battery-life/'         => '/guides/solar-camera-battery-life-no-sun/',
        '/tag/solar-panel/'          => '/guides/solar-camera-panel-angle/',
        '/tag/local-storage/'        => '/tools/4g-data-and-storage-calculator/',
        '/tag/reolink/'              => '/best-solar-security-cameras/',
        '/tag/eufy/'                 => '/best-solar-security-cameras/',
        '/tag/arlo/'                 => '/best-solar-security-cameras/',
        '/tag/ring/'                 => '/best-solar-security-cameras/',
        '/tag/wyze/'                 => '/best-solar-security-cameras/',
        '/tag/solar-camera/'         => '/solar-camera-guides/',
        '/tag/security-camera/'      => '/solar-camera-guides/',
        '/feed/'                     => '/solar-camera-guides/',
        '/comments/feed/'            => '/solar-camera-guides/',
        '/sitemap_index.xml'         => '/sitemap.xml',
        '/post-sitemap.xml'          => '/sitemap.xml',
        '/page-sitemap.xml'          => '/sitemap.xml',
        '/category-sitemap.xml'      => '/sitemap.xml',
        '/post_tag-sitemap.xml'      => '/sitemap.xml',
        '/solar-cctv-camera/'        => '/',
        '/home/'                     => '/',
        '/blog/'                     => '/solar-camera-guides/',
        '/guides/'                   => '/solar-camera-guides/',
        '/reviews/'                  => '/solar-camera-guides/',
        '/use-cases/'                => '/solar-camera-guides/',
        '/how-to/'                   => '/solar-camera-installation/',
        '/compare/'                  => '/compare/solar-vs-wired/',
        '/troubleshooting/'          => '/troubleshooting/not-charging/',
        '/tools/how-many-cctv-cameras/' => '/tools/cctv-camera-planner/',
    ];
}

/** Article metadata (cached per request). */
function article(string $source): array
{
    static $cache = [];
    if (!isset($cache[$source])) {
        $f = ROOT . "/content/$source.php";
        $cache[$source] = is_file($f) ? (array) (include $f) : [];
    }
    return $cache[$source];
}

/** path => meta for every article, optionally filtered by section. */
function articles(?string $section = null): array
{
    $out = [];
    foreach (routes() as $path => [$kind, $src, $sec]) {
        if ($kind !== 'article' || ($section && $sec !== $section)) continue;
        $a = article($src);
        if (!$a) continue;
        $a['path'] = $path;
        $a['section'] = $sec;
        $out[$path] = $a;
    }
    return $out;
}

/** Tool metadata from pages/tools/_meta.php */
function tools_meta(): array
{
    static $m = null;
    return $m ??= (array) include ROOT . '/pages/tools/_meta.php';
}

function route_title(string $path): string
{
    $r = routes()[$path] ?? null;
    if (!$r) return $path;
    if ($r[0] === 'article') return article($r[1])['h1'] ?? $path;
    if ($r[0] === 'tool') return tools_meta()[$r[1]]['name'] ?? $path;
    return [
        '/' => 'Home', '/tools/' => 'Solar Camera Tools', '/solar-camera-guides/' => 'Solar Camera Guides',
        '/about-us/' => 'About Us', '/contact/' => 'Contact', '/affiliate-disclosure/' => 'Affiliate Disclosure',
        '/privacy-policy/' => 'Privacy Policy', '/terms-of-use/' => 'Terms of Use', '/sitemap/' => 'Sitemap',
    ][$path] ?? $path;
}
