"""Site-wide settings, the URL inventory, and the legacy redirect map.

Everything that decides *what URLs exist* lives here, so build.py, validate.py
and the redirect report all read from one place.
"""

SITE = {
    "name": "Arrive Outdoors",
    "domain": "arriveoutdoors.com",
    "url": "https://arriveoutdoors.com",
    "tagline": "Plan it right. Pack it light. Arrive ready.",
    "description": ("Free camping and hiking tools, month-by-month weather guides for "
                    "national parks, and honest gear advice for getting outside."),
    "email": "info@arriveoutdoors.com",
    "amazon_tag": "arriveoutdoors-20",
    # Google tag carried over from the WordPress install (Site Kit).
    "gtag": "GT-PL9QXXQN",
    # AdSense publisher from ads.txt. Auto ads are off: with this little traffic
    # they cost page speed and earn nothing. Flip to True to load them.
    "adsense_client": "ca-pub-3886800648957674",
    "adsense_on": False,
}

# Byline used on every article. Replace with a real person (name, photo, bio,
# outdoor background) as soon as possible: a named, credible author is one of
# the strongest trust signals for this kind of site.
AUTHOR = {
    "name": "The Arrive Outdoors Team",
    "url": "/about/",
    "bio": ("We write about camping, hiking and trip planning, and we build the free "
            "tools on this site. Every guide is reviewed against park-service and "
            "manufacturer sources before it is published and re-checked each season."),
}

NAV = [
    ("Destinations", "/destinations/"),
    ("Weather", "/weather/"),
    ("Tools", "/tools/"),
    ("Guides", "/guides/"),
    ("Gear", "/gear/"),
]

CATEGORIES = {
    "camping": "Camping",
    "hiking": "Hiking & Scrambling",
    "backpacking": "Backpacking",
    "skills": "Safety & Skills",
    "gear": "Gear",
    "rentals": "Renting Gear",
    "places": "Places",
}

# Tool pages: /tools/<slug>/
TOOLS = [
    # slug, name, one-line description, icon
    ("packing-list", "Camping & Backpacking Packing List Generator",
     "A checklist built for your trip type, nights, season and group size. Tick it off, print it, or save it.", "backpack"),
    ("trail-weather", "Trail Weather Forecast & Hike Score",
     "7-day forecast for any trailhead with a go/no-go hike score, heat, wind, storm and freezing-level warnings.", "cloud-sun"),
    ("hiking-time-calculator", "Hiking Time Calculator",
     "How long a hike will take from distance, elevation gain and pace, plus a turnaround time before dark.", "timer"),
    ("water-calculator", "Hiking Water Calculator",
     "How much water to carry for a hike based on duration, temperature, effort and body weight.", "droplet"),
    ("sleeping-bag-temperature", "Sleeping Bag & Pad Temperature Guide",
     "Pick the bag rating and pad R-value you need for the lowest temperature you expect.", "moon"),
    ("backpack-size", "Backpack Size & Torso Fit Calculator",
     "Find your pack size from torso length and hip size, and the right capacity for your trip.", "ruler"),
    ("sunrise-sunset", "Sunrise, Sunset & Daylight Calculator",
     "Sunrise, sunset, golden hour and usable daylight for any place and date.", "sunrise"),
    ("camp-meal-planner", "Camp Meal & Food Weight Planner",
     "Calories and food weight per day for your group, with a meal plan you can adjust.", "utensils"),
    ("rent-vs-buy", "Rent vs Buy Camping Gear Calculator",
     "Find the break-even point between renting and buying a tent, bag, pad and pack.", "scale"),
    ("feels-like", "Wind Chill & Heat Index Calculator",
     "What the air really feels like on the trail, and when it becomes dangerous.", "thermometer"),
]

