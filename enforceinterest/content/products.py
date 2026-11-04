"""Amazon affiliate product recommendations (Associates tag: enforceinterest-20).

Each entry links to one specific Amazon listing (https://www.amazon.com/dp/<ASIN>?tag=...), chosen from
established brands with strong review histories. ASINs were confirmed against amazon.com listing URLs
returned by web search on 2026-11-04 (Amazon blocks automated page checks, so live stock and price were
not verified). Links carry rel="sponsored nofollow noopener". Prices aren't shown, per Amazon's rules.
Recheck the list periodically: a discontinued listing shows "Currently unavailable" on Amazon.
"""
from lib import icon, esc

TAG = "enforceinterest-20"
DISCLOSURE = ("As an Amazon Associate, Enforce Interest earns from qualifying purchases. We pick these products for "
              "what they add to a claim file; manufacturers don&rsquo;t pay for placement.")


def amazon_url(asin):
    return f"https://www.amazon.com/dp/{asin}?tag={TAG}"


# key: (product name, category, icon, why it helps a claim, ASIN)
P = {
    "moisture-pin": ("General Tools MMD4E pin moisture meter", "Water damage", "drop",
                     "Readings in drywall, baseboards and wood give dated, numeric proof of how far water travelled.",
                     "B00275F5O2"),
    "moisture-pinless": ("General Tools MMH800 pin/pinless moisture meter", "Water damage", "drop",
                         "Scans walls and floors without holes and also logs temperature and humidity.",
                         "B00563TQFG"),
    "thermal": ("FLIR ONE Edge Pro thermal camera", "Inspection", "search",
                "Wireless thermal camera for iPhone or Android; shows hidden moisture behind walls in persuasive images.",
                "B0BLJD6Q5G"),
    "hygrometer": ("ThermoPro TP50 digital hygrometer", "Water damage", "drop",
                   "Tracks indoor humidity during drying, supporting mitigation and mold-prevention scope.",
                   "B01H1R0K68"),
    "leak-alarm": ("Govee Wi-Fi water leak sensors (2-pack)", "Prevention", "drop",
                   "Alerts your phone when a supply line or water heater leaks, and timestamps when the loss began.",
                   "B095STF6FG"),
    "shutoff": ("Moen Flo smart water shutoff (3/4-inch)", "Prevention", "shield",
                "Monitors flow and shuts the water off automatically. Some insurers offer a premium discount for one.",
                "B07QC93TRB"),
    "pipe-insulation": ("Frost King pre-slit foam pipe insulation", "Freeze", "snow",
                        "Cheap protection for exposed pipes, and evidence you used reasonable care against freezing.",
                        "B000BQLSBI"),
    "faucet-cover": ("Frost King FC1 outdoor faucet covers (2-pack)", "Freeze", "snow",
                     "Insulates hose bibs, one of the most common freeze-burst points in Texas homes.",
                     "B01251Q67W"),
    "heat-cable": ("Frost King HC6A pipe heat cable (6 ft)", "Freeze", "snow",
                   "Thermostat-controlled cable that keeps vulnerable pipes from freezing during a hard freeze.",
                   "B000IKOU9O"),
    "tarp": ("Grizzly Tarps by B-Air 20&times;30 heavy-duty tarp", "Storm", "wind",
             "Temporary roof protection after hail or wind; policies require reasonable steps to prevent further damage.",
             "B01M0AILNR"),
    "sandbags": ("Quick Dam water-activated flood bags (6-pack)", "Storm", "hurricane",
                 "Sandless flood barriers for doors and garages before a Gulf storm.",
                 "B0085S0612"),
    "dehumidifier": ("Frigidaire 50-pint dehumidifier", "Water damage", "drop",
                     "Speeds drying after a leak and helps prevent the mold that can complicate a water claim.",
                     "B0DG19KP9V"),
    "shopvac": ("CRAFTSMAN 5-gallon wet/dry shop vac", "Water damage", "drop",
                "First-response water extraction while you wait for a mitigation company.",
                "B07MPJQFX8"),
    "air-purifier": ("LEVOIT Core 400S HEPA air purifier", "Fire &amp; smoke", "smoke",
                     "Reduces airborne soot and odor after a fire or wildfire smoke while the claim is resolved.",
                     "B08R794ZMX"),
    "smoke-co": ("First Alert SCO7CN smoke &amp; CO alarm", "Fire &amp; smoke", "flame",
                 "Combination alarm with voice and room location; the first thing to replace after a fire claim.",
                 "B0002CWXZG"),
    "extinguisher": ("Amerex B402 5-lb ABC fire extinguisher", "Fire &amp; smoke", "flame",
                     "Rechargeable, UL-rated extinguisher that stops a small kitchen fire from becoming a total loss.",
                     "B00F5CK9X6"),
    "doc-bag": ("ENGPOW fireproof document bag", "Documentation", "doc",
                "Keeps your policy, declarations page, receipts and home inventory together and protected.",
                "B09V15P69K"),
    "safe": ("SentrySafe SFW082CTB fireproof &amp; waterproof safe", "Documentation", "shield",
             "A stronger home for originals: deeds, policy documents, appraisal awards and payment records.",
             "B015P0X7AO"),
    "scanner": ("Epson WorkForce ES-50 portable scanner", "Documentation", "doc",
                "Turns every claim letter, check stub and receipt into a dated PDF you can send and search.",
                "B07KQZWPYN"),
    "file-box": ("Smead 12-pocket expanding file", "Documentation", "list",
                 "One labeled pocket per claim stage: notice, requests, responses, estimates, payments, appraisal.",
                 "B0002LCUZK"),
    "laser-measure": ("Bosch GLM 50 C laser measure", "Inspection", "calc",
                      "Room dimensions in seconds to check the square footage in the adjuster&rsquo;s estimate.",
                      "B015FCJTEA"),
    "ladder": ("Little Giant Velocity multi-position ladder", "Inspection", "layers",
               "Safe access for photographing gutters and roof edges (when it&rsquo;s safe to climb).",
               "B00E1AQE46"),
    "generator": ("Jackery Explorer 300 portable power station", "Storm", "hurricane",
                  "Keeps phones and laptops charged so you can document and report during outages.",
                  "B082TMBYR6"),
}

