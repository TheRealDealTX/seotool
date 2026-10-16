<?php
// Local preview only: php -S 127.0.0.1:8099 -t . router.php
// Mimics the host: existing files are served as-is, everything else goes to index.php.
$root = $_SERVER['DOCUMENT_ROOT'];
$p = rawurldecode(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
if ($p !== '/' && is_file($root.$p)) return false;
require $root.'/index.php';
