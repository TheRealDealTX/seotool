#!/usr/bin/env python3
"""Add Amazon affiliate "Helpful Finds" blocks to riseapartments.com blog posts.

Usage:
  WP_USER=... WP_APP_PASSWORD=... python3 affiliate_links.py plan   # classify + report, no writes
  WP_USER=... WP_APP_PASSWORD=... python3 affiliate_links.py apply  # write to WordPress

Reads the GA4 "Pages and screens" export (ANALYTICS env var or default path) to
pick posts with views, skips posts that already carry Amazon links, inserts one
Gutenberg block group per post (heading + intro + 4 tagged links + disclosure)
before the Conclusion / Final Thoughts / FAQ heading, and marks the block with
an HTML comment so a rerun never adds a second copy.
"""
import csv, html, json, os, re, sys, time, urllib.parse, urllib.request, base64, collections

SITE = "https://riseapartments.com"
TAG = "riseapartments-20"
MARK = "<!-- rise-amazon-picks -->"
HERE = os.path.dirname(os.path.abspath(__file__))
ANALYTICS = os.environ.get("ANALYTICS", os.path.join(HERE, "analytics.csv"))
CACHE = os.environ.get("POSTS_CACHE", os.path.join(HERE, "posts_cache.json"))
REL = 'target="_blank" rel="nofollow sponsored noopener noreferrer"'

def amz(q):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(q)}&tag={TAG}"

