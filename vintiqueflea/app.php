<?php
/**
 * Vintique Flea — front controller. Every request that isn't a real file lands here.
 */
declare(strict_types=1);

// Local preview (php -S … app.php): let the built-in server serve real static files.
if (PHP_SAPI === 'cli-server') {
    $f = __DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    if (is_file($f) && !str_ends_with($f, '.php') && !preg_match('~/(inc|data)/~', $f)) {
        return false;
    }
}

const ASSET_V = '20261119c';
define('INC', __DIR__ . '/inc');
define('DATA_DIR', __DIR__ . '/data');

require INC . '/config.php';
require INC . '/data.php';
require INC . '/photos.php';
require INC . '/amazon.php';
if (is_file(INC . '/asins.php')) {
    require INC . '/asins.php';
}
require INC . '/layout.php';
require INC . '/routes.php';

$GLOBALS['__schema'] = [];

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(parse_url($uri, PHP_URL_PATH) ?: '/');
$query = [];
parse_str((string) parse_url($uri, PHP_URL_QUERY), $query);

function redirect(string $to, int $code = 301): never
{
    header('Cache-Control: public, max-age=86400');
    header('Location: ' . $to, true, $code);
    exit;
}

function render(string $page, array $vars = [], int $status = 200): never
{
    http_response_code($status);
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'GET') {
        header('Cache-Control: public, max-age=300, s-maxage=300');
        header('X-LiteSpeed-Cache-Control: public,max-age=300');
    } else {
        header('Cache-Control: no-store');
        header('X-LiteSpeed-Cache-Control: no-cache');
    }
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    extract($vars, EXTR_SKIP);
    require INC . '/pages/' . $page . '.php';
    exit;
}

// --- Canonical host + scheme: www -> apex, http -> https (only when the proxy says the request was http) ---
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off' ? 'https' : ''));
if (PHP_SAPI !== 'cli-server' && ($host === 'www.vintiqueflea.com' || ($host === 'vintiqueflea.com' && $proto === 'http'))) {
    redirect(SITE_URL . $uri);
}

// --- Old WordPress query-string URLs (?p=123, ?replytocom=…, ?elementskit_template=…) ---
foreach (['p', 'page_id', 'cat', 'author', 'elementskit_template', 'replytocom', 'attachment_id', 'm', 'tag'] as $wpParam) {
    if (isset($query[$wpParam])) {
        redirect('/');
    }
}
if (isset($query['s']) && $path === '/') {
    redirect('/shop/');
}

// --- Legacy URL map: 301 to the rewritten URL, or 410 for removed content ---
$key = trim($path, '/');
if ($key === 'index.php' || $key === 'app.php') {
    redirect('/');
}
if (isset(LEGACY_REDIRECTS[$key])) {
    redirect(LEGACY_REDIRECTS[$key]);
}
if (in_array($key, LEGACY_GONE, true) || preg_match(LEGACY_GONE_PATTERN, $key)) {
    render('gone', [], 410);
}
// /some-old-post/feed/, /some-old-post/amp/, /page/2/ etc.
if (preg_match('~^(.+?)/(feed|amp|embed|trackback)$~', $key, $mm)) {
    redirect(isset(LEGACY_REDIRECTS[$mm[1]]) ? LEGACY_REDIRECTS[$mm[1]] : '/' . $mm[1] . '/');
}

// --- Web app manifest (served here so it gets the right MIME type on nginx) ---
if ($key === 'site.webmanifest') {
    header('Content-Type: application/manifest+json; charset=UTF-8');
    header('Cache-Control: public, max-age=86400');
    readfile(INC . '/site.webmanifest');
    exit;
}

// --- Canonical trailing slash for page URLs ---
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('~\.[a-z0-9]{2,5}$~i', $path)) {
    redirect($path . '/' . (($q = parse_url($uri, PHP_URL_QUERY)) ? '?' . $q : ''));
}

// --- Routes ---
$parts = $key === '' ? [] : explode('/', $key);

switch ($parts[0] ?? '') {
    case '':
        render('home');
    case 'sitemap.xml':
        require INC . '/sitemap.php';
        exit;
    case 'shop':
        if (count($parts) === 1) {
            render('shop');
        }
        if (count($parts) === 2 && isset(SHOP[$parts[1]])) {
            render('category', ['slug' => $parts[1], 'cat' => SHOP[$parts[1]]]);
        }
        break;
    case 'events':
        if (count($parts) === 1) {
            render('events');
        }
        if (count($parts) === 2 && isset(EDITIONS[$parts[1]])) {
            render('edition', ['slug' => $parts[1], 'ed' => EDITIONS[$parts[1]]]);
        }
        break;
    case 'play':
        if (count($parts) === 1) {
            render('play');
        }
        if (count($parts) === 2 && isset(GAMES[$parts[1]])) {
            render('game', ['slug' => $parts[1], 'game' => GAMES[$parts[1]]]);
        }
        break;
    case 'guides':
        $guides = load_guides();
        if (count($parts) === 1) {
            render('guides', ['guides' => $guides]);
        }
        if (count($parts) === 2 && isset($guides[$parts[1]])) {
            render('guide', ['slug' => $parts[1], 'g' => $guides[$parts[1]], 'guides' => $guides]);
        }
        break;
    case 'subscribe':
        if (count($parts) === 1) {
            require INC . '/forms.php';
            handle_subscribe();
        }
        break;
    default:
        if (count($parts) === 1 && isset(STATIC_PAGES[$parts[0]])) {
            render(STATIC_PAGES[$parts[0]]);
        }
}

render('404', [], 404);
