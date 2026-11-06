<?php
// Lead form handler: validates, filters spam, logs a backup copy, and emails
// the inquiry to the site mailbox over authenticated SMTP (Hostinger Mail).
//
// SMTP credentials are NOT in this repository. They are read from a PHP file
// that returns an array, looked up outside the web root first:
//   <site home>/.h5g/aia-config.php  (beside public_html; the Agency File
//                                     Browser can write here, not to <home>/)
//   <site home>/aia-config.php
//   public_html/api/config.local.php  <- last-resort fallback
// Example contents:
//   <?php return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
//                 'smtp_user' => 'info@alabamainsuranceappraiser.com',
//                 'smtp_pass' => '…', 'to' => 'info@alabamainsuranceappraiser.com'];

declare(strict_types=1);

const SITE_NAME = 'Alabama Insurance Appraiser';
const DEFAULT_TO = 'info@alabamainsuranceappraiser.com';

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(bool $ok, string $msg, int $code = 200): void {
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($code);
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        echo json_encode(['ok' => $ok, 'message' => $msg]);
    } else {
        header('Location: ' . ($ok ? '/thank-you/' : '/contact/?error=1'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(false, 'Method not allowed.', 405);
}

// Same-origin check (blocks cross-site form posts).
$origin = $_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? '');
if ($origin !== '' && !preg_match('#^https?://([a-z0-9-]+\.)*(alabamainsuranceappraiser\.com|hostingersite\.com|localhost)(:\d+)?(/|$)#i', $origin)) {
    respond(false, 'Invalid request origin.', 403);
}

function field(string $k, int $max): string {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    return mb_substr($v, 0, $max);
}
function oneline(string $s): string { return trim(preg_replace('/[\r\n]+/', ' ', $s) ?? ''); }

$name     = oneline(field('name', 100));
$email    = oneline(field('email', 150));
$phone    = oneline(field('phone', 25));
$role     = oneline(field('role', 60));
$loss     = oneline(field('loss_type', 60));
$location = oneline(field('location', 60));
$message  = field('message', 4000);
$page     = oneline(field('page', 200));
$honeypot = field('website', 200);
$ts       = (int)($_POST['ts'] ?? 0);
$consent  = !empty($_POST['consent']);

// Spam filters: honeypot, too-fast submission, link stuffing. Pretend success to bots.
if ($honeypot !== '' || ($ts > 0 && time() - $ts < 3) || preg_match_all('#https?://#i', $message) > 3) {
    respond(true, 'Thank you — your claim details were sent.');
}

$errors = [];
if ($name === '') $errors[] = 'name';
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'a valid email';
if (strlen(preg_replace('/\D/', '', $phone) ?? '') < 10) $errors[] = 'a 10-digit phone number';
if ($loss === '') $errors[] = 'type of loss';
if ($message === '') $errors[] = 'a short description';
if (!$consent) $errors[] = 'your consent to be contacted';
if ($errors) respond(false, 'Please provide ' . implode(', ', $errors) . '.', 422);

// Simple per-IP rate limit: 5 submissions per hour.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? '0');
$ip = trim(explode(',', $ip)[0]);
$rlFile = sys_get_temp_dir() . '/aia_rl_' . hash('sha256', $ip . date('YmdH'));
$hits = is_file($rlFile) ? (int)file_get_contents($rlFile) : 0;
if ($hits >= 5) respond(false, 'Too many submissions. Please call (844) 537-1427.', 429);
@file_put_contents($rlFile, (string)($hits + 1));

// Config (outside web root preferred).
$cfg = [];
foreach ([dirname(__DIR__, 2) . '/.h5g/aia-config.php', dirname(__DIR__, 2) . '/aia-config.php', __DIR__ . '/config.local.php'] as $f) {
    if (is_file($f) && is_readable($f)) { $c = include $f; if (is_array($c)) { $cfg = $c; break; } }
}
$to = $cfg['to'] ?? DEFAULT_TO;

// Backup log of every lead (so nothing is lost if mail fails). Stored outside the
// web root when possible; the fallback file starts with an exit() so it can't be read over HTTP.
$entry = json_encode(['time' => date('c'), 'name' => $name, 'email' => $email, 'phone' => $phone, 'role' => $role,
                      'loss' => $loss, 'location' => $location, 'page' => $page, 'message' => $message, 'ip' => $ip]) . "\n";
$logDir = dirname(__DIR__, 2) . '/.h5g/aia-leads';
if ((is_dir($logDir) || @mkdir($logDir, 0700, true)) && is_writable($logDir)) {
    @file_put_contents($logDir . '/leads-' . date('Y-m') . '.jsonl', $entry, FILE_APPEND | LOCK_EX);
} else {
    $lf = __DIR__ . '/leads.log.php';
    if (!is_file($lf)) @file_put_contents($lf, "<?php http_response_code(404); exit; ?>\n");
    @file_put_contents($lf, $entry, FILE_APPEND | LOCK_EX);
}

// Compose the email. Kept deliberately conventional (plain-ASCII subject,
// quoted-printable text + HTML parts, no custom X-Mailer): a base64-only body
// and encoded ASCII headers got the first version flagged X-Spam by Hostinger.
date_default_timezone_set('America/Chicago');
function ascii(string $s): string {
    $s = strtr($s, ['—' => '-', '–' => '-', '’' => "'", '‘' => "'", '“' => '"', '”' => '"']);
    return preg_replace('/[^\x20-\x7E]/', '', $s) ?? '';
}
$subject = ascii('Website inquiry: ' . $loss . ' - ' . $name . ($location ? ' (' . $location . ')' : ''));
$when = date('l, F j, Y g:i A T');
$rows = [
    'Name' => $name, 'Email' => $email, 'Phone' => $phone, 'I am a' => $role,
    'Type of loss' => $loss, 'Location' => $location ?: '-',
    'Page' => 'https://alabamainsuranceappraiser.com' . $page, 'Received' => $when,
];
$text = "New claim inquiry from the " . SITE_NAME . " website\n\n";
foreach ($rows as $k => $v) $text .= str_pad($k . ':', 14) . $v . "\n";
$text .= "\nMessage:\n$message\n\nReply to this email to respond to $name directly.\n";
$h = fn($v) => htmlspecialchars((string)$v, ENT_QUOTES, 'UTF-8');
$html = '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#173042;max-width:620px">'
      . '<h2 style="margin:0 0 12px;font-size:19px">New claim inquiry from the website</h2><table cellpadding="6" style="border-collapse:collapse">';
foreach ($rows as $k => $v) {
    $val = $k === 'Email' ? '<a href="mailto:' . $h($v) . '">' . $h($v) . '</a>'
         : ($k === 'Phone' ? '<a href="tel:' . $h(preg_replace('/[^\d+]/', '', $v)) . '">' . $h($v) . '</a>' : $h($v));
    $html .= '<tr><td style="color:#6c7f8d;white-space:nowrap;vertical-align:top"><b>' . $h($k) . '</b></td><td>' . $val . '</td></tr>';
}
$html .= '</table><p style="margin:16px 0 6px"><b>Message</b></p><p style="margin:0">' . nl2br($h($message)) . '</p>'
       . '<p style="margin-top:18px;color:#6c7f8d;font-size:13px">Reply to this email to respond to ' . $h($name) . ' directly.</p></div>';

function enc_header(string $s): string {
    return preg_match('/[^\x20-\x7E]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : '"' . addcslashes($s, '"\\') . '"';
}
function qp(string $s): string { return quoted_printable_encode(str_replace(["\r\n", "\n"], ["\n", "\r\n"], $s)); }

function build_message(string $from, string $to, string $replyName, string $replyEmail, string $subject, string $text, string $html): array {
    $boundary = 'b' . bin2hex(random_bytes(10));
    $headers = [
        'Date: ' . date('r'),
        'From: ' . enc_header(SITE_NAME) . " <$from>",
        "To: <$to>",
        'Reply-To: ' . enc_header($replyName) . " <$replyEmail>",
        'Subject: ' . $subject,
        sprintf('Message-ID: <%s@alabamainsuranceappraiser.com>', bin2hex(random_bytes(12))),
        'MIME-Version: 1.0',
        "Content-Type: multipart/alternative; boundary=\"$boundary\"",
    ];
    $body = "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n" . qp($text) . "\r\n"
          . "--$boundary\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n" . qp($html) . "\r\n"
          . "--$boundary--\r\n";
    return [$headers, $body];
}

function smtp_send(array $cfg, string $to, array $headers, string $body): bool {
    $host = $cfg['smtp_host'] ?? 'smtp.hostinger.com';
    $port = (int)($cfg['smtp_port'] ?? 465);
    $user = $cfg['smtp_user'] ?? '';
    $pass = $cfg['smtp_pass'] ?? '';
    if ($user === '' || $pass === '') return false;
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $fp = @stream_socket_client(($port === 465 ? 'ssl://' : 'tcp://') . "$host:$port", $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) { error_log("AIA SMTP connect failed: $errstr"); return false; }
    stream_set_timeout($fp, 20);
    $read = function () use ($fp): string {
        $data = '';
        while (($line = fgets($fp, 515)) !== false) { $data .= $line; if (isset($line[3]) && $line[3] === ' ') break; }
        return $data;
    };
    $cmd = function (string $c, array $okCodes) use ($fp, $read): bool {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        $r = $read();
        $ok = in_array((int)substr($r, 0, 3), $okCodes, true);
        if (!$ok) error_log('AIA SMTP unexpected reply to ' . (str_starts_with($c, 'AUTH') || strlen($c) > 40 ? '[auth]' : $c) . ': ' . trim($r));
        return $ok;
    };
    $ehloHost = 'alabamainsuranceappraiser.com';
    $ok = $cmd('', [220]) && $cmd("EHLO $ehloHost", [250]);
    if ($ok && $port !== 465) {
        $ok = $cmd('STARTTLS', [220]) && stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT) && $cmd("EHLO $ehloHost", [250]);
    }
    $ok = $ok && $cmd('AUTH LOGIN', [334]) && $cmd(base64_encode($user), [334]) && $cmd(base64_encode($pass), [235])
        && $cmd("MAIL FROM:<$user>", [250]) && $cmd("RCPT TO:<$to>", [250, 251]) && $cmd('DATA', [354]);
    if ($ok) {
        // Dot-stuff lines that start with "." (RFC 5321 4.5.2).
        $data = implode("\r\n", $headers) . "\r\n\r\n" . preg_replace('/^\./m', '..', $body) . "\r\n.";
        $ok = $cmd($data, [250]);
    }
    fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}

$from = $cfg['smtp_user'] ?? DEFAULT_TO;
[$headers, $mime] = build_message($from, $to, $name, $email, $subject, $text, $html);
$sent = smtp_send($cfg, $to, $headers, $mime);

if (!$sent) {
    // Fallback to the host's local mailer (same message; To/Subject go as arguments).
    $extra = array_values(array_filter($headers, fn($l) => !preg_match('/^(To|Subject):/i', $l)));
    $sent = @mail($to, $subject, $mime, implode("\r\n", $extra), '-f' . $from);
}

if ($sent) respond(true, "Thank you, $name — your claim details were sent. We'll be in touch shortly.");
// The lead is logged even if both mail paths fail; still tell the visitor how to reach us.
respond(false, 'We saved your message but could not send the notification email. Please also call (844) 537-1427 so we can respond quickly.', 500);
