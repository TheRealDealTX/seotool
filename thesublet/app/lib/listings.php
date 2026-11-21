<?php defined('APP') || exit;

const LISTING_DAYS = 60;

function listing_url(array $l): string
{
    return '/sublet/' . $l['city_slug'] . '-' . strtolower($l['state']) . '/' . $l['slug'] . '-' . $l['id'] . '/';
}

function listing_get(int $id): ?array
{
    return row('SELECT * FROM listings WHERE id = ?', [$id]);
}

function listing_photos(int $id): array
{
    return rows('SELECT id, width, height FROM photos WHERE listing_id = ? ORDER BY sort, id', [$id]);
}

function first_photo_ids(array $ids): array
{
    if (!$ids) return [];
    $in = implode(',', array_map('intval', $ids));
    $out = [];
    foreach (rows("SELECT listing_id, MIN(id) AS pid FROM photos WHERE listing_id IN ($in) GROUP BY listing_id") as $r) {
        $out[(int)$r['listing_id']] = (int)$r['pid'];
    }
    return $out;
}

function is_directory(array $l): bool
{
    return ($l['source'] ?? 'host') === 'directory';
}

function is_unclaimed(array $l): bool
{
    return is_directory($l) && empty($l['claimed_at']);
}

function is_verified(array $l): bool
{
    return $l['tier'] === 'paid';
}

/** Contact details are public only on paid listings whose owner verified their email. */
function contact_public(array $l): bool
{
    if ($l['tier'] !== 'paid' || !$l['owner_id']) return false;
    return (bool)val('SELECT email_verified_at FROM owners WHERE id = ?', [(int)$l['owner_id']]);
}

/**
 * Search active listings.
 * $f keys: state, city (slug), min, max, type, furnished, pets, from, to, summer, ids[], sort, q
 */
function listing_search(array $f, int $limit = 24, int $offset = 0): array
{
    $w = ["status = 'active'"];
    $p = [];
    if (!empty($f['ids'])) {
        $w = ["status IN ('active','rented')"];
        $w[] = 'id IN (' . implode(',', array_map('intval', $f['ids'])) . ')';
    }
    if (!empty($f['state'])) { $w[] = 'state = ?'; $p[] = strtoupper($f['state']); }
    if (!empty($f['city'])) { $w[] = 'city_slug = ?'; $p[] = $f['city']; }
    if (!empty($f['min'])) { $w[] = 'rent >= ?'; $p[] = (int)$f['min']; }
    if (!empty($f['max'])) { $w[] = 'rent <= ? AND rent > 0'; $p[] = (int)$f['max']; }
    if (!empty($f['source'])) { $w[] = 'source = ?'; $p[] = $f['source']; }
    // date-based filters only make sense for host listings with real dates
    if (!empty($f['from']) || !empty($f['to']) || !empty($f['summer'])) $w[] = "source = 'host'";
    if (!empty($f['type']) && isset(property_types()[$f['type']])) { $w[] = 'property_type = ?'; $p[] = $f['type']; }
    if (!empty($f['furnished'])) $w[] = 'furnished = 1';
    if (!empty($f['pets'])) $w[] = "pets IN ('cats','dogs','yes','ask')";
    if (!empty($f['verified'])) $w[] = "tier = 'paid'";
    if (!empty($f['from']) && preg_match('/^\d{4}-\d{2}-\d{2}$/', $f['from'])) {
        // listing must still be available on the renter's move-in date
        $w[] = '(available_to IS NULL OR available_to >= ?)'; $p[] = $f['from'];
        $w[] = '(available_from IS NULL OR available_from <= ?)'; $p[] = date('Y-m-d', strtotime($f['from'] . ' +21 days'));
    }
    if (!empty($f['to']) && preg_match('/^\d{4}-\d{2}-\d{2}$/', $f['to'])) {
        $w[] = '(available_to IS NULL OR available_to >= ?)'; $p[] = date('Y-m-d', strtotime($f['to'] . ' -14 days'));
    }
    if (!empty($f['summer'])) {
        // overlaps June–August of the current/next season
        $y = (int)date('Y'); if ((int)date('n') > 8) $y++;
        $w[] = '(available_from IS NULL OR available_from <= ?)'; $p[] = "$y-07-15";
        $w[] = '(available_to IS NULL OR available_to >= ?)'; $p[] = "$y-06-15";
        $w[] = 'min_stay <= 3';
    }
    if (!empty($f['q'])) {
        $w[] = '(title LIKE ? OR neighborhood LIKE ? OR city LIKE ?)';
        $like = '%' . $f['q'] . '%';
        array_push($p, $like, $like, $like);
    }
    $where = implode(' AND ', $w);
    $order = match ($f['sort'] ?? '') {
        'price_asc' => 'CASE WHEN rent = 0 THEN 1 ELSE 0 END, rent ASC',
        'price_desc' => 'rent DESC',
        'available' => 'available_from ASC',
        default => "CASE WHEN source = 'host' AND tier = 'paid' THEN 0 WHEN source = 'host' THEN 1 WHEN claimed_at IS NOT NULL THEN 2 ELSE 3 END, rank_score DESC, published_at DESC",
    };
    $total = (int)val("SELECT COUNT(*) FROM listings WHERE $where", $p);
    $items = rows("SELECT * FROM listings WHERE $where ORDER BY $order LIMIT " . (int)$limit . ' OFFSET ' . (int)$offset, $p);
    return ['total' => $total, 'items' => $items];
}

