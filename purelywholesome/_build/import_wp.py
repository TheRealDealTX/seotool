"""One-time importer: WordPress scrape -> PHP content files.

Reads the JSON produced by scraping the old WordPress site (one entry per URL
with title, meta description, dates, category and the post-content HTML) and
writes, for every post:

    content/posts/<slug>.php    <?php return [...meta..., 'html' => ..., 'faq' => [...]];

plus content/index.php, the metadata for every post without the body, which the
site uses for listings, related posts, search, feeds and sitemaps.

    python3 _build/import_wp.py <scraped posts.json> <site root>

Cleaning applied to every post:
  * WordPress/Elementor classes, srcset, inline styles and stray forms/scripts removed
  * headings get stable ids; an in-content <h1> is demoted to <h2>
  * Yoast FAQ blocks become structured Q&A (rendered as an accordion + FAQPage schema)
  * absolute internal links become root-relative and are pointed at their final URL
  * external links get rel="noopener"; links in sponsored posts get rel="sponsored nofollow"
  * images get width/height, lazy loading and async decoding
"""

import json
import os
import re
import sys
from datetime import date

from bs4 import BeautifulSoup, NavigableString
from PIL import Image

ORIGIN = "https://purelywholesome.com"
TODAY = date.today().isoformat()

# Posts that are off-topic for a farm & homestead kitchen site: paid guest posts,
# link placements and generic lifestyle filler published from Nov 2025 onward.
# Their URLs stay live (no 404s), but they are noindexed, dropped from listings,
# sitemaps and search, and every outbound link is marked rel="sponsored nofollow".
OFF_TOPIC = {
    "diy-vs-pro-in-home-renovations", "amandahornby", "home-organization-hacks", "home-decor-ideas",
    "diy-home-projects", "family-relationships", "life-style-tips", "diys-for-moms",
    "design-and-business-lifestyle", "home-lighting-ideas", "self-improvement-tips", "creativity-lifestyle",
    "personalized-decorations", "home-improvements-that-add-real-value",
    "using-peel-and-stick-wallpaper-on-your-homestead", "3-easy-ways-to-sell-your-home-faster",
    "5-lazy-bathroom-fixes-that-deliver-instant-luxury", "dundee-decos-faux-brick-wall-panels",
    "3-effortless-ways-to-design-timeless-rustic-rooms", "5-essential-fixes-for-self-running-homes",
    "lazy-morning-habits-for-effortless-gut-balance", "safety-tips-every-user-should-know-before-using-crimp-tools",
    "luxury-bedding-quilts-elevating-comfort-with-timeless-design", "roll-up-garage-doors-a-practical-guide-for-homeowners",
    "hidden-health-risks-of-untreated-hearing-loss-and-why-early-care-matters",
    "renting-a-room-can-support-a-more-sustainable-and-intentional-lifestyle",
    "pro-level-welding-equipment-brands-for-home-improvement-projects",
    "how-can-health-conscious-people-enjoy-house-parties-this-season",
    "contractor-businesses-look-for-in-insurance-providers", "families-concerned-about-microplastics",
    "crucial-tips-for-installation-and-sealing-your-multiwall-roofing", "little-details-that-make-an-outfit-feel-like-you",
    "boost-productivity-for-contractors-and-councils", "truth-about-dog-supplements",
    "trusted-suppliers-of-concrete-barriers-for-infrastructure-projects",
    "benefits-of-using-food-grade-silicone-for-custom-molds-creation",
    "why-great-signage-generates-foot-traffic-without-advertising-spend", "how-much-heat-do-fire-tables-produce-for-patios",
    "proven-benefits-of-hiring-a-professional-rat-removal-service", "floor-leveling-tampa",
    "how-to-price-your-flooring-project-in-60-seconds", "5-kitchen-cabinet-suppliers-in-houston-for-commercial-properties",
    "personal-and-commercial-banking-services", "why-premium-ugandan-green-coffee-is-gaining-global-attention",
    "best-mold-inspection-companies-in-texas-for-same-day-assessments", "how-often-to-service-home-appliances",
    "what-are-landscaping-services", "plant-sourcing-explained", "how-long-does-roof-replacement-take",
    "wholesale-plant-sourcing", "how-to-use-a-dji-matrice-4t-drone-for-farm-surveys", "goat-farm-wedding",
}

