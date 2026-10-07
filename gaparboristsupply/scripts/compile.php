<?php
// Compiles the JSON content in site/data/ into site/data/catalog.php (a PHP
// array opcache can hold) and site/assets/data/catalog-lite.json (the slim
// product list the browser uses for search, filters, cart and compare).
//
//   php scripts/compile.php
//
// Also resolves the redirect table from seo-data/build-plan.json and strips
// body links that point at pages which don't exist.
declare(strict_types=1);
$root = dirname(__DIR__);
$data = "$root/site/data";
$warn = [];

function load_json(string $f): array {
    $d = json_decode(file_get_contents($f), true);
    if (!is_array($d)) { fwrite(STDERR, "Bad JSON: $f\n"); exit(1); }
    return $d;
}

$products = [];
foreach (glob("$data/products/*.json") as $f) {
    foreach (load_json($f) as $p) { $products[$p['path']] = $p; }
}
$categories = [];
foreach (glob("$data/categories/*.json") as $f) {
    foreach (load_json($f) as $c) { $categories[$c['path']] = $c; }
}
$brands = [];
if (is_file("$data/brands.json")) {
    foreach (load_json("$data/brands.json") as $b) { $brands[$b['path']] = $b; }
}
$guides = [];
if (is_file("$data/guides.json")) {
    foreach (load_json("$data/guides.json") as $g) { $guides[$g['path']] = $g; }
}
$plan = load_json("$root/seo-data/build-plan.json");

// ---- old URLs that were category views, not single products ------------------------
// path => [source category, brand slug or null, kind or null]. Rendered as a filtered listing.
$COLLECTIONS = [
    '/climbing/saddles-and-harnesses/weaver-saddles/' => ['/climbing/saddles-and-harnesses/', 'weaver', 'saddle'],
    '/climbing/spurs/lightweight-spurs/' => ['/climbing/spurs/', null, 'spur'],
    '/climbing/climbing-gear/mechanical-friction-devices/mrs-climbing-devices/' => ['/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-mrs/', null, null],
    '/climbing/climbing-gear/mechanical-friction-devices/srs-climbing-devices/' => ['/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-srs/', null, null],
];
$DROP = [ // pseudo-products that simply move to the matching category
    '/climbing/climbing-gear/carabiners-and-hardware/steel-carabiners/' => '/climbing/climbing-gear/carabiners-and-hardware/auto-locking-carabiners/',
    '/climbing/saddles-and-harnesses/full-body-harnesses/' => '/safety/fall-protection/',
    '/climbing/saddles-and-harnesses/saddle-accessories/' => '/climbing/saddles-and-harnesses/saddle-parts-and-shoulder-harnesses/',
    '/safety/helmets/' => '/climbing/helmets/',
    '/safety/chainsaw-protection/' => '/jobsite/chainsaw-accessories/chaps-and-protective-gear/',
];
$collections = [];
foreach ($COLLECTIONS as $path => $src) {
    if (!isset($products[$path])) continue;
    $p = $products[$path]; unset($products[$path]);
    $collections[$path] = ['path' => $path, 'name' => $p['name'], 'h1' => $p['h1'], 'keyword' => $p['keyword'], 'title' => $p['title'],
        'meta' => $p['meta'], 'kind' => $p['kind'], 'intro' => $p['summary'], 'guide' => $p['body'] ?? [], 'faq' => $p['faq'] ?? [], 'source' => $src];
}
foreach ($DROP as $from => $to) unset($products[$from]);

// ---- category tree ---------------------------------------------------------
function parent_path(string $p): ?string {
    $s = explode('/', trim($p, '/'));
    if (count($s) <= 1) return null;
    array_pop($s);
    return '/' . implode('/', $s) . '/';
}
ksort($categories);
foreach ($categories as $path => &$c) {
    $c['parent'] = null;
    for ($q = parent_path($path); $q !== null; $q = parent_path($q)) {
        if (isset($categories[$q])) { $c['parent'] = $q; break; }
    }
    $c['children'] = [];
    $c['products'] = [];
}
unset($c);
foreach ($categories as $path => $c) {
    if ($c['parent']) $categories[$c['parent']]['children'][] = $path;
}
// products: direct category, then roll up to ancestors
$brandSlugToPath = [];
foreach ($brands as $path => $b) { $brandSlugToPath[$b['slug']] = $path; }
foreach ($products as $path => &$p) {
    if (!isset($categories[$p['category']])) { $warn[] = "product $path has unknown category {$p['category']}"; continue; }
    $p['price'] = (int)($p['price'] ?? 0);
    $p['brand_path'] = $brandSlugToPath[$p['brand'] ?? ''] ?? null;
    for ($q = $p['category']; $q !== null; $q = $categories[$q]['parent']) {
        $categories[$q]['products'][] = $path;
    }
}
unset($p);
foreach ($collections as $path => $c) {
    [$srcCat, $brand, $kind] = $c['source'];
    $c['products'] = array_values(array_filter($categories[$srcCat]['products'] ?? [], fn($pp) => (!$brand || ($products[$pp]['brand'] ?? '') === $brand) && (!$kind || $products[$pp]['kind'] === $kind)));
    $c['children'] = [];
    $c['parent'] = null;
    for ($q = parent_path($path); $q !== null; $q = parent_path($q)) if (isset($categories[$q])) { $c['parent'] = $q; break; }
    unset($c['source']);
    $categories[$path] = $c;
    if ($c['parent']) $categories[$c['parent']]['children'][] = $path;
}
foreach ($categories as $path => $c) {
    if (!$c['products']) $warn[] = "category $path has no products";
}
foreach ($brands as $path => &$b) {
    $b['products'] = [];
    foreach ($products as $pp => $p) if (($p['brand'] ?? '') === $b['slug']) $b['products'][] = $pp;
}
unset($b);

