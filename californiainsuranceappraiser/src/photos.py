"""Photo manifest (internal record of source + license in photos.json), alt text and page mappings.
All photos are CC0 or public domain (no attribution required). Sources are recorded for our own records only."""
import json
import os

PHOTOS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos.json"), encoding="utf-8"))

ALT = {
    "hero-home": "Pale green bungalow with a white picket fence on a sunny residential street",
    "wildfire-ruins": "Ash and debris where a home stood after a wildfire, with a bare chimney and scorched trees",
    "wildfire-hills": "Wildfire burning along mountain ridges above the lights of a town at night",
    "smoke-home": "Two-story home in front of a hillside of trees burned by a wildfire",
    "foothill-home": "Rural foothill home and outbuildings below a slope burned by wildfire",
    "smoke-plume": "Large wildfire smoke plume rising beyond homes and open fields",
    "tarp-roof": "Worker securing a blue tarp over a damaged roof near the ocean",
    "roof-tile": "Close-up of clay barrel tile roof with a broken tile",
    "roof-aerial": "Aerial view of a single-story house with a composition shingle roof",
    "roof-crew": "Roofers on ladders repairing storm damage beside a broken palm",
    "palms-wind": "Palm trees bending in strong wind against a pale sky",
    "storm-clouds": "Dark storm clouds and rain shafts over a mountain range at sunset",
    "fallen-tree": "Large old trees toppled near a single-story house after a storm",
    "water-ceiling": "Bedroom with a collapsed, water-damaged ceiling",
    "quake-chimney": "Collapsed brick chimney in a pile of rubble beside a house after an earthquake",
    "la-skyline": "Aerial view of downtown Los Angeles and the surrounding basin",
    "sd-skyline": "San Diego skyline and bay with sailboats and mountains behind",
    "sf-victorians": "Row of Victorian houses on a steep San Francisco street",
    "sacramento-capitol": "Dome of the California State Capitol in Sacramento",
    "san-jose-house": "Historic two-story Thomas Fallon House in downtown San Jose",
    "oakland-view": "View across Oakland neighborhoods from a hilltop with an oak tree",
    "fresno-building": "Art deco civic building on Tulare Avenue in Fresno",
    "riverside-inn": "Arched balconies of the rotunda at the Mission Inn in Riverside",
    "chico-building": "Historic United States Post Office building in downtown Chico",
    "burned-trees": "Fire-killed pines beside green trees and a truck after a foothill wildfire",
    "consult": "Appraiser reviewing notes on a clipboard at a desk with a laptop",
    "clipboard-site": "Professional working through a claim file on a laptop",
    "paper-writing": "Person writing notes on paperwork at a desk",
    "contractor": "Two inspectors in hard hats reviewing plans on a job site",
    "calculator": "Calculator, pencil and sticky notes on a desk",
    "calc-paper": "Scientific calculator resting on printed figures",
    "clipboard": "Signed document on a clipboard beside a pen and camera",
    "kitchen": "Modern kitchen with wood floors and light cabinets",
    "living-room": "Bright living room with a gray sofa and large windows",
    "office": "Glass office building against a blue sky",
    "condo": "Multistory condominium building with balconies and trees",
    "demolition": "Excavator demolishing a damaged wood-frame house",
    "hillside-homes": "Hillside neighborhoods and green slopes in Los Angeles",
}

SVC_PHOTO = {
    "policyholder-appraiser-representation": "consult", "home-claim-appraisal": "hillside-homes",
    "commercial-hoa-claim-appraisal": "office", "roof-damage-appraisal": "roof-tile",
    "santa-ana-wind-damage-appraisal": "palms-wind", "atmospheric-river-storm-claim-appraisal": "fallen-tree",
    "water-leak-claim-appraisal": "water-ceiling", "smoke-ash-fire-claim-appraisal": "smoke-home",
    "wildfire-total-loss-appraisal": "wildfire-ruins", "contents-inventory-appraisal": "living-room",
    "carrier-estimate-review": "calc-paper", "umpire-appointment-services": "clipboard",
}
LOC_PHOTO = {
    "los-angeles": "la-skyline", "san-diego": "sd-skyline", "san-jose": "san-jose-house", "san-francisco": "sf-victorians",
    "sacramento": "sacramento-capitol", "fresno": "fresno-building", "santa-rosa": "burned-trees", "oakland": "oakland-view",
    "riverside": "riverside-inn", "irvine": "condo", "ventura": "wildfire-hills", "chico": "chico-building",
}
TOOL_PHOTO = {
    "appraisal-payoff-estimator": "calculator", "acv-holdback-calculator": "calc-paper",
    "roof-area-pitch-calculator": "roof-aerial", "earthquake-deductible-calculator": "quake-chimney",
    "claim-timeline-builder": "tarp-roof", "appraisal-readiness-check": "contractor",
    "rebuild-cost-underinsurance-check": "demolition",
}
POST_PHOTO = {
    "california-appraisal-clause-section-2071": "clipboard-site", "wildfire-total-loss-claim-order-of-operations": "smoke-plume",
    "smoke-ash-claims-when-the-house-survived": "burned-trees", "fair-plan-claims-and-appraisal": "foothill-home",
    "earthquake-versus-fire-following": "quake-chimney", "reading-a-carrier-estimate": "paper-writing",
}
