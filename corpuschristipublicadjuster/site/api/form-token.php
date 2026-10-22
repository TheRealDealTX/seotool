<?php
/** Returns a fresh signed form token (lets cached pages submit forms reliably). */
declare(strict_types=1);
// Private code and data: next to the web root locally, ../ccpa-app/ on the live server.
define('CCPA_PUBLIC', dirname(__DIR__));
define('CCPA_ROOT', is_file(CCPA_PUBLIC . '/includes/bootstrap.php') ? CCPA_PUBLIC : dirname(CCPA_PUBLIC) . '/ccpa-app');
require_once CCPA_ROOT . '/includes/functions.php';
require_once CCPA_ROOT . '/includes/form.php';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');
echo json_encode(['token' => form_token()]);
