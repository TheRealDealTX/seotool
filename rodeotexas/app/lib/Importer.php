<?php
declare(strict_types=1);

namespace RT;

use RT\Adapters\Adapter;
use RT\Adapters\CsvAdapter;

/**
 * Event import engine.
 *
 * Guarantees:
 *  - one run at a time (flock on storage/locks/import.lock); stale "running" rows are marked abandoned
 *  - a source that fails to fetch changes NOTHING (fetch happens before any write)
 *  - each record is processed in its own transaction; one bad record cannot corrupt others
 *  - idempotent: an unchanged record (same payload hash) is a no-op; stable (source, uid) identity
 *  - cross-source duplicate detection (title + city + overlapping dates), distinct competitions grouped
 *  - admin-locked fields are never overwritten; disagreements become review items
 *  - events are never canceled or deleted because they vanished from a source
 *  - only records that are provably in Texas are imported
 */
final class Importer
{
    private int $runId = 0;
    private array $stats = [];
    private string $mode = 'weekly';
    /** @var resource|null */
    private $lock = null;

    public const STAT_KEYS = ['sources_ok', 'sources_failed', 'fetched', 'created', 'published', 'drafted', 'updated',
        'matched', 'unchanged', 'conflicts', 'review', 'skipped_filter', 'skipped_outside_texas', 'skipped_no_location',
        'skipped_invalid', 'record_errors'];

    /**
     * @param string      $trigger  cron | manual | cli
     * @param string      $mode     weekly | daily | single
     * @param int[]|null  $sourceIds restrict to these sources
     * @param string|null $csvFile  file for a CSV (manual) source
     * @return array{run_id:int,status:string,stats:array,message:string}
     */
    public static function run(string $trigger, string $mode = 'weekly', ?array $sourceIds = null, ?string $csvFile = null, ?string $startedBy = null): array
    {
        $imp = new self();
        return $imp->execute($trigger, $mode, $sourceIds, $csvFile, $startedBy);
    }

    public static function lockFile(): string
    {
        return RT_STORAGE . '/locks/import.lock';
    }

    public static function isRunning(): bool
    {
        $fh = @fopen(self::lockFile(), 'c');
        if (!$fh) {
            return false;
        }
        $free = flock($fh, LOCK_EX | LOCK_NB);
        if ($free) {
            flock($fh, LOCK_UN);
        }
        fclose($fh);
        return !$free;
    }

    private function execute(string $trigger, string $mode, ?array $sourceIds, ?string $csvFile, ?string $startedBy): array
    {
        $this->mode = $mode;
        $this->stats = array_fill_keys(self::STAT_KEYS, 0);
        $this->lock = fopen(self::lockFile(), 'c');
        if (!$this->lock || !flock($this->lock, LOCK_EX | LOCK_NB)) {
            return ['run_id' => 0, 'status' => 'locked', 'stats' => $this->stats,
                'message' => 'Another import is already running. Nothing was changed.'];
        }
        try {
            // We hold the lock, so any "running" row is left over from a crashed process.
            Db::q("UPDATE import_runs SET status = 'abandoned', finished_at = ?, message = 'Process ended without finishing (crash or timeout).' WHERE status = 'running'", [now_utc()]);
            $this->runId = Db::insert('import_runs', [
                'trigger_type' => $trigger, 'mode' => $mode, 'status' => 'running', 'started_at' => now_utc(), 'started_by' => $startedBy,
            ]);
            $this->log('info', "Import started ({$trigger}, {$mode})");

            $params = [];
            if ($sourceIds !== null) {
                $sql = 'SELECT * FROM sources WHERE id IN ' . Db::in('s', $sourceIds, $params);
            } elseif ($mode === 'daily') {
                $sql = "SELECT * FROM sources WHERE enabled = 1 AND daily_check = 1 AND adapter <> 'csv' AND access_status = 'active'";
            } else {
                $sql = "SELECT * FROM sources WHERE enabled = 1 AND adapter <> 'csv' AND access_status = 'active'";
            }
            $sources = Db::all($sql . ' ORDER BY id', $params);
            if (!$sources) {
                $this->log('warning', 'No enabled sources to import.');
            }
            $failures = [];
            foreach ($sources as $src) {
                $ok = $this->processSource($src, $csvFile);
                if (!$ok) {
                    $failures[] = $src['name'] . ': ' . (string) Db::val('SELECT last_error FROM sources WHERE id = ?', [$src['id']]);
                }
            }
            $status = !$sources ? 'success' : (count($failures) === 0 ? 'success' : (count($failures) === count($sources) ? 'failed' : 'partial'));
            $msg = $this->summary();
            Db::update('import_runs', ['status' => $status, 'finished_at' => now_utc(), 'stats' => json_encode($this->stats), 'message' => $msg], 'id = :id', ['id' => $this->runId]);
            $this->log('info', 'Import finished: ' . $status . ' — ' . $msg);
            if ($failures && cfg('import.alert_on_failure', true)) {
                Mailer::toAdmin(
                    'Import ' . $status . ': ' . count($failures) . ' source(s) failed',
                    "The {$mode} event import finished with status \"{$status}\".\n\nFailed sources:\n- " . implode("\n- ", $failures)
                    . "\n\nExisting events from these sources were left unchanged.\n\nSummary: {$msg}\n\nDetails: " . abs_url('/admin/?page=imports&id=' . $this->runId) . "\n"
                );
            }
            return ['run_id' => $this->runId, 'status' => $status, 'stats' => $this->stats, 'message' => $msg];
        } catch (\Throwable $e) {
            if ($this->runId) {
                Db::update('import_runs', ['status' => 'failed', 'finished_at' => now_utc(), 'stats' => json_encode($this->stats), 'message' => 'Fatal: ' . $e->getMessage()], 'id = :id', ['id' => $this->runId]);
                $this->log('error', 'Fatal: ' . $e->getMessage(), ['trace' => $e->getTraceAsString()]);
            }
            app_log('import', 'FATAL ' . $e->getMessage());
            if (cfg('import.alert_on_failure', true)) {
                Mailer::toAdmin('Import failed', "The event import stopped with an error:\n\n" . $e->getMessage() . "\n\nNo partial changes were left behind for the record being processed.\n");
            }
            return ['run_id' => $this->runId, 'status' => 'failed', 'stats' => $this->stats, 'message' => $e->getMessage()];
        } finally {
            flock($this->lock, LOCK_UN);
            fclose($this->lock);
        }
    }

