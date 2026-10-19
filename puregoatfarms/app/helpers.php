<?php
// Shared helpers: escaping, icons, cards, schema and affiliate boxes.
defined('PGF') || exit;

function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

function abs_url(string $path): string
{
    return str_starts_with($path, 'http') ? $path : SITE_URL . $path;
}

function fmt_date(string $ymd): string
{
    return date('F j, Y', strtotime($ymd));
}

function iso_date(string $ymd): string
{
    return $ymd . 'T08:00:00+00:00';
}

function asset(string $path): string
{
    // Cache-bust CSS/JS by modification time.
    $file = DOCROOT . $path;
    return $path . (is_file($file) ? '?v=' . filemtime($file) : '');
}

// Small inline icon set (stroke icons, inherit currentColor).
function icon(string $name, string $class = 'ico'): string
{
    $p = [
        'pail'     => '<path d="M5 8h14l-1.6 11.2a2 2 0 0 1-2 1.8H8.6a2 2 0 0 1-2-1.8z"/><path d="M5 8c0-2.8 3.1-5 7-5s7 2.2 7 5"/><path d="M8 12c1.5 1 6.5 1 8 0"/>',
        'barn'     => '<path d="M3 21V10l9-6 9 6v11"/><path d="M9 21v-6h6v6"/><path d="M9 11h6"/><path d="M3 21h18"/>',
        'goat'     => '<path d="M7 4c-1 2-1 4 0 5"/><path d="M17 4c1 2 1 4 0 5"/><path d="M7 9c0 4 2 7 5 9 3-2 5-5 5-9a5 5 0 0 0-10 0z"/><path d="M12 18v3"/><circle cx="10" cy="11" r=".6"/><circle cx="14" cy="11" r=".6"/>',
        'heart'    => '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/><path d="M9 11h2l1-2 1.5 4 1-2H17"/>',
        'chart'    => '<path d="M3 3v18h18"/><path d="M6 16c3-8 6-10 8-6s3 2 5-4"/>',
        'cheese'   => '<path d="M3 17l9-11 9 11z"/><path d="M3 17v3h18v-3"/><circle cx="10" cy="14" r="1.2"/><circle cx="15" cy="15" r=".9"/>',
        'calendar' => '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M8 14h2v2H8z"/>',
        'hay'      => '<rect x="3" y="7" width="18" height="12" rx="2"/><path d="M3 11h18M3 15h18M8 7v12M16 7v12"/>',
        'scale'    => '<path d="M12 3v3"/><circle cx="12" cy="13" r="7"/><path d="M12 13l3-3"/>',
        'arrow'    => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'mail'     => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        'clock'    => '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'check'    => '<path d="M5 12l5 5 9-10"/>',
        'leaf'     => '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l7-7"/>',
        'book'     => '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>',
        'search'   => '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
        'menu'     => '<path d="M4 7h16M4 12h16M4 17h16"/>',
        'close'    => '<path d="M6 6l12 12M18 6L6 18"/>',
        'chev'     => '<path d="M6 9l6 6 6-6"/>',
        'up'       => '<path d="M12 19V5M6 11l6-6 6 6"/>',
        'pin'      => '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        'spark'    => '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    ][$name] ?? '';
    return '<svg class="' . e($class) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}