# Destinations: /destinations/<slug>/. Coordinates are the main visitor hub,
# used for the climate normals (scripts/fetch_climate.py) and the live forecast.
DESTINATIONS = [
    # slug, name, state, lat, lon, elevation_m, hub label
    ("yosemite", "Yosemite National Park", "California", 37.7456, -119.5936, 1220, "Yosemite Valley"),
    ("joshua-tree", "Joshua Tree National Park", "California", 34.0122, -116.1680, 1270, "Hidden Valley"),
    ("grand-canyon", "Grand Canyon National Park", "Arizona", 36.0544, -112.1401, 2100, "South Rim (Grand Canyon Village)"),
    ("zion", "Zion National Park", "Utah", 37.2002, -112.9867, 1280, "Zion Canyon / Springdale"),
    ("yellowstone", "Yellowstone National Park", "Wyoming", 44.4605, -110.8281, 2240, "Old Faithful"),
    ("great-smoky-mountains", "Great Smoky Mountains National Park", "Tennessee & North Carolina", 35.6852, -83.5361, 450, "Sugarlands / Gatlinburg"),
    ("rocky-mountain", "Rocky Mountain National Park", "Colorado", 40.3666, -105.5600, 2500, "Beaver Meadows / Estes Park"),
    ("glacier", "Glacier National Park", "Montana", 48.5280, -113.9870, 975, "Apgar / Lake McDonald"),
    ("acadia", "Acadia National Park", "Maine", 44.3386, -68.2733, 30, "Bar Harbor"),
    ("olympic", "Olympic National Park", "Washington", 47.8606, -123.9348, 175, "Hoh Rain Forest"),
    ("arches", "Arches National Park", "Utah", 38.6167, -109.6190, 1250, "Moab"),
    ("grand-teton", "Grand Teton National Park", "Wyoming", 43.7520, -110.7230, 2070, "Jenny Lake"),
    ("sequoia", "Sequoia National Park", "California", 36.5647, -118.7730, 2000, "Giant Forest"),
    ("death-valley", "Death Valley National Park", "California", 36.4570, -116.8670, -58, "Furnace Creek"),
    ("big-bend", "Big Bend National Park", "Texas", 29.2700, -103.3000, 1600, "Chisos Basin"),
    ("mount-rainier", "Mount Rainier National Park", "Washington", 46.7860, -121.7350, 1645, "Paradise"),
    ("bryce-canyon", "Bryce Canyon National Park", "Utah", 37.6283, -112.1677, 2400, "Bryce Canyon Lodge area"),
    ("shenandoah", "Shenandoah National Park", "Virginia", 38.5260, -78.4360, 1070, "Big Meadows"),
    ("cloud-peak-wilderness", "Cloud Peak Wilderness", "Wyoming", 44.3820, -107.1740, 2900, "Bighorn high country"),
    ("grand-mesa", "Grand Mesa", "Colorado", 39.0420, -108.0100, 3050, "Grand Mesa lakes"),
]

MONTHS = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]

# Articles (content/articles/<slug>.html). Slugs keep the WordPress URLs so any
# ranking or link equity they have carries over. A slug containing "/" keeps a
# legacy nested path (the 2019 Shopify-era post).
ARTICLES = [
    "blogs/the-outdoor-traveler/camping-101-a-guide-for-the-first-time-camper",
    "how-to-put-out-a-fire",
    "how-to-start-a-fire-with-wet-wood",
    "what-to-do-if-you-get-lost-in-the-woods",
    "backpacking-hygiene",
    "sawyer-squeeze-gravity-setup",
    "cool-a-tent-without-electricity",
    "cold-weather-camping",
    "bikepacking-food",
    "class-3-scramble",
    "class-4-scramble",
    "can-you-hike-el-capitan",
    "cloud-peak-wyoming",
    "grand-mesa-fishing",
    "how-to-measure-torso-length-for-backpack",
    "honda-crv-camper",
    "car-camping-essentials",
    "best-sun-hoodies-for-hiking",
    "best-camera-for-backpacking",
    "how-to-pose-for-hiking-pictures",
    "best-hiking-black-friday-deals",
    "best-camping-gear-to-rent-vs-buy",
    "renting-camp-gear-for-national-park-trips",
    "rent-camping-gear",
]

