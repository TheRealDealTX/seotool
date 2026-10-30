<?php
// Cowboy Tiny Homes - Texas house plan catalog.
//
// Geometry is in feet. W runs left to right on the drawings (the long side), D runs front
// to back; y = 0 is the front wall. 'rooms' tile the main-floor footprint exactly, 'upper'
// tiles the second floor (same footprint), 'loft' areas sit above the main floor and
// 'porch' [x, y, w, d] sits outside the footprint (y < 0 front, y = D rear, x = W right side).
// A room labeled PORCH or BREEZEWAY is open, covered space inside the footprint and is left
// out of the heated square footage. A STAIR room appears on both floors; it climbs toward
// +x / +y, or the other way when 'stair_reverse' is set.
//
// generator/build.py turns each entry into the full plan set; validate.php checks the tiling,
// square footage and copy. 'type' (house | adu | studio | park-model | thow) picks the code
// notes on the cover sheet; 'category' is the catalog filter.
//
// Room entry: [label, x, y, w, d]  (x/y from the top-left corner of the footprint)

const PLAN_CATEGORIES = [
    'single' => 'Small homes',
    'adu'    => 'ADUs & casitas',
    'park'   => 'Park models',
    'thow'   => 'Tiny homes on wheels',
    'studio' => 'Studios & offices',
];

const SLAB = 'Stiffened slab-on-grade for expansive clay (verify with a geotechnical report)';

