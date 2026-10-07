"""Amazon Associates product picks, and where each one is shown.

Links are Amazon *search* URLs carrying the Associates tag, so they never
point at a discontinued product and show readers current options and prices.
No prices or Amazon images are shown (Associates rules require the API for
those).
"""
from urllib.parse import quote_plus

AMAZON_TAG = "josephrayditt-20"
DISCLOSURE = "As an Amazon Associate, Renter News earns from qualifying purchases."


def amazon(query):
    return f"https://www.amazon.com/s?k={quote_plus(query)}&tag={AMAZON_TAG}"


# key: (name, search query, why a renter wants it, icon)
PRODUCTS = {
    "smoke":     ("10-year smoke alarm", "10 year sealed battery smoke alarm", "Sealed battery, no chirping replacements. Ask your landlord first; many leases make alarms their job.", "zap"),
    "co":        ("Plug-in carbon monoxide alarm", "plug in carbon monoxide detector battery backup", "Needed in any unit with gas appliances, a fireplace or an attached garage.", "shield"),
    "ext":       ("Home fire extinguisher", "home fire extinguisher 2-A:10-B:C", "A 2-A:10-B:C rating covers ordinary, grease and electrical fires. Keep it near the kitchen exit.", "flame"),
    "blanket":   ("Kitchen fire blanket", "kitchen fire blanket", "Smothers a small pan fire without the mess of an extinguisher.", "flame"),
    "ladder":    ("Fire escape ladder", "fire escape ladder 2 story", "For second- and third-floor bedrooms where a window is the second way out.", "home"),
    "docbag":    ("Fireproof document bag", "fireproof document bag", "Keeps your lease, IDs, passports and insurance papers together and grab-ready.", "book"),
    "gobag":     ("Emergency go-bag kit", "emergency go bag kit", "Water, light, first aid and essentials in one bag if you must leave fast.", "umbrella"),
    "radio":     ("NOAA weather alert radio", "noaa weather alert radio hand crank", "Sounds National Weather Service warnings even when cell service or power is out.", "cloud"),
    "flashlight": ("Rechargeable flashlight", "rechargeable led flashlight", "For outages and smoky hallways; keep one by the bed.", "zap"),
    "powerbank": ("Portable power bank", "portable power bank high capacity", "Keeps your phone alive during an evacuation or a long outage.", "zap"),
    "battbag":   ("Fireproof battery charging bag", "lithium battery fireproof charging bag", "Contains a failing e-bike or scooter battery while it charges.", "shield"),
    "heater":    ("Space heater with tip-over shutoff", "space heater tip over overheat protection", "If you must use one, pick automatic tip-over and overheat shutoff.", "flame"),
    "boxes":     ("Moving boxes kit", "moving boxes kit with packing paper", "Box sets sized for apartments, usually cheaper than buying one at a time.", "truck"),
    "tape":      ("Packing tape and dispenser", "packing tape with dispenser", "Seals boxes in seconds; buy more than you think you need.", "truck"),
    "dolly":     ("Furniture moving straps and dolly", "furniture moving straps dolly", "Saves backs, walls and doorframes, and your security deposit.", "truck"),
    "toolkit":   ("Apartment tool kit", "home tool kit apartment", "For small fixes, furniture assembly and documenting move-in issues.", "home"),
    "cleaning":  ("Move-out cleaning kit", "cleaning supplies kit", "A spotless unit is the easiest way to get your full deposit back.", "check"),
    "budget":    ("Monthly budget planner", "monthly budget planner", "Track rent, utilities and savings as prices change.", "wallet"),
}

# Article category -> three picks
BY_CATEGORY = {
    "fire":           ["smoke", "ext", "ladder"],
    "safety":         ["smoke", "co", "ext"],
    "guides":         ["gobag", "docbag", "smoke"],
    "tenant-rights":  ["docbag", "toolkit", "smoke"],
    "rent-prices":    ["boxes", "budget", "docbag"],
    "housing-policy": ["docbag", "budget", "boxes"],
}

# Article-specific picks win when a slug contains the keyword
BY_KEYWORD = [
    ("lithium", ["battbag", "ext", "smoke"]),
    ("e-bike", ["battbag", "ext", "smoke"]),
    ("carbon-monoxide", ["co", "smoke", "flashlight"]),
    ("lightning", ["radio", "powerbank", "smoke"]),
    ("cooking", ["blanket", "ext", "smoke"]),
    ("first-72-hours", ["gobag", "docbag", "powerbank"]),
    ("renters-insurance", ["docbag", "smoke", "ext"]),
    ("smoke-alarms", ["smoke", "co", "ladder"]),
    ("security-deposit", ["cleaning", "toolkit", "docbag"]),
    ("habitability", ["toolkit", "docbag", "co"]),
    ("scam", ["docbag", "budget", "boxes"]),
    ("senior", ["smoke", "flashlight", "ladder"]),
]

# Tool page -> picks shown under the calculator
BY_TOOL = {
    "rent-affordability-calculator": ["budget", "boxes", "docbag"],
    "rent-split-calculator": ["budget", "boxes", "toolkit"],
    "rent-increase-calculator": ["budget", "boxes", "docbag"],
    "moving-cost-calculator": ["boxes", "tape", "dolly"],
    "rent-vs-buy-calculator": ["budget", "docbag", "toolkit"],
    "renters-insurance-calculator": ["docbag", "smoke", "ext"],
    "lease-notice-calculator": ["boxes", "cleaning", "dolly"],
    "fire-safety-checklist": ["smoke", "co", "ext", "blanket", "ladder", "battbag"],
}

WEATHER = ["radio", "flashlight", "powerbank"]
SIDEBAR = ["smoke", "co", "ext", "docbag"]

# Sections of the /renter-safety-gear/ page
GEAR_PAGE = [
    ("Fire safety", ["smoke", "co", "ext", "blanket", "ladder", "battbag"]),
    ("Emergencies and outages", ["gobag", "radio", "flashlight", "powerbank", "docbag"]),
    ("Moving day", ["boxes", "tape", "dolly", "cleaning", "toolkit"]),
    ("Money", ["budget"]),
]


def picks_for_article(slug, category):
    for kw, keys in BY_KEYWORD:
        if kw in slug:
            return keys
    return BY_CATEGORY.get(category, ["smoke", "ext", "docbag"])
