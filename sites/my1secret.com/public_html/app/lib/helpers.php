<?php
declare(strict_types=1);
defined('M1S') || exit;

function e($s): string
{
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/** Absolute URL on the canonical host. */
function abs_url(string $path = '/'): string
{
    if (preg_match('#^https?://#', $path)) {
        return $path;
    }
    return rtrim(cfg('base_url'), '/') . '/' . ltrim($path, '/');
}

function redirect(string $to, int $code = 302): never
{
    header('Location: ' . $to, true, $code);
    if ($code === 301 || $code === 308) {
        header('Cache-Control: public, max-age=86400');
    } else {
        header('Cache-Control: no-store');
    }
    exit;
}

function back(string $fallback = '/'): never
{
    $ref = $_SERVER['HTTP_REFERER'] ?? '';
    $host = parse_url($ref, PHP_URL_HOST);
    if ($ref && $host === ($_SERVER['HTTP_HOST'] ?? '')) {
        redirect($ref);
    }
    redirect($fallback);
}

function is_post(): bool
{
    return ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST';
}

function input(string $key, string $default = ''): string
{
    $v = $_POST[$key] ?? $_GET[$key] ?? $default;
    return is_string($v) ? trim($v) : $default;
}

function wants_json(): bool
{
    return str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
}

function json_out(array $data, int $code = 200): never
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

/* ---------- CSRF ---------- */
function csrf_token(): string
{
    session_start_once();
    if (empty($_SESSION['csrf'])) {
        $_SESSION['csrf'] = bin2hex(random_bytes(32));
    }
    $GLOBALS['M1S_PRIVATE_PAGE'] = true;   // page carries a per-user token: never cache it
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="_csrf" value="' . e(csrf_token()) . '">';
}

function csrf_check(): void
{
    session_start_once();
    $t = $_POST['_csrf'] ?? $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
    if (!is_string($t) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $t)) {
        if (wants_json()) {
            json_out(['error' => 'Your session expired. Reload the page and try again.'], 419);
        }
        flash('error', 'Your session expired. Please try again.');
        back();
    }
}

/** Reject cross-site POSTs (Origin/Referer from another host). */
function same_origin_check(): void
{
    $src = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
    $u = $src !== '' ? parse_url($src) : [];
    $srcHost = strtolower(($u['host'] ?? '') . (isset($u['port']) ? ':' . $u['port'] : ''));
    if ($src !== '' && $srcHost !== strtolower($_SERVER['HTTP_HOST'] ?? '')) {
        http_response_code(403);
        exit('Cross-site request blocked.');
    }
}

/** CSRF field for members only (guests use same_origin_check, so no session is created). */
function member_csrf_field(): string
{
    return current_user() ? csrf_field() : '';
}

/* ---------- flash messages ---------- */
function flash(string $type, string $msg): void
{
    session_start_once();
    $_SESSION['flash'][] = [$type, $msg];
}

function take_flashes(): array
{
    if (!session_active_or_cookie()) {
        return [];
    }
    session_start_once();
    $f = $_SESSION['flash'] ?? [];
    unset($_SESSION['flash']);
    if ($f) {
        $GLOBALS['M1S_PRIVATE_PAGE'] = true;
    }
    return $f;
}

/* ---------- old form input (re-fill after validation errors) ---------- */
function remember_input(array $keys): void
{
    session_start_once();
    $_SESSION['old'] = array_intersect_key($_POST, array_flip($keys));
}

function old(string $key, string $default = ''): string
{
    static $old = null;
    if ($old === null) {
        $old = [];
        if (session_active_or_cookie()) {
            session_start_once();
            $old = $_SESSION['old'] ?? [];
            unset($_SESSION['old']);
        }
    }
    $v = $old[$key] ?? $default;
    return is_string($v) ? $v : $default;
}

/* ---------- misc ---------- */
function client_ip(): string
{
    return $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
}

function slugify(string $s, int $max = 70): string
{
    $s = mb_strtolower($s);
    if (function_exists('transliterator_transliterate')) {
        $s = transliterator_transliterate('Any-Latin; Latin-ASCII', $s) ?: $s;
    }
    $s = preg_replace('/[^a-z0-9]+/', '-', $s);
    $s = trim((string)$s, '-');
    if (strlen($s) > $max) {
        $s = substr($s, 0, $max);
        $s = substr($s, 0, strrpos($s, '-') ?: $max);
    }
    return $s !== '' ? $s : 'post';
}

