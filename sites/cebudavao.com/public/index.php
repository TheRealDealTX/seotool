<?php
// cebudavao.com front controller. The platform serves existing files directly
// and sends "/" plus every unknown path here (it ignores .htaccess).
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$home = 'https://cebudavao.com';

function go($to, $code = 301) {
    global $home;
    header('Location: ' . (str_starts_with($to, 'http') ? $to : $home . $to), true, $code);
    header('Cache-Control: public, max-age=86400');
    exit;
}

// 1. Canonical host + scheme (TLS terminates upstream).
$host = strtolower($_SERVER['HTTP_HOST'] ?? 'cebudavao.com');
if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.cebudavao.com') {
    go($uri);
}

// 2. Homepage. Old WordPress query-string URLs (?p=123, ?page_id=…) land here too.
if ($path === '/' || $path === '/index.php') {
    if (isset($_GET['s']) && $_GET['s'] !== '') go('/search/?q=' . rawurlencode($_GET['s']));
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/home.html');
    exit;
}

// 3. RSS feed (old WordPress feed URL kept).
if (preg_match('#^/feed/?$#', $path)) {
    header('Content-Type: application/rss+xml; charset=utf-8');
    readfile(__DIR__ . '/feed.xml');
    exit;
}

// 4. Legacy 301 map (generated from the Semrush export + editorial decisions).
$map = require __DIR__ . '/redirects.php';
$try = [$path, rtrim($path, '/') . '/'];
foreach ($try as $p) { if (isset($map[$p])) go($map[$p]); }

// 5. Pattern rules for old WordPress archives.
$p = rtrim($path, '/') . '/';
if (preg_match('#^(.*)/amp/$#', $p, $m) || preg_match('#^(.*/[^/]+)/\d+/$#', $p, $m)) {
    $base = $m[1] . '/';
    if (isset($map[$base])) go($map[$base]);
    if (is_dir(__DIR__ . $base) && is_file(__DIR__ . $base . 'index.html')) go($base);
}
if (preg_match('#^/(wp-sitemap.*\.xml|sitemap_index\.xml|post-sitemap\.xml|page-sitemap\.xml)$#', $path)) go('/sitemap.xml');
if (preg_match('#^/(feed|comments/feed|category/[^/]+/feed|[^/]+/feed)/?$#', $path)) go('/feed/');
if (preg_match('#^/category/([^/]+)/page/\d+/?$#', $path, $m)) {
    $cat = '/category/' . $m[1] . '/';
    if (isset($map[$cat])) go($map[$cat]);
    if (is_file(__DIR__ . $cat . 'index.html')) go($cat);
}
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|tag|author|page|20\d\d|uncategorized)(/|$)#', $path)) go('/');
if (preg_match('#^/wp-content/#', $path)) go('/');

// 6. Directory without trailing slash.
if (substr($path, -1) !== '/' && is_file(__DIR__ . $path . '/index.html')) go($path . '/');

// 7. Any other URL under a 2017-era section (not in the export) -> homepage, per the brief.
$sections = require __DIR__ . '/sections.php';
$seg = explode('/', trim($path, '/'))[0] ?? '';
$retired = ['politics','public-opinions','viral-news','whats-new','essays','opinions','personal','religion','world-news',
            'exams','lotto-results','pcso-lotto-results','videos','arts','auto','web-development','april-fools-post',
            'restaurants-2','resorts','beach-resorts','photo-albums','guitars','history','services','business','word-meanings',
            'fun-quizzes','festivals','events','hotels','beach','movies','music','technology','finance','real-estate','jobs',
            'health','books','culture','entertainment','food','travel','news','sports'];
if ($seg !== '' && in_array($seg, $retired, true)) {
    if (trim($path, '/') === $seg && isset($sections[$seg])) go($sections[$seg]);
    go('/');
}

// 8. Real 404.
http_response_code(404);
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/404.html');
