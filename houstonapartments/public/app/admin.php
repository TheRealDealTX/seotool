<?php
// Admin panel: /admin/… (listings, leads, users, Rise import).
defined('HA_ROOT') || exit;

// An imported listing auto-publishes once less than this share of its About text matches the Rise original
const ADMIN_REWRITE_MAX_OVERLAP = 0.4;
require_once HA_APP . '/lib/Auth.php';
require_once HA_APP . '/lib/Images.php';
require_once HA_APP . '/lib/Rise.php';

const ADMIN_UNIT_AMENITIES = ['Air Conditioning', 'Balcony', 'Patio', 'Ceiling Fans', 'Dishwasher', 'Disposal', 'Fireplace', 'Hardwood Floor',
    'Vinyl Floor', 'Tile Floor', 'Carpet', 'Kitchen Island', 'Microwave', 'Pantry', 'Refrigerator', 'Stainless Steel Appliances',
    'Granite Countertops', 'Quartz Countertops', 'Walk-in Closet', 'Washer/Dryer', 'Washer/Dryer Hookups', 'High Ceilings', 'Smart Home', 'Wet Bar'];
const ADMIN_COMMUNITY_AMENITIES = ['Pool', 'Fitness Center', 'Clubhouse', 'Business Center', 'Controlled Access', 'Courtyard', 'Elevator',
    'Package Service', 'Pet Grooming Station', 'Dog Park', 'Spa', 'Sauna', 'Concierge', 'Maintenance on site', 'Property Manager on Site',
    'Bicycle Storage', 'Garage Parking', 'Covered Parking', 'EV Charging', 'Grill Area', 'Playground', 'Tennis Court', 'Rooftop Deck',
    'WiFi', 'Valet Trash', 'Laundry'];
const LEAD_STATUSES = ['new' => 'New', 'contacted' => 'Contacted', 'touring' => 'Touring', 'leased' => 'Leased', 'closed' => 'Closed'];

function admin_route(string $path): void
{
    header('X-Robots-Tag: noindex, nofollow');
    header('Cache-Control: no-store');
    db_migrate();
    $method = $_SERVER['REQUEST_METHOD'];
    $sub = substr($path, strlen('/admin'));

    // Machine endpoint (key-protected) kept for scripted imports
    if ($sub === '/sync/') {
        admin_key_sync();
        return;
    }
    if ($sub === '/test-mail/') {
        $key = config('admin_key');
        if (!$key || !hash_equals($key, (string) ($_GET['key'] ?? ''))) {
            http_response_code(404);
            exit('Not found');
        }
        $ok = lead_email(config('lead_email'), ['name' => 'Delivery test – please ignore', 'phone' => '+1 (713) 867-5309', 'email' => SITE['email'],
            'move_in' => '', 'beds' => '', 'budget' => '', 'message' => 'Test message sent ' . date('c') . ' to confirm lead emails arrive.', 'page' => '/']);
        json_out(['sent' => $ok, 'to' => config('lead_email'), 'via' => config('smtp_pass') ? 'smtp' : 'mail()']);
        return;
    }
    if ($sub === '/setup/') {
        admin_setup();
        return;
    }
    if ($sub === '/login/') {
        admin_login();
        return;
    }
    $user = Auth::user();
    if (!$user) {
        redirect('/admin/login/' . ($sub !== '/' && $sub !== '' ? '?next=' . rawurlencode($path) : ''), 302);
    }
    if ($method === 'POST') {
        Auth::checkCsrf();
    }

    $routes = [
        '#^/?$#'                        => fn () => admin_dashboard(),
        '#^/logout/$#'                  => fn () => admin_logout(),
        '#^/listings/$#'                => fn () => admin_listings(),
        '#^/listings/new/$#'            => fn () => $method === 'POST' ? admin_listing_save(null) : admin_listing_form(null),
        '#^/listings/(\d+)/$#'          => fn ($m) => $method === 'POST' ? admin_listing_save((int) $m[1]) : admin_listing_form((int) $m[1]),
        '#^/listings/(\d+)/preview/$#'  => fn ($m) => admin_listing_preview((int) $m[1]),
        '#^/listings/(\d+)/delete/$#'   => fn ($m) => $method === 'POST' ? admin_listing_delete((int) $m[1]) : redirect('/admin/listings/'),
        '#^/geocode/$#'                 => fn () => admin_geocode(),
        '#^/leads/$#'                   => fn () => admin_leads(),
        '#^/leads\.csv$#'               => fn () => admin_leads_csv(),
        '#^/leads/(\d+)/$#'             => fn ($m) => $method === 'POST' ? admin_lead_update((int) $m[1]) : redirect('/admin/leads/'),
        '#^/import/$#'                  => fn () => admin_import(),
        '#^/import/run/$#'              => fn () => $method === 'POST' ? admin_import_run() : redirect('/admin/import/'),
        '#^/users/$#'                   => fn () => admin_users(),
        '#^/users/(\d+)/(delete|password)/$#' => fn ($m) => $method === 'POST' ? admin_user_action((int) $m[1], $m[2]) : redirect('/admin/users/'),
        '#^/account/$#'                 => fn () => admin_account(),
    ];
    foreach ($routes as $re => $h) {
        if (preg_match($re, $sub, $m)) {
            $h($m);
            return;
        }
    }
    http_response_code(404);
    admin_render('message', ['title' => 'Page not found', 'text' => 'That admin page doesn’t exist.']);
}