# On-topic posts that carry vendor placements: indexable, but links are sponsored.
SPONSORED_LINKS = {
    "the-modern-guide-to-cattle-handling-equipment-that-actually-works", "cattle-handling-equipment-tips",
    "cattle-handling-equipment-maintenance-checklist", "plan-cattle-handling-system",
    "cattle-handling-equipment-every-farm-should-have", "which-cream-separator-works-best-for-small-scale-dairy-farms",
    "right-farm-boots-for-work-safety", "farm-kitchen-cooking-equipment-guide", "led-grow-lights-vs-fluorescent-vs-hps",
    "create-an-efficient-garden-shed-workspace-for-sustainable-growing",
    "revolutionizing-farming-sustainable-chemical-free-eco-friendly-agriculture-technology",
    "what-makes-a-chicken-coop-suitable-for-all-seasons", "where-wagyu-cows-come-from",
}

# Old URLs that already redirected (or should) to a live post.
LEGACY = {
    "best-sauce-for-lamb-chops-from-classic-mint-to-bold-tomato": "best-sauce-for-lamb-chops",
    "brine-a-chicken-for-juicy-flavorful-poultry": "how-to-brine-a-chicken",
    "brine-brisket": "how-to-brine-your-own-brisket",
    "canning/citric-acid-for-canning": "citric-acid-for-canning",
    "citric-acid-for-canning-way-to-keep-salsa-and-pickles-safe": "citric-acid-for-canning",
    "food/how-to-store-farm-fresh-eggs": "farm-fresh-eggs",
    "how-to-keep-water-from-freezing": "how-to-keep-livestock-water-from-freezing",
    "nutritional-value-of-lamb-per-serving": "nutritional-value-of-lamb-chops-per-serving",
    "purely-wholesome-nutritional-yeast-recipes": "nutritional-yeast-recipes",
    "what-to-do-with-roosters": "what-to-do-with-a-rooster",
    "growing-garlic-at-home": "growing-garlic-at-home-beginners-guide-to-planting-harvesting",
}

# Links to these are dropped (the anchor text stays): retired off-topic posts and WP admin URLs.
UNLINK = re.compile(r"^/(wp-admin|choose-the-right-camlock-hose-fittings-for-your-water-pumping-system)(/|$)")

