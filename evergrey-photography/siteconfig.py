"""Business details, navigation and tool data for evergrey-photography.com."""

SITE = "https://www.evergrey-photography.com"
NAME = "Evergrey Photography"
EMAIL = "info@evergrey-photography.com"
CITY = "Victoria"
REGION = "BC"
GEO = (48.4284, -123.3656)
AREAS = [
    "Victoria", "Oak Bay", "Saanich", "Esquimalt", "Colwood", "Langford", "Metchosin",
    "Sooke", "Sidney", "Cowichan Valley", "Nanaimo", "Tofino", "Vancouver Island",
]

NAV = [
    ("/weddings", "Weddings"),
    ("/elopements", "Elopements"),
    ("/engagements", "Couples"),
    ("/portfolio", "Portfolio"),
    ("/pricing", "Pricing"),
    ("/blog", "Journal"),
    ("/tools", "Tools"),
    ("/about", "About"),
]

# Sun-tool locations: key, name, lat, lng
LOCATIONS = [
    ("victoria", "Victoria Inner Harbour", 48.4222, -123.3700),
    ("hatley", "Hatley Castle, Colwood", 48.4335, -123.4725),
    ("aylard", "Aylard Farm, East Sooke Park", 48.3480, -123.6280),
    ("fisgard", "Fisgard Lighthouse", 48.4303, -123.4475),
    ("dallas", "Dallas Road & Clover Point", 48.4072, -123.3530),
    ("mtdoug", "Mount Douglas (PKOLS)", 48.4927, -123.3450),
    ("butchart", "Brentwood Bay & Butchart Gardens", 48.5636, -123.4697),
    ("goldstream", "Goldstream Provincial Park", 48.4770, -123.5480),
    ("frenchbeach", "French Beach, Juan de Fuca coast", 48.3970, -123.9480),
    ("botanical", "Botanical Beach, Port Renfrew", 48.5296, -124.4430),
    ("cowichan", "Cowichan Valley (Duncan)", 48.7787, -123.7079),
    ("nanaimo", "Nanaimo", 49.1659, -123.9401),
    ("tofino", "Chesterman Beach, Tofino", 49.1180, -125.8930),
]