function admin_render(string $view, array $vars = []): void
{
    $user = Auth::user();
    $flash = Auth::flash();
    $csrf = Auth::csrf();
    try {
        $newLeads = (int) db()->query("SELECT COUNT(*) FROM leads WHERE status = 'new'")->fetchColumn();
    } catch (PDOException) {
        $newLeads = 0;
    }
    extract($vars, EXTR_SKIP);
    ob_start();
    require HA_APP . "/views/admin/$view.php";
    $content = ob_get_clean();
    require HA_APP . '/views/admin/layout.php';
}

function admin_is_admin(): bool
{
    return (Auth::user()['role'] ?? '') === 'admin';
}

/* ------------------------------------------------------------ auth */

function admin_login(): void
{
    if (Auth::user()) {
        redirect('/admin/', 302);
    }
    $error = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        Auth::checkCsrf();
        if (Auth::throttled()) {
            $error = 'Too many attempts. Please wait 15 minutes and try again.';
        } elseif (Auth::attempt((string) ($_POST['email'] ?? ''), (string) ($_POST['password'] ?? ''))) {
            $next = (string) ($_GET['next'] ?? '/admin/');
            redirect(str_starts_with($next, '/admin/') ? $next : '/admin/', 302);
        } else {
            $error = 'That email and password don’t match.';
        }
    }
    $csrf = Auth::csrf();
    require HA_APP . '/views/admin/login.php';
}

function admin_logout(): void
{
    Auth::logout();
    redirect('/admin/login/', 302);
}

/** One-time creation of the first admin account (needs the config admin_key). */
function admin_setup(): void
{
    $key = config('admin_key');
    $count = (int) db()->query('SELECT COUNT(*) FROM users')->fetchColumn();
    if (!$key || !hash_equals($key, (string) ($_REQUEST['key'] ?? '')) || $count > 0) {
        http_response_code(404);
        exit('Not found');
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && strlen((string) ($_POST['password'] ?? '')) >= 10 && filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL)) {
        Auth::createUser($_POST['email'], (string) ($_POST['name'] ?? 'Admin'), $_POST['password'], 'admin');
        json_out(['ok' => true]);
        return;
    }
    json_out(['ok' => false, 'error' => 'POST email, name and a password of 10+ characters'], 422);
}

function admin_key_sync(): void
{
    $key = config('admin_key');
    if (!$key || !hash_equals($key, (string) ($_GET['key'] ?? ''))) {
        http_response_code(404);
        exit('Not found');
    }
    set_time_limit(0);
    $imp = new RiseImporter();
    if (!empty($_GET['slugs'])) {
        $res = ['imported' => $imp->importSlugs(array_filter(explode(',', $_GET['slugs'])), !empty($_GET['force']))];
    } else {
        $res = $imp->sync((int) ($_GET['limit'] ?? 25), time() + 240);
    }
    json_out($res + ['log' => $imp->log]);
}

/* ------------------------------------------------------------ dashboard */

