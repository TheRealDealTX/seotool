#!/usr/bin/env python3
"""Crawl the site on PHP's built-in server and check SEO/HTML basics.

    python3 validate.py            # starts php -S on a free port, crawls, reports

Checks: every internal link and asset resolves, one H1 per page, unique titles and
descriptions, canonical present, valid JSON-LD, alt text on images, the homepage
mentions the primary keyword at least 14 times, no WordPress leftovers, and the
primary keyword of every service, area and post appears in its title, H1,
description and body.
"""
import html
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.request
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
KEYWORD = "austin landscape lighting"
MIN_HOME_MENTIONS = 14


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "validate.py"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read()


def text_of(h):
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).lower()


def main():
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    proc = subprocess.Popen(["php", "-S", f"127.0.0.1:{port}", "index.php"], cwd=ROOT,
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    time.sleep(0.8)
    errors, warnings = [], []
    titles, descs = {}, {}
    seen, queue = set(), ["/"]
    pages = {}
    assets_checked = {}
    try:
        while queue:
            path = queue.pop(0)
            if path in seen:
                continue
            seen.add(path)
            status, ctype, body = fetch(base + path)
            if path.endswith((".css", ".js", ".webp", ".png", ".ico", ".svg", ".xml", ".txt", ".webmanifest")):
                if status != 200:
                    errors.append(f"{path}: asset status {status}")
                continue
            if status != 200:
                errors.append(f"{path}: status {status}")
                continue
            if "text/html" not in ctype:
                continue
            h = body.decode("utf-8", "replace")
            pages[path] = h
            refs = re.findall(r'(?:href|src)="([^"]+)"', h)
            for ss in re.findall(r'srcset="([^"]+)"', h):
                refs += [p.strip().split(" ")[0] for p in ss.split(",")]
            for u in refs:
                if True:
                    if not u or u.startswith(("mailto:", "tel:", "#", "http", "data:")):
                        continue
                    u = u.split("#")[0].split("?")[0]
                    if u and u not in seen:
                        queue.append(u)
        # per-page checks
        for path, h in sorted(pages.items()):
            h1 = re.findall(r"<h1\b", h)
            if len(h1) != 1:
                errors.append(f"{path}: {len(h1)} <h1> tags")
            t = re.search(r"<title>(.*?)</title>", h, re.S)
            d = re.search(r'<meta name="description" content="(.*?)">', h)
            if not t:
                errors.append(f"{path}: no title")
            else:
                titles.setdefault(t.group(1), []).append(path)
                if len(html.unescape(t.group(1))) > 90:
                    warnings.append(f"{path}: title {len(t.group(1))} chars")
            if not d:
                errors.append(f"{path}: no description")
            else:
                descs.setdefault(d.group(1), []).append(path)
                if len(html.unescape(d.group(1))) > 165:
                    warnings.append(f"{path}: description {len(d.group(1))} chars")
            if '<link rel="canonical"' not in h:
                errors.append(f"{path}: no canonical")
            for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
                try:
                    json.loads(m.group(1))
                except Exception as e:
                    errors.append(f"{path}: bad JSON-LD {e}")
            for tag in re.findall(r"<img\b[^>]*>", h):
                if "alt=" not in tag:
                    errors.append(f"{path}: img without alt")
            for bad in ["wp-content", "wp-includes", "elementor", "litespeed", "wp-json", "hello-elementor"]:
                if bad in h.lower():
                    errors.append(f"{path}: contains '{bad}'")
            for num in set(re.findall(r"\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}", text_of(h))):
                if re.sub(r"\D", "", num)[-10:] != "2817047210" and not re.search(r"555", num):
                    errors.append(f"{path}: unexpected phone {num!r}")
        for v, ps in titles.items():
            if len(ps) > 1 and not any(p.startswith("/404") for p in ps):
                errors.append(f"duplicate title {v!r} on {ps}")
        for v, ps in descs.items():
            if len(ps) > 1:
                errors.append(f"duplicate description on {ps}")
        # homepage keyword
        home = text_of(pages.get("/", ""))
        n = len(re.findall(re.escape(KEYWORD), home))
        print(f"homepage mentions of '{KEYWORD}': {n}")
        if n < MIN_HOME_MENTIONS:
            errors.append(f"/: only {n} mentions of '{KEYWORD}' (want >= {MIN_HOME_MENTIONS})")
        # keyword placement on money pages
        sys.path.insert(0, ROOT)
        content = subprocess.run(["php", "-r", '''
define("ALL_SITE", true); define("SITE_ROOT", __DIR__); require "config.php"; require "lib/helpers.php"; require "lib/content.php";
$o=[]; foreach (services() as $s) $o[]=[$s["path"],$s["keyword"]]; foreach (areas() as $a) $o[]=[$a["path"],$a["keyword"]]; foreach (posts() as $p) $o[]=[$p["path"],$p["keyword"]];
echo json_encode($o);'''], cwd=ROOT, capture_output=True, text=True)
        for path, kw in json.loads(content.stdout):
            h = pages.get(path)
            if not h:
                errors.append(f"{path}: not crawled")
                continue
            words = kw.lower().split()
            title = html.unescape(re.search(r"<title>(.*?)</title>", h, re.S).group(1)).lower()
            desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', h).group(1)).lower()
            h1 = text_of(re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S).group(1))
            body = text_of(h)
            for label, hay in [("title", title), ("description", desc), ("h1", h1)]:
                if not all(w in hay for w in words):
                    warnings.append(f"{path}: keyword {kw!r} words missing from {label}")
            if kw.lower() not in body:
                warnings.append(f"{path}: exact keyword {kw!r} not in body text")
        # sitemap covers every crawled page
        st, _, sm = fetch(base + "/sitemap.xml")
        locs = set(re.findall(r"<loc>https://austinlandscapelighting\.com(/[^<]*)</loc>", sm.decode()))
        for p in pages:
            if p not in locs and p not in ("/thank-you/", "/404/") and "sent=" not in p and 'content="noindex' not in pages[p]:
                errors.append(f"{p}: missing from sitemap.xml")
        for l in locs:
            if l not in pages:
                errors.append(f"sitemap lists uncrawled {l}")
        err = proc.stderr
    finally:
        proc.terminate()
        try:
            stderr = proc.stderr.read().decode("utf-8", "replace")
        except Exception:
            stderr = ""
    php_problems = [l for l in stderr.splitlines() if re.search(r"PHP (Warning|Notice|Fatal|Deprecated|Parse)", l)]
    for l in php_problems[:20]:
        errors.append("php: " + l.strip())
    print(f"{len(pages)} HTML pages crawled, {len(seen) - len(pages)} assets/links checked")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print("  ! " + w)
    if errors:
        print(f"\n{len(errors)} ERROR(s):")
        for e in errors[:80]:
            print("  x " + e)
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
