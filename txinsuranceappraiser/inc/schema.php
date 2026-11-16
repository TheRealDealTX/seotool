<?php
declare(strict_types=1);

/** Shared JSON-LD graph nodes: business, person, website. */
function schema_base(): array
{
    $o = SITE['origin'];
    $areas = array_map(fn($h) => ['@type' => 'City', 'name' => $h . ', TX'], SITE['hubs']);
    $areas[] = ['@type' => 'State', 'name' => 'Texas'];
    return [
        [
            '@type' => ['ProfessionalService', 'LocalBusiness'],
            '@id' => $o . '/#business',
            'name' => SITE['name'],
            'legalName' => SITE['legal'],
            'url' => $o . '/',
            'logo' => $o . SITE['logo'],
            'image' => $o . SITE['og_default'],
            'telephone' => SITE['phone_href'],
            'email' => SITE['email'],
            'priceRange' => '$$',
            'description' => 'TX Insurance Appraiser provides policyholder-side insurance appraisal, umpire, Matterport, Xactimate and Symbility estimating services for disputed property damage claims across Texas.',
            'address' => ['@type' => 'PostalAddress', 'addressRegion' => 'TX', 'addressCountry' => 'US'],
            'areaServed' => $areas,
            'openingHours' => SITE['hours_schema'],
            'founder' => ['@id' => $o . '/#joseph-dittman'],
            'employee' => ['@id' => $o . '/#joseph-dittman'],
            'knowsAbout' => ['Insurance appraisal', 'Appraisal clause', 'Insurance umpire', 'Hail damage claims', 'Wind damage claims', 'Hurricane damage claims', 'Fire damage claims', 'Water damage claims', 'Xactimate', 'Symbility', 'Matterport'],
            'contactPoint' => [
                '@type' => 'ContactPoint', 'telephone' => SITE['phone_href'], 'email' => SITE['email'],
                'contactType' => 'customer service', 'areaServed' => 'US-TX', 'availableLanguage' => 'English',
            ],
        ],
        [
            '@type' => 'Person',
            '@id' => $o . '/#joseph-dittman',
            'name' => SITE['appraiser']['name'],
            'jobTitle' => SITE['appraiser']['role'],
            'worksFor' => ['@id' => $o . '/#business'],
            'url' => $o . '/about-us/',
            'knowsAbout' => ['Property insurance claims', 'Insurance appraisal', 'Xactimate estimating', 'Hail and wind damage inspection'],
            'hasCredential' => [
                '@type' => 'EducationalOccupationalCredential',
                'credentialCategory' => 'license',
                'name' => 'Texas Public Adjuster License #' . SITE['appraiser']['license'] . ' (' . SITE['appraiser']['company'] . ')',
                'recognizedBy' => ['@type' => 'GovernmentOrganization', 'name' => 'Texas Department of Insurance', 'url' => 'https://www.tdi.texas.gov/'],
            ],
        ],
        [
            '@type' => 'WebSite',
            '@id' => $o . '/#website',
            'url' => $o . '/',
            'name' => SITE['name'],
            'publisher' => ['@id' => $o . '/#business'],
            'inLanguage' => 'en-US',
        ],
    ];
}

function schema_breadcrumbs(array $crumbs): array
{
    $items = [];
    foreach ($crumbs as $i => [$name, $url]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => abs_url($url)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function schema_faq(array $faqs): array
{
    return [
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type' => 'Question', 'name' => $f['q'],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f['a'])],
        ], $faqs),
    ];
}

function schema_service(string $name, string $desc, string $path, array $area = null): array
{
    return [
        '@type' => 'Service',
        'name' => $name,
        'serviceType' => $name,
        'description' => $desc,
        'url' => abs_url($path),
        'provider' => ['@id' => SITE['origin'] . '/#business'],
        'areaServed' => $area ?? ['@type' => 'State', 'name' => 'Texas'],
    ];
}

function schema_webpage(string $type, string $title, string $desc, string $path): array
{
    return [
        '@type' => $type,
        '@id' => abs_url($path) . '#webpage',
        'url' => abs_url($path),
        'name' => $title,
        'description' => $desc,
        'isPartOf' => ['@id' => SITE['origin'] . '/#website'],
        'about' => ['@id' => SITE['origin'] . '/#business'],
        'inLanguage' => 'en-US',
    ];
}

function render_schema(array $nodes): string
{
    $graph = ['@context' => 'https://schema.org', '@graph' => array_values(array_merge(schema_base(), $nodes))];
    return '<script type="application/ld+json">' . json_encode($graph, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . '</script>';
}