function admin_dashboard(): void
{
    $q = fn ($sql) => (int) db()->query($sql)->fetchColumn();
    $stats = [
        'published' => $q("SELECT COUNT(*) FROM properties WHERE status = 'publish'"),
        'hidden'    => $q("SELECT COUNT(*) FROM properties WHERE status = 'hidden'"),
        'review'    => $q("SELECT COUNT(*) FROM properties WHERE status = 'review'"),
        'manual'    => $q("SELECT COUNT(*) FROM properties WHERE source = 'manual' AND status <> 'deleted'"),
        'leads_new' => $q("SELECT COUNT(*) FROM leads WHERE status = 'new'"),
        'leads_7d'  => (int) (function () {
            $st = db()->prepare('SELECT COUNT(*) FROM leads WHERE created_at >= ?');
            $st->execute([gmdate('c', time() - 7 * 86400)]);
            return $st->fetchColumn();
        })(),
    ];
    $leads = db()->query('SELECT l.*, p.name AS property FROM leads l LEFT JOIN properties p ON p.id = l.property_id ORDER BY l.id DESC LIMIT 6')->fetchAll();
    $recent = db()->query("SELECT id, slug, name, photo, status, source, updated_at, updated_by FROM properties WHERE status <> 'deleted' ORDER BY updated_at DESC, synced_at DESC LIMIT 6")->fetchAll();
    admin_render('dashboard', compact('stats', 'leads', 'recent'));
}

/* ------------------------------------------------------------ listings */

