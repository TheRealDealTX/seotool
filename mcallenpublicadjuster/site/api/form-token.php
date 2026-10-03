<?php
/** Returns a fresh signed form token (lets cached pages submit forms reliably). */
declare(strict_types=1);
require_once dirname(__DIR__) . '/includes/functions.php';
require_once dirname(__DIR__) . '/includes/form.php';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');
echo json_encode(['token' => form_token()]);
