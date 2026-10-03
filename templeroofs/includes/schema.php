<?php
/**
 * JSON-LD structured data builders. Only verified business details are
 * used: name, phone, website and primary city. No street address, hours,
 * ratings or licence data are published because none have been provided.
 */
defined('TR_ROOT') || exit;

function schema_business(): array
{
    $served = [];
    foreach (areas() as $a) {
        $served[] = ['@type' => 'City', 'name' => $a['city'] . ', TX'];
    }
    if (!$served) {
        $served[] = ['@type' => 'City', 'name' => 'Temple, TX'];
    }
    return [
        '@type'       => 'RoofingContractor',
        '@id'         => abs_url('/#business'),
        'name'        => cfg('site_name'),
        'url'         => abs_url('/'),
        'telephone'   => cfg('phone_e164'),
        'image'       => abs_url('/assets/images/og-image.jpg'),
        'logo'        => abs_url('/assets/images/logo-mark-512.png'),
        'description' => 'Temple Roofers provides roof repair, roof replacement, storm and hail damage repair, metal and commercial roofing, and free roof inspections in Temple, Texas and nearby Bell County communities.',
        'address'     => [
            '@type'           => 'PostalAddress',
            'addressLocality' => 'Temple',
            'addressRegion'   => 'TX',
            'addressCountry'  => 'US',
        ],
        'areaServed'  => $served,
        'makesOffer'  => [
            '@type'         => 'Offer',
            'name'          => 'Free Roof Inspection',
            'price'         => '0',
            'priceCurrency' => 'USD',
            'url'           => abs_url('/free-roof-inspection/'),
        ],
    ];
}

function schema_website(): array
{
    return [
        '@type'     => 'WebSite',
        '@id'       => abs_url('/#website'),
        'url'       => abs_url('/'),
        'name'      => cfg('site_name'),
        'publisher' => ['@id' => abs_url('/#business')],
        'inLanguage' => 'en-US',
    ];
}

/** @param array $crumbs list of [label, path] (Home is added automatically). */
function schema_breadcrumbs(array $crumbs): array
{
    $items = [['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => abs_url('/')]];
    foreach ($crumbs as $i => [$label, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 2, 'name' => $label, 'item' => abs_url($path)];
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
        'mainEntity' => array_map(fn ($f) => [
            '@type'          => 'Question',
            'name'           => $f['q'],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']],
        ], $faqs),
    ];
}

function schema_post(array $p): array
{
    $date = $p['date']->format('c');
    return [
        '@type'            => 'BlogPosting',
        '@id'              => abs_url($p['url'] . '#article'),
        'headline'         => $p['title'],
        'description'      => $p['meta_description'],
        'image'            => abs_url('/assets/images/' . $p['image'] . '-1600.webp'),
        'datePublished'    => $date,
        'dateModified'     => $date,
        'author'           => ['@type' => 'Organization', 'name' => cfg('site_name'), 'url' => abs_url('/')],
        'publisher'        => ['@id' => abs_url('/#business')],
        'mainEntityOfPage' => abs_url($p['url']),
        'keywords'         => $p['focus_keyword'] ?? '',
        'articleSection'   => category_name($p['category'] ?? ''),
        'wordCount'        => word_count($p['body']),
        'inLanguage'       => 'en-US',
    ];
}

function schema_service(array $s): array
{
    return [
        '@type'       => 'Service',
        'name'        => $s['name'],
        'serviceType' => $s['name'],
        'description' => $s['meta_description'],
        'url'         => abs_url($s['url']),
        'provider'    => ['@id' => abs_url('/#business')],
        'areaServed'  => ['@type' => 'City', 'name' => 'Temple, TX'],
    ];
}

function schema_graph(array $nodes): string
{
    $nodes = array_values(array_filter($nodes));
    $json = json_encode(
        ['@context' => 'https://schema.org', '@graph' => $nodes],
        JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP
    );
    return '<script type="application/ld+json">' . $json . '</script>';
}
