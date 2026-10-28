<?php
declare(strict_types=1);
// Minimal authenticated SMTP client (implicit TLS on 465 or STARTTLS on 587). Direct requests are denied by .htaccess.
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === basename(__FILE__)) { http_response_code(404); exit; }

class MailError extends RuntimeException {}

final class SmtpMailer {
    /** @var resource|null */
    private $socket = null;
    public function __construct(private array $config) {}

    public function send(string $to, string $subject, string $text, string $html, ?string $replyTo = null, ?string $replyName = null): void {
        $from = $this->config['from'] ?? $this->config['user'];
        $fromName = $this->config['from_name'] ?? 'Website';
        $port = (int)($this->config['port'] ?? 465);
        $host = $this->config['host'];
        $context = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => $host]]);
        $target = ($port === 465 ? 'ssl://' : 'tcp://') . $host . ':' . $port;
        $this->socket = @stream_socket_client($target, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $context);
        if (!$this->socket) throw new MailError("SMTP connection failed: $errstr ($errno)");
        stream_set_timeout($this->socket, 20);
        try {
            $this->expect(220);
            $domain = preg_replace('/[^a-z0-9.-]/i', '', $_SERVER['SERVER_NAME'] ?? 'localhost') ?: 'localhost';
            $this->command("EHLO $domain", 250);
            if ($port !== 465) {
                $this->command('STARTTLS', 220);
                if (!stream_socket_enable_crypto($this->socket, true, STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT | STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT)) throw new MailError('STARTTLS negotiation failed.');
                $this->command("EHLO $domain", 250);
            }
            $this->command('AUTH LOGIN', 334);
            $this->command(base64_encode($this->config['user']), 334);
            $this->command(base64_encode($this->config['pass']), 235);
            $this->command('MAIL FROM:<' . $from . '>', 250);
            $this->command('RCPT TO:<' . $to . '>', [250, 251]);
            $this->command('DATA', 354);
            $boundary = 'jm-' . bin2hex(random_bytes(12));
            $headers = [
                'Date: ' . date(DATE_RFC2822),
                'Message-ID: <' . bin2hex(random_bytes(16)) . '@' . substr(strrchr($from, '@'), 1) . '>',
                'From: ' . $this->mailbox($from, $fromName),
                'To: <' . $to . '>',
                'Subject: ' . $this->encodeHeader($subject),
                'MIME-Version: 1.0',
                'Content-Type: multipart/alternative; boundary="' . $boundary . '"',
                'X-Mailer: jmautida.com contact form',
            ];
            if ($replyTo) $headers[] = 'Reply-To: ' . $this->mailbox($replyTo, $replyName ?? '');
            $body = implode("\r\n", $headers) . "\r\n\r\n"
                . "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($text)) . "\r\n"
                . "--$boundary\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . chunk_split(base64_encode($html)) . "\r\n"
                . "--$boundary--\r\n";
            // Dot-stuffing: lines that begin with "." get an extra dot.
            $body = preg_replace('/^\./m', '..', $body);
            fwrite($this->socket, $body . "\r\n.\r\n");
            $this->expect(250);
            $this->command('QUIT', 221);
        } finally {
            if (is_resource($this->socket)) fclose($this->socket);
            $this->socket = null;
        }
    }

    private function mailbox(string $email, string $name): string {
        return $name === '' ? "<$email>" : $this->encodeHeader($name) . " <$email>";
    }
    private function encodeHeader(string $value): string {
        $value = str_replace(["\r", "\n"], ' ', $value);
        return preg_match('/[^\x20-\x7e]/', $value) ? '=?UTF-8?B?' . base64_encode($value) . '?=' : $value;
    }
    private function command(string $line, int|array $code): string {
        fwrite($this->socket, $line . "\r\n");
        return $this->expect($code);
    }
    private function expect(int|array $codes): string {
        $response = '';
        while (($line = fgets($this->socket, 1024)) !== false) {
            $response .= $line;
            if (strlen($line) < 4 || $line[3] === ' ') break;
        }
        $status = (int)substr($response, 0, 3);
        if (!in_array($status, (array)$codes, true)) throw new MailError('SMTP error: ' . trim($response));
        return $response;
    }
}
