<?php
// Readable, indexable search URLs: /apartments/{area}/{tokens}/
//
//   /apartments/3-beds/                     beds=3
//   /apartments/3-beds-1200-to-1600/        beds=3, price 1200–1600
//   /apartments/houston-heights/pet-friendly-with-pool/
//
// Tokens always appear in a fixed order (beds, baths, price, flags,
// amenities, year) so each filter combination has exactly one URL.
// Anything that can't be expressed as a token (keyword, drawn area, sort,
// several bedroom counts, size) stays in the query string, and such pages
// are not indexed.
defined('HA_ROOT') || exit;

final class Filters
{
    public const FLAGS = [
        'pets'      => ['pet-friendly', 'Pet-Friendly'],
        'parking'   => ['parking', 'with Parking'],
        'special'   => ['move-in-specials', 'with Move-In Specials'],
        'furnished' => ['furnished', 'Furnished'],
        'essential' => ['income-restricted', 'Income-Restricted'],
    ];

    /**
     * Short amenity words. All "with" amenities (plus parking) share one
     * prefix: /apartments/with-pool-gym-closets/. "gated" stands alone.
     */
    public const AMEN_SLUGS = [
        'pool' => 'pool', 'fitness' => 'gym', 'washer' => 'washer-dryer', 'elevator' => 'elevator',
        'gated' => 'gated', 'balcony' => 'balcony', 'walkin' => 'closets', 'stainless' => 'stainless',
        'hardwood' => 'hardwood', 'dogpark' => 'dog-park', 'business' => 'business-center',
        'concierge' => 'concierge', 'clubhouse' => 'clubhouse', 'package' => 'package-lockers',
        'fireplace' => 'fireplace', 'wifi' => 'wifi',
    ];

    /** Query keys that are carried in the path. */
    private const PATH_KEYS = ['area', 'beds', 'baths', 'price_min', 'price_max', 'pets', 'parking', 'special', 'furnished', 'essential', 'amen', 'year'];
    /** Query keys kept as ?query (not indexable). */
    private const QUERY_KEYS = ['q', 'poly', 'sort', 'sqft', 'page', 'draw'];

    public static function areaShort(string $key): string
    {
        return slugify(str_replace(['/', '&'], ' ', AREAS[$key]['name'] ?? ''));
    }

    public static function areaByShort(string $short): ?string
    {
        foreach (AREAS as $key => $_) {
            if (self::areaShort($key) === $short) {
                return $key;
            }
        }
        return null;
    }

    public static function knownKeys(): array
    {
        return array_merge(self::PATH_KEYS, self::QUERY_KEYS);
    }

    /** Keep only known, non-empty filter values in a canonical form. */
    public static function normalize(array $in): array
    {
        $s = [];
        if (!empty($in['area']) && isset(AREAS[$in['area']])) {
            $s['area'] = $in['area'];
        }
        if (isset($in['beds']) && $in['beds'] !== '') {
            $b = array_unique(array_filter(array_map('intval', explode(',', (string) $in['beds'])), fn ($v) => $v >= 0 && $v <= 4));
            $b = array_values(array_intersect([0, 1, 2, 3, 4], $b));
            if ($b) {
                $s['beds'] = implode(',', $b);
            }
        }
        if (!empty($in['baths']) && (int) $in['baths'] >= 1 && (int) $in['baths'] <= 4) {
            $s['baths'] = (string) (int) $in['baths'];
        }
        foreach (['price_min', 'price_max'] as $k) {
            if (!empty($in[$k]) && (int) $in[$k] >= 100 && (int) $in[$k] <= 50000) {
                $s[$k] = (string) (int) $in[$k];
            }
        }
        if (isset($s['price_min'], $s['price_max']) && (int) $s['price_min'] > (int) $s['price_max']) {
            [$s['price_min'], $s['price_max']] = [$s['price_max'], $s['price_min']];
        }
        foreach (array_keys(self::FLAGS) as $f) {
            if (!empty($in[$f])) {
                $s[$f] = '1';
            }
        }
        if (!empty($in['amen'])) {
            $want = explode(',', (string) $in['amen']);
            $a = array_values(array_filter(array_keys(self::AMEN_SLUGS), fn ($k) => in_array($k, $want, true)));
            if ($a) {
                $s['amen'] = implode(',', $a);
            }
        }
        if (!empty($in['year']) && (int) $in['year'] >= 1950 && (int) $in['year'] <= 2100) {
            $s['year'] = (string) (int) $in['year'];
        }
        foreach (self::QUERY_KEYS as $k) {
            if (isset($in[$k]) && $in[$k] !== '' && !($k === 'page' && (int) $in[$k] <= 1)) {
                $s[$k] = mb_substr((string) $in[$k], 0, $k === 'poly' ? 12000 : 80);
            }
        }
        return $s;
    }

