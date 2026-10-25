<?php
/**
 * Minimal authenticated SMTP sender (implicit TLS, AUTH LOGIN) used by api/form.php.
 *
 * Credentials come from inc/mail-config.php, which is NOT in git (see mail-config.example.php).
 * Returns true when the server accepted the message; on failure returns false and sets $err.
 */
function smtp_send(string $to, string $subject, string $body, string $replyTo, ?string &$err = null): bool
{
    $cfgFile = __DIR__ . '/mail-config.php';
    if (!is_file($cfgFile)) {
        $err = 'mail-config.php missing';
        return false;
    }
    $cfg = require $cfgFile; // ['host','port','user','pass','from_name']

    $fp = @stream_socket_client('ssl://' . $cfg['host'] . ':' . $cfg['port'], $errno, $errstr, 15);
    if (!$fp) {
        $err = "connect: $errstr ($errno)";
        return false;
    }
    stream_set_timeout($fp, 15);

    $read = function () use ($fp): string {
        $data = '';
        while (($line = fgets($fp, 515)) !== false) {
            $data .= $line;
            if (isset($line[3]) && $line[3] === ' ') {
                break;
            }
        }
        return $data;
    };
    $cmd = function (string $line, array $ok) use ($fp, $read, &$err): bool {
        if ($line !== '') {
            fwrite($fp, $line . "\r\n");
        }
        $resp = $read();
        if (!in_array((int) substr($resp, 0, 3), $ok, true)) {
            $err = trim(($line !== '' && stripos($line, 'AUTH') === false && strlen($line) < 80 ? $line . ' -> ' : '') . $resp);
            return false;
        }
        return true;
    };

    $host = $_SERVER['SERVER_NAME'] ?? 'monetizinginfluencers.com';
    $from = $cfg['user'];
    $date = date('r');
    $msgId = '<' . bin2hex(random_bytes(12)) . '@monetizinginfluencers.com>';
    $headers = 'Date: ' . $date . "\r\n"
        . 'Message-ID: ' . $msgId . "\r\n"
        . 'From: =?UTF-8?B?' . base64_encode($cfg['from_name']) . '?= <' . $from . ">\r\n"
        . 'To: <' . $to . ">\r\n"
        . 'Reply-To: ' . $replyTo . "\r\n"
        . 'Subject: =?UTF-8?B?' . base64_encode($subject) . "?=\r\n"
        . "MIME-Version: 1.0\r\n"
        . "Content-Type: text/plain; charset=UTF-8\r\n"
        . "Content-Transfer-Encoding: base64\r\n";
    $data = $headers . "\r\n" . chunk_split(base64_encode($body)) . "\r\n.";

    $ok = $cmd('', [220])
        && $cmd('EHLO ' . $host, [250])
        && $cmd('AUTH LOGIN', [334])
        && $cmd(base64_encode($cfg['user']), [334])
        && $cmd(base64_encode($cfg['pass']), [235])
        && $cmd('MAIL FROM:<' . $from . '>', [250])
        && $cmd('RCPT TO:<' . $to . '>', [250, 251])
        && $cmd('DATA', [354])
        && $cmd($data, [250]);
    @fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}
