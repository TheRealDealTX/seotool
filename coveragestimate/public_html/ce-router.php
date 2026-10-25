<?php
// Redirects legacy WordPress query-string URLs to their permanent paths.
$map = require __DIR__ . '/ce-private/idmap.php';
$target = null;
foreach (['p', 'page_id'] as $key) {
    if (isset($_GET[$key]) && ctype_digit((string) $_GET[$key]) && isset($map['ids'][$_GET[$key]])) {
        $target = $map['ids'][$_GET[$key]];
    }
}
if ($target === null && isset($_GET['cat']) && ctype_digit((string) $_GET['cat']) && isset($map['cats'][$_GET['cat']])) {
    $target = $map['cats'][$_GET['cat']];
}
if ($target === null && isset($_GET['author'])) {
    $target = '/';
}
if ($target === null && isset($_GET['s'])) {
    // The site has no on-page search box; send searches to the article index.
    header('Location: /blog/', true, 302);
    exit;
}
if ($target !== null) {
    header('Location: ' . $target, true, 301);
    exit;
}
http_response_code(404);
readfile(__DIR__ . '/404.html');