$PLANS = [
    // ---- Small single-family homes on a foundation ------------------------------------
    'comal-cottage' => [
        'name' => 'The Comal Cottage', 'title' => 'The Comal Cottage: 20 x 28 Texas Farmhouse Cottage Plan with Front Porch',
        'price' => 895, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 28, 'D' => 20,
        'type' => 'house', 'category' => 'single', 'styles' => ['Farmhouse'],
        'ceiling' => "9' flat", 'roof' => '8:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement board-and-batten siding', 'foundation' => SLAB,
        'rooms' => [['LIVING', 0, 0, 14, 11], ['KITCHEN / DINING', 14, 0, 14, 11], ['BEDROOM', 0, 11, 12, 9], ['HALL', 12, 11, 3, 9], ['BATH', 15, 11, 7, 9], ['LAUNDRY', 22, 11, 6, 9]],
        'porch' => [0, -8, 28, 8],
        'features' => ['8 ft deep covered porch across the whole front', 'Open living room and eat-in kitchen', 'Laundry room with its own back door', 'Bedroom and bath off a short hall, away from the front door', 'Standing-seam metal roof and board-and-batten siding'],
        'intro' => 'The Comal Cottage is a 560 sq ft farmhouse cottage plan with one bedroom, one bath and an 8 ft covered porch across the front, on a 20 x 28 ft slab. It suits a first home, a retirement place on a few acres or a weekend house near the river.',
        'layout' => ['The front door opens from the porch into a living room that flows straight into the eat-in kitchen.', 'A short hall at the back leads to the bedroom and the bath, so guests never walk through private space.', 'The laundry room has a back door for muddy boots and a place for the water heater and panel.', 'Every room has a window on an outside wall, and the porch shades the front windows all summer.'],
        'texas' => 'Face the porch south or east and it blocks the high summer sun from the living-room windows while letting low winter sun in.',
    ],
    'bandera' => [
        'name' => 'The Bandera', 'title' => 'The Bandera: 24 x 32 Hill Country Stone and Metal House Plan, 2 Bedrooms',
        'price' => 1045, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 32, 'D' => 24,
        'type' => 'house', 'category' => 'single', 'styles' => ['Hill Country'],
        'ceiling' => "9' flat", 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, board-and-batten siding with stone wainscot', 'foundation' => SLAB,
        'rooms' => [['LIVING', 0, 0, 16, 13], ['KITCHEN / DINING', 16, 0, 16, 13], ['BEDROOM 1', 0, 13, 12, 11], ['HALL', 12, 13, 10, 4], ['BATH', 12, 17, 6, 7], ['LAUNDRY', 18, 17, 4, 7], ['BEDROOM 2', 22, 13, 10, 11]],
        'porch' => [0, -8, 32, 8],
        'features' => ['Hill Country look: stone wainscot, board-and-batten and a galvalume standing-seam roof', 'Full-width 8 ft porch', 'Kitchen with an island that seats three', 'Two bedrooms at opposite ends of the house', 'Laundry room next to the bath on one wet wall'],
        'intro' => 'The Bandera is a 768 sq ft Hill Country house plan with two bedrooms, one bath, a stone wainscot, a standing-seam metal roof and a full-width front porch, on a 24 x 32 ft slab.',
        'layout' => ['The porch steps up into a living room that opens to a kitchen with a center island.', 'A short hall behind the kitchen reaches the bath, the laundry room and the second bedroom.', 'The bedrooms sit at opposite back corners, so a guest or roommate gets real privacy.', 'The bath and laundry share one plumbing wall, which keeps the slab rough-in simple.'],
        'texas' => 'Stone wainscot shrugs off Texas splash-back and mower strikes, and the light metal roof reflects summer heat.',
    ],
    'gonzales-modern-living' => [
        'name' => 'Gonzales Modern Living', 'title' => 'Gonzales Modern Living: 2-Bedroom Two-Story Small House Plan',
        'price' => 1000, 'beds' => 2, 'baths' => 1.5, 'floors' => 2, 'W' => 28, 'D' => 16,
        'type' => 'house', 'category' => 'single', 'styles' => ['Modern'],
        'ceiling' => "9' first floor, 8' second floor", 'roof' => '4:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding', 'foundation' => SLAB, 'stair_reverse' => true,
        'rooms' => [['LIVING', 0, 0, 14, 12.5], ['KITCHEN', 14, 0, 14, 12.5], ['POWDER', 0, 12.5, 5, 3.5], ['UTILITY', 5, 12.5, 5, 3.5], ['STAIR', 10, 12.5, 14, 3.5], ['HALL', 24, 12.5, 4, 3.5]],
        'upper' => [['BEDROOM 2', 0, 0, 12, 9], ['STUDY', 12, 0, 6, 9], ['PRIMARY BEDROOM', 18, 0, 10, 9], ['BATH', 0, 9, 6, 7], ['HALL', 6, 9, 15.5, 3.5], ['WIC', 21.5, 9, 6.5, 3.5], ['LANDING', 6, 12.5, 4, 3.5], ['STAIR', 10, 12.5, 14, 3.5], ['WIC STORAGE', 24, 12.5, 4, 3.5]],
        'porch' => [0, -6, 14, 6],
        'features' => ['Two bedrooms and a study upstairs, living spaces down', 'Kitchen island with a two-seat mini bar', 'Powder room on the main floor for guests', 'Walk-in closet off the primary bedroom', 'Covered front patio', 'Small 16 x 28 ft footprint leaves more of your lot for yard and parking'],
        'intro' => 'Gonzales Modern Living is an 896 sq ft two-story small house plan with two bedrooms, a study, a full bath upstairs, a powder room downstairs and a mini bar kitchen, on a compact 16 x 28 ft footprint.',
        'layout' => ['The front patio opens into a living room with room for a sofa and a media wall, flowing into the kitchen.', 'The kitchen island doubles as a two-seat mini bar for breakfast or a quick snack.', 'A straight stair along the back wall climbs to a gallery hall; the powder room and utility room tuck under it.', 'Upstairs, two bedrooms and a study line the front, with the bath over the utility room and a walk-in closet off the primary bedroom.'],
        'texas' => 'Stacking the bedrooms over the living space halves the roof and slab, the two most expensive parts of a Texas build, and puts the bedrooms above street noise.',
    ],
    'pedernales' => [
        'name' => 'The Pedernales', 'title' => 'The Pedernales: 24 x 40 Modern Ranch House Plan with Split Bedrooms',
        'price' => 1095, 'beds' => 2, 'baths' => 2, 'floors' => 1, 'W' => 40, 'D' => 24,
        'type' => 'house', 'category' => 'single', 'styles' => ['Modern ranch'],
        'ceiling' => "9' flat", 'roof' => '4:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding', 'foundation' => SLAB,
        'rooms' => [['PRIMARY BEDROOM', 0, 0, 13, 13], ['PRIMARY BATH', 0, 13, 8, 11], ['WIC', 8, 13, 5, 11], ['LIVING', 13, 0, 14, 14], ['KITCHEN / DINING', 13, 14, 14, 10], ['BEDROOM 2', 27, 0, 13, 12], ['HALL', 27, 12, 13, 4], ['BATH 2', 27, 16, 7, 8], ['LAUNDRY', 34, 16, 6, 8]],
        'porch' => [8, -8, 24, 8],
        'features' => ['Split-bedroom plan: a suite at each end of the house', 'Two full baths, including a primary bath with a tub', 'Walk-in closet in the primary suite', 'Open living room and kitchen in the middle', 'Low 4:12 roof for a long, modern ranch line'],
        'intro' => 'The Pedernales is a 960 sq ft modern ranch house plan with two bedrooms and two full baths in a split-bedroom layout, on a 24 x 40 ft slab with a 24 ft covered front porch.',
        'layout' => ['The living room and kitchen fill the middle of the house, open front to back.', 'The primary suite on the left has its own bath and walk-in closet.', 'A short hall on the right serves the second bedroom, the second bath and the laundry room.', 'With a bath for each bedroom, it works for roommates, a parent who lives with you or a short-term rental.'],
        'texas' => 'The long front faces the street with a 24 ft porch, and a low roof keeps the profile close to the ground the way Texas ranch houses always have.',
    ],
    'llano-dogtrot' => [
        'name' => 'The Llano Dogtrot', 'title' => 'The Llano Dogtrot: Texas Dogtrot House Plan with Open Breezeway',
        'price' => 1195, 'beds' => 2, 'baths' => 1.5, 'floors' => 1, 'W' => 44, 'D' => 24,
        'type' => 'house', 'category' => 'single', 'styles' => ['Dogtrot', 'Farmhouse'],
        'ceiling' => "9' flat", 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, board-and-batten siding', 'foundation' => SLAB,
        'rooms' => [['LIVING', 0, 0, 16, 13], ['KITCHEN', 0, 13, 10, 11], ['POWDER', 10, 13, 6, 5], ['LAUNDRY', 10, 18, 6, 6], ['BREEZEWAY', 16, 0, 12, 24],
                    ['BEDROOM 1', 28, 0, 16, 10], ['HALL', 28, 10, 16, 4], ['BEDROOM 2', 28, 14, 10, 10], ['BATH', 38, 14, 6, 10]],
        'porch' => [0, -8, 44, 8],
        'features' => ['Classic Texas dogtrot: two cabins under one roof with a 12 x 24 ft open breezeway', 'Living cabin with kitchen, powder room and laundry', 'Sleeping cabin with two bedrooms and a full bath', '8 ft porch along the whole front', 'Breezeway works as a shaded outdoor room for most of the year'],
        'intro' => 'The Llano Dogtrot is a 768 sq ft dogtrot house plan with two bedrooms, one and a half baths and a 12 x 24 ft open breezeway between two cabins under one metal roof, plus an 8 ft porch across the 44 ft front.',
        'layout' => ['The living cabin on the left holds the living room, the kitchen, a powder room and the laundry room.', 'The open breezeway in the middle catches the breeze and gives you a shaded outdoor living room.', 'The sleeping cabin on the right has its own door from the breezeway, two bedrooms off a hall and a full bath.', 'Each cabin has its own ductless heat pump, so you only cool the side you are using.'],
        'texas' => 'Dogtrots were Texas air conditioning before air conditioning: the breezeway pulls air through and the shared roof shades both cabins.',
    ],
    'lockhart-farmhouse' => [
        'name' => 'The Lockhart Farmhouse', 'title' => 'The Lockhart Farmhouse: 26 x 46 Three-Bedroom Texas Farmhouse Plan',
        'price' => 1195, 'beds' => 3, 'baths' => 2, 'floors' => 1, 'W' => 46, 'D' => 26,
        'type' => 'house', 'category' => 'single', 'styles' => ['Farmhouse'],
        'ceiling' => "9' flat", 'roof' => '8:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement board-and-batten siding', 'foundation' => SLAB,
        'rooms' => [['PRIMARY BEDROOM', 0, 0, 14, 14], ['PRIMARY BATH', 0, 14, 8, 12], ['WIC', 8, 14, 6, 7], ['LAUNDRY', 8, 21, 6, 5], ['LIVING', 14, 0, 16, 14], ['KITCHEN / DINING', 14, 14, 16, 12],
                    ['BEDROOM 2', 30, 0, 16, 11], ['HALL', 30, 11, 16, 4], ['BEDROOM 3', 30, 15, 9, 11], ['BATH 2', 39, 15, 7, 11]],
        'porch' => [8, -8, 30, 8],
        'features' => ['Three bedrooms and two baths, all on one level', 'Primary suite with walk-in closet and a bath with tub', 'Big eat-in kitchen with an island', '30 ft covered front porch', 'Steep 8:12 metal roof and board-and-batten farmhouse look'],
        'intro' => 'The Lockhart Farmhouse is a 1,196 sq ft single-level farmhouse plan with three bedrooms, two baths, a primary suite and a 30 ft covered front porch, on a 26 x 46 ft slab.',
        'layout' => ['The porch opens into a living room at the center of the house, with the eat-in kitchen behind it.', 'The primary suite fills the left end: bedroom, walk-in closet and a bath with a tub.', 'The laundry room sits between the suite and the kitchen, with a door to the backyard.', 'Two more bedrooms and a second bath share a hall at the right end.'],
        'texas' => 'One level, no stairs: easy for aging in place, and the whole house sits on one simple slab.',
    ],
    'fredericksburg' => [
        'name' => 'The Fredericksburg', 'title' => 'The Fredericksburg: 28 x 40 Hill Country Stone Farmhouse Plan, 3 Bedrooms',
        'price' => 1295, 'beds' => 3, 'baths' => 2, 'floors' => 1, 'W' => 40, 'D' => 28,
        'type' => 'house', 'category' => 'single', 'styles' => ['Hill Country', 'Farmhouse'],
        'ceiling' => "9' flat", 'roof' => '8:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding with stone wainscot', 'foundation' => SLAB,
        'rooms' => [['PRIMARY BEDROOM', 0, 0, 14, 14], ['PRIMARY BATH', 0, 14, 8, 9], ['WIC', 8, 14, 6, 9], ['LAUNDRY', 0, 23, 14, 5], ['LIVING', 14, 0, 14, 15], ['KITCHEN / DINING', 14, 15, 14, 13],
                    ['BEDROOM 2', 28, 0, 12, 12], ['HALL', 28, 12, 12, 4], ['BEDROOM 3', 28, 16, 7, 12], ['BATH 2', 35, 16, 5, 12]],
        'porch' => [0, -10, 40, 10],
        'features' => ['10 ft deep porch across the whole 40 ft front', 'Stone wainscot, lap siding and a steep standing-seam roof', 'Primary suite with walk-in closet', 'Island kitchen with room for a farm table', 'Laundry and mudroom with a back door'],
        'intro' => 'The Fredericksburg is a 1,120 sq ft Hill Country farmhouse plan with three bedrooms, two baths, a stone wainscot and a 10 ft deep porch across the 40 ft front, on a 28 x 40 ft slab.',
        'layout' => ['A wide front porch leads into the living room, with the island kitchen and dining area behind it.', 'The primary suite takes the left side, with a walk-in closet between bedroom and bath.', 'A laundry and mudroom across the back has a door to the yard and room for a sink.', 'Two bedrooms and a second bath share a short hall on the right.'],
        'texas' => 'A 10 ft porch is deep enough for a table and rockers and shades the front rooms from the Hill Country sun.',
    ],
    'brazos' => [
        'name' => 'The Brazos', 'title' => 'The Brazos: 30 x 48 Modern Ranch House Plan with Rear Porch',
        'price' => 1395, 'beds' => 3, 'baths' => 2, 'floors' => 1, 'W' => 48, 'D' => 30,
        'type' => 'house', 'category' => 'single', 'styles' => ['Modern ranch'],
        'ceiling' => "9' flat", 'roof' => '4:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding with stone wainscot', 'foundation' => SLAB, 'entry' => 'front',
        'rooms' => [['PRIMARY BEDROOM', 0, 0, 16, 15], ['PRIMARY BATH', 0, 15, 9, 10], ['WIC', 9, 15, 7, 10], ['MUD / LAUNDRY', 0, 25, 16, 5], ['LIVING', 16, 0, 16, 16], ['KITCHEN / DINING', 16, 16, 16, 14],
                    ['BEDROOM 2', 32, 0, 16, 12], ['HALL', 32, 12, 16, 4], ['BEDROOM 3', 32, 16, 10, 14], ['BATH 2', 42, 16, 6, 14]],
        'porch' => [0, 30, 32, 10],
        'features' => ['Long, low ranch profile with a 4:12 metal roof', '10 x 32 ft covered back porch off the kitchen and mudroom', 'Primary suite with a large walk-in closet', 'Mudroom and laundry at the back door', 'Three bedrooms and two baths on one level'],
        'intro' => 'The Brazos is a 1,440 sq ft modern ranch house plan with three bedrooms, two baths, a mudroom and a 10 x 32 ft covered back porch, on a 30 x 48 ft slab.',
        'layout' => ['The front door opens into a 16 x 16 ft living room with the kitchen and dining area behind it.', 'The mudroom and laundry open straight onto the back porch, where Texas evenings happen.', 'The primary suite fills the left wing with a bath and a 7 x 10 ft walk-in closet.', 'Two bedrooms and a full bath share a hall in the right wing.'],
        'texas' => 'Put the back porch on the east or north side and it is shaded by the house for summer evenings.',
    ],
    'mesquite' => [
        'name' => 'The Mesquite', 'title' => 'The Mesquite: 36 x 48 Barndominium-Style House Plan, 3 Bedrooms',
        'price' => 1495, 'beds' => 3, 'baths' => 2, 'floors' => 1, 'W' => 48, 'D' => 36,
        'type' => 'house', 'category' => 'single', 'styles' => ['Barndominium'],
        'ceiling' => "10' flat", 'plate' => 10, 'roof' => '4:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, vertical metal wall panels with stone wainscot', 'foundation' => SLAB,
        'rooms' => [['PRIMARY BEDROOM', 0, 0, 16, 16], ['PRIMARY BATH', 0, 16, 9, 10], ['WIC', 9, 16, 7, 10], ['PANTRY', 0, 26, 6, 10], ['MUD / LAUNDRY', 6, 26, 10, 10], ['GREAT ROOM', 16, 0, 18, 20], ['KITCHEN / DINING', 16, 20, 18, 16],
                    ['BEDROOM 2', 34, 0, 14, 13], ['HALL', 34, 13, 14, 4], ['BATH 2', 34, 17, 6, 11], ['BEDROOM 3', 40, 17, 8, 11], ['OFFICE', 34, 28, 14, 8]],
        'porch' => [0, -12, 48, 12],
        'features' => ['Barndominium look with metal wall panels, a stone wainscot and 10 ft ceilings', '18 x 20 ft great room', '12 ft deep porch across the whole front', 'Big mudroom and laundry with a walk-in pantry', 'Home office off the kitchen', 'Wood-framed, so it permits and insures like a regular house'],
        'intro' => 'The Mesquite is a 1,728 sq ft barndominium-style house plan with three bedrooms, two baths, an office, a walk-in pantry and a 12 ft deep front porch, on a 36 x 48 ft slab with 10 ft ceilings.',
        'layout' => ['The porch opens into an 18 x 20 ft great room with the kitchen and dining area behind it.', 'A mudroom with laundry and a walk-in pantry connects the kitchen to the back door.', 'The primary suite fills the left side; two bedrooms, a bath and an office fill the right.', 'Wood framing and 2x6 walls give you the barndo look with easier insulation and wiring than a steel shell.'],
        'texas' => 'Metal panels, a metal roof and a deep porch: the ranch-barn look Texans like, built with the insulation a Texas summer needs.',
    ],

    // ---- ADUs, casitas and granny flats ------------------------------------------------
    'alamo-heights-casita' => [
        'name' => 'The Alamo Heights Casita', 'title' => 'The Alamo Heights Casita: 16 x 24 Studio Casita ADU Plan',
        'price' => 695, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 24, 'D' => 16,
        'type' => 'adu', 'category' => 'adu', 'styles' => ['Hill Country'], 'bed_label' => 'Studio',
        'ceiling' => "9' flat", 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding with stone wainscot', 'foundation' => SLAB,
        'rooms' => [['STUDIO', 0, 0, 16, 16], ['KITCHEN', 16, 0, 8, 8], ['BATH + W/D', 16, 8, 8, 8]],
        'porch' => [0, -6, 16, 6],
        'features' => ['Open studio with room for a queen bed and a sitting area', 'Galley kitchen', 'Bath with a stacked washer and dryer', 'Covered entry porch', 'Fits behind most San Antonio and Austin houses'],
        'intro' => 'The Alamo Heights Casita is a 384 sq ft studio casita plan with a galley kitchen, a bath with a stacked washer and dryer and a covered porch, on a 16 x 24 ft slab.',
        'layout' => ['The porch opens into a 16 x 16 ft studio with windows on three sides.', 'The kitchen sits beside the studio along the back of the house.', 'The bath holds a shower, toilet, vanity and a stacked washer and dryer.', 'It works as a guest house, a home office or a long-term rental.'],
        'texas' => 'Small enough for most backyard ADU limits in Texas cities; check yours before you buy.',
    ],
    'king-william-casita' => [
        'name' => 'The King William Casita', 'title' => 'The King William Casita: 20 x 24 One-Bedroom Casita Plan',
        'price' => 795, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 24, 'D' => 20,
        'type' => 'adu', 'category' => 'adu', 'styles' => ['Farmhouse'],
        'ceiling' => "9' flat", 'roof' => '8:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding', 'foundation' => SLAB,
        'rooms' => [['LIVING', 0, 0, 13, 11], ['KITCHEN', 13, 0, 11, 11], ['BEDROOM', 0, 11, 11, 9], ['HALL', 11, 11, 3, 9], ['BATH', 14, 11, 6, 9], ['LAUNDRY', 20, 11, 4, 9]],
        'porch' => [0, -6, 24, 6],
        'features' => ['Separate bedroom with a door', 'Full kitchen', 'Laundry closet with a back door', 'Full-width front porch', 'Steep farmhouse roof in standing-seam metal'],
        'intro' => 'The King William Casita is a 480 sq ft one-bedroom casita plan with a full kitchen, a laundry room and a full-width front porch, on a 20 x 24 ft slab.',
        'layout' => ['The porch opens into a living room beside a full kitchen.', 'A short hall leads to the bath; the bedroom opens off the living room.', 'The laundry room off the kitchen has a back door.', 'A true one-bedroom layout makes it an easy long-term rental or a home for a parent.'],
        'texas' => 'A one-bedroom with its own laundry rents well near downtown San Antonio, Austin and Houston.',
    ],
    'mueller-adu' => [
        'name' => 'The Mueller ADU', 'title' => 'The Mueller ADU: 22 x 30 One-Bedroom Backyard ADU Plan',
        'price' => 895, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 30, 'D' => 22,
        'type' => 'adu', 'category' => 'adu', 'styles' => ['Modern'],
        'ceiling' => "9' flat", 'roof' => '4:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding', 'foundation' => SLAB,
        'rooms' => [['LIVING', 0, 0, 15, 12], ['KITCHEN / DINING', 15, 0, 15, 12], ['BEDROOM', 0, 12, 13, 10], ['HALL', 13, 12, 3, 10], ['BATH', 16, 12, 8, 10], ['LAUNDRY', 24, 12, 6, 10]],
        'porch' => [0, -7, 15, 7],
        'features' => ['Modern one-bedroom ADU with a low metal roof', 'Bath with a tub', 'Laundry room with a back door', 'Eat-in kitchen', 'Covered porch at the entry'],
        'intro' => 'The Mueller ADU is a 660 sq ft modern one-bedroom backyard ADU plan with an eat-in kitchen, a bath with a tub, a laundry room and a covered porch, on a 22 x 30 ft slab.',
        'layout' => ['The porch opens into a living room that flows into the eat-in kitchen.', 'The bedroom, bath and laundry line the back of the house off a short hall.', 'The low 4:12 roof keeps the height down, which helps with ADU height limits.', 'Big enough to live in full time, small enough for most city lots.'],
        'texas' => 'Austin\'s HOME code changes made backyard units like this easier to permit; confirm the current rules for your lot.',
    ],
    'bluebonnet-granny-flat' => [
        'name' => 'The Bluebonnet Granny Flat', 'title' => 'The Bluebonnet Granny Flat: 24 x 32 Accessible Two-Bedroom ADU Plan',
        'price' => 945, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 32, 'D' => 24,
        'type' => 'adu', 'category' => 'adu', 'styles' => ['Farmhouse'],
        'ceiling' => "9' flat", 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding', 'foundation' => SLAB,
        'rooms' => [['LIVING', 0, 0, 16, 13], ['KITCHEN / DINING', 16, 0, 16, 13], ['BEDROOM 1', 0, 13, 11, 11], ['HALL', 11, 13, 10, 5], ['ACCESSIBLE BATH + W/D', 11, 18, 10, 6], ['BEDROOM 2', 21, 13, 11, 11]],
        'porch' => [0, -6, 32, 6],
        'features' => ['No-step entry from the porch (slab set for a 1:20 walk)', 'Roll-in shower in a 10 x 6 ft bath', '5 ft wide hall for wheelchair turning', 'Two bedrooms: one for a caregiver or guest', 'Stacked washer and dryer in the bath'],
        'intro' => 'The Bluebonnet Granny Flat is a 768 sq ft accessible ADU plan with two bedrooms, a roll-in shower, a 5 ft wide hall and a no-step porch entry, on a 24 x 32 ft slab.',
        'layout' => ['The porch meets the floor with no step, and the front door opens into an open living room and kitchen.', 'A 5 ft wide hall gives a wheelchair room to turn between the bedrooms and the bath.', 'The bath has a curbless roll-in shower, a stacked washer and dryer and room for grab bars.', 'The second bedroom suits a caregiver, a grandchild or a home office.'],
        'texas' => 'Built for a parent to age in place next to family; set doors at 36 in. and add grab-bar blocking during framing.',
        'code_notes' => ['Accessibility: these drawings follow common universal-design dimensions (36 in. doors, 5 ft turning space, curbless shower). They are not certified to ANSI A117.1 or the Texas Accessibility Standards; confirm any program or lender requirements.'],
    ],
    'bishop-arts-adu' => [
        'name' => 'The Bishop Arts ADU', 'title' => 'The Bishop Arts ADU: 20 x 24 Two-Story Garage-Free ADU Plan',
        'price' => 995, 'beds' => 2, 'baths' => 1.5, 'floors' => 2, 'W' => 24, 'D' => 20,
        'type' => 'adu', 'category' => 'adu', 'styles' => ['Modern'],
        'ceiling' => "9' first floor, 8' second floor", 'roof' => '4:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding', 'foundation' => SLAB, 'stair_reverse' => true,
        'rooms' => [['LIVING', 0, 0, 12, 16.5], ['KITCHEN', 12, 0, 12, 16.5], ['POWDER', 0, 16.5, 6, 3.5], ['STAIR', 6, 16.5, 14, 3.5], ['HALL', 20, 16.5, 4, 3.5]],
        'upper' => [['BEDROOM 1', 0, 0, 10, 12.5], ['BATH + W/D', 10, 0, 5, 12.5], ['BEDROOM 2', 15, 0, 9, 16.5], ['HALL', 0, 12.5, 15, 4], ['LANDING', 0, 16.5, 6, 3.5], ['STAIR', 6, 16.5, 14, 3.5], ['CLOSET', 20, 16.5, 4, 3.5]],
        'features' => ['Two bedrooms on a 480 sq ft footprint', 'Open kitchen with an island downstairs', 'Powder room downstairs, full bath with laundry upstairs', 'Small footprint for tight urban lots', 'Low 4:12 roof to keep the overall height down'],
        'intro' => 'The Bishop Arts ADU is a 960 sq ft two-story ADU plan with two bedrooms, one and a half baths and an island kitchen on a small 20 x 24 ft footprint.',
        'layout' => ['The ground floor is one open room: living area and an island kitchen, with a powder room under the stair.', 'A straight stair along the back wall leads up to a hall that serves both bedrooms and the bath.', 'The upstairs bath includes a stacked washer and dryer.', 'Two bedrooms on a small footprint make it a strong rental where your city allows a two-story accessory unit.'],
        'texas' => 'Many Texas cities cap ADU height or floor area; check whether yours allows a two-story unit before you buy.',
    ],
    'magnolia-guest-house' => [
        'name' => 'The Magnolia Guest House', 'title' => 'The Magnolia Guest House: 28 x 36 Two-Bedroom, Two-Bath Guest House Plan',
        'price' => 1045, 'beds' => 2, 'baths' => 2, 'floors' => 1, 'W' => 36, 'D' => 28,
        'type' => 'adu', 'category' => 'adu', 'styles' => ['Farmhouse'],
        'ceiling' => "9' flat", 'roof' => '8:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement board-and-batten siding', 'foundation' => SLAB,
        'rooms' => [['BEDROOM 1', 0, 0, 12, 13], ['BATH 1', 0, 13, 7, 9], ['WIC', 7, 13, 5, 9], ['LAUNDRY', 0, 22, 12, 6], ['LIVING', 12, 0, 14, 14], ['KITCHEN / DINING', 12, 14, 14, 14],
                    ['BEDROOM 2', 26, 0, 10, 12], ['HALL', 26, 12, 10, 4], ['BATH 2', 26, 16, 5, 12], ['FLEX / OFFICE', 31, 16, 5, 12]],
        'porch' => [0, -8, 36, 8],
        'features' => ['A bedroom and full bath at each end', 'Flex room for an office or nursery', 'Island kitchen with dining space', 'Laundry room with a back door', '8 ft porch across the whole front'],
        'intro' => 'The Magnolia Guest House is a 1,008 sq ft guest house plan with two bedrooms, two full baths, a flex room and an 8 ft front porch, on a 28 x 36 ft slab.',
        'layout' => ['The living room and island kitchen fill the center of the house.', 'The left suite has a walk-in closet and its own bath; the laundry room is behind it.', 'The right side has the second bedroom, a second bath and a flex room off a short hall.', 'Big enough to be the main house on a small lot, or a guest house that guests never want to leave.'],
        'texas' => 'Two full suites make it a natural multigenerational home on a Texas acreage.',
    ],

    // ---- Park models (RVs under ANSI A119.5) --------------------------------------------
    'guadalupe-park-model' => [
        'name' => 'The Guadalupe', 'title' => 'The Guadalupe: 12 x 33 Park Model Home Plan with Porch',
        'price' => 595, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 33, 'D' => 12,
        'type' => 'park-model', 'category' => 'park', 'styles' => ['Cabin'],
        'ceiling' => "8' flat", 'plate' => 8, 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, board-and-batten siding', 'foundation' => 'Steel chassis on piers (ANSI A119.5 park model)',
        'rooms' => [['BEDROOM', 0, 0, 10, 12], ['BATH + W/D', 10, 0, 6, 8], ['HALL', 10, 8, 6, 4], ['KITCHEN', 16, 0, 8, 12], ['LIVING', 24, 0, 9, 12]],
        'porch' => [16, -8, 17, 8],
        'features' => ['396 sq ft: under the 400 sq ft park model limit', 'Separate bedroom with a door', 'Full kitchen and a bath with a stacked washer and dryer', '8 x 17 ft covered porch', 'Built on a steel chassis for RV parks and rural land'],
        'intro' => 'The Guadalupe is a 396 sq ft park model plan with one bedroom, a full kitchen, a bath with laundry and an 8 x 17 ft covered porch, built on a steel chassis under the ANSI A119.5 400 sq ft limit.',
        'layout' => ['The porch opens into a living room at one end, next to a full kitchen.', 'A short hall past the kitchen leads to the bath and the bedroom at the far end.', 'The bath includes a stacked washer and dryer.', 'At 12 ft wide it moves on a permitted wide load and sets up in an RV park or on rural land.'],
        'texas' => 'Park models are popular along the Guadalupe and Frio rivers and in Hill Country RV resorts; check the park\'s rules before you build.',
    ],
    'medina-park-model' => [
        'name' => 'The Medina', 'title' => 'The Medina: 12 x 40 Two-Bedroom Park Model Plan with Inset Porch',
        'price' => 625, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 40, 'D' => 12,
        'type' => 'park-model', 'category' => 'park', 'styles' => ['Cabin'],
        'ceiling' => "8' flat", 'plate' => 8, 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, board-and-batten siding', 'foundation' => 'Steel chassis on piers (ANSI A119.5 park model)',
        'rooms' => [['BUNK ROOM', 0, 0, 7, 12], ['LIVING', 7, 0, 7, 12], ['PORCH', 14, 0, 12, 7], ['KITCHEN', 14, 7, 12, 5], ['BATH', 26, 0, 5, 6], ['HALL', 26, 6, 5, 6], ['BEDROOM', 31, 0, 9, 12]],
        'features' => ['Two bedrooms in 396 sq ft: a queen bedroom and a bunk room', '12 x 7 ft porch set into the front under the main roof', 'Kitchen along the back wall behind the porch', 'Bedrooms at opposite ends for privacy', 'Built on a steel chassis'],
        'intro' => 'The Medina is a 396 sq ft two-bedroom park model plan with a bunk room, a queen bedroom and a 12 x 7 ft porch set into the front under the main roof, on a 12 x 40 ft steel chassis.',
        'layout' => ['The inset porch opens into the living room; the kitchen runs along the back wall behind the porch.', 'A bunk room for two kids or guests sits at the left end, off the living room.', 'The bath and a short hall lead to the queen bedroom at the right end.', 'The porch is under the main roof, so it adds no extra framing or footprint.'],
        'texas' => 'A family weekend place for a lake lot or a ranch: sleeps four without a loft.',
    ],
    'frio-park-model' => [
        'name' => 'The Frio', 'title' => 'The Frio: 13.5 x 29.5 Park Model Plan with Sleeping Loft and Porch',
        'price' => 645, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 29.5, 'D' => 13.5,
        'type' => 'park-model', 'category' => 'park', 'styles' => ['Cabin'], 'bed_label' => '1 bed + loft',
        'ceiling' => "8' flat, sloped in loft", 'plate' => 8, 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, board-and-batten siding', 'foundation' => 'Steel chassis on piers (ANSI A119.5 park model)',
        'rooms' => [['BEDROOM', 0, 0, 10, 13.5], ['BATH', 10, 0, 6, 8.5], ['HALL', 10, 8.5, 6, 5], ['KITCHEN', 16, 0, 6.5, 13.5], ['LIVING', 22.5, 0, 7, 13.5]],
        'loft' => [['SLEEPING LOFT', 10, 0, 6, 13.5]],
        'porch' => [16, -8, 13.5, 8],
        'features' => ['398 sq ft main floor plus an 81 sq ft sleeping loft', 'Queen bedroom on the main floor', 'Loft over the bath for kids or guests', 'Covered porch off the living room', 'Built on a steel chassis'],
        'intro' => 'The Frio is a 479 sq ft park model plan: a 398 sq ft main floor with a queen bedroom, a full kitchen and bath, plus an 81 sq ft sleeping loft and a covered porch, on a 13.5 x 29.5 ft steel chassis.',
        'layout' => ['The porch opens into the living room next to a galley kitchen.', 'A short hall leads to the bath and the queen bedroom at the far end.', 'A ladder reaches the sleeping loft over the bath and hall.', 'The main floor stays under 400 sq ft; under ANSI A119.5 the loft is not counted.'],
        'texas' => 'The loft is the cool-off spot for kids after a day on the river; the ceiling fan and mini-split head keep it livable.',
    ],

    // ---- Tiny homes on wheels -----------------------------------------------------------
    'maverick-tiny-house' => [
        'name' => 'The Maverick', 'title' => 'The Maverick: 20 ft Bumper-Pull Tiny House on Wheels Plan with Loft',
        'price' => 395, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 20, 'D' => 8.5, 'mobile' => true,
        'type' => 'thow', 'category' => 'thow', 'styles' => ['Bumper pull'],
        'height' => "13' 6\"", 'ceiling' => "6' 8\" under loft, 11' at living", 'roof' => 'Gable 4:12, standing-seam metal', 'roof_type' => 'thow',
        'walls' => '2x4 wood framing, board-and-batten siding', 'foundation' => '20 ft bumper-pull tiny house trailer',
        'rooms' => [['BATH', 0, 0, 5, 8.5], ['KITCHEN', 5, 0, 7, 8.5], ['LIVING', 12, 0, 8, 8.5]],
        'loft' => [['SLEEPING LOFT', 0, 0, 8, 8.5]],
        'features' => ['Road-legal in Texas at 8 ft 6 in. wide and 13 ft 6 in. high', 'Queen sleeping loft', 'Galley kitchen and a full bath', 'Light enough for a 10,000 lb trailer and a 3/4-ton truck', 'Standing-seam metal roof'],
        'intro' => 'The Maverick is a 238 sq ft bumper-pull tiny house on wheels plan: 170 sq ft on the main floor plus a 68 sq ft queen sleeping loft, on a 20 ft trailer that stays road-legal in Texas without a permit.',
        'layout' => ['The bath sits at the hitch end over the axles, away from the door.', 'The galley kitchen runs along both walls under the loft.', 'The living room at the back gets the full roof height and tall windows.', 'A ladder or storage stair reaches the queen loft.'],
        'texas' => 'Titled and registered as a trailer with TxDMV; a 20 ft house tows easily to a ranch, a lake lot or a tiny home community.',
    ],
    'wrangler-tiny-house' => [
        'name' => 'The Wrangler', 'title' => 'The Wrangler: 26 ft Bumper-Pull Tiny House Plan with Two Lofts',
        'price' => 445, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 26, 'D' => 8.5, 'mobile' => true,
        'type' => 'thow', 'category' => 'thow', 'styles' => ['Bumper pull'],
        'height' => "13' 6\"", 'ceiling' => "6' 8\" under lofts", 'roof' => 'Gable 4:12, standing-seam metal', 'roof_type' => 'thow',
        'walls' => '2x4 wood framing, board-and-batten siding', 'foundation' => '26 ft bumper-pull tiny house trailer',
        'rooms' => [['LIVING', 0, 0, 8, 8.5], ['KITCHEN', 8, 0, 8, 8.5], ['BATH', 16, 0, 5, 8.5], ['UTILITY', 21, 0, 5, 8.5]],
        'loft' => [['LOFT 1', 0, 0, 7, 8.5], ['LOFT 2', 16, 0, 10, 8.5]],
        'features' => ['Two sleeping lofts for a couple plus a child or guest', 'Utility room for washer, water heater and panel', 'Center kitchen with the best light in the house', 'Road-legal width and height in Texas', 'Bumper-pull hitch fits a 3/4-ton truck'],
        'intro' => 'The Wrangler is a 366 sq ft tiny house on wheels plan with two sleeping lofts, a center kitchen and a utility room: 221 sq ft on the main floor plus 145 sq ft of lofts on a 26 ft bumper-pull trailer.',
        'layout' => ['The living room sits under the smaller loft at the hitch end.', 'The kitchen in the middle gets the full roof height.', 'Storage stairs climb to the primary loft over the bath and utility room.', 'The utility room keeps the washer, water heater and panel out of the living space.'],
        'texas' => 'At 26 ft and under about 12,000 lb loaded, it stays within normal Texas towing rules for a heavy-duty pickup.',
    ],
    'rodeo-gooseneck' => [
        'name' => 'The Rodeo', 'title' => 'The Rodeo: 30 ft Gooseneck Tiny House Plan with Step-Up Bedroom',
        'price' => 545, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 30, 'D' => 8.5, 'mobile' => true,
        'type' => 'thow', 'category' => 'thow', 'styles' => ['Gooseneck'],
        'height' => "13' 6\"", 'ceiling' => "6' 6\" in gooseneck bedroom, 11' main", 'roof' => 'Gable 4:12, standing-seam metal', 'roof_type' => 'gooseneck',
        'walls' => '2x4 wood framing, board-and-batten siding', 'foundation' => '30 ft gooseneck trailer',
        'rooms' => [['LIVING', 0, 0, 10, 8.5], ['KITCHEN', 10, 0, 7, 8.5], ['BATH', 17, 0, 5, 8.5], ['GOOSENECK BEDROOM', 22, 0, 8, 8.5]],
        'features' => ['Step-up queen bedroom over the gooseneck, no ladder', 'Gooseneck hitch tows steadier than a bumper pull', 'Long galley kitchen', 'Full bath between the kitchen and bedroom', '255 sq ft on one level plus steps'],
        'intro' => 'The Rodeo is a 255 sq ft gooseneck tiny house plan with a step-up queen bedroom over the hitch, a galley kitchen and a full bath on a 30 ft gooseneck trailer.',
        'layout' => ['A few steps lead up to the gooseneck bedroom, which fits a queen bed under a lower ceiling.', 'The bath sits between the kitchen and the bedroom on one wet wall.', 'The living room at the back has the full 11 ft ceiling and a glass door.', 'No ladder anywhere: good for anyone who would rather not climb.'],
        'texas' => 'A gooseneck rides on the truck bed, the way Texans already haul horse and stock trailers.',
    ],
    'big-bend-gooseneck' => [
        'name' => 'The Big Bend', 'title' => 'The Big Bend: 36 ft Gooseneck Tiny House Plan with Bedroom and Loft',
        'price' => 595, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 36, 'D' => 8.5, 'mobile' => true,
        'type' => 'thow', 'category' => 'thow', 'styles' => ['Gooseneck'],
        'height' => "13' 6\"", 'ceiling' => "6' 6\" in gooseneck bedroom, 11' main", 'roof' => 'Gable 4:12, standing-seam metal', 'roof_type' => 'gooseneck',
        'walls' => '2x4 wood framing, board-and-batten siding', 'foundation' => '36 ft gooseneck trailer',
        'rooms' => [['LIVING', 0, 0, 10, 8.5], ['KITCHEN', 10, 0, 8, 8.5], ['BATH', 18, 0, 6, 8.5], ['UTILITY', 24, 0, 4, 8.5], ['GOOSENECK BEDROOM', 28, 0, 8, 8.5]],
        'loft' => [['LOFT', 18, 0, 10, 8.5]],
        'features' => ['Step-up gooseneck bedroom plus a sleeping loft', 'Utility room with laundry', '8 ft kitchen along both walls', 'Big living room at the back', 'Note: a loaded 36 ft house can top 14,000 lb; plan the truck and license to match'],
        'intro' => 'The Big Bend is a 391 sq ft gooseneck tiny house plan: 306 sq ft on the main floor with a step-up bedroom and a utility room, plus an 85 sq ft loft, on a 36 ft gooseneck trailer.',
        'layout' => ['The step-up bedroom sits over the gooseneck; the loft over the bath and utility room sleeps two more.', 'The utility room holds the washer, water heater and panel.', 'An 8 ft kitchen runs along both walls between the living room and the bath.', 'The living room at the back has full ceiling height and a glass door.'],
        'texas' => 'Combined weight over 26,000 lb with a trailer over 10,000 lb needs a Class A license in Texas; most owners move a house this size with a hired hauler.',
    ],

    // ---- Backyard studios and offices ---------------------------------------------------
    'hill-country-studio' => [
        'name' => 'The Hill Country Studio', 'title' => 'The Hill Country Studio: 12 x 16 Backyard Office and Studio Plan',
        'price' => 295, 'beds' => 0, 'baths' => 0, 'floors' => 1, 'W' => 16, 'D' => 12,
        'type' => 'studio', 'category' => 'studio', 'styles' => ['Hill Country'],
        'ceiling' => "9' flat", 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, board-and-batten siding with stone wainscot', 'foundation' => SLAB,
        'rooms' => [['OFFICE', 0, 0, 16, 12]],
        'porch' => [0, -5, 16, 5],
        'features' => ['One open room for an office, art studio or gym', 'Windows on three sides', 'Stone wainscot and metal roof to match a Hill Country house', 'Insulated and conditioned with a small mini-split', 'No plumbing: simpler permit and lower cost'],
        'intro' => 'The Hill Country Studio is a 192 sq ft backyard office and studio plan: one insulated, air-conditioned room with windows on three sides, a stone wainscot and a covered entry, on a 12 x 16 ft slab.',
        'layout' => ['A covered entry opens into one 12 x 16 ft room.', 'Windows on three sides give daylight for work or art.', 'A small ductless heat pump keeps it comfortable in August.', 'With no plumbing it is the cheapest building in the catalog to permit and build.'],
        'texas' => 'Some Texas cities exempt small accessory buildings from a permit and others do not; ask before you pour the slab.',
    ],
    'ranch-office' => [
        'name' => 'The Ranch Office', 'title' => 'The Ranch Office: 12 x 20 Backyard Office Plan with Half Bath',
        'price' => 345, 'beds' => 0, 'baths' => 0.5, 'floors' => 1, 'W' => 20, 'D' => 12,
        'type' => 'studio', 'category' => 'studio', 'styles' => ['Farmhouse'],
        'ceiling' => "9' flat", 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, board-and-batten siding', 'foundation' => SLAB,
        'rooms' => [['OFFICE', 0, 0, 15, 12], ['HALF BATH', 15, 0, 5, 6], ['CLOSET', 15, 6, 5, 6]],
        'porch' => [0, -6, 15, 6],
        'features' => ['15 x 12 ft office for two desks or a meeting table', 'Half bath, so nobody walks back to the house', 'Storage closet for files and supplies', 'Covered porch', 'Point-of-use water heater'],
        'intro' => 'The Ranch Office is a 240 sq ft backyard office plan with a 15 x 12 ft work room, a half bath, a storage closet and a covered porch, on a 12 x 20 ft slab.',
        'layout' => ['The porch opens into the main office room.', 'A half bath and a storage closet share the end wall.', 'A small tankless heater under the sink supplies hot water.', 'Works as a home office, a ranch office or a client meeting room.'],
        'texas' => 'A half bath needs a sewer or septic connection; on rural land, confirm septic capacity first.',
    ],
    'pool-house-studio' => [
        'name' => 'The Pool House Studio', 'title' => 'The Pool House Studio: 16 x 20 Pool House Plan with Shower and Kitchenette',
        'price' => 445, 'beds' => 0, 'baths' => 0.75, 'floors' => 1, 'W' => 20, 'D' => 16,
        'type' => 'studio', 'category' => 'studio', 'styles' => ['Hill Country'],
        'ceiling' => "9' flat", 'roof' => '6:12 gable, standing-seam metal', 'roof_type' => 'gable',
        'walls' => '2x6 wood framing, fiber-cement lap siding with stone wainscot', 'foundation' => SLAB,
        'rooms' => [['LOUNGE', 0, 0, 13, 16], ['KITCHENETTE', 13, 0, 7, 8], ['SHOWER BATH', 13, 8, 7, 8]],
        'porch' => [0, -8, 20, 8],
        'features' => ['Lounge for changing, shade and TV by the pool', 'Shower bath (3/4 bath) so wet feet stay out of the house', 'Kitchenette for drinks and snacks', '8 ft covered porch facing the pool', 'Easy to convert to a guest studio later'],
        'intro' => 'The Pool House Studio is a 320 sq ft pool house plan with a lounge, a shower bath, a kitchenette and an 8 ft covered porch, on a 16 x 20 ft slab.',
        'layout' => ['The porch faces the pool and opens into a 13 x 16 ft lounge.', 'A kitchenette and a shower bath share the back wall.', 'Tile floors in the bath handle wet traffic.', 'Add a bed and it becomes a guest studio.'],
        'texas' => 'A shaded porch, a ceiling fan and a cold drink: the pool house a Texas summer calls for.',
    ],
];

