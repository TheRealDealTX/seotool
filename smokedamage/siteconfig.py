"""Global settings for SmokeDamage.com (the "Site Settings" / "Compliance
Information" collections). build.py reads these at build time; the PHP admin
can override the runtime-only ones (lead recipient, popup) without a rebuild.
"""

from datetime import date

SITE = {
    "brand": "Smoke Damage Public Adjuster",
    "domain": "SmokeDamage.com",
    "origin": "https://smokedamage.com",
    "company": "Rise Public Adjusting LLC",
    "license_number": "3356839",
    "license_label": "Texas Department of Insurance License #3356839",
    # Licensed business address exactly as on the TDI record (business location,
    # effective 01-28-2026; verified 2026-09-28 - see research/compliance.md).
    # Tex. Ins. Code 4102.113 requires name, address and license number in every
    # advertisement, which includes the website (28 TAC 19.712). Printed in the
    # footer, on /contact/ and in the Organization schema.
    "licensed_address": "5514 Imogen Dr., Belton, TX 76513",
    "phone_display": "+1 (844) 537-1427",
    "phone_href": "tel:+18445371427",
    "phone_e164": "+18445371427",
    "email": "info@smokedamage.com",
    "lead_recipient": "info@smokedamage.com",
    "service_area": "Texas",
    "blog_author": "Joseph Dittman",
    "tagline": ("SmokeDamage.com helps Texas homeowners and businesses document, prepare, "
                "and negotiate smoke and fire-related property insurance claims."),
    "cta_primary": "Request a Free Claim Review",
    "cta_short": "Free Claim Review",
    "popup_enabled": True,
    "popup_delay_seconds": 5,
    "social": {},  # e.g. {"facebook": "https://..."} - only real profiles
    # Analytics / verification IDs. Empty = not loaded.
    "ga4_id": "",
    "gsc_verification": "",
    "bing_verification": "",
}

DISCLAIMER = ("Information on this website is provided for general educational purposes and is "
              "not legal advice, an insurance coverage determination, a restoration recommendation, "
              "or a guarantee of any claim result. Insurance policies, losses, and claim "
              "circumstances vary.")

NAV = [
    ("Smoke Claims", "/smoke-damage-claims/", None),
    ("Fire Claims", "/fire-damage-claims/", None),
    ("Claim Help", "/smoke-damage-claim-process/", [
        ("Smoke Damage Claims", "/smoke-damage-claims/"),
        ("Fire Damage Claims", "/fire-damage-claims/"),
        ("Soot Damage", "/soot-damage-claims/"),
        ("Smoke Odor Claims", "/smoke-odor-claims/"),
        ("Contents Claims", "/smoke-damaged-contents/"),
        ("HVAC Smoke Damage", "/hvac-smoke-damage/"),
        ("Residential Claims", "/residential-smoke-damage-claims/"),
        ("Commercial Claims", "/commercial-smoke-damage-claims/"),
        ("Denied Claims", "/denied-smoke-damage-claims/"),
        ("Underpaid Claims", "/underpaid-smoke-damage-claims/"),
        ("Delayed Claims", "/delayed-smoke-damage-claims/"),
        ("Our Claim Process", "/smoke-damage-claim-process/"),
    ]),
    ("Tools", "/tools/", [
        ("Smoke Damage Scope Calculator", "/tools/smoke-damage-scope-calculator/"),
        ("Contents RCV/ACV Calculator", "/tools/contents-rcv-acv-calculator/"),
    ]),
    ("Texas Areas", "/texas/", None),
    ("Resources", "/blog/", [
        ("Texas Fire & Smoke Events", "/texas-fire-smoke-events/"),
        ("Texas Fire & Smoke History", "/texas-fire-smoke-history/"),
        ("Texas Public Adjuster Rules", "/texas-public-adjuster-rules/"),
        ("Texas Public Adjuster", "/texas-smoke-damage-public-adjuster/"),
        ("FAQ", "/faq/"),
        ("Blog", "/blog/"),
    ]),
    ("About", "/about/", None),
    ("Contact", "/contact/", None),
]

FOOTER_LINKS = [
    ("Smoke Damage Claims", "/smoke-damage-claims/"),
    ("Fire Damage Claims", "/fire-damage-claims/"),
    ("Soot Claims", "/soot-damage-claims/"),
    ("Contents Claims", "/smoke-damaged-contents/"),
    ("Commercial Claims", "/commercial-smoke-damage-claims/"),
    ("Texas Areas", "/texas/"),
    ("Calculators", "/tools/"),
    ("Texas Fire & Smoke Events", "/texas-fire-smoke-events/"),
    ("Blog", "/blog/"),
    ("About", "/about/"),
    ("Contact", "/contact/"),
    ("Privacy Policy", "/privacy-policy/"),
    ("Terms of Use", "/terms-of-use/"),
    ("Disclaimer", "/disclaimer/"),
    ("Sitemap", "/sitemap/"),
]

# Homepage "Texas statewide" markets. (name, slug-or-None, lng, lat) - a slug
# links to /texas/<slug>/ when that page exists.
MARKETS = [
    "Houston", "Dallas", "Fort Worth", "Austin", "San Antonio", "El Paso", "Corpus Christi",
    "Beaumont", "Port Arthur", "Waco", "Killeen", "Temple", "Lubbock", "Amarillo", "Midland",
    "Odessa", "McAllen", "Edinburg", "Brownsville", "Harlingen", "Laredo", "College Station",
    "Bryan", "Tyler", "Longview", "Galveston", "Pearland", "Sugar Land", "Katy",
    "The Woodlands", "Round Rock", "Georgetown", "New Braunfels", "San Marcos", "Arlington",
    "Plano", "Frisco", "McKinney", "Irving", "Garland",
]

TODAY = date.today().isoformat()
