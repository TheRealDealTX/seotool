<?php
declare(strict_types=1);

defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)

/** All services keyed by slug. */
function services(): array
{
    static $services = null;
    return $services ??= require FR_APP . '/content/services.php';
}

function service(string $slug): ?array
{
    $s = services()[$slug] ?? null;
    return $s ? $s + ['slug' => $slug, 'url' => '/services/' . $slug . '/'] : null;
}

/** All articles keyed by slug, newest first, with computed publication dates. */
function articles(): array
{
    static $articles = null;
    if ($articles !== null) {
        return $articles;
    }
    $launch = DateTimeImmutable::createFromFormat('!Y-m-d', (string) config('launch_date'), new DateTimeZone((string) config('timezone')));
    if (!$launch) {
        throw new RuntimeException('config/site.php launch_date must be YYYY-MM-DD');
    }
    $articles = [];
    foreach (require FR_APP . '/content/articles.php' as $slug => $a) {
        $date = $launch->modify('-' . (int) $a['days_before_launch'] . ' days');
        $a['slug'] = $slug;
        $a['url']  = '/blog/' . $slug . '/';
        $a['date'] = $date->format('Y-m-d');
        $a['date_iso'] = $date->format('Y-m-d\TH:i:sP');
        $a['category_slug'] = category_slug($a['category']);
        $articles[$slug] = $a;
    }
    uasort($articles, fn ($x, $y) => strcmp($y['date'], $x['date']));
    return $articles;
}

function article(string $slug): ?array
{
    return articles()[$slug] ?? null;
}

/** Article body + FAQs from content/articles/{slug}.php */
function article_content(string $slug): array
{
    $file = FR_APP . '/content/articles/' . basename($slug) . '.php';
    return is_file($file) ? require $file : ['body' => '', 'faqs' => []];
}

function category_slug(string $name): string
{
    return trim((string) preg_replace('/[^a-z0-9]+/', '-', strtolower(str_replace('&', 'and', $name))), '-');
}

/** Unique categories in display order: slug => name */
function article_categories(): array
{
    $cats = [];
    foreach (articles() as $a) {
        $cats[$a['category_slug']] = $a['category'];
    }
    return $cats;
}

function faq_groups(): array
{
    static $faqs = null;
    return $faqs ??= require FR_APP . '/content/faqs.php';
}

function home_faqs(): array
{
    $out = [];
    foreach (faq_groups() as $items) {
        foreach ($items as $item) {
            if (!empty($item['home'])) {
                $out[] = [$item['q'], $item['a']];
            }
        }
    }
    return $out;
}

/** Options for the "Service needed" field: value => label */
function service_options(): array
{
    $opts = [];
    foreach (services() as $slug => $s) {
        $opts[$slug] = $s['name'];
    }
    $opts['not-sure'] = 'Not sure / other';
    return $opts;
}

/**
 * Static page metadata. Titles and descriptions are unique per page.
 * 'crumb' is the breadcrumb label; 'parent' an optional parent path.
 */
function page_meta(): array
{
    return [
        '/' => [
            'template' => 'home',
            'title' => 'Friendswood Roofers | Roof Repair & Replacement in Friendswood, TX',
            'description' => 'Friendswood Roofers helps Friendswood, TX homeowners with roof repair, replacement, inspections, storm damage and maintenance. Call or request an estimate.',
            'form' => true,
        ],
        '/about/' => [
            'template' => 'about', 'crumb' => 'About',
            'title' => 'About Friendswood Roofers | Our Approach to Your Roof',
            'description' => 'Learn how Friendswood Roofers approaches roofing for Friendswood, TX homeowners: careful assessments, clear written estimates and honest recommendations.',
        ],
        '/services/' => [
            'template' => 'services', 'crumb' => 'Services',
            'title' => 'Roofing Services in Friendswood, TX | Friendswood Roofers',
            'description' => 'Explore roofing services for Friendswood, TX homes: roof repair, replacement, inspections, storm damage repair, asphalt shingles, metal roofing and maintenance.',
        ],
        '/service-area/' => [
            'template' => 'service-area', 'crumb' => 'Service Area',
            'title' => 'Roofing Service Area: Friendswood, TX | Friendswood Roofers',
            'description' => 'Friendswood Roofers serves homeowners in Friendswood, TX. See local roofing considerations for Friendswood homes and how to request an estimate.',
        ],
        '/faqs/' => [
            'template' => 'faqs', 'crumb' => 'FAQs',
            'title' => 'Roofing FAQs for Friendswood Homeowners | Friendswood Roofers',
            'description' => 'Answers to common roofing questions from Friendswood, TX homeowners about estimates, repairs, replacement, materials, inspections, storms and maintenance.',
        ],
        '/blog/' => [
            'template' => 'blog', 'crumb' => 'Blog',
            'title' => 'Roofing Blog: Guides for Friendswood Homeowners | Friendswood Roofers',
            'description' => 'Practical roofing guides for Friendswood, TX homeowners: choosing a contractor, repair vs. replacement, maintenance, materials and roof inspections.',
        ],
        '/contact/' => [
            'template' => 'contact', 'crumb' => 'Contact Us',
            'title' => 'Contact Friendswood Roofers | Request a Roofing Estimate',
            'description' => 'Call Friendswood Roofers or send an estimate request for roof repair, replacement, inspection or maintenance at your Friendswood, TX home.',
            'form' => true,
        ],
        '/roofing-project-planner/' => [
            'template' => 'planner', 'crumb' => 'Roofing Project Planner',
            'title' => 'Roofing Project Planner | Friendswood Roofers',
            'description' => 'Organize your roofing concern in five quick questions and get a summary you can copy or send with an estimate request to Friendswood Roofers.',
            'form' => true,
        ],
        '/privacy-policy/' => [
            'template' => 'privacy', 'crumb' => 'Privacy Policy',
            'title' => 'Privacy Policy | Friendswood Roofers',
            'description' => 'How the Friendswood Roofers website collects, uses and protects information submitted through the estimate form, and how third-party embeds work.',
        ],
        '/terms-of-use/' => [
            'template' => 'terms', 'crumb' => 'Terms of Use',
            'title' => 'Terms of Use | Friendswood Roofers',
            'description' => 'Terms that apply to using the Friendswood Roofers website, its content, the Roofing Project Planner and the estimate request form.',
        ],
        '/thank-you/' => [
            'template' => 'thank-you', 'crumb' => 'Request Received',
            'title' => 'Thank You | Friendswood Roofers',
            'description' => 'Confirmation that your estimate request was sent to Friendswood Roofers.',
            'noindex' => true, 'form' => true,
        ],
    ];
}
