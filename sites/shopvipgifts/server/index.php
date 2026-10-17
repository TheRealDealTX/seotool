<?php
// shopvipgifts.com - static site front controller.
// The host serves real files directly and routes "/" and unknown paths here.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://shopvipgifts.com';

// Canonical host + scheme (TLS terminates upstream, so check X-Forwarded-Proto).
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
if ($host === 'www.shopvipgifts.com' || ($insecure && $host === 'shopvipgifts.com')) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php' || $path === '/index.html') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// Legacy shop / CMS URLs from the old site -> closest new page.
$legacy = [
    '#^/(shop|store|products?|collections?|product-category|catalog)(/.*)?$#i' => '/gift-guides/',
    '#^/(cart|checkout|my-account|account|wishlist)(/.*)?$#i'                  => '/gift-guides/',
    '#^/(blogs?/news|news|blogs?)(/.*)?$#i'                                    => '/blog/',
    '#^/(pages/)?(about|about-us)/?$#i'                                        => '/about/',
    '#^/(pages/)?(contact|contact-us)/?$#i'                                    => '/contact/',
    '#^/(feed|comments/feed|rss)/?$#i'                                         => '/blog/',
    '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|admin)(/|$)#i' => '/',
    '#^/(privacy|privacy-policy|pages/privacy-policy|policies/privacy-policy)/?$#i' => '/privacy-policy/',
    '#^/(terms|terms-of-service|terms-and-conditions|policies/terms-of-service)/?$#i' => '/terms/',
];
foreach ($legacy as $re => $to) {
    if (preg_match($re, $path) && rtrim($path, '/') . '/' !== $to) {
        header('Location: ' . $home . $to, true, 301);
        exit;
    }
}

// Directory without trailing slash -> add it.
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path) && strpos($path, '..') === false) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
