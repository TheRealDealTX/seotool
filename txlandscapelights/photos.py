"""Royalty-free photos (CC0 / public domain / CC BY / CC BY-SA). Credits: content/photos.json, /photo-credits/."""
import html
import json
import zlib
from pathlib import Path

PHOTOS = {c["key"]: c for c in json.loads((Path(__file__).parent / "content" / "photos.json").read_text())}

# Pools of photos per illustration theme; pages pick one deterministically by slug for variety.
THEME = {
    "facade": ["facade-estate", "house-night", "facade-stone"],
    "path": ["path-lights-walkway", "path-stone"],
    "tree": ["tree-uplights", "tree-glow", "tree-canopy"],
    "patio": ["pergola-lights", "pool-string-lights-2", "string-bulbs", "patio-pool-lights"],
    "pool": ["pool-courtyard", "pool-garden-night", "pool-tropical", "resort-pool"],
    "controls": ["smart-app"],
    "repair": ["path-light-closeup", "string-bulbs"],
    "commercial": ["facade-columns", "columns-uplit", "facade-stone"],
    "city": ["house-porch-night", "pool-patio-night", "tree-uplights", "path-lights-walkway"],
}
SERVICE = {
    "architectural-lighting": "facade-estate", "pathway-driveway-lighting": "path-lights-walkway",
    "tree-garden-lighting": "tree-uplights", "patio-pool-lighting": "pool-string-lights-2",
    "smart-lighting-controls": "smart-app", "landscape-lighting-repair": "path-light-closeup",
    "commercial-landscape-lighting": "facade-columns",
}
CITY = {"houston-tx": "houston", "dallas-tx": "dallas", "austin-tx": "austin", "san-antonio-tx": "san-antonio",
        "fort-worth-tx": "fort-worth", "new-braunfels-tx": "new-braunfels"}
POST = {
    "landscape-lighting-cost-texas": "pool-patio-night", "best-landscape-lighting-for-texas-heat": "pool-tropical",
    "landscape-lighting-techniques": "tree-uplights", "warm-white-vs-cool-white-landscape-lighting": "string-bulbs",
    "path-light-spacing": "path-lights-walkway", "tree-uplighting-guide": "tree-glow",
    "landscape-lighting-transformer-sizing": "path-light-closeup", "halogen-to-led-landscape-lighting": "facade-stone",
    "protecting-landscape-lighting-from-texas-storms": "pool-garden-night", "landscape-lighting-for-home-security": "house-night",
    "landscape-lighting-maintenance-checklist": "path-stone", "how-much-electricity-does-landscape-lighting-use": "smart-app",
}
PAGE = {"about-us": "house-night", "our-process": "path-lights-walkway", "faq": "pergola-lights", "inspiration": "pool-string-lights",
        "contact": "house-porch-night", "quote": "pool-courtyard", "services": "facade-estate", "service-areas": "live-oak-house",
        "tools": "smart-app", "blog": "tree-glow"}


def pick(theme, seed):
    pool = THEME.get(theme, THEME["facade"])
    return pool[zlib.crc32(seed.encode()) % len(pool)]


def src(key, small=False):
    return f"/assets/img/photos/{key}{'-640' if small else ''}.webp"


def img(key, cls="", eager=False, sizes="(max-width: 900px) 100vw, 50vw", alt=None):
    p = PHOTOS[key]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img class="{cls}" src="{src(key)}" srcset="{src(key, True)} 640w, {src(key)} {p["w"]}w" sizes="{sizes}" '
            f'width="{p["w"]}" height="{p["h"]}" alt="{html.escape(alt or p["alt"], quote=True)}" {load} decoding="async">')

TOOL = {"lighting-visualizer": "facade-estate", "energy-cost-calculator": "smart-app", "fixture-estimator": "path-lights-walkway",
        "transformer-sizing-calculator": "path-light-closeup", "led-savings-calculator": "facade-stone",
        "color-temperature-guide": "string-bulbs", "sunset-timer-planner": "pool-string-lights"}
