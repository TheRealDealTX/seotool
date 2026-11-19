<?php
declare(strict_types=1);
defined('M1S') || exit;

function search_page(): void
{
    $qText = mb_substr(trim(input('q')), 0, 100);
    $articles = $threads = [];
    if (mb_strlen($qText) >= 2) {
        $like = '%' . str_replace(['\\', '%', '_'], ['\\\\', '\\%', '\\_'], $qText) . '%';
        $articles = all(ARTICLE_SELECT . " WHERE a.status = 'published' AND (a.title LIKE :q OR a.excerpt LIKE :q2 OR a.body_html LIKE :q3)
            ORDER BY (CASE WHEN a.title LIKE :q4 THEN 0 ELSE 1 END), a.published_at DESC LIMIT 20",
            ['q' => $like, 'q2' => $like, 'q3' => $like, 'q4' => $like]);
        $threads = all(THREAD_SELECT . ' WHERE t.removed = 0 AND t.status = \'live\' AND t.deleted = 0 AND (t.title LIKE :q OR t.body LIKE :q2)
            ORDER BY (CASE WHEN t.title LIKE :q3 THEN 0 ELSE 1 END), t.hot DESC LIMIT 25',
            ['q' => $like, 'q2' => $like, 'q3' => $like]);
    }
    render('search', ['qText' => $qText, 'articles' => $articles, 'threads' => $threads,
        'votes' => my_votes('thread', array_column($threads, 'id'))],
        ['title' => $qText !== '' ? 'Search: ' . $qText : 'Search', 'robots' => 'noindex, follow']);
}

function static_page(string $slug): void
{
    $pages = [
        'about' => ['About My 1 Secret: Our Blog & Community', 'About My 1 Secret: a blog and community for renters, homeowners and Texans sharing practical, real-life secrets.'],
        'privacy-policy' => ['Privacy Policy', 'How My 1 Secret collects, uses and protects your information, which cookies we use, and how to edit or delete your posts and account.'],
        'terms' => ['Terms of Use', 'The terms that apply when you use My 1 Secret and its community forum.'],
        'community-guidelines' => ['Community Guidelines', 'How to be a great member of the My 1 Secret community: be kind, be useful, no spam, protect privacy.'],
        'contact' => ['Contact Us', 'How to reach the My 1 Secret team, report a problem with a post, or make an account or privacy request.'],
    ];
    [$title, $desc] = $pages[$slug];
    render('page_' . str_replace('-', '_', $slug), ['title' => $title], [
        'title' => $title, 'description' => $desc,
        'jsonld' => [breadcrumb_schema([[$title, null]]), ['@type' => $slug === 'about' ? 'AboutPage' : ($slug === 'contact' ? 'ContactPage' : 'WebPage'), 'name' => $title, 'url' => abs_url("/$slug/")]],
        'breadcrumbs' => [[$title, null]],
    ]);
}

function sitemap_xml(): void
{
    $urls = [];
    $add = function (string $path, ?string $lastmod = null, ?array $image = null) use (&$urls) {
        $urls[] = [abs_url($path), $lastmod ? gmdate('Y-m-d', strtotime($lastmod . ' UTC')) : null, $image];
    };
    $latestArticle = (string)val("SELECT MAX(updated_at) FROM articles WHERE status = 'published'");
    $latestThread = (string)(val('SELECT MAX(last_activity_at) FROM threads WHERE removed = 0 AND status = \'live\'') ?: $latestArticle);
    $add('/', max($latestArticle, $latestThread));
    $add('/blog/', $latestArticle);
    $add('/forum/', $latestThread);
    foreach (topics() as $t) {
        if ((int)$t['article_count'] > 0) {
            $add(topic_url($t), (string)val("SELECT MAX(updated_at) FROM articles WHERE topic_id = ? AND status = 'published'", [$t['id']]));
        }
    }
    foreach (all("SELECT slug, updated_at, image, title FROM articles WHERE status = 'published' AND published_at <= ? ORDER BY published_at DESC", [now()]) as $a) {
        $add(article_url($a), $a['updated_at'], $a['image'] ? [abs_url($a['image']), $a['title']] : null);
    }
    foreach (communities() as $c) {
        $add(community_url($c), (string)(val('SELECT MAX(last_activity_at) FROM threads WHERE community_id = ? AND removed = 0 AND status = \'live\'', [$c['id']]) ?: $c['created_at']));
    }
    $threads = all('SELECT t.*, c.slug AS community_slug FROM threads t JOIN communities c ON c.id = t.community_id
        WHERE t.removed = 0 AND t.status = \'live\' AND t.deleted = 0 ORDER BY t.last_activity_at DESC LIMIT 20000');
    foreach ($threads as $t) {
        if (thread_indexable($t)) {
            $add(thread_url($t), $t['edited_at'] && $t['edited_at'] > $t['last_activity_at'] ? $t['edited_at'] : $t['last_activity_at']);
        }
    }
    foreach (all("SELECT u.username, MAX(a.updated_at) AS m FROM articles a JOIN users u ON u.id = a.author_id WHERE a.status = 'published' GROUP BY u.username") as $au) {
        $add('/author/' . $au['username'] . '/', $au['m']);
    }
    $add('/shop/', $latestArticle);
    foreach (['about', 'community-guidelines', 'contact', 'privacy-policy', 'terms'] as $p) {
        $add("/$p/");
    }

    header('Content-Type: application/xml; charset=utf-8');
    header('Cache-Control: public, max-age=3600');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
    foreach ($urls as [$loc, $lastmod, $image]) {
        echo '  <url><loc>' . e($loc) . '</loc>' . ($lastmod ? '<lastmod>' . $lastmod . '</lastmod>' : '');
        if ($image) {
            echo '<image:image><image:loc>' . e($image[0]) . '</image:loc></image:image>';
        }
        echo "</url>\n";
    }
    echo '</urlset>';
    exit;
}

