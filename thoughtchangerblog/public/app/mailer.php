<?php
// Minimal authenticated SMTP client (implicit TLS on 465 or STARTTLS on 587). No dependencies.
declare(strict_types=1);

final class Mailer {
    private $sock;
    private array $log = [];

    public function __construct(private array $cfg) {}

    public function send(string $to, string $subject, string $text, ?string $replyTo = null, ?string $replyName = null): bool {
        $c = $this->cfg;
        if ($c['smtp_pass'] === '') { error_log('Mailer: smtp_pass not configured'); return false; }
        try {
            $host = ((int) $c['smtp_port'] === 465 ? 'ssl://' : 'tcp://') . $c['smtp_host'] . ':' . $c['smtp_port'];
            $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => $c['smtp_host']]]);
            $this->sock = @stream_socket_client($host, $errno, $err, 20, STREAM_CLIENT_CONNECT, $ctx);
            if (!$this->sock) throw new RuntimeException("connect: $err");
            stream_set_timeout($this->sock, 20);
            $this->expect(220);
            $ehlo = 'thoughtchangerblog.com';
            $this->cmd("EHLO $ehlo", 250);
            if ((int) $c['smtp_port'] !== 465) {
                $this->cmd('STARTTLS', 220);
                if (!stream_socket_enable_crypto($this->sock, true, STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT | STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT)) throw new RuntimeException('starttls');
                $this->cmd("EHLO $ehlo", 250);
            }
            $this->cmd('AUTH LOGIN', 334);
            $this->cmd(base64_encode($c['smtp_user']), 334);
            $this->cmd(base64_encode($c['smtp_pass']), 235);
            $this->cmd('MAIL FROM:<' . $c['smtp_user'] . '>', 250);
            $this->cmd('RCPT TO:<' . $to . '>', [250, 251]);
            $this->cmd('DATA', 354);
            $h = [
                'Date: ' . date('r'),
                'From: ' . $this->enc(SITE_NAME . ' Website') . ' <' . $c['smtp_user'] . '>',
                'To: <' . $to . '>',
                'Subject: ' . $this->enc($subject),
                'Message-ID: <' . bin2hex(random_bytes(12)) . '@thoughtchangerblog.com>',
                'MIME-Version: 1.0',
                'Content-Type: text/plain; charset=UTF-8',
                'Content-Transfer-Encoding: base64',
            ];
            if ($replyTo && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
                $h[] = 'Reply-To: ' . ($replyName ? $this->enc($replyName) . ' ' : '') . '<' . $replyTo . '>';
            }
            $data = implode("\r\n", $h) . "\r\n\r\n" . rtrim(chunk_split(base64_encode($text), 76, "\r\n")) . "\r\n.";
            $this->cmd($data, 250);
            $this->cmd('QUIT', 221);
            fclose($this->sock);
            return true;
        } catch (Throwable $ex) {
            error_log('Mailer failed: ' . $ex->getMessage() . ' | ' . implode(' / ', array_slice($this->log, -3)));
            if ($this->sock) @fclose($this->sock);
            return false;
        }
    }

    private function enc(string $s): string {
        return preg_match('/[^\x20-\x7E]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : $s;
    }

    private function cmd(string $line, int|array $ok): void {
        fwrite($this->sock, $line . "\r\n");
        $this->expect($ok);
    }

    private function expect(int|array $ok): void {
        $resp = '';
        while (($l = fgets($this->sock, 515)) !== false) {
            $resp .= $l;
            if (strlen($l) < 4 || $l[3] === ' ') break;
        }
        $this->log[] = trim($resp);
        $code = (int) substr($resp, 0, 3);
        if (!in_array($code, (array) $ok, true)) throw new RuntimeException('SMTP ' . trim($resp));
    }
}
