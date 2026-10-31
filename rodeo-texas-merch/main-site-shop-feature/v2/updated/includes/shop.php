<?php
/**
 * RODEO TEXAS SHOP (shop.rodeotexas.org). Edit shop_products() to change the
 * merch featured on the homepage and in articles. Images live in
 * /assets/img/shop/<slug>.webp. Shop links always open in a new tab.
 */
defined('RT_APP') || exit;

const SHOP_URL = 'https://shop.rodeotexas.org';

/** Featured products: [product slug on the shop, name, short label, image alt text] */
function shop_products(): array
{
    return [
        ['lone-star-tour-tee-dark', 'Lone Star Tour Tee', 'T-shirt', 'Black T-shirt with the Lone Star Tour back print listing all seven Texas rodeo regions'],
        ['hold-on-8-seconds-tee-light', 'Hold On 8 Seconds Tee', 'T-shirt', 'Ivory Hold On 8 Seconds T-shirt'],
        ['its-rodeo-weekend-tee-dark', "It's Rodeo Weekend Tee", 'T-shirt', "Black It's Rodeo Weekend T-shirt with a horseshoe graphic"],
        ['longhorn-skull-tee-light', 'Longhorn Skull Tee', 'T-shirt', 'Ivory T-shirt with a longhorn skull and Rodeo Texas banner'],
        ['lone-star-tour-hoodie-light', 'Lone Star Tour Hoodie', 'Hoodie', 'Bone hoodie with the Lone Star Tour back print'],
        ['rodeo-texas-badge-hoodie', 'Rodeo Texas Badge Hoodie', 'Hoodie', 'Black hoodie with the Rodeo Texas star badge'],
        ['rodeo-texas-star-trucker-hat', 'Star Trucker Hat', 'Hat', 'Black trucker hat with the Rodeo Texas star badge'],
        ['rodeo-texas-corduroy-dad-hat', 'Corduroy Dad Hat', 'Hat', 'Camel corduroy cap with the Rodeo Texas star badge'],
        ['rodeo-season-yall-tee-light', "Rodeo Season Y'all Tee", 'T-shirt', "Ivory Rodeo Season Y'all T-shirt"],
        ['rodeo-texas-wordmark-tee-dark', 'Rodeo Texas Wordmark Tee', 'T-shirt', 'Black T-shirt with the Rodeo Texas wordmark'],
        ['longhorn-skull-hoodie', 'Longhorn Skull Hoodie', 'Hoodie', 'Black hoodie with a longhorn skull graphic'],
        ['rodeo-texas-badge-mug', 'Rodeo Texas Badge Mug', 'Mug', 'White ceramic mug with the Rodeo Texas badge'],
        ['longhorn-enamel-camp-mug', 'Longhorn Camp Mug', 'Mug', 'White enamel camp mug with a longhorn skull'],
        ['rodeo-texas-badge-tumbler', 'Badge Tumbler', 'Tumbler', 'Black stainless steel tumbler with the Rodeo Texas badge'],
        ['lone-star-tour-tote-bag', 'Lone Star Tour Tote', 'Tote bag', 'Natural cotton tote bag with the Lone Star Tour print'],
        ['lone-star-tour-poster', 'Lone Star Tour Poster', 'Poster', 'Lone Star Tour poster listing the seven Texas rodeo regions'],
    ];
}

/** Full shop URL for a path ('' = shop home, 'products/<slug>', 'collections/<slug>'). */
function shop_url(string $path = ''): string
{
    return SHOP_URL . '/' . ltrim($path, '/');
}

/** Attributes that make a shop link open in a new tab. */
function shop_link_attrs(): string
{
    return ' target="_blank" rel="noopener"';
}

/** Product cards for the first $limit featured products. */
function shop_cards(int $limit = 16): string
{
    $out = '';
    foreach (array_slice(shop_products(), 0, $limit) as [$slug, $name, $label, $alt]) {
        $out .= '<li><a class="shop-card" href="' . e(shop_url('products/' . $slug)) . '"' . shop_link_attrs() . '>'
            . '<img src="/assets/img/shop/' . e($slug) . '.webp" alt="' . e($alt) . '" width="640" height="640" loading="lazy" decoding="async">'
            . '<span class="shop-card__label">' . e($label) . '</span>'
            . '<span class="shop-card__name">' . e($name) . '<span class="visually-hidden"> (opens in a new tab)</span></span>'
            . '</a></li>';
    }
    return $out;
}

/** Merch box shown at the end of every blog article. */
function shop_article_cta(): string
{
    return '<aside class="shop-cta" aria-label="Rodeo Texas shop">'
        . '<div class="shop-cta__text"><p class="shop-feature__kicker">Official merch</p>'
        . '<h2>Gear up for rodeo season</h2>'
        . '<p>Tees, hoodies, hats and mugs from the Rodeo Texas shop.</p>'
        . '<p><a class="btn btn--primary" href="' . e(shop_url()) . '"' . shop_link_attrs() . '>Shop Rodeo Texas<span class="visually-hidden"> (opens in a new tab)</span></a></p></div>'
        . '<ul class="shop-grid shop-grid--mini">' . shop_cards(4) . '</ul>'
        . '</aside>';
}

/** Small sidebar card for article pages. */
function shop_side_card(): string
{
    return '<div class="side-card side-card--shop"><h2>Rodeo Texas shop</h2>'
        . '<a href="' . e(shop_url('products/lone-star-tour-tee-dark')) . '"' . shop_link_attrs() . '>'
        . '<img src="/assets/img/shop/lone-star-tour-tee-dark.webp" alt="Lone Star Tour T-shirt" width="640" height="640" loading="lazy" decoding="async"></a>'
        . '<p>Wear the Lone Star rodeo schedule: tees, hoodies, hats and more.</p>'
        . '<p><a class="btn btn--primary" href="' . e(shop_url()) . '"' . shop_link_attrs() . '>Visit the shop<span class="visually-hidden"> (opens in a new tab)</span></a></p></div>';
}
