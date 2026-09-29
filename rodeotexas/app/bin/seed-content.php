<?php
/**
 * One-time (idempotent) migration of content from the old WordPress site:
 *   - 21 articles + categories            (app/data/articles.json)
 *   - Texas events from the old calendar  (app/data/legacy_events.json)
 *   - 301 redirects for retired URLs      (app/data/redirects.json)
 *
 *   php app/bin/seed-content.php [--no-geocode]
 *
 * Re-running never duplicates or overwrites records edited in the admin.
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/bootstrap.php';

use RT\Classifier;
use RT\Db;
use RT\Geo;
use RT\Importer;

function rt_seed_content(bool $geocode = true): array
{
    $now = now_utc();
    $out = ['articles' => 0, 'legacy_events' => 0, 'redirects' => 0, 'venues_located' => 0];
    if ($geocode) {
        Geo::$budget = 300;
    }

    // ---- articles
    $data = json_decode((string) file_get_contents(RT_APP . '/data/articles.json'), true);
    foreach ($data['categories'] as $c) {
        Db::q('INSERT IGNORE INTO categories (slug, name) VALUES (?, ?)', [$c['slug'], $c['name']]);
    }
    foreach ($data['articles'] as $a) {
        if (Db::val('SELECT id FROM articles WHERE slug = ?', [$a['slug']])) {
            continue;
        }
        $id = Db::insert('articles', [
            'slug' => $a['slug'], 'title' => $a['title'], 'seo_title' => $a['seo_title'],
            'meta_description' => $a['meta_description'], 'excerpt' => $a['excerpt'], 'content_html' => $a['content_html'],
            'featured_image' => $a['featured_image'], 'featured_alt' => $a['featured_alt'],
            'featured_width' => $a['featured_width'], 'featured_height' => $a['featured_height'],
            'status' => 'published', 'published_at' => $a['published_at'], 'updated_at' => $a['updated_at'], 'created_at' => $now,
        ]);
        foreach ($a['categories'] as $c) {
            Db::q('INSERT IGNORE INTO article_categories (article_id, category_id) SELECT ?, id FROM categories WHERE slug = ?', [$id, $c['slug']]);
        }
        $out['articles']++;
    }

    // ---- legacy events (archived pages, clearly labelled as unverified)
    $legacySource = Db::one("SELECT * FROM sources WHERE slug = 'legacy-site'");
    $legacy = json_decode((string) file_get_contents(RT_APP . '/data/legacy_events.json'), true);
    foreach ($legacy as $ev) {
        if (Db::val('SELECT id FROM events WHERE slug = ?', [$ev['slug']])) {
            continue;
        }
        $venueId = null; $tz = 'America/Chicago';
        if ($ev['city']) {
            $key = Importer::venueKey(null, $ev['city']);
            $venueId = Db::val('SELECT id FROM venues WHERE norm_key = ?', [$key]);
            if (!$venueId) {
                $geo = $geocode ? Geo::geocode($ev['city'] . ', TX', true) : null;
                if ($geo && ($geo['state'] ?? '') !== 'TX') {
                    $geo = null;
                }
                $venueId = Db::insert('venues', [
                    'norm_key' => $key, 'name' => null, 'city' => $ev['city'], 'county' => $geo['county'] ?? null, 'state' => 'TX',
                    'lat' => $geo['lat'] ?? null, 'lng' => $geo['lng'] ?? null, 'location_precision' => $geo ? 'city' : 'none',
                    'timezone' => Geo::timezoneFor($geo['county'] ?? null, $geo['lng'] ?? null),
                    'region_id' => Geo::regionIdFor($geo['lat'] ?? null, $geo['lng'] ?? null),
                    'created_at' => $now, 'updated_at' => $now,
                ]);
            }
            $tz = (string) Db::val('SELECT timezone FROM venues WHERE id = ?', [$venueId]);
        }
        $assoc = Classifier::idFor('associations', Classifier::associationSlug($ev['title']));
        $desc = $ev['disciplines'] ? 'Events listed on the previous calendar: ' . preg_replace('/\s+(?=[A-Z])/', ', ', $ev['disciplines']) . '.' : null;
        $id = Db::insert('events', [
            'slug' => $ev['slug'], 'title' => $ev['title'], 'description' => $desc,
            'event_type_id' => Classifier::idFor('event_types', Classifier::eventTypeSlug($ev['title'])),
            'association_id' => $assoc,
            'level' => $assoc ? Db::val('SELECT level FROM associations WHERE id = ?', [$assoc]) : Classifier::levelFromText($ev['title']),
            'venue_id' => $venueId, 'start_date' => $ev['start_date'], 'end_date' => $ev['end_date'], 'timezone' => $tz,
            'status' => 'scheduled', 'official_url' => $ev['official_url'],
            'publish_state' => 'published', 'source_id' => $legacySource['id'] ?? null,
            'source_label' => 'Previous RodeoTexas.org calendar', 'source_url' => null,
            'last_verified_at' => null, 'is_legacy' => 1,
            'legacy_note' => 'Archived from the previous RodeoTexas.org calendar. Location is based on the event name; details have not been re-verified.',
            'created_at' => $now, 'updated_at' => $now,
        ]);
        Importer::history($id, 'system', 'created', null, 'migrated from WordPress (legacy id ' . $ev['legacy_id'] . ')');
        $out['legacy_events']++;
    }

    if ($geocode) {
        Geo::$budget = 300;
        $out['venues_located'] = Geo::backfillVenues(300);
    }

    // ---- redirects
    $redirects = json_decode((string) file_get_contents(RT_APP . '/data/redirects.json'), true);
    foreach ($redirects as $from => $to) {
        $n = Db::q('INSERT IGNORE INTO redirects (from_path, to_path, code, created_at) VALUES (?, ?, 301, ?)', [$from, $to, $now])->rowCount();
        $out['redirects'] += $n;
    }
    return $out;
}

if (PHP_SAPI === 'cli' && realpath($argv[0] ?? '') === __FILE__) {
    $r = rt_seed_content(!in_array('--no-geocode', $argv, true));
    echo "Seeded: {$r['articles']} articles, {$r['legacy_events']} legacy events, {$r['redirects']} redirects, {$r['venues_located']} venues located\n";
}
