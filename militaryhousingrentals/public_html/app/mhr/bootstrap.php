<?php
// Listing add-on: claims, paid/free submissions, owner accounts, Stripe and the
// admin panel. Loaded from app/lib.php. Everything lives in app/mhr/ (the web
// server refuses /app/), secrets live in ../private/config.php outside
// public_html, and all state is in MySQL. Existing listings stay in
// app/data/listings.json; this layer only adds to them.

const MHR = __DIR__;
const MHR_SCHEMA_VERSION = 1;

require MHR . '/listings.php';
require MHR . '/mailer.php';
require MHR . '/stripe.php';
require MHR . '/images.php';
require MHR . '/routes.php';
require MHR . '/submit.php';
require MHR . '/editor.php';

function mhr_cfg($key = null) {
    static $c;
    if ($c === null) {
        $f = getenv('MHR_CONFIG') ?: dirname(__DIR__, 3) . '/private/config.php';
        $c = is_file($f) ? (require $f) : [];
        if (!is_array($c)) $c = [];
    }
    if ($key === null) return $c;
    $v = $c;
    foreach (explode('.', $key) as $k) { if (!is_array($v) || !array_key_exists($k, $v)) return null; $v = $v[$k]; }
    return $v;
}

function mhr_admin_path() { return '/' . trim(mhr_cfg('admin_path') ?: 'admin', '/') . '/'; }

// ---------------------------------------------------------------- database

class MhrDbUnavailable extends RuntimeException {}

function mhr_db() {
    static $pdo = false;
    if ($pdo instanceof PDO) return $pdo;
    if ($pdo === null) throw new MhrDbUnavailable('Database unavailable');
    $d = mhr_cfg('db');
    if (!$d || empty($d['name'])) { $pdo = null; throw new MhrDbUnavailable('Database not configured'); }
    try {
        $pdo = new PDO(sprintf('mysql:host=%s;port=%d;dbname=%s;charset=utf8mb4', $d['host'] ?? '127.0.0.1', $d['port'] ?? 3306, $d['name']),
            $d['user'], $d['pass'], [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
                PDO::ATTR_TIMEOUT => 5,
            ]);
        $pdo->exec("SET time_zone = '+00:00'");
        mhr_migrate($pdo);
    } catch (PDOException $e) {
        error_log('mhr db: ' . $e->getMessage());
        $pdo = null;
        throw new MhrDbUnavailable('Database unavailable', 0, $e);
    }
    return $pdo;
}

function mhr_q($sql, array $args = []) {
    $st = mhr_db()->prepare($sql);
    $st->execute($args);
    return $st;
}
function mhr_row($sql, array $args = []) { $r = mhr_q($sql, $args)->fetch(); return $r ?: null; }
function mhr_all($sql, array $args = []) { return mhr_q($sql, $args)->fetchAll(); }
function mhr_now() { return gmdate('Y-m-d H:i:s'); }

function mhr_migrate(PDO $pdo) {
    $pdo->exec('CREATE TABLE IF NOT EXISTS mhr_settings (k VARCHAR(64) PRIMARY KEY, v MEDIUMTEXT NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4');
    $ver = (int)($pdo->query("SELECT v FROM mhr_settings WHERE k = 'schema_version'")->fetchColumn() ?: 0);
    if ($ver < 1) {
        foreach (explode(';', file_get_contents(MHR . '/schema.sql')) as $sql) if (trim($sql) !== '') $pdo->exec($sql);
        $pdo->prepare("REPLACE INTO mhr_settings (k, v) VALUES ('schema_version', ?)")->execute([MHR_SCHEMA_VERSION]);
        mhr_import_message_log($pdo);
    }
    // First admin comes from the private config (a password hash, never a password).
    $boot = mhr_cfg('bootstrap_admin');
    if ($boot && !empty($boot['username']) && !empty($boot['password_hash'])
        && !(int)$pdo->query('SELECT COUNT(*) FROM mhr_admins')->fetchColumn()) {
        $pdo->prepare('INSERT INTO mhr_admins (username, pass_hash, created_at) VALUES (?, ?, ?)')
            ->execute([$boot['username'], $boot['password_hash'], mhr_now()]);
    }
}

