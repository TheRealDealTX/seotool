"""Photo alt text and page-to-photo mapping. Photo metadata (license, source) lives in photos.json."""

PHOTO_ALT = {
    "hero-home": "The Chesapeake Bay Bridge at dusk under a dramatic sky",
    "bay-sunset": "Sunset over the Chesapeake Bay with the Bay Bridge on the horizon",
    "baltimore-skyline": "Baltimore skyline across the water of the Inner Harbor",
    "inner-harbor": "Historic tall ship docked at Baltimore’s Inner Harbor with downtown buildings behind",
    "rowhouses": "Row of brick Baltimore rowhouses with porches and bay windows",
    "rowhouse-street": "Corner of a Baltimore street lined with brick rowhouses",
    "rowhouse-porches": "Long row of porch-front brick rowhouses on a Baltimore avenue",
    "bay-bridge-aerial": "Aerial view of the twin spans of the Chesapeake Bay Bridge",
    "ocean-city": "Oceanfront high-rise hotel on the beach in Ocean City, Maryland",
    "ellicott-main-street": "Main Street in historic Ellicott City on a rainy day",
    "ellicott-stream": "Stream running behind stone buildings in Ellicott City",
    "storm-damaged-house": "Wood-frame house knocked off its foundation by a storm",
    "damaged-home": "Storm-damaged home with collapsed siding and debris",
    "storm-debris-homes": "Neighborhood littered with storm debris and broken trees",
    "tornado-damage": "House beside a road with trees stripped and snapped by a tornado",
    "trees-down": "Large trees uprooted across a lawn near a brick ranch house",
    "slate-roof": "Close-up of weathered multicolored slate roof shingles",
    "shingles": "Rows of dark roof shingles in late-afternoon light",
    "roof-tarp": "Roofers on a lift placing a blue tarp over a damaged brick house roof",
    "icicles-roof": "Icicles hanging from the shingled eave of a cabin roof",
    "icicles-brick": "Icicles and heavy snow along the roof edge of a brick building",
    "snow-chimney": "Snow-covered roof and brick chimney against a blue sky",
    "snowy-house": "Gray house and shrubs blanketed by fresh snow",
    "flooded-house": "Stop sign standing in floodwater in front of a brick house",
    "flooded-dock": "Marina docks and boats with high water during a storm",
    "lightning": "Lightning bolt striking from a dark storm cloud",
    "storm-clouds": "Dark storm clouds gathering over a barn and field",
    "house-fire": "House fully engulfed in flames at night",
    "laptop-calculator": "Person using a calculator beside a laptop spreadsheet",
    "calculator": "Calculator, pencil and sticky notes on a desk",
    "signing": "Hand signing a contract with a pen",
    "consultation": "Two women talking at a round table by an office window",
    "meeting": "Two men reviewing a laptop together in a meeting room",
    "condo-building": "Brick condominium building with balconies beside a pond",
    "highrise": "Multi-story residential high-rise with balconies",
    "foursquare-house": "Two-story yellow frame house with a front porch",
    "suburban-house": "Craftsman-style bungalow with a front porch and steps",
    "notebook-calculator": "Open notebook, pen and calculator on a white table",
    "eave-damage": "Close-up of a damaged roof edge with torn shingles and exposed boards",
    "winter-lake": "Snow and ice along the shore of a forested mountain lake",
}

SVC_PHOTO = {
    "appraisal-demand-representation": "signing",
    "home-insurance-appraisal": "foursquare-house",
    "commercial-hoa-appraisal": "condo-building",
    "roof-hail-damage-appraisal": "shingles",
    "windstorm-tornado-appraisal": "tornado-damage",
    "hurricane-noreaster-appraisal": "flooded-dock",
    "water-damage-appraisal": "flooded-house",
    "fire-smoke-damage-appraisal": "house-fire",
    "snow-ice-dam-freeze-appraisal": "icicles-roof",
    "tree-impact-claim-appraisal": "trees-down",
    "carrier-estimate-review": "laptop-calculator",
    "neutral-umpire-services": "meeting",
}

LOC_PHOTO = {
    "baltimore": "baltimore-skyline", "towson": "rowhouse-porches", "ellicott-city": "ellicott-main-street",
    "annapolis": "bay-sunset", "frederick": "storm-clouds", "rockville": "highrise", "bowie": "suburban-house",
    "waldorf": "storm-debris-homes", "hagerstown": "snowy-house", "cumberland": "winter-lake",
    "salisbury": "flooded-dock", "ocean-city": "ocean-city",
}

TOOL_PHOTO = {
    "claim-gap-fee-estimator": "calculator", "rcv-acv-holdback-worksheet": "notebook-calculator",
    "roof-square-pitch-calculator": "slate-roof", "hurricane-deductible-calculator": "bay-bridge-aerial",
    "claim-timeline-planner": "signing", "appraisal-readiness-checklist": "consultation",
    "snow-load-roof-estimator": "snow-chimney",
}

POST_PHOTO = {
    "maryland-appraisal-clause-guide": "signing", "mia-complaint-or-appraisal": "consultation",
    "baltimore-rowhouse-roof-claims": "rowhouses", "bay-hurricane-deductibles": "bay-bridge-aerial",
    "western-maryland-ice-dam-claims": "icicles-brick", "choosing-an-independent-appraiser": "meeting",
}

PAGE_PHOTO = {
    "services": "roof-tarp", "locations": "inner-harbor", "tools": "laptop-calculator", "process": "notebook-calculator",
    "faq": "rowhouse-street", "glossary": "calculator", "kb": "eave-damage", "about": "consultation",
    "contact": "suburban-house", "legal": "baltimore-skyline", "404": "flooded-house",
}

# (name, subtitle, text, communities, photo) — used on the homepage and the locations index.
REGIONS = [
    ("Western Maryland", "Garrett · Allegany · Washington",
     "Mountain snow, ice dams and frozen pipes in seasonal cabins; hail rolling off the ridges into the Hagerstown Valley; river flooding along the Potomac and its creeks.",
     "Oakland, Deep Creek Lake, Frostburg, Cumberland, Hancock, Hagerstown", "winter-lake"),
    ("Central Maryland", "Baltimore City · Baltimore Co. · Howard · Anne Arundel · Harford · Carroll",
     "Brick rowhouses with low-slope roofs and shared party walls, flash floods in stream valleys like Ellicott City’s, derecho-felled oaks and spring hail in the northern suburbs.",
     "Baltimore, Towson, Catonsville, Ellicott City, Columbia, Annapolis, Bel Air, Westminster", "rowhouses"),
    ("Capital Region", "Montgomery · Prince George’s · Frederick",
     "High-rise condos and HOA communities, 1950s–60s ramblers, big tree canopies that come down in derechos, and hail in the Frederick Valley.",
     "Rockville, Silver Spring, Gaithersburg, Bowie, Laurel, Frederick, Urbana", "highrise"),
    ("Southern Maryland", "Charles · Calvert · St. Mary’s",
     "Tornado history around La Plata, tropical-storm wind and tidal flooding on the Patuxent and Potomac shores, and fast-growing subdivisions around Waldorf.",
     "Waldorf, La Plata, Prince Frederick, Solomons, Lexington Park, Leonardtown", "storm-debris-homes"),
    ("Eastern Shore", "Nine counties from Cecil to Worcester",
     "Hurricane and named-storm deductibles, wind-driven rain, low-lying farmland and waterfront towns, and salt-air wear on Ocean City’s condo towers.",
     "Elkton, Chestertown, Easton, Cambridge, Salisbury, Crisfield, Berlin, Ocean City", "ocean-city"),
]
