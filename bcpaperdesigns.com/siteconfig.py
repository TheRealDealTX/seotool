"""Site-wide constants for bcpaperdesigns.com."""

SITE = {
    "name": "BC Paper Designs",
    "origin": "https://bcpaperdesigns.com",
    "email": "info@bcpaperdesigns.com",
    "tagline": "Paper party decorations, theme guides and free party tools",
    "founded": "2017",
}

NAV = [
    ("Party Themes", "/collections/", [
        ("Baby shower themes", "/collections/baby-shower-decorations/", "Elephants, woodland, safari, ducks and more"),
        ("Birthday party themes", "/collections/birthday-party-decorations/", "Trucks, dinosaurs, monsters, sports"),
        ("Banners", "/collections/banners/", "Pennants, wording ideas and printables"),
        ("All party themes", "/collections/", "Browse and filter every theme"),
    ]),
    ("Party Tools", "/tools/", [
        ("Party banner maker", "/tools/party-banner-maker/", "Type a message, print a banner"),
        ("Party food calculator", "/tools/party-food-calculator/", "How much to buy for your guest list"),
        ("Planning timeline", "/tools/party-planning-timeline/", "A dated countdown checklist"),
        ("Party theme finder", "/tools/party-theme-finder/", "A 5-question theme quiz"),
        ("Baby shower bingo", "/tools/baby-shower-bingo-generator/", "Print unique bingo cards"),
    ]),
    ("Ideas Blog", "/blog/", None),
    ("About", "/about/", None),
]

COLLECTIONS = {
    "baby-shower-decorations": {
        "name": "Baby Shower Decorations",
        "title": "Baby Shower Decorations & Theme Ideas",
        "description": "Baby shower decorations and theme ideas: elephant, woodland, safari, whale, duck and book themes with color palettes, decor lists and DIY printables.",
        "intro": "Every baby shower theme we have designed, from sweet pink elephants to gender-neutral yellow and grey. Each guide comes with a color palette, the paper pieces that make the room, food and game ideas, and a checklist you can tick off as you go.",
        "image": "baby-feet-pink",
        "tag": "baby-shower",
    },
    "birthday-party-decorations": {
        "name": "Birthday Party Decorations",
        "title": "Kids Birthday Party Decorations & Themes",
        "description": "Kids birthday party decorations and theme ideas: construction, fire truck, dinosaur, monster, reptile, sports and more, with palettes, DIY printables and checklists.",
        "intro": "Birthday themes for first birthdays through tweens: diggers and fire trucks, dinosaurs and sharks, friendly monsters, bowling and football. Pick a theme, grab the palette and build the party piece by piece.",
        "image": "birthday-candles-sprinkles",
        "tag": "birthday",
    },
    "banners": {
        "name": "Party Banners",
        "title": "Party Banners: Baby Shower & Birthday Banner Ideas",
        "description": "Party banner ideas for baby showers and birthdays: wording, sizes, pennant shapes and how to hang them, plus a free printable banner maker.",
        "intro": "A banner is the one decoration every guest photographs. These guides cover wording, letter sizes, pennant shapes and hanging tricks, and our free banner maker prints any message on letter-size cardstock.",
        "image": "paper-heart-garland",
        "tag": "banners",
    },
}

