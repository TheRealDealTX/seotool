<?php
/**
 * Temple Roofers — front controller. Every clean URL (/about/, /services/…)
 * is routed here by .htaccess and dispatched to a page in includes/pages.
 */
require __DIR__ . '/includes/bootstrap.php';
require TR_INC . '/router.php';

route_request((string) ($_SERVER['REQUEST_URI'] ?? '/'));
