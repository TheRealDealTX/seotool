<?php
/** @var array $parts */
$key = $parts[1];
[$label, $blurb, $pillar] = TOPICS[$key];
$posts = topic_posts($key);
$toolSlugs = array_keys(array_filter(tools(), fn($t) => $t['topic'] === $key || ($key === 'kitchen' && $t['topic'] === 'baking')));
$crumbs = [['Home', '/'], ['Journal', '/blog/'], [$label, '/topics/' . $key . '/']];
render('topic', compact('key', 'label', 'blurb', 'pillar', 'posts', 'toolSlugs', 'crumbs'), [
    'title' => $label . ': Guides & Recipes | ' . SITE_NAME,
    'desc' => $blurb . ' ' . count($posts) . ' practical guides from Purely Wholesome Farm.',
    'path' => '/topics/' . $key . '/',
    'schema' => [breadcrumb_schema($crumbs), ['@type' => 'CollectionPage', 'name' => $label, 'url' => canonical('/topics/' . $key . '/'),
        'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => array_values(array_map(fn($p, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => canonical(post_url($p['slug']))], array_values($posts), array_keys(array_values($posts))))]]],
]);
