"""Site-wide constants for agadecor.com. Edit here, then `python3 build.py`."""

SITE = {
    "name": "AGA Décor",
    "name_plain": "AGA Decor",
    "tagline": "Art · Glamour · Ambiance",
    "origin": "https://agadecor.com",          # canonical origin once the domain points here
    "email": "hello@agadecor.com",               # shown on the site; create this mailbox before launch
    "region": "Chicago & the North Shore",
    "area_served": [
        "Chicago", "Park Ridge", "Evanston", "Wilmette", "Winnetka", "Glenview", "Highland Park",
        "Lake Forest", "Skokie", "Rosemont", "Des Plaines", "Schaumburg", "Oak Brook", "Naperville",
    ],
}

# Primary navigation: (label, href, [(sublabel, subhref), ...])
NAV = [
    ("Services", "/services", [
        ("Plan · Design · Décor", "/services"),
        ("Planning & Packages", "/wedding-planing"),
        ("Destination Weddings", "/destination-weddings"),
    ]),
    ("Décor Rental", "/decor-rental", [
        ("All Rentals", "/decor-rental"),
        ("Linens", "/linens"),
        ("Furniture", "/furniture"),
        ("Vases & Glass", "/vases"),
        ("Extras & Lighting", "/extras"),
    ]),
    ("Gallery", "/gallery", []),
    ("Journal", "/blog", []),
    ("About", "/about-us", [
        ("Our Studio", "/about-us"),
        ("Chicago Venue Guide", "/vendors"),
    ]),
]
