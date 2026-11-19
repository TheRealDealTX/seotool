<?php
/**
 * Exit Real Estate 540 - front controller.
 * The Hostinger platform serves existing files directly and routes every other
 * request here (it ignores .htaccess), so all clean URLs are resolved below.
 */
declare(strict_types=1);
define('ERE', 1);
define('ROOT', __DIR__);

require ROOT . '/inc/functions.php';
require ROOT . '/inc/layout.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$base = cfg('url');

// Canonical host/scheme (TLS terminates upstream, so trust X-Forwarded-Proto).
$isLive = str_ends_with($host, 'exitrealestate540.com');
if ($isLive && (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.exitrealestate540.com')) {
    redirect($base . $uri);
}

function redirect(string $to, int $code = 301): void
{
    header('Location: ' . $to, true, $code);
    exit;
}

function not_found(): void
{
    http_response_code(404);
    require ROOT . '/inc/pages/404.php';
    exit;
}

// Old WordPress and legacy paths.
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-content|wp-login\.php|xmlrpc\.php|elementor-hf)(/|$)#', $path)) {
    redirect('/');
}
$trim = trim($path, '/');
$legacy = cfg('redirects');
if ($trim !== '' && isset($legacy[$trim])) {
    redirect($legacy[$trim]);
}

// Trailing slash on page routes.
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('#\.[a-z0-9]{2,5}$#i', $path)) {
    redirect($path . '/' . (($q = parse_url($uri, PHP_URL_QUERY)) ? '?' . $q : ''));
}

$seg = $trim === '' ? [] : explode('/', $trim);

switch (true) {
    case $path === '/' || $path === '/index.php':
        require ROOT . '/inc/pages/home.php';
        break;
    case $path === '/blog/':
        require ROOT . '/inc/pages/blog.php';
        break;
    case count($seg) === 2 && $seg[0] === 'blog':
        $post = get_post($seg[1]) ?? not_found();
        require ROOT . '/inc/pages/post.php';
        break;
    case count($seg) === 2 && $seg[0] === 'category':
        $cat = category($seg[1]) ?? not_found();
        require ROOT . '/inc/pages/category.php';
        break;
    case $path === '/tools/':
        require ROOT . '/inc/pages/tools.php';
        break;
    case count($seg) === 2 && $seg[0] === 'tools':
        $tool = tools()[$seg[1]] ?? not_found();
        require ROOT . '/inc/pages/tool.php';
        break;
    case $path === '/recommended-products/':
        require ROOT . '/inc/pages/products.php';
        break;
    case $path === '/contact/':
        require ROOT . '/inc/pages/contact.php';
        break;
    case in_array($trim, ['about', 'write-for-us', 'affiliate-disclosure', 'privacy-policy', 'terms'], true):
        $page = $trim;
        require ROOT . '/inc/pages/static.php';
        break;
    case $path === '/sitemap.xml':
        require ROOT . '/inc/pages/sitemap.php';
        break;
    case $path === '/feed.xml':
        require ROOT . '/inc/pages/feed.php';
        break;
    default:
        not_found();
}
