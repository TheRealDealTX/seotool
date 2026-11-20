<?php defined('WCA') || exit;

const LISTING_FIELDS = ['slug', 'name', 'status', 'type', 'address', 'city', 'state', 'zip', 'lat', 'lng', 'phone', 'email', 'website',
    'office_hours', 'beds_min', 'beds_max', 'baths', 'rent_min', 'rent_max', 'sqft_min', 'sqft_max', 'year_built', 'units', 'cats', 'dogs',
    'pet_notes', 'income_restricted', 'age_restriction', 'amenities', 'description', 'photos', 'owner_id', 'contact_visible', 'featured',
    'source', 'submitter_name', 'submitter_email'];

const LISTING_TYPES = ['apartment' => 'Apartments', 'townhome' => 'Townhomes', 'senior' => 'Senior Living', 'duplex' => 'Duplex / Small Building'];

function listing_insert(PDO $pdo, array $l, bool $exactSlug = false): int
{
    $l['slug'] = $exactSlug ? $l['slug'] : unique_slug($pdo, $l['slug'] ?? slugify($l['name']));
    foreach (['amenities', 'photos'] as $j) if (isset($l[$j]) && is_array($l[$j])) $l[$j] = json_encode(array_values($l[$j]));
    $cols = array_values(array_intersect(LISTING_FIELDS, array_keys($l)));
    $vals = array_map(fn($c) => $l[$c], $cols);
    $cols[] = 'created_at'; $vals[] = $l['created_at'] ?? now();
    $cols[] = 'updated_at'; $vals[] = now();
    $pdo->prepare('INSERT INTO listings (' . implode(',', $cols) . ') VALUES (' . implode(',', array_fill(0, count($cols), '?')) . ')')->execute($vals);
    return (int)$pdo->lastInsertId();
}

function listing_update(int $id, array $l): void
{
    foreach (['amenities', 'photos'] as $j) if (isset($l[$j]) && is_array($l[$j])) $l[$j] = json_encode(array_values($l[$j]));
    $cols = array_values(array_intersect(LISTING_FIELDS, array_keys($l)));
    if (!$cols) return;
    $set = implode(',', array_map(fn($c) => "$c = ?", $cols));
    $vals = array_map(fn($c) => $l[$c], $cols);
    $vals[] = now(); $vals[] = $id;
    db()->prepare("UPDATE listings SET $set, updated_at = ? WHERE id = ?")->execute($vals);
}

function unique_slug(PDO $pdo, string $slug, int $ignoreId = 0): string
{
    $base = slugify($slug); $s = $base; $i = 2;
    $st = $pdo->prepare('SELECT id FROM listings WHERE slug = ? AND id <> ?');
    while (true) {
        $st->execute([$s, $ignoreId]);
        if (!$st->fetchColumn()) return $s;
        $s = $base . '-' . $i++;
    }
}

function listing_hydrate(array $l): array
{
    $l['amenities'] = json_decode($l['amenities'] ?? '[]', true) ?: [];
    $l['photos'] = json_decode($l['photos'] ?? '[]', true) ?: [];
    $l['has_photos'] = (bool)$l['photos'];
    if (!$l['photos']) $l['photos'] = default_photos((int)$l['id']);
    $l['url'] = '/apartments/' . $l['slug'] . '/';
    $l['claimed'] = !empty($l['owner_id']);
    $l['show_contact'] = !empty($l['contact_visible']) && !empty($l['owner_id']);
    return $l;
}

/** Placeholder illustration, varied per listing. */
function default_photos(int $id): array
{
    return ['placeholder-' . (($id % 4) + 1)]; // illustration until the owner adds real photos
}

function listing_by_id(int $id): ?array
{
    $st = db()->prepare('SELECT * FROM listings WHERE id = ?');
    $st->execute([$id]);
    $r = $st->fetch();
    return $r ? listing_hydrate($r) : null;
}

function listing_by_slug(string $slug): ?array
{
    $st = db()->prepare('SELECT * FROM listings WHERE slug = ?');
    $st->execute([$slug]);
    $r = $st->fetch();
    return $r ? listing_hydrate($r) : null;
}

function listings_published(): array
{
    static $all = null;
    if ($all !== null) return $all;
    $rows = db()->query("SELECT * FROM listings WHERE status = 'published' ORDER BY featured DESC, (owner_id IS NOT NULL) DESC, name ASC")->fetchAll();
    return $all = array_map('listing_hydrate', $rows);
}

