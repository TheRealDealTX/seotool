"""Site-wide constants for the live-style.co.uk rebuild."""

from datetime import date

SITE = {
    "name": "Live-Style",
    "tagline": "Interiors, design & the art of living well",
    "origin": "https://live-style.co.uk",
    "email": "info@live-style.co.uk",
    "locale": "en_GB",
    "founded": "2013",
}

CATEGORIES = [
    ("interiors", "Interiors"),
    ("design-makers", "Design & Makers"),
    ("art-prints", "Art & Prints"),
    ("renovation-diary", "Renovation Diary"),
    ("shopping", "Shopping"),
    ("food-drink", "Food & Drink"),
    ("places", "Places"),
    ("january-cure", "January Cure"),
    ("lifestyle", "Lifestyle"),
]
CATEGORY_BY_NAME = {name: slug for slug, name in CATEGORIES}

# Image used for each category tile / header (filenames in assets/img/).
CATEGORY_IMAGES = {
    "interiors": "home-boho-living.jpg",
    "design-makers": "bocci-heals-lighting.jpg",
    "art-prints": "outline-editions.jpg",
    "renovation-diary": "little-greene-paint.jpg",
    "shopping": "aram-store.jpg",
    "food-drink": "favourite-restaurants.jpg",
    "places": "home-london.jpg",
    "january-cure": "january-cure.jpg",
    "lifestyle": "take-your-pleasure-seriously.jpg",
}

NAV = [
    ("Interiors", "/category/interiors/"),
    ("Design", "/category/design-makers/"),
    ("Art", "/category/art-prints/"),
    ("Renovation", "/category/renovation-diary/"),
    ("Food & Places", "/category/food-drink/"),
    ("Journal", "/journal/"),
    ("About", "/about/"),
]

TODAY = date.today().isoformat()
