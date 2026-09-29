<?php
declare(strict_types=1);

namespace RT;

/**
 * Checks official/ticket links of upcoming events and stores the result in
 * link_checks. Used by Admin → Links & missing info and bin/check-links.php.
 */
final class LinkChecker
{
    /** @return array{checked:int, broken:int} */
    public static function run(int $limit = 40, int $maxAgeHours = 72): array
    {
        $rows = Db::all("SELECT id, official_url, ticket_url FROM events
            WHERE publish_state = 'published' AND end_date >= ? AND (official_url IS NOT NULL OR ticket_url IS NOT NULL)
            ORDER BY start_date", [gmdate('Y-m-d')]);
        $urls = [];
        foreach ($rows as $r) {
            foreach (['official_url', 'ticket_url'] as $f) {
                if ($r[$f]) {
                    $urls[$r[$f]] = true;
                }
            }
        }
        $checked = 0; $broken = 0;
        $cut = gmdate('Y-m-d H:i:s', time() - $maxAgeHours * 3600);
        foreach (array_keys($urls) as $u) {
            if ($checked >= $limit) {
                break;
            }
            $h = hash('sha256', $u);
            $last = Db::val('SELECT last_checked_at FROM link_checks WHERE url_hash = ?', [$h]);
            if ($last && $last > $cut) {
                continue;
            }
            $r = Http::once($u, ['head' => true, 'timeout' => 12]);
            if ($r['error'] !== '' || $r['status'] >= 400 || $r['status'] === 0) {
                $r = Http::once($u, ['timeout' => 15, 'max_bytes' => 200000]);   // some servers reject HEAD
            }
            $ok = $r['error'] === '' && $r['status'] >= 200 && $r['status'] < 400;
            Db::q('INSERT INTO link_checks (url_hash, url, http_status, ok, error, last_checked_at) VALUES (?,?,?,?,?,?)
                   ON DUPLICATE KEY UPDATE http_status = VALUES(http_status), ok = VALUES(ok), error = VALUES(error), last_checked_at = VALUES(last_checked_at)',
                [$h, mb_substr($u, 0, 500), $r['status'] ?: null, $ok ? 1 : 0, $r['error'] !== '' ? mb_substr($r['error'], 0, 255) : null, now_utc()]);
            $checked++;
            if (!$ok) {
                $broken++;
            }
        }
        return ['checked' => $checked, 'broken' => $broken];
    }
}