function listings_by_owner(int $uid): array
{
    $st = db()->prepare('SELECT * FROM listings WHERE owner_id = ? ORDER BY name');
    $st->execute([$uid]);
    return array_map('listing_hydrate', $st->fetchAll());
}

function beds_label(array $l): string
{
    $a = $l['beds_min']; $b = $l['beds_max'];
    if ($a === null && $b === null) return 'Call for floor plans';
    $f = fn($n) => (int)$n === 0 ? 'Studio' : (int)$n;
    if ($a === null || (int)$a === (int)$b) return $f($b ?? $a) . ((int)($b ?? $a) === 0 ? '' : ' Bed');
    return $f($a) . '–' . (int)$b . ' Beds';
}

function rent_label(array $l): string
{
    if (!$l['rent_min'] && !$l['rent_max']) return 'Contact for pricing';
    if (!$l['rent_max'] || $l['rent_min'] == $l['rent_max']) return money($l['rent_min'] ?: $l['rent_max']) . '/mo';
    if (!$l['rent_min']) return 'Up to ' . money($l['rent_max']) . '/mo';
    return money($l['rent_min']) . '–' . money($l['rent_max']) . '/mo';
}

function sqft_label(array $l): string
{
    if (!$l['sqft_min'] && !$l['sqft_max']) return '';
    if (!$l['sqft_max'] || $l['sqft_min'] == $l['sqft_max']) return number_format($l['sqft_min'] ?: $l['sqft_max']) . ' sq ft';
    return number_format($l['sqft_min']) . '–' . number_format($l['sqft_max']) . ' sq ft';
}

function pets_label(array $l): string
{
    if ($l['cats'] === null && $l['dogs'] === null) return 'Ask about pets';
    if ($l['cats'] && $l['dogs']) return 'Cats & dogs OK';
    if ($l['cats']) return 'Cats OK';
    if ($l['dogs']) return 'Dogs OK';
    return 'No pets';
}

function is_pet_friendly(array $l): bool
{
    return !empty($l['cats']) || !empty($l['dogs']);
}

/** Compact JSON used by the client-side directory filters + map. Never includes contact details. */
function listing_public_json(array $l): array
{
    return [
        'id' => (int)$l['id'], 'name' => $l['name'], 'url' => $l['url'], 'type' => $l['type'], 'city' => $l['city'],
        'address' => $l['address'] . ', ' . $l['city'] . ', ' . $l['state'] . ' ' . $l['zip'],
        'lat' => $l['lat'] !== null ? (float)$l['lat'] : null, 'lng' => $l['lng'] !== null ? (float)$l['lng'] : null,
        'bmin' => $l['beds_min'] !== null ? (int)$l['beds_min'] : null, 'bmax' => $l['beds_max'] !== null ? (int)$l['beds_max'] : null,
        'rmin' => $l['rent_min'] ? (int)$l['rent_min'] : null, 'rmax' => $l['rent_max'] ? (int)$l['rent_max'] : null,
        'beds' => beds_label($l), 'rent' => rent_label($l), 'pets' => is_pet_friendly($l), 'petsLabel' => pets_label($l),
        'cats' => $l['cats'] === null ? null : (bool)$l['cats'], 'dogs' => $l['dogs'] === null ? null : (bool)$l['dogs'],
        'img' => photo_url($l['photos'][0], true), 'claimed' => $l['claimed'], 'featured' => (bool)$l['featured'],
        'income' => (bool)$l['income_restricted'], 'age' => $l['age_restriction'],
        'sqft' => sqft_label($l), 'year' => $l['year_built'] ? (int)$l['year_built'] : null,
        'amen' => array_slice($l['amenities'], 0, 30),
    ];
}

/* ---------- Landing pages (SEO filtered directory views) ---------- */

