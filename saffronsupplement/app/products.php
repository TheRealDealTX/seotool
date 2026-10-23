<?php
// Product catalogue. Facts (dose, standardisation, count) come from each
// product's Amazon listing title as of October 2026; scores are editorial.
// Prices change constantly, so the site links to Amazon instead of quoting them.
defined('SS_APP') || exit;

const PRODUCTS = [
    'nootropics-depot' => [
        'name' => 'Nootropics Depot High Potency Saffron Extract',
        'brand' => 'Nootropics Depot', 'asin' => 'B0B69MGMFW',
        'badge' => 'Best Overall', 'score' => 9.6,
        'dose' => 30, 'dose_label' => '30 mg', 'form' => 'Capsule',
        'extract' => 'Standardized to ≥7.5% crocins and ≥1% safranal',
        'std' => true, 'vegan' => true, 'goals' => ['mood', 'sleep', 'eyes', 'focus'],
        'summary' => 'A 30 mg capsule sits squarely in the dose range used in most published mood trials, and the label states both crocin and safranal minimums, which most saffron supplements leave out.',
        'pros' => ['30 mg matches the most-studied daily dose', 'Crocin and safranal content both disclosed', 'Single-ingredient formula, no fillers to work around'],
        'cons' => ['Costs more per capsule than bulk 88.5 mg brands', 'Not a branded clinical extract like affron® or Satiereal®'],
    ],
    'vinatura-affron' => [
        'name' => 'VINATURA Organic Saffron Supplement 28 mg (affron®)',
        'brand' => 'VINATURA', 'asin' => 'B0GH4TF614',
        'badge' => 'Best affron® Extract', 'score' => 9.4,
        'dose' => 28, 'dose_label' => '28 mg', 'form' => 'Veggie capsule',
        'extract' => 'affron® saffron extract (≥3.5% Lepticrosalides®)',
        'std' => true, 'vegan' => true, 'goals' => ['mood', 'sleep', 'stress'],
        'summary' => 'affron® is the extract behind several of the best-known saffron trials for low mood, stress and sleep. The 28 mg daily dose mirrors those studies almost exactly.',
        'pros' => ['Branded extract with its own published trials', '28 mg mirrors the studied affron® dose', 'Organic and vegan'],
        'cons' => ['45-capsule bottle runs out faster than bulk options', 'Newer listing with fewer reviews'],
    ],
    'life-extension' => [
        'name' => 'Life Extension Optimized Saffron',
        'brand' => 'Life Extension', 'asin' => 'B003UGS4T0',
        'badge' => 'Best for Appetite Control', 'score' => 9.1,
        'dose' => 88.5, 'dose_label' => '88.5 mg', 'form' => 'Veggie capsule',
        'extract' => 'Satiereal® saffron extract',
        'std' => true, 'vegan' => true, 'goals' => ['appetite', 'mood'],
        'summary' => 'Satiereal® is the extract studied for snacking and satiety. Life Extension has been selling this formula for years, and it is one of the few appetite-focused saffron products with a clinical extract behind it.',
        'pros' => ['Uses the extract studied for snacking and satiety', 'Long-established brand with in-house testing', 'Fits the twice-daily protocol from the trials'],
        'cons' => ['Appetite-focused; mood buyers may prefer a crocin-standardized 30 mg product', 'Premium price per serving'],
    ],
    'sports-research' => [
        'name' => 'Sports Research Pure Saffron 30 mg Plantgels™',
        'brand' => 'Sports Research', 'asin' => 'B0FY497SJJ',
        'badge' => 'Best Softgel', 'score' => 9.0,
        'dose' => 30, 'dose_label' => '30 mg', 'form' => 'Plant-based softgel',
        'extract' => 'Pure saffron extract',
        'std' => false, 'vegan' => true, 'goals' => ['mood', 'eyes', 'sleep'],
        'summary' => 'A 30 mg softgel from a brand known for third-party testing. It suits anyone who finds capsules hard to swallow.',
        'pros' => ['30 mg per serving', 'Plant-based softgel is easy to swallow', 'Well-known brand with a testing program'],
        'cons' => ['Standardization percentages not shown in the listing title', 'Higher price than capsule options'],
    ],
    'nutricost' => [
        'name' => 'Nutricost Saffron Extract 88.5 mg, 240 Capsules',
        'brand' => 'Nutricost', 'asin' => 'B09DTN7P4W',
        'badge' => 'Best Value', 'score' => 8.7,
        'dose' => 88.5, 'dose_label' => '88.5 mg', 'form' => 'Veggie capsule',
        'extract' => 'Saffron extract (standardization not specified)',
        'std' => false, 'vegan' => true, 'goals' => ['mood', 'appetite'],
        'summary' => 'With 240 capsules per bottle, Nutricost is one of the cheapest ways to take saffron daily for months. It is a good starter bottle if you want to see how saffron suits you before paying for a branded extract.',
        'pros' => ['240 capsules, roughly an 8-month supply at one a day', 'Very low cost per serving', 'Gluten-free veggie capsules'],
        'cons' => ['Crocin/safranal content not disclosed', '88.5 mg is a generic serving size, not a trial-matched dose'],
    ],
    'source-naturals' => [
        'name' => 'Source Naturals Serene Science Saffron Extract 15 mg',
        'brand' => 'Source Naturals', 'asin' => 'B07VXP9CBK',
        'badge' => 'Best Budget / Flexible Dosing', 'score' => 8.6,
        'dose' => 15, 'dose_label' => '15 mg', 'form' => 'Tablet',
        'extract' => 'Saffron extract, 15 mg per tablet',
        'std' => false, 'vegan' => false, 'goals' => ['mood', 'pms', 'sleep'],
        'summary' => 'At 15 mg per tablet, this lets you follow the classic "15 mg twice a day" protocol from the early depression and PMS trials, or start at 15 mg to judge your tolerance.',
        'pros' => ['15 mg tablets copy the twice-daily trial protocol', 'Easy to start low and step up', 'Very low price per bottle'],
        'cons' => ['30 tablets is only 15 days at 30 mg/day', 'Tablet, not capsule'],
    ],
    'now-foods' => [
        'name' => 'NOW Supplements Saffron 50 mg with 10% Crocins',
        'brand' => 'NOW Foods', 'asin' => 'B092XM6XCQ',
        'badge' => 'Most Trusted Brand', 'score' => 8.5,
        'dose' => 50, 'dose_label' => '50 mg', 'form' => 'Veggie capsule',
        'extract' => 'Saffron extract standardized to 10% crocins',
        'std' => true, 'vegan' => true, 'goals' => ['mood', 'eyes'],
        'summary' => 'NOW is one of the most widely audited supplement makers in the US, and this capsule discloses a 10% crocin standard.',
        'pros' => ['Crocin standardization disclosed', 'Trusted, GMP-certified manufacturer', 'Fair price'],
        'cons' => ['50 mg is above the 30 mg used in most mood trials', 'Not a branded clinical extract'],
    ],
    'zazzee' => [
        'name' => 'Zazzee USDA Organic Saffron 20:1 Extract 88.5 mg',
        'brand' => 'Zazzee', 'asin' => 'B0FPCT4L5J',
        'badge' => 'Best Organic', 'score' => 8.4,
        'dose' => 88.5, 'dose_label' => '88.5 mg', 'form' => 'Vegan capsule',
        'extract' => '20:1 extract, 0.3% safranal',
        'std' => true, 'vegan' => true, 'goals' => ['mood', 'appetite'],
        'summary' => 'Certified USDA Organic, with the extract ratio and safranal level printed on the label.',
        'pros' => ['USDA Organic certified', 'Extract ratio and safranal % disclosed', 'Vegan'],
        'cons' => ['Crocin content not stated', 'Generic 88.5 mg serving'],
    ],
    'affron-magnesium' => [
        'name' => 'affron® Saffron 28 mg + Magnesium Glycinate',
        'brand' => 'affron® formula', 'asin' => 'B0GCQ1TMBG',
        'badge' => 'Best for Stress & Sleep Combo', 'score' => 8.3,
        'dose' => 28, 'dose_label' => '28 mg', 'form' => 'Capsule',
        'extract' => 'affron® 28 mg with magnesium glycinate and L-theanine',
        'std' => true, 'vegan' => false, 'goals' => ['stress', 'sleep', 'mood'],
        'summary' => 'Pairs the studied 28 mg affron® dose with magnesium glycinate, a popular evening stack for stress and sleep.',
        'pros' => ['Clinical-dose affron®', 'Magnesium glycinate in the same capsule', 'Good fit for an evening routine'],
        'cons' => ['Blends make it harder to tell which ingredient is helping', 'Magnesium can loosen stools at high doses'],
    ],
    'thorne' => [
        'name' => 'Thorne Rapid Relief Saffron',
        'brand' => 'Thorne', 'asin' => 'B0H72WJ6JW',
        'badge' => 'Best Premium Brand', 'score' => 8.2,
        'dose' => 0, 'dose_label' => 'See label', 'form' => 'Capsule',
        'extract' => 'Saffron extract',
        'std' => false, 'vegan' => false, 'goals' => ['mood', 'stress'],
        'summary' => 'Thorne is known for NSF Certified for Sport products and tight manufacturing standards. You pay a premium for the name.',
        'pros' => ['Premium manufacturer with a strong testing reputation', 'Simple formula'],
        'cons' => ['Highest price on this list', 'Only 30 capsules', 'Few reviews yet'],
    ],
    'pink-stork' => [
        'name' => 'Pink Stork Saffron Extract for Women',
        'brand' => 'Pink Stork', 'asin' => 'B0G94TBXLH',
        'badge' => 'Best for Women / PMS', 'score' => 8.0,
        'dose' => 0, 'dose_label' => 'See label', 'form' => 'Capsule',
        'extract' => 'Saffron extract',
        'std' => false, 'vegan' => false, 'goals' => ['pms', 'mood'],
        'summary' => 'Made by a women\'s-health brand and marketed for monthly mood balance, which lines up with the saffron PMS studies.',
        'pros' => ['Women-focused brand', 'Simple, single-purpose formula'],
        'cons' => ['Only 30 capsules', 'Standardization not stated in the title'],
    ],
    'brainmd' => [
        'name' => 'BrainMD Happy Saffron Plus',
        'brand' => 'BrainMD', 'asin' => 'B08F2SK7ZW',
        'badge' => 'Best Saffron Blend', 'score' => 7.9,
        'dose' => 0, 'dose_label' => 'See label', 'form' => 'Vegan capsule',
        'extract' => 'Saffron flower extract + curcumin + zinc',
        'std' => false, 'vegan' => true, 'goals' => ['mood', 'focus'],
        'summary' => 'A mood blend that adds curcumin and zinc to saffron. Choose it if you want one combined capsule rather than separate supplements.',
        'pros' => ['Saffron, curcumin and zinc in one product', '90 capsules', 'Vegan and gluten-free'],
        'cons' => ['Expensive', 'Blends make dose-matching to trials harder'],
    ],
];

