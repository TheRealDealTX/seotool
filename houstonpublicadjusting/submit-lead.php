<?php
// Lead form handler. Emails every submission to LEAD_TO and keeps a backup copy in /leads/
// (blocked from the web by leads/.htaccess). Returns JSON for fetch() requests and
// redirects to /thank-you/ for plain form posts.

require __DIR__ . '/inc/config.php';

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');

function respond(bool $ok, string $error = ''): never {
    global $wantsJson;
    if ($wantsJson) {
        header('Content-Type: application/json');
        http_response_code($ok ? 200 : 400);
        echo json_encode(['ok' => $ok, 'error' => $error]);
    } else {
        header('Location: ' . ($ok ? '/thank-you/' : '/contact/?error=1'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /contact/', true, 303);
    exit;
}

function field(string $k, int $max = 200): string {
    $v = trim((string)($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
}

$lead = [
    'name'    => field('name', 100),
    'phone'   => field('phone', 30),
    'email'   => field('email', 120),
    'zip'     => field('zip', 10),
    'damage'  => field('damage', 60),
    'status'  => field('status', 60),
    'message' => field('message', 3000),
    'source'  => field('source', 200),
];

// Spam checks: honeypot field, and a form filled in under 3 seconds is a bot.
if (field('website') !== '') respond(true);
$ts = (int)($_POST['ts'] ?? 0);
if ($ts > 0 && time() - $ts < 3) respond(true);

foreach (['name', 'phone', 'email', 'zip', 'damage', 'status', 'source'] as $k) {
    $lead[$k] = preg_replace('/[\n\t]+/', ' ', $lead[$k]);
}
if ($lead['name'] === '') respond(false, 'Please enter your name.');
if ($lead['phone'] === '' && $lead['email'] === '') respond(false, 'Please enter a phone number or email.');
if ($lead['email'] !== '' && !filter_var($lead['email'], FILTER_VALIDATE_EMAIL)) respond(false, 'Please check your email address.');
if ($lead['phone'] !== '' && strlen(preg_replace('/\D/', '', $lead['phone'])) < 10) respond(false, 'Please check your phone number.');
if (empty($_POST['consent'])) respond(false, 'Please agree to be contacted.');

// Simple per-IP rate limit: 5 submissions per hour.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
$ip = trim(explode(',', $ip)[0]);
$rlDir = __DIR__ . '/leads/.rl';
if (!is_dir($rlDir)) @mkdir($rlDir, 0750, true);
$rlFile = $rlDir . '/' . md5($ip);
$hits = array_filter(is_file($rlFile) ? explode("\n", (string)file_get_contents($rlFile)) : [], fn($t) => $t !== '' && (int)$t > time() - 3600);
if (count($hits) >= 5) respond(false, 'Too many submissions.');
$hits[] = time();
@file_put_contents($rlFile, implode("\n", $hits));

$when = (new DateTime('now', new DateTimeZone('America/Chicago')))->format('D, M j, Y g:i A T');
$subject = 'New claim review request: ' . $lead['name'] . ($lead['damage'] ? ' (' . $lead['damage'] . ')' : '');
$lines = [
    'New lead from ' . SITE_NAME . ' (' . SITE_URL . ')',
    '',
    'Name:          ' . $lead['name'],
    'Phone:         ' . $lead['phone'],
    'Email:         ' . $lead['email'],
    'Property ZIP:  ' . $lead['zip'],
    'Damage type:   ' . $lead['damage'],
    'Claim status:  ' . $lead['status'],
    '',
    'What happened:',
    $lead['message'] !== '' ? $lead['message'] : '(not provided)',
    '',
    'Submitted:     ' . $when,
    'Form / page:   ' . $lead['source'],
    'IP address:    ' . $ip,
    'Consent:       Agreed to be contacted by call, text or email',
];
$body = implode("\n", $lines);

// Backup log (one JSON object per line) so no lead is lost if email delivery fails.
$logDir = __DIR__ . '/leads';
if (!is_dir($logDir)) @mkdir($logDir, 0750, true);
@file_put_contents($logDir . '/leads-' . date('Y-m') . '.jsonl',
    json_encode(['time' => date('c'), 'ip' => $ip] + $lead, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n", FILE_APPEND | LOCK_EX);

$replyTo = $lead['email'] !== '' ? $lead['email'] : LEAD_FROM;
$sent = SMTP_HOST !== '' ? smtp_send(LEAD_TO, $subject, $body, $replyTo) : mail_send(LEAD_TO, $subject, $body, $replyTo);

if (!$sent) {
    error_log('[lead] email delivery failed for ' . $lead['name']);
    // The lead is saved in /leads/, so the visitor still gets a success message.
}
respond(true);

function encode_subject(string $s): string { return '=?UTF-8?B?' . base64_encode($s) . '?='; }

function mail_send(string $to, string $subject, string $body, string $replyTo): bool {
    $headers = implode("\r\n", [
        'From: ' . encode_subject(SITE_NAME) . ' <' . LEAD_FROM . '>',
        'Reply-To: ' . $replyTo,
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
        'X-Mailer: houstonpublicadjusting.com',
    ]);
    return @mail($to, encode_subject($subject), $body, $headers, '-f' . LEAD_FROM);
}

/** Minimal authenticated SMTP over implicit TLS (port 465) or STARTTLS (587). */
function smtp_send(string $to, string $subject, string $body, string $replyTo): bool {
    $tls = SMTP_PORT === 465;
    $fp = @stream_socket_client(($tls ? 'ssl://' : 'tcp://') . SMTP_HOST . ':' . SMTP_PORT, $errno, $errstr, 15);
    if (!$fp) { error_log("[lead] SMTP connect failed: $errstr"); return false; }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) { $r = ''; while (($l = fgets($fp, 515)) !== false) { $r .= $l; if (isset($l[3]) && $l[3] === ' ') break; } return $r; };
    $cmd = function (string $c, string $expect) use ($fp, $read) { fwrite($fp, $c . "\r\n"); $r = $read(); if (strncmp($r, $expect, 3) !== 0) throw new RuntimeException(trim($c === '' ? 'greeting' : explode(' ', $c)[0]) . ': ' . trim($r)); return $r; };
    try {
        $g = $read(); if (strncmp($g, '220', 3) !== 0) throw new RuntimeException('greeting: ' . trim($g));
        $host = parse_url(SITE_URL, PHP_URL_HOST);
        $cmd('EHLO ' . $host, '250');
        if (!$tls) {
            $cmd('STARTTLS', '220');
            stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT);
            $cmd('EHLO ' . $host, '250');
        }
        $cmd('AUTH LOGIN', '334');
        $cmd(base64_encode(SMTP_USER), '334');
        $cmd(base64_encode(SMTP_PASS), '235');
        $cmd('MAIL FROM:<' . LEAD_FROM . '>', '250');
        $cmd('RCPT TO:<' . $to . '>', '250');
        $cmd('DATA', '354');
        $msg = implode("\r\n", [
            'Date: ' . date('r'),
            'From: ' . encode_subject(SITE_NAME) . ' <' . LEAD_FROM . '>',
            'To: <' . $to . '>',
            'Reply-To: ' . $replyTo,
            'Subject: ' . encode_subject($subject),
            'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $host . '>',
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: 8bit',
            '',
            preg_replace('/^\./m', '..', str_replace("\n", "\r\n", $body)),
        ]);
        $cmd($msg . "\r\n.", '250');
        $cmd('QUIT', '221');
        fclose($fp);
        return true;
    } catch (Throwable $e) {
        error_log('[lead] SMTP error: ' . $e->getMessage());
        fclose($fp);
        return false;
    }
}
