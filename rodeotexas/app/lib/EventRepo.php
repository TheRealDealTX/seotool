<?php
declare(strict_types=1);

namespace RT;

/**
 * Read-side queries for the public site (search, filters, calendar, map).
 * Every value from the request is bound as a parameter.
 */
final class EventRepo
{
    public const PER_PAGE = 20;

    private const SELECT = "SELECT e.*, v.name AS venue_name, v.address AS venue_address, v.city, v.county, v.state, v.postal_code,
            v.lat, v.lng, v.location_precision, v.parking_info AS venue_parking, v.accessibility_info AS venue_accessibility,
            r.slug AS region_slug, r.name AS region_name, a.slug AS assoc_slug, a.abbr AS assoc_abbr, a.name AS assoc_name,
            t.slug AS type_slug, t.name AS type_name, o.name AS org_name, o.website AS org_website, o.email AS org_email, o.phone AS org_phone,
            (SELECT MIN(p.starts_at) FROM performances p WHERE p.event_id = e.id) AS first_perf,
            (SELECT COUNT(*) FROM performances p WHERE p.event_id = e.id) AS perf_count
        FROM events e
        LEFT JOIN venues v ON v.id = e.venue_id
        LEFT JOIN regions r ON r.id = v.region_id
        LEFT JOIN associations a ON a.id = e.association_id
        LEFT JOIN event_types t ON t.id = e.event_type_id
        LEFT JOIN organizers o ON o.id = e.organizer_id";

    /** Normalize raw request input into a filter array. */
    public static function filtersFrom(array $in): array
    {
        $f = [
            'q' => clean_str($in['q'] ?? null, 100),
            'from' => valid_date($in['from'] ?? null),
            'to' => valid_date($in['to'] ?? null),
            'region' => self::slugParam($in['region'] ?? null),
            'association' => self::slugParam($in['association'] ?? null),
            'type' => self::slugParam($in['type'] ?? null),
            'level' => in_array($in['level'] ?? null, levels(), true) ? $in['level'] : null,
            'when' => in_array($in['when'] ?? null, ['weekend', 'month'], true) ? $in['when'] : null,
            'page' => max(1, min(500, (int) ($in['page'] ?? 1))),
            'view' => in_array($in['view'] ?? null, ['list', 'calendar', 'map'], true) ? $in['view'] : 'list',
            'month' => (isset($in['month']) && preg_match('/^\d{4}-\d{2}$/', (string) $in['month'])) ? $in['month'] : null,
        ];
        if ($f['when'] === 'weekend') {
            [$f['from'], $f['to']] = Dates::weekend();
        } elseif ($f['when'] === 'month') {
            [$f['from'], $f['to']] = Dates::thisMonth();
        }
        if ($f['from'] && $f['to'] && $f['to'] < $f['from']) {
            [$f['from'], $f['to']] = [$f['to'], $f['from']];
        }
        return $f;
    }

    private static function slugParam($v): ?string
    {
        $v = is_string($v) ? strtolower(trim($v)) : '';
        return preg_match('/^[a-z0-9-]{1,60}$/', $v) ? $v : null;
    }

    /** @return array{0:string,1:array,2:?string} [where-sql, params, zip-note] */
    private static function where(array $f, bool $past = false): array
    {
        $w = ["e.publish_state = 'published'"];
        $p = [];
        $today = Dates::today();
        if ($past) {
            $w[] = 'e.end_date < :today';
            $p['today'] = $today;
        } elseif (!$f['from'] && !$f['to']) {
            $w[] = 'e.end_date >= :today';
            $p['today'] = $today;
        }
        if ($f['from']) {
            $w[] = 'e.end_date >= :from';
            $p['from'] = $f['from'];
        }
        if ($f['to']) {
            $w[] = 'e.start_date <= :to';
            $p['to'] = $f['to'];
        }
        foreach (['region' => 'r.slug', 'association' => 'a.slug', 'type' => 't.slug', 'level' => 'e.level'] as $k => $col) {
            if ($f[$k]) {
                $w[] = "{$col} = :{$k}";
                $p[$k] = $f[$k];
            }
        }
        $note = null;
        if ($f['q']) {
            if (preg_match('/^\d{5}$/', $f['q'])) {
                $exact = (int) Db::val('SELECT COUNT(*) FROM venues WHERE postal_code = ?', [$f['q']]);
                if ($exact > 0) {
                    $w[] = 'v.postal_code = :zip';
                    $p['zip'] = $f['q'];
                } else {
                    $w[] = 'v.postal_code LIKE :zip';
                    $p['zip'] = substr($f['q'], 0, 3) . '%';
                    $note = 'No events list ZIP ' . $f['q'] . ' exactly, so we are showing the surrounding ' . substr($f['q'], 0, 3) . 'xx ZIP area.';
                }
            } else {
                $i = 0;
                $words = array_values(array_filter(array_map(static fn($w) => trim($w, " ,.;:'\""), preg_split('/\s+/', $f['q']) ?: []),
                    static fn($w) => mb_strlen($w) >= 2));
                if (!$words) {
                    $words = [$f['q']];   // very short query: match it literally rather than returning everything
                }
                foreach (array_slice($words, 0, 6) as $word) {
                    $like = '%' . addcslashes($word, '%_\\') . '%';
                    $cols = ['e.title', 'v.name', 'v.city', 'v.county', 'o.name', 'a.abbr', 'v.postal_code'];
                    $ors = [];
                    foreach ($cols as $j => $c) {
                        $ors[] = "{$c} LIKE :q{$i}_{$j}";
                        $p["q{$i}_{$j}"] = $like;
                    }
                    $w[] = '(' . implode(' OR ', $ors) . ')';
                    $i++;
                }
            }
        }
        return [implode(' AND ', $w), $p, $note];
    }