function listing_card_data(array $items): array
{
    $photos = first_photo_ids(array_column($items, 'id'));
    $types = property_types();
    return array_map(function ($l) use ($photos, $types) {
        return [
            'id' => (int)$l['id'],
            'title' => $l['title'],
            'url' => listing_url($l),
            'city' => $l['city'], 'state' => $l['state'], 'neighborhood' => $l['neighborhood'],
            'rent' => (int)$l['rent'],
            'type' => $types[$l['property_type']] ?? $l['property_type'],
            'furnished' => (bool)$l['furnished'],
            'beds' => $l['beds'], 'baths' => $l['baths'],
            'from' => $l['available_from'], 'to' => $l['available_to'],
            'from_h' => $l['available_from'] ? fmt_date($l['available_from'], 'M j') : 'Now',
            'to_h' => $l['available_to'] ? fmt_date($l['available_to'], 'M j, Y') : 'Flexible',
            'min_stay' => (int)$l['min_stay'],
            'pets' => $l['pets'],
            'utilities' => (bool)$l['utilities_included'],
            'verified' => $l['tier'] === 'paid',
            'directory' => ($l['source'] ?? 'host') === 'directory',
            'unclaimed' => ($l['source'] ?? 'host') === 'directory' && empty($l['claimed_at']),
            'status' => $l['status'],
            'photo' => isset($photos[$l['id']]) ? '/photo/' . $photos[$l['id']] . '.webp' : null,
            'lat' => $l['lat'] !== null ? (float)$l['lat'] : null,
            'lng' => $l['lng'] !== null ? (float)$l['lng'] : null,
        ];
    }, $items);
}

/** Server-rendered card (mirrors the JS renderer in site.js). */
function listing_card_html(array $c): string
{
    $img = $c['photo']
        ? '<img src="' . e($c['photo']) . '" alt="' . e($c['title']) . '" loading="lazy" width="480" height="320">'
        : placeholder_svg($c['type'], true);
    $badges = '';
    if ($c['verified']) $badges .= '<span class="badge badge-verified" title="Paid listing with a verified email">✔ Verified host</span>';
    if ($c['status'] === 'rented') $badges .= '<span class="badge badge-muted">Rented</span>';
    if (!empty($c['unclaimed'])) $badges .= '<span class="badge badge-glass">Property directory</span>';
    $meta = !empty($c['directory'])
        ? e($c['type']) . ($c['furnished'] ? ' · Furnished' : '')
        : e($c['type']) . ' · ' . ($c['furnished'] ? 'Furnished' : 'Unfurnished') . ' · ' . e($c['beds']) . ' bd / ' . e($c['baths']) . ' ba';
    $price = $c['rent'] > 0
        ? '<strong>' . money($c['rent']) . '</strong>/mo' . ($c['utilities'] ? ' <span class="muted">· utilities incl.</span>' : '')
        : '<strong class="rate-req">Rates on request</strong>';
    $dates = !empty($c['directory']) ? (!empty($c['unclaimed']) ? 'Owner? <span class="claim-link">Claim this listing →</span>' : 'Flexible stays — contact for availability') : e($c['from_h']) . ' → ' . e($c['to_h']);
    return '<article class="card" data-id="' . $c['id'] . '">'
        . '<a class="card-img" href="' . e($c['url']) . '">' . $img . '<span class="card-badges">' . $badges . '</span></a>'
        . '<button class="fav-btn" type="button" data-fav="' . $c['id'] . '" aria-label="Save to favorites" aria-pressed="false">♡</button>'
        . '<div class="card-body">'
        . '<p class="card-price">' . $price . '</p>'
        . '<h3 class="card-title"><a href="' . e($c['url']) . '">' . e($c['title']) . '</a></h3>'
        . '<p class="card-loc">' . e(($c['neighborhood'] ? $c['neighborhood'] . ', ' : '') . $c['city'] . ', ' . $c['state']) . '</p>'
        . '<p class="card-meta">' . $meta . '</p>'
        . '<p class="card-dates">' . $dates . '</p>'
        . '<label class="cmp"><input type="checkbox" data-compare="' . $c['id'] . '"> Compare</label>'
        . '</div></article>';
}

