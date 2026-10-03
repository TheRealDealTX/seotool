<?php
/**
 * Front controller. .htaccess sends every request that is not a real file here.
 */

declare(strict_types=1);

require __DIR__ . '/includes/bootstrap.php';

$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode((string) parse_url($uri, PHP_URL_PATH));
$path = '/' . ltrim(preg_replace('#/+#', '/', $path), '/');
$query = (string) parse_url($uri, PHP_URL_QUERY);

function redirect_to(string $to, int $code = 301): void
{
    header('Location: ' . $to, true, $code);
    exit;
}

// Paths that should never reach the app (old WordPress internals, probes).
if (preg_match('#^/(wp-admin|wp-login\.php|xmlrpc\.php|wp-json|wp-includes|wp-cron\.php)#i', $path)) {
    http_response_code(410);
    header('X-Robots-Tag: noindex');
    exit('Gone');
}

$redirects = require __DIR__ . '/includes/redirects.php';

// WordPress shortlinks: /?p=123, /?page_id=22
if ($path === '/' && $query !== '') {
    parse_str($query, $q);
    foreach (['p', 'page_id'] as $k) {
        if (isset($q[$k]) && ctype_digit((string) $q[$k]) && isset($redirects['ids'][(int) $q[$k]])) {
            redirect_to($redirects['ids'][(int) $q[$k]]);
        }
    }
}

// Machine-readable routes.
switch ($path) {
    case '/sitemap.xml':
        require __DIR__ . '/includes/sitemap.php';
        output_sitemap();
        exit;
    case '/feed/':
    case '/feed':
    case '/rss/':
        require __DIR__ . '/includes/sitemap.php';
        output_feed();
        exit;
}

if (isset($redirects['paths'][$path])) {
    redirect_to($redirects['paths'][$path]);
}
if (isset($redirects['paths'][$path . '/'])) {
    redirect_to($redirects['paths'][$path . '/']);
}

// Old WordPress pagination & feeds: /blog/page/2/ -> /blog/?pg=2, /slug/feed/ -> /slug/
if (preg_match('#^/blog/page/(\d+)/?$#', $path, $m)) {
    redirect_to('/blog/' . ((int) $m[1] > 1 ? '?pg=' . (int) $m[1] : ''));
}
if (preg_match('#^/(page|category/[a-z0-9-]+/page)/(\d+)/?$#', $path)) {
    redirect_to('/blog/');
}
if (preg_match('#^/([a-z0-9-]+)/(feed|amp|embed)/?$#', $path, $m) && find_content('/' . $m[1] . '/')) {
    redirect_to('/' . $m[1] . '/');
}

// Enforce lowercase + trailing slash on page URLs (matches original permalinks).
if (!preg_match('#\.[a-z0-9]{2,5}$#i', $path)) {
    $canon = strtolower($path);
    if (substr($canon, -1) !== '/') {
        $canon .= '/';
    }
    if ($canon !== $path && find_content($canon)) {
        redirect_to($canon . ($query !== '' ? '?' . $query : ''));
    }
}

$page = find_content($path);
if ($page && empty($page['draft'])) {
    render_page($page);
    exit;
}

render_404();
