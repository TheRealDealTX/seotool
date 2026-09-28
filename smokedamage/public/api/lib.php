<?php
// SmokeDamage.com - shared server helpers (leads, settings, admin).
// Private data (leads, uploads, settings, redirects, admin credentials) lives in
// .h5g/sd-private/ NEXT TO public_html, never inside it: this host ignores .htaccess,
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
    // Hostinger Agency sites: the site home isn't writable, but .h5g/ beside public_html is.
    $candidates[] = dirname($docroot) . '/.h5g/sd-private';
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

// ------------------------------------------------------------------ email
/**
 * Send a plain-text email. Uses authenticated SMTP when configured in
 * Admin > Settings (this host's PHP mail() is not available), else mail().
 * Returns [bool ok, string info].
 */
function sd_send_mail(string $to, string $subject, string $body, string $replyTo = ''): array {
    $s = sd_settings();
    $encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
    $replyTo = preg_replace('/[\r\n]+/', '', $replyTo);
    if (!empty($s['smtp_host']) && !empty($s['smtp_user']) && !empty($s['smtp_pass'])) {
        return sd_smtp_send($s, $to, $encSubject, $body, $replyTo);
    }
    $from = filter_var($s['mail_from'] ?? '', FILTER_VALIDATE_EMAIL) ? $s['mail_from'] : 'no-reply@smokedamage.com';
    $hd = ['From' => 'SmokeDamage.com <' . $from . '>', 'Content-Type' => 'text/plain; charset=UTF-8'];
    if ($replyTo) $hd['Reply-To'] = $replyTo;
    $ok = @mail($to, $encSubject, $body, $hd);
    return [$ok, $ok ? 'mail()' : 'mail() unavailable - configure SMTP in Admin > Settings'];
}

function sd_smtp_send(array $s, string $to, string $encSubject, string $body, string $replyTo): array {
    $host = (string)$s['smtp_host'];
    $port = (int)($s['smtp_port'] ?? 465);
    $user = (string)$s['smtp_user'];
    $from = $user;
    $remote = ($port === 465 ? 'ssl://' : 'tcp://') . $host . ':' . $port;
    $fp = @stream_socket_client($remote, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]));
    if (!$fp) return [false, "SMTP connect failed: $errstr ($errno)"];
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) { $out = ''; while (($line = fgets($fp, 1024)) !== false) { $out .= $line; if (strlen($line) < 4 || $line[3] === ' ') break; } return $out; };
    $cmd = function (string $c, array $ok) use ($fp, $read) { if ($c !== '') fwrite($fp, $c . "\r\n"); $r = $read(); if (!in_array((int)substr($r, 0, 3), $ok, true)) throw new RuntimeException(trim($r) ?: 'no response'); return $r; };
    try {
        $cmd('', [220]);
        $cmd('EHLO smokedamage.com', [250]);
        if ($port === 587) {
            $cmd('STARTTLS', [220]);
            if (!stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) throw new RuntimeException('STARTTLS failed');
            $cmd('EHLO smokedamage.com', [250]);
        }
        $cmd('AUTH LOGIN', [334]);
        $cmd(base64_encode($user), [334]);
        $cmd(base64_encode((string)$s['smtp_pass']), [235]);
        $cmd('MAIL FROM:<' . $from . '>', [250]);
        $cmd('RCPT TO:<' . $to . '>', [250, 251]);
        $cmd('DATA', [354]);
        $headers = "From: SmokeDamage.com <$from>\r\nTo: <$to>\r\nSubject: $encSubject\r\nDate: " . date('r') . "\r\n"
            . ($replyTo ? "Reply-To: $replyTo\r\n" : '') . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n"
            . 'Message-ID: <' . bin2hex(random_bytes(8)) . '@smokedamage.com>' . "\r\n";
        $data = str_replace("\n.", "\n..", str_replace(["\r\n", "\r"], "\n", $body));
        $cmd($headers . "\r\n" . str_replace("\n", "\r\n", $data) . "\r\n.", [250]);
        $cmd('QUIT', [221]);
        fclose($fp);
        return [true, 'smtp'];
    } catch (Throwable $e) {
        @fclose($fp);
        return [false, 'SMTP: ' . substr($e->getMessage(), 0, 200)];
    }
}
