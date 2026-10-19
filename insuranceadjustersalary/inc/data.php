<?php
// Pay model inputs shared by the calculators, the state explorer and the homepage.
// National anchor: BLS OOH median for claims adjusters, appraisers, examiners & investigators, May 2024.

const BLS_MEDIAN_ANNUAL = 76790;
const BLS_MEDIAN_HOURLY = 36.92;
const BLS_JOBS          = 365300;
const BLS_URL           = 'https://www.bls.gov/ooh/business-and-financial/claims-adjusters-appraisers-examiners-and-investigators.htm';

/**
 * State wage index (1.00 = national) and catastrophe-claim demand.
 * Index values are our regional pay estimates, not official BLS state figures.
 */
function states(): array
{
    $rows = [
        // code, name, wage index, CAT demand (H/M/L)
        ['AL', 'Alabama', .90, 'H'], ['AK', 'Alaska', 1.08, 'L'], ['AZ', 'Arizona', .98, 'M'], ['AR', 'Arkansas', .87, 'M'],
        ['CA', 'California', 1.15, 'H'], ['CO', 'Colorado', 1.06, 'H'], ['CT', 'Connecticut', 1.10, 'L'], ['DE', 'Delaware', 1.02, 'L'],
        ['DC', 'District of Columbia', 1.18, 'L'], ['FL', 'Florida', .97, 'H'], ['GA', 'Georgia', .97, 'H'], ['HI', 'Hawaii', 1.03, 'M'],
        ['ID', 'Idaho', .90, 'L'], ['IL', 'Illinois', 1.04, 'M'], ['IN', 'Indiana', .92, 'M'], ['IA', 'Iowa', .94, 'M'],
        ['KS', 'Kansas', .92, 'H'], ['KY', 'Kentucky', .90, 'M'], ['LA', 'Louisiana', .91, 'H'], ['ME', 'Maine', .95, 'L'],
        ['MD', 'Maryland', 1.06, 'L'], ['MA', 'Massachusetts', 1.13, 'L'], ['MI', 'Michigan', .96, 'L'], ['MN', 'Minnesota', 1.03, 'M'],
        ['MS', 'Mississippi', .85, 'H'], ['MO', 'Missouri', .93, 'M'], ['MT', 'Montana', .90, 'M'], ['NE', 'Nebraska', .94, 'H'],
        ['NV', 'Nevada', .97, 'L'], ['NH', 'New Hampshire', 1.04, 'L'], ['NJ', 'New Jersey', 1.11, 'M'], ['NM', 'New Mexico', .92, 'L'],
        ['NY', 'New York', 1.12, 'M'], ['NC', 'North Carolina', .95, 'H'], ['ND', 'North Dakota', .97, 'M'], ['OH', 'Ohio', .95, 'M'],
        ['OK', 'Oklahoma', .90, 'H'], ['OR', 'Oregon', 1.04, 'L'], ['PA', 'Pennsylvania', 1.00, 'L'], ['RI', 'Rhode Island', 1.05, 'L'],
        ['SC', 'South Carolina', .91, 'H'], ['SD', 'South Dakota', .88, 'M'], ['TN', 'Tennessee', .93, 'M'], ['TX', 'Texas', 1.00, 'H'],
        ['UT', 'Utah', .97, 'L'], ['VT', 'Vermont', .97, 'L'], ['VA', 'Virginia', 1.03, 'M'], ['WA', 'Washington', 1.10, 'L'],
        ['WV', 'West Virginia', .87, 'L'], ['WI', 'Wisconsin', .96, 'L'], ['WY', 'Wyoming', .93, 'M'],
    ];
    $out = [];
    foreach ($rows as [$code, $name, $idx, $cat]) {
        $median = (int) (round(BLS_MEDIAN_ANNUAL * $idx / 100) * 100);
        $out[] = [
            'code'   => $code,
            'name'   => $name,
            'index'  => $idx,
            'median' => $median,
            'low'    => (int) (round($median * .64 / 100) * 100),
            'high'   => (int) (round($median * 1.5 / 100) * 100),
            'hourly' => round($median / 2080, 2),
            'cat'    => $cat,
        ];
    }
    return $out;
}

/** Pay ranges by type, used by the homepage chart (low, high). */
function chart_data(): array
{
    return [
        'type' => [
            'label' => 'By adjuster type',
            'note'  => 'Typical annual earnings. Independent, CAT and public adjuster income swings with storm activity.',
            'rows'  => [
                ['Staff desk adjuster', 52000, 78000],
                ['Staff field adjuster', 60000, 92000],
                ['Independent adjuster', 45000, 130000],
                ['CAT adjuster', 50000, 200000],
                ['Public adjuster', 50000, 150000],
            ],
        ],
        'line' => [
            'label' => 'By line of business',
            'note'  => 'Staff (W-2) adjusters with 2-5 years of experience. Field roles often add a company car and gas card.',
            'rows'  => [
                ['Auto / material damage', 50000, 72000],
                ['Property (desk)', 55000, 75000],
                ['Property (field)', 62000, 90000],
                ['Workers compensation', 55000, 82000],
                ['Bodily injury / casualty', 60000, 88000],
                ['Large loss / commercial', 85000, 120000],
            ],
        ],
        'exp' => [
            'label' => 'By experience',
            'note'  => 'Staff adjuster salary progression. Designations such as AIC and CPCU speed up the climb.',
            'rows'  => [
                ['Trainee (year 1)', 45000, 60000],
                ['Adjuster (2-4 yrs)', 55000, 75000],
                ['Senior (5-9 yrs)', 72000, 98000],
                ['Complex / large loss', 85000, 120000],
                ['Claims manager', 95000, 140000],
            ],
        ],
    ];
}
