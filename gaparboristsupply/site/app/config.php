<?php
// Site settings. Edit here, then redeploy. Nothing secret belongs in this file.
defined('GAP') || exit;

return [
    'name'        => 'Gap Arborist Supply',
    'short'       => 'Gap Arborist',
    'tagline'     => 'Arborist gear, picked by people who climb',
    // Canonical origin used in canonical tags, sitemap and JSON-LD.
    'origin'      => 'https://gaparboristsupply.com',
    // false while the site lives on the temporary *.hostingersite.com domain:
    // every page is noindex and robots.txt disallows everything. Flip to true
    // once gaparboristsupply.com points at this website.
    'live'        => false,
    // When live, requests for any other host (www., the temporary domain) are
    // 301'd to the canonical origin.
    'canonical_host' => 'gaparboristsupply.com',
    'email'       => 'hello@gaparboristsupply.com',

    // Affiliate links. Per-product links go in data/affiliates.json
    // ({"/product/path/": "https://..."}). Products without one use the
    // fallback search URL below; {q} is replaced with the URL-encoded product name.
    // Add your Amazon Associates tag to amazon_tag to have it appended.
    'affiliate_fallback' => 'https://www.amazon.com/s?k={q}',
    'amazon_tag'  => '',

    // Departments in navigation order.
    'departments' => [
        '/climbing/', '/rigging/', '/rope/', '/cutting-and-pruning/', '/jobsite/',
        '/safety/', '/clothing/', '/plant-care/', '/books-and-training-materials/',
    ],
];
