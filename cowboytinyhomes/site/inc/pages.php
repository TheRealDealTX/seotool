<?php
// Route table: URL path => page metadata. The router serves pages/<file>.php for
// each path, and sitemap.xml is generated from this list.
//
//   file      page template under pages/
//   title     <title> (keep under ~60 chars, primary keyword first)
//   desc      meta description (~150-160 chars)
//   type      home | page | service | area | guide | tool | hub | legal
//   crumb     breadcrumb label
//   parent    path of the parent page for breadcrumbs (omit for top level)
//   image     social/OG image under /assets/img/
//   priority  sitemap priority
//   updated   last meaningful content change (Y-m-d)

define('PAGES', [
    '/' => [
        'file' => 'home', 'type' => 'home', 'crumb' => 'Home', 'priority' => '1.0',
        'title' => 'Tiny Home Builders Texas | Cowboy Tiny Homes',
        'desc'  => 'Cowboy Tiny Homes designs and builds custom tiny homes, ADUs, casitas, park models and tiny homes on wheels across Texas. Get a free design consult.',
        'image' => 'og-cowboy-tiny-homes.jpg',
    ],

    // ---- Services ---------------------------------------------------------
    '/custom-tiny-homes-texas/' => [
        'file' => 'services/custom-tiny-homes', 'type' => 'service', 'crumb' => 'Custom Tiny Homes', 'priority' => '0.9',
        'title' => 'Custom Tiny Homes Texas | Design & Build | Cowboy Tiny Homes',
        'desc'  => 'Custom tiny homes in Texas, designed around your land, budget and lifestyle and built to IRC code. Floor plans, renderings and full design-build service.',
        'image' => 'Custom-Tiny-Homes.webp',
    ],
    '/adu-builders-texas/' => [
        'file' => 'services/adu-builders', 'type' => 'service', 'crumb' => 'ADU Builders', 'priority' => '0.9',
        'title' => 'ADU Builders Texas | Casitas & Granny Flats | Cowboy Tiny Homes',
        'desc'  => 'Texas ADU builders for backyard casitas, granny flats, guest houses and mother-in-law suites. Permit-ready plans and code-compliant construction.',
        'image' => 'Accessory-Dwelling-Units.webp',
    ],
    '/tiny-homes-on-wheels-texas/' => [
        'file' => 'services/tiny-homes-on-wheels', 'type' => 'service', 'crumb' => 'Tiny Homes on Wheels', 'priority' => '0.9',
        'title' => 'Tiny Homes on Wheels Texas | Custom THOW | Cowboy Tiny Homes',
        'desc'  => 'Custom tiny homes on wheels built in Texas on bumper-pull or gooseneck trailers. Road-ready layouts, lofts, off-grid options and RV park placement help.',
        'image' => 'Tiny-Homes-On-Wheels.webp',
    ],
    '/park-model-homes-texas/' => [
        'file' => 'services/park-model-homes', 'type' => 'service', 'crumb' => 'Park Model Homes', 'priority' => '0.9',
        'title' => 'Park Model Homes Texas | Under 400 Sq Ft | Cowboy Tiny Homes',
        'desc'  => 'Park model homes for Texas RV parks, ranches and rural land. Designs around 399 sq ft with full kitchens, porches and lofts. Plan and build with us.',
        'image' => 'Park-Model-Homes.webp',
    ],
    '/tiny-house-design-services/' => [
        'file' => 'services/design-services', 'type' => 'service', 'crumb' => 'Tiny House Design Services', 'priority' => '0.8',
        'title' => 'Tiny House Design Services & Plans | Cowboy Tiny Homes',
        'desc'  => 'Tiny house design services: feasibility study, floor plans, elevations, roof, site and electrical plans, plus 3D renderings. Permit-ready drawings.',
        'image' => 'Cowboy-Tiny-Homes-Home-BG.webp',
    ],
    '/home-remodel-design-texas/' => [
        'file' => 'services/home-remodel', 'type' => 'service', 'crumb' => 'Home Remodel Design', 'priority' => '0.7',
        'title' => 'Home Remodel Design Texas | Kitchens, Baths & More',
        'desc'  => 'Home remodel design in Texas: kitchens, bathrooms, living areas and bedrooms. Cowboy Tiny Homes turns your ideas into detailed, buildable plans.',
        'image' => 'Home-Remodel.webp',
    ],

    // ---- Service areas ----------------------------------------------------
    '/service-areas/' => [
        'file' => 'areas/index', 'type' => 'hub', 'crumb' => 'Service Areas', 'priority' => '0.7',
        'title' => 'Texas Service Areas | Cowboy Tiny Homes',
        'desc'  => 'Cowboy Tiny Homes builds tiny homes, ADUs and park models in San Antonio, Austin, Dallas, Fort Worth, Houston and across Texas. Find your area.',
        'image' => 'og-cowboy-tiny-homes.jpg',
    ],
    '/tiny-home-builders-san-antonio/' => [
        'file' => 'areas/san-antonio', 'type' => 'area', 'crumb' => 'San Antonio', 'parent' => '/service-areas/', 'priority' => '0.8', 'city' => 'San Antonio',
        'title' => 'Tiny Home Builders San Antonio, TX | Cowboy Tiny Homes',
        'desc'  => 'San Antonio tiny home builders for custom tiny houses, backyard casitas, ADUs and park models across Bexar County and the Hill Country. Free consult.',
        'image' => 'Custom-Tiny-Homes.webp',
    ],
    '/tiny-home-builders-austin/' => [
        'file' => 'areas/austin', 'type' => 'area', 'crumb' => 'Austin', 'parent' => '/service-areas/', 'priority' => '0.8', 'city' => 'Austin',
        'title' => 'Tiny Home Builders Austin, TX | ADUs | Cowboy Tiny Homes',
        'desc'  => 'Austin tiny home builders for backyard ADUs, custom tiny houses and tiny homes on wheels. Plans that fit Austin lots and the HOME code changes.',
        'image' => 'Accessory-Dwelling-Units.webp',
    ],
    '/tiny-home-builders-dallas/' => [
        'file' => 'areas/dallas', 'type' => 'area', 'crumb' => 'Dallas', 'parent' => '/service-areas/', 'priority' => '0.8', 'city' => 'Dallas',
        'title' => 'Tiny House Builders Dallas, TX | Cowboy Tiny Homes',
        'desc'  => 'Dallas tiny house builders for custom tiny homes, ADUs, park models and tiny homes on wheels across DFW. Design, permitting help and construction.',
        'image' => 'Tiny-Homes-On-Wheels.webp',
    ],
    '/tiny-home-builders-fort-worth/' => [
        'file' => 'areas/fort-worth', 'type' => 'area', 'crumb' => 'Fort Worth', 'parent' => '/service-areas/', 'priority' => '0.8', 'city' => 'Fort Worth',
        'title' => 'Tiny Home Builders Fort Worth, TX | Cowboy Tiny Homes',
        'desc'  => 'Fort Worth tiny home builders for western-style tiny houses, ranch casitas, ADUs and park models across Tarrant County. Get a free design consult.',
        'image' => 'Park-Model-Homes.webp',
    ],
    '/tiny-home-builders-houston/' => [
        'file' => 'areas/houston', 'type' => 'area', 'crumb' => 'Houston', 'parent' => '/service-areas/', 'priority' => '0.8', 'city' => 'Houston',
        'title' => 'Tiny Home Builders Houston, TX | Cowboy Tiny Homes',
        'desc'  => 'Houston tiny home builders for custom tiny houses, garage apartments, ADUs and park models built for Gulf Coast heat, humidity and wind.',
        'image' => 'Custom-Tiny-Homes.webp',
    ],

    // ---- House designs ----------------------------------------------------
    '/home-designs/' => [
        'file' => 'home-designs', 'type' => 'page', 'crumb' => 'House Designs', 'priority' => '0.8',
        'title' => 'Tiny House Plans & Designs Texas | Cowboy Tiny Homes',
        'desc'  => 'Buy Texas tiny house plans: small homes, ADUs, casitas, park models and tiny homes on wheels. Full plan sets, 3D models and cost estimates. Or have us build it.',
        'image' => '3.webp', 'updated' => '2026-10-30',
    ],
    '/gonzales-modern-living/' => [
        'file' => 'gonzales-modern-living', 'type' => 'plan', 'plan' => 'gonzales-modern-living', 'crumb' => 'Gonzales Modern Living', 'parent' => '/home-designs/', 'priority' => '0.8', 'updated' => '2026-10-30',
        'title' => 'Gonzales Modern Living | 2 Bed Small House Plan',
        'desc'  => 'The Gonzales Modern Living is a two-story, 2-bedroom, 1.5-bath small house plan with a home office, mini bar kitchen and patio. See the layout.',
        'image' => '3.webp',
    ],

    // ---- Tools ------------------------------------------------------------
    '/tools/' => [
        'file' => 'tools/index', 'type' => 'hub', 'crumb' => 'Tools', 'priority' => '0.7',
        'title' => 'Free Tiny Home Calculators & Planning Tools',
        'desc'  => 'Free tiny home planning tools: cost calculator, size planner, loan calculator, ADU rental income calculator and a quiz to find the right home type.',
        'image' => 'og-cowboy-tiny-homes.jpg',
    ],
    '/tools/tiny-home-cost-calculator/' => [
        'file' => 'tools/cost-calculator', 'type' => 'tool', 'crumb' => 'Tiny Home Cost Calculator', 'parent' => '/tools/', 'priority' => '0.8',
        'title' => 'Tiny Home Cost Calculator (Texas 2026 Estimates)',
        'desc'  => 'Estimate what your tiny home will cost to build in Texas. Pick the type, size, finish level and add-ons to see a low-to-high budget range instantly.',
        'image' => 'Custom-Tiny-Homes.webp',
    ],
    '/tools/which-tiny-home-is-right-for-me/' => [
        'file' => 'tools/quiz', 'type' => 'tool', 'crumb' => 'Which Tiny Home Is Right for Me?', 'parent' => '/tools/', 'priority' => '0.7',
        'title' => 'Which Tiny Home Is Right for Me? Free 60-Second Quiz',
        'desc'  => 'Answer six quick questions about land, mobility, budget and how you will use it, and get matched with a tiny home on wheels, park model, ADU or custom home.',
        'image' => 'Tiny-Homes-On-Wheels.webp',
    ],
    '/tools/tiny-house-size-planner/' => [
        'file' => 'tools/size-planner', 'type' => 'tool', 'crumb' => 'Tiny House Size Planner', 'parent' => '/tools/', 'priority' => '0.7',
        'title' => 'Tiny House Size Planner | How Many Square Feet Do I Need?',
        'desc'  => 'Add the rooms you want and see how many square feet your tiny house needs, which home types fit, and a rough budget. Free interactive planner.',
        'image' => '4.webp',
    ],
    '/tools/adu-rental-income-calculator/' => [
        'file' => 'tools/adu-rental-calculator', 'type' => 'tool', 'crumb' => 'ADU Rental Income Calculator', 'parent' => '/tools/', 'priority' => '0.7',
        'title' => 'ADU Rental Income Calculator | Casita ROI & Payback',
        'desc'  => 'See what a backyard ADU or casita could earn. Compare long-term and short-term rental income, expenses, cash flow, ROI and payback period.',
        'image' => 'Accessory-Dwelling-Units.webp',
    ],
    '/tools/tiny-home-loan-calculator/' => [
        'file' => 'tools/loan-calculator', 'type' => 'tool', 'crumb' => 'Tiny Home Loan Calculator', 'parent' => '/tools/', 'priority' => '0.7',
        'title' => 'Tiny Home Loan Calculator | Monthly Payment Estimator',
        'desc'  => 'Estimate your monthly tiny home payment for RV loans, personal loans, HELOCs or mortgages. Adjust price, down payment, rate and term.',
        'image' => 'Park-Model-Homes.webp',
    ],

    // ---- Guides -----------------------------------------------------------
    '/guides/' => [
        'file' => 'guides/index', 'type' => 'hub', 'crumb' => 'Guides', 'priority' => '0.7',
        'title' => 'Texas Tiny Home Guides | Laws, Costs & Planning',
        'desc'  => 'Plain-English guides to tiny house laws in Texas, building costs, financing, ADUs vs park models vs tiny homes on wheels, and choosing a builder.',
        'image' => 'og-cowboy-tiny-homes.jpg',
    ],
    '/guides/tiny-house-laws-texas/' => [
        'file' => 'guides/tiny-house-laws-texas', 'type' => 'guide', 'crumb' => 'Tiny House Laws in Texas', 'parent' => '/guides/', 'priority' => '0.8',
        'title' => 'Tiny House Laws in Texas: Permits, Zoning & Codes (2026)',
        'desc'  => 'Are tiny homes legal in Texas? How building permits, zoning, IRC Appendix Q, RV rules and HOA restrictions apply, plus an interactive permit checklist.',
        'image' => 'Cowboy-Tiny-Homes-Home-BG.webp', 'published' => '2026-10-28',
    ],
    '/guides/cost-to-build-a-tiny-house-in-texas/' => [
        'file' => 'guides/cost-to-build', 'type' => 'guide', 'crumb' => 'Cost to Build a Tiny House in Texas', 'parent' => '/guides/', 'priority' => '0.8',
        'title' => 'How Much Does It Cost to Build a Tiny House in Texas?',
        'desc'  => 'Real 2026 cost ranges for tiny homes on wheels, park models, ADUs and foundation tiny houses in Texas, with a line-by-line budget breakdown.',
        'image' => 'Custom-Tiny-Homes.webp', 'published' => '2026-10-28',
    ],
    '/guides/adu-vs-park-model-vs-tiny-house-on-wheels/' => [
        'file' => 'guides/adu-vs-park-model-vs-thow', 'type' => 'guide', 'crumb' => 'ADU vs Park Model vs Tiny Home on Wheels', 'parent' => '/guides/', 'priority' => '0.7',
        'title' => 'ADU vs Park Model vs Tiny House on Wheels: Which Is Best?',
        'desc'  => 'Compare ADUs, park model homes and tiny houses on wheels on cost, size, permits, financing, mobility and resale, and see which fits your Texas property.',
        'image' => 'Park-Model-Homes.webp', 'published' => '2026-10-28',
    ],
    '/guides/how-to-choose-a-tiny-home-builder-in-texas/' => [
        'file' => 'guides/choose-a-builder', 'type' => 'guide', 'crumb' => 'How to Choose a Tiny Home Builder', 'parent' => '/guides/', 'priority' => '0.7',
        'title' => 'How to Choose the Best Tiny Home Builder in Texas',
        'desc'  => 'What separates the best tiny home builders in Texas: certifications, contracts, warranties, red flags and 15 questions to ask before you sign.',
        'image' => 'Design-and-build-contact.webp', 'published' => '2026-10-28',
    ],
    '/guides/tiny-home-financing-texas/' => [
        'file' => 'guides/financing', 'type' => 'guide', 'crumb' => 'Tiny Home Financing in Texas', 'parent' => '/guides/', 'priority' => '0.7',
        'title' => 'Tiny Home Financing in Texas: 7 Ways to Pay for It',
        'desc'  => 'How to finance a tiny home in Texas: RV loans, personal loans, HELOCs, construction loans, mortgages, builder financing and cash, compared.',
        'image' => '4.webp', 'published' => '2026-10-28',
    ],

    // ---- Blog (type 'post'; 'published' sets the date shown, the schema and the sitemap) --
    '/blog/' => [
        'file' => 'blog/index', 'type' => 'hub', 'crumb' => 'Blog', 'priority' => '0.7', 'updated' => '2026-10-22',
        'title' => 'Tiny Home Blog | Texas Tiny Living Tips | Cowboy Tiny Homes',
        'desc'  => 'Tiny home ideas, design tips and practical advice for Texans: western-style tiny homes, backyard casitas, trailers, staying cool and tiny house communities.',
        'image' => 'blog-western-tiny-homes.webp',
    ],
    '/blog/tiny-house-communities-texas/' => [
        'file' => 'blog/tiny-house-communities-texas', 'type' => 'post', 'crumb' => 'Tiny House Communities in Texas', 'parent' => '/blog/', 'priority' => '0.6',
        'title' => 'Tiny House Communities in Texas: How They Work & What to Ask',
        'desc'  => 'How tiny house communities in Texas work: lot leases vs ownership, rules, utilities, costs and the questions to ask before you move your tiny home in.',
        'image' => 'blog-tiny-house-communities-texas.webp', 'published' => '2026-10-22', 'category' => 'Tiny Living', 'read' => 8,
    ],
    '/blog/tiny-home-design-texas-heat/' => [
        'file' => 'blog/tiny-home-design-texas-heat', 'type' => 'post', 'crumb' => 'Designing a Tiny Home for Texas Heat', 'parent' => '/blog/', 'priority' => '0.6',
        'title' => 'Designing a Tiny Home for Texas Heat: 12 Ways to Stay Cool',
        'desc'  => 'Twelve proven ways to keep a tiny home cool in a Texas summer: orientation, shade, insulation, windows, roofing, mini-splits, ventilation and humidity control.',
        'image' => 'blog-tiny-home-texas-heat.webp', 'published' => '2026-09-17', 'category' => 'Building Smart', 'read' => 9,
    ],
    '/blog/gooseneck-vs-bumper-pull-tiny-house/' => [
        'file' => 'blog/gooseneck-vs-bumper-pull', 'type' => 'post', 'crumb' => 'Gooseneck vs Bumper Pull Tiny House', 'parent' => '/blog/', 'priority' => '0.6',
        'title' => 'Gooseneck vs Bumper Pull Tiny House: Which Trailer Is Best?',
        'desc'  => 'Gooseneck or bumper pull? Compare tiny house trailer types on space, towing, stability, cost and Texas road rules to choose the right base for your THOW.',
        'image' => 'blog-gooseneck-vs-bumper-pull.webp', 'published' => '2026-08-06', 'category' => 'Tiny Homes on Wheels', 'read' => 8,
    ],
    '/blog/backyard-casita-ideas-texas/' => [
        'file' => 'blog/backyard-casita-ideas', 'type' => 'post', 'crumb' => 'Backyard Casita Ideas', 'parent' => '/blog/', 'priority' => '0.6',
        'title' => '9 Backyard Casita Ideas Texans Love (With Planning Tips)',
        'desc'  => 'Nine backyard casita ideas for Texas homes — guest suites, rentals, home offices, pool houses and more — with size, layout and permit tips for each.',
        'image' => 'blog-backyard-casita-ideas.webp', 'published' => '2026-06-25', 'category' => 'ADUs & Casitas', 'read' => 9,
    ],
    '/blog/western-tiny-homes-texas-ranch-style/' => [
        'file' => 'blog/western-tiny-homes', 'type' => 'post', 'crumb' => 'Western Tiny Homes', 'parent' => '/blog/', 'priority' => '0.6',
        'title' => 'Western Tiny Homes: How to Get Texas Ranch Style in a Small House',
        'desc'  => 'Western tiny homes bring ranch style to small living: board-and-batten, metal roofs, deep porches, stone and rustic interiors. Ideas from Cowboy Tiny Homes.',
        'image' => 'blog-western-tiny-homes.webp', 'published' => '2026-05-14', 'category' => 'Design & Style', 'read' => 8,
    ],

    // ---- Company & support pages -----------------------------------------
    '/our-process/' => [
        'file' => 'our-process', 'type' => 'page', 'crumb' => 'Our Process', 'priority' => '0.6',
        'title' => 'Our Design-Build Process | Cowboy Tiny Homes',
        'desc'  => 'How Cowboy Tiny Homes takes a tiny home, ADU or remodel from first call to move-in: feasibility, design, permits, construction and handover.',
        'image' => 'Cowboy-Tiny-Homes-Home-BG.webp',
    ],
    '/faqs/' => [
        'file' => 'faqs', 'type' => 'page', 'crumb' => 'FAQs', 'priority' => '0.7',
        'title' => 'Tiny Home FAQs Texas | Permits, Costs & Land',
        'desc'  => 'Answers to common questions about building a tiny home in Texas: permits, regulations, land, utilities, costs, financing, timelines and design.',
        'image' => 'og-cowboy-tiny-homes.jpg',
    ],
    '/contact-us/' => [
        'file' => 'contact-us', 'type' => 'page', 'crumb' => 'Contact Us', 'priority' => '0.7',
        'title' => 'Contact Cowboy Tiny Homes | Free Design Consultation',
        'desc'  => 'Start your tiny home, ADU or remodel project. Call 210-903-9471 or send your project details for a free design consultation with Cowboy Tiny Homes.',
        'image' => 'Design-and-build-contact.webp',
    ],
    '/write-for-us/' => [
        'file' => 'write-for-us', 'type' => 'page', 'crumb' => 'Write for Us', 'priority' => '0.3',
        'title' => 'Write for Us | Tiny Home Guest Posts | Cowboy Tiny Homes',
        'desc'  => 'Share your tiny home, ADU or small-space design expertise. Guest post guidelines, topic ideas and how to pitch an article to Cowboy Tiny Homes.',
        'image' => 'og-cowboy-tiny-homes.jpg',
    ],
    '/terms-of-sale/' => [
        'file' => 'terms-of-sale', 'type' => 'legal', 'crumb' => 'Terms of Sale', 'priority' => '0.2',
        'title' => 'Terms of Sale for House Plans | Cowboy Tiny Homes',
        'desc'  => 'License, delivery, refunds and build-credit terms for Cowboy Tiny Homes house plans, and the professional review Texas buyers need.',
        'image' => 'og-cowboy-tiny-homes.jpg', 'updated' => '2026-10-30',
    ],
    '/privacy-policy/' => [
        'file' => 'privacy-policy', 'type' => 'legal', 'crumb' => 'Privacy Policy', 'priority' => '0.2',
        'title' => 'Privacy Policy | Cowboy Tiny Homes',
        'desc'  => 'How Cowboy Tiny Homes collects, uses and protects the information you share through cowboytinyhomes.com and our contact forms.',
        'image' => 'og-cowboy-tiny-homes.jpg',
    ],
] + plan_routes() + order_routes());