# ---------------------------------------------------------------- product sets
# key: (heading, intro, [(display name, amazon search query, why)])
SETS = {
 "shower": ("Helpful Finds for a Walk-In Shower",
   "A great shower deserves a few renter-friendly upgrades. These are the add-ons we see tenants pick up first after moving in:",
   [("Tension-Pole Shower Caddy","tension pole shower caddy rust proof","no drilling, holds everything off the floor of an open shower"),
    ("High-Pressure Rainfall Shower Head","high pressure rainfall shower head handheld combo","an easy swap that you can take with you when you move out"),
    ("Non-Slip Bath Mat","non slip shower mat for textured tile","walk-in showers have no lip, so grip matters"),
    ("Shower Squeegee","shower squeegee stainless steel","keeps frameless glass free of water spots")]),
 "closet": ("Helpful Finds for a Walk-In Closet",
   "A walk-in closet is only as good as the way you organize it. These renter-friendly pieces make the most of the space:",
   [("Slim Velvet Hangers (50-Pack)","velvet hangers 50 pack","doubles your hanging space and stops clothes slipping"),
    ("Closet Organizer System","closet organizer system shelves and drawers","adds shelving without touching the walls"),
    ("Stackable Shoe Rack","stackable shoe rack for closet","keeps the floor clear in a walk-in"),
    ("Fabric Storage Bins","fabric storage bins for closet shelves","turns the top shelf into usable seasonal storage")]),
 "airbnb": ("Helpful Finds for Airbnb Hosting",
   "Hosting in an Airbnb-friendly apartment is easier with a few guest-ready basics:",
   [("Smart Lock with Keypad","smart lock keypad for renters apartment","lets guests self check-in with a code you can change between stays"),
    ("Hotel-Style Bath Towel Set","hotel bath towels set white","white towels photograph well and bleach clean"),
    ("Folding Luggage Rack","folding luggage rack for guest room","a small touch guests always mention"),
    ("Smart Plug Pack","smart plug 4 pack alexa google","control lamps and fans remotely between guests")]),
 "golf": ("Helpful Finds for Golfers",
   "If an on-site golf simulator sold you on the building, round out your game at home with these:",
   [("Golf Practice Net","golf practice net indoor","work on your swing on days the simulator is booked"),
    ("Indoor Putting Mat","indoor putting green mat","putting practice that fits in a hallway"),
    ("Portable Launch Monitor","golf launch monitor portable","track ball speed and carry distance on the range or in the sim"),
    ("Golf Impact Bag","golf impact bag swing trainer","builds a solid strike without hitting balls")]),
 "pickleball": ("Helpful Finds for Pickleball Players",
   "Living next to a pickleball court means you will play more. Bring your own gear:",
   [("Pickleball Paddle Set","pickleball paddles set of 2 with balls","everything two players need to start"),
    ("Outdoor Pickleballs (12-Pack)","outdoor pickleballs 12 pack","outdoor balls hold up on community courts"),
    ("Pickleball Bag","pickleball bag backpack","carries paddles, balls and water to the court"),
    ("Court Shoes","pickleball court shoes","lateral support that running shoes do not give")]),
 "basketball": ("Helpful Finds for Basketball Fans",
   "An indoor court downstairs is a rare amenity. Make the most of it:",
   [("Indoor/Outdoor Basketball","indoor outdoor basketball official size","a composite ball that works on both surfaces"),
    ("Ball Pump with Needles","basketball pump with pressure gauge","keep the bounce consistent"),
    ("Ankle Braces","ankle brace for basketball","the most common pickup-game injury is the easiest to prevent"),
    ("Mesh Ball Bag","basketball bag mesh drawstring","carry the ball and sneakers down to the court")]),
 "tennis": ("Helpful Finds for Tennis Players",
   "With a court on the property, your racket will get more use. A few essentials:",
   [("Tennis Racket (Adult)","adult tennis racket pre strung","a solid all-around racket for community courts"),
    ("Pressureless Tennis Balls","pressureless tennis balls bulk","practice balls that last for months"),
    ("Tennis Ball Hopper","tennis ball hopper","no more bending for solo practice"),
    ("Overgrip Tape","tennis overgrip tape","fresh grip for hot Texas afternoons")]),
 "gym": ("Helpful Finds for Apartment Workouts",
   "A community gym covers the big machines. These fill the gaps on busy nights:",
   [("Resistance Band Set","resistance bands set with handles","a full workout that stores in a drawer"),
    ("Adjustable Dumbbells","adjustable dumbbells pair","replaces a rack of weights in a small apartment"),
    ("Thick Yoga Mat","yoga mat thick non slip","stretching and floor work at home"),
    ("Insulated Water Bottle","insulated water bottle 32 oz","stays cold through a long gym session")]),
 "pool": ("Helpful Finds for Pool Days",
   "A resort-style pool is one of the best perks of apartment living. Pack for it:",
   [("Oversized Beach Towel","oversized beach towel quick dry","bigger than the ones the pool deck provides"),
    ("Waterproof Phone Pouch","waterproof phone pouch","protects your phone poolside"),
    ("Reef-Safe Sunscreen SPF 50","reef safe sunscreen spf 50","Texas sun is no joke"),
    ("Insulated Tumbler","insulated tumbler with lid 30 oz","keeps drinks cold on the lounge chair")]),
 "garage": ("Helpful Finds for an Attached Garage",
   "An attached garage is prime storage space. These keep it usable for a car and more:",
   [("Heavy-Duty Garage Shelving","garage shelving unit heavy duty 5 tier","frees the floor for the car"),
    ("Wall-Mounted Bike Rack","bike wall mount rack garage","gets bikes up and out of the way"),
    ("Wall Tool Organizer","garage wall tool organizer","hooks for brooms, cords and tools"),
    ("Garage Floor Mat","garage floor mat containment","catches drips and rain runoff")]),
 "outdoor": ("Helpful Finds for a Private Yard or Patio",
   "Private outdoor space is rare in apartment living. Make yours a room you actually use:",
   [("Outdoor String Lights","outdoor string lights patio waterproof","instant evening atmosphere, no electrician needed"),
    ("Patio Conversation Set","patio furniture set small space","sized for apartment yards and balconies"),
    ("Outdoor Area Rug","outdoor rug 5x7 waterproof","defines the space and hides worn concrete"),
    ("Raised Garden Bed","raised garden bed kit","herbs and vegetables without digging up the landlord's lawn")]),
 "pets": ("Helpful Finds for Apartment Pets",
   "Pet-friendly living goes smoother with a few apartment-sized essentials:",
   [("Enclosed Cat Litter Box","enclosed litter box furniture","hides the box and traps odor in a small space"),
    ("Pet Camera with Treat Dispenser","pet camera treat dispenser","check in on your pet during the workday"),
    ("Washable Pet Bed","washable dog bed medium","easy to keep clean in an apartment"),
    ("Pet Hair Vacuum","pet hair vacuum cordless","the single most used tool in a pet household")]),
 "fireplace": ("Helpful Finds for a Cozy Fireplace Nook",
   "A fireplace turns an apartment into a home. Set the scene around it:",
   [("Chunky Knit Throw Blanket","chunky knit throw blanket","the fireside essential"),
    ("Flameless LED Candles","flameless candles set with remote","safe ambient light on the mantel"),
    ("Faux Fur Area Rug","faux fur rug fireplace","softens a tile hearth area"),
    ("Mantel Decor Set","mantel decor set modern","makes the fireplace the room's focal point")]),
 "kitchen": ("Helpful Finds for a Chef's Kitchen",
   "An island, gas range or stone counters deserve tools that match. Our picks:",
   [("Counter-Height Bar Stools (Set of 2)","counter height bar stools set of 2","turns the island into a breakfast bar"),
    ("Acacia Wood Cutting Board","acacia wood cutting board large","protects granite and quartz from knife marks"),
    ("Granite & Quartz Countertop Cleaner","granite and quartz countertop cleaner","keeps stone counters streak-free"),
    ("Cast Iron Skillet","cast iron skillet 12 inch pre seasoned","built for a gas range")]),
 "appliances": ("Helpful Finds for Appliance Care",
   "Stainless appliances look great until the first fingerprint. Keep them showroom-ready:",
   [("Stainless Steel Cleaner & Polish","stainless steel cleaner and polish spray","removes smudges without streaks"),
    ("Microfiber Cloths (24-Pack)","microfiber cleaning cloths 24 pack","the right cloth for stainless and glass"),
    ("Dishwasher Cleaner Tablets","dishwasher cleaner tablets","monthly maintenance that prevents odor"),
    ("Washing Machine Cleaner","washing machine cleaner tablets","front-loaders need it every month")]),
 "highrise": ("Helpful Finds for High-Rise Living",
   "Floor-to-ceiling windows and skyline views come with a lot of sun and glass. These help:",
   [("Blackout Curtains","blackout curtains 96 inch","sleep past sunrise on the 20th floor"),
    ("Heat-Blocking Window Film","heat control window film removable","cuts glare and cooling bills without damaging the glass"),
    ("Robot Vacuum","robot vacuum self emptying","keeps open-plan floors clean on autopilot"),
    ("Window Cleaning Kit","window cleaning kit squeegee extension","for the inside of all that glass")]),
 "smart": ("Helpful Finds for a Smart Apartment",
   "You do not need a smart building to live in a smart home. These renter-friendly devices move with you:",
   [("Smart Plug Pack","smart plug 4 pack alexa google","schedules lamps, fans and coffee makers"),
    ("Smart LED Bulbs","smart light bulbs color changing 4 pack","no wiring, no landlord permission"),
    ("Smart Speaker","smart speaker alexa","the hub for everything else"),
    ("Smart Door Sensor","door window sensor smart home","know when the door opens while you are out")]),
 "ev": ("Helpful Finds for EV Owners",
   "EV charging in the garage is a huge win. A couple of accessories make it seamless:",
   [("Portable Level 1/2 EV Charger","portable ev charger level 2 nema 14-50","a backup for when community chargers are full"),
    ("EV Charging Cable Organizer","ev charging cable holder","keeps the cable off the garage floor"),
    ("Charging Adapter Set","ev charger adapter","compatibility with more public stations"),
    ("Tire Inflator (Portable)","portable tire inflator 12v","EV tires lose pressure like any other")]),
 "laundry": ("Helpful Finds for In-Unit Laundry",
   "In-unit laundry is a daily luxury. Set it up right:",
   [("Collapsible Laundry Basket","collapsible laundry basket","stores flat in a small laundry closet"),
    ("Mesh Laundry Bags","mesh laundry bags set","protects delicates in a compact washer"),
    ("Wool Dryer Balls","wool dryer balls","cuts drying time and static without sheets"),
    ("Washing Machine Cleaner","washing machine cleaner tablets","monthly care for a stacked unit")]),
 "family": ("Helpful Finds for Families in Apartments",
   "Family-friendly communities make life easier. A few apartment-proofing basics help too:",
   [("Pressure-Mount Baby Gate","pressure mounted baby gate no drill","renter-friendly, no holes in the wall"),
    ("Outlet Covers","outlet covers baby proofing","the first thing to do on move-in day"),
    ("Furniture Anti-Tip Straps","furniture anchors anti tip straps","for dressers and bookshelves"),
    ("Kids' Step Stool","kids step stool two step","reaches apartment-height sinks")]),
 "pests": ("Helpful Finds for a Pest-Free Apartment",
   "Whether you are dealing with an infestation or preventing one, these are the essentials:",
   [("Bed Bug Mattress Encasement","bed bug mattress encasement queen","traps anything in the mattress and protects a new one"),
    ("Bed Bug Interceptors","bed bug interceptors for bed legs","catches and monitors activity"),
    ("Handheld Steamer","handheld steamer for bed bugs","heat is the treatment that works"),
    ("Diatomaceous Earth","food grade diatomaceous earth","a safe barrier along baseboards")]),
 "humidity": ("Helpful Finds for Humid Climates",
   "Gulf Coast humidity gets into everything. These keep an apartment dry and comfortable:",
   [("Dehumidifier (1,500 sq ft)","dehumidifier 1500 sq ft","the single biggest comfort upgrade in Houston"),
    ("Digital Hygrometer","digital hygrometer indoor humidity monitor","know when you are above 50 percent"),
    ("Moisture Absorber Boxes","moisture absorber for closets","for closets and bathrooms"),
    ("Mold & Mildew Remover","mold and mildew remover spray","for grout, caulk and window sills")]),
 "energy": ("Helpful Finds to Lower Your Electric Bill",
   "You cannot replace the HVAC in a rental, but these cut the bill anyway:",
   [("Smart Power Strip","smart power strip energy monitoring","kills phantom load from electronics"),
    ("LED Bulbs (Pack of 16)","led light bulbs 60 watt equivalent 16 pack","the fastest payback of any upgrade"),
    ("Thermal Insulated Curtains","thermal insulated curtains","keeps summer heat out and winter heat in"),
    ("Door Draft Stopper","door draft stopper under door","seals the gap on apartment entry doors")]),
 "approval": ("Helpful Finds for a Stronger Rental Application",
   "Getting approved with a past eviction, broken lease or thin credit comes down to preparation. These help you walk in ready:",
   [("Accordion Document Organizer","accordion file organizer letter size","keep pay stubs, references and ID copies together for every application"),
    ("Every Tenant's Legal Guide (Nolo)","every tenant's legal guide nolo","know your rights and what landlords can legally ask"),
    ("Monthly Budget Planner","monthly budget planner book","shows a landlord you have a plan for rent"),
    ("Portable Door Lock","portable door lock for apartment","extra security in a new place from day one")]),
 "moving": ("Helpful Finds for Moving Day",
   "Once the lease is signed, the move is the next hurdle. These make it painless:",
   [("Moving Boxes Kit","moving boxes kit with tape","assorted sizes delivered to your door"),
    ("Furniture Sliders","furniture sliders for hardwood and carpet","move a sofa without scratching the floors you just inspected"),
    ("Packing Tape Dispenser","packing tape dispenser with tape","the tool you will wish you bought first"),
    ("Mattress Bag","mattress bag for moving queen","keeps the mattress clean in the truck")]),
 "safety": ("Helpful Finds for Protecting Your Apartment",
   "Renters insurance covers the loss. These help prevent it:",
   [("Fire Extinguisher (Kitchen)","fire extinguisher for home kitchen","every apartment kitchen should have one"),
    ("Smoke & CO Detector","smoke and carbon monoxide detector battery","a backup for the one the landlord installed"),
    ("Water Leak Sensor","water leak detector alarm","catches a washer or AC leak before it hits the floor below"),
    ("Fireproof Document Bag","fireproof document bag","lease, passport and insurance paperwork in one place")]),
 "storage": ("Helpful Finds for Small-Space Storage",
   "Every inch counts in an apartment. These create storage where there was none:",
   [("Under-Bed Storage Bags","under bed storage bags","the biggest unused space in a bedroom"),
    ("Over-the-Door Organizer","over the door organizer pockets","shoes, toiletries or pantry items"),
    ("Floating Wall Shelves","floating shelves set of 3","vertical storage that looks like decor"),
    ("Stackable Storage Bins","stackable storage bins with lids","for the top shelf of every closet")]),
 "office": ("Helpful Finds for an Apartment Home Office",
   "Working from an apartment means the office has to earn its square footage. These do:",
   [("Compact Standing Desk","small standing desk for apartment","full workstation in a corner"),
    ("Ergonomic Office Chair","ergonomic office chair small space","your back will notice"),
    ("Laptop Stand","adjustable laptop stand","brings the screen to eye level"),
    ("Clip-On Desk Lamp","clamp desk lamp led","light without taking desk space")]),
 "flooring": ("Helpful Finds for Apartment Floors",
   "You cannot change the flooring in a rental, but you can protect it and dress it up:",
   [("Peel-and-Stick Floor Tiles","peel and stick floor tile vinyl","a removable makeover for dated floors"),
    ("Area Rug (5x7)","area rug 5x7 living room","defines a space and softens hard floors"),
    ("Non-Slip Rug Pad","rug pad 5x7 non slip","keeps rugs flat and protects the floor under them"),
    ("Felt Furniture Pads","felt furniture pads for hardwood floors","avoids scratches that cost your deposit")]),
 "wallpaper": ("Helpful Finds for Renter-Friendly Walls",
   "Peel-and-stick is the renter's best friend. Tools and favorites:",
   [("Peel-and-Stick Wallpaper","peel and stick wallpaper removable","removable, so your deposit is safe"),
    ("Wallpaper Smoothing Tool Kit","wallpaper smoothing tool kit","bubble-free application"),
    ("Damage-Free Picture Hangers","command picture hanging strips","hang art without nails"),
    ("Laser Level","laser level for hanging pictures","straight lines the first time")]),
 "floral": ("Helpful Finds for Fresh and Faux Florals",
   "Flowers are the cheapest way to make an apartment feel finished. Our picks:",
   [("Ceramic Vase Set","ceramic vase set of 3 modern","the base for every arrangement"),
    ("Realistic Faux Eucalyptus","faux eucalyptus stems","greenery that never wilts"),
    ("Dried Pampas Grass","dried pampas grass decor","one stem fills a corner"),
    ("Floral Shears","floral shears","for anyone buying fresh bunches")]),
 "decor": ("Helpful Finds to Finish the Look",
   "A few well-chosen pieces pull a room together. These work in nearly any apartment:",
   [("Textured Throw Pillow Covers","throw pillow covers set of 4 textured","the fastest sofa refresh"),
    ("Arched Floor Mirror","arched floor mirror full length","makes a small room feel bigger"),
    ("Linen Curtains","linen curtains 96 inch","softens light and hides vertical blinds"),
    ("Arc Floor Lamp","arc floor lamp living room","overhead-style light without wiring")]),
 "boat": ("Helpful Finds for a Day on Lake Belton",
   "Renting a boat is the easy part. Bring the gear the rental does not include:",
   [("Coast Guard-Approved Life Jackets","life jacket adult coast guard approved","rentals supply them, but yours will fit better"),
    ("Waterproof Dry Bag","waterproof dry bag 20l","phones, keys and wallets stay dry"),
    ("Rolling Cooler","rolling cooler 50 quart","ice all day in Central Texas heat"),
    ("Polarized Sunglasses","polarized sunglasses for boating","cuts glare off the water")]),
 "travel": ("Helpful Finds for a Mountain Getaway",
   "Heading up for the weekend? These make a lodge or cabin trip more comfortable:",
   [("Hiking Daypack","hiking daypack 25l","trails, lakes and meadows in one bag"),
    ("Insulated Water Bottle","insulated water bottle 32 oz","altitude dries you out fast"),
    ("Packable Down Jacket","packable down jacket","mountain evenings get cold in every season"),
    ("Headlamp","rechargeable headlamp","for campsites and dark lodge paths")]),
 "landlord": ("Helpful Finds for Landlords and Investors",
   "Owning or managing rental property is a business. These are the tools that pay for themselves:",
   [("The Book on Managing Rental Properties","the book on managing rental properties","the standard guide for small landlords"),
    ("Keypad Deadbolt","keypad deadbolt lock","rekey between tenants in seconds"),
    ("Smoke & CO Detector (2-Pack)","smoke and carbon monoxide detector 2 pack","code compliance made simple"),
    ("Property Inspection Checklist Pad","rental property inspection checklist forms","document move-in and move-out condition")]),
 "tools": ("Helpful Finds for Apartment Repairs and Upkeep",
   "Most small fixes do not need a maintenance ticket. A compact kit handles them:",
   [("Household Tool Kit","household tool kit for apartment","hammer, drivers, pliers and tape in one case"),
    ("Drain Snake","drain snake hair clog remover","the most common apartment plumbing problem"),
    ("Spackle Repair Kit","wall repair kit spackle","patch nail holes before move-out inspection"),
    ("Cordless Drill","cordless drill set compact","for curtain rods, shelves and furniture assembly")]),
 "painting": ("Helpful Finds for Painting Before Move-In",
   "Painting a rental is the highest-impact weekend project. Get the right supplies:",
   [("Painter's Tape","painters tape multi pack","clean lines along trim and ceilings"),
    ("Paint Roller Kit","paint roller kit with tray","everything for a room in one box"),
    ("Canvas Drop Cloth","canvas drop cloth 9x12","protects the floors you are responsible for"),
    ("Peel-and-Stick Paint Samples","peel and stick paint samples","test colors without opening a can")]),
 "touring": ("Helpful Finds for Apartment Tours",
   "The best renters show up to a tour with a few tools. Here is the kit:",
   [("Laser Distance Measure","laser distance measure","confirm your sofa and bed fit before you sign"),
    ("Outlet Tester","outlet tester gfci","catches dead or miswired outlets in seconds"),
    ("Pocket Flashlight","small led flashlight bright","look under sinks and inside closets"),
    ("Apartment Hunting Notebook","apartment hunting checklist notebook","compare units side by side")]),
 "senior": ("Helpful Finds for Senior Apartment Living",
   "Comfort and safety upgrades that do not require a landlord's permission:",
   [("Suction Grab Bar","suction grab bar for shower","removable bathroom support"),
    ("Non-Slip Bath Mat","non slip bath mat for seniors","shower safety first"),
    ("Reacher Grabber Tool","reacher grabber tool 32 inch","for high shelves and dropped items"),
    ("Motion-Sensor Night Lights","motion sensor night light plug in","lights the path to the bathroom")]),
 "content": ("Helpful Finds for Apartment Content Creators",
   "Great apartment photos and videos come from good light and a steady shot:",
   [("Ring Light with Tripod","ring light with tripod stand","even light for interiors and selfies"),
    ("Phone Tripod with Remote","phone tripod with bluetooth remote","hands-free walkthroughs"),
    ("Wireless Lavalier Mic","wireless lavalier microphone for phone","clear audio for tour videos"),
    ("Wide-Angle Phone Lens","wide angle phone camera lens","fits a whole room in frame")]),
 "vacuumseal": ("Helpful Finds for Freezer Organization",
   "Vacuum sealing changes how an apartment freezer works. The essentials:",
   [("Chamber Vacuum Sealer","chamber vacuum sealer home","seals liquids and marinades, not just dry goods"),
    ("Vacuum Sealer Bags","chamber vacuum sealer bags","bulk bags cost pennies each"),
    ("Freezer Bin Organizers","freezer organizer bins stackable","keep sealed packs sorted"),
    ("Freezer Labels","freezer labels dissolvable","know what and when")]),
 "power": ("Helpful Finds for Backup Power in an Apartment",
   "Rooftop solar is off the table for renters, but portable power is not:",
   [("Portable Power Station","portable power station 1000wh","keeps the fridge or router running through an outage"),
    ("Foldable Solar Panel","portable solar panel 100w foldable","recharges on a balcony"),
    ("Rechargeable LED Lantern","rechargeable led lantern","safer than candles"),
    ("Power Bank","power bank 20000mah fast charging","phones first")]),
 "security": ("Helpful Finds for Feeling Safe at Home",
   "Peace of mind in a rental should not depend on the landlord. These renter-friendly additions need no installation:",
   [("Portable Door Lock","portable door lock for apartment","blocks the door from inside even if someone has a key"),
    ("Door and Window Alarm Sensors","door window alarm sensors wireless","a loud alert if an entry point opens"),
    ("Personal Safety Alarm","personal safety alarm keychain","130 dB on a keychain"),
    ("Fireproof Document Bag","fireproof document bag","lease, ID and important papers ready to grab")]),
 "essentials": ("Helpful Finds for Your New Apartment",
   "Found the right place? These are the move-in essentials nearly every renter buys in the first week:",
   [("Moving Boxes Kit","moving boxes kit with tape","assorted sizes delivered to your door"),
    ("Damage-Free Picture Hangers","command picture hanging strips","hang art without losing your deposit"),
    ("Household Tool Kit","household tool kit for apartment","for furniture assembly and small fixes"),
    ("Blackout Curtains","blackout curtains 84 inch","the upgrade that improves sleep the most")]),
}