# Hand-edited titles, H1s, descriptions and headings for the pages that carried
# the site's search traffic. Titles target the queries each page actually ranked
# for in Search Console (several sat at position 2-4 with a 0.3-0.9% CTR).
OVERRIDES = {
    "sides-for-lamb-chops": dict(
        title="What to Serve with Lamb Chops: The Best Sides for Every Season",
        h1="Sides for Lamb Chops: My Go-To Pairings That Always Impress",
        desc="The best sides for lamb chops, from garlic-herb potatoes and minted peas to summer salads, with sample menus and an interactive plate builder."),
    "pumpkin-pie-filling": dict(
        title="Watery Pumpkin Pie Filling? Why It Happens and How to Fix It",
        h1="Pumpkin Pie Filling Too Watery? How to Fix It for a Silky, Set Pie",
        desc="Why pumpkin pie filling turns watery and how to fix it: reduce the puree, blind-bake the crust, bake low and slow, and test for doneness the right way."),
    "best-sauce-for-lamb-chops": dict(
        title="Best Sauce for Lamb Chops: Mint, Tomato & Pan Sauces Compared",
        h1="The Best Sauce for Lamb Chops: From Classic Mint to Bold Tomato",
        desc="The best sauce for lamb chops, compared: bright mint sauce, rich tomato, mint-tomato and quick pan sauces, with when to use each one.",
        headings={"Tomato Sauce": "Tomato Sauce: Bold and Comforting",
                  "Mint Sauce": "Mint Sauce: The Fresh Classic",
                  "Lamb Recipe": "Building a Complete Lamb Dinner Around the Sauce",
                  "Lamb Chops": "How I Cook the Chops Themselves",
                  "Lamb Chops Sauce": "Quick Pan Sauces for Lamb Chops",
                  "Mint Tomato Sauce": "Mint-Tomato Sauce: The Best of Both",
                  "Best Sauce for Lamb Chops": "My Verdict: Which Sauce Is Best?"}),
    "how-to-brine-a-chicken": dict(
        title="How to Brine a Chicken: Salt Ratio, Times & Step-by-Step Method",
        h1="How to Brine a Chicken for Juicy, Flavorful Poultry",
        desc="How to brine a chicken: the salt-to-water ratio, how long to brine each cut, and the rinse-and-dry steps for crisp skin. Includes a free brine calculator.",
        headings={"Salt Brine Chicken": "Getting the Salt Right",
                  "Brine Chicken": "The Three Essentials: Salt, Time and Temperature",
                  "Chicken Brine Recipe": "My Kosher Salt Chicken Brine Recipe"}),
    "how-to-brine-your-own-brisket": dict(
        title="How to Brine Brisket: Recipe, Brine Time & Corned Beef Method",
        desc="How to brine brisket at home: a simple brisket brine recipe, how long to brine, the corned beef variation and how to cook it after brining."),
    "what-to-do-with-a-rooster": dict(
        title="What to Do With a Rooster: Keep, Rehome or Process?",
        h1="What to Do With a Rooster: Lessons from My Backyard Flock",
        desc="What to do with a rooster you didn't plan on: how to handle an aggressive rooster, rehoming options, keeping one with your hens, and rooster vs hen differences."),
    "how-to-keep-livestock-water-from-freezing": dict(
        title="How to Keep Livestock Water from Freezing: 6 Winter Methods",
        desc="How to keep livestock water from freezing in winter: heated buckets, frost-free hydrants, insulated holders, trough de-icers and low-power tricks that work."),
    "frozen-eggs-for-dinner": dict(
        title="Can You Eat Eggs That Froze? Thawing & Cooking Frozen Eggs",
        h1="Frozen Eggs: Are They Safe, and How to Cook With Them",
        desc="Eggs froze in the coop or fridge? Here's when frozen eggs are safe to eat, how to thaw them, and the quiches, pies and skillet recipes they work best in."),
    "best-brining-container": dict(
        title="Best Brining Container for Chicken & Turkey (Food-Safe Options)",
        desc="The best brining containers for chicken and turkey: food-grade buckets, brining bags, stainless pots and what to use instead when you don't have one."),
    "over-brined-chicken": dict(
        title="Over Brined Chicken: Signs, How to Fix It & Safe Brine Times",
        desc="Brined your chicken too long? How to tell, how to fix over brined chicken, and safe brining times for every cut so it stays juicy rather than salty."),
    "chicken-brining": dict(
        title="Chicken Brine Ratio: Best Salt-to-Water Ratio & Salt Types",
        h1="Chicken Brining: Finding the Best Salt Ratio for Chicken Brine",
        desc="The best salt-to-water ratio for chicken brine, how different salts measure up, and my step-by-step brining process. Includes a brine calculator."),
    "pan-seared-lamb-chops": dict(
        title="Pan Seared Lamb Chops: Easy Recipe, Temps & Timing",
        desc="Juicy pan seared lamb chops in under 20 minutes: ingredients, the right pan temperature, internal temps for each doneness and what to serve alongside."),
    "cheddar-substitute": dict(
        title="Cheddar Cheese Powder Substitute: Easy Homemade Options",
        desc="Homemade cheddar cheese powder substitutes for popcorn, fries and mac and cheese, plus how to dehydrate your own cheese powder at home."),
    "farm-fresh-eggs": dict(
        title="How Long Do Farm Fresh Eggs Last? Storage, Float Test & Egg Bloom",
        h1="Farm Fresh Eggs: How I Store, Test and Preserve Every Egg",
        desc="How long farm fresh eggs last on the counter and in the fridge, how the egg bloom works, the float test, freezing eggs and spotting a bad egg.",
        headings={"Cooked Eggs": "How Long Cooked Eggs Last", "Egg Expiration": "Do Farm Eggs Expire?",
                  "Hard Boiled Eggs": "Hard Boiling Farm Fresh Eggs", "Freezing Eggs": "Freezing Extra Eggs",
                  "Fridge Temperature": "The Right Fridge Temperature", "Egg Carton": "Why the Carton Matters",
                  "Raw Eggs": "Raw Eggs and Freshness", "Egg Shelf Life": "Egg Shelf Life at a Glance",
                  "Egg Storage": "My Egg Storage Routine", "Rotten Eggs": "How to Spot a Rotten Egg",
                  "Egg Bloom": "What the Egg Bloom Does", "Unwashed Eggs": "Storing Unwashed Eggs"}),
    "how-to-sterilize-mason-jars-for-canning": dict(
        title="How to Sterilize Mason Jars for Canning (Boil, Oven & Steam)",
        desc="How to sterilize mason jars for canning by boiling, steaming or in the oven, when you actually need to, and the mistakes that cause seals to fail."),
    "goat-pregnancy": dict(
        title="Goat Pregnancy: Gestation Length, Signs & Due Date Calculator",
        desc="Goat pregnancy from breeding to birth: how long goats are pregnant, signs of pregnancy and labor, care by stage, and a due date calculator."),
    "sweet-pickle-recipe": dict(
        title="Old-Fashioned Sweet Pickle Recipe (Crisp, Canned or Fridge)",
        desc="An old-fashioned sweet pickle recipe with a safe vinegar ratio, a warm spice blend and tips for crisp pickles, canned or as refrigerator pickles."),
    "goat-temperature": dict(
        title="Normal Goat Temperature: What's Normal, Fever & Hypothermia Signs",
        desc="Normal goat temperature is about 101.5-103.5°F. How to take a goat's temperature, what a fever or low reading means, and when to call the vet."),
    "scours-in-goats": dict(
        title="Scours in Baby Goats: Causes and How to Treat Them",
        desc="How to treat scours in baby goats: common causes, electrolytes and hydration, when it's an emergency, and how to prevent scours in your kids."),
    "signs-of-worms-in-goats": dict(
        title="Signs of Worms in Goats: Symptoms, FAMACHA & Treatment",
        desc="Signs of worms in goats, from pale eyelids and bottle jaw to weight loss, how to check with FAMACHA and fecal tests, and what to do about it."),
    "citric-acid-for-canning": dict(
        title="Citric Acid for Canning: How Much to Use in Tomatoes & Salsa",
        desc="How much citric acid to use when canning tomatoes, salsa and pickles, why acidity matters for safety, and how it compares with lemon juice."),
    "fertilized-vs-unfertilized-eggs": dict(
        title="Fertilized vs Unfertilized Eggs: How to Tell and Does It Matter?",
        desc="Fertilized vs unfertilized eggs: how to tell them apart, whether they taste different, and how to store and eat eggs from a flock with a rooster."),
    "pumpkin-pie-spices": dict(
        title="Pumpkin Pie Spice Ratio: The Best Homemade Blend",
        desc="The best pumpkin pie spice ratio: cinnamon, ginger, nutmeg, cloves and allspice in balance, plus how much to use per pie."),
    "nutritional-value-of-lamb-chops-per-serving": dict(
        title="Lamb Chop Nutrition: Calories & Protein Per Serving",
        desc="Nutritional value of lamb chops per serving: calories, protein, fat, iron and B12, and how cooking method and trimming change the numbers."),
    "lamb-chops-marinade": dict(
        title="Lamb Chops Marinade: Easy Recipes for Juicy, Flavor-Packed Chops",
        desc="Lamb chops marinade recipes with garlic, rosemary, lemon and yogurt, how long to marinate, and how to cook marinated chops without burning them."),
    "lamb-gravy-turning-every-roast-into-magic": dict(
        title="Lamb Gravy from Pan Drippings: Easy Recipe for Roast Lamb",
        h1="Lamb Gravy: Turning Every Roast into Magic",
        desc="How to make lamb gravy from pan drippings: deglazing, thickening, seasoning and fixing lumpy or thin gravy for roast lamb."),
}

