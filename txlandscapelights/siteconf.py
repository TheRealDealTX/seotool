"""Business details, cities, services, tools and icons for txlandscapelights.com."""

DOMAIN = "txlandscapelights.com"
BASE = f"https://{DOMAIN}"
NAME = "Texas Landscape Lights"
PHONE = "(281) 704-7210"
TEL = "tel:+12817047210"
PHONE_E164 = "+12817047210"
EMAIL = "info@txlandscapelights.com"
ASSET_V = "20261019"

# Service-area cities (each has a content/areas/<slug>.html page).
CITIES = [
    dict(slug="houston-tx", name="Houston, TX", short="Houston", lat=29.7604, lon=-95.3698, county="Harris County", region="Gulf Coast", blurb="River Oaks, Memorial, the Heights and Bellaire: lighting built for humidity, live oaks and storm season."),
    dict(slug="dallas-tx", name="Dallas, TX", short="Dallas", lat=32.7767, lon=-96.7970, county="Dallas County", region="North Texas", blurb="Preston Hollow, Highland Park and Lakewood: hail-ready fixtures for brick and stone estates."),
    dict(slug="austin-tx", name="Austin, TX", short="Austin", lat=30.2672, lon=-97.7431, county="Travis County", region="Hill Country", blurb="Limestone, cedar elms and hillside lots: low-glare lighting that respects the night sky."),
    dict(slug="san-antonio-tx", name="San Antonio, TX", short="San Antonio", lat=29.4241, lon=-98.4936, county="Bexar County", region="South Central", blurb="Alamo Heights, Olmos Park and the Dominion: Spanish revival, Hill Country stone and big oaks.", dy=12),
    dict(slug="fort-worth-tx", name="Fort Worth, TX", short="Fort Worth", lat=32.7555, lon=-97.3308, county="Tarrant County", region="North Texas", blurb="Westover Hills, Tanglewood and Crestline: classic brick homes and mature pecans."),
    dict(slug="plano-tx", name="Plano, TX", short="Plano", lat=33.0198, lon=-96.6989, county="Collin County", region="North Texas", blurb="Willow Bend and Legacy: HOA-friendly designs for brick traditionals and modern builds."),
    dict(slug="frisco-tx", name="Frisco, TX", short="Frisco", lat=33.1507, lon=-96.8236, county="Collin & Denton Counties", region="North Texas", blurb="Starwood, Newman Village and master-planned streets: new-build lighting done right.", dy=-8),
    dict(slug="the-woodlands-tx", name="The Woodlands, TX", short="The Woodlands", lat=30.1658, lon=-95.4613, county="Montgomery County", region="Gulf Coast", blurb="Tall pines, wooded lots and village design standards: subtle lighting under the canopy.", dy=-6),
    dict(slug="katy-tx", name="Katy, TX", short="Katy", lat=29.7858, lon=-95.8245, county="Harris, Fort Bend & Waller", region="Gulf Coast", dy=-8, blurb="Cinco Ranch, Cross Creek Ranch and Firethorne: patios, pools and new-construction yards."),
    dict(slug="sugar-land-tx", name="Sugar Land, TX", short="Sugar Land", lat=29.6197, lon=-95.6349, county="Fort Bend County", region="Gulf Coast", blurb="First Colony, Telfair and Sweetwater: lakeside homes, palms and deed-restricted streets.", dy=14),
    dict(slug="round-rock-tx", name="Round Rock, TX", short="Round Rock", lat=30.5083, lon=-97.6789, county="Williamson County", region="Hill Country", blurb="Forest Creek, Teravista and Brushy Creek: limestone accents and family backyards."),
    dict(slug="new-braunfels-tx", name="New Braunfels, TX", short="New Braunfels", lat=29.7030, lon=-98.1245, county="Comal & Guadalupe Counties", region="Hill Country", dy=14, blurb="River-adjacent and Hill Country lots: flood-smart, dark-sky-friendly outdoor lighting."),
]
MAP_SIDE = {"dallas-tx": "r", "fort-worth-tx": "l", "plano-tx": "r", "frisco-tx": "l", "katy-tx": "l", "sugar-land-tx": "r",
            "san-antonio-tx": "l", "new-braunfels-tx": "r", "austin-tx": "l", "round-rock-tx": "r", "houston-tx": "r", "the-woodlands-tx": "r"}

# Weather picker: service areas plus other big Texas cities.
WEATHER = [(c["slug"], c["name"], c["lat"], c["lon"]) for c in CITIES] + [
    ("el-paso", "El Paso, TX", 31.7619, -106.4850), ("corpus-christi", "Corpus Christi, TX", 27.8006, -97.3964),
    ("lubbock", "Lubbock, TX", 33.5779, -101.8552), ("amarillo", "Amarillo, TX", 35.2220, -101.8313),
    ("waco", "Waco, TX", 31.5493, -97.1467), ("tyler", "Tyler, TX", 32.3513, -95.3011),
    ("mcallen", "McAllen, TX", 26.2034, -98.2300), ("midland", "Midland, TX", 31.9974, -102.0779),
    ("galveston", "Galveston, TX", 29.3013, -94.7977), ("beaumont", "Beaumont, TX", 30.0802, -94.1266),
]
WEATHER.sort(key=lambda c: c[1])

