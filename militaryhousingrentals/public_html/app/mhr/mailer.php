<?php
// Minimal SMTP client: implicit TLS (port 465) with AUTH LOGIN, UTF-8 mail
// (plain text, optionally with an HTML part). Settings come from the private config ('smtp' => [...]). Every send is
// written to the PHP error log on failure; nothing here ever echoes the password.

// Optional $html adds an HTML part (multipart/alternative) next to the plain text.
function mhr_mail($to, $subject, $body, $reply_to = null, &$error = null, $html = null) {
    $s = mhr_cfg('smtp') ?: [];
    $from = $s['from'] ?? cfg('email');
    $from_name = $s['from_name'] ?? cfg('name');
    if (mhr_cfg('dev') && !empty($s['capture_dir'])) return mhr_mail_capture($s['capture_dir'], $to, $subject, $body, $html);
    if (empty($s['pass'])) { $error = 'SMTP password is not set in the private config.'; error_log('mhr mail: ' . $error); return false; }

    $clean = fn($v) => preg_replace('/[\r\n]+/', ' ', (string)$v);
    $to = $clean($to);
    if (!filter_var($to, FILTER_VALIDATE_EMAIL)) { $error = 'Invalid recipient.'; return false; }
    $host = $s['host'] ?? 'smtp.hostinger.com';
    $port = (int)($s['port'] ?? 465);

    $headers = [
        'Date: ' . date('r'),
        'From: ' . mhr_mime_header($from_name) . " <$from>",
        "To: <$to>",
        'Subject: ' . mhr_mime_header($subject),
        'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . (parse_url(cfg('origin'), PHP_URL_HOST) ?: 'localhost') . '>',
        'MIME-Version: 1.0',
    ];
    if ($reply_to && filter_var($reply_to, FILTER_VALIDATE_EMAIL)) $headers[] = 'Reply-To: <' . $clean($reply_to) . '>';
    $b64 = fn($t) => rtrim(chunk_split(base64_encode(str_replace("\n", "\r\n", str_replace("\r\n", "\n", $t))), 76, "\r\n"));
    if ($html === null) {
        $headers[] = 'Content-Type: text/plain; charset=UTF-8';
        $headers[] = 'Content-Transfer-Encoding: base64';
        $data = implode("\r\n", $headers) . "\r\n\r\n" . $b64($body);
    } else {
        $bd = 'mhr-' . bin2hex(random_bytes(12));
        $headers[] = 'Content-Type: multipart/alternative; boundary="' . $bd . '"';
        $data = implode("\r\n", $headers) . "\r\n\r\n"
            . "--$bd\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . $b64($body) . "\r\n"
            . "--$bd\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n" . $b64($html) . "\r\n"
            . "--$bd--";
    }

    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => $host]]);
    $fp = @stream_socket_client("ssl://$host:$port", $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) { $error = "Could not connect to $host:$port ($errstr)"; error_log('mhr mail: ' . $error); return false; }
    stream_set_timeout($fp, 20);
    try {
        $ehlo = parse_url(cfg('origin'), PHP_URL_HOST) ?: 'localhost';
        mhr_smtp($fp, null, 220);
        mhr_smtp($fp, "EHLO $ehlo", 250);
        mhr_smtp($fp, 'AUTH LOGIN', 334);
        mhr_smtp($fp, base64_encode($s['user'] ?? $from), 334);
        mhr_smtp($fp, base64_encode($s['pass']), 235, true);
        mhr_smtp($fp, "MAIL FROM:<$from>", 250);
        mhr_smtp($fp, "RCPT TO:<$to>", [250, 251]);
        mhr_smtp($fp, 'DATA', 354);
        mhr_smtp($fp, preg_replace('/^\./m', '..', $data) . "\r\n.", 250);
        mhr_smtp($fp, 'QUIT', 221);
        return true;
    } catch (RuntimeException $e) {
        $error = $e->getMessage();
        error_log('mhr mail: ' . $error);
        return false;
    } finally {
        fclose($fp);
    }
}

function mhr_smtp($fp, $cmd, $expect, $secret = false) {
    if ($cmd !== null) fwrite($fp, $cmd . "\r\n");
    $resp = '';
    while (($line = fgets($fp, 1024)) !== false) {
        $resp .= $line;
        if (strlen($line) < 4 || $line[3] === ' ') break;
    }
    $code = (int)substr($resp, 0, 3);
    if (!in_array($code, (array)$expect, true)) {
        $shown = $secret ? '[credentials]' : ($cmd === null ? 'connect' : strtok($cmd, "\r\n"));
        if (str_starts_with((string)$cmd, 'MAIL') || str_starts_with((string)$cmd, 'RCPT')) $shown = strtok($cmd, ':');
        throw new RuntimeException("SMTP $shown failed: " . trim($resp ?: 'no response'));
    }
    return $resp;
}

function mhr_mime_header($s) {
    return preg_match('/[^\x20-\x7e]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : $s;
}

// Local development: write mail to files instead of sending.
function mhr_mail_capture($dir, $to, $subject, $body, $html = null) {
    if (!is_dir($dir)) mkdir($dir, 0700, true);
    $base = $dir . '/' . date('Ymd-His') . '-' . bin2hex(random_bytes(3));
    file_put_contents("$base.txt", "To: $to\nSubject: $subject\n\n$body");
    if ($html !== null) file_put_contents("$base.html", $html);
    return true;
}
