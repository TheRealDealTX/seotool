<?php
// Rise Roommates — core bootstrap: config, DB, session, helpers.
declare(strict_types=1);

define('APP_ROOT', dirname(__DIR__));
define('APP_DIR', __DIR__);

$configFile = APP_DIR . '/config.php';
if (!is_file($configFile)) {
    http_response_code(503);
    exit('Rise Roommates is not configured yet. Copy app/config.sample.php to app/config.php.');
}
$CONFIG = require $configFile;

date_default_timezone_set($CONFIG['timezone'] ?? 'America/Chicago');
if (!empty($CONFIG['debug'])) {
    ini_set('display_errors', '1');
    error_reporting(E_ALL);
} else {
    ini_set('display_errors', '0');
}

require APP_DIR . '/lib.php';
require APP_DIR . '/match.php';

// ---------- Database ----------
function db(): PDO
{
    static $pdo = null;
    global $CONFIG;
    if ($pdo === null) {
        $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4',
            $CONFIG['db_host'], (int)($CONFIG['db_port'] ?? 3306), $CONFIG['db_name']);
        $pdo = new PDO($dsn, $CONFIG['db_user'], $CONFIG['db_pass'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]);
        $pdo->exec("SET time_zone = '" . (new DateTime())->format('P') . "'");
    }
    return $pdo;
}

function q(string $sql, array $params = []): PDOStatement
{
    $st = db()->prepare($sql);
    $st->execute($params);
    return $st;
}
function one(string $sql, array $params = []): ?array
{
    $r = q($sql, $params)->fetch();
    return $r === false ? null : $r;
}
function all(string $sql, array $params = []): array
{
    return q($sql, $params)->fetchAll();
}
function val(string $sql, array $params = [])
{
    $r = q($sql, $params)->fetchColumn();
    return $r === false ? null : $r;
}

// Create tables on first run / after schema changes.
function migrate(): void
{
    $sql = file_get_contents(APP_DIR . '/schema.sql');
    $sql = preg_replace('/^--.*$/m', '', $sql);
    foreach (array_filter(array_map('trim', explode(';', $sql))) as $stmt) {
        db()->exec($stmt);
    }
    // Columns added after the first release (CREATE TABLE IF NOT EXISTS won't add them).
    $addCols = [
        'properties' => [
            'external_id' => 'INT UNSIGNED NULL', 'external_url' => 'VARCHAR(255) NULL', 'image_url' => 'VARCHAR(500) NULL',
        ],
    ];
    foreach ($addCols as $table => $cols) {
        $have = array_column(all("SHOW COLUMNS FROM `$table`"), 'Field');
        foreach ($cols as $col => $def) {
            if (!in_array($col, $have, true)) db()->exec("ALTER TABLE `$table` ADD COLUMN `$col` $def");
        }
    }
    $defaults = [
        'site_name' => 'Rise Roommates',
        'tagline' => 'Find your people. Find your place.',
        'announcement' => '',
        'messaging_friends_only' => '0',
        'allow_property_submissions' => '1',
        'require_property_approval' => '1',
        'registration_open' => '1',
        'schema_version' => '2',
        'sync_source' => 'https://riseapartments.com',
        'last_sync' => '',
    ];
    foreach ($defaults as $k => $v) {
        q('INSERT IGNORE INTO settings (k, v) VALUES (?, ?)', [$k, $v]);
    }
}

function setting(string $key, ?string $default = null): ?string
{
    static $cache = null;
    if ($cache === null) {
        try {
            $cache = [];
            foreach (all('SELECT k, v FROM settings') as $r) {
                $cache[$r['k']] = $r['v'];
            }
        } catch (PDOException $e) {
            migrate();
            $cache = [];
            foreach (all('SELECT k, v FROM settings') as $r) {
                $cache[$r['k']] = $r['v'];
            }
        }
    }
    return $cache[$key] ?? $default;
}

// ---------- Session ----------
$secure = (($_SERVER['HTTPS'] ?? '') === 'on') || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
session_name('rr_sess');
session_set_cookie_params([
    'lifetime' => 60 * 60 * 24 * 30,
    'path' => '/',
    'secure' => $secure,
    'httponly' => true,
    'samesite' => 'Lax',
]);
ini_set('session.gc_maxlifetime', (string)(60 * 60 * 24 * 30));
session_start();

header('X-Frame-Options: SAMEORIGIN');
header('X-Content-Type-Options: nosniff');
header('Referrer-Policy: strict-origin-when-cross-origin');
// Personalised pages must never be cached by LiteSpeed or a CDN.
header('Cache-Control: private, no-store, max-age=0');
header('X-LiteSpeed-Cache-Control: no-cache');