TOPICS = [  # (slug, label, slug-keyword patterns) - first match wins
    ("brining", "Brining", r"brin"),
    ("lamb", "Lamb Recipes", r"lamb|mint-sauce|mint-tomato|romesco|basting|carve|roastedleg"),
    ("goats", "Raising Goats", r"goat|scours|pasture-management|pygmy|nubian|alpine|boer|kidding|cdt-vacc|postpartum|bottle-jaw"),
    ("chickens-eggs", "Chickens & Eggs", r"egg|chick|rooster|coop|hens|poultry|molting|layer"),
    ("canning", "Canning & Preserving", r"cann|mason-jar|pickle|salsa|applesauce|water-bath|safe-storage|citric|tomato-sauce|peaches|stockpile"),
    ("baking", "Pumpkin, Pies & Baking", r"pumpkin|pie|sourdough|bread|blind-baking|cracker|dough|dessert|frosting|bars|thanksgiving|toast-nuts|edible-gifts|maple|syrup|cheddar|nutritional-yeast|pizza|charcuterie|holiday-snacks|chai"),
    ("homestead", "Homestead & Garden", r"beet|garlic|dandelion|grow|plant|weevil|shed|cattle|wagyu|boots|separator|farming|leaving-the-farm|tranquil|kitchen-cooking|five-things"),
    ("crafts", "Farmhouse Crafts", r"cloth|towel|yarn|knit|crochet|clean-pans|wreath|fabric"),
]
TOPIC_LABEL = {t[0]: t[1] for t in TOPICS}


