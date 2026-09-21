"""Business, locality and navigation constants for huttoroofs.com.

Imported by build.py and by every module under content/ so that the phone
number, service-area list and other local facts are defined exactly once.
"""

from datetime import date

BIZ = {
    "name": "Hutto Roofers",
    "phone_display": "+1 (512) 297-7580",
    "phone_short": "(512) 297-7580",
    "phone_href": "+15122977580",
    "email": "info@huttoroofs.com",
    "origin": "https://huttoroofs.com",
    "city": "Hutto",
    "state": "TX",
    "state_long": "Texas",
    "zip": "78634",
    "county": "Williamson County",
    "region": "Central Texas",
    "latitude": "30.5427",
    "longitude": "-97.5467",
}

NEARBY = ["Round Rock", "Pflugerville", "Taylor", "Georgetown", "Manor"]
# Rendered on every page footer. Uses &amp; because it is emitted directly into HTML.
FOOTER_SERVING = "Serving Hutto, Round Rock, Pflugerville, Taylor, Georgetown &amp; Manor"

NAV = [
    ("Services", "/services/"),
    ("Service Areas", "/service-areas/"),
    ("Blog", "/blog/"),
    ("Why Us", "/#about"),
    ("Contact", "/#contact"),
]

TODAY = date.today().isoformat()
