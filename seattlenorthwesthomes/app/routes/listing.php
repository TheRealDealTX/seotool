<?php defined('SNW') || (http_response_code(404) && exit);
$l = listing($slug);
if (!$l) { not_found(); return; }
$hood = neighborhoods()[$l['neighborhood']];
$similar = array_filter(listings(), fn($x) => $x['slug'] !== $l['slug'] && $x['status'] !== 'Sold'
    && ($x['neighborhood'] === $l['neighborhood'] || $x['type'] === $l['type']));
usort($similar, fn($a, $b) => abs($a['price'] - $l['price']) <=> abs($b['price'] - $l['price']));
$label = $l['status'] === 'Sold' ? 'Sold' : 'For Sale';
// Prefer "<Hood> <type> for sale: <summary>"; fall back to the summary alone if that runs past 145 chars.
$desc = $hood['name'] . ' ' . strtolower($l['type']) . ' ' . strtolower($label) . ': ' . $l['summary'];
if (mb_strlen($desc) > 145) $desc = $l['summary'];
$desc = meta_desc($desc);
render('listing', ['l' => $l, 'hood' => $hood, 'similar' => array_slice($similar, 0, 3)], [
    'title'       => $l['title'] . ' — ' . money($l['price']),
    'description' => $desc,
    'canonical'   => '/homes-for-sale/' . $l['slug'] . '/',
    'image'       => photo($l['images'][0]),
    'type'        => 'product',
    'preload'     => photo($l['images'][0]),
    'schema'      => [schema_listing($l), schema_breadcrumbs([['Homes for Sale', '/homes-for-sale/'], [$hood['name'], '/neighborhoods/' . $l['neighborhood'] . '/'], [$l['title'], '/homes-for-sale/' . $l['slug'] . '/']])],
]);
