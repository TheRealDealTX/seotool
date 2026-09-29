<?php
declare(strict_types=1);

namespace RT;

/**
 * Assigns event type, association and level from explicit wording in the
 * title/categories. When nothing explicit is present the value stays null
 * ("not listed") or falls back to the source's configured default — we never
 * guess an association from the venue or circuit.
 */
final class Classifier
{
    /** [regex, event_type slug] in priority order */
    private const TYPE_RULES = [
        ['/\branch rodeo\b/i', 'ranch-rodeo'],
        ['/\b(finals?|championship finals)\b/i', 'finals'],
        ['/\bbreakaway\b/i', 'breakaway-roping'],
        ['/\b(steer roping|legacy sr|\bSR\b)\b/', 'steer-roping'],
        ['/\b(x-?treme bulls|xbulls|bull ?riding|bull madness|bulls night|bullriding|pbr)\b/i', 'bull-riding'],
        ['/\b(broncs?|bares|bareback|roughstock|rough stock)\b/i', 'roughstock'],
        ['/\bbarrels?\b/i', 'barrel-racing'],
        ['/\b(team roping|tie-?down|roping)\b/i', 'roping'],
        ['/\bbulldogging|steer wrestling\b/i', 'roping'],
        ['/\b(rodeo|round-?up|stampede|frontier days|pro rodeo|prorodeo)\b/i', 'rodeo'],
        ['/\b(stock show|livestock show|horse show|cutting|reining|ranch sorting|team penning|mutton bustin)\b/i', 'related'],
    ];

    /** [regex, association slug] */
    private const ASSOC_RULES = [
        ['/\bPRCA\b|\bprorodeo\b|\bpro rodeo\b/i', null],   // "pro rodeo" alone is not proof of PRCA
        ['/\bPRCA\b/', 'prca'],
        ['/\bWPRA\b/', 'wpra'],
        ['/\bPBR\b/', 'pbr'],
        ['/\bIPRA\b/', 'ipra'],
        ['/\bUPRA\b/', 'upra'],
        ['/\bCPRA\b/', 'cpra'],
        ['/\bACRA\b/', 'acra'],
        ['/\bTHSRA\b/', 'thsra'],
        ['/\bTYRA\b/', 'tyra'],
        ['/\bAJRA\b/', 'ajra'],
        ['/\bNLBRA\b/', 'nlbra'],
        ['/\bNIRA\b/', 'nira'],
        ['/\bIGRA\b|\bgay rodeo\b/i', 'igra'],
        ['/\bWRCA\b/', 'wrca'],
    ];

    public static function eventTypeSlug(string $title, array $categories = []): ?string
    {
        $hay = $title . ' ' . implode(' ', $categories);
        foreach (self::TYPE_RULES as [$re, $slug]) {
            if (preg_match($re, $hay)) {
                return $slug;
            }
        }
        return null;
    }

    public static function associationSlug(string $title, array $categories = []): ?string
    {
        $hay = $title . ' ' . implode(' ', $categories);
        foreach (self::ASSOC_RULES as [$re, $slug]) {
            if ($slug !== null && preg_match($re, $hay)) {
                return $slug;
            }
        }
        return null;
    }

    public static function levelFromText(string $title, array $categories = []): ?string
    {
        $hay = $title . ' ' . implode(' ', $categories);
        if (preg_match('/\bhigh school\b|\bTHSRA\b|\bNHSRA\b/i', $hay)) return 'high_school';
        if (preg_match('/\b(college|NIRA|collegiate)\b/i', $hay)) return 'college';
        if (preg_match('/\b(youth|junior|jr\.?|kids|little britches|AJRA|TYRA|NLBRA)\b/i', $hay)) return 'youth';
        return null;
    }

    public static function idFor(string $table, ?string $slug): ?int
    {
        if ($slug === null) {
            return null;
        }
        static $cache = [];
        $k = $table . ':' . $slug;
        if (!array_key_exists($k, $cache)) {
            $allowed = ['event_types', 'associations', 'regions'];
            if (!in_array($table, $allowed, true)) {
                throw new \InvalidArgumentException('bad table');
            }
            $id = Db::val("SELECT id FROM `$table` WHERE slug = ?", [$slug]);
            $cache[$k] = $id === null ? null : (int) $id;
        }
        return $cache[$k];
    }
}