def topic_for(slug, sections):
    for key, _, pat in TOPICS:
        if re.search(pat, slug):
            return key
    return "kitchen" if "Recipes" in sections else "homestead"


TOPIC_LABEL["kitchen"] = "From the Farm Kitchen"

# Interactive tools surfaced inside posts (rendered by app/tools/*.php).
TOOLS_BY_TOPIC = {
    "brining": ["brine-calculator"], "lamb": ["lamb-cooking-calculator"], "goats": ["goat-temperature-checker"],
    "chickens-eggs": ["egg-production-planner"], "canning": ["canning-altitude-adjuster"],
    "baking": ["recipe-scaler"], "kitchen": ["recipe-scaler"],
}
TOOLS_BY_SLUG = {
    "sides-for-lamb-chops": ["lamb-sides-builder", "lamb-cooking-calculator"],
    "roast-lamb-side-dishes": ["lamb-sides-builder"],
    "pumpkin-pie-filling": ["pumpkin-pie-troubleshooter"], "perfect-pumpkin-pie": ["pumpkin-pie-troubleshooter"],
    "homemade-pumpkin-pie": ["pumpkin-pie-troubleshooter"], "pumpkin-pie-recipe": ["pumpkin-pie-troubleshooter"],
    "dairy-free-pumpkin-pie": ["pumpkin-pie-troubleshooter"], "blind-baking": ["pumpkin-pie-troubleshooter"],
    "goat-pregnancy": ["goat-gestation-calculator"], "goat-pregnancy-1": ["goat-gestation-calculator"],
    "goat-kidding": ["goat-gestation-calculator"], "preparing-for-kidding-season": ["goat-gestation-calculator"],
    "goat-birthing-kit": ["goat-gestation-calculator"], "postpartum-goat-care-after-birth": ["goat-gestation-calculator"],
    "goat-colostrum": ["goat-gestation-calculator"], "goat-udder": ["goat-gestation-calculator"],
    "how-to-brine-your-own-brisket": ["brine-calculator"],
    "how-to-keep-livestock-water-from-freezing": ["egg-production-planner"],
}


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60].rstrip("-") or "section"


def local_path(url):
    """https://purelywholesome.com/x/ -> /x/ ; leaves anything else alone."""
    if url.startswith(ORIGIN):
        url = url[len(ORIGIN):] or "/"
    m = re.match(r"^/([^?#]*?)/?([?#].*)?$", url)
    if m and not url.startswith("/wp-content/"):
        path = m.group(1)
        path = LEGACY.get(path, path)
        url = "/" + (path + "/" if path else "") + (m.group(2) or "")
    return url


def optimized(root, src):
    """Large uploads get a resized WebP copy under /wp-content/uploads/optimized/ for
    display; the original stays at its old URL so nothing indexed breaks."""
    if not src.startswith("/wp-content/uploads/") or src.startswith("/wp-content/uploads/optimized/"):
        return src
    path = os.path.join(root, src.lstrip("/"))
    if not os.path.exists(path) or os.path.getsize(path) <= 250_000:
        return src
    rel = src[len("/wp-content/uploads/"):]
    out_rel = "/wp-content/uploads/optimized/" + os.path.splitext(rel)[0] + ".webp"
    out = os.path.join(root, out_rel.lstrip("/"))
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with Image.open(path) as im:
            im = im.convert("RGB")
            if im.width > 1400:
                im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
            im.save(out, "WEBP", quality=80, method=6)
    return out_rel


