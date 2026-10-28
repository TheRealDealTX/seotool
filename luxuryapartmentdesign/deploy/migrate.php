<?php
// One-time switchover, run once over HTTPS by deploy.sh and then deleted.
//   1. Dumps the WordPress database into the backup folder.
//   2. Moves every WordPress file in public_html into the backup folder.
//   3. Moves the new site out of the staging folder into public_html.
// Requires ?token=<the token baked in by deploy.sh>.

declare(strict_types=1);
header('Content-Type: application/json');
set_time_limit(600);

const TOKEN   = '__TOKEN__';
const BACKUP  = 'wp-backup-2026-10-28';
const STAGING = '_lad_new';
const KEEP    = ['.', '..', '.private', '.well-known', BACKUP, STAGING];

if (!hash_equals(TOKEN, (string) ($_GET['token'] ?? ''))) {
    http_response_code(403);
    exit('{"error":"forbidden"}');
}
$root = __DIR__;
$self = basename(__FILE__);
$log = [];
$step = $_GET['step'] ?? 'all';

function fail(string $msg, array $log): never
{
    http_response_code(500);
    echo json_encode(['error' => $msg, 'log' => $log], JSON_PRETTY_PRINT);
    exit;
}

if (!is_dir("$root/" . STAGING) || !is_file("$root/" . STAGING . '/index.php')) {
    fail('staging folder missing', $log);
}
if (!is_dir("$root/" . BACKUP) && !mkdir("$root/" . BACKUP, 0755)) {
    fail('cannot create backup folder', $log);
}

// 1. Database dump (credentials are read from wp-config.php, never printed)
if (in_array($step, ['all', 'db'], true) && is_file("$root/wp-config.php")) {
    $cfg = file_get_contents("$root/wp-config.php");
    $get = function (string $k) use ($cfg) {
        return preg_match("/define\(\s*['\"]" . $k . "['\"]\s*,\s*(['\"])(.*?)\\1\s*\)/s", $cfg, $m) ? stripcslashes($m[2]) : null;
    };
    $host = $get('DB_HOST') ?: 'localhost';
    $port = null;
    if (str_contains($host, ':')) [$host, $port] = explode(':', $host, 2);
    mysqli_report(MYSQLI_REPORT_OFF);
    $db = @new mysqli($host, (string) $get('DB_USER'), (string) $get('DB_PASSWORD'), (string) $get('DB_NAME'), $port ? (int) $port : 3306);
    if ($db->connect_errno) {
        fail('db connect failed: ' . $db->connect_error, $log);
    }
    $db->set_charset('utf8mb4');
    @mkdir("$root/" . BACKUP . '/database', 0755);
    $file = "$root/" . BACKUP . '/database/' . $get('DB_NAME') . '-2026-10-28.sql';
    $fh = fopen($file, 'w');
    fwrite($fh, "-- WordPress database backup of luxuryapartmentdesign.com, " . date('c') . "\nSET NAMES utf8mb4;\nSET FOREIGN_KEY_CHECKS=0;\n\n");
    $tables = 0;
    $rows = 0;
    $res = $db->query('SHOW TABLES');
    while ($t = $res->fetch_row()) {
        $table = $t[0];
        $create = $db->query("SHOW CREATE TABLE `$table`")->fetch_row()[1];
        fwrite($fh, "DROP TABLE IF EXISTS `$table`;\n$create;\n\n");
        $q = $db->query("SELECT * FROM `$table`", MYSQLI_USE_RESULT);
        $batch = [];
        while ($r = $q->fetch_row()) {
            $batch[] = '(' . implode(',', array_map(fn($v) => $v === null ? 'NULL' : "'" . $db->real_escape_string((string) $v) . "'", $r)) . ')';
            $rows++;
            if (count($batch) >= 200) {
                fwrite($fh, "INSERT INTO `$table` VALUES\n" . implode(",\n", $batch) . ";\n");
                $batch = [];
            }
        }
        if ($batch) {
            fwrite($fh, "INSERT INTO `$table` VALUES\n" . implode(",\n", $batch) . ";\n");
        }
        $q->free();
        fwrite($fh, "\n");
        $tables++;
    }
    fwrite($fh, "SET FOREIGN_KEY_CHECKS=1;\n");
    fclose($fh);
    $log[] = "database: $tables tables, $rows rows, " . filesize($file) . ' bytes';
}

if ($step === 'db') {
    echo json_encode(['ok' => true, 'log' => $log], JSON_PRETTY_PRINT);
    exit;
}

// 2. Move WordPress out of the web root
$moved = 0;
foreach (scandir($root) as $name) {
    if (in_array($name, KEEP, true) || $name === $self) continue;
    if (!rename("$root/$name", "$root/" . BACKUP . "/$name")) {
        fail("could not move $name", $log);
    }
    $moved++;
}
$log[] = "moved $moved WordPress entries into " . BACKUP;

if (is_file("$root/" . BACKUP . '/.htaccess')) {
    rename("$root/" . BACKUP . '/.htaccess', "$root/" . BACKUP . '/.htaccess.wordpress');  // keep the original
}
file_put_contents("$root/" . BACKUP . '/.htaccess', "# WordPress backup - not publicly accessible\nOptions -Indexes\nRequire all denied\n");
if (is_dir("$root/" . BACKUP . '/wp-content/uploads')) {
    file_put_contents("$root/" . BACKUP . '/wp-content/uploads/.htaccess', "# Old media URLs stay reachable via the /wp-content/uploads/ rewrite\nOptions -Indexes\nRequire all denied\n<FilesMatch \"\\.(webp|jpe?g|png|gif|svg|avif|pdf)$\">\nRequire all granted\n</FilesMatch>\n");
}
file_put_contents("$root/" . BACKUP . '/README.txt', "WordPress backup of luxuryapartmentdesign.com taken " . date('c') . ".\n\nThis folder holds every file that was in public_html, plus a SQL dump in database/.\nThe WordPress database itself was left untouched.\n\nTo restore WordPress: move the new site's files out of public_html, move everything in this\nfolder (except database/ and this README) back into public_html, then rename\n.htaccess.wordpress back to .htaccess (replacing the deny-all .htaccess written here).\n");

// 3. Promote the new site
$promoted = 0;
foreach (scandir("$root/" . STAGING) as $name) {
    if ($name === '.' || $name === '..') continue;
    if (file_exists("$root/$name")) {
        fail("target exists: $name", $log);
    }
    if (!rename("$root/" . STAGING . "/$name", "$root/$name")) {
        fail("could not promote $name", $log);
    }
    $promoted++;
}
@rmdir("$root/" . STAGING);
$log[] = "promoted $promoted new-site entries";

@unlink(__FILE__);
echo json_encode(['ok' => true, 'log' => $log], JSON_PRETTY_PRINT);
