"""Site-wide settings for the customsouthernco.com rebuild."""

SITE = {
    "name": "Custom Southern Co.",
    "short": "Custom Southern",
    "domain": "customsouthernco.com",
    "url": "https://customsouthernco.com",
    "email": "info@customsouthernco.com",
    "tagline": "Vintage finds, repurposed decor & Southern home know-how",
    "description": (
        "Custom Southern Co. shares the stories behind vintage finds, easy repurposed "
        "decor projects and old-fashioned Southern home know-how."
    ),
    "author": "The Custom Southern Co. Team",
    "founded": "2019",
}

CATEGORIES = {
    "vintage-finds": {
        "name": "Vintage Finds",
        "blurb": "The history behind the tins, jars, barns and kitchen oddities we love, plus how to date, clean and value them.",
        "image": "flea-market",
    },
    "diy-repurpose": {
        "name": "DIY & Repurpose",
        "blurb": "Weekend projects that turn thrift-store and junk-pile pieces into decor with a story.",
        "image": "old-window",
    },
    "seasonal": {
        "name": "Seasonal Decor",
        "blurb": "Spring cloches, fall pumpkins, Valentine banners and vintage Christmas, made from what you already have.",
        "image": "xmas-ornaments",
    },
    "southern-home": {
        "name": "Southern Home",
        "blurb": "Old-fashioned know-how for the laundry room, the porch and every corner in between.",
        "image": "porch",
    },
}

# Which season a DIY post belongs to (drives the homepage season tabs and project finder).
SEASONS = {
    "how-to-make-a-faux-tinsel-tree": "christmas",
    "diy-spindle-snowman-ornament": "christmas",
    "quick-vintage-door-knob-tree": "christmas",
    "easy-christmas-spindle-ornaments": "christmas",
    "simple-barn-wood-christmas-trees": "christmas",
    "the-christmas-barn-sale-trail": "christmas",
    "easy-pumpkin-funnel-diy": "fall",
    "vintage-jello-mold-pumpkin-diy": "fall",
    "rustic-cloche-diy-for-spring": "spring",
    "upcycled-vintage-cutting-board-for-spring": "spring",
    "succulent-dustpan-decor": "spring",
    "easy-vintage-valentine-banner": "valentine",
    "easy-valentine-book-decor-diy": "valentine",
    "rustic-patriotic-decor-diy": "summer",
    "southern-front-porch-decor-ideas": "summer",
}

TOOLS = [
    {
        "slug": "prince-albert-tin-dater",
        "key": "tin-dater",
        "name": "Prince Albert Tin Dater",
        "short": "Narrow down when your tobacco tin was made from the clues printed on it.",
        "icon": "tin",
        "keyword": "how to date a prince albert tobacco tin",
        "seo_title": "Prince Albert Tin Dater: How Old Is Your Tin?",
        "description": "Free Prince Albert tin dater. Tick the clues on your tobacco tin (tax stamp, ZIP code, barcode, patent date) and get an estimated date range.",
        "related": ["history-of-prince-albert-tins", "vintage-tobacco-tin-values", "how-to-remove-rust-from-vintage-metal"],
    },
    {
        "slug": "ball-jar-age-finder",
        "key": "jar-dater",
        "name": "Ball Jar Age Finder",
        "short": "Match the logo on your Ball jar to its era in a few clicks.",
        "icon": "jar",
        "keyword": "ball jar age",
        "seo_title": "Ball Jar Age Finder: Date Your Ball Mason Jar",
        "description": "Find the age of a Ball mason jar by its logo. Pick the logo style and color that match your jar to get the approximate years it was made.",
        "related": ["how-to-date-ball-mason-jars", "what-vintage-jars-to-look-for", "how-to-clean-old-jars"],
    },
    {
        "slug": "laundry-detergent-calculator",
        "key": "detergent",
        "name": "DIY Laundry Detergent Calculator",
        "short": "Scale the 3-ingredient recipe to your household and see the real cost per load.",
        "icon": "drop",
        "keyword": "diy laundry detergent calculator",
        "seo_title": "DIY Laundry Detergent Calculator: Cost Per Load",
        "description": "Scale the 3-ingredient homemade laundry detergent recipe to your household, see how much to make, and compare the cost per load with store-bought.",
        "related": ["how-to-make-laundry-detergent-with-3-ingredients", "homemade-fabric-softener", "how-to-remove-rust-from-vintage-metal"],
    },
    {
        "slug": "diy-project-finder",
        "key": "project-finder",
        "name": "DIY Project Finder",
        "short": "Pick a season, your time and budget, and we'll match you to a project.",
        "icon": "spark",
        "keyword": "vintage diy project ideas",
        "seo_title": "DIY Project Finder: Vintage Decor Project Ideas",
        "description": "Find your next vintage DIY project. Filter repurposed decor ideas by season, time, budget and skill level and jump straight to the step-by-step guide.",
        "related": ["easy-vintage-cutting-board-decor", "how-to-repurpose-antique-light-globes", "old-window-decoupage-mirror"],
    },
]

