<?php defined('SNW') || (http_response_code(404) && exit);
/*
 * Lead forms (buy, sell, contact, showing request, newsletter).
 * All post to /submit/. Protection: CSRF token (session), honeypot field,
 * minimum fill time, per-IP rate limit. Leads are emailed to cfg('email') and
 * appended to a guarded PHP log in cfg('storage_dir').
 */

const FORM_FIELDS = [
    'buy'        => ['first_name', 'last_name', 'email', 'phone', 'property_type', 'neighborhood', 'budget', 'beds', 'baths', 'timeline', 'message'],
    'sell'       => ['first_name', 'last_name', 'email', 'phone', 'address', 'neighborhood', 'zip', 'property_type', 'beds', 'baths', 'estimated_price', 'timeline', 'message'],
    'contact'    => ['first_name', 'last_name', 'email', 'phone', 'interest', 'message'],
    'showing'    => ['first_name', 'last_name', 'email', 'phone', 'listing', 'preferred_time', 'message'],
    'newsletter' => ['email'],
];
const FORM_LABELS = [
    'buy' => 'Home buyer inquiry', 'sell' => 'Home seller inquiry', 'contact' => 'Contact form',
    'showing' => 'Showing request', 'newsletter' => 'Newsletter signup',
];

function is_https(): bool
{
    return ($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
}

/** Server secret for stateless form tokens (no sessions, so CDN-cached pages still submit). */
function form_secret(): string
{
    static $s = null;
    if ($s !== null) return $s;
    $dir = storage_dir();
    $f = $dir ? $dir . '/secret.php' : null;
    if ($f && is_file($f)) $s = (string) (include $f);
    if (!$s) {
        $s = bin2hex(random_bytes(32));
        if ($f) @file_put_contents($f, "<?php return '" . $s . "';\n", LOCK_EX);
        else $s = hash('sha256', __FILE__ . php_uname());
    }
    return $s;
}

/** Hidden inputs every form needs. */
function form_guard(string $form): string
{
    $t = time();
    $sig = hash_hmac('sha256', $form . '|' . $t, form_secret());
    return '<input type="hidden" name="form" value="' . e($form) . '">'
        . '<input type="hidden" name="ts" value="' . $t . '">'
        . '<input type="hidden" name="token" value="' . $sig . '">'
        . '<div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>';
}

function storage_dir(): ?string
{
    $dir = cfg('storage_dir');
    if (!is_dir($dir)) @mkdir($dir, 0750, true);
    if (is_dir($dir) && is_writable($dir)) return $dir;
    // Fallback inside the app tree; files are .php with an exit guard so they are never readable over HTTP.
    $dir = APP . '/storage';
    if (!is_dir($dir)) @mkdir($dir, 0750, true);
    return is_writable($dir) ? $dir : null;
}

function rate_limited(string $ip): bool
{
    $dir = storage_dir();
    if (!$dir) return false;
    $f = $dir . '/rate-' . md5($ip . form_secret()) . '.php';
    $hits = array_filter(array_slice(explode("\n", (string) @file_get_contents($f)), 1), fn($t) => $t !== '' && (int) $t > time() - 3600);
    if (count($hits) >= 8) return true;
    $hits[] = (string) time();
    @file_put_contents($f, "<?php exit; ?>\n" . implode("\n", $hits), LOCK_EX);
    return false;
}

function handle_submit(): void
{
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') redirect('/contact-seattle-real-estate-agents/');
    $form = $_POST['form'] ?? '';
    $back = $_SERVER['HTTP_REFERER'] ?? '/';
    $back = parse_url($back, PHP_URL_PATH) ?: '/';
    if (!isset(FORM_FIELDS[$form])) { http_response_code(400); exit('Invalid form.'); }

    $ts = (int) ($_POST['ts'] ?? 0);
    $ok = hash_equals(hash_hmac('sha256', $form . '|' . $ts, form_secret()), (string) ($_POST['token'] ?? ''))
        && $ts > time() - 14 * 86400;
    $bot = ($_POST['website'] ?? '') !== '' || ($ts && time() - $ts < 3);
    if ($bot) redirect('/thank-you/', 303);               // silently drop, look successful
    if (!$ok) redirect($back . '?err=expired#form', 303);
    if (rate_limited(client_ip())) redirect($back . '?err=limit#form', 303);

    $data = [];
    foreach (FORM_FIELDS[$form] as $f) {
        $v = trim((string) ($_POST[$f] ?? ''));
        $v = str_replace(["\r", "\0"], '', $v);
        $data[$f] = mb_substr($v, 0, $f === 'message' ? 4000 : 200);
    }
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) redirect($back . '?err=email#form', 303);

    $lead = ['form' => $form, 'time' => date('c'), 'page' => $back, 'ip' => client_ip()] + $data;
    if ($dir = storage_dir()) {
        $file = $dir . '/leads-' . date('Y-m') . '.php';
        if (!is_file($file)) @file_put_contents($file, "<?php exit; ?>\n");
        @file_put_contents($file, json_encode($lead, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n", FILE_APPEND | LOCK_EX);
    }

    $lines = [];
    foreach ($data as $k => $v) if ($v !== '') $lines[] = ucwords(str_replace('_', ' ', $k)) . ': ' . $v;
    $lines[] = '';
    $lines[] = 'Submitted from: ' . abs_url($back);
    $lines[] = 'Time: ' . date('F j, Y g:i a T');
    $host = parse_url(cfg('url'), PHP_URL_HOST);
    $headers = [
        'From: ' . cfg('name') . ' <no-reply@' . $host . '>',
        'Reply-To: ' . $data['email'],
        'Content-Type: text/plain; charset=UTF-8',
    ];
    $name = trim(($data['first_name'] ?? '') . ' ' . ($data['last_name'] ?? ''));
    @mail(cfg('email'), '=?UTF-8?B?' . base64_encode(FORM_LABELS[$form] . ($name ? ' — ' . $name : '')) . '?=',
        implode("\n", $lines), implode("\r\n", $headers));

    redirect('/thank-you/?f=' . $form, 303);
}

function client_ip(): string
{
    $fwd = explode(',', (string) ($_SERVER['HTTP_X_FORWARDED_FOR'] ?? ''))[0];
    return trim($fwd) ?: ($_SERVER['REMOTE_ADDR'] ?? '0');
}

function form_flash(): string
{
    $msgs = [
        'expired' => 'That form had expired. Please submit it again.',
        'limit'   => 'Too many submissions from your connection. Please try again later or email us directly.',
        'email'   => 'Please enter a valid email address.',
    ];
    $err = $msgs[$_GET['err'] ?? ''] ?? '';
    return $err ? '<p class="form-error" role="alert">' . e($err) . '</p>' : '';
}
