"""Business facts, navigation and shared constants for alabamainsuranceappraiser.com.

Everything that appears on more than one page (phone, email, city list, nav)
is defined once here and imported by build.py and the content modules.
"""

from datetime import date

BIZ = {
    "name": "Alabama Insurance Appraiser",
    "short": "AIA",
    "phone_display": "+1 (844) 537-1427",
    "phone_short": "(844) 537-1427",
    "phone_href": "+18445371427",
    "email": "info@alabamainsuranceappraiser.com",
    "origin": "https://alabamainsuranceappraiser.com",
    "state": "AL",
    "state_long": "Alabama",
    "tagline": "Independent property insurance appraisal, estimating & claim documentation across Alabama",
}

# Statewide service cities. slug -> facts used by content/areas.py, the footer,
# the homepage city grid and the LocalBusiness areaServed list.
CITIES = [
    ("Birmingham", "birmingham-al"),
    ("Huntsville", "huntsville-al"),
    ("Montgomery", "montgomery-al"),
    ("Mobile", "mobile-al"),
    ("Tuscaloosa", "tuscaloosa-al"),
    ("Hoover", "hoover-al"),
    ("Auburn", "auburn-al"),
    ("Dothan", "dothan-al"),
    ("Decatur", "decatur-al"),
    ("Florence", "florence-al"),
    ("Gadsden", "gadsden-al"),
]

# Main navigation. Items with a list of children render as dropdowns.
NAV = [
    ("About", "/about-us/", None),
    ("Services", "/services/", "services"),
    ("Service Areas", "/service-areas/", "areas"),
    ("Tools", "/tools/", "tools"),
    ("Resources", "/blog/", "resources"),
    ("Contact", "/contact/", None),
]

TODAY = date.today().isoformat()

# (slug, menu name, one-line blurb, icon). Pages live at /services/<slug>/.
SERVICES = [
    ("property-insurance-appraisal", "Property Insurance Appraisal", "Independent amount-of-loss evaluation under your policy's appraisal clause.", "scale"),
    ("residential-property-appraisal", "Residential Property Appraisal", "Homes, condos, townhomes and rental property losses.", "home"),
    ("commercial-property-appraisal", "Commercial Property Appraisal", "Office, retail, multi-family, church and industrial buildings.", "building"),
    ("estimate-review", "Claim Estimate Review", "Line-by-line comparison of carrier and contractor estimates.", "compare"),
    ("xactimate-estimates", "Xactimate Estimates", "Detailed, defensible line-item repair estimates.", "file"),
    ("symbility-estimates", "Symbility Estimates", "Structured estimates on the Symbility (CoreLogic) platform.", "layers"),
    ("matterport-documentation", "Matterport Documentation", "3D scans, measurements and a permanent visual record.", "cube"),
    ("hail-damage-appraisal", "Hail Damage Appraisal", "Roof coverings, soft metals, siding and exterior finishes.", "hail"),
    ("wind-storm-damage-appraisal", "Wind & Storm Damage Appraisal", "Tornado, straight-line wind and hurricane losses.", "wind"),
    ("water-damage-appraisal", "Water Damage Appraisal", "Plumbing failures, roof leaks and interior water losses.", "droplets"),
    ("fire-smoke-damage-appraisal", "Fire & Smoke Damage Appraisal", "Structural repairs, cleaning, demolition and rebuild scope.", "flame"),
]

# (slug, name, blurb, icon). Pages live at /tools/<slug>/.
TOOLS = [
    ("claim-gap-calculator", "Claim Gap Calculator", "See how far apart two estimates are and what the gap means after deductible and depreciation.", "calculator"),
    ("depreciation-calculator", "Depreciation (ACV) Calculator", "Estimate actual cash value and recoverable depreciation for a damaged item.", "trending"),
    ("roof-square-calculator", "Roof Square Calculator", "Turn a building footprint and pitch into roof area, squares and waste.", "ruler"),
    ("hurricane-deductible-calculator", "Hurricane & Wind Deductible Calculator", "Convert a percentage deductible into dollars before you file.", "umbrella"),
    ("appraisal-readiness-checklist", "Appraisal Readiness Checklist", "An interactive checklist of the documents to gather before appraisal.", "clipboard"),
]

# Resource pages shown in the Resources dropdown (besides blog posts).
RESOURCES = [
    ("/insurance-appraisal-process/", "Appraisal Process", "How Alabama insurance appraisal works, step by step.", "list"),
    ("/faq/", "FAQ", "Straight answers to common appraisal questions.", "help"),
    ("/glossary/", "Claim Glossary", "Plain-English definitions of insurance claim terms.", "book"),
    ("/blog/", "Blog & Guides", "In-depth articles for Alabama property owners.", "file"),
]
