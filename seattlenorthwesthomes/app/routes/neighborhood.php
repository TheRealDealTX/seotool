<?php defined('SNW') || (http_response_code(404) && exit);
$hood = neighborhoods()[$slug] ?? null;
if (!$hood) { not_found(); return; }
$homes = array_values(array_filter(listings(), fn($l) => $l['neighborhood'] === $slug));
usort($homes, fn($a, $b) => ($a['status'] === 'Sold') <=> ($b['status'] === 'Sold') ?: strcmp($b['listed'], $a['listed']));
$name = $hood['name'];
$posts = array_slice(array_filter(posts(), fn($p) => stripos($p['body'], '/neighborhoods/' . $slug . '/') !== false || stripos($p['title'], $name) !== false), 0, 3);
$faq = [
    ['q' => 'What kinds of homes are in ' . $name . '?', 'a' => $hood['body'][0][1]],
    ['q' => 'How do people get around from ' . $name . '?', 'a' => $hood['body'][1][1]],
    ['q' => 'Who is ' . $name . ' a good fit for?', 'a' => $hood['body'][2][1]],
];
render('neighborhood', ['slug' => $slug, 'hood' => $hood, 'homes' => $homes, 'posts' => $posts, 'faq' => $faq], [
    'title'       => $name . ' Homes for Sale | Seattle Neighborhood Guide',
    'description' => 'Explore ' . $name . ' homes for sale and our guide to living in ' . $name . ', Seattle: housing, commute, parks and who it suits.',
    'canonical'   => '/neighborhoods/' . $slug . '/',
    'image'       => photo($hood['image']),
    'schema'      => [
        schema_breadcrumbs([['Neighborhoods', '/neighborhoods/'], [$name, '/neighborhoods/' . $slug . '/']]),
        ['@type' => 'Place', 'name' => $name . ', Seattle, WA', 'description' => $hood['intro'],
         'containedInPlace' => ['@type' => 'City', 'name' => 'Seattle']],
        schema_faq($faq),
    ],
]);
