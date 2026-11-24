"""Map Google Search Console queries to the page that should rank for them.

    python3 gsc_keywords.py    # reads data/gsc-performance-2026-11.json, writes data/gsc_keywords.json
build.py uses the result to (a) list real search phrases on each page and (b) make sure each
page's main query is used naturally throughout the copy.
"""
import json, os, re
import catalog, build

ROOT = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(ROOT, "data", "gsc-performance-2026-11.json")))["Queries"][1:]
P = catalog.products()
n = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
STOP = {"camera", "cameras", "film", "35mm", "the", "for", "sale", "vintage", "used", "price", "prices", "review", "a", "of", "with",
        "battery", "batteries", "lens", "lenses", "manual", "instant", "zoom_", "date", "black", "silver", "buy", "best", "old"}
SYN = {"fujifilm": "fuji", "fujica": "fuji", "sureshot": "sureshot", "eos": "eos", "nikkormat": "nikomat"}
BRAND = {"relics", "relic", "wearerelics", "relyckphoto"}

def toks(s):
    out = []
    for t in re.split(r"[\s\-/&.,]+", s.lower()):
        t = n(t)
        if t:
            out.append(SYN.get(t, t))
    return out

def name_index(p):
    t = toks(p["name"] + " " + p["slug"].replace("-", " "))
    pairs = {a + b for a, b in zip(t, t[1:])}
    triples = {a + b + c for a, b, c in zip(t, t[1:], t[2:])}
    return set(t) | pairs | triples

IDX = [(p, name_index(p)) for p in P]
RULES = [  # (any of these substrings, target page)
    (("why are my film", "film photos blank", "blank film"), "/blogs/guides/why-are-my-film-photos-blank-common-mistakes"),
    ((" cla", "cla ", "repair", "restored", "refurbished", "servic"), "/camera-repairs"),
    (("medium format", "120 film camera", "120mm"), "/collections/medium-format-cameras"),
    (("point and shoot", "point & shoot", "compact film camera"), "/collections/point-shoot-cameras"),
    (("develop", "processing", "film lab", "scan"), "/film-services"),
    (("pentax k1000", "k1000"), "/products/pentax-k-1000-with-50mm-lens-1"),
]

def target(q):
    ql = " " + q.lower() + " "
    qt = toks(q)
    if any(t in BRAND for t in qt) or "long beach" in ql:
        return "/"
    for keys, page in RULES[:2]:
        if any(k in ql for k in keys):
            return page
    core = [t for t in qt if t not in STOP]
    best = None
    if core:
        for p, ix in IDX:
            if all(t in ix for t in core):
                sc = -build.rank_of(p) + (50 if n(q) in n(p["name"]) else 0) - len(ix) * 0.01
                if not best or sc > best[0]:
                    best = (sc, "/products/" + p["slug"])
    if best:
        return best[1]
    for keys, page in RULES[2:]:
        if any(k in ql for k in keys):
            return page
    return None

def main():
    out = {}
    unmapped = 0
    for q, clicks, impr, ctr, pos in G:
        t = target(q)
        if not t:
            unmapped += 1
            continue
        out.setdefault(t, []).append([q, int(clicks), int(impr)])
    for k in out:
        out[k].sort(key=lambda r: (-r[1], -r[2]))
    json.dump(out, open(os.path.join(ROOT, "data", "gsc_keywords.json"), "w"), indent=0)
    print(f"mapped {sum(len(v) for v in out.values())} queries to {len(out)} pages; {unmapped} unmapped")

if __name__ == "__main__":
    main()