# ---------------------------------------------------------------- classifier
# (regex on slug, set key) -- first match wins
RULES = [
 (r"walk-in-shower", "shower"),
 (r"walk-in-closet", "closet"),
 (r"airbnb", "airbnb"),
 (r"golf", "golf"),
 (r"pickleball", "pickleball"),
 (r"basketball", "basketball"),
 (r"tennis", "tennis"),
 (r"gym|fitness", "gym"),
 (r"sauna|hot-tub|pool", "pool"),
 (r"garage", "garage"),
 (r"private-yard|with-yards|landscaping|outdoor|backyard|patio|retractable-screens|build-to-rent|new-homes-for-rent|rental-home-community", "outdoor"),
 (r"dog-park|pet|esa-requests|service-animal", "pets"),
 (r"fireplace", "fireplace"),
 (r"kitchen-island|gas-range|granite|quartz|countertop|cabinet|kitchen", "kitchen"),
 (r"stainless-steel|appliance|home-warranty", "appliances"),
 (r"in-unit-laundry", "laundry"),
 (r"ev-charging", "ev"),
 (r"solar-batter", "power"),
 (r"smart-technology|smart-home|technology-is-changing|building-networks", "smart"),
 (r"playground|for-families|families-should", "family"),
 (r"bed-bug|mold", "pests"),
 (r"humid", "humidity"),
 (r"electric-bill|savings", "energy"),
 (r"domestic-violence|safe-rental|car-accident|premises-liability|slip-and-fall", "security"),
 (r"renters-insurance|loss-of-use|building-fire", "safety"),
 (r"storage|living-small|cramped|reclaim-every-inch|effortless", "storage"),
 (r"office", "office"),
 (r"flooring", "flooring"),
 (r"wallpaper", "wallpaper"),
 (r"floral", "floral"),
 (r"vacuum-sealer", "vacuumseal"),
 (r"instagram", "content"),
 (r"painting", "painting"),
 (r"touring", "touring"),
 (r"senior", "senior"),
 (r"boat", "boat"),
 (r"tamarack|bear-valley", "travel"),
 (r"plumbing|repairs|diy|maintenance-costs|maintenance-response|tenant-upgrades|structural-problems", "tools"),
 (r"soft-furnishings|design|decor|radiator|sliding-doors|interior|luxury-apartments-apart", "decor"),
 (r"eviction|felon|broken-lease|no-credit|bad-credit|section-8|second-chance|low-income|get-approved|rental-history|first-time-renters|budget-check|how-long", "approval"),
 (r"moving|relocation|movers|checklist|move-to-an-apartment|downsize|home-sale|timeline|pack|inherit|home-closing|renting-to-owning|sells-the-building|foreclosure|chattanooga", "moving"),
 (r"skyline|floor-to-ceiling|high-rise|highest|mid-rise|concierge|valet|luxury|midtown|downtown", "highrise"),
 (r"landlord|property-manag|investor|investment|rental-property|hoa|real-estate|rpm-living|wrong-tenant|asset-strateg|pricing-trends|property-value|construction|roof|paving|handrail|rigging|staff-apparel|event-spaces|gps-time-clock|majors|realtor|pet-fee|multi-family", "landlord"),
 (r".", "essentials"),
]

