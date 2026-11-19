<?php
defined('INC') || exit;
/**
 * Minimal authenticated SMTP sender (implicit TLS, AUTH LOGIN).
 * Credentials live ONLY on the server in data/smtp.php, never in the repository:
 *   <?php return ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => 'info@vintiqueflea.com', 'pass' => '…'];
 */

function smtp_config(): ?array
{
    $f = DATA_DIR . '/smtp.php';
    if (!is_file($f)) {
        return null;
    }
    $c = include $f;
    return is_array($c) && !empty($c['user']) && !empty($c['pass']) ? $c + ['host' => 'smtp.hostinger.com', 'port' => 465] : null;
}

function smtp_send(array $cfg, string $to, string $subject, string $body, string $replyTo = ''): bool
{
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $fp = @stream_socket_client('ssl://' . $cfg['host'] . ':' . (int) $cfg['port'], $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) {
        error_log("smtp connect failed: $errstr");
        return false;
    }
    stream_set_timeout($fp, 20);
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
    $cmd = function (string $c, array $ok) use ($fp, $read): bool {
        fwrite($fp, $c . "\r\n");
        $r = $read();
        if (!in_array((int) substr($r, 0, 3), $ok, true)) {
            error_log('smtp unexpected reply: ' . trim($r));
            return false;
        }
        return true;
    };
    $host = (string) parse_url(SITE_URL, PHP_URL_HOST);
    $ok = (int) substr($read(), 0, 3) === 220
        && $cmd("EHLO $host", [250])
        && $cmd('AUTH LOGIN', [334])
        && $cmd(base64_encode($cfg['user']), [334])
        && $cmd(base64_encode($cfg['pass']), [235])
        && $cmd('MAIL FROM:<' . $cfg['user'] . '>', [250])
        && $cmd('RCPT TO:<' . $to . '>', [250, 251])
        && $cmd('DATA', [354]);
    if ($ok) {
        $h = 'Date: ' . date('r') . "\r\n"
            . 'From: ' . SITE_NAME . ' Website <' . $cfg['user'] . ">\r\n"
            . "To: <$to>\r\n"
            . "Subject: $subject\r\n"
            . 'Message-ID: <' . bin2hex(random_bytes(10)) . "@$host>\r\n"
            . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n";
        if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
            $h .= "Reply-To: $replyTo\r\n";
        }
        $body = str_replace(["\r\n", "\r"], "\n", $body);
        $body = preg_replace('/^\./m', '..', $body);
        $ok = $cmd($h . "\r\n" . str_replace("\n", "\r\n", $body) . "\r\n.", [250]);
    }
    @fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}
