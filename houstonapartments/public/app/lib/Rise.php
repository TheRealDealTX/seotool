<?php
// Imports listings from riseapartments.com (the same owner's WordPress site).
//
// The REST API (application password) gives the property list, taxonomy
// terms and featured image. The detailed fields (floor plans, prices,
// amenities, schools, FAQs) are ACF fields that are not exposed over REST,
// so they are read from each property's public page.
defined('HA_ROOT') || exit;

final class RiseClient
{
    private const BASE = 'https://riseapartments.com';
    private float $last = 0;

    public function __construct(private string $user, private string $pass) {}

    /** GET with retries; Rise's firewall resets bursts, so requests are spaced out. */
    public function get(string $url, bool $auth = false, float $gap = 1.2): string
    {
        $url = str_starts_with($url, 'http') ? $url : self::BASE . $url;
        for ($try = 1; ; $try++) {
            $wait = $gap - (microtime(true) - $this->last);
            if ($wait > 0) {
                usleep((int) ($wait * 1e6));
            }
            $this->last = microtime(true);
            $ch = curl_init($url);
            curl_setopt_array($ch, [
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_FOLLOWLOCATION => true,
                CURLOPT_TIMEOUT        => 60,
                CURLOPT_USERAGENT      => 'HoustonApartments-Sync/1.0 (+https://houstonapartments.com)',
                CURLOPT_ENCODING       => '',
            ]);
            if ($auth && $this->pass !== '') {
                curl_setopt($ch, CURLOPT_USERPWD, $this->user . ':' . $this->pass);
            }
            $body = curl_exec($ch);
            $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            $err = curl_error($ch);
            curl_close($ch);
            if ($body !== false && $code >= 200 && $code < 300) {
                return $body;
            }
            if ($try >= 4 || ($code >= 400 && $code < 500 && $code !== 429)) {
                throw new RuntimeException("GET $url failed: HTTP $code $err");
            }
            sleep(3 * $try);
        }
    }

    public function json(string $path): array
    {
        return json_decode($this->get($path, true), true) ?? [];
    }

    /** @return array<int, array> property summaries for one page of a city term */
    public function listPage(int $city, int $page, int $perPage = 100): array
    {
        $fields = 'id,slug,title,modified,location,city,featured_media,link';
        return $this->json("/wp-json/wp/v2/apartment?city=$city&per_page=$perPage&page=$page&orderby=modified&order=desc&_fields=$fields");
    }

    public function bySlug(string $slug): ?array
    {
        $rows = $this->json('/wp-json/wp/v2/apartment?slug=' . rawurlencode($slug) . '&_fields=id,slug,title,modified,location,city,featured_media,link');
        return $rows[0] ?? null;
    }

    /** @return array<int, array{name:string,parent:int}> */
    public function locations(): array
    {
        $out = [];
        foreach ([1, 2] as $page) {
            foreach ($this->json("/wp-json/wp/v2/location?per_page=100&page=$page&_fields=id,name,parent") as $t) {
                $out[$t['id']] = ['name' => html_entity_decode($t['name']), 'parent' => $t['parent']];
            }
        }
        return $out;
    }

    public function mediaUrl(int $id): string
    {
        if (!$id) {
            return '';
        }
        try {
            return $this->json("/wp-json/wp/v2/media/$id?_fields=source_url")['source_url'] ?? '';
        } catch (RuntimeException) {
            return '';
        }
    }
}

final class RiseParser
{
    /** Flat list of [kind, value, hidden] in document order. */
    private array $tok = [];

    public static function parse(string $html, string $name): array
    {
        $p = new self();
        $p->tokenize($html);
        return $p->extract($name);
    }

    private function tokenize(string $html): void
    {
        $doc = new DOMDocument();
        libxml_use_internal_errors(true);
        $doc->loadHTML('<?xml encoding="utf-8"?>' . $html, LIBXML_NOERROR | LIBXML_NOWARNING);
        libxml_clear_errors();
        $body = $doc->getElementsByTagName('body')->item(0);
        if ($body) {
            $this->walk($body, false);
        }
    }

