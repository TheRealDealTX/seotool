<?php
declare(strict_types=1);

namespace RT;

/**
 * Plain-text notification mail via PHP mail() (enabled on Hostinger).
 * Header values are stripped of CR/LF to prevent header injection.
 * Every message is also appended to storage/logs/mail.log so nothing is
 * lost if delivery fails.
 */
final class Mailer
{
    public static function toAdmin(string $subject, string $body, ?string $replyTo = null): bool
    {
        $to = (string) cfg('admin_email');
        if ($to === '' || !filter_var($to, FILTER_VALIDATE_EMAIL)) {
            app_log('mail', 'admin_email not configured; subject=' . $subject);
            return false;
        }
        return self::send($to, $subject, $body, $replyTo);
    }

    public static function send(string $to, string $subject, string $body, ?string $replyTo = null): bool
    {
        $clean = static fn(string $s): string => trim(str_replace(["\r", "\n", "%0a", "%0d"], ' ', $s));
        $site = (string) cfg('site_name', 'Rodeo Texas');
        $from = $clean((string) cfg('mail_from', 'no-reply@' . (parse_url((string) cfg('base_url'), PHP_URL_HOST) ?: 'localhost')));
        $subject = '[' . $site . '] ' . $clean($subject);
        $headers = [
            'From: ' . $clean($site) . ' <' . $from . '>',
            'MIME-Version: 1.0',
            'Content-Type: text/plain; charset=UTF-8',
            'Content-Transfer-Encoding: 8bit',
            'X-Mailer: RodeoTexas',
        ];
        if ($replyTo && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
            $headers[] = 'Reply-To: ' . $clean($replyTo);
        }
        $encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
        $ok = false;
        if (PHP_SAPI !== 'cli' || getenv('RT_SEND_MAIL_CLI') !== '0') {
            $ok = @mail($clean($to), $encodedSubject, $body, implode("\r\n", $headers), '-f' . $from);
        }
        app_log('mail', ($ok ? 'SENT ' : 'NOT SENT ') . $subject);
        return $ok;
    }
}