function admin_listings(): void
{
    $where = ["status <> 'deleted'"];
    $args = [];
    $f = ['q' => trim((string) ($_GET['q'] ?? '')), 'area' => (string) ($_GET['area'] ?? ''), 'status' => (string) ($_GET['status'] ?? ''), 'source' => (string) ($_GET['source'] ?? '')];
    if ($f['q'] !== '') {
        $where[] = '(name LIKE ? OR street LIKE ? OR zip LIKE ? OR neighborhood LIKE ?)';
        $kw = '%' . $f['q'] . '%';
        array_push($args, $kw, $kw, $kw, $kw);
    }
    if (isset(AREAS[$f['area']])) {
        $where[] = 'rise_location IN (' . implode(',', array_map('intval', AREAS[$f['area']]['rise'])) . ')';
    }
    if (in_array($f['status'], ['publish', 'hidden', 'review'], true)) {
        $where[] = 'status = ?';
        $args[] = $f['status'];
    }
    if ($f['source'] === 'manual') {
        $where[] = "source = 'manual'";
    } elseif ($f['source'] === 'rise') {
        $where[] = "source = 'rise' AND locked = 0";
    } elseif ($f['source'] === 'edited') {
        $where[] = "source = 'rise' AND locked = 1";
    }
    $w = implode(' AND ', $where);
    $st = db()->prepare("SELECT COUNT(*) FROM properties WHERE $w");
    $st->execute($args);
    $total = (int) $st->fetchColumn();
    $per = 50;
    $page = max(1, (int) ($_GET['page'] ?? 1));
    $st = db()->prepare("SELECT id, slug, name, street, city, zip, neighborhood, price_min, beds_min, beds_max, photo, status, source, locked, updated_at, synced_at
        FROM properties WHERE $w ORDER BY name LIMIT $per OFFSET " . (($page - 1) * $per));
    $st->execute($args);
    $rows = $st->fetchAll();
    admin_render('listings', ['rows' => $rows, 'total' => $total, 'page' => $page, 'pages' => max(1, (int) ceil($total / $per)), 'f' => $f]);
}

function admin_listing_form(?int $id): void
{
    if ($id) {
        $st = db()->prepare("SELECT * FROM properties WHERE id = ? AND status <> 'deleted'");
        $st->execute([$id]);
        $p = $st->fetch();
        if (!$p) {
            Auth::flash('That listing no longer exists.', 'err');
            redirect('/admin/listings/', 302);
        }
        $p['d'] = json_decode($p['data'] ?? '{}', true) ?: [];
    } else {
        $p = ['id' => 0, 'slug' => '', 'name' => '', 'street' => '', 'city' => 'Houston', 'zip' => '', 'lat' => null, 'lng' => null,
              'neighborhood' => '', 'rise_location' => 0, 'pets' => 1, 'parking' => 0, 'furnished' => 0, 'essential' => 0,
              'year_built' => null, 'units' => null, 'stories' => null, 'rating' => null, 'status' => 'publish', 'source' => 'manual', 'locked' => 1,
              'd' => ['floorplans' => [], 'prices' => [], 'photos' => [], 'amenities' => [], 'schools' => [], 'faqs' => [], 'about' => [], 'special' => '', 'hours' => '']];
    }
    $areaKey = $id ? Listings::areaKeyFor($p) : '';
    $have = array_unique(array_merge(...array_values(($p['d']['amenities'] ?? []) ?: [[]])));
    $other = array_values(array_diff($have, ADMIN_UNIT_AMENITIES, ADMIN_COMMUNITY_AMENITIES));
    admin_render('edit', compact('p', 'areaKey', 'have', 'other'));
}

function admin_listing_save(?int $id): void
{
    $in = $_POST;
    $old = null;
    if ($id) {
        $st = db()->prepare('SELECT * FROM properties WHERE id = ?');
        $st->execute([$id]);
        $old = $st->fetch();
        if (!$old) {
            redirect('/admin/listings/', 302);
        }
    }
    $name = trim((string) ($in['name'] ?? ''));
    $street = trim((string) ($in['street'] ?? ''));
    if ($name === '' || $street === '') {
        Auth::flash('Please fill in the property name and street address.', 'err');
        redirect($id ? "/admin/listings/$id/" : '/admin/listings/new/', 302);
    }
    $id = $id ?: admin_new_id();
    $data = $old ? (json_decode($old['data'] ?? '{}', true) ?: []) : [];

    // Photos: kept existing ones in the chosen order, then new uploads
    $keep = json_decode((string) ($in['photos_keep'] ?? '[]'), true) ?: [];
    $photos = array_values(array_filter($keep, fn ($ph) => is_string($ph) && str_starts_with($ph, '/media/')));
    foreach (Images::files('photos_new') as $file) {
        if ($path = Images::saveUpload($file, $id)) {
            $photos[] = $path;
        }
    }

    // Floor plans
    $plans = [];
    $planFiles = Images::files('plan_img');
    foreach ((array) ($in['plans'] ?? []) as $i => $pl) {
        if (!empty($pl['remove']) || ($pl['beds'] ?? '') === '') {
            continue;
        }
        $img = (string) ($pl['image'] ?? '');
        if (isset($planFiles[$i]) && ($up = Images::saveUpload($planFiles[$i], $id, 'plan'))) {
            $img = $up;
        }
        $plans[] = ['beds' => (int) $pl['beds'], 'baths' => (float) ($pl['baths'] ?: 1), 'sqft' => (int) ($pl['sqft'] ?? 0),
                    'available' => trim((string) ($pl['available'] ?? '')), 'image' => str_starts_with($img, '/media/') ? $img : ''];
    }

    $prices = [];
    foreach ((array) ($in['price'] ?? []) as $b => $v) {
        $v = (int) preg_replace('/[^\d]/', '', (string) $v);
        if ($v >= 100) {
            $prices[(int) $b] = $v;
        }
    }

    $other = array_filter(array_map('trim', preg_split('/[,\n]/', (string) ($in['amen_other'] ?? ''))));
    $amenities = array_filter([
        'Unit Features'       => array_values(array_intersect(ADMIN_UNIT_AMENITIES, (array) ($in['amen_unit'] ?? []))),
        'Community Amenities' => array_values(array_intersect(ADMIN_COMMUNITY_AMENITIES, (array) ($in['amen_comm'] ?? []))),
        'Other Amenities'     => array_values($other),
    ]);

    $faqs = [];
    foreach ((array) ($in['faqs'] ?? []) as $f) {
        $q = trim((string) ($f['q'] ?? ''));
        $a = trim((string) ($f['a'] ?? ''));
        if ($q !== '' && $a !== '') {
            $faqs[] = ['q' => $q, 'a' => [$a]];
        }
    }
    $schools = array_filter([
        'District' => trim((string) ($in['school_district'] ?? '')), 'Elementary School' => trim((string) ($in['school_elem'] ?? '')),
        'Middle School' => trim((string) ($in['school_middle'] ?? '')), 'High School' => trim((string) ($in['school_high'] ?? '')),
    ]);
    $flag = fn ($k) => !empty($in[$k]) ? 1 : 0;
    $tags = array_values(array_filter([$flag('pets') ? 'Pets Allowed' : '', $flag('parking') ? 'Parking Included' : '',
        $flag('furnished') ? 'Furnished' : 'Unfurnished', $flag('essential') ? 'Essential Housing' : '']));
    $city = trim((string) ($in['city'] ?? '')) ?: 'Houston';
    $zip = preg_replace('/[^\d]/', '', (string) ($in['zip'] ?? ''));
    $address = "$street, $city, TX $zip";

    $data = array_merge($data, [
        'about'      => array_values(array_filter(array_map('trim', preg_split('/\R\s*\R/', (string) ($in['about'] ?? ''))))),
        'floorplans' => $plans,
        'prices'     => $prices,
        'photos'     => $photos,
        'amenities'  => $amenities,
        'schools'    => $schools,
        'faqs'       => $faqs,
        'tags'       => $tags,
        'hours'      => trim((string) ($in['hours'] ?? '')),
        'special'    => trim((string) ($in['special'] ?? '')),
        'address'    => $address,
        'info'       => array_filter(['Year Built' => (string) ($in['year_built'] ?? ''), 'Units' => (string) ($in['units'] ?? ''),
                                      'Stories' => (string) ($in['stories'] ?? ''), 'Furniture' => $flag('furnished') ? 'Furnished' : 'Unfurnished']),
    ]);
    unset($data['price_source']);

    $lat = is_numeric($in['lat'] ?? null) ? (float) $in['lat'] : null;
    $lng = is_numeric($in['lng'] ?? null) ? (float) $in['lng'] : null;
    if ($lat === null || $lng === null) {
        [$lat, $lng] = Geocoder::locate($address);
    }
    $areaKey = (string) ($in['area'] ?? '');
    $riseLoc = (int) ($old['rise_location'] ?? 0);
    if (isset(AREAS[$areaKey]) && !in_array($riseLoc, AREAS[$areaKey]['rise'], true)) {
        $riseLoc = AREAS[$areaKey]['rise'][0];
    } elseif ($areaKey === '' && $old && Listings::areaKeyFor($old) !== '') {
        $riseLoc = 0;
    }
    $source = $old['source'] ?? 'manual';
    $user = Auth::user();

    // Imported listings wait in 'review' until the About text is rewritten, then go live by themselves
    $status = in_array($in['status'] ?? '', ['publish', 'hidden', 'review'], true) ? $in['status'] : 'publish';
    $publishedNow = false;
    $overlap = null;
    if ($status === 'review') {
        $orig = $data['rise_about'] ?? (($old['status'] ?? '') === 'review' ? (json_decode($old['data'] ?? '{}', true)['about'] ?? []) : []);
        $overlap = Listings::aboutOverlap($data['about'], $orig);
        if ($data['about'] && $overlap < ADMIN_REWRITE_MAX_OVERLAP) {
            $status = 'publish';
            $publishedNow = true;
        }
    }
    $rec = [
        'id' => $id,
        'slug' => $old['slug'] ?? admin_unique_slug($name),
        'name' => $name,
        'street' => $street, 'city' => $city, 'state' => 'TX', 'zip' => $zip,
        'lat' => $lat, 'lng' => $lng,
        'area' => $old['area'] ?? '',
        'neighborhood' => trim((string) ($in['neighborhood'] ?? '')) ?: (AREAS[$areaKey]['name'] ?? ''),
        'rise_location' => $riseLoc,
        'pets' => $flag('pets'), 'parking' => $flag('parking'), 'furnished' => $flag('furnished'), 'essential' => $flag('essential'),
        'special' => (int) ($data['special'] !== ''),
        'year_built' => (int) ($in['year_built'] ?? 0) ?: null,
        'units' => (int) ($in['units'] ?? 0) ?: null,
        'stories' => (int) ($in['stories'] ?? 0) ?: null,
        'rating' => is_numeric($in['rating'] ?? null) ? min(5, max(0, (float) $in['rating'])) : null,
        'data' => json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE),
        'rise_modified' => $old['rise_modified'] ?? '',
        'synced_at' => $old['synced_at'] ?? gmdate('c'),
        'status' => $status,
        'source' => $source,
        'locked' => $source === 'rise' && !empty($in['keep_sync']) ? 0 : 1,
        'updated_at' => gmdate('c'),
        'updated_by' => $user['name'] ?: $user['email'],
    ] + Listings::derive($data);
    Listings::upsert($rec);
    if ($lat === null) {
        Auth::flash('Saved – but we couldn’t place this address on the map. Drag the pin to set the location.', 'err');
    } elseif ($publishedNow) {
        Auth::flash('Saved and published – the rewritten About section is now live on the website.', 'ok');
    } elseif ($status === 'review') {
        Auth::flash($data['about']
            ? sprintf('Saved, still hidden: about %d%% of the About section still matches the riseapartments.com text. Rewrite it in your own words (under %d%%) and save again to publish.', round($overlap * 100), ADMIN_REWRITE_MAX_OVERLAP * 100)
            : 'Saved, still hidden: write an About section in your own words and save again to publish.', 'err');
    } else {
        Auth::flash('Listing saved.', 'ok');
    }
    redirect("/admin/listings/$id/", 302);
}

