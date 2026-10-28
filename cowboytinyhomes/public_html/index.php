<?php
// Cowboy Tiny Homes — front controller. .htaccess sends every request that is
// not a real file here; PAGES (inc/pages.php) maps clean URLs to templates.
declare(strict_types=1);

require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/pages.php';
require __DIR__ . '/inc/layout.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$qs   = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';

function redirect(string $to, int $code = 301): void
{
    header('Location: ' . SITE_URL . $to, true, $code);
    exit;
}

// Collapse duplicate slashes and strip index.php so every page has one URL.
$clean = preg_replace('#/+#', '/', $path);
$clean = preg_replace('#/index\.php$#', '/', $clean);
if ($clean !== $path) redirect($clean . $qs);

if (isset(REDIRECTS[$path])) redirect(REDIRECTS[$path]);
if (!str_ends_with($path, '/') && isset(REDIRECTS[$path . '/'])) redirect(REDIRECTS[$path . '/']);

// Old WordPress media URLs (incl. resized copies like name-300x200.webp) => the same image in /assets/img/.
if (preg_match('#^/wp-content/uploads/\d{4}/\d{2}/(?:cropped-)?([\w-]+?)(?:-\d+x\d+)?\.(webp|jpe?g|png)$#i', $path, $mm)
    && is_file(__DIR__ . '/assets/img/' . $mm[1] . '.' . $mm[2])) {
    redirect('/assets/img/' . $mm[1] . '.' . $mm[2]);
}

// Old WordPress single-design URLs, admin and feeds.
if (preg_match('#^/category/#', $path)) redirect('/home-designs/');
if (preg_match('#^/(wp-admin|wp-login\.php|wp-json|xmlrpc\.php|wp-includes)(/|$)#', $path)) redirect('/');
if (preg_match('#/feed/?$#', $path)) redirect('/guides/');

if ($path === '/sitemap.xml') {
    header('Content-Type: application/xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (PAGES as $p => $m) {
        echo '  <url><loc>' . e(abs_url($p)) . '</loc><lastmod>' . ($m['updated'] ?? '2026-10-28')
           . '</lastmod><priority>' . $m['priority'] . "</priority></url>\n";
    }
    echo "</urlset>\n";
    exit;
}

// Missing trailing slash on a real page.
if (!str_ends_with($path, '/') && isset(PAGES[$path . '/'])) redirect($path . '/' . $qs);

$GLOBALS['path'] = $path;
$meta = PAGES[$path] ?? null;
$status = 200;
if (!$meta) {
    $status = 404;
    $GLOBALS['path'] = $path = '/404/';
    $meta = ['file' => '404', 'type' => 'page', 'crumb' => 'Page Not Found', 'image' => 'og-cowboy-tiny-homes.jpg',
             'title' => 'Page Not Found | ' . SITE_NAME, 'desc' => 'The page you were looking for could not be found.'];
}
$GLOBALS['page'] = $meta;

ob_start();
require __DIR__ . '/pages/' . $meta['file'] . '.php';
$content = ob_get_clean();

render_page($path, $meta, $content, $status);
