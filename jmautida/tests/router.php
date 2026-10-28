<?php
// Local preview: php -S localhost:8080 -t jmautida/public jmautida/tests/router.php
// Mirrors the clean-URL rewrites in public/.htaccess.
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$root = $_SERVER['DOCUMENT_ROOT'];
if (preg_match('~^/api/(lib|mailer|config[^/]*)\.php$~', $path)) { http_response_code(403); exit; }
if ($path === '/') { readfile("$root/index.html"); return true; }
if (preg_match('~^/tools/([a-z-]+)$~', $path, $m) && is_file("$root/pages/{$m[1]}.html")) { header('Content-Type: text/html; charset=utf-8'); readfile("$root/pages/{$m[1]}.html"); return true; }
if (preg_match('~^/(tools|about|contact|privacy)$~', $path, $m)) { header('Content-Type: text/html; charset=utf-8'); readfile("$root/{$m[1]}.html"); return true; }
if (is_file($root . $path)) {
    if (str_ends_with($path, '.webmanifest')) { header('Content-Type: application/manifest+json'); readfile($root . $path); return true; }
    return false;
}
http_response_code(404); header('Content-Type: text/html; charset=utf-8'); readfile("$root/404.html");
