<?php
/**
 * ROOF REPLACEMENT COST CALCULATOR — EDITABLE ASSUMPTIONS
 *
 * These are ILLUSTRATIVE planning figures for Central Texas, not verified
 * live contractor prices and not Temple Roofers' quoted prices. Update them
 * whenever your real material and labor costs change. All money values are
 * US dollars as [low, high] ranges.
 *
 * Units: a roofing "square" = 100 sq ft of roof surface.
 */
defined('TR_ROOT') || exit;

return [
    'last_reviewed' => 'October 2026',

    // Roof footprint = floor area / stories × this factor (eave & rake overhangs).
    'overhang_factor' => 1.10,

    // Per-square material and installation labor ranges by roofing type.
    'materials' => [
        'three_tab'     => ['label' => 'Standard 3-tab asphalt shingles',        'material' => [100, 140], 'labor' => [150, 200]],
        'architectural' => ['label' => 'Architectural (dimensional) shingles',   'material' => [130, 180], 'labor' => [160, 215]],
        'impact'        => ['label' => 'Impact-resistant (Class 4) shingles',    'material' => [200, 280], 'labor' => [170, 230]],
        'standing_seam' => ['label' => 'Standing-seam metal',                    'material' => [450, 650], 'labor' => [350, 500]],
        'stone_coated'  => ['label' => 'Stone-coated steel',                     'material' => [380, 520], 'labor' => [300, 430]],
    ],

    // Underlayment, drip edge, starter, ridge cap, flashing and vents, per square.
    'accessories_per_square' => [45, 80],

    // Tear-off and disposal, per square, per existing layer.
    'tearoff_per_square_per_layer' => [45, 75],

    // Replacement decking, per 4×8 sheet (32 sq ft) installed.
    'decking_per_sheet' => [70, 110],

    // Labor multipliers. Pitch: applies when rise (per 12) is >= the key.
    'pitch_labor' => [0 => 1.00, 7 => 1.10, 9 => 1.22, 11 => 1.35],
    'story_labor' => [1 => 1.00, 2 => 1.10, 3 => 1.20],

    // Roof complexity: labor multiplier and default waste allowance (%).
    'complexity' => [
        'simple'   => ['label' => 'Simple — mostly one gable or hip, few cuts',      'labor' => 1.00, 'waste' => 10],
        'moderate' => ['label' => 'Moderate — hips, a few valleys or dormers',       'labor' => 1.08, 'waste' => 12],
        'complex'  => ['label' => 'Complex — many valleys, dormers, levels',         'labor' => 1.18, 'waste' => 15],
    ],
];
