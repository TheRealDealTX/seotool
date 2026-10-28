<?php
// Read side of the listings database: search, cards, property pages.
defined('HA_ROOT') || exit;

final class Listings
{
    /** Amenity filter keys → substrings matched against the normalized amenity list. */
    public const AMENITIES = [
        'pool'      => ['Pool', ['pool']],
        'fitness'   => ['Fitness Center', ['fitness', 'gym']],
        'washer'    => ['Washer/Dryer', ['washer']],
        'elevator'  => ['Elevator', ['elevator']],
        'gated'     => ['Gated / Controlled Access', ['controlled access', 'gated']],
        'balcony'   => ['Balcony / Patio', ['patio', 'balcony']],
        'walkin'    => ['Walk-in Closets', ['walk-in closet']],
        'stainless' => ['Stainless Appliances', ['stainless']],
        'hardwood'  => ['Hardwood / Plank Floors', ['hardwood', 'vinyl floor', 'plank']],
        'dogpark'   => ['Dog Park / Pet Spa', ['pet grooming', 'dog park', 'pet wash', 'dog run']],
        'business'  => ['Business Center', ['business center', 'co-working', 'coworking']],
        'concierge' => ['Concierge', ['concierge']],
        'clubhouse' => ['Clubhouse', ['clubhouse']],
        'package'   => ['Package Service', ['package']],
        'fireplace' => ['Fireplace', ['fireplace']],
        'wifi'      => ['Wi-Fi', ['wifi', 'wi-fi']],
    ];

    private const CARD_COLS = 'id, slug, name, street, city, zip, lat, lng, neighborhood, rise_location, price_min, price_max, beds_min, beds_max, beds_mask, baths_max, sqft_min, sqft_max, pets, parking, furnished, essential, special, year_built, units, stories, rating, photo, photo_count, data';

