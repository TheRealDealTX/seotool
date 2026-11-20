<?php defined('WCA') || exit;

function cfg(string $key, $default = null)
{
    $c = $GLOBALS['CFG'];
    foreach (explode('.', $key) as $k) {
        if (!is_array($c) || !array_key_exists($k, $c)) return $default;
        $c = $c[$k];
    }
    return $c;
}

/** Admin-editable setting (DB) falling back to config file. */
function setting(string $key, $default = null)
{
    static $cache = null;
    if ($cache === null) {
        $cache = [];
        try {
            foreach (db()->query('SELECT k, v FROM settings') as $r) $cache[$r['k']] = $r['v'];
        } catch (Throwable $e) { /* table may not exist yet */ }
    }
    if (isset($cache[$key]) && $cache[$key] !== '') return $cache[$key];
    return cfg($key, $default);
}

function setting_save(string $key, string $value): void
{
    db()->prepare('REPLACE INTO settings (k, v) VALUES (?, ?)')->execute([$key, $value]);
}

function e($s): string
{
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function url(string $path = ''): string
{
    return rtrim(cfg('site_url'), '/') . $path;
}

function asset(string $path): string
{
    $file = ROOT_DIR . '/assets/' . $path;
    $v = is_file($file) ? filemtime($file) : 1;
    return '/assets/' . $path . '?v=' . $v;
}

function redirect(string $to, int $code = 302): never
{
    header('Location: ' . $to, true, $code);
    exit;
}

function money($n): string
{
    return '$' . number_format((float)$n);
}

function slugify(string $s): string
{
    $s = strtolower(trim($s));
    $s = preg_replace('/[^a-z0-9]+/', '-', $s);
    return trim($s, '-') ?: 'listing';
}

function client_ip(): string
{
    return $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
}

/* ---------- Sessions, CSRF, flash ---------- */

function session_start_once(): void
{
    if (session_status() !== PHP_SESSION_ACTIVE) session_start();
}

function csrf_token(): string
{
    session_start_once();
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(16));
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="_csrf" value="' . e(csrf_token()) . '">';
}

function csrf_check(): void
{
    session_start_once();
    $t = $_POST['_csrf'] ?? '';
    if (!$t || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $t)) {
        http_response_code(400);
        exit('Your session expired. Please go back, refresh the page and try again.');
    }
}

/** Simple honeypot + timing check for public forms. */
function spam_check(): bool
{
    if (!empty($_POST['website_url'])) return false; // honeypot
    return true;
}

function honeypot_field(): string
{
    return '<div class="hp" aria-hidden="true"><label>Leave empty<input type="text" name="website_url" tabindex="-1" autocomplete="off"></label></div>';
}

function flash(string $type, string $msg): void
{
    session_start_once();
    $_SESSION['flash'][] = [$type, $msg];
}

function flashes(): array
{
    if (session_status() !== PHP_SESSION_ACTIVE && empty($_COOKIE[session_name()])) return [];
    session_start_once();
    $f = $_SESSION['flash'] ?? [];
    unset($_SESSION['flash']);
    return $f;
}

function post(string $k, $d = ''): string
{
    return trim((string)($_POST[$k] ?? $d));
}

function valid_email(string $e): bool
{
    return (bool)filter_var($e, FILTER_VALIDATE_EMAIL);
}

/* ---------- Auth ---------- */

function current_user(): ?array
{
    static $u = false;
    if ($u !== false) return $u;
    if (empty($_COOKIE[session_name()])) return $u = null;
    session_start_once();
    if (empty($_SESSION['uid'])) return $u = null;
    $st = db()->prepare('SELECT * FROM users WHERE id = ? AND verified_at IS NOT NULL');
    $st->execute([$_SESSION['uid']]);
    return $u = ($st->fetch() ?: null);
}

function login_user(int $id): void
{
    session_start_once();
    session_regenerate_id(true);
    $_SESSION['uid'] = $id;
}

function require_user(): array
{
    $u = current_user();
    if (!$u) {
        flash('info', 'Please sign in to continue.');
        redirect('/account/login/');
    }
    return $u;
}

function is_admin(): bool
{
    if (empty($_COOKIE[session_name()])) return false;
    session_start_once();
    return !empty($_SESSION['admin']);
}

function require_admin(): void
{
    if (!is_admin()) redirect('/admin/login/');
}

function sign_token(string $data): string
{
    return hash_hmac('sha256', $data, (string)cfg('app_key'));
}

function random_token(): string
{
    return bin2hex(random_bytes(24));
}

/* ---------- Rendering ---------- */

function partial(string $name, array $vars = []): void
{
    extract($vars, EXTR_SKIP);
    include APP_DIR . '/views/' . $name . '.php';
}

/**
 * Render a view inside the layout.
 * $meta: title, description, canonical, robots, image, schema (array of JSON-LD objects), breadcrumbs, nocache
 */
function render(string $view, array $vars = [], array $meta = [], int $status = 200): never
{
    http_response_code($status);
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('X-Frame-Options: SAMEORIGIN');
    if (!empty($meta['nocache']) || current_user() || is_admin()) {
        header('Cache-Control: private, no-store, max-age=0');
    } else {
        header('Cache-Control: public, max-age=300');
    }
    extract($vars, EXTR_SKIP);
    ob_start();
    include APP_DIR . '/views/' . $view . '.php';
    $content = ob_get_clean();
    include APP_DIR . '/views/layout.php';
    exit;
}

function not_found(): never
{
    render('pages/404', [], ['title' => 'Page Not Found', 'robots' => 'noindex, follow', 'nocache' => true], 404);
}

function gone(): never
{
    render('pages/410', [], ['title' => 'This Page Has Been Removed', 'robots' => 'noindex, follow', 'nocache' => true], 410);
}

function amazon_url(string $query): string
{
    return 'https://www.amazon.com/s?k=' . rawurlencode($query) . '&tag=' . rawurlencode((string)cfg('amazon_tag', 'riseapartments-20'));
}

function photo_url(string $key, bool $small = false): string
{
    if (str_starts_with($key, '/uploads/')) return $key; // owner-uploaded photo
    if (str_starts_with($key, 'placeholder-')) return '/assets/img/placeholders/' . $key . '.svg';
    return '/assets/img/photos/' . $key . ($small ? '-sm' : '') . '.webp';
}

function breadcrumb_schema(array $crumbs): array
{
    $items = [];
    foreach (array_values($crumbs) as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => url($path)];
    }
    return ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function time_ago(string $dt): string
{
    return date('M j, Y', strtotime($dt));
}
