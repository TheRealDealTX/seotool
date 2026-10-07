"""Site-wide constants for cebudavao.com."""
from datetime import date

SITE = {
    "name": "Cebu-Davao",
    "tagline": "News, travel, food & life from Cebu, Davao and the Philippines",
    "origin": "https://cebudavao.com",
    "email": "hello@cebudavao.com",
    "locale": "en_PH",
    "lang": "en",
    "founded": "2010",
    "editorial": "Cebu-Davao Editorial Team",
}

TODAY = date.today().isoformat()

# slug -> (name, short description, accent colour)
CATEGORIES = {
    "news":          ("News", "Explainers, public-service guides and the latest headlines from Cebu, Davao and the Philippines.", "#d62839"),
    "travel":        ("Travel", "Beaches, islands, mountains and how to get there — Cebu, Davao and the best of the Philippines.", "#0e9f9a"),
    "food":          ("Food", "Lechon, kinilaw, street food and home recipes from Visayas and Mindanao kitchens.", "#f08a24"),
    "culture":       ("Culture", "Festivals, faith, history and the Bisaya language — the stories behind the places.", "#7b4fd6"),
    "lifestyle":     ("Lifestyle", "Health, books, home and everyday living in the Philippines.", "#e0457b"),
    "entertainment": ("Entertainment", "OPM, P-pop, movies and the music scenes of Cebu and Davao.", "#c2185b"),
    "sports":        ("Sports", "Basketball, boxing, football, running and the pickleball boom.", "#1f7a3a"),
    "money":         ("Money & Work", "Jobs, renting, banking and the real cost of living in Cebu and Davao.", "#2b6cb0"),
    "tech":          ("Tech & Esports", "E-wallets, internet, gadgets and the Mobile Legends nation.", "#334155"),
    "expat-living":  ("Living Abroad", "Moving, renting and travelling — guides from our Texan wanderlust years.", "#8a6d3b"),
}

PLACES = {
    "cebu":  ("Cebu", "/cebu/"),
    "davao": ("Davao", "/davao/"),
    "other": ("Philippines", "/philippines/"),
}

NAV = [
    ("News", "/news/"),
    ("Cebu", "/cebu/"),
    ("Davao", "/davao/"),
    ("Travel", "/category/travel/"),
    ("Food", "/category/food/"),
    ("Culture", "/category/culture/"),
    ("Sports", "/category/sports/"),
    ("Entertainment", "/category/entertainment/"),
    ("Money", "/category/money/"),
    ("Tech", "/category/tech/"),
    ("Weather", "/weather/"),
    ("Tools", "/tools/"),
]

# Weather pages: slug -> (name, lat, lon, region, blurb)
WEATHER_CITIES = {
    "cebu-city": ("Cebu City", 10.3157, 123.8854, "Central Visayas",
        "Cebu City has a tropical climate with a drier stretch from roughly February to May and more rain from June to December. Typhoons that cross the Visayas can bring strong winds and heavy rain, most often in the second half of the year."),
    "davao-city": ("Davao City", 7.1907, 125.4553, "Davao Region",
        "Davao City is warm year-round and sits south of the usual typhoon tracks, so its rain comes mostly from afternoon thunderstorms rather than cyclones. There is no sharp dry season; showers can happen in any month."),
    "lapu-lapu-city": ("Lapu-Lapu City (Mactan)", 10.3103, 123.9494, "Central Visayas",
        "Mactan shares Cebu's pattern: generally drier, sunnier months in the first half of the year and a wetter season later. Sea conditions for island hopping depend on wind — check advisories before booking boats."),
    "manila": ("Manila", 14.5995, 120.9842, "Metro Manila",
        "Metro Manila has a distinct dry season (about December to May, hottest in April-May) and a southwest-monsoon rainy season from about June to October, when flooding and typhoons are most likely."),
    "baguio": ("Baguio", 16.4023, 120.5960, "Cordillera",
        "At around 1,500 metres, Baguio is the coolest major city in the Philippines. The dry months are pleasant, while the rainy season brings very heavy rain and fog."),
    "boracay": ("Boracay", 11.9674, 121.9248, "Western Visayas",
        "Boracay's White Beach is calmest during the amihan (northeast monsoon) months of roughly November to May. During habagat (about June to October) many boats move to the eastern side."),
    "bohol": ("Tagbilaran, Bohol", 9.6475, 123.8556, "Central Visayas",
        "Bohol's weather tracks Cebu's: drier months early in the year, more rain from mid-year. Typhoon season can disrupt fast craft trips across the Bohol Strait."),
    "siargao": ("Siargao (General Luna)", 9.7868, 126.1569, "Caraga",
        "Siargao faces the Pacific, so it gets rain in most months, with the wettest stretch usually from about November to January. Surf is biggest roughly from August to November."),
    "el-nido": ("El Nido, Palawan", 11.1784, 119.3923, "Palawan",
        "El Nido is best visited from about November to May. The southwest monsoon from roughly June to October brings rougher seas that can cancel island-hopping tours."),
    "cagayan-de-oro": ("Cagayan de Oro", 8.4542, 124.6319, "Northern Mindanao",
        "Cagayan de Oro is warm year-round with rain spread across the year. It is less exposed to typhoons than the Visayas, but tropical storms can still cause floods."),
    "general-santos": ("General Santos", 6.1164, 125.1716, "SOCCSKSARGEN",
        "General Santos is one of the drier cities in Mindanao and lies well south of the usual typhoon belt. Expect hot, sunny days with occasional thunderstorms."),
    "iloilo-city": ("Iloilo City", 10.7202, 122.5621, "Western Visayas",
        "Iloilo has a dry season of roughly December to May and a wet season from about June to November, when the southwest monsoon and typhoons bring heavy rain."),
}
