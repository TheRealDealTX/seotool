"""Business, navigation and tool registry for roofestimatepro.com.

Imported by build.py and the modules under content/ so contact details, the
tool list and the service-area facts are defined exactly once.
"""

from datetime import date

TODAY = date.today().isoformat()

BIZ = {
    "name": "Roof Estimate Pro",
    "phone_display": "(210) 903-9471",
    "phone_href": "+12109039471",
    "email": "contact@roofestimatepro.com",
    "origin": "https://roofestimatepro.com",
    "street": "2525 McKinnon St",
    "city": "Dallas",
    "state": "TX",
    "zip": "75201",
    "price_claim_review": 50,
    "price_scope": 200,
}

# Tool registry. Order here is the order on /tools/, in the nav and in the
# footer. "group" drives the tool-hub filter chips.
TOOLS = [
    {"slug": "roof-replacement-cost-calculator", "name": "Roof Replacement Cost Calculator",
     "short": "Replacement Cost", "group": "Cost", "icon": "house",
     "blurb": "Itemized Texas pricing for a full tear-off and re-roof: materials, labor, decking, permits and O&P."},
    {"slug": "roof-square-footage-calculator", "name": "Roof Square Footage Calculator",
     "short": "Roof Area & Squares", "group": "Measure", "icon": "ruler",
     "blurb": "Turn a footprint or plane-by-plane measurements into true roof area, squares and waste."},
    {"slug": "roof-pitch-calculator", "name": "Roof Pitch Calculator",
     "short": "Roof Pitch", "group": "Measure", "icon": "angle",
     "blurb": "Convert rise/run, degrees and percent; get the pitch multiplier, hip/valley factor and rafter length."},
    {"slug": "shingle-calculator", "name": "Shingle & Materials Calculator",
     "short": "Shingle Materials", "group": "Materials", "icon": "layers",
     "blurb": "Bundles, starter, ridge cap, underlayment, ice & water, drip edge, nails and vents for a shingle roof."},
    {"slug": "metal-roof-calculator", "name": "Metal Roof Calculator",
     "short": "Metal Roof", "group": "Materials", "icon": "panel",
     "blurb": "Panel counts and lengths, fasteners or clips, trim and installed cost for standing seam or R-panel."},
    {"slug": "flat-roof-calculator", "name": "Flat & Commercial Roof Calculator",
     "short": "Flat / Commercial", "group": "Materials", "icon": "building",
     "blurb": "TPO, EPDM, PVC, mod-bit and coatings: membrane rolls, insulation boards, fasteners and cost."},
    {"slug": "roof-insurance-claim-calculator", "name": "Roof Insurance Claim Calculator",
     "short": "Insurance Claim", "group": "Insurance", "icon": "shield",
     "blurb": "RCV, depreciation, deductible and O&P: see the first check, the holdback and your out-of-pocket."},
    {"slug": "roof-depreciation-calculator", "name": "Roof Depreciation Calculator",
     "short": "Depreciation (ACV)", "group": "Insurance", "icon": "trend",
     "blurb": "Straight-line depreciation by material and age, with a year-by-year ACV schedule."},
    {"slug": "roof-repair-cost-calculator", "name": "Roof Repair Cost Calculator",
     "short": "Repair Cost", "group": "Cost", "icon": "wrench",
     "blurb": "Build a repair ticket line by line: shingles, flashing, boots, decking, tarps and more."},
    {"slug": "gutter-calculator", "name": "Gutter & Downspout Calculator",
     "short": "Gutters", "group": "Cost", "icon": "drop",
     "blurb": "Size gutters for Texas downpours, count downspouts and price seamless aluminum, steel or copper."},
    {"slug": "attic-ventilation-calculator", "name": "Attic Ventilation Calculator",
     "short": "Attic Ventilation", "group": "Measure", "icon": "wind",
     "blurb": "Net free area for the 1/150 and 1/300 rules, split intake/exhaust and count vents."},
    {"slug": "roofing-bid-calculator", "name": "Roofing Bid & Profit Calculator",
     "short": "Bid & Profit", "group": "Contractor", "icon": "calc",
     "blurb": "Overhead, profit, commission and markup vs. margin to price a roofing job per square."},
]

SERVICES = [
    {"slug": "xactimate-roof-estimates", "name": "Xactimate Roof Estimates",
     "blurb": "Line-item residential roof estimates built from scratch in Xactimate format."},
    {"slug": "commercial-roof-estimates", "name": "Commercial Roof Estimates",
     "blurb": "Low-slope and steep-slope commercial takeoffs, system pricing and scopes."},
    {"slug": "insurance-claim-estimate-review", "name": "Claim Estimate Review",
     "blurb": "We compare the carrier's estimate to the roof and flag what is missing."},
    {"slug": "scope-of-damages", "name": "Scope of Damages",
     "blurb": "Professional scope of damages from your photos, measurements and cause of loss."},
]

NAV = [
    ("Tools", "/tools/"),
    ("Services", "/services/"),
    ("How It Works", "/how-it-works/"),
    ("Areas", "/areas/"),
    ("Blog", "/blog/"),
    ("About", "/about/"),
]

