<?php
// Clean-URL router. This host is nginx and ignores .htaccess: real files
// (style.css, blog/) are served directly and every other path lands here -
// but only while no root index.html exists (the platform would answer every
// unknown path with it), so the homepage is home.html. Pages live in _pages/
// as guarded PHP so the old .html URLs no longer exist and can be 301'd:
//   /about -> _pages/about.php    /about.html, /about/ -> 301 /about
//   anything else -> 404.html with a real 404 status.
define('ROUTER', 1);
$root = __DIR__;
$path = rawurldecode(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/');
$qs = isset($_SERVER['QUERY_STRING']) && $_SERVER['QUERY_STRING'] !== '' ? '?' . $_SERVER['QUERY_STRING'] : '';

function send($html, $code = 200) {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: public, max-age=3600');
    echo $html;
    exit;
}
function page($name) {
    ob_start();
    include __DIR__ . "/_pages/$name.php";
    send(ob_get_clean());
}
function redirect($to) { header('Location: ' . $to, true, 301); exit; }
function page_exists($name) {
    return $name !== '' && preg_match('#^[A-Za-z0-9][A-Za-z0-9/_-]*$#', $name) && is_file(__DIR__ . "/_pages/$name.php");
}

if ($path === '/') send(file_get_contents("$root/home.html"));
if (in_array($path, ['/index.php', '/index.html', '/index', '/home.html', '/home'], true)) redirect("/$qs");
if (strpos($path, '..') === false) {
    $name = trim($path, '/');
    if (substr($name, -5) === '.html') {
        $name = substr($name, 0, -5);
        if (page_exists($name)) redirect("/$name$qs");
    } elseif (page_exists($name)) {
        if ($path !== "/$name") redirect("/$name$qs");
        page($name);
    }
}
// The 404 page uses relative links; pin them to the site root.
send(preg_replace('/<head>/i', '<head><base href="/">', file_get_contents("$root/404.html"), 1), 404);
