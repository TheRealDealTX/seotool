<?php
// Tiny Homes Blueprint - plan catalog.
//
// Each plan's geometry is in feet. W runs left to right on the drawings (the long side),
// D runs front to back. 'rooms' tile the main-floor footprint exactly; 'loft' areas sit
// above it; 'porch' sits outside it. A room labeled PORCH is a covered porch inset into
// the footprint: it is drawn with the rooms but left out of the heated square footage. build-plans.php draws the floor plan and front
// elevation SVGs (assets/plans/) from this data, and validate.php checks the tiling and
// that sqft = main floor + loft.
//
// Room entry: [label, x, y, w, d]  (x/y from the top-left corner of the footprint)

$PLANS = [
    // Original store plans (photo renderings, no room geometry)
    'plan-12-2418' => [
        'name' => 'Plan 12-2418', 'title' => 'Rustic 3-Bedroom Tiny House Plan with Covered Porch',
        'price' => 550, 'beds' => 3, 'baths' => 2, 'floors' => 2, 'sqft' => 700, 'W' => 38, 'D' => 20,
        'height' => "14' 4\"", 'ceiling' => "9'", 'roof' => '4:12 pitch, truss framing, shingle roof',
        'walls' => '2x6 wood framing, siding and stone exterior', 'foundation' => 'Slab or crawlspace',
        'features' => ['Covered front porch', 'Open living, kitchen and dining', 'Flex room with retractable wall (dining, office or guest room)', 'Main-floor laundry', 'Private bedroom wing', 'Can be flipped to put the porch at the rear'],
        'styles' => ['small-cabin-plans', 'tiny-cottage-plans', 'adu-plans', 'small-farmhouse-plans'],
        'image' => '/assets/img/plan-12-2418.webp', 'roof_type' => 'gable',
        'rooms' => [['PORCH', 0, 0, 14, 10], ['LIVING', 0, 10, 14, 10], ['KITCHEN', 14, 0, 10, 10], ['FLEX ROOM', 14, 10, 10, 10],
                    ['BEDROOM 1', 24, 0, 14, 8], ['BATH 1', 24, 8, 7, 5], ['BATH 2 + W/D', 31, 8, 7, 5], ['BEDROOM 2', 24, 13, 14, 7]],
        'loft' => [['BEDROOM 3 LOFT', 24, 0, 8, 10]],
        'intro' => 'Plan 12-2418 is a rustic 700 sq ft tiny house plan with three bedrooms, two baths and a covered front porch, drawn on a compact 20 x 38 ft footprint. It works as an affordable primary residence, a family vacation cabin or a roomy backyard ADU where zoning allows.',
        'layout' => [
            'The side main entrance opens into an open living area with direct access to the covered front porch, so the porch works as an extra outdoor room in good weather.',
            'The kitchen is large enough for either a dining table or an island, which is rare in a home this size.',
            'Off the living room, a flexible room with a retractable wall can be a formal dining room, a home office or a guest bedroom, and it opens up to the living area when you entertain.',
            'Bedrooms sit at the far end of the house for privacy, and the second floor adds sleeping space without enlarging the footprint.',
            'Laundry is on the main floor, and the plan can be flipped on the lot to put the porch at the rear for a view or for privacy from the road.',
        ],
    ],
    'plan-12-2417' => [
        'name' => 'Plan 12-2417', 'title' => 'Single-Level 2-Bedroom Tiny Cabin Plan',
        'price' => 1050, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'sqft' => 700, 'W' => 38, 'D' => 20,
        'height' => "14' 4\"", 'ceiling' => "9'", 'roof' => '4:12 pitch, truss framing, shingle roof',
        'walls' => '2x6 wood framing, siding and stone exterior', 'foundation' => 'Slab or crawlspace',
        'features' => ['Everything on one floor, no stairs', 'Side entry into an open great room', 'Kitchen sized for a table or island', 'Flex room with retractable wall', 'Full shower bath', 'Main-floor laundry'],
        'styles' => ['small-cabin-plans', 'tiny-cottage-plans', 'adu-plans'],
        'image' => '/assets/img/plan-12-2417.webp', 'roof_type' => 'gable',
        'rooms' => [['PORCH', 0, 0, 12, 5], ['GREAT ROOM', 0, 5, 12, 15], ['KITCHEN', 12, 0, 10, 10], ['FLEX ROOM', 12, 10, 10, 10],
                    ['BEDROOM 1', 22, 0, 16, 8], ['BATH', 22, 8, 8, 5], ['LAUNDRY', 30, 8, 8, 5], ['BEDROOM 2', 22, 13, 16, 7]],
        'intro' => 'Plan 12-2417 is a single-level 700 sq ft tiny cabin plan with two bedrooms and one full bath on a 20 x 38 ft footprint. With everything on one floor and no stairs, it suits full-time living, downsizing and aging in place as well as weekend getaways.',
        'layout' => [
            'A side entry leads into one open great room that combines living, kitchen and dining, with access to the covered front porch.',
            'The flexible kitchen fits a table or an island, so you can choose more prep space or a dedicated dining spot.',
            'A flex room with a retractable wall can be closed off as a guest room or office, or opened up to extend the living area.',
            'Both bedrooms are grouped at the far end of the house for quiet and privacy, sharing a bath with a full shower.',
            'Main-floor laundry and a single level make it easy to live in long-term, and the plan can be flipped to put the porch at the rear.',
        ],
    ],

    // ---- Tiny houses on wheels -------------------------------------------------------
    'plan-12-2419' => [
        'name' => 'Plan 12-2419', 'title' => 'The Wren: 20 ft Tiny House on Wheels with Sleeping Loft',
        'price' => 395, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 20, 'D' => 8.5, 'mobile' => true,
        'height' => "13' 6\"", 'ceiling' => "6' 8\" under loft, 11' at living", 'roof' => 'Gable, standing-seam metal',
        'walls' => '2x4 wood framing, lap siding', 'foundation' => '20 ft flatbed tiny house trailer', 'roof_type' => 'thow',
        'rooms' => [['BATH', 0, 0, 5, 8.5], ['KITCHEN', 5, 0, 7, 8.5], ['LIVING', 12, 0, 8, 8.5]],
        'loft' => [['SLEEPING LOFT', 0, 0, 8, 8.5]],
        'features' => ['Road-legal 8.5 ft width and 13.5 ft height', 'Queen-size sleeping loft over the bath and kitchen', 'Full-height living room with tall windows', 'Galley kitchen with room for a 24 in. range and fridge', 'Bath with 32 in. shower and composting or flush toilet', 'Light enough for a 10,000 lb GVWR trailer'],
        'styles' => ['tiny-house-on-wheels-plans', 'tiny-house-plans-with-loft'],
        'intro' => 'The Wren is a 20 ft tiny house on wheels plan with a queen sleeping loft, a galley kitchen and a full bath packed into 238 sq ft of living space. It is the smallest, lightest and easiest-to-tow plan in the Tiny Homes Blueprint catalog.',
        'layout' => ['The bath sits at the hitch end, keeping plumbing over the trailer axles and away from the door.', 'The galley kitchen runs along both walls under the loft, with the fridge tucked beside the bath wall.', 'The living room at the rear gets the full roof height, so the house never feels cramped.', 'A ladder or alternating-tread stair reaches the 8 x 8.5 ft loft, which fits a queen mattress.'],
    ],
    'plan-12-2420' => [
        'name' => 'Plan 12-2420', 'title' => 'The Finch: 24 ft Tiny House on Wheels with Two Lofts',
        'price' => 445, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 24, 'D' => 8.5, 'mobile' => true,
        'height' => "13' 6\"", 'ceiling' => "6' 8\" under lofts", 'roof' => 'Gable, standing-seam metal',
        'walls' => '2x4 wood framing, cedar or lap siding', 'foundation' => '24 ft flatbed tiny house trailer', 'roof_type' => 'thow',
        'rooms' => [['LIVING', 0, 0, 8, 8.5], ['KITCHEN', 8, 0, 7, 8.5], ['BATH', 15, 0, 5, 8.5], ['UTILITY', 20, 0, 4, 8.5]],
        'loft' => [['LOFT 1', 0, 0, 7, 8.5], ['LOFT 2', 15, 0, 9, 8.5]],
        'features' => ['Two sleeping lofts for a couple plus a child or guest', 'Storage stairs to the main loft', 'Utility room for washer, water heater and electrical panel', 'Open kitchen in the center of the house', 'Road-legal width and height'],
        'styles' => ['tiny-house-on-wheels-plans', 'tiny-house-plans-with-loft'],
        'intro' => 'The Finch is a 24 ft tiny house on wheels plan with two sleeping lofts, a center kitchen and a dedicated utility room, giving a small family about 340 sq ft of usable space on a standard tiny house trailer.',
        'layout' => ['The living room sits under Loft 1 at the front, with a low ceiling that makes it a cozy den.', 'The kitchen in the middle of the house gets the full roof height and the best light.', 'Storage stairs climb to Loft 2, the primary bedroom, over the bath and utility room.', 'A separate utility room keeps the water heater, washer and panel out of the living space.'],
    ],
    'plan-12-2421' => [
        'name' => 'Plan 12-2421', 'title' => 'The Kestrel: 28 ft Tiny House on Wheels with Main-Floor Bedroom',
        'price' => 495, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 28, 'D' => 8.5, 'mobile' => true,
        'height' => "13' 6\"", 'ceiling' => "10' to 11'", 'roof' => 'Shed (mono-pitch), standing-seam metal',
        'walls' => '2x4 wood framing, metal and wood siding', 'foundation' => '28 ft tiny house trailer', 'roof_type' => 'shed-thow',
        'rooms' => [['BEDROOM', 0, 0, 8, 8.5], ['BATH', 8, 0, 5, 8.5], ['KITCHEN', 13, 0, 7, 8.5], ['LIVING', 20, 0, 8, 8.5]],
        'features' => ['Main-floor bedroom, no ladder or loft', 'Shed roof with a wall of clerestory windows', 'Bath between bedroom and kitchen for privacy', 'Full-size kitchen with apartment fridge and 4-burner range', 'Good choice for older owners or anyone done with lofts'],
        'styles' => ['tiny-house-on-wheels-plans'],
        'intro' => 'The Kestrel is a 28 ft tiny house on wheels plan with a real main-floor bedroom, so nobody has to climb a ladder at night. Its single-slope shed roof adds height and clerestory light across all 238 sq ft.',
        'layout' => ['The bedroom at the front fits a queen bed with walkways on one side and a closet at the foot.', 'The bath acts as a sound buffer between the bedroom and the living areas.', 'An L-shaped kitchen opens into the living room at the rear door.', 'The high side of the shed roof faces south in most layouts for winter sun.'],
    ],
    'plan-12-2422' => [
        'name' => 'Plan 12-2422', 'title' => 'The Heron: 32 ft Gooseneck Tiny House with Step-Up Bedroom',
        'price' => 545, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 32, 'D' => 8.5, 'mobile' => true,
        'height' => "13' 6\"", 'ceiling' => "6' 6\" in gooseneck bedroom, 11' main", 'roof' => 'Gable, standing-seam metal',
        'walls' => '2x4 wood framing, board-and-batten siding', 'foundation' => '32 ft gooseneck trailer', 'roof_type' => 'gooseneck',
        'rooms' => [['LIVING', 0, 0, 9, 8.5], ['KITCHEN', 9, 0, 8, 8.5], ['BATH', 17, 0, 5, 8.5], ['W/D', 22, 0, 2, 8.5], ['GOOSENECK BEDROOM', 24, 0, 8, 8.5]],
        'features' => ['Step-up bedroom over the gooseneck, no ladder', 'Washer/dryer closet', 'Longest kitchen counter in our tiny house on wheels plans', 'Gooseneck hitch tows more steadily than a bumper pull at this length', 'About 272 sq ft on one level plus steps'],
        'styles' => ['tiny-house-on-wheels-plans'],
        'intro' => 'The Heron is a 32 ft gooseneck tiny house plan with a step-up bedroom over the hitch, a long galley kitchen and a laundry closet. It gives full-time owners about 272 sq ft without a ladder loft.',
        'layout' => ['Three steps lead up to the gooseneck bedroom, which fits a queen bed under a lower ceiling.', 'A washer/dryer closet sits beside the bath, sharing the wet wall.', 'The kitchen runs 8 ft along both walls between the bath and the living room.', 'The living room at the rear has the full 11 ft ceiling and a glass door.'],
    ],

    // ---- A-frames --------------------------------------------------------------------
    'plan-12-2423' => [
        'name' => 'Plan 12-2423', 'title' => 'The Alpine: 16 x 24 A-Frame Cabin with Loft',
        'price' => 650, 'beds' => 1, 'baths' => 1, 'floors' => 2, 'W' => 24, 'D' => 16,
        'height' => "21'", 'ceiling' => 'Open to the ridge', 'roof' => 'A-frame, 12:5 pitch, metal roofing',
        'walls' => 'A-frame rafters with 2x6 gable walls', 'foundation' => 'Concrete piers or slab', 'roof_type' => 'aframe',
        'rooms' => [['GREAT ROOM', 0, 0, 14, 16], ['KITCHEN', 14, 0, 10, 8], ['BATH', 14, 8, 5, 8], ['ENTRY', 19, 8, 5, 8]],
        'loft' => [['LOFT BEDROOM', 12, 3, 12, 10]],
        'porch' => [0, -6, 24, 6],
        'features' => ['Classic steep A-frame that sheds snow', 'Two-story glass gable wall in the great room', 'Loft bedroom over the kitchen and bath', 'Mudroom entry for boots and gear', 'Front deck across the gable end'],
        'styles' => ['a-frame-house-plans', 'tiny-house-plans-with-loft', 'small-cabin-plans'],
        'intro' => 'The Alpine is a 16 x 24 ft A-frame cabin plan with a soaring great room, a loft bedroom and a mudroom entry, adding up to 504 sq ft. It is built for snowy weekends and four-season getaways.',
        'layout' => ['The great room fills the front gable with a two-story wall of glass facing the deck.', 'Kitchen and bath sit at the back under the loft, keeping plumbing together.', 'A dedicated entry handles boots, skis and wet coats.', 'The loft bedroom overlooks the great room and fits a queen bed at the center of the A.'],
    ],
    'plan-12-2424' => [
        'name' => 'Plan 12-2424', 'title' => 'The Summit: 20 x 28 Two-Bedroom A-Frame House Plan',
        'price' => 895, 'beds' => 2, 'baths' => 1, 'floors' => 2, 'W' => 28, 'D' => 20,
        'height' => "24'", 'ceiling' => 'Open to the ridge in living', 'roof' => 'A-frame, 12:5 pitch, metal roofing',
        'walls' => 'A-frame rafters with 2x6 gable walls', 'foundation' => 'Crawlspace or slab', 'roof_type' => 'aframe',
        'rooms' => [['LIVING', 0, 0, 14, 20], ['KITCHEN', 14, 0, 14, 9], ['BEDROOM', 14, 9, 8.5, 11], ['BATH', 22.5, 9, 5.5, 11]],
        'loft' => [['LOFT BEDROOM', 14, 4, 14, 12]],
        'porch' => [0, -8, 28, 8],
        'features' => ['Main-floor bedroom plus loft bedroom', 'Living room open to a 24 ft ridge', 'Large kitchen with island space', 'Wide front deck', 'Good fit for a full-time A-frame home'],
        'styles' => ['a-frame-house-plans', 'tiny-house-plans-with-loft'],
        'intro' => 'The Summit is a 20 x 28 ft two-bedroom A-frame house plan with 728 sq ft over two levels: a main-floor bedroom, a loft bedroom and a living room open to the ridge.',
        'layout' => ['The living room takes the full front of the house with floor-to-ridge glass.', 'A 14 ft kitchen spans the back wall with room for an island.', 'The main-floor bedroom and bath sit side by side at the rear.', 'The loft bedroom over the kitchen looks down into the living room.'],
    ],
    'plan-12-2425' => [
        'name' => 'Plan 12-2425', 'title' => 'The Pinecone: 12 x 16 Micro A-Frame Cabin Plan',
        'price' => 345, 'beds' => 1, 'baths' => 1, 'floors' => 2, 'W' => 16, 'D' => 12,
        'height' => "15'", 'ceiling' => 'Open to the ridge', 'roof' => 'A-frame, metal roofing',
        'walls' => 'A-frame rafters with 2x4 gable walls', 'foundation' => 'Concrete piers', 'roof_type' => 'aframe',
        'rooms' => [['LIVING', 0, 0, 10, 12], ['KITCHENETTE', 10, 0, 6, 6], ['BATH', 10, 6, 6, 6]],
        'loft' => [['LOFT', 8, 2, 8, 8]],
        'porch' => [0, -4, 16, 4],
        'features' => ['Tiny footprint that often fits small-structure rules', 'Kitchenette and bath for overnight stays', 'Sleeping loft for a full mattress', 'Simple framing for a first DIY build', 'Works as a backyard studio or glamping cabin'],
        'styles' => ['a-frame-house-plans', 'small-cabin-plans', 'tiny-house-plans-with-loft'],
        'intro' => 'The Pinecone is a 12 x 16 ft micro A-frame cabin plan with a kitchenette, a bath and a sleeping loft in 256 sq ft. It is an easy first build for a backyard studio, hunting camp or glamping rental.',
        'layout' => ['The living area fills the glass gable end and opens onto a small front deck.', 'Kitchenette and bath share one wall at the back.', 'A ladder reaches the 8 x 8 ft sleeping loft.', 'Check local rules on habitable space before using it as a dwelling.'],
    ],

    // ---- Shipping containers ---------------------------------------------------------
    'plan-12-2426' => [
        'name' => 'Plan 12-2426', 'title' => 'The Dockside: 20 ft Shipping Container Studio Plan',
        'price' => 395, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 20, 'D' => 8,
        'height' => "9' 6\" high-cube", 'ceiling' => "about 8' 10\" finished", 'roof' => 'Container roof with optional shade roof',
        'walls' => 'One 20 ft high-cube container, spray-foam insulation', 'foundation' => 'Concrete piers or slab', 'roof_type' => 'container',
        'rooms' => [['STUDIO', 0, 0, 10, 8], ['KITCHEN', 10, 0, 6, 8], ['BATH', 16, 0, 4, 8]],
        'features' => ['Built from one 20 ft high-cube container', 'Studio room for a bed or sofa bed', 'Kitchen along both walls', 'Bath at the closed end of the box', 'Large glass door in place of the cargo doors'],
        'styles' => ['shipping-container-home-plans'],
        'intro' => 'The Dockside is a 20 ft shipping container studio plan with a sleeping and living room, a kitchen and a full bath in 160 sq ft. It suits a backyard office, a rental studio or a minimalist cabin.',
        'layout' => ['The cargo doors are replaced with a glass door and sidelights into the studio.', 'The kitchen sits in the middle of the box with counters on both walls.', 'The bath fills the closed end, so plumbing runs only through one short section of floor.', 'Openings are kept to one side wall to preserve the container\'s strength.'],
    ],
    'plan-12-2427' => [
        'name' => 'Plan 12-2427', 'title' => 'The Harbor: 40 ft Shipping Container Home Plan',
        'price' => 595, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 40, 'D' => 8,
        'height' => "9' 6\" high-cube", 'ceiling' => "about 8' 10\" finished", 'roof' => 'Container roof with optional shed roof',
        'walls' => 'One 40 ft high-cube container, spray-foam insulation', 'foundation' => 'Concrete piers or strip footings', 'roof_type' => 'container',
        'rooms' => [['BEDROOM', 0, 0, 11, 8], ['BATH', 11, 0, 5, 8], ['KITCHEN', 16, 0, 10, 8], ['LIVING', 26, 0, 14, 8]],
        'features' => ['One 40 ft high-cube container', 'Separate bedroom with a door', 'Full kitchen with 10 ft of counter on each side', 'Living room with glass doors at the end', 'Simple, linear plumbing run'],
        'styles' => ['shipping-container-home-plans'],
        'intro' => 'The Harbor is a 40 ft shipping container home plan with a private bedroom, a full bath, a 10 ft kitchen and a living room in 320 sq ft. It is one of the most cost-effective full-time container layouts.',
        'layout' => ['The bedroom sits at the closed end for privacy and quiet.', 'The bath is between the bedroom and kitchen on a single wet wall.', 'A long galley kitchen opens into the living room.', 'Glass doors replace the cargo doors at the living-room end.'],
    ],
    'plan-12-2428' => [
        'name' => 'Plan 12-2428', 'title' => 'The Freight: Double 40 ft Container Home, 2 Bedrooms',
        'price' => 895, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 40, 'D' => 16,
        'height' => "9' 6\" high-cube", 'ceiling' => "about 8' 10\" finished", 'roof' => 'Shed roof over both containers',
        'walls' => 'Two 40 ft high-cube containers joined side by side', 'foundation' => 'Strip footings or slab', 'roof_type' => 'container-double',
        'rooms' => [['BEDROOM 1', 0, 0, 12, 8], ['BATH', 12, 0, 6, 8], ['BEDROOM 2', 0, 8, 12, 8], ['LAUNDRY', 12, 8, 6, 8], ['KITCHEN', 18, 0, 10, 16], ['LIVING', 28, 0, 12, 16]],
        'features' => ['Two 40 ft containers joined for a 16 ft wide interior', 'Open kitchen and living across both boxes', 'Two bedrooms and a laundry room', 'Kitchen island where the shared walls are removed', 'Shed roof adds drainage and shade'],
        'styles' => ['shipping-container-home-plans'],
        'intro' => 'The Freight is a double 40 ft shipping container home plan with two bedrooms, a laundry room and a 16 ft wide open kitchen and living area, for 640 sq ft of family-sized space.',
        'layout' => ['Side walls are removed along the kitchen and living room to create one 16 ft wide space.', 'Bedrooms sit one in each container at the closed end.', 'Bath and laundry share the plumbing wall between the bedrooms and kitchen.', 'An engineer must specify the steel framing where container walls are cut.'],
    ],

    // ---- Cottages --------------------------------------------------------------------
    'plan-12-2429' => [
        'name' => 'Plan 12-2429', 'title' => 'The Bluebell: 20 x 24 Tiny Cottage Plan with Front Porch',
        'price' => 795, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 24, 'D' => 20,
        'height' => "17'", 'ceiling' => "9' walls, vaulted living", 'roof' => '8:12 gable, architectural shingles',
        'walls' => '2x6 wood framing, lap siding', 'foundation' => 'Crawlspace or slab', 'roof_type' => 'gable',
        'rooms' => [['LIVING', 0, 0, 13, 12], ['KITCHEN', 13, 0, 11, 12], ['BEDROOM', 0, 12, 11, 8], ['BATH', 11, 12, 6, 8], ['LAUNDRY', 17, 12, 7, 8]],
        'porch' => [0, -6, 24, 6],
        'features' => ['Full-width covered front porch', 'Vaulted living room', 'Real laundry room with storage', 'Bedroom tucked at the back', 'Classic cottage gable that fits older neighborhoods'],
        'styles' => ['tiny-cottage-plans', 'adu-plans'],
        'intro' => 'The Bluebell is a 20 x 24 ft tiny cottage plan with a full-width front porch, a vaulted living room, one bedroom and a laundry room in 480 sq ft. It works as a downsizing home or a backyard cottage.',
        'layout' => ['The porch leads straight into a vaulted living room and an open kitchen.', 'Bedroom, bath and laundry line the back of the house.', 'The laundry room doubles as a pantry and storage room.', 'An 8:12 roof pitch gives the cottage its storybook profile.'],
    ],
    'plan-12-2430' => [
        'name' => 'Plan 12-2430', 'title' => 'The Primrose: 24 x 30 Two-Bedroom Cottage Plan',
        'price' => 1050, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 30, 'D' => 24,
        'height' => "18'", 'ceiling' => "9'", 'roof' => '8:12 gable, architectural shingles',
        'walls' => '2x6 wood framing, shingle and lap siding', 'foundation' => 'Crawlspace or slab', 'roof_type' => 'gable',
        'rooms' => [['LIVING', 0, 0, 16, 13], ['KITCHEN', 16, 0, 14, 13], ['BEDROOM 1', 0, 13, 11, 11], ['BATH', 11, 13, 6, 11], ['BEDROOM 2', 17, 13, 13, 11]],
        'porch' => [8, -6, 14, 6],
        'features' => ['Two good-size bedrooms', 'Open living and kitchen across the front', 'Centered entry porch', 'Single bath between the bedrooms', 'Easy to build on a narrow lot'],
        'styles' => ['tiny-cottage-plans', 'adu-plans'],
        'intro' => 'The Primrose is a 24 x 30 ft two-bedroom cottage plan with an open front living room and kitchen, a centered entry porch and 720 sq ft on one level.',
        'layout' => ['The entry porch opens into a living room and kitchen that span the front of the house.', 'Two bedrooms at the back are separated by the bath.', 'Bedroom 2 is large enough for a queen bed and a desk.', 'Everything is on one floor, so it ages well.'],
    ],
    'plan-12-2440' => [
        'name' => 'Plan 12-2440', 'title' => 'The Willow: 24 x 36 Three-Bedroom, Two-Bath Small House Plan',
        'price' => 1195, 'beds' => 3, 'baths' => 2, 'floors' => 1, 'W' => 36, 'D' => 24,
        'height' => "18'", 'ceiling' => "9'", 'roof' => '6:12 gable, architectural shingles or metal',
        'walls' => '2x6 wood framing, board-and-batten siding', 'foundation' => 'Crawlspace or slab', 'roof_type' => 'gable',
        'rooms' => [['LIVING', 0, 0, 14, 14], ['KITCHEN', 14, 0, 12, 14], ['PRIMARY', 26, 0, 10, 12], ['PRIMARY BATH', 26, 12, 10, 12], ['BEDROOM 2', 0, 14, 11, 10], ['BATH 2', 11, 14, 6, 10], ['BEDROOM 3', 17, 14, 9, 10]],
        'porch' => [0, -8, 26, 8],
        'features' => ['Three bedrooms and two full baths in 864 sq ft', 'Primary suite with its own bath', 'Large open kitchen', 'Deep front porch', 'Split-bedroom layout for privacy'],
        'styles' => ['tiny-cottage-plans', 'small-farmhouse-plans'],
        'intro' => 'The Willow is a 24 x 36 ft small house plan with three bedrooms and two full baths in 864 sq ft, including a primary suite with its own bath. It is the largest plan in the Tiny Homes Blueprint catalog.',
        'layout' => ['The primary suite sits at one end, apart from the other two bedrooms.', 'Living room and kitchen form one open space across the front.', 'Bedrooms 2 and 3 share a hall bath at the back.', 'An 8 ft deep porch runs along the living and kitchen side.'],
    ],

    // ---- Cabins ----------------------------------------------------------------------
    'plan-12-2431' => [
        'name' => 'Plan 12-2431', 'title' => 'The Timberline: 16 x 24 Small Cabin Plan with Side Porch',
        'price' => 650, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 24, 'D' => 16,
        'height' => "15'", 'ceiling' => "8' walls, vaulted great room", 'roof' => '8:12 gable, metal roofing',
        'walls' => '2x6 wood framing, log-look or board siding', 'foundation' => 'Piers or crawlspace', 'roof_type' => 'gable',
        'rooms' => [['GREAT ROOM + KITCHEN', 0, 0, 15, 16], ['BEDROOM', 15, 0, 9, 9.5], ['BATH', 15, 9.5, 9, 6.5]],
        'porch' => [24, 0, 8, 16],
        'features' => ['Open great room with kitchen along the back wall', 'Room for a wood stove', 'Bedroom and roomy bath at the rear', 'Covered side porch', 'Classic 16 x 24 footprint that is cheap to frame'],
        'styles' => ['small-cabin-plans'],
        'intro' => 'The Timberline is a 16 x 24 ft small cabin plan with an open great room, a bedroom, a full bath and a covered side porch in 384 sq ft. It is a simple, affordable weekend or hunting cabin.',
        'layout' => ['A vaulted great room combines living, dining and a kitchen along one wall.', 'The bedroom fits a queen bed with a closet.', 'The bath is big enough for a tub or a 48 in. shower.', 'The side porch is covered by an extension of the main roof.'],
    ],
    'plan-12-2432' => [
        'name' => 'Plan 12-2432', 'title' => 'The Ridgeview: 20 x 32 Cabin Plan with Loft',
        'price' => 995, 'beds' => 2, 'baths' => 1, 'floors' => 2, 'W' => 32, 'D' => 20,
        'height' => "22'", 'ceiling' => 'Vaulted great room', 'roof' => '10:12 gable, metal roofing',
        'walls' => '2x6 wood framing, board-and-batten siding', 'foundation' => 'Crawlspace or basement', 'roof_type' => 'gable-steep',
        'rooms' => [['GREAT ROOM', 0, 0, 16, 20], ['KITCHEN', 16, 0, 10, 10], ['BEDROOM', 16, 10, 10, 10], ['BATH', 26, 0, 6, 10], ['MUD / LAUNDRY', 26, 10, 6, 10]],
        'loft' => [['LOFT', 16, 2, 16, 12]],
        'porch' => [0, -8, 16, 8],
        'features' => ['Two-story great room with a wall of windows', 'Main-floor bedroom plus a large loft', 'Mudroom and laundry at the back door', 'Steep 10:12 roof for snow country', 'Front porch across the great room'],
        'styles' => ['small-cabin-plans', 'tiny-house-plans-with-loft'],
        'intro' => 'The Ridgeview is a 20 x 32 ft cabin plan with a loft, a two-story great room, a main-floor bedroom and a mudroom, totaling 832 sq ft. It makes a comfortable full-time mountain home.',
        'layout' => ['The great room rises two stories behind a wall of glass facing the porch.', 'Kitchen and bedroom sit under the loft in the back half.', 'Mudroom, laundry and bath share the back wall and its plumbing.', 'The 16 x 12 ft loft works as a second bedroom, bunk room or office.'],
    ],

    // ---- Shed conversions --------------------------------------------------------------
    'plan-12-2433' => [
        'name' => 'Plan 12-2433', 'title' => 'The Bunkie: 12 x 16 Shed to Tiny House Conversion Plan',
        'price' => 295, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 16, 'D' => 12,
        'height' => "12' 6\"", 'ceiling' => "7' walls, open gambrel", 'roof' => 'Gambrel (barn), shingles or metal',
        'walls' => '2x4 shed walls furred out for insulation', 'foundation' => 'Skids on gravel pad or piers', 'roof_type' => 'gambrel',
        'rooms' => [['SLEEP / LIVING', 0, 0, 10, 12], ['KITCHENETTE', 10, 0, 6, 6], ['BATH', 10, 6, 6, 6]],
        'loft' => [['STORAGE LOFT', 0, 0, 8, 12]],
        'features' => ['Designed around a standard 12 x 16 barn shed', 'Sleep and living room for one or two', 'Kitchenette with sink and induction burner', 'Compact bath with shower', 'Storage loft in the gambrel roof'],
        'styles' => ['shed-to-tiny-house'],
        'intro' => 'The Bunkie is a 12 x 16 ft shed to tiny house conversion plan that turns a standard barn-style shed into a sleeping room, a kitchenette and a bath, with a storage loft above. That gives 288 sq ft in total: 192 sq ft on the main floor and a 96 sq ft loft.',
        'layout' => ['The main room holds a full or queen bed and a small seating area by the double doors.', 'A kitchenette and a bath share a wet wall at the back.', 'The gambrel roof leaves room for an 8 x 12 ft storage loft.', 'Converting to habitable space usually needs a permit: check before you start.'],
    ],
    'plan-12-2434' => [
        'name' => 'Plan 12-2434', 'title' => 'The Workshop Studio: 14 x 28 Lofted Barn Shed Conversion',
        'price' => 595, 'beds' => 1, 'baths' => 1, 'floors' => 2, 'W' => 28, 'D' => 14,
        'height' => "15'", 'ceiling' => "7' 6\" walls, open gambrel", 'roof' => 'Gambrel (barn), metal roofing',
        'walls' => '2x4 or 2x6 framing, T1-11 or board siding', 'foundation' => 'Piers or slab', 'roof_type' => 'gambrel',
        'rooms' => [['LIVING', 0, 0, 12, 14], ['KITCHEN', 12, 0, 8, 14], ['BATH', 20, 0, 8, 7], ['OFFICE', 20, 7, 8, 7]],
        'loft' => [['LOFT BEDROOM', 0, 0, 10, 14]],
        'features' => ['Built from a 14 x 28 lofted barn shed', 'Loft bedroom in the gambrel roof', 'Separate home office', 'Full kitchen and bath', 'Great for a rural home office or rental'],
        'styles' => ['shed-to-tiny-house', 'tiny-house-plans-with-loft'],
        'intro' => 'The Workshop Studio is a 14 x 28 ft lofted barn shed conversion plan with a living room, full kitchen, bath, home office and loft bedroom, for 532 sq ft in total.',
        'layout' => ['The living room sits under the loft at the front, with the barn doors as the entry.', 'A full kitchen runs across the middle of the building.', 'The bath and a 7 x 8 ft office split the back.', 'The gambrel roof gives the 10 x 14 ft loft usable headroom.'],
    ],

    // ---- Farmhouses ------------------------------------------------------------------
    'plan-12-2435' => [
        'name' => 'Plan 12-2435', 'title' => 'The Homestead: 24 x 32 Small Farmhouse Plan with Mudroom',
        'price' => 1095, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 32, 'D' => 24,
        'height' => "19'", 'ceiling' => "9'", 'roof' => '10:12 gable, standing-seam metal',
        'walls' => '2x6 wood framing, board-and-batten siding', 'foundation' => 'Crawlspace or slab', 'roof_type' => 'gable-steep',
        'rooms' => [['MUDROOM', 0, 0, 8, 12], ['KITCHEN / DINING', 8, 0, 12, 12], ['LIVING', 20, 0, 12, 12], ['BEDROOM 1', 0, 12, 12, 12], ['BATH', 12, 12, 7, 12], ['BEDROOM 2', 19, 12, 13, 12]],
        'porch' => [0, -8, 32, 8],
        'features' => ['Full-width 8 ft deep front porch', 'Big mudroom with laundry and boot bench', 'Farmhouse kitchen with dining table', 'Two bedrooms with a shared bath', 'Steep metal roof and board-and-batten siding'],
        'styles' => ['small-farmhouse-plans', 'tiny-cottage-plans'],
        'intro' => 'The Homestead is a 24 x 32 ft small farmhouse plan with a full-width porch, a working mudroom, a farmhouse kitchen and two bedrooms in 768 sq ft. It is built for homesteads and small farms.',
        'layout' => ['The mudroom handles boots, chores and laundry before you reach the kitchen.', 'Kitchen, dining and living run across the front of the house.', 'Two bedrooms at the back share a large bath.', 'The full-width porch faces the road or the fields.'],
    ],
    'plan-12-2436' => [
        'name' => 'Plan 12-2436', 'title' => 'The Meadowlark: 20 x 30 Modern Farmhouse Tiny House with Loft',
        'price' => 925, 'beds' => 2, 'baths' => 1, 'floors' => 2, 'W' => 30, 'D' => 20,
        'height' => "22'", 'ceiling' => 'Vaulted living room', 'roof' => '12:12 gable, standing-seam metal',
        'walls' => '2x6 wood framing, white board-and-batten', 'foundation' => 'Crawlspace or slab', 'roof_type' => 'gable-steep',
        'rooms' => [['LIVING', 0, 0, 14, 20], ['KITCHEN', 14, 0, 16, 9], ['BEDROOM', 14, 9, 11, 11], ['BATH', 25, 9, 5, 11]],
        'loft' => [['LOFT', 14, 2, 16, 10]],
        'porch' => [0, -6, 14, 6],
        'features' => ['Modern farmhouse look with a steep 12:12 roof', 'Vaulted living room', '16 ft kitchen across the back', 'Main-floor bedroom plus loft', 'Covered porch at the living room'],
        'styles' => ['small-farmhouse-plans', 'tiny-house-plans-with-loft'],
        'intro' => 'The Meadowlark is a 20 x 30 ft modern farmhouse tiny house plan with a vaulted living room, a main-floor bedroom and a loft, for 760 sq ft under a steep standing-seam roof.',
        'layout' => ['The living room is open to the roof peak.', 'A 16 ft kitchen spans the back of the house under the loft.', 'The bedroom and bath are tucked behind the kitchen.', 'The 16 x 10 ft loft makes a guest room or office.'],
    ],

    // ---- ADUs ------------------------------------------------------------------------
    'plan-12-2437' => [
        'name' => 'Plan 12-2437', 'title' => 'The Garden Suite: 16 x 32 One-Bedroom ADU Plan',
        'price' => 795, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 32, 'D' => 16,
        'height' => "15'", 'ceiling' => "9'", 'roof' => '6:12 gable, shingles',
        'walls' => '2x6 wood framing, fiber-cement siding', 'foundation' => 'Slab', 'roof_type' => 'gable',
        'rooms' => [['LIVING', 0, 0, 11, 16], ['KITCHEN', 11, 0, 6, 16], ['BATH', 17, 0, 5, 8], ['W/D + CLOSET', 17, 8, 5, 8], ['BEDROOM', 22, 0, 10, 16]],
        'features' => ['512 sq ft, under many cities\' 600 to 800 sq ft ADU limits', 'Narrow 16 ft width for side and rear yards', 'Washer/dryer and walk-in closet', 'Separate bedroom with full-width windows', 'Slab-on-grade with no steps at the entry'],
        'styles' => ['adu-plans', 'tiny-cottage-plans'],
        'intro' => 'The Garden Suite is a 16 x 32 ft one-bedroom ADU plan with a living room, a full kitchen, laundry and a separate bedroom in 512 sq ft. Its narrow footprint fits most backyards.',
        'layout' => ['The entry opens into the living room at one end of the suite.', 'A galley kitchen leads to the bath and laundry closet.', 'The bedroom at the far end is private from the living space.', 'A slab foundation keeps the entry step-free for aging parents or renters.'],
    ],
    'plan-12-2438' => [
        'name' => 'Plan 12-2438', 'title' => 'The Carriage: 22 x 28 Two-Bedroom ADU Plan',
        'price' => 945, 'beds' => 2, 'baths' => 1, 'floors' => 1, 'W' => 28, 'D' => 22,
        'height' => "16'", 'ceiling' => "9'", 'roof' => '6:12 gable, shingles',
        'walls' => '2x6 wood framing, lap siding', 'foundation' => 'Slab or crawlspace', 'roof_type' => 'gable',
        'rooms' => [['LIVING', 0, 0, 15, 12], ['KITCHEN', 15, 0, 13, 12], ['BEDROOM 1', 0, 12, 11, 10], ['BATH', 11, 12, 6, 10], ['BEDROOM 2', 17, 12, 11, 10]],
        'features' => ['Two bedrooms in 616 sq ft for higher rent', 'Open living and kitchen', 'Bath centered between the bedrooms', 'Simple rectangle for lower build cost', 'Fits typical 20 x 30 ft ADU zones'],
        'styles' => ['adu-plans'],
        'intro' => 'The Carriage is a 22 x 28 ft two-bedroom ADU plan with an open living room and kitchen in 616 sq ft. A second bedroom usually brings meaningfully higher rent than a studio.',
        'layout' => ['Living room and kitchen share the front half of the unit.', 'Two equal bedrooms at the back each fit a queen bed.', 'The bath sits between them on one wet wall with the kitchen.', 'Windows can be placed away from the main house for privacy.'],
    ],
    'plan-12-2439' => [
        'name' => 'Plan 12-2439', 'title' => 'The Studio Flex: 12 x 20 Backyard Studio and Office ADU',
        'price' => 395, 'beds' => 1, 'baths' => 1, 'floors' => 1, 'W' => 20, 'D' => 12,
        'height' => "12'", 'ceiling' => "8' to 10' (shed roof)", 'roof' => 'Shed (mono-pitch), metal roofing',
        'walls' => '2x6 wood framing, vertical siding', 'foundation' => 'Slab or piers', 'roof_type' => 'shed',
        'rooms' => [['STUDIO', 0, 0, 13, 12], ['KITCHENETTE', 13, 0, 7, 5], ['BATH', 13, 5, 7, 7]],
        'features' => ['Backyard office, guest studio or short-term rental', 'Shed roof with high clerestory windows', 'Kitchenette and full bath', 'Studio room fits a queen bed or desk and sofa', 'Small enough to permit quickly in many cities'],
        'styles' => ['adu-plans', 'shed-to-tiny-house'],
        'intro' => 'The Studio Flex is a 12 x 20 ft backyard studio and office ADU plan with a studio room, a kitchenette and a full bath in 240 sq ft, under a modern shed roof.',
        'layout' => ['The studio room takes two-thirds of the floor, with glass doors to the yard.', 'A kitchenette and bath share the back corner.', 'The shed roof slopes away from the main house and raises the ceiling on the yard side.', 'It works as an office now and a rental or guest suite later.'],
    ],
];