    /** @return string[] path tokens for a normalized state (empty when nothing pathable). */
    public static function tokens(array $s): array
    {
        $t = [];
        if (isset($s['beds']) && !str_contains($s['beds'], ',')) {
            $b = (int) $s['beds'];
            $t[] = $b === 0 ? 'studio' : ($b === 1 ? '1-bed' : ($b === 4 ? '4-plus-beds' : "$b-beds"));
        }
        if (isset($s['baths'])) {
            $t[] = $s['baths'] . ((int) $s['baths'] === 1 ? '-bath' : '-baths');
        }
        if (isset($s['price_min'], $s['price_max'])) {
            $t[] = $s['price_min'] . '-to-' . $s['price_max'];
        } elseif (isset($s['price_max'])) {
            $t[] = 'under-' . $s['price_max'];
        } elseif (isset($s['price_min'])) {
            $t[] = 'over-' . $s['price_min'];
        }
        foreach (self::FLAGS as $k => [$slug]) {
            if (isset($s[$k]) && $k !== 'parking') {
                $t[] = $slug;
            }
        }
        $amen = explode(',', $s['amen'] ?? '');
        if (in_array('gated', $amen, true)) {
            $t[] = 'gated';
        }
        $with = isset($s['parking']) ? ['parking'] : [];
        foreach ($amen as $a) {
            if (isset(self::AMEN_SLUGS[$a]) && $a !== 'gated') {
                $with[] = self::AMEN_SLUGS[$a];
            }
        }
        if ($with) {
            $t[] = 'with-' . implode('-', $with);
        }
        if (isset($s['year'])) {
            $t[] = 'built-' . $s['year'] . '-or-later';
        }
        return $t;
    }

    /** Canonical URL (path + leftover query) for a state. */
    public static function url(array $in, bool $withQuery = true): string
    {
        $s = self::normalize($in);
        $path = '/apartments/';
        if (isset($s['area'])) {
            $path .= self::areaShort($s['area']) . '/';
        }
        if ($t = self::tokens($s)) {
            $path .= implode('-', $t) . '/';
        }
        if (!$withQuery) {
            return $path;
        }
        $q = array_intersect_key($s, array_flip(self::QUERY_KEYS));
        if (isset($s['beds']) && str_contains($s['beds'], ',')) {
            $q = ['beds' => $s['beds']] + $q;
        }
        return $path . ($q ? '?' . http_build_query($q) : '');
    }

    /** Parse "/apartments/{a}/{b}/" segments into a state; null if not a valid filter URL. */
    public static function parse(array $segments): ?array
    {
        $s = [];
        if ($segments && ($area = self::areaByShort($segments[0]))) {
            $s['area'] = $area;
            array_shift($segments);
        }
        if (count($segments) > 1) {
            return null;
        }
        $rest = $segments[0] ?? '';
        $patterns = [
            '(studio|1-bed|([23])-beds|4-plus-beds)' => function ($m) use (&$s) {
                $s['beds'] = (string) ($m[1] === 'studio' ? 0 : ($m[1] === '1-bed' ? 1 : ($m[1] === '4-plus-beds' ? 4 : (int) $m[2])));
            },
            '([1-4])-baths?' => function ($m) use (&$s) { $s['baths'] = $m[1]; },
            '(\d{3,5})-to-(\d{3,5})' => function ($m) use (&$s) { $s['price_min'] = $m[1]; $s['price_max'] = $m[2]; },
            'under-(\d{3,5})' => function ($m) use (&$s) { $s['price_max'] = $m[1]; },
            'over-(\d{3,5})' => function ($m) use (&$s) { $s['price_min'] = $m[1]; },
            'built-(\d{4})-or-later' => function ($m) use (&$s) { $s['year'] = $m[1]; },
        ];
        foreach (self::FLAGS as $k => [$slug]) {
            if ($k !== 'parking') {
                $patterns[preg_quote($slug, '#')] = function () use (&$s, $k) { $s[$k] = '1'; };
            }
        }
        $patterns['gated'] = function () use (&$s) { $s['amen'] = trim(($s['amen'] ?? '') . ',gated', ','); };
        // "with-" followed by one or more amenity words (longest first so washer-dryer beats washer)
        $words = array_filter(self::AMEN_SLUGS, fn ($w) => $w !== 'gated') + ['parking' => 'parking'];
        uasort($words, fn ($a, $b) => strlen($b) <=> strlen($a));
        $alt = implode('|', array_map(fn ($w) => preg_quote($w, '#'), $words));
        $patterns["with-((?:(?:with-)?(?:$alt)(?:-(?=(?:with-)?(?:$alt)(?:-|$))|))+)"] = function ($m) use (&$s, $words, $alt) {
            preg_match_all("#(?:with-)?($alt)(?=-|$)#", $m[1], $mm);
            foreach ($mm[1] as $w) {
                $key = array_search($w, $words, true);
                if ($key === 'parking') {
                    $s['parking'] = '1';
                } else {
                    $s['amen'] = trim(($s['amen'] ?? '') . ',' . $key, ',');
                }
            }
        };
        while ($rest !== '') {
            $hit = false;
            foreach ($patterns as $re => $apply) {
                if (preg_match('#^' . $re . '(?:-|$)#', $rest, $m)) {
                    $apply($m);
                    $rest = substr($rest, strlen(rtrim($m[0], '-')));
                    $rest = ltrim($rest, '-');
                    $hit = true;
                    break;
                }
            }
            if (!$hit) {
                return null;
            }
        }
        return $s;
    }

