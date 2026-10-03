<?php
/**
 * Plugin Name: Pure Goat Farms – Amazon affiliate boxes
 * Description: Adds Amazon product boxes (tag josephrayditt-20) to blog posts at render time, plus the Amazon Associates disclosure in posts, the footer and the privacy policy. Post content in the database is never changed. Delete this file to remove everything.
 * Version: 1.0.0
 *
 * ▸ Products: pgf_aff_products(). Swap a product by changing its ASIN (the
 *   10-character ID after /dp/ in an Amazon URL); 'asin' => null links to a
 *   tagged Amazon search for 'q' instead.
 * ▸ Placements: pgf_aff_placements(). Post slug => [heading text, box title,
 *   [product keys]]. The box goes at the end of the section that starts with
 *   that heading. Posts with no placements get one "essentials" box at the end.
 * ▸ Turn everything off by setting PGF_AFF_ENABLED to false.
 */

defined('ABSPATH') || exit;

const PGF_AFF_ENABLED = true;
const PGF_AFF_TAG = 'josephrayditt-20';

function pgf_aff_products(): array
{
    return [
        // Milking
        'milk-pail' => ['name' => 'Dairy Shoppe seamless stainless pail (13 qt)', 'asin' => 'B018015MC6', 'q' => 'stainless steel goat milking pail', 'note' => 'Hooded pail keeps hay and hair out'],
        'milk-strainer' => ['name' => 'Stainless mason-jar milk strainer + 300 filters', 'asin' => 'B00WRFB1H2', 'q' => 'stainless milk strainer with filters', 'note' => 'Strain right after milking'],
        'milk-jars' => ['name' => 'Ball half-gallon wide-mouth jars', 'asin' => 'B07FHK53Q5', 'q' => 'Ball half gallon wide mouth mason jars', 'note' => 'Chill milk fast and store it clean'],
        'milk-stand' => ['name' => 'VEVOR goat milking stand', 'asin' => 'B0D3192122', 'q' => 'goat milking stand', 'note' => 'Same spot, same height, every milking'],
        'hand-milker' => ['name' => 'Udderly EZ hand milker', 'asin' => 'B0BZWJSYFH', 'q' => 'hand goat milker', 'note' => 'Easier on the hands for twice-daily milking'],
        'teat-dip' => ['name' => 'Fight Bac teat spray', 'asin' => 'B004Z61XS8', 'q' => 'teat dip for goats', 'note' => 'Post-milking dip helps prevent mastitis'],
        'udder-balm' => ['name' => 'Bag Balm udder ointment', 'asin' => 'B00FNKXZLI', 'q' => 'Bag Balm', 'note' => 'For chapped or dry teats'],
        'cmt-kit' => ['name' => 'California Mastitis Test kit', 'asin' => 'B09WY3DMYK', 'q' => 'California mastitis test kit', 'note' => 'Catch subclinical mastitis early'],
        'milk-scale' => ['name' => 'AWS digital hanging scale (110 lb)', 'asin' => 'B0012TDR9E', 'q' => 'digital hanging scale', 'note' => 'Weigh each milking for your records'],
        // Feed
        'goat-mineral' => ['name' => 'Manna Pro loose goat mineral', 'asin' => null, 'q' => 'Manna Pro goat mineral', 'note' => 'Free-choice minerals support production'],
        'goat-balancer' => ['name' => 'Manna Pro Goat Balancer', 'asin' => 'B0024E81T2', 'q' => 'Manna Pro Goat Balancer', 'note' => 'Top-dress supplement for does in milk'],
        'alfalfa-pellets' => ['name' => 'Standlee alfalfa pellets', 'asin' => 'B00R1OWJ6Q', 'q' => 'Standlee alfalfa pellets', 'note' => 'Protein and calcium for milkers'],
        'kid-bottle' => ['name' => 'Premier 1 kid bottle with Pritchard teat', 'asin' => 'B08NZ1FVQX', 'q' => 'Pritchard teat goat kid', 'note' => 'Fits standard soda bottles'],
        // Cheese
        'thermometer' => ['name' => 'CDN digital dairy thermometer', 'asin' => 'B00279OPDU', 'q' => 'dairy cheese making thermometer', 'note' => 'Culture and rennet need exact temperatures'],
        'stockpot' => ['name' => 'Cook N Home 12-qt stainless stockpot', 'asin' => 'B012OIVRP2', 'q' => 'stainless steel stock pot heavy bottom 12 quart', 'note' => 'Heats milk evenly without scorching'],
        'chevre-culture' => ['name' => 'New England Cheesemaking chevre culture', 'asin' => 'B0064OLRH6', 'q' => 'chevre culture packets', 'note' => 'Culture and rennet in one packet'],
        'rennet' => ['name' => 'Liquid animal rennet', 'asin' => 'B008EKF6D4', 'q' => 'liquid rennet cheese making', 'note' => 'For firmer and aged cheeses'],
        'butter-muslin' => ['name' => 'Grade 90 cheesecloth (butter muslin)', 'asin' => 'B08CRXK469', 'q' => 'butter muslin cheesecloth', 'note' => 'Fine weave for draining soft curds'],
        'cheese-press' => ['name' => 'Mad Millie hard cheese press', 'asin' => 'B071KTRBNB', 'q' => 'cheese press home', 'note' => 'Needed for firm and aged cheeses'],
        'cheese-molds' => ['name' => 'French chevre draining molds (set of 4)', 'asin' => 'B0C6PPMJQR', 'q' => 'cheese molds set', 'note' => 'Shapes and drains soft cheeses'],
        'cheese-kit' => ['name' => 'Standing Stone Farms cheese making kit', 'asin' => 'B01JT7KUUO', 'q' => 'goat cheese making kit', 'note' => 'Everything for your first batch of chevre'],
        // Books
        'book-cheese' => ['name' => 'Home Cheese Making (Ricki Carroll)', 'asin' => '161212867X', 'q' => 'Home Cheese Making Ricki Carroll', 'note' => 'The standard home cheesemaking guide'],
        'book-dairy-goats' => ['name' => 'Storey’s Guide to Raising Dairy Goats', 'asin' => '1612129323', 'q' => 'Storey\'s Guide to Raising Dairy Goats', 'note' => 'Breeds, feeding, kidding and milking'],
    ];
}

