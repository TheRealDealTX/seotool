"""Business, locality and navigation constants for rooftarp.com.

Imported by build.py and by every module under content/ so that the phone
number, metro list and other facts are defined exactly once.

Brand tokens below are the live site's own Elementor globals, carried over so
the rebuild keeps the same identity:
    primary #18230F, secondary #27391C, accent #1F7D53, alert #D20000,
    text #252525.
"""

from datetime import date

BIZ = {
    "name": "Roof Tarp",
    "legal_name": "Roof Tarp",
    "phone_display": "+1 (956) 465-6045",
    "phone_short": "(956) 465-6045",
    "phone_href": "+19564656045",
    "dispatch_display": "(210) 903-9471",
    "dispatch_href": "+12109039471",
    "email": "info@rooftarp.com",
    "origin": "https://rooftarp.com",
    "state": "TX",
    "state_long": "Texas",
    "region": "Texas",
    # Registered operating base. Individual metro pages carry their own
    # geography; this is the business address for LocalBusiness schema.
    "city": "Hutto",
    "zip": "78634",
    "county": "Williamson County",
    "latitude": "30.5427",
    "longitude": "-97.5467",
}

# Response promise used in copy and schema. Defined once so the number never
# drifts between pages.
RESPONSE_WINDOW = "within hours of your call"

NAV = [
    ("Services", "/services/"),
    ("Service Areas", "/service-areas/"),
    ("Blog", "/blog/"),
    ("FAQs", "/faqs/"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
]

FOOTER_SERVING = (
    "Emergency roof tarping across Texas &mdash; Houston, Dallas, Fort Worth, "
    "Austin, San Antonio, El Paso, Lubbock &amp; Corpus Christi"
)

TODAY = date.today().isoformat()
