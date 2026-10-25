<?php
// php -S router emulating the .htaccess essentials for local testing.
$root = $_SERVER['DOCUMENT_ROOT'];
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($path === '/wp-admin/admin-ajax.php') { require $root . $path; return true; }
if (str_starts_with($path, '/ce-private')) { http_response_code(404); readfile($root . '/404.html'); return true; }
if ($path === '/' && preg_match('/(^|&)(p|page_id|cat|s|author)=/', $_SERVER['QUERY_STRING'] ?? '')) { require $root . '/ce-router.php'; return true; }
$file = $root . $path;
if (is_file($file)) { return false; }
if (is_dir($file) && substr($path, -1) !== '/') { header('Location: ' . $path . '/', true, 301); return true; }
foreach (['index.html', 'index.xml'] as $idx) { if (is_file($file . $idx)) { if ($idx === 'index.xml') header('Content-Type: application/rss+xml'); readfile($file . $idx); return true; } }
http_response_code(404); readfile($root . '/404.html'); return true;
