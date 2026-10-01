<?php
declare(strict_types=1);

/**
 * Structured data. Only verified business details are used: name, website,
 * phone and the city served. No street address, ratings, reviews,
 * credentials or opening hours are included because none are confirmed.
 */
function business_schema(): array
{
    $areas = [];
    foreach ((array) config('service_cities', ['Friendswood']) as $city) {
        $areas[] = [
            '@type' => 'City',
            'name'  => $city . ', ' . config('state'),
            'containedInPlace' => ['@type' => 'State', 'name' => config('state_name')],
        ];
    }
    return [
        '@type'     => 'RoofingContractor',
        '@id'       => abs_url('/#business'),
        'name'      => config('name'),
        'url'       => abs_url('/'),
        'telephone' => config('phone_tel'),
        'logo'      => abs_url('/assets/img/logo-mark.png'),
        'image'     => abs_url('/assets/img/og-default.jpg'),
        'areaServed'=> count($areas) === 1 ? $areas[0] : $areas,
        'knowsAbout'=> array_values(array_map(fn ($s) => $s['name'], services())),
    ];
}

function website_schema(): array
{
    return [
        '@type'     => 'WebSite',
        '@id'       => abs_url('/#website'),
        'url'       => abs_url('/'),
        'name'      => config('name'),
        'publisher' => ['@id' => abs_url('/#business')],
        'inLanguage'=> 'en-US',
    ];
}

function breadcrumb_schema(array $trail): ?array
{
    if (count($trail) < 2) {
        return null;
    }
    $items = [];
    foreach ($trail as $i => [$label, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'item' => abs_url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function page_schema(array $route, array $trail): array
{
    $graph = [];
    if ($route['path'] === '/') {
        $graph[] = business_schema();
        $graph[] = website_schema();
    }
    if (!empty($route['is_404'])) {
        return [];
    }
    if ($route['template'] === 'contact' || $route['template'] === 'service-area' || $route['template'] === 'about') {
        $graph[] = business_schema();
    }
    if ($route['template'] === 'service') {
        $s = $route['service'];
        $graph[] = [
            '@type'       => 'Service',
            'name'        => $s['name'],
            'serviceType' => $s['name'],
            'description' => $s['description'],
            'url'         => abs_url($s['url']),
            'provider'    => ['@type' => 'RoofingContractor', '@id' => abs_url('/#business'), 'name' => config('name'), 'telephone' => config('phone_tel'), 'url' => abs_url('/')],
            'areaServed'  => ['@type' => 'City', 'name' => config('city') . ', ' . config('state')],
        ];
    }
    if ($route['template'] === 'article') {
        $a = $route['article'];
        $graph[] = [
            '@type'            => 'BlogPosting',
            'headline'         => $a['title'],
            'description'      => $a['description'],
            'image'            => abs_url('/assets/img/' . $a['image'] . '-1600.webp'),
            'datePublished'    => $a['date_iso'],
            'dateModified'     => $a['date_iso'],
            'author'           => ['@type' => 'Organization', 'name' => 'Friendswood Roofers Editorial Team', 'url' => abs_url('/about/')],
            'publisher'        => ['@type' => 'Organization', '@id' => abs_url('/#business'), 'name' => config('name'), 'logo' => ['@type' => 'ImageObject', 'url' => abs_url('/assets/img/logo-mark.png')]],
            'mainEntityOfPage' => abs_url($a['url']),
            'articleSection'   => $a['category'],
            'inLanguage'       => 'en-US',
        ];
    }
    if ($b = breadcrumb_schema($trail)) {
        $graph[] = $b;
    }
    return $graph;
}

function json_ld(array $graph): string
{
    if (!$graph) {
        return '';
    }
    $json = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP);
    return '<script type="application/ld+json">' . $json . '</script>';
}