/** Show a listing exactly as visitors would see it, whatever its status (never indexed). */
function admin_listing_preview(int $id): void
{
    $st = db()->prepare("SELECT * FROM properties WHERE id = ? AND status <> 'deleted'");
    $st->execute([$id]);
    $p = $st->fetch();
    if (!$p) {
        redirect('/admin/listings/', 302);
    }
    $p['d'] = json_decode($p['data'] ?? '{}', true) ?: [];
    $nearby = Listings::nearby($p, 6);
    $areaKey = Listings::areaKeyFor($p);
    header('X-Robots-Tag: noindex, nofollow');
    render('property', compact('p', 'nearby', 'areaKey'), [
        'title'      => 'Preview: ' . $p['name'] . ' | Houston Apartments',
        'canonical'  => listing_url($p['slug']),
        'body_class' => 'property-page',
        'noindex'    => true,
    ]);
}

function admin_new_id(): int
{
    $max = (int) db()->query('SELECT MAX(id) FROM properties WHERE id >= 900000000')->fetchColumn();
    return max(900000001, $max + 1);
}

function admin_unique_slug(string $name): string
{
    $base = slugify($name);
    $slug = $base;
    for ($n = 2; ; $n++) {
        $st = db()->prepare('SELECT 1 FROM properties WHERE slug = ?');
        $st->execute([$slug]);
        if (!$st->fetchColumn()) {
            return $slug;
        }
        $slug = "$base-$n";
    }
}

