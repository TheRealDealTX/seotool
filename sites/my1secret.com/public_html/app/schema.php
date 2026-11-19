<?php
declare(strict_types=1);
defined('M1S') || exit;

/**
 * Database schema + first-run seed. Works on MySQL (production) and SQLite (tests).
 * Run through /install/?token=<install_token from config> or tools/install.php.
 */
function schema_sql(bool $sqlite): array
{
    $pk = $sqlite ? 'INTEGER PRIMARY KEY AUTOINCREMENT' : 'INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY';
    $int = $sqlite ? 'INTEGER' : 'INT';
    $fk = $sqlite ? 'INTEGER' : 'INT UNSIGNED';
    $long = $sqlite ? 'TEXT' : 'MEDIUMTEXT';
    $end = $sqlite ? '' : ' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci';

    return [
        "CREATE TABLE IF NOT EXISTS users (
            id $pk,
            username VARCHAR(20) NOT NULL UNIQUE,
            email VARCHAR(190) NULL UNIQUE,
            pass_hash VARCHAR(255) NOT NULL,
            role VARCHAR(10) NOT NULL DEFAULT 'member',
            display_name VARCHAR(60) NULL,
            bio TEXT NULL,
            karma $int NOT NULL DEFAULT 0,
            banned TINYINT NOT NULL DEFAULT 0,
            session_epoch $int NOT NULL DEFAULT 0,
            reset_hash VARCHAR(64) NULL,
            reset_expires DATETIME NULL,
            created_at DATETIME NOT NULL,
            last_seen_at DATETIME NOT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS topics (
            id $pk,
            slug VARCHAR(60) NOT NULL UNIQUE,
            name VARCHAR(80) NOT NULL,
            seo_title VARCHAR(120) NULL,
            description TEXT NULL,
            sort $int NOT NULL DEFAULT 0
        )$end",
        "CREATE TABLE IF NOT EXISTS communities (
            id $pk,
            slug VARCHAR(40) NOT NULL UNIQUE,
            name VARCHAR(60) NOT NULL,
            title VARCHAR(120) NOT NULL,
            description TEXT NOT NULL,
            rules TEXT NULL,
            color VARCHAR(7) NOT NULL DEFAULT '#1f8fcf',
            sort $int NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS articles (
            id $pk,
            slug VARCHAR(120) NOT NULL UNIQUE,
            legacy_slug VARCHAR(190) NULL,
            wp_id $int NULL,
            title VARCHAR(200) NOT NULL,
            seo_title VARCHAR(120) NULL,
            meta_description VARCHAR(200) NULL,
            excerpt TEXT NULL,
            body_html $long NOT NULL,
            topic_id $fk NULL,
            author_id $fk NULL,
            image VARCHAR(255) NULL,
            image_w $int NULL,
            image_h $int NULL,
            image_alt VARCHAR(255) NULL,
            image_credit VARCHAR(300) NULL,
            image_credit_url VARCHAR(500) NULL,
            status VARCHAR(10) NOT NULL DEFAULT 'published',
            published_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            reading_minutes $int NOT NULL DEFAULT 1,
            score $int NOT NULL DEFAULT 0,
            upvotes $int NOT NULL DEFAULT 0,
            downvotes $int NOT NULL DEFAULT 0,
            comment_count $int NOT NULL DEFAULT 0,
            community_id $fk NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS threads (
            id $pk,
            community_id $fk NOT NULL,
            user_id $fk NULL,
            guest_name VARCHAR(60) NULL,
            guest_email VARCHAR(190) NULL,
            status VARCHAR(10) NOT NULL DEFAULT 'live',
            title VARCHAR(300) NOT NULL,
            slug VARCHAR(80) NOT NULL,
            body $long NULL,
            body_html $long NULL,
            link_url VARCHAR(1000) NULL,
            image VARCHAR(255) NULL,
            image_w $int NULL,
            image_h $int NULL,
            score $int NOT NULL DEFAULT 0,
            upvotes $int NOT NULL DEFAULT 0,
            downvotes $int NOT NULL DEFAULT 0,
            comment_count $int NOT NULL DEFAULT 0,
            hot DOUBLE NOT NULL DEFAULT 0,
            pinned TINYINT NOT NULL DEFAULT 0,
            locked TINYINT NOT NULL DEFAULT 0,
            removed TINYINT NOT NULL DEFAULT 0,
            deleted TINYINT NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL,
            edited_at DATETIME NULL,
            last_activity_at DATETIME NOT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS comments (
            id $pk,
            target_type VARCHAR(10) NOT NULL,
            target_id $fk NOT NULL,
            parent_id $fk NULL,
            user_id $fk NULL,
            guest_name VARCHAR(60) NULL,
            guest_email VARCHAR(190) NULL,
            status VARCHAR(10) NOT NULL DEFAULT 'live',
            body TEXT NOT NULL,
            body_html TEXT NOT NULL,
            depth $int NOT NULL DEFAULT 0,
            score $int NOT NULL DEFAULT 0,
            upvotes $int NOT NULL DEFAULT 0,
            downvotes $int NOT NULL DEFAULT 0,
            removed TINYINT NOT NULL DEFAULT 0,
            deleted TINYINT NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL,
            edited_at DATETIME NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS votes (
            user_id $fk NOT NULL,
            target_type VARCHAR(10) NOT NULL,
            target_id $fk NOT NULL,
            value TINYINT NOT NULL,
            created_at DATETIME NOT NULL,
            PRIMARY KEY (user_id, target_type, target_id)
        )$end",
        "CREATE TABLE IF NOT EXISTS reports (
            id $pk,
            user_id $fk NULL,
            target_type VARCHAR(10) NOT NULL,
            target_id $fk NOT NULL,
            reason VARCHAR(500) NOT NULL,
            created_at DATETIME NOT NULL,
            resolved_by $fk NULL,
            resolved_at DATETIME NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS sessions (
            id VARCHAR(64) NOT NULL PRIMARY KEY,
            data TEXT NOT NULL,
            user_id $fk NULL,
            updated_at DATETIME NOT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS throttle (
            id $pk,
            k VARCHAR(120) NOT NULL,
            created_at DATETIME NOT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS guests (
            email VARCHAR(190) NOT NULL PRIMARY KEY,
            name VARCHAR(60) NOT NULL,
            verified_at DATETIME NULL,
            banned TINYINT NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS guest_tokens (
            id $pk,
            email VARCHAR(190) NOT NULL,
            token_hash VARCHAR(64) NOT NULL,
            target_type VARCHAR(10) NOT NULL,
            target_id $fk NOT NULL,
            created_at DATETIME NOT NULL,
            used_at DATETIME NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS products (
            id $pk,
            name VARCHAR(160) NOT NULL,
            blurb VARCHAR(300) NULL,
            query VARCHAR(200) NULL,
            url VARCHAR(500) NULL,
            image VARCHAR(500) NULL,
            tags VARCHAR(1000) NOT NULL DEFAULT '',
            sort $int NOT NULL DEFAULT 0,
            active TINYINT NOT NULL DEFAULT 1,
            created_at DATETIME NOT NULL
        )$end",
        "CREATE TABLE IF NOT EXISTS settings (
            k VARCHAR(60) NOT NULL PRIMARY KEY,
            v TEXT NULL
        )$end",
    ];
}

function schema_indexes(): array
{
    return [
        'CREATE INDEX idx_threads_comm_hot ON threads (community_id, removed, hot)',
        'CREATE INDEX idx_threads_hot ON threads (removed, hot)',
        'CREATE INDEX idx_threads_new ON threads (removed, created_at)',
        'CREATE INDEX idx_threads_user ON threads (user_id, created_at)',
        'CREATE INDEX idx_comments_target ON comments (target_type, target_id)',
        'CREATE INDEX idx_comments_user ON comments (user_id, created_at)',
        'CREATE INDEX idx_articles_pub ON articles (status, published_at)',
        'CREATE INDEX idx_articles_topic ON articles (topic_id, published_at)',
        'CREATE INDEX idx_articles_legacy ON articles (legacy_slug)',
        'CREATE INDEX idx_votes_target ON votes (target_type, target_id)',
        'CREATE INDEX idx_reports_open ON reports (resolved_at)',
        'CREATE INDEX idx_sessions_upd ON sessions (updated_at)',
        'CREATE INDEX idx_throttle_k ON throttle (k, created_at)',
        'CREATE INDEX idx_threads_status ON threads (status, created_at)',
        'CREATE INDEX idx_comments_status ON comments (status, created_at)',
    ];
}

/** Column additions for databases created before they existed (errors = already there). */
function schema_migrations(): array
{
    return [
        "ALTER TABLE threads ADD COLUMN guest_name VARCHAR(60) NULL",
        "ALTER TABLE threads ADD COLUMN guest_email VARCHAR(190) NULL",
        "ALTER TABLE threads ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'live'",
        "ALTER TABLE comments ADD COLUMN guest_name VARCHAR(60) NULL",
        "ALTER TABLE comments ADD COLUMN guest_email VARCHAR(190) NULL",
        "ALTER TABLE comments ADD COLUMN status VARCHAR(10) NOT NULL DEFAULT 'live'",
        "ALTER TABLE articles ADD COLUMN image_credit VARCHAR(300) NULL",
        "ALTER TABLE articles ADD COLUMN image_credit_url VARCHAR(500) NULL",
    ];
}

function seed_communities(): array
{
    $common = "1. **Be kind and useful.** Disagree with ideas, not people.\n"
            . "2. **No spam or self-promotion.** Links are fine when they help; ads, affiliate dumps and SEO links get removed.\n"
            . "3. **Protect privacy.** No addresses, policy numbers, phone numbers or anyone's personal details.\n"
            . "4. **Not professional advice.** Posts here are experiences and opinions. For legal, insurance or financial decisions, talk to a licensed professional.";
    return [
        ['renting', 'Renting', 'Renting & Apartment Living Forum',
         'Ask anything about renting: finding an apartment, leases, deposits, landlords, roommates, moving and everyday apartment life.', '#1f8fcf'],
        ['small-space-living', 'Small-Space Living', 'Small Apartment Design & Organization Forum',
         'Share small apartment layouts, storage hacks, budget furniture finds and before-and-after photos. Make every square foot count.', '#7c5cff'],
        ['insurance-claims', 'Insurance Claims', 'Renters & Homeowners Insurance Claims Forum',
         'Storm, fire, water or theft damage? Compare notes on renters and homeowners insurance claims, appraisals and adjusters.', '#e8590c'],
        ['texas', 'Texas Living', 'Texas Living Forum: Houston, Dallas, Austin & More',
         'Moving to or living in Texas: neighborhoods, apartments, weather, cost of living and local recommendations.', '#c92a2a'],
        ['lifestyle', 'Lifestyle', 'Lifestyle, Wellness & Productivity Forum',
         'Wellness at home, routines, productivity, budgeting and the small habits that make life easier.', '#2b8a3e'],
        ['one-secret', 'One Secret', 'Share Your One Best Life Hack',
         'The heart of My 1 Secret: post the one tip, trick or lesson you wish someone had told you sooner. One secret per post.', '#0b7285'],
    ];
}

function welcome_posts(): array
{
    return [
        'renting' => ['Welcome to Renting: start here',
            "This is the place for every renting question, big or small: apartment hunting, lease terms, security deposits, maintenance requests, roommates and moving day.\n\n"
            . "**To get a great answer:**\n\n- Put the real question in your title\n- Say what city or state you are in (rules vary a lot)\n- Share what you have already tried\n\n"
            . "New here? Our blog has detailed guides to [the best time of year to rent](/blog/best-time-of-year-to-rent-an-apartment/), [apartment security](/blog/apartment-security-tips/) and [what no one tells you about apartment life](/blog/apartment-living-tips/)."],
        'small-space-living' => ['Welcome! Show us your small space',
            "Studios, one-bedrooms, tiny kitchens and closets that should not be this small: this community is for making them work.\n\n"
            . "Post your layout problem, your best storage hack or a before-and-after photo. Upload images right in the post form.\n\n"
            . "Need ideas first? Try [small apartment design ideas](/blog/small-apartment-design-ideas/) or [furnishing an apartment for under \$1,000](/blog/furnish-an-apartment-for-under-1000/)."],
        'insurance-claims' => ['Welcome to Insurance Claims: please read before posting',
            "Dealing with a claim is stressful. This community is for sharing experiences and getting your bearings on renters and homeowners insurance claims, appraisal and adjusters.\n\n"
            . "**Please do not post** policy numbers, claim numbers, addresses or anything that identifies you or your insurer's staff.\n\n"
            . "Posts here are not legal or insurance advice. For decisions about your claim, talk to your insurer, a licensed public adjuster or an attorney.\n\n"
            . "Background reading: [how public adjusters help with insurance claims](/blog/how-public-adjusters-help-with-insurance-claims/) and [insurance appraisal tips](/blog/insurance-appraisal-tips/)."],
        'texas' => ['Welcome to Texas Living',
            "Moving to Houston? Comparing Dallas suburbs? Wondering how bad the summers really are? Ask here.\n\n"
            . "Local recommendations are welcome. Please keep it helpful and skip the ads.\n\n"
            . "Start with our guides to [moving to Houston](/blog/moving-to-houston-tx/) and [Texas climate regions](/blog/texas-climate-regions-guide/)."],
        'lifestyle' => ['Welcome to Lifestyle',
            "Routines, wellness, productivity, money habits: share what is working for you and ask about what is not.\n\n"
            . "A few reads to get started: [10 time-saving tips for busy professionals](/blog/time-saving-tips-for-busy-professionals/) and [forest bathing benefits](/blog/forest-bathing-benefits/)."],
        'one-secret' => ['What is your one secret? Read this first',
            "My 1 Secret started with a simple idea: everyone has one tip they wish they had known sooner.\n\n"
            . "**How it works:**\n\n1. One secret per post. Put it in the title.\n2. Explain why it works in the body.\n3. Vote up the secrets that actually helped you.\n\n"
            . "The best secrets get featured on the homepage. What is yours?"],
    ];
}

/**
 * Create tables and seed content. Safe to re-run: existing rows are kept.
 * Returns a log of what it did, plus the generated admin password on first run.
 */
function run_install(): array
{
    $log = [];
    $sqlite = db_is_sqlite();
    foreach (schema_sql($sqlite) as $sql) {
        db()->exec($sql);
    }
    foreach (schema_migrations() as $sql) {
        try {
            db()->exec($sql);
        } catch (PDOException $e) {
            // column already exists
        }
    }
    foreach (schema_indexes() as $sql) {
        try {
            db()->exec($sql);
        } catch (PDOException $e) {
            // index already exists
        }
    }
    $log[] = 'schema ok';

    $adminPassword = null;
    if (!one("SELECT id FROM users WHERE username = 'my1secret'")) {
        $adminPassword = rtrim(strtr(base64_encode(random_bytes(15)), '+/', 'xy'), '=');
        insert('users', [
            'username' => 'my1secret', 'email' => cfg('admin_email') ?: null,
            'pass_hash' => password_hash($adminPassword, PASSWORD_DEFAULT), 'role' => 'admin',
            'display_name' => 'My 1 Secret Team', 'bio' => 'The team behind My 1 Secret.',
            'created_at' => now(), 'last_seen_at' => now(),
        ]);
        $log[] = 'admin user my1secret created';
    }
    if (!one("SELECT id FROM users WHERE username = 'meagan'")) {
        insert('users', [
            'username' => 'meagan', 'email' => null,
            'pass_hash' => password_hash(bin2hex(random_bytes(24)), PASSWORD_DEFAULT), 'role' => 'admin',
            'display_name' => 'Meagan', 'bio' => 'Writer and editor at My 1 Secret, covering apartment living, renting in Texas, small-space design and insurance claims.',
            'created_at' => '2023-09-19 01:19:18', 'last_seen_at' => now(),
        ]);
        $log[] = 'author meagan created';
    }
    $meagan = (int)val("SELECT id FROM users WHERE username = 'meagan'");
    $team = (int)val("SELECT id FROM users WHERE username = 'my1secret'");

    foreach (seed_communities() as $i => [$slug, $name, $title, $desc, $color]) {
        if (!one('SELECT id FROM communities WHERE slug = ?', [$slug])) {
            insert('communities', ['slug' => $slug, 'name' => $name, 'title' => $title, 'description' => $desc,
                'rules' => null, 'color' => $color, 'sort' => $i, 'created_at' => now()]);
            $log[] = "community $slug";
        }
    }

    $seed = require M1S_APP . '/seed/articles.php';
    foreach (glob(M1S_APP . '/seed/articles-*.php') as $extra) {
        $more = require $extra;
        $seed['articles'] = array_merge($seed['articles'], $more['articles']);
    }
    foreach ($seed['topics'] as $t) {
        if (!one('SELECT id FROM topics WHERE slug = ?', [$t['slug']])) {
            insert('topics', $t);
        }
    }
    $topicIds = [];
    foreach (all('SELECT id, slug FROM topics') as $t) {
        $topicIds[$t['slug']] = (int)$t['id'];
    }
    $added = 0;
    foreach ($seed['articles'] as $a) {
        $existing = one('SELECT id, image, image_credit FROM articles WHERE slug = ? OR wp_id = ?', [$a['slug'], $a['wp_id']]);
        if ($existing) {
            // pick up a newer photo + credit for the same image path, unless an admin changed the image
            if (!empty($a['image']['credit']) && $existing['image'] === $a['image']['src'] && $existing['image_credit'] !== $a['image']['credit']) {
                update('articles', ['image_w' => $a['image']['w'], 'image_h' => $a['image']['h'], 'image_credit' => $a['image']['credit'],
                    'image_credit_url' => $a['image']['credit_url'] ?? null], 'id = :id', ['id' => $existing['id']]);
                $log[] = 'photo credit updated: ' . $a['slug'];
            }
            continue;
        }
        insert('articles', [
            'slug' => $a['slug'], 'legacy_slug' => $a['legacy_slug'], 'wp_id' => $a['wp_id'],
            'title' => $a['title'], 'seo_title' => $a['seo_title'], 'meta_description' => $a['meta_description'],
            'excerpt' => $a['excerpt'], 'body_html' => $a['body_html'], 'topic_id' => $topicIds[$a['topic']] ?? null,
            'author_id' => ($a['author'] ?? 'meagan') === 'team' ? $team : $meagan, 'image' => $a['image']['src'] ?? null, 'image_w' => $a['image']['w'] ?? null,
            'image_h' => $a['image']['h'] ?? null, 'image_alt' => $a['image']['alt'] ?? null,
            'image_credit' => $a['image']['credit'] ?? null, 'image_credit_url' => $a['image']['credit_url'] ?? null, 'status' => 'published',
            'published_at' => $a['published_at'], 'updated_at' => $a['updated_at'], 'reading_minutes' => $a['reading_minutes'],
        ]);
        $added++;
    }
    $log[] = "articles imported: $added";

    if (is_file(M1S_APP . '/seed/seo-updates.php')) {
        $n = 0;
        foreach (require M1S_APP . '/seed/seo-updates.php' as $slug => $fields) {
            foreach ($fields as $field => [$old, $new]) {
                if (in_array($field, ['seo_title', 'meta_description'], true)) {
                    $n += q("UPDATE articles SET $field = ? WHERE slug = ? AND $field = ?", [$new, $slug, $old])->rowCount();
                }
            }
        }
        $log[] = "seo fields updated: $n";
    }

    foreach (welcome_posts() as $cslug => [$title, $body]) {
        $cid = (int)val('SELECT id FROM communities WHERE slug = ?', [$cslug]);
        if ($cid && !one('SELECT id FROM threads WHERE community_id = ? AND pinned = 1', [$cid])) {
            insert('threads', [
                'community_id' => $cid, 'user_id' => $team, 'title' => $title, 'slug' => slugify($title),
                'body' => $body, 'body_html' => md($body), 'hot' => hot_score(1, now()), 'score' => 1, 'upvotes' => 1,
                'pinned' => 1, 'created_at' => now(), 'last_activity_at' => now(),
            ]);
            $tid = (int)db()->lastInsertId();
            insert('votes', ['user_id' => $team, 'target_type' => 'thread', 'target_id' => $tid, 'value' => 1, 'created_at' => now()]);
            $log[] = "welcome post in $cslug";
        }
    }

    $pseed = is_file(M1S_APP . '/seed/products.php') ? require M1S_APP . '/seed/products.php' : [];
    $padded = 0;
    foreach ($pseed as $i => $p) {
        if (!one('SELECT id FROM products WHERE name = ? AND tags = ?', [$p['name'], $p['tags']])) {
            insert('products', ['name' => $p['name'], 'blurb' => $p['blurb'] ?? null, 'query' => $p['query'] ?? null,
                'url' => $p['url'] ?? null, 'image' => null, 'tags' => $p['tags'], 'sort' => $i, 'active' => 1, 'created_at' => now()]);
            $padded++;
        }
    }
    $log[] = "products added: $padded";

    foreach (['installed_at' => now(), 'schema_version' => '1'] as $k => $v) {
        if (!one('SELECT k FROM settings WHERE k = ?', [$k])) {
            insert('settings', ['k' => $k, 'v' => $v]);
        }
    }
    return ['log' => $log, 'admin_password' => $adminPassword];
}
