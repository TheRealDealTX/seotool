<?php
// Listing layer. listings.json stays the source for the existing 139 listings;
// mhr_listings rows add owner edits (as overrides), status and contact
// visibility, and hold new submissions in full. Public pages call listings()
// in app/lib.php, which passes the JSON through mhr_listings() below.

const MHR_CONTACT_FIELDS = ['phone', 'email', 'website', 'phone_note'];

const MHR_DEFAULTS = [
    'slug' => '', 'title' => '', 'base' => '', 'featured' => false, 'date' => '', 'address' => '', 'lat' => null, 'lng' => null,
    'price' => 0, 'beds' => 0, 'baths' => 0, 'sqft' => 0, 'website' => '', 'amenities' => [], 'images' => [], 'description' => '',
    'operator' => '', 'phone' => '', 'email' => '', 'hours' => '', 'eligibility' => '', 'pets' => '', 'utilities' => '',
    'beds_range' => '', 'sqft_range' => '', 'schools' => [], 'nearby' => [], 'highlights' => [], 'photo_note' => '',
    'sources' => [], 'baths_range' => '', 'phone_note' => '',
];

// Fields owners and admins can edit, with their type.
const MHR_EDITABLE = [
    'title' => 'line', 'base' => 'base', 'address' => 'line', 'price' => 'int', 'rent_note' => 'line',
    'beds' => 'num', 'baths' => 'num', 'sqft' => 'int', 'beds_range' => 'line', 'baths_range' => 'line', 'sqft_range' => 'line',
    'operator' => 'line', 'eligibility' => 'line', 'utilities' => 'line', 'pets' => 'line', 'hours' => 'line',
    'description' => 'html', 'highlights' => 'list', 'amenities' => 'list', 'nearby' => 'list', 'schools' => 'list',
    'phone' => 'line', 'email' => 'email', 'website' => 'url',
];
const MHR_ADMIN_EDITABLE = ['lat' => 'float', 'lng' => 'float', 'featured' => 'bool'];

function mhr_json_listings() { return data('listings'); }

function mhr_json_listing($slug) {
    foreach (mhr_json_listings() as $l) if ($l['slug'] === $slug) return $l;
    return null;
}

function mhr_rows() {
    static $rows = null;
    if ($rows !== null) return $rows;
    try { $rows = array_column(mhr_all('SELECT * FROM mhr_listings'), null, 'slug'); }
    catch (MhrDbUnavailable $e) { $rows = []; }
    return $rows;
}
function mhr_row_for($slug) { return mhr_row('SELECT * FROM mhr_listings WHERE slug = ?', [$slug]); }

function mhr_normalize(array $l) {
    $l = $l + MHR_DEFAULTS;
    foreach (['amenities', 'images', 'schools', 'nearby', 'highlights', 'sources'] as $k) if (!is_array($l[$k])) $l[$k] = [];
    return $l;
}

// Full listing data (no redaction) for a slug, plus its row. For admin and owner pages.
function mhr_listing_full($slug, $row = false) {
    if ($row === false) $row = mhr_row_for($slug);
    $json = mhr_json_listing($slug);
    if ($json) {
        $over = $row && $row['data'] ? (json_decode($row['data'], true) ?: []) : [];
        return [mhr_normalize(array_merge($json, $over)), $row, 'json'];
    }
    if ($row && $row['origin'] === 'db') return [mhr_normalize(json_decode($row['data'], true) ?: []), $row, 'db'];
    return [null, null, null];
}

function mhr_apply_visibility(array $l, $row) {
    $visible = $row && (int)$row['contact_visible'] === 1;
    $l['_mhr'] = ['contact_visible' => $visible, 'verified' => $row && (int)$row['verified'] === 1, 'claimed' => $row && $row['owner_id']];
    if (!$visible) {
        foreach (MHR_CONTACT_FIELDS as $k) $l[$k] = '';
        $l['sources'] = [];
        $l['description'] = mhr_redact($l['description']);
    }
    return $l;
}

