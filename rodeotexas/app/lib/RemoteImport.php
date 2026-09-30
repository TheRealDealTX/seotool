<?php
declare(strict_types=1);

namespace RT;

/**
 * Authenticated API used by the external weekly routine.
 *
 *   GET  /api/import/sources/   → the sources the routine should fetch (active + enabled, with adapter config)
 *   POST /api/import/           → {"source": "<slug>", "records": [...]}  or  {"source": "<slug>", "error": "…"}
 *
 * Authentication: "Authorization: Bearer <token>" (or "X-Import-Token: <token>").
 * Only a SHA-256 hash of the token is stored (settings.import_api_token_sha256); the
 * token is shown once in Admin → Account when generated. HTTPS is required in production.
 * The endpoint accepts DATA only (event records); every record goes through the normal
 * importer: validation, Texas check, dedupe, admin locks and review rules.
 */
final class RemoteImport
{
    public const SETTING = 'import_api_token_sha256';
    public const MAX_BODY = 5_000_000;
    public const MAX_RECORDS = 1000;

    /** Create a new token (replaces any previous one). Returns the plain token — show it once. */
    public static function generateToken(): string
    {
        $token = 'rt_' . bin2hex(random_bytes(24));
        Db::q('REPLACE INTO settings (name, value) VALUES (?, ?)', [self::SETTING, hash('sha256', $token)]);
        Db::q("REPLACE INTO settings (name, value) VALUES ('import_api_token_created', ?)", [now_utc()]);
        return $token;
    }

    public static function revokeToken(): void
    {
        Db::q("DELETE FROM settings WHERE name IN (?, 'import_api_token_created')", [self::SETTING]);
    }

    public static function tokenCreatedAt(): ?string
    {
        $v = Db::val("SELECT value FROM settings WHERE name = 'import_api_token_created'");
        return $v === null ? null : (string) $v;
    }

    public static function presentedToken(): string
    {
        $h = (string) ($_SERVER['HTTP_AUTHORIZATION'] ?? $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ?? '');
        if (preg_match('/^Bearer\s+(\S+)$/i', $h, $m)) {
            return $m[1];
        }
        return trim((string) ($_SERVER['HTTP_X_IMPORT_TOKEN'] ?? ''));
    }

    public static function authorized(): bool
    {
        $stored = Db::val('SELECT value FROM settings WHERE name = ?', [self::SETTING]);
        $given = self::presentedToken();
        return is_string($stored) && strlen($stored) === 64 && $given !== '' && hash_equals($stored, hash('sha256', $given));
    }

    /** Sources the routine should fetch itself (never CSV/push sources). */
    public static function sourcesForRoutine(): array
    {
        $rows = Db::all("SELECT slug, name, adapter, config, homepage FROM sources
            WHERE enabled = 1 AND access_status = 'active' AND adapter IN ('tribe_rest', 'ical', 'jsonld') ORDER BY id");
        $push = Db::all("SELECT slug, name, adapter FROM sources WHERE adapter = 'push' AND access_status = 'active' ORDER BY id");
        return ['fetch' => array_map(static function ($r) {
            $r['config'] = json_decode((string) $r['config'], true) ?: new \stdClass();
            return $r;
        }, $rows), 'push_only' => $push];
    }

    /**
     * Handle one POST body. @return array{0:int,1:array} [HTTP status, response]
     */
    public static function handle(string $body): array
    {
        if (strlen($body) > self::MAX_BODY) {
            return [413, ['error' => 'Body too large']];
        }
        $in = json_decode($body, true);
        if (!is_array($in) || !is_string($in['source'] ?? null)) {
            return [400, ['error' => 'Expected JSON {"source": "<slug>", "records": [...]} or {"source": "<slug>", "error": "..."}']];
        }
        $src = Db::one("SELECT * FROM sources WHERE slug = ? AND access_status = 'active' AND adapter IN ('tribe_rest', 'ical', 'jsonld', 'push')", [$in['source']]);
        if (!$src) {
            return [404, ['error' => 'Unknown or inactive source']];
        }
        if (isset($in['error'])) {
            $r = Importer::runPushed((int) $src['id'], null, mb_substr((string) $in['error'], 0, 500));
        } else {
            $records = $in['records'] ?? null;
            if (!is_array($records) || !array_is_list($records)) {
                return [400, ['error' => '"records" must be a JSON array']];
            }
            if (count($records) > self::MAX_RECORDS) {
                return [413, ['error' => 'Too many records (max ' . self::MAX_RECORDS . ' per request)']];
            }
            Geo::$budget = 10;   // keep the request short; missing map positions are filled on later runs
            $r = Importer::runPushed((int) $src['id'], $records, null);
            if ($r['status'] !== 'locked') {
                Geo::backfillVenues(5);
            }
        }
        $code = $r['status'] === 'locked' ? 409 : 200;
        return [$code, ['run_id' => $r['run_id'], 'status' => $r['status'], 'message' => $r['message'], 'stats' => $r['stats']]];
    }
}
