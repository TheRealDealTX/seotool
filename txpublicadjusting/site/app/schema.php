<?php
/** JSON-LD builders. Every page emits a @graph with the org, person and website nodes. */

function schema_org(): array
{
    $addr = [
        '@type'           => 'PostalAddress',
        'addressLocality' => BIZ['city'],
        'addressRegion'   => BIZ['region'],
        'postalCode'      => BIZ['postal'],
        'addressCountry'  => 'US',
    ];
    if (BIZ['show_street']) {
        $addr['streetAddress'] = BIZ['street'];
    }
    return [
        '@type'      => 'ProfessionalService',
        '@id'        => CANONICAL_ORIGIN . '/#org',
        'name'       => BIZ['name'],
        'legalName'  => BIZ['legal_name'],
        'url'        => CANONICAL_ORIGIN . '/',
        'logo'       => CANONICAL_ORIGIN . '/assets/img/TX-Public-Adjusting-Logo.webp',
        'image'      => CANONICAL_ORIGIN . '/assets/img/og-default.jpg',
        'telephone'  => BIZ['phone_e164'],
        'address'    => $addr,
        'geo'        => ['@type' => 'GeoCoordinates', 'latitude' => BIZ['lat'], 'longitude' => BIZ['lng']],
        'areaServed' => ['@type' => 'State', 'name' => 'Texas'],
        'priceRange' => 'Contingency fee, no upfront cost',
        'description'=> 'Licensed Texas public insurance adjusters representing homeowners and businesses on roof, hail, water, fire, hurricane and commercial property claims.',
        'employee'   => ['@id' => CANONICAL_ORIGIN . '/about-us/#joseph-dittman'],
        'knowsAbout' => ['Property insurance claims', 'Hail damage claims', 'Water damage claims', 'Fire damage claims', 'Windstorm claims', 'Commercial property claims', 'Insurance appraisal'],
    ];
}

function schema_person(): array
{
    return [
        '@type'    => 'Person',
        '@id'      => CANONICAL_ORIGIN . '/about-us/#joseph-dittman',
        'name'     => BIZ['adjuster'],
        'jobTitle' => 'Licensed Public Insurance Adjuster',
        'url'      => CANONICAL_ORIGIN . '/about-us/',
        'image'    => CANONICAL_ORIGIN . '/assets/img/Joseph-Dittman-TX-Public-Adjusting.webp',
        'worksFor' => ['@id' => CANONICAL_ORIGIN . '/#org'],
        'hasCredential' => [
            '@type'              => 'EducationalOccupationalCredential',
            'credentialCategory' => 'license',
            'name'               => 'Texas Public Insurance Adjuster License',
            'identifier'         => BIZ['license'],
            'recognizedBy'       => ['@type' => 'GovernmentOrganization', 'name' => 'Texas Department of Insurance', 'url' => 'https://www.tdi.texas.gov/'],
        ],
        'knowsAbout' => ['Texas Insurance Code', 'Xactimate', 'Property claim documentation', 'Hail and wind damage assessment'],
    ];
}

function schema_website(): array
{
    return [
        '@type'     => 'WebSite',
        '@id'       => CANONICAL_ORIGIN . '/#website',
        'url'       => CANONICAL_ORIGIN . '/',
        'name'      => BIZ['name'],
        'publisher' => ['@id' => CANONICAL_ORIGIN . '/#org'],
        'inLanguage'=> 'en-US',
    ];
}

function schema_breadcrumbs(array $crumbs): array
{
    $items = [];
    foreach ($crumbs as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => canonical($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function schema_faq(array $faqs): ?array
{
    if (!$faqs) {
        return null;
    }
    return [
        '@type'      => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type'          => 'Question',
            'name'           => strip_tags($f['q']),
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f['a'], '<a>')],
        ], $faqs),
    ];
}

function schema_article(array $p, string $path): array
{
    $img = '/assets/img/blog/' . $p['_slug'] . '.webp';
    return [
        '@type'            => 'BlogPosting',
        'headline'         => $p['h1'] ?? $p['title'],
        'description'      => $p['description'] ?? '',
        'datePublished'    => $p['published'] ?? $p['updated'] ?? null,
        'dateModified'     => $p['updated'] ?? $p['published'] ?? null,
        'author'           => ['@id' => CANONICAL_ORIGIN . '/about-us/#joseph-dittman'],
        'publisher'        => ['@id' => CANONICAL_ORIGIN . '/#org'],
        'mainEntityOfPage' => canonical($path),
        'image'            => is_file(SITE_ROOT . $img) ? canonical($img) : CANONICAL_ORIGIN . '/assets/img/og-default.jpg',
        'articleSection'   => $p['category'] ?? null,
        'wordCount'        => word_count($p['body'] ?? ''),
    ];
}

function schema_service(array $p, string $path): array
{
    return [
        '@type'       => 'Service',
        'name'        => $p['h1'] ?? $p['title'],
        'description' => $p['description'] ?? '',
        'serviceType' => 'Public insurance adjusting',
        'provider'    => ['@id' => CANONICAL_ORIGIN . '/#org'],
        'areaServed'  => isset($p['city'])
            ? ['@type' => 'City', 'name' => $p['city'] . ', Texas']
            : ['@type' => 'State', 'name' => 'Texas'],
        'url'         => canonical($path),
    ];
}

function schema_graph(array $nodes): string
{
    $graph = array_values(array_filter(array_merge([schema_org(), schema_person(), schema_website()], $nodes)));
    $json = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
    return '<script type="application/ld+json">' . $json . '</script>';
}
