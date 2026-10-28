<?php
$root = __DIR__;  // local preview router for php -S
$p = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if ($p !== '/' && is_file($root . $p) && !str_ends_with($p, '.php')) return false;
chdir($root);
require $root . '/index.php';
