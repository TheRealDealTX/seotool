<?php
// Katy Roofer - lead form handler. Every site form posts here.
declare(strict_types=1);
date_default_timezone_set('America/Chicago');
$cfg = require __DIR__ . '/includes/config.php';

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(bool $ok, string $msg, bool $json): void {
    if ($json) {
        header('Content-Type: application/json; charset=utf-8');
        http_response_code($ok ? 200 : 422);
        echo json_encode(['ok' => $ok, 'message' => $msg]);
    } elseif ($ok) {
        header('Location: /thank-you/', true, 303);
    } else {
        http_response_code(422);
        header('Content-Type: text/html; charset=utf-8');
        echo '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Please check the form</title>'
           . '<body style="font-family:system-ui;max-width:560px;margin:60px auto;padding:0 16px"><h1>Almost there</h1><p>'
           . htmlspecialchars($msg) . '</p><p><a href="javascript:history.back()">Go back to the form</a> or call <a href="tel:+15122977580">(512) 297-7580</a>.</p>';
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
    return function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max);
}
function oneLine(string $v): string { return trim(preg_replace('/\s+/', ' ', $v)); }

// Spam traps: hidden honeypot field and a minimum fill time.
if (field('website') !== '') respond(true, 'Thanks!', $wantsJson);
$t = (int)field('t', 20);
if ($t > 0 && (microtime(true) * 1000 - $t) < 2500) respond(false, 'That was a little fast - please try again.', $wantsJson);

$name    = oneLine(field('name', 100));
$phone   = oneLine(field('phone', 40));
$email   = oneLine(field('email', 120));
$address = oneLine(field('address', 200));
$service = oneLine(field('service', 80));
$timing  = oneLine(field('timing', 80));
$message = field('message', 3000);
$page    = oneLine(field('page', 200));
$form    = oneLine(field('form', 60));

if ($name === '') respond(false, 'Please enter your name.', $wantsJson);
if (strlen(preg_replace('/\D/', '', $phone)) < 10) respond(false, 'Please enter a valid phone number so we can reach you.', $wantsJson);
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) respond(false, 'Please check your email address.', $wantsJson);
if (preg_match_all('#https?://#i', $message) > 2) respond(false, 'Please remove the links from your message.', $wantsJson);

$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
$ip = trim(explode(',', $ip)[0]);
$lines = [
    'Form'         => $form ?: 'Website form',
    'Name'         => $name,
    'Phone'        => $phone,
    'Email'        => $email ?: '(not provided)',
    'Address / ZIP'=> $address ?: '(not provided)',
    'Service'      => $service ?: '(not specified)',
    'Timing'       => $timing ?: '(not specified)',
    'Page'         => $page,
    'Submitted'    => date('D, M j, Y g:i A T'),
    'IP'           => $ip,
];
$body = "New lead from rooferkaty.com\n\n";
foreach ($lines as $k => $v) $body .= str_pad($k . ':', 15) . $v . "\n";
$body .= "\nMessage:\n" . ($message !== '' ? $message : '(none)') . "\n";

$subject = $cfg['subject'] . ' - ' . $name;

// Backup log (file starts with a PHP exit so it can never be read over the web).
$log = $cfg['log_file'];
if (!file_exists($log)) @file_put_contents($log, "<?php http_response_code(404); exit; ?>\n");
@file_put_contents($log, str_repeat('-', 60) . "\n" . $body, FILE_APPEND | LOCK_EX);

$sent = !empty($cfg['smtp_user']) ? smtp_send($cfg, $subject, $body, $email, $name) : mail_send($cfg, $subject, $body, $email, $name);

if (!$sent) respond(false, 'Sorry, we could not send your request right now. Please call (512) 297-7580 and we will help you directly.', $wantsJson);
respond(true, 'Thanks! We received your request and will call you shortly.', $wantsJson);

// ---------------------------------------------------------------------------

function enc(string $s): string { return '=?UTF-8?B?' . base64_encode($s) . '?='; }

function mail_send(array $cfg, string $subject, string $body, string $replyTo, string $replyName): bool {
    $headers = [
        'From: ' . enc($cfg['from_name']) . ' <' . $cfg['from'] . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
        'X-Mailer: rooferkaty.com',
    ];
    if ($replyTo !== '') $headers[] = 'Reply-To: ' . enc($replyName) . ' <' . $replyTo . '>';
    return @mail($cfg['to'], enc($subject), $body, implode("\r\n", $headers), '-f' . $cfg['from']);
}

function smtp_send(array $cfg, string $subject, string $body, string $replyTo, string $replyName): bool {
    $host = ($cfg['smtp_port'] == 465 ? 'ssl://' : '') . $cfg['smtp_host'];
    $fp = @stream_socket_client($host . ':' . $cfg['smtp_port'], $errno, $errstr, 15);
    if (!$fp) return mail_send($cfg, $subject, $body, $replyTo, $replyName);
    stream_set_timeout($fp, 15);
    $read = function () use ($fp): string {
        $data = '';
        while (($line = fgets($fp, 515)) !== false) { $data .= $line; if (isset($line[3]) && $line[3] === ' ') break; }
        return $data;
    };
    $cmd = function (string $c, array $ok) use ($fp, $read): bool {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        return in_array((int)substr($read(), 0, 3), $ok, true);
    };
    $msgHeaders = [
        'Date: ' . date('r'),
        'From: ' . enc($cfg['from_name']) . ' <' . $cfg['from'] . '>',
        'To: <' . $cfg['to'] . '>',
        'Subject: ' . enc($subject),
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    if ($replyTo !== '') $msgHeaders[] = 'Reply-To: ' . enc($replyName) . ' <' . $replyTo . '>';
    $data = implode("\r\n", $msgHeaders) . "\r\n\r\n" . chunk_split(base64_encode($body));
    $ok = $cmd('', [220])
        && $cmd('EHLO rooferkaty.com', [250])
        && $cmd('AUTH LOGIN', [334])
        && $cmd(base64_encode($cfg['smtp_user']), [334])
        && $cmd(base64_encode($cfg['smtp_pass']), [235])
        && $cmd('MAIL FROM:<' . $cfg['from'] . '>', [250])
        && $cmd('RCPT TO:<' . $cfg['to'] . '>', [250, 251])
        && $cmd('DATA', [354])
        && $cmd($data . "\r\n.", [250]);
    $cmd('QUIT', [221]);
    fclose($fp);
    return $ok ?: mail_send($cfg, $subject, $body, $replyTo, $replyName);
}