# Texas regions drive the /areas/ page and the regional price factors in the
# cost tools. Factors are relative to the DFW baseline used in the price tables.
TEXAS_REGIONS = [
    {"key": "dfw", "name": "Dallas–Fort Worth", "factor": 1.00,
     "cities": ["Dallas", "Fort Worth", "Arlington", "Plano", "Frisco", "McKinney", "Irving", "Garland",
                "Grand Prairie", "Denton", "Mesquite", "Lewisville", "Carrollton", "Allen", "Rockwall"]},
    {"key": "houston", "name": "Houston & Gulf Coast", "factor": 1.00,
     "cities": ["Houston", "Katy", "Sugar Land", "The Woodlands", "Pearland", "League City", "Pasadena",
                "Baytown", "Galveston", "Beaumont", "Port Arthur", "Corpus Christi", "Victoria", "Friendswood"]},
    {"key": "central", "name": "Austin & Central Texas", "factor": 1.04,
     "cities": ["Austin", "Round Rock", "Georgetown", "Cedar Park", "Pflugerville", "Hutto", "Leander",
                "San Marcos", "Kyle", "Temple", "Killeen", "Belton", "Waco", "Bastrop", "College Station"]},
    {"key": "sa", "name": "San Antonio & Hill Country", "factor": 0.97,
     "cities": ["San Antonio", "New Braunfels", "Schertz", "Boerne", "Seguin", "Helotes", "Fredericksburg",
                "Kerrville", "Universal City", "Converse"]},
    {"key": "south", "name": "Rio Grande Valley & South Texas", "factor": 0.90,
     "cities": ["McAllen", "Edinburg", "Mission", "Pharr", "Harlingen", "Brownsville", "Laredo", "Weslaco"]},
    {"key": "west", "name": "West Texas & Panhandle", "factor": 0.95,
     "cities": ["Lubbock", "Amarillo", "Midland", "Odessa", "Abilene", "San Angelo", "El Paso", "Wichita Falls"]},
    {"key": "east", "name": "East Texas", "factor": 0.94,
     "cities": ["Tyler", "Longview", "Texarkana", "Nacogdoches", "Lufkin", "Marshall", "Huntsville"]},
]

# Outside Texas, same baseline.
US_REGIONS = [
    {"key": "us-south", "name": "Other Southern states (LA, OK, AR, MS, AL, GA, FL, TN)", "factor": 1.02},
    {"key": "us-midwest", "name": "Midwest (KS, MO, NE, CO plains, IA, IL, OH…)", "factor": 1.08},
    {"key": "us-west", "name": "Mountain West & Southwest (NM, AZ, NV, UT, CO)", "factor": 1.10},
    {"key": "us-pacific", "name": "Pacific (CA, OR, WA)", "factor": 1.30},
    {"key": "us-northeast", "name": "Northeast & Mid-Atlantic", "factor": 1.28},
]

# Steep-slope roofing systems used by the cost tools. Prices are DFW-baseline
# 2026 contractor costs per square (100 sq ft) before overhead & profit:
#   mat = roofing product, acc = underlayment/starter/ridge/drip edge/vents,
#   lab = install labor. "life" is the useful life used for depreciation.
# Totals after 20% O&P land inside the published Texas ranges in "range".
MATERIALS = [
    {"key": "arch", "name": "Architectural asphalt shingles", "mat": 140, "acc": 60, "lab": 170, "life": 30,
     "waste": "shingle", "range": [450, 650]},
    {"key": "class4", "name": "Impact-resistant (Class 4) shingles", "mat": 200, "acc": 60, "lab": 180, "life": 30,
     "waste": "shingle", "range": [550, 800]},
    {"key": "3tab", "name": "3-tab asphalt shingles", "mat": 105, "acc": 60, "lab": 150, "life": 20,
     "waste": "shingle", "range": [380, 520]},
    {"key": "designer", "name": "Designer / luxury shingles", "mat": 260, "acc": 65, "lab": 200, "life": 35,
     "waste": "shingle", "range": [650, 900]},
    {"key": "ss", "name": "Standing seam metal", "mat": 560, "acc": 70, "lab": 420, "life": 50,
     "waste": "metal", "range": [1100, 1700]},
    {"key": "rpanel", "name": "Exposed-fastener metal (R-panel / 5V)", "mat": 260, "acc": 50, "lab": 210, "life": 40,
     "waste": "metal", "range": [650, 950]},
    {"key": "stone", "name": "Stone-coated steel", "mat": 470, "acc": 70, "lab": 330, "life": 50,
     "waste": "metal", "range": [950, 1450]},
    {"key": "ctile", "name": "Concrete tile", "mat": 330, "acc": 90, "lab": 400, "life": 50,
     "waste": "tile", "range": [950, 1450]},
    {"key": "clay", "name": "Clay tile", "mat": 650, "acc": 100, "lab": 480, "life": 60,
     "waste": "tile", "range": [1300, 2000]},
    {"key": "shake", "name": "Wood shake", "mat": 420, "acc": 60, "lab": 330, "life": 30,
     "waste": "shingle", "range": [900, 1300]},
]

# Waste factor (%) by material family and roof complexity.
WASTE = {
    "shingle": {"simple": 10, "moderate": 14, "complex": 18},
    "metal": {"simple": 5, "moderate": 8, "complex": 12},
    "tile": {"simple": 10, "moderate": 13, "complex": 17},
}