# Quiz tags for the theme finder (who / vibe / color / world)
THEME_TAGS = {
    "pink-elephant-baby-shower-decorations": "girl sweet pink animals",
    "blue-elephant-baby-shower-decorations": "boy sweet blue animals",
    "yellow-elephant-baby-shower-decorations-yellow-and-grey": "neutral sweet neutral animals",
    "yellow-elephant-baby-shower-banner-for-gender-neutral-party": "neutral sweet neutral animals",
    "pdf-elephant-baby-shower-or-birthday-decorations-banner-invitations-cake-topper-centerpiece-cupcakes-diy-printable": "neutral girl boy sweet neutral animals",
    "construction-truck-birthday-decorations": "boy little big bold bright vehicles",
    "fire-truck-birthday-party-decorations": "boy little big bold bright vehicles",
    "blue-boy-lion-king-baby-shower-decorations": "boy natural blue animals",
    "monster-birthday-party-decorations": "little big playful bright storybook",
    "reptile-birthday-party-decorations": "big boy natural bright animals",
    "b-whale-baby-shower-navy-teal-b-br-or-birthday-party-decorations": "boy neutral sweet blue ocean",
    "coral-owl-baby-shower-or-birthday-party-decorations": "girl neutral natural pink animals",
    "ladybug-birthday-party-or-baby-shower-decorations": "girl little playful bright animals",
    "pink-gold-giraffe-baby-shower-or-birthday-party-decorations": "girl sweet pink animals",
    "woodland-baby-shower-decorations": "neutral natural neutral animals",
    "dinosaur-birthday-party-or-baby-shower-decorations": "boy little big bold bright animals",
    "baby-shark-birthday-party-or-baby-shower-decorations": "little playful blue bright ocean",
    "jungle-safari-baby-shower-decorations": "little big natural neutral animals",
    "jungle-safari-baby-shower-decorations-1": "neutral boy natural neutral animals",
    "duck-baby-shower-decorations-blue-yellow": "boy neutral sweet blue ocean",
    "pink-girl-rubber-duck-baby-shower-or-birthday-party-decorations": "girl little sweet pink ocean",
    "pink-hot-air-balloon-baby-shower-decorations": "girl sweet pink storybook",
    "book-themed-baby-shower-decorations-printable-instant-download-banner-centerpiece-cupcakes-thank-you-games": "neutral sweet neutral storybook",
    "book-themed-baby-shower-games-printable-instant-download": "neutral playful neutral storybook",
    "bowling-birthday-cake-topper-bowling-party-decorations-diy-printable-decorations-made-to-match-banner-invitation-signs-cupcake-toppers-favor-tags": "big bold bright games",
    "football-birthday-cake-topper-football-party-decorations-personalized-diy-printable-editable-made-to-match-banner-invitation-signs-cupcake-toppers-favor-tags": "big boy bold blue games",
    "kids-halloween-birthday-party-decorations-instant-download-printable-files-banner-centerpiece-cupcake-toppers-thank-you-cards": "little big playful bright games",
    "pink-girl-turtle-party-banners": "girl little playful pink ocean",
    "pink-turtle-baby-shower-or-birthday-party-decorations": "girl sweet pink ocean",
    "my-little-pony-horse-birthday-party-or-baby-shower-decorations": "girl little sweet pink animals",
    "emoji-banner": "big playful bright games",
}

# Old store URLs folded into a sibling page (301s, see index.php)
PRODUCT_ALIASES = {
    "fire-truck-birthday-decorations-instant-download-printable-files-banner-centerpiece-cupcake-toppers-thank-you-cards": "fire-truck-birthday-party-decorations",
    "monster-birthday-banner-party-decoration-supplies-happy-birthday-handmade-in-usa": "monster-birthday-party-decorations",
    "reptile-birthday-decorations-instant-download-printable-files-banner-centerpiece-cupcake-toppers-thank-you-cards": "reptile-birthday-party-decorations",
    "reptile-birthday-banner-party-decoration-supplies-happy-birthday-handmade-in-usa": "reptile-birthday-party-decorations",
    "woodland-animal-themed-baby-shower-decorations-printable-instant-download-banner-centerpiece-cupcakes-thank-you-games": "woodland-baby-shower-decorations",
    "pink-girl-book-themed-baby-shower-games-printable-instant-download": "book-themed-baby-shower-games-printable-instant-download",
    "pink-girl-turtle-party-banners-instant-download-pdf-printable-file": "pink-girl-turtle-party-banners",
}

# Highest-traffic themes, shown first on the homepage
FEATURED = [
    "pink-elephant-baby-shower-decorations",
    "construction-truck-birthday-decorations",
    "yellow-elephant-baby-shower-banner-for-gender-neutral-party",
    "blue-boy-lion-king-baby-shower-decorations",
    "monster-birthday-party-decorations",
    "reptile-birthday-party-decorations",
    "b-whale-baby-shower-navy-teal-b-br-or-birthday-party-decorations",
    "woodland-baby-shower-decorations",
]