function landing_pages(): array
{
    return [
        'pet-friendly' => [
            'h1' => 'Pet-Friendly Apartments in West Carrollton, OH',
            'title' => 'Pet-Friendly Apartments in West Carrollton, OH',
            'desc' => 'Browse pet-friendly apartments and townhomes in West Carrollton, Ohio that welcome cats and dogs. Compare pet policies, rent and amenities.',
            'intro' => 'Bringing a cat or dog? These West Carrollton communities have told renters they accept pets. Policies change, so always confirm pet rent, deposits, weight limits and breed rules before you apply. Wilson Park and the Great Miami River Trail make West Carrollton an easy place to walk a dog.',
            'filter' => fn($l) => is_pet_friendly($l),
        ],
        'under-1000' => [
            'h1' => 'Apartments Under $1,000 in West Carrollton, OH',
            'title' => 'Cheap Apartments Under $1,000 in West Carrollton, OH',
            'desc' => 'Find affordable apartments under $1,000 a month in West Carrollton, Ohio. Compare starting rents, floor plans and amenities in one place.',
            'intro' => 'West Carrollton is one of the more affordable suburbs in the Dayton area. These communities have advertised at least one floor plan starting under $1,000 per month. Rents move with availability, so treat these as starting points and use our <a href="/tools/rent-affordability-calculator/">rent affordability calculator</a> to find your budget.',
            'filter' => fn($l) => $l['rent_min'] && $l['rent_min'] < 1000,
        ],
        'studios' => [
            'h1' => 'Studio Apartments in West Carrollton, OH',
            'title' => 'Studio Apartments for Rent in West Carrollton, OH',
            'desc' => 'Studio and efficiency apartments for rent in West Carrollton, Ohio. Compare rent, square footage and amenities.',
            'intro' => 'Studios keep rent and utility bills low and are a good fit if you are close to work in Dayton, Moraine or Miamisburg. These communities list studio or efficiency floor plans.',
            'filter' => fn($l) => $l['beds_min'] !== null && (int)$l['beds_min'] === 0,
        ],
        '1-bedroom' => [
            'h1' => '1-Bedroom Apartments in West Carrollton, OH',
            'title' => '1 Bedroom Apartments for Rent in West Carrollton, OH',
            'desc' => 'Compare 1-bedroom apartments in West Carrollton, Ohio: rent ranges, square footage, pet policies and amenities.',
            'intro' => 'One-bedroom apartments are the most common floor plan in West Carrollton. These communities offer at least one 1-bedroom layout.',
            'filter' => fn($l) => ($l['beds_min'] ?? 9) <= 1 && ($l['beds_max'] ?? -1) >= 1,
        ],
        '2-bedroom' => [
            'h1' => '2-Bedroom Apartments in West Carrollton, OH',
            'title' => '2 Bedroom Apartments for Rent in West Carrollton, OH',
            'desc' => 'Find 2-bedroom apartments and townhomes for rent in West Carrollton, Ohio. Compare rent, size, pets and amenities.',
            'intro' => 'Need room for a roommate, a home office or a growing family? These West Carrollton communities offer 2-bedroom floor plans. Splitting rent? Try the <a href="/tools/roommate-rent-splitter/">roommate rent splitter</a>.',
            'filter' => fn($l) => ($l['beds_min'] ?? 9) <= 2 && ($l['beds_max'] ?? -1) >= 2,
        ],
        '3-bedroom' => [
            'h1' => '3-Bedroom Apartments & Townhomes in West Carrollton, OH',
            'title' => '3 Bedroom Apartments & Townhomes in West Carrollton, OH',
            'desc' => '3-bedroom apartments and townhomes for rent in West Carrollton, Ohio, near West Carrollton City Schools, parks and I-75.',
            'intro' => 'Larger households have options in West Carrollton, including townhome-style communities. These listings include at least one 3-bedroom floor plan.',
            'filter' => fn($l) => ($l['beds_max'] ?? 0) >= 3,
        ],
        'townhomes' => [
            'h1' => 'Townhomes for Rent in West Carrollton, OH',
            'title' => 'Townhomes for Rent in West Carrollton, OH',
            'desc' => 'Rent a townhome in West Carrollton, Ohio. Compare townhome communities, floor plans, garages and pet policies.',
            'intro' => 'Townhomes give you more privacy, often a private entrance and sometimes a garage. These communities are townhome-style or include townhome floor plans.',
            'filter' => fn($l) => $l['type'] === 'townhome' || preg_match('/townhome/i', implode(' ', $l['amenities']) . ' ' . $l['description']),
        ],
        'senior' => [
            'h1' => 'Senior Apartments in West Carrollton, OH',
            'title' => 'Senior & 55+ Apartments in West Carrollton, OH',
            'desc' => 'Senior and 55+ apartment communities in and near West Carrollton, Ohio, including income-based options.',
            'intro' => 'These communities are age-restricted (55+ or 62+). Several are income-based, so ask about eligibility and waiting lists. The West Carrollton Senior Center is part of the Civic Center complex on South Elm Street.',
            'filter' => fn($l) => $l['type'] === 'senior' || !empty($l['age_restriction']),
        ],
        'income-based' => [
            'h1' => 'Income-Based & Affordable Housing in West Carrollton, OH',
            'title' => 'Income-Based Apartments in West Carrollton, OH',
            'desc' => 'Income-restricted, tax-credit and HUD-assisted apartments in and near West Carrollton, Ohio.',
            'intro' => 'These communities participate in affordable housing programs such as tax credits or HUD assistance. Income limits apply and waiting lists are common, so contact the property early.',
            'filter' => fn($l) => !empty($l['income_restricted']),
        ],
    ];
}

