"""Firm details, practice constants and navigation for claimsconsultant.com.

Everything a human needs to change before launch lives in this file. build.py
and every module under content/ import from here, so the phone number, the
positioning line and the service-area list are each defined exactly once.

The phone number is live. Anything still marked TODO is a placeholder: fill it
in, run `python3 build.py`, and it updates everywhere on the site at once.
"""

from datetime import date

BIZ = {
    "name": "Claims Consultant",
    "legal_name": "Claims Consultant",           # TODO: registered entity name
    "tagline": "Expert Witness & Damage Consulting",
    "descriptor": ("expert witnesses and damage consultants retained by policyholders, "
                   "insurers, risk pools, brokers and counsel on large commercial property "
                   "losses"),
    "phone_display": "(832) 503-5866",
    "phone_href": "+18325035866",
    "email": "info@claimsconsultant.com",        # TODO: real inbox
    "origin": "https://claimsconsultant.com",
    "city": "Houston",
    "state": "TX",
    "state_long": "Texas",
    "region": "Texas and the Gulf Coast",
    "latitude": "29.7604",
    "longitude": "-95.3698",
    "founded": "",                               # TODO: real year founded (omitted from schema while blank)
    # Texas licences. Both are held; the numbers go in when you have them to
    # hand, and they then render in the top bar and the footer automatically.
    "license_ia": "",                            # TODO: adjuster licence no. (Tex. Ins. Code ch. 4101)
    "license_pa": "",                            # TODO: public insurance adjuster licence no. (ch. 4102)
    "credential": "",                            # TODO: e.g. "HAAG / IICRC certified" — omitted while blank
    "hours": "Mo-Fr 08:00-18:00",
}

# Subject-matter references quoted across the site. These describe the law we
# work within, not a licence we hold — see /disclaimer/.
STATUTE = {
    "prompt_pay": "Tex. Ins. Code ch. 542, subch. B",
    "forces_of_nature": "Tex. Ins. Code ch. 542A",
    "ack_days": "15",
    "decide_days": "15 business",
    "pay_days": "5 business",
    "presuit_days": "61",
}

# How we are paid. Stated in one place because it appears on several pages and
# because it is the thing that makes working either side possible.
# Expert, consulting and appraisal work is never contingent. Public adjusting
# is the one capacity where a percentage basis may apply, capped by statute.
FEES = {
    "basis": "Hourly, fixed-fee or per-project",
    "not": "Never contingent on expert or consulting work",
    "pa_cap": "10%",
    "pa_cite": "Tex. Ins. Code &sect;4102.104",
}

NAV = [
    ("Services", "/services/"),
    ("Loss Types", "/loss-types/"),
    ("Who We Serve", "/who-we-serve/"),
    ("Tools", "/tools/"),
    ("Insights", "/blog/"),
    ("Firm", "/about/"),
]

FOOTER_SERVING = (
    "Houston &middot; Austin &middot; Dallas&ndash;Fort Worth &middot; San Antonio "
    "&middot; Corpus Christi &middot; Rio Grande Valley &middot; statewide Texas"
)

def license_line(sep=" &middot; "):
    """"TDI Adjuster #x · Public Adjuster #y", or "" until the numbers exist."""
    parts = []
    if BIZ.get("license_ia"):
        parts.append("TDI Adjuster #%s" % BIZ["license_ia"])
    if BIZ.get("license_pa"):
        parts.append("Public Adjuster #%s" % BIZ["license_pa"])
    if BIZ.get("credential"):
        parts.append(BIZ["credential"])
    return sep.join(parts)


TODAY = date.today().isoformat()
YEAR = date.today().year
