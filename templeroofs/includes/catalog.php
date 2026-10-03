<?php
/**
 * Site catalog: the order of services, service areas, tools and blog
 * categories. Page copy lives in /content; this file only controls what
 * is listed and in which order.
 */
defined('TR_ROOT') || exit;

return [
    // Service slugs in display order (each has content/services/{slug}.php).
    'services' => [
        'roof-repair-temple-tx',
        'roof-replacement-temple-tx',
        'storm-damage-roof-repair-temple-tx',
        'hail-damage-roof-repair-temple-tx',
        'wind-damage-roof-repair-temple-tx',
        'roof-insurance-claim-assistance-temple-tx',
        'roof-inspection-temple-tx',
        'emergency-roof-leak-repair-temple-tx',
        'asphalt-shingle-roofing-temple-tx',
        'metal-roofing-temple-tx',
        'commercial-roofing-temple-tx',
        'gutters-roof-drainage-temple-tx',
    ],

    // Service areas. Set 'published' => false for any community you do NOT
    // serve: the page then returns 404 and disappears from menus, the
    // service-area list, structured data and both sitemaps. The content file
    // stays in /content/areas as an unpublished template.
    'areas' => [
        'temple-tx'               => ['published' => true],
        'belton-tx'               => ['published' => true],
        'troy-tx'                 => ['published' => true],
        'salado-tx'               => ['published' => true],
        'little-river-academy-tx' => ['published' => true],
        'morgans-point-resort-tx' => ['published' => true],
        'nolanville-tx'           => ['published' => true],
        'harker-heights-tx'       => ['published' => true],
        'rogers-tx'               => ['published' => true],
    ],

    'tools' => [
        'roof-replacement-cost-calculator' => [
            'name'    => 'Roof Replacement Cost Calculator',
            'short'   => 'Cost Calculator',
            'icon'    => 'calculator',
            'summary' => 'Plan a re-roof budget for a Temple-area home: roof area, squares, materials, labor, tear-off and decking in one estimate range.',
        ],
        'roof-pitch-calculator' => [
            'name'    => 'Roof Pitch & Area Calculator',
            'short'   => 'Pitch & Area Calculator',
            'icon'    => 'ruler',
            'summary' => 'Convert rise and run to pitch, angle and slope multiplier, then turn a footprint into roof area, squares and shingle bundles.',
        ],
        'storm-damage-checklist' => [
            'name'    => 'Storm & Hail Damage Self-Check',
            'short'   => 'Storm Damage Self-Check',
            'icon'    => 'checklist',
            'summary' => 'Walk through what you can safely see from the ground after wind or hail and get practical next steps for your home.',
        ],
    ],

    'blog_categories' => [
        'roof-maintenance'      => 'Roof Maintenance',
        'storm-hail-damage'     => 'Storm & Hail Damage',
        'roof-replacement'      => 'Roof Replacement',
        'roofing-materials'     => 'Roofing Materials',
        'insurance-costs'       => 'Insurance & Costs',
        'local-roofing-guides'  => 'Local Roofing Guides',
    ],

    // Options for the "Type of roofing concern" field on every lead form.
    'concerns' => [
        'inspection'  => 'Free roof inspection',
        'leak'        => 'Roof leak',
        'storm'       => 'Storm, hail or wind damage',
        'repair'      => 'Roof repair',
        'replacement' => 'Roof replacement',
        'insurance'   => 'Insurance claim documentation',
        'metal'       => 'Metal roofing',
        'commercial'  => 'Commercial roofing',
        'gutters'     => 'Gutters & drainage',
        'other'       => 'Something else',
    ],
];
