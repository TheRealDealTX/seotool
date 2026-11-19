<?php
declare(strict_types=1);
defined('M1S') || exit;

/**
 * Minimal authenticated SMTP client (implicit TLS, port 465) for transactional mail.
 * Config: 'smtp' => ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => '…', 'pass' => '…']
 * Returns true on success; logs and returns false on failure.
 */
function smtp_send(string $to, string $subject, string $body, ?string $replyTo = null): bool
{
    $c = cfg('smtp');
    $from = $c['user'];
    $errno = 0;
    $errstr = '';
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'SNI_enabled' => true]]);
    $fp = @stream_socket_client('ssl://' . $c['host'] . ':' . ($c['port'] ?? 465), $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) {
        error_log("[m1s] smtp connect failed: $errstr ($errno)");
        return false;
    }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp): string {
        $data = '';
        while (($line = fgets($fp, 1024)) !== false) {
            $data .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') {
                break;
            }
        }
        return $data;
    };
    $cmd = function (string $line, array $ok) use ($fp, $read): bool {
        fwrite($fp, $line . "\r\n");
        $resp = $read();
        if (!in_array((int)substr($resp, 0, 3), $ok, true)) {
            $safe = preg_match('/^(EHLO|MAIL FROM|RCPT TO|DATA|AUTH LOGIN)/', $line) ? $line : '[redacted]';
            error_log('[m1s] smtp "' . $safe . '" -> ' . trim($resp));
            return false;
        }
        return true;
    };
    $domain = parse_url(cfg('base_url'), PHP_URL_HOST) ?: 'localhost';
    $ok = (int)substr($read(), 0, 3) === 220
        && $cmd('EHLO ' . $domain, [250])
        && $cmd('AUTH LOGIN', [334])
        && $cmd(base64_encode($c['user']), [334])
        && $cmd(base64_encode($c['pass']), [235])
        && $cmd('MAIL FROM:<' . $from . '>', [250])
        && $cmd('RCPT TO:<' . $to . '>', [250, 251])
        && $cmd('DATA', [354]);
    if ($ok) {
        $headers = [
            'Date: ' . date('r'),
            'From: ' . mail_header_encode(cfg('site_name')) . ' <' . $from . '>',
            'To: <' . $to . '>',
            'Subject: ' . mail_header_encode($subject),
            'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $domain . '>',
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: 8bit',
        ];
        if ($replyTo) {
            $headers[] = 'Reply-To: <' . $replyTo . '>';
        }
        $text = preg_replace('/^\./m', '..', str_replace(["\r\n", "\r"], "\n", $body));
        $ok = $cmd(implode("\r\n", $headers) . "\r\n\r\n" . str_replace("\n", "\r\n", $text) . "\r\n.", [250]);
    }
    @fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}

function mail_header_encode(string $s): string
{
    return preg_match('/[^\x20-\x7E]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : $s;
}
