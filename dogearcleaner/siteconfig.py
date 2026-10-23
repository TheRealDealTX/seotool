"""Site-wide constants for dogearcleaner.com. Imported by build.py."""

from datetime import date

SITE = {
    "name": "Dog Ear Cleaner",
    "origin": "https://dogearcleaner.com",
    "tagline": "Safe dog ear cleaning guides, honest ear cleaner reviews and free tools",
    "logo": "/assets/img/Dog-Ear-Cleaner-Logo.webp",
    "social_image": "/assets/img/Dog-Ear-Cleaner-Site-Image.webp",
    "founded": "2026",
}

AUTHOR = {
    "name": "Dog Ear Cleaner Editorial Team",
    "url": "/about-us/",
    "bio": ("The Dog Ear Cleaner editorial team researches ear-care products the slow way: "
            "reading full ingredient lists and manufacturer directions, checking them against "
            "published veterinary guidance, and sorting through owner feedback for patterns. "
            "We are dog owners, not veterinarians, and we say so."),
}

NAV = [
    ("Best Ear Cleaners", "/best-dog-ear-cleaner/"),
    ("Reviews", "/topic/reviews/"),
    ("How-To", "/topic/how-to/"),
    ("Guides", "/topic/guides/"),
    ("Free Tools", "/tools/"),
    ("About", "/about-us/"),
]

CATEGORIES = {
    "reviews": {
        "name": "Dog Ear Cleaner Reviews",
        "short": "Reviews",
        "path": "/topic/reviews/",
        "title": "Dog Ear Cleaner Reviews: Epi-Otic, Zymox, Vetericyn & More",
        "description": ("Honest dog ear cleaner reviews from Dog Ear Cleaner: Virbac Epi-Otic, Zymox, "
                        "Vetericyn Plus and Pet MD compared on ingredients, gentleness and value."),
        "intro": ("Every dog ear cleaner review on Dog Ear Cleaner breaks a product down by what is actually "
                  "in the bottle, how it is meant to be used, which dogs it suits, and where it falls "
                  "short. Start with our roundup of the best dog ear cleaners if you just want a pick."),
    },
    "how-to": {
        "name": "Dog Ear Cleaning How-To Guides",
        "short": "How-To",
        "path": "/topic/how-to/",
        "title": "How to Clean Dog Ears: Step-by-Step How-To Guides",
        "description": ("Step-by-step dog ear cleaning how-to guides from Dog Ear Cleaner: supplies, "
                        "technique, mistakes to avoid and how often to clean your dog's ears."),
        "intro": ("Plain-language, step-by-step instructions for cleaning your dog's ears at home "
                  "safely, without cotton swabs, guesswork or a wrestling match."),
    },
    "guides": {
        "name": "Dog Ear Care Guides",
        "short": "Guides",
        "path": "/topic/guides/",
        "title": "Dog Ear Care Guides: Infections, Routines & Breeds",
        "description": ("Dog ear care guides from Dog Ear Cleaner: ear infection signs, cleaning routines, "
                        "floppy-ear breeds and after-bath care to keep your dog's ears healthy."),
        "intro": ("Deeper guides on keeping dog ears healthy: spotting infection early, building a "
                  "cleaning routine that fits your dog, and breed-specific ear care."),
    },
}

TODAY = date.today().isoformat()
