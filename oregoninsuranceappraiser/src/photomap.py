"""Which photo (key in photos.json) appears on which page."""

SVC_PHOTO = {
    "appraisal-clause-help": "meeting", "home-insurance-appraisal": "house-dusk", "commercial-hoa-appraisal": "commercial-glass",
    "roof-hail-appraisal": "roof-damage", "windstorm-tornado-appraisal": "coast-waves", "ice-storm-snow-appraisal": "ice-storm",
    "water-damage-appraisal": "rain-window", "house-fire-smoke-appraisal": "house-fire", "wildfire-loss-appraisal": "wildfire-aftermath",
    "fallen-tree-appraisal": "tree-roof", "carrier-estimate-review": "plans-clipboard", "neutral-umpire-services": "builder-house",
}
LOC_PHOTO = {
    "portland": "portland-downtown", "beaverton": "house-dusk", "hillsboro": "barn-valley", "lake-oswego": "hood-lake",
    "salem": "salem-capitol", "eugene": "siuslaw-winter", "corvallis": "calapooia-winter", "bend": "bend-drake-park",
    "medford": "wildfire-street", "grants-pass": "wildfire-crew", "newport": "cannon-beach", "pendleton": "storm-hills",
}
TOOL_PHOTO = {
    "appraisal-payoff-estimator": "calculator", "depreciation-holdback-tracker": "kitchen", "roof-pitch-squares-converter": "roof-shingles",
    "percentage-deductible-checker": "lightning", "claim-calendar-builder": "plans-clipboard", "appraisal-readiness-checkup": "meeting",
    "wildfire-contents-estimator": "living-room",
}
POST_PHOTO = {
    "oregon-appraisal-clause-basics": "meeting", "documenting-a-wildfire-total-loss": "wildfire-aftermath",
    "after-an-ice-storm-claim-checklist": "ice-limbs", "earthquake-coverage-and-appraisal": "apartments",
    "reading-an-insurance-estimate": "calculator", "appraisal-dfr-complaint-or-attorney": "salem-capitol",
}
# Order matches build.REGIONS: Portland Metro, Willamette Valley, Coast, Southern, Central, Eastern.
REGION_PHOTO = ["hero-home", "calapooia-winter", "coast-waves", "wildfire-forest", "crooked-river", "storm-hills"]
PAGE_PHOTO = {
    "services": "builder-house", "locations": "hood-lake", "tools": "calculator", "process": "plans-clipboard",
    "faq": "living-room", "glossary": "roof-shingles", "posts": "snow-cabin", "about": "cannon-beach", "about-inline": "meeting",
    "contact": "house-dusk", "legal": "storm-clouds", "404": "smoke-landscape",
}
