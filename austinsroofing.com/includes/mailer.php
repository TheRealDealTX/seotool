<?php
/**
 * Minimal authenticated SMTP sender (SSL, AUTH LOGIN) so form mail goes out
 * through the info@austinsroofing.com mailbox instead of PHP mail().
 *
 * Credentials live in includes/.smtp.php on the server only (never in git):
 *   <?php return ['host' => 'smtp.hostinger.com', 'port' => 465,
 *                 'user' => 'info@austinsroofing.com', 'pass' => '...'];
 */

function smtp_config(): ?array
{
    $f = __DIR__ . '/.smtp.php';
    return is_readable($f) ? (include $f) : null;
}

/** Send a plain-text email. Returns true on success; $error gets the reason on failure. */
function smtp_send(array $cfg, string $to, string $subject, string $body, string $replyTo = '', ?string &$error = null): bool
{
    $fp = @stream_socket_client('ssl://' . $cfg['host'] . ':' . (int) $cfg['port'], $errno, $errstr, 15);
    if (!$fp) {
        $error = "connect: $errstr ($errno)";
        return false;
    }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp): string {
        $resp = '';
        while (($line = fgets($fp, 515)) !== false) {
            $resp .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') {
                break;
            }
        }
        return $resp;
    };
    $cmd = function (?string $line, string $expect) use ($fp, $read, &$error): bool {
        if ($line !== null) {
            fwrite($fp, $line . "\r\n");
        }
        $resp = $read();
        if (strncmp($resp, $expect, strlen($expect)) !== 0) {
            $error = trim(($line !== null && stripos($line, 'AUTH') === false && strlen($line) < 200 ? $line : '[cmd]') . ' -> ' . $resp);
            return false;
        }
        return true;
    };

    $from = $cfg['user'];
    $host = parse_url(BIZ['origin'], PHP_URL_HOST) ?: 'localhost';
    $headers = [
        'Date: ' . date('r'),
        'From: Austin Roofing Website <' . $from . '>',
        'To: <' . $to . '>',
        'Subject: =?UTF-8?B?' . base64_encode($subject) . '?=',
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $host . '>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    ];
    if ($replyTo !== '') {
        $headers[] = 'Reply-To: ' . $replyTo;
    }
    // Normalise newlines and dot-stuff the body.
    $body = preg_replace("/\r\n|\r|\n/", "\r\n", $body);
    $body = preg_replace('/^\./m', '..', $body);
    $data = implode("\r\n", $headers) . "\r\n\r\n" . $body . "\r\n.";

    $ok = $cmd(null, '220')
        && $cmd('EHLO ' . $host, '250')
        && $cmd('AUTH LOGIN', '334')
        && $cmd(base64_encode($cfg['user']), '334')
        && $cmd(base64_encode($cfg['pass']), '235')
        && $cmd('MAIL FROM:<' . $from . '>', '250')
        && $cmd('RCPT TO:<' . $to . '>', '25')
        && $cmd('DATA', '354')
        && $cmd($data, '250');
    @fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}
