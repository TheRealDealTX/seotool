<?php
/**
 * austinlandscapelighting.com - front controller.
 *
 * The Hostinger Agency (php-fpm) platform serves existing files directly and
 * routes "/" plus every unknown path here. PHP's built-in server does the same
 * when started with this file as the router:  php -S 127.0.0.1:8080 index.php
 */
declare(strict_types=1);

require __DIR__ . '/lib/bootstrap.php';
const ASSET_VERSION = '20261006';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = parse_url($uri, PHP_URL_PATH) ?: '/';
$path = preg_replace('#/{2,}#', '/', $path);

// --- Built-in server: hand real files back to the server -------------------
if (PHP_SAPI === 'cli-server' && $path !== '/' && is_file(__DIR__ . $path)) {
    return false;
}

// --- Canonical scheme + host (TLS terminates upstream, so check the header) --
$host = $_SERVER['HTTP_HOST'] ?? '';
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
if ($insecure || $host === 'www.austinlandscapelighting.com') {
    redirect(SITE_ORIGIN . $uri);
}

// --- Form handler ------------------------------------------------------------
if ($path === '/contact/send') {
    require __DIR__ . '/pages/contact-send.php';
    exit;
}

// --- Machine-readable files --------------------------------------------------
if ($path === '/sitemap.xml') {
    require __DIR__ . '/pages/sitemap-xml.php';
    exit;
}
if (preg_match('#^/(sitemap_index|post-sitemap|page-sitemap|category-sitemap)\.xml$#', $path)) {
    redirect(SITE_ORIGIN . '/sitemap.xml');
}

// --- Legacy WordPress paths --------------------------------------------------
if (preg_match('#^/(feed|comments/feed|category(/.*)?|tag(/.*)?|author(/.*)?)/?$#', $path)) {
    redirect(SITE_ORIGIN . '/blog/');
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-content)(/|$)#', $path)) {
    redirect(SITE_ORIGIN . '/');
}
if ($path === '/terms-of-use/' || $path === '/terms/') {
    redirect(SITE_ORIGIN . '/terms-of-service/');
}
if ($path === '/index.php' || $path === '/home/' || $path === '/home') {
    redirect(SITE_ORIGIN . '/');
}

// --- Trailing slash ----------------------------------------------------------
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('#\.[a-z0-9]{2,5}$#i', $path)) {
    redirect(SITE_ORIGIN . $path . '/');
}

// --- Routes ------------------------------------------------------------------
$static = [
    '/'                  => 'home',
    '/services/'         => 'services',
    '/service-areas/'    => 'areas',
    '/blog/'             => 'blog',
    '/tools/'            => 'tools',
    '/gallery/'          => 'gallery',
    '/about-us/'         => 'about',
    '/contact/'          => 'contact',
    '/reviews/'          => 'reviews',
    '/faq/'              => 'faq',
    '/privacy-policy/'   => 'privacy',
    '/terms-of-service/' => 'terms',
    '/sitemap/'          => 'sitemap',
    '/thank-you/'        => 'thank-you',
];

if (isset($static[$path])) {
    require __DIR__ . '/pages/' . $static[$path] . '.php';
    exit;
}

if (preg_match('#^/services/([a-z0-9-]+)/$#', $path, $m) && service($m[1])) {
    $slug = $m[1];
    require __DIR__ . '/pages/service.php';
    exit;
}
if (preg_match('#^/service-areas/([a-z0-9-]+)/$#', $path, $m) && area($m[1])) {
    $slug = $m[1];
    require __DIR__ . '/pages/area.php';
    exit;
}
if (preg_match('#^/tools/([a-z0-9-]+)/$#', $path, $m) && isset(TOOLS[$m[1]])) {
    $slug = $m[1];
    require __DIR__ . '/pages/tool.php';
    exit;
}
if (preg_match('#^/blog/([a-z0-9-]+)/$#', $path, $m) && post($m[1])) {
    // Posts live at the root (as on the old site); keep /blog/<slug>/ working.
    redirect(SITE_ORIGIN . '/' . $m[1] . '/');
}
if (preg_match('#^/([a-z0-9-]+)/$#', $path, $m) && post($m[1])) {
    $slug = $m[1];
    require __DIR__ . '/pages/post.php';
    exit;
}

// --- 404 ---------------------------------------------------------------------
http_response_code(404);
require __DIR__ . '/pages/404.php';
