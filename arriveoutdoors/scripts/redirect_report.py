"""Write REDIRECTS.md: the delete / merge / redirect plan for every old URL."""
import csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from siteconfig import REDIRECTS, GONE, KEPT_FROM_WORDPRESS, ARTICLES

root = os.path.join(os.path.dirname(__file__), "..")
posts = list(csv.reader(open(os.path.join(root, "source-archive", "index.tsv")), delimiter="\t"))
out = ["# Arrive Outdoors: what happened to every old URL", "",
       "Generated from `siteconfig.py` by `scripts/redirect_report.py`. The `.htaccess` rules are built from the same data.", "",
       "## The 30 posts that were live on WordPress", "",
       "| Old post | Action | New URL | Why |", "|---|---|---|---|"]
for slug, date, title in posts:
    if slug == "blogs":
        continue
    s = slug.replace("__", "/")
    p = "/" + s + "/"
    if s in KEPT_FROM_WORDPRESS:
        merged = [o for o, (n, w) in REDIRECTS.items() if n == p and w.startswith("Merged")]
        act = "**Keep + rewrite**" + (" (merge target)" if merged else "")
        out.append(f"| {title} | {act} | `{p}` (same URL) | Rewritten for depth and accuracy" + (f"; absorbs {', '.join('`'+m+'`' for m in merged)}" if merged else "") + " |")
    elif p in REDIRECTS:
        n, why = REDIRECTS[p]
        act = "**Merge → 301**" if why.startswith("Merged") else "**Remove → 301**"
        out.append(f"| {title} | {act} | `{n}` | {why} |")
    elif p in GONE:
        out.append(f"| {title} | **Delete → 410 Gone** | — | {GONE[p]} |")
    else:
        out.append(f"| {title} | ? | | |")
new = [a for a in ARTICLES if a not in KEPT_FROM_WORDPRESS]
out += ["", "## New articles", ""] + [f"- `/{a}/`" + (" — restores a previously deleted URL" if a in ("how-to-start-a-fire-with-wet-wood", "cold-weather-camping", "car-camping-essentials") else "") for a in new]
out += ["", "## All other redirects (301)", "", "| Old URL | Goes to | Note |", "|---|---|---|"]
post_paths = {"/" + r[0].replace("__", "/") + "/" for r in posts}
for o, (n, w) in REDIRECTS.items():
    if o not in post_paths:
        out.append(f"| `{o}` | `{n}` | {w} |")
out += ["", "## Gone (410)", "", "| Old URL | Why |", "|---|---|"] + [f"| `{g}` | {w} |" for g, w in GONE.items() if g not in post_paths]
out += ["", "## Pattern rules", "",
        "- `/products/*`, `/group/*`, `/collections*` → `/gear/`",
        "- `/pages/*` → `/destinations/`; `/blogs/*` (except Camping 101) → `/guides/`",
        "- `/category/*`, `/tag/*`, date archives `/20xx/...`, `/feed/` → `/guides/`; `/author/*` → `/about/`",
        "- `*/feed/` and `*/amp/` → the page itself",
        "- `www.` and `http://` → `https://arriveoutdoors.com`",
        "- Old Yoast sitemap files (`/sitemap_index.xml`, `/post-sitemap.xml`, …) now serve the new sitemap", ""]
open(os.path.join(root, "REDIRECTS.md"), "w").write("\n".join(out))
print("wrote REDIRECTS.md")
