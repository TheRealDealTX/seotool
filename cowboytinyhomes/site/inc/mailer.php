<?php
// Outgoing mail through the contact@ mailbox over authenticated SMTP (Hostinger).
// Credentials live in <STORE_PREFIX>-secrets.php in PRIVATE_DIR (one level above the web root), never in the repo:
//   <?php return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
//                 'smtp_user' => 'contact@example.com', 'smtp_pass' => '...'];
// A site may define SMTP_FALLBACK_FILE: an older secrets file returning host/port/user/pass,
// used when the secrets file has no SMTP keys. Without either, or if SMTP fails, it falls
// back to PHP mail().

function thb_secrets(): array {
    static $s = null;
    if ($s === null) {
        $f = PRIVATE_DIR . '/' . STORE_PREFIX . '-secrets.php';
        $s = is_file($f) ? (array)(include $f) : [];
        if (empty($s['smtp_pass']) && defined('SMTP_FALLBACK_FILE') && is_file(SMTP_FALLBACK_FILE)) {
            $l = (array)(include SMTP_FALLBACK_FILE);
            $s += ['smtp_host' => $l['host'] ?? null, 'smtp_port' => $l['port'] ?? null, 'smtp_user' => $l['user'] ?? null, 'smtp_pass' => $l['pass'] ?? null];
        }
    }
    return $s;
}

/** Send a plain-text email. Returns true when the message was accepted for delivery. */
function send_mail(string $to, string $subject, string $body, string $replyTo = '', string $replyName = ''): bool {
    $clean = function (string $v): string { return trim(str_replace(["\r", "\n"], ' ', $v)); };
    $s = thb_secrets();
    $from = $s['smtp_user'] ?? SITE_EMAIL;
    $subj = '=?UTF-8?B?' . base64_encode($clean($subject)) . '?=';
    $headers = [
        'Date: ' . date('r'),
        'From: =?UTF-8?B?' . base64_encode(SITE_NAME . ' Website') . "?= <$from>",
        "To: <$to>",
        "Subject: $subj",
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . parse_url(SITE_URL, PHP_URL_HOST) . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
        $headers[] = 'Reply-To: ' . ($replyName !== '' ? '=?UTF-8?B?' . base64_encode($clean($replyName)) . '?= ' : '') . '<' . $clean($replyTo) . '>';
    }
    $data = implode("\r\n", $headers) . "\r\n\r\n" . rtrim(chunk_split(base64_encode($body), 76, "\r\n"));

    if (!empty($s['smtp_pass']) && smtp_send($s, $from, $to, $data)) return true;

    // Fallback: local mail(). Headers other than To/Subject go in the extra-headers argument.
    $extra = array_filter($headers, function ($h) { return stripos($h, 'To:') !== 0 && stripos($h, 'Subject:') !== 0; });
    return @mail($to, $subj, chunk_split(base64_encode($body)), implode("\r\n", $extra), '-f' . $from);
}

function smtp_send(array $s, string $from, string $to, string $data): bool {
    $host = $s['smtp_host'] ?? 'smtp.hostinger.com';
    $port = (int)($s['smtp_port'] ?? 465);
    $fp = @stream_socket_client(($port === 465 ? 'ssl://' : 'tcp://') . "$host:$port", $errno, $errstr, 15);
    if (!$fp) { error_log("smtp connect failed: $errstr"); return false; }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) {
        $out = '';
        while (($line = fgets($fp, 515)) !== false) { $out .= $line; if (isset($line[3]) && $line[3] === ' ') break; }
        return $out;
    };
    $cmd = function (string $c, array $ok) use ($fp, $read) {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        $r = $read();
        if (!in_array((int)substr($r, 0, 3), $ok, true)) throw new RuntimeException(trim($r));
        return $r;
    };
    try {
        $cmd('', [220]);
        $ehlo = 'EHLO ' . parse_url(SITE_URL, PHP_URL_HOST);
        $cmd($ehlo, [250]);
        if ($port !== 465) {
            $cmd('STARTTLS', [220]);
            stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT);
            $cmd($ehlo, [250]);
        }
        $cmd('AUTH LOGIN', [334]);
        $cmd(base64_encode($s['smtp_user']), [334]);
        $cmd(base64_encode($s['smtp_pass']), [235]);
        $cmd("MAIL FROM:<$from>", [250]);
        $cmd("RCPT TO:<$to>", [250, 251]);
        $cmd('DATA', [354]);
        $cmd(preg_replace('/^\./m', '..', $data) . "\r\n.", [250]);
        $cmd('QUIT', [221]);
        fclose($fp);
        return true;
    } catch (Throwable $e) {
        error_log('smtp send failed: ' . $e->getMessage());
        @fclose($fp);
        return false;
    }
}
