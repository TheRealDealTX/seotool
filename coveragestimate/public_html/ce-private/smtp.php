<?php
// Minimal authenticated SMTP client (implicit TLS on 465, or STARTTLS on 587).

function ce_smtp_send(array $cfg, string $from, string $fromName, array $to, string $subject, string $html, ?string $replyTo = null): array
{
    $log = [];
    $host = $cfg['host'];
    $port = (int) $cfg['port'];
    $remote = ($port === 465 ? 'ssl://' : 'tcp://') . $host . ':' . $port;
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $fp = @stream_socket_client($remote, $errno, $errstr, 20, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) {
        return [false, "connect failed: $errstr ($errno)"];
    }
    stream_set_timeout($fp, 20);

    $read = function () use ($fp, &$log) {
        $data = '';
        while (($line = fgets($fp, 515)) !== false) {
            $data .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') {
                break;
            }
        }
        $log[] = 'S: ' . trim($data);
        return $data;
    };
    $cmd = function (string $c, array $ok, bool $hide = false) use ($fp, $read, &$log) {
        fwrite($fp, $c . "\r\n");
        $log[] = 'C: ' . ($hide ? '***' : $c);
        $resp = $read();
        if (!in_array((int) substr($resp, 0, 3), $ok, true)) {
            throw new RuntimeException('SMTP error after "' . ($hide ? '***' : $c) . '": ' . trim($resp));
        }
        return $resp;
    };

    try {
        $greet = $read();
        if ((int) substr($greet, 0, 3) !== 220) {
            throw new RuntimeException('bad greeting: ' . trim($greet));
        }
        $ehloHost = $_SERVER['SERVER_NAME'] ?? 'localhost';
        $cmd('EHLO ' . $ehloHost, [250]);
        if ($port !== 465) {
            $cmd('STARTTLS', [220]);
            if (!stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new RuntimeException('STARTTLS negotiation failed');
            }
            $cmd('EHLO ' . $ehloHost, [250]);
        }
        $cmd('AUTH LOGIN', [334]);
        $cmd(base64_encode($cfg['username']), [334], true);
        $cmd(base64_encode($cfg['password']), [235], true);
        $cmd('MAIL FROM:<' . $from . '>', [250]);
        foreach ($to as $rcpt) {
            $cmd('RCPT TO:<' . $rcpt . '>', [250, 251]);
        }
        $cmd('DATA', [354]);

        $enc = function (string $s) {
            return preg_match('/[^\x20-\x7E]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : $s;
        };
        $boundary = 'ce_' . bin2hex(random_bytes(10));
        $headers = [
            'Date: ' . date('r'),
            'From: ' . $enc($fromName) . ' <' . $from . '>',
            'To: ' . implode(', ', $to),
            'Subject: ' . $enc($subject),
            'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . substr(strrchr($from, '@'), 1) . '>',
            'MIME-Version: 1.0',
            'Content-Type: multipart/alternative; boundary="' . $boundary . '"',
        ];
        if ($replyTo) {
            $headers[] = 'Reply-To: ' . $replyTo;
        }
        $text = html_entity_decode(strip_tags(preg_replace('#<br\s*/?>#i', "\n", $html)), ENT_QUOTES, 'UTF-8');
        $doc = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.5;color:#1B2430">' . $html . '</body></html>';
        $qp = fn($s) => str_replace("\n", "\r\n", str_replace("\r\n", "\n", quoted_printable_encode($s)));
        $body = implode("\r\n", $headers) . "\r\n\r\n"
            . '--' . $boundary . "\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n" . $qp($text) . "\r\n"
            . '--' . $boundary . "\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n" . $qp($doc) . "\r\n"
            . '--' . $boundary . '--';
        // SMTP dot-stuffing
        $body = preg_replace('/^\./m', '..', $body);
        fwrite($fp, $body . "\r\n.\r\n");
        $resp = $read();
        if ((int) substr($resp, 0, 3) !== 250) {
            throw new RuntimeException('message rejected: ' . trim($resp));
        }
        $cmd('QUIT', [221]);
        fclose($fp);
        return [true, implode("\n", $log)];
    } catch (Throwable $e) {
        @fclose($fp);
        return [false, $e->getMessage() . "\n" . implode("\n", $log)];
    }
}
