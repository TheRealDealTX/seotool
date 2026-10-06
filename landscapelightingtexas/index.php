<?php
// Landscape Lighting Texas — front controller.
//
// The host serves real files (assets, images) directly and sends every other
// request here. Routes come from inc/registry.php; anything unknown gets a
// real 404. Old WordPress-only URLs are 301'd to their nearest equivalent.
// Local preview: php -S localhost:8080 index.php (serves real files directly).
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH))) return false;

define('LLT', 1);
require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/registry.php';
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/components.php';
require __DIR__ . '/inc/feeds.php';
require __DIR__ . '/inc/widgets.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$path = preg_replace('#/{2,}#', '/', $path);
$qs   = $_SERVER['QUERY_STRING'] ?? '';

function redirect(string $to, int $code = 301): void {
    header('Location: ' . SITE_ORIGIN . $to, true, $code);
    exit;
}

// Canonical scheme and host (TLS terminates upstream, so trust X-Forwarded-Proto).
$host = strtolower($_SERVER['HTTP_HOST'] ?? SITE_HOST);
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? 'https') === 'http';
if (PHP_SAPI !== 'cli-server' && ($host === 'www.' . SITE_HOST || ($insecure && $host === SITE_HOST))) {
    redirect($uri);
}

// WordPress query-string URLs (?p=, ?page_id=, ?s=, ?feed=).
if ($path === '/' && $qs !== '') {
    parse_str($qs, $q);
    if (isset($q['s']))    redirect('/sitemap/');
    if (isset($q['feed'])) redirect('/feed/');
    if (isset($q['p']) || isset($q['page_id']) || isset($q['cat'])) redirect('/blog/');
}

// Feeds and XML sitemaps (the WordPress site published all of these).
switch ($path) {
    case '/feed/': case '/feed': render_rss(); exit;
    case '/sitemap.xml': case '/sitemap_index.xml': render_sitemap_index(); exit;
    case '/page-sitemap.xml':     render_sitemap('page'); exit;
    case '/post-sitemap.xml':     render_sitemap('post'); exit;
    case '/category-sitemap.xml': render_sitemap('category'); exit;
    case '/robots.txt': render_robots(); exit;
}

// Legacy WordPress paths.
$legacy = [
    '#^/(comments/feed|.+/feed)/?$#'                         => '/feed/',
    '#^/(wp-admin|wp-login\.php|xmlrpc\.php|wp-json|wp-includes)(/.*)?$#' => '/',
    '#^/author/.*$#'                                         => '/about-us/',
    '#^/(contact|contact-us)/?$#'                            => '/quote/',
    '#^/(blog/page/\d+|page/\d+)/?$#'                        => '/blog/',
    '#^/category/uncategorized/?$#'                          => '/category/general/',
    '#^/(reviews|testimonials)/?$#'                          => '/about-us/',
    '#^/(process|our-process)/?$#'                           => '/about-us/',
    '#^/(project-gallery|portfolio|our-work)/?$#'            => '/gallery/',
    '#^/(service-areas)/?$#'                                 => '/areas/',
    '#^/(terms|terms-of-use)/?$#'                            => '/terms-of-service/',
    '#^/(get-a-quote|free-quote|estimate)/?$#'               => '/quote/',
    '#^/(cost-calculator|calculator)/?$#'                    => '/landscape-lighting-cost-calculator/',
];
foreach ($legacy as $re => $to) {
    if ($to && preg_match($re, $path)) redirect($to);
}

// Trailing slash: /about-us -> /about-us/
if ($path !== '/' && substr($path, -1) !== '/' && isset($PAGES[$path . '/'])) {
    redirect($path . '/' . ($qs ? '?' . $qs : ''));
}

// Quote form submissions (from /quote/ or any page's embedded form).
if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST' && $path === '/quote/') {
    require __DIR__ . '/inc/quote-handler.php';
    exit;
}

if (isset($PAGES[$path])) {
    render_page($PAGES[$path]);
    exit;
}

http_response_code(404);
render_page([
    'path' => $path, 'file' => 'pages/404.php', 'type' => 'page',
    'title' => 'Page Not Found | Landscape Lighting Texas', 'h1' => 'This Path Is Unlit',
    'description' => 'The page you were looking for could not be found.', 'image' => null,
    'noindex' => true, 'modified' => BUILD_DATE,
]);
