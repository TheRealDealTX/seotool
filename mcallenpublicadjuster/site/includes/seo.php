<?php
/**
 * SEO: titles, meta, Open Graph, and JSON-LD structured data.
 */

declare(strict_types=1);

function seo_title(array $page): string
{
    if (!empty($page['seo_title'])) {
        return $page['seo_title'];
    }
    $t = $page['title'] ?? cfg('site_name');
    return $page['path'] === '/' ? $t : $t . ' | ' . cfg('site_name');
}

function og_image(array $page): string
{
    $img = $page['og_image'] ?? $page['image'] ?? '/wp-content/uploads/2026/02/McAllen-Public-Adjuster-Site-Image.webp';
    return url($img);
}

function breadcrumbs_for(array $page): array
{
    if (($page['path'] ?? '/') === '/') {
        return [];
    }
    $crumbs = [['Home', '/']];
    $type = $page['_type'] ?? 'page';
    if (!empty($page['breadcrumb_parent'])) {
        $crumbs[] = $page['breadcrumb_parent'];
    } elseif ($type === 'post') {
        $crumbs[] = ['Blog', '/blog/'];
    } elseif ($type === 'service') {
        $crumbs[] = ['Services', '/services/'];
    }
    $crumbs[] = [$page['crumb'] ?? $page['title'], $page['path']];
    return $crumbs;
}

function org_schema(): array
{
    $site = rtrim(cfg('site_url'), '/');
    $areas = ['McAllen', 'Mission', 'Edinburg', 'Pharr', 'San Juan', 'Alamo', 'Hidalgo', 'Weslaco', 'Donna', 'Mercedes'];
    return [
        '@type'       => ['ProfessionalService', 'LocalBusiness'],
        '@id'         => $site . '/#business',
        'name'        => cfg('site_name'),
        'legalName'   => cfg('company'),
        'url'         => $site . '/',
        'telephone'   => cfg('phone_e164'),
        'email'       => cfg('public_email'),
        'image'       => $site . '/wp-content/uploads/2026/02/McAllen-Public-Adjuster-Site-Image.webp',
        'logo'        => $site . '/assets/img/logo-mark.png',
        'description' => 'Licensed Texas public adjusting services for McAllen and Hidalgo County homeowners and business owners with hail, wind, storm, fire, and water damage insurance claims.',
        'priceRange'  => 'Free claim review',
        'areaServed'  => array_merge(
            array_map(fn($c) => ['@type' => 'City', 'name' => $c . ', TX'], $areas),
            [['@type' => 'AdministrativeArea', 'name' => 'Hidalgo County, TX']]
        ),
        'founder'     => ['@id' => $site . '/author/joseph-dittman/#person'],
        'hasCredential' => [
            '@type' => 'EducationalOccupationalCredential',
            'credentialCategory' => 'license',
            'name' => 'Texas Public Adjuster License #' . cfg('license'),
            'recognizedBy' => ['@type' => 'GovernmentOrganization', 'name' => 'Texas Department of Insurance'],
        ],
        'knowsAbout'  => ['Property insurance claims', 'Hail damage claims', 'Wind damage claims', 'Fire damage claims', 'Water damage claims', 'Insurance appraisal'],
    ];
}

function person_schema(): array
{
    $site = rtrim(cfg('site_url'), '/');
    return [
        '@type'    => 'Person',
        '@id'      => $site . '/author/joseph-dittman/#person',
        'name'     => cfg('author_name'),
        'jobTitle' => cfg('author_title'),
        'url'      => $site . '/author/joseph-dittman/',
        'image'    => $site . '/assets/img/joseph-dittman.webp',
        'worksFor' => ['@id' => $site . '/#business'],
        'knowsAbout' => ['Public adjusting', 'Insurance appraisal', 'Insurance umpire services', 'Hail and wind claims', 'Fire and water claims', 'Commercial property claims'],
        'sameAs'   => ['https://txpublicadjusting.com/', 'https://promptumpire.com/'],
    ];
}

