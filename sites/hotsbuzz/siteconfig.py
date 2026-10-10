"""Site-wide constants for the hotsbuzz.com rebuild."""

from datetime import date

SITE = {
    "name": "HotsBuzz",
    "domain": "hotsbuzz.com",
    # Canonical origin. Canonicals, sitemap and JSON-LD always point here,
    # even while the build is previewed on a temporary hosting domain.
    "origin": "https://hotsbuzz.com",
    "tagline": "DIY projects, DIY ideas, crafts and more",
    "about": (
        "DIY projects, DIY ideas and crafts are the best way to create unique "
        "masterpieces. That’s why we gather crafts you can make as gifts or as "
        "home decoration, not just for yourself but for your close friends too."
    ),
    "email": "hello@hotsbuzz.com",
    "founded": "2016",
}

# True while the site lives on the temporary Hostinger domain: every page gets
# <meta name="robots" content="noindex"> and robots.txt blocks crawling, so the
# temporary hostname never competes with hotsbuzz.com in search. Flip to False
# (and rebuild + redeploy) the day hotsbuzz.com is connected to the website.
STAGING = True

# slug, name, short label, colors (gradient start, gradient end, accent), blurb
CATEGORIES = [
    {
        "slug": "diy-home-decor", "name": "DIY Home Decor", "short": "Home Decor",
        "c1": "#12b5a0", "c2": "#0a5f69", "accent": "#ffd166", "motif": "frame",
        "blurb": "Budget-friendly makeovers, shelf styling and handmade accents that make a house feel like yours.",
    },
    {
        "slug": "creative-crafts", "name": "Creative Crafts", "short": "Crafts",
        "c1": "#8b5cf6", "c2": "#4c1d95", "accent": "#ffcf5c", "motif": "scissors",
        "blurb": "Paper, paint, wax and flowers: weekend crafts that double as thoughtful handmade gifts.",
    },
    {
        "slug": "christmas-crafts", "name": "Christmas DIY & Crafts", "short": "Christmas",
        "c1": "#e23a4e", "c2": "#14633c", "accent": "#ffe08a", "motif": "tree",
        "blurb": "Wreaths, ornaments and paper stars to make the merriest tree and mantel on the block.",
    },
    {
        "slug": "halloween-crafts", "name": "Halloween Crafts", "short": "Halloween",
        "c1": "#ff7a1a", "c2": "#2b1640", "accent": "#c6ff3d", "motif": "ghost",
        "blurb": "Spooky-cute pumpkins, ghosts and bats you can make in an evening, no carving knife required.",
    },
    {
        "slug": "thanksgiving-crafts", "name": "Thanksgiving Crafts", "short": "Thanksgiving",
        "c1": "#e07a3a", "c2": "#6e3214", "accent": "#ffd38a", "motif": "leaf",
        "blurb": "Gratitude projects, harvest garlands and table decor for a warm, handmade Thanksgiving.",
    },
    {
        "slug": "valentines-crafts", "name": "Valentine’s Crafts", "short": "Valentine’s",
        "c1": "#ff4d8d", "c2": "#a3124a", "accent": "#ffe1ec", "motif": "heart",
        "blurb": "Pop-up cards, heart garlands and jar gifts that say it better than store-bought.",
    },
    {
        "slug": "st-patricks-day-crafts", "name": "St. Patrick’s Day Crafts", "short": "St. Patrick’s",
        "c1": "#2bb75a", "c2": "#0b5a2a", "accent": "#ffd400", "motif": "shamrock",
        "blurb": "Shamrocks, rainbows and pots of gold: lucky little crafts for kids and grown-ups alike.",
    },
]
CAT = {c["slug"]: c for c in CATEGORIES}

HOLIDAYS = ["christmas-crafts", "halloween-crafts", "thanksgiving-crafts",
            "valentines-crafts", "st-patricks-day-crafts"]

TODAY = date.today().isoformat()