OVERRIDES = {
 "why-durable-handrails-matter-in-multi-family-housing-design": "landlord",
 "structural-quality-and-smart-design-influence-value-of-high-rise-apartments": "highrise",
 "why-chattanooga-tn-is-perfect-for-families-guide-to-moving": "moving",
}

def classify(slug):
    if slug in OVERRIDES:
        return OVERRIDES[slug]
    for pat, key in RULES:
        if re.search(pat, slug):
            return key
    return "essentials"

# ---------------------------------------------------------------- block builder
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def build_block(key):
    heading, intro, items = SETS[key]
    li = []
    for name, q, why in items:
        li.append('<!-- wp:list-item -->\n<li><a href="%s" %s><strong>%s</strong></a> &#8211; %s.</li>\n<!-- /wp:list-item -->'
                  % (amz(q), REL, html.escape(name), html.escape(why)))
    return "\n\n".join([
        MARK,
        '<!-- wp:separator -->\n<hr class="wp-block-separator has-alpha-channel-opacity"/>\n<!-- /wp:separator -->',
        '<!-- wp:heading {"level":3} -->\n<h3 class="wp-block-heading" id="h-%s">%s</h3>\n<!-- /wp:heading -->' % (slugify(heading), html.escape(heading)),
        '<!-- wp:paragraph -->\n<p>%s</p>\n<!-- /wp:paragraph -->' % html.escape(intro),
        '<!-- wp:list -->\n<ul class="wp-block-list">' + "\n\n".join(li) + '</ul>\n<!-- /wp:list -->',
        '<!-- wp:paragraph {"fontSize":"small"} -->\n<p class="has-small-font-size"><em>Rise Apartments is a participant in the Amazon Services LLC Associates Program. As an Amazon Associate we earn from qualifying purchases made through the links above, at no extra cost to you.</em></p>\n<!-- /wp:paragraph -->',
    ]) + "\n\n"