// Fill in derived fields.
foreach ($PLANS as $slug => &$p) {
    $ft = function (float $v): string { $f = (int)floor($v); $in = (int)round(($v - $f) * 12); return $in ? "$f' $in\"" : "$f'"; };
    $p['width'] = $ft($p['W']);   // long side
    $p['depth'] = $ft($p['D']);
    $porchArea = array_sum(array_map(function ($r) { return $r[0] === 'PORCH' ? $r[3] * $r[4] : 0; }, $p['rooms'] ?? []));
    $p['main_sqft'] = isset($p['rooms']) ? (int)round($p['W'] * $p['D'] - $porchArea) : ($p['sqft'] ?? 0);
    $p['loft_sqft'] = (int)round(array_sum(array_map(function ($r) { return $r[3] * $r[4]; }, $p['loft'] ?? [])));
    if (!isset($p['sqft'])) $p['sqft'] = $p['main_sqft'] + $p['loft_sqft'];
    $p['mobile'] = $p['mobile'] ?? false;
    $p['has_loft'] = !empty($p['loft']);
    $p['image'] = $p['image'] ?? "/assets/plans/$slug-elevation.svg";
    $p['floorplan'] = isset($p['rooms']) ? "/assets/plans/$slug-floor-plan.svg" : null;
}
unset($p);
uasort($PLANS, function ($a, $b) { return $a['sqft'] <=> $b['sqft'] ?: strcmp($a['name'], $b['name']); });

/** Generated plan-set details (estimate, materials summary, sheets, files) from generator/build.py. */
function plan_sets(): array {
    static $sets = null;
    if ($sets === null) {
        $f = __DIR__ . '/plan-sets.json';
        $sets = is_file($f) ? (json_decode((string)file_get_contents($f), true) ?: []) : [];
    }
    return $sets;
}