# ---------------------------------------------------------------------------
# Legacy URL handling. Every old URL we know about (WordPress posts that were
# merged or removed, posts deleted before the rebuild that still had internal
# links, the WooCommerce-style product/group pages, and the 2019–2023 Shopify
# rental-site paths that still have backlinks) is either redirected (301) to
# its closest equivalent or marked gone (410).
# Paths are matched with and without a trailing slash.
# ---------------------------------------------------------------------------
REDIRECTS = {
    # Merged duplicates
    "/class-3-scrambling/": ("/class-3-scramble/", "Merged: duplicate of Class 3 Scramble"),
    "/hiking-backpack-black-friday/": ("/best-hiking-black-friday-deals/", "Merged: duplicate Black Friday post"),
    "/how-to-look-good-in-hiking-pictures/": ("/how-to-pose-for-hiking-pictures/", "Merged: duplicate of How to Pose for Hiking Pictures"),
    "/camera-strap-for-hiking/": ("/best-camera-for-backpacking/", "Merged into the camera guide (carrying section)"),
    "/tips-for-renting-camping-equipment-for-a-trip/": ("/rent-camping-gear/", "Merged into the new rental hub"),
    "/arrive-outdoors-camping-gear-rental-review/": ("/about/", "Removed: first-person review of a rental service that no longer runs; brand searches land on the About page's history"),
    # Old WordPress pages / archives
    "/blogs/": ("/guides/", "Old blog index"),
    "/blogs/the-outdoor-traveler/": ("/guides/", "Old Shopify blog index"),
    "/faq/": ("/about/", "Old store FAQ"),
    "/category/blog/": ("/guides/", "WordPress category archive"),
    "/category/uncategorized/": ("/guides/", "WordPress category archive"),
    "/products/": ("/gear/", "Old product catalog"),
    "/group/boots/": ("/gear/#footwear", "Old product group"),
    "/group/camphike/": ("/gear/", "Old product group"),
    "/group/camphike/chairs/": ("/gear/#camp", "Old product group"),
    "/group/camphike/packs/": ("/gear/#packs", "Old product group"),
    "/group/camphike/tents/": ("/gear/#camp", "Old product group"),
    "/group/camphike/sleeping-bags/": ("/gear/#sleep", "Old product group"),
    "/group/camphike/camping-sets/": ("/gear/#camp", "Old product group"),
    "/products/deuter-speed-lite-26l-backpack/": ("/gear/#packs", "Old product page"),
    "/products/deuter-speed-lite-sl-30l-backpack-womens/": ("/gear/#packs", "Old product page"),
    "/products/deuter-aircontact-lite-40-10-mens-backpacking-pack/": ("/tools/backpack-size/", "Old product page"),
    "/products/deuter-kid-comfort-air-carrier/": ("/gear/#packs", "Old product page"),
    "/products/oboz-sawtooth-ii-low-waterproof-hiking-shoes/": ("/gear/#footwear", "Old product page"),
    "/products/oboz-womens-sawtooth-ii-low-waterproof-hiking-boot/": ("/gear/#footwear", "Old product page"),
    "/products/oboz-mens-bridger-mid-waterproof-hiking-boot/": ("/gear/#footwear", "Old product page"),
    "/products/oboz-womans-bridger-mid-waterproof-hiking-boot/": ("/gear/#footwear", "Old product page"),
    "/products/complete-backpacking-set-for-two/": ("/tools/packing-list/", "Old product page"),
    "/products/marmot-limelight-3-person-tent/": ("/gear/#camp", "Old product page"),
    "/products/amazon-basics-camping-chair/": ("/gear/#camp", "Old product page"),
    "/products/helinox-chair-one/": ("/gear/#camp", "Old product page"),
    # 2019–2023 rental-site paths that still have backlinks
    "/pages/": ("/destinations/", "Old rental site"),
    "/pages/parks/": ("/destinations/", "Old rental site: park list (Michigan DNR and other partner links)"),
    "/pages/about/": ("/about/", "Old rental site"),
    "/pages/how-it-works/": ("/rent-camping-gear/", "Old rental site"),
    "/pages/yosemite/": ("/destinations/yosemite/", "Old rental site"),
    "/pages/sunday-river/": ("/rent-camping-gear/", "Old rental site"),
    "/collections/": ("/gear/", "Old rental site"),
    "/collections/all/": ("/gear/", "Old rental site"),
    "/group/camphike/category/27/": ("/gear/", "Old rental site"),
    # Posts deleted before the rebuild that kept internal links / may have links
    "/appalachian-trail-shelters-a-hikers-lifeline-in-the-wilderness/": ("/destinations/great-smoky-mountains/", "Deleted earlier"),
    "/backpacking-lunch-ideas/": ("/tools/camp-meal-planner/", "Deleted earlier"),
    "/vegan-backpacking-food/": ("/tools/camp-meal-planner/", "Deleted earlier"),
    "/backpacking-luxury-items/": ("/tools/packing-list/", "Deleted earlier"),
    "/backpacking-necessities/": ("/tools/packing-list/", "Deleted earlier"),
    "/solo-backpacking/": ("/what-to-do-if-you-get-lost-in-the-woods/", "Deleted earlier"),
    "/best-base-layer-for-hiking/": ("/gear/#clothing", "Deleted earlier"),
    "/hiking-clothes-for-men/": ("/gear/#clothing", "Deleted earlier"),
    "/womens-hiking-shorts/": ("/gear/#clothing", "Deleted earlier"),
    "/mens-lightweight-hoodie/": ("/best-sun-hoodies-for-hiking/", "Deleted earlier"),
    "/womens-hiking-shirts-for-hot-weather/": ("/best-sun-hoodies-for-hiking/", "Deleted earlier"),
    "/easy-hikes-in-glacier-national-park/": ("/destinations/glacier/", "Deleted earlier"),
    "/west-glacier-hikes/": ("/destinations/glacier/", "Deleted earlier"),
    "/facing-the-teton-crest-trail-head-on/": ("/destinations/grand-teton/", "Deleted earlier"),
    "/hoh-river-trail/": ("/destinations/olympic/", "Deleted earlier"),
    "/how-to-carry-camera-while-hiking/": ("/best-camera-for-backpacking/", "Deleted earlier"),
    "/how-to-keep-a-tent-cool-in-the-summer/": ("/cool-a-tent-without-electricity/", "Deleted earlier"),
    "/ways-to-stay-cool-while-camping/": ("/cool-a-tent-without-electricity/", "Deleted earlier"),
    "/how-to-stay-clean-while-camping/": ("/backpacking-hygiene/", "Deleted earlier"),
    "/renting-camp-gear-for-beginners/": ("/rent-camping-gear/", "Deleted earlier"),
    "/where-to-rent-camping-gear-near-me/": ("/rent-camping-gear/", "Deleted earlier"),
    "/water-filter-backpacking/": ("/sawyer-squeeze-gravity-setup/", "Deleted earlier"),
    "/hiking-training-plan/": ("/tools/hiking-time-calculator/", "Deleted earlier"),
    "/resupply-pct-a-complete-guide-for-thru-hikers/": ("/tools/camp-meal-planner/", "Deleted earlier"),
    "/edge-of-the-world-arizona/": ("/destinations/grand-canyon/", "Deleted earlier"),
}

