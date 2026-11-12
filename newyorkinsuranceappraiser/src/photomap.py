"""Which photo each page uses, and alt text for every photo (keys match src/photos.json)."""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
ALT = {k: v["alt"] for k, v in json.load(open(os.path.join(_HERE, "photos.json"))).items()}

SVC_PHOTO = {
    "appraisal-panel-representation": "consult", "homeowners-insurance-appraisal": "who-home",
    "co-op-condo-commercial-appraisal": "apartment", "roof-hail-damage-appraisal": "hail",
    "windstorm-tornado-appraisal": "fallen-tree", "hurricane-noreaster-appraisal": "waves",
    "burst-pipe-water-damage-appraisal": "water-ceiling", "fire-smoke-damage-appraisal": "house-fire",
    "snow-load-ice-dam-appraisal": "icicles", "carrier-estimate-review": "laptop",
    "appraisal-umpire-services": "consult2",
}
LOC_PHOTO = {
    "manhattan": "manhattan", "brooklyn": "brooklyn", "queens": "queens", "staten-island": "staten-island",
    "hempstead": "long-island", "islip": "south-shore", "white-plains": "westchester", "albany": "albany",
    "syracuse": "syracuse", "rochester": "rochester", "buffalo": "buffalo", "binghamton": "binghamton",
}
TOOL_PHOTO = {
    "settlement-gap-fee-estimator": "calculator", "acv-rcv-holdback-calculator": "clipboard",
    "roof-area-pitch-estimator": "roof-shingles", "hurricane-deductible-calculator": "storm",
    "claim-calendar-builder": "laptop", "appraisal-readiness-checkup": "tarp",
    "co-op-condo-claim-splitter": "apartment",
}
POST_PHOTO = {
    "new-york-standard-fire-policy-appraisal-clause": "clipboard", "hurricane-deductibles-long-island-nyc": "noreaster",
    "ice-dam-roof-leak-claims": "snow-roof", "co-op-condo-master-policy-vs-ho6": "commercial",
    "basement-water-sewer-backup-vs-flood": "water-ceiling", "appraiser-public-adjuster-or-attorney-new-york": "consult",
}
