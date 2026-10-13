<?php
// Dev router emulating the production .htaccess.
$root = $_SERVER['DOCUMENT_ROOT'];
$uri = urldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if (preg_match('#^/(sitemap_index|page-sitemap|post-sitemap|category-sitemap)\.xml$#', $uri, $m)) { $_GET['map'] = $m[1]; require $root . '/sitemap.php'; return true; }
if (preg_match('#^/(inc|content)(/|$)#', $uri)) { http_response_code(403); echo 'Forbidden'; return true; }
$f = $root . $uri;
if (is_file($f)) { if (substr($f, -4) === '.php') { require $f; return true; } return false; }
if (is_dir($f)) {
  if (substr($uri, -1) !== '/') { header('Location: ' . $uri . '/', true, 301); return true; }
  if (is_file($f . 'index.php')) { $_SERVER['SCRIPT_NAME'] = $uri . 'index.php'; chdir($f); require $f . 'index.php'; return true; }
}
require $root . '/404.php'; return true;
