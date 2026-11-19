<?php defined('SNW') || (http_response_code(404) && exit);
/*
 * Minimal authenticated SMTP sender (implicit TLS, port 465) for lead emails.
 *
 * Credentials come from app/secrets.php, which exists only on the server and is
 * git-ignored. Format:
 *   <?php defined('SNW') || (http_response_code(404) && exit);
 *   return ['smtp_host' => 'smtp.hostinger.com', 'smtp_port' => 465,
 *           'smtp_user' => 'info@seattlenorthwesthomes.com', 'smtp_pass' => '…'];
 * Without it, send_mail() falls back to PHP mail().
 */

function secrets(): array
{
    static $s = null;
    if ($s === null) {
        $f = APP . '/secrets.php';
        $s = is_file($f) ? (array) require $f : [];
    }
    return $s;
}

/** Returns true when the message was accepted by the SMTP server (or mail()). */
function send_mail(string $to, string $subject, string $body, string $replyTo = ''): bool
{
    $s = secrets();
    $from = $s['smtp_user'] ?? cfg('email');
    $encSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
    $headers = [
        'From: ' . '=?UTF-8?B?' . base64_encode(cfg('name')) . '?= <' . $from . '>',
        'To: <' . $to . '>',
        'Subject: ' . $encSubject,
        'Date: ' . date('r'),
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . substr(strrchr($from, '@'), 1) . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) $headers[] = 'Reply-To: <' . $replyTo . '>';

    if (empty($s['smtp_pass'])) {
        $h = array_filter($headers, fn($x) => !preg_match('/^(To|Subject):/', $x));
        return @mail($to, $encSubject, chunk_split(base64_encode($body)), implode("\r\n", $h));
    }

    $host = $s['smtp_host'] ?? 'smtp.hostinger.com';
    $port = (int) ($s['smtp_port'] ?? 465);
    $fp = @stream_socket_client('ssl://' . $host . ':' . $port, $errno, $errstr, 15);
    if (!$fp) { error_log("SMTP connect failed: $errstr"); return false; }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) {
        $out = '';
        while (($line = fgets($fp, 515)) !== false) { $out .= $line; if (isset($line[3]) && $line[3] === ' ') break; }
        return $out;
    };
    $cmd = function (string $c, array $ok) use ($fp, $read) {
        if ($c !== '') fwrite($fp, $c . "\r\n");
        $r = $read();
        if (!in_array((int) substr($r, 0, 3), $ok, true)) throw new RuntimeException(trim($r));
        return $r;
    };
    try {
        $cmd('', [220]);
        $cmd('EHLO ' . (parse_url(cfg('url'), PHP_URL_HOST) ?: 'localhost'), [250]);
        $cmd('AUTH LOGIN', [334]);
        $cmd(base64_encode($s['smtp_user']), [334]);
        $cmd(base64_encode($s['smtp_pass']), [235]);
        $cmd('MAIL FROM:<' . $from . '>', [250]);
        $cmd('RCPT TO:<' . $to . '>', [250, 251]);
        $cmd('DATA', [354]);
        $msg = implode("\r\n", $headers) . "\r\n\r\n" . chunk_split(base64_encode($body));
        $cmd(str_replace("\n.", "\n..", $msg) . "\r\n.", [250]);
        $cmd('QUIT', [221]);
        fclose($fp);
        return true;
    } catch (Throwable $e) {
        error_log('SMTP send failed: ' . $e->getMessage());
        @fclose($fp);
        return false;
    }
}
