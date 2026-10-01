<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/**
 * Roofing Project Planner questions. Used by templates/pages/planner.php for
 * both the server-rendered summary (no JavaScript) and, via data attributes,
 * the in-browser summary in site.js.
 *
 * 'service' pre-selects the estimate form's "Service needed" field (the
 * visitor can change it). 'tip' is a general, non-diagnostic note.
 */
return [
    'concern' => [
        'legend' => 'What is your main roofing concern?',
        'label'  => 'Main concern',
        'options' => [
            'leak'      => ['Leak or water stain', 'service' => 'roof-repair', 'link' => '/services/roof-repair/', 'link_label' => 'Roof Repair'],
            'damaged'   => ['Missing or damaged shingles or panels', 'service' => 'roof-repair', 'link' => '/services/roof-repair/', 'link_label' => 'Roof Repair'],
            'storm'     => ['Possible damage after a storm', 'service' => 'storm-damage-roof-repair', 'link' => '/services/storm-damage-roof-repair/', 'link_label' => 'Storm Damage Roof Repair'],
            'aging'     => ['Aging roof / wondering about replacement', 'service' => 'roof-inspections', 'link' => '/blog/roof-repair-or-replacement-friendswood/', 'link_label' => 'Roof Repair or Replacement? A Guide for Friendswood Homeowners'],
            'inspection'=> ['Routine inspection or maintenance', 'service' => 'roof-inspections', 'link' => '/services/roof-inspections/', 'link_label' => 'Roof Inspections'],
            'material'  => ['Planning a new roof or a different material', 'service' => 'roof-replacement', 'link' => '/blog/asphalt-shingles-vs-metal-roofing-friendswood-tx/', 'link_label' => 'Asphalt Shingles vs. Metal Roofing'],
            'other'     => ['Something else', 'service' => 'not-sure', 'link' => '/services/', 'link_label' => 'Roofing services overview'],
        ],
    ],
    'age' => [
        'legend' => 'Approximately how old is the roof?',
        'label'  => 'Approximate roof age',
        'options' => [
            'lt5'    => ['Less than 5 years'],
            '5-10'   => ['5 to 10 years'],
            '11-15'  => ['11 to 15 years'],
            '16-20'  => ['16 to 20 years'],
            'gt20'   => ['More than 20 years'],
            'unsure' => ['Not sure'],
        ],
    ],
    'material' => [
        'legend' => 'What is the roofing material, if you know?',
        'label'  => 'Roofing material',
        'options' => [
            'shingle' => ['Asphalt shingles'],
            'metal'   => ['Metal'],
            'tile'    => ['Tile'],
            'flat'    => ['Flat or low-slope roofing'],
            'other'   => ['Other'],
            'unsure'  => ['Not sure'],
        ],
    ],
    'damage' => [
        'legend' => 'Are there visible leaks or damage?',
        'label'  => 'Leaks or visible damage',
        'options' => [
            'active'  => ['Yes, water is coming inside now', 'tip' => 'Move belongings away from the drip, put a container under it and take photos. Keep people away from any sagging ceiling, and do not go on the roof. Call us to talk about timing.'],
            'visible' => ['Yes, visible damage but no water inside', 'tip' => 'Take photos from the ground and note where the damage is. Keep an eye on ceilings and the attic during the next rain.'],
            'unsure'  => ['I noticed something but I\'m not sure', 'tip' => 'Photos taken safely from the ground or inside the house will help us understand what you are seeing.'],
            'none'    => ['No visible leaks or damage', 'tip' => 'A routine check can still be useful, especially before hurricane season or if the roof\'s history is unknown.'],
        ],
    ],
    'timeframe' => [
        'legend' => 'When would you like the work done?',
        'label'  => 'Preferred timeframe',
        'options' => [
            'asap'     => ['As soon as possible'],
            'month'    => ['Within the next month'],
            'quarter'  => ['Within 1 to 3 months'],
            'planning' => ['Just planning or researching'],
        ],
    ],
];
