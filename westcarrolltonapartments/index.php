<?php
require __DIR__ . '/app/bootstrap.php';

$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(parse_url($uri, PHP_URL_PATH) ?: '/');
$qs = parse_url($uri, PHP_URL_QUERY);
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

// Canonical host: strip www.
if (str_starts_with($host, 'www.')) {
    redirect(url($path . ($qs ? "?$qs" : '')), 301);
}

// Legacy WordPress URLs
$legacyKey = rtrim($path, '/') . (str_ends_with($path, '.xml') ? '' : '/');
if ($legacyKey !== '/') {
    $legacy = legacy_redirects();
    if (isset($legacy[$legacyKey])) redirect($legacy[$legacyKey], 301);
    if (in_array($legacyKey, legacy_gone(), true)) gone();
    if (preg_match('#^/(wp-content|wp-includes|wp-json|wp-admin)/#', $path) || $path === '/wp-login.php' || $path === '/xmlrpc.php') gone();
    if (preg_match('#^/(category|tag|author)/#', $path)) redirect('/blog/', 301);
    if (preg_match('#^/page/\d+/?$#', $path)) redirect('/blog/', 301);
}

// Enforce trailing slash on page URLs (not files)
if ($method === 'GET' && $path !== '/' && !str_ends_with($path, '/') && !preg_match('/\.[a-z0-9]{2,5}$/i', $path)) {
    redirect($path . '/' . ($qs ? "?$qs" : ''), 301);
}

require APP_DIR . '/controllers.php';
require APP_DIR . '/account.php';
require APP_DIR . '/admin.php';

$routes = [
    '#^/$#' => 'page_home',
    '#^/apartments/$#' => 'page_directory',
    '#^/apartments/(pet-friendly|under-1000|studios|1-bedroom|2-bedroom|3-bedroom|townhomes|senior|income-based)/$#' => 'page_landing',
    '#^/apartments/([a-z0-9-]+)/$#' => 'page_listing',
    '#^/compare/$#' => 'page_compare',
    '#^/claim/([a-z0-9-]+)/$#' => 'page_claim',
    '#^/list-your-property/$#' => 'page_submit',
    '#^/list-your-property/thanks/$#' => 'page_submit_thanks',
    '#^/checkout/success/$#' => 'page_checkout_success',
    '#^/checkout/cancel/$#' => 'page_checkout_cancel',
    '#^/stripe/webhook/?$#' => 'stripe_webhook',
    '#^/blog/$#' => 'page_blog',
    '#^/blog/category/([a-z0-9-]+)/$#' => 'page_blog_category',
    '#^/blog/([a-z0-9-]+)/$#' => 'page_post',
    '#^/tools/$#' => 'page_tools',
    '#^/tools/([a-z0-9-]+)/$#' => 'page_tool',
    '#^/west-carrollton-living-guide/$#' => 'page_guide',
    '#^/about/$#' => 'page_about',
    '#^/contact/$#' => 'page_contact',
    '#^/privacy-policy/$#' => 'page_privacy',
    '#^/terms-of-use/$#' => 'page_terms',
    '#^/affiliate-disclosure/$#' => 'page_disclosure',
    '#^/sitemap\.xml$#' => 'sitemap_xml',
    '#^/robots\.txt$#' => 'robots_txt',
    // Owner accounts
    '#^/account/$#' => 'account_dashboard',
    '#^/account/login/$#' => 'account_login',
    '#^/account/verify/$#' => 'account_verify',
    '#^/account/magic/$#' => 'account_magic',
    '#^/account/logout/$#' => 'account_logout',
    '#^/account/listings/edit/$#' => 'account_edit_listing',
    // Admin
    '#^/admin/$#' => 'admin_dashboard',
    '#^/admin/login/$#' => 'admin_login',
    '#^/admin/logout/$#' => 'admin_logout',
    '#^/admin/listings/$#' => 'admin_listings',
    '#^/admin/listings/edit/$#' => 'admin_edit_listing',
    '#^/admin/listings/action/$#' => 'admin_listing_action',
    '#^/admin/users/$#' => 'admin_users',
    '#^/admin/payments/$#' => 'admin_payments',
    '#^/admin/messages/$#' => 'admin_messages',
    '#^/admin/settings/$#' => 'admin_settings',
];

try {
    foreach ($routes as $re => $fn) {
        if (preg_match($re, $path, $m)) {
            array_shift($m);
            $fn(...$m);
            exit;
        }
    }
    not_found();
} catch (Throwable $e) {
    error_log('[wca] ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    http_response_code(500);
    if (cfg('debug')) { echo '<pre>' . e((string)$e) . '</pre>'; exit; }
    echo '<!doctype html><meta charset="utf-8"><title>Something went wrong</title><div style="font-family:sans-serif;max-width:560px;margin:80px auto;text-align:center"><h1>Something went wrong</h1><p>Please try again in a moment.</p><p><a href="/">Back to West Carrollton Apartments</a></p></div>';
}
