<?php
// Plan catalog UI pieces shared by the plan pages, /home-designs/ and the service pages.

function money(float $v): string
{
    return '$' . number_format($v);
}

/** Card for one plan. $h is the heading level inside the card. */
function plan_card(string $slug, string $h = 'h3'): string
{
    global $PLANS;
    $p = $PLANS[$slug];
    $specs = [number_format($p['sqft']) . ' sq ft', $p['bed_label'], $p['bath_label'], $p['width'] . ' x ' . $p['depth']];
    return '<article class="card plan-card" data-design="' . e($p['category']) . '">'
        . '<a class="plan-card-img" href="' . e($p['url']) . '" tabindex="-1" aria-hidden="true">'
        . '<img src="' . e($p['image']) . '" alt="" width="1200" height="750" loading="lazy"></a>'
        . '<div class="card-body"><span class="card-kicker">' . e(PLAN_CATEGORIES[$p['category']] . ' · ' . implode(', ', $p['styles'])) . '</span>'
        . "<$h><a href=\"" . e($p['url']) . '">' . e($p['name']) . "</a></$h>"
        . '<div class="spec-row">' . implode('', array_map(fn($s) => '<span class="spec">' . e($s) . '</span>', $specs)) . '</div>'
        . '<p class="plan-card-foot"><span class="plan-price">' . money($p['price']) . '</span><a class="card-more" href="' . e($p['url']) . '">View plan →</a></p>'
        . '</div></article>';
}

function plan_grid(array $slugs, string $h = 'h3'): void
{
    echo '<div class="grid-3 plan-grid">' . implode('', array_map(fn($s) => plan_card($s, $h), $slugs)) . '</div>';
}

/** "Plans you can buy" strip for service and area pages. */
function plan_strip(array $categories, string $heading, string $intro = '', int $limit = 3): void
{
    global $PLANS;
    // Alternate between the categories so a mixed strip shows a bit of each.
    $by = array_map(fn($c) => array_keys(array_filter($PLANS, fn($p) => $p['category'] === $c)), $categories);
    $slugs = [];
    for ($i = 0; count($slugs) < $limit && $i < 30; $i++) {
        foreach ($by as $list) if (isset($list[$i]) && count($slugs) < $limit) $slugs[] = $list[$i];
    }
    echo '<section class="section section--alt"><div class="wrap"><div class="section-head"><h2>' . e($heading) . '</h2>';
    if ($intro) echo '<p class="section-intro">' . $intro . '</p>';
    echo '</div>';
    plan_grid($slugs);
    echo '<p class="btn-row"><a class="btn btn--outline" href="/home-designs/">See all ' . count($PLANS) . ' Texas house plans</a></p></div></section>';
}

/** How each home type is regulated in Texas: [heading, paragraph HTML]. */
function texas_rules(array $p): array
{
    $laws = '<a href="/guides/tiny-house-laws-texas/">Texas tiny house laws guide</a>';
    switch ($p['type']) {
        case 'thow':
            return ['A tiny house on wheels in Texas',
                'In Texas a tiny house on wheels is titled and registered as a trailer through TxDMV. This plan stays inside the no-permit road limits of 8 ft 6 in. wide and 14 ft high (it is drawn at 13 ft 6 in.), and a truck and trailer together can be up to 65 ft long. Trailers over 4,500 lb need brakes, and a combination over 26,000 lb with a trailer over 10,000 lb needs a Class A license. Where you can live in it full time is up to the city, county or RV park. See the ' . $laws . '.'];
        case 'park-model':
            return ['A park model in Texas',
                'A park model is a recreational vehicle, not a house: it is built to ANSI A119.5 (400 sq ft or less in setup mode) and NFPA 70 Article 551, certified by the manufacturer and titled through the Texas DMV. It is not reviewed under the IRC. These drawings give a park model manufacturer or builder a complete design to certify. RV parks, HOAs and some counties set their own placement rules. See the ' . $laws . '.'];
        case 'adu':
            return ['Building an ADU in Texas',
                'Texas cities that regulate building adopt the International Residential Code (IRC) with local amendments, and each city writes its own ADU rules: maximum size, height, setbacks, parking, utilities and whether the owner must live on site. Austin, San Antonio, Dallas, Fort Worth and Houston all allow accessory units in some form, with different limits. Confirm with your city before you buy. See the ' . $laws . '.'];
        case 'studio':
            return ['Permits for a backyard studio in Texas',
                'Accessory buildings without a kitchen are usually simpler to permit than a dwelling, and some Texas cities exempt small buildings altogether. Rules on size, height and setbacks still apply, and adding a bathroom or sleeping area can change how the city classifies it. Ask your building department first. See the ' . $laws . '.'];
        default:
            return ['Building this home in Texas',
                'Texas cities adopt the International Residential Code (IRC) with local amendments and review plans like this one for a building permit. Many unincorporated county areas have no residential building code at all, though septic, floodplain and driveway permits still apply, and lenders and insurers often expect code-built work anyway. See the ' . $laws . '.'];
    }
}

/** Texas climate, soils and wind notes common to every plan. */
function texas_build_notes(array $p): array
{
    $n = [
        ['Cooling-first design', 'Drawn for IECC climate zones 2 and 3: radiant-barrier roof deck, R-38 attic, R-21 walls, windows with SHGC 0.25 or less, 18 in. overhangs, shaded porches, ceiling fans and ductless heat pumps sized room by room.'],
        ['Wind', 'Framed for 115 mph design wind (inland Texas, Exposure B) with a continuous load path. Houston-area and Gulf Coast sites need an engineer\'s wind upgrade, and sites in the TDI catastrophe area need Texas Department of Insurance windstorm certification.'],
        ['Termites', 'Texas is a very heavy termite area: the plans call for soil treatment or a barrier, treated sill plates and siding kept 6 in. above grade.'],
    ];
    if (!$p['mobile'] && $p['type'] !== 'park-model') {
        array_splice($n, 1, 0, [['Expansive clay soils', 'The slab is drawn as a stiffened slab-on-grade with 12 x 24 in. grade beams for moderate soils. Get a geotechnical report for your lot; a Texas-licensed engineer finalizes the slab (or a post-tensioned design) from it.']]);
    }
    return $n;
}
