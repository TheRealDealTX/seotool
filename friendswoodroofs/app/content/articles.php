<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/**
 * Blog articles. Each renders at /blog/{slug}/ with its body from
 * content/articles/{slug}.php.
 *
 * Publication dates: "days_before_launch" is subtracted from the launch_date
 * in config/site.php. The schedule is fixed (0, 3, 6, 9, 12 days), so dates
 * only change when the owner edits launch_date, never on page load.
 */
return [
    'how-to-choose-a-roofing-contractor-friendswood' => [
        'title'       => 'Friendswood Roofers: How to Choose a Roofing Contractor',
        'seo_title'   => 'Friendswood Roofers: How to Choose a Roofing Contractor',
        'description' => 'A practical checklist for comparing Friendswood roofers: what to ask, what a written estimate should include and the red flags to avoid after a storm.',
        'category'    => 'Hiring & Estimates',
        'image'       => 'roofing-crew-trucks',
        'excerpt'     => 'What to ask, what a written estimate should include, and the warning signs that should make you slow down before you sign.',
        'days_before_launch' => 0,
        'services'    => ['roof-replacement', 'roof-repair', 'storm-damage-roof-repair'],
    ],
    'roof-repair-or-replacement-friendswood' => [
        'title'       => 'Roof Repair or Replacement? A Guide for Friendswood Homeowners',
        'seo_title'   => 'Roof Repair or Replacement? A Friendswood Homeowner Guide',
        'description' => 'Not sure whether to repair or replace your roof? Learn the signs that point each way, the questions to ask and how Friendswood weather factors in.',
        'category'    => 'Repair & Replacement',
        'image'       => 'shingle-tear-off',
        'excerpt'     => 'How the extent of damage, the roof\'s overall condition and your plans for the home point toward a repair or a full replacement.',
        'days_before_launch' => 3,
        'services'    => ['roof-repair', 'roof-replacement', 'roof-inspections'],
    ],
    'friendswood-roof-maintenance-checklist' => [
        'title'       => 'Friendswood Roofing Maintenance: A Seasonal Checklist',
        'seo_title'   => 'Friendswood Roofing Maintenance: A Seasonal Checklist',
        'description' => 'A season-by-season roof maintenance checklist for Friendswood, TX homeowners, with ground-level checks you can do safely and when to call a roofer.',
        'category'    => 'Maintenance',
        'image'       => 'roof-cleaning-maintenance',
        'excerpt'     => 'Simple, ground-level checks for spring, summer, fall and winter, plus what to look at before and after the Gulf storm season.',
        'days_before_launch' => 6,
        'services'    => ['roof-maintenance', 'roof-inspections', 'storm-damage-roof-repair'],
    ],
    'asphalt-shingles-vs-metal-roofing-friendswood-tx' => [
        'title'       => 'Asphalt Shingles vs. Metal Roofing for Homes in Friendswood, TX',
        'seo_title'   => 'Asphalt Shingles vs. Metal Roofing in Friendswood, TX',
        'description' => 'Compare asphalt shingles and metal roofing for a Friendswood, TX home: upfront cost, durability, wind and heat performance, noise, looks and maintenance.',
        'category'    => 'Materials',
        'image'       => 'metal-roof-aerial',
        'excerpt'     => 'An honest side-by-side look at cost, durability, heat, wind, noise and appearance to help you decide which material fits your home.',
        'days_before_launch' => 9,
        'services'    => ['asphalt-shingle-roofing', 'metal-roofing', 'roof-replacement'],
    ],
    'roof-inspection-what-to-expect-friendswood' => [
        'title'       => 'What to Expect During a Roof Inspection in Friendswood',
        'seo_title'   => 'What to Expect During a Roof Inspection in Friendswood, TX',
        'description' => 'What happens during a roof inspection in Friendswood, TX: what gets checked, how long it takes, how to prepare and what you should receive afterward.',
        'category'    => 'Inspections',
        'image'       => 'roof-damage-documentation',
        'excerpt'     => 'A step-by-step look at a professional roof inspection: what gets checked, how to prepare and what your report should include.',
        'days_before_launch' => 12,
        'services'    => ['roof-inspections', 'roof-repair', 'storm-damage-roof-repair'],
    ],
];
