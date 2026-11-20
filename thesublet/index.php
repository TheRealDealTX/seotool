<?php
// thesublet.com — front controller. nginx sends every unknown path here (.htaccess is ignored).
define('APP', true);

$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');

// php -S local dev: let the built-in server deliver real static files
if (PHP_SAPI === 'cli-server' && $path !== '/' && is_file(__DIR__ . $path) && !str_starts_with($path, '/app/') && !str_ends_with($path, '.php')) {
    return false;
}

require __DIR__ . '/app/bootstrap.php';

// ---- canonical scheme + host (TLS terminates at the CDN; trust X-Forwarded-Proto) ----
$canonHost = (string)cfg('canonical_host', '');
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$proto = strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (($_SERVER['HTTPS'] ?? '') === 'on' ? 'https' : 'http'));
if (cfg('env') !== 'dev' && $canonHost !== '' && ($host !== $canonHost || $proto === 'http')) {
    if ($host === $canonHost || $host === 'www.' . $canonHost) {
        header('Location: https://' . $canonHost . $uri, true, 301);
        exit;
    }
}

// Never expose app internals even if someone requests the files directly
if (preg_match('#^/(app|dev)(/|$)#', $path)) not_found();

$routes = [
    // public pages
    ['GET',  '#^/$#', 'home'],
    ['GET',  '#^/sublets/$#', 'browse'],
    ['GET',  '#^/sublets/([a-z]{2})/$#', 'state'],
    ['GET',  '#^/sublets/([a-z]{2})/([a-z0-9-]+)/$#', 'city'],
    ['GET',  '#^/sublets/([a-z]{2})/([a-z0-9-]+)/([a-z0-9-]+)/$#', 'city'],
    ['GET',  '#^/sublet/([a-z0-9-]+)-([a-z]{2})/([a-z0-9-]+)-(\d+)/$#', 'listing'],
    ['POST', '#^/listing/(\d+)/contact/$#', 'listing_contact'],
    ['POST', '#^/listing/(\d+)/report/$#', 'listing_report'],
    ['GET',  '#^/photo/(\d+)\.webp$#', 'photo'],
    ['ANY',  '#^/post-a-sublet/$#', 'submit'],
    ['GET',  '#^/post-a-sublet/thanks/$#', 'submit_thanks'],
    ['POST', '#^/checkout/start/(\d+)/$#', 'checkout_start'],
    ['GET',  '#^/checkout/success/$#', 'checkout_success'],
    ['GET',  '#^/checkout/cancel/$#', 'checkout_cancel'],
    ['POST', '#^/stripe/webhook/?$#', 'stripe_webhook'],
    ['ANY',  '#^/upgrade/(\d+)/$#', 'upgrade'],
    ['ANY',  '#^/renew/(\d+)/$#', 'renew'],
    ['ANY',  '#^/manage/(\d+)/$#', 'manage'],
    ['ANY',  '#^/login/$#', 'account/login'],
    ['ANY',  '#^/auth/([a-f0-9]+)/$#', 'account/auth'],
    ['ANY',  '#^/logout/$#', 'account/logout'],
    ['GET',  '#^/account/$#', 'account/dashboard'],
    ['ANY',  '#^/account/listing/(\d+)/$#', 'account/edit'],
    ['POST', '#^/account/listing/(\d+)/action/$#', 'account/action'],
    ['ANY',  '#^/account/new/$#', 'account/new'],
    ['GET',  '#^/api/listings/?$#', 'api_listings'],
    ['GET',  '#^/api/csrf/?$#', 'api_csrf'],
    ['GET',  '#^/blog/$#', 'blog'],
    ['GET',  '#^/blog/([a-z0-9-]+)/$#', 'blog_post'],
    ['GET',  '#^/tools/$#', 'tools'],
    ['GET',  '#^/tools/([a-z0-9-]+)/$#', 'tools'],
    ['GET',  '#^/favorites/$#', 'favorites'],
    ['GET',  '#^/compare/$#', 'compare'],
    ['ANY',  '#^/contact/$#', 'contact'],
    ['GET',  '#^/(about|safety|fair-housing|terms|privacy|pricing|credits)/$#', 'static'],
    ['GET',  '#^/sitemap\.xml$#', 'sitemap'],
    ['GET',  '#^/cron/run/?$#', 'cron'],
    // admin
    ['ANY',  '#^/admin/?$#', 'admin/dashboard'],
    ['ANY',  '#^/admin/login/$#', 'admin/login'],
    ['ANY',  '#^/admin/logout/$#', 'admin/logout'],
    ['ANY',  '#^/admin/listings/$#', 'admin/listings'],
    ['ANY',  '#^/admin/listing/(\d+)/$#', 'admin/listing'],
    ['ANY',  '#^/admin/owners/$#', 'admin/owners'],
    ['GET',  '#^/admin/payments/$#', 'admin/payments'],
    ['GET',  '#^/admin/messages/$#', 'admin/messages'],
    ['ANY',  '#^/admin/reports/$#', 'admin/reports'],
    ['ANY',  '#^/admin/settings/$#', 'admin/settings'],
];

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
foreach ($routes as [$m, $re, $handler]) {
    if (!preg_match($re, $path, $mm)) continue;
    if ($m !== 'ANY' && $m !== $method && !($m === 'GET' && $method === 'HEAD')) {
        http_response_code(405);
        header('Allow: ' . $m);
        exit;
    }
    array_shift($mm);
    $params = $mm;
    if (!str_starts_with($handler, 'admin') && $handler !== 'photo' && $handler !== 'stripe_webhook') maybe_run_cron();
    require APPDIR . '/pages/' . $handler . '.php';
    exit;
}

// ---- legacy URLs from the old WordPress site ----
require APPDIR . '/legacy.php';
legacy_route($path);

// Add a trailing slash to clean paths (e.g. /blog → /blog/)
if (!str_ends_with($path, '/') && !str_contains(basename($path), '.') && preg_match('#^/[a-z0-9/-]+$#', $path)) {
    $qs = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
    redirect($path . '/' . $qs, 301);
}

not_found();
