<?php
declare(strict_types=1);
defined('M1S') || exit;

/**
 * Amazon affiliate product recommendations.
 *
 * Each product links either to a URL an admin pasted (any amazon.com product
 * link, e.g. https://www.amazon.com/dp/B0XXXXXXX) or, by default, to an Amazon
 * search for its query. The Associates tag is always (re)applied, so links stay
 * attributed even if someone pastes a link with another tag.
 * Tags: "article:<slug>" ties a product to one article, "topic:<slug>" to a blog topic,
 * "shop" shows it on /shop/.
 */
function amazon_tag(): string
{
    return (string)cfg('amazon_tag', 'josephrayditt-20');
}

function amazon_url(array $p): string
{
    $url = trim((string)($p['url'] ?? ''));
    if ($url !== '' && preg_match('#^https://(www\.)?amazon\.com/#i', $url)) {
        $parts = parse_url($url);
        parse_str($parts['query'] ?? '', $qs);
        $qs['tag'] = amazon_tag();
        return 'https://www.amazon.com' . ($parts['path'] ?? '/') . '?' . http_build_query($qs);
    }
    if (preg_match('/^[A-Z0-9]{10}$/', $url)) {   // bare ASIN
        return 'https://www.amazon.com/dp/' . $url . '/?tag=' . amazon_tag();
    }
    return 'https://www.amazon.com/s?' . http_build_query(['k' => $p['query'] ?: $p['name'], 'tag' => amazon_tag()]);
}

/** Products for an article: its own picks first, then its topic's, up to $limit. */
function products_for_article(array $a, int $limit = 5): array
{
    $own = all("SELECT * FROM products WHERE active = 1 AND (tags LIKE ? OR tags LIKE ? OR tags LIKE ? OR tags = ?) ORDER BY sort, id",
        tag_like('article:' . $a['slug']));
    if (count($own) >= 3 || empty($a['topic_slug'])) {
        return array_slice($own, 0, $limit);
    }
    $topic = all("SELECT * FROM products WHERE active = 1 AND (tags LIKE ? OR tags LIKE ? OR tags LIKE ? OR tags = ?) ORDER BY sort, id",
        tag_like('topic:' . $a['topic_slug']));
    $seen = array_column($own, 'id');
    foreach ($topic as $p) {
        if (!in_array($p['id'], $seen, false)) {
            $own[] = $p;
        }
    }
    return array_slice($own, 0, $limit);
}

/** LIKE patterns matching one tag inside a comma-separated list. */
function tag_like(string $tag): array
{
    return [$tag . ',%', '%,' . $tag . ',%', '%,' . $tag, $tag];
}

function amazon_disclosure(): string
{
    return 'As an Amazon Associate, My 1 Secret earns from qualifying purchases. Links open Amazon; we never see what you buy.';
}

function product_box(array $products, string $heading = 'Helpful finds for this guide'): string
{
    if (!$products) {
        return '';
    }
    $h = '<aside class="products" aria-label="Recommended products">' . ($heading !== '' ? '<h2 class="products-h">' . e($heading) . '</h2>' : '') . '<ul class="product-list">';
    foreach ($products as $p) {
        $url = amazon_url($p);
        $h .= '<li class="product">'
            . ($p['image'] ? '<img src="' . e($p['image']) . '" alt="" loading="lazy" width="72" height="72">' : '<span class="product-icon" aria-hidden="true">🛒</span>')
            . '<div><a class="product-name" href="' . e($url) . '" rel="sponsored nofollow noopener" target="_blank">' . e($p['name']) . '</a>'
            . ($p['blurb'] ? '<p>' . e($p['blurb']) . '</p>' : '') . '</div>'
            . '<a class="btn btn-sm btn-amazon" href="' . e($url) . '" rel="sponsored nofollow noopener" target="_blank">See options on Amazon</a></li>';
    }
    return $h . '</ul><p class="disclosure">' . e(amazon_disclosure()) . '</p></aside>';
}