// Amazon affiliate products already used across the original posts.
const AFF = [
    'scale'       => ['B0012TDR9E', 'AWS digital hanging scale (110 lb)', 'Weigh each milking for your records'],
    'pail'        => ['B018015MC6', 'Dairy Shoppe seamless stainless pail (13 qt)', 'Hooded pail keeps hay and hair out'],
    'stand'       => ['B0D3192122', 'VEVOR goat milking stand', 'Same spot, same height, every milking'],
    'hand_milker' => ['B0BZWJSYFH', 'Udderly EZ hand milker', 'Easier on the hands for twice-daily milking'],
    'teat_spray'  => ['B004Z61XS8', 'Fight Bac teat spray', 'Post-milking dip helps prevent mastitis'],
    'bag_balm'    => ['B00FNKXZLI', 'Bag Balm udder ointment', 'For chapped or dry teats'],
    'cmt'         => ['B09WY3DMYK', 'California Mastitis Test kit', 'Catch subclinical mastitis early'],
    'strainer'    => ['B00WRFB1H2', 'Stainless mason-jar milk strainer + 300 filters', 'Strain right after milking'],
    'jars'        => ['B07FHK53Q5', 'Ball half-gallon wide-mouth jars', 'Chill milk fast and store it clean'],
    'alfalfa'     => ['B00R1OWJ6Q', 'Standlee alfalfa pellets', 'Protein and calcium for milkers'],
    'balancer'    => ['B0024E81T2', 'Manna Pro Goat Balancer', 'Top-dress supplement for does in milk'],
    'book_dairy'  => ['1612129323', 'Storey’s Guide to Raising Dairy Goats', 'Breeds, feeding, kidding and milking'],
    'book_cheese' => ['161212867X', 'Home Cheese Making (Ricki Carroll)', 'The standard home cheesemaking guide'],
    'cheese_kit'  => ['B01JT7KUUO', 'Standing Stone Farms cheese making kit', 'Everything for your first batch of chevre'],
    'mineral'     => ['search:Manna Pro goat mineral', 'Manna Pro loose goat mineral', 'Free-choice minerals support production'],
];

function aff_url(string $id): string
{
    if (str_starts_with($id, 'search:')) {
        return 'https://www.amazon.com/s?k=' . rawurlencode(substr($id, 7)) . '&tag=' . AMAZON_TAG;
    }
    return "https://www.amazon.com/dp/$id/?tag=" . AMAZON_TAG;
}

function aff_box(string $label, array $keys): string
{
    $li = '';
    foreach ($keys as $k) {
        [$id, $name, $note] = AFF[$k];
        $li .= '<li><a href="' . e(aff_url($id)) . '" rel="sponsored nofollow noopener" target="_blank">' . e($name) . '</a><span class="pgf-aff-note">' . e($note) . '</span></li>';
    }
    return '<aside class="pgf-aff-box" aria-label="' . e($label) . '"><p class="pgf-aff-label">' . e($label) . '</p><ul>' . $li . '</ul><p class="pgf-aff-cta">Opens on Amazon. We may earn a commission.</p></aside>';
}

function cat_link(string $slug): string
{
    return '<a class="tag" href="/category/' . e($slug) . '/">' . e(CATEGORIES[$slug]['name']) . '</a>';
}

function read_minutes(string $html): int
{
    $words = str_word_count(strip_tags(preg_replace('#<(script|style)\b.*?</\1>#s', '', $html)));
    return max(2, (int) round($words / 230));
}

function post_body(string $slug): string
{
    ob_start();
    include APP . "/posts/$slug.php";
    return ob_get_clean();
}

function post_card(string $slug, array $p, string $variant = ''): string
{
    [$src, $w, $h] = $p['image'];
    $cat = $p['cats'][0];
    return '<article class="post-card ' . e($variant) . ' reveal">'
        . '<a class="post-card__img" href="/' . e($slug) . '/" tabindex="-1" aria-hidden="true"><img src="' . e($src) . '" alt="' . e($p['alt']) . '" width="' . $w . '" height="' . $h . '" loading="lazy" decoding="async"></a>'
        . '<div class="post-card__body">'
        . '<div class="post-card__meta">' . cat_link($cat) . '<time datetime="' . e($p['date']) . '">' . e(fmt_date($p['date'])) . '</time></div>'
        . '<h3 class="post-card__title"><a href="/' . e($slug) . '/">' . e($p['title']) . '</a></h3>'
        . '<p class="post-card__excerpt">' . e($p['excerpt']) . '</p>'
        . '<a class="link-arrow" href="/' . e($slug) . '/">Read the guide ' . icon('arrow') . '</a>'
        . '</div></article>';
}