    private function walk(DOMNode $node, bool $hidden): void
    {
        foreach ($node->childNodes as $c) {
            if ($c instanceof DOMElement) {
                $tag = strtolower($c->tagName);
                if (in_array($tag, ['script', 'style', 'svg', 'noscript', 'header', 'footer', 'nav'], true)) {
                    continue;
                }
                // Anywhere-Elementor marks conditionally hidden widgets with this class
                $h = $hidden || str_contains(' ' . $c->getAttribute('class') . ' ', ' ae-visibility-hidden ');
                if ($tag === 'img') {
                    $src = $c->getAttribute('data-lazy-src') ?: $c->getAttribute('data-src') ?: $c->getAttribute('src');
                    $this->tok[] = ['img', $src, $h];
                } elseif ($tag === 'a' && $c->getAttribute('href') !== '') {
                    $this->tok[] = ['a', $c->getAttribute('href'), $h];
                }
                foreach (['data-dce-background-image-url', 'data-bg-image-url'] as $attr) {
                    if ($c->getAttribute($attr)) {
                        $this->tok[] = ['img', $c->getAttribute($attr), $h];
                    }
                }
                $this->walk($c, $h);
            } elseif ($c instanceof DOMText) {
                $t = trim(preg_replace('/\s+/u', ' ', str_replace('\\$', '$', $c->nodeValue)));
                if ($t !== '') {
                    $this->tok[] = ['t', $t, $hidden];
                }
            }
        }
    }

    private function find(string $text, int $from = 0, bool $prefix = false): int
    {
        for ($i = $from, $n = count($this->tok); $i < $n; $i++) {
            [$k, $v] = $this->tok[$i];
            if ($k === 't' && ($prefix ? str_starts_with($v, $text) : $v === $text)) {
                return $i;
            }
        }
        return -1;
    }

    /** Visible text tokens in [a, b). */
    private function texts(int $a, int $b, bool $visibleOnly = true): array
    {
        $out = [];
        for ($i = max(0, $a); $i < $b; $i++) {
            [$k, $v, $h] = $this->tok[$i];
            if ($k === 't' && (!$visibleOnly || !$h)) {
                $out[] = $v;
            }
        }
        return $out;
    }

    private static function upload(string $src): ?string
    {
        if (!preg_match('#^https://riseapartments\.com/wp-content/uploads/(?!elementor/)\d{4}/\d{2}/[^?\#]+\.(webp|jpe?g|png)$#i', $src)) {
            return null;
        }
        return preg_replace('/-\d+x\d+(\.\w+)$/', '$1', $src);
    }

