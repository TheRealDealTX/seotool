<?php defined('SNW') || (http_response_code(404) && exit);
/* /homes-for-sale/ — server-side filtering via GET so every result set is a crawlable, shareable URL. */
$f = [
    'q'      => trim((string) ($_GET['q'] ?? '')),
    'hood'   => (string) ($_GET['hood'] ?? ''),
    'type'   => (string) ($_GET['type'] ?? ''),
    'min'    => (int) ($_GET['min'] ?? 0),
    'max'    => (int) ($_GET['max'] ?? 0),
    'beds'   => (int) ($_GET['beds'] ?? 0),
    'status' => (string) ($_GET['status'] ?? ''),
    'sort'   => (string) ($_GET['sort'] ?? 'newest'),
];
$hoods = neighborhoods();
$results = array_filter(listings(), function ($l) use ($f, $hoods) {
    if ($f['hood'] && $l['neighborhood'] !== $f['hood']) return false;
    if ($f['type'] && $l['type'] !== $f['type']) return false;
    if ($f['min'] && $l['price'] < $f['min']) return false;
    if ($f['max'] && $l['price'] > $f['max']) return false;
    if ($f['beds'] && $l['beds'] < $f['beds']) return false;
    if ($f['status'] === 'active' && $l['status'] === 'Sold') return false;
    if ($f['status'] && $f['status'] !== 'active' && $l['status'] !== $f['status']) return false;
    if ($f['q'] !== '') {
        $hay = strtolower($l['title'] . ' ' . $l['summary'] . ' ' . $hoods[$l['neighborhood']]['name'] . ' ' . $l['zip'] . ' ' . $l['type']);
        foreach (preg_split('/\s+/', strtolower($f['q'])) as $w) if ($w !== '' && !str_contains($hay, $w)) return false;
    }
    return true;
});
$sorts = [
    'newest'     => fn($a, $b) => strcmp($b['listed'], $a['listed']),
    'price-asc'  => fn($a, $b) => $a['price'] <=> $b['price'],
    'price-desc' => fn($a, $b) => $b['price'] <=> $a['price'],
    'sqft'       => fn($a, $b) => $b['sqft'] <=> $a['sqft'],
];
usort($results, $sorts[$f['sort']] ?? $sorts['newest']);
// Sold homes sink to the bottom whatever the sort.
usort($results, fn($a, $b) => ($a['status'] === 'Sold') <=> ($b['status'] === 'Sold'));
$filtered = (bool) array_filter($f, fn($v, $k) => $k !== 'sort' && $v, ARRAY_FILTER_USE_BOTH) || $f['sort'] !== 'newest';

render('listings', ['results' => $results, 'f' => $f, 'filtered' => $filtered], [
    'title'       => 'Seattle Homes for Sale | Houses, Condos & Townhomes',
    'description' => 'Browse Seattle homes for sale: Craftsman houses, townhomes and condos in Ballard, Queen Anne, Capitol Hill, West Seattle and more. Filter by price and beds.',
    'canonical'   => '/homes-for-sale/',
    'noindex'     => $filtered,     // filtered variants consolidate to the main listing page
    'schema'      => [schema_breadcrumbs([['Homes for Sale', '/homes-for-sale/']]),
                      schema_item_list(array_map(fn($l) => '/homes-for-sale/' . $l['slug'] . '/', $results))],
]);
