<?php
// holybiblewords.com front controller. Every non-file request lands here
// (via .htaccess, or the host's own unknown-path fallback).
declare(strict_types=1);

require __DIR__ . '/lib/bible.php';
require __DIR__ . '/lib/layout.php';
require __DIR__ . '/lib/pages.php';
require __DIR__ . '/lib/api.php';
require __DIR__ . '/lib/sitemap.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$qs   = $_SERVER['QUERY_STRING'] ?? '';

function redirect(string $to, int $code = 301): never {
    header('Location: ' . $to, true, $code);
    exit;
}

function not_found(): never {
    http_response_code(404);
    render_page(page_404());
    exit;
}

// Canonical host and scheme. TLS terminates upstream, so trust X-Forwarded-Proto.
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
if ($host === 'www.holybiblewords.com' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http') {
    redirect(SITE_URL . $uri);
}

$vers = versions();
$verRe = implode('|', array_map('preg_quote', array_keys($vers)));

// ---- old WordPress URLs ----
if (isset($_GET['s'])) redirect('/search/?' . http_build_query(['q' => $_GET['s']]));
if (isset($_GET['feed']) || preg_match('#^/(feed|comments/feed)/?$#', $path)) redirect('/blog/');
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|author|category|tag)(/|$)#', $path)) {
    redirect(preg_match('#^/category/#', $path) ? '/blog/' : '/');
}
if (preg_match('#^/((ml|ta|post|page|category)-sitemap\d*|main-sitemap)\.(xml|xsl)$#', $path)) redirect('/sitemap_index.xml');
// Ang Biblia, 2011 (/ml/) is switched off until it is licensed: send its readers
// to the same place in Ang Pulong sa Dios, the other Cebuano version.
if (!isset($vers['ml']) && preg_match('#^/ml(/.*)?$#', $path, $m)) {
    $rest = preg_replace('#/(\d+)-\d+(?=/)#', '/$1', $m[1] ?? '/');
    redirect('/ceb' . ($rest === '' ? '/' : $rest));
}
// WordPress de-duplicated slugs: /ta/genesis/13-2/7-2/ -> /ta/genesis/13/7/
if (preg_match("#^/($verRe)/([a-z0-9]+)/(\d+)(?:-\d+)?/(?:(\d+)(?:-\d+)?/)?$#", $path, $m) && str_contains($path, '-')) {
    redirect(url_for($m[1], $m[2], (int)$m[3], isset($m[4]) && $m[4] !== '' ? (int)$m[4] : null));
}

// ---- normalisation ----
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('#\.[a-z0-9]+$#i', $path) && !str_starts_with($path, '/api/')) {
    redirect($path . '/' . ($qs !== '' ? "?$qs" : ''));
}
if (preg_match('#[A-Z]#', $path) && preg_match("#^/($verRe)/#i", $path)) redirect(strtolower($path));

// ---- routes ----
if ($path === '/' || $path === '/index.php') { render_page(page_home()); exit; }

if (str_starts_with($path, '/api/')) { api($path); exit; }

if (preg_match('#^/([a-z0-9_\-]+\.xml)$#', $path, $m) && sitemap($m[1])) exit;

if (preg_match("#^/($verRe)/(?:([a-z0-9]+)/(?:(\d+)/(?:(\d+)/)?)?)?$#", $path, $m)) {
    $ver = $m[1];
    $slug = $m[2] ?? '';
    if ($slug === '') { render_page(page_version($ver)); exit; }
    if (!isset(books()[$slug])) {
        $found = find_book($slug);
        if ($found) redirect(url_for($ver, $found, isset($m[3]) ? (int)$m[3] : null, isset($m[4]) ? (int)$m[4] : null));
        not_found();
    }
    $book = books()[$slug];
    if (empty($m[3])) { render_page(page_book($ver, $slug)); exit; }
    $c = (int)$m[3];
    if ($c < 1 || $c > count($book['verses'])) not_found();
    if (empty($m[4])) { render_page(page_chapter($ver, $slug, $c)); exit; }
    $v = (int)$m[4];
    if ($v < 1 || $v > $book['verses'][$c - 1]) not_found();
    // a verse this translation joins with the previous one -> the start of that range
    if (verse_text($ver, $slug, $c, $v) === '') redirect(url_for($ver, $slug, $c, verse_display($ver, $slug, $c, $v)['n']));
    render_page(page_verse($ver, $slug, $c, $v));
    exit;
}

switch ($path) {
    case '/search/':
        $q = trim((string)($_GET['q'] ?? ''));
        $ver = isset($vers[$_GET['v'] ?? '']) ? $_GET['v'] : 'ta';
        // a reference goes straight to the passage
        if ($q !== '' && empty($_GET['page']) && ($ref = parse_ref($q))) redirect(url_for($ver, $ref[0], $ref[1], $ref[2]), 302);
        $t = in_array($_GET['t'] ?? '', ['ot', 'nt'], true) ? $_GET['t'] : '';
        render_page(page_search(mb_substr($q, 0, 200), $ver, $t, max(1, (int)($_GET['page'] ?? 1))));
        exit;
    case '/verse-of-the-day/':
        render_page(page_votd(isset($vers[$_GET['v'] ?? '']) ? $_GET['v'] : 'ta'));
        exit;
    case '/plan/':   render_page(page_plan()); exit;
    case '/saved/':  render_page(page_saved()); exit;
    case '/app/':    render_page(page_app()); exit;
    case '/offline/': render_page(page_offline()); exit;
    case '/blog/':   render_page(page_blog_index()); exit;
    case '/privacy-policy/': render_page(page_static('privacy-policy')); exit;
}

if (preg_match('#^/blog/([a-z0-9\-]+)/$#', $path, $m) && isset(blog_posts()[$m[1]])) {
    render_page(page_blog_post(blog_posts()[$m[1]]));
    exit;
}

not_found();
