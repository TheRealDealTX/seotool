<?php
// live-style.co.uk front controller. The host serves existing files directly and
// sends "/" plus every unknown path here (it ignores .htaccess), so this file
// handles the homepage, robots.txt, legacy WordPress URLs and real 404s.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$prod = 'live-style.co.uk';

function go($to) { header('Location: ' . $to, true, 301); exit; }

// Canonical host and scheme on the real domain (TLS terminates upstream).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.' . $prod || ($host === $prod && $insecure)) {
    go('https://' . $prod . $uri);
}

if ($path === '/robots.txt') {
    header('Content-Type: text/plain; charset=utf-8');
    if ($host !== $prod) {           // temporary/preview domains stay out of the index
        echo "User-agent: *\nDisallow: /\n";
    } else {
        echo "User-agent: *\nDisallow: /contact.php\nDisallow: /home.html\n\nSitemap: https://$prod/sitemap.xml\n";
    }
    exit;
}

// Old WordPress query-string URLs.
if ($path === '/' || $path === '/index.php') {
    if (isset($_GET['cat'])) go($_GET['cat'] === '134588537' ? '/category/january-cure/' : '/journal/');
    if (isset($_GET['s']) || isset($_GET['p']) || isset($_GET['page_id']) || isset($_GET['m'])) go('/journal/');
    if (isset($_GET['feed'])) go('/');
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old WordPress paths.
if (preg_match('#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#', $path)) go('/');
if (preg_match('#^/(comments/)?feed/?$#', $path)) go('/journal/');
if (preg_match('#^/page/\d+/?$#', $path)) go('/journal/');
if (preg_match('#^/author/[^/]+#', $path)) go('/about/');
if (preg_match('#^/\d{4}(/\d{2}(/\d{2})?)?/?$#', $path)) go('/journal/');
if (preg_match('#^/((?:category|tag)/[^/]+)/(page/\d+|feed)/?$#', $path, $m)) go('/' . $m[1] . '/');
if (preg_match('#^/category/[^/]+/([^/]+)/?$#', $path, $m) && is_dir(__DIR__ . '/category/' . $m[1])) go('/category/' . $m[1] . '/');

// Directory without trailing slash.
if (substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.html')) go($path . '/');

// Unknown child of a real page (old attachment pages, /amp/, /feed/, /comment-page-2/): send to the parent.
$parent = rtrim(dirname(rtrim($path, '/')), '/');
if ($parent !== '' && strpos($parent, '..') === false && is_file(__DIR__ . $parent . '/index.html')) go($parent . '/');

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
