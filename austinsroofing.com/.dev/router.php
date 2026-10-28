<?php
// Local preview router for `php -S` (emulates the production .htaccess:
// directory index, trailing-slash redirect, sitemap rewrites, 404 page).
// Usage: php -S 127.0.0.1:8080 -t austinsroofing.com austinsroofing.com/.dev/router.php
$root = dirname(__DIR__);
$path = urldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$map = ['/sitemap_index.xml' => 'index', '/sitemap.xml' => 'index', '/wp-sitemap.xml' => 'index',
        '/page-sitemap.xml' => 'page', '/post-sitemap.xml' => 'post', '/category-sitemap.xml' => 'category'];
if (isset($map[$path])) { $_GET['type'] = $map[$path]; require $root . '/sitemap-xml.php'; return true; }
if (str_starts_with($path, '/includes/') || str_starts_with($path, '/.dev/')) { http_response_code(403); return true; }
$f = $root . $path;
if (is_dir($f)) {
    if (substr($path, -1) !== '/') { header('Location: ' . $path . '/', true, 301); return true; }
    if (is_file($f . 'index.php')) { $_SERVER['SCRIPT_NAME'] = $path . 'index.php'; chdir($f); require $f . 'index.php'; return true; }
}
if (is_file($f)) { if (str_ends_with($f, '.php')) { require $f; return true; } return false; }
http_response_code(404); require $root . '/404.php'; return true;
