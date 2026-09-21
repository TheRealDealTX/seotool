<?php
/**
 * Plugin Name: Static site shim
 * Description: huttoroofs.com is a static site. The Hostinger managed-WordPress platform keeps a
 *              protected index.php in the document root, routes "/" and every unknown path to
 *              it, and ignores .htaccess. This must-use plugin runs before any theme loads and
 *              turns that front controller into a static file server: the homepage for "/",
 *              301s for old WordPress and upload URLs, and a real 404 for everything else.
 */
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$home = 'https://huttoroofs.com';

if ($path === '/' || $path === '/index.php') {
    header('Content-Type: text/html; charset=utf-8');
    readfile(ABSPATH . 'index.html');
    exit;
}

// Media that used to live under wp-content/uploads now lives in /assets/img/.
if (preg_match('#^/wp-content/uploads/\d{4}/\d{2}/([^/]+)$#', $path, $m)) {
    $file = preg_replace('/-\d+x\d+(\.\w+)$/', '$1', $m[1]);   // drop WP size suffixes
    if (is_file(ABSPATH . 'assets/img/' . $file)) {
        header('Location: ' . $home . '/assets/img/' . $file, true, 301);
        exit;
    }
}

if (preg_match('#^/(feed|comments/feed)/?$#', $path)) {
    header('Location: ' . $home . '/blog/', true, 301);
    exit;
}

if (preg_match('#^/(wp-admin|wp-includes|wp-content|wp-json|wp-login\.php|xmlrpc\.php|wp-[a-z-]+\.php)(/|$)#', $path)) {
    header('Location: ' . $home . '/', true, 301);
    exit;
}

// A directory URL without its trailing slash, e.g. /services -> /services/.
if (is_dir(ABSPATH . ltrim($path, '/')) && substr($path, -1) !== '/') {
    header('Location: ' . $home . $path . '/', true, 301);
    exit;
}

http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
header('X-LiteSpeed-Cache-Control: no-cache');
readfile(ABSPATH . '404.html');
exit;
