<?php
/**
 * Loads configuration and every helper. Required once by index.php.
 */
declare(strict_types=1);

define('ALL_SITE', true);
define('SITE_ROOT', dirname(__DIR__));

require SITE_ROOT . '/config.php';
require __DIR__ . '/helpers.php';
require __DIR__ . '/icons.php';
require __DIR__ . '/content.php';
require __DIR__ . '/schema.php';
require __DIR__ . '/components.php';
require __DIR__ . '/tools.php';
require __DIR__ . '/render.php';