function json_ld(array $page): string
{
    $site = rtrim(cfg('site_url'), '/');
    $canonical = url($page['path']);
    $graph = [];

    $graph[] = [
        '@type' => 'WebSite',
        '@id'   => $site . '/#website',
        'url'   => $site . '/',
        'name'  => cfg('site_name'),
        'publisher' => ['@id' => $site . '/#business'],
        'inLanguage' => 'en-US',
    ];
    $graph[] = org_schema();

    $type = $page['_type'] ?? 'page';
    $webpage = [
        '@type' => ($page['schema_type'] ?? 'WebPage'),
        '@id'   => $canonical . '#webpage',
        'url'   => $canonical,
        'name'  => seo_title($page),
        'description' => $page['description'] ?? '',
        'isPartOf' => ['@id' => $site . '/#website'],
        'inLanguage' => 'en-US',
    ];
    if (!empty($page['image'])) {
        $webpage['primaryImageOfPage'] = ['@type' => 'ImageObject', 'url' => url($page['image'])];
    }
    $crumbs = breadcrumbs_for($page);
    if ($crumbs) {
        $webpage['breadcrumb'] = ['@id' => $canonical . '#breadcrumb'];
        $items = [];
        foreach ($crumbs as $i => [$name, $path]) {
            $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => url($path)];
        }
        $graph[] = ['@type' => 'BreadcrumbList', '@id' => $canonical . '#breadcrumb', 'itemListElement' => $items];
    }
    if (!empty($page['person_schema'])) {
        $p = person_schema();
        $p['description'] = $page['description'] ?? '';
        $graph[] = $p;
        $webpage['mainEntity'] = ['@id' => $site . '/author/joseph-dittman/#person'];
    }
    $graph[] = $webpage;

    if ($type === 'post') {
        $graph[] = [
            '@type' => 'BlogPosting',
            '@id'   => $canonical . '#article',
            'headline' => $page['title'],
            'description' => $page['description'] ?? '',
            'image' => !empty($page['image']) ? [url($page['image'])] : [],
            'datePublished' => iso_date($page['date'] ?? null),
            'dateModified'  => iso_date($page['updated'] ?? $page['date'] ?? null),
            'author'    => ['@id' => $site . '/author/joseph-dittman/#person'],
            'publisher' => ['@id' => $site . '/#business'],
            'mainEntityOfPage' => ['@id' => $canonical . '#webpage'],
            'articleSection' => $page['category'] ?? 'Property Insurance Claims',
            'wordCount' => str_word_count(strip_tags($page['body'] ?? '')),
            'inLanguage' => 'en-US',
        ];
        $graph[] = person_schema();
    }
    if ($type === 'service') {
        $graph[] = [
            '@type' => 'Service',
            '@id'   => $canonical . '#service',
            'name'  => $page['service_name'] ?? $page['title'],
            'serviceType' => $page['service_name'] ?? $page['title'],
            'description' => $page['description'] ?? '',
            'provider' => ['@id' => $site . '/#business'],
            'areaServed' => ['@type' => 'AdministrativeArea', 'name' => 'Hidalgo County, TX'],
            'url' => $canonical,
        ];
    }
    if (!empty($page['faqs'])) {
        $qa = [];
        foreach ($page['faqs'] as $f) {
            $qa[] = [
                '@type' => 'Question',
                'name'  => $f['q'],
                'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(strip_tags($f['a'], '<a><strong><em><br>'))],
            ];
        }
        $graph[] = ['@type' => 'FAQPage', '@id' => $canonical . '#faq', 'mainEntity' => $qa];
    }
    if (!empty($page['extra_schema']) && is_array($page['extra_schema'])) {
        foreach ($page['extra_schema'] as $s) {
            $graph[] = $s;
        }
    }

    $json = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    // Never allow "</script>" inside the JSON block.
    $json = str_replace('</', '<\/', $json);
    return '<script type="application/ld+json">' . $json . '</script>';
}
