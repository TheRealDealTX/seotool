<?php
/**
 * Admin front controller: /admin/?page=<name>
 * Admin templates live outside the web root in app/admin/. The public
 * includes/head.php (analytics, pixels) is NOT used here.
 */
declare(strict_types=1);

define('RT_PUBLIC', dirname(__DIR__));
require dirname(__DIR__, 2) . '/app/bootstrap.php';
require RT_APP . '/admin/layout.php';

use RT\Auth;

security_headers(true);
Auth::start();

$pages = ['login', 'logout', 'dashboard', 'events', 'event', 'venues', 'venue', 'review', 'sources', 'source', 'imports',
    'articles', 'article', 'links', 'redirects', 'account', 'associations'];
$name = (string) ($_GET['page'] ?? 'dashboard');
if (!in_array($name, $pages, true)) {
    http_response_code(404);
    $name = 'dashboard';
}
if ($name !== 'login') {
    $admin = Auth::require();
    if (is_post()) {
        Auth::checkCsrf();
    }
}
try {
    require RT_APP . '/admin/pages/' . $name . '.php';
} catch (\Throwable $ex) {
    app_log('admin-error', $ex->getMessage() . ' @ ' . $ex->getFile() . ':' . $ex->getLine());
    if (cfg('debug')) {
        throw $ex;
    }
    http_response_code(500);
    admin_header('Error');
    echo '<div class="alert alert--danger">Something went wrong: ' . e($ex->getMessage()) . '</div>';
    admin_footer();
}
