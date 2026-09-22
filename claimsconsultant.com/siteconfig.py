"""Firm details, practice constants and navigation for claimsconsultant.com.

Everything a human needs to change before launch lives in this file. build.py
and every module under content/ import from here, so the phone number, the
license line and the service-area list are each defined exactly once.

The phone number is live. Anything still marked TODO is a placeholder: fill it
in, run `python3 build.py`, and it updates everywhere on the site at once.
"""

from datetime import date

BIZ = {
    "name": "Claims Consultant",
    "legal_name": "Claims Consultant",           # TODO: registered entity name
    "tagline": "Large-Loss Public Adjusters",
    "descriptor": "public insurance adjusters for institutional and large commercial property losses",
    "phone_display": "(832) 503-5866",
    "phone_href": "+18325035866",
    "email": "claims@claimsconsultant.com",      # TODO: real inbox
    "origin": "https://claimsconsultant.com",
    "city": "Austin",
    "state": "TX",
    "state_long": "Texas",
    "region": "Texas and the Gulf Coast",
    "latitude": "30.2672",
    "longitude": "-97.7431",
    "founded": "",                               # TODO: real year founded (omitted from schema while blank)
    "license": "",                               # TODO: e.g. "TDI #1234567" — left blank, copy adapts
    "hours": "Mo-Fr 08:00-18:00",
}

# Public-adjuster licensing statute and fee cap, quoted on several pages.
STATUTE = {
    "chapter": "Chapter 4102, Texas Insurance Code",
    "fee_cap": "10%",
    "fee_cite": "Tex. Ins. Code &sect;4102.104",
    "prompt_pay": "Tex. Ins. Code ch. 542, subch. B",
    "forces_of_nature": "Tex. Ins. Code ch. 542A",
}

NAV = [
    ("Who We Serve", "/who-we-serve/"),
    ("Services", "/services/"),
    ("Tools", "/tools/"),
    ("Service Areas", "/service-areas/"),
    ("Insights", "/blog/"),
    ("Firm", "/about/"),
]

# Rendered in the footer's first column and in several schema blocks.
FOOTER_SERVING = (
    "Austin &middot; Houston &middot; Dallas&ndash;Fort Worth &middot; San Antonio "
    "&middot; Corpus Christi &middot; Rio Grande Valley &middot; statewide Texas"
)

TODAY = date.today().isoformat()
YEAR = date.today().year
