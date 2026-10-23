<?php
// Contact form handler for /contact-us/.
// Messages are appended to a CSV outside the web root (never inside it: the host ignores .htaccess),
// and emailed through authenticated SMTP using the settings in a private config file:
//   <website root>/.h5g/dogearcleaner-private/config.php   (lives only on the server; never commit it)
//     <?php return ['to' => 'info@dogearcleaner.com', 'smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
//                   'smtp_user' => 'info@dogearcleaner.com', 'smtp_pass' => '...'];
//   <website root>/.h5g/dogearcleaner-private/messages.csv (created automatically)
// The website root itself is read-only to PHP on this host; .h5g is writable and not web-served.
$back = '/contact-us/';
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { header('Location: ' . $back, true, 303); exit; }

function field($k, $max) { return trim(mb_substr(str_replace(["\r", "\0"], '', (string)($_POST[$k] ?? '')), 0, $max)); }
$first = field('first_name', 80); $last = field('last_name', 80); $email = field('email', 160);
$topic = field('topic', 60); $msg = field('message', 5000);

if (field('website', 200) !== '') { header('Location: ' . $back . '?sent=1', true, 303); exit; } // honeypot
if ($first === '' || $msg === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: ' . $back . '?error=invalid', true, 303); exit;
}

$private = dirname(__DIR__) . '/.h5g/dogearcleaner-private';
$dir = $private;
if (!is_dir($dir)) { @mkdir($dir, 0700, true); }
if (!is_dir($dir) || !is_writable($dir)) { $dir = null; }   // never fall back to a folder inside the web root

// Basic flood control: max 5 messages per IP per hour.
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] ?? ($_SERVER['REMOTE_ADDR'] ?? '');
$ip = trim(explode(',', $ip)[0]);
if ($dir) {
    $rl = $dir . '/rate-' . md5($ip) . '.txt';
    $hits = array_filter(array_map('intval', @file($rl, FILE_IGNORE_NEW_LINES) ?: []), fn($t) => $t > time() - 3600);
    if (count($hits) >= 5) { header('Location: ' . $back . '?error=rate', true, 303); exit; }
    $hits[] = time(); @file_put_contents($rl, implode("\n", $hits));
}

$row = [date('c'), $first, $last, $email, $topic, $msg, $ip];
$ok = false;
if ($dir && ($fh = @fopen($dir . '/messages.csv', 'a'))) { $ok = fputcsv($fh, $row) !== false; fclose($fh); }

$cfg = is_file($private . '/config.php') ? include $private . '/config.php' : [];
if (!empty($cfg['to'])) {
    $subject = 'Dog Ear Cleaner contact: ' . ($topic ?: 'Message') . ' from ' . trim("$first $last");
    $body = "Name: $first $last\nEmail: $email\nTopic: $topic\nIP: $ip\nSent: " . date('r') . "\n\n$msg\n";
    $sent = !empty($cfg['smtp_pass']) ? smtp_send($cfg, $cfg['to'], $subject, $body, $email, trim("$first $last"), $err) : false;
    if (!$sent && empty($cfg['smtp_pass'])) {
        $sent = @mail($cfg['to'], $subject, $body, "From: Dog Ear Cleaner <" . $cfg['to'] . ">\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8");
    }
    if (!$sent && $dir) { @file_put_contents($dir . '/mail-errors.log', date('c') . ' ' . ($err ?? 'mail() failed') . "\n", FILE_APPEND); }
    $ok = $ok || $sent;
}
header('Location: ' . $back . ($ok ? '?sent=1' : '?error=save'), true, 303);

// Minimal SMTP client (implicit TLS on 465, or STARTTLS on 587) with AUTH LOGIN.
function smtp_send(array $c, string $to, string $subject, string $body, string $replyTo, string $replyName, &$err): bool {
    $host = $c['smtp_host'] ?? 'smtp.hostinger.com'; $port = (int)($c['smtp_port'] ?? 465);
    $user = $c['smtp_user'] ?? $to; $from = $c['from'] ?? $user;
    $fp = @stream_socket_client(($port === 465 ? 'ssl://' : 'tcp://') . "$host:$port", $no, $str, 15);
    if (!$fp) { $err = "connect: $str"; return false; }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) { $r = ''; while (($l = fgets($fp, 515)) !== false) { $r .= $l; if (isset($l[3]) && $l[3] === ' ') break; } return $r; };
    $cmd = function ($line, $expect) use ($fp, $read, &$err) {
        if ($line !== null) fwrite($fp, $line . "\r\n");
        $r = $read();
        if ((int)substr($r, 0, 3) !== $expect) { $err = trim(($line && stripos($line, 'AUTH') === false && !preg_match('/^[A-Za-z0-9+\/=]+$/', $line) ? $line : '[auth]') . ' -> ' . $r); return false; }
        return true;
    };
    $helo = 'dogearcleaner.com';
    $ok = $cmd(null, 220) && $cmd("EHLO $helo", 250);
    if ($ok && $port !== 465) {
        $ok = $cmd('STARTTLS', 220) && stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT) && $cmd("EHLO $helo", 250);
    }
    $ok = $ok && $cmd('AUTH LOGIN', 334) && $cmd(base64_encode($user), 334) && $cmd(base64_encode($c['smtp_pass']), 235)
        && $cmd("MAIL FROM:<$from>", 250) && $cmd("RCPT TO:<$to>", 250) && $cmd('DATA', 354);
    if ($ok) {
        $enc = fn($s) => '=?UTF-8?B?' . base64_encode($s) . '?=';
        $headers = [
            'Date: ' . date('r'),
            'From: ' . $enc('Dog Ear Cleaner') . " <$from>",
            "To: <$to>",
            'Reply-To: ' . $enc($replyName ?: $replyTo) . " <$replyTo>",
            'Subject: ' . $enc($subject),
            'Message-ID: <' . bin2hex(random_bytes(12)) . '@dogearcleaner.com>',
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: base64',
        ];
        $data = implode("\r\n", $headers) . "\r\n\r\n" . chunk_split(base64_encode($body), 76, "\r\n");
        fwrite($fp, $data . ".\r\n");
        $ok = $cmd(null, 250);
    }
    @fwrite($fp, "QUIT\r\n"); fclose($fp);
    return $ok;
}
