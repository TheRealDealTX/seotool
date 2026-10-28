<?php
/**
 * Site-wide constants and page registry for austinsroofing.com.
 *
 * Everything that appears on more than one page (business details, nav,
 * the service / area / tool / blog lists) is defined here once. The
 * registries also drive the blog index, the HTML sitemap, the XML sitemaps
 * and the internal-link blocks, so adding a page means adding it here.
 */

if (!defined('AR_ROOT')) {
    define('AR_ROOT', dirname(__DIR__));
}

const BIZ = [
    'name'          => 'Austin Roofing',
    'legal_name'    => 'Austin Roofing',
    'origin'        => 'https://austinsroofing.com',
    'phone_display' => '+1 (956) 465-6045',
    'phone_short'   => '(956) 465-6045',
    'phone_href'    => '+19564656045',
    'email'         => 'info@austinsroofing.com',
    'city'          => 'Austin',
    'state'         => 'TX',
    'state_long'    => 'Texas',
    'county'        => 'Travis County',
    'region'        => 'Central Texas',
    'latitude'      => '30.2672',
    'longitude'     => '-97.7431',
    'hours'         => '24/7 Emergency Services',
    'ga4'           => 'G-G6C3B8SGY7',
    'logo'          => '/wp-content/uploads/2025/11/Austin-Roofing-Logo.webp',
    'logo_small'    => '/wp-content/uploads/2025/11/Austin-Roofing-Logo-300x146.webp',
    'icon'          => '/wp-content/uploads/2025/11/cropped-Austin-Roofing-Icon.webp',
    'og_image'      => '/wp-content/uploads/2025/12/Austin-Roofing-Site-Image.webp',
];

// Where the estimate / contact form is delivered.
const FORM_TO = 'info@austinsroofing.com';

const NAV = [
    ['Home', '/'],
    ['About Us', '/about-us/'],
    ['Services', '/services/', 'services'],
    ['Service Areas', '/service-areas/', 'areas'],
    ['Roofing Tools', '/roofing-tools/', 'tools'],
    ['FAQs', '/faqs/'],
    ['Blog', '/blog/'],
];

/**
 * Service pages: /services/{slug}/
 * anchor = the matching section id on the /services/ hub (old WordPress
 * anchors are kept so footer links from Google's cache still land).
 */
