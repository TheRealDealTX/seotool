<?php defined('NHS') || exit;
/*
 * Minimal authenticated SMTP sender (SSL, AUTH PLAIN).
 * Credentials live ONLY on the server in storage/mail-config.php (never in git, never deployed):
 *   <?php return ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => 'info@…', 'pass' => '…'];
 * Falls back to PHP mail() when that file is missing.
 */
function send_mail(string $to, string $subject, string $body, string $replyTo = ''): bool {
    $cfgFile = APP_ROOT . '/storage/mail-config.php';
    $from = SITE['mail_from'];
    $clean = fn($s) => str_replace(["\r", "\n"], ' ', $s);
    $subject = $clean($subject);
    $replyTo = filter_var($replyTo, FILTER_VALIDATE_EMAIL) ? $replyTo : '';
    if (!is_file($cfgFile)) {
        $h = 'From: ' . SITE['name'] . " <$from>\r\n" . ($replyTo ? "Reply-To: $replyTo\r\n" : '') . 'Content-Type: text/plain; charset=utf-8';
        return @mail($to, $subject, $body, $h);
    }
    $c = require $cfgFile;
    $fp = @stream_socket_client('ssl://' . $c['host'] . ':' . (int) $c['port'], $errno, $errstr, 15);
    if (!$fp) { error_log("SMTP connect failed: $errstr"); return false; }
    stream_set_timeout($fp, 20);
    $read = function () use ($fp) {
        $data = '';
        while (($line = fgets($fp, 515)) !== false) { $data .= $line; if (isset($line[3]) && $line[3] === ' ') break; }
        return $data;
    };
    $cmd = function (string $line, array $ok) use ($fp, $read) {
        if ($line !== '') fwrite($fp, $line . "\r\n");
        $resp = $read();
        if (!in_array((int) substr($resp, 0, 3), $ok, true)) throw new RuntimeException(trim($resp));
        return $resp;
    };
    try {
        $cmd('', [220]);
        $cmd('EHLO ' . parse_url(SITE['origin'], PHP_URL_HOST), [250]);
        // AUTH PLAIN: Hostinger drops AUTH LOGIN connections intermittently after the username step.
        $cmd('AUTH PLAIN ' . base64_encode("\0" . $c['user'] . "\0" . $c['pass']), [235]);
        $cmd("MAIL FROM:<$from>", [250]);
        $cmd('RCPT TO:<' . $clean($to) . '>', [250, 251]);
        $cmd('DATA', [354]);
        $headers = [
            'Date: ' . date('r'),
            'From: ' . SITE['name'] . " <$from>",
            "To: <$to>",
            'Subject: =?UTF-8?B?' . base64_encode($subject) . '?=',
            'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . parse_url(SITE['origin'], PHP_URL_HOST) . '>',
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=utf-8',
            'Content-Transfer-Encoding: 8bit',
        ];
        if ($replyTo) $headers[] = "Reply-To: $replyTo";
        // Build with bare \n, then convert every line ending to CRLF exactly once.
        // (Converting an already-CRLF string again produced \r\r\n and unreadable headers.)
        $body = str_replace(["\r\n", "\r"], "\n", $body);
        $msg = implode("\n", $headers) . "\n\n" . $body;
        $msg = preg_replace('/^\./m', '..', $msg);          // SMTP dot-stuffing
        $cmd(str_replace("\n", "\r\n", $msg) . "\r\n.", [250]);
        $cmd('QUIT', [221]);
        fclose($fp);
        return true;
    } catch (Throwable $e) {
        error_log('SMTP send failed: ' . $e->getMessage());
        @fclose($fp);
        return false;
    }
}
