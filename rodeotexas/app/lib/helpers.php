<?php
/**
 * Small global helpers used by templates and library code.
 */
declare(strict_types=1);

/** Read a config value with dot notation: cfg('db.host'). */
function cfg(string $key, $default = null)
{
    $v = $GLOBALS['RT_CONFIG'];
    foreach (explode('.', $key) as $k) {
        if (!is_array($v) || !array_key_exists($k, $v)) {
            return $default;
        }
        $v = $v[$k];
    }
    return $v;
}

/** HTML-escape for text nodes and attribute values. */
function e($v): string
{
    return htmlspecialchars((string) ($v ?? ''), ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5, 'UTF-8');
}

/** Absolute URL on this site. */
function abs_url(string $path = '/'): string
{
    if (preg_match('~^https?://~i', $path)) {
        return $path;
    }
    return rtrim((string) cfg('base_url'), '/') . '/' . ltrim($path, '/');
}

/** Asset URL with cache-busting version from file modification time. */
function asset(string $path): string
{
    $path = ltrim($path, '/');
    $file = RT_PUBLIC . '/' . $path;
    $v = is_file($file) ? (string) filemtime($file) : '1';
    return '/' . $path . '?v=' . $v;
}

function now_utc(): string
{
    return gmdate('Y-m-d H:i:s');
}

function is_post(): bool
{
    return ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST';
}

function redirect(string $to, int $code = 302): void
{
    header('Location: ' . $to, true, $code);
    exit;
}

function json_out($data, int $code = 200): void
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

/** URL-safe slug. */
function slugify(string $s, int $max = 120): string
{
    $s = html_entity_decode($s, ENT_QUOTES | ENT_HTML5, 'UTF-8');
    if (function_exists('transliterator_transliterate')) {
        $t = transliterator_transliterate('Any-Latin; Latin-ASCII', $s);
        if (is_string($t)) {
            $s = $t;
        }
    }
    $s = strtolower($s);
    $s = str_replace(['&', "'", '’'], ['and', '', ''], $s);
    $s = preg_replace('/[^a-z0-9]+/', '-', $s) ?? '';
    $s = trim(substr(trim($s, '-'), 0, $max), '-');
    return $s !== '' ? $s : 'item';
}

/** Collapse whitespace and trim; returns null for empty strings. */
function clean_str($v, int $max = 0): ?string
{
    if ($v === null) {
        return null;
    }
    $s = trim(preg_replace('/\s+/u', ' ', (string) $v) ?? '');
    if ($max > 0 && mb_strlen($s) > $max) {
        $s = mb_substr($s, 0, $max);
    }
    return $s === '' ? null : $s;
}

/** Multi-line text: normalise newlines, trim, cap length. */
function clean_text($v, int $max = 5000): ?string
{
    if ($v === null) {
        return null;
    }
    $s = trim(str_replace(["\r\n", "\r"], "\n", (string) $v));
    $s = preg_replace("/\n{3,}/", "\n\n", $s) ?? '';
    if (mb_strlen($s) > $max) {
        $s = mb_substr($s, 0, $max);
    }
    return $s === '' ? null : $s;
}

/** Accept only absolute http(s) URLs. Returns normalized URL or null. */
function valid_url($v): ?string
{
    $v = clean_str($v, 500);
    if ($v === null) {
        return null;
    }
    if (!preg_match('~^https?://~i', $v) && preg_match('~^[a-z0-9.-]+\.[a-z]{2,}(/.*)?$~i', $v)) {
        $v = 'https://' . $v;
    }
    if (!filter_var($v, FILTER_VALIDATE_URL)) {
        return null;
    }
    $scheme = strtolower((string) parse_url($v, PHP_URL_SCHEME));
    return in_array($scheme, ['http', 'https'], true) ? $v : null;
}

function valid_email($v): ?string
{
    $v = clean_str($v, 255);
    return ($v !== null && filter_var($v, FILTER_VALIDATE_EMAIL)) ? $v : null;
}

/** Validate Y-m-d. */
function valid_date($v): ?string
{
    $v = clean_str($v, 10);
    if ($v === null || !preg_match('/^\d{4}-\d{2}-\d{2}$/', $v)) {
        return null;
    }
    [$y, $m, $d] = array_map('intval', explode('-', $v));
    return checkdate($m, $d, $y) ? $v : null;
}

function client_ip(): string
{
    // Hostinger terminates TLS in front of LiteSpeed; REMOTE_ADDR is the real client.
    return (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0');
}

function ip_hash(?string $ip = null): string
{
    return hash_hmac('sha256', $ip ?? client_ip(), (string) cfg('app_secret'));
}

function is_https(): bool
{
    return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https')
        || (($_SERVER['SERVER_PORT'] ?? '') === '443');
}

/** Current request path without query string, always starting with '/'. */
function request_path(): string
{
    $p = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
    return is_string($p) && $p !== '' ? $p : '/';
}

/** Build a query string from current GET merged with overrides (null removes). */
function qs(array $override = [], ?array $base = null): string
{
    $q = array_merge($base ?? $_GET, $override);
    $q = array_filter($q, static fn($v) => $v !== null && $v !== '' && $v !== []);
    return $q ? '?' . http_build_query($q) : '';
}

/** Plain-text excerpt. */
function excerpt(?string $text, int $len = 160): string
{
    $t = trim(preg_replace('/\s+/u', ' ', strip_tags((string) $text)) ?? '');
    if (mb_strlen($t) <= $len) {
        return $t;
    }
    $cut = mb_substr($t, 0, $len);
    $sp = mb_strrpos($cut, ' ');
    return rtrim(mb_substr($cut, 0, $sp ?: $len), ' ,.;:') . '…';
}

/** Log a line to app/storage/logs/<channel>.log */
function app_log(string $channel, string $msg): void
{
    $line = '[' . gmdate('Y-m-d H:i:s') . ' UTC] ' . $msg . "\n";
    @file_put_contents(RT_STORAGE . '/logs/' . preg_replace('/[^a-z0-9_-]/i', '', $channel) . '.log', $line, FILE_APPEND | LOCK_EX);
}

/** Send common security headers. */
function security_headers(bool $admin = false): void
{
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('Permissions-Policy: camera=(), microphone=(), geolocation=(self)');
    if (is_https()) {
        header('Strict-Transport-Security: max-age=31536000');
    }
    if ($admin) {
        header('X-Frame-Options: DENY');
        header("Content-Security-Policy: default-src 'self'; img-src 'self' data: https:; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'none'");
        header('Cache-Control: no-store');
        header('X-Robots-Tag: noindex, nofollow');
    } else {
        header('X-Frame-Options: SAMEORIGIN');
    }
}

/** Human labels for enumerations used across the site. */
function level_label(?string $level): string
{
    return [
        'professional' => 'Professional',
        'amateur'      => 'Amateur',
        'local'        => 'Local / community',
        'youth'        => 'Youth',
        'high_school'  => 'High school',
        'college'      => 'College',
    ][$level ?? ''] ?? 'Level not listed';
}

function levels(): array
{
    return ['professional', 'amateur', 'local', 'youth', 'high_school', 'college'];
}

if (!function_exists('array_is_list')) {
    /** PHP 8.0 polyfill (the cron PHP binary may be older than the web PHP). */
    function array_is_list(array $a): bool
    {
        $i = 0;
        foreach ($a as $k => $_) {
            if ($k !== $i++) {
                return false;
            }
        }
        return true;
    }
}