    public static function search(array $q): array
    {
        $q = Filters::normalize($q) + array_intersect_key($q, array_flip(['bounds', 'per']));
        $where = ["status = 'publish'", 'lat IS NOT NULL'];
        $args = [];

        if (!empty($q['area']) && isset(AREAS[$q['area']])) {
            $ids = AREAS[$q['area']]['rise'];
            $where[] = 'rise_location IN (' . implode(',', array_map('intval', $ids)) . ')';
        }
        if (!empty($q['bounds'])) {
            $b = array_map('floatval', explode(',', $q['bounds']));
            if (count($b) === 4) {
                $where[] = 'lat BETWEEN ? AND ? AND lng BETWEEN ? AND ?';
                array_push($args, $b[0], $b[2], $b[1], $b[3]);
            }
        }
        $poly = self::polygon($q['poly'] ?? '');
        if ($poly) {
            $lats = array_column($poly, 0);
            $lngs = array_column($poly, 1);
            $where[] = 'lat BETWEEN ? AND ? AND lng BETWEEN ? AND ?';
            array_push($args, min($lats), max($lats), min($lngs), max($lngs));
        }
        $pmin = (int) ($q['price_min'] ?? 0);
        $pmax = (int) ($q['price_max'] ?? 0);
        if ($pmin || $pmax) {
            $where[] = 'price_min IS NOT NULL';
            if ($pmax) {
                $where[] = 'price_min <= ?';
                $args[] = $pmax;
            }
            if ($pmin) {
                $where[] = 'COALESCE(price_max, price_min) >= ?';
                $args[] = $pmin;
            }
        }
        if (isset($q['beds']) && $q['beds'] !== '') {
            $mask = 0;
            foreach (explode(',', (string) $q['beds']) as $b) {
                if (is_numeric($b)) {
                    $mask |= 1 << min(4, max(0, (int) $b));
                }
            }
            if ($mask) {
                $where[] = '(beds_mask & ' . $mask . ') > 0';
            }
        }
        if (!empty($q['baths'])) {
            $where[] = 'baths_max >= ?';
            $args[] = (float) $q['baths'];
        }
        foreach (['pets', 'parking', 'furnished', 'special', 'essential'] as $flag) {
            if (!empty($q[$flag])) {
                $where[] = "$flag = 1";
            }
        }
        if (!empty($q['sqft'])) {
            $where[] = 'COALESCE(sqft_max, 0) >= ?';
            $args[] = (int) $q['sqft'];
        }
        if (!empty($q['year'])) {
            $where[] = 'year_built >= ?';
            $args[] = (int) $q['year'];
        }
        if (!empty($q['amen'])) {
            foreach (explode(',', (string) $q['amen']) as $key) {
                if (!isset(self::AMENITIES[$key])) {
                    continue;
                }
                $or = [];
                foreach (self::AMENITIES[$key][1] as $needle) {
                    $or[] = 'amenities LIKE ?';
                    $args[] = '%' . $needle . '%';
                }
                $where[] = '(' . implode(' OR ', $or) . ')';
            }
        }
        if (!empty($q['q'])) {
            $kw = '%' . mb_substr(trim((string) $q['q']), 0, 60) . '%';
            $where[] = '(name LIKE ? OR street LIKE ? OR neighborhood LIKE ? OR zip LIKE ? OR city LIKE ?)';
            array_push($args, $kw, $kw, $kw, $kw, $kw);
        }

        $order = match ($q['sort'] ?? '') {
            'price_asc'  => 'CASE WHEN price_min IS NULL THEN 1 ELSE 0 END, price_min ASC',
            'price_desc' => 'price_min IS NULL, COALESCE(price_max, price_min) DESC',
            'newest'     => 'year_built IS NULL, year_built DESC',
            'rating'     => 'rating IS NULL, rating DESC',
            'sqft'       => 'sqft_max IS NULL, sqft_max DESC',
            default      => 'photo_count DESC, rating DESC, id DESC',
        };
        $st = db()->prepare('SELECT ' . self::CARD_COLS . ' FROM properties WHERE ' . implode(' AND ', $where) . " ORDER BY $order");
        $st->execute($args);
        $rows = $st->fetchAll();
        if ($poly) {
            $rows = array_values(array_filter($rows, fn ($r) => self::inPolygon((float) $r['lat'], (float) $r['lng'], $poly)));
        }

        $per = min(60, max(6, (int) ($q['per'] ?? 24)));
        $page = max(1, (int) ($q['page'] ?? 1));
        $total = count($rows);
        $showPrice = config('price_display') !== 'hidden';
        $hoods = array_count_values(array_filter(array_column($rows, 'neighborhood')));
        arsort($hoods);
        return [
            'total'   => $total,
            'page'    => $page,
            'pages'   => max(1, (int) ceil($total / $per)),
            'hoods'   => array_slice($hoods, 0, 6, true),
            'items'   => array_map([self::class, 'card'], array_slice($rows, ($page - 1) * $per, $per)),
            'markers' => array_map(fn ($r) => [(int) $r['id'], round((float) $r['lat'], 6), round((float) $r['lng'], 6), $showPrice && $r['price_min'] ? (int) $r['price_min'] : null, $r['slug']], $rows),
        ];
    }

    /** "lat,lng;lat,lng;..." → [[lat, lng], ...] (at least a triangle). */
    private static function polygon(string $s): array
    {
        $pts = [];
        foreach (explode(';', $s) as $pair) {
            $xy = explode(',', $pair);
            if (count($xy) === 2 && is_numeric($xy[0]) && is_numeric($xy[1])) {
                $pts[] = [(float) $xy[0], (float) $xy[1]];
            }
        }
        return count($pts) >= 3 ? array_slice($pts, 0, 500) : [];
    }

    /** Ray casting point-in-polygon. */
    public static function inPolygon(float $lat, float $lng, array $poly): bool
    {
        $in = false;
        for ($i = 0, $j = count($poly) - 1; $i < count($poly); $j = $i++) {
            [$yi, $xi] = $poly[$i];
            [$yj, $xj] = $poly[$j];
            if ((($yi > $lat) !== ($yj > $lat)) && ($lng < ($xj - $xi) * ($lat - $yi) / (($yj - $yi) ?: 1e-12) + $xi)) {
                $in = !$in;
            }
        }
        return $in;
    }

