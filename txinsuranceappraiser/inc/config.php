<?php
/**
 * Site-wide configuration for TX Insurance Appraiser.
 * Business facts live here once; every template reads them from SITE.
 */
declare(strict_types=1);

const SITE = [
    'name'        => 'TX Insurance Appraiser',
    'legal'       => 'TX Insurance Appraisals LLC',
    'origin'      => 'https://txinsuranceappraiser.com',   // canonical production origin
    'prod_host'   => 'txinsuranceappraiser.com',
    'phone'       => '+1 (254) 421-5412',
    'phone_short' => '(254) 421-5412',
    'phone_href'  => '+12544215412',
    'email'       => 'info@txinsuranceappraiser.com',
    'hours'       => 'Mon – Fri: 9 AM – 6 PM',
    'hours_schema'=> 'Mo-Fr 09:00-18:00',
    'hubs'        => ['Austin', 'Waco', 'Dallas', 'Houston'],
    'tagline'     => 'Precision in Appraisal, Thorough on Inspection.',
    'logo'        => '/assets/img/site/TX-Insurance-Appraiser-Logo-S.webp',
    'icon'        => '/assets/img/site/TX-Insurance-Appraiser-Icon.webp',
    'og_default'  => '/assets/img/site/TX-Insurance-Appraiser-Site-Image.webp',
    'appraiser'   => [
        'name'     => 'Joseph Dittman',
        'role'     => 'Lead Insurance Appraiser',
        'company'  => 'Rise Public Adjusting LLC',
        'license'  => '3356839',
        'tdi_url'  => 'https://www.tdi.texas.gov/agent/agentlookup.html',
    ],
    // Contact form delivery
    'form_to'     => 'info@txinsuranceappraiser.com',
    'form_from'   => 'no-reply@txinsuranceappraiser.com',
];

// Main navigation: [label, url, children]
const NAV = [
    ['Home', '/', []],
    ['About', '/about-us/', [
        ['About Joseph Dittman', '/about-us/'],
        ['What Is an Appraisal?', '/what-is-an-appraisal/'],
    ]],
    ['Services', '/services/', [
        ['Insurance Appraisal', '/services/appraisal/'],
        ['Umpire Services', '/services/umpire/'],
        ['Matterport 3D Scans', '/services/matterport/'],
        ['Xactimate Estimates', '/services/xactimate-estimate/'],
        ['Symbility Estimates', '/services/symbility-estimate/'],
    ]],
    ['Areas', '/areas/', [
        ['Houston, TX', '/areas/houston-insurance-appraiser/'],
        ['Dallas, TX', '/areas/dallas-insurance-appraiser/'],
        ['Austin, TX', '/areas/austin-insurance-appraiser/'],
        ['Fort Worth, TX', '/areas/fort-worth-insurance-appraiser/'],
        ['San Antonio, TX', '/areas/san-antonio-insurance-appraiser/'],
        ['Arlington, TX', '/areas/arlington-insurance-appraiser/'],
        ['Waco, TX', '/areas/waco-insurance-appraiser/'],
        ['All 288 Texas Cities →', '/areas/'],
    ]],
    ['Free Tools', '/tools/', [
        ['Recoverable Depreciation Calculator', '/tools/recoverable-depreciation-calculator/'],
        ['Is Appraisal Worth It?', '/tools/appraisal-cost-calculator/'],
        ['Roof Square & Waste Calculator', '/tools/roof-square-calculator/'],
        ['Texas Claim Deadline Calculator', '/tools/texas-claim-deadline-calculator/'],
        ['Claim Documentation Checklist', '/tools/claim-documentation-checklist/'],
    ]],
    ['Blog', '/blog/', []],
    ['Contact', '/contact-us/', []],
];

const TOOLS = [
    'recoverable-depreciation-calculator' => [
        'title' => 'Recoverable Depreciation Calculator',
        'short' => 'See what your carrier should pay now (ACV) and what you can recover after repairs (RCV holdback).',
        'icon'  => 'percent',
    ],
    'appraisal-cost-calculator' => [
        'title' => 'Is Appraisal Worth It? Calculator',
        'short' => 'Compare the carrier’s number to your estimate and see the likely net gain after appraisal costs.',
        'icon'  => 'scale',
    ],
    'roof-square-calculator' => [
        'title' => 'Roof Square, Pitch & Waste Calculator',
        'short' => 'Convert footprint and pitch into true roof squares and check the waste factor on an estimate.',
        'icon'  => 'roof',
    ],
    'texas-claim-deadline-calculator' => [
        'title' => 'Texas Claim Deadline Calculator',
        'short' => 'Map Texas Insurance Code Chapter 542 prompt-payment deadlines from your own claim dates.',
        'icon'  => 'calendar',
    ],
    'claim-documentation-checklist' => [
        'title' => 'Claim Documentation Checklist',
        'short' => 'An interactive, printable checklist of the evidence that wins appraisal disputes.',
        'icon'  => 'check',
    ],
];

const BLOG_CATEGORIES = [
    'Appraisal Process', 'Roof Claims', 'Commercial Claims',
    'Insurance Basics', 'Estimating & Technology', 'Texas Weather & Claims',
];
