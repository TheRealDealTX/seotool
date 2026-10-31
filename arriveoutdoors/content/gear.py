"""Gear page data. Product links reuse the Amazon ASINs already used on the old
site (tag arriveoutdoors-20). Notes say what each item is for — no fake testing claims.
Group anchors match the legacy redirects (/gear/#packs etc.)."""

GEAR = [
    ("packs", "Packs", "Fit matters more than brand: size by torso length with the backpack size calculator.", "/tools/backpack-size/", [
        ("Osprey Talon 22 daypack", "B06WWJJ2V7", "A popular, light daypack for full-day hikes with a ventilated back panel and hipbelt pockets."),
        ("Osprey Atmos AG 65", "B086HMX9DB", "A ventilated, suspended-mesh backpacking pack for multi-night trips with heavier loads."),
        ("Gregory Baltoro 65", "B09GXM55XQ", "A well-padded load hauler for long trips or carrying shared group gear."),
    ]),
    ("sleep", "Sleep system", "Buy by the comfort rating, and match the pad R-value to the ground temperature.", "/tools/sleeping-bag-temperature/", [
        ("Therm-a-Rest NeoAir XLite NXT", "B0BQ4PCHBG", "A light, warm inflatable pad that's a common choice for three-season backpacking."),
        ("Sleeping bag", "B084X4R2XH", "The bag linked in our older beginner guide; check the comfort rating against your expected lows."),
        ("Outraveler SUV air mattress", "B0BVZ4V3MP", "An inflatable mattress shaped for SUV cargo areas — see our Honda CR-V camper guide."),
    ]),
    ("camp", "Camp & kitchen", "Car campers can go heavier and comfier; backpackers should weigh everything.", "/car-camping-essentials/", [
        ("Tent", "B07QK8KN8S", "The tent linked in our Camping 101 guide — a simple starting point for first car-camping trips."),
        ("Helinox Chair One", "B07YX4M4JP", "A packable camp chair that's light enough for some backpackers."),
        ("Jetboil Flash cooking system", "B07N8HMPYF", "Boils water quickly for coffee and freeze-dried meals."),
        ("Sea to Summit long-handled spoon", "B0029ZC4H6", "Reaches the bottom of freeze-dried meal bags without messy fingers."),
        ("Tarp", "B07BNZK137", "Shade and rain cover over a camp kitchen or picnic table."),
        ("Odoland rechargeable tent fan with light", "B07W41D6XT", "Moves air in a hot tent at night — see how to cool a tent without electricity."),
        ("Jackery Explorer 300 Plus", "B0CFV93GZM", "A portable power station for car camping: phones, lights, fans."),
        ("Sailnovo rooftop cargo bag", "B0773L75SR", "Frees up interior space when you sleep in the car."),
    ]),
    ("water", "Water", "Hollow-fiber filters remove bacteria and protozoa, not viruses; protect them from freezing.", "/sawyer-squeeze-gravity-setup/", [
        ("Sawyer Squeeze water filter", "B0988M1RTF", "A light, field-cleanable filter that can be set up as a gravity system."),
        ("Dirty water bag", "B07QBQ894L", "A larger dirty bag for gravity-filtering water at camp."),
    ]),
    ("footwear", "Footwear", "Break boots in before a big trip; fit with the socks you'll hike in.", None, [
        ("Merrell Moab 3 hiking shoes", "B0DFC9X72D", "A comfortable, widely available hiking shoe for trail days."),
        ("La Sportiva TX4 approach shoes", "B0CH3WSKZY", "Sticky-rubber approach shoes for scrambling and rocky trails."),
    ]),
    ("clothing", "Clothing", "Layer: wicking base, warm mid layer, waterproof shell — plus sun protection.", "/best-sun-hoodies-for-hiking/", [
        ("Outdoor Research Echo hoodie", "B0CHVS26C2", "A very light sun hoodie for hot, exposed trails."),
        ("Smartwool merino sun hoodie", "B0F92GTZ8Y", "A merino-blend sun hoodie that resists odor on multi-day trips."),
        ("Kula Cloth", "B0DFK4NJG2", "A reusable, antimicrobial pee cloth that cuts down on toilet paper."),
    ]),
    ("safety", "Safety & navigation", "The Ten Essentials go on every hike, even short ones.", "/what-to-do-if-you-get-lost-in-the-woods/", [
        ("Headlamp (300+ lumens, rechargeable or AAA)", None, "A bright, compact headlamp — the one item people most often wish they'd brought."),
        ("Suunto A-10 compass", "B000JL6G7Q", "A simple baseplate compass for map navigation when your phone dies."),
        ("Whistle", "B0F812C969", "Three blasts is the universal distress signal and carries farther than your voice."),
        ("SOL emergency bivvy", "B000WXX0JS", "A tiny emergency shelter for an unplanned night out."),
        ("Bear spray", "B001DQ76JI", "Carry it in a holster where you can reach it in seconds in bear country."),
        ("Black Diamond Trail Sport trekking poles", "B0B78BQZFR", "Take strain off knees on descents and add balance on stream crossings."),
        ("Fire extinguisher", "B0D35XH9XF", "A compact extinguisher for the car-camping kit."),
        ("Fire blanket", "B07MXDMRNC", "Smothers small cooking or grease fires at camp."),
    ]),
    ("scrambling", "Scrambling", "Rockfall and slips are the main hazards — wear a helmet on loose class 3 and 4 terrain.", "/class-3-scramble/", [
        ("Black Diamond Half Dome helmet", "B0BTKP3192", "A durable climbing helmet for scrambles and loose gullies."),
        ("Petzl Boreo helmet", "B0794DVVSF", "A hybrid-shell helmet that's comfortable on long approach days."),
        ("Black Diamond Crag gloves", "B0819YKY94", "Protect hands on rough rock and fixed cables."),
    ]),
    ("photo", "Camera gear", "Carry the camera where you can reach it, or you won't take it out.", "/best-camera-for-backpacking/", [
        ("Peak Design Capture camera clip", "B07818LB9D", "Clips a camera to your pack's shoulder strap for quick access."),
        ("Peak Design Slide Lite strap", "B0781RYKTW", "An adjustable sling strap for carrying a camera across your body."),
        ("JOBY GorillaPod 3K kit", "B074WC9YKL", "A bendable tripod that wraps around branches and rocks."),
        ("OM System Tough TG-7", "B0CH1QPT77", "A waterproof, rugged compact camera for wet and dusty trips."),
        ("GoPro HERO13 Black", "B0DCM34GXX", "A small action camera for video on the move."),
    ]),
    ("fishing", "Fishing", "Buy a current state license and check local regulations before you fish.", "/grand-mesa-fishing/", [
        ("Ugly Stik GX2 spinning combo", "B0D1537STT", "A tough, beginner-friendly rod and reel combo."),
        ("Panther Martin trout spinner kit", "B002NUFQRC", "Classic spinners for trout in lakes and streams."),
        ("Plano StowAway tackle box", "B00469AX4O", "Keeps small tackle organized in a pack or car."),
    ]),
]
