<?php
// Tiny Homes Blueprint - site data: business details, navigation, plans and the route registry.
// Every public URL is listed in $ROUTES; the router, sitemap.xml, the HTML sitemap and
// the hub pages (styles, tools, guides) all read from it, so a page added here shows up everywhere.

const SITE_NAME   = 'Tiny Homes Blueprint';
const SITE_URL    = 'https://tinyhomesblueprint.com';
const SITE_TAG    = 'Tiny House Plans & Blueprints';
const SITE_PHONE  = '210-903-9471';
const SITE_TEL    = '+12109039471';
const SITE_EMAIL  = 'contact@tinyhomesblueprint.com';
const ASSET_VER   = '20261025';

// Primary navigation. Each entry: label => path, or label => [path, children].
$NAV = [
    'House Plans' => ['/tiny-house-plans/', [
        'All Tiny House Plans'      => '/tiny-house-plans/',
        'A-Frame House Plans'       => '/a-frame-house-plans/',
        'Shipping Container Homes'  => '/shipping-container-home-plans/',
        'Tiny Cottage Plans'        => '/tiny-cottage-plans/',
        'Small Cabin Plans'         => '/small-cabin-plans/',
        'Tiny House on Wheels'      => '/tiny-house-on-wheels-plans/',
        'Plans With a Loft'         => '/tiny-house-plans-with-loft/',
        'Shed to Tiny House'        => '/shed-to-tiny-house/',
        'Small Farmhouse Plans'     => '/small-farmhouse-plans/',
        'ADU Plans'                 => '/adu-plans/',
    ]],
    'Free Tools' => ['/tools/', [
        'All Planning Tools'        => '/tools/',
        'Tiny House Cost Calculator'=> '/tools/tiny-house-cost-calculator/',
        'Layout Planner'            => '/tools/tiny-house-layout-planner/',
        'Size Calculator'           => '/tools/how-big-should-my-tiny-house-be/',
        'Trailer Weight Calculator' => '/tools/tiny-house-trailer-weight-calculator/',
        'Off-Grid Solar Calculator' => '/tools/off-grid-solar-calculator/',
        'Style Quiz'                => '/tools/tiny-house-style-quiz/',
    ]],
    'Guides'  => '/blog/',
    'About'   => '/about/',
    'Contact' => '/contact/',
];

// Plans for sale. Specs are as published on the original store.
$PLANS = [
    'plan-12-2418' => [
        'name'   => 'Plan 12-2418',
        'title'  => 'Rustic 3-Bedroom Tiny House Plan with Covered Porch',
        'price'  => 550,
        'beds'   => 3, 'baths' => 2, 'floors' => 2,
        'sqft'   => 700, 'width' => "20'", 'depth' => "38'", 'height' => "14' 4\"", 'ceiling' => "9'",
        'roof'   => '4:12 pitch, truss framing, shingle roof',
        'walls'  => '2x6 wood framing, siding and stone exterior',
        'features' => ['Covered front porch', 'Open living, kitchen and dining', 'Flex room with retractable wall (dining, office or guest room)', 'Main-floor laundry', 'Private bedroom wing', 'Can be flipped to put the porch at the rear'],
        'styles' => ['small-cabin-plans', 'tiny-cottage-plans', 'adu-plans', 'small-farmhouse-plans'],
        'image'  => '/assets/img/plan-12-2418.webp',
    ],
    'plan-12-2417' => [
        'name'   => 'Plan 12-2417',
        'title'  => 'Single-Level 2-Bedroom Tiny Cabin Plan',
        'price'  => 1050,
        'beds'   => 2, 'baths' => 1, 'floors' => 1,
        'sqft'   => 700, 'width' => "20'", 'depth' => "38'", 'height' => "14' 4\"", 'ceiling' => "9'",
        'roof'   => '4:12 pitch, truss framing, shingle roof',
        'walls'  => '2x6 wood framing, siding and stone exterior',
        'features' => ['Everything on one floor, no stairs', 'Side entry into an open great room', 'Kitchen sized for a table or island', 'Flex room with retractable wall', 'Full shower bath', 'Main-floor laundry'],
        'styles' => ['small-cabin-plans', 'tiny-cottage-plans', 'adu-plans'],
        'image'  => '/assets/img/plan-12-2417.webp',
    ],
];

