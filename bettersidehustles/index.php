<?php
// Front controller for bettersidehustles.com. .htaccess sends every request
// that is not a real file here; this maps the path to a template.

declare(strict_types=1);

// Local preview with `php -S localhost:8000 index.php`: let real files through.
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH))) {
    return false;
}

define('BASE_DIR', __DIR__);
require BASE_DIR . '/inc/config.php';
require BASE_DIR . '/inc/functions.php';
require BASE_DIR . '/inc/tools.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(parse_url($uri, PHP_URL_PATH) ?: '/');
$qs   = parse_url($uri, PHP_URL_QUERY);

function redirect(string $to, int $code = 301): never
{
    header('Location: ' . (str_starts_with($to, 'http') ? $to : SITE_URL . $to), true, $code);
    exit;
}

// Canonical scheme and host (Hostinger terminates TLS upstream on some plans).
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$https = ($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https'
    || ($_SERVER['SERVER_PORT'] ?? '') === '443';
$isLocal = $host === '' || str_starts_with($host, 'localhost') || str_starts_with($host, '127.0.0.1');
if (!$isLocal && ($host === 'www.bettersidehustles.com' || !$https)) {
    redirect($uri);
}

// WordPress leftovers.
if (isset($_GET['s'])) {
    redirect('/blog/?q=' . rawurlencode((string) $_GET['s']));
}
if (isset(REDIRECTS[$path])) {
    redirect(REDIRECTS[$path]);
}
if (preg_match('#^/(wp-admin|wp-login\.php|xmlrpc\.php|wp-json|wp-includes)(/|$)#', $path)) {
    redirect('/');
}
if (preg_match('#^/(author|tag|category)/[^/]+/?$#', $path) || preg_match('#^/20\d\d(/\d\d){0,2}/?$#', $path)) {
    redirect('/blog/');
}
if (preg_match('#^/([a-z0-9-]+)/(feed|amp)/?$#', $path, $m)) {
    redirect("/{$m[1]}/");
}

// WordPress generated resized copies (image-300x200.webp); only originals were
// kept, so send old thumbnail URLs to the full-size file.
if (preg_match('#^(/wp-content/uploads/.+)-\d+x\d+(\.(?:webp|png|jpe?g))$#i', $path, $m) && is_file(BASE_DIR . $m[1] . $m[2])) {
    redirect($m[1] . $m[2]);
}
if (preg_match('#^/wp-content/uploads/[^/]+/[^/]+/cropped-Better-Side-Hustles-Site-Icon#', $path)) {
    redirect('/apple-touch-icon.png');
}

// Machine-readable endpoints.
switch ($path) {
    case '/sitemap.xml':
    case '/sitemap_index.xml':
    case '/post-sitemap.xml':
    case '/page-sitemap.xml':
        require BASE_DIR . '/inc/sitemap.php';
        exit;
    case '/feed/':
    case '/feed':
        require BASE_DIR . '/inc/feed.php';
        exit;
}

// Trailing slash for page URLs.
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('#\.[a-z0-9]{2,5}$#i', $path)) {
    redirect($path . '/' . ($qs ? "?$qs" : ''));
}

header('Content-Type: text/html; charset=utf-8');

if ($path === '/') {
    render('home');
    exit;
}
if ($path === '/blog/') {
    render('blog');
    exit;
}
if ($path === '/tools/') {
    render('tools-hub');
    exit;
}
if (preg_match('#^/tools/([a-z0-9-]+)/$#', $path, $m) && isset(TOOLS[$m[1]])) {
    render('tool', ['toolSlug' => $m[1]]);
    exit;
}
if ($path === '/contact/') {
    render('contact');
    exit;
}
if ($path === '/side-hustle-gear/') {
    render('gear');
    exit;
}
if (preg_match('#^/([a-z0-9-]+)/$#', $path, $m) && ($page = content_load($m[1]))) {
    render($page['type'] === 'post' ? 'article' : 'page', ['page' => $page]);
    exit;
}

not_found();
