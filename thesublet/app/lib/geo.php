<?php defined('APP') || exit;

function states(): array
{
    return [
        'AL' => 'Alabama', 'AK' => 'Alaska', 'AZ' => 'Arizona', 'AR' => 'Arkansas', 'CA' => 'California',
        'CO' => 'Colorado', 'CT' => 'Connecticut', 'DE' => 'Delaware', 'DC' => 'District of Columbia',
        'FL' => 'Florida', 'GA' => 'Georgia', 'HI' => 'Hawaii', 'ID' => 'Idaho', 'IL' => 'Illinois',
        'IN' => 'Indiana', 'IA' => 'Iowa', 'KS' => 'Kansas', 'KY' => 'Kentucky', 'LA' => 'Louisiana',
        'ME' => 'Maine', 'MD' => 'Maryland', 'MA' => 'Massachusetts', 'MI' => 'Michigan', 'MN' => 'Minnesota',
        'MS' => 'Mississippi', 'MO' => 'Missouri', 'MT' => 'Montana', 'NE' => 'Nebraska', 'NV' => 'Nevada',
        'NH' => 'New Hampshire', 'NJ' => 'New Jersey', 'NM' => 'New Mexico', 'NY' => 'New York',
        'NC' => 'North Carolina', 'ND' => 'North Dakota', 'OH' => 'Ohio', 'OK' => 'Oklahoma', 'OR' => 'Oregon',
        'PA' => 'Pennsylvania', 'RI' => 'Rhode Island', 'SC' => 'South Carolina', 'SD' => 'South Dakota',
        'TN' => 'Tennessee', 'TX' => 'Texas', 'UT' => 'Utah', 'VT' => 'Vermont', 'VA' => 'Virginia',
        'WA' => 'Washington', 'WV' => 'West Virginia', 'WI' => 'Wisconsin', 'WY' => 'Wyoming',
    ];
}

function state_name(string $code): string
{
    return states()[strtoupper($code)] ?? strtoupper($code);
}

/** Pre-written city guides, keyed "st/city-slug". */
function city_content(): array
{
    static $all = null;
    if ($all !== null) return $all;
    $all = [];
    foreach (glob(APPDIR . '/content/cities/*.php') ?: [] as $f) {
        $data = require $f;
        if (is_array($data)) $all += $data;
    }
    ksort($all);
    return $all;
}

function city_guide(string $st, string $slug): ?array
{
    return city_content()[strtolower($st) . '/' . $slug] ?? null;
}

/** Cities with at least one active listing: [key => [name, state, count]] */
function cities_with_listings(): array
{
    static $c = null;
    if ($c !== null) return $c;
    $c = [];
    foreach (rows("SELECT state, city_slug, MIN(city) AS city, COUNT(*) AS n FROM listings WHERE status = 'active' GROUP BY state, city_slug") as $r) {
        $c[strtolower($r['state']) . '/' . $r['city_slug']] = ['name' => $r['city'], 'state' => $r['state'], 'n' => (int)$r['n']];
    }
    return $c;
}

/** All cities that deserve a page (guide or listings), optionally for one state. */
function known_cities(?string $st = null): array
{
    $out = [];
    foreach (city_content() as $k => $g) {
        $out[$k] = ['name' => $g['name'], 'state' => $g['state'], 'n' => 0, 'guide' => true, 'type' => $g['type'] ?? 'metro'];
    }
    foreach (cities_with_listings() as $k => $c) {
        if (isset($out[$k])) $out[$k]['n'] = $c['n'];
        else $out[$k] = $c + ['guide' => false, 'type' => 'metro'];
    }
    if ($st) $out = array_filter($out, fn($k) => str_starts_with($k, strtolower($st) . '/'), ARRAY_FILTER_USE_KEY);
    uasort($out, fn($a, $b) => strcmp($a['name'], $b['name']));
    return $out;
}

function city_url(string $st, string $slug): string
{
    return '/sublets/' . strtolower($st) . '/' . $slug . '/';
}

function state_url(string $st): string
{
    return '/sublets/' . strtolower($st) . '/';
}

/** Filtered landing pages under a city. */
function city_filters(): array
{
    return [
        'furnished'      => ['label' => 'Furnished sublets', 'short' => 'Furnished', 'where' => ['furnished' => 1]],
        'private-rooms'  => ['label' => 'Private rooms for rent', 'short' => 'Private rooms', 'where' => ['type' => 'private_room']],
        'entire-apartments' => ['label' => 'Entire apartments', 'short' => 'Entire apartments', 'where' => ['type' => 'entire_apartment']],
        'summer'         => ['label' => 'Summer sublets', 'short' => 'Summer', 'where' => ['summer' => 1]],
        'pet-friendly'   => ['label' => 'Pet-friendly sublets', 'short' => 'Pet-friendly', 'where' => ['pets' => 1]],
        'under-1000'     => ['label' => 'Sublets under $1,000', 'short' => 'Under $1,000', 'where' => ['max' => 1000]],
        'under-1500'     => ['label' => 'Sublets under $1,500', 'short' => 'Under $1,500', 'where' => ['max' => 1500]],
        'under-2000'     => ['label' => 'Sublets under $2,000', 'short' => 'Under $2,000', 'where' => ['max' => 2000]],
    ];
}

function property_types(): array
{
    return [
        'private_room'     => 'Private room',
        'shared_room'      => 'Shared room',
        'entire_apartment' => 'Entire apartment',
        'entire_house'     => 'Entire house',
    ];
}

function amenity_options(): array
{
    return [
        'wifi' => 'Wi-Fi', 'ac' => 'Air conditioning', 'heating' => 'Heating', 'laundry_in_unit' => 'In-unit laundry',
        'laundry_building' => 'Laundry in building', 'kitchen' => 'Full kitchen', 'parking' => 'Parking',
        'workspace' => 'Desk / workspace', 'tv' => 'TV', 'dishwasher' => 'Dishwasher', 'elevator' => 'Elevator',
        'gym' => 'Gym', 'pool' => 'Pool', 'outdoor' => 'Balcony / yard', 'private_bath' => 'Private bathroom',
        'linens' => 'Linens & towels', 'step_free' => 'Step-free entry', 'near_transit' => 'Near transit',
    ];
}

function pet_options(): array
{
    return ['no' => 'No pets', 'cats' => 'Cats OK', 'dogs' => 'Dogs OK', 'yes' => 'Cats & dogs OK', 'ask' => 'Ask host'];
}
