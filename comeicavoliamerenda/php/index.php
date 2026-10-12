<?php
// comeicavoliamerenda.com front controller.
// The host serves existing files directly and sends everything else here
// (it ignores .htaccess). We serve the homepage, 301 the old site's URLs to
// their new pages, answer old spam PDFs with 410, and 404 the rest.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Canonical host/scheme once the real domain is attached (TLS ends upstream).
$canonical = 'comeicavoliamerenda.com';
$insecure  = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.' . $canonical || ($host === $canonical && $insecure)) {
    header('Location: https://' . $canonical . $uri, true, 301);
    exit;
}
// Keep the temporary *.hostingersite.com preview out of search indexes.
if (substr($host, -strlen('.hostingersite.com')) === '.hostingersite.com') {
    header('X-Robots-Tag: noindex, nofollow');
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

$redirects = require __DIR__ . '/redirects.php';
$lookup = rawurldecode($path);
if (isset($redirects[$lookup])) {
    header('Location: ' . $redirects[$lookup], true, 301);
    exit;
}
// Same URL without the trailing slash / with "www" variants already handled above.
$alt = substr($lookup, -1) === '/' ? rtrim($lookup, '/') : $lookup . '/';
if (isset($redirects[$alt])) {
    header('Location: ' . $redirects[$alt], true, 301);
    exit;
}
// Old Blogger-era posts, labels and feeds -> homepage.
if (preg_match('#^/(19|20)\d\d/\d\d/.+\.html$#', $lookup) || preg_match('#^/(search|feeds)(/|$)#', $lookup)) {
    header('Location: /', true, 301);
    exit;
}
$gone = require __DIR__ . '/gone.php';
if (isset($gone[$lookup]) || preg_match('#^/[^/]+\.pdf$#i', $lookup)) {
    http_response_code(410);
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/404.html');
    exit;
}
if (preg_match('#^/(wp-admin|wp-login\.php|wp-content|wp-includes|xmlrpc\.php|feed)(/|$)#', $lookup)) {
    header('Location: /', true, 301);
    exit;
}
if (substr($lookup, -1) !== '/' && is_dir(__DIR__ . $lookup) && strpos($lookup, '..') === false) {
    header('Location: ' . $lookup . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