END_HEADINGS = re.compile(r"conclusion|final thoughts|frequently asked|\bfaqs?\b|wrapping up|the bottom line|key takeaways", re.I)

def insert_point(raw):
    """Offset where the block goes: before the first Conclusion/FAQ heading block, else end."""
    for m in re.finditer(r"<!-- wp:heading[^>]*-->\s*<h[1-6][^>]*>(.*?)</h[1-6]>", raw, flags=re.S):
        text = re.sub("<[^>]+>", "", m.group(1))
        if END_HEADINGS.search(text):
            return m.start()
    # no closing section: put it before a trailing AdSense html block if there is one
    m = re.search(r"<!-- wp:html -->\s*<script[^>]*adsbygoogle.*?<!-- /wp:html -->\s*$", raw, flags=re.S)
    return m.start() if m else len(raw)

def inject(raw, key):
    if MARK in raw:
        return None
    i = insert_point(raw)
    block = build_block(key)
    before, after = raw[:i].rstrip("\n"), raw[i:]
    return (before + "\n\n" if before else "") + block + after.lstrip("\n")

# ---------------------------------------------------------------- data access
def auth_header():
    u, p = os.environ.get("WP_USER"), os.environ.get("WP_APP_PASSWORD")
    if not (u and p):
        sys.exit("set WP_USER and WP_APP_PASSWORD")
    return "Basic " + base64.b64encode(f"{u}:{p}".encode()).decode()