# Elopement finder spots. scene: forest / ocean / garden / city / view
SPOTS = [
    dict(name="Aylard Farm, East Sooke Regional Park", loc="aylard", scene=["ocean", "forest"], walk="moderate", privacy="med", drive=45,
         blurb="An open meadow that runs down to pocket beaches and wind-shaped rock. Short trails, huge views across the strait, and our favourite rainy-day forest edges."),
    dict(name="Botanical Beach, Port Renfrew", loc="botanical", scene=["ocean"], walk="moderate", privacy="med", drive=120,
         blurb="Sandstone shelves, tide pools and old-growth on the walk in. Plan around a low tide and leave the whole afternoon for it."),
    dict(name="Mystic Beach, Juan de Fuca", loc="frenchbeach", scene=["ocean", "forest"], walk="hike", privacy="high", drive=75,
         blurb="A rooty forest trail drops to a beach with a waterfall spilling over the cliff. Wear real shoes and bring a dry bag for the dress."),
    dict(name="French Beach Provincial Park", loc="frenchbeach", scene=["ocean", "forest"], walk="easy", privacy="med", drive=60,
         blurb="A wide pebble beach a few steps from the parking area, with big driftwood and moody Olympic Mountain views across the water."),
    dict(name="Goldstream Provincial Park", loc="goldstream", scene=["forest"], walk="easy", privacy="med", drive=25,
         blurb="Towering cedars and Douglas-firs close to the city. The canopy softens the light and keeps most of the rain off."),
    dict(name="Mount Finlayson summit", loc="goldstream", scene=["view"], walk="hike", privacy="high", drive=30,
         blurb="A steep, scrambly climb rewarded with a panorama over the Saanich Inlet. Best for confident hikers in dry weather."),
    dict(name="Mount Douglas (PKOLS) summit", loc="mtdoug", scene=["view", "forest"], walk="easy", privacy="low", drive=15,
         blurb="A 360-degree view over Haro Strait and the Gulf Islands with a road almost to the top — sunrise here is spectacular."),
    dict(name="Fisgard Lighthouse & Fort Rodd Hill", loc="fisgard", scene=["ocean", "city"], walk="easy", privacy="low", drive=20,
         blurb="A red-and-white lighthouse on a causeway with Esquimalt Lagoon nearby. Check Parks Canada hours and photography rules first."),
    dict(name="Hatley Park gardens", loc="hatley", scene=["garden"], walk="easy", privacy="med", drive=25,
         blurb="Edwardian castle walls, a Japanese garden and grand lawns. Professional photography requires a permit from Hatley Park."),
    dict(name="Abkhazi Garden", loc="victoria", scene=["garden"], walk="easy", privacy="med", drive=10,
         blurb="A small, romantic garden on a rocky Oak Bay hillside — rhododendrons in spring, Garry oaks all year."),
    dict(name="Dallas Road & Clover Point", loc="dallas", scene=["ocean", "city"], walk="easy", privacy="low", drive=5,
         blurb="Driftwood beaches, kites, and the Olympics on the horizon. Easy, central and gorgeous an hour before sunset."),
    dict(name="Inner Harbour & Fan Tan Alley", loc="victoria", scene=["city"], walk="easy", privacy="low", drive=0,
         blurb="Heritage brick, harbour lights and Canada's narrowest street. Ideal for blue-hour portraits and a celebratory dinner after."),
    dict(name="Witty's Lagoon Regional Park", loc="aylard", scene=["ocean", "forest"], walk="moderate", privacy="med", drive=30,
         blurb="A forest trail past a waterfall to a sandy spit and salt marsh. Soft, quiet and full of texture."),
    dict(name="Cathedral Grove (MacMillan Park)", loc="nanaimo", scene=["forest"], walk="easy", privacy="low", drive=150,
         blurb="Ancient Douglas-firs on the road to Tofino. Go early on a weekday — the boardwalk is popular."),
    dict(name="Chesterman Beach, Tofino", loc="tofino", scene=["ocean"], walk="easy", privacy="med", drive=270,
         blurb="Long open sand, surf, and sea-stack silhouettes at sunset. Make a weekend of it."),
    dict(name="Gonzales Hill", loc="dallas", scene=["view", "city"], walk="easy", privacy="med", drive=10,
         blurb="A little observatory on a rocky knoll with sweeping views of the city, the strait and Mount Baker."),
]

PRICING = dict(
    weddingBase=1700,
    weddingHour=250,
    elopement={
        "two": dict(label="Two-hour elopement", price=1650),
        "four": dict(label="Four-hour adventure elopement", price=2450),
        "micro": dict(label="Micro-wedding (up to 30 guests, 5 h)", price=2950),
    },
    addons={
        "second": dict(label="Second photographer", price=95, perHour=True),
        "engagement": dict(label="Engagement session", price=450),
        "album": dict(label="Heirloom linen album (10x10)", price=850),
        "rehearsal": dict(label="Rehearsal dinner coverage (1.5 h)", price=500),
        "prints": dict(label="Fine-art print box (20 prints)", price=320),
    },
    travel={
        "victoria": dict(label="Greater Victoria, Saanich Peninsula & West Shore", price=0),
        "sooke": dict(label="Sooke, Metchosin & East Sooke", price=75),
        "cowichan": dict(label="Cowichan Valley & Malahat", price=150),
        "nanaimo": dict(label="Nanaimo, Parksville & Qualicum", price=300),
        "ferry": dict(label="Gulf Islands or Vancouver (ferry)", price=450),
        "tofino": dict(label="Tofino & Ucluelet", price=650),
    },
)
