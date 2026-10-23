"""Amazon product catalog for dogearcleaner.com.

Every affiliate link on the site is built from this file, so the tracking tag
is defined exactly once. ASINs were taken from Amazon US search results on
2026-10-23. Prices and star ratings are deliberately NOT stored or shown: the
Amazon Associates agreement forbids static prices/ratings, so the site uses
"Check price on Amazon" calls to action instead.

Content files reference products by key with shortcodes (see CONTENT_SPEC.md):
    [[product:epi-otic]]                 full product card
    [[amazon:epi-otic|anchor text]]      inline text link
    [[amazon-search:dog ear powder|anchor text]]   Amazon search link (accessories)
"""

from urllib.parse import quote_plus

AMAZON_TAG = "dogearcleanerjditt-20"


def amazon_url(asin):
    return f"https://www.amazon.com/dp/{asin}?tag={AMAZON_TAG}"


def amazon_search_url(query):
    return f"https://www.amazon.com/s?k={quote_plus(query)}&tag={AMAZON_TAG}"


# key: (asin, display name, brand, one-line "best for", feature tags, review page or None)
PRODUCTS = {
    "epi-otic": dict(
        asin="B0056EAKUA", name="Virbac Epi-Otic Advanced Ear Cleanser (4 oz)", brand="Virbac",
        best_for="Best overall routine cleaner, vet favorite",
        tags=["alcohol-free", "drying", "ph-balanced", "vet-brand"],
        review="/virbac-epi-otic-flush-review/"),
    "epi-otic-8oz": dict(
        asin="B0056EAKSM", name="Virbac Epi-Otic Advanced Ear Cleaner (8 oz)", brand="Virbac",
        best_for="Best value size for multi-dog homes and weekly cleaners",
        tags=["alcohol-free", "drying", "ph-balanced", "vet-brand"],
        review="/virbac-epi-otic-flush-review/"),
    "zymox-cleanser": dict(
        asin="B0064HTOVY", name="Zymox Ear Cleanser with Bio-Active Enzymes (4 oz)", brand="Zymox",
        best_for="Best enzymatic cleaner for smelly, waxy ears",
        tags=["alcohol-free", "enzymatic", "gentle"],
        review="/zymox-ear-cleanser-review/"),
    "zymox-otic": dict(
        asin="B007NVJAJG", name="Zymox Otic Enzymatic Solution with 0.5% Hydrocortisone", brand="Zymox",
        best_for="Over-the-counter enzymatic treatment for itchy, inflamed ears",
        tags=["enzymatic", "hydrocortisone", "treatment"],
        review="/zymox-ear-cleanser-review/"),
    "vetericyn-plus": dict(
        asin="B01N6AFRVA", name="Vetericyn Plus Dog Ear Rinse", brand="Vetericyn",
        best_for="Best no-sting rinse for sensitive or sore ears",
        tags=["alcohol-free", "no-sting", "gentle", "hypochlorous"],
        review="/vetericyn-plus-ear-rinse-review/"),
    "vetericyn-triple": dict(
        asin="B0DZLNB221", name="Vetericyn Triple-Action Dog Ear Treatment (1% Hydrocortisone)", brand="Vetericyn",
        best_for="Itch relief drops to pair with the Plus rinse",
        tags=["hydrocortisone", "treatment"],
        review="/vetericyn-plus-ear-rinse-review/"),
    "petmd-tris-flush": dict(
        asin="B07YXCG1NW", name="Pet MD Veterinary Tris Flush Ear Cleaner (12 oz)", brand="Pet MD",
        best_for="Best budget flush: Tris-EDTA plus ketoconazole in a big bottle",
        tags=["tris-edta", "ketoconazole", "budget"],
        review="/pet-md-ear-flush-review/"),
    "petmd-otic-clean": dict(
        asin="B07YXD2VVB", name="Pet MD Otic Clean Ear Solution, Cucumber Melon (8 oz)", brand="Pet MD",
        best_for="Pleasant-smelling everyday cleaner",
        tags=["scented", "budget"],
        review="/pet-md-ear-flush-review/"),
    "petmd-wipes": dict(
        asin="B01IRO7WR4", name="Pet MD Dog Ear Cleaning Wipes (100 ct)", brand="Pet MD",
        best_for="Best ear wipes for quick outer-ear cleanups",
        tags=["wipes", "budget"],
        review="/pet-md-ear-flush-review/"),
    "zymox-wipes": dict(
        asin="B0CSGXJV7K", name="Zymox Advanced Enzymatic Ear Wipes (100 ct)", brand="Zymox",
        best_for="Enzymatic wipes for between-flush maintenance",
        tags=["wipes", "enzymatic"],
        review=None),
    "epiklean": dict(
        asin="B07N1KSYD3", name="Dechra EpiKlean Ear Cleanser (12 oz)", brand="Dechra",
        best_for="Vet-clinic alternative to Epi-Otic",
        tags=["vet-brand", "drying"],
        review=None),
    "ear-therapy": dict(
        asin="B0002DIP5C", name="Veterinary Formula Clinical Care Ear Therapy (4 oz)", brand="Veterinary Formula",
        best_for="Cheapest gentle cleaner for light wax",
        tags=["alcohol-free", "budget", "gentle"],
        review=None),
    "nutri-vet": dict(
        asin="B00CHRZB9E", name="Nutri-Vet Ear Cleanse for Dogs, Aloe Vera (8 oz)", brand="Nutri-Vet",
        best_for="Budget cleaner with soothing aloe",
        tags=["budget", "aloe"],
        review=None),
    "vets-best": dict(
        asin="B00335SI08", name="Vet's Best Dog Ear Relief Wash (4 oz)", brand="Vet's Best",
        best_for="Plant-based option for owners avoiding harsher actives",
        tags=["natural", "gentle"],
        review=None),
    "pet-honesty": dict(
        asin="B0CQN1GXM9", name="Pet Honesty Restore + Soothe Ear Cleaner (4 oz)", brand="Pet Honesty",
        best_for="Aloe-based cleaner for itchy, allergy-prone ears",
        tags=["aloe", "gentle"],
        review=None),
    "skouts-honor": dict(
        asin="B07YP9CZ3X", name="Skout's Honor Probiotic Dog Ear Cleaner (4 oz)", brand="Skout's Honor",
        best_for="Microbiome-friendly, non-medicated cleaner",
        tags=["alcohol-free", "probiotic", "natural"],
        review=None),
}

# Accessories are linked as Amazon searches (no single ASIN is the obvious pick).
ACCESSORIES = {
    "cotton-rounds": ("Large cotton rounds", "large cotton rounds for pet ear cleaning"),
    "gauze": ("Non-woven gauze pads", "non woven gauze pads 4x4"),
    "ear-powder": ("Dog ear powder", "dog ear powder"),
    "lick-mat": ("Lick mat for dogs", "lick mat for dogs"),
    "dog-towel": ("Microfiber dog drying towel", "microfiber dog drying towel"),
    "dog-dryer": ("Low-heat dog grooming dryer", "dog grooming dryer low heat"),
    "otoscope": ("Pet otoscope", "pet otoscope"),
    "treats": ("Soft training treats", "soft dog training treats"),
    "swim-ear": ("Dog ear drying solution", "dog ear drying solution after swimming"),
    "snood": ("Dog ear snood", "dog ear snood"),
    "slicker-brush": ("Slicker brush", "dog slicker brush"),
    "deshedding-tool": ("Deshedding tool", "dog deshedding tool"),
}

for p in PRODUCTS.values():
    p["url"] = amazon_url(p["asin"])