const SERVICES = [
    'roof-repair' => [
        'name' => 'Roof Repair', 'h1' => 'Austin Roof Repair',
        'kw' => 'austin roof repair', 'icon' => 'hammer', 'group' => 'residential',
        'blurb' => 'Leaks, missing shingles, failed flashing and storm wear repaired fast — with photos of every problem before we fix it.',
    ],
    'roof-replacement' => [
        'name' => 'Roof Replacement', 'h1' => 'Austin Roof Replacement',
        'kw' => 'austin roof replacement', 'icon' => 'house', 'group' => 'residential',
        'blurb' => 'Full tear-off and new roof systems built for Central Texas heat and hail, usually completed in one to two days.',
    ],
    'roof-installation' => [
        'name' => 'Roof Installation', 'h1' => 'Austin Roof Installation',
        'kw' => 'austin roof installation', 'icon' => 'layers', 'group' => 'residential',
        'blurb' => 'New-construction and additions roofed to code with matched underlayment, ventilation and flashing details.',
    ],
    'residential-roofing' => [
        'name' => 'Residential Roofing', 'h1' => 'Austin Residential Roofing',
        'kw' => 'austin residential roofing', 'icon' => 'home', 'group' => 'residential',
        'blurb' => 'Shingle, metal and composition roofs for Austin homeowners — repair, replacement, ventilation and gutters.',
    ],
    'shingle-roofing' => [
        'name' => 'Composition Shingle Roofing', 'h1' => 'Austin Composition Shingle Roofing',
        'kw' => 'austin composition roofing', 'icon' => 'grid', 'group' => 'residential',
        'blurb' => 'Architectural, impact-resistant (Class 4) and designer composition shingles installed to manufacturer spec.',
    ],
    'metal-roofing' => [
        'name' => 'Metal Roofing', 'h1' => 'Austin Metal Roofing',
        'kw' => 'austin metal roofing', 'icon' => 'bars', 'group' => 'residential',
        'blurb' => 'Standing seam, exposed-fastener and stone-coated steel roofs that shrug off Texas sun and last 40+ years.',
    ],
    'commercial-roofing' => [
        'name' => 'Commercial Roofing', 'h1' => 'Austin Commercial Roofing',
        'kw' => 'austin commercial roofing', 'icon' => 'building', 'group' => 'commercial', 'anchor' => 'Commercial-Roof-Repair',
        'blurb' => 'TPO, EPDM, modified bitumen, built-up and metal systems — repair, replacement and maintenance plans.',
    ],
    'commercial-roof-coatings' => [
        'name' => 'Commercial Roof Coatings', 'h1' => 'Austin Commercial Roof Coatings',
        'kw' => 'austin commercial roof coatings', 'icon' => 'drop', 'group' => 'commercial', 'anchor' => 'Commercial-Roof-Coatings',
        'blurb' => 'Silicone, acrylic and polyurethane coatings that seal leaks and cut cooling loads without a tear-off.',
    ],
    'multifamily-roofing' => [
        'name' => 'Multi-Family Roofing', 'h1' => 'Austin Multi-Family Roofing',
        'kw' => 'austin multi-family roofing', 'icon' => 'apartments', 'group' => 'commercial', 'anchor' => 'Multifamily-Roofing',
        'blurb' => 'Apartments, townhomes, condos and HOA communities roofed on a phased schedule with minimal resident disruption.',
    ],
    'roof-restoration' => [
        'name' => 'Roof Restoration', 'h1' => 'Austin Roof Restoration',
        'kw' => 'austin roof restoration', 'icon' => 'refresh', 'group' => 'residential', 'anchor' => 'Roof-Restoration',
        'blurb' => 'Repair, reinforce and re-seal a roof that still has good bones — years of extra life for a fraction of replacement.',
    ],
    'hail-damage-repair' => [
        'name' => 'Hail Damage Repair', 'h1' => 'Austin Hail Damage Roof Repair',
        'kw' => 'austin hail damage roof repair', 'icon' => 'hail', 'group' => 'storm', 'anchor' => 'Hail-Damage-Repair',
        'blurb' => 'Bruised shingles, granule loss and dented metal found, photographed and documented for your insurer.',
    ],
    'wind-damage-repair' => [
        'name' => 'Wind Damage Repair', 'h1' => 'Austin Wind Damage Roof Repair',
        'kw' => 'austin wind damage roof repair', 'icon' => 'wind', 'group' => 'storm', 'anchor' => 'Wind-Damage-Repair',
        'blurb' => 'Lifted tabs, creased shingles, blown-off ridge caps and torn flashing secured before the next rain.',
    ],
    'emergency-roof-repair' => [
        'name' => 'Emergency Roof Repair', 'h1' => 'Austin Emergency Roof Repair',
        'kw' => 'austin emergency roof repair', 'icon' => 'alert', 'group' => 'storm',
        'blurb' => '24/7 tarping and leak control after storms, fallen limbs or sudden leaks — call and talk to a roofer.',
    ],
    'roof-insurance-claims' => [
        'name' => 'Roof Insurance Claim Help', 'h1' => 'Austin Roof Insurance Claim Help',
        'kw' => 'roof damage insurance claims in austin', 'icon' => 'shield', 'group' => 'storm',
        'blurb' => 'Photo-documented damage reports and adjuster meetings so your hail or wind claim reflects the real damage.',
    ],
    'roof-inspection' => [
        'name' => 'Roof Inspection', 'h1' => 'Austin Roof Inspection',
        'kw' => 'austin roof inspection', 'icon' => 'search', 'group' => 'residential',
        'blurb' => 'Free, photo-documented inspections for storms, home sales, insurance renewals and aging roofs.',
    ],
];

