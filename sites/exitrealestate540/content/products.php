<?php
/**
 * Amazon affiliate product catalog.
 *
 * Each product links to an Amazon search for the exact product name with the
 * Associates tag appended (see amazon_url() in inc/functions.php). Search links
 * never go stale when a listing's ASIN changes. No prices are shown on purpose:
 * Amazon Associates rules forbid displaying prices that are not pulled live.
 *
 * key => [name, group, blurb, query]
 */
defined('ERE') or exit;

return [
    // ---- Storm, flood & hurricane prep ----
    'quick-dam-flood-barrier' => ['Quick Dam Water-Activated Flood Barrier', 'storm', 'Lightweight bags that swell with water in minutes to block doorways and garage openings during street flooding.', 'Quick Dam water activated flood barrier'],
    'midland-weather-radio'   => ['Midland WR120 NOAA Weather Alert Radio', 'storm', 'Loud, battery-backed NOAA alerts that wake you up for tornado, flood and hurricane warnings even when the power and cell service are out.', 'Midland WR120 NOAA weather alert radio'],
    'champion-inverter-generator' => ['Champion Dual-Fuel Inverter Generator', 'storm', 'Runs on gasoline or propane and is quiet and clean enough for a fridge, fans and phone charging after a hurricane knocks out power.', 'Champion dual fuel inverter generator'],
    'heavy-duty-tarp'         => ['Heavy-Duty Waterproof Roof Tarp (20x30)', 'storm', 'Thick, UV-resistant poly tarp for emergency roof coverage - the "reasonable repairs" most policies expect you to make after storm damage.', 'heavy duty waterproof tarp 20x30 roof'],
    'portable-power-station'  => ['Jackery Explorer Portable Power Station', 'storm', 'Silent battery backup for phones, CPAP machines, Wi-Fi routers and lights during outages - safe to run indoors, unlike a generator.', 'Jackery Explorer portable power station'],
    'waterproof-document-bag' => ['Fireproof & Waterproof Document Bag', 'storm', 'Keeps deeds, insurance policies, passports and cash together in one grab-and-go pouch for evacuations.', 'fireproof waterproof document bag'],
    'emergency-crank-radio'   => ['Hand-Crank Emergency Radio with Flashlight', 'storm', 'Solar and hand-crank powered radio, flashlight and phone charger that never needs batteries.', 'hand crank emergency weather radio flashlight phone charger'],

    // ---- Home safety ----
    'first-alert-smoke-co'    => ['First Alert Combination Smoke & Carbon Monoxide Alarm', 'safety', 'One device that covers both smoke and CO - put one on every level and outside every sleeping area.', 'First Alert combination smoke carbon monoxide alarm'],
    'fire-extinguisher-home'  => ['First Alert HOME1 Rechargeable Fire Extinguisher', 'safety', 'A UL-rated ABC extinguisher for the kitchen and garage that handles grease, electrical and ordinary combustible fires.', 'First Alert HOME1 rechargeable fire extinguisher'],
    'fire-escape-ladder'      => ['Two-Story Fire Escape Ladder', 'safety', 'Hooks over a window sill and deploys in seconds - essential for any upstairs bedroom.', 'two story fire escape ladder'],
    'sentrysafe-fireproof'    => ['SentrySafe Fireproof & Waterproof Safe', 'safety', 'UL-rated fire protection and water resistance for the documents you will need after a disaster or at closing.', 'SentrySafe fireproof waterproof safe'],
    'ring-video-doorbell'     => ['Ring Video Doorbell', 'safety', 'See who is at the door from anywhere and keep a recorded history of deliveries and visitors.', 'Ring video doorbell'],
    'schlage-encode-lock'     => ['Schlage Encode Smart Wi-Fi Deadbolt', 'safety', 'Keyless entry with codes you can give and revoke - ideal after buying a home or for rental turnovers.', 'Schlage Encode smart wifi deadbolt'],

    // ---- Leak detection & maintenance tools ----
    'govee-water-sensor'      => ['Govee Wi-Fi Water Leak Detectors (3-Pack)', 'maintenance', 'Phone alerts the moment water shows up under a sink, water heater or washer - catching leaks before they become claims.', 'Govee wifi water leak detector'],
    'moisture-meter'          => ['General Tools Pin-Type Moisture Meter', 'maintenance', 'Confirms whether drywall, wood and subfloors are actually dry after a leak - the same check inspectors and adjusters make.', 'General Tools pin type moisture meter'],
    'outlet-tester'           => ['Klein Tools GFCI Outlet Tester', 'maintenance', 'Checks wiring and GFCI protection in seconds - a five-minute test worth doing at every showing.', 'Klein Tools RT250 GFCI outlet tester'],
    'laser-measure'           => ['Bosch Laser Distance Measure', 'maintenance', 'Accurate room measurements for listings, flooring quotes and documenting damaged areas for a claim.', 'Bosch laser distance measure'],
    'ir-thermometer'          => ['Infrared Thermometer Gun', 'maintenance', 'Finds hidden moisture, poor insulation and failing HVAC vents by spotting temperature differences.', 'infrared thermometer gun home'],
    'wet-dry-vac'             => ['Craftsman Wet/Dry Shop Vacuum', 'maintenance', 'Pulls standing water out fast after a leak or minor flood - the first step in preventing mold.', 'Craftsman wet dry shop vac'],
    'midea-dehumidifier'      => ['Midea Cube Dehumidifier', 'maintenance', 'Houston humidity is relentless; a quality dehumidifier protects closets, bedrooms and drying rooms from mold.', 'Midea cube dehumidifier'],
    'filtrete-air-filters'    => ['Filtrete MERV 11 Air Filters (6-Pack)', 'maintenance', 'Change every 1-3 months in Texas heat to keep your HVAC efficient and your warranty valid.', 'Filtrete MERV 11 air filter 6 pack'],
    'homeowner-tool-kit'      => ['DEWALT Mechanics Tool Set', 'maintenance', 'A solid starter set for the hundred small fixes every new homeowner runs into.', 'DEWALT mechanics tool set'],
    'caulk-gun-sealant'       => ['DAP Kwik Seal Kitchen & Bath Caulk', 'maintenance', 'Re-caulking tubs, sinks and windows is the cheapest water-damage prevention there is.', 'DAP Kwik Seal kitchen bath caulk'],

    // ---- Smart home & efficiency ----
    'nest-thermostat'         => ['Google Nest Learning Thermostat', 'smart', 'Learns your schedule and trims cooling costs - a big deal for Texas summer electric bills.', 'Google Nest Learning Thermostat'],
    'ecobee-thermostat'       => ['ecobee Smart Thermostat Premium', 'smart', 'Room sensors balance hot and cold spots in two-story Texas homes.', 'ecobee smart thermostat premium'],
    'smart-water-shutoff'     => ['Moen Flo Smart Water Monitor & Shutoff', 'smart', 'Monitors your main line and shuts the water off automatically when it detects a leak - some insurers offer discounts for it.', 'Moen Flo smart water monitor shutoff'],

    // ---- Moving & organizing ----
    'moving-boxes-kit'        => ['Moving Boxes Kit with Tape and Markers', 'moving', 'Everything for a weekend pack: mixed-size boxes, tape, markers and labels.', 'moving boxes kit with tape'],
    'furniture-sliders'       => ['Furniture Sliders for Carpet & Hard Floors', 'moving', 'Move couches and dressers without scratching floors or hurting your back.', 'furniture sliders carpet hardwood'],
    'accordion-file-organizer'=> ['Expanding Accordion File Organizer', 'moving', 'One home for your closing disclosure, deed, warranty, inspection report and tax records.', 'expanding accordion file organizer'],
    'label-maker'             => ['Brother P-Touch Label Maker', 'moving', 'Label boxes, breaker panels and storage bins so the new house runs smoothly from day one.', 'Brother P-touch label maker'],
    'document-scanner'        => ['Fujitsu ScanSnap iX1600 Document Scanner', 'moving', 'Scan receipts, policies and contractor estimates into searchable PDFs - indispensable for an insurance claim.', 'ScanSnap iX1600 document scanner'],

    // ---- Books ----
    'book-millionaire-investor' => ['The Millionaire Real Estate Investor - Gary Keller', 'books', 'The classic framework for building wealth through property from the founder of Keller Williams.', 'The Millionaire Real Estate Investor Gary Keller book'],
    'book-rental-property'    => ['The Book on Rental Property Investing - Brandon Turner', 'books', 'A practical, numbers-first guide to buying and managing cash-flowing rentals.', 'The Book on Rental Property Investing Brandon Turner'],
    'book-brrrr'              => ['Buy, Rehab, Rent, Refinance, Repeat - David Greene', 'books', 'The definitive walkthrough of the BRRRR strategy from start to refinance.', 'Buy Rehab Rent Refinance Repeat David Greene book'],
    'book-first-time-buyer'   => ['The First-Time Homebuyer\'s Guide (Latest Edition)', 'books', 'Plain-English walkthrough of budgeting, mortgages, inspections and closing.', 'first time home buyer guide book'],
    'book-house-hacking'      => ['The House Hacking Strategy - Craig Curelop', 'books', 'How to live for free (or close to it) by renting out part of the home you buy.', 'The House Hacking Strategy Craig Curelop book'],
    'book-rich-dad'           => ['Rich Dad Poor Dad - Robert Kiyosaki', 'books', 'The mindset book that got a generation of investors started.', 'Rich Dad Poor Dad book'],
];