/** Shortlist shown on the homepage, in rank order. */
const TOP_PICKS = ['nootropics-depot', 'vinatura-affron', 'life-extension', 'sports-research', 'nutricost'];

/** Related (non-saffron-pill) products, linked as Amazon searches. */
const RELATED = [
    ['Premium Grade I saffron threads (for cooking & tea)', 'grade 1 saffron threads'],
    ['Saffron tea bags', 'saffron tea'],
    ['Magnesium glycinate (evening stack)', 'magnesium glycinate'],
    ['AREDS2 lutein & zeaxanthin (eye support)', 'areds 2 eye vitamins lutein zeaxanthin'],
    ['L-theanine (calm focus)', 'l-theanine 200mg'],
    ['Weekly pill organizer', 'weekly pill organizer am pm'],
];

function product($id) { return PRODUCTS[$id] ?? null; }

/** Full product review card. */
function product_card($id, $rank = null) {
    $p = PRODUCTS[$id];
    $h = '<article class="pcard" id="' . e($id) . '">';
    $h .= '<div class="pcard-top">' . ($rank ? '<span class="rank">#' . $rank . '</span>' : '')
        . '<span class="badge">' . e($p['badge']) . '</span><span class="score" title="Editorial score out of 10">'
        . number_format($p['score'], 1) . '<small>/10</small></span></div>';
    $h .= '<h3>' . amz($p['asin'], e($p['name'])) . '</h3>';
    $h .= '<ul class="specs"><li><b>Dose</b>' . e($p['dose_label']) . '</li><li><b>Form</b>' . e($p['form']) . '</li><li><b>Extract</b>' . e($p['extract']) . '</li></ul>';
    $h .= '<p>' . e($p['summary']) . '</p>';
    $h .= '<div class="pc"><div><h4>Pros</h4><ul class="pros">';
    foreach ($p['pros'] as $x) $h .= '<li>' . e($x) . '</li>';
    $h .= '</ul></div><div><h4>Cons</h4><ul class="cons">';
    foreach ($p['cons'] as $x) $h .= '<li>' . e($x) . '</li>';
    $h .= '</ul></div></div>' . amz_btn($p['asin']) . '</article>';
    return $h;
}