    /** Pages worth indexing: only path filters, at most three of them, and at least one result. */
    public static function indexable(array $s, int $total): bool
    {
        $s = self::normalize($s);
        if ($total < 1 || array_intersect_key($s, array_flip(self::QUERY_KEYS)) || (isset($s['beds']) && str_contains($s['beds'], ','))) {
            return false;
        }
        return count(self::tokens($s)) <= 3;
    }

    /** Human label pieces for titles, headings and descriptions. */
    public static function describe(array $in): array
    {
        $s = self::normalize($in);
        $pre = [];
        foreach (['pets', 'furnished', 'essential'] as $f) {
            if (isset($s[$f])) {
                $pre[] = self::FLAGS[$f][1];
            }
        }
        $size = '';
        if (isset($s['beds']) && !str_contains($s['beds'], ',')) {
            $b = (int) $s['beds'];
            $size = $b === 0 ? 'Studio' : ($b === 4 ? '4+ Bedroom' : "$b Bedroom");
        } elseif (isset($s['beds'])) {
            $size = implode(' & ', array_map(fn ($b) => $b === '0' ? 'Studio' : ($b === '4' ? '4+' : $b), explode(',', $s['beds']))) . ' Bedroom';
        }
        if (isset($s['baths'])) {
            $size = trim(($size ? str_replace(' Bedroom', ' Bed', $size) . ', ' : '') . $s['baths'] . '+ Bath');
        }
        $with = [];
        foreach (explode(',', $s['amen'] ?? '') as $a) {
            if (isset(Listings::AMENITIES[$a])) {
                $with[] = preg_replace('# / .*$#', '', Listings::AMENITIES[$a][0]);
            }
        }
        if (isset($s['parking'])) {
            $with[] = 'Parking';
        }
        $price = '';
        if (isset($s['price_min'], $s['price_max'])) {
            $price = '$' . number_format((int) $s['price_min']) . ' to $' . number_format((int) $s['price_max']);
        } elseif (isset($s['price_max'])) {
            $price = 'Under $' . number_format((int) $s['price_max']);
        } elseif (isset($s['price_min'])) {
            $price = 'Over $' . number_format((int) $s['price_min']);
        }
        $place = isset($s['area']) ? AREAS[$s['area']]['name'] . ', Houston' : 'Houston, TX';
        $noun = trim(implode(' ', $pre) . ' ' . $size . ' Apartments');
        $tail = ($with ? ' with ' . self::andList($with) : '') . (isset($s['special']) ? ' with Move-In Specials' : '') . (isset($s['year']) ? ' Built ' . $s['year'] . '+' : '');
        $h1 = $noun . ' for Rent in ' . $place . $tail . ($price ? ' – ' . $price : '');
        return ['noun' => $noun, 'place' => $place, 'price' => $price, 'tail' => $tail, 'h1' => $h1];
    }

    private static function andList(array $items): string
    {
        return count($items) > 1 ? implode(', ', array_slice($items, 0, -1)) . ' & ' . end($items) : ($items[0] ?? '');
    }

    /** Links for "popular searches" blocks and the sitemap. */
    public static function popular(?string $area = null): array
    {
        $base = $area ? ['area' => $area] : [];
        $combos = [
            ['beds' => '0'], ['beds' => '1'], ['beds' => '2'], ['beds' => '3'], ['pets' => '1'],
            ['price_max' => '1200'], ['price_max' => '1500'], ['price_min' => '1200', 'price_max' => '1600'],
            ['amen' => 'pool'], ['amen' => 'washer'], ['amen' => 'fitness'], ['special' => '1'], ['furnished' => '1'],
            ['parking' => '1'], ['essential' => '1'], ['beds' => '2', 'pets' => '1'], ['beds' => '1', 'price_max' => '1200'],
        ];
        return array_map(fn ($c) => $base + $c, $combos);
    }
}