function robots_txt(): void
{
    header('Content-Type: text/plain; charset=utf-8');
    header('Cache-Control: public, max-age=86400');
    $staging = !cfg('allow_indexing', true);
    if ($staging) {
        echo "User-agent: *\nDisallow: /\n";
        exit;
    }
    echo "User-agent: *\n"
       . "Disallow: /admin/\n"
       . "Disallow: /login/\n"
       . "Disallow: /register/\n"
       . "Disallow: /submit/\n"
       . "Disallow: /settings/\n"
       . "Disallow: /search/\n"
       . "Disallow: /report/\n"
       . "Disallow: /forgot-password/\n"
       . "Disallow: /reset-password/\n"
       . "Disallow: /install/\n"
       . "Disallow: /*?sort=\n"
       . "Disallow: /*&sort=\n"
       . "Disallow: /*?reply=\n"
       . "Disallow: /app/\n"
       . "\nSitemap: " . abs_url('/sitemap.xml') . "\n";
    exit;
}

function rss_feed(): void
{
    [$articles] = article_list(null, 1, 20);
    header('Content-Type: application/rss+xml; charset=utf-8');
    header('Cache-Control: public, max-age=1800');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    echo '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>';
    echo '<title>' . e(cfg('site_name')) . '</title><link>' . e(abs_url('/')) . '</link>';
    echo '<atom:link href="' . e(abs_url('/feed/')) . '" rel="self" type="application/rss+xml"/>';
    echo '<description>' . e(M1S_TAGLINE) . '</description><language>en-us</language>';
    foreach ($articles as $a) {
        echo '<item><title>' . e($a['title']) . '</title><link>' . e(abs_url(article_url($a))) . '</link>'
           . '<guid isPermaLink="true">' . e(abs_url(article_url($a))) . '</guid>'
           . '<pubDate>' . gmdate('D, d M Y H:i:s', strtotime($a['published_at'] . ' UTC')) . ' +0000</pubDate>'
           . '<category>' . e((string)$a['topic_name']) . '</category>'
           . '<description>' . e($a['meta_description'] ?: $a['excerpt']) . '</description></item>';
    }
    echo '</channel></rss>';
    exit;
}

/** One-time setup: /install/?token=<install_token>. Disabled once the token is removed from config. */
function install_page(): void
{
    $token = (string)cfg('install_token', '');
    if ($token === '' || !hash_equals($token, (string)($_GET['token'] ?? ''))) {
        not_found();
    }
    require_once M1S_APP . '/schema.php';
    $r = run_install();
    header('Content-Type: text/plain; charset=utf-8');
    header('Cache-Control: no-store');
    echo implode("\n", $r['log']), "\n";
    if ($r['admin_password']) {
        echo "\nAdmin login: my1secret / {$r['admin_password']}\n(shown once; change it under Settings)\n";
    }
    exit;
}

function shop_page(): void
{
    $groups = [];
    foreach (topics() as $t) {
        $rows = all("SELECT * FROM products WHERE active = 1 AND (tags LIKE ? OR tags LIKE ? OR tags LIKE ? OR tags = ?) ORDER BY sort, id", tag_like('topic:' . $t['slug']));
        if ($rows) {
            $groups[] = [$t, $rows];
        }
    }
    render('shop', ['groups' => $groups], [
        'title' => 'Renter Essentials: Apartment & Home Finds',
        'description' => 'Practical picks for renters and homeowners: organization, small-space furniture, smart home, emergency prep and claim-ready tools.',
        'jsonld' => [breadcrumb_schema([['Shop', null]])],
        'breadcrumbs' => [['Shop', null]],
    ]);
}

/** Web app manifest (Android home-screen icons), served with the proper MIME type. */
function web_manifest(): void
{
    header('Content-Type: application/manifest+json; charset=utf-8');
    header('Cache-Control: public, max-age=86400');
    readfile(M1S_APP . '/site.webmanifest.json');
    exit;
}
