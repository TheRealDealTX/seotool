<?php
// Site-wide constants for luxuryapartmentdesign.com.

const SITE_NAME   = 'Luxury Apartment Design';
const SITE_ORIGIN = 'https://luxuryapartmentdesign.com';
const SITE_TAGLINE = 'Luxury apartment interior design ideas, guides and free design tools';
const GA_TAG      = 'GT-KVJZ795B';           // Google tag carried over from the WordPress Site Kit install
const ASSET_VER   = '20261028';              // bump to bust browser caches for css/js

// Contact form messages and newsletter sign-ups are emailed here (sent
// through SMTP, see inc/mailer.php) and also stored in the private data folder.
const CONTACT_EMAIL = 'info@luxuryapartmentdesign.com';

const CATEGORIES = [
    'apartment-design-inspiration' => [
        'name'  => 'Design Inspiration',
        'title' => 'Luxury Apartment Design Inspiration & Interior Styles',
        'description' => 'Luxury apartment design inspiration: interior styles, room-by-room ideas and the principles that make a rental look high-end.',
        'intro' => 'Styles, principles and room-by-room ideas for an apartment that looks and feels high-end, from quiet luxury and Japandi to studio layouts.',
        'image' => 'japandi-rug',
    ],
    'living-tips' => [
        'name'  => 'Decor & Styling',
        'title' => 'Apartment Decor & Styling Tips',
        'description' => 'Apartment decor and styling tips: hanging art, styling pillows, lighting with fairy lights, easy and DIY decor ideas, and seasonal refreshes.',
        'intro' => 'The styling moves that make the biggest difference: art at the right height, pillows that look intentional, warm layered light and smart DIY.',
        'image' => 'how-to-style-pillows-on-a-couch',
    ],
    'space-optimization-storage' => [
        'name'  => 'Small Spaces & Storage',
        'title' => 'Small Apartment Ideas, Storage & Organization',
        'description' => 'Small apartment ideas, storage solutions and organization guides: decluttering, entryways, laundry closets, spare rooms and compact home gyms.',
        'intro' => 'Make every square foot work: storage that hides clutter, layouts that feel bigger, and organization systems that actually last.',
        'image' => 'studio-apartment',
    ],
    'renovations-makeovers' => [
        'name'  => 'Renovations & Makeovers',
        'title' => 'Apartment Renovations, Makeovers & Renter-Friendly Upgrades',
        'description' => 'Apartment makeovers and renter-friendly upgrades: small bathrooms, kitchens, shower doors, trim and drywall repair, explained step by step.',
        'intro' => 'Practical upgrades for kitchens, bathrooms and walls, with renter-friendly alternatives whenever a full renovation is off the table.',
        'image' => 'small-bathroom-design',
    ],
    'color-paint' => [
        'name'  => 'Color & Paint',
        'title' => 'Color & Paint Ideas for Apartments',
        'description' => 'Color and paint guides for apartments: pastel interior design, warm bedroom paint colors, lavender palettes and how to build a 60-30-10 scheme.',
        'intro' => 'How to choose colors that look expensive: undertones, palettes and pairings, with hex codes you can take straight to the paint store.',
        'image' => 'pastel-colors-for-home',
    ],
    'balcony-outdoor' => [
        'name'  => 'Balcony & Outdoor Living',
        'title' => 'Balcony, Patio & Small Garden Ideas',
        'description' => 'Balcony, patio and small garden ideas for apartments: luxury small garden design, arranging potted plants and decorating a patio on any budget.',
        'intro' => 'Turn a balcony, terrace or small patio into an outdoor room, with planting, furniture and lighting ideas sized for apartment life.',
        'image' => 'luxury-small-garden-ideas',
    ],
];

// Order and icons for the /tools/ hub. Copy lives in content/tools/.
const TOOLS = [
    'interior-design-style-quiz'   => ['name' => 'Interior Design Style Quiz',   'icon' => 'sparkle', 'short' => 'Find your style in 8 questions'],
    'room-color-palette-generator' => ['name' => 'Room Color Palette Generator', 'icon' => 'palette', 'short' => '60-30-10 palettes with hex codes'],
    'rug-size-calculator'          => ['name' => 'Rug Size Calculator',          'icon' => 'rug',     'short' => 'The right rug size for any room'],
    'art-hanging-calculator'       => ['name' => 'Art Hanging Calculator',       'icon' => 'frame',   'short' => 'Exact nail height and spacing'],
    'room-layout-planner'          => ['name' => 'Room Layout Planner',          'icon' => 'layout',  'short' => 'Drag-and-drop furniture planner'],
    'paint-calculator'             => ['name' => 'Paint Calculator',             'icon' => 'roller',  'short' => 'Gallons, primer and cost'],
    'room-lighting-calculator'     => ['name' => 'Room Lighting Calculator',     'icon' => 'bulb',    'short' => 'Lumens and a layered lighting plan'],
    'curtain-size-calculator'      => ['name' => 'Curtain Size Calculator',      'icon' => 'curtain', 'short' => 'Rod, panel width and length'],
    'decorating-budget-planner'    => ['name' => 'Decorating Budget Planner',    'icon' => 'budget',  'short' => 'Split your budget like a designer'],
];

const NAV = [
    ['Inspiration', '/category/apartment-design-inspiration/'],
    ['Small Spaces', '/category/space-optimization-storage/'],
    ['Decor', '/category/living-tips/'],
    ['Color', '/category/color-paint/'],
    ['Design Tools', '/tools/'],
    ['All Articles', '/blogs/'],
];
