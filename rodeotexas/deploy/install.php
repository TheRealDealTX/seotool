<?php
/**
 * ONE-TIME INSTALLER for Hostinger (used when there is no SSH session).
 *
 * tools/build-package.sh copies this file to public_html/_install_<random>.php
 * with __TOKEN__ and __ADMIN_*__ filled in, next to rodeotexas-package.zip.
 * Call each step in order (HTTPS):
 *
 *   ?t=TOKEN&step=check      environment report (PHP, extensions, paths)
 *   ?t=TOKEN&step=backup     dump the WordPress DB + move WordPress files to ../backups/wp-<date>/
 *   ?t=TOKEN&step=extract    unpack app/ (outside public_html) and the new public_html files
 *   ?t=TOKEN&step=migrate    create/upgrade database tables
 *   ?t=TOKEN&step=seed       import the old articles, Texas legacy events and 301 redirects
 *   ?t=TOKEN&step=admin      create the administrator (password hash embedded, never plaintext)
 *   ?t=TOKEN&step=import     first real event import
 *   ?t=TOKEN&step=cleanup    delete the package and THIS FILE
 *
 * Every step is idempotent and prints a short plain-text report.
 */
declare(strict_types=1);

const TOKEN = '__TOKEN__';
const ADMIN_EMAIL = '__ADMIN_EMAIL__';
const ADMIN_HASH = '__ADMIN_HASH__';
const PACKAGE = 'rodeotexas-package.zip';

header('Content-Type: text/plain; charset=utf-8');
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');
if (strlen(TOKEN) < 32 || !hash_equals(TOKEN, (string) ($_GET['t'] ?? ''))) {
    http_response_code(404);
    exit;
}
@set_time_limit(480);
ignore_user_abort(true);

$pub = __DIR__;                       // …/domains/rodeotexas.org/public_html
$root = dirname($pub);                // …/domains/rodeotexas.org
$appDir = $root . '/app';
$step = (string) ($_GET['step'] ?? 'check');
$out = static function (string $s): void { echo $s, "\n"; @ob_flush(); @flush(); };

function rt_boot(string $appDir): void
{
    if (!defined('RT_APP')) {
        define('RT_PUBLIC', __DIR__);
        require_once $appDir . '/bootstrap.php';
    }
}

