<?php
// hotsbuzz.com - static site front controller. See sites/hotsbuzz/README.md, "Hosting".
// The platform serves real files directly and routes "/" plus every unknown
// path here, so this file serves the homepage, 301s legacy WordPress-style
// URLs and returns a real 404 for everything else.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Canonical scheme/host. TLS terminates upstream, so trust X-Forwarded-Proto.
// Only hotsbuzz.com hosts are forced; the temporary preview domain is left alone.
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.hotsbuzz.com' || ($insecure && $host === 'hotsbuzz.com')) {
    header('Location: https://hotsbuzz.com' . $uri, true, 301);
    exit;
}
if ($insecure && $host !== '') {
    header('Location: https://' . $host . $uri, true, 301);
    exit;
}

// Old WordPress search links ("/?s=term").
if (isset($_GET['s']) && is_string($_GET['s'])) { header('Location: /projects/?q=' . rawurlencode($_GET['s']), true, 301); exit; }

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Legacy WordPress URLs from the original hotsbuzz.com.
$legacy = [
    '#^/(feed|rss|comments/feed)(/.*)?$#'                             => '/feed.xml',
    '#^/(page/\d+|blog|tag/[^/]+|search/.*|\d{4}(/\d{2})?(/\d{2})?)/?$#' => '/projects/',
    '#^/(author/[^/]+|about-us)/?$#'                                  => '/about/',
    '#^/(contact-us)/?$#'                                             => '/contact/',
    '#^/(privacy|privacy-policy-2)/?$#'                               => '/privacy-policy/',
    '#^/category/(diy|diy-projects|diy-ideas|home-decor)/?$#'         => '/category/diy-home-decor/',
    '#^/category/(crafts|craft|craft-ideas)/?$#'                      => '/category/creative-crafts/',
    '#^/category/(christmas|christmas-diy-crafts)/?$#'                => '/category/christmas-crafts/',
    '#^/category/(halloween|happy-halloween)/?$#'                     => '/category/halloween-crafts/',
    '#^/category/(thanksgiving)/?$#'                                  => '/category/thanksgiving-crafts/',
    '#^/category/(valentines|valentines-day)/?$#'                     => '/category/valentines-crafts/',
    '#^/category/(st-patricks-day|saint-patricks-day)/?$#'            => '/category/st-patricks-day-crafts/',
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-content)(/|$)#' => '/',
];
foreach ($legacy as $re => $to) {
    if (preg_match($re, $path)) {
        header('Location: ' . $to, true, 301);
        exit;
    }
}

// Directory without trailing slash.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