    public static function card(array $r): array
    {
        $d = json_decode($r['data'] ?? '{}', true) ?: [];
        return [
            'id'      => (int) $r['id'],
            'slug'    => $r['slug'],
            'url'     => listing_url($r['slug']),
            'name'    => $r['name'],
            'address' => trim($r['street'] . ', ' . $r['city'] . ', TX ' . $r['zip'], ', '),
            'hood'    => $r['neighborhood'],
            'lat'     => (float) $r['lat'],
            'lng'     => (float) $r['lng'],
            'price'   => self::priceLabel($r),
            'beds'    => beds_range($r),
            'sqft'    => $r['sqft_min'] ? number_format((int) $r['sqft_min']) . ($r['sqft_max'] != $r['sqft_min'] ? '–' . number_format((int) $r['sqft_max']) : '') . ' sqft' : '',
            'photos'  => array_slice($d['photos'] ?? [], 0, 5),
            'rating'  => $r['rating'] ? (float) $r['rating'] : null,
            'pets'    => (bool) $r['pets'],
            'special' => (bool) $r['special'],
            'year'    => $r['year_built'] ? (int) $r['year_built'] : null,
            'new'     => $r['year_built'] && (int) $r['year_built'] >= (int) date('Y') - 3,
        ];
    }

    /**
     * Public price text. Exact rents stay in the database for the filters;
     * visitors only see "Starts at $X" (price_display = starts_at) or
     * "Check for availability" (price_display = hidden, or no price known).
     */
    public static function priceLabel(array $r): string
    {
        return self::startsAt($r['price_min'] ?? null);
    }

    public static function startsAt($price): string
    {
        if (!$price || config('price_display') === 'hidden') {
            return 'Check for availability';
        }
        return 'Starts at ' . money($price);
    }

    /** Drop sentences that quote rent figures (imported descriptions often do). */
    public static function stripPrices(string $text): string
    {
        $parts = preg_split('/(?<=[.!?])\s+/', $text);
        return implode(' ', array_filter($parts, fn ($p) => !preg_match('/\$\s?\d[\d,]{2,}/', $p)));
    }

    /**
     * Derived search columns for a listing from its detail data
     * (shared by the Rise importer and the admin editor).
     */
    public static function derive(array $data): array
    {
        $plans = $data['floorplans'] ?? [];
        $prices = array_filter(array_map('intval', $data['prices'] ?? []));
        $beds = array_unique(array_merge(array_map('intval', array_column($plans, 'beds')), array_map('intval', array_keys($prices))));
        sort($beds);
        $mask = 0;
        foreach ($beds as $b) {
            $mask |= 1 << min($b, 4);
        }
        $sqft = array_filter(array_map('intval', array_column($plans, 'sqft')));
        $amen = !empty($data['amenities']) ? array_merge(...array_values($data['amenities'])) : [];
        $photos = $data['photos'] ?? [];
        return [
            'price_min'   => $prices ? min($prices) : null,
            'price_max'   => $prices ? max($prices) : null,
            'beds_min'    => $beds ? min($beds) : 0,
            'beds_max'    => $beds ? max($beds) : 0,
            'beds_mask'   => $mask,
            'baths_max'   => $plans ? max(array_map('floatval', array_column($plans, 'baths'))) : 0,
            'sqft_min'    => $sqft ? min($sqft) : null,
            'sqft_max'    => $sqft ? max($sqft) : null,
            'amenities'   => '|' . implode('|', array_unique(array_map('strtolower', $amen))) . '|',
            'photo'       => $photos[0] ?? '',
            'photo_count' => count($photos),
        ];
    }

