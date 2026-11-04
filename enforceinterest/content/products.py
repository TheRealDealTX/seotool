"""Amazon affiliate product recommendations (Associates tag: enforceinterest-20).

Links are Amazon *search* URLs for a specific product type rather than single-ASIN links, so they never
go dead when a listing changes and never point at an unverified item. Every link carries the tag and
rel="sponsored nofollow noopener". Prices aren't shown (Amazon's rules forbid unverified prices).
"""
from urllib.parse import quote_plus
from lib import icon, esc

TAG = "enforceinterest-20"
DISCLOSURE = ("As an Amazon Associate, Enforce Interest earns from qualifying purchases. Recommendations are product "
              "types we find useful for documenting claims; we don&rsquo;t accept payment from manufacturers.")


def amazon_url(query):
    return f"https://www.amazon.com/s?k={quote_plus(query)}&tag={TAG}"


# key: (name, category, icon, why it helps a claim, Amazon search query)
P = {
    "moisture-pin": ("Pin-type moisture meter", "Water damage", "drop",
                     "Readings in drywall, baseboards and subfloor give dated, numeric proof of how far water travelled.",
                     "pin moisture meter drywall wood"),
    "moisture-pinless": ("Pinless moisture meter", "Water damage", "drop",
                         "Scans walls and floors without holes, so you can map wet areas before the adjuster arrives.",
                         "pinless moisture meter"),
    "thermal": ("Smartphone thermal camera", "Inspection", "search",
                "Shows hidden moisture behind walls and missing insulation; thermal images are persuasive claim photos.",
                "thermal imaging camera for smartphone"),
    "hygrometer": ("Digital hygrometer (3-pack)", "Water damage", "drop",
                   "Logs indoor humidity during drying, supporting mitigation and mold-prevention scope.",
                   "digital hygrometer indoor thermometer humidity"),
    "leak-alarm": ("Wi-Fi water leak sensors", "Prevention", "drop",
                   "Alerts your phone the moment a supply line or water heater leaks, and timestamps when the loss began.",
                   "wifi water leak detector sensor"),
    "shutoff": ("Automatic water shut-off valve", "Prevention", "shield",
                "Stops a burst pipe in seconds. Some insurers offer a premium discount for one.",
                "automatic water shut off valve leak detection"),
    "pipe-insulation": ("Foam pipe insulation", "Freeze", "snow",
                        "Cheap protection for exposed pipes, and evidence you used reasonable care against freezing.",
                        "foam pipe insulation tubes"),
    "faucet-cover": ("Outdoor faucet covers", "Freeze", "snow",
                     "Insulates hose bibs, one of the most common freeze-burst points in Texas homes.",
                     "outdoor faucet cover winter insulated"),
    "heat-cable": ("Self-regulating pipe heat cable", "Freeze", "snow",
                   "Keeps vulnerable pipes above freezing during a hard freeze or power-restored cold snap.",
                   "self regulating pipe heat cable"),
    "tarp": ("Heavy-duty waterproof tarp", "Storm", "wind",
             "Temporary roof protection after hail or wind; policies require reasonable steps to prevent further damage.",
             "heavy duty waterproof tarp 20x30"),
    "sandbags": ("Reusable water-activated sandbags", "Storm", "hurricane",
                 "Quick flood barriers for doors and garages before a Gulf storm.",
                 "water activated flood bags"),
    "dehumidifier": ("Large-capacity dehumidifier", "Water damage", "drop",
                     "Speeds drying after a leak and helps prevent the mold that can complicate a water claim.",
                     "dehumidifier 50 pint large room"),
    "shopvac": ("Wet/dry shop vacuum", "Water damage", "drop",
                "First-response water extraction while you wait for a mitigation company.",
                "wet dry shop vacuum"),
    "air-purifier": ("HEPA air purifier", "Fire & smoke", "smoke",
                     "Reduces airborne soot and odor after a fire or wildfire smoke while the claim is resolved.",
                     "hepa air purifier large room smoke"),
    "smoke-co": ("Combination smoke & CO alarms", "Fire & smoke", "flame",
                 "Required safety gear and the first thing to replace after a fire claim.",
                 "combination smoke carbon monoxide detector"),
    "extinguisher": ("Home fire extinguisher (ABC)", "Fire & smoke", "flame",
                     "Stops a small kitchen fire from becoming a total loss.",
                     "home fire extinguisher abc rechargeable"),
    "doc-bag": ("Fireproof & waterproof document bag", "Documentation", "doc",
                "Keeps your policy, declarations page, receipts and a home inventory safe through fire and flood.",
                "fireproof waterproof document bag"),
    "safe": ("Fireproof document safe", "Documentation", "shield",
             "A stronger home for originals: deeds, policy documents, appraisal awards and payment records.",
             "fireproof waterproof document safe"),
    "scanner": ("Portable document scanner", "Documentation", "doc",
                "Turns every claim letter, check stub and receipt into a dated PDF you can send and search.",
                "portable document scanner"),
    "file-box": ("Expanding accordion file organizer", "Documentation", "list",
                 "One labeled pocket per claim stage: notice, requests, responses, estimates, payments, appraisal.",
                 "expanding file folder accordion organizer"),
    "laser-measure": ("Laser distance measure", "Inspection", "calc",
                      "Room dimensions in seconds to check the square footage in the adjuster&rsquo;s estimate.",
                      "laser distance measure"),
    "ladder": ("Telescoping extension ladder", "Inspection", "layers",
               "Safe access for photographing roof damage and gutters (when it&rsquo;s safe to climb).",
               "telescoping extension ladder"),
    "camera-stick": ("Phone tripod / extension pole", "Inspection", "search",
                     "Steady, high-angle photos of roofs, ceilings and attics without climbing.",
                     "phone extension pole tripod selfie stick long"),
    "generator": ("Portable power station", "Storm", "hurricane",
                  "Keeps phones charged and documentation flowing during outages after a storm or freeze.",
                  "portable power station"),
}