NAV = [
    ("Vintage Finds", "/category/vintage-finds/"),
    ("DIY & Repurpose", "/category/diy-repurpose/"),
    ("Seasonal", "/category/seasonal/"),
    ("Southern Home", "/category/southern-home/"),
    ("Blog", "/blog/"),
]

# Accurate alt text for each photo (what the image actually shows).
IMAGE_ALT = {'about': 'Weathered hands measuring a turned wooden piece with calipers at a workbench',
 'albert-tin': 'Vintage lithographed pocket tobacco tin with a hinged lid',
 'antiques-shop': 'Crowded antique shop with old clocks, lamps and framed pictures',
 'barn-winter': 'Red barn standing in a snowy field below the mountains',
 'barnwood': 'Close-up of weathered gray-brown barn wood planks',
 'barnwood-tree': 'Rustic barn wood boards decorated with evergreen garland, pinecones and wooden stars',
 'bread': 'Rustic round loaf of bread with rosemary on blue linen',
 'chalk-paint': 'Shop filled with painted vintage furniture in soft chalky colors',
 'cloche': 'Glass cloche dome on pink linen',
 'cutting-board': 'Well-worn wooden cutting board with a kitchen knife',
 'doorknobs': 'Antique painted porcelain doorknob and keyhole on an old wooden door',
 'estate-sale': 'Stack of vintage suitcases beside old furniture at an estate sale',
 'flag': 'American flag hanging on a rustic wooden barn wall',
 'flea-market': 'Flea market table covered with vintage glassware, colored bottles and brass pieces',
 'folded-towels': 'Stacks of soft folded towels in neutral and pink tones',
 'hero': 'Old country kitchen with stoneware jugs on shelves, wooden crates and arched windows',
 'jars-shelf': 'Shelves of home-canned lemons and cherries in jars with cloth-topped lids',
 'jello-mold': 'Collection of vintage copper jelly and pudding molds',
 'kitchen-vintage': 'Vintage blue painted kitchen dresser with blue-and-white plates',
 'laundry': 'Shirts drying on a clothesline',
 'light-globe': 'Clear glass pendant light shades glowing above',
 'mason-jars': 'Mason jars filled with dried raspberries and dried orange slices',
 'old-books': 'Row of antique leather-bound books',
 'old-photos': 'Vintage black-and-white snapshots among dried flowers',
 'old-window': 'Weathered wooden shutters and window frames on an old building',
 'pie': 'Golden homemade pie cooling on a wire rack',
 'porch': 'Wooden front porch with a rocking chair and stone pillars',
 'pumpkins': 'Small pumpkins and squash in a rustic basket',
 'red-barn': 'Classic red barn with white trim and a silo under a blue sky',
 'rusty-metal': 'Rusty wrenches, sockets and pliers on corroded metal',
 'sheet-music': 'Old sheet music with dried roses, scissors and twine',
 'snowman': 'Small snowman with twig arms standing in fresh snow',
 'soap-bar': 'Bars of handmade soap on white linen with a bath brush',
 'spice-tins': 'Shelves crowded with vintage kitchen and spice tins',
 'succulents': 'Two succulents in white ceramic pots on a wooden table',
 'tiered-tray': 'Styled vignette with a layered cake on a vintage mint-green cake stand',
 'tinsel-tree': 'Silver vintage-style tinsel with a small red lantern ornament',
 'tobacco-tins': 'Glass-front cabinet filled with assorted vintage tins',
 'valentine': 'Wooden letter tiles spelling LOVE with a red heart on a wood slice',
 'xmas-ornaments': 'Shiny glass Christmas ornaments in a basket',
 'yardstick': 'Old wooden yardstick with antique scissors and a sewing pattern'}
