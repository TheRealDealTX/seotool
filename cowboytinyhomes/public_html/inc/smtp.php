<?php
// Minimal authenticated SMTP sender (implicit TLS, AUTH LOGIN) for contact-form leads.
//
// Credentials live in inc/secrets.php on the server only (git-ignored):
//   <?php return ['host' => 'smtp.hostinger.com', 'port' => 465,
//                 'user' => 'contact@cowboytinyhomes.com', 'pass' => '…'];
// If that file is missing or SMTP fails, send_mail() falls back to PHP mail().

function smtp_log(string $msg): void
{
    $dir = __DIR__ . '/data';
    if (!is_dir($dir)) @mkdir($dir, 0750, true);
    @file_put_contents($dir . '/mail.log', date('c') . ' ' . $msg . "\n", FILE_APPEND | LOCK_EX);
}

/** Send a plain-text email. Returns true when the server accepted it. */
function send_mail(string $to, string $subject, string $body, string $replyTo = '', string $replyName = ''): bool
{
    $encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
    $replyHdr = $replyTo ? ($replyName ? '"' . addcslashes($replyName, '"\\') . '" ' : '') . '<' . $replyTo . '>' : '';
    $secrets = is_file(__DIR__ . '/secrets.php') ? include __DIR__ . '/secrets.php' : null;

    if (is_array($secrets) && !empty($secrets['pass'])) {
        try {
            smtp_send($secrets, $to, $encSubject, $body, $replyHdr);
            return true;
        } catch (Throwable $e) {
            smtp_log('SMTP failed: ' . $e->getMessage() . ' — falling back to mail()');
        }
    }
    $headers = 'From: ' . SITE_NAME . ' Website <' . MAIL_FROM . ">\r\n"
             . ($replyHdr ? 'Reply-To: ' . $replyHdr . "\r\n" : '')
             . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit";
    $ok = @mail($to, $encSubject, $body, $headers, '-f' . MAIL_FROM);
    if (!$ok) smtp_log('mail() fallback also failed');
    return $ok;
}

function smtp_send(array $cfg, string $to, string $encSubject, string $body, string $replyHdr): void
{
    $host = $cfg['host'] ?? 'smtp.hostinger.com';
    $port = (int)($cfg['port'] ?? 465);
    $user = $cfg['user'];
    $fp = @stream_socket_client('ssl://' . $host . ':' . $port, $errno, $errstr, 15);
    if (!$fp) throw new RuntimeException("connect $host:$port: $errstr ($errno)");
    stream_set_timeout($fp, 15);

    $read = function () use ($fp): string {
        $out = '';
        while (($line = fgets($fp, 1024)) !== false) {
            $out .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') break;   // last line of a (multi-line) reply
        }
        return $out;
    };
    $cmd = function (string $c, array $expect) use ($fp, $read): string {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        $r = $read();
        if (!in_array((int)substr($r, 0, 3), $expect, true)) {
            $shown = stripos($c, 'AUTH') === 0 || preg_match('/^[A-Za-z0-9+\/=]+$/', $c) ? '[auth]' : $c;
            throw new RuntimeException('SMTP ' . ($shown ?: 'greeting') . ' => ' . trim($r));
        }
        return $r;
    };

    $cmd('', [220]);
    $cmd('EHLO ' . SITE_HOST, [250]);
    $cmd('AUTH LOGIN', [334]);
    $cmd(base64_encode($user), [334]);
    $cmd(base64_encode($cfg['pass']), [235]);
    $cmd('MAIL FROM:<' . $user . '>', [250]);
    $cmd('RCPT TO:<' . $to . '>', [250, 251]);
    $cmd('DATA', [354]);

    $headers = [
        'Date: ' . date('r'),
        'From: "' . SITE_NAME . ' Website" <' . $user . '>',
        'To: <' . $to . '>',
        'Subject: ' . $encSubject,
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . SITE_HOST . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    if ($replyHdr) $headers[] = 'Reply-To: ' . $replyHdr;
    $msg = implode("\r\n", $headers) . "\r\n\r\n" . chunk_split(base64_encode($body), 76, "\r\n");
    fwrite($fp, $msg . "\r\n.\r\n");
    $cmd('', [250]);
    $cmd('QUIT', [221]);
    fclose($fp);
}