function pgf_aff_placements(): array
{
    return [
        'how-many-goats-do-you-need-to-make-cheese' => [
            ['How Much Milk Does It Take to Make Goat Cheese?', 'Cheesemaking basics', ['stockpot', 'thermometer']],
            ['Fresh Cheese vs Aged Cheese', 'Cheesemaking supplies', ['chevre-culture', 'butter-muslin', 'cheese-molds', 'rennet', 'cheese-press']],
            ['The Milk Collection Window Matters', 'Collecting and storing milk', ['milk-pail', 'milk-strainer', 'milk-jars']],
            ['Do Not Forget Milk Reserved for Kids', 'For bottle kids', ['kid-bottle']],
            ['Feed and Care Affect Milk Supply', 'Feeding does in milk', ['goat-mineral', 'goat-balancer', 'alfalfa-pellets']],
            ['Homemade Cheese vs Selling Goat Cheese', 'Further reading', ['book-cheese']],
            ['Final Thoughts', 'Ready for your first batch?', ['cheese-kit']],
        ],
        'how-much-milk-can-a-goat-really-give-at-once' => [
            ['Average Amount of Milk a Goat Gives Per Milking', 'Measure each milking', ['milk-scale', 'milk-pail']],
            ['Nutrition and Feeding Quality', 'Feeding does in milk', ['goat-mineral', 'goat-balancer', 'alfalfa-pellets']],
            ['Health and Stress Management', 'Udder health', ['teat-dip', 'udder-balm', 'cmt-kit']],
            ['Maintain a Consistent Milking Schedule', 'Milking setup', ['milk-stand', 'hand-milker']],
            ['Track Production Records', 'Record keeping', ['milk-scale', 'book-dairy-goats']],
            ['How Much Milk Does a Goat Provide for a Family?', 'Using your milk', ['milk-strainer', 'milk-jars', 'cheese-kit']],
        ],
    ];
}

/** Box added to the end of any post that has no placements of its own (new posts included). */
function pgf_aff_default_keys(): array
{
    return ['milk-pail', 'milk-strainer', 'goat-mineral', 'book-dairy-goats'];
}

function pgf_aff_url(string $key): string
{
    $p = pgf_aff_products()[$key] ?? null;
    if (!$p) {
        return '';
    }
    if (!empty($p['asin'])) {
        return 'https://www.amazon.com/dp/' . rawurlencode($p['asin']) . '/?tag=' . rawurlencode(PGF_AFF_TAG);
    }
    return 'https://www.amazon.com/s?k=' . rawurlencode($p['q']) . '&tag=' . rawurlencode(PGF_AFF_TAG);
}

function pgf_aff_box(string $title, array $keys): string
{
    $items = '';
    foreach ($keys as $k) {
        $p = pgf_aff_products()[$k] ?? null;
        if (!$p) {
            continue;
        }
        $items .= '<li><a href="' . esc_url(pgf_aff_url($k)) . '" rel="sponsored nofollow noopener" target="_blank">' . esc_html($p['name']) . '</a>'
            . (!empty($p['note']) ? '<span class="pgf-aff-note">' . esc_html($p['note']) . '</span>' : '') . '</li>';
    }
    if ($items === '') {
        return '';
    }
    return '<aside class="pgf-aff-box" aria-label="' . esc_attr($title) . '"><p class="pgf-aff-label">' . esc_html($title) . '</p><ul>' . $items . '</ul>'
        . '<p class="pgf-aff-cta">Opens on Amazon. We may earn a commission.</p></aside>';
}

