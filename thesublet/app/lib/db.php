<?php defined('APP') || exit;

const SCHEMA_VERSION = 2;

function db(): PDO
{
    static $pdo = null;
    if ($pdo) return $pdo;
    $c = cfg('db');
    if (($c['driver'] ?? 'mysql') === 'sqlite') {
        $pdo = new PDO('sqlite:' . $c['path']);
        $pdo->exec('PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL;');
    } else {
        $dsn = 'mysql:host=' . ($c['host'] ?? 'localhost') . ';dbname=' . $c['name'] . ';charset=utf8mb4';
        $pdo = new PDO($dsn, $c['user'], $c['pass'], [PDO::MYSQL_ATTR_INIT_COMMAND => "SET time_zone = '+00:00'"]);
    }
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
    db_migrate($pdo);
    return $pdo;
}

function is_sqlite(): bool
{
    return (cfg('db.driver') ?? 'mysql') === 'sqlite';
}

function q(string $sql, array $params = []): PDOStatement
{
    $st = db()->prepare($sql);
    $isList = array_is_list($params);
    $i = 0;
    foreach ($params as $k => $v) {
        $type = is_int($v) ? PDO::PARAM_INT : (is_null($v) ? PDO::PARAM_NULL : PDO::PARAM_STR);
        if (is_bool($v)) { $v = (int)$v; $type = PDO::PARAM_INT; }
        $st->bindValue($isList ? ++$i : ':' . ltrim($k, ':'), $v, $type);
    }
    $st->execute();
    return $st;
}

function row(string $sql, array $p = []): ?array
{
    $r = q($sql, $p)->fetch();
    return $r ?: null;
}

function rows(string $sql, array $p = []): array
{
    return q($sql, $p)->fetchAll();
}

function val(string $sql, array $p = [])
{
    $v = q($sql, $p)->fetchColumn();
    return $v === false ? null : $v;
}

function insert(string $table, array $data): int
{
    $cols = array_keys($data);
    $sql = 'INSERT INTO ' . $table . ' (' . implode(',', $cols) . ') VALUES (' . implode(',', array_fill(0, count($cols), '?')) . ')';
    q($sql, array_values($data));
    return (int)db()->lastInsertId();
}

function update(string $table, array $data, string $where, array $wp = []): int
{
    $set = implode(',', array_map(fn($c) => "$c = ?", array_keys($data)));
    return q("UPDATE $table SET $set WHERE $where", array_merge(array_values($data), $wp))->rowCount();
}

function now(): string
{
    return gmdate('Y-m-d H:i:s');
}

