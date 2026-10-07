<?php
// Gap Arborist Supply — front controller. The host serves real files directly
// and sends everything else here (there is deliberately no index.html).
declare(strict_types=1);
const GAP = true;
require __DIR__ . '/app/bootstrap.php';

$uri  = $_SERVER['REQUEST_URI'] ?? '/';
$path = rawurldecode(strtok($uri, '?') ?: '/');
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');

// Canonical host + https once the real domain is live.
if ($CFG['live']) {
    $insecure = ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? 'https') === 'http';
    if ($insecure || ($host !== '' && $host !== $CFG['canonical_host'])) redirect($CFG['origin'] . $uri);
}

// ---- machine files ------------------------------------------------------------
if ($path === '/robots.txt') {
    header('Content-Type: text/plain; charset=utf-8');
    if (!$CFG['live']) { echo "User-agent: *\nDisallow: /\n"; exit; }
    echo "User-agent: *\nDisallow: /cart/\nDisallow: /search/\nDisallow: /search.php\nDisallow: /go/\nAllow: /\n\nSitemap: " . abs_url('/sitemap.xml') . "\n";
    exit;
}
if ($path === '/sitemap.xml') {
    header('Content-Type: application/xml; charset=utf-8');
    $urls = ['/', '/shop-all/', '/brands/', '/guides/', '/tools/', '/about/', '/contact/'];
    foreach (TOOLS as $slug => $_) $urls[] = "/tools/$slug/";
    foreach (['categories', 'products', 'brands', 'guides'] as $set) foreach ($CAT[$set] as $p => $_) $urls[] = $p;
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach ($urls as $u) echo '<url><loc>' . e(abs_url($u)) . '</loc><lastmod>' . $CAT['built'] . "</lastmod></url>\n";
    echo "</urlset>\n";
    exit;
}

// ---- outbound retailer links: /go/?p=/product/path/ ---------------------------------
if ($path === '/go/' || $path === '/go') {
    $p = $CAT['products'][(string)($_GET['p'] ?? '')] ?? null;
    header('X-Robots-Tag: noindex, nofollow');
    redirect($p ? aff_url($p) : '/', 302);
}

// ---- old search URLs (the old store's /search.php is linked from other sites) -------
if ($path === '/search.php' || $path === '/search' || $path === '/standard/search') {
    $q = $_GET['search_query'] ?? $_GET['q'] ?? $_GET['s'] ?? '';
    redirect('/search/' . ($q !== '' ? '?q=' . rawurlencode($q) : ''));
}
if ($path === '/' && isset($_GET['s'])) redirect('/search/?q=' . rawurlencode((string)$_GET['s']));

if (str_starts_with($path, '/?')) redirect('/');

// ---- trailing slash + lowercase -------------------------------------------------
if ($path !== '/' && !str_ends_with($path, '/') && !preg_match('/\.[a-z0-9]{2,4}$/i', $path)) {
    $try = $path . '/';
    if (isset($CAT['products'][$try]) || isset($CAT['categories'][$try]) || isset($CAT['brands'][$try]) || isset($CAT['guides'][$try]) || isset($CAT['redirects'][$try])
        || in_array($try, ['/shop-all/', '/brands/', '/guides/', '/tools/', '/cart/', '/about/', '/contact/', '/search/', '/affiliate-disclosure/', '/privacy-policy/', '/terms-of-use/'], true)
        || isset(TOOLS[trim(substr($try, 7), '/')])) {
        redirect($try . (($q = parse_url($uri, PHP_URL_QUERY)) ? "?$q" : ''));
    }
}

