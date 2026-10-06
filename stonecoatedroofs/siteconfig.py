"""Business facts, navigation and keyword overrides for stonecoatedroofs.com."""

from datetime import date

BIZ = {
    "name": "Stone Coated Roofs",
    "tagline": "Texas's specialist installer of stone coated steel roofing",
    "phone_display": "+1 (512) 297-7580",
    "phone_short": "(512) 297-7580",
    "phone_href": "+15122977580",
    "origin": "https://stonecoatedroofs.com",
    "state": "Texas",
}

TODAY = date.today().isoformat()

NAV = [
    ("Why Replace", "/why-replace/", None),
    ("Service Area", "/service-area/", None),
    ("Brands", "/topic/roof-brands/", None),
    ("Styles", "/topic/roof-styles/", None),
    ("Commercial", "/commercial/", None),
    ("Compare", "/topic/compare/", None),
    ("Tools", "/tools/", None),
    ("Blog", "/blog/", None),
]

# Featured on the homepage and footer, in this order (slug prefix of /service-area/<x>-stone-coated-roofs/)
FEATURED_CITIES = ["houston", "dallas", "austin", "san-antonio", "fort-worth", "el-paso",
                   "arlington", "corpus-christi", "plano", "lubbock", "belton", "lufkin"]

# Region grouping for the service-area hub
REGIONS = {
    "Dallas–Fort Worth": ["dallas", "fort-worth", "arlington", "plano", "frisco", "mckinney", "prosper",
                          "denton", "lewisville", "coppell", "irving", "grand-prairie", "mesquite",
                          "grapevine", "southlake", "colleyville", "keller", "westlake"],
    "Houston & Gulf Coast": ["houston", "corpus-christi"],
    "Central Texas": ["austin", "san-antonio", "belton"],
    "West Texas & Panhandle": ["el-paso", "lubbock"],
    "East Texas": ["lufkin"],
}

BRANDS = [
    # name, blurb, warranty, price tier, href
    ("Decra", "The original stone coated steel, since 1957.", "50-yr warranty", "$$$", "/decra-stone-coated-metal-roofing-review/"),
    ("Roser", "Spanish-engineered profiles with Mediterranean character.", "Lifetime warranty", "$$$", "/roser-stone-coated-roof/"),
    ("TEK", "HURRICANE® Metal Shake — CAT5 wind tested, foam-insulated.", "50-yr warranty", "$$$$", "/tek-stone-coated-steel-roof/"),
    ("Tilcor", "New Zealand engineering, hurricane-rated to 175 mph.", "50-yr warranty", "$$$$", "/tilcor-stone-coated-steel-roof/"),
    ("Boral", "Now Westlake Royal — broad profile range, Class 4 hail.", "50-yr warranty", "$$$", None),
    ("Gerard", "Heritage steel tile with the deepest stone coating on market.", "50-yr warranty", "$$$", None),
    ("Metro", "Wide profile selection and the most installer-friendly system.", "Lifetime warranty", "$$$", None),
    ("Allmet", "Value-tier stone coated with full UL certification.", "50-yr warranty", "$$", None),
    ("Unified", "Unified Steel — Westlake Royal's stone coated line with a wide profile range.", "50-yr warranty", "$$$", None),
]