/** Friendly drawn placeholder when a listing has no photos. */
function placeholder_svg(string $type = '', bool $small = false): string
{
    $label = $small ? '' : '<text x="240" y="292" text-anchor="middle" font-family="system-ui,sans-serif" font-size="17" fill="#5b6b62">No photos yet</text>';
    return '<svg class="ph" viewBox="0 0 480 320" role="img" aria-label="Illustration: no photos yet" xmlns="http://www.w3.org/2000/svg">'
        . '<rect width="480" height="320" fill="#eef5f0"/>'
        . '<circle cx="390" cy="70" r="28" fill="#ffd27a"/>'
        . '<path d="M0 250 Q120 205 240 240 T480 225 V320 H0Z" fill="#cfe5d6"/>'
        . '<rect x="150" y="135" width="180" height="115" rx="6" fill="#ffffff" stroke="#2f6f4f" stroke-width="4"/>'
        . '<path d="M135 142 L240 70 L345 142" fill="none" stroke="#2f6f4f" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>'
        . '<rect x="222" y="190" width="36" height="60" rx="3" fill="#e46f4c"/>'
        . '<rect x="170" y="160" width="34" height="30" rx="3" fill="#bfe0f2" stroke="#2f6f4f" stroke-width="3"/>'
        . '<rect x="276" y="160" width="34" height="30" rx="3" fill="#bfe0f2" stroke="#2f6f4f" stroke-width="3"/>'
        . '<circle cx="250" cy="222" r="3" fill="#fff"/>'
        . $label . '</svg>';
}

/** Coarsen coordinates so the exact address is never public (~400–800 m jitter, stable per listing). */
function approx_coords(?float $lat, ?float $lng, int $seed): array
{
    if ($lat === null || $lng === null || abs($lat) > 90 || abs($lng) > 180) return [null, null];
    mt_srand($seed * 7919);
    $dLat = (mt_rand(-1000, 1000) / 1000) * 0.0045;
    $dLng = (mt_rand(-1000, 1000) / 1000) * 0.0055;
    mt_srand();
    return [round(round($lat, 3) + $dLat, 4), round(round($lng, 3) + $dLng, 4)];
}

/** Expiry: the earlier of available_to (end of day) and published + 60 days. */
function compute_expiry(?string $availableTo, ?string $from = null): string
{
    $base = $from ? strtotime($from) : time();
    $exp = $base + LISTING_DAYS * 86400;
    if ($availableTo && ($t = strtotime($availableTo . ' 23:59:59')) && $t > time()) $exp = min($exp, $t);
    return gmdate('Y-m-d H:i:s', $exp);
}

function publish_listing(int $id): void
{
    $l = listing_get($id);
    if (!$l) return;
    update('listings', [
        'status' => 'active',
        'published_at' => $l['published_at'] ?: now(),
        'expires_at' => compute_expiry($l['available_to']),
        'reminder_sent_at' => null,
        'updated_at' => now(),
    ], 'id = ?', [$id]);
}