const SERVICE_GROUPS = [
    'residential' => 'Residential Roofing',
    'commercial'  => 'Commercial & Multi-Family',
    'storm'       => 'Storm Damage & Emergency',
];

/**
 * Service-area pages: /service-areas/{slug}/
 */
const AREAS = [
    'east-austin'      => ['name' => 'East Austin',      'h1' => 'East Austin Roofing',            'county' => 'Travis County',  'kind' => 'neighborhood'],
    'south-austin'     => ['name' => 'South Austin',     'h1' => 'South Austin Roofing',           'county' => 'Travis County',  'kind' => 'neighborhood'],
    'round-rock-tx'    => ['name' => 'Round Rock',       'h1' => 'Round Rock Roofing',             'county' => 'Williamson County'],
    'pflugerville-tx'  => ['name' => 'Pflugerville',     'h1' => 'Pflugerville Roofing',           'county' => 'Travis County'],
    'cedar-park-tx'    => ['name' => 'Cedar Park',       'h1' => 'Cedar Park Roofing',             'county' => 'Williamson County'],
    'leander-tx'       => ['name' => 'Leander',          'h1' => 'Leander Roofing',                'county' => 'Williamson County'],
    'georgetown-tx'    => ['name' => 'Georgetown',       'h1' => 'Georgetown Roofing',             'county' => 'Williamson County'],
    'hutto-tx'         => ['name' => 'Hutto',            'h1' => 'Hutto Roofing',                  'county' => 'Williamson County'],
    'kyle-tx'          => ['name' => 'Kyle',             'h1' => 'Kyle Roofing',                   'county' => 'Hays County'],
    'san-marcos-tx'    => ['name' => 'San Marcos',       'h1' => 'San Marcos Roofing',             'county' => 'Hays County'],
    'dripping-springs-tx' => ['name' => 'Dripping Springs', 'h1' => 'Dripping Springs Roofing',    'county' => 'Hays County'],
    'lockhart-tx'      => ['name' => 'Lockhart',         'h1' => 'Lockhart Roofing',               'county' => 'Caldwell County'],
    'bastrop-tx'       => ['name' => 'Bastrop',          'h1' => 'Bastrop Roofing',                'county' => 'Bastrop County'],
];

/**
 * Interactive tools: /roofing-tools/{slug}/
 * 'tool' is the data-tool key the JS mounts on.
 */
const TOOLS = [
    'roof-cost-calculator' => [
        'name' => 'Roof Replacement Cost Calculator', 'tool' => 'cost', 'icon' => 'calc',
        'blurb' => 'Estimate a planning range for a new roof in the Austin area by size, pitch, material and tear-off.',
    ],
    'roofing-square-calculator' => [
        'name' => 'Roofing Square & Shingle Bundle Calculator', 'tool' => 'squares', 'icon' => 'grid',
        'blurb' => 'Turn your home’s footprint and pitch into roofing squares, shingle bundles, underlayment rolls and ridge cap.',
    ],
    'roof-pitch-calculator' => [
        'name' => 'Roof Pitch Calculator', 'tool' => 'pitch', 'icon' => 'pitch',
        'blurb' => 'Enter rise and run to get pitch, angle and the area multiplier — with a live roof diagram.',
    ],
    'repair-or-replace-quiz' => [
        'name' => 'Repair or Replace? Roof Quiz', 'tool' => 'quiz', 'icon' => 'question',
        'blurb' => 'Seven quick questions that tell you whether your roof probably needs a repair, a closer look or a replacement.',
    ],
    'hail-damage-checker' => [
        'name' => 'Hail Size & Roof Damage Checker', 'tool' => 'hail', 'icon' => 'hail',
        'blurb' => 'Pick the hail size you saw and your roof type to see the damage it typically causes and what to do next.',
    ],
    'roof-lifespan-calculator' => [
        'name' => 'Roof Lifespan Calculator', 'tool' => 'lifespan', 'icon' => 'clock',
        'blurb' => 'See how many years your roof likely has left in Central Texas heat, based on material, age and attic ventilation.',
    ],
];

