-- RodeoTexas.org schema (MySQL 5.7+/8 and MariaDB 10.4+). utf8mb4 throughout.
-- Applied by app/bin/migrate.php, which records each file in schema_migrations.

CREATE TABLE IF NOT EXISTS schema_migrations (
  version     VARCHAR(100) NOT NULL PRIMARY KEY,
  applied_at  DATETIME     NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS settings (
  name   VARCHAR(100) NOT NULL PRIMARY KEY,
  value  TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------- taxonomy
CREATE TABLE IF NOT EXISTS regions (
  id    SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug  VARCHAR(60)  NOT NULL UNIQUE,
  name  VARCHAR(120) NOT NULL,
  sort  SMALLINT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS associations (
  id       SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug     VARCHAR(60)  NOT NULL UNIQUE,
  abbr     VARCHAR(20)  NOT NULL,
  name     VARCHAR(160) NOT NULL,
  level    VARCHAR(20)  NOT NULL DEFAULT 'amateur',
  website  VARCHAR(500) NULL,
  sort     SMALLINT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS event_types (
  id    SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug  VARCHAR(60)  NOT NULL UNIQUE,
  name  VARCHAR(120) NOT NULL,
  sort  SMALLINT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------- places & people
CREATE TABLE IF NOT EXISTS venues (
  id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  norm_key            VARCHAR(255) NOT NULL UNIQUE,
  name                VARCHAR(255) NULL,
  address             VARCHAR(255) NULL,
  city                VARCHAR(120) NULL,
  county              VARCHAR(120) NULL,
  state               CHAR(2)      NOT NULL DEFAULT 'TX',
  postal_code         VARCHAR(10)  NULL,
  lat                 DECIMAL(9,6) NULL,
  lng                 DECIMAL(9,6) NULL,
  location_precision  VARCHAR(20)  NOT NULL DEFAULT 'none',  -- address | city | none
  timezone            VARCHAR(40)  NOT NULL DEFAULT 'America/Chicago',
  region_id           SMALLINT UNSIGNED NULL,
  parking_info        TEXT NULL,
  accessibility_info  TEXT NULL,
  manually_edited     TINYINT(1) NOT NULL DEFAULT 0,
  created_at          DATETIME NOT NULL,
  updated_at          DATETIME NOT NULL,
  KEY idx_venue_city (city),
  KEY idx_venue_zip (postal_code),
  CONSTRAINT fk_venue_region FOREIGN KEY (region_id) REFERENCES regions(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS organizers (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  norm_key    VARCHAR(255) NOT NULL UNIQUE,
  name        VARCHAR(255) NOT NULL,
  website     VARCHAR(500) NULL,
  email       VARCHAR(255) NULL,
  phone       VARCHAR(40)  NULL,
  created_at  DATETIME NOT NULL,
  updated_at  DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------- sources
CREATE TABLE IF NOT EXISTS sources (
  id                     SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug                   VARCHAR(60)  NOT NULL UNIQUE,
  name                   VARCHAR(160) NOT NULL,
  adapter                VARCHAR(40)  NOT NULL,            -- tribe_rest | ical | jsonld | csv
  config                 TEXT NULL,                        -- JSON
  homepage               VARCHAR(500) NULL,
  access_status          VARCHAR(30)  NOT NULL DEFAULT 'active',  -- active | awaiting_permission | awaiting_credentials | manual_only | disabled
  access_note            TEXT NULL,
  enabled                TINYINT(1) NOT NULL DEFAULT 0,
  auto_publish           TINYINT(1) NOT NULL DEFAULT 1,
  daily_check            TINYINT(1) NOT NULL DEFAULT 0,
  default_association_id SMALLINT UNSIGNED NULL,
  default_level          VARCHAR(20) NULL,
  last_run_at            DATETIME NULL,
  last_success_at        DATETIME NULL,
  last_record_count      INT NULL,
  last_error             TEXT NULL,
  consecutive_failures   INT NOT NULL DEFAULT 0,
  created_at             DATETIME NOT NULL,
  updated_at             DATETIME NOT NULL,
  CONSTRAINT fk_source_assoc FOREIGN KEY (default_association_id) REFERENCES associations(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------- events
CREATE TABLE IF NOT EXISTS event_groups (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  created_at  DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS events (
  id                  INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug                VARCHAR(190) NOT NULL UNIQUE,
  title               VARCHAR(255) NOT NULL,
  description         TEXT NULL,
  event_type_id       SMALLINT UNSIGNED NULL,
  association_id      SMALLINT UNSIGNED NULL,
  level               VARCHAR(20) NULL,     -- professional | amateur | youth | high_school | college | local | ranch
  venue_id            INT UNSIGNED NULL,
  organizer_id        INT UNSIGNED NULL,
  group_id            INT UNSIGNED NULL,
  start_date          DATE NOT NULL,
  end_date            DATE NOT NULL,
  timezone            VARCHAR(40) NOT NULL DEFAULT 'America/Chicago',
  status              VARCHAR(20) NOT NULL DEFAULT 'scheduled',   -- scheduled | postponed | canceled
  status_note         VARCHAR(255) NULL,
  official_url        VARCHAR(500) NULL,
  ticket_url          VARCHAR(500) NULL,
  ticket_url_verified TINYINT(1) NOT NULL DEFAULT 0,
  price_text          VARCHAR(255) NULL,
  parking_info        TEXT NULL,
  accessibility_info  TEXT NULL,
  image_url           VARCHAR(500) NULL,
  publish_state       VARCHAR(20) NOT NULL DEFAULT 'draft',        -- draft | published | archived
  featured            TINYINT(1) NOT NULL DEFAULT 0,
  source_id           SMALLINT UNSIGNED NULL,   -- primary (first/most trusted) source
  source_label        VARCHAR(255) NULL,        -- human-readable "information source"
  source_url          VARCHAR(500) NULL,
  last_verified_at    DATETIME NULL,
  locked_fields       TEXT NULL,                -- JSON array of field names edited by an admin
  is_legacy           TINYINT(1) NOT NULL DEFAULT 0,
  legacy_note         VARCHAR(255) NULL,
  created_at          DATETIME NOT NULL,
  updated_at          DATETIME NOT NULL,
  KEY idx_event_dates (publish_state, end_date, start_date),
  KEY idx_event_group (group_id),
  KEY idx_event_title (title),
  CONSTRAINT fk_event_type   FOREIGN KEY (event_type_id)  REFERENCES event_types(id)  ON DELETE SET NULL,
  CONSTRAINT fk_event_assoc  FOREIGN KEY (association_id) REFERENCES associations(id) ON DELETE SET NULL,
  CONSTRAINT fk_event_venue  FOREIGN KEY (venue_id)       REFERENCES venues(id)       ON DELETE SET NULL,
  CONSTRAINT fk_event_org    FOREIGN KEY (organizer_id)   REFERENCES organizers(id)   ON DELETE SET NULL,
  CONSTRAINT fk_event_group  FOREIGN KEY (group_id)       REFERENCES event_groups(id) ON DELETE SET NULL,
  CONSTRAINT fk_event_source FOREIGN KEY (source_id)      REFERENCES sources(id)      ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Individual performances / sessions. Times are wall-clock in events.timezone.
CREATE TABLE IF NOT EXISTS performances (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  event_id    INT UNSIGNED NOT NULL,
  starts_at   DATETIME NOT NULL,
  ends_at     DATETIME NULL,
  label       VARCHAR(160) NULL,
  KEY idx_perf_event (event_id, starts_at),
  CONSTRAINT fk_perf_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS event_history (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  event_id    INT UNSIGNED NOT NULL,
  actor       VARCHAR(80) NOT NULL,     -- admin:<id> | import:<source-slug> | system
  field       VARCHAR(60) NOT NULL,
  old_value   TEXT NULL,
  new_value   TEXT NULL,
  created_at  DATETIME NOT NULL,
  KEY idx_hist_event (event_id, created_at),
  CONSTRAINT fk_hist_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- One row per record seen in a source. (source_id, source_uid) is the stable identity.
CREATE TABLE IF NOT EXISTS source_records (
  id              INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  source_id       SMALLINT UNSIGNED NOT NULL,
  source_uid      VARCHAR(255) NOT NULL,
  event_id        INT UNSIGNED NULL,
  state           VARCHAR(20) NOT NULL,          -- linked | review | skipped
  skip_reason     VARCHAR(255) NULL,
  payload         MEDIUMTEXT NOT NULL,           -- normalized JSON
  payload_hash    CHAR(64) NOT NULL,
  first_seen_at   DATETIME NOT NULL,
  last_seen_at    DATETIME NOT NULL,
  last_changed_at DATETIME NOT NULL,
  UNIQUE KEY uq_source_uid (source_id, source_uid),
  KEY idx_sr_event (event_id),
  CONSTRAINT fk_sr_source FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE,
  CONSTRAINT fk_sr_event  FOREIGN KEY (event_id)  REFERENCES events(id)  ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------- import bookkeeping
CREATE TABLE IF NOT EXISTS import_runs (
  id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  trigger_type VARCHAR(20) NOT NULL,     -- cron | manual | cli
  mode         VARCHAR(20) NOT NULL,     -- weekly | daily | single
  status       VARCHAR(20) NOT NULL,     -- running | success | partial | failed | abandoned
  started_at   DATETIME NOT NULL,
  finished_at  DATETIME NULL,
  stats        TEXT NULL,                -- JSON
  message      TEXT NULL,
  started_by   VARCHAR(120) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS import_logs (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  run_id      INT UNSIGNED NOT NULL,
  source_id   SMALLINT UNSIGNED NULL,
  level       VARCHAR(10) NOT NULL,      -- info | warning | error
  message     VARCHAR(1000) NOT NULL,
  context     TEXT NULL,
  created_at  DATETIME NOT NULL,
  KEY idx_log_run (run_id),
  CONSTRAINT fk_log_run FOREIGN KEY (run_id) REFERENCES import_runs(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------- moderation
CREATE TABLE IF NOT EXISTS review_items (
  id               INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  kind             VARCHAR(30) NOT NULL,   -- submission | correction | contact | import_conflict | import_ambiguous | import_incomplete
  status           VARCHAR(20) NOT NULL DEFAULT 'open',   -- open | approved | rejected | resolved
  event_id         INT UNSIGNED NULL,
  source_record_id INT UNSIGNED NULL,
  summary          VARCHAR(255) NOT NULL,
  payload          MEDIUMTEXT NULL,        -- JSON
  dedupe_key       CHAR(64) NULL UNIQUE,
  submitter_name   VARCHAR(160) NULL,
  submitter_email  VARCHAR(255) NULL,
  ip_hash          CHAR(64) NULL,
  created_at       DATETIME NOT NULL,
  resolved_at      DATETIME NULL,
  resolved_by      INT UNSIGNED NULL,
  resolution_note  VARCHAR(500) NULL,
  KEY idx_review_status (status, kind),
  CONSTRAINT fk_review_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE SET NULL,
  CONSTRAINT fk_review_sr    FOREIGN KEY (source_record_id) REFERENCES source_records(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------- content
CREATE TABLE IF NOT EXISTS categories (
  id    SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug  VARCHAR(80)  NOT NULL UNIQUE,
  name  VARCHAR(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS articles (
  id               INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug             VARCHAR(190) NOT NULL UNIQUE,
  title            VARCHAR(255) NOT NULL,
  seo_title        VARCHAR(255) NULL,
  meta_description VARCHAR(320) NULL,
  excerpt          TEXT NULL,
  content_html     MEDIUMTEXT NOT NULL,
  featured_image   VARCHAR(500) NULL,
  featured_alt     VARCHAR(255) NULL,
  featured_width   SMALLINT UNSIGNED NULL,
  featured_height  SMALLINT UNSIGNED NULL,
  status           VARCHAR(20) NOT NULL DEFAULT 'draft',  -- draft | published | archived
  published_at     DATETIME NULL,
  updated_at       DATETIME NOT NULL,
  created_at       DATETIME NOT NULL,
  KEY idx_article_pub (status, published_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS article_categories (
  article_id   INT UNSIGNED NOT NULL,
  category_id  SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY (article_id, category_id),
  CONSTRAINT fk_ac_article  FOREIGN KEY (article_id)  REFERENCES articles(id)   ON DELETE CASCADE,
  CONSTRAINT fk_ac_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS redirects (
  id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  from_path   VARCHAR(190) NOT NULL UNIQUE,
  to_path     VARCHAR(500) NOT NULL,
  code        SMALLINT NOT NULL DEFAULT 301,
  hits        INT UNSIGNED NOT NULL DEFAULT 0,
  created_at  DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------------------------------------------------------------- security
CREATE TABLE IF NOT EXISTS admins (
  id             INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email          VARCHAR(255) NOT NULL UNIQUE,
  name           VARCHAR(120) NOT NULL,
  password_hash  VARCHAR(255) NOT NULL,
  created_at     DATETIME NOT NULL,
  last_login_at  DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS login_attempts (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  ip_hash       CHAR(64) NOT NULL,
  email         VARCHAR(255) NOT NULL,
  success       TINYINT(1) NOT NULL,
  attempted_at  DATETIME NOT NULL,
  KEY idx_la_ip (ip_hash, attempted_at),
  KEY idx_la_email (email, attempted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS rate_limits (
  bucket        VARCHAR(40) NOT NULL,
  ip_hash       CHAR(64) NOT NULL,
  hits          INT UNSIGNED NOT NULL,
  window_start  DATETIME NOT NULL,
  PRIMARY KEY (bucket, ip_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS link_checks (
  url_hash         CHAR(64) NOT NULL PRIMARY KEY,
  url              VARCHAR(500) NOT NULL,
  http_status      SMALLINT NULL,
  ok               TINYINT(1) NOT NULL DEFAULT 0,
  error            VARCHAR(255) NULL,
  last_checked_at  DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS geocode_cache (
  query_hash  CHAR(64) NOT NULL PRIMARY KEY,
  query       VARCHAR(500) NOT NULL,
  result      TEXT NULL,
  created_at  DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