function db_migrate(PDO $pdo): void
{
    try {
        $v = (int)$pdo->query("SELECT v FROM settings WHERE k = 'schema_version'")->fetchColumn();
    } catch (Throwable $e) {
        $v = 0;
    }
    if ($v >= SCHEMA_VERSION) return;

    $sqlite = is_sqlite();
    $T = [
        '{PK}'   => $sqlite ? 'INTEGER PRIMARY KEY AUTOINCREMENT' : 'INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY',
        '{FK}'   => $sqlite ? 'INTEGER' : 'INT UNSIGNED',
        '{BLOB}' => $sqlite ? 'BLOB' : 'MEDIUMBLOB',
        '{DT}'   => $sqlite ? 'TEXT' : 'DATETIME',
        '{D}'    => $sqlite ? 'TEXT' : 'DATE',
        '{TXT}'  => $sqlite ? 'TEXT' : 'MEDIUMTEXT',
        '{ENG}'  => $sqlite ? '' : ' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci',
    ];
    $ddl = [
        "CREATE TABLE IF NOT EXISTS settings (k VARCHAR(64) NOT NULL PRIMARY KEY, v TEXT){ENG}",
        "CREATE TABLE IF NOT EXISTS owners (
            id {PK}, email VARCHAR(190) NOT NULL UNIQUE, name VARCHAR(120) NOT NULL DEFAULT '',
            phone VARCHAR(40) NOT NULL DEFAULT '', status VARCHAR(20) NOT NULL DEFAULT 'active',
            email_verified_at {DT} NULL, last_login_at {DT} NULL, created_at {DT} NOT NULL
        ){ENG}",
        "CREATE TABLE IF NOT EXISTS login_tokens (
            id {PK}, owner_id {FK} NOT NULL, token_hash CHAR(64) NOT NULL, expires_at {DT} NOT NULL,
            used_at {DT} NULL, created_at {DT} NOT NULL
        ){ENG}",
        "CREATE TABLE IF NOT EXISTS listings (
            id {PK}, owner_id {FK} NULL, slug VARCHAR(160) NOT NULL DEFAULT '',
            title VARCHAR(140) NOT NULL, description {TXT} NOT NULL,
            city VARCHAR(80) NOT NULL, city_slug VARCHAR(80) NOT NULL, state CHAR(2) NOT NULL,
            zip VARCHAR(10) NOT NULL DEFAULT '', neighborhood VARCHAR(80) NOT NULL DEFAULT '',
            property_type VARCHAR(20) NOT NULL, furnished TINYINT NOT NULL DEFAULT 1,
            rent INT NOT NULL, deposit INT NOT NULL DEFAULT 0, utilities_included TINYINT NOT NULL DEFAULT 0,
            available_from {D} NULL, available_to {D} NULL, min_stay INT NOT NULL DEFAULT 1,
            beds VARCHAR(10) NOT NULL DEFAULT '1', baths VARCHAR(10) NOT NULL DEFAULT '1',
            amenities TEXT, house_rules TEXT, pets VARCHAR(10) NOT NULL DEFAULT 'no',
            lat DECIMAL(9,5) NULL, lng DECIMAL(9,5) NULL,
            contact_name VARCHAR(120) NOT NULL DEFAULT '', contact_email VARCHAR(190) NOT NULL,
            contact_phone VARCHAR(40) NOT NULL DEFAULT '',
            tier VARCHAR(10) NOT NULL DEFAULT 'free', status VARCHAR(20) NOT NULL DEFAULT 'pending',
            reject_reason TEXT, admin_note TEXT,
            published_at {DT} NULL, expires_at {DT} NULL, reminder_sent_at {DT} NULL,
            views INT NOT NULL DEFAULT 0, ip VARCHAR(64) NOT NULL DEFAULT '',
            created_at {DT} NOT NULL, updated_at {DT} NOT NULL
        ){ENG}",
        "CREATE INDEX idx_listings_loc ON listings (status, state, city_slug)",
        "CREATE INDEX idx_listings_owner ON listings (owner_id)",
        "CREATE TABLE IF NOT EXISTS photos (
            id {PK}, listing_id {FK} NOT NULL, data {BLOB} NOT NULL, width INT NOT NULL DEFAULT 0,
            height INT NOT NULL DEFAULT 0, sort INT NOT NULL DEFAULT 0, created_at {DT} NOT NULL
        ){ENG}",
        "CREATE INDEX idx_photos_listing ON photos (listing_id, sort)",
        "CREATE TABLE IF NOT EXISTS payments (
            id {PK}, listing_id {FK} NULL, owner_id {FK} NULL, stripe_session_id VARCHAR(255) NOT NULL UNIQUE,
            kind VARCHAR(20) NOT NULL DEFAULT 'new', amount_cents INT NOT NULL DEFAULT 0, currency VARCHAR(8) NOT NULL DEFAULT 'usd',
            status VARCHAR(30) NOT NULL DEFAULT 'open', email VARCHAR(190) NOT NULL DEFAULT '', promo VARCHAR(80) NOT NULL DEFAULT '',
            created_at {DT} NOT NULL, completed_at {DT} NULL
        ){ENG}",
        "CREATE TABLE IF NOT EXISTS messages (
            id {PK}, listing_id {FK} NULL, kind VARCHAR(20) NOT NULL DEFAULT 'listing', sender_name VARCHAR(120) NOT NULL,
            sender_email VARCHAR(190) NOT NULL, body TEXT NOT NULL, ip VARCHAR(64) NOT NULL DEFAULT '',
            relayed TINYINT NOT NULL DEFAULT 0, created_at {DT} NOT NULL
        ){ENG}",
        "CREATE TABLE IF NOT EXISTS reports (
            id {PK}, listing_id {FK} NOT NULL, reason VARCHAR(40) NOT NULL, details TEXT,
            reporter_email VARCHAR(190) NOT NULL DEFAULT '', ip VARCHAR(64) NOT NULL DEFAULT '',
            resolved TINYINT NOT NULL DEFAULT 0, created_at {DT} NOT NULL
        ){ENG}",
        "CREATE TABLE IF NOT EXISTS rate_limits (id {PK}, k VARCHAR(190) NOT NULL, created_at {DT} NOT NULL){ENG}",
        "CREATE INDEX idx_rate ON rate_limits (k, created_at)",
        "CREATE TABLE IF NOT EXISTS email_log (
            id {PK}, to_addr VARCHAR(190) NOT NULL, subject VARCHAR(255) NOT NULL, status VARCHAR(10) NOT NULL,
            error TEXT, created_at {DT} NOT NULL
        ){ENG}",
        "CREATE TABLE IF NOT EXISTS sessions (id VARCHAR(128) NOT NULL PRIMARY KEY, data {TXT} NOT NULL, updated_at INT NOT NULL){ENG}",
    ];
    foreach ($ddl as $sql) {
        $sql = strtr($sql, $T);
        try {
            $pdo->exec($sql);
        } catch (PDOException $e) {
            // CREATE INDEX re-runs fail harmlessly when the index already exists
            if (stripos($sql, 'CREATE INDEX') !== 0) throw $e;
        }
    }
    // v2: directory (claimable) listings + claims
    if ($v < 2) {
        $cols = [
            "source VARCHAR(12) NOT NULL DEFAULT 'host'",
            "business_name VARCHAR(160) NOT NULL DEFAULT ''",
            "address_line VARCHAR(190) NOT NULL DEFAULT ''",
            "address_city VARCHAR(80) NOT NULL DEFAULT ''",
            "website VARCHAR(300) NOT NULL DEFAULT ''",
            "phone_public VARCHAR(40) NOT NULL DEFAULT ''",
            "category VARCHAR(80) NOT NULL DEFAULT ''",
            "place_ref VARCHAR(64) NOT NULL DEFAULT ''",
            "rank_score INT NOT NULL DEFAULT 0",
            "claimed_at {DT} NULL",
        ];
        foreach ($cols as $c) {
            try { $pdo->exec('ALTER TABLE listings ADD COLUMN ' . strtr($c, $T)); } catch (PDOException $e) { /* exists */ }
        }
        foreach ([
            "CREATE INDEX idx_listings_source ON listings (source, status)",
            "CREATE INDEX idx_listings_place ON listings (place_ref)",
        ] as $sql) { try { $pdo->exec($sql); } catch (PDOException $e) {} }
        $pdo->exec(strtr("CREATE TABLE IF NOT EXISTS claims (
            id {PK}, listing_id {FK} NOT NULL, name VARCHAR(120) NOT NULL, email VARCHAR(190) NOT NULL,
            phone VARCHAR(40) NOT NULL DEFAULT '', role VARCHAR(40) NOT NULL DEFAULT '', message TEXT,
            domain_match TINYINT NOT NULL DEFAULT 0, status VARCHAR(20) NOT NULL DEFAULT 'pending',
            ip VARCHAR(64) NOT NULL DEFAULT '', created_at {DT} NOT NULL, decided_at {DT} NULL
        ){ENG}", $T));
    }
    $st = $pdo->prepare($sqlite ? "INSERT OR REPLACE INTO settings (k, v) VALUES ('schema_version', ?)"
        : "REPLACE INTO settings (k, v) VALUES ('schema_version', ?)");
    $st->execute([(string)SCHEMA_VERSION]);
}

