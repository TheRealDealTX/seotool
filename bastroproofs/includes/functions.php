<?php
/** Escaping, URLs, icons and JSON-LD builders. */

function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function abs_url(string $path): string
{
    return SITE['origin'] . $path;
}

function img(string $file): string
{
    return '/assets/img/' . $file;
}

/** Current request path, used to mark the active nav item. */
function current_path(): string
{
    $p = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
    return $p === false ? '/' : $p;
}

/** Inline stroke icons (24px grid, currentColor). */
function icon(string $name, string $class = 'icon'): string
{
    static $paths = [
        'phone'    => '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2z"/>',
        'mail'     => '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
        'pin'      => '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
        'clock'    => '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        'check'    => '<path d="M20 6 9 17l-5-5"/>',
        'arrow'    => '<path d="M5 12h14M13 5l7 7-7 7"/>',
        'chevron'  => '<path d="m6 9 6 6 6-6"/>',
        'home'     => '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
        'hammer'   => '<path d="m15 12-8.5 8.5a2.1 2.1 0 0 1-3-3L12 9"/><path d="M17.6 15 22 10.6l-4.4-4.4-2-2a4 4 0 0 0-5.7 0L9 5l7 7z"/>',
        'refresh'  => '<path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M8 16H3v5"/>',
        'layers'   => '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
        'shield'   => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
        'search'   => '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        'storm'    => '<path d="M19 16.9A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><path d="m13 11-4 6h6l-4 6"/>',
        'hail'     => '<path d="M20 16.6A5 5 0 0 0 18 7h-1.3A8 8 0 1 0 4 15.3"/><circle cx="8" cy="19" r="1"/><circle cx="12" cy="21" r="1"/><circle cx="16" cy="19" r="1"/><circle cx="12" cy="16" r="1"/>',
        'siren'    => '<path d="M7 18v-6a5 5 0 0 1 10 0v6"/><path d="M5 21a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v1H5z"/><path d="M21 12h1M18.5 4.5 18 5M2 12h1M12 2v1M4.9 4.9l.7.7"/>',
        'building' => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
        'sun'      => '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
        'wind'     => '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>',
        'drop'     => '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5S12.5 5.5 12 3c-.5 2.5-2 4.9-4 6.5S5 13 5 15a7 7 0 0 0 7 7z"/>',
        'tree'     => '<path d="m17 14 3 3.3a1 1 0 0 1-.7 1.7H4.7a1 1 0 0 1-.7-1.7L7 14h-.3a1 1 0 0 1-.7-1.7L9 9h-.2A1 1 0 0 1 8 7.3L12 3l4 4.3a1 1 0 0 1-.8 1.7H15l3 3.3a1 1 0 0 1-.7 1.7z"/><path d="M12 22v-3"/>',
        'flame'    => '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.3 1.4 1.5 2.8 3.5 2.8z"/>',
        'calc'     => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M16 14v4M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01"/>',
        'ruler'    => '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0z"/><path d="m14.5 12.5 2-2M11.5 9.5l2-2M8.5 6.5l2-2M17.5 15.5l2-2"/>',
        'list'     => '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
        'scale'    => '<path d="m16 16 3-8 3 8c-.9.7-1.9 1-3 1s-2.1-.3-3-1zM2 16l3-8 3 8c-.9.7-1.9 1-3 1s-2.1-.3-3-1z"/><path d="M7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
        'help'     => '<circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3M12 17h.01"/>',
        'star'     => '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
        'menu'     => '<path d="M4 6h16M4 12h16M4 18h16"/>',
        'x'        => '<path d="M18 6 6 18M6 6l12 12"/>',
        'warehouse'=> '<path d="M22 8.4V20a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8.4a2 2 0 0 1 1.3-1.9l8-3.2a2 2 0 0 1 1.5 0l8 3.2A2 2 0 0 1 22 8.4z"/><path d="M6 18h12M6 14h12M6 10h12"/>',
    ];
    $inner = $paths[$name] ?? $paths['check'];
    return '<svg class="' . e($class) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $inner . '</svg>';
}

/* ---------------------------------------------------------------- JSON-LD */

function business_schema(): array
{
    global $AREAS;
    $areas = [['@type' => 'City', 'name' => 'Bastrop, TX']];
    foreach ($AREAS as $a) {
        $areas[] = ['@type' => 'City', 'name' => $a['name'] . ', TX'];
    }
    return [
        '@type'       => ['RoofingContractor', 'LocalBusiness'],
        '@id'         => abs_url('/#business'),
        'name'        => SITE['name'],
        'url'         => abs_url('/'),
        'logo'        => abs_url(img('Bastrop-Roofing-Logo.webp')),
        'image'       => abs_url(img('A-Stronger-Roof-Starts-With-a-Clear-Plan.webp')),
        'telephone'   => SITE['phone_display'],
        'email'       => SITE['email'],
        'priceRange'  => '$$',
        'description' => 'Bastrop Roofing is a local Bastrop, TX roofer providing roof repair, roof replacement, metal roofing, shingle roofing, inspections and storm damage repair across Bastrop County.',
        'address'     => [
            '@type'           => 'PostalAddress',
            'addressLocality' => SITE['city'],
            'addressRegion'   => SITE['state'],
            'postalCode'      => SITE['zip'],
            'addressCountry'  => 'US',
        ],
        'geo' => [
            '@type'     => 'GeoCoordinates',
            'latitude'  => SITE['latitude'],
            'longitude' => SITE['longitude'],
        ],
        'areaServed' => $areas,
        'openingHoursSpecification' => [[
            '@type'     => 'OpeningHoursSpecification',
            'dayOfWeek' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'opens'     => '07:00',
            'closes'    => '19:00',
        ]],
        'knowsAbout' => ['Roof repair', 'Roof replacement', 'Metal roofing', 'Asphalt shingle roofing', 'Storm damage roofing', 'Hail damage roof repair', 'Commercial roofing'],
    ];
}

function website_schema(): array
{
    return [
        '@type'     => 'WebSite',
        '@id'       => abs_url('/#website'),
        'url'       => abs_url('/'),
        'name'      => SITE['name'],
        'publisher' => ['@id' => abs_url('/#business')],
    ];
}

function breadcrumb_schema(array $crumbs): array
{
    $items = [];
    foreach ($crumbs as $i => [$label, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'item' => abs_url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function faq_schema(array $faqs): array
{
    return [
        '@type'      => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type'          => 'Question',
            'name'           => $f['q'],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f['a'])],
        ], $faqs),
    ];
}

function service_schema(string $name, string $desc, string $path, string $area = 'Bastrop, TX'): array
{
    return [
        '@type'       => 'Service',
        'name'        => $name,
        'serviceType' => $name,
        'description' => $desc,
        'url'         => abs_url($path),
        'provider'    => ['@id' => abs_url('/#business')],
        'areaServed'  => ['@type' => 'City', 'name' => $area],
    ];
}

function json_ld(array $nodes): string
{
    $graph = ['@context' => 'https://schema.org', '@graph' => array_values($nodes)];
    return '<script type="application/ld+json">' . json_encode($graph, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . '</script>';
}

function fmt_date(string $iso): string
{
    return date('F j, Y', strtotime($iso));
}
