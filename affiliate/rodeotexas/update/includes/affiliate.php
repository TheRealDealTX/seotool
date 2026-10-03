<?php
/**
 * AMAZON AFFILIATE LINKS (Amazon Associates tag: josephrayditt-20).
 *
 * ▸ Products live in aff_products(). To swap a product, change its ASIN (the
 *   10-character ID after /dp/ in an Amazon URL). Leave 'asin' => null to link
 *   to a tagged Amazon search for 'q' instead.
 * ▸ Article placements live in aff_placements(): article slug => list of
 *   [heading text to match, box title, [product keys]]. Each box is inserted at
 *   the end of the section that starts with the matching <h2>/<h3>/<h4>, so the
 *   article text stored in the database is never changed.
 * ▸ To turn everything off at once, set AFF_ENABLED to false.
 */
defined('RT_APP') || exit;

const AFF_ENABLED = true;
const AFF_TAG = 'josephrayditt-20';

function aff_products(): array
{
    static $p = null;
    if ($p !== null) {
        return $p;
    }
    return $p = [
        // Boots
        'ariat-heritage-roper' => ['name' => 'Ariat Heritage Roper (men’s)', 'asin' => 'B001AS708G', 'q' => 'Ariat Heritage Roper boot', 'note' => 'Round toe, riding heel, easy break-in'],
        'justin-bent-rail' => ['name' => 'Justin Bent Rail (men’s)', 'asin' => 'B00D7JZ9X4', 'q' => 'Justin Bent Rail boot', 'note' => 'Thick leather, sturdy shaft'],
        'ariat-fatbaby' => ['name' => 'Ariat Fatbaby (women’s)', 'asin' => 'B08Y6YGRLK', 'q' => 'Ariat Fatbaby women', 'note' => 'Light and flexible'],
        'durango-rebel' => ['name' => 'Durango Rebel (men’s)', 'asin' => 'B0D9KFDFVN', 'q' => 'Durango Rebel western boot', 'note' => 'Leather boot at a budget price'],
        'tony-lama-americana' => ['name' => 'Tony Lama Americana Stockman', 'asin' => 'B00EL7CVIC', 'q' => 'Tony Lama Americana 7956', 'note' => 'Handmade, premium leather'],
        'ariat-round-up-women' => ['name' => 'Ariat Round Up (women’s)', 'asin' => 'B076RQ9JRB', 'q' => 'Ariat Round Up women western boot', 'note' => 'Classic, comfortable all-day boot'],
        'ariat-kids-heritage' => ['name' => 'Ariat Kids’ Heritage boot', 'asin' => 'B004IJL6WA', 'q' => 'Ariat kids heritage western boot', 'note' => 'Durable boot for young fans'],
        // Boot care
        'bick-4' => ['name' => 'Bick 4 Leather Conditioner', 'asin' => 'B001CS8G3C', 'q' => 'Bick 4 leather conditioner', 'note' => 'Conditions without darkening leather'],
        'horsehair-brush' => ['name' => 'Kiwi Horsehair Shine Brush', 'asin' => 'B0010TR6NE', 'q' => 'horsehair boot brush', 'note' => 'Knocks arena dust off before conditioning'],
        'boot-jack' => ['name' => 'Boot jack', 'asin' => 'B0BN5YTM4G', 'q' => 'boot jack cowboy boots', 'note' => 'Pull off snug new boots without a fight'],
        // Clothing
        'wrangler-13mwz' => ['name' => 'Wrangler Cowboy Cut 13MWZ jeans', 'asin' => 'B07CJYFWFK', 'q' => 'Wrangler 13MWZ Cowboy Cut', 'note' => 'The classic rodeo jean'],
        'wrangler-snap-shirt' => ['name' => 'Wrangler western snap shirt', 'asin' => 'B07P4HR23Z', 'q' => 'Wrangler western snap shirt', 'note' => 'Pearl snaps, long sleeves'],
        'wrangler-women-bootcut' => ['name' => 'Wrangler women’s bootcut jeans', 'asin' => 'B0CK4FLXLZ', 'q' => 'Wrangler women western bootcut jean', 'note' => 'Stretch denim that fits over boots'],
        'resistol-straw' => ['name' => 'Resistol 10X Gambler straw hat', 'asin' => 'B01M5K24A0', 'q' => 'Resistol straw cowboy hat', 'note' => 'For summer and daytime rodeos'],
        'stetson-felt' => ['name' => 'Stetson Powder River 4X felt hat', 'asin' => 'B00DYW87UG', 'q' => 'Stetson Powder River felt hat', 'note' => 'For fall and winter rodeos'],
        'nocona-belt' => ['name' => 'Nocona leather western belt', 'asin' => 'B00FTGOX62', 'q' => 'Nocona western belt', 'note' => 'Tooled leather with conchos'],
        'sherpa-jacket' => ['name' => 'Wrangler sherpa-lined denim jacket', 'asin' => 'B07MXP9MZ6', 'q' => 'Wrangler sherpa lined denim jacket', 'note' => 'Warm layer for cold arenas'],
        'wild-rag' => ['name' => 'Wyoming Traders silk wild rag', 'asin' => 'B094RJ9NHF', 'q' => 'Wyoming Traders silk wild rag', 'note' => 'Real silk; warm or cool as needed'],
        'hat-case' => ['name' => 'CASEMATIX cowboy hat case', 'asin' => 'B0BTQJK4WD', 'q' => 'cowboy hat travel case', 'note' => 'Keeps the brim in shape on the drive'],
        // Spectator gear
        'stadium-seat' => ['name' => 'Coleman stadium seat with backrest', 'asin' => 'B00339C3QE', 'q' => 'stadium seat cushion with back support bleachers', 'note' => 'Bleachers are hard; rodeos run 2–5 hours'],
        'clear-bag' => ['name' => 'Bagenius clear stadium bag (12×12×6)', 'asin' => 'B07RFBFG4H', 'q' => 'clear stadium bag 12x12x6', 'note' => 'Many large arenas allow clear bags only'],
        'kids-earmuffs' => ['name' => 'Dr.meter kids’ ear muffs', 'asin' => 'B01LWYWH43', 'q' => 'kids hearing protection ear muffs', 'note' => 'Announcers and fireworks are loud for little ears'],
        'binoculars' => ['name' => 'Nikon Aculon A30 10×25 binoculars', 'asin' => 'B00BD53BWU', 'q' => 'compact binoculars for sports events', 'note' => 'See the chutes from the upper rows'],
        'power-bank' => ['name' => 'Anker 10,000mAh power bank', 'asin' => 'B0D5CLSMFB', 'q' => 'Anker portable charger power bank', 'note' => 'Mobile tickets and long nights'],
        'sunscreen' => ['name' => 'Banana Boat Sport Ultra SPF 50', 'asin' => 'B004CDV7EY', 'q' => 'sport sunscreen spf 50', 'note' => 'For daytime and outdoor arenas'],
        'cooling-towel' => ['name' => 'Frogg Toggs Chilly Pad cooling towel', 'asin' => 'B002JAIKWY', 'q' => 'cooling towel', 'note' => 'Texas summer rodeos get hot'],
        'rain-jacket' => ['name' => 'Columbia Watertight II rain jacket', 'asin' => 'B00HN53994', 'q' => 'packable rain jacket', 'note' => 'Folds into a pocket for outdoor arenas'],
        // Rider gear
        'bull-helmet' => ['name' => 'Rodeo Hard bull riding helmet', 'asin' => 'B07CSGM3TH', 'q' => 'bull riding helmet', 'note' => 'Now standard for young riders'],
        'rodeo-vest' => ['name' => 'Hilason pro rodeo bull riding vest', 'asin' => 'B07K6QXMK5', 'q' => 'rodeo protective vest', 'note' => 'Protects ribs and organs'],
        'mouthguard' => ['name' => 'Shock Doctor Gel Max Power mouthguard', 'asin' => 'B01NAXEYJL', 'q' => 'Shock Doctor mouthguard', 'note' => 'Small piece of gear, big difference'],
        'bull-glove' => ['name' => 'Heritage Pro 8.0 bull riding glove', 'asin' => 'B005X5HLLS', 'q' => 'bull riding glove', 'note' => 'Grip on the rope'],
        'bull-rope' => ['name' => 'FCBR 9×9 bull rope', 'asin' => 'B098FDD3RD', 'q' => 'bull rope', 'note' => 'Your lifeline on the bull'],
        'rosin' => ['name' => 'Buck Sticky rodeo rosin', 'asin' => 'B07FQWXD47', 'q' => 'rodeo rosin', 'note' => 'Adds grip to rope and glove'],
        'spurs' => ['name' => 'Rodeo spurs', 'asin' => null, 'q' => 'rodeo spurs', 'note' => 'Helps hold position'],
        'roping-gloves' => ['name' => 'Heritage ProGrip roping gloves', 'asin' => 'B005X5G3YO', 'q' => 'roping gloves', 'note' => 'Feel for the rope, protection from burns'],
        'team-rope' => ['name' => 'Classic Powerline Lite team rope', 'asin' => 'B000652FDY', 'q' => 'team rope', 'note' => 'Headers use shorter ropes, heelers longer'],
        'breakaway-rope' => ['name' => 'Rattler Spitfire breakaway rope', 'asin' => 'B07L8KBYY5', 'q' => 'breakaway rope', 'note' => 'Light for fast handling'],
        'breakaway-honda' => ['name' => 'Nothin But Neck breakaway honda', 'asin' => 'B00I4A96B2', 'q' => 'breakaway honda', 'note' => 'Releases cleanly when the calf runs through'],
        'roping-dummy' => ['name' => 'Classic Rattler steer head roping dummy', 'asin' => 'B0CW6M5JJ1', 'q' => 'roping dummy', 'note' => 'Practice your swing and throw at home'],
        'splint-boots' => ['name' => 'Classic Equine Legacy2 support boots', 'asin' => 'B0792G838L', 'q' => 'horse splint boots', 'note' => 'Protects your horse’s legs'],
        'rope-bag' => ['name' => 'Classic Rope professional rope bag', 'asin' => 'B09KHH6T3Q', 'q' => 'rope bag roping', 'note' => 'Keeps ropes stiff and clean'],
        'chaps' => ['name' => 'Hilason leather rodeo chinks', 'asin' => 'B09X1Y9FDG', 'q' => 'western chinks chaps', 'note' => 'Leg protection for riding events'],
        // Books and film
        'eight-seconds' => ['name' => '8 Seconds (1994) on DVD', 'asin' => 'B00002SSKG', 'q' => '8 Seconds Luke Perry', 'note' => 'The story of bull rider Lane Frost'],
        'rodeo-history-book' => ['name' => 'Rodeo in America (Wooden & Ehringer)', 'asin' => '0700609652', 'q' => 'rodeo history book', 'note' => 'The sport from ranch work to the NFR'],
        'texas-cowboy-book' => ['name' => 'The Trail Drivers of Texas (J. Marvin Hunter)', 'asin' => '0292730764', 'q' => 'Texas cowboy history book', 'note' => 'Cattle drives and the open range'],
    ];
}

