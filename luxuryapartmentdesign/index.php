<?php
// Front controller for luxuryapartmentdesign.com. .htaccess sends every
// request that is not an existing file here.

declare(strict_types=1);

require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/functions.php';
require __DIR__ . '/inc/layout.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$path = preg_replace('#/+#', '/', $path);

function redirect(string $to, int $code = 301): never
{
    header('Location: ' . (str_starts_with($to, 'http') ? $to : url($to)), true, $code);
    exit;
}

function render(string $view, array $vars = []): never
{
    extract($vars);
    require __DIR__ . '/pages/' . $view . '.php';
    exit;
}

function not_found(): never
{
    http_response_code(404);
    render('404');
}

// Old WordPress media URLs: serve the files from the backup folder
if (preg_match('#^/wp-content/uploads/(.+\.(webp|jpe?g|png|gif|svg|avif|pdf))$#i', $path, $m)) {
    $base = realpath(__DIR__ . '/wp-backup-2026-10-28/wp-content/uploads');
    $file = $base ? realpath($base . '/' . $m[1]) : false;
    if ($file && str_starts_with($file, $base . '/') && is_file($file)) {
        $types = ['webp' => 'image/webp', 'jpg' => 'image/jpeg', 'jpeg' => 'image/jpeg', 'png' => 'image/png', 'gif' => 'image/gif', 'svg' => 'image/svg+xml', 'avif' => 'image/avif', 'pdf' => 'application/pdf'];
        header('Content-Type: ' . $types[strtolower($m[2])]);
        header('Cache-Control: public, max-age=31536000');
        header('Content-Length: ' . filesize($file));
        readfile($file);
        exit;
    }
    not_found();
}

// Legacy WordPress URLs
$redirects = require __DIR__ . '/inc/redirects.php';
$key = rtrim($path, '/') . (str_ends_with($path, '.xml') ? '' : '/');
if (isset($redirects[$key])) {
    redirect($redirects[$key]);
}
if (preg_match('#^/(wp-admin|wp-login\.php|wp-json|xmlrpc\.php|wp-includes)(/|$)#', $path)) {
    redirect('/');
}
if (preg_match('#^/(author|tag)/#', $path)) {
    redirect('/blogs/');
}
if (preg_match('#^/(.+?)/(feed|amp|embed)/?$#', $path, $m)) {
    redirect('/' . $m[1] . '/');
}
if (preg_match('#^(/.*?)/page/\d+/?$#', $path, $m)) {
    redirect(($m[1] ?: '') . '/');
}
if (isset($_GET['p']) || isset($_GET['page_id'])) {
    redirect('/');
}
if (isset($_GET['s']) && $path === '/') {
    redirect('/search/?q=' . rawurlencode((string) $_GET['s']));
}

// Trailing slash on page URLs
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('#\.[a-z0-9]{2,5}$#i', $path)) {
    $qs = parse_url($uri, PHP_URL_QUERY);
    redirect($path . '/' . ($qs ? '?' . $qs : ''));
}

$static = [
    '/'                  => 'home',
    '/blogs/'            => 'blog',
    '/tools/'            => 'tools',
    '/about-us/'         => 'about',
    '/contact/'          => 'contact',
    '/editorial-policy/' => 'editorial',
    '/privacy-policy/'   => 'privacy',
    '/terms-of-use/'     => 'terms',
    '/sitemap/'          => 'sitemap-html',
    '/search/'           => 'search',
    '/sitemap.xml'       => 'sitemap-xml',
    '/rss.xml'           => 'rss',
    '/subscribe/'        => 'subscribe',
    '/search-index.json' => 'search-index',
];
if (isset($static[$path])) {
    render($static[$path]);
}

if (preg_match('#^/category/([a-z0-9-]+)/$#', $path, $m)) {
    if (!isset(CATEGORIES[$m[1]])) {
        not_found();
    }
    render('category', ['slug' => $m[1]]);
}

if (preg_match('#^/tools/([a-z0-9-]+)/$#', $path, $m)) {
    $tool = tool($m[1]);
    if (!$tool) {
        not_found();
    }
    render('tool', ['tool' => $tool]);
}

if (preg_match('#^/([a-z0-9-]+)/$#', $path, $m) && ($a = article($m[1]))) {
    render('article', ['a' => $a]);
}

not_found();
