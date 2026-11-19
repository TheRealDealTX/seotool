<?php defined('SNW') || (http_response_code(404) && exit);
$featured = array_values(array_filter(listings(), fn($l) => !empty($l['featured']) && $l['status'] !== 'Sold'));
usort($featured, fn($a, $b) => strcmp($b['listed'], $a['listed']));
render('home', [
    'featured' => array_slice($featured, 0, 6),
    'latest'   => array_slice(posts(), 0, 3),
], [
    'title'       => 'Seattle Homes for Sale & Local Real Estate Experts',
    'description' => 'Search Seattle homes for sale, explore neighborhood guides and get local help buying or selling in Ballard, Queen Anne, West Seattle and more.',
    'canonical'   => '/',
    'image'       => '/assets/img/brand/og-default.jpg',
    'schema'      => [],
    'preload'     => '/assets/img/brand/seattle-skyline-hero.webp',
]);