def api(path, data=None, method=None):
    req = urllib.request.Request(SITE + "/wp-json/wp/v2" + path,
                                 data=json.dumps(data).encode() if data is not None else None,
                                 method=method or ("POST" if data is not None else "GET"),
                                 headers={"Authorization": auth_header(), "Content-Type": "application/json",
                                          "User-Agent": "rise-affiliate-links/1.0"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r), r.headers
        except Exception as e:  # noqa
            if attempt == 4:
                raise
            time.sleep(2 ** attempt)

def fetch_posts():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    posts, page = [], 1
    while True:
        data, hdr = api(f"/posts?per_page=100&page={page}&status=publish&context=edit&_fields=id,slug,link,title,categories,content")
        posts += data
        if page >= int(hdr.get("X-WP-TotalPages", "1")):
            break
        page += 1
    json.dump(posts, open(CACHE, "w"))
    return posts

def norm_title(t):
    t = html.unescape(t).strip()
    t = re.sub(r"\s*\|\s*(Rise Apartments|Get Rewards When You Lease|Lease & Earn Rewards|Free Apartment Locator in Texas)\s*$", "", t)
    return t.lower()

def load_views():
    views = collections.Counter()
    lines = [l for l in open(ANALYTICS, encoding="utf-8-sig") if not l.startswith("#") and l.strip()]
    for row in csv.DictReader(lines):
        try:
            views[norm_title(row["Page title and screen class"])] += int(row["Views"])
        except (KeyError, ValueError):
            pass
    return views

def targets(posts, views):
    out = []
    for p in posts:
        raw = p["content"]["raw"]
        v = views.get(norm_title(p["title"]["rendered"]), 0)
        if v <= 0:
            continue
        if "amzn.to" in raw or "amazon." in raw:
            continue  # already monetized by hand
        out.append((v, p))
    out.sort(key=lambda x: -x[0])
    return out

# ---------------------------------------------------------------- main
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "plan"
    posts = fetch_posts()
    views = load_views()
    plan = targets(posts, views)
    rows = []
    for v, p in plan:
        key = classify(p["slug"])
        rows.append({"views": v, "id": p["id"], "slug": p["slug"], "title": html.unescape(p["title"]["rendered"]),
                     "url": p["link"], "set": key, "heading": SETS[key][0]})
    with open(os.path.join(HERE, "report.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["views", "id", "slug", "title", "url", "set", "heading", "status"])
        w.writeheader()
        if mode == "plan":
            for r in rows:
                w.writerow({**r, "status": "planned"})
            print(f"{len(rows)} posts planned; set counts: {collections.Counter(r['set'] for r in rows).most_common()}")
            return
        if mode == "apply":
            done = 0
            for r in rows:
                p = next(x for x in posts if x["id"] == r["id"])
                new = inject(p["content"]["raw"], r["set"])
                if new is None:
                    r["status"] = "skipped-already-marked"
                else:
                    try:
                        api(f"/posts/{r['id']}", {"content": new})
                        r["status"] = "updated"
                        done += 1
                    except Exception as e:  # noqa
                        r["status"] = f"error: {e}"
                w.writerow(r)
                fh.flush()
                print(r["status"], r["id"], r["slug"], flush=True)
            print(f"updated {done}/{len(rows)}")

if __name__ == "__main__":
    main()
