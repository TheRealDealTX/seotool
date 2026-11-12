#!/usr/bin/env python3
"""Pre-build sanity checks for the content modules in src/ (run: python3 check_content.py).

Catches the most common validate.py failures early: title length/width, description
length, heading order inside bodies, sister-state names, PHP tags and unknown internal links.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

BANNED = ["Alabama", "Florida", "Georgia", "North Carolina", "Nevada", "Arizona", "Missouri", "Montana",
          "Massachusetts", "Wyoming", "West Virginia", "Maryland"]

_W = dict(zip("abcdefghijklmnopqrstuvwxyz", [556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500]))
_W.update(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611]))
_W.update({c: 556 for c in "0123456789"}); _W.update({" ": 278, "|": 260, "&": 667, "-": 333, ",": 278, ".": 278, "?": 556, ":": 278, "'": 191, "’": 222, "(": 333, ")": 333, "/": 278, "$": 556, "%": 889})


SERVICE_SLUGS = ["party-appraiser-representation", "home-insurance-appraisal", "commercial-hoa-appraisal", "roof-hail-appraisal",
                 "tornado-wind-appraisal", "water-damage-appraisal", "fire-smoke-appraisal", "ice-storm-freeze-appraisal",
                 "farm-equine-property-appraisal", "second-look-estimate-review", "neutral-umpire-services"]
LOCATION_SLUGS = ["louisville", "lexington", "bowling-green", "owensboro", "covington", "richmond", "elizabethtown", "paducah",
                  "frankfort", "hopkinsville", "pikeville", "ashland"]
POST_SLUGS = ["kentucky-appraisal-clause-basics", "ice-storm-frozen-pipe-claims", "tornado-claim-first-30-days", "matching-discontinued-materials",
              "flood-vs-water-damage-kentucky", "choosing-appraiser-and-umpire", "sinkholes-mine-subsidence-coverage"]


def title_px(t):
    return sum(_W.get(c, 556) for c in t) * 20 / 1000


errs = []


def check_title(where, t):
    if len(t) > 60:
        errs.append(f"{where}: title {len(t)} chars > 60: {t}")
    if title_px(t) > 580:
        errs.append(f"{where}: title ~{title_px(t):.0f}px > 580: {t}")


def check_desc(where, d):
    if not 110 <= len(d) <= 150:
        errs.append(f"{where}: description {len(d)} chars (want 110-150): {d}")


def check_body(where, html, start=2):
    levels = [int(x) for x in re.findall(r"<h([1-6])\b", html)]
    if 1 in levels:
        errs.append(f"{where}: body must not contain <h1>")
    prev = start - 1
    for lv in levels:
        if lv > prev + 1:
            errs.append(f"{where}: heading jump h{prev} -> h{lv}")
            break
        prev = lv
    if "<?" in html:
        errs.append(f"{where}: PHP tag in body")


def check_text(where, s):
    for b in BANNED:
        if re.search(b, s, re.I):
            errs.append(f"{where}: mentions banned sister-state name '{b}'")


def check_links(where, s, known):
    for href in re.findall(r'href="([^"]+)"', s):
        if href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        p = href.split("#")[0]
        if p not in known:
            errs.append(f"{where}: unknown internal link {href}")


def main():
    import importlib, types
    def load(n, **empty):
        try:
            return importlib.import_module(n)
        except ModuleNotFoundError:
            print(f"(src/{n}.py not written yet - skipped)")
            return types.SimpleNamespace(__file__=None, **empty)
    services = load("services", SERVICES=[])
    locations = load("locations", LOCATIONS=[])
    learn = load("learn", POSTS=[], PROCESS_BODY="", GLOSSARY=[None] * 40)
    SERVICES, LOCATIONS = services.SERVICES, locations.LOCATIONS
    known = {"/", "/about-us/", "/contact-us/", "/insurance-appraisal/", "/regions-served/", "/appraisal-calculators/",
             "/kentucky-appraisal-process/", "/insurance-appraisal-questions/", "/appraisal-terms/", "/appraisal-articles/",
             "/privacy/", "/terms/", "/legal-disclaimer/", "/photo-credits/", "/site-index/"}
    known |= {f"/insurance-appraisal/{s}/" for s in SERVICE_SLUGS}
    known |= {f"/regions-served/{s}/" for s in LOCATION_SLUGS}
    known |= {f"/appraisal-calculators/{t}/" for t in ["appraisal-payoff-estimator", "rcv-acv-holdback-calculator", "roof-measurement-calculator",
                                                      "percentage-deductible-calculator", "claim-timeline-builder", "appraisal-readiness-checkup",
                                                      "tree-removal-coverage-calculator"]}
    known |= {f"/appraisal-articles/{s}/" for s in POST_SLUGS}
    titles, descs = {}, {}
    for mod in (services, locations, learn):
        if not mod.__file__:
            continue
        src = open(mod.__file__, encoding="utf-8").read()
        check_text(os.path.basename(mod.__file__), src)
        check_links(os.path.basename(mod.__file__), src, known)
    for s in SERVICES:
        w = f"service {s['slug']}"
        check_title(w, s["title"]); check_desc(w, s["desc"]); check_body(w, s["body"])
        titles.setdefault(s["title"], []).append(w); descs.setdefault(s["desc"], []).append(w)
    for l in LOCATIONS:
        w = f"location {l['slug']}"
        check_title(w, l["title"]); check_desc(w, l["desc"]); check_body(w, l["body"])
        titles.setdefault(l["title"], []).append(w); descs.setdefault(l["desc"], []).append(w)
        for n in l["near"]:
            if n not in LOCATION_SLUGS:
                errs.append(f"{w}: unknown near slug {n}")
    check_body("PROCESS_BODY", learn.PROCESS_BODY)
    for p in learn.POSTS:
        w = f"post {p['slug']}"
        check_title(w, p["seo"]); check_desc(w, p["desc"]); check_body(w, p["body"])
        titles.setdefault(p["seo"], []).append(w); descs.setdefault(p["desc"], []).append(w)
    if len(learn.GLOSSARY) < 35:
        errs.append(f"glossary has {len(learn.GLOSSARY)} terms (< 35)")
    for t, ws in titles.items():
        if len(ws) > 1:
            errs.append(f"duplicate title {t}: {ws}")
    for d, ws in descs.items():
        if len(ws) > 1:
            errs.append(f"duplicate description: {ws}")
    for e in errs:
        print("ERROR", e)
    print(f"{len(errs)} problems")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
