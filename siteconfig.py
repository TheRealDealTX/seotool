"""Business, brand and navigation constants for beltonbanners.com.

Imported by build.py and every module under content/ so that the phone
number, email, brand names and keyword strings are defined exactly once.
"""

from datetime import date

BIZ = {
    "name": "Christina Dittman Creations",
    "short": "CDC",
    "brand_alt": "Belton Banners",           # the primary keyword, title-cased
    "keyword": "belton banners",              # the primary keyword, as typed
    "tagline": "Custom hand-painted banners for life's most meaningful moments",
    "phone_display": "+1 817-729-2961",
    "phone_short": "817-729-2961",
    "phone_href": "+18177292961",
    "email": "dittmanbanners@gmail.com",
    "origin": "https://beltonbanners.com",
    "city": "Belton",
    "state": "TX",
    "state_long": "Texas",
    "region": "Central Texas",
    "county": "Bell County",
    "latitude": "31.0560",
    "longitude": "-97.4642",
    "founder": "Christina Dittman",
    "logo": "/assets/img/brand/christina-dittman-creations-logo.webp",
    "og_image": "/assets/img/brand/christina-dittman-creations-site-image.webp",
}

NEARBY = ["Temple", "Killeen", "Harker Heights", "Salado", "Nolanville", "Troy", "Copperas Cove"]
FOOTER_SERVING = "Serving Belton, Temple, Killeen, Harker Heights, Salado &amp; Central Texas"

SIZES = ['30" x 30"', '36" x 30"', '48" x 30"', '60" x 30"', '36" x 60"']

NAV = [
    ("Custom Banners", "/custom-banners/"),
    ("Gallery", "/gallery/"),
    ("How It Works", "/how-it-works/"),
    ("Pricing", "/pricing-and-sizes/"),
    ("About", "/about-christina-dittman-creations/"),
    ("Blog", "/blog/"),
    ("Contact", "/contact-us/"),
]

TODAY = date.today().isoformat()
