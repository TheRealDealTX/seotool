<?php
// Site-wide settings. Business details here feed the header, footer, schema and forms.

const SITE_NAME   = 'Best Jobs Pro';
const SITE_URL    = 'https://bestjobspro.com';
const SITE_PHONE  = '210-903-9471';
const SITE_TEL    = '+12109039471';
const SITE_EMAIL  = 'careers@bestjobspro.com';
const SITE_STREET = '2140 E Southlake Blvd';
const SITE_CITY   = 'Southlake';
const SITE_REGION = 'TX';
const SITE_ZIP    = '76092';
const SITE_MAP    = 'https://goo.gl/maps/PM6Wc4HnNQnEnRx86';
const SITE_FOUNDED = '2023';

// Form delivery. With SMTP_* set in inc/secret.php, mail goes out through that mailbox;
// FORM_FROM is only used by the PHP mail() fallback.
const FORM_TO   = 'careers@bestjobspro.com';
const FORM_FROM = 'no-reply@bestjobspro.com';
const RESUME_MAX_BYTES = 10 * 1024 * 1024;

// Bump when assets/css or assets/js change so browsers fetch the new files.
const ASSET_VER = '1.0.0';

// Old URL -> new URL (301). Everything else that existed on the WordPress site
// is served at its original path.
const REDIRECTS = [
    '/write-for-us/'           => '/blog/',
    '/feed/'                   => '/blog/',
    '/comments/feed/'          => '/blog/',
    '/category/job-articles/feed/' => '/category/job-articles/',
    '/post-sitemap.xml'        => '/sitemap.xml',
    '/page-sitemap.xml'        => '/sitemap.xml',
    '/category-sitemap.xml'    => '/sitemap.xml',
    '/sitemap_index.xml'       => '/sitemap.xml',
    '/author/best-jobs-pro/'   => '/about/',
    '/home/'                   => '/',
];

const NAV = [
    ['/', 'Home'],
    ['/about/', 'About'],
    ['/our-services/', 'Our Services'],
    ['/employers/', 'Employers'],
    ['/job-postings/', 'Job Postings'],
    ['/career-tools/', 'Career Tools'],
    ['/blog/', 'Blog'],
    ['/contact-us/', 'Contact Us'],
];

// Job openings shown on /job-postings/ and offered in the application form.
const JOBS = [
    ['Accounting Specialist',               'office',   'Full-time', 'Reconcile accounts, process payables and receivables, and support month-end close.'],
    ['Administrative Assistant',            'office',   'Full-time', 'Keep an office running: scheduling, data entry, phones, filing and correspondence.'],
    ['Apartment Maintenance',               'trades',   'Full-time', 'Make-ready work, work orders, basic plumbing, electrical and HVAC for apartment communities.'],
    ['Automotive Parts Counter',            'customer', 'Full-time', 'Look up and sell parts to shops and walk-in customers; manage counter inventory.'],
    ['Concrete Workers (Day & Night Shift)', 'labor',   'Day / Night', 'Form setting, pouring and finishing on commercial and residential jobs.'],
    ['Drivers: ACDL/BCDL',                  'driving',  'Full-time', 'Class A or B CDL routes; clean MVR and current medical card required.'],
    ['Food Service',                        'customer', 'Flexible',  'Prep, line and service roles for cafeterias, events and restaurants.'],
    ['General Labor with DL & Clean BG',    'labor',    'Flexible',  'Loading, cleanup and site support. Valid driver\'s license and clean background.'],
    ['Housekeeping',                        'customer', 'Flexible',  'Commercial, hotel and residential cleaning with reliable, set schedules.'],
    ['Hydraulics Assembler',                'trades',   'Full-time', 'Assemble and test hydraulic components from blueprints and work orders.'],
    ['Machine Operators',                   'labor',    'Shift work', 'Set up and run production machinery; quality checks and basic upkeep.'],
    ['Mechanical Maintenance',              'trades',   'Full-time', 'Troubleshoot and repair plant equipment, conveyors, motors and pneumatics.'],
    ['Packer/Stocker/Warehouse',            'labor',    'Flexible',  'Pick, pack, stock and ship. Forklift experience is a plus.'],
    ['Receptionist',                        'office',   'Full-time', 'Be the first face and voice of the business: greet visitors, route calls, schedule.'],
    ['Skilled Carpenters',                  'trades',   'Full-time', 'Framing, trim and finish carpentry on residential and commercial builds.'],
    ['Welders',                             'trades',   'Full-time', 'MIG, TIG and stick welding; fabrication shop and field positions.'],
];

const JOB_CATEGORIES = [
    'office'   => 'Office & Admin',
    'labor'    => 'Warehouse & Labor',
    'trades'   => 'Skilled Trades',
    'customer' => 'Customer Service',
    'driving'  => 'Driving',
];

// Career tools: slug => [title, short description, icon, tool key]
const TOOLS = [
    'paycheck-calculator'            => ['Texas Paycheck Calculator', 'Turn an hourly wage or salary into weekly, monthly and yearly pay, with an estimated take-home after federal tax and FICA.', 'wallet', 'paycheck'],
    'job-match-quiz'                 => ['Job Match Quiz', 'Answer six quick questions and see which kinds of Texas jobs fit how you like to work.', 'compass', 'job-quiz'],
    'resume-keyword-checker'         => ['Résumé Keyword Checker', 'Paste a job description and your résumé to see which keywords you match and which you are missing.', 'scan', 'resume-keywords'],
    'self-employment-tax-calculator' => ['1099 Self-Employment Tax Calculator', 'Estimate self-employment tax, federal income tax and your quarterly payments as an independent contractor.', 'receipt', 'contractor-tax'],
    'freelance-rate-calculator'      => ['Freelance Rate Calculator', 'Work out the hourly rate you need to hit your income goal after expenses, time off and platform fees.', 'gauge', 'freelance-rate'],
    'cost-of-vacancy-calculator'     => ['Cost of Vacancy Calculator', 'For employers: see what an open position and a bad hire really cost, and what you save by filling it faster.', 'chart', 'vacancy-cost'],
];
