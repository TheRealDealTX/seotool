<?php
// Minimal authenticated SMTP sender (SSL, AUTH LOGIN) for lead notifications.
// Sending through the domain's own mailbox keeps SPF/DKIM aligned so mail
// lands in the inbox instead of spam. Falls back to mail() without credentials.
defined('HA_ROOT') || exit;

final class Mailer
{
    public static function send(string $to, string $subject, string $text, string $replyTo = '', ?string $html = null): bool
    {
        $from = config('smtp_user') ?: SITE['email'];
        $headers = [
            'Date: ' . date('r'),
            'From: "Houston Apartments Website" <' . $from . '>',
            'To: <' . $to . '>',
            'Subject: ' . self::encode($subject),
            'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . substr(strrchr($from, '@'), 1) . '>',
            'MIME-Version: 1.0',
        ];
        if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
            $headers[] = 'Reply-To: <' . $replyTo . '>';
        }
        if ($html !== null) {
            $b = 'b' . bin2hex(random_bytes(8));
            $headers[] = 'Content-Type: multipart/alternative; boundary="' . $b . '"';
            $body = "--$b\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($text))
                  . "--$b\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($html)) . "--$b--\r\n";
        } else {
            $headers[] = 'Content-Type: text/plain; charset=UTF-8';
            $headers[] = 'Content-Transfer-Encoding: base64';
            $body = chunk_split(base64_encode($text));
        }

        if (!config('smtp_pass')) {
            $hdr = array_values(array_filter($headers, fn ($h) => !preg_match('/^(To|Subject|Date):/', $h)));
            return @mail($to, self::encode($subject), $body, implode("\r\n", $hdr));
        }
        try {
            self::smtp($from, $to, implode("\r\n", $headers) . "\r\n\r\n" . $body);
            return true;
        } catch (Throwable $e) {
            error_log('SMTP send failed: ' . $e->getMessage());
            return false;
        }
    }

    private static function encode(string $s): string
    {
        return preg_match('/[^\x20-\x7e]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : $s;
    }

    private static function smtp(string $from, string $to, string $message): void
    {
        $host = config('smtp_host', 'smtp.hostinger.com');
        $port = (int) config('smtp_port', 465);
        $fp = stream_socket_client("ssl://$host:$port", $errno, $errstr, 20);
        if (!$fp) {
            throw new RuntimeException("connect $host:$port – $errstr");
        }
        stream_set_timeout($fp, 20);
        $expect = function (string $code) use ($fp) {
            $resp = '';
            while (($line = fgets($fp, 1024)) !== false) {
                $resp .= $line;
                if (isset($line[3]) && $line[3] === ' ') {
                    break;
                }
            }
            if (strncmp($resp, $code, 3) !== 0) {
                throw new RuntimeException('SMTP expected ' . $code . ', got: ' . trim($resp));
            }
        };
        $cmd = function (string $c, string $code) use ($fp, $expect) {
            fwrite($fp, $c . "\r\n");
            $expect($code);
        };
        $expect('220');
        $cmd('EHLO ' . (gethostname() ?: 'localhost'), '250');
        $cmd('AUTH LOGIN', '334');
        $cmd(base64_encode(config('smtp_user')), '334');
        $cmd(base64_encode(config('smtp_pass')), '235');
        $cmd("MAIL FROM:<$from>", '250');
        $cmd("RCPT TO:<$to>", '250');
        $cmd('DATA', '354');
        // dot-stuffing per RFC 5321
        $message = preg_replace('/^\./m', '..', str_replace(["\r\n", "\n"], ["\n", "\r\n"], $message));
        fwrite($fp, $message . "\r\n.\r\n");
        $expect('250');
        fwrite($fp, "QUIT\r\n");
        fclose($fp);
    }
}