function aff_placements(): array
{
    return [
        'best-cowboy-boots-for-rodeo' => [
            ['Best Overall Rodeo Boots', 'Our pick', ['ariat-heritage-roper']],
            ['Best for Bull Riding', 'Our pick', ['justin-bent-rail']],
            ['Best for Barrel Racing', 'Our pick', ['ariat-fatbaby']],
            ['Best Budget Cowboy Boots', 'Our pick', ['durango-rebel']],
            ['Best Premium Cowboy Boots', 'Our pick', ['tony-lama-americana']],
            ['How to Break in Cowboy Boots', 'Helpful for new boots', ['boot-jack']],
            ['Basic Care Routine', 'Boot care kit', ['bick-4', 'horsehair-brush']],
        ],
        'what-to-wear-to-a-rodeo-the-ultimate' => [
            ['Denim Jeans', 'Shop the look', ['wrangler-13mwz', 'wrangler-women-bootcut']],
            ['Western Shirt', 'Shop the look', ['wrangler-snap-shirt']],
            ['Cowboy Hat', 'Shop the look', ['resistol-straw', 'stetson-felt']],
            ['Belt and Accessories', 'Shop the look', ['nocona-belt']],
            ['Family-Friendly Outfit Tips', 'For the kids', ['ariat-kids-heritage', 'kids-earmuffs']],
        ],
        'what-to-wear-to-a-rodeo-a-practical-stylish-guide' => [
            ['Cowboy Boots (Yes, They Matter)', 'Boots we like', ['ariat-heritage-roper', 'ariat-round-up-women']],
            ['Denim: The Rodeo Uniform', 'Shop the look', ['wrangler-13mwz', 'wrangler-women-bootcut']],
            ['Western Shirts', 'Shop the look', ['wrangler-snap-shirt']],
            ['Summer Rodeo', 'Beat the heat', ['resistol-straw', 'cooling-towel']],
            ['Winter Rodeo', 'Stay warm', ['sherpa-jacket', 'wild-rag']],
        ],
        'rodeo-fashion-guide-how-to-dress' => [
            ['Cowboy Hat', 'Hats and hat care', ['stetson-felt', 'hat-case']],
            ['Cowboy Boots', 'Boots we like', ['ariat-heritage-roper', 'ariat-round-up-women']],
            ['Belts and Buckles', 'Shop the look', ['nocona-belt']],
            ['Outerwear', 'Shop the look', ['sherpa-jacket', 'wild-rag']],
            ['Rainy or Dusty Conditions', 'Be ready for weather', ['rain-jacket']],
        ],
        'how-long-does-a-rodeo-last' => [
            ['Bring Essentials', 'What to pack', ['stadium-seat', 'sunscreen', 'power-bank']],
        ],
        'what-happens-at-a-rodeo-a-complete-guide' => [
            ['Quick Tips', 'First-rodeo checklist', ['stadium-seat', 'kids-earmuffs', 'binoculars']],
        ],
        'how-to-bull-ride-a-beginner' => [
            ['Protective Equipment', 'Protective gear', ['bull-helmet', 'rodeo-vest', 'mouthguard', 'bull-glove']],
            ['Riding Equipment', 'Riding gear', ['bull-rope', 'rosin', 'spurs']],
        ],
        'how-to-get-into-rodeo' => [
            ['Essential Rodeo Gear', 'Starter gear', ['ariat-heritage-roper', 'rodeo-vest', 'roping-gloves']],
            ['Event-Specific Gear', 'Event gear', ['team-rope', 'chaps']],
        ],
        'what-is-breakaway-roping-a-complete-guide' => [
            ['Essential Gear for Breakaway Roping', 'Breakaway gear', ['breakaway-rope', 'breakaway-honda', 'roping-gloves']],
            ['Use a Roping Dummy', 'Practice at home', ['roping-dummy']],
        ],
        'how-does-team-roping-work' => [
            ['Equipment That Makes It Work', 'Team roping gear', ['team-rope', 'roping-gloves', 'splint-boots', 'rope-bag']],
            ['Learn the Basics', 'Practice at home', ['roping-dummy']],
        ],
        'bull-riding-scoring-explained' => [
            ['Tips for Fans', 'For your next rodeo', ['binoculars']],
        ],
        'how-is-bull-riding-scored' => [
            ['Famous High Scores', 'Watch it', ['eight-seconds']],
        ],
        'famous-texas-rodeo-cowboys' => [
            ['Hall of Fame and Legacy', 'Further reading', ['rodeo-history-book']],
        ],
        'history-of-rodeo-in-texas-where-grit' => [
            ['Practical Takeaways', 'Further reading', ['texas-cowboy-book', 'rodeo-history-book']],
        ],
    ];
}

