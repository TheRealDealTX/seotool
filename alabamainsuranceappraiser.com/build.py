#!/usr/bin/env python3
"""Generate alabamainsuranceappraiser.com into ./public_html.

    python3 build.py && python3 validate.py

Static content pages are rendered to HTML; index.php (front controller) and
api/contact.php (lead form -> SMTP) are copied from ./static with every other
asset. No dependencies beyond the Python 3 standard library.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from components import render_page, url  # noqa: E402
from siteconfig import TODAY  # noqa: E402
from content import home, services, areas, posts, pages, tools  # noqa: E402

OUT = os.path.join(HERE, "public_html")
STATIC = os.path.join(HERE, "static")


def all_pages():
    ps = [home.page()]
    ps += services.pages()
    ps += areas.pages()
    ps += tools.pages()
    ps += posts.pages()
    ps += pages.pages()
    return ps


def out_path(path):
    if path == "/":
        return os.path.join(OUT, "home.html")
    if path.endswith(".html"):
        return os.path.join(OUT, path.lstrip("/"))
    return os.path.join(OUT, path.strip("/"), "index.html")


def sitemap_xml(ps):
    rows = []
    for p in ps:
        if p.get("noindex") or p["path"].endswith(".html"):
            continue
        rows.append(f"  <url><loc>{url(p['path'])}</loc><lastmod>{p.get('modified', TODAY)}</lastmod>"
                    f"<changefreq>{p.get('changefreq', 'monthly')}</changefreq><priority>{p.get('priority', '0.6')}</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    ps = all_pages()
    paths = [p["path"] for p in ps]
    dupes = {x for x in paths if paths.count(x) > 1}
    if dupes:
        sys.exit(f"duplicate paths: {dupes}")
    for p in ps:
        f = out_path(p["path"])
        os.makedirs(os.path.dirname(f), exist_ok=True)
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(render_page(p))
    with open(os.path.join(OUT, "sitemap.xml"), "w") as fh:
        fh.write(sitemap_xml(ps))
    with open(os.path.join(OUT, "robots.txt"), "w") as fh:
        fh.write("User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /home.html\nDisallow: /thank-you/\n\n"
                 f"Sitemap: {url('/sitemap.xml')}\n")
    print(f"built {len(ps)} pages into {OUT}")


if __name__ == "__main__":
    main()