/* ---------- Amazon product sets ---------- */

function amazon_products_for_listing(array $l): array
{
    $base = [
        ['name' => 'Moving boxes kit with tape', 'query' => 'moving boxes kit with packing tape', 'icon' => '📦', 'why' => 'Everything you need to pack for moving day.'],
        ['name' => 'Renter-friendly tool kit', 'query' => 'home tool kit apartment', 'icon' => '🧰', 'why' => 'Assemble furniture and hang curtains on day one.'],
        ['name' => 'Command damage-free hooks', 'query' => 'command damage free hanging strips', 'icon' => '🖼️', 'why' => 'Decorate without losing your security deposit.'],
        ['name' => 'Smart plug 4-pack', 'query' => 'smart plug 4 pack', 'icon' => '🔌', 'why' => 'Automate lamps and cut phantom power use.'],
        ['name' => 'Blackout curtains', 'query' => 'thermal blackout curtains', 'icon' => '🪟', 'why' => 'Block drafts in Ohio winters and heat in summer.'],
        ['name' => 'Air purifier', 'query' => 'hepa air purifier for bedroom', 'icon' => '🌬️', 'why' => 'Cleaner air in a smaller space.'],
        ['name' => 'Over-the-door organizer', 'query' => 'over the door organizer', 'icon' => '🚪', 'why' => 'Instant storage for closets and pantries.'],
        ['name' => 'Shower caddy & bath set', 'query' => 'apartment bathroom accessories set', 'icon' => '🛁', 'why' => 'Set up your bathroom in minutes.'],
    ];
    $pets = [
        ['name' => 'Washable pet bed', 'query' => 'washable dog bed', 'icon' => '🐶', 'why' => 'A cozy spot that keeps fur off the sofa.'],
        ['name' => 'Pet hair vacuum', 'query' => 'cordless vacuum pet hair', 'icon' => '🧹', 'why' => 'Keep carpet move-out ready.'],
        ['name' => 'Enzyme stain remover', 'query' => 'enzyme pet stain odor remover', 'icon' => '🧴', 'why' => 'Lifts accidents before they cost you.'],
    ];
    $senior = [
        ['name' => 'Shower grab bar (suction)', 'query' => 'suction shower grab bar', 'icon' => '🛁', 'why' => 'Extra stability without drilling.'],
        ['name' => 'Motion-sensor night lights', 'query' => 'motion sensor night light plug in', 'icon' => '💡', 'why' => 'Safer late-night trips down the hall.'],
    ];
    $set = $base;
    if (is_pet_friendly($l)) $set = array_merge($pets, $set);
    if ($l['type'] === 'senior' || $l['age_restriction']) $set = array_merge($senior, $set);
    // rotate a little per listing for variety
    $off = ((int)$l['id']) % 3;
    $set = array_merge(array_slice($set, 0, 3), array_slice(array_slice($set, 3), $off), array_slice(array_slice($set, 3), 0, $off));
    return array_slice($set, 0, 8);
}

/** Save an uploaded image (re-encoded to WebP via GD). Returns public path or null. */
function save_uploaded_photo(array $file): ?string
{
    if (($file['error'] ?? 1) !== UPLOAD_ERR_OK || $file['size'] > 6 * 1024 * 1024) return null;
    return save_photo_file($file['tmp_name']);
}

/** Download an image from a URL (admin import) and store it like an upload. */
function import_photo_url(string $url): ?string
{
    if (!preg_match('#^https?://#i', $url)) return null;
    $tmp = tempnam(sys_get_temp_dir(), 'wcaimg');
    $fh = fopen($tmp, 'wb');
    $ch = curl_init($url);
    curl_setopt_array($ch, [CURLOPT_FILE => $fh, CURLOPT_FOLLOWLOCATION => true, CURLOPT_MAXREDIRS => 3, CURLOPT_TIMEOUT => 20,
        CURLOPT_USERAGENT => 'Mozilla/5.0 (compatible; WestCarrolltonApartments/1.0)', CURLOPT_PROTOCOLS => CURLPROTO_HTTP | CURLPROTO_HTTPS,
        CURLOPT_NOPROGRESS => false, CURLOPT_PROGRESSFUNCTION => fn($c, $dt, $d) => $d > 12 * 1024 * 1024 ? 1 : 0]);
    $ok = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    fclose($fh);
    $path = ($ok && $code < 400) ? save_photo_file($tmp) : null;
    @unlink($tmp);
    return $path;
}

