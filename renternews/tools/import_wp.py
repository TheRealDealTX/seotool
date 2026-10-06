#!/usr/bin/env python3
"""One-time import of the original WordPress content (posts + pages).

    python3 tools/import_wp.py posts.json pages.json   # REST dumps with _embed=1

Writes content/legacy_posts.json and content/legacy_pages.json. The original
URLs are kept exactly: /news/<slug>/ for posts and /<slug>/ for pages.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def clean(c):
    c = re.sub(r"<!--.*?-->", "", c, flags=re.S)
    c = c.replace("https://renternews.net/", "/")
    c = re.sub(r'\s(?:class|id)="(?:wp-block-[^"]*|h-[^"]*|has-[^"]*|wp-image-\d+|size-[^"]*)"', "", c)
    c = re.sub(r'\sdecoding="async"|\sfetchpriority="[^"]*"', "", c)
    c = re.sub(r"\n{3,}", "\n\n", c)
    return c.strip()


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


posts, pages = (json.load(open(p)) for p in sys.argv[1:3])
out = []
for p in posts:
    y = p.get("yoast_head_json") or {}
    fm = (p.get("_embedded", {}).get("wp:featuredmedia") or [{}])[0]
    out.append({
        "slug": p["slug"],
        "path": p["link"].replace("https://renternews.net", ""),
        "title": text(p["title"]["rendered"]),
        "seo_title": y.get("title", ""),
        "description": y.get("description") or text(p["excerpt"]["rendered"])[:155],
        "wp_id": p["id"],
        "date": p["date_gmt"] + "+00:00",
        "modified": p["modified_gmt"] + "+00:00",
        "category": "fire",
        "image": fm.get("source_url", "").replace("https://renternews.net", ""),
        "image_alt": fm.get("alt_text") or text(p["title"]["rendered"]),
        "image_w": (fm.get("media_details") or {}).get("width"),
        "image_h": (fm.get("media_details") or {}).get("height"),
        "body_html": clean(p["content"]["rendered"]),
        "legacy": True,
    })
out.sort(key=lambda x: x["date"], reverse=True)
json.dump(out, open(os.path.join(ROOT, "content/legacy_posts.json"), "w"), indent=1, ensure_ascii=False)

pg = [{"slug": p["slug"], "wp_id": p["id"], "title": text(p["title"]["rendered"]),
       "description": (p.get("yoast_head_json") or {}).get("description", ""),
       "body_html": clean(p["content"]["rendered"])} for p in pages]
json.dump(pg, open(os.path.join(ROOT, "content/legacy_pages.json"), "w"), indent=1, ensure_ascii=False)
print(len(out), "posts,", len(pg), "pages")