/** Tagged Amazon URL for a product key. */
function aff_url(string $key): string
{
    $p = aff_products()[$key] ?? null;
    if (!$p) {
        return '';
    }
    if (!empty($p['asin'])) {
        return 'https://www.amazon.com/dp/' . rawurlencode($p['asin']) . '/?tag=' . rawurlencode(AFF_TAG);
    }
    return 'https://www.amazon.com/s?k=' . rawurlencode($p['q']) . '&tag=' . rawurlencode(AFF_TAG);
}

function aff_link(string $key, bool $withNote = true): string
{
    $p = aff_products()[$key] ?? null;
    if (!$p) {
        return '';
    }
    $html = '<a href="' . e(aff_url($key)) . '" rel="sponsored nofollow noopener" target="_blank">' . e($p['name']) . '</a>';
    if ($withNote && !empty($p['note'])) {
        $html .= '<span class="aff-note">' . e($p['note']) . '</span>';
    }
    return $html;
}

/** Styles are printed once, the first time an affiliate block renders. */
function aff_styles(): string
{
    static $done = false;
    if ($done) {
        return '';
    }
    $done = true;
    return '<style>'
        . '.aff-box{margin:1.5rem 0;padding:1rem 1.15rem;border:1px solid rgba(122,59,27,.25);border-left:4px solid #7a3b1b;border-radius:6px;background:rgba(122,59,27,.04)}'
        . '.aff-box__label{margin:0 0 .5rem;font-size:.78rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#7a3b1b}'
        . '.aff-box ul,.aff-card ul{margin:0;padding:0;list-style:none;display:grid;gap:.55rem}'
        . '.aff-box li,.aff-card li{margin:0;padding:0}'
        . '.aff-box a,.aff-card a{font-weight:700}'
        . '.aff-note{display:block;font-size:.88em;opacity:.8}'
        . '.aff-box__cta{margin:.6rem 0 0;font-size:.8rem;opacity:.75}'
        . '.aff-disclosure{font-size:.85rem;opacity:.8;margin:0 0 1.25rem;font-style:italic}'
        . '</style>';
}