    private function extract(string $name): array
    {
        $n = count($this->tok);
        $out = ['address' => '', 'tags' => [], 'floorplans' => [], 'prices' => [], 'photos' => [],
                'amenities' => [], 'info' => [], 'schools' => [], 'about' => [], 'faqs' => [],
                'rating' => null, 'hours' => '', 'special' => ''];

        foreach ($this->tok as [$k, $v]) {
            if ($k === 'a' && str_starts_with($v, 'https://maps.google.com/?q=')) {
                $out['address'] = trim(urldecode(substr($v, 27)));
                break;
            }
        }

        $pricing = $this->find('Pricing & Floor Plans');
        $amen = $this->find('Amenities', max(0, $pricing));
        $details = $this->find('Property Details', max(0, $amen));
        $about = $this->find('About ' . $name, max(0, $details), true);
        if ($about < 0) {
            $about = $this->find('About ', max(0, $details), true);
        }
        $contact = $this->find('Contact Info', max(0, $about));
        $faq = $this->find('Frequently Asked Questions', max(0, $contact));
        $faqEnd = $this->find('My Personal Touring Experience', max(0, $faq));
        $tour = $this->find('Book A Tour Now');
        $offers = $this->find('Special Offers', max(0, $tour));

        // Gallery: uploaded photos before the pricing section
        $photos = [];
        for ($i = 0; $i < ($pricing > 0 ? $pricing : $n); $i++) {
            if (in_array($this->tok[$i][0], ['img', 'a'], true) && ($u = self::upload($this->tok[$i][1])) && !preg_match('/logo/i', $u)) {
                $photos[$u] = true;
            }
        }
        $out['photos'] = array_keys($photos);

        // Badges between the tour button and "Special Offers" (visible only)
        if ($tour >= 0 && $offers > $tour) {
            $out['tags'] = array_values(array_filter($this->texts($tour + 1, $offers), fn ($t) => strlen($t) < 40));
        }
        if ($offers >= 0 && $pricing > $offers) {
            $sp = array_diff($this->texts($offers + 1, $pricing), [
                'Move-in Specials', 'Currently Not Offering Specials',
                'Contact us for more information about the apartment move-in specials.', 'Apartmentlocating service',
            ]);
            $out['special'] = trim(implode(' ', $sp));
        }

        // Floor plans: per-bedroom "Price Starts At" headings plus plan cards
        if ($pricing >= 0) {
            $end = $amen > 0 ? $amen : $n;
            $seen = [];
            for ($i = $pricing; $i < $end; $i++) {
                [$k, $v] = $this->tok[$i];
                if ($k !== 't') {
                    continue;
                }
                if (preg_match('/^(Studio|(\d+) Beds?) Price Starts At \$([\d,]+)/', $v, $m)) {
                    $b = $m[1] === 'Studio' ? 0 : (int) $m[2];
                    $out['prices'][$b] = (int) str_replace(',', '', $m[3]);
                    continue;
                }
                if (preg_match('/^(Studio|\d+ Beds?)$/', $v) && $i + 2 < $end
                    && preg_match('/^([\d.]+) Baths?$/', $this->tok[$i + 1][1], $bm)
                    && preg_match('/^([\d,]+) sqft$/', $this->tok[$i + 2][1], $sm)) {
                    $beds = $v === 'Studio' ? 0 : (int) $v;
                    $plan = ['beds' => $beds, 'baths' => (float) $bm[1], 'sqft' => (int) str_replace(',', '', $sm[1]),
                             'available' => '', 'image' => ''];
                    for ($j = $i + 3; $j < min($end, $i + 30); $j++) {
                        [$k2, $v2] = $this->tok[$j];
                        if ($k2 === 't' && $v2 === 'Availability' && isset($this->tok[$j + 1])) {
                            $plan['available'] = $this->tok[$j + 1][1];
                        }
                        if ($k2 === 'img' && ($u = self::upload($v2))) {
                            $plan['image'] = $u;
                            break;
                        }
                        if ($k2 === 't' && $j > $i + 3 && preg_match('/^(Studio|\d+ Beds?)$/', $v2)) {
                            break;
                        }
                    }
                    $key = "$beds|{$plan['baths']}|{$plan['sqft']}|{$plan['image']}";
                    if (!isset($seen[$key])) {
                        $seen[$key] = true;
                        $out['floorplans'][] = $plan;
                    }
                }
            }
        }

        // Amenity groups
        if ($amen >= 0 && $details > $amen) {
            $group = null;
            foreach ($this->texts($amen + 1, $details) as $t) {
                if (in_array($t, ['Unit Features', 'Community Amenities', 'Luxuries', 'Lease Terms', 'Utilities Included', 'Pet Policy', 'Parking'], true)) {
                    $group = $t;
                    continue;
                }
                if ($group) {
                    $out['amenities'][$group][] = $t;
                }
            }
            foreach ($out['amenities'] as $g => $list) {
                $out['amenities'][$g] = array_values(array_unique($list));
            }
        }

        // Property info / education as label → value pairs
        if ($details >= 0) {
            $t = $this->texts($details + 1, $about > 0 ? $about : min($n, $details + 60));
            $labels = ['Year Built', 'Units', 'Stories', 'Furniture', 'District', 'Elementary School', 'Middle School', 'High School'];
            foreach ($t as $idx => $label) {
                if (in_array($label, $labels, true) && isset($t[$idx + 1]) && !in_array($t[$idx + 1], $labels, true)) {
                    if (in_array($label, ['District', 'Elementary School', 'Middle School', 'High School'], true)) {
                        $out['schools'][$label] = $t[$idx + 1];
                    } else {
                        $out['info'][$label] = $t[$idx + 1];
                    }
                }
            }
        }

        if ($about >= 0 && $contact > $about) {
            $out['about'] = $this->texts($about + 1, $contact);
        }

        if ($contact >= 0) {
            $c = $this->texts($contact, $faq > 0 ? $faq : min($n, $contact + 20));
            foreach ($c as $i => $t) {
                if ($t === 'Google Rating' && isset($c[$i + 1]) && preg_match('#^([\d.]+)/5$#', $c[$i + 1], $m)) {
                    $out['rating'] = (float) $m[1];
                }
                if (preg_match('/^\d{1,2}(:\d\d)? ?-? ?\d{1,2}(:\d\d)? ?(AM|PM)$/i', $t)) {
                    $out['hours'] = $t;
                }
            }
        }

        // FAQs: question tokens end with "?", answers follow until the next question
        if ($faq >= 0) {
            $t = $this->texts($faq + 1, $faqEnd > 0 ? $faqEnd : min($n, $faq + 120));
            $cur = null;
            foreach ($t as $line) {
                if (str_starts_with($line, 'Thanks for stopping by')) {
                    break;
                }
                if (str_ends_with($line, '?')) {
                    if ($cur) {
                        $out['faqs'][] = $cur;
                    }
                    $cur = ['q' => $line, 'a' => []];
                } elseif ($cur) {
                    $cur['a'][] = $line;
                }
            }
            if ($cur) {
                $out['faqs'][] = $cur;
            }
        }
        return $out;
    }
}

