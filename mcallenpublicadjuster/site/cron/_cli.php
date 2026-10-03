<?php
/**
 * Shared setup for cron scripts. These scripts are meant for Hostinger's
 * Cron Jobs panel (PHP CLI). The /cron folder is blocked from the web.
 */
declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(403);
    exit("CLI only\n");
}
define('MPA_ROOT', dirname(__DIR__));
require_once MPA_ROOT . '/includes/config.php';
require_once MPA_ROOT . '/includes/functions.php';
require_once MPA_ROOT . '/includes/weather.php';
require_once MPA_ROOT . '/includes/storms.php';
@set_time_limit(600);
ini_set('memory_limit', '256M');

function cli_opt(string $name, $default = null)
{
    global $argv;
    foreach ($argv ?? [] as $a) {
        if ($a === '--' . $name) {
            return true;
        }
        if (strpos($a, '--' . $name . '=') === 0) {
            return substr($a, strlen($name) + 3);
        }
    }
    return $default;
}

function out(string $channel, string $msg): void
{
    echo '[' . date('Y-m-d H:i:s') . "] $msg\n";
    log_line($channel, $msg);
}