// Old WordPress URLs => new homes (301). Anything under /wp-* that is not
// listed here falls through to the router's generic rules.
const REDIRECTS = [
    '/category/accessory-structures/'      => '/adu-builders-texas/',
    '/category/dwelling-units/'            => '/adu-builders-texas/',
    '/category/park-models/'               => '/park-model-homes-texas/',
    '/category/single-family-residential/' => '/custom-tiny-homes-texas/',
    '/category/tiny-house-on-wheels/'      => '/tiny-homes-on-wheels-texas/',
    '/category/miscellaneous/'             => '/home-designs/',
    '/category/uncategorized/'             => '/home-designs/',
    '/house-designs/'                      => '/home-designs/',
    '/faq/'                                => '/faqs/',
    '/contact/'                            => '/contact-us/',
    '/about/'                              => '/our-process/',
    '/about-us/'                           => '/our-process/',
    '/feed/'                               => '/blog/',
    '/comments/feed/'                      => '/blog/',
    '/sitemap_index.xml'                   => '/sitemap.xml',
    '/page-sitemap.xml'                    => '/sitemap.xml',
    '/post-sitemap.xml'                    => '/sitemap.xml',
    '/category-sitemap.xml'                => '/sitemap.xml',
    '/wp-sitemap.xml'                      => '/sitemap.xml',
];

