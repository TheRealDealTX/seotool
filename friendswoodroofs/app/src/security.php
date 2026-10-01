<?php
declare(strict_types=1);

function is_https(): bool
{
    return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https')
        || ((int) ($_SERVER['SERVER_PORT'] ?? 0) === 443);
}

function send_security_headers(): void
{
    if (headers_sent()) {
        return;
    }
    $frame = 'https://www.rainviewer.com';
    header("Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
        . "frame-src {$frame}; connect-src 'self'; font-src 'self'; form-action 'self'; base-uri 'self'; "
        . "frame-ancestors 'self'; object-src 'none'");
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('X-Frame-Options: SAMEORIGIN');
    header('Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()');
    if (is_https()) {
        header('Strict-Transport-Security: max-age=31536000');
    }
}

/** Start the session only on pages that need it (forms, submit, thank-you). */
function ensure_session(): void
{
    if (session_status() === PHP_SESSION_ACTIVE) {
        return;
    }
    session_name('fr_sess');
    session_set_cookie_params([
        'lifetime' => 0,
        'path'     => '/',
        'secure'   => is_https(),
        'httponly' => true,
        'samesite' => 'Lax',
    ]);
    ini_set('session.use_strict_mode', '1');
    ini_set('session.use_only_cookies', '1');
    session_start();
}

function csrf_token(): string
{
    ensure_session();
    if (empty($_SESSION['csrf']) || !is_string($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf'];
}

function csrf_valid(?string $token): bool
{
    ensure_session();
    return is_string($token) && !empty($_SESSION['csrf']) && hash_equals((string) $_SESSION['csrf'], $token);
}

/** Persistent random secret used for signing and hashing (auto-created). */
function app_secret(): string
{
    static $secret = null;
    if ($secret !== null) {
        return $secret;
    }
    $file = FR_APP . '/storage/secret.key';
    if (is_file($file)) {
        $secret = trim((string) file_get_contents($file));
    }
    if (empty($secret)) {
        $secret = bin2hex(random_bytes(32));
        @file_put_contents($file, $secret, LOCK_EX);
        @chmod($file, 0600);
    }
    return $secret;
}

/** Signed form-render timestamp, used to reject instant bot submissions. */
function form_timestamp_token(): string
{
    $ts = (string) time();
    return $ts . '.' . hash_hmac('sha256', $ts, app_secret());
}

/** Seconds since the form was rendered, or null if the token is invalid. */
function form_age(?string $token): ?int
{
    if (!is_string($token) || !preg_match('/^(\d{10})\.([a-f0-9]{64})$/', $token, $m)) {
        return null;
    }
    if (!hash_equals(hash_hmac('sha256', $m[1], app_secret()), $m[2])) {
        return null;
    }
    return time() - (int) $m[1];
}

function storage_dir(string $sub): string
{
    $dir = FR_APP . '/storage/' . $sub;
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
    if (!is_writable($dir)) {
        $dir = rtrim(sys_get_temp_dir(), '/') . '/fr-' . $sub;
        if (!is_dir($dir)) {
            @mkdir($dir, 0700, true);
        }
    }
    return $dir;
}

/**
 * Sliding-window rate limit per visitor (IP is hashed, never stored).
 * Returns true if the action is allowed and records it.
 */
function rate_limit_allow(string $action, int $max, int $windowSeconds): bool
{
    $key  = hash('sha256', $action . '|' . client_ip() . '|' . app_secret());
    $file = storage_dir('ratelimit') . '/' . $key . '.json';
    $fh = @fopen($file, 'c+');
    if (!$fh) {
        return true; // fail open rather than block real customers
    }
    flock($fh, LOCK_EX);
    $now  = time();
    $hits = json_decode((string) stream_get_contents($fh), true);
    $hits = array_values(array_filter(is_array($hits) ? $hits : [], fn ($t) => is_int($t) && $t > $now - $windowSeconds));
    $allowed = count($hits) < $max;
    if ($allowed) {
        $hits[] = $now;
    }
    ftruncate($fh, 0);
    rewind($fh);
    fwrite($fh, json_encode($hits));
    flock($fh, LOCK_UN);
    fclose($fh);

    // Occasionally prune stale files.
    if (random_int(1, 50) === 1) {
        foreach (glob(dirname($file) . '/*.json') ?: [] as $f) {
            if (filemtime($f) < $now - 86400) {
                @unlink($f);
            }
        }
    }
    return $allowed;
}

/** Remove control characters (incl. CR/LF) from single-line input. */
function clean_line(mixed $value, int $max): string
{
    $value = is_string($value) ? $value : '';
    $value = (string) preg_replace('/[\x00-\x1F\x7F]+/u', ' ', $value);
    $value = trim((string) preg_replace('/\s+/u', ' ', $value));
    return mb_substr($value, 0, $max);
}

/** Multi-line text: keep newlines, drop other control characters. */
function clean_text(mixed $value, int $max): string
{
    $value = is_string($value) ? $value : '';
    $value = str_replace(["\r\n", "\r"], "\n", $value);
    $value = (string) preg_replace('/[\x00-\x09\x0B-\x1F\x7F]+/u', ' ', $value);
    $value = (string) preg_replace("/\n{3,}/", "\n\n", $value);
    return mb_substr(trim($value), 0, $max);
}

function app_log(string $channel, string $message): void
{
    $line = '[' . date('c') . '] ' . $message . "\n";
    @file_put_contents(storage_dir('logs') . '/' . $channel . '.log', $line, FILE_APPEND | LOCK_EX);
}