function aff_box(string $title, array $keys): string
{
    $items = '';
    foreach ($keys as $k) {
        $l = aff_link($k);
        if ($l !== '') {
            $items .= '<li>' . $l . '</li>';
        }
    }
    if ($items === '') {
        return '';
    }
    return aff_styles() . '<aside class="aff-box" aria-label="' . e($title) . '"><p class="aff-box__label">' . e($title) . '</p><ul>' . $items . '</ul>'
        . '<p class="aff-box__cta">Opens on Amazon. We may earn a commission.</p></aside>';
}

/** Sidebar card for articles and event pages. */
function aff_side_card(string $heading = 'Packing for the rodeo', ?array $keys = null): string
{
    if (!AFF_ENABLED) {
        return '';
    }
    $keys = $keys ?? ['stadium-seat', 'clear-bag', 'kids-earmuffs', 'binoculars', 'power-bank'];
    $items = '';
    foreach ($keys as $k) {
        $items .= '<li>' . aff_link($k) . '</li>';
    }
    return aff_styles() . '<div class="side-card aff-card"><h2>' . e($heading) . '</h2><ul>' . $items . '</ul>'
        . '<p class="fineprint">As an Amazon Associate, Rodeo Texas earns from qualifying purchases.</p></div>';
}

/** Normalize heading text for matching: no tags, decoded entities, straight quotes, lower case. */
function aff_norm(string $s): string
{
    $s = html_entity_decode(strip_tags($s), ENT_QUOTES | ENT_HTML5, 'UTF-8');
    $s = str_replace(["\u{2019}", "\u{2018}", "\u{201C}", "\u{201D}", "\u{00A0}"], ["'", "'", '"', '"', ' '], $s);
    return strtolower(trim(preg_replace('/\s+/u', ' ', $s)));
}

