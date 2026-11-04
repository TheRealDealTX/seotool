<?php
// Amazon Associates product links.
//
// Every product lives once in AMAZON_PRODUCTS (key => [ASIN, display name, why we like it]).
// Templates link to products by key, so a dead or replaced listing is fixed in one place.
//   amz('x-chock')                 inline text link using the product name
//   amz('x-chock', 'wheel chocks') inline text link with custom anchor text
//   gear_box($keys, $heading, $intro)   boxed "gear we recommend" list with the disclosure
// Links go to the product page (/dp/ASIN) with the store tag, open in a new tab and carry
// rel="sponsored nofollow" as Google asks for paid links.

const AMAZON_TAG = 'cowboytinyhomes-20';
const AMAZON_DISCLOSURE = 'As an Amazon Associate, Cowboy Tiny Homes earns from qualifying purchases.';

require __DIR__ . '/amazon-products.php';

function amz_url(string $key): string
{
    $p = AMAZON_PRODUCTS[$key] ?? null;
    if (!$p) throw new RuntimeException("Unknown Amazon product key: $key");
    return 'https://www.amazon.com/dp/' . $p[0] . '?tag=' . AMAZON_TAG;
}

function amz(string $key, ?string $text = null): string
{
    $GLOBALS['amz_used'] = true;
    return '<a href="' . e(amz_url($key)) . '" target="_blank" rel="sponsored nofollow noopener">'
         . e($text ?? AMAZON_PRODUCTS[$key][1]) . '</a>';
}

function gear_box(array $keys, string $heading, string $intro = ''): void
{
    $GLOBALS['amz_used'] = true;
    echo '<aside class="gear-box" aria-label="' . e($heading) . '"><h3>' . e($heading) . '</h3>';
    if ($intro) echo '<p>' . $intro . '</p>';
    echo '<ul class="gear-list">';
    foreach ($keys as $k) {
        [, $name, $why] = AMAZON_PRODUCTS[$k];
        echo '<li class="gear-item"><div><strong>' . e($name) . '</strong><span>' . $why . '</span></div>'
           . '<a class="gear-btn" href="' . e(amz_url($k)) . '" target="_blank" rel="sponsored nofollow noopener">View on Amazon</a></li>';
    }
    echo '</ul><p class="gear-note">' . AMAZON_DISCLOSURE . ' We only list gear we would put in our own builds.</p></aside>';
}

// Short disclosure line for pages that use inline amz() links without a gear box.
function amz_disclosure(): void
{
    echo '<p class="gear-note">' . AMAZON_DISCLOSURE . '</p>';
}
