"""Photo assignments per post: hero image + inline figures.

Every file lives in static/assets/img/photos/<name>.webp (+ -sm.webp) and its
licence/credit is in photos.json (sourced via Openverse: CC0, public domain,
CC BY or CC BY-SA, all free for commercial use with attribution).
Captions describe what is actually in the photo; generic food shots are never
captioned as a specific restaurant.
"""

IMAGES = {
    "katz-deli-some-delicious-pastrami": {
        "hero": ("katzs-delicatessen-storefront-houston-street", "Katz's Delicatessen storefront on East Houston Street, New York", "Katz's Delicatessen at East Houston and Ludlow Streets."),
        "inline": [("katzs-delicatessen-neon-sign", "Katz's Delicatessen neon sign at dusk", "The neon has lit up the corner for generations."),
                   ("pastrami-sandwich-on-rye", "A pastrami sandwich on rye bread", "Pastrami on rye: the order.")],
    },
    "porto-rico-importing-co": {
        "hero": ("porto-rico-importing-co-bleecker-street", "Porto Rico Importing Co. storefront in Greenwich Village", "Porto Rico Importing Co.: \"finest coffee & tea since 1907\"."),
        "inline": [],
    },
    "little-tong-noodle-shop": {
        "hero": ("yunnan-rice-noodles-spicy-soup", "Yunnan-style rice noodles in a spicy red broth", "Spicy, sour and fragrant: Yunnan rice noodles come in endless variations."),
        "inline": [("yunnan-crossing-the-bridge-rice-noodles", "A bowl of Yunnan crossing-the-bridge rice noodles", "Crossing-the-bridge mixian, Yunnan's most famous noodle dish.")],
    },
    "mountain-province": {
        "hero": ("coffee-beans", "A bowl of coffee beans", "Philippine coffee spans Arabica, Robusta, Liberica and Excelsa."),
        "inline": [],
    },
    "subway-photos-trial-no1": {
        "hero": ("new-york-subway-car-riders-black-and-white", "Black and white photo of riders inside a New York subway car", "Riders on a New York subway car: the city's most democratic portrait studio."),
        "inline": [("new-york-subway-car-interior", "Passengers inside a New York City subway car", "Flat, greenish light and a captive audience.")],
    },
    "journalistic-inquiry-notes-quotes-and-details": {
        "hero": ("tsukuba-ramen-festival", "Crowds at an outdoor ramen festival", "A ramen festival in Tsukuba, Japan. Festivals like it are a crash course in reporting."),
        "inline": [("cup-noodles-museum-yokohama", "Exhibit at the Cup Noodles Museum in Yokohama", "The Cup Noodles Museum in Yokohama tells Momofuku Ando's story.")],
    },
    "its-more-than-just-a-slice-to-end-the-night": {
        "hero": ("2-bros-pizza-storefront-new-york", "2 Bros. Pizza storefront in New York City", "2 Bros. Pizza, the name most associated with the dollar slice."),
        "inline": [("dollar-pizza-slice-counter-new-york", "People eating slices outside a 2 Bros. Pizza shop at night", "The cheap slice: eaten standing up, any hour.")],
    },
    "defining-your-own-rules-welcome-to-the-new-age-of-spirituality": {
        "hero": ("metaphysical-shop-window", "Window of a metaphysical shop with hanging lanterns and stars", "Metaphysical shops double as gathering places."),
        "inline": [("tarot-card-and-candle", "A tarot-style card beside a candle on a moon-shaped holder", "Cards, candles and a practice of your own.")],
    },
    "pies-thighs-and-all-things-nice": {
        "hero": ("fried-chicken-biscuit-collard-greens", "Fried chicken with a biscuit and collard greens", "Fried chicken, a biscuit and greens: Southern comfort food."),
        "inline": [("fried-chicken-biscuits-and-gravy", "Fried chicken on biscuits with sausage gravy", "Biscuits and gravy, the brunch move.")],
    },
    "more-than-skin-deep-with-byron-kim": {
        "hero": ("hand-poked-tattoos-street-posters", "Street posters advertising hand-poked tattoos", "Hand-poked tattoos, advertised the DIY way."),
        "inline": [("japanese-hand-tattooing", "An artist tattooing by hand with a long needle tool", "Japanese hand tattooing (tebori): ink placed by hand, one point at a time.")],
    },
    "on-pole-dancing-with-shawanda-davis": {
        "hero": ("pole-dance-class-studio", "Students stretching during a pole dance class", "Flexibility work in a pole class."),
        "inline": [("pole-fitness-demonstration-union-square", "Pole fitness demonstration on a stage in Union Square, New York", "A pole fitness demonstration in Union Square, Manhattan.")],
    },
    "young-women-come-together-at-photoville-for-this-is-18-a-zine-by-the-nytimes": {
        "hero": ("photoville-shipping-container-exhibition", "Photographs displayed on a shipping container at Photoville", "Photoville shows work on repurposed shipping containers."),
        "inline": [],
    },
    "24-hours-in-new-orleans-a-mini-mardi-gras-bender": {
        "hero": ("krewe-of-orpheus-leviathan-float-new-orleans", "The Krewe of Orpheus Leviathan float, a giant sea dragon, at Mardi Gras World in New Orleans", "The Krewe of Orpheus' Leviathan float at Mardi Gras World, where many of the city's parade floats are built."),
        "inline": [("french-quarter-cast-iron-balcony", "Cast-iron balcony with hanging flower baskets in the French Quarter", "The French Quarter's cast-iron balconies.")],
    },
    "turkish-immigrant-restaurant-owners-in-new-york-amp-london": {
        "hero": ("ocakbasi-mixed-grill-london", "A Turkish mixed grill plate at an ocakbaşı restaurant in London", "A mixed grill at a London ocakbaşı."),
        "inline": [("green-lanes-harringay-festival-grill", "Charcoal grills at a street festival on Green Lanes, Harringay", "Grills out on Green Lanes during the Harringay festival."),
                   ("turkish-tea-glass", "Turkish tea in a tulip-shaped glass", "Tea, always: hospitality is part of the business model.")],
    },
    "4-photos-from-economy-candy": {
        "hero": ("economy-candy-storefront-rivington-street", "Economy Candy storefront with its red script sign and striped awning", "Economy Candy on Rivington Street."),
        "inline": [],
    },
    "4-photos-from-salerno": {
        "hero": ("salerno-coastline-aerial-view", "Aerial view of Salerno and its coastline on the Gulf of Salerno", "Salerno curves along its gulf at the start of the Amalfi Coast."),
        "inline": [],
    },
}

