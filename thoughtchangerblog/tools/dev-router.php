<?php
// Local preview: php -S localhost:8080 -t public tools/dev-router.php  (mimics the .htaccess rules)
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if (preg_match('#^/(app|content)(/|$)#', $path)) { http_response_code(404); exit; }
if ($path !== '/' && is_file($_SERVER['DOCUMENT_ROOT'] . $path)) return false;
require $_SERVER['DOCUMENT_ROOT'] . '/index.php';