function mhr_redact($html) {
    $html = preg_replace('/(?<![\w$])\+?1?[\s.-]?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b/', '[phone hidden]', $html);
    $html = preg_replace('/<a\b[^>]*href="(?:mailto:|tel:)[^"]*"[^>]*>(.*?)<\/a>/is', '$1', $html);
    return preg_replace('/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i', '[email hidden]', $html);
}

// Public listing set: JSON + overrides + published submissions, contact details
// removed from every listing whose owner has not verified.
function mhr_listings(array $json) {
    static $out = null;
    if ($out !== null) return $out;
    $rows = mhr_rows();
    $out = [];
    foreach ($json as $l) {
        $row = $rows[$l['slug']] ?? null;
        if ($row && in_array($row['status'], ['unpublished', 'deleted'], true)) continue;
        if ($row && $row['data']) $l = array_merge($l, json_decode($row['data'], true) ?: []);
        $out[] = mhr_apply_visibility(mhr_normalize($l), $row);
    }
    foreach ($rows as $row) {
        if ($row['origin'] !== 'db' || $row['status'] !== 'published') continue;
        $l = mhr_normalize(json_decode($row['data'], true) ?: []);
        if (!$l['slug'] || !base($l['base'])) continue;
        $out[] = mhr_apply_visibility($l, $row);
    }
    return $out;
}

function mhr_base_center($base_slug) {
    $pts = array_filter(mhr_json_listings(), fn($l) => $l['base'] === $base_slug && $l['lat'] && $l['lng']);
    if (!$pts) return [39.8283, -98.5795];
    return [round(array_sum(array_column($pts, 'lat')) / count($pts), 5), round(array_sum(array_column($pts, 'lng')) / count($pts), 5)];
}

function mhr_slugify($s) {
    $s = strtolower(trim(preg_replace('/[^A-Za-z0-9]+/', '-', iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $s) ?: $s), '-'));
    return substr($s ?: 'listing', 0, 80);
}
function mhr_unique_slug($title) {
    $base = mhr_slugify($title);
    $slug = $base;
    for ($i = 2; mhr_json_listing($slug) || mhr_row_for($slug); $i++) $slug = $base . '-' . $i;
    return $slug;
}

// Make sure an existing (JSON) listing has a row we can attach state to.
function mhr_ensure_row($slug) {
    if ($row = mhr_row_for($slug)) return $row;
    if (!mhr_json_listing($slug)) return null;
    mhr_q("INSERT INTO mhr_listings (slug, origin, data, status, created_at, updated_at) VALUES (?, 'json', NULL, 'published', ?, ?)", [$slug, mhr_now(), mhr_now()]);
    return mhr_row_for($slug);
}

function mhr_set_cols($slug, array $cols) {
    if (!$cols) return;
    mhr_ensure_row($slug);
    $allowed = ['status', 'owner_id', 'contact_visible', 'verified', 'plan', 'admin_note', 'published_at'];
    $set = []; $args = [];
    foreach ($cols as $k => $v) { if (!in_array($k, $allowed, true)) continue; $set[] = "$k = ?"; $args[] = $v; }
    $set[] = 'updated_at = ?'; $args[] = mhr_now(); $args[] = $slug;
    mhr_q('UPDATE mhr_listings SET ' . implode(', ', $set) . ' WHERE slug = ?', $args);
}

// Save edited fields. JSON listings store only the overrides; submissions store everything.
function mhr_save_fields($slug, array $fields) {
    $row = mhr_ensure_row($slug);
    if (!$row) return false;
    $fields['modified'] = gmdate('Y-m-d');
    $cur = $row['data'] ? (json_decode($row['data'], true) ?: []) : [];
    mhr_q('UPDATE mhr_listings SET data = ?, updated_at = ? WHERE slug = ?',
        [json_encode(array_merge($cur, $fields), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), mhr_now(), $slug]);
    return true;
}

