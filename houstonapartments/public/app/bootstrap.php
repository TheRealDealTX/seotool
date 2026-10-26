<?php
// Shared setup: config, database, view helpers.
define('HA_ROOT', dirname(__DIR__));
define('HA_APP', __DIR__);

require HA_APP . '/site.php';

function config(string $key, $default = null)
{
    static $cfg;
    if ($cfg === null) {
        $local = HA_APP . '/config.local.php';
        $cfg = array_merge(require HA_APP . '/config.sample.php', is_file($local) ? require $local : []);
    }
    return $cfg[$key] ?? $default;
}

function db(bool $fresh = false): PDO
{
    static $pdo;
    if (!$pdo || $fresh) {
        $pdo = new PDO(config('db_dsn'), config('db_user'), config('db_pass'), [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
        if (db_driver($pdo) === 'sqlite') {
            $pdo->exec('PRAGMA journal_mode=WAL');
        }
    }
    return $pdo;
}

/** Reconnect if the server dropped an idle connection (long imports outlast wait_timeout). */
function db_alive(): PDO
{
    try {
        @db()->query('SELECT 1');
        return db();
    } catch (PDOException) {
        return db(true);
    }
}

function db_driver(?PDO $pdo = null): string
{
    return ($pdo ?? db())->getAttribute(PDO::ATTR_DRIVER_NAME);
}

/** Create tables if missing. Safe to call repeatedly. */
function db_migrate(): void
{
    $sql = file_get_contents(HA_APP . '/schema.sql');
    if (db_driver() === 'sqlite') {
        $sql = preg_replace(['/\bAUTO_INCREMENT\b/', '/\bINT UNSIGNED\b/', '/ENGINE=\w+[^;]*/', '/\bLONGTEXT\b/', '/\bMEDIUMTEXT\b/'],
                            ['AUTOINCREMENT', 'INTEGER', '', 'TEXT', 'TEXT'], $sql);
        $sql = str_replace('INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', $sql);
        $sql = preg_replace('/,\s*(UNIQUE )?KEY \w+ \([^)]*\)/', '', $sql);
    }
    foreach (array_filter(array_map('trim', explode(';', $sql))) as $stmt) {
        db()->exec($stmt);
    }
}

function e($s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function site_url(string $path = '/'): string
{
    return rtrim(config('site_url'), '/') . $path;
}

/** Asset URL with a modification-time cache buster. */
function asset(string $path): string
{
    $file = HA_ROOT . '/assets/' . $path;
    return '/assets/' . $path . (is_file($file) ? '?v=' . filemtime($file) : '');
}

function money($n): string
{
    return $n ? '$' . number_format((int) $n) : '';
}

function beds_label(int $b): string
{
    return $b === 0 ? 'Studio' : $b . ' Bed' . ($b > 1 ? 's' : '');
}

function beds_range(array $p): string
{
    $lo = (int) $p['beds_min'];
    $hi = (int) $p['beds_max'];
    if ($lo === $hi) {
        return beds_label($lo);
    }
    return ($lo === 0 ? 'Studio' : $lo) . ' – ' . $hi . ' Beds';
}

function slugify(string $s): string
{
    $s = strtolower(trim(preg_replace('/[^A-Za-z0-9]+/', '-', $s), '-'));
    return $s ?: 'item';
}

/** Render a view inside the layout. $meta: title, description, canonical, schema, body_class. */
function render(string $view, array $vars = [], array $meta = []): void
{
    extract($vars, EXTR_SKIP);
    ob_start();
    require HA_APP . "/views/$view.php";
    $content = ob_get_clean();
    require HA_APP . '/views/layout.php';
}

function json_out($data, int $code = 200): void
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
}

function content(string $kind): array
{
    static $cache = [];
    return $cache[$kind] ??= json_decode(file_get_contents(HA_APP . "/content/$kind.json"), true);
}

function find_content(string $kind, string $path): ?array
{
    foreach (content($kind) as $row) {
        if ($row['path'] === $path) {
            return $row;
        }
    }
    return null;
}
