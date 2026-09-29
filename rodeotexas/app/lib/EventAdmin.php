<?php
declare(strict_types=1);

namespace RT;

/**
 * Create/update events from the admin form.
 *
 * Every field an administrator changes is added to events.locked_fields, so
 * later imports cannot silently overwrite the manual correction (they raise an
 * import_conflict review item instead). Locks can be released in the editor.
 */
final class EventAdmin
{
    /** Fields the importer manages and that can therefore be locked. */
    public const LOCKABLE = ['title', 'start_date', 'end_date', 'official_url', 'ticket_url', 'price_text', 'description',
        'image_url', 'status', 'venue_id', 'organizer_id', 'performances', 'publish_state'];

    /**
     * @return array{0:?int,1:array<string,string>} [event id, errors]
     */
    public static function save(?int $id, array $in, int $adminId): array
    {
        $cur = $id ? Db::one('SELECT * FROM events WHERE id = ?', [$id]) : null;
        if ($id && !$cur) {
            return [null, ['form' => 'Event not found']];
        }
        $err = [];
        $d = [
            'title' => clean_str($in['title'] ?? null, 255),
            'description' => clean_text($in['description'] ?? null, 8000),
            'event_type_id' => self::intOrNull($in['event_type_id'] ?? null),
            'association_id' => self::intOrNull($in['association_id'] ?? null),
            'level' => in_array($in['level'] ?? null, levels(), true) ? $in['level'] : null,
            'start_date' => valid_date($in['start_date'] ?? null),
            'end_date' => valid_date($in['end_date'] ?? null),
            'status' => in_array($in['status'] ?? null, ['scheduled', 'postponed', 'canceled'], true) ? $in['status'] : 'scheduled',
            'status_note' => clean_str($in['status_note'] ?? null, 255),
            'official_url' => valid_url($in['official_url'] ?? null),
            'ticket_url' => valid_url($in['ticket_url'] ?? null),
            'ticket_url_verified' => !empty($in['ticket_url_verified']) ? 1 : 0,
            'price_text' => clean_str($in['price_text'] ?? null, 255),
            'parking_info' => clean_text($in['parking_info'] ?? null, 2000),
            'accessibility_info' => clean_text($in['accessibility_info'] ?? null, 2000),
            'image_url' => valid_url($in['image_url'] ?? null),
            'publish_state' => in_array($in['publish_state'] ?? null, ['draft', 'published', 'archived'], true) ? $in['publish_state'] : 'draft',
            'featured' => !empty($in['featured']) ? 1 : 0,
            'source_label' => clean_str($in['source_label'] ?? null, 255),
            'source_url' => valid_url($in['source_url'] ?? null),
            'group_id' => null,
        ];
        foreach (['official_url', 'ticket_url', 'image_url', 'source_url'] as $u) {
            if (trim((string) ($in[$u] ?? '')) !== '' && $d[$u] === null) {
                $err[$u] = 'Enter a full URL starting with https://';
            }
        }
        if (!$d['title']) { $err['title'] = 'Title is required.'; }
        if (!$d['start_date']) { $err['start_date'] = 'Start date is required (YYYY-MM-DD).'; }
        $d['end_date'] = $d['end_date'] ?? $d['start_date'];
        if ($d['start_date'] && $d['end_date'] < $d['start_date']) { $err['end_date'] = 'End date is before the start date.'; }
        if ($d['ticket_url'] === null) { $d['ticket_url_verified'] = 0; }

        // Venue: existing id, or a new one from the fields.
        $venueId = self::intOrNull($in['venue_id'] ?? null);
        $newVenue = ['name' => clean_str($in['venue_name'] ?? null, 255), 'address' => clean_str($in['venue_address'] ?? null, 255),
            'city' => clean_str($in['venue_city'] ?? null, 120), 'postal_code' => clean_str($in['venue_zip'] ?? null, 10), 'state' => 'TX'];
        if (!$venueId && ($newVenue['city'] || $newVenue['name'])) {
            if (!$newVenue['city']) {
                $err['venue_city'] = 'A new venue needs a Texas city.';
            } elseif ($newVenue['postal_code'] && !Geo::isTexasZip($newVenue['postal_code'])) {
                $err['venue_zip'] = 'Not a Texas ZIP code — only Texas venues can be listed.';
            }
        }
        // Organizer
        $org = ['name' => clean_str($in['org_name'] ?? null, 255), 'website' => valid_url($in['org_website'] ?? null),
            'email' => valid_email($in['org_email'] ?? null), 'phone' => clean_str($in['org_phone'] ?? null, 40)];
        // Performances: one per line "YYYY-MM-DD HH:MM[-HH:MM] [| label]"
        [$perfs, $perfErr] = self::parsePerformances((string) ($in['performances'] ?? ''));
        if ($perfErr) { $err['performances'] = $perfErr; }
        // Related group: link to another event id
        $groupWith = self::intOrNull($in['group_with'] ?? null);
        $slugIn = clean_str($in['slug'] ?? null, 190);
        if ($slugIn !== null && !preg_match('/^[a-z0-9-]{3,190}$/', $slugIn)) {
            $err['slug'] = 'Use lowercase letters, numbers and hyphens.';
        }
        if ($err) {
            return [$id, $err];
        }

        return Db::tx(function () use ($id, $cur, $d, $venueId, $newVenue, $org, $perfs, $groupWith, $slugIn, $in, $adminId) {
            $now = now_utc();
            $actor = 'admin:' . $adminId;
            if (!$venueId && ($newVenue['city'] || $newVenue['name'])) {
                $venueId = Importer::upsertVenue($newVenue);
            }
            $d['venue_id'] = $venueId;
            $d['timezone'] = $venueId ? (string) Db::val('SELECT timezone FROM venues WHERE id = ?', [$venueId]) : 'America/Chicago';
            $existingOrgId = $cur['organizer_id'] ?? null;
            if ($org['name']) {
                $orgId = Importer::upsertOrganizer($org);
                // Admin edits overwrite organizer contact details.
                Db::update('organizers', array_filter(['website' => $org['website'], 'email' => $org['email'], 'phone' => $org['phone']]) + ['updated_at' => $now], 'id = :id', ['id' => $orgId]);
                $d['organizer_id'] = $orgId;
            } else {
                $d['organizer_id'] = null;
            }
            if ($groupWith) {
                $other = Db::one('SELECT id, title, group_id FROM events WHERE id = ?', [$groupWith]);
                if ($other && (!$cur || (int) $other['id'] !== (int) $cur['id'])) {
                    $gid = $other['group_id'] ?: Db::insert('event_groups', ['name' => $other['title'], 'created_at' => $now]);
                    Db::update('events', ['group_id' => $gid], 'id = :id', ['id' => $other['id']]);
                    $d['group_id'] = (int) $gid;
                }
            } elseif ($cur && empty($in['ungroup'])) {
                $d['group_id'] = $cur['group_id'];
            }
            if (!empty($in['mark_verified'])) {
                $d['last_verified_at'] = $now;
            }
            if (!$cur) {
                $d['slug'] = $slugIn && !Db::val('SELECT 1 FROM events WHERE slug = ?', [$slugIn]) ? $slugIn : Importer::uniqueSlug((string) $d['title'], (string) $d['start_date']);
                $d['source_label'] = $d['source_label'] ?? 'Rodeo Texas editors';
                $d['last_verified_at'] = $d['last_verified_at'] ?? $now;
                $d['locked_fields'] = json_encode(self::LOCKABLE);   // hand-made events are fully owned by admins
                $d['created_at'] = $now;
                $d['updated_at'] = $now;
                $newId = Db::insert('events', $d);
                Importer::replacePerformances($newId, $perfs);
                Importer::history($newId, $actor, 'created', null, $d['publish_state']);
                return [$newId, []];
            }
            // Update: record changes, lock changed import-managed fields.
            $locked = json_decode((string) $cur['locked_fields'], true) ?: [];
            $changes = [];
            foreach ($d as $k => $v) {
                if ((string) ($cur[$k] ?? '') !== (string) ($v ?? '')) {
                    $changes[$k] = $v;
                    if (in_array($k, self::LOCKABLE, true) && !in_array($k, $locked, true)) {
                        $locked[] = $k;
                    }
                    if (!in_array($k, ['last_verified_at', 'timezone'], true)) {
                        Importer::history((int) $cur['id'], $actor, $k, $cur[$k] ?? null, $v);
                    }
                }
            }
            $curPerfs = Db::all('SELECT starts_at AS start, ends_at AS end, label FROM performances WHERE event_id = ? ORDER BY starts_at', [$cur['id']]);
            if (json_encode($curPerfs) !== json_encode($perfs)) {
                Importer::replacePerformances((int) $cur['id'], $perfs);
                Importer::history((int) $cur['id'], $actor, 'performances', json_encode($curPerfs), json_encode($perfs));
                if (!in_array('performances', $locked, true)) {
                    $locked[] = 'performances';
                }
                $changes['updated_at'] = $now;
            }
            // Explicit unlocks from the editor.
            foreach ((array) ($in['unlock'] ?? []) as $u) {
                $locked = array_values(array_diff($locked, [$u]));
            }
            if ($slugIn && $slugIn !== $cur['slug'] && !Db::val('SELECT 1 FROM events WHERE slug = ?', [$slugIn])) {
                Db::q('INSERT INTO redirects (from_path, to_path, code, created_at) VALUES (?, ?, 301, ?) ON DUPLICATE KEY UPDATE to_path = VALUES(to_path)',
                    ['/rodeos/' . $cur['slug'] . '/', '/rodeos/' . $slugIn . '/', $now]);
                Db::q('DELETE FROM redirects WHERE from_path = ?', ['/rodeos/' . $slugIn . '/']);
                $changes['slug'] = $slugIn;
                Importer::history((int) $cur['id'], $actor, 'slug', $cur['slug'], $slugIn);
            }
            $changes['locked_fields'] = json_encode(array_values(array_unique($locked)));
            $changes['updated_at'] = $now;
            Db::update('events', $changes, 'id = :id', ['id' => $cur['id']]);
            if ($existingOrgId && $existingOrgId !== ($d['organizer_id'] ?? null)) {
                // leave the old organizer row; it may be used elsewhere
            }
            return [(int) $cur['id'], []];
        });
    }

