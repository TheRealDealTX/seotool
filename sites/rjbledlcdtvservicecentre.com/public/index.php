<?php
// rjbledlcdtvservicecentre.com front controller. The host serves real files directly, ignores
// .htaccess and routes "/" plus every unknown path here. See README "Hosting".
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = strtok($uri, '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://rjbledlcdtvservicecentre.com';

// Canonical host/scheme, only once the real domain points here (the temporary
// *.hostingersite.com domain is left alone). TLS terminates upstream.
if (strpos($host, 'rjbledlcdtvservicecentre.com') !== false) {
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($insecure || $host === 'www.rjbledlcdtvservicecentre.com') {
        header('Location: ' . $home . $uri, true, 301);
        exit;
    }
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Old WordPress URLs that still carry links or rankings.
$legacy = [
    '/author/admin' => '/about/',
    '/tag/lcd-tv-repairing-centre-in-budge-budge' => '/lcd-tv-repairing-centre-in-budge-budge/',
    '/tag/lcd-tv-repairing-centre-in-gangpur' => '/lcd-tv-repairing-centre-in-gangpur/',
    '/tag/led-tv-repairing-service-centre-in-kolkata' => '/led-lcd-tv-repairing-in-kolkata/',
    '/tag/lg-led-tv-service-centre-in-kakurgachi' => '/lg-led-tv-service-centre-in-kakurgachi/',
    '/tag/lg-led-tv-service-centre-in-kolkata' => '/lg-led-lcd-tv-service-centre-kolkata/',
    '/tag/lg-led-tv-service-centre-in-palta' => '/lg-led-tv-service-centre-in-palta/',
    '/tag/samsung-led-tv-service-centre-in-barrackpore' => '/samsung-led-tv-service-centre-in-barrackpore/',
    '/tag/samsung-led-tv-service-centre-in-bhadreshwar' => '/samsung-led-tv-service-centre-in-bhadreshwar/',
    '/tag/samsung-led-tv-service-centre-in-kolkata' => '/samsung-led-lcd-tv-service-centre-kolkata/',
    '/tag/samsung-led-tv-service-centre-in-naihati' => '/samsung-led-tv-service-centre-in-naihati/',
    '/tag/sony-led-tv-service-centre-in-kolkata' => '/sony-led-lcd-tv-service-centre-kolkata/'
];
$key = rtrim($path, '/');
if (isset($legacy[$key])) {
    header('Location: ' . $legacy[$key], true, 301);
    exit;
}
if (preg_match('#^/tag/#', $path)) {
    header('Location: /service-areas/', true, 301);
    exit;
}
if (preg_match('#^/(feed|comments/feed|category/[^/]+)/?$#', $path)) {
    header('Location: /', true, 301);
    exit;
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-content|wp-login\.php|xmlrpc\.php)(/|$)#', $path)) {
    header('Location: /', true, 301);
    exit;
}
// /some-page -> /some-page/ (old backlinks often omit the slash)
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) {
    header('Location: ' . $path . '/' . (strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : ''), true, 301);
    exit;
}
// /some-page/ without index.html on this host -> serve it if present
$candidate = __DIR__ . rtrim($path, '/') . '/index.html';
if (strpos($path, '..') === false && is_file($candidate)) {
    header('Content-Type: text/html; charset=utf-8');
    readfile($candidate);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
