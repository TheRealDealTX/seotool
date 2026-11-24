CREATE TABLE IF NOT EXISTS mhr_owners (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(190) NOT NULL DEFAULT '',
  email VARCHAR(190) NOT NULL,
  email_verified_at DATETIME NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL,
  last_login_at DATETIME NULL,
  UNIQUE KEY uq_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS mhr_listings (
  slug VARCHAR(190) PRIMARY KEY,
  origin VARCHAR(10) NOT NULL DEFAULT 'json',
  data LONGTEXT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'published',
  owner_id INT UNSIGNED NULL,
  contact_visible TINYINT(1) NOT NULL DEFAULT 0,
  verified TINYINT(1) NOT NULL DEFAULT 0,
  plan VARCHAR(10) NULL,
  submitter_name VARCHAR(190) NULL,
  submitter_email VARCHAR(190) NULL,
  submitter_phone VARCHAR(60) NULL,
  admin_note TEXT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  published_at DATETIME NULL,
  KEY idx_status (status),
  KEY idx_owner (owner_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS mhr_tokens (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  owner_id INT UNSIGNED NOT NULL,
  purpose VARCHAR(20) NOT NULL,
  token_hash CHAR(64) NOT NULL,
  expires_at DATETIME NOT NULL,
  used_at DATETIME NULL,
  created_at DATETIME NOT NULL,
  UNIQUE KEY uq_hash (token_hash),
  KEY idx_owner (owner_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS mhr_payments (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  kind VARCHAR(20) NOT NULL,
  listing_slug VARCHAR(190) NOT NULL,
  owner_id INT UNSIGNED NULL,
  name VARCHAR(190) NOT NULL DEFAULT '',
  email VARCHAR(190) NOT NULL DEFAULT '',
  stripe_session_id VARCHAR(255) NULL,
  amount_total INT NULL,
  currency VARCHAR(10) NULL,
  payment_status VARCHAR(40) NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  note VARCHAR(255) NULL,
  created_at DATETIME NOT NULL,
  fulfilled_at DATETIME NULL,
  UNIQUE KEY uq_session (stripe_session_id),
  KEY idx_listing (listing_slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS mhr_messages (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  kind VARCHAR(20) NOT NULL,
  name VARCHAR(190) NOT NULL DEFAULT '',
  email VARCHAR(190) NOT NULL DEFAULT '',
  phone VARCHAR(60) NOT NULL DEFAULT '',
  subject VARCHAR(255) NOT NULL DEFAULT '',
  body MEDIUMTEXT NULL,
  ip VARCHAR(45) NULL,
  created_at DATETIME NOT NULL,
  KEY idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS mhr_admins (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  pass_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL,
  last_login_at DATETIME NULL,
  UNIQUE KEY uq_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS mhr_login_attempts (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  scope VARCHAR(20) NOT NULL,
  ip VARCHAR(45) NOT NULL,
  ident VARCHAR(190) NOT NULL DEFAULT '',
  success TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL,
  KEY idx_ip (scope, ip, created_at),
  KEY idx_ident (scope, ident, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
