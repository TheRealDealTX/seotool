<?php
/**
 * Sends lead emails as info@sugarlandpublicadjuster.com.
 *
 * Preferred: authenticated SMTP through Hostinger (smtp.hostinger.com:465) using
 * the info@ mailbox. Credentials live OUTSIDE the web root in
 *   ../slpa-private/smtp.php   (returns ['host'=>..., 'port'=>465, 'secure'=>'ssl', 'user'=>..., 'pass'=>...])
 * Fallback when that file is missing or SMTP fails: PHP mail() with info@ as the
 * From address and envelope sender.
 */

function smtp_config(): ?array
{
    $file = dirname(__DIR__, 2) . '/slpa-private/smtp.php';
    if (!is_file($file)) {
        return null;
    }
    $c = include $file;
    return is_array($c) && !empty($c['user']) && !empty($c['pass']) ? $c : null;
}

/** Returns [bool ok, string method, string error]. */
function send_mail(string $to, string $subject, string $body, string $replyTo = '', string $replyName = ''): array
{
    $from = SITE['mail_from'];
    $host = parse_url(SITE['origin'], PHP_URL_HOST);
    $encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
    $encName = '=?UTF-8?B?' . base64_encode(SITE['name']) . '?=';
    $headers = [
        'Date: ' . date('r'),
        'From: ' . $encName . ' <' . $from . '>',
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $host . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
        'X-Mailer: SLPA-Lead/2.0',
    ];
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
        $name = trim(preg_replace('/[\r\n"<>]/', '', $replyName));
        $headers[] = 'Reply-To: ' . ($name !== '' ? '=?UTF-8?B?' . base64_encode($name) . '?= ' : '') . '<' . $replyTo . '>';
    }
    $encodedBody = rtrim(chunk_split(base64_encode($body), 76, "\r\n"));

    $err = '';
    if ($cfg = smtp_config()) {
        [$ok, $err] = smtp_send($cfg, $from, $to, array_merge(['To: <' . $to . '>', 'Subject: ' . $encSubject], $headers), $encodedBody);
        if ($ok) {
            return [true, 'smtp', ''];
        }
    }
    $ok = @mail($to, $encSubject, $encodedBody, implode("\r\n", $headers), '-f' . $from);
    return [$ok, 'mail()', $err];
}

/** Minimal SMTP client (implicit TLS on 465, STARTTLS on 587, or plain). Returns [bool, error]. */
function smtp_send(array $c, string $from, string $to, array $headers, string $body): array
{
    $host = $c['host'] ?? 'smtp.hostinger.com';
    $port = (int) ($c['port'] ?? 465);
    $secure = $c['secure'] ?? 'ssl';
    $remote = ($secure === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port;
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $fp = @stream_socket_client($remote, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) {
        return [false, "connect: $errstr"];
    }
    stream_set_timeout($fp, 20);
    $read = function () use ($fp) {
        $data = '';
        while (($line = fgets($fp, 515)) !== false) {
            $data .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') {
                break;
            }
        }
        return $data;
    };
    $cmd = function (string $line, array $expect) use ($fp, $read) {
        if ($line !== '') {
            fwrite($fp, $line . "\r\n");
        }
        $resp = $read();
        if (!in_array((int) substr($resp, 0, 3), $expect, true)) {
            throw new RuntimeException(trim(preg_replace('/\s+/', ' ', ($line && stripos($line, 'AUTH') === false ? $line . ' -> ' : '') . $resp)));
        }
        return $resp;
    };
    try {
        $me = parse_url(SITE['origin'], PHP_URL_HOST);
        $cmd('', [220]);
        $cmd('EHLO ' . $me, [250]);
        if ($secure === 'tls') {
            $cmd('STARTTLS', [220]);
            if (!stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new RuntimeException('STARTTLS failed');
            }
            $cmd('EHLO ' . $me, [250]);
        }
        $cmd('AUTH LOGIN', [334]);
        $cmd(base64_encode($c['user']), [334]);
        $cmd(base64_encode($c['pass']), [235]);
        $cmd('MAIL FROM:<' . $from . '>', [250]);
        $cmd('RCPT TO:<' . $to . '>', [250, 251]);
        $cmd('DATA', [354]);
        $msg = implode("\r\n", $headers) . "\r\n\r\n" . $body;
        $msg = preg_replace('/^\./m', '..', $msg);
        $cmd($msg . "\r\n.", [250]);
        $cmd('QUIT', [221]);
        fclose($fp);
        return [true, ''];
    } catch (Throwable $e) {
        @fclose($fp);
        return [false, $e->getMessage()];
    }
}
