<?php
// Minimal SMTP client (SSL, AUTH LOGIN) for Hostinger mail. Falls back to mail().
function send_mail(string $to, string $subject, string $text, string $replyTo = ''): bool {
    $from = SMTP_USER;
    $headers = [
        'Date: ' . date('r'),
        'From: ' . SITE_NAME . ' <' . $from . '>',
        'To: <' . $to . '>',
        'Subject: =?UTF-8?B?' . base64_encode($subject) . '?=',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
        'Message-ID: <' . bin2hex(random_bytes(8)) . '@freegradecalculator.com>',
    ];
    if ($replyTo && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) $headers[] = 'Reply-To: <' . $replyTo . '>';
    $body = chunk_split(base64_encode($text));

    if (SMTP_PASS === '') {   // no password configured yet: try PHP mail()
        $h = array_filter($headers, fn($x) => !preg_match('/^(To|Subject|Date):/', $x));
        return @mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $h));
    }
    $fp = @stream_socket_client('ssl://' . SMTP_HOST . ':' . SMTP_PORT, $errno, $errstr, 15);
    if (!$fp) return false;
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) { $r = ''; while (($l = fgets($fp, 515)) !== false) { $r .= $l; if (isset($l[3]) && $l[3] === ' ') break; } return $r; };
    $cmd = function (string $c, string $expect) use ($fp, $read) { fwrite($fp, $c . "\r\n"); $r = $read(); return strncmp($r, $expect, 3) === 0; };
    $ok = strncmp($read(), '220', 3) === 0
        && $cmd('EHLO freegradecalculator.com', '250')
        && $cmd('AUTH LOGIN', '334')
        && $cmd(base64_encode(SMTP_USER), '334')
        && $cmd(base64_encode(SMTP_PASS), '235')
        && $cmd('MAIL FROM:<' . $from . '>', '250')
        && $cmd('RCPT TO:<' . $to . '>', '250')
        && $cmd('DATA', '354')
        && $cmd(implode("\r\n", $headers) . "\r\n\r\n" . $body . "\r\n.", '250');
    @fwrite($fp, "QUIT\r\n"); fclose($fp);
    return $ok;
}
