<?php defined('SNW') || (http_response_code(404) && exit);
$l = listing($slug);
if (!$l) { not_found(); return; }
$hood = neighborhoods()[$l['neighborhood']];
$similar = array_filter(listings(), fn($x) => $x['slug'] !== $l['slug'] && $x['status'] !== 'Sold'
    && ($x['neighborhood'] === $l['neighborhood'] || $x['type'] === $l['type']));
usort($similar, fn($a, $b) => abs($a['price'] - $l['price']) <=> abs($b['price'] - $l['price']));
$label = $l['status'] === 'Sold' ? 'Sold' : 'For Sale';
render('listing', ['l' => $l, 'hood' => $hood, 'similar' => array_slice($similar, 0, 3)], [
    'title'       => $l['title'] . ' — ' . money($l['price']),
    'description' => excerpt($hood['name'] . ', Seattle ' . strtolower($l['type']) . ' ' . strtolower($label) . ': ' . $l['beds'] . ' bed, ' . fmt_baths($l['baths']) . ' bath, ' . number_format($l['sqft']) . ' sq ft. ' . $l['summary'], 158),
    'canonical'   => '/homes-for-sale/' . $l['slug'] . '/',
    'image'       => photo($l['images'][0]),
    'type'        => 'product',
    'preload'     => photo($l['images'][0]),
    'schema'      => [schema_listing($l), schema_breadcrumbs([['Homes for Sale', '/homes-for-sale/'], [$hood['name'], '/neighborhoods/' . $l['neighborhood'] . '/'], [$l['title'], '/homes-for-sale/' . $l['slug'] . '/']])],
]);