    public static function upsert(array $rec): void
    {
        $cols = array_keys($rec);
        $ph = implode(',', array_fill(0, count($cols), '?'));
        if (db_driver() === 'sqlite') {
            $sql = 'INSERT OR REPLACE INTO properties (' . implode(',', $cols) . ") VALUES ($ph)";
        } else {
            $upd = implode(',', array_map(fn ($c) => "$c = VALUES($c)", array_diff($cols, ['id'])));
            $sql = 'INSERT INTO properties (' . implode(',', $cols) . ") VALUES ($ph) ON DUPLICATE KEY UPDATE $upd";
        }
        db_alive()->prepare($sql)->execute(array_values($rec));
    }

    /** Listing statuses as the admin shows them. 'review' = imported, hidden until the About text is rewritten. */
    public const STATUS_LABELS = ['publish' => 'Live', 'review' => 'Awaiting rewrite', 'hidden' => 'Hidden'];

    /**
     * Share (0–1) of the rewritten About text's 3-word phrases that also appear in the
     * original imported text. A genuine rewrite lands well under 0.5; light edits stay high.
     */
    public static function aboutOverlap(array $new, array $orig): float
    {
        $grams = function (array $paras): array {
            $w = preg_split('/[^\p{L}\p{N}$]+/u', mb_strtolower(implode(' ', $paras)), -1, PREG_SPLIT_NO_EMPTY);
            $g = [];
            for ($i = 0, $n = count($w) - 2; $i < $n; $i++) {
                $g[$w[$i] . ' ' . $w[$i + 1] . ' ' . $w[$i + 2]] = true;
            }
            return $g;
        };
        $a = $grams($new);
        if (!$a) {
            return 1.0;
        }
        return count(array_intersect_key($a, $grams($orig))) / count($a);
    }

    public static function bySlug(string $slug): ?array
    {
        $st = db()->prepare("SELECT * FROM properties WHERE slug = ? AND status = 'publish'");
        $st->execute([$slug]);
        $p = $st->fetch();
        if (!$p) {
            return null;
        }
        $p['d'] = json_decode($p['data'] ?? '{}', true) ?: [];
        return $p;
    }

