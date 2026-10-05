<?php
/**
 * Austin Landscape Lighting - site configuration.
 *
 * Business facts, navigation and route tables live here so they are defined
 * exactly once. Everything else (lib/, pages/, content/) reads from this file.
 */
declare(strict_types=1);

const SITE_ORIGIN = 'https://austinlandscapelighting.com';
const SITE_NAME   = 'Austin Landscape Lighting';
const SITE_TAGLINE = 'Outdoor Lighting Design & Installation in Austin, TX';

const BIZ = [
    'name'          => 'Austin Landscape Lighting',
    'legal'         => 'Austin Landscape Lighting',
    'phone_display' => '+1 (281) 704-7210',
    'phone_short'   => '(281) 704-7210',
    'phone_href'    => 'tel:+12817047210',
    'phone_e164'    => '+12817047210',
    'email'         => 'info@austinlandscapelighting.com',
    'hours'         => 'Mon–Fri 8am–6pm · Sat 9am–2pm CT',
    'city'          => 'Austin',
    'state'         => 'TX',
    'state_long'    => 'Texas',
    'region'        => 'Central Texas',
    'country'       => 'US',
    'lat'           => 30.2672,
    'lng'           => -97.7431,
    'founded'       => '2020',
    'years'         => '6',
    'projects'      => '500+',
    'rating'        => '4.9',
    'reviews'       => '127',
    'warranty'      => '2-year workmanship warranty',
    'price_range'   => '$$',
];

/** Cities served, in the order they appear across the site. Slugs match content/areas/. */
const AREAS_ORDER = [
    'austin', 'round-rock', 'cedar-park', 'pflugerville', 'georgetown', 'bee-cave',
    'lakeway', 'westlake-hills', 'rollingwood', 'kyle', 'buda', 'dripping-springs',
];

/** Services, in display order. Slugs match content/services/. */
const SERVICES_ORDER = [
    'architectural-uplighting', 'path-and-walkway-lighting', 'garden-and-tree-lighting',
    'deck-and-patio-lighting', 'pool-and-water-feature-lighting', 'smart-lighting-systems',
    'led-upgrade-and-retrofit', 'security-and-safety-lighting', 'commercial-landscape-lighting',
    'maintenance-and-repair', 'custom-lighting-design', 'low-voltage-landscape-lighting',
];

/** Icon name per service (see lib/icons.php). */
const SERVICE_ICONS = [
    'architectural-uplighting'        => 'uplight',
    'path-and-walkway-lighting'       => 'path',
    'garden-and-tree-lighting'        => 'tree',
    'deck-and-patio-lighting'         => 'deck',
    'pool-and-water-feature-lighting' => 'pool',
    'smart-lighting-systems'          => 'wifi',
    'led-upgrade-and-retrofit'        => 'bulb',
    'security-and-safety-lighting'    => 'shield',
    'commercial-landscape-lighting'   => 'building',
    'maintenance-and-repair'          => 'wrench',
    'custom-lighting-design'          => 'pencil',
    'low-voltage-landscape-lighting'  => 'bolt',
];

/** Interactive tools. Slug => [name, short description, icon]. Pages live in pages/tools/<slug>.php */
const TOOLS = [
    'fixture-calculator'      => ['How Many Lights Do I Need?', 'Estimate fixture counts for your facade, paths, trees and patio in under a minute.', 'calc'],
    'cost-estimator'          => ['Project Cost Estimator', 'Build a planning budget from fixture count, fixture grade and smart controls.', 'dollar'],
    'lighting-visualizer'     => ['Lighting Visualizer', 'Switch techniques on and off in a night scene and watch the design come together.', 'sparkle'],
    'led-savings-calculator'  => ['LED Savings Calculator', 'See what an LED retrofit saves versus halogen, per year and over a decade.', 'bulb'],
    'transformer-calculator'  => ['Transformer Sizing Tool', 'Add up fixture wattage, apply headroom and get the right low-voltage transformer.', 'bolt'],
    'color-temperature-guide' => ['Color Temperature Guide', 'Slide from candlelight to daylight and see which Kelvin suits your home.', 'thermo'],
    'sunset-timer'            => ['Austin Sunset Timer', 'Tonight\'s sunset and dusk for Austin, plus a year-round schedule for your timer.', 'sun'],
    'lighting-style-quiz'     => ['Lighting Style Quiz', 'Eight quick questions to find the lighting style that fits your home.', 'quiz'],
];

const NAV = [
    ['Services', '/services/'],
    ['Service Areas', '/service-areas/'],
    ['Gallery', '/gallery/'],
    ['Tools', '/tools/'],
    ['Blog', '/blog/'],
    ['About', '/about-us/'],
];

/** Testimonials shown on the homepage and /reviews/. Carried over from the previous site. */
const REVIEWS = [
    ['name' => 'Jennifer M.', 'place' => 'Tarrytown, Austin', 'text' => 'We had three companies come out for quotes. Austin Landscape Lighting was the only one that actually understood what we were going for aesthetically. The result is stunning, like something out of a magazine.', 'service' => 'Architectural uplighting'],
    ['name' => 'David & Priya K.', 'place' => 'Westlake Hills', 'text' => 'They transformed our backyard patio into something we actually want to be in every night. The smart controls are intuitive and the crew was respectful of our landscaping. Highly recommend.', 'service' => 'Patio lighting + smart controls'],
    ['name' => 'Marcus T.', 'place' => 'South Congress, Austin', 'text' => 'Called them on a Tuesday, had a free estimate on Thursday, and lights installed the following Monday. The whole process was smooth and the price was exactly what they quoted. Perfect.', 'service' => 'Path and entry lighting'],
    ['name' => 'Sandra W.', 'place' => 'Rollingwood', 'text' => 'Our oak trees look incredible now. They used a moon-lighting technique that creates the most natural, beautiful dappled light effect. Every neighbor has asked who did it.', 'service' => 'Tree moonlighting'],
    ['name' => 'Robert A.', 'place' => 'Cedar Park', 'text' => 'Switched from halogen to LED with these guys. My electricity bill dropped noticeably and the light quality is actually better. The retrofit was clean and fast, could not be happier.', 'service' => 'LED retrofit'],
    ['name' => 'Linda C.', 'place' => 'East Austin business owner', 'text' => 'We hired them for our commercial property and the results exceeded expectations. Excellent communication throughout, and the after-dark curb appeal has noticeably increased foot traffic to our restaurant.', 'service' => 'Commercial lighting'],
];

const PROCESS_STEPS = [
    ['Free night consultation', 'We walk your property, ideally at dusk, listen to how you use your outdoor space and note the features worth showing off. No pressure, no obligation.'],
    ['Custom lighting design', 'You receive a fixture-by-fixture plan: techniques, beam spreads, color temperature, transformer sizing and a written, itemized estimate.'],
    ['One-day installation', 'Our licensed crew installs brass fixtures, buried low-voltage wiring and the transformer cleanly, usually in a single day with your beds left as we found them.'],
    ['Night aiming and handoff', 'We return after dark to aim every fixture, set schedules and app controls, and walk you through the system. Then the two-year warranty begins.'],
];