/** Compact one-line pick used in sidebars and inline recommendations. */
function product_inline($id, $why = '') {
    $p = PRODUCTS[$id];
    return '<div class="pinline"><div><span class="badge">' . e($p['badge']) . '</span><strong>' . e($p['name']) . '</strong>'
        . ($why ? '<p>' . e($why) . '</p>' : '') . '</div>' . amz_btn($p['asin'], 'View on Amazon') . '</div>';
}

/** Comparison table of all (or some) products. */
function compare_table(array $ids = null) {
    $ids = $ids ?? array_keys(PRODUCTS);
    $h = '<div class="table-wrap"><table class="compare"><thead><tr><th>Supplement</th><th>Best for</th><th>Dose</th><th>Extract details</th><th>Score</th><th></th></tr></thead><tbody>';
    foreach ($ids as $id) {
        $p = PRODUCTS[$id];
        $h .= '<tr><td><a href="/best-saffron-supplements/#' . e($id) . '">' . e($p['name']) . '</a></td><td>' . e($p['badge']) . '</td><td>'
            . e($p['dose_label']) . '</td><td>' . e($p['extract']) . '</td><td><b>' . number_format($p['score'], 1) . '</b></td><td>'
            . amz($p['asin'], 'Amazon', 'btn btn-sm btn-amz') . '</td></tr>';
    }
    return $h . '</tbody></table></div>';
}

/** JSON-friendly product list for the client-side tools. */
function products_json() {
    $out = [];
    foreach (PRODUCTS as $id => $p) {
        $out[] = ['id' => $id, 'name' => $p['name'], 'badge' => $p['badge'], 'dose' => $p['dose'], 'goals' => $p['goals'],
                  'std' => $p['std'], 'vegan' => $p['vegan'], 'score' => $p['score'], 'url' => amz_url($p['asin'])];
    }
    return json_encode($out, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
}
