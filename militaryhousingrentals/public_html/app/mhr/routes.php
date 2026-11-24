<?php
// Routes for the add-on, called from site.php before its trailing-slash
// redirect (Stripe posts to /stripe/webhook without one). Returns true when the
// request was handled.

function mhr_route($path) {
    if ($path === '/stripe/webhook' || $path === '/stripe/webhook/') {
        if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); header('Allow: POST'); echo 'POST only'; return true; }
        mhr_stripe_webhook();
        return true;
    }
    $admin = rtrim(mhr_admin_path(), '/');
    $prefixes = ['/claim', '/checkout', '/account', $admin];
    $match = false;
    foreach ($prefixes as $p) if ($path === $p || str_starts_with($path, $p . '/')) $match = $p;
    if (!$match) return false;
    if (!str_ends_with($path, '/')) {
        $qs = $_SERVER['QUERY_STRING'] ?? '';
        redirect($path . '/' . ($qs !== '' ? '?' . $qs : ''));
    }
    $sub = substr($path, strlen($match)); // e.g. "/", "/some-slug/"
    try {
        mhr_db();
    } catch (MhrDbUnavailable $e) {
        mhr_page_start('Temporarily unavailable', $path);
        http_response_code(503);
        echo '<section class="section"><div class="wrap narrow"><div class="card form-card"><h1>Temporarily unavailable</h1><p>This part of the site is being set up. Please try again shortly, or <a href="/contact-us/">contact us</a>.</p></div></div></section>';
        layout_end();
        return true;
    }
    switch ($match) {
        case '/claim': require MHR . '/views/claim.php'; break;
        case '/checkout': require MHR . '/views/checkout.php'; break;
        case '/account': require MHR . '/views/account.php'; break;
        default: require MHR . '/views/admin.php';
    }
    return true;
}
