<?php
// agadecor.com front controller. See README "Hosting" — the platform serves real
// files directly and sends every other path here.
declare(strict_types=1);

const PROD_HOST = 'agadecor.com';
const ORIGIN = 'https://agadecor.com';
// Where inquiry emails go. Every inquiry is also appended to _leads/leads.php (one JSON
// object per line). It starts with an exit() guard, so requesting it over HTTP shows nothing;
// read it in the hPanel File Manager.
const LEAD_EMAIL = '';
// Old Wix member-profile URLs (/profile/<id>/profile) only ever received nofollow
// spam links. 'gone' answers 410; set to 'home' to 301 them to the homepage instead.
const PROFILE_MODE = 'gone';

$routes = require __DIR__ . '/routes.php';
$uri = $_SERVER['REQUEST_URI'] ?? '/';
$path = parse_url($uri, PHP_URL_PATH) ?: '/';
$path = preg_replace('#/{2,}#', '/', $path);
$query = (string) parse_url($uri, PHP_URL_QUERY);
$host = strtolower(preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? ''));
$isProd = $host === PROD_HOST || $host === 'www.' . PROD_HOST;

function go(string $to, int $code = 301): void {
    header('Location: ' . $to, true, $code);
    exit;
}
function page(string $file, int $code = 200): void {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    readfile(__DIR__ . '/pages/' . $file);
    exit;
}

if ($isProd) {
    // TLS terminates upstream; plain http shows up as X-Forwarded-Proto: http.
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http';
    if ($insecure || $host !== PROD_HOST) go(ORIGIN . $uri);
} else {
    // Temporary / preview domain: keep it out of search indexes.
    header('X-Robots-Tag: noindex, nofollow');
}

// robots.txt and sitemap.xml are generated so they can differ per host.
if ($path === '/robots.txt') {
    header('Content-Type: text/plain; charset=utf-8');
    echo $isProd
        ? "User-agent: *\nDisallow: /pages/\nDisallow: /routes.php\n\nSitemap: " . ORIGIN . "/sitemap.xml\n"
        : "User-agent: *\nDisallow: /\n";
    exit;
}
if ($path === '/sitemap.xml') {
    header('Content-Type: application/xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach ($routes as $p => [$file, $lastmod, $prio]) {
        echo '  <url><loc>' . htmlspecialchars(ORIGIN . $p) . "</loc><lastmod>$lastmod</lastmod><priority>$prio</priority></url>\n";
    }
    echo "</urlset>\n";
    exit;
}

// Inquiry form.
if ($path === '/contact-us' && ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    $f = fn(string $k, int $max = 300) => trim(mb_substr(strip_tags((string) ($_POST[$k] ?? '')), 0, $max));
    $email = filter_var($f('email'), FILTER_VALIDATE_EMAIL);
    $ts = (int) ($_POST['ts'] ?? 0);
    $bot = $f('website') !== '' || ($ts > 0 && (int) (microtime(true) * 1000) - $ts < 2500);
    if ($bot) go('/contact-us?sent=1#form', 303);              // silently drop spam
    if (!$email || $f('name') === '') go('/contact-us?sent=0#form', 303);
    $services = array_map(fn($s) => preg_replace('/[^a-z]/', '', (string) $s), (array) ($_POST['services'] ?? []));
    $lead = [
        'received' => gmdate('c'), 'name' => $f('name'), 'email' => $email, 'phone' => $f('phone', 40),
        'date' => $f('date', 20), 'venue' => $f('venue'), 'guests' => $f('guests', 20),
        'services' => implode(', ', $services), 'heard' => $f('heard', 60), 'message' => $f('message', 4000),
        'host' => $host, 'ip' => $_SERVER['REMOTE_ADDR'] ?? '',
    ];
    $log = __DIR__ . '/_leads/leads.php';
    if (!is_dir(dirname($log))) @mkdir(dirname($log), 0750);
    if (!is_file($log)) @file_put_contents($log, "<?php http_response_code(404); exit; ?>\n");
    @file_put_contents($log, json_encode($lead, JSON_UNESCAPED_UNICODE) . "\n", FILE_APPEND | LOCK_EX);
    if (LEAD_EMAIL !== '') {
        $body = '';
        foreach ($lead as $k => $v) $body .= ucfirst($k) . ': ' . $v . "\n";
        @mail(LEAD_EMAIL, 'New AGA Décor inquiry: ' . $lead['name'], $body,
              "From: AGA Decor <no-reply@" . PROD_HOST . ">\r\nReply-To: " . $email . "\r\nContent-Type: text/plain; charset=utf-8");
    }
    go('/contact-us?sent=1#form', 303);
}

// Exact route.
if (isset($routes[$path])) page($routes[$path][0]);

// Trailing slash or wrong case on a known route -> canonical form.
$trim = $path === '/' ? '/' : rtrim($path, '/');
foreach ($routes as $p => $_) {
    if (strcasecmp($p, $trim) === 0) go($p . ($query !== '' ? '?' . $query : ''));
}

// Legacy URLs from the old Wix (2013-2024) and HTML (2012) sites.
$legacy = [
    '#^/(index\.html?|home|2home|index\.php)$#i'                    => '/',
    '#^/aga-galus$#i'                                               => '/about-us',
    '#^/(copy-of-gallery|photo-gallery\.html|gallery\.html)$#i'     => '/gallery',
    '#^/(book-online|contact\.html|contact)$#i'                     => '/contact-us',
    '#^/(shop-1|shop|cart-page|backdrops\.html)$#i'                 => '/decor-rental',
    '#^/product-page/#i'                                            => '/decor-rental',
    '#^/(ceremony|hall|mandaps)\.html$#i'                           => '/services',
    '#^/(packages|wedding-planning)$#i'                             => '/wedding-planing',
    '#^/honeymoon$#i'                                               => '/destination-weddings',
    '#^/(blog/(archive|date|author|tag|categories|hashtags)/.*|blog-feed\.xml|feed\.xml|feed|single-post)$#i' => '/blog',
    '#^/(account|members|_api|_partials)(/.*)?$#i'                  => '/',
    '#^/(wp-admin|wp-login\.php|xmlrpc\.php|wp-includes|wp-json)(/.*)?$#i' => '/',
];
foreach ($legacy as $re => $to) {
    if (preg_match($re, $trim)) go($to);
}

// Old Wix blog post URLs with a different date or case -> match on the slug.
if (preg_match('#^/(single-)?post/(?:\d{4}/\d{2}/\d{2}/)?([^/]+)$#i', $trim, $m)) {
    foreach ($routes as $p => $_) {
        if (strcasecmp(basename($p), $m[2]) === 0) go($p);
    }
    go('/blog');
}

if (preg_match('#^/profile/[^/]+(/profile)?$#i', $trim)) {
    if (PROFILE_MODE === 'home') go('/');
    page('_410.html', 410);
}

page('_404.html', 404);