// ---- routes -------------------------------------------------------------------
switch ($path) {
    case '/':          render('home');
    case '/shop-all/': render('shop');
    case '/brands/':   render('brands');
    case '/guides/':   render('guides');
    case '/tools/':    render('tools');
    case '/cart/':     render('cart');
    case '/search/':   render('search', ['q' => trim((string)($_GET['q'] ?? ''))]);
    case '/about/': case '/contact/': case '/affiliate-disclosure/': case '/privacy-policy/': case '/terms-of-use/':
        render('page', ['slug' => trim($path, '/')]);
}
if (preg_match('#^/tools/([a-z0-9\-]+)/$#', $path, $m) && isset(TOOLS[$m[1]])) render('tool', ['slug' => $m[1]]);
if (isset($CAT['products'][$path]))   render('product', ['p' => $CAT['products'][$path]]);
if (isset($CAT['categories'][$path])) render('category', ['c' => $CAT['categories'][$path]]);
if (isset($CAT['brands'][$path]))     render('brand', ['b' => $CAT['brands'][$path]]);
if (isset($CAT['guides'][$path]))     render('guide', ['g' => $CAT['guides'][$path]]);
if (isset($CAT['redirects'][$path]))  redirect($CAT['redirects'][$path]);

// Lower-case variants of real pages.
$lower = strtolower($path);
if ($lower !== $path && (isset($CAT['products'][$lower]) || isset($CAT['categories'][$lower]) || isset($CAT['redirects'][$lower]))) redirect($lower);

// Backlinked URLs from the store's earlier platforms, pinned to the closest page.
const LEGACY = [
    'singing-tree-rope-runner' => '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-srs/',
    'petzl-ok-triact-locking-carabiner-tactical-black' => '/climbing/climbing-gear/carabiners-and-hardware/auto-locking-carabiners/',
    '8mm-sirius-hitch-cord' => '/rope/tech-cordage/',
    '8mm-yale-bee-line' => '/climbing/climbing-gear/hitch-cord-and-split-tails/split-tails/yale-8mm-bee-line-split-tail/',
    'yale-scandere-117mm-climbing-line-200ft' => '/rope/climbing-rope/static-climbing-rope/',
    'yale-cordage-double-braid-splicing-training-kit' => '/rope/rope-care-and-splicing/',
    'weaver-shin-cup-climber-pads' => '/climbing/spurs/climber-pads/',
    'rock-exotica-omni-block-45' => '/rigging/blocks-and-other-hardware/rigging-pulleys/',
    'razor-back-michigan-axe' => '/jobsite/logging-tools/axes-and-mauls/',
    'the-sawpod' => '/climbing/climbing-gear/other-gear/the-sawpod/',
    'good-rigging-control-system-drill-driver-adapter' => '/rigging/lowering-devices/good-rigging-control-system/',
    'threaded-pocket-for-tomahawk-stump-grinder-teeth' => '/jobsite/stump-grinding/',
    'counter-bore-pocket-for-tomahawk-stump-grinder-teeth' => '/jobsite/stump-grinding/',
    'tomahawk-stump-grinder-teeth-left' => '/jobsite/stump-grinding/',
    'arbortec-scafell-lite-boots' => '/clothing/arborist-boots/arbortec-scafell-lite-chainsaw-boots-lime-green/',
];
$first = strtolower(explode('/', trim($path, '/'))[0] ?? '');
if (isset(LEGACY[$first])) redirect(LEGACY[$first]);

// Old store platforms: /Some-Product-Name/item/123, /X/image/item/..., /shop/product/slug/, /Name/folder/8
if (preg_match('#^/(?:shop/product/)?([A-Za-z0-9%\-\.]+)/(?:image/)?(?:item|folder)\b#', $path, $m)
    || preg_match('#^/shop/product/([a-z0-9\-]+)/?$#', $path, $m)
    || preg_match('#^/([A-Z][A-Za-z0-9\-]+)/?$#', $path, $m)) {
    redirect(fuzzy_target($m[1]));
}
if (preg_match('#^/image/item/#', $path)) redirect('/shop-all/');
// Old WordPress / WooCommerce paths
if (preg_match('#^/(wp-admin|wp-login\.php|wp-content|wp-includes|xmlrpc\.php|feed|cart|checkout|my-account|product-category|product)(/|$)#', $path)) redirect('/');

render('404', [], 404);
