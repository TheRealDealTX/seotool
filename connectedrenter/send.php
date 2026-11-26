<?php
// connectedrenter.com - contact / newsletter form handler.
// Sends each submission to info@connectedrenter.com through Hostinger SMTP, authenticated as that
// mailbox, so the message carries the domain's SPF/DKIM and doesn't land in spam.
//
// The mailbox password is NOT in this file or in git. It lives in mail-config.php, uploaded once
// next to public_html (outside the web root) and returning:
//   <?php return ['user' => 'info@connectedrenter.com', 'pass' => '...'];
// See README.md "Contact form".
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function out($ok, $error = null, $code = 200) {
    http_response_code($code);
    echo json_encode($error === null ? ['ok' => $ok] : ['ok' => $ok, 'error' => $error]);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') out(false, 'Method not allowed.', 405);

$cfg = null;
foreach ([dirname(__DIR__) . '/mail-config.php', __DIR__ . '/.private/mail-config.php', __DIR__ . '/mail-config.php'] as $f) {
    if (is_file($f)) { $cfg = include $f; break; }
}
if (!is_array($cfg) || empty($cfg['user']) || empty($cfg['pass'])) {
    error_log('send.php: mail-config.php missing');
    out(false, 'Our form is temporarily unavailable. Please email info@connectedrenter.com.', 500);
}
$to   = $cfg['to'] ?? $cfg['user'];
$host = $cfg['host'] ?? 'smtp.hostinger.com';
$port = (int)($cfg['port'] ?? 465);

// Bots: the hidden "website" field must stay empty. Treat a filled one as success so bots learn nothing.
if (trim($_POST['website'] ?? '') !== '') out(true);

$clean = function ($v, $max) {
    $v = trim(str_replace("\0", '', (string)$v));
    return mb_substr($v, 0, $max);
};
$form    = $clean($_POST['form'] ?? 'contact', 20) === 'newsletter' ? 'newsletter' : 'contact';
$name    = $clean($_POST['name'] ?? '', 100);
$email   = $clean($_POST['email'] ?? '', 200);
$subject = $clean($_POST['subject'] ?? '', 150);
$message = $clean($_POST['message'] ?? '', 5000);

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) out(false, 'Please enter a valid email address.', 422);
if ($form === 'contact' && ($name === '' || $message === '')) out(false, 'Please fill in your name and message.', 422);

// Simple per-IP rate limit: 5 submissions per 10 minutes.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? '0';
$ip = trim(explode(',', $ip)[0]);
$rl = sys_get_temp_dir() . '/cr-form-' . md5($ip);
$hits = array_filter(is_file($rl) ? (array)json_decode((string)file_get_contents($rl), true) : [], fn($t) => $t > time() - 600);
if (count($hits) >= 5) out(false, 'Too many messages. Please try again in a few minutes.', 429);
$hits[] = time();
@file_put_contents($rl, json_encode(array_values($hits)));

// Header-safe values (no CR/LF injection).
$hdr = fn($v) => preg_replace('/[\r\n]+/', ' ', $v);
$name = $hdr($name); $email = $hdr($email);
if ($subject === '') $subject = $form === 'newsletter' ? 'Subscribe me to Connected Renter updates' : 'Connected Renter website enquiry';
$subject = '[Website] ' . $hdr($subject);

$lines = $form === 'newsletter'
    ? ["New newsletter sign-up", "", "Email: $email"]
    : ["New message from the connectedrenter.com contact form", "", "Name: $name", "Email: $email", "Topic: " . ($_POST['subject'] ?? 'General question'), "", "Message:", $message];
$lines[] = "";
$lines[] = "Sent " . gmdate('Y-m-d H:i') . " UTC from " . ($_SERVER['HTTP_REFERER'] ?? 'connectedrenter.com');
$body = implode("\r\n", $lines);

$encName = fn($n) => '=?UTF-8?B?' . base64_encode($n) . '?=';
$domain  = substr(strrchr($cfg['user'], '@'), 1);
$headers = [
    'Date: ' . date('r'),
    'From: ' . $encName('Connected Renter Website') . ' <' . $cfg['user'] . '>',
    'To: <' . $to . '>',
    'Reply-To: ' . ($name !== '' ? $encName($name) . ' ' : '') . '<' . $email . '>',
    'Subject: ' . $encName($subject),
    'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $domain . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
];
$data = implode("\r\n", $headers) . "\r\n\r\n" . chunk_split(base64_encode($body));

// Minimal SMTP client (implicit TLS on 465, or STARTTLS on 587).
function smtp_send($host, $port, $user, $pass, $from, $to, $data) {
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => $host]]);
    $remote = ($port === 465 ? 'ssl://' : 'tcp://') . $host . ':' . $port;
    $s = @stream_socket_client($remote, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$s) throw new Exception("connect: $errstr ($errno)");
    stream_set_timeout($s, 20);
    $read = function () use ($s) {
        $resp = '';
        while (($line = fgets($s, 1024)) !== false) { $resp .= $line; if (isset($line[3]) && $line[3] === ' ') break; }
        return $resp;
    };
    $cmd = function ($c, $expect) use ($s, $read) {
        if ($c !== null) fwrite($s, $c . "\r\n");
        $r = $read();
        if ((int)substr($r, 0, 3) !== $expect) throw new Exception('SMTP ' . ($c === null ? 'greeting' : strtok($c, ' ')) . ': ' . trim($r));
        return $r;
    };
    $cmd(null, 220);
    $ehlo = 'EHLO connectedrenter.com';
    $cmd($ehlo, 250);
    if ($port !== 465) {
        $cmd('STARTTLS', 220);
        if (!stream_socket_enable_crypto($s, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) throw new Exception('STARTTLS failed');
        $cmd($ehlo, 250);
    }
    $cmd('AUTH LOGIN', 334);
    $cmd(base64_encode($user), 334);
    $cmd(base64_encode($pass), 235);
    $cmd("MAIL FROM:<$from>", 250);
    $cmd("RCPT TO:<$to>", 250);
    $cmd('DATA', 354);
    $cmd(preg_replace('/^\./m', '..', $data) . "\r\n.", 250);
    fwrite($s, "QUIT\r\n");
    fclose($s);
}

try {
    smtp_send($host, $port, $cfg['user'], $cfg['pass'], $cfg['user'], $to, $data);
} catch (Exception $e) {
    error_log('send.php: ' . $e->getMessage());
    out(false, 'Sorry, we could not send that right now. Please email info@connectedrenter.com.', 502);
}
out(true);
