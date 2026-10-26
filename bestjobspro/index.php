<?php
// Front controller: every request that is not a real file lands here (see .htaccess).

declare(strict_types=1);

// Local preview (php -S localhost:8000 index.php): let the dev server serve real files.
if (PHP_SAPI === 'cli-server' && is_file(__DIR__ . parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH))) {
    return false;
}

require __DIR__ . '/inc/config.php';
require __DIR__ . '/inc/layout.php';
require __DIR__ . '/inc/posts.php';
require __DIR__ . '/inc/tools.php';
require __DIR__ . '/inc/forms.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(parse_url($uri, PHP_URL_PATH) ?: '/');
$qs   = parse_url($uri, PHP_URL_QUERY);

function redirect(string $to, int $code = 301): never
{
    header('Location: ' . (str_starts_with($to, 'http') ? $to : SITE_URL . $to), true, $code);
    exit;
}

// Canonical scheme and host. Hostinger terminates TLS at its proxy, so trust the forwarded header too.
// Only redirect on positive evidence of plain http, so a proxy that hides the scheme can't cause a loop.
$xfp      = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '');
$insecure = $xfp === 'http' || ($xfp === '' && ($_SERVER['HTTPS'] ?? '') !== 'on' && ($_SERVER['SERVER_PORT'] ?? '') === '80');
$host     = strtolower($_SERVER['HTTP_HOST'] ?? 'bestjobspro.com');
if (PHP_SAPI !== 'cli-server' && ($insecure || $host === 'www.bestjobspro.com')) {
    redirect(SITE_URL . $uri);
}

if (isset(REDIRECTS[$path])) {
    redirect(REDIRECTS[$path]);
}
// WordPress leftovers: admin, feeds, ?p= links, pagination and date archives.
if (preg_match('#^/(wp-admin|wp-login\.php|wp-includes|wp-json|xmlrpc\.php)(/|$)#', $path)) {
    redirect('/');
}
if (preg_match('#^/(.+)/(feed|amp|embed)/?$#', $path, $m)) {
    redirect('/' . $m[1] . '/');
}
if (preg_match('#^/(blog|category/job-articles)/page/\d+/?$#', $path, $m)) {
    redirect('/' . $m[1] . '/');
}
if ($path === '/' && $qs && preg_match('/(^|&)(p|page_id|s)=/', $qs)) {
    redirect('/');
}
// Old WordPress image URLs (Google Images, backlinks) -> the copy we kept, if any.
if (preg_match('#^/wp-content/uploads/\d{4}/\d{2}/([A-Za-z0-9._-]+?)(-\d+x\d+)?\.(webp|jpe?g|png)$#', $path, $m)) {
    foreach (['blog', 'site'] as $dir) {
        if (is_file(__DIR__ . "/assets/img/$dir/{$m[1]}.webp")) {
            redirect("/assets/img/$dir/{$m[1]}.webp");
        }
    }
}
if ($path === '/index.php') {
    redirect('/');
}

// Every HTML page lives at a trailing-slash URL, like the WordPress site did.
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('#\.[a-z0-9]+$#i', $path)) {
    redirect($path . '/' . ($qs ? '?' . $qs : ''));
}

const PAGES = [
    '/'                      => 'home',
    '/about/'                => 'about',
    '/our-services/'         => 'our-services',
    '/employers/'            => 'employers',
    '/job-postings/'         => 'job-postings',
    '/applications/'         => 'applications',
    '/contact-us/'           => 'contact-us',
    '/blog/'                 => 'blog',
    '/category/job-articles/' => 'blog',
    '/career-tools/'         => 'career-tools',
    '/privacy-policy/'       => 'privacy-policy',
    '/terms-of-use/'         => 'terms-of-use',
];

header('Content-Type: text/html; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: strict-origin-when-cross-origin');

if ($path === '/sitemap.xml') {
    require __DIR__ . '/inc/sitemap.php';
    exit;
}

if (isset(PAGES[$path])) {
    $route = $path;
    require __DIR__ . '/inc/pages/' . PAGES[$path] . '.php';
    exit;
}

if (preg_match('#^/career-tools/([a-z0-9-]+)/$#', $path, $m) && isset(TOOLS[$m[1]])) {
    $toolSlug = $m[1];
    require __DIR__ . '/inc/pages/tool.php';
    exit;
}

if (preg_match('#^/([a-z0-9-]+)/$#', $path, $m) && ($post = get_post($m[1]))) {
    require __DIR__ . '/inc/pages/post.php';
    exit;
}

http_response_code(404);
require __DIR__ . '/inc/pages/404.php';
