<?php
// asmith.photography front controller. The host serves real files directly and routes
// everything else here (it ignores .htaccess). See README.
$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?'));
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
$qs   = strpos($uri, '?') !== false ? substr($uri, strpos($uri, '?')) : '';
$canon = 'https://asmith.photography';

// Production host: force https and the bare domain. TLS terminates upstream.
$prod = ($host === 'asmith.photography' || $host === 'www.asmith.photography');
if ($prod && (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || $host === 'www.asmith.photography')) {
    header('Location: ' . $canon . $uri, true, 301);
    exit;
}
// Temporary/preview hosts must not be indexed.
if (!$prod) {
    header('X-Robots-Tag: noindex, nofollow');
}

$routes = [
    'about' => 1,
    'alaska' => 1,
    'angela-lindvall-for-the-laterals-new' => 1,
    'awareness-kenneth-cole' => 1,
    'baseball-teens' => 1,
    'bello-magazine-december-cover-story' => 1,
    'bud-light-my-team-can' => 1,
    'car-window-for-damaged-goods-magazine' => 1,
    'contact' => 1,
    'credits' => 1,
    'dave-roberts-for-ucla' => 1,
    'disney-interactive' => 1,
    'dodgers-billy-gasparino-for-c-magazine' => 1,
    'downtown-for-something-about-magazine' => 1,
    'etnia-barcelona-vintage-collection-campaign' => 1,
    'fila-2016' => 1,
    'fila-spring-2017' => 1,
    'florsheim-shoes' => 1,
    'football' => 1,
    'george-esquivel-for-c-magazine' => 1,
    'janelle-monae-for-nylon-magazine' => 1,
    'johnny-layton-for-vans' => 1,
    'journal' => 1,
    'kenneth-cole' => 1,
    'kenneth-cole-summer-2015' => 1,
    'kilian-martin-for-stern-magazine' => 1,
    'leica-sofort-campaign-2' => 1,
    'lifestyle-book-1' => 1,
    'nas-for-bevel' => 1,
    'neff-headwear-summer-campaign' => 1,
    'nike-running' => 1,
    'nike-sb' => 1,
    'nunn-bush-spring-2017' => 1,
    'park-and-ride-film' => 1,
    'people' => 1,
    'personal-weekly' => 1,
    'poland-national-team-velodrome-training' => 1,
    'polaroid-eyewear' => 1,
    'quiksilver' => 1,
    'shaun-white-for-oakley' => 1,
    'skateboarding' => 1,
    'something-about-magazine-film' => 1,
    'spring-2018-florsheim' => 1,
    'stacy-adams-shoes' => 1,
    'stacy-adams-spring-2016-campaign' => 1,
    'stacy-adams-spring-2017' => 1,
    'stacy-adams-spring-2018' => 1,
    'thrasher-magazine' => 1,
    'timothy-brady-for-nylon-mens' => 1,
    'ucla-water-polo' => 1,
    'waldo-fernandez-for-la-confidential' => 1,
    'womens-march-los-angeles' => 1
];
$redirects = [
    '/fila-spring-2017-new' => '/fila-spring-2017',
    '/etnia-barcelona-vintage-campaign-2016' => '/etnia-barcelona-vintage-collection-campaign',
    '/leica-sofort-campaign-3' => '/leica-sofort-campaign-2',
    '/m/disney-mix' => '/disney-interactive',
    '/m//day-in-the-life-kelly-vittengl/kelly-vittengl-of-coed-venice-59_3_705.html' => '/people'
];

function send_page($file, $code = 200) {
    http_response_code($code);
    header('Content-Type: text/html; charset=utf-8');
    readfile(__DIR__ . '/' . $file);
    exit;
}

if ($path === '/' || $path === '/index.php' || $path === '/home') {
    if ($path !== '/') { header('Location: /' . $qs, true, 301); exit; }
    send_page('home.html');
}
if (isset($redirects[$path])) {
    header('Location: ' . $redirects[$path], true, 301);
    exit;
}
// Old portfolio used /m/<slug> for mobile pages.
if (preg_match('#^/m/+([a-z0-9-]+)/?$#', $path, $m) && isset($routes[$m[1]])) {
    header('Location: /' . $m[1], true, 301);
    exit;
}
$slug = trim($path, '/');
if ($slug !== '' && $path !== '/' . $slug && isset($routes[$slug])) {
    header('Location: /' . $slug . $qs, true, 301);   // strip trailing slash
    exit;
}
if (strtolower($slug) !== $slug && isset($routes[strtolower($slug)])) {
    header('Location: /' . strtolower($slug) . $qs, true, 301);
    exit;
}

if ($slug === 'contact' && ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
    $f = function ($k, $n) { return mb_substr(trim((string)($_POST[$k] ?? '')), 0, $n); };
    if ($f('website', 10) === '' && filter_var($f('email', 200), FILTER_VALIDATE_EMAIL) && $f('message', 5000) !== '') {
        $dir = dirname(__DIR__) . '/asmith-messages';
        if (!is_dir($dir)) { @mkdir($dir, 0700, true); }
        $row = ['at' => gmdate('c'), 'ip' => $_SERVER['REMOTE_ADDR'] ?? '', 'name' => $f('name', 120),
                'email' => $f('email', 200), 'topic' => $f('topic', 40), 'message' => $f('message', 5000)];
        @file_put_contents($dir . '/messages.jsonl', json_encode($row) . "\n", FILE_APPEND | LOCK_EX);
        $from = filter_var($row['email'], FILTER_VALIDATE_EMAIL) ? str_replace(["\r", "\n"], '', $row['email']) : '';
        @mail('info@asmith.photography', '[asmith.photography] ' . $row['topic'] . ' from ' . str_replace(["\r", "\n"], ' ', $row['name']),
              $row['message'] . "\n\n-- " . $row['name'] . ' <' . $from . '>',
              'From: info@asmith.photography' . "\r\n" . ($from ? 'Reply-To: ' . $from : ''));
    }
    header('Location: /contact?sent=1', true, 303);
    exit;
}
if (isset($routes[$slug])) {
    send_page('pages/' . $slug . '.html');
}
send_page('404.html', 404);
