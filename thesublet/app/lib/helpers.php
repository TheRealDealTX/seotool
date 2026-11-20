<?php defined('APP') || exit;

const AMAZON_TAG = 'riseapartments-20';

function e($s): string
{
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function base_url(string $path = '/'): string
{
    return rtrim((string)cfg('base_url'), '/') . $path;
}

function redirect(string $to, int $code = 302): never
{
    header('Cache-Control: no-store');
    header('Location: ' . $to, true, $code);
    exit;
}

function cache_public(int $maxAge = 300): void
{
    header('Cache-Control: public, max-age=' . $maxAge);
}

function cache_private(): void
{
    header('Cache-Control: no-store, private');
    header('Pragma: no-cache');
}

function json_out($data, int $code = 200): never
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    if (!headers_sent() && !in_array('Cache-Control', array_map(fn($h) => strtok($h, ':'), headers_list()), true)) {
        cache_private();
    }
    echo json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    exit;
}

function client_ip(): string
{
    $xff = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? '';
    if ($xff !== '') {
        $ip = trim(explode(',', $xff)[0]);
        if (filter_var($ip, FILTER_VALIDATE_IP)) return $ip;
    }
    $rip = $_SERVER['HTTP_X_REAL_IP'] ?? '';
    if ($rip !== '' && filter_var($rip, FILTER_VALIDATE_IP)) return $rip;
    return $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
}

function is_post(): bool
{
    return ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST';
}

function post(string $k, $default = ''): string
{
    $v = $_POST[$k] ?? $default;
    return is_string($v) ? trim($v) : (string)$default;
}

function get(string $k, $default = ''): string
{
    $v = $_GET[$k] ?? $default;
    return is_string($v) ? trim($v) : (string)$default;
}

/* ---------- sessions, CSRF, flash ---------- */

function session_boot(): void
{
    if (session_status() === PHP_SESSION_ACTIVE) return;
    session_set_save_handler(new DbSessionHandler(), true);
    session_name('ts_sess');
    session_set_cookie_params([
        'lifetime' => 0, 'path' => '/', 'secure' => cfg('env') !== 'dev',
        'httponly' => true, 'samesite' => 'Lax',
    ]);
    ini_set('session.gc_maxlifetime', '1209600');
    ini_set('session.use_strict_mode', '1');
    session_start();
}

function csrf_token(): string
{
    session_boot();
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(32));
    return $_SESSION['csrf'];
}

function csrf_field(): string
{
    return '<input type="hidden" name="_csrf" value="' . e(csrf_token()) . '">';
}

/** Honeypot: a field humans never see. Must stay empty. */
function honeypot_field(): string
{
    return '<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="website_url" tabindex="-1" autocomplete="off"></label></div>';
}

/** Validates CSRF + honeypot + same-origin. Returns error string or null. */
function form_guard(): ?string
{
    session_boot();
    if (post('website_url') !== '') return 'Submission blocked.';
    $tok = $_POST['_csrf'] ?? '';
    if (!is_string($tok) || empty($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $tok)) {
        return 'Your session expired. Please reload the page and try again.';
    }
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if ($origin !== '' && $origin !== 'null') {
        $host = parse_url($origin, PHP_URL_HOST);
        if ($host && $host !== ($_SERVER['HTTP_HOST'] ?? '') && $host !== parse_url(cfg('base_url'), PHP_URL_HOST)) {
            return 'Cross-site submission blocked.';
        }
    }
    return null;
}

function flash(string $msg, string $type = 'ok'): void
{
    session_boot();
    $_SESSION['flash'][] = [$type, $msg];
}

function flashes(): string
{
    if (session_status() !== PHP_SESSION_ACTIVE && !isset($_COOKIE['ts_sess'])) return '';
    session_boot();
    $out = '';
    foreach ($_SESSION['flash'] ?? [] as [$t, $m]) {
        $out .= '<div class="flash flash-' . e($t) . '" role="status">' . e($m) . '</div>';
    }
    unset($_SESSION['flash']);
    return $out;
}

/* ---------- rate limiting ---------- */

/** True if allowed. Records the hit. */
function rate_limit(string $bucket, int $max, int $windowSec): bool
{
    $k = $bucket . ':' . client_ip();
    $since = gmdate('Y-m-d H:i:s', time() - $windowSec);
    $n = (int)val('SELECT COUNT(*) FROM rate_limits WHERE k = ? AND created_at > ?', [$k, $since]);
    if ($n >= $max) return false;
    insert('rate_limits', ['k' => $k, 'created_at' => now()]);
    if (random_int(1, 50) === 1) q('DELETE FROM rate_limits WHERE created_at < ?', [gmdate('Y-m-d H:i:s', time() - 86400 * 2)]);
    return true;
}

/* ---------- signing ---------- */

function sign(string $data): string
{
    return substr(hash_hmac('sha256', $data, (string)cfg('app_secret')), 0, 32);
}

function sign_ok(string $data, string $sig): bool
{
    return hash_equals(sign($data), $sig);
}

/* ---------- formatting ---------- */