function tool_card(string $slug, array $t): string
{
    return '<a class="tool-card reveal tilt" href="/tools/' . e($slug) . '/">'
        . '<span class="tool-card__icon">' . icon($t['icon']) . '</span>'
        . '<span class="tool-card__kicker">' . e($t['short']) . '</span>'
        . '<span class="tool-card__title">' . e($t['name']) . '</span>'
        . '<span class="tool-card__desc">' . e($t['desc']) . '</span>'
        . '<span class="link-arrow">Open tool ' . icon('arrow') . '</span>'
        . '</a>';
}

// Adds ids to <h2> headings and returns [html, toc].
function add_heading_ids(string $html): array
{
    $toc = [];
    $seen = [];
    $html = preg_replace_callback('#<h2>(.*?)</h2>#s', function ($m) use (&$toc, &$seen) {
        $text = trim(html_entity_decode(strip_tags($m[1]), ENT_QUOTES, 'UTF-8'));
        $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($text)), '-') ?: 'section';
        $base = $id;
        $n = 2;
        while (isset($seen[$id])) {
            $id = $base . '-' . $n++;
        }
        $seen[$id] = true;
        $toc[] = [$id, $text];
        return '<h2 id="' . $id . '">' . $m[1] . '</h2>';
    }, $html);
    return [$html, $toc];
}

function faq_html(array $faq, string $heading = 'Frequently Asked Questions'): string
{
    $out = $heading === ''
        ? '<section class="faq" aria-label="Frequently asked questions">'
        : '<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">' . e($heading) . '</h2>';
    foreach ($faq as $i => [$q, $a]) {
        $out .= '<details class="faq__item"' . ($i === 0 ? ' open' : '') . '><summary>' . e($q) . '<span class="faq__icon" aria-hidden="true"></span></summary><div class="faq__a"><p>' . e($a) . '</p></div></details>';
    }
    return $out . '</section>';
}

// ---- JSON-LD -------------------------------------------------------------

function schema_org(): array
{
    return [
        '@type' => 'Organization',
        '@id' => SITE_URL . '/#organization',
        'name' => SITE_NAME,
        'url' => SITE_URL . '/',
        'email' => SITE_EMAIL,
        'logo' => ['@type' => 'ImageObject', 'url' => abs_url(IMG['logo']), 'width' => 600, 'height' => 117],
        'image' => abs_url(IMG['og']),
        'description' => 'Pure Goat Farms is a family-run dairy-goat farm publishing practical, field-tested guides on goat milk production, breeds, health and farm life.',
    ];
}

function schema_website(): array
{
    return [
        '@type' => 'WebSite',
        '@id' => SITE_URL . '/#website',
        'url' => SITE_URL . '/',
        'name' => SITE_NAME,
        'alternateName' => ['Pure Goat Farm', 'PureGoatFarms'],
        'description' => SITE_TAGLINE,
        'publisher' => ['@id' => SITE_URL . '/#organization'],
        'inLanguage' => 'en-US',
    ];
}

function schema_breadcrumbs(array $crumbs): array
{
    $items = [];
    foreach ($crumbs as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => abs_url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function schema_faq(array $faq): array
{
    return [
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($qa) => [
            '@type' => 'Question',
            'name' => $qa[0],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $qa[1]],
        ], $faq),
    ];
}

function schema_tool(string $slug, array $t): array
{
    return [
        '@type' => 'WebApplication',
        'name' => $t['name'],
        'url' => SITE_URL . "/tools/$slug/",
        'applicationCategory' => 'UtilitiesApplication',
        'operatingSystem' => 'Any (web browser)',
        'description' => $t['desc'],
        'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
        'publisher' => ['@id' => SITE_URL . '/#organization'],
    ];
}