function save_photo_file(string $tmp): ?string
{
    $info = @getimagesize($tmp);
    if (!$info || !in_array($info[2], [IMAGETYPE_JPEG, IMAGETYPE_PNG, IMAGETYPE_WEBP], true)) return null;
    $src = match ($info[2]) {
        IMAGETYPE_JPEG => @imagecreatefromjpeg($tmp),
        IMAGETYPE_PNG => @imagecreatefrompng($tmp),
        IMAGETYPE_WEBP => @imagecreatefromwebp($tmp),
    };
    if (!$src) return null;
    $w = imagesx($src); $h = imagesy($src);
    $max = 1600;
    if ($w > $max) {
        $nh = (int)round($h * $max / $w);
        $dst = imagecreatetruecolor($max, $nh);
        imagecopyresampled($dst, $src, 0, 0, 0, 0, $max, $nh, $w, $h);
        imagedestroy($src);
        $src = $dst;
    }
    $dir = ROOT_DIR . '/uploads/' . date('Y/m');
    if (!is_dir($dir)) mkdir($dir, 0755, true);
    $name = bin2hex(random_bytes(10)) . '.webp';
    imagewebp($src, "$dir/$name", 80);
    imagedestroy($src);
    return '/uploads/' . date('Y/m') . '/' . $name;
}

/** Shared validation for listing forms (owner, admin, submit). Returns [data, errors]. */
function listing_from_post(bool $admin = false): array
{
    $err = [];
    $int = fn($k) => ($v = preg_replace('/[^0-9]/', '', post($k))) === '' ? null : (int)$v;
    $tri = fn($k) => post($k) === '' ? null : (int)(post($k) === '1');
    $d = [
        'name' => mb_substr(post('name'), 0, 160),
        'type' => array_key_exists(post('type'), LISTING_TYPES) ? post('type') : 'apartment',
        'address' => mb_substr(post('address'), 0, 190),
        'city' => mb_substr(post('city', 'West Carrollton') ?: 'West Carrollton', 0, 80),
        'state' => 'OH',
        'zip' => mb_substr(preg_replace('/[^0-9-]/', '', post('zip')), 0, 10),
        'phone' => mb_substr(post('phone'), 0, 60) ?: null,
        'email' => valid_email(post('email')) ? post('email') : null,
        'website' => filter_var(post('website'), FILTER_VALIDATE_URL) && preg_match('#^https?://#i', post('website')) ? post('website') : null,
        'office_hours' => mb_substr(post('office_hours'), 0, 190) ?: null,
        'beds_min' => $int('beds_min'), 'beds_max' => $int('beds_max'),
        'baths' => mb_substr(post('baths'), 0, 20) ?: null,
        'rent_min' => $int('rent_min'), 'rent_max' => $int('rent_max'),
        'sqft_min' => $int('sqft_min'), 'sqft_max' => $int('sqft_max'),
        'year_built' => $int('year_built'), 'units' => $int('units'),
        'cats' => $tri('cats'), 'dogs' => $tri('dogs'),
        'pet_notes' => mb_substr(post('pet_notes'), 0, 255) ?: null,
        'income_restricted' => post('income_restricted') ? 1 : 0,
        'age_restriction' => in_array(post('age_restriction'), ['55+', '62+'], true) ? post('age_restriction') : null,
        'description' => mb_substr(strip_tags(post('description')), 0, 5000),
        'amenities' => array_values(array_filter(array_map(fn($a) => mb_substr(trim(strip_tags($a)), 0, 60), preg_split('/[\r\n,]+/', post('amenities'))))),
    ];
    if ($d['beds_max'] === null) $d['beds_max'] = $d['beds_min'];
    if (mb_strlen($d['name']) < 3) $err[] = 'Please enter the property name.';
    if (mb_strlen($d['address']) < 5) $err[] = 'Please enter the street address.';
    if (mb_strlen($d['description']) < 40) $err[] = 'Please add a description of at least 40 characters.';
    return [$d, $err];
}

/** Approximate geocode via OpenStreetMap Nominatim (used when a new listing has no coordinates). */
function geocode(string $address): ?array
{
    $ch = curl_init('https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=us&q=' . rawurlencode($address));
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 8, CURLOPT_USERAGENT => 'WestCarrolltonApartmentsDirectory/1.0']);
    $r = json_decode((string)curl_exec($ch), true);
    curl_close($ch);
    if (!empty($r[0]['lat'])) return [(float)$r[0]['lat'], (float)$r[0]['lon']];
    return null;
}
