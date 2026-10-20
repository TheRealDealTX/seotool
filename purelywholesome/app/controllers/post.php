<?php
/** @var array $post */
$index = posts_index();
$topic = $post['topic'];
[$topicLabel] = TOPICS[$topic] ?? ['Journal'];
$crumbs = [['Home', '/'], [$topicLabel, $post['indexable'] && isset(TOPICS[$topic]) ? '/topics/' . $topic . '/' : '/blog/'], [$post['h1'], post_url($post['slug'])]];
$related = array_values(array_filter(array_map(fn($s) => $index[$s] ?? null, $index[$post['slug']]['related'] ?? [])));

// Table of contents from the article's h2s.
preg_match_all('#<h2 id="([^"]+)">(.*?)</h2>#s', $post['html'], $m, PREG_SET_ORDER);
$toc = array_map(fn($x) => [$x[1], strip_tags($x[2])], $m);

// Put the first tool mid-article (before the third h2) so readers meet it while reading.
$html = $post['html'];
$toolHtml = $post['tools'] ? render_tool($post['tools'][0]) : '';
if ($toolHtml) {
    $parts = preg_split('#(?=<h2 )#', $html);
    $at = min(3, count($parts) - 1);
    $html = $at > 0 ? implode('', array_slice($parts, 0, $at)) . '<div class="embed-tool">' . $toolHtml . '</div>' . implode('', array_slice($parts, $at)) : $html . $toolHtml;
}
// Lead image loads eagerly; the first inline image is usually below the fold.
$url = canonical(post_url($post['slug']));
$schema = [
    [
        '@type' => 'BlogPosting', '@id' => $url . '#article', 'headline' => $post['h1'], 'description' => $post['desc'],
        'datePublished' => $post['published'], 'dateModified' => $post['modified'], 'wordCount' => $post['words'],
        'mainEntityOfPage' => $url, 'inLanguage' => 'en-US', 'articleSection' => $topicLabel,
        'author' => ['@type' => 'Organization', 'name' => SITE_NAME . ' Kitchen & Barn Team', 'url' => SITE_ORIGIN . '/about-us/'],
        'publisher' => ['@id' => SITE_ORIGIN . '/#organization'],
        'image' => $post['image'] ? ['@type' => 'ImageObject', 'url' => canonical($post['image']), 'width' => $post['image_w'], 'height' => $post['image_h']] : null,
    ],
    breadcrumb_schema($crumbs),
];
if ($post['faq']) {
    $schema[] = ['@type' => 'FAQPage', '@id' => $url . '#faq', 'mainEntity' => array_map(fn($f) => [
        '@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f['a'])]], $post['faq'])];
}
render('post', compact('post', 'html', 'toc', 'related', 'crumbs', 'topicLabel'), [
    'title' => $post['title'] . ' | ' . SITE_NAME,
    'desc' => $post['desc'],
    'path' => post_url($post['slug']),
    'robots' => $post['indexable'] ? null : 'noindex, follow',
    'og_type' => 'article',
    'og_image' => $post['image'] ?: null,
    'preload' => $post['image'] ?: null,
    'schema' => $schema,
    'body_class' => 'is-post',
]);
