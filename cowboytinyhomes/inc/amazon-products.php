<?php
// Amazon products linked from the site: key => [ASIN, display name, why we recommend it (HTML ok)].
// ASINs checked against live Amazon.com listings on 2026-11-04. If a listing dies, swap the ASIN here.

const AMAZON_PRODUCTS = [
    // --- Towing, parking & hookups (tiny homes on wheels, park models) ---
    'leveler'      => ['B01LYQ1Z8S', 'Andersen Camper Leveler (2-pack)', 'Curved ramp levelers: pull on, chock, done. Rated well past the weight of a tandem-axle tiny home and far faster than stacking boards.'],
    'x-chock'      => ['B002XLHUQG', 'BAL X-Chock Wheel Stabilizers (pair)', 'Locks between tandem tires so the home does not rock when you walk across the floor. The single best fix for that "parked RV" feeling.'],
    'tpms'         => ['B082QJ7H1R', 'TireMinder i10 Tire Pressure Monitoring System', 'Real-time tire pressure and temperature for every trailer tire. Cheap insurance when you are towing a 10,000+ lb house down I-35.'],
    'surge-50'     => ['B00IACGFOA', 'Surge Guard 50 Amp Portable Surge Protector', 'Plugs in at the pedestal and checks for miswired or failing park power before it reaches your mini-split and appliances.'],
    'surge-smart'  => ['B015Y9A4HU', 'Progressive Industries SSP-50XL Smart Surge Protector', 'Weatherproof 50-amp surge protector with a fault display, a favorite for long-term RV park and community sites.'],
    'water-hose'   => ['B004ME11FS', 'Camco TastePURE 25 ft Drinking Water Hose', 'Lead-free, drinking-water-safe hose for your fresh-water hookup. Never fill a home from a garden hose.'],
    'sewer-kit'    => ['B01HPHR30U', 'Camco RhinoFLEX 20 ft RV Sewer Hose Kit', 'The standard sewer connection kit for RV-style hookups, with swivel fittings and storage caps.'],
    'blocks'       => ['B072VSBLH7', 'Camco RV Leveling Blocks (interlocking)', 'Stackable blocks for leveling side to side and for putting under tongue jacks and stabilizers on soft ground.'],
    'pressure-reg' => ['B003BZD08U', 'Camco Brass RV Water Pressure Regulator', 'Park water pressure can spike well above what PEX fittings and fixtures like. This screws on at the spigot and holds it in a safe range.'],
    'inline-filter'=> ['B0006IX87S', 'Camco TastePURE RV Inline Water Filter', 'Cuts chlorine taste and sediment from campground water before it reaches your tank or plumbing.'],

    // --- Heat, humidity & efficiency ---
    'radiant'      => ['B0022NH3E4', 'Reflectix Bubble Pack Foil Insulation (24 in x 25 ft)', 'Reflective foil insulation for roof decks, sheds, doors and window inserts. Works best with an air gap facing the foil.'],
    'mini-split'   => ['B00UV3LGUE', 'Senville LETO 12,000 BTU Mini Split Heat Pump', 'A well-reviewed 12k BTU inverter mini-split, a common size for a 300–500 sq ft tiny home or casita. Have it sized and installed by a licensed HVAC tech.'],
    'hygrometer'   => ['B0872ZWV8X', 'Govee WiFi Thermometer Hygrometer', 'Logs indoor temperature and humidity to your phone, with alerts. Keep it below about 50–55% RH to head off mold.'],
    'dehumidifier' => ['B06X9MFTZZ', 'hOmeLabs 32 Pint Dehumidifier', 'A compact dehumidifier sized for a small home. Helpful on the Gulf Coast and in shoulder seasons when the mini-split barely runs.'],
    'window-ac'    => ['B0FDQLNGHZ', 'Midea U-Shaped Smart Inverter Window AC (10,000 BTU)', 'A quiet inverter window unit that lets the window still open. A good stopgap for a workshop or office casita before a mini-split goes in.'],
    'window-film'  => ['B01GV0U9SK', 'Gila Heat Control Window Film (3 ft x 15 ft)', 'DIY film that cuts solar heat and glare through existing west- and south-facing glass.'],
    'sun-shade'    => ['B07WX571MW', 'Coolaroo Exterior Roller Shade', 'Stops sun on the outside of the glass, which is far more effective than any interior blind. Great on porches and west windows.'],

    // --- Off-grid, water & cooking ---
    'solar-kit'        => ['B00BCRG22A', 'Renogy 200W 12V Solar Starter Kit', 'A small, proven kit for lights, fans and device charging on a weekend cabin or as a first step toward off-grid power.'],
    'composting-toilet'=> ['B009Z7EKIC', "Nature's Head Self-Contained Composting Toilet", 'The composting toilet we see most in tiny homes and cabins. Check county rules before relying on one instead of septic.'],
    'tankless'         => ['B01NAUZJPE', 'Rheem RTEX-13 Electric Tankless Water Heater', 'Compact 240V tankless unit that frees up the closet a tank would take. Needs a dedicated circuit; let your electrician size it.'],
    'induction'        => ['B0045QEPYM', 'Duxtop 1800W Portable Induction Cooktop', 'Puts heat into the pan, not the room — a real advantage in a small Texas kitchen in July.'],

    // --- Safety ---
    'smoke-co'     => ['B086S4Y9H5', 'Kidde Hardwired Smoke & Carbon Monoxide Alarm', 'Hardwired, interconnectable combo alarm with battery backup, the type new construction calls for. Essential with propane or a loft bedroom.'],
    'extinguisher' => ['B01LTICQYE', 'First Alert Home Fire Extinguisher', 'Keep one mounted near the kitchen and the door. In a small home, a kitchen fire spreads fast.'],

    // --- Storage & space-saving ---
    'barn-door'      => ['B06XSB6VHF', 'WINSOON Sliding Barn Door Hardware Kit (6 ft)', 'Heavy-duty black track and rollers for a single barn door. Frees the floor space a swinging door needs.'],
    'pocket-door'    => ['B0026SZ6X0', 'Johnson Hardware 1500 Pocket Door Frame Kit', 'The commercial-grade pocket door frame builders trust. The door disappears into the wall entirely.'],
    'sink-organizer' => ['B0CFQFMC4F', 'REALINN Pull-Out Under Sink Organizer', 'Two-tier pull-out shelves that work around the drain pipes and make the cabinet under the sink usable.'],
    'cabinet-lights' => ['B01L6W7F3U', 'Litever Under Cabinet LED Lighting Kit', 'Plug-in or hardwired LED strips that light the counter and make a small kitchen feel bigger and brighter.'],
    'sofa-bed'       => ['B077H7PW7J', 'Zinus Suzanne Daybed with Trundle', 'A sofa by day and twin beds at night. One of the most flexible pieces you can put in a casita or tiny home living room.'],

    // --- Casita & rental ---
    'smart-lock'   => ['B07HXFKMYR', 'Schlage Encode Smart WiFi Deadbolt', 'Keyless entry with codes you can create and delete from your phone — ideal for guests, tenants and short-term rentals.'],
    'doorbell'     => ['B0FHJ7TKZM', 'Ring Battery Doorbell', 'A wire-free video doorbell for a casita entry, so you can see who is at the back unit from the main house.'],
    'ceiling-fan'  => ['B085W5RRJF', 'Hunter Swanson 44" Ceiling Fan with LED Light', 'A small-room fan that suits tiny home and casita ceilings and lets you set the thermostat a few degrees higher.'],

    // --- Porch & western style ---
    'rocker'        => ['B079VYGVVC', 'POLYWOOD Vineyard Porch Rocker', 'Made in the USA from recycled HDPE lumber. It will not rot, splinter or need paint after a Texas summer.'],
    'string-lights' => ['B00WVOV3W2', 'Brightech Ambience Pro 48 ft Outdoor String Lights', 'Weatherproof, dimmable Edison-style string lights for the porch that make evenings outside feel like a room.'],
    'outdoor-fan'   => ['B01CDG0UA8', 'Hunter Cassius 52" Indoor/Outdoor Ceiling Fan', 'An indoor/outdoor fan for a covered porch. Moving air makes a shaded porch usable on August evenings.'],
    'griddle'       => ['B076MFM8LX', 'Blackstone 22" Tabletop Griddle', 'Cook outside and keep the heat out of a small kitchen. Fits on a porch rail table or a tailgate.'],
    'cast-iron'     => ['B00006JSUB', 'Lodge 12" Cast Iron Skillet', 'One pan that does nearly everything — the most useful thing you can put in a tiny kitchen, and very much at home in a ranch-style one.'],
    'cowhide'       => ['B01CO67JV0', 'Genuine Brindle Cowhide Rug (6 x 7 ft)', 'A real cowhide adds warmth and a western note to a small floor without the visual weight of a patterned rug.'],

    // --- Planning, tools & books ---
    'laser-measure'   => ['B0C76CPGC7', 'Bosch GLM100-23 Laser Distance Measure', 'Measures a room or a lot line in seconds and calculates area. Makes your sketches far more accurate.'],
    'architect-scale' => ['B07QWRG5G7', 'Aluminum Triangular Architect Scale Ruler', 'Read plans and sketch to scale. A $10 tool that makes conversations with your designer much easier.'],
    'drill-kit'       => ['B00IJ0ALYS', 'DEWALT 20V MAX Drill and Impact Driver Kit', 'The workhorse combo kit for any owner-builder or weekend upgrade project.'],
    'book-simple-shelter' => ['0936070528', 'Tiny Homes: Simple Shelter by Lloyd Kahn', 'Hundreds of real small homes in photos. Our favorite book for sparking ideas.'],
    'book-design-guide'   => ['0997288701', 'Tiny House Design & Construction Guide by Dan Louche', 'A clear, technical walkthrough of how a tiny house on wheels is framed, wired and plumbed.'],
    'book-big-tiny'       => ['014218179X', 'The Big Tiny by Dee Williams', 'A memoir of building and living in a tiny house — the honest read on whether tiny living suits you.'],
    'book-microshelters'  => ['1612123538', 'Microshelters by Derek Diedricksen', '59 creative cabins, tiny houses and backyard retreats with plenty of design detail.'],
];