/** One route per catalog plan (Gonzales Modern Living keeps its own entry above). */
function plan_routes(): array
{
    global $PLANS;
    $kind = ['single' => 'House Plan', 'adu' => 'ADU Plan', 'park' => 'Park Model Plan', 'thow' => 'Tiny House on Wheels Plan', 'studio' => 'Backyard Studio Plan'];
    $out = [];
    foreach ($PLANS as $slug => $p) {
        if ($p['url'] !== "/home-designs/$slug/") continue;
        $k = $kind[$p['category']];
        $title = $p['name'] . ': ' . number_format($p['sqft']) . ' Sq Ft ' . $k;
        if (strlen($title) <= 44) $title .= ' | Cowboy Tiny Homes';
        $out[$p['url']] = [
            'file' => 'plan', 'type' => 'plan', 'plan' => $slug, 'crumb' => $p['name'], 'parent' => '/home-designs/', 'priority' => '0.8',
            'title' => $title,
            'desc'  => $p['name'] . ': ' . strtolower($p['bed_label']) . ', ' . strtolower($p['bath_label']) . ', ' . number_format($p['sqft']) . ' sq ft ' . strtolower($k)
                     . ' for Texas. Plan set with CAD, 3D model and cost estimate, $' . number_format($p['price']) . '. Or have us build it.',
            'image' => "/assets/plans/$slug/3d.webp", 'updated' => '2026-10-30',
        ];
    }
    return $out;
}

/** Store pages: never indexed or listed in the sitemap. */
function order_routes(): array
{
    $r = fn($file, $crumb, $title) => ['file' => "order/$file", 'type' => 'page', 'crumb' => $crumb, 'parent' => '/home-designs/', 'priority' => '0',
        'noindex' => true, 'title' => $title . ' | ' . SITE_NAME, 'desc' => 'Cowboy Tiny Homes plan store.', 'image' => 'og-cowboy-tiny-homes.jpg'];
    return [
        '/order/checkout/' => $r('checkout', 'Checkout', 'Checkout'),
        '/order/complete/' => $r('complete', 'Your Plan Files', 'Your Plan Files'),
        '/order/download/' => $r('download', 'Download', 'Download'),
        '/order/lookup/'   => $r('lookup', 'Find My Plan Download', 'Find My Plan Download'),
        '/order/webhook/'  => $r('webhook', 'Webhook', 'Webhook'),
    ];
}
