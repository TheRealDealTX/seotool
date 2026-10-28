CREATE TABLE IF NOT EXISTS properties (
    id INT UNSIGNED NOT NULL PRIMARY KEY,
    slug VARCHAR(191) NOT NULL,
    name VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL DEFAULT '',
    city VARCHAR(100) NOT NULL DEFAULT '',
    state VARCHAR(10) NOT NULL DEFAULT 'TX',
    zip VARCHAR(10) NOT NULL DEFAULT '',
    lat DOUBLE NULL,
    lng DOUBLE NULL,
    area VARCHAR(100) NOT NULL DEFAULT '',
    neighborhood VARCHAR(150) NOT NULL DEFAULT '',
    rise_location INT NOT NULL DEFAULT 0,
    price_min INT NULL,
    price_max INT NULL,
    beds_min INT NOT NULL DEFAULT 0,
    beds_max INT NOT NULL DEFAULT 0,
    beds_mask INT NOT NULL DEFAULT 0,
    baths_max DOUBLE NOT NULL DEFAULT 0,
    sqft_min INT NULL,
    sqft_max INT NULL,
    pets INT NOT NULL DEFAULT 0,
    parking INT NOT NULL DEFAULT 0,
    furnished INT NOT NULL DEFAULT 0,
    essential INT NOT NULL DEFAULT 0,
    special INT NOT NULL DEFAULT 0,
    year_built INT NULL,
    units INT NULL,
    stories INT NULL,
    rating DOUBLE NULL,
    amenities TEXT,
    photo VARCHAR(255) NOT NULL DEFAULT '',
    photo_count INT NOT NULL DEFAULT 0,
    data LONGTEXT,
    rise_modified VARCHAR(30) NOT NULL DEFAULT '',
    synced_at VARCHAR(30) NOT NULL DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'publish',
    source VARCHAR(10) NOT NULL DEFAULT 'rise',
    locked INT NOT NULL DEFAULT 0,
    updated_at VARCHAR(30) NOT NULL DEFAULT '',
    updated_by VARCHAR(150) NOT NULL DEFAULT '',
    UNIQUE KEY uq_slug (slug),
    KEY ix_geo (lat, lng),
    KEY ix_price (price_min),
    KEY ix_loc (rise_location)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS leads (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at VARCHAR(30) NOT NULL,
    property_id INT NULL,
    name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(190) NOT NULL DEFAULT '',
    phone VARCHAR(40) NOT NULL DEFAULT '',
    move_in VARCHAR(40) NOT NULL DEFAULT '',
    beds VARCHAR(20) NOT NULL DEFAULT '',
    budget VARCHAR(40) NOT NULL DEFAULT '',
    message TEXT,
    page VARCHAR(255) NOT NULL DEFAULT '',
    ip VARCHAR(64) NOT NULL DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    notes TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(190) NOT NULL,
    name VARCHAR(150) NOT NULL DEFAULT '',
    pass_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'editor',
    created_at VARCHAR(30) NOT NULL DEFAULT '',
    last_login VARCHAR(30) NOT NULL DEFAULT '',
    UNIQUE KEY uq_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS login_attempts (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(64) NOT NULL,
    at INT NOT NULL,
    KEY ix_ip (ip)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS geocache (
    address VARCHAR(191) NOT NULL PRIMARY KEY,
    lat DOUBLE NULL,
    lng DOUBLE NULL,
    source VARCHAR(20) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS settings (
    k VARCHAR(64) NOT NULL PRIMARY KEY,
    v TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
