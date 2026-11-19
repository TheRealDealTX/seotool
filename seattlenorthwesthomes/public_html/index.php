<?php
/*
 * Seattle Northwest Homes — front controller.
 *
 * The Hostinger php-fpm platform serves real files directly, ignores .htaccess,
 * and sends every other request here, so all routing and every legacy
 * WordPress redirect lives in this file.
 */
// Local dev (php -S … index.php): let the built-in server deliver real files.
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH))) return false;
define('PUBLIC_DIR', __DIR__);
// App code lives beside public_html when deployed (not web-reachable); fall back to ./app.
require is_file(__DIR__ . '/../app/bootstrap.php') ? __DIR__ . '/../app/bootstrap.php' : __DIR__ . '/app/bootstrap.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(parse_url($uri, PHP_URL_PATH) ?: '/');
$qs   = (string) parse_url($uri, PHP_URL_QUERY);
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

/* ---------- canonical scheme + host ---------- */
if (cfg('force_canonical_host')) {
    $canon = parse_url(cfg('url'), PHP_URL_HOST);
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($insecure || ($host !== '' && $host !== $canon)) redirect(cfg('url') . $uri);
}

// Keep preview/staging hostnames out of search results.
if (str_ends_with($host, '.hostingersite.com')) header('X-Robots-Tag: noindex, nofollow');

/* ---------- legacy WordPress URLs (301) ---------- */
$p = trim($path, '/');
$legacyPages = [
    'about-us' => '/about-seattle-northwest-homes/',
    'buying' => '/buy-a-home-in-seattle/',
    'selling' => '/sell-your-home-seattle/',
    'contact-us' => '/contact-seattle-real-estate-agents/',
    'category/articles' => '/blog/',
    'author/selena' => '/about-seattle-northwest-homes/',
    'home' => '/',
    'comments/feed' => '/feed/',
    'blog/feed' => '/feed/',
    'index.php' => '/',
];
if (isset($legacyPages[$p])) redirect($legacyPages[$p]);
if (preg_match('#^(category/articles|author/selena|page)/(page/)?\d+$#', $p)) redirect('/blog/');
if (preg_match('#^(sitemap_index|post-sitemap|page-sitemap|category-sitemap|author-sitemap|wp-sitemap[\w-]*)\.xml$#', $p)) redirect('/sitemap.xml');
if (preg_match('#^(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-content/(themes|plugins))(/|$)#', $p)) redirect('/');
if (str_starts_with($p, 'wp-content/uploads/')) {
    $map = data('legacy-media');
    redirect($map['/' . $p] ?? '/');
}
// Old post URLs lived at the site root: /<old-slug>/ and /<old-slug>/feed/
if (preg_match('#^([a-z0-9-]+)(/feed|/amp)?$#', $p, $m)) {
    $lm = legacy_post_map();
    if (isset($lm[$m[1]])) redirect('/blog/' . $lm[$m[1]] . '/');
}
// ?p=123 / ?page_id=… style WordPress links
if ($path === '/' && preg_match('/(^|&)(p|page_id|cat|author)=/', $qs)) redirect('/');

/* ---------- trailing slash ---------- */
$isFile = (bool) preg_match('#\.[a-z0-9]{2,5}$#i', $path);
if (!$isFile && $path !== '/' && !str_ends_with($path, '/')) redirect($path . '/' . ($qs ? '?' . $qs : ''));

/* ---------- routes ---------- */
$seg = $p === '' ? [] : explode('/', $p);
$m = [];

switch (true) {
    case $p === '':
        require APP . '/routes/home.php'; break;

    case $p === 'homes-for-sale':
        require APP . '/routes/listings.php'; break;
    case count($seg) === 2 && $seg[0] === 'homes-for-sale':
        $slug = $seg[1];
        require APP . '/routes/listing.php'; break;

    case $p === 'neighborhoods':
        require APP . '/routes/neighborhoods.php'; break;
    case count($seg) === 2 && $seg[0] === 'neighborhoods':
        $slug = $seg[1];
        require APP . '/routes/neighborhood.php'; break;

    case $p === 'blog':
    case preg_match('#^blog/page/(\d+)$#', $p, $m) === 1:
        $page = (int) ($m[1] ?? 1); $category = null;
        require APP . '/routes/blog.php'; break;
    case preg_match('#^blog/category/([a-z0-9-]+)(?:/page/(\d+))?$#', $p, $m) === 1:
        $category = $m[1]; $page = (int) ($m[2] ?? 1);
        require APP . '/routes/blog.php'; break;
    case count($seg) === 2 && $seg[0] === 'blog':
        $slug = $seg[1];
        require APP . '/routes/post.php'; break;

    case in_array($p, ['buy-a-home-in-seattle', 'sell-your-home-seattle', 'about-seattle-northwest-homes',
                       'contact-seattle-real-estate-agents', 'privacy-policy', 'terms-of-use', 'thank-you'], true):
        require APP . '/routes/page.php'; break;

    case $p === 'submit':
        handle_submit(); break;
    case $p === 'sitemap.xml':
        require APP . '/routes/sitemap.php'; break;
    case $p === 'feed':
        require APP . '/routes/feed.php'; break;

    default:
        not_found();
}