final class Geocoder
{
    /** @return array{0: ?float, 1: ?float} */
    public static function locate(string $address): array
    {
        $key = substr(strtolower(trim($address)), 0, 190);
        $st = db_alive()->prepare('SELECT lat, lng FROM geocache WHERE address = ?');
        $st->execute([$key]);
        if ($row = $st->fetch()) {
            return [$row['lat'] !== null ? (float) $row['lat'] : null, $row['lng'] !== null ? (float) $row['lng'] : null];
        }
        [$lat, $lng, $src] = self::census($address) ?? self::nominatim($address) ?? [null, null, 'none'];
        $ins = db()->prepare('INSERT INTO geocache (address, lat, lng, source) VALUES (?, ?, ?, ?)');
        $ins->execute([$key, $lat, $lng, $src]);
        return [$lat, $lng];
    }

    private static function fetch(string $url): ?array
    {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 30,
            CURLOPT_USERAGENT => 'HoustonApartments/1.0 (listing geocoder)']);
        $body = curl_exec($ch);
        curl_close($ch);
        return $body ? json_decode($body, true) : null;
    }

    private static function census(string $a): ?array
    {
        $j = self::fetch('https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?benchmark=Public_AR_Current&format=json&address=' . rawurlencode($a));
        $m = $j['result']['addressMatches'][0]['coordinates'] ?? null;
        return $m ? [(float) $m['y'], (float) $m['x'], 'census'] : null;
    }

    private static function nominatim(string $a): ?array
    {
        usleep(1100000); // Nominatim usage policy: max 1 request/second
        $j = self::fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=us&q=' . rawurlencode($a));
        return isset($j[0]['lat']) ? [(float) $j[0]['lat'], (float) $j[0]['lon'], 'nominatim'] : null;
    }
}

final class RiseImporter
{
    private RiseClient $rise;
    private ?array $locations = null;
    public array $log = [];

    public function __construct()
    {
        $this->rise = new RiseClient(config('rise_user'), config('rise_pass'));
    }

    private function say(string $msg): void
    {
        $this->log[] = $msg;
        if (PHP_SAPI === 'cli') {
            fwrite(STDERR, $msg . "\n");
        }
    }

