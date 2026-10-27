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
        // Served on the real domain: canonical URLs point there and search engines may index.
        // Any other host (the temporary hostingersite.com preview) keeps its own settings (noindex).
        $host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
        if ($cfg['live_host'] && in_array($host, [$cfg['live_host'], 'www.' . $cfg['live_host']], true)) {
            $cfg['site_url'] = 'https://' . $cfg['live_host'];
            $cfg['indexable'] = empty($cfg['force_noindex']);
        }
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
    // Columns added after the first deploy (CREATE TABLE IF NOT EXISTS won't add them)
    $add = [
        'properties' => ['source' => "VARCHAR(10) NOT NULL DEFAULT 'rise'", 'locked' => 'INT NOT NULL DEFAULT 0',
                         'updated_at' => "VARCHAR(30) NOT NULL DEFAULT ''", 'updated_by' => "VARCHAR(150) NOT NULL DEFAULT ''"],
        'leads'      => ['status' => "VARCHAR(20) NOT NULL DEFAULT 'new'", 'notes' => 'TEXT'],
    ];
    foreach ($add as $table => $cols) {
        $have = table_columns($table);
        foreach ($cols as $col => $def) {
            if (!in_array($col, $have, true)) {
                db()->exec("ALTER TABLE $table ADD COLUMN $col $def");
            }
        }
    }
}

function table_columns(string $table): array
{
    $st = db()->query("SELECT * FROM $table LIMIT 0");
    $out = [];
    for ($i = 0; $i < $st->columnCount(); $i++) {
        $out[] = $st->getColumnMeta($i)['name'];
    }
    return $out;
}

/*
 * US phone validation (lead spam filter). Keep in sync with usPhone() in
 * assets/js/site.js. Accepts NANP numbers whose area code is a US one:
 * not Canada or the Caribbean, not toll-free/premium, not N11/N9X/37X/96X,
 * with a valid exchange and no obvious fake patterns.
 */
const NON_US_AREA_CODES = [
    // Canada
    204, 226, 236, 249, 250, 257, 263, 289, 306, 343, 354, 365, 367, 368, 382, 403, 416, 418, 428, 431, 437, 438, 450, 460,
    468, 474, 506, 514, 519, 548, 579, 581, 584, 587, 600, 604, 613, 622, 639, 647, 672, 683, 705, 709, 742, 753, 778, 780,
    782, 807, 819, 825, 867, 873, 879, 902, 905,
    // Caribbean / Atlantic NANP countries
    242, 246, 264, 268, 284, 345, 441, 473, 649, 658, 664, 721, 758, 767, 784, 809, 829, 849, 868, 869, 876,
    // toll-free, premium and special use
    500, 521, 522, 523, 524, 525, 526, 527, 528, 529, 533, 544, 566, 577, 588, 700, 710, 800, 822, 833, 844, 855, 866, 877,
    880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 900, 976,
];

/** Normalize to "+1 (832) 297-3982", or null when it isn't a plausible US number. */
function us_phone(string $raw): ?string
{
    $d = preg_replace('/\D/', '', $raw);
    if (strlen($d) === 11 && $d[0] === '1') {
        $d = substr($d, 1);
    }
    if (strlen($d) !== 10) {
        return null;
    }
    $area = (int) substr($d, 0, 3);
    $exch = substr($d, 3, 3);
    $valid = $d[0] >= '2' && $d[1] !== '9' && substr($d, 1, 2) !== '11'
        && !in_array($area, NON_US_AREA_CODES, true) && !preg_match('/^(37|96)/', (string) $area)
        && $exch[0] >= '2' && substr($exch, 1) !== '11' && $exch !== '555'
        && !preg_match('/^(\d)\1{9}$/', $d) && !in_array(substr($d, 3), ['1234567', '0000000'], true);
    return $valid ? sprintf('+1 (%s) %s-%s', substr($d, 0, 3), $exch, substr($d, 6)) : null;
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
