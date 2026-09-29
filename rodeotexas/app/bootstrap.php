<?php
/**
 * Loaded first by every entry point (public front controller, admin, CLI).
 * Sets up paths, configuration, error handling and the class autoloader.
 */
declare(strict_types=1);

define('RT_APP', __DIR__);
if (!defined('RT_PUBLIC')) {
    define('RT_PUBLIC', dirname(__DIR__) . '/public_html');
}
define('RT_STORAGE', RT_APP . '/storage');

$__cfgFile = getenv('RT_CONFIG') ?: RT_APP . '/config.php';
if (!is_file($__cfgFile)) {
    http_response_code(500);
    exit("Configuration missing: copy app/config.example.php to app/config.php\n");
}
$GLOBALS['RT_CONFIG'] = require $__cfgFile;
unset($__cfgFile);

date_default_timezone_set('UTC');   // everything stored in UTC; venue zones applied on output
mb_internal_encoding('UTF-8');

$__debug = !empty($GLOBALS['RT_CONFIG']['debug']) || PHP_SAPI === 'cli';
ini_set('display_errors', $__debug ? '1' : '0');
ini_set('log_errors', '1');
ini_set('error_log', RT_STORAGE . '/logs/php-error.log');
error_reporting(E_ALL);
unset($__debug);

foreach (['logs', 'locks', 'cache', 'imports'] as $__d) {
    if (!is_dir(RT_STORAGE . '/' . $__d)) {
        @mkdir(RT_STORAGE . '/' . $__d, 0750, true);
    }
}

spl_autoload_register(static function (string $class): void {
    if (strncmp($class, 'RT\\', 3) !== 0) {
        return;
    }
    $rel = str_replace('\\', '/', substr($class, 3));
    // RT\Adapters\Foo → app/adapters/Foo.php ; RT\Foo → app/lib/Foo.php
    $f = strncmp($rel, 'Adapters/', 9) === 0
        ? RT_APP . '/adapters/' . substr($rel, 9) . '.php'
        : RT_APP . '/lib/' . $rel . '.php';
    if (is_file($f)) {
        require $f;
    }
});

require RT_APP . '/lib/helpers.php';
