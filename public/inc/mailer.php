<?php
/**
 * Minimal SMTP client (implicit TLS, AUTH LOGIN) for the contact form.
 * Credentials come from config(): smtp_host, smtp_port, smtp_user, smtp_pass.
 * Falls back to PHP mail() when no password is configured.
 */
defined('SCC') || exit;

function smtp_send(string $to, string $subject, string $body, string $replyTo = ''): bool
{
    $host = config('smtp_host', 'smtp.hostinger.com');
    $port = (int) config('smtp_port', 465);
    $user = config('smtp_user', SITE_EMAIL);
    $pass = config('smtp_pass');
    $from = SITE_EMAIL;
    $subject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
    $headers = [
        'Date: ' . date('r'),
        'From: "' . SITE_NAME . ' website" <' . $from . '>',
        'To: <' . $to . '>',
        'Subject: ' . $subject,
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@solarcctvcamera.com>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    if ($replyTo) $headers[] = 'Reply-To: <' . $replyTo . '>';
    $data = implode("\r\n", $headers) . "\r\n\r\n" . chunk_split(base64_encode($body));

    if (!$pass) {
        $h = array_filter($headers, fn($x) => !preg_match('/^(To|Subject):/', $x));
        return @mail($to, $subject, chunk_split(base64_encode($body)), implode("\r\n", $h), '-f' . $from);
    }
    $fp = @stream_socket_client("ssl://$host:$port", $errno, $errstr, 15, STREAM_CLIENT_CONNECT,
        stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]));
    if (!$fp) { error_log("smtp connect failed: $errstr"); return false; }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) { $r = ''; while (($l = fgets($fp, 515)) !== false) { $r .= $l; if (isset($l[3]) && $l[3] === ' ') break; } return $r; };
    $cmd = function ($c, $ok) use ($fp, $read) { if ($c !== null) fwrite($fp, $c . "\r\n"); $r = $read(); if ((int) substr($r, 0, 3) !== $ok) { error_log('smtp: ' . trim($r)); return false; } return true; };
    $ok = $cmd(null, 220) && $cmd('EHLO solarcctvcamera.com', 250) && $cmd('AUTH LOGIN', 334)
        && $cmd(base64_encode($user), 334) && $cmd(base64_encode($pass), 235)
        && $cmd("MAIL FROM:<$from>", 250) && $cmd("RCPT TO:<$to>", 250) && $cmd('DATA', 354)
        && $cmd(preg_replace('/^\./m', '..', $data) . "\r\n.", 250);
    $cmd('QUIT', 221);
    fclose($fp);
    return $ok;
}
