<?php
// Front controller for militaryhousingrentals.com. Every request that is not a
// real file is routed here by .htaccess.
require __DIR__ . '/app/lib.php';

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$path = '/' . ltrim(rawurldecode($path), '/');

// Legacy WordPress query links: /?p=123, /?page_id=123, /?s=term
if ($path === '/' && isset($_GET['p'], cfg('legacy_ids')[(int)$_GET['p']])) redirect(cfg('legacy_ids')[(int)$_GET['p']]);
if ($path === '/' && isset($_GET['page_id'], cfg('legacy_ids')[(int)$_GET['page_id']])) redirect(cfg('legacy_ids')[(int)$_GET['page_id']]);
if ($path === '/' && isset($_GET['s'])) { require APP . '/views/search.php'; exit; }

// Exact-match routes
$xml = [
    '/sitemap_index.xml' => 'index', '/post-sitemap.xml' => 'post', '/page-sitemap.xml' => 'page',
    '/properties-sitemap.xml' => 'properties', '/bases-sitemap.xml' => 'bases', '/category-sitemap.xml' => 'category',
];
if (isset($xml[$path])) { $sitemap = $xml[$path]; require APP . '/views/sitemap.php'; exit; }
if ($path === '/sitemap.xml' || $path === '/wp-sitemap.xml') redirect('/sitemap_index.xml');
if ($path === '/llms.txt') { require APP . '/views/llms.php'; exit; }
if (in_array($path, ['/feed/', '/feed', '/rss/', '/blog/feed/'], true)) { require APP . '/views/feed.php'; exit; }

// WordPress-style trailing slash
if (!str_ends_with($path, '/') && !preg_match('/\.[a-z0-9]{2,5}$/i', $path)) {
    $qs = $_SERVER['QUERY_STRING'] ?? '';
    redirect($path . '/' . ($qs !== '' ? '?' . $qs : ''));
}

$routes = [
    '/'                  => 'home',
    '/properties/'       => 'properties',
    '/marine-bases/'     => 'bases',
    '/blog/'             => 'blog',
    '/category/blog/'    => 'blog', // canonical points at /blog/
    '/contact-us/'       => 'contact',
    '/submit-property/'  => 'submit',
    '/privacy-policy/'   => 'legal',
    '/terms-of-use/'     => 'legal',
];
$aliases = [
    '/home/' => '/', '/bases/' => '/marine-bases/', '/military-bases/' => '/marine-bases/',
    '/author/militaryhousing/' => '/blog/', '/comments/feed/' => '/feed/',
    '/contact/' => '/contact-us/', '/listings/' => '/properties/', '/bases/fort-hood/' => '/bases/fort-cavazos/',
    '/bases/fort-liberty/' => '/bases/fort-bragg/', '/bases/fort-moore/' => '/bases/fort-benning/',
];
if (isset($aliases[$path])) redirect($aliases[$path]);
if (preg_match('#^/(blog|category/blog)/page/\d+/$#', $path)) redirect('/blog/');

if (isset($routes[$path])) { require APP . '/views/' . $routes[$path] . '.php'; exit; }

if (preg_match('#^/properties/([a-z0-9-]+)/$#', $path, $m)) {
    $listing = listing($m[1]) ?? not_found();
    require APP . '/views/property.php'; exit;
}
if (preg_match('#^/bases/([a-z0-9-]+)/$#', $path, $m)) {
    $slug = $m[1];
    if ($slug !== 'featured' && !base($slug)) not_found();
    require APP . '/views/base.php'; exit;
}
if (preg_match('#^/([a-z0-9-]+)/$#', $path, $m) && ($post = post($m[1]))) {
    require APP . '/views/post.php'; exit;
}
// /what-is-base-housing/amp/ and similar WordPress endpoints
if (preg_match('#^/([a-z0-9-]+)/(amp|feed|embed)/$#', $path, $m) && post($m[1])) redirect('/' . $m[1] . '/');
if (preg_match('#^/properties/([a-z0-9-]+)/(feed|embed)/$#', $path, $m) && listing($m[1])) redirect('/properties/' . $m[1] . '/');

not_found();