/**
 * Blog posts: /blog/{slug}/  (all URLs carried over from WordPress)
 * img paths are the original WordPress uploads.
 */
const POSTS = [
    'roofing-underlayment-material-types' => [
        'title' => 'Roof Underlayment Types: Roofing Felt, Synthetic & More',
        'h1' => 'Roofing Underlayment Material Types: A Complete Guide',
        'desc' => 'Compare roof underlayment types — #15 and #30 roofing felt, synthetic and peel-and-stick — with costs, lifespans and which works best for Austin, TX roofs.',
        'date' => '2026-01-09', 'modified' => '2026-10-28', 'wp_id' => 163,
        'img' => '/wp-content/uploads/2026/01/Roofing-Underlayment-Material-Types-A-Complete-Guide.webp',
        'thumb' => '/wp-content/uploads/2026/01/Roofing-Underlayment-Material-Types-A-Complete-Guide-768x511.webp',
        'excerpt' => 'Felt, synthetic or self-adhered? Every type of roof underlayment and roofing paper compared side by side, with what Austin roofers actually install.',
        'tool' => 'roofing-square-calculator',
    ],
    'cost-of-asphalt-shingles-per-square' => [
        'title' => 'Cost of Asphalt Shingles Per Square (2026 Price Guide)',
        'h1' => 'Cost of Asphalt Shingles Per Square: A Complete Pricing Guide',
        'desc' => 'What shingles cost per square in 2026 — 3-tab, architectural (dimensional) and premium — material vs installed price, and a free shingle calculator.',
        'date' => '2026-01-05', 'modified' => '2026-10-28', 'wp_id' => 130,
        'img' => '/wp-content/uploads/2026/01/Cost-of-Asphalt-Shingles-Per-Square.webp',
        'thumb' => '/wp-content/uploads/2026/01/Cost-of-Asphalt-Shingles-Per-Square-768x511.webp',
        'excerpt' => 'Shingle prices per square for 3-tab, dimensional and premium asphalt shingles, plus what drives the installed price on an Austin roof.',
        'tool' => 'roofing-square-calculator',
    ],
    'insurance-coverage-for-storm-damaged-roofs' => [
        'title' => 'Insurance Coverage for Storm-Damaged Roofs in Texas',
        'h1' => 'Insurance Coverage for Storm-Damaged Roofs',
        'desc' => 'How homeowners insurance covers hail and wind roof damage in Austin and Texas: ACV vs RCV, deductibles, the claim process and why claims get underpaid.',
        'date' => '2026-01-12', 'modified' => '2026-10-28', 'wp_id' => 167,
        'img' => '/wp-content/uploads/2026/01/insurance-coverage-for-storm-damaged-roofs.png',
        'thumb' => '/wp-content/uploads/2026/01/insurance-coverage-for-storm-damaged-roofs-768x512.png',
        'excerpt' => 'What your policy covers after hail or wind, how ACV and replacement-cost policies differ, and how to file a roof claim in Austin without leaving money behind.',
        'tool' => 'hail-damage-checker',
    ],
    'architectural-shingle-vs-asphalt-shingles' => [
        'title' => 'Architectural Shingles vs Asphalt Shingles: Key Differences',
        'h1' => 'Architectural Shingle vs Asphalt Shingles',
        'desc' => 'Architectural vs 3-tab asphalt shingles compared: cost per square, lifespan, wind and hail ratings, and which is the better buy for a Texas roof.',
        'date' => '2026-01-06', 'modified' => '2026-10-28', 'wp_id' => 144,
        'img' => '/wp-content/uploads/2026/01/Architectural-Shingle-vs-Asphalt-Shingles.webp',
        'thumb' => '/wp-content/uploads/2026/01/Architectural-Shingle-vs-Asphalt-Shingles-768x511.webp',
        'excerpt' => 'Both are asphalt shingles — but thickness, wind rating, lifespan and price per square are very different. Here is how they compare.',
        'tool' => 'roof-cost-calculator',
    ],
    'roof-replacement-permit-requirements' => [
        'title' => 'Roof Replacement Permit Requirements & Guidelines',
        'h1' => 'Roof Replacement Permit Requirements: Homeowners Need to Know',
        'desc' => 'Roof replacement permit requirements and guidelines: when a re-roof needs a permit, who pulls it, inspections, codes and what applies in Austin, TX.',
        'date' => '2026-01-04', 'modified' => '2026-10-28', 'wp_id' => 149,
        'img' => '/wp-content/uploads/2026/01/Roof-Replacement-Permit-Requirements.webp',
        'thumb' => '/wp-content/uploads/2026/01/Roof-Replacement-Permit-Requirements-768x511.webp',
        'excerpt' => 'When a re-roof needs a permit, who is responsible for pulling it, what inspectors check and what Austin-area homeowners should ask their roofer.',
        'tool' => 'roof-cost-calculator',
    ],
    'residential-metal-roofing-lifespan' => [
        'title' => 'Residential Metal Roofing Lifespan: How Long It Lasts',
        'h1' => 'Residential Metal Roofing Lifespan: What Impacts Their Durability',
        'desc' => 'Residential metal roofs last 40–70+ years. See lifespan by metal type and profile, what shortens it in Texas heat and hail, and whether metal is worth it.',
        'date' => '2026-01-03', 'modified' => '2026-10-28', 'wp_id' => 139,
        'img' => '/wp-content/uploads/2026/01/Residential-Metal-Roofing-Lifespan.webp',
        'thumb' => '/wp-content/uploads/2026/01/Residential-Metal-Roofing-Lifespan-768x511.webp',
        'excerpt' => 'Steel, aluminum, standing seam or stone-coated: how long each metal roof lasts and the installation details that decide it.',
        'tool' => 'roof-lifespan-calculator',
    ],
    'how-much-does-it-cost-to-replace-a-roof' => [
        'title' => 'Cost to Replace a Roof on a 1,500 Sq Ft House (2026)',
        'h1' => 'How Much Does It Cost to Replace a Roof on a 1,500 Square Foot House?',
        'desc' => 'Roof replacement cost for a 1,500 sq ft house by material, with squares math, tear-off, decking and permit costs explained — plus a free cost calculator.',
        'date' => '2026-01-02', 'modified' => '2026-10-28', 'wp_id' => 127,
        'img' => '/wp-content/uploads/2026/01/How-much-does-it-cost-to-replace-a-roof-on-a-1500-square-foot-house.webp',
        'thumb' => '/wp-content/uploads/2026/01/How-much-does-it-cost-to-replace-a-roof-on-a-1500-square-foot-house-768x511.webp',
        'excerpt' => 'A one-story 1,500 sq ft house needs roughly 20–22 squares of roofing — a two-story about half that. Here is what that costs in shingles, metal and tile.',
        'tool' => 'roof-cost-calculator',
    ],
    'what-is-a-square-in-roofing' => [
        'title' => 'What Is a Square in Roofing? How to Calculate Squares',
        'h1' => 'What Is a Square in Roofing?',
        'desc' => 'A roofing square is 100 sq ft of roof surface. Learn how to calculate squares from your home’s footprint and pitch, waste factor and bundles per square.',
        'date' => '2025-12-30', 'modified' => '2026-10-28', 'wp_id' => 103,
        'img' => '/wp-content/uploads/2025/12/What-Is-a-Square-in-Roofing.webp',
        'thumb' => '/wp-content/uploads/2025/12/What-Is-a-Square-in-Roofing-768x512.webp',
        'excerpt' => 'One roofing square equals 100 square feet. How to measure squares, add pitch and waste, and read a roofing estimate like a contractor.',
        'tool' => 'roofing-square-calculator',
    ],
    'residential-roofing-warranty-coverage-guide-for-homeowners' => [
        'title' => 'Residential Roofing Warranty Coverage Guide for Homeowners',
        'h1' => 'Residential Roofing Warranty Coverage Guide for Homeowners',
        'desc' => 'Roofing warranties explained: manufacturer vs workmanship coverage, prorated vs non-prorated terms, common exclusions and how to keep your warranty valid.',
        'date' => '2026-01-12', 'modified' => '2026-10-28', 'wp_id' => 171,
        'img' => '/wp-content/uploads/2026/01/Residential-Roofing-Warranty-Coverage-Guide-for-Homeowners.webp',
        'thumb' => '/wp-content/uploads/2026/01/Residential-Roofing-Warranty-Coverage-Guide-for-Homeowners-768x511.webp',
        'excerpt' => 'Material warranties, workmanship warranties and system warranties — what each one actually covers and the fine print that voids them.',
        'tool' => 'roof-lifespan-calculator',
    ],
    'ice-and-water-shield-installation-cost' => [
        'title' => 'Ice and Water Shield Installation Cost Explained',
        'h1' => 'Ice and Water Shield Installation Cost Explained',
        'desc' => 'Ice and water shield costs per roll and per square, targeted vs full-deck installation, and where self-adhered membrane earns its keep on Texas roofs.',
        'date' => '2026-01-08', 'modified' => '2026-10-28', 'wp_id' => 159,
        'img' => '/wp-content/uploads/2026/01/Ice-and-Water-Shield-Installation-Cost.webp',
        'thumb' => '/wp-content/uploads/2026/01/Ice-and-Water-Shield-Installation-Cost-768x511.webp',
        'excerpt' => 'Self-adhered membrane in valleys and at penetrations, or across the whole deck? What each approach costs and when it is worth it.',
        'tool' => 'roofing-square-calculator',
    ],
    'attic-ventilation-upgrade-benefits' => [
        'title' => 'Attic Ventilation Upgrade Benefits for Texas Homes',
        'h1' => 'Attic Ventilation Upgrade Benefits for Long-Term Home Performance',
        'desc' => 'Attic ventilation upgrade benefits: cooler attics, lower AC bills, longer shingle life and fewer moisture problems — plus how to size intake and exhaust.',
        'date' => '2026-01-07', 'modified' => '2026-10-28', 'wp_id' => 155,
        'img' => '/wp-content/uploads/2026/01/Attic-Ventilation-Upgrade-Benefits.webp',
        'thumb' => '/wp-content/uploads/2026/01/Attic-Ventilation-Upgrade-Benefits-768x511.webp',
        'excerpt' => 'Why a balanced intake-and-exhaust system can drop attic temperatures, protect shingles and ease the load on your AC through an Austin summer.',
        'tool' => 'roof-lifespan-calculator',
    ],
];

/**
 * Core pages (for the HTML/XML sitemaps). Paths carried over from WordPress
 * are marked wp => true.
 */
const CORE_PAGES = [
    '/'                  => ['Austin Roofing — Home', 'wp' => true, 'wp_id' => 18],
    '/about-us/'         => ['About Austin Roofing', 'wp' => true, 'wp_id' => 23],
    '/services/'         => ['Austin Roofing Services', 'wp' => true, 'wp_id' => 69],
    '/service-areas/'    => ['Service Areas'],
    '/roofing-tools/'    => ['Roofing Tools & Calculators'],
    '/faqs/'             => ['Roofing FAQs', 'wp' => true, 'wp_id' => 80],
    '/blog/'             => ['Roofing Blog', 'wp' => true],
    '/contact-us/'       => ['Contact Us — Free Estimate', 'wp' => true, 'wp_id' => 25],
    '/sitemap/'          => ['Sitemap', 'wp' => true, 'wp_id' => 123],
    '/privacy-policy/'   => ['Privacy Policy', 'wp' => true, 'wp_id' => 3],
    '/terms-of-service/' => ['Terms of Service', 'wp' => true, 'wp_id' => 75],
];

// Last content update, shown in sitemaps.
const SITE_UPDATED = '2026-10-28';
