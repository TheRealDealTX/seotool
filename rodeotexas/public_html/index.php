<?php
/**
 * Public front controller. Every public URL that is not a static file is
 * routed here by .htaccess. Page templates live in /pages and all share the
 * includes in /includes (head, header, footer, scripts).
 */
declare(strict_types=1);

define('RT_PUBLIC', __DIR__);
require dirname(__DIR__) . '/app/bootstrap.php';

use RT\Db;

security_headers();

$path = request_path();
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
if (!in_array($method, ['GET', 'HEAD', 'POST'], true)) {
    http_response_code(405);
    header('Allow: GET, HEAD, POST');
    exit;
}

// Clean paths: collapse slashes, add the trailing slash to page URLs.
if (str_contains($path, '//')) {
    redirect(preg_replace('#/+#', '/', $path) . (isset($_SERVER['QUERY_STRING']) && $_SERVER['QUERY_STRING'] !== '' ? '?' . $_SERVER['QUERY_STRING'] : ''), 301);
}
$lastSeg = basename($path);
if ($path !== '/' && !str_ends_with($path, '/') && !str_contains($lastSeg, '.')) {
    $qsTail = ($_SERVER['QUERY_STRING'] ?? '') !== '' ? '?' . $_SERVER['QUERY_STRING'] : '';
    redirect($path . '/' . $qsTail, 301);
}

/** Render a page template from /pages with the given variables. */
function rt_page(string $name, array $vars = []): void
{
    extract($vars, EXTR_SKIP);
    require RT_PUBLIC . '/pages/' . $name . '.php';
    exit;
}

function rt_not_found(): void
{
    // Before giving up, honour the redirect table (old WordPress URLs etc.).
    $p = request_path();
    $row = Db::one('SELECT id, to_path, code FROM redirects WHERE from_path IN (?, ?) LIMIT 1', [$p, rtrim($p, '/')]);
    if ($row) {
        Db::q('UPDATE redirects SET hits = hits + 1 WHERE id = ?', [$row['id']]);
        redirect($row['to_path'], in_array((int) $row['code'], [301, 302, 307, 308], true) ? (int) $row['code'] : 301);
    }
    http_response_code(404);
    rt_page('404');
}

$m = [];
try {
    switch (true) {
        case $path === '/':
            rt_page('home');
        case $path === '/rodeos/':
            rt_page('directory', ['mode' => 'upcoming']);
        case $path === '/past-events/':
            rt_page('directory', ['mode' => 'past']);
        case (bool) preg_match('#^/rodeos/(region|association|type|level)/([a-z0-9_-]+)/$#', $path, $m):
            rt_page('directory', ['mode' => 'upcoming', 'preset' => [$m[1], $m[2]]]);
        case (bool) preg_match('#^/rodeos/([a-z0-9-]+)/calendar\.ics$#', $path, $m):
            rt_page('ics', ['slug' => $m[1]]);
        case (bool) preg_match('#^/rodeos/([a-z0-9-]+)/report/$#', $path, $m):
            rt_page('correction', ['slug' => $m[1]]);
        case (bool) preg_match('#^/rodeos/([a-z0-9-]+)/$#', $path, $m):
            rt_page('event', ['slug' => $m[1]]);
        case $path === '/submit-event/':
            rt_page('submit');
        case $path === '/favorites/':
            rt_page('favorites');
        case $path === '/contact/':
            rt_page('contact');
        case $path === '/about/':
            rt_page('about');
        case $path === '/privacy-policy/':
            rt_page('privacy');
        case $path === '/api/events/':
        case $path === '/api/events.json':
            rt_page('api-events');
        case $path === '/sitemap.xml':
        case (bool) preg_match('#^/sitemap-(pages|events|articles)\.xml$#', $path, $m):
            rt_page('sitemap', ['part' => $m[1] ?? 'index']);
        case (bool) preg_match('#^/blog/(?:page/(\d+)/)?$#', $path, $m):
            rt_page('blog', ['pageNo' => (int) ($m[1] ?? 1)]);
        case (bool) preg_match('#^/category/([a-z0-9-]+)/(?:page/(\d+)/)?$#', $path, $m):
            rt_page('blog', ['category' => $m[1], 'pageNo' => (int) ($m[2] ?? 1)]);
        case (bool) preg_match('#^/([a-z0-9-]+)/$#', $path, $m):
            $article = Db::one("SELECT * FROM articles WHERE slug = ? AND status = 'published'", [$m[1]]);
            if ($article) {
                rt_page('article', ['article' => $article]);
            }
            rt_not_found();
        default:
            rt_not_found();
    }
} catch (\Throwable $e) {
    app_log('php-error', $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    if (cfg('debug')) {
        throw $e;
    }
    http_response_code(500);
    if (!headers_sent()) {
        header('Content-Type: text/html; charset=utf-8');
    }
    echo '<!doctype html><meta charset="utf-8"><title>Temporarily unavailable</title><p style="font-family:sans-serif;padding:2rem">Sorry — something went wrong on our side. Please try again in a minute.</p>';
}