/** Validate & normalise listing form input. Returns [data, errors]. */
function listing_from_input(array $in, bool $requireContact = true, bool $directory = false): array
{
    $err = [];
    $s = fn($k, $max) => mb_substr(trim((string)($in[$k] ?? '')), 0, $max);
    $d = [];
    $d['title'] = $s('title', 120);
    if (mb_strlen($d['title']) < 8) $err['title'] = 'Add a descriptive title (at least 8 characters).';
    $d['description'] = $s('description', 6000);
    if (mb_strlen($d['description']) < 60) $err['description'] = 'Describe the place in at least 60 characters.';
    $d['city'] = $s('city', 80);
    $d['city'] = preg_replace('/\s+/', ' ', ucwords(strtolower($d['city'])));
    if (mb_strlen($d['city']) < 2) $err['city'] = 'Enter the city.';
    $d['state'] = strtoupper($s('state', 2));
    if (!isset(states()[$d['state']])) $err['state'] = 'Choose a state.';
    $d['city_slug'] = slugify($d['city'], 60);
    $d['zip'] = preg_replace('/[^0-9]/', '', $s('zip', 10));
    if ($d['zip'] !== '' && strlen($d['zip']) !== 5) $err['zip'] = 'ZIP should be 5 digits.';
    $d['neighborhood'] = $s('neighborhood', 80);
    $d['property_type'] = $s('property_type', 20);
    if (!isset(property_types()[$d['property_type']])) $err['property_type'] = 'Choose a property type.';
    $d['furnished'] = !empty($in['furnished']) && $in['furnished'] !== '0' ? 1 : 0;
    $d['rent'] = (int)preg_replace('/[^0-9]/', '', (string)($in['rent'] ?? ''));
    if (!($directory && $d['rent'] === 0) && ($d['rent'] < 100 || $d['rent'] > 50000)) $err['rent'] = 'Monthly rent should be between $100 and $50,000' . ($directory ? ' (or 0 for “rates on request”).' : '.');
    $d['deposit'] = min(100000, (int)preg_replace('/[^0-9]/', '', (string)($in['deposit'] ?? '')));
    $d['utilities_included'] = !empty($in['utilities_included']) ? 1 : 0;
    foreach (['available_from', 'available_to'] as $k) {
        $v = $s($k, 10);
        $d[$k] = preg_match('/^\d{4}-\d{2}-\d{2}$/', $v) && strtotime($v) ? $v : null;
    }
    if (!$d['available_from'] && !$directory) $err['available_from'] = 'Choose the date it becomes available.';
    if ($d['available_to'] && $d['available_from'] && $d['available_to'] <= $d['available_from']) $err['available_to'] = 'The end date must be after the start date.';
    if ($d['available_to'] && $d['available_to'] < date('Y-m-d')) $err['available_to'] = 'The end date is in the past.';
    $d['min_stay'] = max(1, min(12, (int)($in['min_stay'] ?? 1)));
    $d['beds'] = in_array($in['beds'] ?? '', ['studio', '1', '2', '3', '4', '5+'], true) ? $in['beds'] : '1';
    $d['baths'] = in_array($in['baths'] ?? '', ['shared', '1', '1.5', '2', '2.5', '3+'], true) ? $in['baths'] : '1';
    $am = array_values(array_intersect((array)($in['amenities'] ?? []), array_keys(amenity_options())));
    $d['amenities'] = implode(',', $am);
    $d['house_rules'] = $s('house_rules', 2000);
    $d['pets'] = isset(pet_options()[$in['pets'] ?? '']) ? $in['pets'] : 'no';
    $lat = isset($in['lat']) && is_numeric($in['lat']) ? (float)$in['lat'] : null;
    $lng = isset($in['lng']) && is_numeric($in['lng']) ? (float)$in['lng'] : null;
    // keep within the US-ish bounding box
    if ($lat !== null && ($lat < 17 || $lat > 72 || $lng > -64 || $lng < -180)) { $lat = $lng = null; }
    $d['_lat'] = $lat; $d['_lng'] = $lng;
    $d['contact_name'] = $s('contact_name', 120);
    $d['contact_email'] = strtolower($s('contact_email', 190));
    $d['contact_phone'] = preg_replace('/[^0-9+()\-. ]/', '', $s('contact_phone', 40));
    if ($requireContact) {
        if (mb_strlen($d['contact_name']) < 2) $err['contact_name'] = 'Enter your name.';
        if (!valid_email($d['contact_email'])) $err['contact_email'] = 'Enter a valid email address.';
    }
    // simple spam heuristics
    if (preg_match_all('#https?://#i', $d['description']) > 2) $err['description'] = 'Please remove links from the description.';
    if (preg_match('/western union|moneygram|wire (the )?(money|transfer)|gift ?card|bitcoin|zelle only/i', $d['description'] . ' ' . $d['house_rules'])) {
        $err['description'] = 'For renter safety, listings can’t ask for wires, gift cards or crypto.';
    }
    return [$d, $err];
}

/** Fill lat/lng: owner pin (coarsened) or city guide center. */
function resolve_coords(array &$d, int $seed): void
{
    $lat = $d['_lat'] ?? null; $lng = $d['_lng'] ?? null;
    unset($d['_lat'], $d['_lng']);
    if ($lat === null) {
        $g = city_guide($d['state'], $d['city_slug']);
        if ($g) { $lat = (float)$g['lat']; $lng = (float)$g['lng']; }
    }
    [$d['lat'], $d['lng']] = approx_coords($lat, $lng, $seed);
}

function listing_status_label(string $s): string
{
    return [
        'pending' => 'Awaiting review', 'pending_payment' => 'Awaiting payment', 'active' => 'Live',
        'rejected' => 'Not approved', 'rented' => 'Rented', 'unavailable' => 'Unavailable', 'expired' => 'Expired',
    ][$s] ?? ucfirst($s);
}

