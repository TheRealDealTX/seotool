#!/usr/bin/env python3
"""Build the one-time migration data from the old WordPress site.

Reads the public WordPress REST API of https://rodeotexas.org (before cutover)
and writes three JSON files into app/data/:

  articles.json        21 blog posts (content, SEO title/description, image)
  legacy_events.json   old Events Calendar events that are verifiably in Texas
  redirects.json       301 map for every old URL that does not survive as-is

Usage:  python3 tools/build_migration_data.py [--audit-dir DIR]

Only the Python standard library is used. Already run once; the generated
files are committed, so this is kept for audit/reproducibility only (the
WordPress API will be gone after cutover).
"""
import argparse
import glob
import html
import json
import os
import re
import urllib.request

SITE = "https://rodeotexas.org"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "app", "data")
UA = {"User-Agent": "Mozilla/5.0 (compatible; RodeoTexasMigration/1.0)"}

# Legacy event title fragment -> Texas city (None = Texas, city not stated).
# Only rodeos whose Texas location is well established are listed. Anything
# not matched here is treated as non-Texas / unverifiable and redirected.
TEXAS_EVENTS = [
    ("Amarillo Tri", "Amarillo"), ("Angelina Benefit", "Lufkin"),
    ("Bandera", "Bandera"), ("Bellville", "Bellville"), ("Belton", "Belton"),
    ("Big Spring", "Big Spring"), ("Brazoria County Fair", "Angleton"),
    ("Coleman", "Coleman"), ("Comal County Fair", "New Braunfels"),
    ("Corpus Christi", "Corpus Christi"),
    ("Cowboy Capital Of The World PRCA", "Stephenville"),
    ("Crockett Lions", "Crockett"), ("Decatur PRCA", "Decatur"),
    ("East Texas State Fair", "Tyler"), ("Ellis County Livestock", None),
    ("Fort Bend County Fair", "Rosenberg"), ("Fort Worth", "Fort Worth"),
    ("Southwestern Exposition", "Fort Worth"), ("Stockyard", "Fort Worth"),
    ("Gaines County Riding Club", "Seminole"), ("Gladewater", "Gladewater"),
    ("Goliad County Fair", "Goliad"), ("Guadalupe County Fair", "Seguin"),
    ("Heart O", "Waco"), ("Helotes", "Helotes"), ("Hempstead", "Hempstead"),
    ("Henderson County First Responders", "Athens"),
    ("Hood County Stampede", "Granbury"),
    ("Johnson County Sheriff", "Cleburne"), ("Liberty Hill", "Liberty Hill"),
    ("Longview PRCA", "Longview"), ("Mesquite Championship", "Mesquite"),
    ("Mt Pleasant", "Mount Pleasant"), ("Mt. Pleasant", "Mount Pleasant"),
    ("Nacogdoches", "Nacogdoches"), ("North Texas Fair", "Denton"),
    ("Panola County Cattlemen", "Carthage"), ("Parker County Sheriff", "Weatherford"),
    ("Pasadena Livestock", "Pasadena"), ("Rio Grande Valley Livestock", "Mercedes"),
    ("Rodeo Austin", "Austin"), ("Rodeo Celina", "Celina"),
    ("Rodeo El Paso", "El Paso"), ("Rodeo Killeen", "Killeen"),
    ("Rosenberg", "Rosenberg"), ("San Angelo", "San Angelo"),
    ("San Antonio", "San Antonio"), ("Stephenville", "Stephenville"),
    ("Texas Circuit Finals", None), ("Tops In Texas", "Jacksonville"),
    ("Tops in Texas", "Jacksonville"), ("Waco Permit", "Waco"),
    ("Walker County Fair", "Huntsville"), ("West Of The Pecos", "Pecos"),
    ("West of the Pecos", "Pecos"), ("West Texas Fair", "Abilene"),
    ("Wharton County Youth Fair", "Wharton"), ("Wichita Falls", "Wichita Falls"),
    ("XIT Rodeo", "Dalhart"), ("ABC Pro Rodeo", "Lubbock"),
    ("George Paul Memorial", "Del Rio"),
]
# Official links that the old site attached indiscriminately (not the event's site).
BAD_LINKS = {"https://www.banderaprorodeo.org/"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def texas_city(title):
    for frag, city in TEXAS_EVENTS:
        if frag.lower() in title.lower():
            return True, city
    return False, None


def clean_content(c):
    c = c.replace(SITE + "/", "/")
    c = re.sub(r'\s(fetchpriority|decoding)="[^"]*"', "", c)
    c = re.sub(r"<img ", '<img loading="lazy" decoding="async" ', c)
    return c.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-dir", help="reuse downloaded JSON instead of the live API")
    a = ap.parse_args()
    os.makedirs(DATA, exist_ok=True)

    # ---- articles
    if a.audit_dir:
        posts = json.load(open(os.path.join(a.audit_dir, "posts_embed.json")))
        meta = json.load(open(os.path.join(a.audit_dir, "post_meta.json")))
        cats = json.load(open(os.path.join(a.audit_dir, "cats.json")))
    else:
        posts = json.loads(get(SITE + "/wp-json/wp/v2/posts?per_page=100&_embed=1"))
        cats = json.loads(get(SITE + "/wp-json/wp/v2/categories?per_page=100"))
        meta = []
        for p in posts:
            h = get(p["link"])
            t = re.search(r"<title>(.*?)</title>", h, re.S)
            d = re.search(r'<meta name="description" content="([^"]*)"', h)
            fm = (p.get("_embedded", {}).get("wp:featuredmedia") or [{}])[0]
            md = fm.get("media_details") or {}
            meta.append(dict(seo_title=html.unescape(t.group(1)).strip() if t else None,
                             meta_description=html.unescape(d.group(1)) if d else None,
                             featured=fm.get("source_url"), featured_alt=fm.get("alt_text"),
                             fw=md.get("width"), fh=md.get("height")))
    cat_by_id = {c["id"]: {"slug": c["slug"], "name": html.unescape(c["name"])} for c in cats}
    articles = []
    for p, m in zip(posts, meta):
        seo = (m.get("seo_title") or "").replace(" | Rodeo Texas", "").strip()
        articles.append({
            "slug": p["slug"],
            "title": html.unescape(p["title"]["rendered"]),
            "seo_title": seo or None,
            "meta_description": m.get("meta_description"),
            "excerpt": text(p["excerpt"]["rendered"]).replace(" […]", "…").replace(" [&hellip;]", "…"),
            "content_html": clean_content(p["content"]["rendered"]),
            "featured_image": (m.get("featured") or "").replace(SITE, "") or None,
            "featured_alt": m.get("featured_alt") or html.unescape(p["title"]["rendered"]),
            "featured_width": m.get("fw"), "featured_height": m.get("fh"),
            "categories": [cat_by_id[c] for c in p["categories"] if c in cat_by_id],
            "published_at": p["date_gmt"].replace("T", " "),
            "updated_at": p["modified_gmt"].replace("T", " "),
        })
    json.dump({"categories": list(cat_by_id.values()), "articles": articles},
              open(os.path.join(DATA, "articles.json"), "w"), indent=1, ensure_ascii=False)

    # ---- events
    if a.audit_dir:
        events = json.load(open(os.path.join(a.audit_dir, "events_all.json")))
    else:
        events = []
        for page in range(1, 20):
            d = json.loads(get(f"{SITE}/wp-json/tribe/events/v1/events?per_page=50&page={page}"
                               "&start_date=2000-01-01&end_date=2030-12-31"))
            events += d.get("events", [])
            if page >= d.get("total_pages", 1):
                break
    legacy, redirects = [], {}
    for e in events:
        title = html.unescape(e["title"]).strip()
        path = "/" + e["url"].replace(SITE + "/", "")
        if title.startswith("Main Navigation "):
            redirects[path] = "/rodeos/"
            continue
        is_tx, city = texas_city(title)
        if not is_tx:
            redirects[path] = "/rodeos/"
            continue
        site = (e.get("website") or "").strip()
        if site in BAD_LINKS or not site:
            site = None
        elif not site.startswith("http"):
            site = "https://" + site
        legacy.append({
            "legacy_id": e["id"], "slug": e["slug"], "title": title,
            "start_date": e["start_date"][:10], "end_date": e["end_date"][:10],
            "city": city, "disciplines": text(e["description"]),
            "official_url": site, "legacy_url": path,
        })
    json.dump(legacy, open(os.path.join(DATA, "legacy_events.json"), "w"), indent=1, ensure_ascii=False)

    # WordPress-only paths
    redirects.update({
        "/events/": "/rodeos/", "/rodeos/list/": "/rodeos/", "/rodeos/month/": "/rodeos/?view=calendar",
        "/rodeos/today/": "/rodeos/", "/rodeos/photo/": "/rodeos/",
        "/rodeos/category/past-rodeo/": "/past-events/", "/rodeos/category/ongoing/": "/rodeos/",
        "/feed/": "/blog/", "/comments/feed/": "/blog/",
        "/post-sitemap.xml": "/sitemap.xml", "/page-sitemap.xml": "/sitemap.xml",
        "/tribe_events-sitemap1.xml": "/sitemap.xml", "/tribe_events-sitemap2.xml": "/sitemap.xml",
        "/category-sitemap.xml": "/sitemap.xml", "/sitemap_index.xml": "/sitemap.xml",
        "/home/": "/", "/news/": "/blog/", "/schedule/": "/rodeos/",
    })
    json.dump(dict(sorted(redirects.items())), open(os.path.join(DATA, "redirects.json"), "w"), indent=1)
    print(f"articles={len(articles)} legacy_texas_events={len(legacy)} redirects={len(redirects)}")


if __name__ == "__main__":
    main()