# Search-console driven overrides: path -> dict(title=, description=, h1=)
# Titles are <= 60 chars before the " | Stone Coated Roofs" suffix is considered.
SEO = {
    "/stone-coated-steel-roof-problems/": dict(
        title="Stone Coated Steel Roofing Problems: Causes & Fixes",
        h1="Stone Coated Steel Roofing Problems: Common Issues, Causes, and How to Avoid Them",
        description="Stone coated steel roofing problems explained: leaks at flashings, noise, granule loss, rust and install errors — what causes each and how Texas owners avoid them."),
    "/the-biggest-problems-with-stone-coated-steel-roofs/": dict(
        title="Disadvantages of Stone Coated Metal Roofs (Honest List)",
        h1="The Biggest Problems With Stone Coated Steel Roofs (and the Disadvantages to Weigh)",
        description="The real disadvantages of stone coated metal roofing — upfront cost, installer skill, walkability, granule shedding — and which problems are myths."),
    "/pros-and-cons-of-stone-coated-steel-roofing/": dict(
        title="Stone Coated Steel Roofing Pros and Cons",
        description="Stone coated steel roofing pros and cons for Texas homes: hail and wind ratings, lifespan, weight, noise, cost and insurance — weighed honestly before you buy."),
    "/stone-coated-roofing-cost-texas/": dict(
        title="Stone Coated Steel Roofing Cost in Texas (2026 Prices)",
        h1="Stone Coated Steel Roofing Cost in Texas: Complete Pricing Guide",
        description="What stone coated steel roofing costs in Texas: $10–$18 per sq ft installed, typical totals by roof size, what drives price, and how it compares with asphalt."),
    "/best-roofing-material-for-hailstorms-in-texas/": dict(
        title="Best Roof Material for Hail: Texas Homeowner's Guide",
        h1="Best Roof Material for Hail in Texas: A Complete Homeowner's Guide",
        description="The best roof material for hail in Texas compared — Class 4 stone coated steel, impact shingles, tile and standing seam — with ratings, cost and lifespan."),
    "/best-roof-for-texas-hailstorms/": dict(
        title="Best Roof for Hail Storms in Texas",
        description="Choosing the best roof for Texas hail storms: which systems carry UL 2218 Class 4 ratings, how they hold up to large hail, and what insurers reward."),
    "/hurricane-resistant-roofing-systems/": dict(
        title="Hurricane Resistant Roofing: Hurricane Proof Roofs for Texas",
        h1="Hurricane Resistant Roofing Systems: Building a Hurricane Proof Roof in Texas",
        description="Hurricane resistant roofing for the Texas coast: uplift ratings, foam-set stone coated steel, roof shape and fasteners that make a roof hurricane proof."),
    "/roof-replacement-after-hail-storm/": dict(
        title="Hail Damage Roof Replacement: After the Hail Storm",
        h1="Hail Damage Roof Replacement: What to Do After a Hail Storm",
        description="Roof replacement after a hail storm: spotting hail damage, filing the claim, repair vs replace, and upgrading to a Class 4 stone coated steel roof in Texas."),
    "/wind-resistant-roofing-texas/": dict(
        title="Wind Resistant Roofing in Texas: Best Roofs for High Winds",
        description="Wind resistant roofing in Texas: the best roofing material for high winds, uplift ratings to look for, and why interlocking stone coated steel stays on."),
    "/what-roof-performs-best-during-texas-windstorms/": dict(
        title="Storm Resistant Roofs: What Performs Best in Texas Storms",
        h1="Storm Resistant Roofs: What Roof Performs Best During Texas Windstorms?",
        description="Which storm resistant roofs hold up best in Texas windstorms and tornado-driven gusts — uplift testing, roof shape, fastening and material compared."),
    "/stone-coated-roof-maintenance-checklist/": dict(
        title="Roof Maintenance Checklist & Log (Printable)",
        h1="Stone Coated Roof Maintenance Checklist: Schedule, Log, and Inspection Steps",
        description="A roof maintenance checklist, schedule and log for stone coated steel roofs — what to inspect each season and after storms. Includes an interactive log tool."),
    "/church-metal-roofing-systems/": dict(
        title="Best Roofing for Churches: Church Metal Roofing Systems",
        h1="Church Metal Roofing Systems: The Best Roofing for Churches and Religious Buildings",
        description="Best roofing for churches in Texas: metal and stone coated steel systems for sanctuaries, steeples and fellowship halls, with budgeting and phasing advice."),
    "/hotel-roofing-replacement/": dict(
        title="Hotel Roofing Replacement & Hospitality Roof Warranties",
        h1="Hotel Roofing Replacement: What Owners Need to Know (Including Hospitality Roofing Warranties)",
        description="Hotel roofing replacement without closing rooms: phasing, guest safety, hospitality roofing warranty terms, and long-life stone coated steel for mansard roofs."),
    "/hoa-roofing-replacement/": dict(
        title="HOA Roof Replacement: Who Pays & How to Plan It",
        h1="HOA Roof Replacement: A Complete Guide for Communities and Board Members",
        description="HOA roof replacement explained: does the HOA cover roof replacement, budgeting and reserves, material requirements, bidding and community-wide reroof planning."),
    "/wood-shake-roof/": dict(
        title="Wood Shake Roof: Looks, Lifespan & Stone Coated Option",
        description="Wood shake roof pros and cons in Texas — fire risk, rot and upkeep — and how stone coated steel shake gives the cedar look with a Class A fire rating."),
    "/apartment-roofing-systems-texas/": dict(
        title="Apartment Roofing Systems in Texas: Multifamily Guide",
        description="Apartment roofing systems in Texas: choosing an apartment roof for multifamily buildings, phasing work around tenants, and cutting lifecycle cost."),
    "/tilcor-stone-coated-steel-roof/": dict(
        title="Tilcor Roofing Systems: Tilcor Stone Coated Steel Review",
        description="Tilcor roofing systems reviewed: Tilcor stone coated steel profiles, hurricane ratings, warranty, Tilcor roofing cost, and where it fits Texas homes."),
    "/stone-coated-vs-standing-seam-metal/": dict(
        title="Stone Coated Steel vs Standing Seam Metal Roofing",
        h1="Stone Coated Steel Roofing vs Standing Seam Metal: Which Is Worth It?",
        description="Stone coated steel roofing vs standing seam metal: lifespan, hail denting, noise, looks, cost and insurance compared for Texas homes."),
    "/insurance-discounts-for-class-4-roofing/": dict(
        title="Class 4 Roof Insurance Discounts in Texas (Shingles & Steel)",
        description="Class 4 shingles and stone coated steel insurance discounts in Texas: how much you can save, the Class 4 roof certificate, and how to claim the discount."),
    "/can-you-get-insurance-discounts-for-stone-coated-roofing/": dict(
        title="Metal Roof Insurance Discount: Does Stone Coated Qualify?",
        description="Does a metal roof lower your insurance? How stone coated steel qualifies for impact-resistant roof discounts in Texas and what paperwork insurers ask for."),
    "/what-is-stone-coated-steel-roofing/": dict(
        title="What Is Stone Coated Steel Roofing? Complete Guide",
        description="What is stone coated steel roofing? How the steel core, coatings and stone granules work, the profiles available, lifespan, cost and who it suits."),
    "/stone-coated-roofing-reviews/": dict(
        title="Stone Coated Metal Roofing Reviews: What Owners Say",
        description="Stone coated metal roofing reviews: what homeowners love, common complaints, and whether stone coated steel roofing is worth it in Texas."),
    "/stone-coated-vs-asphalt-shingle/": dict(
        title="Stone Coated Steel Roofing vs Asphalt Shingles",
        description="Stone coated steel roofing vs asphalt shingles: 70 vs 20-year lifespan, Class 4 hail, cost per square and insurance discounts compared side by side."),
    "/class-4-stone-coated-roofing/": dict(
        title="Class 4 Stone Coated Roofing: Impact Resistant Metal Roofs",
        description="Class 4 stone coated roofing explained: UL 2218 impact testing, how Class 4 metal roofs handle Texas hail, and the insurance savings they can unlock."),
    "/stone-coated-steel-roof-lifespan/": dict(
        title="Stone Coated Steel Roof Lifespan: How Long It Lasts",
        description="How long does a stone coated steel roof last? Real-world lifespan in Texas heat and hail, warranty terms, and what shortens or extends it."),
    "/decra-stone-coated-metal-roofing-review/": dict(
        title="Decra Stone Coated Metal Roofing Review",
        description="Decra stone coated metal roofing reviewed: profiles, Class 4 hail and wind ratings, warranty, cost and how Decra compares with Tilcor, TEK and Roser."),
    "/stone-coated-steel-roof-warranty/": dict(
        title="Stone Coated Steel Roof Warranty: What's Covered",
        description="Stone coated steel roof warranties explained: 50-year vs lifetime, transferability, hail and wind coverage, and the installer workmanship warranty."),
}

# Area pages: better titles/H1s than the WordPress "Houston" page title
AREA_KEYWORDS = {
    "houston": ("Stone Coated Steel Roofing Houston TX", "Hail resistant roofing in Houston, TX — stone coated steel built for hurricanes, hail and Gulf humidity. Free estimates from Stone Coated Roofs."),
    "dallas": ("Stone Coated Steel Roofing Dallas TX", "Stone-coated steel roofing in Dallas, TX: Class 4 hail protection, 120 mph wind ratings and every major brand. Free estimates from Stone Coated Roofs."),
    "corpus-christi": ("Stone Coated Steel Roofing Corpus Christi", "Stone coated steel roofing in Corpus Christi: hurricane-rated Tilcor and Decra systems, foam-set installs and salt-air protection. Free coastal estimates."),
    "lubbock": ("Stone Coated Steel Roofing Lubbock TX", "Stone coated steel roofing in Lubbock, TX — Class 4 hail and high-wind protection for the South Plains, an upgrade over impact shingles. Free estimates."),
}