function admin_listing_delete(int $id): void
{
    $st = db()->prepare('SELECT source, name FROM properties WHERE id = ?');
    $st->execute([$id]);
    $p = $st->fetch();
    if ($p && $p['source'] === 'manual') {
        db()->prepare('DELETE FROM properties WHERE id = ?')->execute([$id]);
        Images::removeDir($id);
    } elseif ($p) {
        // Rise listings are kept as "deleted" + locked so the sync doesn't bring them back
        db()->prepare("UPDATE properties SET status = 'deleted', locked = 1, updated_at = ? WHERE id = ?")->execute([gmdate('c'), $id]);
    }
    Auth::flash($p ? "“{$p['name']}” was deleted." : 'Listing not found.');
    redirect('/admin/listings/', 302);
}

function admin_geocode(): void
{
    [$lat, $lng] = Geocoder::locate((string) ($_GET['q'] ?? ''));
    json_out(['lat' => $lat, 'lng' => $lng]);
}

/* ------------------------------------------------------------ leads */

function admin_leads(): void
{
    $status = (string) ($_GET['status'] ?? '');
    $where = isset(LEAD_STATUSES[$status]) ? 'WHERE l.status = ' . db()->quote($status) : '';
    $rows = db()->query("SELECT l.*, p.name AS property, p.slug FROM leads l LEFT JOIN properties p ON p.id = l.property_id $where ORDER BY l.id DESC LIMIT 500")->fetchAll();
    admin_render('leads', compact('rows', 'status'));
}

function admin_lead_update(int $id): void
{
    $status = (string) ($_POST['status'] ?? 'new');
    db()->prepare('UPDATE leads SET status = ?, notes = ? WHERE id = ?')
        ->execute([isset(LEAD_STATUSES[$status]) ? $status : 'new', mb_substr(trim((string) ($_POST['notes'] ?? '')), 0, 4000), $id]);
    if (!empty($_POST['ajax'])) {
        json_out(['ok' => true]);
        return;
    }
    Auth::flash('Lead updated.');
    redirect('/admin/leads/', 302);
}

