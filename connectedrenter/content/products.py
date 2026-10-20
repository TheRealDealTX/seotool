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

WHY = {}  # asin -> our own blurb, filled below once products are chosen

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