function time_ago(string $datetime): string
{
    $t = strtotime($datetime . ' UTC');
    $d = time() - $t;
    if ($d < 60) return 'just now';
    if ($d < 3600) return floor($d / 60) . 'm ago';
    if ($d < 86400) return floor($d / 3600) . 'h ago';
    if ($d < 86400 * 30) return floor($d / 86400) . 'd ago';
    if ($d < 86400 * 365) return floor($d / (86400 * 30)) . 'mo ago';
    return floor($d / (86400 * 365)) . 'y ago';
}

function nice_date(string $datetime): string
{
    return gmdate('F j, Y', strtotime($datetime . ' UTC'));
}

function iso_date(string $datetime): string
{
    return gmdate('c', strtotime($datetime . ' UTC'));
}

function plural(int $n, string $one, ?string $many = null): string
{
    return number_format($n) . ' ' . ($n === 1 ? $one : ($many ?? $one . 's'));
}

function excerpt(string $text, int $len = 160): string
{
    $text = trim(preg_replace('/\s+/u', ' ', strip_tags($text)));
    if (mb_strlen($text) <= $len) {
        return $text;
    }
    $cut = mb_substr($text, 0, $len);
    $sp = mb_strrpos($cut, ' ');
    return rtrim(mb_substr($cut, 0, $sp ?: $len), ' ,.;:') . '…';
}

function page_num(): int
{
    $p = (int)($_GET['page'] ?? 1);
    return max(1, min($p, 1000));
}

/**
 * Simple fixed-window rate limit backed by the DB.
 * Returns true if the action is allowed (and records it).
 */
function throttle(string $action, int $max, int $windowSeconds, ?string $who = null): bool
{
    $key = $action . ':' . ($who ?? client_ip());
    $since = gmdate('Y-m-d H:i:s', time() - $windowSeconds);
    $n = (int)val('SELECT COUNT(*) FROM throttle WHERE k = ? AND created_at > ?', [$key, $since]);
    if ($n >= $max) {
        return false;
    }
    insert('throttle', ['k' => $key, 'created_at' => now()]);
    if (random_int(1, 50) === 1) {
        q('DELETE FROM throttle WHERE created_at < ?', [gmdate('Y-m-d H:i:s', time() - 86400 * 2)]);
    }
    return true;
}

/** Honeypot + minimum fill time for public forms. */
function bot_check_fields(): string
{
    $ts = time();
    $sig = hash_hmac('sha256', (string)$ts, cfg('secret'));
    return '<div class="hp" aria-hidden="true"><label>Leave this empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>'
         . '<input type="hidden" name="_ts" value="' . $ts . '"><input type="hidden" name="_tss" value="' . $sig . '">';
}

function bot_check_passes(int $minSeconds = 3): bool
{
    if (($_POST['website'] ?? '') !== '') {
        return false;
    }
    $ts = (int)($_POST['_ts'] ?? 0);
    $sig = (string)($_POST['_tss'] ?? '');
    if (!hash_equals(hash_hmac('sha256', (string)$ts, cfg('secret')), $sig)) {
        return false;
    }
    return (time() - $ts) >= $minSeconds && (time() - $ts) < 86400;
}

function setting(string $key, ?string $default = null): ?string
{
    static $cache = null;
    if ($cache === null) {
        $cache = [];
        foreach (all('SELECT k, v FROM settings') as $r) {
            $cache[$r['k']] = $r['v'];
        }
    }
    return $cache[$key] ?? $default;
}

function asset(string $path): string
{
    $file = M1S_ROOT . '/' . ltrim($path, '/');
    $v = is_file($file) ? substr(md5((string)filemtime($file) . filesize($file)), 0, 8) : M1S_VERSION;
    return '/' . ltrim($path, '/') . '?v=' . $v;
}

/* ---------- rendering ---------- */

/**
 * Render a view inside the layout.
 * $meta keys: title, description, canonical, robots, image, type, jsonld[], breadcrumbs[], body_class
 */
