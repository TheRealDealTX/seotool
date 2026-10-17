#!/usr/bin/env python3
"""Build "related verses" from OpenBible.info cross references (CC BY).

Source: https://a.openbible.info/data/cross-references.zip (cached in sources/cache/).
Each pair carries community votes; we keep the best MAX_PER_VERSE with at least
MIN_VOTES per verse.

Output: public/data/related/<book>.json  {"r": [[["<bookIndex>.<ch>.<v>[-<endV>]", votes], ...] per verse] per chapter}
Run:  python3 tools/build_related.py
"""
import io
import json
import re
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "sources" / "cache" / "openbible-cross-references.txt"
OUT = ROOT / "public" / "data" / "related"
URL = "https://a.openbible.info/data/cross-references.zip"
MAX_PER_VERSE, MIN_VOTES = 10, 3
OSIS = ("Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov "
        "Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal Matt Mark "
        "Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet "
        "2Pet 1John 2John 3John Jude Rev").split()
IDX = {b: i for i, b in enumerate(OSIS)}


def parse(ref):
    m = re.fullmatch(r"([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)", ref)
    return (IDX[m[1]], int(m[2]), int(m[3])) if m and m[1] in IDX else None


def main():
    if not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL, timeout=120).read()))
        CACHE.write_bytes(z.read("cross_references.txt"))
    books = json.loads((ROOT / "public" / "data" / "books.json").read_text(encoding="utf-8"))
    rel = {}
    for line in CACHE.read_text(encoding="utf-8").splitlines()[1:]:
        f = line.split("\t")
        if len(f) < 3 or not f[2].lstrip("-").isdigit() or int(f[2]) < MIN_VOTES:
            continue
        src = parse(f[0])
        a, _, b = f[1].partition("-")
        dst, end = parse(a), parse(b) if b else None
        if not src or not dst:
            continue
        bi, c, v = dst
        if not (c <= len(books[bi]["verses"]) and v <= books[bi]["verses"][c - 1]):
            continue
        key = f"{bi}.{c}.{v}" + (f"-{end[2]}" if end and end[:2] == dst[:2] and end[2] > v else "")
        rel.setdefault(src, []).append((int(f[2]), key))
    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for bi, b in enumerate(books):
        chapters = []
        for c, n in enumerate(b["verses"], 1):
            row = []
            for v in range(1, n + 1):
                best = sorted(rel.get((bi, c, v), []), reverse=True)[:MAX_PER_VERSE]
                row.append([[k, votes] for votes, k in best])
                total += len(best)
            chapters.append(row)
        (OUT / f"{b['slug']}.json").write_text(json.dumps({"r": chapters}, separators=(",", ":")), encoding="utf-8")
    print(f"related links kept: {total}")


if __name__ == "__main__":
    main()