// Route registry. type: home|catalog|plan|style|tool|guide|company|legal|hub
// file is relative to /pages. 'nav' is the short label used on hub cards.
$ROUTES = [
    '/' => ['file' => 'home.php', 'type' => 'home', 'priority' => '1.0',
        'title' => 'Tiny House Plans & Blueprints | Tiny Homes Blueprint',
        'description' => 'Tiny Homes Blueprint sells build-ready tiny house plans and blueprints, plus free cost, layout, size and solar calculators to plan your small home with confidence.'],

    '/tiny-house-plans/' => ['file' => 'catalog.php', 'type' => 'catalog', 'priority' => '0.9',
        'title' => 'Tiny House Floor Plans: Browse Build-Ready Blueprints',
        'description' => 'Browse tiny house floor plans with full specs: square footage, bedrooms, dimensions and what is in each plan set. Filter by style, beds and floors.'],

    // Style landing pages
    '/a-frame-house-plans/' => ['file' => 'styles/a-frame-house-plans.php', 'type' => 'style', 'nav' => 'A-Frame House Plans', 'icon' => 'aframe',
        'title' => 'A-Frame House Plans: Tiny A-Frame Cabin Designs & Costs',
        'description' => 'A-frame house plans for tiny cabins and getaways: sizes, build costs, roof pitch, loft layouts and the pros and cons of building an A-frame.'],
    '/shipping-container-home-plans/' => ['file' => 'styles/shipping-container-home-plans.php', 'type' => 'style', 'nav' => 'Shipping Container Homes', 'icon' => 'container',
        'title' => 'Shipping Container Home Plans: 20ft & 40ft Layouts',
        'description' => 'Shipping container home plans and layouts for 20ft and 40ft boxes, with real costs, insulation and permit advice, and how to plan a container build.'],
    '/tiny-cottage-plans/' => ['file' => 'styles/tiny-cottage-plans.php', 'type' => 'style', 'nav' => 'Tiny Cottage Plans', 'icon' => 'cottage',
        'title' => 'Tiny Cottage Plans: Small Cottage House Designs',
        'description' => 'Tiny cottage plans with porches, gables and cozy layouts under 800 sq ft. See floor plan ideas, costs and the plans available to buy.'],
    '/small-cabin-plans/' => ['file' => 'styles/small-cabin-plans.php', 'type' => 'style', 'nav' => 'Small Cabin Plans', 'icon' => 'cabin',
        'title' => 'Small Cabin Plans: Rustic Tiny Cabin Blueprints',
        'description' => 'Small cabin plans for weekend retreats and full-time living: rustic layouts, sizes from 200 to 800 sq ft, build costs and foundation options.'],
    '/tiny-house-on-wheels-plans/' => ['file' => 'styles/tiny-house-on-wheels-plans.php', 'type' => 'style', 'nav' => 'Tiny House on Wheels', 'icon' => 'wheels',
        'title' => 'Tiny House on Wheels Plans: Mobile Tiny Home Designs',
        'description' => 'Tiny house on wheels plans built around road limits: 8.5 ft width, 13.5 ft height, trailer weight and the layouts that work on a mobile tiny home.'],
    '/tiny-house-plans-with-loft/' => ['file' => 'styles/tiny-house-plans-with-loft.php', 'type' => 'style', 'nav' => 'Tiny House Plans With Loft', 'icon' => 'loft',
        'title' => 'Tiny House Plans With Loft: Sleeping Loft Layouts',
        'description' => 'Tiny house plans with a loft: headroom rules, stairs vs ladders, egress windows and layout ideas that double your usable floor space.'],
    '/shed-to-tiny-house/' => ['file' => 'styles/shed-to-tiny-house.php', 'type' => 'style', 'nav' => 'Shed to Tiny House', 'icon' => 'shed',
        'title' => 'Shed to Tiny House Conversion: Plans, Costs & Steps',
        'description' => 'How to turn a shed into a tiny house: choosing the right shed, insulation, plumbing, permits, costs and conversion floor plan ideas.'],
    '/small-farmhouse-plans/' => ['file' => 'styles/small-farmhouse-plans.php', 'type' => 'style', 'nav' => 'Small Farmhouse Plans', 'icon' => 'farm',
        'title' => 'Small Farmhouse Plans: Tiny Modern Farmhouse Designs',
        'description' => 'Small farmhouse plans with porches, board-and-batten and practical mudrooms. Tiny modern farmhouse layouts for homesteads and small farms.'],
    '/adu-plans/' => ['file' => 'styles/adu-plans.php', 'type' => 'style', 'nav' => 'ADU Plans', 'icon' => 'adu',
        'title' => 'ADU Plans: Backyard Cottage & Granny Flat Designs',
        'description' => 'ADU plans for backyard cottages, granny flats and rental units: size limits, setbacks, costs, rental return and layouts that pass permit review.'],

    // Tools
    '/tools/' => ['file' => 'tools/index.php', 'type' => 'hub', 'priority' => '0.9',
        'title' => 'Free Tiny House Planning Tools & Calculators',
        'description' => 'Free tiny house calculators from Tiny Homes Blueprint: build cost, layout planner, size calculator, trailer weight, off-grid solar and a style quiz.'],
    '/tools/tiny-house-cost-calculator/' => ['file' => 'tools/tiny-house-cost-calculator.php', 'type' => 'tool', 'nav' => 'Tiny House Cost Calculator', 'icon' => 'cost',
        'title' => 'Tiny House Cost Calculator: Estimate Your Build Cost',
        'description' => 'How much does a tiny house cost? Use this free calculator to estimate your build by size, foundation, finish level, utilities and DIY vs builder labor.'],
    '/tools/tiny-house-layout-planner/' => ['file' => 'tools/tiny-house-layout-planner.php', 'type' => 'tool', 'nav' => 'Tiny House Layout Planner', 'icon' => 'layout',
        'title' => 'Tiny House Layout Planner: Design Your Floor Plan Free',
        'description' => 'Sketch a tiny house layout in your browser. Drag rooms and furniture onto a scaled grid, check square footage and save your floor plan as an image.'],
    '/tools/how-big-should-my-tiny-house-be/' => ['file' => 'tools/how-big-should-my-tiny-house-be.php', 'type' => 'tool', 'nav' => 'Tiny House Size Calculator', 'icon' => 'size',
        'title' => 'How Big Should My Tiny House Be? Square Footage Calculator',
        'description' => 'Find the right tiny house square footage for your household, work and storage needs, then compare it to trailer, cottage and ADU sizes.'],
    '/tools/tiny-house-trailer-weight-calculator/' => ['file' => 'tools/tiny-house-trailer-weight-calculator.php', 'type' => 'tool', 'nav' => 'Trailer Weight Calculator', 'icon' => 'weight',
        'title' => 'Tiny House Trailer Weight Calculator (GVWR Check)',
        'description' => 'Estimate the weight of a tiny house on wheels by length, framing, siding and contents, and check it against trailer GVWR and towing limits.'],
    '/tools/off-grid-solar-calculator/' => ['file' => 'tools/off-grid-solar-calculator.php', 'type' => 'tool', 'nav' => 'Off-Grid Solar Calculator', 'icon' => 'solar',
        'title' => 'Off-Grid Solar Calculator for Tiny Houses',
        'description' => 'Size an off-grid solar system for a tiny house: add your appliances, pick your sun hours and get panel wattage, battery bank and inverter size.'],
    '/tools/tiny-house-style-quiz/' => ['file' => 'tools/tiny-house-style-quiz.php', 'type' => 'tool', 'nav' => 'Tiny House Style Quiz', 'icon' => 'quiz',
        'title' => 'Tiny House Style Quiz: Which Tiny Home Fits You?',
        'description' => 'Answer eight quick questions and find the tiny house style that fits your budget, land and lifestyle: A-frame, cabin, container, THOW, cottage or ADU.'],

    // Guides
    '/blog/' => ['file' => 'guides/index.php', 'type' => 'hub', 'priority' => '0.8',
        'title' => 'Tiny House Guides: Costs, Building, Zoning & Layouts',
        'description' => 'In-depth tiny house guides from Tiny Homes Blueprint on cost, how to build, zoning laws, layout ideas, trailers, kits and free plans.'],
    '/blog/how-much-does-a-tiny-house-cost/' => ['file' => 'guides/how-much-does-a-tiny-house-cost.php', 'type' => 'guide', 'date' => '2026-10-25', 'nav' => 'How Much Does a Tiny House Cost?',
        'title' => 'How Much Does a Tiny House Cost in 2026? Full Breakdown',
        'description' => 'How much does a tiny house cost? A line-by-line 2026 breakdown of DIY, shell and builder prices, land, utilities and hidden costs, with a free calculator.'],
    '/blog/how-to-build-a-tiny-house/' => ['file' => 'guides/how-to-build-a-tiny-house.php', 'type' => 'guide', 'date' => '2026-10-25', 'nav' => 'How to Build a Tiny House',
        'title' => 'How to Build a Tiny House: 12-Step Guide for Beginners',
        'description' => 'How to build a tiny house step by step, from plans and permits to framing, utilities and finishes, with timelines, tools and mistakes to avoid.'],
    '/blog/tiny-house-zoning-laws/' => ['file' => 'guides/tiny-house-zoning-laws.php', 'type' => 'guide', 'date' => '2026-10-25', 'nav' => 'Tiny House Zoning Laws',
        'title' => 'Tiny House Zoning Laws: Where Can You Legally Live?',
        'description' => 'Tiny house zoning explained: minimum dwelling size, IRC Appendix AQ, RV vs ADU rules, and how to check what your county allows before you build.'],
    '/blog/free-tiny-house-plans/' => ['file' => 'guides/free-tiny-house-plans.php', 'type' => 'guide', 'date' => '2026-10-25', 'nav' => 'Free Tiny House Plans vs Paid',
        'title' => 'Free Tiny House Plans: What You Get vs Paid Blueprints',
        'description' => 'Are free tiny house plans good enough to build from? What free plans leave out, what a full blueprint set includes, and when paying for plans saves money.'],
    '/blog/tiny-house-kits-vs-plans/' => ['file' => 'guides/tiny-house-kits-vs-plans.php', 'type' => 'guide', 'date' => '2026-10-25', 'nav' => 'Tiny House Kits vs Plans',
        'title' => 'Tiny House Kits vs Plans: Which Is Cheaper to Build?',
        'description' => 'Tiny house kits vs plans compared on cost, build time, customization and permits, so you can pick the right path for your tiny home build.'],
    '/blog/tiny-house-layout-ideas/' => ['file' => 'guides/tiny-house-layout-ideas.php', 'type' => 'guide', 'date' => '2026-10-25', 'nav' => 'Tiny House Layout Ideas',
        'title' => '15 Tiny House Layout Ideas That Make Small Spaces Work',
        'description' => 'Tiny house layout ideas with floor plan diagrams: galley kitchens, loft placement, flex rooms, storage stairs and bathroom layouts that save space.'],
    '/blog/tiny-house-trailer-size-guide/' => ['file' => 'guides/tiny-house-trailer-size-guide.php', 'type' => 'guide', 'date' => '2026-10-25', 'nav' => 'Tiny House Trailer Size Guide',
        'title' => 'Tiny House Trailer Sizes: Length, Width, Height & Weight',
        'description' => 'Tiny house trailer sizes explained: legal width and height, common lengths from 16 to 32 ft, GVWR ratings and how to choose the right trailer.'],
    '/embracing-tiny-homes-unlocking-the-advantages-of-compact-living/' => ['file' => 'guides/compact-living.php', 'type' => 'guide', 'date' => '2023-07-10', 'modified' => '2026-10-25', 'nav' => 'The Advantages of Compact Living',
        'title' => 'Compact Living: 9 Real Advantages of Living in a Tiny Home',
        'description' => 'The advantages of compact living, backed by real numbers: lower costs, less upkeep, smaller footprint and more freedom, plus the trade-offs to weigh.'],

    // Company and legal
    '/about/' => ['file' => 'company/about.php', 'type' => 'company',
        'title' => 'About Tiny Homes Blueprint',
        'description' => 'Tiny Homes Blueprint designs build-ready tiny house plans and free planning tools for owner-builders, families and small-home investors.'],
    '/contact/' => ['file' => 'company/contact.php', 'type' => 'company',
        'title' => 'Contact Tiny Homes Blueprint | Order a Plan or Ask a Question',
        'description' => 'Contact Tiny Homes Blueprint to order a tiny house plan, request a modification or ask about your project. Call 210-903-9471.'],
    '/write-for-us/' => ['file' => 'company/write-for-us.php', 'type' => 'company',
        'title' => 'Write for Us: Tiny House Guest Posts | Tiny Homes Blueprint',
        'description' => 'Pitch a guest post to Tiny Homes Blueprint. We publish practical articles on tiny house design, building, budgets, off-grid living and zoning.'],
    '/privacy-policy/' => ['file' => 'company/privacy-policy.php', 'type' => 'legal', 'priority' => '0.2',
        'title' => 'Privacy Policy | Tiny Homes Blueprint',
        'description' => 'How Tiny Homes Blueprint collects, uses and protects the information you share on this website.'],
    '/terms-conditions/' => ['file' => 'company/terms-conditions.php', 'type' => 'legal', 'priority' => '0.2',
        'title' => 'Terms & Conditions | Tiny Homes Blueprint',
        'description' => 'Terms and conditions for using Tiny Homes Blueprint and purchasing tiny house plans, including plan licensing and refunds.'],
    '/sitemap/' => ['file' => 'company/sitemap.php', 'type' => 'legal', 'priority' => '0.3',
        'title' => 'Sitemap | Tiny Homes Blueprint',
        'description' => 'Every page on Tiny Homes Blueprint: tiny house plans, style guides, free calculators and articles.'],
];