function slugify(string $s, int $max = 70): string
{
    $s = strtolower(trim($s));
    $s = strtr($s, ['&' => ' and ', "'" => '', '’' => '']);
    if (function_exists('iconv')) {
        $t = @iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $s);
        if ($t !== false) $s = $t;
    }
    $s = preg_replace('/[^a-z0-9]+/', '-', $s);
    $s = trim(substr(trim($s, '-'), 0, $max), '-');
    return $s !== '' ? $s : 'listing';
}

function money($n): string
{
    return '$' . number_format((float)$n, 0);
}

function fmt_date(?string $d, string $f = 'M j, Y'): string
{
    if (!$d) return '';
    $t = strtotime($d);
    return $t ? date($f, $t) : '';
}

function excerpt(string $s, int $len = 160): string
{
    $s = trim(preg_replace('/\s+/', ' ', strip_tags(html_entity_decode($s, ENT_QUOTES, 'UTF-8'))));
    if (mb_strlen($s) <= $len) return $s;
    $cut = mb_substr($s, 0, $len);
    $sp = mb_strrpos($cut, ' ');
    return rtrim(mb_substr($cut, 0, $sp ?: $len), ' ,.;:') . '…';
}

function nl2p(string $text): string
{
    $parts = preg_split('/\n\s*\n/', trim(str_replace("\r", '', $text)));
    return implode('', array_map(fn($p) => '<p>' . nl2br(e(trim($p))) . '</p>', array_filter($parts, fn($p) => trim($p) !== '')));
}

/* ---------- Amazon affiliate ---------- */

function amazon_url(string $query): string
{
    return 'https://www.amazon.com/s?k=' . rawurlencode($query) . '&tag=' . AMAZON_TAG;
}

function amazon_block(array $items, string $heading = 'Handy for your stay'): string
{
    if (!$items) return '';
    $h = '<aside class="amz" aria-label="Recommended products"><h2 class="amz-h">' . e($heading) . '</h2><ul class="amz-list">';
    foreach ($items as $it) {
        $h .= '<li><a href="' . e(amazon_url($it['query'])) . '" target="_blank" rel="nofollow sponsored noopener">'
            . '<span class="amz-ico" aria-hidden="true">' . ($it['icon'] ?? '🛒') . '</span>'
            . '<span>' . e($it['label']) . '</span><span class="amz-go">View on Amazon →</span></a></li>';
    }
    $h .= '</ul><p class="amz-disc">As an Amazon Associate, The Sublet earns from qualifying purchases. Links are search results on Amazon; prices and availability change.</p></aside>';
    return $h;
}

function listing_amazon_items(array $l): array
{
    $base = [
        ['label' => 'Packing cubes', 'query' => 'packing cubes set', 'icon' => '🧳'],
        ['label' => 'Twin/full sheet set', 'query' => 'microfiber sheet set full', 'icon' => '🛏️'],
        ['label' => 'Over-door hooks & organizers', 'query' => 'over the door organizer hooks', 'icon' => '🪝'],
        ['label' => 'Portable door lock', 'query' => 'portable door lock travel', 'icon' => '🔒'],
        ['label' => 'Extension cord with USB', 'query' => 'power strip with usb flat plug', 'icon' => '🔌'],
        ['label' => 'Blackout curtains (no-drill)', 'query' => 'portable blackout curtain', 'icon' => '🌙'],
    ];
    if ($l['pets'] !== 'no') $base[] = ['label' => 'Travel pet bed', 'query' => 'travel pet bed portable', 'icon' => '🐾'];
    if (!$l['furnished']) $base[1] = ['label' => 'Air mattress / folding bed', 'query' => 'self inflating air mattress queen', 'icon' => '🛏️'];
    return array_slice($base, 0, 6);
}

/* ---------- misc ---------- */

function paginate(int $total, int $per, int $page): array
{
    $pages = max(1, (int)ceil($total / $per));
    $page = max(1, min($page, $pages));
    return ['page' => $page, 'pages' => $pages, 'offset' => ($page - 1) * $per, 'per' => $per, 'total' => $total];
}

function view(string $name, array $vars = []): string
{
    extract($vars, EXTR_SKIP);
    ob_start();
    require APPDIR . '/views/' . $name . '.php';
    return (string)ob_get_clean();
}

function not_found(string $msg = ''): never
{
    http_response_code(404);
    cache_public(300);
    page([
        'title' => 'Page not found | The Sublet',
        'description' => 'That page could not be found on The Sublet.',
        'robots' => 'noindex',
        'body' => view('notfound', ['msg' => $msg]),
    ]);
    exit;
}

function gone(): never
{
    http_response_code(410);
    cache_public(3600);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1"><title>410 Gone | The Sublet</title><link rel="stylesheet" href="/assets/css/site.css"></head><body><main class="wrap narrow" style="padding:4rem 1rem;text-align:center"><h1>This page is gone</h1><p>It was part of an older version of The Sublet and has been removed permanently.</p><p><a class="btn" href="/">Go to The Sublet homepage</a> <a class="btn btn-ghost" href="/sublets/">Browse sublets</a></p></main></body></html>';
    exit;
}

function valid_email(string $e): bool
{
    return (bool)filter_var($e, FILTER_VALIDATE_EMAIL) && strlen($e) <= 190;
}