    /** @return array{rows:array,total:int,pages:int,note:?string} */
    public static function search(array $f, bool $past = false): array
    {
        [$where, $p, $note] = self::where($f, $past);
        $total = (int) Db::val('SELECT COUNT(*) FROM events e
            LEFT JOIN venues v ON v.id = e.venue_id LEFT JOIN regions r ON r.id = v.region_id
            LEFT JOIN associations a ON a.id = e.association_id LEFT JOIN event_types t ON t.id = e.event_type_id
            LEFT JOIN organizers o ON o.id = e.organizer_id WHERE ' . $where, $p);
        $pages = max(1, (int) ceil($total / self::PER_PAGE));
        $page = min($f['page'], $pages);
        $order = $past ? 'e.start_date DESC, e.title' : 'e.start_date ASC, e.featured DESC, e.title';
        $rows = Db::all(self::SELECT . ' WHERE ' . $where . ' ORDER BY ' . $order . ' LIMIT ' . self::PER_PAGE . ' OFFSET ' . (($page - 1) * self::PER_PAGE), $p);
        return ['rows' => $rows, 'total' => $total, 'pages' => $pages, 'page' => $page, 'note' => $note];
    }

    /** Events overlapping a calendar month (Y-m). */
    public static function month(array $f, string $ym): array
    {
        $first = $ym . '-01';
        $last = date('Y-m-t', strtotime($first));
        $f2 = array_merge($f, ['from' => $first, 'to' => $last, 'when' => null]);
        [$where, $p] = self::where($f2);
        return Db::all(self::SELECT . ' WHERE ' . $where . ' ORDER BY e.start_date, e.title LIMIT 600', $p);
    }

    /** Points for the map view (only venues with coordinates). */
    public static function mapPoints(array $f): array
    {
        [$where, $p] = self::where($f);
        return Db::all(self::SELECT . ' WHERE ' . $where . ' AND v.lat IS NOT NULL ORDER BY e.start_date LIMIT 500', $p);
    }

    public static function bySlug(string $slug, bool $includeUnpublished = false): ?array
    {
        $sql = self::SELECT . ' WHERE e.slug = ?' . ($includeUnpublished ? '' : " AND e.publish_state IN ('published','archived')");
        return Db::one($sql, [$slug]);
    }

    public static function bySlugs(array $slugs): array
    {
        $slugs = array_slice(array_values(array_filter($slugs, static fn($s) => is_string($s) && preg_match('/^[a-z0-9-]{1,190}$/', $s))), 0, 100);
        if (!$slugs) {
            return [];
        }
        $p = [];
        $in = Db::in('s', $slugs, $p);
        return Db::all(self::SELECT . " WHERE e.slug IN {$in} AND e.publish_state IN ('published','archived') ORDER BY e.start_date", $p);
    }

    public static function performances(int $eventId): array
    {
        return Db::all('SELECT * FROM performances WHERE event_id = ? ORDER BY starts_at', [$eventId]);
    }

    public static function related(array $e): array
    {
        if (!$e['group_id']) {
            return [];
        }
        return Db::all(self::SELECT . " WHERE e.group_id = ? AND e.id <> ? AND e.publish_state = 'published' ORDER BY e.start_date LIMIT 12", [$e['group_id'], $e['id']]);
    }

    /** Upcoming events at the same venue or city (for "More nearby"). */
    public static function nearby(array $e, int $limit = 4): array
    {
        if (!$e['city']) {
            return [];
        }
        return Db::all(self::SELECT . " WHERE e.publish_state = 'published' AND e.id <> ? AND e.end_date >= ? AND (v.city = ? OR r.slug = ?)
            ORDER BY (v.city = ?) DESC, e.start_date LIMIT " . (int) $limit,
            [$e['id'], Dates::today(), $e['city'], (string) $e['region_slug'], $e['city']]);
    }

    public static function upcoming(int $limit = 6): array
    {
        return Db::all(self::SELECT . " WHERE e.publish_state = 'published' AND e.end_date >= ? ORDER BY e.featured DESC, e.start_date LIMIT " . (int) $limit, [Dates::today()]);
    }

    public static function counts(): array
    {
        $today = Dates::today();
        return [
            'upcoming' => (int) Db::val("SELECT COUNT(*) FROM events WHERE publish_state = 'published' AND end_date >= ?", [$today]),
            'weekend' => (function () {
                [$a, $b] = Dates::weekend();
                return (int) Db::val("SELECT COUNT(*) FROM events WHERE publish_state = 'published' AND end_date >= ? AND start_date <= ?", [$a, $b]);
            })(),
            'month' => (function () {
                [$a, $b] = Dates::thisMonth();
                return (int) Db::val("SELECT COUNT(*) FROM events WHERE publish_state = 'published' AND end_date >= ? AND start_date <= ?", [$a, $b]);
            })(),
        ];
    }

    public static function regions(): array
    {
        return Db::all('SELECT slug, name FROM regions ORDER BY sort');
    }

    public static function associations(): array
    {
        return Db::all('SELECT slug, abbr, name, level FROM associations ORDER BY sort, abbr');
    }

    public static function types(): array
    {
        return Db::all('SELECT slug, name FROM event_types ORDER BY sort');
    }
}