    /** Import specific properties by Rise slug. */
    public function importSlugs(array $slugs): int
    {
        $ok = 0;
        foreach ($slugs as $slug) {
            try {
                $row = $this->rise->bySlug($slug);
                if (!$row) {
                    $this->say("not found: $slug");
                    continue;
                }
                $this->importOne($row);
                $ok++;
            } catch (Throwable $e) {
                $this->say("error $slug: " . $e->getMessage());
            }
        }
        return $ok;
    }

    /**
     * Walk the configured Rise cities, importing new or changed listings.
     * $limit caps how many are (re)imported this run; $deadline is a unix time
     * to stop at so a web-triggered run stays inside max_execution_time.
     */
    public function sync(int $limit = 0, int $deadline = 0): array
    {
        $done = $skipped = 0;
        foreach (config('rise_cities', [21]) as $city) {
            for ($page = 1; ; $page++) {
                $rows = $this->rise->listPage((int) $city, $page);
                foreach ($rows as $row) {
                    if (($limit && $done >= $limit) || ($deadline && time() > $deadline)) {
                        return ['imported' => $done, 'unchanged' => $skipped, 'complete' => false];
                    }
                    $st = db_alive()->prepare('SELECT rise_modified FROM properties WHERE id = ?');
                    $st->execute([$row['id']]);
                    if ($st->fetchColumn() === $row['modified']) {
                        $skipped++;
                        continue;
                    }
                    try {
                        $this->importOne($row);
                        $done++;
                    } catch (Throwable $e) {
                        $this->say("error {$row['slug']}: " . $e->getMessage());
                    }
                }
                if (count($rows) < 100) {
                    break;
                }
            }
        }
        return ['imported' => $done, 'unchanged' => $skipped, 'complete' => true];
    }