SETS = {
    "toolkit": list(P),
    "water": ["moisture-pin", "thermal", "dehumidifier", "leak-alarm", "shutoff", "hygrometer"],
    "freeze": ["pipe-insulation", "faucet-cover", "heat-cable", "leak-alarm", "shutoff", "generator"],
    "hail": ["tarp", "camera-stick", "ladder", "laser-measure", "scanner", "file-box"],
    "hurricane": ["tarp", "sandbags", "generator", "doc-bag", "dehumidifier", "moisture-pin"],
    "fire": ["air-purifier", "smoke-co", "extinguisher", "doc-bag", "safe", "scanner"],
    "smoke": ["air-purifier", "smoke-co", "thermal", "doc-bag", "scanner", "extinguisher"],
    "docs": ["scanner", "file-box", "doc-bag", "safe", "laser-measure", "camera-stick"],
}


def card(key):
    name, cat, ico, why, q = P[key]
    return (f'<div class="card product-card"><div class="pc-top"><div class="ico">{icon(ico)}</div><span class="tag">{cat}</span></div>'
            f'<h3>{name}</h3><p>{why}</p>'
            f'<a class="btn btn-ghost btn-sm" href="{amazon_url(q)}" target="_blank" rel="sponsored nofollow noopener">'
            f'View on Amazon<span class="sr-only"> (opens in a new tab)</span></a></div>')


def box(set_name, title="Gear that makes this claim easier to document", lede="", cols=3):
    keys = SETS[set_name]
    l = f'<p class="muted" style="margin-top:-6px">{lede}</p>' if lede else ""
    return (f'<section class="products" aria-label="Recommended products"><h2>{title}</h2>{l}'
            f'<div class="grid g{cols}" style="margin-top:18px">{"".join(card(k) for k in keys)}</div>'
            f'<p class="aff-note">{DISCLOSURE} <a href="/claim-documentation-toolkit/">See the full toolkit</a>.</p></section>')
