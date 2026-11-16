"""Business facts and navigation for policyholderappraiser.com.

Everything that could change (phone, email, license, service list order) is
defined here once and imported by build.py and the content modules.
"""

from datetime import date

BIZ = {
    "name": "Policyholder Appraiser",
    "legal_name": "Rise Public Adjusting LLC",
    "tagline": "Independent insurance appraisers for Texas policyholders",
    "phone_display": "(832) 503-5866",
    "phone_href": "+18325035866",
    "email": "josephdittmanappraiser@gmail.com",
    "origin": "https://policyholderappraiser.com",
    "state": "TX",
    "state_long": "Texas",
    "region": "Texas",
    "license_label": "Texas public adjuster license #3341461",
    "license_number": "3341461",
    "ia_license_number": "2341686",
    "firm_license_number": "3356839",
    "principal": "Joseph Dittman",
    "principal_title": "Certified insurance appraiser and umpire; licensed Texas public and independent adjuster",
    "hours": "Mon-Sat 8:00 am - 7:00 pm",
}

# Markets named on the service-area page and in schema. Statewide service,
# no per-city pages: the appraisal process is the same everywhere in Texas.
MARKETS = [
    "Houston", "Dallas", "Fort Worth", "San Antonio", "Austin",
    "Corpus Christi", "Beaumont", "Galveston", "Sugar Land", "The Woodlands",
    "McAllen", "Lubbock", "El Paso", "Waco", "Tyler",
]

NAV = [
    ("Services", "/services/"),
    ("Areas Served", "/service-areas/"),
    ("How Appraisal Works", "/appraisal-process/"),
    ("2027 Rules", "/texas-appraisal-rules/"),
    ("Guides", "/guides/"),
    ("Blog", "/blog/"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
]

TODAY = date.today().isoformat()