    public static function nearby(array $p, int $n): array
    {
        if ($p['lat'] === null) {
            return [];
        }
        $st = db()->prepare("SELECT " . self::CARD_COLS . " FROM properties WHERE status = 'publish' AND id <> ? AND lat IS NOT NULL
            ORDER BY ((lat - ?) * (lat - ?) + (lng - ?) * (lng - ?)) LIMIT $n");
        $st->execute([$p['id'], $p['lat'], $p['lat'], $p['lng'], $p['lng']]);
        return array_map([self::class, 'card'], $st->fetchAll());
    }

    public static function featured(int $n): array
    {
        try {
            $rows = db()->query("SELECT " . self::CARD_COLS . " FROM properties WHERE status = 'publish' AND lat IS NOT NULL ORDER BY photo_count DESC, rating DESC LIMIT $n")->fetchAll();
        } catch (PDOException) {
            return [];
        }
        return array_map([self::class, 'card'], $rows);
    }

    public static function inArea(array $area, int $n): array
    {
        $res = self::search(['area' => $area['slug'], 'per' => $n]);
        return $res['items'];
    }

    public static function areaKeyFor(array $p): string
    {
        foreach (AREAS as $key => $a) {
            if (in_array((int) $p['rise_location'], $a['rise'], true)) {
                return $key;
            }
        }
        return '';
    }

    /** @return array<string, array{count:int, min:?int}> */
    public static function areaCounts(): array
    {
        $out = [];
        try {
            $rows = db()->query("SELECT rise_location, COUNT(*) c, MIN(price_min) m FROM properties WHERE status = 'publish' GROUP BY rise_location")->fetchAll();
        } catch (PDOException) {
            $rows = [];
        }
        foreach (AREAS as $key => $a) {
            $out[$key] = ['count' => 0, 'min' => null];
            foreach ($rows as $r) {
                if (in_array((int) $r['rise_location'], $a['rise'], true)) {
                    $out[$key]['count'] += (int) $r['c'];
                    if ($r['m'] && config('price_display') !== 'hidden' && (!$out[$key]['min'] || $r['m'] < $out[$key]['min'])) {
                        $out[$key]['min'] = (int) $r['m'];
                    }
                }
            }
        }
        return $out;
    }

    public static function stats(): array
    {
        try {
            $r = db()->query("SELECT COUNT(*) n, AVG(price_min) avg, MIN(price_min) lo, SUM(COALESCE(units, 0)) units FROM properties WHERE status = 'publish'")->fetch();
        } catch (PDOException) {
            $r = ['n' => 0, 'avg' => 0, 'lo' => 0, 'units' => 0];
        }
        return ['count' => (int) $r['n'], 'avg' => (int) $r['avg'], 'low' => (int) $r['lo'], 'units' => (int) $r['units']];
    }

    public static function allSlugs(): array
    {
        try {
            return db()->query("SELECT slug, synced_at FROM properties WHERE status = 'publish' ORDER BY slug")->fetchAll();
        } catch (PDOException) {
            return [];
        }
    }

    public static function metaDescription(array $p): string
    {
        $bits = [beds_range($p)];
        if ($p['price_min'] && config('price_display') !== 'hidden') {
            $bits[] = 'starting at ' . money($p['price_min']) . '/mo';
        }
        if ($p['pets']) {
            $bits[] = 'pet friendly';
        }
        $where = $p['neighborhood'] ? $p['neighborhood'] . ', ' . ($p['city'] ?: 'Houston') : ($p['city'] ?: 'Houston');
        return mb_substr(sprintf('%s apartments in %s, TX: %s. See floor plans, photos, amenities and schools – and get up to $%d back when you lease through Houston Apartments.',
            $p['name'], $where, implode(', ', $bits), SITE['cashback']), 0, 300);
    }

    public static function schema(array $p): array
    {
        $d = $p['d'];
        $s = [
            '@context' => 'https://schema.org',
            '@type' => 'ApartmentComplex',
            'name' => $p['name'],
            'url' => site_url(listing_url($p['slug'])),
            'image' => array_map('site_url', array_slice($d['photos'] ?? [], 0, 6)),
            'address' => ['@type' => 'PostalAddress', 'streetAddress' => $p['street'], 'addressLocality' => $p['city'],
                          'addressRegion' => 'TX', 'postalCode' => $p['zip'], 'addressCountry' => 'US'],
            'petsAllowed' => (bool) $p['pets'],
        ];
        if ($p['lat'] !== null) {
            $s['geo'] = ['@type' => 'GeoCoordinates', 'latitude' => (float) $p['lat'], 'longitude' => (float) $p['lng']];
        }
        if ($p['units']) {
            $s['numberOfAccommodationUnits'] = (int) $p['units'];
        }
        if (!empty($d['amenities'])) {
            $s['amenityFeature'] = array_map(fn ($a) => ['@type' => 'LocationFeatureSpecification', 'name' => $a, 'value' => true],
                array_slice(array_values(array_unique(array_merge(...array_values($d['amenities'])))), 0, 30));
        }
        $graph = [$s];
        if (!empty($d['faqs'])) {
            $graph[] = ['@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array_map(fn ($f) => [
                '@type' => 'Question', 'name' => $f['q'],
                'acceptedAnswer' => ['@type' => 'Answer', 'text' => implode(' ', $f['a'])],
            ], $d['faqs'])];
        }
        $graph[] = ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => [
            ['@type' => 'ListItem', 'position' => 1, 'name' => 'Houston Apartments', 'item' => site_url('/')],
            ['@type' => 'ListItem', 'position' => 2, 'name' => 'Apartments for Rent', 'item' => site_url('/apartments/')],
            ...(($ak = self::areaKeyFor($p)) ? [['@type' => 'ListItem', 'position' => 3, 'name' => AREAS[$ak]['name'], 'item' => site_url('/apartments/' . Filters::areaShort($ak) . '/')]] : []),
            ['@type' => 'ListItem', 'position' => self::areaKeyFor($p) ? 4 : 3, 'name' => $p['name'], 'item' => site_url(listing_url($p['slug']))],
        ]];
        return $graph;
    }
}
