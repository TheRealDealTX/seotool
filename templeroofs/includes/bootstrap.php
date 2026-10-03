<?php
/**
 * Loaded by every entry point. Sets up constants, configuration,
 * timezone, error handling and the shared helper functions.
 */
define('TR_ROOT', dirname(__DIR__));
define('TR_INC', TR_ROOT . '/includes');
define('TR_CONTENT', TR_ROOT . '/content');
define('TR_STORAGE', TR_ROOT . '/storage');
define('TR_VERSION', '1.0.0');

$GLOBALS['TR_CONFIG']  = require TR_INC . '/config.php';
$GLOBALS['TR_CATALOG'] = require TR_INC . '/catalog.php';

date_default_timezone_set($GLOBALS['TR_CONFIG']['timezone']);

// Never print PHP errors to visitors; log them privately instead.
ini_set('display_errors', '0');
ini_set('log_errors', '1');
if (is_dir(TR_STORAGE . '/logs') && is_writable(TR_STORAGE . '/logs')) {
    ini_set('error_log', TR_STORAGE . '/logs/php-errors.log');
}
if (PHP_SAPI === 'cli') {
    ini_set('display_errors', '1');
}

require TR_INC . '/helpers.php';
require TR_INC . '/content.php';
require TR_INC . '/components.php';
require TR_INC . '/schema.php';
require TR_INC . '/layout.php';
require TR_INC . '/icons.php';
require TR_INC . '/forms.php';