    public function importOne(array $row): void
    {
        $name = html_entity_decode($row['title']['rendered'] ?? $row['slug'], ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $html = $this->rise->get($row['link'] ?? "/apartment/{$row['slug']}/");
        $d = RiseParser::parse($html, $name);

        $this->locations ??= $this->rise->locations();
        $locId = (int) ($row['location'][0] ?? 0);
        $loc = $this->locations[$locId] ?? ['name' => '', 'parent' => 0];
        $parent = $this->locations[$loc['parent']]['name'] ?? '';

        // "1810 Main St, Houston, TX 77002"
        $street = $city = $zip = '';
        $addr = preg_replace('/\s{2,}/', ', ', $d['address']);
        if (preg_match('/^(.*?),\s*([^,]+),\s*TX\s*(\d{5})?/i', $addr, $m)) {
            [$street, $city, $zip] = [trim($m[1]), trim($m[2]), $m[3] ?? ''];
        }
        [$lat, $lng] = $d['address'] !== '' ? Geocoder::locate($d['address']) : [null, null];

        $plans = $d['floorplans'];
        $bedsList = array_unique(array_merge(array_column($plans, 'beds'), array_keys($d['prices'])));
        sort($bedsList);
        $mask = 0;
        foreach ($bedsList as $b) {
            $mask |= 1 << min($b, 4);
        }
        $sqft = array_filter(array_column($plans, 'sqft'));
        $tags = $d['tags'];
        $furniture = $d['info']['Furniture'] ?? '';

        // Images are copied to our own server so the site never hotlinks Rise
        $id = (int) $row['id'];
        $photos = $d['photos'];
        if (!$photos && ($fm = $this->rise->mediaUrl((int) ($row['featured_media'] ?? 0)))) {
            $photos = [$fm];
        }
        $photos = array_slice($photos, 0, 24);
        $localPhotos = array_values(array_filter(array_map(fn ($u) => $this->copyImage($id, $u), $photos)));
        foreach ($plans as &$p) {
            $p['image'] = $p['image'] ? (string) $this->copyImage($id, $p['image']) : '';
        }
        unset($p);

        $allAmen = array_merge(...array_values($d['amenities'] ?: [[]]));
        $data = [
            'about'      => $d['about'],
            'floorplans' => $plans,
            'prices'     => $d['prices'],
            'photos'     => $localPhotos,
            'amenities'  => $d['amenities'],
            'info'       => $d['info'],
            'schools'    => $d['schools'],
            'faqs'       => $d['faqs'],
            'tags'       => $tags,
            'hours'      => $d['hours'],
            'special'    => $d['special'],
            'address'    => $d['address'],
        ];
        $prices = array_values($d['prices']);
        if (!$prices) {
            // No "Price Starts At" headings: fall back to the range quoted in the description
            preg_match_all('/\$\s?(\d{1,2},?\d{3})(?!\d)/', implode(' ', $d['about']), $pm);
            $prices = array_values(array_filter(array_map(fn ($v) => (int) str_replace(',', '', $v), $pm[1]), fn ($v) => $v >= 500 && $v <= 20000));
            $data['price_source'] = $prices ? 'description' : '';
        }
        $rec = [
            'id' => $id, 'slug' => $row['slug'], 'name' => $name,
            'street' => $street, 'city' => $city, 'state' => 'TX', 'zip' => $zip,
            'lat' => $lat, 'lng' => $lng,
            'area' => $parent, 'neighborhood' => preg_replace('/\s*(TX\s*)?Apartments?(\s+Houston)?\s*$/i', '', str_replace('Apartments in ', '', $loc['name'])),
            'rise_location' => $locId,
            'price_min' => $prices ? min($prices) : null,
            'price_max' => $prices ? max($prices) : null,
            'beds_min' => $bedsList ? min($bedsList) : 0,
            'beds_max' => $bedsList ? max($bedsList) : 0,
            'beds_mask' => $mask,
            'baths_max' => $plans ? max(array_column($plans, 'baths')) : 0,
            'sqft_min' => $sqft ? min($sqft) : null,
            'sqft_max' => $sqft ? max($sqft) : null,
            'pets' => (int) in_array('Pets Allowed', $tags, true),
            'parking' => (int) (in_array('Parking Included', $tags, true) || in_array('Parking', array_keys($d['amenities']), true)),
            'furnished' => (int) (stripos($furniture, 'furnished') === 0 || in_array('Furnished', $tags, true)),
            'essential' => (int) in_array('Essential Housing', $tags, true),
            'special' => (int) ($d['special'] !== ''),
            'year_built' => isset($d['info']['Year Built']) ? (int) $d['info']['Year Built'] ?: null : null,
            'units' => isset($d['info']['Units']) ? (int) $d['info']['Units'] ?: null : null,
            'stories' => isset($d['info']['Stories']) ? (int) $d['info']['Stories'] ?: null : null,
            'rating' => $d['rating'],
            'amenities' => '|' . implode('|', array_unique(array_map('strtolower', $allAmen))) . '|',
            'photo' => $localPhotos[0] ?? '',
            'photo_count' => count($localPhotos),
            'data' => json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE),
            'rise_modified' => $row['modified'],
            'synced_at' => gmdate('c'),
            'status' => 'publish',
        ];
        $this->upsert($rec);
        $this->say(sprintf('imported %s (%s, %d plans, %d photos, %s)', $row['slug'], $rec['neighborhood'], count($plans),
            count($localPhotos), $lat ? 'geocoded' : 'NO COORDS'));
    }

    private function upsert(array $rec): void
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

    /** Download a Rise upload into /media/p/{id}/; returns the public path or null. */
    private function copyImage(int $id, string $url): ?string
    {
        $base = preg_replace('/[^A-Za-z0-9._-]/', '-', basename(parse_url($url, PHP_URL_PATH)));
        $rel = "/media/p/$id/$base";
        $dest = HA_ROOT . $rel;
        if (is_file($dest) && filesize($dest) > 0) {
            return $rel;
        }
        try {
            $bytes = $this->rise->get($url, false, 0.25);
        } catch (RuntimeException $e) {
            $this->say('image failed: ' . $url);
            return null;
        }
        if (!is_dir(dirname($dest))) {
            mkdir(dirname($dest), 0755, true);
        }
        file_put_contents($dest, $bytes);
        return $rel;
    }
}
