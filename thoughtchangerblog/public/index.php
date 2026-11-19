<?php
// Thought Changer — front controller. Every request that is not an existing file lands here.
declare(strict_types=1);
require __DIR__ . '/app/bootstrap.php';

$uri   = $_SERVER['REQUEST_URI'] ?? '/';
$path  = rawurldecode((string) parse_url($uri, PHP_URL_PATH));
$query = $_GET;
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';

function redirect(string $to, int $code = 301): never {
    header('Location: ' . (str_starts_with($to, 'http') ? $to : SITE_URL . $to), true, $code);
    exit;
}

function not_found(): never {
    http_response_code(404);
    view('404');
    exit;
}

// 1. Canonical host + HTTPS (TLS may terminate upstream, so trust X-Forwarded-Proto too).
$host = strtolower($_SERVER['HTTP_HOST'] ?? 'thoughtchangerblog.com');
$https = ($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https'
      || ($_SERVER['SERVER_PORT'] ?? '') === '443';
$isLocal = str_starts_with($host, 'localhost') || str_starts_with($host, '127.0.0.1') || getenv('TC_DEV');
if (!$isLocal && (!in_array($host, ['thoughtchangerblog.com', 'staging.thoughtchangerblog.com'], true) || !$https)) redirect($uri);

// 2. Legacy query-string URLs.
if (isset($query['p']) && ctype_digit((string) $query['p'])) {
    $ids = json_decode((string) file_get_contents(WEBROOT . '/content/legacy-ids.json'), true) ?: [];
    redirect(isset($ids[$query['p']]) ? '/' . $ids[$query['p']] . '/' : '/');
}
if (isset($query['m']) && count($query) === 1) redirect($path);              // Blogger ?m=1
if (isset($query['s']) && $path === '/') { view('search', ['q' => trim((string) $query['s'])]); exit; }

// 3. Forms.
if ($method === 'POST') { require APP . '/forms.php'; handle_form($path); exit; }

$p = $path;
$lower = strtolower($p);

// 4. Fixed routes.
$static = [
    '/'                     => fn() => view('home'),
    '/blog/'                => fn() => view('archive', ['kind' => 'blog', 'page' => 1]),
    '/mindset/'             => fn() => view('archive', ['kind' => 'Mindset', 'page' => 1]),
    '/quotes/'              => fn() => view('archive', ['kind' => 'Quotes', 'page' => 1]),
    '/category/general/'    => fn() => view('archive', ['kind' => 'General', 'page' => 1]),
    '/about-us/'            => fn() => view('page', ['slug' => 'about-us']),
    '/contact-us/'          => fn() => view('contact'),
    '/privacy-policy/'      => fn() => view('page', ['slug' => 'privacy-policy']),
    '/terms-of-use/'        => fn() => view('page', ['slug' => 'terms-of-use']),
    '/affiliate-disclosure/'=> fn() => view('page', ['slug' => 'affiliate-disclosure']),
    '/recommended-reads/'   => fn() => view('bookshelf'),
    '/feed/'                => fn() => view('feed'),
    '/sitemap_index.xml'    => fn() => view('sitemap', ['which' => 'index']),
    '/post-sitemap.xml'     => fn() => view('sitemap', ['which' => 'post']),
    '/page-sitemap.xml'     => fn() => view('sitemap', ['which' => 'page']),
    '/category-sitemap.xml' => fn() => view('sitemap', ['which' => 'category']),
];
if (isset($static[$p])) { $static[$p](); exit; }

// Paginated archives: /blog/page/2/, /category/general/page/2/, /page/2/ (old home pagination).
if (preg_match('#^/(blog|category/general|mindset|quotes)/page/(\d+)/$#', $p, $m)) {
    $kind = ['blog' => 'blog', 'category/general' => 'General', 'mindset' => 'Mindset', 'quotes' => 'Quotes'][$m[1]];
    if ((int) $m[2] === 1) redirect('/' . $m[1] . '/');
    view('archive', ['kind' => $kind, 'page' => (int) $m[2]]);
    exit;
}
if (preg_match('#^/page/(\d+)/?$#', $p, $m)) redirect('/blog/' . ((int) $m[1] > 1 ? 'page/' . (int) $m[1] . '/' : ''));

// 5. Posts.
if (preg_match('#^/([a-z0-9_-]+)/$#', $p, $m) && ($post = post_by_slug($m[1]))) {
    view('post', ['post' => $post]);
    exit;
}

// 6. Redirect rules for everything WordPress/Blogger ever exposed.
$aliases = [
    'sitemap.xml' => '/sitemap_index.xml', 'sitemap' => '/sitemap_index.xml', 'wp-sitemap.xml' => '/sitemap_index.xml',
    'comments/feed' => '/feed/', 'rss' => '/feed/', 'feeds/posts/default' => '/feed/', 'rss.xml' => '/feed/', 'atom.xml' => '/feed/',
    'category/mindset' => '/mindset/', 'category/quotes' => '/quotes/', 'category/uncategorized' => '/blog/',
    'about' => '/about-us/', 'contact' => '/contact-us/', 'p/about.html' => '/about-us/', 'p/contact.html' => '/contact-us/',
    'privacy' => '/privacy-policy/', 'terms' => '/terms-of-use/', 'home' => '/', 'index.html' => '/', 'index.php' => '/',
    'org' => '/', 'thoughtchangerblog.com/index.html' => '/', 'i-hashang/...' => '/i-had-an-epiphany-the-courtship-of-an-idea/',
    'shop' => '/recommended-reads/', 'books' => '/recommended-reads/',
    'barrier-or-boundary-it-starts-with-a-thought' => '/boundaries-vs-barriers/',
    'in-alignment-a-life-philosophy' => '/with-to-in-alignment-living-and-leading-from-congruence/',
    'complacency' => '/11-signs-youre-stuck-in-complacency/', 'stuck-in-complacency' => '/11-signs-youre-stuck-in-complacency/',
    'the-courtship-of-an-idea' => '/i-had-an-epiphany-the-courtship-of-an-idea/',
    'what-an-epiphany-really-is-and-what-it-isnt' => '/i-had-an-epiphany-the-courtship-of-an-idea/',
];
$key = trim($lower, '/');
if (isset($aliases[$key])) redirect($aliases[$key]);

// Bot noise for WordPress internals: real 404, never a redirect.
if (preg_match('#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php|wp-content/(plugins|themes)|\.env|\.git)#i', $p)
    || preg_match('#\.(php|asp|aspx|jsp|cgi|env|sql|zip|bak)$#i', $p)) not_found();
// Missing media files stay 404 (no soft redirects for images).
if (preg_match('#^/wp-content/#i', $p)) not_found();

// /slug/feed/, /slug/amp/, /slug/embed/, /slug/comment-page-2/ … -> the post itself.
if (preg_match('#^/([^/]+)/(feed|amp|embed|trackback|comment-page-\d+|attachment/.*)/?$#i', $p, $m) && post_by_slug(strtolower($m[1]))) {
    redirect('/' . strtolower($m[1]) . '/');
}
// /author/*, /tag/*, /search/*, /date archives -> nearest listing.
if (preg_match('#^/(author|tag)(/|$)#i', $p)) redirect('/blog/');
if (preg_match('#^/search/(label/)?(.+?)/?$#i', $p, $m)) redirect('/?s=' . urlencode(str_replace(['-', '+'], ' ', $m[2])));

// Blogger permalinks /YYYY/MM/slug.html and anything else: match to a post by slug similarity.
$cands = [];
if (preg_match('#^/\d{4}/\d{2}/([^/]+?)(\.html)?/?$#i', $p, $m)) $cands[] = $m[1];
foreach (explode('/', trim($p, '/')) as $seg) if ($seg !== '' && !preg_match('#^\d+$#', $seg)) $cands[] = $seg;

$best = null; $bestScore = 0.0;
foreach ($cands as $c) {
    $c = strtolower(preg_replace('/[^a-z0-9]+/i', '-', $c));
    $c = trim(preg_replace('/\.html$/', '', $c), '-');
    if ($c === '') continue;
    foreach (posts() as $post) {
        $s = $post['slug'];
        $norm = str_replace('_', '-', $s);
        if ($c === $s || $c === $norm) { $best = $s; $bestScore = 101; break 2; }
        similar_text($c, $norm, $pct);
        if (strlen($c) >= 12 && (str_starts_with($norm, $c) || str_starts_with($c, $norm))) $pct = max($pct, 90);
        if ($pct > $bestScore) { $bestScore = $pct; $best = $s; }
    }
}
if ($best && $bestScore >= 72) redirect('/' . $best . '/');

// Missing trailing slash on a fixed route.
if (!str_ends_with($p, '/') && isset($static[$p . '/'])) redirect($p . '/');
if ($lower !== $p && isset($static[$lower])) redirect($lower);

// The WordPress site sent every unknown URL to the homepage; keep that for content-looking paths so
// no inbound link lands on an error, but show a proper 404 for obviously bogus requests.
if (preg_match('#^/\d{4}(/\d{2})?/#', $p)) redirect('/');
not_found();