SERVICES = [
    dict(slug="architectural-lighting", name="Architectural Lighting", art="facade", short="Uplighting, grazing and washing that bring out limestone, brick, columns, gables and entries."),
    dict(slug="pathway-driveway-lighting", name="Pathway & Driveway Lighting", art="path", short="Low-glare path lights, driveway markers and step lights that make every arrival safe and inviting."),
    dict(slug="tree-garden-lighting", name="Tree & Garden Lighting", art="tree", short="Live oaks, pecans, crape myrtles and palms, uplit or moonlit, plus beds and specimen plants."),
    dict(slug="patio-pool-lighting", name="Patio & Pool Lighting", art="patio", short="Outdoor kitchens, pergolas, string lights, pool decks and fire features for Texas evenings outside."),
    dict(slug="smart-lighting-controls", name="Smart Lighting Controls", art="controls", short="Astronomical timers, zones, dimming and app control that track Texas sunsets all year."),
    dict(slug="landscape-lighting-repair", name="Repairs & LED Upgrades", art="repair", short="Dead fixtures, cut wire, failing transformers and halogen-to-LED retrofits, whoever installed it."),
    dict(slug="commercial-landscape-lighting", name="Commercial & HOA Lighting", art="commercial", short="Monument signs, HOA entrances, multifamily, retail and church grounds lit for safety and curb appeal."),
]

TOOLS = [
    dict(slug="lighting-visualizer", name="Lighting Visualizer", icon="wand", short="Switch lighting layers on and off on a Texas home and see fixtures, watts and running cost update live."),
    dict(slug="energy-cost-calculator", name="Energy Cost Calculator", icon="bolt", short="Estimate nightly, monthly and yearly electricity cost for any landscape lighting system."),
    dict(slug="fixture-estimator", name="Fixture Count Estimator", icon="grid", short="Describe your yard and get a planning-level fixture count, total watts and transformer size."),
    dict(slug="transformer-sizing-calculator", name="Transformer & Voltage Drop", icon="plug", short="Size a low-voltage transformer and check voltage drop on a wire run before you dig."),
    dict(slug="led-savings-calculator", name="Halogen to LED Savings", icon="leaf", short="Compare an old halogen system with LED: energy, lamp replacements and payback."),
    dict(slug="color-temperature-guide", name="Color Temperature Explorer", icon="thermo", short="Slide from 2200K to 5000K and see which light color flatters brick, limestone and foliage."),
    dict(slug="sunset-timer-planner", name="Sunset & Timer Planner", icon="sunset", short="Month-by-month sunset times for 22 Texas cities with timer settings and yearly run hours."),
]

CATEGORIES = {
    "guides": ("Guides", "Cost, sizing, spacing and energy: practical planning guides for Texas homeowners."),
    "design-ideas": ("Design Ideas", "Techniques, color temperature and layouts that make a Texas property glow."),
    "maintenance": ("Maintenance", "Keep your system bright through Texas heat, storms, floods and freezes."),
}

# Lucide icon paths (ISC license).
ICONS = {
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "star": '<path d="M11.5 2.3a.5.5 0 0 1 1 0l2.3 4.7 5.2.8a.5.5 0 0 1 .3.9l-3.8 3.6.9 5.2a.5.5 0 0 1-.8.5L12 15.6l-4.6 2.4a.5.5 0 0 1-.8-.5l.9-5.2-3.8-3.6a.5.5 0 0 1 .3-.9l5.2-.8z"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "bulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "pin": '<path d="M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "wand": '<path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72"/><path d="m14 7 3 3"/><path d="M5 6v4"/><path d="M19 14v4"/><path d="M10 2v2"/><path d="M7 8H3"/><path d="M21 16h-4"/><path d="M11 3H9"/>',
    "bolt": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "grid": '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    "plug": '<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "thermo": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
    "sunset": '<path d="M12 10V2"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m16 6-4 4-4-4"/><path d="M16 18a4 4 0 0 0-8 0"/>',
    "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "up": '<path d="m18 15-6-6-6 6"/>',
    "cal": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "wind": '<path d="M12.8 19.6A2 2 0 1 0 14 16H2"/><path d="M17.5 8a2.5 2.5 0 1 1 2 4H2"/><path d="M9.8 4.4A2 2 0 1 1 11 8H2"/>',
}


def icon(name, cls=""):
    return (f'<svg class="ico {cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')
