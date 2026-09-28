<?php
// SmokeDamage.com front controller. The platform serves existing files
// directly, ignores .htaccess, and routes "/" and unknown paths here.
$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$home = 'https://smokedamage.com';

// Canonical host + scheme (TLS terminates upstream; REQUEST_SCHEME is always http here).
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($host === 'www.smokedamage.com' || ($insecure && $host === 'smokedamage.com')) {
    header('Location: ' . $home . $uri, true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Admin and API directories (in case the platform doesn't resolve index.php itself).
if ($path === '/admin' || $path === '/admin/' || $path === '/admin/index.php') {
    if ($path === '/admin') { header('Location: /admin/', true, 301); exit; }
    require __DIR__ . '/admin/index.php';
    exit;
}

// Redirect manager (admin-editable) + permanent redirects from the old WordPress site.
$redirects = [
    '#^/(feed|comments/feed)/?$#' => '/blog/',
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/.*)?$#' => '/',
    '#^/page-sitemap\.xml$#' => '/sitemap.xml',
    '#^/main-sitemap\.xsl$#' => '/sitemap.xml',
    '#^/claims?/?$#' => '/smoke-damage-claims/',
    '#^/services?/?$#' => '/smoke-damage-claims/',
    '#^/service-areas?/?$#' => '/texas/',
    '#^/areas/?$#' => '/texas/',
    '#^/free-claim-review/?$#' => '/contact/',
    '#^/contact-us/?$#' => '/contact/',
    '#^/about-us/?$#' => '/about/',
    '#^/process/?$#' => '/smoke-damage-claim-process/',
];
foreach ($redirects as $re => $to) {
    if (preg_match($re, $path)) { header('Location: ' . $home . $to, true, 301); exit; }
}
if (is_file(__DIR__ . '/api/lib.php')) {
    require_once __DIR__ . '/api/lib.php';
    foreach (sd_read_json('redirects.json', []) as $r) {
        $from = rtrim((string)($r['from'] ?? ''), '/');
        if ($from !== '' && ($from === rtrim($path, '/'))) {
            $code = in_array((int)($r['code'] ?? 301), [301, 302, 307, 308], true) ? (int)$r['code'] : 301;
            $to = (string)($r['to'] ?? '/');
            header('Location: ' . (str_starts_with($to, 'http') ? $to : $home . $to), true, $code);
            exit;
        }
    }
}

// Directory without trailing slash -> add it.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && is_file(__DIR__ . $path . '/index.html')) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
// Directory with trailing slash that the platform handed to us anyway.
if (substr($path, -1) === '/' && strpos($path, '..') === false && is_file(__DIR__ . $path . 'index.html')) {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . $path . 'index.html');
    exit;
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
