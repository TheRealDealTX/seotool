<?php
// amandahornby.com front controller: serves the static pages in _pages/ at the
// original site's extensionless URLs and returns real 404s for anything else.
$path = rawurldecode(strtok($_SERVER['REQUEST_URI'] ?? '/', '?'));
// Local preview (php -S): let the built-in server serve real files.
if (PHP_SAPI === 'cli-server' && $path !== '/' && is_file(__DIR__ . $path)) return false;
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$home = 'https://amandahornby.com';
$live = ($host === 'amandahornby.com' || $host === 'www.amandahornby.com');

// On the live domain, force https and the bare host. TLS ends upstream, so check X-Forwarded-Proto.
if ($live && (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.amandahornby.com')) {
    header('Location: ' . $home . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
// Keep the temporary staging domain out of search results.
if (!$live) {
    header('X-Robots-Tag: noindex, nofollow');
}

function go($to) { header('Location: ' . $to, true, 301); exit; }

// Old site's URLs and common variants.
$redirects = [
    '/index.php' => '/', '/home' => '/', '/index.html' => '/',
    '/projects' => '/projects-1', '/blog' => '/journal',
];
if (isset($redirects[$path])) go($redirects[$path]);
if ($path !== '/' && substr($path, -1) === '/') go(rtrim($path, '/'));   // /about/ -> /about

$routes = [
    '/' => 'home', '/about' => 'about', '/projects-1' => 'projects-1', '/press' => 'press',
    '/contact' => 'contact', '/journal' => 'journal', '/privacy' => 'privacy',
];
$page = $routes[$path] ?? null;
if ($page === null && preg_match('#^/journal/([a-z0-9-]+)$#', $path, $m)) {
    $page = 'journal--' . $m[1];
}
$file = $page !== null ? __DIR__ . '/_pages/' . $page . '.html' : null;

header('Content-Type: text/html; charset=utf-8');
if ($file && is_file($file)) {
    header('Cache-Control: public, max-age=600');
    readfile($file);
    exit;
}
http_response_code(404);
readfile(__DIR__ . '/_pages/404.html');
