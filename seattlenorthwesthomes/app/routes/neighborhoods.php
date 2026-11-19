<?php defined('SNW') || (http_response_code(404) && exit);
render('neighborhoods', [], [
    'title'       => 'Seattle Neighborhood Guide | Where to Buy a Home in Seattle',
    'description' => 'Compare Seattle neighborhoods like Ballard, Queen Anne, Capitol Hill and West Seattle, with housing, commute and lifestyle notes plus homes for sale.',
    'canonical'   => '/neighborhoods/',
    'schema'      => [schema_breadcrumbs([['Neighborhoods', '/neighborhoods/']]),
                      schema_item_list(array_map(fn($s) => '/neighborhoods/' . $s . '/', array_keys(neighborhoods())))],
]);