/** Settings stored in DB override config defaults. */
function setting(string $k, $default = null)
{
    if (!isset($GLOBALS['__settings'])) {
        $GLOBALS['__settings'] = [];
        foreach (rows('SELECT k, v FROM settings') as $r) $GLOBALS['__settings'][$r['k']] = $r['v'];
    }
    $c = $GLOBALS['__settings'];
    return (isset($c[$k]) && $c[$k] !== '') ? $c[$k] : $default;
}

function setting_set(string $k, ?string $v): void
{
    q(is_sqlite() ? 'INSERT OR REPLACE INTO settings (k, v) VALUES (?, ?)' : 'REPLACE INTO settings (k, v) VALUES (?, ?)', [$k, $v]);
    unset($GLOBALS['__settings']);
}

/** DB-backed PHP sessions (the hosting root is read-only; keep all state in MySQL). */
final class DbSessionHandler implements SessionHandlerInterface
{
    public function open($path, $name): bool { return true; }
    public function close(): bool { return true; }
    public function read($id): string|false
    {
        return (string)(val('SELECT data FROM sessions WHERE id = ?', [$id]) ?? '');
    }
    public function write($id, $data): bool
    {
        q(is_sqlite() ? 'INSERT OR REPLACE INTO sessions (id, data, updated_at) VALUES (?, ?, ?)'
            : 'REPLACE INTO sessions (id, data, updated_at) VALUES (?, ?, ?)', [$id, $data, time()]);
        return true;
    }
    public function destroy($id): bool
    {
        q('DELETE FROM sessions WHERE id = ?', [$id]);
        return true;
    }
    public function gc($max): int|false
    {
        return q('DELETE FROM sessions WHERE updated_at < ?', [time() - (int)$max])->rowCount();
    }
}
