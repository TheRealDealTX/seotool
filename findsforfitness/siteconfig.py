"""Site-wide constants for findsforfitness.com."""

from datetime import date

SITE = {
    "name": "Finds For Fitness",
    "short": "FindsForFitness",
    "tagline": "Fitness gear, workouts, weight loss & skin care, minus the hype",
    "origin": "https://findsforfitness.com",
    "email": "info@findsforfitness.com",
    "description": (
        "Honest fitness gear guides, beginner workouts, weight loss nutrition and "
        "skin care tips, plus free calculators to plan your training."
    ),
}

# Category slugs match the old WordPress URLs (/category/<slug>/) so existing links keep working.
CATEGORIES = {
    "workout": {
        "name": "Workouts",
        "title": "Workouts & Training",
        "blurb": "Beginner-friendly routines, running plans and strength training that fit real schedules.",
        "image": "home-workout-class",
        "color": "lime",
    },
    "weight_loss": {
        "name": "Weight Loss",
        "title": "Weight Loss & Nutrition",
        "blurb": "Sustainable eating habits, calorie basics and breakfasts that keep you full.",
        "image": "colorful-salad",
        "color": "coral",
    },
    "skin_care": {
        "name": "Skin Care",
        "title": "Skin Care & Glow-Up",
        "blurb": "Simple routines and ingredient guides for healthy, comfortable skin.",
        "image": "avocado-face-mask",
        "color": "violet",
    },
    "product-reviews": {
        "name": "Gear Guides",
        "title": "Fitness Gear Guides",
        "blurb": "Shoes and gear picks for flat feet, courts and roads, with buying guides that explain why.",
        "image": "neon-trainer",
        "color": "sky",
    },
    "health-tips": {
        "name": "Health Tips",
        "title": "Everyday Health Tips",
        "blurb": "Hydration, protein, foot health and recovery habits that support every workout.",
        "image": "glass-of-water",
        "color": "amber",
    },
}

NAV = [
    ("Workouts", "/category/workout/"),
    ("Weight Loss", "/category/weight_loss/"),
    ("Skin Care", "/category/skin_care/"),
    ("Gear Guides", "/category/product-reviews/"),
    ("Free Tools", "/tools/"),
    ("Blog", "/blog/"),
]

TODAY = date.today().isoformat()
