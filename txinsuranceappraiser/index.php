<?php
/**
 * TX Insurance Appraiser — front controller.
 * Every request that is not a real file is routed here by .htaccess.
 */
declare(strict_types=1);

define('ROOT', __DIR__);
require ROOT . '/inc/config.php';
require ROOT . '/inc/helpers.php';
require ROOT . '/inc/schema.php';
require ROOT . '/inc/layout.php';
require ROOT . '/inc/longform.php';
require ROOT . '/inc/redirects.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$qs   = ($q = parse_url($uri, PHP_URL_QUERY)) ? '?' . $q : '';

function redirect(string $to, int $code = 301): never
{
    header('Location: ' . $to, true, $code);
    exit;
}

function not_found(): never
{
    http_response_code(404);
    require ROOT . '/pages/404.php';
    exit;
}

/* ---- canonical host / scheme (production only; staging domain is left alone) */
if (is_production()) {
    $host  = strtolower($_SERVER['HTTP_HOST'] ?? '');
    $https = ($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https'
        || ($_SERVER['SERVER_PORT'] ?? '') === '443';
    if (!$https || $host === 'www.' . SITE['prod_host']) {
        redirect(SITE['origin'] . $uri);
    }
}

/* ---- legacy WordPress URLs ------------------------------------------------ */
if ($to = legacy_redirect($path)) {
    redirect($to . ($to[0] === '/' && !str_contains($to, '?') ? $qs : ''));
}

/* ---- machine files ------------------------------------------------------- */
if ($path === '/sitemap.xml') { require ROOT . '/pages/sitemap-xml.php'; exit; }
if ($path === '/robots.txt')  { require ROOT . '/pages/robots.php'; exit; }
if ($path === '/contact-submit/' || $path === '/contact-submit') { require ROOT . '/inc/contact-handler.php'; exit; }

/* ---- enforce trailing slash on page URLs ---------------------------------- */
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('/\.[a-z0-9]{2,5}$/i', $path)) {
    redirect($path . '/' . $qs);
}

/* ---- routes ---------------------------------------------------------------- */
$static = [
    '/'                       => 'home',
    '/about-us/'              => 'about',
    '/what-is-an-appraisal/'  => 'what-is-an-appraisal',
    '/services/'              => 'services',
    '/areas/'                 => 'areas',
    '/blog/'                  => 'blog',
    '/contact-us/'            => 'contact',
    '/privacy-policy/'        => 'privacy',
    '/terms-conditions/'      => 'terms',
    '/tools/'                 => 'tools',
    '/thank-you/'             => 'thank-you',
];
if (isset($static[$path])) {
    require ROOT . '/pages/' . $static[$path] . '.php';
    exit;
}

if (preg_match('#^/services/(appraisal|umpire|matterport|xactimate-estimate|symbility-estimate)/$#', $path, $m)) {
    $service_slug = $m[1];
    require ROOT . '/pages/service.php';
    exit;
}

if (preg_match('#^/areas/([a-z0-9-]+)-insurance-appraiser/$#', $path, $m) && isset(cities()[$m[1]])) {
    $city = cities()[$m[1]];
    require ROOT . '/pages/city.php';
    exit;
}

if (preg_match('#^/tools/([a-z0-9-]+)/$#', $path, $m) && isset(TOOLS[$m[1]])) {
    $tool_slug = $m[1];
    require ROOT . '/pages/tool.php';
    exit;
}

if (preg_match('#^/([a-z0-9-]+)/$#', $path, $m) && isset(posts()[$m[1]])) {
    $post = posts()[$m[1]];
    require ROOT . '/pages/post.php';
    exit;
}

not_found();
