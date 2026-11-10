<?php
// One-time installer. Requires app/config.php with a non-empty 'setup_token'.
// POST token=...&action=install (+ admin_name, admin_email, admin_username, admin_password)
//      token=...&action=archive_wordpress   -> moves leftover WordPress files out of the web root
//      token=...&action=selfdestruct        -> deletes this file
declare(strict_types=1);
header('Content-Type: application/json');

$config = @include __DIR__ . '/app/config.php';
$token = $_POST['token'] ?? '';
if (!is_array($config) || empty($config['setup_token']) || !is_string($token) || !hash_equals($config['setup_token'], $token)) {
    http_response_code(403);
    exit(json_encode(['error' => 'forbidden']));
}
$_SERVER['REQUEST_METHOD'] = 'GET'; // keep bootstrap quiet
require __DIR__ . '/app/bootstrap.php';

$action = $_POST['action'] ?? '';
$out = ['action' => $action];

if ($action === 'install') {
    migrate();
    $out['tables'] = array_column(all('SHOW TABLES'), array_key_first(all('SHOW TABLES')[0]));
    $email = strtolower(trim($_POST['admin_email'] ?? ''));
    $username = strtolower(trim($_POST['admin_username'] ?? ''));
    $pass = (string)($_POST['admin_password'] ?? '');
    if ($email && $username && strlen($pass) >= 8) {
        $existing = one('SELECT id FROM users WHERE email = ? OR username = ?', [$email, $username]);
        if ($existing) {
            q("UPDATE users SET role = 'admin', status = 'active', password_hash = ? WHERE id = ?", [password_hash($pass, PASSWORD_DEFAULT), $existing['id']]);
            $out['admin'] = 'updated #' . $existing['id'];
        } else {
            q("INSERT INTO users (email, username, password_hash, name, role, is_verified) VALUES (?, ?, ?, ?, 'admin', 1)",
                [$email, $username, password_hash($pass, PASSWORD_DEFAULT), trim($_POST['admin_name'] ?? 'Admin') ?: 'Admin']);
            $out['admin'] = 'created #' . db()->lastInsertId();
        }
    }
    // Optional property seed: JSON array of {name, address, city, state, zip, website, rent_min, rent_max, description, image_url}
    if (!empty($_POST['properties'])) {
        $list = json_decode((string)$_POST['properties'], true) ?: [];
        $added = 0;
        foreach ($list as $p) {
            if (empty($p['name']) || val('SELECT 1 FROM properties WHERE name = ?', [$p['name']])) continue;
            $img = null;
            if (!empty($p['image_url']) && preg_match('~^https://~', $p['image_url'])) {
                $data = @file_get_contents($p['image_url'], false, stream_context_create(['http' => ['timeout' => 15]]));
                if ($data && ($src = @imagecreatefromstring($data))) {
                    $w = imagesx($src); $h = imagesy($src); $r = min(1, 1600 / $w, 1000 / $h);
                    $dst = imagecreatetruecolor(max(1, (int)($w * $r)), max(1, (int)($h * $r)));
                    imagecopyresampled($dst, $src, 0, 0, 0, 0, imagesx($dst), imagesy($dst), $w, $h);
                    $img = bin2hex(random_bytes(12)) . '.jpg';
                    @mkdir(APP_ROOT . '/uploads/properties', 0755, true);
                    imagejpeg($dst, APP_ROOT . '/uploads/properties/' . $img, 85);
                }
            }
            q("INSERT INTO properties (name, slug, address, city, state, zip, website, rent_min, rent_max, description, amenities, image, status, is_featured) VALUES (?,?,?,?,?,?,?,?,?,?,?,?, 'approved', ?)", [
                $p['name'], unique_slug($p['name']), $p['address'] ?? null, $p['city'] ?? null, $p['state'] ?? null, $p['zip'] ?? null,
                $p['website'] ?? null, $p['rent_min'] ?? null, $p['rent_max'] ?? null, $p['description'] ?? null, $p['amenities'] ?? null, $img, !empty($p['featured']) ? 1 : 0,
            ]);
            $added++;
        }
        $out['properties_added'] = $added;
    }
    $out['ok'] = true;
} elseif ($action === 'archive_wordpress') {
    // Move WordPress leftovers to a sibling folder outside the public web root.
    $dest = dirname(dirname(__DIR__)) . '/roommate_wordpress_backup_' . date('Ymd_His');
    if (!is_dir(dirname($dest)) || !is_writable(dirname($dest))) {
        $dest = dirname(__DIR__) . '/../roommate_wordpress_backup_' . date('Ymd_His');
    }
    $keep = ['index.php', '.htaccess', 'app', 'assets', 'uploads', 'setup.php', '.private'];
    $moved = [];
    $failed = [];
    @mkdir($dest, 0750, true);
    foreach (scandir(__DIR__) as $f) {
        if ($f === '.' || $f === '..' || in_array($f, $keep, true)) continue;
        if (preg_match('/^(wp-|xmlrpc\.php|license\.txt|readme\.html|default\.php|\.htaccess\.bk|\.user\.ini|error_log)/', $f)) {
            if (@rename(__DIR__ . '/' . $f, $dest . '/' . $f)) $moved[] = $f; else $failed[] = $f;
        }
    }
    $out += ['backup_dir' => realpath($dest) ?: $dest, 'moved' => $moved, 'failed' => $failed, 'ok' => !$failed];
} elseif ($action === 'selfdestruct') {
    $out['ok'] = @unlink(__FILE__);
} elseif ($action === 'status') {
    $out['php'] = PHP_VERSION;
    $out['gd'] = extension_loaded('gd');
    $out['root'] = __DIR__;
    $out['files'] = array_values(array_diff(scandir(__DIR__), ['.', '..']));
    $out['db'] = (bool)val('SELECT 1');
    $out['ok'] = true;
} else {
    http_response_code(400);
    $out['error'] = 'unknown action';
}
echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
