<?php
// Every public URL on the site, in one place. The router, the blog index, the
// HTML sitemap, the XML sitemaps and the RSS feed all read from this list.
//
// type: home | page | service | area | tool | post | legal
// file: the content file under pages/ or posts/ (relative to the site root)
// title: the <title>; h1 defaults to title when omitted
// date/modified: YYYY-MM-DD (posts show these; sitemaps use modified)
defined('LLT') or die(http_response_code(404));

const BUILD_DATE = '2026-10-06';

$PAGES = [
    '/' => [
        'file' => 'pages/home.php', 'type' => 'home',
        'title' => 'Landscape Lighting Texas | Outdoor Lighting Design & Installation',
        'description' => 'Landscape Lighting Texas designs and installs custom LED outdoor lighting for homes and businesses statewide. Free dusk consultation, 5-year warranty.',
        'image' => 'architectural-uplighting',
    ],

    // ----- Company -----
    '/about-us/' => [
        'file' => 'pages/about-us.php', 'type' => 'page',
        'title' => 'About Landscape Lighting Texas | Our Story, Team & Values',
        'h1' => 'We Help Texas Properties Shine After Dark',
        'description' => 'Meet Landscape Lighting Texas: 1,400+ outdoor lighting projects, a design-first process, professional-grade LED systems and a 5-year workmanship warranty.',
        'image' => 'landscape-lighting-texas-home',
    ],
    '/quote/' => [
        'file' => 'pages/quote.php', 'type' => 'page',
        'title' => 'Get a Free Landscape Lighting Quote | Landscape Lighting Texas',
        'h1' => 'Get Your Free Lighting Quote',
        'description' => 'Request a free, no-obligation landscape lighting quote anywhere in Texas. Tell us about your property and a lighting designer replies within one business day.',
        'image' => 'garden-pathway-lighting',
    ],
    '/gallery/' => [
        'file' => 'pages/gallery.php', 'type' => 'page',
        'title' => 'Landscape Lighting Gallery | Texas Outdoor Lighting Ideas',
        'h1' => 'Texas Properties, Transformed After Dark',
        'description' => 'Browse landscape lighting work and ideas from across Texas: architectural uplighting, live oak moonlighting, pools, pathways, driveways and patios.',
        'image' => 'oak-tree-uplighting',
    ],
    '/faq/' => [
        'file' => 'pages/faq.php', 'type' => 'page',
        'title' => 'Landscape Lighting FAQ | Costs, LEDs, Installation & Warranty',
        'h1' => 'Landscape Lighting Questions, Answered',
        'description' => 'Answers to the questions Texas homeowners ask most about landscape lighting: cost, LED efficiency, installation day, wiring, HOAs, warranties and maintenance.',
        'image' => 'driveway-lighting',
    ],

    // ----- Services -----
    '/services/' => [
        'file' => 'pages/services.php', 'type' => 'page',
        'title' => 'Landscape Lighting Services in Texas | Design, Install & Repair',
        'h1' => 'Outdoor Lighting Services for Every Texas Property',
        'description' => 'Architectural uplighting, tree and garden lighting, pathways, pools, patios, smart controls, security lighting and maintenance — designed and installed across Texas.',
        'image' => 'architectural-uplighting',
    ],
    '/services/architectural-uplighting/' => [
        'file' => 'pages/services/architectural-uplighting.php', 'type' => 'service',
        'title' => 'Architectural Uplighting in Texas | Facade & Home Lighting',
        'h1' => 'Architectural Uplighting',
        'description' => 'Architectural uplighting for Texas homes: grazed limestone, lit columns and entries, balanced facades and low-glare LED fixtures aimed on-site after dark.',
        'image' => 'architectural-uplighting',
    ],
    '/services/garden-tree-lighting/' => [
        'file' => 'pages/services/garden-tree-lighting.php', 'type' => 'service',
        'title' => 'Tree & Garden Lighting in Texas | Live Oak Uplighting',
        'h1' => 'Garden & Tree Lighting',
        'description' => 'Tree and garden lighting for Texas landscapes: live oak uplighting and moonlighting, specimen plants, beds and hardscape accents with warm, efficient LEDs.',
        'image' => 'oak-tree-uplighting',
    ],
    '/services/pathway-driveway-lighting/' => [
        'file' => 'pages/services/pathway-driveway-lighting.php', 'type' => 'service',
        'title' => 'Pathway & Driveway Lighting in Texas | Path Lights & Bollards',
        'h1' => 'Pathway & Driveway Lighting',
        'description' => 'Pathway and driveway lighting for Texas homes: path lights, bollards and in-grade fixtures spaced for safe, even, glare-free navigation from curb to door.',
        'image' => 'driveway-lighting',
    ],
    '/services/pool-water-feature-lighting/' => [
        'file' => 'pages/services/pool-water-feature-lighting.php', 'type' => 'service',
        'title' => 'Pool & Water Feature Lighting in Texas | Fountain & Pond Lights',
        'h1' => 'Pool & Water Feature Lighting',
        'description' => 'Pool and water feature lighting for Texas backyards: surrounding landscape light, fountain and pond fixtures, and layered scenes that feel like a resort.',
        'image' => 'pool-lighting',
    ],
    '/services/patio-outdoor-living-lighting/' => [
        'file' => 'pages/services/patio-outdoor-living-lighting.php', 'type' => 'service',
        'title' => 'Patio & Outdoor Living Lighting in Texas | Pergolas, Kitchens',
        'h1' => 'Patio & Outdoor Living Lighting',
        'description' => 'Patio and outdoor living lighting for Texas homes: string lights, step and deck lights, pergola and kitchen downlights layered for long evenings outside.',
        'image' => 'patio-lighting',
    ],
    '/services/smart-lighting-systems/' => [
        'file' => 'pages/services/smart-lighting-systems.php', 'type' => 'service',
        'title' => 'Smart Landscape Lighting Systems in Texas | App & Zone Control',
        'h1' => 'Smart Lighting Systems',
        'description' => 'Smart landscape lighting for Texas homes: app control, zoning, astronomical timers, dimming, color scenes and integration with your smart home.',
        'image' => 'garden-pathway-lighting',
    ],
    '/services/security-lighting/' => [
        'file' => 'pages/services/security-lighting.php', 'type' => 'service',
        'title' => 'Security Lighting & Floodlights in Texas | Homes & Businesses',
        'h1' => 'Security & Floodlighting',
        'description' => 'Security lighting for Texas homes and businesses: shielded floodlights, motion zones and well-lit entries that improve visibility without harsh glare.',
        'image' => 'landscape-lighting-texas-home',
    ],
    '/services/landscape-lighting-maintenance/' => [
        'file' => 'pages/services/landscape-lighting-maintenance.php', 'type' => 'service',
        'title' => 'Landscape Lighting Repair & Maintenance in Texas | LED Retrofits',
        'h1' => 'Landscape Lighting Maintenance & Repair',
        'description' => 'Landscape lighting repair and maintenance in Texas: troubleshooting, re-aiming, transformer and wire repair, LED retrofits and annual tune-ups for any brand.',
        'image' => 'garden-pathway-lighting',
    ],

    // ----- Areas -----
    '/areas/' => [
        'file' => 'pages/areas.php', 'type' => 'page',
        'title' => 'Service Areas | Landscape Lighting Across Texas',
        'h1' => 'Professional Outdoor Lighting, Wherever You Call Home in Texas',
        'description' => 'Landscape Lighting Texas serves Austin, Houston, Dallas–Fort Worth, San Antonio, West Texas and the Gulf Coast. Find your city and request a free quote.',
        'image' => 'oak-tree-uplighting',
    ],
    '/areas/austin/' => [
        'file' => 'pages/areas/austin.php', 'type' => 'area',
        'title' => 'Austin Landscape Lighting | Round Rock, Cedar Park & Hill Country',
        'h1' => 'Austin Landscape Lighting',
        'description' => 'Custom landscape lighting in Austin and Central Texas: limestone facades, live oaks, Hill Country views and dark-sky-friendly designs. Free dusk consultation.',
        'image' => 'oak-tree-uplighting',
    ],
    '/areas/houston/' => [
        'file' => 'pages/areas/houston.php', 'type' => 'area',
        'title' => 'Houston Landscape Lighting | Katy, Sugar Land & The Woodlands',
        'h1' => 'Houston Landscape Lighting',
        'description' => 'Landscape lighting in Houston built for humidity, storms and lush yards: pools, patios, oaks and pines across Katy, Sugar Land, Cypress and The Woodlands.',
        'image' => 'pool-lighting',
    ],
    '/areas/dallas-fort-worth/' => [
        'file' => 'pages/areas/dallas-fort-worth.php', 'type' => 'area',
        'title' => 'Dallas–Fort Worth Landscape Lighting | Plano, Frisco & Southlake',
        'h1' => 'Dallas–Fort Worth Landscape Lighting',
        'description' => 'Landscape lighting across Dallas–Fort Worth: estate facades, driveways, pools and smart LED systems in Plano, Frisco, McKinney, Southlake and beyond.',
        'image' => 'architectural-uplighting',
    ],
    '/areas/san-antonio/' => [
        'file' => 'pages/areas/san-antonio.php', 'type' => 'area',
        'title' => 'San Antonio Landscape Lighting | Boerne, New Braunfels & Schertz',
        'h1' => 'San Antonio Landscape Lighting',
        'description' => 'San Antonio landscape lighting for historic homes, Hill Country estates, patios and pools across Boerne, New Braunfels, Alamo Heights and Schertz.',
        'image' => 'patio-lighting',
    ],
    '/areas/west-texas/' => [
        'file' => 'pages/areas/west-texas.php', 'type' => 'area',
        'title' => 'West Texas Landscape Lighting | El Paso, Midland, Lubbock',
        'h1' => 'West Texas Landscape Lighting',
        'description' => 'Outdoor lighting for West Texas and the Panhandle: wind- and dust-tough fixtures, desert landscapes and big properties in El Paso, Midland, Lubbock and Amarillo.',
        'image' => 'driveway-lighting',
    ],
    '/areas/gulf-coast/' => [
        'file' => 'pages/areas/gulf-coast.php', 'type' => 'area',
        'title' => 'Gulf Coast Landscape Lighting | Corpus Christi, Galveston & RGV',
        'h1' => 'Coastal Texas Landscape Lighting',
        'description' => 'Coastal landscape lighting for Corpus Christi, Galveston and the Rio Grande Valley: salt-resistant brass and copper fixtures, palms, pools and wind-ready installs.',
        'image' => 'pool-lighting',
    ],

    // ----- Tools -----
    '/tools/' => [
        'file' => 'pages/tools.php', 'type' => 'page',
        'title' => 'Free Landscape Lighting Tools & Calculators | Landscape Lighting Texas',
        'h1' => 'Landscape Lighting Tools & Calculators',
        'description' => 'Free landscape lighting tools: cost calculator, design simulator, color temperature visualizer, transformer and voltage drop, beam spread, dusk timer and more.',
        'image' => 'garden-pathway-lighting',
    ],
    '/tools/lighting-design-simulator/' => [
        'file' => 'pages/tools/lighting-design-simulator.php', 'type' => 'tool',
        'title' => 'Landscape Lighting Design Simulator | Try Zones & Scenes',
        'h1' => 'Landscape Lighting Design Simulator',
        'description' => 'Switch uplights, path lights, tree lights and the patio on and off on a Texas home, dim each zone, change color temperature and try smart scenes.',
        'image' => 'architectural-uplighting',
    ],
    '/tools/color-temperature-visualizer/' => [
        'file' => 'pages/tools/color-temperature-visualizer.php', 'type' => 'tool',
        'title' => 'Landscape Lighting Color Temperature Visualizer (2200K–5000K)',
        'h1' => 'Color Temperature Visualizer',
        'description' => 'See how 2200K, 2700K, 3000K, 4000K and 5000K landscape lighting changes a Texas home at night, with recommendations for stone, brick, trees and water.',
        'image' => 'architectural-uplighting',
    ],
    '/tools/transformer-calculator/' => [
        'file' => 'pages/tools/transformer-calculator.php', 'type' => 'tool',
        'title' => 'Landscape Lighting Transformer & Voltage Drop Calculator',
        'h1' => 'Transformer Size & Voltage Drop Calculator',
        'description' => 'Size a low-voltage landscape lighting transformer and check voltage drop for 16, 14, 12 and 10 gauge cable, with the tap setting to use.',
        'image' => 'garden-pathway-lighting',
    ],
    '/tools/beam-spread-calculator/' => [
        'file' => 'pages/tools/beam-spread-calculator.php', 'type' => 'tool',
        'title' => 'Landscape Lighting Beam Spread Calculator | Beam Angle Tool',
        'h1' => 'Beam Spread Calculator',
        'description' => 'Calculate how wide a landscape light beam will be at any height or distance, and find the right beam angle for trees, columns, walls and signs.',
        'image' => 'oak-tree-uplighting',
    ],
    '/tools/dusk-timer/' => [
        'file' => 'pages/tools/dusk-timer.php', 'type' => 'tool',
        'title' => 'Texas Dusk Timer | Sunset Times for Outdoor Lighting Schedules',
        'h1' => 'Texas Dusk Timer',
        'description' => 'Sunset and civil dusk times for Texas cities by date, plus month-by-month timer settings for your landscape lighting transformer.',
        'image' => 'driveway-lighting',
    ],
    '/tools/energy-savings-calculator/' => [
        'file' => 'pages/tools/energy-savings-calculator.php', 'type' => 'tool',
        'title' => 'LED vs Halogen Landscape Lighting Energy Savings Calculator',
        'h1' => 'LED Energy Savings Calculator',
        'description' => 'Compare the yearly running cost of halogen and LED landscape lighting at Texas electricity rates and see your savings and payback period.',
        'image' => 'patio-lighting',
    ],
    '/tools/lighting-style-quiz/' => [
        'file' => 'pages/tools/lighting-style-quiz.php', 'type' => 'tool',
        'title' => 'Landscape Lighting Style Quiz | Find Your Lighting Plan',
        'h1' => 'Which Lighting Style Fits Your Home?',
        'description' => 'Answer six quick questions about your home and yard and get a landscape lighting plan matched to your style, priorities and budget.',
        'image' => 'pool-lighting',
    ],

    // ----- Blog -----
    '/blog/' => [
        'file' => 'pages/blog.php', 'type' => 'page',
        'title' => 'Landscape Lighting Blog | Guides & Ideas for Texas Homes',
        'h1' => 'Landscape Lighting Articles',
        'description' => 'Landscape lighting guides, design ideas, cost breakdowns and how-tos for Texas homeowners from the Landscape Lighting Texas design team.',
        'image' => 'landscape-lighting-texas-home',
    ],
    '/category/general/' => [
        'file' => 'pages/blog.php', 'type' => 'page', 'category' => 'general',
        'title' => 'General Articles | Landscape Lighting Texas Blog',
        'h1' => 'General',
        'description' => 'All general landscape lighting articles from Landscape Lighting Texas: guides, cost calculators, design ideas and maintenance advice for Texas properties.',
        'image' => 'landscape-lighting-texas-home',
    ],
    '/landscape-lighting-complete-guide/' => [
        'file' => 'posts/landscape-lighting-complete-guide.php', 'type' => 'post',
        'title' => 'Landscape Lighting: The Complete Guide (2026) | Texas Homes',
        'h1' => 'Landscape Lighting: The Complete Guide',
        'description' => 'Discover how landscape lighting enhances curb appeal, safety, security and outdoor living, with expert design techniques, fixture types and Texas tips.',
        'image' => 'landscape-lighting-texas-home', 'date' => '2026-06-23', 'modified' => BUILD_DATE,
    ],
    '/landscape-lighting-cost-calculator/' => [
        'file' => 'posts/landscape-lighting-cost-calculator.php', 'type' => 'post',
        'title' => 'Landscape Lighting Cost Calculator | Texas Pricing Estimator',
        'h1' => 'Landscape Lighting Cost Calculator',
        'description' => 'Use our landscape lighting cost calculator to estimate fixtures, installation, transformer size and energy costs for your Texas property.',
        'image' => 'cost-calculator', 'date' => '2026-07-17', 'modified' => BUILD_DATE,
    ],
    '/landscape-lighting-ideas-texas-homes/' => [
        'file' => 'posts/landscape-lighting-ideas-texas-homes.php', 'type' => 'post',
        'title' => '25 Landscape Lighting Ideas for Texas Homes (With Photos)',
        'h1' => '25 Landscape Lighting Ideas for Texas Homes',
        'description' => '25 landscape lighting ideas for Texas homes: limestone facades, live oaks, pools, pathways, patios and smart scenes, with fixture tips for each idea.',
        'image' => 'architectural-uplighting', 'date' => '2026-08-04',
    ],
    '/how-to-light-live-oak-trees/' => [
        'file' => 'posts/how-to-light-live-oak-trees.php', 'type' => 'post',
        'title' => 'How to Light Live Oak Trees: Uplighting & Moonlighting Guide',
        'h1' => 'How to Light Live Oak Trees',
        'description' => 'How to light live oak trees the right way: how many uplights, beam angles, moonlighting from the canopy, protecting roots and avoiding glare.',
        'image' => 'oak-tree-uplighting', 'date' => '2026-08-18',
    ],
    '/landscape-lighting-color-temperature-guide/' => [
        'file' => 'posts/landscape-lighting-color-temperature-guide.php', 'type' => 'post',
        'title' => 'Landscape Lighting Color Temperature Guide: 2700K vs 3000K',
        'h1' => 'Landscape Lighting Color Temperature Guide',
        'description' => 'Which color temperature is best for landscape lighting? Compare 2200K, 2700K, 3000K and 4000K for stone, brick, plants, water and Texas homes.',
        'image' => 'architectural-uplighting', 'date' => '2026-09-01',
    ],
    '/led-vs-halogen-landscape-lighting/' => [
        'file' => 'posts/led-vs-halogen-landscape-lighting.php', 'type' => 'post',
        'title' => 'LED vs Halogen Landscape Lighting: Cost, Life & Light Quality',
        'h1' => 'LED vs Halogen Landscape Lighting',
        'description' => 'LED vs halogen landscape lighting compared: energy use, bulb life, heat, light quality, upfront cost and when an LED retrofit pays for itself in Texas.',
        'image' => 'garden-pathway-lighting', 'date' => '2026-09-15',
    ],
    '/low-voltage-landscape-lighting-guide/' => [
        'file' => 'posts/low-voltage-landscape-lighting-guide.php', 'type' => 'post',
        'title' => 'Low-Voltage Landscape Lighting: How Systems Work & Are Wired',
        'h1' => 'Low-Voltage Landscape Lighting Explained',
        'description' => 'How low-voltage landscape lighting works: transformers, wire gauge, voltage drop, hub wiring, burial depth and what separates a pro install from a kit.',
        'image' => 'driveway-lighting', 'date' => '2026-09-24',
    ],
    '/landscape-lighting-maintenance-checklist/' => [
        'file' => 'posts/landscape-lighting-maintenance-checklist.php', 'type' => 'post',
        'title' => 'Landscape Lighting Maintenance Checklist for Texas Seasons',
        'h1' => 'Landscape Lighting Maintenance Checklist',
        'description' => 'A season-by-season landscape lighting maintenance checklist for Texas: cleaning lenses, re-aiming, trimming, checking connections and resetting timers.',
        'image' => 'patio-lighting', 'date' => '2026-10-02',
    ],

    // ----- Legal & utility -----
    '/privacy-policy/' => [
        'file' => 'pages/privacy-policy.php', 'type' => 'legal',
        'title' => 'Privacy Policy | Landscape Lighting Texas',
        'h1' => 'Privacy Policy',
        'description' => 'How Landscape Lighting Texas collects, uses and protects the information you share through our website, quote requests and consultations.',
    ],
    '/terms-of-service/' => [
        'file' => 'pages/terms-of-service.php', 'type' => 'legal',
        'title' => 'Terms of Service | Landscape Lighting Texas',
        'h1' => 'Terms of Service',
        'description' => 'The terms that govern use of the Landscape Lighting Texas website, estimates, consultations and outdoor lighting services.',
    ],
    '/sitemap/' => [
        'file' => 'pages/sitemap.php', 'type' => 'page',
        'title' => 'Sitemap | Landscape Lighting Texas',
        'h1' => 'Sitemap',
        'description' => 'Every page on the Landscape Lighting Texas website: services, service areas, tools and calculators, blog articles and company pages.',
    ],
];

foreach ($PAGES as $p => &$pg) {
    $pg['path'] = $p;
    $pg += ['h1' => $pg['title'], 'image' => null, 'modified' => $pg['date'] ?? BUILD_DATE];
    if ($pg['type'] === 'post') $pg += ['category' => 'general'];
}
unset($pg);

/** Blog posts, newest first. */
function posts(): array {
    global $PAGES;
    $posts = array_filter($PAGES, fn($p) => $p['type'] === 'post');
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    return $posts;
}