switch ($step) {
    case 'check':
        $out('PHP ' . PHP_VERSION . ' (' . PHP_SAPI . ')');
        foreach (['pdo_mysql', 'zip', 'curl', 'intl', 'mbstring', 'gd', 'json', 'openssl'] as $ext) {
            $out(str_pad($ext, 10) . (extension_loaded($ext) ? 'yes' : 'NO'));
        }
        $out('public_html: ' . $pub . (is_writable($pub) ? ' (writable)' : ' (NOT writable)'));
        $out('app dir:     ' . $appDir . (is_writable($root) ? ' (parent writable)' : ' (parent NOT writable)'));
        $out('package:     ' . (is_file($pub . '/' . PACKAGE) ? filesize($pub . '/' . PACKAGE) . ' bytes' : 'MISSING'));
        $out('wp-config:   ' . (is_file($pub . '/wp-config.php') ? 'present' : 'absent'));
        $out('php.ini date.timezone=' . ini_get('date.timezone') . ' · server now ' . date('Y-m-d H:i:s T') . ' · UTC ' . gmdate('H:i'));
        $out('disabled functions: ' . ini_get('disable_functions'));
        $out('max_execution_time=' . ini_get('max_execution_time') . ' memory_limit=' . ini_get('memory_limit'));
        $out('disk free: ' . round((float) @disk_free_space($root) / 1048576) . ' MB');
        break;

    case 'backup':
        $dest = $root . '/backups/wp-' . gmdate('Ymd');
        if (!is_dir($dest) && !mkdir($dest, 0750, true)) {
            $out('ERROR cannot create ' . $dest);
            break;
        }
        file_put_contents($root . '/backups/.htaccess', "Require all denied\n");
        // 1) Database dump (from wp-config.php credentials)
        if (is_file($pub . '/wp-config.php') && !is_file($dest . '/wordpress-database.sql.gz')) {
            $cfg = (string) file_get_contents($pub . '/wp-config.php');
            $def = static function (string $k) use ($cfg): ?string {
                return preg_match("/define\(\s*['\"]" . $k . "['\"]\s*,\s*['\"](.*?)['\"]\s*\)/", $cfg, $m) ? stripcslashes($m[1]) : null;
            };
            $host = $def('DB_HOST') ?: 'localhost';
            $port = 3306;
            if (str_contains($host, ':')) { [$host, $port] = explode(':', $host, 2); $port = (int) $port; }
            $db = new mysqli($host, (string) $def('DB_USER'), (string) $def('DB_PASSWORD'), (string) $def('DB_NAME'), $port);
            $db->set_charset('utf8mb4');
            $gz = gzopen($dest . '/wordpress-database.sql.gz.part', 'wb6');
            gzwrite($gz, "-- WordPress backup of " . $def('DB_NAME') . ' taken ' . gmdate('c') . "\nSET NAMES utf8mb4;\nSET FOREIGN_KEY_CHECKS=0;\n");
            $tables = 0; $rows = 0;
            foreach ($db->query('SHOW TABLES')->fetch_all() as [$table]) {
                $create = $db->query('SHOW CREATE TABLE `' . $table . '`')->fetch_row()[1];
                gzwrite($gz, "\nDROP TABLE IF EXISTS `{$table}`;\n{$create};\n");
                $res = $db->query('SELECT * FROM `' . $table . '`', MYSQLI_USE_RESULT);
                $batch = [];
                while ($r = $res->fetch_row()) {
                    $batch[] = '(' . implode(',', array_map(static fn($v) => $v === null ? 'NULL' : "'" . $db->real_escape_string((string) $v) . "'", $r)) . ')';
                    $rows++;
                    if (count($batch) >= 200) { gzwrite($gz, "INSERT INTO `{$table}` VALUES " . implode(",\n", $batch) . ";\n"); $batch = []; }
                }
                if ($batch) { gzwrite($gz, "INSERT INTO `{$table}` VALUES " . implode(",\n", $batch) . ";\n"); }
                $res->free();
                $tables++;
            }
            gzwrite($gz, "SET FOREIGN_KEY_CHECKS=1;\n");
            gzclose($gz);
            rename($dest . '/wordpress-database.sql.gz.part', $dest . '/wordpress-database.sql.gz');
            $out("Database {$def('DB_NAME')}: {$tables} tables, {$rows} rows → " . $dest . '/wordpress-database.sql.gz (' . filesize($dest . '/wordpress-database.sql.gz') . ' bytes)');
        } else {
            $out('Database dump: ' . (is_file($dest . '/wordpress-database.sql.gz') ? 'already done' : 'no wp-config.php found'));
        }
        // 2) Move WordPress files aside (instant rename; nothing is deleted).
        //    wp-content/uploads stays in place: migrated articles still use those images.
        $keep = [basename(__FILE__), PACKAGE, '.private', '.well-known', 'wp-content', 'googlecccfbf2f7e9e5ae4.html'];
        $moved = 0;
        @mkdir($dest . '/public_html/wp-content', 0750, true);
        foreach (scandir($pub) as $f) {
            if ($f === '.' || $f === '..' || in_array($f, $keep, true)) { continue; }
            if (rename($pub . '/' . $f, $dest . '/public_html/' . $f)) { $moved++; }
        }
        if (is_dir($pub . '/wp-content')) {
            foreach (scandir($pub . '/wp-content') as $f) {
                if ($f === '.' || $f === '..' || $f === 'uploads') { continue; }
                if (rename($pub . '/wp-content/' . $f, $dest . '/public_html/wp-content/' . $f)) { $moved++; }
            }
            file_put_contents($pub . '/wp-content/uploads/.htaccess', "# Uploaded media only — never execute scripts here\n<FilesMatch \"\\.(php|phtml|phar|pl|py|cgi|sh)$\">\n  Require all denied\n</FilesMatch>\nOptions -Indexes\n");
        }
        $out("Moved {$moved} WordPress files/folders to {$dest}/public_html (restore = move them back).");
        break;

    case 'extract':
        $zip = new ZipArchive();
        if ($zip->open($pub . '/' . PACKAGE) !== true) {
            $out('ERROR cannot open package');
            break;
        }
        $n = 0;
        for ($i = 0; $i < $zip->numFiles; $i++) {
            $name = $zip->getNameIndex($i);
            if ($name === false || str_contains($name, '..') || str_ends_with($name, '/')) { continue; }
            if (str_starts_with($name, 'app/')) {
                $target = $root . '/' . $name;
            } elseif (str_starts_with($name, 'public_html/')) {
                $target = $pub . '/' . substr($name, 12);
            } else {
                continue;
            }
            if (!is_dir(dirname($target))) { mkdir(dirname($target), 0755, true); }
            file_put_contents($target, $zip->getFromIndex($i));
            $n++;
        }
        $zip->close();
        @chmod($appDir . '/config.php', 0600);
        foreach (['logs', 'locks', 'cache', 'imports'] as $d) { @mkdir($appDir . '/storage/' . $d, 0750, true); }
        file_put_contents($appDir . '/.htaccess', "Require all denied\n");   // belt and braces: app/ is outside public_html anyway
        $out("Extracted {$n} files (app/ → {$appDir}, public_html/ → {$pub}).");
        break;

    case 'migrate':
        rt_boot($appDir);
        require_once $appDir . '/bin/migrate.php';
        $a = rt_migrate();
        $out($a ? 'Applied: ' . implode(', ', $a) : 'Database already up to date.');
        break;

    case 'seed':
        rt_boot($appDir);
        require_once $appDir . '/bin/seed-content.php';
        $r = rt_seed_content(true);
        $out("Articles {$r['articles']}, legacy Texas events {$r['legacy_events']}, redirects {$r['redirects']}, venues located {$r['venues_located']}.");
        break;

    case 'admin':
        rt_boot($appDir);
        if (!str_starts_with(ADMIN_HASH, '$2y$') && !str_starts_with(ADMIN_HASH, '$argon2')) { $out('No admin hash embedded.'); break; }
        $ex = RT\Db::val('SELECT id FROM admins WHERE email = ?', [ADMIN_EMAIL]);
        if ($ex) {
            RT\Db::update('admins', ['password_hash' => ADMIN_HASH], 'id = :id', ['id' => $ex]);
        } else {
            RT\Db::insert('admins', ['email' => ADMIN_EMAIL, 'name' => 'Owner', 'password_hash' => ADMIN_HASH, 'created_at' => gmdate('Y-m-d H:i:s')]);
        }
        $out('Administrator ready: ' . ADMIN_EMAIL);
        break;

    case 'import':
        rt_boot($appDir);
        $r = RT\Importer::run('manual', 'weekly', null, null, 'installer');
        $out("Import #{$r['run_id']} {$r['status']}: {$r['message']}");
        break;

    case 'cleanup':
        @unlink($pub . '/' . PACKAGE);
        $ok = @unlink(__FILE__);
        $out($ok ? 'Package and installer deleted.' : 'Could not delete installer — remove it by hand!');
        break;

    default:
        http_response_code(400);
        $out('Unknown step');
}