function render(string $view, array $data = [], array $meta = [], int $status = 200): never
{
    $content = view($view, $data);
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    send_security_headers();
    $layout = view('layout', ['content' => $content, 'meta' => $meta]);
    // Per-user pages must never be stored by the CDN or a shared cache.
    if (!empty($GLOBALS['M1S_PRIVATE_PAGE']) || current_user()) {
        header('Cache-Control: private, no-store');
    } else {
        header('Cache-Control: public, max-age=0, must-revalidate');
    }
    echo $layout;
    exit;
}

function view(string $name, array $data = []): string
{
    extract($data, EXTR_SKIP);
    ob_start();
    require M1S_APP . '/views/' . $name . '.php';
    return (string)ob_get_clean();
}

/** Per-request nonce for the few inline scripts we allow (Google Tag Manager). */
function csp_nonce(): string
{
    static $n = null;
    return $n ??= base64_encode(random_bytes(16));
}

function send_security_headers(): void
{
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('X-Frame-Options: SAMEORIGIN');
    header('Permissions-Policy: camera=(), microphone=(), geolocation=()');
    // Google Tag Manager / Analytics are allowed; inline scripts need the per-request nonce.
    // 'unsafe-eval' is required by GTM "Custom JavaScript" variables.
    $g = 'https://*.googletagmanager.com https://*.google-analytics.com https://*.analytics.google.com https://*.google.com https://*.doubleclick.net https://*.googleadservices.com';
    header("Content-Security-Policy: default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline' https://*.googletagmanager.com https://fonts.googleapis.com; "
        . "font-src 'self' data: https://fonts.gstatic.com; script-src 'self' 'nonce-" . csp_nonce() . "' 'unsafe-eval' $g; connect-src 'self' $g; "
        . "frame-src https://*.googletagmanager.com https://*.doubleclick.net; frame-ancestors 'self'; form-action 'self'; base-uri 'self'; object-src 'none'");
    if (($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https') {
        header('Strict-Transport-Security: max-age=31536000');
    }
}

function not_found(string $message = 'That page does not exist or was moved.'): never
{
    render('error', ['code' => 404, 'heading' => 'Page not found', 'message' => $message],
        ['title' => 'Page not found', 'robots' => 'noindex, follow'], 404);
}

function gone(): never
{
    render('error', ['code' => 410, 'heading' => 'This post has been removed',
        'message' => 'This old post is no longer part of My 1 Secret. Browse the latest guides or join a conversation in the community.'],
        ['title' => 'Removed', 'robots' => 'noindex, follow'], 410);
}

function forbidden(string $message = 'You do not have permission to do that.'): never
{
    if (wants_json()) {
        json_out(['error' => $message], 403);
    }
    render('error', ['code' => 403, 'heading' => 'Not allowed', 'message' => $message],
        ['title' => 'Not allowed', 'robots' => 'noindex'], 403);
}

/** Pagination links. $base must not contain ?page= */
function pager(int $page, bool $hasNext, string $base): string
{
    if ($page <= 1 && !$hasNext) {
        return '';
    }
    $sep = str_contains($base, '?') ? '&' : '?';
    $out = '<nav class="pager" aria-label="Pagination">';
    if ($page > 1) {
        $prev = $page - 1 === 1 ? $base : $base . $sep . 'page=' . ($page - 1);
        $out .= '<a class="btn btn-ghost" rel="prev" href="' . e($prev) . '">&larr; Previous</a>';
    }
    $out .= '<span class="pager-num">Page ' . $page . '</span>';
    if ($hasNext) {
        $out .= '<a class="btn btn-ghost" rel="next" href="' . e($base . $sep . 'page=' . ($page + 1)) . '">Next &rarr;</a>';
    }
    return $out . '</nav>';
}

function send_mail(string $to, string $subject, string $body): bool
{
    if (cfg('mail_log')) {   // local dev: write mail to a file instead of sending
        file_put_contents(cfg('mail_log'), "To: $to\nSubject: $subject\n\n$body\n----\n", FILE_APPEND);
        return true;
    }
    if (cfg('smtp')) {
        return smtp_send($to, $subject, $body);
    }
    $from = cfg('mail_from');
    $headers = 'From: ' . cfg('site_name') . ' <' . $from . ">\r\n"
             . 'Reply-To: ' . $from . "\r\n"
             . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\n";
    return @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers, '-f' . $from);
}
