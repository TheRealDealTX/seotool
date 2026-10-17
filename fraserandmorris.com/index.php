<?php
// fraserandmorris.com - front controller and router.
//
// The host serves existing files directly and ignores .htaccess, so every page
// lives in _pages/ as a guarded PHP file and is served from here. That lets this
// one script enforce https + the bare domain (301), send proper status codes and
// cache headers, and redirect legacy URLs. See README, "Hosting".
define('FM_PAGE', 1);
$canonicalHost = 'fraserandmorris.com';
$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$query = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';   // TLS ends upstream

function redirect($to) {
    header('Location: ' . $to, true, 301);
    header('Cache-Control: public, max-age=86400');
    exit;
}

// 1. One canonical origin: https://fraserandmorris.com
if ($host === 'www.' . $canonicalHost || ($host === $canonicalHost && $insecure)) {
    redirect('https://' . $canonicalHost . $uri);
}
$production = $host === $canonicalHost;
$base = $production ? 'https://' . $canonicalHost : 'https://' . ($host ?: $canonicalHost);
if (!$production) {
    header('X-Robots-Tag: noindex, nofollow');   // preview / temporary domains
}

function serve($file, $status = 200) {
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: ' . ($status === 200 ? 'public, max-age=600' : 'no-cache'));
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('X-Frame-Options: SAMEORIGIN');
    include $file;
    exit;
}

$pages = __DIR__ . '/_pages';

// 2. Legacy and alias URLs.
$redirects = [
    '/index.php' => '/',
    '/index.html' => '/',
    '/index.htm' => '/',
    '/home.html' => '/',
    '/gardens/index.html' => '/gardens.html',
    '/gardens/' => '/gardens.html',
    '/gardens' => '/gardens.html',
    '/blog' => '/blog/',
    '/blog/index.html' => '/blog/',
    '/journal' => '/blog/',
    '/news' => '/blog/',
    '/news.html' => '/blog/',
    '/press.html' => '/about.html',
    '/pdfs/GardensIllustrated.pdf' => '/gardens/artists.html',
];
if (isset($redirects[$path])) {
    redirect($base . $redirects[$path] . ($path === '/index.php' ? '' : $query));
}

// 3. Pages.
if (preg_match('#^/[A-Za-z0-9/_.-]*$#', $path) && strpos($path, '..') === false && strpos($path, '/_') === false) {
    $file = substr($path, -1) === '/' ? $pages . $path . 'index.html.php' : $pages . $path . '.php';
    if (is_file($file)) {
        serve($file);
    }
    // /gardens/fox -> /gardens/fox.html ; /blog -> /blog/
    if (pathinfo($path, PATHINFO_EXTENSION) === '' && substr($path, -1) !== '/') {
        if (is_file($pages . $path . '.html.php')) redirect($base . $path . '.html' . $query);
        if (is_file($pages . $path . '/index.html.php')) redirect($base . $path . '/' . $query);
    }
    // Case-insensitive match for old mixed-case links.
    $lower = strtolower($path);
    if ($lower !== $path) {
        $f = substr($lower, -1) === '/' ? $pages . $lower . 'index.html.php' : $pages . $lower . '.php';
        if (is_file($f)) redirect($base . $lower . $query);
    }
}
if (preg_match('#^/pdfs/#i', $path)) {
    redirect($base . '/about.html');
}

// 4. Everything else: a real 404.
serve($pages . '/404.html.php', 404);
