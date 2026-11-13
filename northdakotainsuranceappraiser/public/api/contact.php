<?php
// North Dakota Insurance Appraiser — lead form handler.
// Sends each submission through the site mailbox over authenticated SMTP (Hostinger),
// falls back to PHP mail(), and always keeps a private JSON-lines backup.
// SMTP credentials are NOT in git. They live on the server in api/_private/config.php,
// a PHP file that returns an array and 404s if requested directly:
//   return ['smtp_host'=>'smtp.hostinger.com','smtp_port'=>465,'smtp_user'=>'info@…','smtp_pass'=>'…'];
declare(strict_types=1);

const TO_EMAIL   = 'info@northdakotainsuranceappraiser.com';
const FROM_EMAIL = 'info@northdakotainsuranceappraiser.com';
const SITE_NAME  = 'North Dakota Insurance Appraiser';

header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'method']);
    exit;
}
if (!empty($_POST['website'])) {            // honeypot
    echo json_encode(['ok' => true]);
    exit;
}

// Per-IP throttle: 5 submissions per 10 minutes.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? '0');
$ip = trim(explode(',', $ip)[0]);
$bucket = sys_get_temp_dir() . '/ndia_' . md5($ip);
$hits = array_filter(
    is_file($bucket) ? (array) json_decode((string) file_get_contents($bucket), true) : [],
    fn($t) => is_int($t) && $t > time() - 600
);
if (count($hits) >= 5) {
    http_response_code(429);
    echo json_encode(['ok' => false, 'error' => 'rate']);
    exit;
}
$hits[] = time();
@file_put_contents($bucket, json_encode(array_values($hits)));

$clean = function (string $k, int $max = 300): string {
    $v = trim((string) ($_POST[$k] ?? ''));
    $v = str_replace(["\r", "\0"], '', $v);
    return mb_substr($v, 0, $max);
};
$name    = $clean('name', 120);
$email   = $clean('email', 160);
$phone   = $clean('phone', 40);
$role    = $clean('role', 60);
$loss    = $clean('loss', 60);
$city    = $clean('city', 80);
$carrier = $clean('carrier', 120);
$amount  = $clean('amount', 60);
$details = $clean('details', 4000);
$page    = $clean('page', 200);
$consent = !empty($_POST['consent']);

if ($name === '' || (!filter_var($email, FILTER_VALIDATE_EMAIL) && $phone === '') || !$consent) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'invalid']);
    exit;
}

$lines = [
    'Name' => $name, 'Email' => $email, 'Phone' => $phone, 'Role' => $role,
    'Type of loss' => $loss, 'Location' => $city, 'Insurer' => $carrier,
    'Amount in dispute' => $amount, 'Submitted from' => $page, 'IP' => $ip,
    'Time' => gmdate('Y-m-d H:i:s') . ' UTC',
];
$body = "New claim inquiry from " . SITE_NAME . "\n\n";
foreach ($lines as $k => $v) {
    if ($v !== '') $body .= str_pad($k . ':', 20) . $v . "\n";
}
$body .= "\nClaim details:\n" . ($details !== '' ? $details : '(none)') . "\n";
$subject = 'New claim inquiry: ' . $name . ($loss ? " ($loss)" : '');
$replyTo = filter_var($email, FILTER_VALIDATE_EMAIL) ? $email : '';

/** Minimal SMTP client (implicit TLS on 465, or STARTTLS on 587) with AUTH LOGIN. */
function smtp_send(array $c, string $to, string $subject, string $body, string $replyTo, ?string &$err): bool
{
    $host = $c['smtp_host'] ?? 'smtp.hostinger.com';
    $port = (int) ($c['smtp_port'] ?? 465);
    $user = $c['smtp_user'] ?? FROM_EMAIL;
    $pass = $c['smtp_pass'] ?? '';
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'SNI_enabled' => true]]);
    $fp = @stream_socket_client(($port === 465 ? 'ssl://' : 'tcp://') . $host . ':' . $port, $no, $str, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) { $err = "connect: $str"; return false; }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp): string {
        $out = '';
        while (($line = fgets($fp, 1024)) !== false) {
            $out .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') break;
        }
        return $out;
    };
    $cmd = function (string $c, array $okCodes) use ($fp, $read, &$err): bool {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        $r = $read();
        if (!in_array((int) substr($r, 0, 3), $okCodes, true)) { $err = trim(preg_replace('/AUTH.*|[A-Za-z0-9+\/=]{20,}/', '', $c)) . ' -> ' . trim($r); return false; }
        return true;
    };
    $ehlo = 'EHLO northdakotainsuranceappraiser.com';
    if (!$cmd('', [220]) || !$cmd($ehlo, [250])) { fclose($fp); return false; }
    if ($port !== 465) {
        if (!$cmd('STARTTLS', [220]) || !stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT) || !$cmd($ehlo, [250])) { fclose($fp); return false; }
    }
    if (!$cmd('AUTH LOGIN', [334]) || !$cmd(base64_encode($user), [334]) || !$cmd(base64_encode($pass), [235])) { fclose($fp); return false; }
    if (!$cmd('MAIL FROM:<' . FROM_EMAIL . '>', [250]) || !$cmd('RCPT TO:<' . $to . '>', [250, 251]) || !$cmd('DATA', [354])) { fclose($fp); return false; }
    $headers = [
        'Date: ' . date('r'),
        'From: ' . SITE_NAME . ' <' . FROM_EMAIL . '>',
        'To: <' . $to . '>',
        'Subject: =?UTF-8?B?' . base64_encode($subject) . '?=',
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@northdakotainsuranceappraiser.com>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    if ($replyTo !== '') $headers[] = 'Reply-To: ' . $replyTo;
    $msg = implode("\r\n", $headers) . "\r\n\r\n" . rtrim(chunk_split(base64_encode($body), 76, "\r\n")) . "\r\n.";
    $ok = $cmd($msg, [250]);
    $cmd('QUIT', [221]);
    fclose($fp);
    return $ok;
}

define('NDIA_CONFIG_OK', true);
$cfg = [];
foreach ([__DIR__ . '/_private/config.php', dirname(__DIR__, 2) . '/ndia-config.php'] as $cfgFile) {
    if (is_file($cfgFile)) { $cfg = (array) include $cfgFile; break; }
}
$err = null;
$via = 'none';
$sent = false;
if (!empty($cfg['smtp_pass'])) {
    $sent = smtp_send($cfg, TO_EMAIL, $subject, $body, $replyTo, $err);
    $via = $sent ? 'smtp' : 'smtp-failed';
}
if (!$sent) {
    $h = ['From: ' . SITE_NAME . ' <' . FROM_EMAIL . '>', 'Content-Type: text/plain; charset=UTF-8'];
    if ($replyTo !== '') $h[] = 'Reply-To: ' . $replyTo;
    $sent = @mail(TO_EMAIL, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $h), '-f' . FROM_EMAIL);
    if ($sent) $via .= '+mail';
}

// Private JSON-lines backup in api/_private/ (404s if requested), in case delivery ever fails.
$log = __DIR__ . '/_private/leads.log.php';
if (!is_dir(__DIR__ . '/_private')) @mkdir(__DIR__ . '/_private', 0755, true);
if (!is_file($log)) @file_put_contents($log, "<?php http_response_code(404); exit; ?>\n");
@file_put_contents($log,
    json_encode(['t' => time()] + $lines + ['details' => $details, 'via' => $via, 'err' => $err]) . "\n", FILE_APPEND | LOCK_EX);

echo json_encode(['ok' => true]);