// Copy the messages the old forms appended to app/storage/submissions.log.
function mhr_import_message_log(PDO $pdo) {
    $f = APP . '/storage/submissions.log';
    if (!is_file($f)) return;
    $ins = $pdo->prepare('INSERT INTO mhr_messages (kind, name, email, phone, subject, body, ip, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
    foreach (file($f, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $m = json_decode($line, true);
        if (!is_array($m)) continue;
        $kind = $m['kind'] ?? 'contact';
        $subject = $kind === 'contact' ? ($m['topic'] ?? '') : ('Property: ' . ($m['pname'] ?? ''));
        $at = isset($m['at']) ? gmdate('Y-m-d H:i:s', strtotime($m['at'])) : mhr_now();
        $body = array_diff_key($m, array_flip(['kind', 'at', 'ip', 'name', 'email', 'phone']));
        $ins->execute([$kind, mb_substr($m['name'] ?? '', 0, 190), mb_substr($m['email'] ?? '', 0, 190), mb_substr($m['phone'] ?? '', 0, 60),
            mb_substr($subject, 0, 255), json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), $m['ip'] ?? null, $at]);
    }
}

// ---------------------------------------------------------------- settings

function mhr_setting($k, $default = null) {
    static $cache = null;
    if ($cache === null) {
        try { $cache = array_column(mhr_all('SELECT k, v FROM mhr_settings'), 'v', 'k'); }
        catch (MhrDbUnavailable $e) { $cache = []; }
    }
    return array_key_exists($k, $cache) ? $cache[$k] : $default;
}
function mhr_setting_set($k, $v) {
    mhr_q('REPLACE INTO mhr_settings (k, v) VALUES (?, ?)', [$k, (string)$v]);
}
function mhr_secret_setting($k) {
    $v = mhr_setting($k, '');
    return $v === '' ? '' : (mhr_decrypt($v) ?? '');
}
function mhr_price_cents() { return max(50, (int)mhr_setting('price_cents', 1000)); }
function mhr_price_label() { return '$' . rtrim(rtrim(number_format(mhr_price_cents() / 100, 2), '0'), '.'); }
function mhr_notify_email() { return mhr_setting('notify_email', '') ?: (mhr_cfg('notify_email') ?: cfg('email')); }

// Settings secrets (Stripe keys) are encrypted at rest with the app secret.
function mhr_key() {
    $s = (string)mhr_cfg('app_secret');
    if (strlen($s) < 32) throw new RuntimeException('app_secret missing from private config');
    return hash('sha256', 'mhr-enc|' . $s, true);
}
function mhr_encrypt($plain) {
    $iv = random_bytes(12);
    $ct = openssl_encrypt($plain, 'aes-256-gcm', mhr_key(), OPENSSL_RAW_DATA, $iv, $tag);
    return 'v1:' . base64_encode($iv . $tag . $ct);
}
function mhr_decrypt($enc) {
    if (!str_starts_with($enc, 'v1:')) return null;
    $raw = base64_decode(substr($enc, 3), true);
    if ($raw === false || strlen($raw) < 29) return null;
    $p = openssl_decrypt(substr($raw, 28), 'aes-256-gcm', mhr_key(), OPENSSL_RAW_DATA, substr($raw, 0, 12), substr($raw, 12, 16));
    return $p === false ? null : $p;
}
function mhr_hmac($data) { return hash_hmac('sha256', $data, 'mhr-sig|' . mhr_cfg('app_secret')); }

// ---------------------------------------------------------------- http, session, forms

function mhr_is_https() {
    return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || strtolower($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https'
        || (int)($_SERVER['SERVER_PORT'] ?? 0) === 443;
}

function mhr_session_start() {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    ini_set('session.use_strict_mode', '1');
    ini_set('session.use_only_cookies', '1');
    session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'secure' => mhr_is_https() || !mhr_cfg('dev'),
        'httponly' => true, 'samesite' => 'Lax']);
    session_start();
}

