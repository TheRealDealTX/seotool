<?php
// Local preview: php -S 127.0.0.1:8080 -t site scripts/dev-router.php
// Mirrors the host: real files are served as-is, everything else goes to index.php.
$f = __DIR__ . '/../site' . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (is_file($f) && !str_ends_with($f, 'index.php')) {
    if (str_ends_with($f, '.php')) { require $f; return true; }
    return false;
}
require __DIR__ . '/../site/index.php';
