#!/usr/bin/env python3
"""Generates the Resources pages for stormclaims.org from content/resources.py:
   resources/index.html, resources/<slug>/index.html, and the Resources
   section of the homepage (between the resources:start / resources:end
   markers). Everything else on the site is hand-written HTML."""

import os
import re
from datetime import date
from html import escape

from content.resources import RESOURCES

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN = "https://stormclaims.org"


def nice_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def head(title, description, path, noindex=False):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{ORIGIN}{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/">
      <span class="mark" aria-hidden="true">R</span>
      <span><b>Rise Public Adjusting</b><span>Referral portal · StormClaims.org</span></span>
    </a>
    <nav aria-label="Site">
      <a href="/#how">How it works</a>
      <a href="/#checklist">What to send</a>
      <a href="/resources/">Resources</a>
      <a href="/#contact">Contact</a>
      <a class="cta" href="/upload/">Upload files</a>
    </nav>
  </div>
</header>
"""


FOOTER = """
<footer>
  <div class="wrap">
    <span>© 2026 Rise Public Adjusting LLC · Texas Public Adjuster License #3356839 · Houston, TX</span>
    <span>Public adjusters, not attorneys. <a href="/upload/">Direct upload link</a></span>
  </div>
</footer>
</body>
</html>
"""


def card(r):
    file_bit = f'<span class="res-file">{escape(r["file_label"])}</span>' if r.get("file") else ""
    return f"""        <article class="post">
          <div class="post-meta"><span class="post-cat">{escape(r["category"])}</span> · {nice_date(r["published"])}{file_bit}</div>
          <h2><a href="/resources/{r["slug"]}/">{escape(r["title"])}</a></h2>
          <p class="post-src">{escape(r["source"])}</p>
          <p>{escape(r["summary"])}</p>
          <a class="post-more" href="/resources/{r["slug"]}/">Read and download →</a>
        </article>"""


def index_page():
    cards = "\n".join(card(r) for r in RESOURCES)
    return head("Resources | StormClaims.org", "Reference documents and guides for Rise Public Adjusting referrals: industry bulletins, claim documentation tips and what to attach to an estimate.", "/resources/") + f"""
<main>
  <section class="hero hero-sm">
    <div class="wrap">
      <h1>Resources</h1>
      <p>Reference documents contractors ask us for, each with a short write-up on when it helps and how to use it on a claim. Attach them to your estimate or send the link to the homeowner.</p>
    </div>
  </section>
  <section class="posts-sec">
    <div class="wrap posts">
{cards}
    </div>
  </section>
</main>
""" + FOOTER


def resource_page(r):
    path = f"/resources/{r['slug']}/"
    file_block = ""
    if r.get("file"):
        href = f"/resources/{r['file']}"
        file_block = f"""
      <div class="dl">
        <a class="btn btn-primary" href="{href}" download>Download the PDF</a>
        <a class="btn btn-ghost" href="{href}" target="_blank" rel="noopener">Open in a new tab</a>
        <span class="dl-meta">{escape(r["file_label"])}</span>
      </div>"""
    preview = ""
    if r.get("file") and r["file"].lower().endswith(".pdf"):
        href = f"/resources/{r['file']}"
        preview = f"""
      <section class="preview">
        <h2>Preview</h2>
        <object data="{href}#view=FitH" type="application/pdf" aria-label="PDF preview">
          <p>Your browser can't show the PDF inline. <a href="{href}">Download it instead.</a></p>
        </object>
      </section>"""
    return head(f"{r['title']} | Resources | StormClaims.org", r["summary"][:155], path) + f"""
<main class="wrap article-wrap">
  <article class="article">
    <p class="crumbs"><a href="/resources/">Resources</a> › {escape(r["category"])}</p>
    <h1>{escape(r["title"])}</h1>
    <p class="post-meta">{escape(r["source"])} · Document dated {nice_date(r["date"])} · Posted {nice_date(r["published"])}</p>
    <p class="lede">{escape(r["summary"])}</p>{file_block}
    <div class="prose">
{r["body"].strip()}
    </div>{preview}
    <div class="article-foot">
      <a class="btn btn-ghost" href="/resources/">← All resources</a>
      <a class="btn btn-primary" href="/upload/">Upload a claim</a>
    </div>
  </article>
</main>
""" + FOOTER


def home_section():
    latest = RESOURCES[:3]
    items = "\n".join(f"""        <a class="res" href="/resources/{r["slug"]}/">
          <span class="res-icon" aria-hidden="true">{'PDF' if r.get('file', '').lower().endswith('.pdf') else 'DOC'}</span>
          <span class="res-body">
            <b>{escape(r["title"])}</b>
            <span>{escape(r["summary"])}</span>
          </span>
          <span class="res-meta">{escape(r["category"])}</span>
        </a>""" for r in latest)
    return f"""<!-- resources:start -->
  <section id="resources">
    <div class="wrap">
      <div class="section-head">
        <h2>Resources</h2>
        <p><a href="/resources/">See all resources →</a></p>
      </div>
      <div class="resources">
{items}
      </div>
    </div>
  </section>
<!-- resources:end -->"""


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(html)
    print("wrote", path)


def main():
    write("resources/index.html", index_page())
    for r in RESOURCES:
        write(f"resources/{r['slug']}/index.html", resource_page(r))
    home = os.path.join(ROOT, "index.html")
    t = open(home).read()
    new, n = re.subn(r"<!-- resources:start -->.*?<!-- resources:end -->", home_section(), t, flags=re.S)
    if not n:
        raise SystemExit("index.html is missing the resources:start / resources:end markers")
    open(home, "w").write(new)
    print("updated index.html resources section")


if __name__ == "__main__":
    main()