# Removed for good (HTTP 410). Off-topic or paid-placement content that should
# drop out of the index quickly rather than be redirected.
GONE = {
    "/book-your-luxury-villa-getaway/": "Off-topic paid guest post (St. John villa rentals) with a commercial outbound link",
    "/adventure-travel-planning-made-easy/": "Off-topic paid guest post (Guam freight forwarding)",
    "/things-to-do-in-fire-island/": "Off-topic beach travel post",
    "/hajar-mountains/": "Deleted earlier; international, outside the site's focus",
    "/mount-hua-shan-where-peaks-touch-sky/": "Deleted earlier; international, outside the site's focus",
    "/nangma-valley/": "Deleted earlier; international, outside the site's focus",
    "/hiking-in-patagonia/": "Deleted earlier; international, outside the site's focus",
    "/things-to-do-in-kenai-alaska/": "Deleted earlier; travel listicle, outside the site's focus",
    "/hello-world/": "WordPress default post",
}

# Old WordPress posts whose URL is kept and whose content was rewritten.
KEPT_FROM_WORDPRESS = [
    "blogs/the-outdoor-traveler/camping-101-a-guide-for-the-first-time-camper",
    "how-to-put-out-a-fire", "what-to-do-if-you-get-lost-in-the-woods", "backpacking-hygiene",
    "sawyer-squeeze-gravity-setup", "cool-a-tent-without-electricity", "bikepacking-food",
    "class-3-scramble", "class-4-scramble", "can-you-hike-el-capitan", "cloud-peak-wyoming",
    "grand-mesa-fishing", "how-to-measure-torso-length-for-backpack", "honda-crv-camper",
    "best-sun-hoodies-for-hiking", "best-camera-for-backpacking", "how-to-pose-for-hiking-pictures",
    "best-hiking-black-friday-deals", "best-camping-gear-to-rent-vs-buy",
    "renting-camp-gear-for-national-park-trips",
]
