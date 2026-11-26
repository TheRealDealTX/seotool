<?php defined('APP') || exit;

function schema_org(): array
{
    return [
        '@context' => 'https://schema.org',
        '@type' => 'Organization',
        '@id' => base_url('/#org'),
        'name' => 'The Sublet',
        'alternateName' => 'thesublet',
        'url' => base_url('/'),
        'logo' => base_url('/assets/img/logo-512.png'),
        'email' => 'info@thesublet.com',
    ];
}

function schema_website(): array
{
    return [
        '@context' => 'https://schema.org',
        '@type' => 'WebSite',
        '@id' => base_url('/#website'),
        'name' => 'The Sublet',
        'alternateName' => 'thesublet.com',
        'url' => base_url('/'),
        'publisher' => ['@id' => base_url('/#org')],
        'potentialAction' => [
            '@type' => 'SearchAction',
            'target' => ['@type' => 'EntryPoint', 'urlTemplate' => base_url('/sublets/?q={search_term_string}')],
            'query-input' => 'required name=search_term_string',
        ],
    ];
}

function schema_breadcrumbs(array $crumbs): array
{
    $items = [];
    foreach (array_values($crumbs) as $i => [$label, $url]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'item' => base_url($url)];
    }
    return ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function schema_faq(array $faqs): ?array
{
    if (!$faqs) return null;
    return [
        '@context' => 'https://schema.org',
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type' => 'Question',
            'name' => html_entity_decode(strip_tags($f['q']), ENT_QUOTES, 'UTF-8'),
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => html_entity_decode(strip_tags($f['a']), ENT_QUOTES, 'UTF-8')],
        ], $faqs),
    ];
}

function schema_itemlist(array $cards, string $name): ?array
{
    if (!$cards) return null;
    return [
        '@context' => 'https://schema.org',
        '@type' => 'ItemList',
        'name' => $name,
        'numberOfItems' => count($cards),
        'itemListElement' => array_map(fn($c, $i) => [
            '@type' => 'ListItem', 'position' => $i + 1, 'url' => base_url($c['url']), 'name' => $c['title'],
        ], $cards, array_keys($cards)),
    ];
}

function schema_accommodation(array $l, array $photos): array
{
    $typeMap = ['private_room' => 'Room', 'shared_room' => 'Room', 'entire_apartment' => 'Apartment', 'entire_house' => 'House'];
    $acc = [
        '@type' => $typeMap[$l['property_type']] ?? 'Accommodation',
        'name' => $l['title'],
        'description' => excerpt($l['description'], 300),
        'address' => array_filter([
            '@type' => 'PostalAddress',
            'addressLocality' => $l['city'],
            'addressRegion' => $l['state'],
            'postalCode' => $l['zip'] ?: null,
            'addressCountry' => 'US',
        ]),
        'petsAllowed' => $l['pets'] !== 'no',
        'amenityFeature' => array_map(fn($a) => ['@type' => 'LocationFeatureSpecification', 'name' => amenity_options()[$a] ?? $a, 'value' => true],
            array_filter(explode(',', (string)$l['amenities']))),
    ];
    if (is_numeric($l['beds'])) $acc['numberOfBedrooms'] = (int)$l['beds'];
    if (is_numeric($l['baths'])) $acc['numberOfBathroomsTotal'] = (float)$l['baths'];
    if ($l['lat'] !== null) $acc['geo'] = ['@type' => 'GeoCoordinates', 'latitude' => (float)$l['lat'], 'longitude' => (float)$l['lng']];
    if ($photos) $acc['image'] = array_map(fn($p) => base_url(photo_src((int)$p['id'])), array_slice($photos, 0, 5));
    $offer = [
        '@context' => 'https://schema.org',
        '@type' => 'Offer',
        'url' => base_url(listing_url($l)),
        'name' => $l['title'],
        'price' => (int)$l['rent'],
        'priceCurrency' => 'USD',
        'priceSpecification' => [
            '@type' => 'UnitPriceSpecification', 'price' => (int)$l['rent'], 'priceCurrency' => 'USD',
            'unitCode' => 'MON', 'unitText' => 'month',
        ],
        'availability' => $l['status'] === 'active' ? 'https://schema.org/InStock' : 'https://schema.org/SoldOut',
        'businessFunction' => 'http://purl.org/goodrelations/v1#LeaseOut',
        'itemOffered' => $acc,
    ];
    if ($l['available_from']) $offer['availabilityStarts'] = $l['available_from'];
    if ($l['available_to']) $offer['availabilityEnds'] = $l['available_to'];
    return $offer;
}

function schema_article(array $post): array
{
    return [
        '@context' => 'https://schema.org',
        '@type' => 'BlogPosting',
        'headline' => $post['title'],
        'description' => $post['description'],
        'datePublished' => $post['date'],
        'dateModified' => $post['updated'] ?? $post['date'],
        'mainEntityOfPage' => base_url('/blog/' . $post['slug'] . '/'),
        'author' => ['@type' => 'Organization', 'name' => 'The Sublet', 'url' => base_url('/')],
        'publisher' => ['@id' => base_url('/#org')],
        'image' => base_url(photo_url('blog.' . $post['slug'], '/assets/img/og-default.png')),
    ];
}

function schema_business(array $l): array
{
    $type = ['extended_stay' => 'Hotel', 'student_housing' => 'ApartmentComplex', 'furnished_community' => 'ApartmentComplex'][$l['property_type']] ?? 'LodgingBusiness';
    $s = [
        '@context' => 'https://schema.org',
        '@type' => $type,
        'name' => $l['title'],
        'url' => base_url(listing_url($l)),
        'address' => array_filter([
            '@type' => 'PostalAddress',
            'streetAddress' => $l['address_line'] ?: null,
            'addressLocality' => $l['address_city'] ?: $l['city'],
            'addressRegion' => $l['state'],
            'postalCode' => $l['zip'] ?: null,
            'addressCountry' => 'US',
        ]),
    ];
    if ($l['phone_public']) $s['telephone'] = $l['phone_public'];
    if ($l['website']) $s['sameAs'] = preg_replace('#[?].*$#', '', $l['website']);
    if ($l['lat'] !== null) $s['geo'] = ['@type' => 'GeoCoordinates', 'latitude' => (float)$l['lat'], 'longitude' => (float)$l['lng']];
    return $s;
}
