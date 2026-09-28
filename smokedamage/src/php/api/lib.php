<?php
// SmokeDamage.com - shared server helpers (leads, settings, admin).
// Private data (leads, uploads, settings, redirects, admin credentials) lives in
// sd-private/ NEXT TO public_html, never inside it: this host ignores .htaccess,
// so nothing under public_html can be protected by server config.
if (realpath($_SERVER['SCRIPT_FILENAME'] ?? '') === realpath(__FILE__)) { http_response_code(404); exit; }

const SD_DEFAULTS = [
    'lead_recipient' => 'info@smokedamage.com',
    'popup_enabled' => true,
    'popup_delay_seconds' => 5,
    'phone_display' => '+1 (844) 537-1427',
    'email' => 'info@smokedamage.com',
    'company' => 'Rise Public Adjusting LLC',
    'license_number' => '3356839',
    'mail_from' => 'no-reply@smokedamage.com',
    'semrush_connected' => false,
];

function sd_private_dir(): ?string {
    static $dir = false;
    if ($dir !== false) return $dir;
    $candidates = [];
    if (getenv('SD_PRIVATE_DIR')) $candidates[] = getenv('SD_PRIVATE_DIR');
    $docroot = rtrim($_SERVER['DOCUMENT_ROOT'] ?? dirname(__DIR__), '/');
    $candidates[] = dirname($docroot) . '/sd-private';
    $candidates[] = dirname(__DIR__, 2) . '/sd-private';
    foreach ($candidates as $c) {
        if (is_dir($c) && is_writable($c)) return $dir = $c;
        if (!file_exists($c) && @mkdir($c, 0750, true)) return $dir = $c;
    }
    return $dir = null;
}

function sd_path(string $rel): ?string {
    $d = sd_private_dir();
    return $d ? $d . '/' . ltrim($rel, '/') : null;
}

function sd_read_json(string $rel, $default = []) {
    $p = sd_path($rel);
    if (!$p || !is_file($p)) return $default;
    $raw = @file_get_contents($p);
    $data = json_decode($raw ?: '', true);
    return is_array($data) ? $data : $default;
}

function sd_write_json(string $rel, $data): bool {
    $p = sd_path($rel);
    if (!$p) return false;
    if (!is_dir(dirname($p))) @mkdir(dirname($p), 0750, true);
    $tmp = $p . '.tmp' . bin2hex(random_bytes(4));
    if (@file_put_contents($tmp, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE), LOCK_EX) === false) return false;
    return @rename($tmp, $p);
}

function sd_settings(): array {
    $manifest = sd_read_json('site-manifest.json', []);
    $site = is_array($manifest['site'] ?? null) ? $manifest['site'] : [];
    return array_merge(SD_DEFAULTS, $site, sd_read_json('settings.json', []));
}

function sd_client_ip(): string {
    // TLS terminates upstream; the platform's proxy sets X-Forwarded-For.
    $xff = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? '';
    if ($xff) { $first = trim(explode(',', $xff)[0]); if (filter_var($first, FILTER_VALIDATE_IP)) return $first; }
    return $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
}

/** Sliding-window rate limit. Returns true when the action is allowed. */
function sd_rate_limit(string $bucket, int $max, int $window): bool {
    $key = 'ratelimit/' . $bucket . '-' . hash('sha256', sd_client_ip() . '|' . $bucket) . '.json';
    $now = time();
    $hits = array_values(array_filter(sd_read_json($key, []), fn($t) => is_int($t) && $t > $now - $window));
    if (count($hits) >= $max) return false;
    $hits[] = $now;
    sd_write_json($key, $hits);
    return true;
}

function sd_json(array $data, int $code = 200): void {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($data);
    exit;
}

function sd_clean(string $s, int $max): string {
    $s = trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $s) ?? '');
    return mb_substr($s, 0, $max);
}

function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }

// ------------------------------------------------------------------ admin auth
function sd_session_start(): void {
    if (session_status() === PHP_SESSION_ACTIVE) return;
    $sessDir = sd_path('sessions');
    if ($sessDir) { if (!is_dir($sessDir)) @mkdir($sessDir, 0700, true); session_save_path($sessDir); }
    session_name('sd_admin');
    session_set_cookie_params(['lifetime' => 0, 'path' => '/admin/', 'secure' => true, 'httponly' => true, 'samesite' => 'Strict']);
    session_start();
}

function sd_csrf(): string {
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(24));
    return $_SESSION['csrf'];
}

function sd_check_csrf(): bool {
    return isset($_POST['csrf'], $_SESSION['csrf']) && hash_equals($_SESSION['csrf'], (string)$_POST['csrf']);
}

function sd_admin_logged_in(): bool {
    return !empty($_SESSION['admin']) && ($_SESSION['admin_until'] ?? 0) > time();
}
