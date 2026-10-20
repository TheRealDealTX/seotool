"""Set the <title> of individual posts in content/ (index and post file).

    python3 _build/set_titles.py
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
TITLES = {
    "best-agricultural-practices-to-avoid-sweet-potato-weevil-infestation": "Sweet Potato Weevil: How to Prevent an Infestation",
    "farm-kitchen-cooking-equipment-guide": "Farm Kitchen Cooking Equipment: A First-Timer's Guide",
    "cattle-handling-equipment-tips": "Cattle Handling Equipment Tips for Safer Ranch Work",
    "create-an-efficient-garden-shed-workspace-for-sustainable-growing": "How to Set Up an Efficient Garden Shed Workspace",
    "the-modern-guide-to-cattle-handling-equipment-that-actually-works": "The Modern Guide to Cattle Handling Equipment",
    "growing-garlic-at-home-beginners-guide-to-planting-harvesting": "Growing Garlic at Home: Planting, Harvesting & Storing",
    "revolutionizing-farming-sustainable-chemical-free-eco-friendly-agriculture-technology": "How Technology Supports Chemical-Free Farming",
    "no-cook-recipes-are-perfect-for-beginner": "No-Cook Recipes for Beginner Cooks and Small Kitchens",
    "chicken-brining": "Chicken Brine Ratio: Best Salt-to-Water Ratio & Salt Types",
    "goat-pregnancy": "Goat Pregnancy: Gestation Length, Signs & Due Date Calculator",
    "bernat-handicrafter-cotton-yarn": "Bernat Handicrafter Cotton Yarn for Kitchen Dish Cloths",
    "what-to-do-with-a-rooster": "What to Do With a Rooster: Keep, Rehome or Process?",
}
PAT = re.compile(r"(<<<'PWFJSON'\n)(.*)(\nPWFJSON, true\);)", re.S)


def edit(path, fn):
    src = open(path, encoding="utf-8").read()
    m = PAT.search(src)
    data = fn(json.loads(m.group(2)))
    blob = json.dumps(data, ensure_ascii=False, indent=1)
    open(path, "w", encoding="utf-8").write(src[:m.start(2)] + blob + src[m.end(2):])


def set_index(d):
    for slug, t in TITLES.items():
        d[slug]["title"] = t
    return d


def set_post(t):
    def fn(d):
        d["title"] = t
        return d
    return fn


edit(os.path.join(ROOT, "content/index.php"), set_index)
for slug, t in TITLES.items():
    assert len(t) <= 65, (slug, len(t))
    edit(os.path.join(ROOT, "content/posts", slug + ".php"), set_post(t))
print(f"updated {len(TITLES)} titles")
