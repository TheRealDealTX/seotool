<?php
declare(strict_types=1);
defined('M1S') || exit;

const M1S_VERSION = '1.0.0';

/* ---------- configuration ----------
 * Looked up, in order:
 *   1. $M1S_CONFIG environment variable (local development / tests)
 *   2. ../.h5g/my1secret-config.php   (Hostinger: outside the web root)
 *   3. ../config.local.php            (local checkout)
 * See config.sample.php for the keys.
 */
function m1s_load_config(): array
{
    $candidates = array_filter([
        getenv('M1S_CONFIG') ?: null,
        dirname(M1S_ROOT) . '/.h5g/my1secret-config.php',
        dirname(M1S_ROOT) . '/config.local.php',
    ]);
    foreach ($candidates as $file) {
        if (is_file($file)) {
            $cfg = require $file;
            if (is_array($cfg)) {
                return $cfg + [
                    'site_name'   => 'My 1 Secret',
                    'base_url'    => 'https://my1secret.com',
                    'canonical_host' => null,
                    'mail_from'   => 'no-reply@my1secret.com',
                    'debug'       => false,
                    'secret'      => '',
                ];
            }
        }
    }
    http_response_code(503);
    header('Content-Type: text/plain; charset=utf-8');
    echo "Site configuration missing.";
    exit;
}

$GLOBALS['M1S_CFG'] = m1s_load_config();

function cfg(string $key, $default = null)
{
    return $GLOBALS['M1S_CFG'][$key] ?? $default;
}

error_reporting(E_ALL);
ini_set('display_errors', cfg('debug') ? '1' : '0');
ini_set('log_errors', '1');
date_default_timezone_set('UTC');
mb_internal_encoding('UTF-8');

require M1S_APP . '/lib/db.php';
require M1S_APP . '/lib/helpers.php';
require M1S_APP . '/lib/session.php';
require M1S_APP . '/lib/auth.php';
require M1S_APP . '/lib/markdown.php';
require M1S_APP . '/lib/seo.php';
require M1S_APP . '/lib/content.php';
require M1S_APP . '/lib/mailer.php';
require M1S_APP . '/lib/guest.php';
require M1S_APP . '/lib/products.php';
require M1S_APP . '/views/partials.php';

set_exception_handler(function (Throwable $e) {
    error_log('[m1s] ' . $e->getMessage() . ' @ ' . $e->getFile() . ':' . $e->getLine());
    if (!headers_sent()) {
        http_response_code(500);
        header('Content-Type: text/html; charset=utf-8');
        header('Cache-Control: no-store');
    }
    if (cfg('debug')) {
        echo '<pre>' . e((string)$e) . '</pre>';
        return;
    }
    echo '<!doctype html><meta charset="utf-8"><title>Something went wrong</title>'
       . '<p style="font:16px system-ui;margin:3rem auto;max-width:36rem">Something went wrong on our side. '
       . 'Please try again in a moment. <a href="/">Back to My 1 Secret</a></p>';
});