def img_size(root, src):
    try:
        with Image.open(os.path.join(root, src.lstrip("/"))) as im:
            return im.size
    except Exception:
        return None


def clean(html, slug, root, sponsored, headings_map):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup.find_all(["script", "style", "form", "input", "button", "label", "textarea", "noscript"]):
        t.decompose()
    for t in soup.find_all(class_=re.compile(r"^(ccc-|elementor)")):
        if t.parent is not None:
            t.decompose()

    # Yoast FAQ block -> structured data; drop the block and its "FAQs" heading.
    faq = []
    for block in soup.select(".schema-faq"):
        for sec in block.select(".schema-faq-section"):
            q = sec.select_one(".schema-faq-question")
            a = sec.select_one(".schema-faq-answer")
            if q and a:
                for br in a.find_all("br"):
                    br.decompose()
                faq.append({"q": q.get_text(" ", strip=True), "a": a.decode_contents().strip()})
        prev = block.find_previous_sibling()
        if prev is not None and prev.name in ("h2", "h3") and re.match(r"^\s*(faqs?|faq.s|frequently asked)", prev.get_text(strip=True), re.I):
            prev.decompose()
        block.decompose()

    used = set()
    for h in soup.find_all(["h1", "h2", "h3", "h4"]):
        if h.name == "h1":
            h.name = "h2"
        text = h.get_text(" ", strip=True)
        if text in headings_map:
            h.clear()
            h.append(headings_map[text])
            text = headings_map[text]
        hid = slugify(text)
        while hid in used:
            hid += "-2"
        used.add(hid)
        h.attrs = {"id": hid}

    for img in soup.find_all("img"):
        src = optimized(root, local_path(img.get("src", "")))
        alt = img.get("alt", "").strip()
        alt = re.sub(r"\s+\d+$", "", alt) if alt else ""
        attrs = {"src": src, "alt": alt or soup_title_fallback(slug), "loading": "lazy", "decoding": "async"}
        size = img_size(root, src)
        if size:
            attrs["width"], attrs["height"] = str(size[0]), str(size[1])
        img.attrs = attrs
    for fig in soup.find_all("figure"):
        if fig.find("table"):
            fig.name = "div"
            fig.attrs = {"class": "table-wrap"}
        else:
            fig.attrs = {}
    for table in soup.find_all("table"):
        table.attrs = {}
        if table.parent.name != "div" or "table-wrap" not in table.parent.get("class", []):
            table.wrap(soup.new_tag("div", attrs={"class": "table-wrap"}))

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if not href:
            a.unwrap()
            continue
        href = local_path(href)
        if UNLINK.match(href):
            a.unwrap()
            continue
        attrs = {"href": href}
        if href.startswith("http"):
            host = href.split("/")[2]
            rel = ["noopener"]
            if sponsored or "amzn.to" in host or "amazon." in host:
                rel = ["sponsored", "nofollow", "noopener"]
            attrs["rel"] = " ".join(rel)
            attrs["target"] = "_blank"
        a.attrs = attrs

    keep_class = {"table-wrap"}
    for t in soup.find_all(True):
        if t.name in ("a", "img") or t.name.startswith("h"):
            continue
        cls = [c for c in t.get("class", []) if c in keep_class]
        t.attrs = {"class": cls} if cls else {}
        if t.name == "div" and not cls and t.find(True) is None and not t.get_text(strip=True):
            t.decompose()
    for t in soup.find_all(["div", "span"]):
        if not t.attrs:
            t.unwrap()
    for p in soup.find_all("p"):
        if not p.get_text(strip=True) and not p.find("img"):
            p.decompose()

    out = str(soup)
    out = re.sub(r"\n{2,}", "\n", out).replace("\xa0", " ").strip()
    return out, faq


_titles = {}


