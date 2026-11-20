<?php defined('WCA') || exit;

/**
 * Minimal SMTP client (SSL on 465 or STARTTLS on 587) for the Hostinger mailbox.
 * Returns true on success; failures are logged to the PHP error log.
 */
function send_mail(string $to, string $subject, string $html, ?string $replyTo = null): bool
{
    $s = cfg('smtp');
    $fromEmail = $s['from'];
    $fromName = $s['from_name'] ?? cfg('site_name');
    $text = trim(html_entity_decode(strip_tags(preg_replace(['/<br\s*\/?>/i', '/<\/p>/i', '/<a [^>]*href="([^"]+)"[^>]*>(.*?)<\/a>/i'], ["\n", "\n\n", '$2 ($1)'], $html)), ENT_QUOTES, 'UTF-8'));
    $boundary = 'b' . bin2hex(random_bytes(8));
    $domain = substr(strrchr($fromEmail, '@'), 1);

    $headers = [
        'Date: ' . date('r'),
        'From: ' . mime_header($fromName) . " <$fromEmail>",
        "To: <$to>",
        'Subject: ' . mime_header($subject),
        'Message-ID: <' . bin2hex(random_bytes(12)) . "@$domain>",
        'MIME-Version: 1.0',
        "Content-Type: multipart/alternative; boundary=\"$boundary\"",
    ];
    if ($replyTo) $headers[] = "Reply-To: <$replyTo>";

    $body = "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($text))
        . "--$boundary\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode(email_wrap($subject, $html)))
        . "--$boundary--\r\n";
    $data = implode("\r\n", $headers) . "\r\n\r\n" . $body;

    try {
        $port = (int)($s['port'] ?? 465);
        $host = ($port === 465 ? 'ssl://' : 'tcp://') . $s['host'];
        $fp = @stream_socket_client("$host:$port", $errno, $errstr, 15);
        if (!$fp) throw new RuntimeException("connect failed: $errstr");
        stream_set_timeout($fp, 15);
        smtp_expect($fp, 220);
        smtp_cmd($fp, 'EHLO ' . $domain, 250);
        if ($port === 587) {
            smtp_cmd($fp, 'STARTTLS', 220);
            stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT);
            smtp_cmd($fp, 'EHLO ' . $domain, 250);
        }
        smtp_cmd($fp, 'AUTH LOGIN', 334);
        smtp_cmd($fp, base64_encode($s['user']), 334);
        smtp_cmd($fp, base64_encode($s['pass']), 235);
        smtp_cmd($fp, "MAIL FROM:<$fromEmail>", 250);
        smtp_cmd($fp, "RCPT TO:<$to>", 250);
        smtp_cmd($fp, 'DATA', 354);
        $data = preg_replace('/^\./m', '..', $data); // dot-stuffing
        smtp_cmd($fp, $data . "\r\n.", 250);
        smtp_cmd($fp, 'QUIT', 221);
        fclose($fp);
        return true;
    } catch (Throwable $e) {
        error_log('[mail] ' . $e->getMessage());
        return false;
    }
}

function mime_header(string $s): string
{
    return preg_match('/[^\x20-\x7E]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : $s;
}

function smtp_cmd($fp, string $cmd, int $expect): string
{
    fwrite($fp, $cmd . "\r\n");
    return smtp_expect($fp, $expect);
}

function smtp_expect($fp, int $code): string
{
    $resp = '';
    while (($line = fgets($fp, 515)) !== false) {
        $resp .= $line;
        if (isset($line[3]) && $line[3] === ' ') break;
    }
    if ((int)substr($resp, 0, 3) !== $code) throw new RuntimeException("SMTP expected $code, got: " . trim($resp));
    return $resp;
}

function email_wrap(string $title, string $html): string
{
    $site = e(cfg('site_name'));
    $u = e(url('/'));
    return '<!doctype html><html><body style="margin:0;background:#f4f6f8;font-family:Arial,Helvetica,sans-serif;color:#1f2a37">'
        . '<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:24px">'
        . '<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#fff;border-radius:10px;overflow:hidden">'
        . '<tr><td style="background:#0f4c5c;color:#fff;padding:18px 24px;font-size:20px;font-weight:bold">' . $site . '</td></tr>'
        . '<tr><td style="padding:24px;font-size:15px;line-height:1.6">' . $html . '</td></tr>'
        . '<tr><td style="padding:16px 24px;background:#f9fafb;color:#6b7280;font-size:12px">West Carrollton, Ohio apartment directory &middot; <a href="' . $u . '" style="color:#0f4c5c">' . $u . '</a></td></tr>'
        . '</table></td></tr></table></body></html>';
}

function email_button(string $href, string $label): string
{
    return '<p style="margin:24px 0"><a href="' . e($href) . '" style="background:#e36414;color:#fff;padding:12px 22px;border-radius:6px;text-decoration:none;font-weight:bold;display:inline-block">' . e($label) . '</a></p>'
        . '<p style="font-size:12px;color:#6b7280">Or paste this link into your browser:<br>' . e($href) . '</p>';
}

function notify_admin(string $subject, string $html, ?string $replyTo = null): void
{
    send_mail((string)cfg('admin_email'), '[WCA] ' . $subject, $html, $replyTo);
}
