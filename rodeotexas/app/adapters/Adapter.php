<?php
declare(strict_types=1);

namespace RT\Adapters;

/**
 * Base class for event-source adapters.
 *
 * An adapter only FETCHES and NORMALIZES. It never writes to the database;
 * the Importer decides what to publish, update, review or skip.
 *
 * fetch() returns a list of normalized records:
 * [
 *   'uid'          => string   stable identifier within the source (required)
 *   'title'        => string
 *   'description'  => ?string  plain text
 *   'start_date'   => 'Y-m-d'  local date at the venue
 *   'end_date'     => 'Y-m-d'
 *   'timezone'     => ?string  IANA zone the source reported, if any
 *   'performances' => [ ['start' => 'Y-m-d H:i:s' (local), 'end' => ?string, 'label' => ?string], … ]
 *   'venue'        => ['name','address','city','state','postal_code','country','lat','lng'] (nullable values)
 *   'organizer'    => ['name','website','email','phone'] | null
 *   'official_url' => ?string, 'ticket_url' => ?string, 'price_text' => ?string,
 *   'image_url'    => ?string, 'source_url' => ?string,
 *   'status'       => null | 'scheduled' | 'canceled' | 'postponed'   (ONLY when the source says so explicitly)
 *   'categories'   => string[]
 *   'association'  => ?string  association slug if the source states it
 *   'level'        => ?string
 * ]
 *
 * Common config keys (JSON in sources.config):
 *   require_keywords  string[]  keep only records whose title/categories contain one of these
 *   exclude_keywords  string[]  drop records whose title contains one of these
 *   title_strip_regex string    regex removed from titles (e.g. leading date codes)
 *   title_replace     object    exact title → display title (expand abbreviations the source uses)
 *   exclude_acts      bool      drop "Performer at the XYZ Rodeo" listings (concerts at a rodeo)
 *   default_venue     object    venue used when the feed omits it (the organizer's own arena)
 *   min_delay         float     seconds between requests (robots Crawl-delay is honoured anyway)
 */
abstract class Adapter
{
    protected array $config;
    protected array $source;
    /** @var callable(string,string):void */
    protected $log;

    public function __construct(array $source, ?callable $log = null)
    {
        $this->source = $source;
        $this->config = json_decode((string) ($source['config'] ?? '{}'), true) ?: [];
        $this->log = $log ?? static function (string $level, string $msg): void {};
    }

    /** @return array<int,array> normalized records */
    abstract public function fetch(): array;

    /** Human description for the admin sources screen. */
    abstract public static function describe(): string;

    protected function log(string $level, string $msg): void
    {
        ($this->log)($level, $msg);
    }

    /** Apply keyword filters. Returns a reason string when the record should be skipped. */
    public function filterReason(array $rec): ?string
    {
        $hay = strtolower($rec['title'] . ' ' . implode(' ', $rec['categories'] ?? []));
        foreach ((array) ($this->config['exclude_keywords'] ?? []) as $kw) {
            if ($kw !== '' && str_contains(strtolower($rec['title']), strtolower($kw))) {
                return 'excluded keyword "' . $kw . '"';
            }
        }
        $req = (array) ($this->config['require_keywords'] ?? []);
        if (!empty($this->config['exclude_acts'])
            && preg_match('/^(.+?)\s+(?:at|@)\s+(?:the\s+)?(.+)$/i', $rec['title'], $m)
            && !$this->hasKeyword(strtolower($m[1]), $req ?: ['rodeo'])
            && $this->hasKeyword(strtolower($m[2]), $req ?: ['rodeo'])) {
            return 'act appearing at a rodeo (concert/performance), not a competition';
        }
        if ($req) {
            foreach ($req as $kw) {
                if ($kw !== '' && preg_match('/\b' . preg_quote(strtolower($kw), '/') . '/', $hay)) {
                    return null;
                }
            }
            return 'not rodeo-related (no required keyword)';
        }
        return null;
    }

    private function hasKeyword(string $hay, array $kws): bool
    {
        foreach ($kws as $kw) {
            if ($kw !== '' && preg_match('/\b' . preg_quote(strtolower($kw), '/') . '/', $hay)) {
                return true;
            }
        }
        return false;
    }

    protected function cleanTitle(string $t): string
    {
        $t = html_entity_decode(strip_tags($t), ENT_QUOTES | ENT_HTML5, 'UTF-8');
        if (!empty($this->config['title_strip_regex'])) {
            $t = (string) preg_replace('~' . str_replace('~', '\~', $this->config['title_strip_regex']) . '~u', '', $t);
        }
        $t = trim(preg_replace('/\s+/u', ' ', $t) ?? $t);
        $map = (array) ($this->config['title_replace'] ?? []);
        return isset($map[$t]) ? (string) $map[$t] : $t;
    }

    protected function plain(?string $html, int $max = 4000): ?string
    {
        if ($html === null) {
            return null;
        }
        $t = preg_replace('~<(br|/p|/li|/h\d)\s*/?>~i', "\n", $html) ?? $html;
        $t = html_entity_decode(strip_tags($t), ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $t = preg_replace("/[ \t]+/", ' ', $t) ?? $t;
        $t = trim(preg_replace("/\n\s*\n+/", "\n\n", $t) ?? $t);
        return $t === '' ? null : mb_substr($t, 0, $max);
    }

    /** Merge the configured default venue into a (possibly empty) venue. */
    protected function venue(array $v): array
    {
        $base = ['name' => null, 'address' => null, 'city' => null, 'state' => null, 'postal_code' => null,
                 'country' => null, 'lat' => null, 'lng' => null];
        $v = array_merge($base, array_intersect_key($v, $base));
        $def = $this->config['default_venue'] ?? null;
        if (is_array($def)) {
            $sameVenue = $v['name'] === null || $def['name'] === null
                || strcasecmp(trim((string) $v['name']), trim((string) $def['name'])) === 0;
            if ($sameVenue && $v['city'] === null && $v['address'] === null) {
                $v = array_merge($v, array_filter(array_intersect_key($def, $base), static fn($x) => $x !== null && $x !== ''));
            }
        }
        foreach ($v as $k => $x) {
            $v[$k] = is_string($x) ? (trim(html_entity_decode($x, ENT_QUOTES | ENT_HTML5, 'UTF-8')) ?: null) : $x;
            if (is_string($v[$k]) && !preg_match('/[\p{L}\p{N}]/u', $v[$k])) {
                $v[$k] = null;   // placeholders such as "-" or "TBA:" punctuation only
            }
        }
        return $v;
    }

    /** Status only when the source states it: explicit field or a title prefix like "CANCELED:". */
    protected function explicitStatus(string $title, ?string $field = null): ?string
    {
        $f = strtolower((string) $field);
        if ($f !== '') {
            if (str_contains($f, 'cancel')) return 'canceled';
            if (str_contains($f, 'postpon') || str_contains($f, 'rescheduled')) return 'postponed';
            if (str_contains($f, 'scheduled') || str_contains($f, 'confirmed')) return 'scheduled';
        }
        if (preg_match('/^\W*(cancell?ed)\b/i', $title)) return 'canceled';
        if (preg_match('/^\W*(postponed)\b/i', $title)) return 'postponed';
        return null;
    }

    protected function stripStatusPrefix(string $title): string
    {
        return trim(preg_replace('/^\W*(cancell?ed|postponed)\W*/i', '', $title) ?? $title);
    }

    protected function http(string $url, array $opts = []): array
    {
        $opts['min_delay'] = (float) ($this->config['min_delay'] ?? 1);
        return \RT\Http::get($url, $opts);
    }
}