function admin_leads_csv(): void
{
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename="houston-apartments-leads-' . date('Y-m-d') . '.csv"');
    $out = fopen('php://output', 'w');
    fputcsv($out, ['Date', 'Name', 'Phone', 'Email', 'Move-in', 'Beds', 'Budget', 'Property', 'Message', 'Status', 'Notes', 'Page']);
    foreach (db()->query('SELECT l.*, p.name AS property FROM leads l LEFT JOIN properties p ON p.id = l.property_id ORDER BY l.id DESC') as $r) {
        fputcsv($out, [$r['created_at'], $r['name'], $r['phone'], $r['email'], $r['move_in'], $r['beds'], $r['budget'], $r['property'], $r['message'], $r['status'], $r['notes'], $r['page']]);
    }
}

/* ------------------------------------------------------------ Rise import */

function admin_import(): void
{
    $last = db()->query("SELECT MAX(synced_at) FROM properties WHERE source = 'rise'")->fetchColumn();
    $counts = db()->query("SELECT COUNT(*) total, SUM(CASE WHEN locked = 1 THEN 1 ELSE 0 END) locked FROM properties WHERE source = 'rise' AND status <> 'deleted'")->fetch();
    admin_render('import', compact('last', 'counts'));
}

/** One unit of import work per request (the CDN cuts requests off after ~100 s). */
function admin_import_run(): void
{
    set_time_limit(300);
    $imp = new RiseImporter();
    if (!empty($_POST['slug'])) {
        $n = $imp->importSlugs([(string) $_POST['slug']], !empty($_POST['force']));
        json_out(['imported' => $n, 'log' => $imp->log]);
        return;
    }
    $res = $imp->sync(3, time() + 75);
    json_out($res + ['log' => $imp->log]);
}

/* ------------------------------------------------------------ users */

function admin_users(): void
{
    if (!admin_is_admin()) {
        Auth::flash('Only admins can manage users.', 'err');
        redirect('/admin/', 302);
    }
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $email = trim((string) ($_POST['email'] ?? ''));
        $pass = (string) ($_POST['password'] ?? '');
        if (!filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($pass) < 10) {
            Auth::flash('Enter a valid email and a password of at least 10 characters.', 'err');
        } else {
            try {
                Auth::createUser($email, (string) ($_POST['name'] ?? ''), $pass, (string) ($_POST['role'] ?? 'editor'));
                Auth::flash("Added $email. Share the password with them privately.");
            } catch (PDOException) {
                Auth::flash('That email already has an account.', 'err');
            }
        }
        redirect('/admin/users/', 302);
    }
    $rows = db()->query('SELECT id, email, name, role, created_at, last_login FROM users ORDER BY name, email')->fetchAll();
    admin_render('users', compact('rows'));
}

function admin_user_action(int $id, string $action): void
{
    if (!admin_is_admin()) {
        redirect('/admin/', 302);
    }
    if ($action === 'delete') {
        if ($id === (int) Auth::user()['id']) {
            Auth::flash('You can’t delete your own account.', 'err');
        } else {
            db()->prepare('DELETE FROM users WHERE id = ?')->execute([$id]);
            Auth::flash('User removed.');
        }
    } else {
        $pass = (string) ($_POST['password'] ?? '');
        if (strlen($pass) < 10) {
            Auth::flash('Passwords need at least 10 characters.', 'err');
        } else {
            db()->prepare('UPDATE users SET pass_hash = ? WHERE id = ?')->execute([password_hash($pass, PASSWORD_DEFAULT), $id]);
            Auth::flash('Password updated.');
        }
    }
    redirect('/admin/users/', 302);
}

function admin_account(): void
{
    $u = Auth::user();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $st = db()->prepare('SELECT pass_hash FROM users WHERE id = ?');
        $st->execute([$u['id']]);
        if (!password_verify((string) ($_POST['current'] ?? ''), (string) $st->fetchColumn())) {
            Auth::flash('Your current password isn’t right.', 'err');
        } elseif (strlen((string) ($_POST['password'] ?? '')) < 10 || $_POST['password'] !== ($_POST['confirm'] ?? '')) {
            Auth::flash('New passwords must match and be at least 10 characters.', 'err');
        } else {
            db()->prepare('UPDATE users SET pass_hash = ?, name = ? WHERE id = ?')
                ->execute([password_hash($_POST['password'], PASSWORD_DEFAULT), trim((string) ($_POST['name'] ?? $u['name'])), $u['id']]);
            Auth::flash('Password changed.');
        }
        redirect('/admin/account/', 302);
    }
    admin_render('account', ['u' => $u]);
}