SETS = {
    "toolkit": list(P),
    "water": ["moisture-pin", "thermal", "dehumidifier", "leak-alarm", "shutoff", "hygrometer"],
    "freeze": ["pipe-insulation", "faucet-cover", "heat-cable", "leak-alarm", "shutoff", "generator"],
    "hail": ["tarp", "ladder", "laser-measure", "thermal", "scanner", "file-box"],
    "hurricane": ["tarp", "sandbags", "generator", "doc-bag", "dehumidifier", "moisture-pin"],
    "fire": ["air-purifier", "smoke-co", "extinguisher", "doc-bag", "safe", "scanner"],
    "smoke": ["air-purifier", "smoke-co", "thermal", "doc-bag", "scanner", "extinguisher"],
    "docs": ["scanner", "file-box", "doc-bag", "safe", "laser-measure", "moisture-pin"],
}


def card(key):
    name, cat, ico, why, asin = P[key]
    return (f'<div class="card product-card"><div class="pc-top"><div class="ico">{icon(ico)}</div><span class="tag">{cat}</span></div>'
            f'<h3>{name}</h3><p>{why}</p>'
            f'<a class="btn btn-ghost btn-sm" href="{amazon_url(asin)}" target="_blank" rel="sponsored nofollow noopener">'
            f'View on Amazon<span class="sr-only"> (opens in a new tab)</span></a></div>')


def box(set_name, title="Gear that makes this claim easier to document", lede="", cols=3):
    keys = SETS[set_name]
    l = f'<p class="muted" style="margin-top:-6px">{lede}</p>' if lede else ""
    return (f'<section class="products" aria-label="Recommended products"><h2>{title}</h2>{l}'
            f'<div class="grid g{cols}" style="margin-top:18px">{"".join(card(k) for k in keys)}</div>'
            f'<p class="aff-note">{DISCLOSURE} <a href="/claim-documentation-toolkit/">See the full toolkit</a>.</p></section>')