// Fill in derived fields.
foreach ($PLANS as $slug => &$p) {
    $ft = function (float $v): string { $f = (int)floor($v); $in = (int)round(($v - $f) * 12); return $in ? "$f' $in\"" : "$f'"; };
    $p['width'] = $ft($p['W']);   // long side
    $p['depth'] = $ft($p['D']);
    $open = function (array $rooms): float {   // inset porch / breezeway area
        return array_sum(array_map(fn($r) => in_array($r[0], ['PORCH', 'BREEZEWAY'], true) ? $r[3] * $r[4] : 0, $rooms));
    };
    $p['main_sqft'] = (int)round($p['W'] * $p['D'] - $open($p['rooms']));
    $p['upper_sqft'] = isset($p['upper']) ? (int)round($p['W'] * $p['D']) : 0;
    $p['loft_sqft'] = (int)round(array_sum(array_map(fn($r) => $r[3] * $r[4], $p['loft'] ?? [])));
    $p['sqft'] = $p['main_sqft'] + $p['upper_sqft'] + $p['loft_sqft'];
    $p['mobile'] = $p['mobile'] ?? false;
    $p['has_loft'] = !empty($p['loft']);
    if (!isset($p['height'])) {
        // grade to ridge: slab or chassis + walls (+ second floor) + roof rise over half the depth
        preg_match('/(\d+(?:\.\d+)?):12/', $p['roof'], $mm);
        $base = strpos($p['foundation'], 'chassis') !== false ? 2.5 : 0.67;
        $h = $base + ($p['plate'] ?? 9) + (isset($p['upper']) ? 9 : 0) + $p['D'] / 2 * (float)($mm[1] ?? 6) / 12;
        $p['height'] = $ft(round($h * 2) / 2);
    }
    $p['url'] = plan_url($slug);
    $p['ref'] = strncmp($p['name'], 'The ', 4) === 0 ? $p['name'] : 'the ' . $p['name'];   // mid-sentence: "build the Gonzales...", "build The Bandera"
    $p['bed_label'] = $p['bed_label'] ?? ($p['beds'] ? $p['beds'] . ' bed' : 'No bedroom');
    $p['bath_label'] = ['0' => 'No bath', '0.5' => 'Half bath', '0.75' => '3/4 bath'][(string)$p['baths']] ?? ($p['baths'] . ' bath');
    $p['image'] = "/assets/plans/$slug/3d.webp";
}
unset($p);

/** Generated plan-set details (estimate, materials summary, sheets, files) from generator/build.py. */
function plan_sets(): array {
    static $sets = null;
    if ($sets === null) {
        $f = __DIR__ . '/plan-sets.json';
        $sets = is_file($f) ? (json_decode((string)file_get_contents($f), true) ?: []) : [];
    }
    return $sets;
}