    private function summary(): string
    {
        $s = $this->stats;
        return sprintf('%d fetched, %d new (%d published, %d held for review), %d updated, %d unchanged, %d matched to existing, %d conflicts, %d filtered, %d outside Texas, %d no location, %d errors; %d/%d sources OK',
            $s['fetched'], $s['created'], $s['published'], $s['drafted'], $s['updated'], $s['unchanged'], $s['matched'], $s['conflicts'],
            $s['skipped_filter'], $s['skipped_outside_texas'], $s['skipped_no_location'], $s['record_errors'] + $s['skipped_invalid'],
            $s['sources_ok'], $s['sources_ok'] + $s['sources_failed']);
    }

    private function log(string $level, string $msg, array $ctx = [], ?int $sourceId = null): void
    {
        if ($this->runId) {
            Db::insert('import_logs', [
                'run_id' => $this->runId, 'source_id' => $sourceId, 'level' => $level,
                'message' => mb_substr($msg, 0, 1000), 'context' => $ctx ? json_encode($ctx, JSON_UNESCAPED_SLASHES) : null,
                'created_at' => now_utc(),
            ]);
        }
        if (PHP_SAPI === 'cli' && getenv('RT_QUIET') !== '1') {
            fwrite(STDOUT, '[' . strtoupper($level) . '] ' . $msg . "\n");
        }
    }

    public static function adapterFor(array $src, ?callable $log = null): Adapter
    {
        $map = [
            'tribe_rest' => Adapters\TribeRestAdapter::class,
            'ical'       => Adapters\IcalAdapter::class,
            'jsonld'     => Adapters\JsonLdAdapter::class,
            'csv'        => Adapters\CsvAdapter::class,
        ];
        $cls = $map[$src['adapter']] ?? null;
        if ($cls === null) {
            throw new \RuntimeException('Unknown adapter: ' . $src['adapter']);
        }
        return new $cls($src, $log);
    }

    public static function adapters(): array
    {
        return [
            'tribe_rest' => Adapters\TribeRestAdapter::describe(),
            'ical'       => Adapters\IcalAdapter::describe(),
            'jsonld'     => Adapters\JsonLdAdapter::describe(),
            'csv'        => Adapters\CsvAdapter::describe(),
        ];
    }

    // ------------------------------------------------------------------ per source

    private function processSource(array $src, ?string $csvFile): bool
    {
        $sid = (int) $src['id'];
        $this->log('info', 'Fetching ' . $src['name'], [], $sid);
        $adapter = self::adapterFor($src, function (string $level, string $msg) use ($sid): void {
            $this->log($level, $msg, [], $sid);
        });
        if ($adapter instanceof CsvAdapter) {
            if ($csvFile === null) {
                $this->log('warning', 'CSV source needs an uploaded file; skipped.', [], $sid);
                return true;
            }
            $adapter->setFile($csvFile);
        }
        Db::update('sources', ['last_run_at' => now_utc()], 'id = :id', ['id' => $sid]);
        try {
            $records = $adapter->fetch();
        } catch (\Throwable $e) {
            $this->stats['sources_failed']++;
            $this->log('error', 'Source failed — existing events left unchanged: ' . $e->getMessage(), [], $sid);
            Db::q('UPDATE sources SET last_error = ?, consecutive_failures = consecutive_failures + 1, updated_at = ? WHERE id = ?',
                [mb_substr($e->getMessage(), 0, 1000), now_utc(), $sid]);
            return false;
        }
        $n = count($records);
        $this->stats['fetched'] += $n;
        $prev = (int) ($src['last_record_count'] ?? 0);
        if ($n === 0 && $prev > 3) {
            $this->log('warning', "Source returned 0 records (previously {$prev}). Nothing was removed or canceled.", [], $sid);
        }
        if ($this->mode === 'daily') {
            $today = Dates::today();
            $limit = date('Y-m-d', strtotime($today . ' +7 days'));
            $records = array_values(array_filter($records, static fn($r) => ($r['start_date'] ?? '') <= $limit && ($r['end_date'] ?? '') >= $today));
            $this->log('info', count($records) . ' record(s) fall within the next 7 days', [], $sid);
        }
        foreach ($records as $rec) {
            try {
                Db::tx(fn() => $this->processRecord($src, $rec, $adapter));
            } catch (\Throwable $e) {
                $this->stats['record_errors']++;
                $this->log('error', 'Record "' . ($rec['title'] ?? '?') . '" failed: ' . $e->getMessage(), ['uid' => $rec['uid'] ?? null], $sid);
            }
        }
        $this->stats['sources_ok']++;
        Db::update('sources', [
            'last_success_at' => now_utc(), 'last_error' => null, 'consecutive_failures' => 0,
            'last_record_count' => $n, 'updated_at' => now_utc(),
        ], 'id = :id', ['id' => $sid]);
        $this->log('info', "{$src['name']}: {$n} record(s) processed", [], $sid);
        return true;
    }

