<?php
declare(strict_types=1);

namespace RT;

/**
 * Spam and forgery protection for anonymous public forms (no session needed,
 * so public pages stay cacheable):
 *  - signed token (HMAC) binding form name + issue time → CSRF-style protection and time trap
 *  - minimum fill time (4 s) and maximum age (24 h)
 *  - honeypot field that humans never see
 *  - per-IP rate limit (hashed IP, sliding window)
 *  - link-count heuristic on free text
 */
final class PublicForm
{
    public const HONEYPOT = 'company_website';
    public const MIN_SECONDS = 4;
    public const MAX_AGE = 86400;

    public static function token(string $form): string
    {
        $t = (string) time();
        return $t . '.' . hash_hmac('sha256', $form . '|' . $t, (string) cfg('app_secret'));
    }

    public static function fields(string $form): string
    {
        return '<input type="hidden" name="_ft" value="' . e(self::token($form)) . '">'
            . '<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="' . self::HONEYPOT . '" tabindex="-1" autocomplete="off"></label></div>';
    }

    /**
     * @return string|null error for the visitor, or null when the submission may proceed
     */
    public static function check(string $form, array $post, int $maxPerHour = 5): ?string
    {
        if (trim((string) ($post[self::HONEYPOT] ?? '')) !== '') {
            return 'spam';   // silently discarded by caller
        }
        $tok = (string) ($post['_ft'] ?? '');
        if (!preg_match('/^(\d+)\.([a-f0-9]{64})$/', $tok, $m)
            || !hash_equals(hash_hmac('sha256', $form . '|' . $m[1], (string) cfg('app_secret')), $m[2])) {
            return 'This form has expired. Please reload the page and try again.';
        }
        $age = time() - (int) $m[1];
        if ($age < self::MIN_SECONDS) {
            return 'spam';
        }
        if ($age > self::MAX_AGE) {
            return 'This form has expired. Please reload the page and try again.';
        }
        if (!self::rateLimit($form, $maxPerHour)) {
            return 'You have sent several messages in a short time. Please try again in an hour.';
        }
        $text = implode(' ', array_map(static fn($v) => is_string($v) ? $v : '', $post));
        if (preg_match_all('~https?://~i', $text) > 6 || preg_match('/\[url=|<a\s+href/i', $text)) {
            return 'spam';
        }
        return null;
    }

    public static function rateLimit(string $bucket, int $max, int $windowSec = 3600): bool
    {
        $ip = ip_hash();
        $row = Db::one('SELECT hits, window_start FROM rate_limits WHERE bucket = ? AND ip_hash = ?', [$bucket, $ip]);
        $now = time();
        if (!$row || strtotime($row['window_start'] . ' UTC') < $now - $windowSec) {
            Db::q('REPLACE INTO rate_limits (bucket, ip_hash, hits, window_start) VALUES (?, ?, 1, ?)', [$bucket, $ip, now_utc()]);
            return true;
        }
        if ((int) $row['hits'] >= $max) {
            return false;
        }
        Db::q('UPDATE rate_limits SET hits = hits + 1 WHERE bucket = ? AND ip_hash = ?', [$bucket, $ip]);
        return true;
    }
}
