"""Site-wide constants for shopvipgifts.com."""

from datetime import date

SITE = {
    "name": "Shop VIP Gifts",
    "origin": "https://shopvipgifts.com",
    "email": "info@shopvipgifts.com",
    "ver": "1",
}

TODAY = date.today().isoformat()

GUIDE_LINKS = [
    ("All gift guides", "/gift-guides/"),
    ("Gifts for Him", "/gifts-for-him/"),
    ("Gifts for Her", "/gifts-for-her/"),
    ("Corporate & Client Gifts", "/corporate-gifts/"),
    ("Luxury Gift Boxes & Baskets", "/luxury-gift-boxes/"),
    ("Experience Gifts", "/experience-gifts/"),
    ("Personalized Gifts", "/personalized-gifts/"),
]

TOOL_LINKS = [
    ("All free tools", "/tools/"),
    ("Gift Finder Quiz", "/gift-finder/"),
    ("Gift Budget Planner", "/gift-budget-planner/"),
    ("Gift Message Generator", "/gift-message-generator/"),
    ("Anniversary Gifts by Year", "/anniversary-gifts-by-year/"),
]

# (label, href, children)
NAV = [
    ("Gift Guides", "/gift-guides/", GUIDE_LINKS),
    ("Tools", "/tools/", TOOL_LINKS),
    ("Blog", "/blog/", None),
    ("About", "/about/", None),
    ("Contact", "/contact/", None),
]

FOOTER_COLS = [
    ("Gift guides", GUIDE_LINKS[1:]),
    ("Free tools", TOOL_LINKS[1:]),
    ("Company", [("About us", "/about/"), ("Blog", "/blog/"), ("Contact", "/contact/"),
                 ("Privacy policy", "/privacy-policy/"), ("Terms of use", "/terms/")]),
]
