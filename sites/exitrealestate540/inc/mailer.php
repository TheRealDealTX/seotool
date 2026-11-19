<?php
defined('ERE') or exit;

/**
 * Minimal authenticated SMTP sender (implicit TLS, AUTH LOGIN) - enough for the
 * contact form, with no Composer dependency.
 *
 * Credentials are NOT in the repository. They live on the server only, in
 * site-data/smtp.php, which returns:
 *   ['host' => 'smtp.hostinger.com', 'port' => 465, 'user' => 'info@exitrealestate540.com', 'pass' => '...']
 *
 * Returns [bool $ok, string $error].
 */
function smtp_send(string $to, string $subject, string $body, string $replyTo = ''): array
{
    $file = ROOT . '/site-data/smtp.php';
    if (!is_file($file)) {
        return [false, 'smtp credentials missing'];
    }
    $c = require $file;
    $from = $c['user'];
    $fp = @stream_socket_client('ssl://' . $c['host'] . ':' . ($c['port'] ?? 465), $errno, $errstr, 15);
    if (!$fp) {
        return [false, "connect: $errstr ($errno)"];
    }
    stream_set_timeout($fp, 15);

    $read = function () use ($fp): string {
        $out = '';
        while (($line = fgets($fp, 1024)) !== false) {
            $out .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') {
                break;
            }
        }
        return $out;
    };
    $cmd = function (string $line, array $expect) use ($fp, $read): string {
        if ($line !== '') {
            fwrite($fp, $line . "\r\n");
        }
        $resp = $read();
        if (!in_array((int) substr($resp, 0, 3), $expect, true)) {
            throw new RuntimeException(trim($resp) ?: 'no response');
        }
        return $resp;
    };

    $clean = fn(string $s) => trim(preg_replace('/[\r\n]+/', ' ', $s));
    $headers = [
        'Date: ' . date('r'),
        'From: "Exit Real Estate 540" <' . $from . '>',
        'To: <' . $to . '>',
        'Subject: =?UTF-8?B?' . base64_encode($clean($subject)) . '?=',
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@exitrealestate540.com>',
        'MIME-Version: 1.0',
        'Content-Type: text/plain; charset=UTF-8',
        'Content-Transfer-Encoding: 8bit',
    ];
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
        $headers[] = 'Reply-To: <' . $clean($replyTo) . '>';
    }
    $data = implode("\r\n", $headers) . "\r\n\r\n" . str_replace("\n.", "\n..", str_replace(["\r\n", "\r"], "\n", $body));
    $data = str_replace("\n", "\r\n", $data);

    try {
        $cmd('', [220]);
        $cmd('EHLO exitrealestate540.com', [250]);
        $cmd('AUTH LOGIN', [334]);
        $cmd(base64_encode($c['user']), [334]);
        $cmd(base64_encode($c['pass']), [235]);
        $cmd('MAIL FROM:<' . $from . '>', [250]);
        $cmd('RCPT TO:<' . $to . '>', [250, 251]);
        $cmd('DATA', [354]);
        $cmd($data . "\r\n.", [250]);
        $cmd('QUIT', [221]);
        fclose($fp);
        return [true, ''];
    } catch (Throwable $e) {
        @fclose($fp);
        return [false, substr($e->getMessage(), 0, 200)];
    }
}