function mhr_private_headers() {
    header('Cache-Control: no-store, no-cache, must-revalidate, private');
    header('Pragma: no-cache');
    header('X-Robots-Tag: noindex, nofollow');
}

function mhr_csrf() { mhr_session_start(); return $_SESSION['csrf'] ??= bin2hex(random_bytes(16)); }

function mhr_guard_fields($timed = true) {
    return '<input type="hidden" name="csrf" value="' . e(mhr_csrf()) . '">'
        . ($timed ? '<input type="hidden" name="t" value="' . time() . '">' : '')
        . '<label class="hp" aria-hidden="true">Leave this empty <input type="text" name="website_url" tabindex="-1" autocomplete="off"></label>';
}

// Returns null when fine, 'honeypot' for bots (callers pretend success), or an error message.
function mhr_guard_check($timed = true) {
    mhr_session_start();
    if (!hash_equals($_SESSION['csrf'] ?? '', (string)($_POST['csrf'] ?? ''))) return 'Your session expired. Please reload the page and try again.';
    if (!empty($_POST['website_url'])) return 'honeypot';
    if ($timed && time() - (int)($_POST['t'] ?? 0) < 3) return 'Please take a moment to fill out the form.';
    return null;
}

function mhr_post($k, $max = 300) {
    $v = trim(str_replace(["\r\n", "\r"], "\n", (string)($_POST[$k] ?? '')));
    return mb_substr($v, 0, $max);
}
function mhr_line($k, $max = 300) { return str_replace("\n", ' ', mhr_post($k, $max)); }

function mhr_redirect($to, $code = 303) { header('Location: ' . $to, true, $code); exit; }

function mhr_flash($msg = null, $type = 'ok') {
    mhr_session_start();
    if ($msg !== null) { $_SESSION['mhr_flash'][] = [$type, $msg]; return ''; }
    $out = '';
    foreach ($_SESSION['mhr_flash'] ?? [] as [$t, $m]) $out .= '<div class="notice notice-' . ($t === 'ok' ? 'ok' : 'err') . '" role="' . ($t === 'ok' ? 'status' : 'alert') . '">' . e($m) . '</div>';
    unset($_SESSION['mhr_flash']);
    return $out;
}

function mhr_errors_html(array $errors) {
    if (!$errors) return '';
    return '<div class="notice notice-err" role="alert"><strong>Please fix the following:</strong><ul>'
        . implode('', array_map(fn($x) => '<li>' . e($x) . '</li>', $errors)) . '</ul></div>';
}

function mhr_client_ip() { return substr((string)($_SERVER['REMOTE_ADDR'] ?? ''), 0, 45); }

function mhr_css_link() {
    $f = dirname(APP) . '/assets/css/mhr.css';
    return '<link rel="stylesheet" href="/assets/css/mhr.css?v=' . (is_file($f) ? substr(md5_file($f), 0, 8) : '1') . '">';
}

// Page shell for the add-on's public pages: the site layout, noindex, no-store.
function mhr_page_start($title, $path, array $extra = []) {
    mhr_private_headers();
    layout_start($extra + ['title' => $title, 'path' => $path, 'robots' => 'noindex, nofollow',
        'description' => $extra['description'] ?? $title, 'head_extra' => mhr_css_link()]);
}

// ---------------------------------------------------------------- owners

function mhr_owner_by_email($email) { return mhr_row('SELECT * FROM mhr_owners WHERE email = ?', [mb_strtolower(trim($email))]); }
function mhr_owner($id) { return $id ? mhr_row('SELECT * FROM mhr_owners WHERE id = ?', [$id]) : null; }