    // ------------------------------------------------------------------ per record

    /** Canonical, stable hash of a record (key order independent). */
    public static function hashRecord(array $rec): string
    {
        $norm = static function ($v) use (&$norm) {
            if (is_array($v)) {
                if (!array_is_list($v)) {
                    ksort($v);
                }
                return array_map($norm, $v);
            }
            return $v;
        };
        return hash('sha256', json_encode($norm($rec), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    }

    private function processRecord(array $src, array $rec, Adapter $adapter): void
    {
        $sid = (int) $src['id'];
        $rec = $this->sanitize($rec);
        if ($rec === null) {
            $this->stats['skipped_invalid']++;
            return;
        }
        $hash = self::hashRecord($rec);
        $sr = Db::one('SELECT * FROM source_records WHERE source_id = ? AND source_uid = ? FOR UPDATE', [$sid, $rec['uid']]);

        // Idempotency: identical payload → just record that we saw it.
        if ($sr && $sr['payload_hash'] === $hash) {
            Db::update('source_records', ['last_seen_at' => now_utc()], 'id = :id', ['id' => $sr['id']]);
            if ($sr['event_id']) {
                Db::update('events', ['last_verified_at' => now_utc()], 'id = :id', ['id' => $sr['event_id']]);
            }
            $this->stats['unchanged']++;
            return;
        }

        if ($reason = $adapter->filterReason($rec)) {
            $this->saveSourceRecord($sr, $sid, $rec, $hash, 'skipped', $reason, $sr['event_id'] ?? null);
            $this->stats['skipped_filter']++;
            return;
        }

        $verdict = Geo::texasVerdict($rec['venue']);
        if ($verdict === 'no') {
            $this->saveSourceRecord($sr, $sid, $rec, $hash, 'skipped', 'outside Texas (' . ($rec['venue']['state'] ?? $rec['venue']['postal_code'] ?? '?') . ')', $sr['event_id'] ?? null);
            $this->stats['skipped_outside_texas']++;
            return;
        }
        if ($verdict === 'unknown') {
            $cfg = json_decode((string) $src['config'], true) ?: [];
            if (($cfg['unknown_location'] ?? 'skip') === 'review' && !($sr && $sr['state'] === 'review')) {
                $srId = $this->saveSourceRecord($sr, $sid, $rec, $hash, 'review', 'location not stated', null);
                $this->review('import_ambiguous', 'Location not stated: ' . $rec['title'] . ' (' . $rec['start_date'] . ')', null, $srId,
                    ['record' => $rec, 'source' => $src['name'], 'problem' => 'The source does not say where this event takes place, so it cannot be confirmed as a Texas event.'],
                    'noloc|' . $sid . '|' . $rec['uid'] . '|' . $hash);
                $this->stats['review']++;
            } else {
                $this->saveSourceRecord($sr, $sid, $rec, $hash, 'skipped', 'location not stated', null);
                $this->stats['skipped_no_location']++;
            }
            return;
        }

        // Known record already linked to an event → update it.
        if ($sr && $sr['event_id']) {
            $event = Db::one('SELECT * FROM events WHERE id = ?', [$sr['event_id']]);
            if ($event) {
                $this->saveSourceRecord($sr, $sid, $rec, $hash, 'linked', null, (int) $event['id']);
                $this->updateEvent($event, $rec, $src);
                return;
            }
        }

        // New (or previously unlinked) record → look for an existing event.
        $match = $this->findMatch($rec);
        if ($match['type'] === 'same') {
            $srId = $this->saveSourceRecord($sr, $sid, $rec, $hash, 'linked', null, (int) $match['event']['id']);
            $this->stats['matched']++;
            $this->log('info', 'Matched "' . $rec['title'] . '" to existing event #' . $match['event']['id'], [], $sid);
            $this->updateEvent($match['event'], $rec, $src);
            return;
        }
        if ($match['type'] === 'ambiguous') {
            $srId = $this->saveSourceRecord($sr, $sid, $rec, $hash, 'review', 'possible duplicate', null);
            $this->review('import_ambiguous', 'Possible duplicate: ' . $rec['title'] . ' (' . $rec['start_date'] . ')', null, $srId, [
                'record' => $rec, 'source' => $src['name'],
                'candidates' => array_map(static fn($e) => ['id' => (int) $e['id'], 'title' => $e['title'], 'start_date' => $e['start_date'], 'city' => $e['city']], $match['candidates']),
                'problem' => 'This record looks like an existing event, but the match is not certain.',
            ], 'dup|' . $sid . '|' . $rec['uid'] . '|' . $hash);
            $this->stats['review']++;
            return;
        }
        $eventId = $this->createEvent($rec, $src, $match['related'] ?? null);
        $this->saveSourceRecord($sr, $sid, $rec, $hash, 'linked', null, $eventId);
    }

    /** Validate/normalize a record from an adapter. */
    private function sanitize(array $rec): ?array
    {
        $rec['uid'] = mb_substr(trim((string) ($rec['uid'] ?? '')), 0, 255);
        $rec['title'] = clean_str($rec['title'] ?? null, 255);
        $rec['start_date'] = valid_date($rec['start_date'] ?? null);
        $rec['end_date'] = valid_date($rec['end_date'] ?? null) ?? $rec['start_date'];
        if ($rec['uid'] === '' || !$rec['title'] || !$rec['start_date']) {
            return null;
        }
        if ($rec['end_date'] < $rec['start_date']) {
            $rec['end_date'] = $rec['start_date'];
        }
        // Reject absurd ranges (e.g. a whole-year "event") — route nothing, just skip.
        if ((strtotime($rec['end_date']) - strtotime($rec['start_date'])) > 86400 * 60) {
            return null;
        }
        foreach (['official_url', 'ticket_url', 'image_url', 'source_url'] as $k) {
            $rec[$k] = valid_url($rec[$k] ?? null);
        }
        $rec['price_text'] = clean_str($rec['price_text'] ?? null, 255);
        $rec['description'] = clean_text($rec['description'] ?? null, 4000);
        $rec['status'] = in_array($rec['status'] ?? null, ['scheduled', 'canceled', 'postponed'], true) ? $rec['status'] : null;
        $v = $rec['venue'] ?? [];
        $rec['venue'] = [
            'name' => clean_str($v['name'] ?? null, 255), 'address' => clean_str($v['address'] ?? null, 255),
            'city' => clean_str($v['city'] ?? null, 120), 'state' => clean_str($v['state'] ?? null, 20),
            'postal_code' => clean_str($v['postal_code'] ?? null, 10), 'country' => clean_str($v['country'] ?? null, 60),
            'lat' => isset($v['lat']) && is_numeric($v['lat']) ? round((float) $v['lat'], 6) : null,
            'lng' => isset($v['lng']) && is_numeric($v['lng']) ? round((float) $v['lng'], 6) : null,
        ];
        if (Geo::isTexasState($rec['venue']['state'])) {
            $rec['venue']['state'] = 'TX';
        }
        if (!empty($rec['organizer']) && is_array($rec['organizer'])) {
            $o = $rec['organizer'];
            $rec['organizer'] = ['name' => clean_str($o['name'] ?? null, 255), 'website' => valid_url($o['website'] ?? null),
                'email' => valid_email($o['email'] ?? null), 'phone' => clean_str($o['phone'] ?? null, 40)];
            if (!$rec['organizer']['name']) {
                $rec['organizer'] = null;
            }
        } else {
            $rec['organizer'] = null;
        }
        $perfs = [];
        foreach ((array) ($rec['performances'] ?? []) as $p) {
            $s = $p['start'] ?? '';
            if (preg_match('/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$/', $s)) {
                $perfs[] = ['start' => strlen($s) === 16 ? $s . ':00' : $s,
                    'end' => (isset($p['end']) && preg_match('/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})?$/', (string) $p['end'])) ? (strlen($p['end']) === 16 ? $p['end'] . ':00' : $p['end']) : null,
                    'label' => clean_str($p['label'] ?? null, 160)];
            }
        }
        usort($perfs, static fn($a, $b) => strcmp($a['start'], $b['start']));
        $rec['performances'] = $perfs;
        $rec['categories'] = array_values(array_filter(array_map(static fn($c) => clean_str($c, 80), (array) ($rec['categories'] ?? []))));
        return $rec;
    }

    private function saveSourceRecord(?array $sr, int $sid, array $rec, string $hash, string $state, ?string $reason, ?int $eventId): int
    {
        $now = now_utc();
        if ($sr) {
            Db::update('source_records', [
                'payload' => json_encode($rec, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), 'payload_hash' => $hash,
                'state' => $state, 'skip_reason' => $reason, 'event_id' => $eventId,
                'last_seen_at' => $now, 'last_changed_at' => $now,
            ], 'id = :id', ['id' => $sr['id']]);
            return (int) $sr['id'];
        }
        return Db::insert('source_records', [
            'source_id' => $sid, 'source_uid' => $rec['uid'], 'event_id' => $eventId, 'state' => $state, 'skip_reason' => $reason,
            'payload' => json_encode($rec, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), 'payload_hash' => $hash,
            'first_seen_at' => $now, 'last_seen_at' => $now, 'last_changed_at' => $now,
        ]);
    }

    /**
     * @return array{type:string, event?:array, candidates?:array, related?:?array}
     */
    public function findMatch(array $rec): array
    {
        $rows = Db::all('SELECT e.*, v.city FROM events e LEFT JOIN venues v ON v.id = e.venue_id
            WHERE e.start_date <= DATE_ADD(?, INTERVAL 1 DAY) AND e.end_date >= DATE_SUB(?, INTERVAL 1 DAY)',
            [$rec['end_date'], $rec['start_date']]);
        $city = Matcher::normCity($rec['venue']['city'] ?? null);
        $strong = []; $weak = []; $related = null;
        foreach ($rows as $e) {
            $cmp = Matcher::compare($rec['title'], $e['title']);
            $ecity = Matcher::normCity($e['city']);
            $cityKnown = $city !== '' && $ecity !== '';
            $cityMatch = $cityKnown && $city === $ecity;
            if ($cmp === 'same' && $cityMatch) {
                $strong[] = $e;
            } elseif ($cmp === 'same' && !$cityKnown) {
                $weak[] = $e;
            } elseif ($cmp === 'related' && $cityMatch && $related === null) {
                $related = $e;
            }
        }
        if (count($strong) === 1 && !$weak) {
            return ['type' => 'same', 'event' => $strong[0]];
        }
        if (count($strong) > 1 || $weak) {
            return ['type' => 'ambiguous', 'candidates' => array_merge($strong, $weak)];
        }
        return ['type' => 'none', 'related' => $related];
    }

    private function createEvent(array $rec, array $src, ?array $related): int
    {
        $venueId = self::upsertVenue($rec['venue']);
        $venue = $venueId ? Db::one('SELECT * FROM venues WHERE id = ?', [$venueId]) : null;
        $tz = $venue['timezone'] ?? 'America/Chicago';
        $orgId = self::upsertOrganizer($rec['organizer']);

        $assocSlug = $rec['association'] ?? Classifier::associationSlug($rec['title'], $rec['categories']);
        $assocId = Classifier::idFor('associations', $assocSlug) ?? ($src['default_association_id'] ? (int) $src['default_association_id'] : null);
        $level = $rec['level'] ?? Classifier::levelFromText($rec['title'], $rec['categories']);
        if ($level === null && $assocId) {
            $level = Db::val('SELECT level FROM associations WHERE id = ?', [$assocId]);
        }
        $level = $level ?? ($src['default_level'] ?: null);
        $typeId = Classifier::idFor('event_types', Classifier::eventTypeSlug($rec['title'], $rec['categories']));

        $missing = self::missingForPublish($rec, $venue);
        $publish = !$missing && (int) $src['auto_publish'] === 1;
        $now = now_utc();
        $groupId = null;
        if ($related) {
            $groupId = $related['group_id'] ? (int) $related['group_id'] : Db::insert('event_groups', ['name' => $related['title'], 'created_at' => $now]);
            if (!$related['group_id']) {
                Db::update('events', ['group_id' => $groupId], 'id = :id', ['id' => $related['id']]);
            }
        }
        $id = Db::insert('events', [
            'slug' => self::uniqueSlug($rec['title'], $rec['start_date']),
            'title' => $rec['title'],
            'description' => $rec['description'],
            'event_type_id' => $typeId, 'association_id' => $assocId, 'level' => $level,
            'venue_id' => $venueId, 'organizer_id' => $orgId, 'group_id' => $groupId,
            'start_date' => $rec['start_date'], 'end_date' => $rec['end_date'], 'timezone' => $tz,
            'status' => $rec['status'] ?? 'scheduled',
            'official_url' => $rec['official_url'], 'ticket_url' => $rec['ticket_url'],
            'ticket_url_verified' => 0,
            'price_text' => $rec['price_text'], 'image_url' => $rec['image_url'],
            'publish_state' => $publish ? 'published' : 'draft',
            'source_id' => (int) $src['id'], 'source_label' => $src['name'], 'source_url' => $rec['source_url'],
            'last_verified_at' => $now, 'locked_fields' => null,
            'created_at' => $now, 'updated_at' => $now,
        ]);
        self::replacePerformances($id, self::perfsToZone($rec, $tz));
        self::history($id, 'import:' . $src['slug'], 'created', null, $publish ? 'published' : 'draft (needs review)');
        $this->stats['created']++;
        if ($publish) {
            $this->stats['published']++;
            $this->log('info', 'Published new event #' . $id . ' "' . $rec['title'] . '"', [], (int) $src['id']);
        } else {
            $this->stats['drafted']++;
            $why = $missing ? 'Missing: ' . implode(', ', $missing) : 'Source is set to hold new events for review';
            $this->review('import_incomplete', 'Review imported event: ' . $rec['title'] . ' (' . $rec['start_date'] . ')', $id, null,
                ['source' => $src['name'], 'problem' => $why, 'missing' => $missing], 'incomplete|' . $id);
            $this->log('info', 'Held new event #' . $id . ' "' . $rec['title'] . '" for review — ' . $why, [], (int) $src['id']);
        }
        return $id;
    }

    /** Required for automatic publishing. Returns human-readable list of what is missing. */
    public static function missingForPublish(array $rec, ?array $venue): array
    {
        $m = [];
        if (!$venue || empty($venue['city'])) {
            $m[] = 'venue city';
        }
        if (empty($rec['official_url']) && empty($rec['source_url'])) {
            $m[] = 'official or source link';
        }
        $today = Dates::today();
        if ($rec['end_date'] < $today) {
            $m[] = 'event is already over';
        }
        if ($rec['start_date'] > date('Y-m-d', strtotime($today . ' +2 years'))) {
            $m[] = 'date more than two years away (check year)';
        }
        return $m;
    }

    /** Apply a record to an existing event, honouring locks and source priority. */
    private function updateEvent(array $event, array $rec, array $src): void
    {
        $sid = (int) $src['id'];
        $actor = 'import:' . $src['slug'];
        $locked = json_decode((string) $event['locked_fields'], true) ?: [];
        $isPrimary = (int) $event['source_id'] === $sid || $event['source_id'] === null;
        $changes = [];
        $conflicts = 0;

        $incoming = [
            'title' => $rec['title'],
            'start_date' => $rec['start_date'],
            'end_date' => $rec['end_date'],
            'official_url' => $rec['official_url'],
            'ticket_url' => $rec['ticket_url'],
            'price_text' => $rec['price_text'],
            'description' => $rec['description'],
            'image_url' => $rec['image_url'],
            'source_url' => $rec['source_url'],
            'status' => $rec['status'],   // null unless the source said so explicitly
        ];
        if ($rec['venue']['city'] || $rec['venue']['name']) {
            $vid = self::upsertVenue($rec['venue']);
            if ($vid) {
                $incoming['venue_id'] = $vid;
            }
        }
        if ($rec['organizer']) {
            $incoming['organizer_id'] = self::upsertOrganizer($rec['organizer']);
        }
        foreach ($incoming as $field => $new) {
            if ($new === null || $new === '') {
                continue;   // a source going quiet never erases information
            }
            $cur = $event[$field];
            if ((string) $cur === (string) $new) {
                continue;
            }
            // Fill-only fields from secondary sources; description/image never overwrite.
            $empty = $cur === null || $cur === '';
            if (in_array($field, $locked, true)) {
                $conflicts += $this->conflict($event, $field, $cur, $new, $src, 'This field was edited by an administrator and is locked.');
                continue;
            }
            if (in_array($field, ['description', 'image_url', 'source_url'], true) && !$empty) {
                continue;
            }
            if ($field === 'status' && $new === 'scheduled' && $cur === 'scheduled') {
                continue;
            }
            if ($isPrimary || $empty) {
                $changes[$field] = $new;
            } else {
                $conflicts += $this->conflict($event, $field, $cur, $new, $src, 'Another source already supplied this value.');
            }
        }
        // Performances (show times).
        if ($rec['performances']) {
            $tz = $event['timezone'];
            if (isset($changes['venue_id'])) {
                $tz = (string) Db::val('SELECT timezone FROM venues WHERE id = ?', [$changes['venue_id']]) ?: $tz;
                $changes['timezone'] = $tz;
            }
            $newPerfs = self::perfsToZone($rec, $tz);
            $curPerfs = Db::all('SELECT starts_at AS start, ends_at AS end, label FROM performances WHERE event_id = ? ORDER BY starts_at', [$event['id']]);
            if (json_encode($newPerfs) !== json_encode($curPerfs)) {
                if (in_array('performances', $locked, true)) {
                    $conflicts += $this->conflict($event, 'performances', json_encode($curPerfs), json_encode($newPerfs), $src, 'Show times were edited by an administrator.');
                } elseif ($isPrimary || !$curPerfs) {
                    self::replacePerformances((int) $event['id'], $newPerfs);
                    self::history((int) $event['id'], $actor, 'performances', json_encode($curPerfs), json_encode($newPerfs));
                    $changes['updated_at'] = now_utc();
                }
            }
        }
        // A draft held only for missing data is published once the data arrives.
        if ($event['publish_state'] === 'draft' && !in_array('publish_state', $locked, true) && (int) $src['auto_publish'] === 1 && !$event['is_legacy']) {
            $venue = Db::one('SELECT * FROM venues WHERE id = ?', [$changes['venue_id'] ?? $event['venue_id']]);
            $merged = array_merge($event, $changes);
            $openIncomplete = Db::val("SELECT id FROM review_items WHERE kind = 'import_incomplete' AND status = 'open' AND event_id = ?", [$event['id']]);
            if ($openIncomplete && !self::missingForPublish(['official_url' => $merged['official_url'], 'source_url' => $merged['source_url'], 'start_date' => $merged['start_date'], 'end_date' => $merged['end_date']], $venue)) {
                $changes['publish_state'] = 'published';
                Db::update('review_items', ['status' => 'resolved', 'resolved_at' => now_utc(), 'resolution_note' => 'Completed by a later import'], 'id = :id', ['id' => $openIncomplete]);
            }
        }
        $changes['last_verified_at'] = now_utc();
        if (count($changes) > 1 || isset($changes['updated_at'])) {
            $changes['updated_at'] = now_utc();
            foreach ($changes as $f => $v) {
                if (!in_array($f, ['updated_at', 'last_verified_at'], true)) {
                    self::history((int) $event['id'], $actor, $f, $event[$f] ?? null, $v);
                }
            }
            $this->stats['updated']++;
            $this->log('info', 'Updated event #' . $event['id'] . ' "' . $event['title'] . '": ' . implode(', ', array_diff(array_keys($changes), ['updated_at', 'last_verified_at'])), [], $sid);
        }
        Db::update('events', $changes, 'id = :id', ['id' => $event['id']]);
        $this->stats['conflicts'] += $conflicts;
    }

    private function conflict(array $event, string $field, $cur, $new, array $src, string $why): int
    {
        $created = $this->review('import_conflict', 'Conflict on "' . $event['title'] . '": ' . $field, (int) $event['id'], null, [
            'field' => $field, 'current' => $cur, 'incoming' => $new, 'source' => $src['name'], 'source_id' => (int) $src['id'], 'problem' => $why,
        ], 'conflict|' . $event['id'] . '|' . $field . '|' . sha1((string) $new));
        return $created ? 1 : 0;
    }

    /** Insert a review item unless an identical one already exists. Returns true when created. */
    private function review(string $kind, string $summary, ?int $eventId, ?int $srId, array $payload, string $dedupe): bool
    {
        $st = Db::q('INSERT IGNORE INTO review_items (kind, status, event_id, source_record_id, summary, payload, dedupe_key, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            [$kind, 'open', $eventId, $srId, mb_substr($summary, 0, 255), json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), hash('sha256', $dedupe), now_utc()]);
        return $st->rowCount() > 0;
    }

    /**
     * Admin action: turn a source record held for review into a DRAFT event
     * (never auto-published), and link the record to it.
     */
    public static function createDraftFromSourceRecord(int $srId): int
    {
        $sr = Db::one('SELECT * FROM source_records WHERE id = ?', [$srId]);
        if (!$sr) {
            throw new \RuntimeException('Source record not found');
        }
        $src = Db::one('SELECT * FROM sources WHERE id = ?', [$sr['source_id']]);
        $rec = json_decode((string) $sr['payload'], true);
        $src['auto_publish'] = 0;
        $imp = new self();
        $imp->stats = array_fill_keys(self::STAT_KEYS, 0);
        return Db::tx(function () use ($imp, $rec, $src, $sr) {
            $id = $imp->createEvent($rec, $src, null);
            Db::update('source_records', ['event_id' => $id, 'state' => 'linked'], 'id = :id', ['id' => $sr['id']]);
            return $id;
        });
    }

    /** Admin action: link a held source record to an existing event (fills empty fields only). */
    public static function linkSourceRecord(int $srId, int $eventId): void
    {
        $sr = Db::one('SELECT * FROM source_records WHERE id = ?', [$srId]);
        $event = Db::one('SELECT * FROM events WHERE id = ?', [$eventId]);
        if (!$sr || !$event) {
            throw new \RuntimeException('Record or event not found');
        }
        $src = Db::one('SELECT * FROM sources WHERE id = ?', [$sr['source_id']]);
        $imp = new self();
        $imp->stats = array_fill_keys(self::STAT_KEYS, 0);
        Db::tx(function () use ($imp, $sr, $event, $src) {
            Db::update('source_records', ['event_id' => $event['id'], 'state' => 'linked'], 'id = :id', ['id' => $sr['id']]);
            $imp->updateEvent($event, json_decode((string) $sr['payload'], true), $src);
        });
    }

    // ------------------------------------------------------------------ shared helpers (also used by admin)

    /** Convert source-local performance times into the venue's zone. */
    public static function perfsToZone(array $rec, string $tz): array
    {
        $srcTz = $rec['timezone'] ?? null;
        $out = [];
        foreach ($rec['performances'] as $p) {
            $s = ($srcTz && $srcTz !== $tz) ? Dates::toLocal($p['start'], $tz, $srcTz) : $p['start'];
            $e = $p['end'] ? (($srcTz && $srcTz !== $tz) ? Dates::toLocal($p['end'], $tz, $srcTz) : $p['end']) : null;
            $out[] = ['start' => $s, 'end' => $e, 'label' => $p['label']];
        }
        return $out;
    }

    public static function replacePerformances(int $eventId, array $perfs): void
    {
        Db::q('DELETE FROM performances WHERE event_id = ?', [$eventId]);
        foreach ($perfs as $p) {
            Db::insert('performances', ['event_id' => $eventId, 'starts_at' => $p['start'], 'ends_at' => $p['end'], 'label' => $p['label']]);
        }
    }

    public static function history(int $eventId, string $actor, string $field, $old, $new): void
    {
        Db::insert('event_history', [
            'event_id' => $eventId, 'actor' => $actor, 'field' => $field,
            'old_value' => $old === null ? null : mb_substr((string) $old, 0, 5000),
            'new_value' => $new === null ? null : mb_substr((string) $new, 0, 5000),
            'created_at' => now_utc(),
        ]);
    }

    public static function uniqueSlug(string $title, string $startDate): string
    {
        $year = substr($startDate, 0, 4);
        $base = slugify($title, 100);
        if (!str_contains($base, $year)) {
            $base .= '-' . $year;
        }
        $slug = $base;
        $i = 2;
        while (Db::val('SELECT 1 FROM events WHERE slug = ?', [$slug]) || Db::val('SELECT 1 FROM redirects WHERE from_path = ?', ['/rodeos/' . $slug . '/'])) {
            $slug = $base . '-' . $i++;
        }
        return $slug;
    }

    public static function venueKey(?string $name, ?string $city): string
    {
        return slugify((string) ($name ?: 'venue-not-listed'), 150) . '|' . slugify((string) $city, 80);
    }

    /** Find or create a venue; geocodes new ones. Never overwrites manual edits. */
    public static function upsertVenue(array $v): ?int
    {
        if (empty($v['city']) && empty($v['name'])) {
            return null;
        }
        $key = self::venueKey($v['name'] ?? null, $v['city'] ?? null);
        $row = Db::one('SELECT * FROM venues WHERE norm_key = ?', [$key]);
        if ($row) {
            if (!(int) $row['manually_edited']) {
                $fill = [];
                foreach (['address', 'postal_code'] as $f) {
                    if (empty($row[$f]) && !empty($v[$f])) {
                        $fill[$f] = $v[$f];
                    }
                }
                if ($row['location_precision'] !== 'address' && isset($v['lat'], $v['lng']) && Geo::inTexasBox($v['lat'], $v['lng'])) {
                    $fill += ['lat' => $v['lat'], 'lng' => $v['lng'], 'location_precision' => 'address'];
                }
                if ($fill) {
                    $fill['updated_at'] = now_utc();
                    Db::update('venues', $fill, 'id = :id', ['id' => $row['id']]);
                }
            }
            return (int) $row['id'];
        }
        $lat = $v['lat'] ?? null; $lng = $v['lng'] ?? null; $county = null; $precision = 'none';
        if ($lat !== null && $lng !== null && Geo::inTexasBox((float) $lat, (float) $lng)) {
            $precision = 'address';
        } else {
            $lat = $lng = null;
        }
        $geo = null;
        if (!empty($v['city'])) {
            $q = implode(', ', array_filter([$v['name'] ?? null, $v['address'] ?? null, $v['city'], 'TX', $v['postal_code'] ?? null]));
            $geo = Geo::geocode($q);
            if (!$geo || ($geo['state'] ?? '') !== 'TX') {
                $geo = Geo::geocode($v['city'] . ', TX', true);
            }
            if ($geo && ($geo['state'] ?? '') !== 'TX') {
                $geo = null;
            }
        }
        if ($geo) {
            $county = $geo['county'];
            if ($lat === null) {
                $lat = $geo['lat']; $lng = $geo['lng']; $precision = $geo['precision'];
            }
        }
        $now = now_utc();
        return Db::insert('venues', [
            'norm_key' => $key, 'name' => $v['name'] ?? null, 'address' => $v['address'] ?? null, 'city' => $v['city'] ?? null,
            'county' => $county, 'state' => 'TX', 'postal_code' => $v['postal_code'] ?? ($geo['postal_code'] ?? null) ?: null,
            'lat' => $lat, 'lng' => $lng, 'location_precision' => $precision,
            'timezone' => Geo::timezoneFor($county, $lng !== null ? (float) $lng : null, $v['postal_code'] ?? ($geo['postal_code'] ?? null)),
            'region_id' => Geo::regionIdFor($lat !== null ? (float) $lat : null, $lng !== null ? (float) $lng : null),
            'created_at' => $now, 'updated_at' => $now,
        ]);
    }

    public static function upsertOrganizer(?array $o): ?int
    {
        if (!$o || empty($o['name'])) {
            return null;
        }
        $key = slugify($o['name'], 200);
        $row = Db::one('SELECT * FROM organizers WHERE norm_key = ?', [$key]);
        if ($row) {
            $fill = [];
            foreach (['website', 'email', 'phone'] as $f) {
                if (empty($row[$f]) && !empty($o[$f])) {
                    $fill[$f] = $o[$f];
                }
            }
            if ($fill) {
                $fill['updated_at'] = now_utc();
                Db::update('organizers', $fill, 'id = :id', ['id' => $row['id']]);
            }
            return (int) $row['id'];
        }
        $now = now_utc();
        return Db::insert('organizers', ['norm_key' => $key, 'name' => $o['name'], 'website' => $o['website'] ?? null,
            'email' => $o['email'] ?? null, 'phone' => $o['phone'] ?? null, 'created_at' => $now, 'updated_at' => $now]);
    }
}
