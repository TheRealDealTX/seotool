<?php
// Minimal authenticated SMTP sender (Hostinger mail, SSL on port 465).
// Credentials live outside the web root in lad-data/mail.php:
//   <?php return ['host' => 'smtp.hostinger.com', 'port' => 465,
//                 'user' => 'info@luxuryapartmentdesign.com', 'pass' => '…'];

function mail_config(): ?array
{
    $file = dirname(__DIR__, 2) . '/lad-data/mail.php';
    $cfg = is_file($file) ? include $file : null;
    return is_array($cfg) && !empty($cfg['user']) && !empty($cfg['pass']) ? $cfg : null;
}

/** Send a plain-text email. Returns true on success. */
function smtp_send(string $to, string $subject, string $body, string $replyTo = ''): bool
{
    $cfg = mail_config();
    if (!$cfg) {
        return false;
    }
    $host = $cfg['host'] ?? 'smtp.hostinger.com';
    $port = (int) ($cfg['port'] ?? 465);
    $fp = @stream_socket_client("ssl://$host:$port", $errno, $errstr, 15);
    if (!$fp) {
        error_log("smtp connect failed: $errstr");
        return false;
    }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp): string {
        $out = '';
        while (($line = fgets($fp, 515)) !== false) {
            $out .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') break;
        }
        return $out;
    };
    $cmd = function (string $c, array $ok) use ($fp, $read): bool {
        fwrite($fp, $c . "\r\n");
        $r = $read();
        if (!in_array((int) substr($r, 0, 3), $ok, true)) {
            error_log('smtp error after ' . strtok($c, ' ') . ': ' . trim($r));
            return false;
        }
        return true;
    };
    $clean = fn($s) => str_replace(["\r", "\n"], ' ', $s);
    $from = $cfg['user'];
    $headers = [
        'Date: ' . date('r'),
        'From: ' . SITE_NAME . ' <' . $from . '>',
        'To: <' . $clean($to) . '>',
        'Subject: =?UTF-8?B?' . base64_encode($clean($subject)) . '?=',
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@luxuryapartmentdesign.com>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: base64',
    ];
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
        $headers[] = 'Reply-To: <' . $replyTo . '>';
    }
    $data = implode("\r\n", $headers) . "\r\n\r\n" . chunk_split(base64_encode($body));

    $ok = (int) substr($read(), 0, 3) === 220
        && $cmd('EHLO luxuryapartmentdesign.com', [250])
        && $cmd('AUTH LOGIN', [334])
        && $cmd(base64_encode($cfg['user']), [334])
        && $cmd(base64_encode($cfg['pass']), [235])
        && $cmd('MAIL FROM:<' . $from . '>', [250])
        && $cmd('RCPT TO:<' . $clean($to) . '>', [250, 251])
        && $cmd('DATA', [354])
        && $cmd($data . "\r\n.", [250]);
    @fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}