    /** @return array{0:array,1:?string} */
    public static function parsePerformances(string $text): array
    {
        $out = [];
        foreach (preg_split('/\r?\n/', trim($text)) ?: [] as $n => $line) {
            $line = trim($line);
            if ($line === '') {
                continue;
            }
            if (!preg_match('/^(\d{4}-\d{2}-\d{2})\s+(\d{1,2}):(\d{2})\s*(am|pm)?(?:\s*-\s*(\d{1,2}):(\d{2})\s*(am|pm)?)?\s*(?:\|\s*(.+))?$/i', $line, $m)) {
                return [[], 'Line ' . ($n + 1) . ' is not in the format "2026-10-03 19:30" (optionally "-21:30 | label").'];
            }
            $h = static function (string $hh, ?string $ap): int {
                $x = (int) $hh;
                if ($ap) {
                    $x = $x % 12 + (strtolower($ap) === 'pm' ? 12 : 0);
                }
                return $x;
            };
            if (!valid_date($m[1])) {
                return [[], 'Line ' . ($n + 1) . ' has an invalid date.'];
            }
            $sh = $h($m[2], $m[4] ?? null);
            $start = sprintf('%s %02d:%02d:00', $m[1], $sh, (int) $m[3]);
            $end = !empty($m[5]) ? sprintf('%s %02d:%02d:00', $m[1], $h($m[5], ($m[7] ?? '') ?: ($m[4] ?? null)), (int) $m[6]) : null;
            if ($sh > 23 || (int) $m[3] > 59) {
                return [[], 'Line ' . ($n + 1) . ' has an invalid time.'];
            }
            $out[] = ['start' => $start, 'end' => $end, 'label' => isset($m[8]) ? clean_str($m[8], 160) : null];
        }
        usort($out, static fn($a, $b) => strcmp($a['start'], $b['start']));
        return [$out, null];
    }

    public static function perfsToText(int $eventId): string
    {
        $lines = [];
        foreach (Db::all('SELECT * FROM performances WHERE event_id = ? ORDER BY starts_at', [$eventId]) as $p) {
            $lines[] = substr($p['starts_at'], 0, 16) . ($p['ends_at'] ? '-' . substr($p['ends_at'], 11, 5) : '') . ($p['label'] ? ' | ' . $p['label'] : '');
        }
        return implode("\n", $lines);
    }

    private static function intOrNull($v): ?int
    {
        return (is_string($v) || is_int($v)) && ctype_digit((string) $v) && (int) $v > 0 ? (int) $v : null;
    }
}
