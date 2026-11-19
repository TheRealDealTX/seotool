<?php
/**
 * my1secret.com front controller.
 *
 * The Hostinger (nginx) platform serves existing files directly and sends every
 * other request here, so this file is the router for the whole site.
 */
declare(strict_types=1);

define('M1S', true);
define('M1S_ROOT', __DIR__);
define('M1S_APP', __DIR__ . '/app');

require M1S_APP . '/bootstrap.php';
require M1S_APP . '/routes.php';

m1s_dispatch();