// Plain text <-> the listing description HTML
function mhr_text_to_html($text) {
    $paras = preg_split('/\n\s*\n/', trim($text));
    return implode("\n", array_map(fn($p) => '<p>' . nl2br(e(trim($p)), false) . '</p>', array_filter($paras, fn($p) => trim($p) !== '')));
}
function mhr_html_to_text($html) {
    $t = preg_replace(['#<br\s*/?>#i', '#</p>\s*#i', '#</li>\s*#i'], ["\n", "\n\n", "\n"], $html);
    return trim(preg_replace("/\n{3,}/", "\n\n", html_entity_decode(strip_tags($t), ENT_QUOTES | ENT_HTML5, 'UTF-8')));
}
function mhr_list_from_text($t) {
    $items = preg_split('/\s*(?:\n|,(?![^(]*\)))\s*/', trim($t));
    return array_values(array_slice(array_unique(array_filter(array_map(fn($x) => mb_substr(trim($x, " -•\t"), 0, 120), $items), 'strlen')), 0, 40));
}

// Validate posted editor fields. Returns [fields, errors].
function mhr_read_editor(array $spec) {
    $f = []; $err = [];
    foreach ($spec as $k => $type) {
        if (!array_key_exists($k, $_POST) && $type !== 'bool') continue;
        $raw = mhr_post($k, $type === 'html' ? 8000 : ($type === 'list' ? 4000 : 300));
        switch ($type) {
            case 'line': $f[$k] = str_replace("\n", ' ', $raw); break;
            case 'int': $f[$k] = $raw === '' ? 0 : (int)preg_replace('/[^0-9]/', '', $raw); break;
            case 'num': $f[$k] = $raw === '' ? 0 : round((float)$raw, 1); break;
            case 'float': if ($raw !== '' && is_numeric($raw)) $f[$k] = (float)$raw; break;
            case 'bool': $f[$k] = !empty($_POST[$k]); break;
            case 'html': $f[$k] = mhr_text_to_html($raw); break;
            case 'list': $f[$k] = mhr_list_from_text($raw); break;
            case 'base': if (base($raw)) $f[$k] = $raw; else $err[] = 'Please choose the nearest installation.'; break;
            case 'email':
                if ($raw !== '' && !filter_var($raw, FILTER_VALIDATE_EMAIL)) $err[] = 'Please enter a valid listing email.';
                else $f[$k] = $raw; break;
            case 'url':
                if ($raw !== '' && !preg_match('#^https?://#i', $raw)) $raw = 'https://' . $raw;
                if ($raw !== '' && (!filter_var($raw, FILTER_VALIDATE_URL) || !preg_match('#^https?://#i', $raw))) $err[] = 'Please enter a valid website address.';
                else $f[$k] = $raw; break;
        }
    }
    if (isset($f['title']) && $f['title'] === '') $err[] = 'Property name is required.';
    return [$f, $err];
}

// Admin overview of every listing, JSON and submitted.
function mhr_admin_listing_index() {
    $rows = array_column(mhr_all('SELECT * FROM mhr_listings'), null, 'slug');
    $out = [];
    foreach (mhr_json_listings() as $l) {
        $row = $rows[$l['slug']] ?? null;
        $over = $row && $row['data'] ? (json_decode($row['data'], true) ?: []) : [];
        $out[] = ['slug' => $l['slug'], 'title' => $over['title'] ?? $l['title'], 'base' => $over['base'] ?? $l['base'], 'origin' => 'json', 'row' => $row,
            'status' => $row['status'] ?? 'published', 'date' => $l['date']];
    }
    foreach ($rows as $row) {
        if ($row['origin'] !== 'db') continue;
        $d = json_decode($row['data'], true) ?: [];
        $out[] = ['slug' => $row['slug'], 'title' => $d['title'] ?? $row['slug'], 'base' => $d['base'] ?? '', 'origin' => 'db', 'row' => $row,
            'status' => $row['status'], 'date' => substr($row['created_at'], 0, 10)];
    }
    return $out;
}
