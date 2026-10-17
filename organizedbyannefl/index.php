<?php
// organizedbyannefl.com front controller. The host serves real files directly and
// sends every other path here, so this maps clean URLs (/about, /blog/<slug>) to the
// generated HTML in pages/, keeps old Wix URLs alive with 301s, and returns real 404s.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$qs   = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://organizedbyannefl.com';

function go($to) { header('Location: ' . $to, true, 301); exit; }

// Canonical host and scheme, only once the real domain points here (the temporary
// hostingersite.com domain keeps working as-is). TLS ends upstream, so use X-Forwarded-Proto.
if ($host === 'www.organizedbyannefl.com' ||
    ($host === 'organizedbyannefl.com' && ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http')) {
    go($home . $uri);
}

if ($path === '/contact-submit') { require __DIR__ . '/lib/contact.php'; exit; }

// Old Wix-era and common alternate paths.
$legacy = [
    '/home' => '/', '/index' => '/', '/index.html' => '/', '/blank' => '/', '/about-us' => '/about', '/about-1' => '/about',
    '/services-1' => '/services', '/book-online' => '/contact', '/contact-us' => '/contact', '/contact-1' => '/contact',
    '/blog-1' => '/blog', '/portfolio' => '/services', '/gallery' => '/services', '/feed' => '/blog',
];
$lc = strtolower($path);
if (isset($legacy[rtrim($lc, '/')])) go($legacy[rtrim($lc, '/')] . $qs);
if (preg_match('#^/(post|blog/categories|blog/tags|blog/page|category|tag)(/|$)#', $lc)) go('/blog');
if (preg_match('#^/(wp-admin|wp-login\.php|wp-content|wp-includes|xmlrpc\.php)#', $lc)) go('/');

// Normalise: no trailing slash, lowercase.
if ($path !== '/' && substr($path, -1) === '/') go(rtrim($path, '/') . $qs);
if ($path !== $lc && preg_match('#^/[a-z0-9/-]+$#', $lc)) go($lc . $qs);

$file = null;
if ($path === '/') {
    $file = __DIR__ . '/pages/home.html';
} elseif (preg_match('#^/[a-z0-9-]+(/[a-z0-9-]+)?$#', $path) && $path !== '/404' && is_file(__DIR__ . '/pages' . $path . '.html')) {
    $file = __DIR__ . '/pages' . $path . '.html';
}
header('Content-Type: text/html; charset=utf-8');
header('X-Content-Type-Options: nosniff');
// Keep the hostingersite.com preview domain out of search results; only the real domain is indexed.
if ($host !== 'organizedbyannefl.com') header('X-Robots-Tag: noindex, nofollow');
header('Referrer-Policy: strict-origin-when-cross-origin');
if ($file) {
    header('Cache-Control: public, max-age=600');
    readfile($file);
} else {
    http_response_code(404);
    readfile(__DIR__ . '/pages/404.html');
}