def soup_title_fallback(slug):
    return _titles.get(slug, slug.replace("-", " "))


def excerpt_from(html, n=170):
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0]
    return cut.rstrip(",;:—-") + "…"


def php_file(data):
    blob = json.dumps(data, ensure_ascii=False, indent=1)
    assert "\nPWFJSON" not in blob
    return "<?php\nreturn json_decode(<<<'PWFJSON'\n" + blob + "\nPWFJSON, true);\n"


def main(src, root):
    raw = json.load(open(src, encoding="utf-8"))
    os.makedirs(os.path.join(root, "content/posts"), exist_ok=True)
    index = {}
    os.makedirs(os.path.join(root, "content/pages"), exist_ok=True)
    for key in ("privacy-policy", "terms-of-use"):
        html, _ = clean(raw[key]["content"], key, root, False, {})
        with open(os.path.join(root, "content/pages", key + ".php"), "w", encoding="utf-8") as f:
            f.write(php_file({"title": raw[key]["h1"], "desc": raw[key]["desc"], "html": html}))
    for key, d in raw.items():
        if not d.get("published") or "__" in key:
            continue
        slug = key
        title = re.sub(r"\s*\|\s*Purely Wholesome Farm\s*$", "", d["title"]).strip()
        _titles[slug] = d["h1"] or title
        ov = OVERRIDES.get(slug, {})
        sponsored = slug in OFF_TOPIC or slug in SPONSORED_LINKS
        html, faq = clean(d["content"], slug, root, sponsored, ov.get("headings", {}))
        thumb = local_path(d.get("thumb") or d.get("og_image") or "")
        if thumb and not os.path.exists(os.path.join(root, thumb.lstrip("/"))):
            thumb = ""
        thumb = optimized(root, thumb) if thumb else ""
        tsize = img_size(root, thumb) if thumb else None
        words = len(BeautifulSoup(html, "html.parser").get_text(" ").split()) + sum(len(BeautifulSoup(f["a"], "html.parser").get_text(" ").split()) for f in faq)
        topic = topic_for(slug, d.get("section", []))
        tools = TOOLS_BY_SLUG.get(slug) or TOOLS_BY_TOPIC.get(topic, [])
        if slug in OFF_TOPIC:
            tools = []
        title = re.sub(r":(?=\S)", ": ", ov.get("title", title))
        meta = {
            "slug": slug,
            "title": title,
            "h1": re.sub(r":(?=\S)", ": ", ov.get("h1", d["h1"] or title)),
            "desc": ov.get("desc", d.get("desc") or excerpt_from(html, 155)),
            "excerpt": excerpt_from(html),
            "published": d["published"][:10],
            "modified": TODAY if ov else (d.get("modified") or d["published"])[:10],
            "categories": [c for c in d.get("section", [])] or ["General"],
            "topic": topic,
            "image": thumb,
            "image_w": tsize[0] if tsize else 0,
            "image_h": tsize[1] if tsize else 0,
            "words": words,
            "minutes": max(2, round(words / 230)),
            "indexable": slug not in OFF_TOPIC,
            "sponsored": sponsored,
            "tools": tools,
        }
        index[slug] = meta
        with open(os.path.join(root, "content/posts", slug + ".php"), "w", encoding="utf-8") as f:
            f.write(php_file({**meta, "html": html, "faq": faq}))

    # Related posts: same topic first, then shared title words; indexable only.
    def words_of(m):
        return {w for w in re.findall(r"[a-z]{4,}", (m["title"] + " " + m["slug"]).lower())}
    live = [m for m in index.values() if m["indexable"]]
    for m in index.values():
        mw = words_of(m)
        scored = sorted(
            (o for o in live if o["slug"] != m["slug"]),
            key=lambda o: (-(3 if o["topic"] == m["topic"] else 0) - len(mw & words_of(o)), o["slug"]))
        m["related"] = [o["slug"] for o in scored[:4]]
    ordered = dict(sorted(index.items(), key=lambda kv: (kv[1]["published"], kv[0]), reverse=True))
    with open(os.path.join(root, "content/index.php"), "w", encoding="utf-8") as f:
        f.write(php_file(ordered))
    print(f"posts={len(index)} indexable={len(live)} noindex={len(index) - len(live)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
