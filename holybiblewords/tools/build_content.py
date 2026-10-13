#!/usr/bin/env python3
"""Convert the WordPress export (sources/wordpress-*.json) into the small
content files the PHP app reads (public/lib/content/*.json)."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
OUT = ROOT / "public" / "lib" / "content"
IMAGES = {  # featured images, re-hosted at their original WordPress paths
    47973: "/wp-content/uploads/2025/10/Faith-in-the-Age-of-AI-Keeping-Christianity-Alive-in-a-Digital-Worl.webp",
    816: "/wp-content/uploads/2025/02/50-Easy-Bible-Quiz-Questions-for-Kids-With-Answers.webp",
}
PRIVACY_EXTRA = (
    '<h2>Reading data stored on your device</h2>'
    '<p>Bookmarks, highlights, notes, reading history, reading-plan progress and display settings are saved in your '
    'browser&rsquo;s local storage (or in the app on your phone). They stay on your device and are never sent to us.</p>'
)


def tidy(h):
    h = re.sub(r'\s+class="wp-block-[^"]*"', "", h)
    h = re.sub(r"<p>\s*</p>", "", h)
    h = re.sub(r"\n{2,}", "\n", h)
    h = h.replace('href="https://holybiblewords.com/', 'href="/')
    return h.strip()


def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    posts = []
    for p in json.loads((SRC / "wordpress-posts.json").read_text(encoding="utf-8")):
        posts.append({
            "slug": p["slug"],
            "title": text(p["title"]["rendered"]),
            "date": p["date"], "modified": p["modified"],
            "excerpt": text(p["excerpt"]["rendered"]).replace(" [&hellip;]", "").replace(" […]", "")[:180].rsplit(" ", 1)[0] + "…",
            "image": IMAGES[p["featured_media"]],
            "html": tidy(p["content"]["rendered"]),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    (OUT / "posts.json").write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in json.loads((SRC / "wordpress-pages.json").read_text(encoding="utf-8")):
        if p["slug"] == "privacy-policy":
            body = tidy(p["content"]["rendered"])
            body = body.replace("<h2>7. Contact Us</h2>", PRIVACY_EXTRA + "<h2>7. Contact Us</h2>")
            (OUT / "privacy-policy.json").write_text(json.dumps({"title": text(p["title"]["rendered"]), "html": body}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(posts)} posts, privacy policy")


if __name__ == "__main__":
    main()
