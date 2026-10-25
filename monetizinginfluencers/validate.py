#!/usr/bin/env python3
"""Crawl the local preview of monetizinginfluencers.com, check every page, and
write public/sitemap.xml from the indexable pages it finds.

    python3 validate.py            # starts `php -S` itself on a free port
    python3 validate.py --no-write # check only, leave sitemap.xml alone

Checks: HTTP 200, no PHP warnings, one <h1>, title 25-65 chars, meta
description 70-165 chars, unique titles/descriptions, canonical equals the
page URL, JSON-LD parses, every internal link/asset resolves, in-page #anchors
exist, every <img> has alt text and width/height. The homepage must mention
"Monetizing Influencers" at least 14 times in its <main> content.
"""
import html
import json
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

HERE = Path(__file__).resolve().parent
PUBLIC = HERE / "public"
ORIGIN = "https://monetizinginfluencers.com"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.desc, self.canonical, self.robots = "", None, None, ""
        self.h1, self.links, self.assets, self.ids, self.imgs, self.ld = 0, [], [], set(), [], []
        self._in_title = self._in_ld = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "title" and not self.title:
            self._in_title = True
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        elif tag == "meta" and a.get("name") == "robots":
            self.robots = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "manifest"):
            self.assets.append(a["href"])
        elif tag == "h1":
            self.h1 += 1
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "script" and a.get("src"):
            self.assets.append(a["src"])
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld, self._buf = True, ""
        elif tag == "img":
            self.imgs.append(a)
            if a.get("src"):
                self.assets.append(a["src"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_ld:
            self.ld.append(self._buf)
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._buf += data


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace"), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), ""


def main():
    write = "--no-write" not in sys.argv
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    srv = subprocess.Popen(["php", "-S", f"127.0.0.1:{port}", "-t", str(PUBLIC), str(HERE / "dev-router.php")],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    errors, pages, seen_assets = [], {}, set()
    try:
        queue, seen = ["/"], {"/"}
        while queue:
            path = queue.pop(0)
            status, body, ctype = fetch(base + path)
            if status != 200:
                errors.append(f"{path}: HTTP {status}")
                continue
            if "text/html" not in ctype:
                continue
            if re.search(r"(Warning|Notice|Fatal error|Deprecated|Parse error)</b>:|\b(Warning|Notice|Deprecated): ", body):
                errors.append(f"{path}: PHP warning/notice in output")
            p = Page()
            p.feed(body)
            pages[path] = (p, body)
            for href in p.links:
                u = urlparse(urljoin(ORIGIN + path, href))
                if u.scheme not in ("http", "https") or u.netloc != urlparse(ORIGIN).netloc:
                    continue
                target = u.path or "/"
                if u.fragment and target == path:
                    continue
                if target not in seen and not re.search(r"\.(png|webp|ico|xml|txt|css|js|html)$", target):
                    seen.add(target)
                    queue.append(target)
                elif re.search(r"\.(png|webp|ico|xml|txt)$", target):
                    seen_assets.add(target)
            for a in p.assets:
                u = urlparse(urljoin(ORIGIN + path, a))
                if u.netloc == urlparse(ORIGIN).netloc:
                    seen_assets.add(u.path)

        titles, descs = {}, {}
        for path, (p, body) in pages.items():
            t = html.unescape(p.title.strip())
            d = html.unescape(p.desc or "")
            noindex = "noindex" in p.robots
            if p.h1 != 1:
                errors.append(f"{path}: {p.h1} <h1> tags")
            if not 25 <= len(t) <= 65:
                errors.append(f"{path}: title length {len(t)} ({t})")
            if not 70 <= len(d) <= 165:
                errors.append(f"{path}: description length {len(d)}")
            if not noindex:
                titles.setdefault(t, []).append(path)
                descs.setdefault(d, []).append(path)
                if p.canonical != ORIGIN + path:
                    errors.append(f"{path}: canonical {p.canonical}")
            for block in p.ld:
                try:
                    json.loads(block)
                except ValueError as e:
                    errors.append(f"{path}: bad JSON-LD ({e})")
            for img in p.imgs:
                if img.get("alt") is None:
                    errors.append(f"{path}: img without alt {img.get('src')}")
                if not (img.get("width") and img.get("height")):
                    errors.append(f"{path}: img without width/height {img.get('src')}")
            for href in p.links:
                u = urlparse(urljoin(ORIGIN + path, href))
                if u.fragment and u.netloc == urlparse(ORIGIN).netloc:
                    tgt = pages.get(u.path or "/")
                    if tgt and u.fragment not in tgt[0].ids:
                        errors.append(f"{path}: missing anchor {u.path}#{u.fragment}")
        for t, ps in titles.items():
            if len(ps) > 1:
                errors.append(f"duplicate title {t!r}: {ps}")
        for d, ps in descs.items():
            if len(ps) > 1:
                errors.append(f"duplicate description: {ps}")
        for a in sorted(seen_assets):
            if a == "/sitemap.xml":
                continue
            if not (PUBLIC / a.lstrip("/")).is_file():
                status, _, _ = fetch(base + a)
                if status != 200:
                    errors.append(f"missing asset {a}")

        home = pages.get("/")
        if home:
            main_html = re.search(r'<main id="main">(.*)</main>', home[1], re.S).group(1)
            main_html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", main_html, flags=re.S)
            n = html.unescape(re.sub(r"<[^>]+>", " ", main_html)).count("Monetizing Influencers")
            print(f"homepage mentions of 'Monetizing Influencers' in <main>: {n}")
            if n < 14:
                errors.append(f"homepage mentions 'Monetizing Influencers' only {n} times")

        indexable = sorted(p for p, (pg, _) in pages.items() if "noindex" not in pg.robots)
        if write:
            today = date.today().isoformat()
            urls = []
            for p in indexable:
                prio = "1.0" if p == "/" else "0.9" if p.count("/") == 2 else "0.7"
                urls.append(f"  <url><loc>{ORIGIN}{p}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
            xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
            (PUBLIC / "sitemap.xml").write_text(xml)
            print(f"wrote sitemap.xml with {len(urls)} URLs")
    finally:
        srv.terminate()

    print(f"crawled {len(pages)} pages, {len(seen_assets)} assets")
    for e in errors:
        print("ERROR", e)
    print("OK" if not errors else f"{len(errors)} problem(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
