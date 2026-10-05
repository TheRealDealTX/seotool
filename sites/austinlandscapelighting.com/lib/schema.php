<?php
/**
 * JSON-LD builders. Each returns an associative array; render_page() encodes
 * the whole graph once per page.
 */
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

function schema_org(): array
{
    $areas = [];
    foreach (areas() as $a) {
        $areas[] = ['@type' => 'City', 'name' => $a['city'] . ', TX'];
    }
    if (!$areas) {
        $areas[] = ['@type' => 'City', 'name' => 'Austin, TX'];
    }
    return [
        '@type' => ['HomeAndConstructionBusiness', 'LocalBusiness', 'Organization'],
        '@id' => url('/#organization'),
        'name' => BIZ['name'],
        'url' => url('/'),
        'telephone' => BIZ['phone_e164'],
        'email' => BIZ['email'],
        'description' => 'Austin Landscape Lighting designs, installs and maintains low-voltage LED landscape lighting for homes and businesses in Austin, TX and the surrounding Hill Country communities.',
        'foundingDate' => BIZ['founded'],
        'priceRange' => BIZ['price_range'],
        'image' => url('/assets/img/brand/austin-landscape-lighting-site-image.webp'),
        'logo' => ['@type' => 'ImageObject', 'url' => url('/assets/img/brand/austin-landscape-lighting-logo.webp'), 'width' => 500, 'height' => 81],
        'address' => ['@type' => 'PostalAddress', 'addressLocality' => 'Austin', 'addressRegion' => 'TX', 'addressCountry' => 'US'],
        'geo' => ['@type' => 'GeoCoordinates', 'latitude' => BIZ['lat'], 'longitude' => BIZ['lng']],
        'areaServed' => $areas,
        'openingHoursSpecification' => [
            ['@type' => 'OpeningHoursSpecification', 'dayOfWeek' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens' => '08:00', 'closes' => '18:00'],
            ['@type' => 'OpeningHoursSpecification', 'dayOfWeek' => ['Saturday'], 'opens' => '09:00', 'closes' => '14:00'],
        ],
        'knowsAbout' => ['Landscape lighting design', 'Low-voltage LED lighting', 'Architectural uplighting', 'Tree moonlighting', 'Path lighting', 'Smart outdoor lighting'],
        'hasOfferCatalog' => [
            '@type' => 'OfferCatalog',
            'name' => 'Landscape lighting services',
            'itemListElement' => array_values(array_map(fn($s) => [
                '@type' => 'Offer',
                'itemOffered' => ['@type' => 'Service', 'name' => $s['name'], 'url' => url($s['path'])],
            ], services())),
        ],
    ];
}

function schema_website(): array
{
    return [
        '@type' => 'WebSite',
        '@id' => url('/#website'),
        'url' => url('/'),
        'name' => BIZ['name'],
        'publisher' => ['@id' => url('/#organization')],
        'inLanguage' => 'en-US',
    ];
}

function schema_webpage(array $page, string $type = 'WebPage'): array
{
    $s = [
        '@type' => $type,
        '@id' => url($page['path']) . '#webpage',
        'url' => url($page['path']),
        'name' => $page['title'],
        'description' => $page['description'],
        'isPartOf' => ['@id' => url('/#website')],
        'about' => ['@id' => url('/#organization')],
        'inLanguage' => 'en-US',
    ];
    if (!empty($page['image'])) {
        $s['primaryImageOfPage'] = ['@type' => 'ImageObject', 'url' => url(img($page['image']))];
    }
    return $s;
}

/** $trail = [['Home','/'], ['Services','/services/'], ['Name', '/services/x/']] */
function schema_breadcrumb(array $trail): array
{
    $items = [];
    foreach ($trail as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function schema_service(array $s): array
{
    return [
        '@type' => 'Service',
        '@id' => url($s['path']) . '#service',
        'name' => $s['name'],
        'serviceType' => $s['name'],
        'description' => $s['description'],
        'url' => url($s['path']),
        'provider' => ['@id' => url('/#organization')],
        'areaServed' => array_values(array_map(fn($a) => ['@type' => 'City', 'name' => $a['city'] . ', TX'], areas())),
        'image' => url(img($s['image'])),
    ];
}

function schema_faq(array $faqs): array
{
    return [
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type' => 'Question',
            'name' => $f['q'],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']],
        ], array_values($faqs)),
    ];
}

function schema_article(array $p): array
{
    return [
        '@type' => 'BlogPosting',
        '@id' => url($p['path']) . '#article',
        'headline' => $p['h1'],
        'description' => $p['description'],
        'image' => url(img($p['image'])),
        'datePublished' => $p['published'],
        'dateModified' => $p['modified'] ?? $p['published'],
        'author' => ['@id' => url('/#organization')],
        'publisher' => ['@id' => url('/#organization')],
        'mainEntityOfPage' => url($p['path']),
        'articleSection' => $p['category'],
        'wordCount' => $p['words'],
        'inLanguage' => 'en-US',
    ];
}

function schema_itemlist(array $items, string $name): array
{
    $els = [];
    foreach (array_values($items) as $i => [$label, $path]) {
        $els[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'url' => url($path)];
    }
    return ['@type' => 'ItemList', 'name' => $name, 'itemListElement' => $els];
}

function schema_tool(array $t): array
{
    return [
        '@type' => 'WebApplication',
        'name' => $t['name'] . ' by Austin Landscape Lighting',
        'url' => url($t['path']),
        'applicationCategory' => 'UtilitiesApplication',
        'operatingSystem' => 'Any',
        'browserRequirements' => 'Requires JavaScript',
        'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
        'provider' => ['@id' => url('/#organization')],
        'description' => $t['description'],
    ];
}

function schema_encode(array $graph): string
{
    return json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
}
