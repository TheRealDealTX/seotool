<?php
declare(strict_types=1);

defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)

function dispatch(string $path, string $method): void
{
    // Canonical scheme and host. Done here because the Hostinger platform
    // ignores .htaccess. Only applies to the production host names.
    $host = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
    $prodHost = (string) parse_url((string) config('base_url'), PHP_URL_HOST);
    if ($host === $prodHost || $host === 'www.' . $prodHost) {
        $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (is_https() ? 'https' : 'http')) === 'http';
        if ($insecure || $host !== $prodHost) {
            redirect(rtrim((string) config('base_url'), '/') . ($_SERVER['REQUEST_URI'] ?? '/'));
            return;
        }
    }

    // Collapse duplicate slashes and normalise /index.php to /
    $clean = (string) preg_replace('#/+#', '/', $path);
    if ($clean === '/index.php') {
        $clean = '/';
    }
    if ($clean !== $path) {
        redirect($clean);
        return;
    }

    if ($path === '/sitemap.xml') {
        render_sitemap();
        return;
    }

    if ($path === '/submit-estimate/' || $path === '/submit-estimate') {
        if ($method !== 'POST') {
            redirect('/contact/');
            return;
        }
        handle_estimate_submission();
        return;
    }

    if ($method !== 'GET' && $method !== 'HEAD') {
        http_response_code(405);
        header('Allow: GET, HEAD');
        render_not_found();
        return;
    }

    // Add trailing slash for known routes (e.g. /about -> /about/)
    if (!str_ends_with($path, '/') && resolve_route($path . '/') !== null) {
        redirect($path . '/' . (isset($_SERVER['QUERY_STRING']) && $_SERVER['QUERY_STRING'] !== '' ? '?' . $_SERVER['QUERY_STRING'] : ''));
        return;
    }

    $route = resolve_route($path);
    if ($route === null) {
        render_not_found();
        return;
    }
    render_page($route);
}

function redirect(string $to, int $status = 301): void
{
    header('Location: ' . $to, true, $status);
}

/** Map a path to a route array or null. */
function resolve_route(string $path): ?array
{
    $meta = page_meta();
    if (isset($meta[$path])) {
        return $meta[$path] + ['path' => $path];
    }
    if (preg_match('#^/services/([a-z0-9-]+)/$#', $path, $m) && ($s = service($m[1]))) {
        return [
            'template' => 'service', 'path' => $path, 'service' => $s,
            'title' => $s['title'], 'description' => $s['description'],
            'crumb' => $s['name'], 'parent' => '/services/', 'image' => $s['image'],
        ];
    }
    if (preg_match('#^/blog/([a-z0-9-]+)/$#', $path, $m) && ($a = article($m[1]))) {
        return [
            'template' => 'article', 'path' => $path, 'article' => $a,
            'title' => $a['seo_title'], 'description' => $a['description'],
            'crumb' => $a['title'], 'parent' => '/blog/', 'image' => $a['image'], 'og_type' => 'article',
        ];
    }
    return null;
}

/** Breadcrumb trail: list of [label, path]. */
function breadcrumb_trail(array $route): array
{
    if ($route['path'] === '/') {
        return [];
    }
    $trail = [['Home', '/']];
    if (!empty($route['parent'])) {
        $parent = page_meta()[$route['parent']] ?? null;
        $trail[] = [$parent['crumb'] ?? 'Back', $route['parent']];
    }
    $trail[] = [$route['crumb'] ?? $route['title'], $route['path']];
    return $trail;
}

function render_page(array $route, int $status = 200): void
{
    if (!empty($route['form'])) {
        ensure_session();
        header('Cache-Control: no-store, private');
    } else {
        header('Cache-Control: public, max-age=600');
    }
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');

    $page = $route;
    $page['breadcrumbs'] = breadcrumb_trail($route);
    $page['schema'] = page_schema($route, $page['breadcrumbs']);

    ob_start();
    require FR_APP . '/templates/pages/' . $route['template'] . '.php';
    $content = (string) ob_get_clean();

    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'HEAD') {
        return;
    }
    require FR_APP . '/templates/layout.php';
}

function render_not_found(): void
{
    render_page([
        'template' => '404', 'path' => request_path(), 'crumb' => 'Page not found',
        'title' => 'Page Not Found | Friendswood Roofers',
        'description' => 'The page you were looking for could not be found.',
        'noindex' => true, 'is_404' => true,
    ], http_response_code() === 405 ? 405 : 404);
}

/** All indexable URLs for the sitemap: path => lastmod (Y-m-d). */
function sitemap_entries(): array
{
    $launch = (string) config('launch_date');
    $entries = [];
    foreach (page_meta() as $path => $m) {
        if (empty($m['noindex'])) {
            $entries[$path] = $launch;
        }
    }
    foreach (array_keys(services()) as $slug) {
        $entries['/services/' . $slug . '/'] = $launch;
    }
    foreach (articles() as $a) {
        $entries[$a['url']] = $a['date'];
    }
    return $entries;
}

function render_sitemap(): void
{
    header('Content-Type: application/xml; charset=utf-8');
    header('Cache-Control: public, max-age=3600');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (sitemap_entries() as $path => $lastmod) {
        echo '  <url><loc>' . e(abs_url($path)) . '</loc><lastmod>' . e($lastmod) . '</lastmod></url>' . "\n";
    }
    echo '</urlset>' . "\n";
}
