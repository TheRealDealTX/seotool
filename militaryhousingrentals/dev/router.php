<?php
// php -S router emulating public_html/.htaccess (local testing only).
$root = $_SERVER['DOCUMENT_ROOT'];
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if (preg_match('#^/app(/|$)#', $path) || preg_match('#(^|/)\.(?!well-known)#', $path)) { http_response_code(403); echo 'Forbidden'; return true; }
if (preg_match('#^/wp-content/uploads/owners/.*\.(php\d?|phtml|phar|html?|svg|js)$#i', $path)) { http_response_code(403); echo 'Forbidden'; return true; }
if ($path !== '/' && is_file($root . $path) && !preg_match('/\.php$/', $path)) return false;
$_SERVER['SCRIPT_NAME'] = '/site.php';
require $root . '/site.php';