// Plan detail routes are generated from $PLANS.
foreach ($PLANS as $slug => $p) {
    $ROUTES["/plans/$slug/"] = ['file' => 'plan.php', 'type' => 'plan', 'plan' => $slug, 'priority' => '0.8',
        'title' => $p['name'] . ': ' . $p['title'],
        'description' => sprintf('%s is a %s sq ft, %d-bed, %d-bath tiny house plan (%s x %s). See specs, features and what is in the plan set from Tiny Homes Blueprint.',
            $p['name'], number_format($p['sqft']), $p['beds'], $p['baths'], $p['width'], $p['depth'])];
}

// Permanent redirects from the old WordPress/WooCommerce URLs.
$REDIRECTS = [
    '/shop/'                                => '/tiny-house-plans/',
    '/plan-category/styles/'                => '/tiny-house-plans/',
    '/plan-category/styles/a-frame/'        => '/a-frame-house-plans/',
    '/plan-category/styles/container-homes/'=> '/shipping-container-home-plans/',
    '/plan-category/styles/cottages/'       => '/tiny-cottage-plans/',
    '/plan-category/styles/mobile-tiny-homes/' => '/tiny-house-on-wheels-plans/',
    '/plan-category/styles/shed-remodels/'  => '/shed-to-tiny-house/',
    '/plan-category/styles/small-farm/'     => '/small-farmhouse-plans/',
    '/cart/'                                => '/tiny-house-plans/',
    '/checkout/'                            => '/contact/',
    '/my-account/'                          => '/contact/',
    '/login/'                               => '/contact/',
    '/feed/'                                => '/blog/',
    '/comments/feed/'                       => '/blog/',
    '/blog/feed/'                           => '/blog/',
    '/category/blog/'                       => '/blog/',
    '/author/tiny-homes-blueprint/'         => '/about/',
    '/terms-and-conditions/'                => '/terms-conditions/',
    '/sitemap_index.xml'                    => '/sitemap.xml',
    '/wp-sitemap.xml'                       => '/sitemap.xml',
    '/post-sitemap.xml'                     => '/sitemap.xml',
    '/page-sitemap.xml'                     => '/sitemap.xml',
    '/product-sitemap.xml'                  => '/sitemap.xml',
    '/product_cat-sitemap.xml'              => '/sitemap.xml',
];
