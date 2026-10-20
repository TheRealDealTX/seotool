"""Amazon affiliate shop.

Product data (ASIN, title, image, features) lives in products.json and comes from Amazon listings.
Prices and star ratings are deliberately NOT shown: Amazon Associates rules only allow them when
they come live from Amazon's API. WHY holds our own renter-focused blurb per ASIN.
"""
import json
import os
import re

AFFILIATE_TAG = "connectedrenter-20"

SHOP_CATS = {
    "moving-day": ("Moving Day Essentials", "truck", "Boxes, tape and gear that make the haul easier.", ("Hiring movers", "/moving-resources/movers/")),
    "damage-free": ("Damage-Free Decor", "home", "Make it yours without losing your deposit.", ("Get your deposit back", "/blog/how-to-get-your-security-deposit-back/")),
    "safety-security": ("Safety & Security", "lock", "Renter-friendly protection — no drilling, no rewiring.", ("Renters insurance guide", "/moving-resources/rental-insurance/")),
    "cleaning-deposit": ("Cleaning & Deposit Savers", "sparkles", "Move-out clean like a pro and patch the little stuff.", ("Move-out cleaning guide", "/moving-resources/maid-services/")),
    "kitchen-starter": ("First Kitchen", "box", "The basics to cook your first meal in a new place.", ("First apartment checklist", "/blog/first-apartment-checklist/")),
    "storage-small-space": ("Small-Space Storage", "sofa", "Find more room in closets, corners and under the bed.", ("Furnishing a rental", "/moving-resources/furniture/")),
    "energy-comfort": ("Energy & Comfort", "zap", "Stay comfortable and keep the power bill in check.", ("Electricity guide", "/moving-resources/electricity/")),
}

WHY = {
    "B00KP37XYS": "Lidded, tape-free boxes in the two sizes you actually need — small for books and kitchen, medium for everything else. They stack neatly in a truck and in a closet afterward.",
    "B075CR94J3": "Slide the dresser instead of dragging it. Sliders save your back on moving day and keep you from scraping the landlord's floors when you rearrange.",
    "B01J2GMUFA": "Two people, one couch, no drama. These straps move the weight to your shoulders and legs so heavy furniture is easier to carry down apartment stairs.",
    "B07JG459R7": "Moving trucks are dusty and storage units are worse. A zip-up bag keeps your mattress clean, dry and bed-bug-free from one apartment to the next.",
    "B0753NHZVQ": "The renter's best friend. Hang coats, bags and towels without putting a single hole in the wall — and peel them off cleanly at move-out.",
    "B07P32RHQ4": "Make your place feel like home with art on the walls, minus the nail holes your landlord could charge you to patch.",
    "B07FRDZ5NF": "A feature wall without paint or permission headaches. Peel-and-stick wallpaper comes off when your lease ends (always test a small spot first).",
    "B073Q7Q9B8": "Curtains without a drill. A tension rod fits inside the window frame, so there are no bracket holes to fill when you move out.",
    "B00186URTY": "Extra peace of mind for apartments and travel. It adds a lock on the inside of the door without changing the landlord's hardware.",
    "B09H2T18WD": "See who's at the door from your phone. Battery power means no rewiring — just check your lease or ask before mounting anything outside.",
    "B0CY3BZCX9": "Your landlord should provide working alarms, but an extra battery smoke and CO alarm for the bedroom is cheap insurance you can take with you.",
    "B00002ND64": "Kitchens are where most apartment fires start. A small home extinguisher under the sink can stop a grease or toaster fire before it spreads.",
    "B07MF3DY3C": "Scuffs on walls, doors and light switches are classic deposit deductions. A few minutes with a Magic Eraser before your walkthrough goes a long way.",
    "B0016HF5GK": "Carpet stains are another common deposit hit. A portable spot cleaner handles spills, pet accidents and move-out touch-ups yourself.",
    "B01NB0729G": "A slow drain is the most common maintenance request. Clear hair clogs yourself in two minutes, no harsh chemicals that can damage old pipes.",
    "B0007M43WW": "Nail holes happen. Patch them before you move out (if your lease allows) so small holes don't turn into a painting charge.",
    "B001167VIQ": "Everything you need to cook in your first apartment in one box — pans, pots and utensils — without buying piece by piece.",
    "B00GIBKC3K": "A complete knife set with a block for your countertop, so your first kitchen has the right knife for every job.",
    "B07PSKSG1M": "Meal prep, leftovers and pantry staples sorted. Lids snap together so cabinets stay tidy in a small kitchen.",
    "B00FLYWNYQ": "One appliance that replaces a pressure cooker, slow cooker and rice cooker — a big win when counter space is tight.",
    "B07JGWSB8T": "Turn the space under your bed into a closet for off-season clothes and extra bedding. A must for studios and small bedrooms.",
    "B01D58DRVC": "Doors are free storage. Hang it over a closet or pantry door for shoes, snacks or cleaning supplies — no screws required.",
    "B086G7QX2K": "Apartment closets are often just a rod. Hanging shelves add instant cubbies for sweaters, bags and folded clothes.",
    "B073WFCV1L": "Lift your bed a few inches and gain a whole storage zone underneath — pair them with under-bed bags.",
    "B01CS31QE0": "Block afternoon sun to keep rooms cooler and your A/C bill lower, plus darker bedrooms for better sleep. Hang them on a tension rod.",
    "B08PDDSDHY": "A fan uses far less electricity than cranking the A/C. A quiet tower fan fits in a corner and moves a lot of air.",
    "B07B8W2KHZ": "Put lamps and electronics on a schedule and switch them off from anywhere. No wiring changes — they plug right into the outlet.",
    "B07V6M3PDX": "Warm up a chilly room without heating the whole apartment. Tip-over and overheat protection matter in small spaces — check your lease for any heater rules.",
}

_HERE = os.path.dirname(os.path.abspath(__file__))


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load_products():
    path = os.path.join(_HERE, "..", "products.json")
    if not os.path.exists(path):
        return []
    items = json.load(open(path, encoding="utf-8"))
    seen = set()
    for p in items:
        s = slugify(p["name"])
        while s in seen:
            s += "-2"
        seen.add(s)
        p["slug"] = s
        p["url"] = f"https://www.amazon.com/dp/{p['asin']}?tag={AFFILIATE_TAG}"
        p["why"] = WHY.get(p["asin"], "")
    return [p for p in items if p["cat"] in SHOP_CATS]


PRODUCTS = load_products()
