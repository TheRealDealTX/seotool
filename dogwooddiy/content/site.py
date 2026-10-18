"""Site-wide settings, categories and navigation for dogwooddiy.com."""

SITE = {
    "name": "Dogwood DIY",
    "origin": "https://dogwooddiy.com",
    "email": "info@dogwooddiy.com",
    "ga4": "G-37L4LEFEJ0",
    "authors": ["Stephanie Tilton", "Jared Tilton"],
    "tagline": "Home renovation, decor and garden DIY on a real-life budget.",
    "home_title": "Dogwood DIY | Home Renovation, Decor & Garden Projects",
    "home_desc": "Follow Jared and Stephanie as they turn a 1960s brick ranch into a modern farmhouse. DIY guides for German schmear, shrubs, bathrooms and gardens.",
    "featured": "german-schmear-fireplace",
    "popular": ["german-schmear-fireplace", "remove-overgrown-shrubs-easy", "replace-old-caulk-bathtub",
                "painted-grout-bathroom", "simple-wallpaper-removal"],
}

CATS = {
    "home-renovation": {
        "name": "Home Renovation",
        "img": "german-schmear-fireplace",
        "blurb": "Fireplaces, bathrooms, walls and the bones of a 1960s ranch.",
        "title": "Home Renovation DIY Projects & Tutorials | Dogwood DIY",
        "h1": "Home renovation projects",
        "desc": "Budget home renovation tutorials: German schmear brick, re-caulking tubs, painted grout, wallpaper removal, painted cabinets and ranch upgrades.",
        "intro": "The hands-dirty side of the Dogwood House: brick, mortar, caulk, grout, drywall and paint. Every guide includes what we spent and what we'd do differently.",
    },
    "decor-design": {
        "name": "Decor & Design",
        "img": "farmhouse-living-room",
        "blurb": "Farmhouse style, outdoor rooms and wreaths you can make in minutes.",
        "title": "Decor & Design: Farmhouse Style on a Budget | Dogwood DIY",
        "h1": "Decor & design",
        "desc": "Farmhouse decor ideas, DIY wreaths, outdoor living spaces and budget styling tips from Dogwood DIY. Make your home feel finished without a designer budget.",
        "intro": "The fun part after the renovation dust settles - styling rooms, decorating outdoor spaces and making seasonal decor from what's growing in the yard.",
    },
    "garden-outdoor": {
        "name": "Garden & Outdoors",
        "img": "shrub-hedge-path",
        "blurb": "Shrubs, red clay soil, dogwoods and curb appeal.",
        "title": "Garden & Landscaping DIY: Shrubs & Soil | Dogwood DIY",
        "h1": "Garden & outdoor projects",
        "desc": "Beginner gardening and landscaping guides: remove overgrown shrubs, plant in red clay soil, grow dogwoods and pick shrubs for your front yard.",
        "intro": "Our North Carolina yard came with red clay, overgrown shrubs and a lot of potential. Here's everything we've learned getting it into shape.",
    },
}

NAV = [
    ("Home", "/"),
    ("Projects", "/blog/"),
    ("Renovation", "/category/home-renovation/"),
    ("Decor", "/category/decor-design/"),
    ("Garden", "/category/garden-outdoor/"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
]
