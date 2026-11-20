<?php defined('WCA') || exit;

function db(): PDO
{
    static $pdo = null;
    if ($pdo) return $pdo;
    $d = cfg('db');
    if (!empty($d['sqlite'])) {
        $pdo = new PDO('sqlite:' . $d['sqlite']);
    } else {
        $pdo = new PDO(
            'mysql:host=' . $d['host'] . ';dbname=' . $d['name'] . ';charset=utf8mb4',
            $d['user'], $d['pass']
        );
    }
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    db_migrate($pdo);
    return $pdo;
}

function db_is_sqlite(PDO $pdo): bool
{
    return $pdo->getAttribute(PDO::ATTR_DRIVER_NAME) === 'sqlite';
}

const SCHEMA_VERSION = 1;

function db_migrate(PDO $pdo): void
{
    $sqlite = db_is_sqlite($pdo);
    $ai = $sqlite ? 'INTEGER PRIMARY KEY AUTOINCREMENT' : 'INT UNSIGNED AUTO_INCREMENT PRIMARY KEY';
    $tail = $sqlite ? '' : ' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4';
    $pdo->exec("CREATE TABLE IF NOT EXISTS settings (k VARCHAR(64) PRIMARY KEY, v TEXT)$tail");
    $ver = (int)($pdo->query("SELECT v FROM settings WHERE k = 'schema_version'")->fetchColumn() ?: 0);
    if ($ver >= SCHEMA_VERSION) return;

    $pdo->exec("CREATE TABLE IF NOT EXISTS users (
        id $ai,
        name VARCHAR(120) NOT NULL,
        email VARCHAR(190) NOT NULL UNIQUE,
        verified_at DATETIME NULL,
        verify_token VARCHAR(64) NULL,
        login_token VARCHAR(64) NULL,
        login_expires DATETIME NULL,
        created_at DATETIME NOT NULL
    )$tail");

    $pdo->exec("CREATE TABLE IF NOT EXISTS listings (
        id $ai,
        slug VARCHAR(160) NOT NULL UNIQUE,
        name VARCHAR(160) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'published',
        type VARCHAR(20) NOT NULL DEFAULT 'apartment',
        address VARCHAR(190) NOT NULL DEFAULT '',
        city VARCHAR(80) NOT NULL DEFAULT 'West Carrollton',
        state VARCHAR(2) NOT NULL DEFAULT 'OH',
        zip VARCHAR(10) NOT NULL DEFAULT '45449',
        lat DECIMAL(9,6) NULL,
        lng DECIMAL(9,6) NULL,
        phone VARCHAR(60) NULL,
        email VARCHAR(190) NULL,
        website VARCHAR(255) NULL,
        office_hours VARCHAR(190) NULL,
        beds_min TINYINT NULL,
        beds_max TINYINT NULL,
        baths VARCHAR(20) NULL,
        rent_min INT NULL,
        rent_max INT NULL,
        sqft_min INT NULL,
        sqft_max INT NULL,
        year_built SMALLINT NULL,
        units SMALLINT NULL,
        cats TINYINT NULL,
        dogs TINYINT NULL,
        pet_notes VARCHAR(255) NULL,
        income_restricted TINYINT NOT NULL DEFAULT 0,
        age_restriction VARCHAR(20) NULL,
        amenities TEXT NULL,
        description TEXT NULL,
        photos TEXT NULL,
        owner_id INT NULL,
        contact_visible TINYINT NOT NULL DEFAULT 0,
        featured TINYINT NOT NULL DEFAULT 0,
        source VARCHAR(10) NOT NULL DEFAULT 'seed',
        submitter_name VARCHAR(120) NULL,
        submitter_email VARCHAR(190) NULL,
        views INT NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL
    )$tail");

    $pdo->exec("CREATE TABLE IF NOT EXISTS payments (
        id $ai,
        session_id VARCHAR(255) NULL UNIQUE,
        purpose VARCHAR(10) NOT NULL,
        listing_id INT NOT NULL,
        user_id INT NULL,
        name VARCHAR(120) NOT NULL,
        email VARCHAR(190) NOT NULL,
        amount INT NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'pending',
        created_at DATETIME NOT NULL,
        completed_at DATETIME NULL
    )$tail");

    $pdo->exec("CREATE TABLE IF NOT EXISTS messages (
        id $ai,
        name VARCHAR(120) NOT NULL,
        email VARCHAR(190) NOT NULL,
        subject VARCHAR(190) NOT NULL DEFAULT '',
        body TEXT NOT NULL,
        is_read TINYINT NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL
    )$tail");

    $pdo->exec("CREATE TABLE IF NOT EXISTS login_attempts (
        id $ai,
        ip VARCHAR(64) NOT NULL,
        created_at DATETIME NOT NULL
    )$tail");

    // Seed listings on first install
    $count = (int)$pdo->query('SELECT COUNT(*) FROM listings')->fetchColumn();
    if ($count === 0) {
        $seed = require APP_DIR . '/data/seed_listings.php';
        foreach ($seed as $l) listing_insert($pdo, $l);
    }

    $pdo->prepare('REPLACE INTO settings (k, v) VALUES (?, ?)')->execute(['schema_version', (string)SCHEMA_VERSION]);
}

function now(): string
{
    return date('Y-m-d H:i:s');
}
