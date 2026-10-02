<?php
/**
 * The Colony Public Adjuster — contact form handler (Hostinger / PHP 7.4+).
 *
 * GET  -> returns a fresh CSRF token as JSON.
 * POST -> validates and emails the request, returns JSON (or redirects when JS is off).
 *
 * Edit the three settings below if the mailbox changes. FROM_EMAIL must be an
 * address on this domain (create it in hPanel > Emails) or Hostinger may reject it.
 */
const TO_EMAIL   = 'info@thecolonypublicadjuster.com';
const FROM_EMAIL = 'noreply@thecolonypublicadjuster.com';
const SITE_NAME  = 'The Colony Public Adjuster';
const RATE_LIMIT = 5;        // submissions allowed ...
const RATE_WINDOW = 3600;    // ... per this many seconds, per visitor

session_set_cookie_params(['lifetime' => 0, 'path' => '/', 'secure' => !empty($_SERVER['HTTPS']) || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https', 'httponly' => true, 'samesite' => 'Lax']);
session_start();
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function token(): string {
    if (empty($_SESSION['csrf'])) { $_SESSION['csrf'] = bin2hex(random_bytes(32)); }
    return $_SESSION['csrf'];
}
function respond(bool $ok, string $message, int $code = 200): void {
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['ok' => $ok, 'message' => $message, 'csrf' => token()]);
    } else {
        header('Location: /contact/?' . ($ok ? 'sent=1' : 'error=1') . '#request', true, 303);
    }
    exit;
}
function clean(string $key, int $max = 200): string {
    $v = trim((string)($_POST[$key] ?? ''));
    $v = str_replace(["\r", "\n", "\0"], ' ', $v);
    return mb_substr($v, 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['csrf' => token()]);
    exit;
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond(false, 'Method not allowed.', 405);
}

// Spam traps: honeypot field must stay empty and the form must not be submitted instantly.
if (!empty($_POST['website'])) { respond(true, 'Thank you. We received your request.'); }
$ts = (int)($_POST['ts'] ?? 0);
if ($ts > 0 && (microtime(true) * 1000 - $ts) < 3000) { respond(false, 'Please take a moment to review your request, then submit again.', 400); }

// CSRF (only enforced when JS loaded the token; the no-JS path still has the other checks).
$sent = (string)($_POST['csrf'] ?? '');
if ($sent !== '' && !hash_equals(token(), $sent)) { respond(false, 'Your session expired. Please refresh the page and try again.', 400); }

// Rate limit by hashed IP (no raw IP stored).
$ipHash = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . __FILE__);
$rlFile = sys_get_temp_dir() . '/tcpa_rl_' . substr($ipHash, 0, 32);
$hits = [];
if (is_file($rlFile)) { $hits = array_filter(array_map('intval', explode(',', (string)file_get_contents($rlFile))), fn($t) => $t > time() - RATE_WINDOW); }
if (count($hits) >= RATE_LIMIT) { respond(false, 'Too many requests. Please call (832) 503-5866 instead.', 429); }

$name    = clean('name', 100);
$phone   = clean('phone', 40);
$email   = clean('email', 160);
$city    = clean('city', 80);
$type    = clean('claim_type', 60);
$status  = clean('claim_status', 60);
$message = trim(mb_substr((string)($_POST['message'] ?? ''), 0, 3000));
$consent = !empty($_POST['consent']);

$errors = [];
if ($name === '') $errors[] = 'name';
if (!preg_match('/\d{3}.*\d{3}.*\d{4}/', $phone)) $errors[] = 'phone number';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'email address';
if ($type === '') $errors[] = 'claim type';
if ($message === '') $errors[] = 'description of what happened';
if (!$consent) $errors[] = 'consent checkbox';
if ($errors) { respond(false, 'Please check your ' . implode(', ', $errors) . '.', 422); }

$hits[] = time();
@file_put_contents($rlFile, implode(',', $hits), LOCK_EX);

$body = "New free claim review request\n"
      . "------------------------------\n"
      . "Name:          $name\n"
      . "Phone:         $phone\n"
      . "Email:         $email\n"
      . "Property city: " . ($city ?: '-') . "\n"
      . "Claim type:    $type\n"
      . "Claim status:  " . ($status ?: '-') . "\n\n"
      . "What happened:\n" . wordwrap($message, 76) . "\n\n"
      . "Submitted: " . date('Y-m-d H:i T') . " via " . ($_SERVER['HTTP_HOST'] ?? 'website') . "\n";

$subject = '=?UTF-8?B?' . base64_encode('Claim review request: ' . $name . ' (' . $type . ')') . '?=';
$headers = [
    'From: ' . SITE_NAME . ' <' . FROM_EMAIL . '>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . PHP_VERSION,
];
$ok = @mail(TO_EMAIL, $subject, $body, implode("\r\n", $headers), '-f' . FROM_EMAIL);

if ($ok) {
    respond(true, 'Thank you, ' . htmlspecialchars($name, ENT_QUOTES) . '. Your request was sent. We will contact you shortly to talk through your claim.');
}
respond(false, 'We could not send your request right now. Please call (832) 503-5866 or email ' . TO_EMAIL . '.', 500);