function renew_link(array $l): string
{
    return base_url('/renew/' . $l['id'] . '/?t=' . sign('renew:' . $l['id'] . ':' . $l['contact_email']));
}

function upgrade_link(array $l): string
{
    return base_url('/upgrade/' . $l['id'] . '/?t=' . sign('upgrade:' . $l['id'] . ':' . $l['contact_email']));
}

/** Expire listings and send reminders. Runs from cron and opportunistically (once an hour). */
function run_expiry_jobs(): array
{
    $now = now();
    $expired = q("UPDATE listings SET status = 'expired', updated_at = ? WHERE status = 'active' AND expires_at IS NOT NULL AND expires_at < ?", [$now, $now])->rowCount();
    $soon = gmdate('Y-m-d H:i:s', time() + 5 * 86400);
    $sent = 0;
    foreach (rows("SELECT * FROM listings WHERE status = 'active' AND expires_at IS NOT NULL AND expires_at < ? AND reminder_sent_at IS NULL LIMIT 25", [$soon]) as $l) {
        if (!valid_email((string)$l['contact_email'])) { update('listings', ['reminder_sent_at' => $now], 'id = ?', [(int)$l['id']]); continue; }
        $body = view('emails/expiry', ['l' => $l]);
        send_mail($l['contact_email'], 'Your sublet listing expires soon: ' . $l['title'], $body);
        update('listings', ['reminder_sent_at' => $now], 'id = ?', [(int)$l['id']]);
        $sent++;
    }
    q('DELETE FROM login_tokens WHERE expires_at < ?', [gmdate('Y-m-d H:i:s', time() - 86400)]);
    setting_set('last_cron', (string)time());
    return ['expired' => $expired, 'reminders' => $sent];
}

function maybe_run_cron(): void
{
    if ((int)setting('last_cron', 0) < time() - 3600) {
        try { run_expiry_jobs(); } catch (Throwable $e) { error_log('[cron] ' . $e->getMessage()); }
    }
}

/** Import claimable directory entries (from dev/directory/directory.json). Skips refs already present. */
function import_directory(array $rows): array
{
    $guides = city_content();
    $added = 0; $skipped = 0;
    foreach ($rows as $r) {
        $key = $r['key'] ?? '';
        if (!isset($guides[$key]) || empty($r['ref'])) { $skipped++; continue; }
        if (val('SELECT id FROM listings WHERE place_ref = ?', [(string)$r['ref']])) { $skipped++; continue; }
        $g = $guides[$key];
        [$st, $slug] = explode('/', $key);
        $now = now();
        insert('listings', [
            'source' => 'directory', 'slug' => slugify($r['title'], 60), 'title' => mb_substr($r['title'], 0, 140),
            'business_name' => mb_substr($r['title'], 0, 160), 'description' => '',
            'city' => $g['name'], 'city_slug' => $slug, 'state' => strtoupper($st), 'zip' => (string)($r['zip'] ?? ''),
            'neighborhood' => mb_substr((string)($r['borough'] ?? ''), 0, 80),
            'address_line' => mb_substr((string)($r['address'] ?? ''), 0, 190), 'address_city' => mb_substr((string)($r['address_city'] ?? ''), 0, 80),
            'website' => mb_substr((string)($r['url'] ?? ''), 0, 300), 'phone_public' => mb_substr((string)($r['phone'] ?? ''), 0, 40),
            'category' => mb_substr((string)($r['category'] ?? ''), 0, 80), 'place_ref' => mb_substr((string)$r['ref'], 0, 64),
            'rank_score' => (int)($r['score'] ?? 0),
            'property_type' => $r['ptype'] ?? 'furnished_community', 'furnished' => (int)($r['furnished'] ?? 1),
            'rent' => 0, 'deposit' => 0, 'min_stay' => 1, 'beds' => '1', 'baths' => '1',
            'amenities' => implode(',', array_intersect((array)($r['amenities'] ?? []), array_keys(amenity_options()))),
            'house_rules' => '', 'pets' => in_array($r['pets'] ?? 'ask', ['yes', 'ask'], true) ? $r['pets'] : 'ask',
            'lat' => isset($r['lat']) ? round((float)$r['lat'], 5) : null, 'lng' => isset($r['lng']) ? round((float)$r['lng'], 5) : null,
            'contact_name' => '', 'contact_email' => '', 'contact_phone' => '',
            'tier' => 'free', 'status' => 'active', 'published_at' => $now, 'created_at' => $now, 'updated_at' => $now,
        ]);
        $added++;
    }
    return ['added' => $added, 'skipped' => $skipped];
}
