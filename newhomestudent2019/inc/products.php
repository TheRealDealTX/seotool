<?php defined('NHS') || exit;

const PRODUCT_GROUPS = [
    'books'      => ['Books for Home Builders', 'book'],
    'tools'      => ['Owner-Builder Tools', 'tool'],
    'safety'     => ['Safety & Protection', 'shield'],
    'smart-home' => ['Smart Home & Security', 'chip'],
    'energy'     => ['Energy Efficiency', 'bolt'],
    'office'     => ['Planning & Paperwork', 'clip'],
    'investing'  => ['Real Estate Investing Books', 'chart'],
    'home'       => ['Home & Apartment Comfort', 'sofa'],
    'outdoor'    => ['Patio, Balcony & Garden', 'leaf'],
    'moving'     => ['Moving Day', 'box'],
    'pets'       => ['Moving with Pets', 'paw'],
];

function amazon_url(?string $asin, string $query): string {
    $tag = rawurlencode(SITE['amazon_tag']);
    if ($asin) return 'https://www.amazon.com/dp/' . rawurlencode($asin) . '?tag=' . $tag;
    return 'https://www.amazon.com/s?k=' . rawurlencode($query) . '&tag=' . $tag;
}

function products(): array {
    static $all = null;
    if ($all !== null) return $all;
    $meta = require APP_ROOT . '/data/product-meta.php';
    $asins = is_file(APP_ROOT . '/data/asins.php') ? require APP_ROOT . '/data/asins.php' : [];
    $all = [];
    foreach ($meta as $key => [$name, $blurb, $group, $query]) {
        $a = $asins[$key] ?? null;
        $all[$key] = [
            'key' => $key,
            'name' => $name,
            'blurb' => $blurb,
            'group' => $group,
            'asin' => $a,
            'url' => amazon_url($a, $query),
        ];
    }
    return $all;
}

function product(string $key): ?array { return products()[$key] ?? null; }

function product_card(array $p): string {
    $iconName = PRODUCT_GROUPS[$p['group']][1] ?? 'house';
    return '<div class="product">'
        . '<span class="product-icon">' . icon($iconName) . '</span>'
        . '<div class="product-body">'
        . '<h3 class="product-name">' . e($p['name']) . '</h3>'
        . '<p>' . e($p['blurb']) . '</p>'
        . '<a class="btn btn-amz" href="' . e($p['url']) . '" rel="sponsored nofollow noopener" target="_blank">Check price on Amazon</a>'
        . '</div></div>';
}

function product_grid(array $keys, string $heading = ''): string {
    $cards = '';
    foreach ($keys as $k) {
        $p = product($k);
        if ($p) $cards .= product_card($p);
    }
    if ($cards === '') return '';
    return '<aside class="products" aria-label="Recommended products">'
        . ($heading !== '' ? '<p class="products-title">' . e($heading) . '</p>' : '')
        . '<div class="product-grid">' . $cards . '</div>'
        . '<p class="products-note">Affiliate links — we may earn a commission at no extra cost to you.</p>'
        . '</aside>';
}
