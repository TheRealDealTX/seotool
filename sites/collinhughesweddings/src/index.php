<?php
// collinhughesweddings.com front controller: serves home.html for "/", redirects
// legacy WordPress paths, and returns a real 404 for anything else.
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Once the real domain is attached: force https and the bare domain.
if ($host === 'www.collinhughesweddings.com' ||
    ($host === 'collinhughesweddings.com' && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http')) {
    header('Location: https://collinhughesweddings.com' . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

$redirects = [
    '#^/(feed|comments/feed|blog|portfolio|gallery|galleries|journal)(/.*)?$#' => '/weddings/',
    '#^/(category|tag|\d{4})(/.*)?$#'                                => '/weddings/',
    '#^/(about-me|about-us|bio|meet-collin)/?$#'                     => '/about/',
    '#^/(contact-me|contact-us|inquire|inquiry|booking)/?$#'         => '/contact/',
    '#^/(pricing|investment|packages|info|information)/?$#'          => '/collections/',
    '#^/(destination|travel|destinations)/?$#'                       => '/destination-weddings/',
    '#^/(chris-jasmine|chrisjasmine|wedding-chris-jasmine)/?$#'     => '/wedding-chrisjasmine/',
    '#^/(maddy-ben|maddy-ben-surrey)/?$#'                            => '/maddy-ben-surrey-uk/',
    '#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#' => '/',
];
foreach ($redirects as $re => $to) {
    if (preg_match($re, $path)) { header('Location: ' . $to, true, 301); exit; }
}
if (substr($path, -1) !== '/' && is_dir(__DIR__ . $path)) {
    header('Location: ' . $path . '/', true, 301);
    exit;
}
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
