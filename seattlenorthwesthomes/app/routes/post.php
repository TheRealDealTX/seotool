<?php defined('SNW') || (http_response_code(404) && exit);
$post = post($slug);
if (!$post) { not_found(); return; }
$cat = categories()[$post['category']] ?? ['name' => 'Articles'];
$title = $post['title'];
if (mb_strlen($title) < 45) $title .= ' | Seattle Northwest Homes';
render('post', ['post' => $post, 'cat' => $cat, 'related' => related_posts($post)], [
    'title'       => $title,
    'description' => $post['description'],
    'canonical'   => '/blog/' . $post['slug'] . '/',
    'image'       => post_image($post),
    'type'        => 'article',
    'published'   => $post['date'],
    'modified'    => $post['modified'],
    'schema'      => [
        schema_post($post),
        schema_breadcrumbs([['Blog', '/blog/'], [$cat['name'], '/blog/category/' . $post['category'] . '/'], [$post['title'], '/blog/' . $post['slug'] . '/']]),
        schema_faq($post['faq'] ?? []),
    ],
]);