# The "4 Photos" series: (caption, text, photo name).
PLATES = {
    "4-photos-from-economy-candy": [
        ("The wall of bins", "Bins and shelves run floor to ceiling, holding jelly beans, gummies, malt balls and more licorice than you knew existed.", "economy-candy-wall-of-bins"),
        ("Est. 1937", "The flag outside says it plainly: Economy Candy, 108 Rivington Street, since 1937.", "economy-candy-sign-est-1937"),
        ("The window", "Windows packed with nostalgia candy: brands you remember from childhood and some you thought were discontinued.", "economy-candy-shop-window"),
        ("Rivington Street", "The storefront on the Lower East Side, a short walk from Katz's and the late-night slice shops.", "economy-candy-108-rivington-street"),
    ],
    "4-photos-from-salerno": [
        ("The lungomare", "Salerno's seafront promenade runs for more than a kilometer. At night the lights of the whole bay come on.", "salerno-lungomare-at-night"),
        ("Old-town rooftops", "Terracotta roofs pack the centro storico between the hills and the sea.", "salerno-old-town-rooftops"),
        ("Duomo bells", "The cathedral of San Matteo, consecrated in the 11th century, still marks the hours over the old town.", "salerno-duomo-san-matteo"),
        ("Castello di Arechi", "The medieval castle watches over the city from the ridge above the harbor.", "castello-di-arechi-salerno"),
    ],
}