function mhr_owner_find_or_create($name, $email) {
    $email = mb_strtolower(trim($email));
    if ($o = mhr_owner_by_email($email)) {
        if ($name !== '' && $o['name'] === '') mhr_q('UPDATE mhr_owners SET name = ? WHERE id = ?', [$name, $o['id']]);
        return mhr_owner($o['id']);
    }
    mhr_q('INSERT INTO mhr_owners (name, email, created_at) VALUES (?, ?, ?)', [$name, $email, mhr_now()]);
    return mhr_owner((int)mhr_db()->lastInsertId());
}

// One-time tokens for email links. Only a hash is stored.
function mhr_token_create($owner_id, $purpose, $ttl) {
    $t = bin2hex(random_bytes(24));
    mhr_q('INSERT INTO mhr_tokens (owner_id, purpose, token_hash, expires_at, created_at) VALUES (?, ?, ?, ?, ?)',
        [$owner_id, $purpose, hash('sha256', $t), gmdate('Y-m-d H:i:s', time() + $ttl), mhr_now()]);
    return $t;
}
function mhr_token_consume($t) {
    if (!preg_match('/^[a-f0-9]{48}$/', $t)) return null;
    $db = mhr_db();
    $db->beginTransaction();
    $row = mhr_row('SELECT * FROM mhr_tokens WHERE token_hash = ? FOR UPDATE', [hash('sha256', $t)]);
    if (!$row || $row['used_at'] || strtotime($row['expires_at'] . ' UTC') < time()) { $db->rollBack(); return null; }
    mhr_q('UPDATE mhr_tokens SET used_at = ? WHERE id = ?', [mhr_now(), $row['id']]);
    $db->commit();
    return $row;
}

function mhr_owner_login($owner_id) {
    mhr_session_start();
    session_regenerate_id(true);
    $_SESSION['mhr_owner'] = (int)$owner_id;
    mhr_q('UPDATE mhr_owners SET last_login_at = ? WHERE id = ?', [mhr_now(), $owner_id]);
}
function mhr_current_owner() {
    mhr_session_start();
    $id = $_SESSION['mhr_owner'] ?? 0;
    if (!$id) return null;
    $o = mhr_owner($id);
    if (!$o || $o['status'] !== 'active') { unset($_SESSION['mhr_owner']); return null; }
    return $o;
}

function mhr_send_login_link($owner, $purpose = 'login') {
    $ttl = $purpose === 'verify' ? 7 * 86400 : 1800;
    $t = mhr_token_create($owner['id'], $purpose, $ttl);
    $url = abs_url('/account/verify/?t=' . $t);
    if ($purpose === 'verify') {
        $subject = 'Confirm your email for ' . cfg('name');
        $body = "Hi " . ($owner['name'] ?: 'there') . ",\n\nPlease confirm your email address to activate your owner account on " . cfg('name') . ".\n\n$url\n\n"
            . "This link also signs you in to your owner dashboard, where you can edit your listing and upload photos. It works once and expires in 7 days.\n\n"
            . "If you didn't request this, you can ignore this email.\n\n— " . cfg('name');
    } else {
        $subject = 'Your sign-in link for ' . cfg('name');
        $body = "Hi " . ($owner['name'] ?: 'there') . ",\n\nUse this link to sign in to your owner dashboard:\n\n$url\n\n"
            . "It works once and expires in 30 minutes. If you didn't ask to sign in, you can ignore this email.\n\n— " . cfg('name');
    }
    return mhr_mail($owner['email'], $subject, $body);
}

function mhr_log_message($kind, $name, $email, $phone, $subject, array $body) {
    try {
        mhr_q('INSERT INTO mhr_messages (kind, name, email, phone, subject, body, ip, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [
            $kind, mb_substr($name, 0, 190), mb_substr($email, 0, 190), mb_substr($phone, 0, 60), mb_substr($subject, 0, 255),
            json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), mhr_client_ip(), mhr_now()]);
    } catch (Throwable $e) { error_log('mhr message log: ' . $e->getMessage()); }
}