// ---- redirects ---------------------------------------------------------------
$exists = fn(string $p) => isset($products[$p]) || isset($categories[$p]) || isset($brands[$p]) || isset($guides[$p]);
$redirects = [];
foreach (array_merge($plan['product_redirects'], $plan['category_redirects']) as $r) {
    $to = $r['to'];
    for ($i = 0; $i < 6 && !$exists($to) && ($q = parent_path($to)); $i++) $to = $q;
    if (!$exists($to)) $to = '/shop-all/';
    if (!$exists($r['path'])) $redirects[$r['path']] = $to;
}
foreach ($brands as $path => $b) {
    foreach ($b['aliases'] ?? [] as $a) $redirects[$a] = $path;
}
// planned brand URLs with no brand entry fall back to the brand index
foreach ($plan['brands'] as $b) if (!$exists($b['path']) && !isset($redirects[$b['path']])) $redirects[$b['path']] = '/brands/';
$redirects += $DROP;
$redirects += [
    '/climbing-gear/'      => '/climbing/climbing-gear/',
    '/volume-purchasing/'  => '/shop-all/',
    '/brands/all/'         => '/brands/',
];

// ---- body links: keep only links to real pages ----------------------------------
$static = ['/', '/shop-all/', '/brands/', '/guides/', '/tools/', '/cart/', '/about/', '/contact/'];
$linkOk = fn(string $h) => $exists($h) || in_array($h, $static, true) || str_starts_with($h, '/tools/');
$fixLinks = function (string $s) use ($linkOk, &$warn): string {
    return preg_replace_callback('#<a href="([^"]*)">(.*?)</a>#', function ($m) use ($linkOk, &$warn) {
        if ($linkOk($m[1])) return $m[0];
        $warn[] = "dropped link to {$m[1]}";
        return $m[2];
    }, $s);
};
$walk = function (array &$sections) use ($fixLinks) {
    foreach ($sections as &$s) {
        foreach (['p', 'list'] as $k) if (isset($s[$k])) foreach ($s[$k] as &$t) $t = $fixLinks($t);
        unset($t);
    }
};
foreach ($products as &$p) { if (isset($p['body'])) $walk($p['body']); } unset($p);
foreach ($categories as &$c) { if (isset($c['guide'])) $walk($c['guide']); } unset($c);
foreach ($guides as &$g) { if (isset($g['sections'])) $walk($g['sections']); } unset($g);

// ---- photos: each product, category and guide gets a real photo from its kind's pool ----
$images = is_file("$data/images.json") ? load_json("$data/images.json") : [];
$pool = fn(string $kind) => $images[$kind] ?? [];
$turn = [];
foreach ($products as $path => &$p) {               // round-robin per kind so neighbours differ
    $list = $pool($p['kind']);
    if (!$list) { $warn[] = "no photo for kind {$p['kind']}"; continue; }
    $i = $turn[$p['kind']] = (($turn[$p['kind']] ?? -1) + 1);
    $p['photo'] = $list[$i % count($list)];
}
unset($p);
foreach ($categories as $path => &$c) {
    $list = $pool($c['kind']);
    if ($list) $c['photo'] = $list[crc32($path) % count($list)];
}
unset($c);
foreach ($guides as $path => &$g) {
    $list = $pool($g['kind']);
    if ($list) $g['photo'] = $list[crc32($path) % count($list)];
}
unset($g);

$catalog = compact('products', 'categories', 'brands', 'guides', 'redirects', 'images');
$catalog['built'] = gmdate('Y-m-d');
file_put_contents("$data/catalog.php", "<?php\n// Generated by scripts/compile.php — do not edit.\nreturn " . var_export($catalog, true) . ";\n");

// ---- slim browser catalog -------------------------------------------------------
$lite = [];
foreach ($products as $path => $p) {
    $dept = '/' . explode('/', trim($p['category'], '/'))[0] . '/';
    $lite[] = [
        'p' => $path, 'n' => $p['name'], 'b' => $p['brand'] ?? '', 'bn' => $p['brand_name'] ?? '',
        'k' => $p['kind'], 'pr' => $p['price'], 'c' => $p['category'], 'd' => $dept,
        't' => $p['tagline'] ?? '', 'u' => $p['use'] ?? [], 'l' => $p['level'] ?? 'all',
        's' => array_slice($p['specs'] ?? [], 0, 8), 'i' => $p['photo']['sm'] ?? '',
    ];
}
@mkdir("$root/site/assets/data", 0775, true);
file_put_contents("$root/site/assets/data/catalog-lite.json", json_encode($lite, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE));

printf("products %d, categories %d, brands %d, guides %d, redirects %d\n",
    count($products), count($categories), count($brands), count($guides), count($redirects));
foreach (array_unique($warn) as $w) fwrite(STDERR, "warn: $w\n");
