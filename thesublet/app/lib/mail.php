<?php defined('APP') || exit;

/**
 * Minimal SMTP client (implicit TLS on 465, AUTH LOGIN). Sends HTML + text alternative.
 * Returns true on success; logs every attempt to email_log.
 */
function send_mail(string $to, string $subject, string $html, ?string $replyTo = null, ?string &$error = null): bool
{
    $c = cfg('smtp');
    $error = null;
    $ok = false;
    try {
        if (cfg('env') === 'dev' && empty($c['pass'])) {
            // local testing: write to dev/mail.log instead of sending
            @file_put_contents(ROOT . '/dev/mail.log', "TO: $to\nSUBJECT: $subject\nREPLY-TO: $replyTo\n\n" . html_to_text($html) . "\n-----\n", FILE_APPEND);
            $ok = true;
        } else {
            if (empty($c['pass'])) throw new RuntimeException('SMTP password not configured in app/config.php');
            $ok = smtp_send($c, $to, $subject, $html, $replyTo);
        }
    } catch (Throwable $e) {
        $error = $e->getMessage();
        error_log('[mail] ' . $error);
    }
    try {
        insert('email_log', ['to_addr' => mb_substr($to, 0, 190), 'subject' => mb_substr($subject, 0, 255),
            'status' => $ok ? 'sent' : 'failed', 'error' => $error, 'created_at' => now()]);
    } catch (Throwable $e) {}
    return $ok;
}

function smtp_send(array $c, string $to, string $subject, string $html, ?string $replyTo): bool
{
    $host = $c['host'] ?? 'smtp.hostinger.com';
    $port = (int)($c['port'] ?? 465);
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'SNI_enabled' => true, 'peer_name' => $host]]);
    $fp = @stream_socket_client("ssl://$host:$port", $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) throw new RuntimeException("SMTP connect failed: $errstr ($errno)");
    stream_set_timeout($fp, 20);
    $read = function () use ($fp) {
        $data = '';
        while (($line = fgets($fp, 1024)) !== false) {
            $data .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') break;
        }
        return $data;
    };
    $cmd = function (string $line, array $expect) use ($fp, $read) {
        if ($line !== '') fwrite($fp, $line . "\r\n");
        $resp = $read();
        $code = (int)substr($resp, 0, 3);
        if (!in_array($code, $expect, true)) {
            throw new RuntimeException('SMTP error after "' . (str_starts_with($line, 'AUTH') || strlen($line) > 60 ? substr($line, 0, 10) . '…' : $line) . '": ' . trim($resp));
        }
        return $resp;
    };
    $cmd('', [220]);
    $cmd('EHLO thesublet.com', [250]);
    $cmd('AUTH LOGIN', [334]);
    $cmd(base64_encode($c['user']), [334]);
    $cmd(base64_encode($c['pass']), [235]);
    $from = $c['from'] ?? $c['user'];
    $cmd('MAIL FROM:<' . $from . '>', [250]);
    $cmd('RCPT TO:<' . $to . '>', [250, 251]);
    $cmd('DATA', [354]);

    $boundary = 'b' . bin2hex(random_bytes(12));
    $text = html_to_text($html);
    $enc = fn($s) => '=?UTF-8?B?' . base64_encode($s) . '?=';
    $headers = [
        'Date: ' . date('r'),
        'From: ' . $enc($c['from_name'] ?? 'The Sublet') . ' <' . $from . '>',
        'To: <' . $to . '>',
        'Subject: ' . $enc($subject),
        'Message-ID: <' . bin2hex(random_bytes(10)) . '@thesublet.com>',
        'MIME-Version: 1.0',
        'Content-Type: multipart/alternative; boundary="' . $boundary . '"',
    ];
    if ($replyTo && valid_email($replyTo)) $headers[] = 'Reply-To: <' . $replyTo . '>';
    $body = "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($text))
        . "--$boundary\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode(email_wrap($html)))
        . "--$boundary--";
    $msg = implode("\r\n", $headers) . "\r\n\r\n" . $body;
    $msg = preg_replace('/^\./m', '..', $msg);
    $cmd($msg . "\r\n.", [250]);
    try { $cmd('QUIT', [221]); } catch (Throwable $e) {}
    fclose($fp);
    return true;
}

function email_wrap(string $inner): string
{
    return '<!doctype html><html><body style="margin:0;background:#f4f7f5;font-family:Arial,Helvetica,sans-serif;color:#1d2a24">'
        . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:24px 12px">'
        . '<table role="presentation" width="100%" style="max-width:560px;background:#ffffff;border-radius:10px;padding:28px" cellpadding="0" cellspacing="0"><tr><td>'
        . '<p style="margin:0 0 18px;font-size:20px;font-weight:bold;color:#2f6f4f">The Sublet</p>'
        . '<div style="font-size:15px;line-height:1.6">' . $inner . '</div>'
        . '<p style="margin-top:28px;font-size:12px;color:#6b7b73">The Sublet · thesublet.com · Never wire money or pay before touring and verifying a rental.</p>'
        . '</td></tr></table></td></tr></table></body></html>';
}

function email_button(string $url, string $label): string
{
    return '<p style="margin:22px 0"><a href="' . e($url) . '" style="background:#2f6f4f;color:#ffffff;text-decoration:none;padding:12px 20px;border-radius:8px;display:inline-block;font-weight:bold">' . e($label) . '</a></p>';
}

function notify_admin(string $subject, string $html): void
{
    $to = cfg('admin_notify') ?: cfg('smtp.from');
    if ($to) send_mail($to, '[The Sublet] ' . $subject, $html);
}

function html_to_text(string $html): string
{
    $html = preg_replace_callback('#<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>#is', function ($m) {
        $label = trim(strip_tags($m[2]));
        return html_entity_decode($label, ENT_QUOTES, 'UTF-8') === html_entity_decode($m[1], ENT_QUOTES, 'UTF-8') ? $m[1] : $label . ' (' . $m[1] . ')';
    }, $html);
    $html = preg_replace(['#<br\s*/?>#i', '#</(p|tr|h\d|div)>#i', '#</td>\s*<td[^>]*>#i'], ["\n", "\n\n", ': '], $html);
    $text = html_entity_decode(strip_tags($html), ENT_QUOTES, 'UTF-8');
    $text = preg_replace(['/[ \t]+/', '/ *\n */', '/\n{3,}/'], [' ', "\n", "\n\n"], $text);
    $text = str_replace('✔: ', '• ', $text);
    return trim($text);
}
