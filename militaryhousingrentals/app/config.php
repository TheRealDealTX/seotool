<?php
// Site-wide settings. Listings, bases and posts live in app/data/.
return [
    'name'        => 'Military Housing Rentals',
    'tagline'     => 'Reliable Housing for Every Move',
    'origin'      => 'https://militaryhousingrentals.com',
    'email'       => 'info@militaryhousingrentals.com',
    'phone'       => '+1 832-720-7978',
    'phone_href'  => 'tel:+18327207978',
    'logo'        => '/wp-content/uploads/2025/06/Military-Housing-Rentals-Logo.webp',
    'icon'        => '/wp-content/uploads/2025/06/cropped-Military-Housing-Rentals-Site-Icon.webp',
    'og_image'    => '/wp-content/uploads/2025/06/Military-Housing-Rentals-BG-1.webp',
    'amazon_tag'  => 'militaryhousingrentals-20',
    'ga_ids'      => ['G-VXSSXDHMRS', 'GT-TXBQ6W8F'],
    'adsense'     => 'ca-pub-3886800648957674',
    'social'      => [
        'Facebook'  => 'https://www.facebook.com/Military-Housing-Rentals-806797346092374/',
        'Instagram' => 'https://www.instagram.com/militaryhousingrentals/',
        'Pinterest' => 'https://www.pinterest.com/militaryhousing/',
    ],
    'nav' => [
        '/'             => 'Home',
        '/properties/'  => 'Listings',
        '/marine-bases/' => 'Military Bases',
        '/blog/'        => 'Blog',
        '/contact-us/'  => 'Contact Us',
    ],
    // Old WordPress ?p=ID links
    'legacy_ids' => [
        263 => '/what-is-base-housing/', 220 => '/renting-vs-buying/',
        271 => '/pcs-moving-checklist/', 272 => '/bah-explained-military-housing-allowance/',
        273 => '/scra-military-clause-breaking-a-lease/', 274 => '/move-in-move-out-inspection-tips/',
        275 => '/renter-friendly-upgrades-for-base-housing/', 276 => '/pcs-with-pets-military-housing/',
        277 => '/how-to-find-off-base-housing/',
        77 => '/properties/comanche-cavalry-family-housing/', 135 => '/properties/airman-scott-village-1193-lackland-family-homes/',
        13 => '/', 15 => '/blog/', 17 => '/contact-us/', 129 => '/marine-bases/', 131 => '/submit-property/',
        3 => '/privacy-policy/', 156 => '/terms-of-use/',
    ],
];
