#!/usr/bin/env python3
"""Post-build checks. Starts PHP's built-in server on ./public and verifies:
  * every old URL from the keyword exports and backlink export returns 200, or 301 -> 200
  * every internal link on every page resolves
  * one <h1>, unique <title>, meta description present on every page
  * every Amazon link carries the affiliate tag
"""
import csv, json, os, re, subprocess, sys, time, urllib.request, urllib.error
from urllib.parse import urlparse
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
PORT = 8765
BASE = f"http://127.0.0.1:{PORT}"
ROUTER = os.path.join(ROOT, "src", "dev_router.php")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None
opener = urllib.request.build_opener(NoRedirect)

def fetch(path):
    try:
        r = opener.open(BASE + path, timeout=10)
        return r.status, r.headers.get("Location"), r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location"), ""

def resolve(path, hops=4):
    chain = []
    for _ in range(hops):
        st, loc, body = fetch(path)
        chain.append((st, path))
        if st in (301, 302) and loc:
            path = urlparse(loc).path + (("?" + urlparse(loc).query) if urlparse(loc).query else "")
            continue
        return st, chain, body
    return st, chain, body

def main():
    srv = subprocess.Popen(["php", "-S", f"127.0.0.1:{PORT}", "-t", PUB, ROUTER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.2)
    errors = []
    try:
        old = set()
        for f in ("positions-2026-10.csv", "positions-2025-12.csv"):
            for r in csv.DictReader(open(os.path.join(ROOT, "data", f))):
                u = urlparse(r["URL"]); old.add(u.path + (("?" + u.query) if u.query else ""))
        for r in csv.DictReader(open(os.path.join(ROOT, "data", "backlinks.csv"))):
            u = urlparse(r["Target url"]); old.add(u.path + (("?" + u.query) if u.query else ""))
        redirected = 0
        for p in sorted(old):
            st, chain, _ = resolve(p or "/")
            if st != 200:
                errors.append(f"OLD URL {p} -> {chain}")
            elif len(chain) > 1:
                redirected += 1
                if len(chain) > 2:
                    errors.append(f"redirect chain {chain}")
        print(f"old URLs checked: {len(old)}  (200 direct: {len(old) - redirected}, via 301: {redirected})")

        pages = []
        for d, _, fs in os.walk(os.path.join(PUB, "_p")):
            for f in fs:
                rel = os.path.relpath(os.path.join(d, f), os.path.join(PUB, "_p"))[:-5]
                pages.append("/" if rel == "home" else "/" + rel)
        titles, links = {}, set()
        amz_dp = amz_s = 0
        for p in pages:
            st, loc, body = fetch(p)
            if st != 200:
                errors.append(f"page {p} status {st}"); continue
            if body.count("<h1") != 1:
                errors.append(f"{p}: {body.count('<h1')} h1 tags")
            t = re.search(r"<title>(.*?)</title>", body).group(1)
            if t in titles:
                errors.append(f"duplicate title {t!r}: {p} & {titles[t]}")
            titles[t] = p
            m = re.search(r'<meta name="description" content="(.*?)"', body)
            if not m or len(m.group(1)) < 50:
                errors.append(f"{p}: short/missing description")
            for href in re.findall(r'href="([^"#]*)"', body):
                if href.startswith("/") and not href.startswith("//"):
                    links.add(href.split("?")[0])
                if "amazon.com/dp/" in href: amz_dp += 1
                elif "amazon.com/s?" in href: amz_s += 1
                if "amazon.com/" in href and "tag=relicsfilmlab-20" not in href:
                    errors.append(f"{p}: amazon link missing tag")
            for src in re.findall(r'src="(/[^"]+)"', body):
                links.add(src.split("?")[0])
        for l in sorted(links):
            if l.startswith("/assets/") or l.startswith("/cdn/") or "." in l.rsplit("/", 1)[-1]:
                if not os.path.exists(os.path.join(PUB, l.lstrip("/"))):
                    errors.append(f"missing file {l}")
                continue
            st, loc, _ = fetch(l)
            if st != 200:
                errors.append(f"internal link {l} -> {st} {loc or ''}")
        st, _, _ = fetch("/definitely-not-a-page")
        if st != 404:
            errors.append(f"unknown URL returned {st}, expected 404")
        st, loc, _ = fetch("/products/canon-ae-1/")
        if st != 301:
            errors.append("trailing slash not redirected")
        print(f"pages: {len(pages)}, internal links checked: {len(links)}")
        print(f"amazon links: {amz_dp} direct product (/dp/), {amz_s} search fallback")
    finally:
        srv.terminate()
    for e in errors[:80]:
        print("ERROR", e)
    print("errors:", len(errors))
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