/**
 * Insert product boxes into an article's HTML. Returns the HTML unchanged if
 * the article has no placements or anything goes wrong.
 */
function aff_inject(string $slug, string $html): string
{
    if (!AFF_ENABLED) {
        return $html;
    }
    $place = aff_placements()[$slug] ?? null;
    if (!$place) {
        return $html;
    }
    try {
        if (!preg_match_all('#<h([2-4])\b[^>]*>(.*?)</h\1>#is', $html, $m, PREG_OFFSET_CAPTURE)) {
            return $html;
        }
        $heads = [];
        foreach ($m[0] as $i => $full) {
            $heads[] = ['start' => $full[1], 'end' => $full[1] + strlen($full[0]), 'text' => aff_norm($m[2][$i][0])];
        }
        $inserts = [];
        $used = [];
        foreach ($place as [$match, $title, $keys]) {
            $needle = aff_norm($match);
            foreach ($heads as $i => $h) {
                if (isset($used[$i]) || !str_contains($h['text'], $needle)) {
                    continue;
                }
                $used[$i] = true;
                // End of this section = start of the next heading, or end of content.
                $pos = isset($heads[$i + 1]) ? $heads[$i + 1]['start'] : strlen($html);
                $inserts[$pos] = ($inserts[$pos] ?? '') . aff_box($title, $keys);
                break;
            }
        }
        if (!$inserts) {
            return $html;
        }
        krsort($inserts);
        foreach ($inserts as $pos => $box) {
            $html = substr($html, 0, $pos) . $box . substr($html, $pos);
        }
        return aff_styles() . '<p class="aff-disclosure">This guide contains affiliate links. As an Amazon Associate, Rodeo Texas earns from qualifying purchases, at no extra cost to you.</p>' . $html;
    } catch (\Throwable $ex) {
        return $html;
    }
}