function pgf_aff_norm(string $s): string
{
    $s = html_entity_decode(wp_strip_all_tags($s), ENT_QUOTES | ENT_HTML5, 'UTF-8');
    $s = str_replace(["\u{2019}", "\u{2018}", "\u{201C}", "\u{201D}", "\u{00A0}"], ["'", "'", '"', '"', ' '], $s);
    return strtolower(trim(preg_replace('/\s+/u', ' ', $s)));
}

/** Insert boxes at the end of matching sections. Pure function so it can be tested outside WordPress. */
function pgf_aff_inject(string $slug, string $html): string
{
    if (strpos($html, 'pgf-aff-box') !== false) {
        return $html; // already processed
    }
    $place = pgf_aff_placements()[$slug] ?? null;
    $inserts = [];
    if ($place && preg_match_all('#<h([2-4])\b[^>]*>(.*?)</h\1>#is', $html, $m, PREG_OFFSET_CAPTURE)) {
        $heads = [];
        foreach ($m[0] as $i => $full) {
            $heads[] = ['start' => $full[1], 'text' => pgf_aff_norm($m[2][$i][0])];
        }
        $used = [];
        foreach ($place as [$match, $title, $keys]) {
            $needle = pgf_aff_norm($match);
            foreach ($heads as $i => $h) {
                if (isset($used[$i]) || strpos($h['text'], $needle) === false) {
                    continue;
                }
                $used[$i] = true;
                // End of section = next top-level heading (skip headings nested inside widgets like calculators).
                $pos = strlen($html);
                for ($j = $i + 1; $j < count($heads); $j++) {
                    $before = substr($html, 0, $heads[$j]['start']);
                    if (substr_count($before, '<div') - substr_count($before, '</div>') === 0) {
                        $pos = $heads[$j]['start'];
                        break;
                    }
                }
                $inserts[$pos] = ($inserts[$pos] ?? '') . pgf_aff_box($title, $keys);
                break;
            }
        }
    }
    if (!$inserts) {
        $inserts[strlen($html)] = pgf_aff_box('Dairy goat essentials', pgf_aff_default_keys());
    }
    krsort($inserts);
    foreach ($inserts as $pos => $box) {
        $html = substr($html, 0, $pos) . $box . substr($html, $pos);
    }
    return '<p class="pgf-aff-disclosure">This post contains affiliate links. As an Amazon Associate, Pure Goat Farms earns from qualifying purchases, at no extra cost to you.</p>' . $html;
}

if (!function_exists('add_filter')) {
    return; // loaded outside WordPress (tests)
}

add_filter('the_content', function ($content) {
    if (!PGF_AFF_ENABLED || is_admin() || is_feed() || !is_string($content) || $content === '') {
        return $content;
    }
    try {
        if (is_singular('post') && get_the_ID() === get_queried_object_id()) {
            return pgf_aff_inject((string) get_post_field('post_name', get_the_ID()), $content);
        }
        if (is_page('privacy-policy') && strpos($content, 'Amazon Services LLC Associates Program') === false) {
            return $content . '<h2>Amazon Associates</h2><p>Pure Goat Farms is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. When you click a product link on our site, Amazon may set cookies in your browser to record that the visit came from us. We may earn a commission on qualifying purchases at no extra cost to you. We do not receive any personal information about you or what you buy.</p>';
        }
    } catch (\Throwable $e) {
        // Never break a page over an affiliate box.
    }
    return $content;
}, 20);

add_action('wp_head', function () {
    if (!PGF_AFF_ENABLED) {
        return;
    }
    echo '<style id="pgf-aff-css">'
        . '.pgf-aff-box{margin:1.75em 0;padding:1em 1.2em;border:1px solid rgba(90,110,60,.3);border-left:4px solid #5a6e3c;border-radius:6px;background:rgba(90,110,60,.06)}'
        . '.pgf-aff-label{margin:0 0 .5em!important;font-size:.78em;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#5a6e3c}'
        . '.pgf-aff-box ul{margin:0!important;padding:0!important;list-style:none!important;display:grid;gap:.6em}'
        . '.pgf-aff-box li{margin:0!important;padding:0!important}'
        . '.pgf-aff-box li::before{content:none!important}'
        . '.pgf-aff-box a{font-weight:700}'
        . '.pgf-aff-note{display:block;font-size:.88em;opacity:.8}'
        . '.pgf-aff-cta{margin:.7em 0 0!important;font-size:.8em;opacity:.7}'
        . '.pgf-aff-disclosure{font-size:.85em;font-style:italic;opacity:.8}'
        . '.pgf-aff-footer{text-align:center;font-size:12px;opacity:.75;padding:10px 16px;margin:0}'
        . '</style>';
});

add_action('wp_footer', function () {
    if (PGF_AFF_ENABLED) {
        echo '<p class="pgf-aff-footer">As an Amazon Associate, Pure Goat Farms earns from qualifying purchases.</p>';
    }
}, 5);
