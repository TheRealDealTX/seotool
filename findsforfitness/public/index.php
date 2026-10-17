<?php
// findsforfitness.com front controller. The host routes "/" and unknown paths here
// (and ignores .htaccess), so this file serves the homepage, legacy redirects and real 404s.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://findsforfitness.com';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.findsforfitness.com') {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}
$redirects = [
    '#^/contact-us(-2)?/?$#'            => '/contact/',
    '#^/privacy-policy-\d+/?$#'          => '/privacy-policy/',
    '#^/disclaimer/?$#'                  => '/disclaimers/',
    '#^/terms(-of-use|-and-conditions)?/?$#' => '/terms-of-service/',
    '#^/category/health_news/?$#'        => '/blog/',
    '#^/category/uncategorized/?$#'      => '/blog/',
    '#^/(page/\d+|feed|comments/feed|author/[^/]+)/?$#' => '/blog/',
    '#^/category/([a-z_-]+)/page/\d+/?$#' => '/category/$1/',
    '#^/(wp-admin|wp-includes|wp-json|wp-content|wp-login\.php|xmlrpc\.php)(/|$)#' => '/',
];
foreach ($redirects as $re => $to) {
    if (preg_match($re, $path, $m)) {
        header('Location: ' . $home . preg_replace($re, $to, $path), true, 301);
        exit;
    }
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
