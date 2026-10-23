<?php
// Minimal SMTP client for the contact form (no Composer on this host).
// Credentials live only on the server, in app/private/smtp.php (git-ignored,
// skipped by deploy.sh; the host executes .php rather than serving it, and the
// file exits unless loaded by the app). It returns:
//   ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => 'info@…', 'pass' => '…']
defined('SS_APP') || exit;

function smtp_config() {
    $f = __DIR__ . '/private/smtp.php';
    return is_file($f) ? include $f : null;
}

/** Send a plain-text email. Returns true on success; falls back to mail() when SMTP isn't configured. */
function send_mail($to, $subject, $body, $replyTo = '') {
    $replyTo = str_replace(["\r", "\n"], '', $replyTo);
    $subject = str_replace(["\r", "\n"], ' ', $subject);
    $cfg = smtp_config();
    if (!$cfg) {
        return @mail($to, $subject, $body, 'From: ' . SITE_EMAIL . ($replyTo ? "\r\nReply-To: $replyTo" : ''));
    }
    $fp = @stream_socket_client('ssl://' . $cfg['host'] . ':' . (int)$cfg['port'], $errno, $errstr, 15);
    if (!$fp) return false;
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) {
        $out = '';
        while (($line = fgets($fp, 515)) !== false) { $out .= $line; if (isset($line[3]) && $line[3] === ' ') break; }
        return $out;
    };
    $cmd = function ($c, $expect) use ($fp, $read) {
        if ($c !== null) fwrite($fp, $c . "\r\n");
        return strpos($read(), (string)$expect) === 0;
    };
    $date = date('r');
    $msgId = '<' . bin2hex(random_bytes(12)) . '@saffronsupplement.com>';
    $headers = "Date: $date\r\nFrom: " . SITE_NAME . " <{$cfg['user']}>\r\nTo: <$to>\r\n"
        . ($replyTo ? "Reply-To: <$replyTo>\r\n" : '')
        . 'Subject: =?UTF-8?B?' . base64_encode($subject) . "?=\r\nMessage-ID: $msgId\r\n"
        . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n";
    $data = $headers . "\r\n" . chunk_split(base64_encode($body)) . "\r\n.";
    $ok = $cmd(null, 220)
        && $cmd('EHLO saffronsupplement.com', 250)
        && $cmd('AUTH LOGIN', 334)
        && $cmd(base64_encode($cfg['user']), 334)
        && $cmd(base64_encode($cfg['pass']), 235)
        && $cmd('MAIL FROM:<' . $cfg['user'] . '>', 250)
        && $cmd('RCPT TO:<' . $to . '>', 250)
        && $cmd('DATA', 354)
        && $cmd($data, 250);
    $cmd('QUIT', 221);
    fclose($fp);
    return $ok;
}
