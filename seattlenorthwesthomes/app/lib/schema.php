<?php defined('SNW') || (http_response_code(404) && exit);
/* JSON-LD builders. Each returns a node for the page's @graph. */

function schema_org(): array
{
    $n = [
        '@type' => 'RealEstateAgent',
        '@id' => abs_url('/#organization'),
        'name' => cfg('name'),
        'url' => abs_url('/'),
        'logo' => abs_url('/assets/img/brand/logo-square.webp'),
        'image' => abs_url('/assets/img/brand/og-default.jpg'),
        'email' => cfg('email'),
        'description' => 'Seattle real estate team helping buyers and sellers across Seattle neighborhoods and the greater Puget Sound area.',
        'address' => ['@type' => 'PostalAddress', 'addressLocality' => cfg('city'), 'addressRegion' => cfg('region'), 'addressCountry' => 'US'],
        'geo' => ['@type' => 'GeoCoordinates', 'latitude' => cfg('geo')['lat'], 'longitude' => cfg('geo')['lng']],
        'areaServed' => array_merge(
            [['@type' => 'City', 'name' => 'Seattle']],
            array_map(fn($h) => ['@type' => 'Place', 'name' => $h['name'] . ', Seattle, WA'], array_values(neighborhoods()))
        ),
    ];
    if (cfg('phone')) $n['telephone'] = cfg('phone');
    if (cfg('social')) $n['sameAs'] = cfg('social');
    return $n;
}

function schema_website(): array
{
    return [
        '@type' => 'WebSite',
        '@id' => abs_url('/#website'),
        'url' => abs_url('/'),
        'name' => cfg('name'),
        'publisher' => ['@id' => abs_url('/#organization')],
        'potentialAction' => [
            '@type' => 'SearchAction',
            'target' => ['@type' => 'EntryPoint', 'urlTemplate' => abs_url('/homes-for-sale/?q={search_term_string}')],
            'query-input' => 'required name=search_term_string',
        ],
    ];
}

/** $crumbs = [[name, path], ...] (Home is added automatically). */
function schema_breadcrumbs(array $crumbs): array
{
    $items = [['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => abs_url('/')]];
    foreach ($crumbs as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 2, 'name' => $name, 'item' => abs_url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function schema_listing(array $l): array
{
    $hood = neighborhoods()[$l['neighborhood']];
    $url = abs_url('/homes-for-sale/' . $l['slug'] . '/');
    $typeMap = ['Single Family' => 'SingleFamilyResidence', 'Condo' => 'Apartment', 'Townhome' => 'House'];
    $avail = ['For Sale' => 'https://schema.org/InStock', 'Pending' => 'https://schema.org/LimitedAvailability', 'Sold' => 'https://schema.org/SoldOut'];
    return [
        '@type' => 'RealEstateListing',
        '@id' => $url . '#listing',
        'url' => $url,
        'name' => $l['title'],
        'description' => $l['summary'],
        'datePosted' => $l['listed'],
        'image' => array_map(fn($i) => abs_url(photo($i)), $l['images']),
        'offers' => [
            '@type' => 'Offer',
            'price' => $l['price'],
            'priceCurrency' => 'USD',
            'availability' => $avail[$l['status']] ?? 'https://schema.org/InStock',
            'seller' => ['@id' => abs_url('/#organization')],
        ],
        'mainEntity' => [
            '@type' => $typeMap[$l['type']] ?? 'House',
            'name' => $l['title'],
            'numberOfRooms' => $l['beds'],
            'numberOfBedrooms' => $l['beds'],
            'numberOfBathroomsTotal' => $l['baths'],
            'floorSize' => ['@type' => 'QuantitativeValue', 'value' => $l['sqft'], 'unitCode' => 'FTK'],
            'yearBuilt' => $l['year'],
            'address' => [
                '@type' => 'PostalAddress',
                'addressLocality' => 'Seattle',
                'addressRegion' => 'WA',
                'postalCode' => $l['zip'],
                'addressCountry' => 'US',
                'streetAddress' => $hood['name'],
            ],
        ],
    ];
}

function schema_post(array $p): array
{
    $url = abs_url('/blog/' . $p['slug'] . '/');
    return [
        '@type' => 'BlogPosting',
        '@id' => $url . '#article',
        'mainEntityOfPage' => $url,
        'headline' => $p['title'],
        'description' => $p['description'],
        'image' => abs_url(post_image($p)),
        'datePublished' => $p['date'],
        'dateModified' => $p['modified'],
        'wordCount' => str_word_count(strip_tags($p['body'])),
        'articleSection' => categories()[$p['category']]['name'] ?? '',
        'author' => ['@type' => 'Person', 'name' => cfg('agent'), 'url' => abs_url('/about-seattle-northwest-homes/')],
        'publisher' => ['@id' => abs_url('/#organization')],
        'isPartOf' => ['@id' => abs_url('/#website')],
    ];
}

function schema_faq(array $faq): ?array
{
    if (!$faq) return null;
    return [
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type' => 'Question',
            'name' => $f['q'],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']],
        ], $faq),
    ];
}

/** ItemList of URLs (listing index, blog index, neighborhoods). */
function schema_item_list(array $urls): array
{
    $items = [];
    foreach (array_values($urls) as $i => $u) $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url($u)];
    return ['@type' => 'ItemList', 'itemListElement' => $items];
}

function schema_json(array $nodes): string
{
    $graph = array_values(array_filter(array_merge([schema_org(), schema_website()], $nodes)));
    return json_encode(['@context' => 'https://schema.org', '@graph' => $graph],
        JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
}
