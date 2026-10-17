#!/usr/bin/env python3
"""Build verse commentaries from public-domain SWORD modules (CrossWire).

  MHCC  Matthew Henry's Concise Commentary (passage by passage)
  JFB   Jamieson-Fausset-Brown Bible Commentary (verse notes)

Output: public/data/commentary/<mod>/<book>.json
  {"e": [html, ...],            distinct commentary entries of the book
   "m": [[i | -1, ...], ...]}   per chapter, per verse: index into "e"
A verse without its own entry is covered by the entry before it in the same
chapter (both modules store a passage once, under its first verse).

Run:  python3 tools/build_commentary.py      (downloads the modules on first run)
"""
import html
import io
import json
import re
import sys
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sword import read_module  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "sources" / "cache"
OUT = ROOT / "public" / "data" / "commentary"
MODULES = {
    "mhcc": ("MHCC", "modules/comments/zcom/mhcc", False),
    "jfb": ("JFB", "modules/comments/zcom/jfb", True),
}
URL = "https://www.crosswire.org/ftpmirror/pub/sword/packages/rawzip/{}.zip"

OSIS_BOOKS = ("Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov "
              "Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal Matt Mark "
              "Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet "
              "2Pet 1John 2John 3John Jude Rev").split()


class OsisToHtml(HTMLParser):
    """OSIS fragment -> small, safe HTML (p, strong, em, h4, br, a)."""

    def __init__(self, slugs):
        super().__init__(convert_charrefs=True)
        self.slugs = slugs
        self.out = []
        self.stack = []        # what each open OSIS element became
        self.skip = 0          # inside <note>

    def emit(self, s):
        if not self.skip:
            self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "note":
            self.skip += 1; self.stack.append("note"); return
        if tag == "div":
            if "sid" in a and a.get("type") in ("x-p", "paragraph"):
                self.emit("<p>")
            elif "eid" in a and a.get("type") in ("x-p", "paragraph"):
                self.emit("</p>")
            self.stack.append(None)
            return
        if tag == "title":
            self.emit("<h4>"); self.stack.append("h4"); return
        if tag == "hi":
            t = "strong" if a.get("type") == "bold" else "em"
            self.emit(f"<{t}>"); self.stack.append(t); return
        if tag == "reference":
            href = self.ref_url(a.get("osisref", ""))
            if href:
                self.emit(f'<a href="{href}">'); self.stack.append("a"); return
            self.stack.append(None); return
        if tag in ("lb", "br"):
            self.emit("<br>"); return
        if tag == "l":
            self.stack.append("lbr"); return
        self.stack.append(None)

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if tag == "div" and a.get("type") in ("x-p", "paragraph"):
            self.emit("<p>" if "sid" in a else "</p>")
        elif tag in ("lb", "br"):
            self.emit("<br>")

    def handle_endtag(self, tag):
        if not self.stack:
            return
        t = self.stack.pop()
        if t == "note":
            self.skip -= 1
        elif t == "lbr":
            self.emit("<br>")
        elif t:
            self.emit(f"</{t}>")

    def handle_data(self, data):
        self.emit(html.escape(data, quote=False))

    def ref_url(self, osis):
        m = re.match(r"(?:\w+:)?([1-3]?[A-Za-z]+)\.(\d+)(?:\.(\d+))?", osis)
        if not m or m.group(1) not in OSIS_BOOKS:
            return None
        slug = self.slugs[OSIS_BOOKS.index(m.group(1))]
        return f"/ta/{slug}/{m.group(2)}/" + (f"{m.group(3)}/" if m.group(3) else "")


def to_html(osis, slugs):
    p = OsisToHtml(slugs)
    p.feed(osis)
    p.close()
    h = "".join(p.out)
    # tidy: drop empty paragraphs/headings, balance stray <p>, collapse whitespace
    h = re.sub(r"\s+", " ", h)
    h = re.sub(r"<p>\s*(?=<p>)", "", h)
    h = re.sub(r"<(p|h4|strong|em)>\s*</\1>", "", h)
    h = re.sub(r"(<br>\s*){3,}", "<br><br>", h)
    if h.count("<p>") > h.count("</p>"):
        h += "</p>" * (h.count("<p>") - h.count("</p>"))
    return h.strip()


def module_dir(name, subdir):
    d = CACHE / f"sword-{name}"
    if not (d / subdir).exists():
        print("downloading", name)
        raw = urllib.request.urlopen(URL.format(name), timeout=180).read()
        zipfile.ZipFile(io.BytesIO(raw)).extractall(d)
    return d / subdir


def main():
    books = json.loads((ROOT / "public" / "data" / "books.json").read_text(encoding="utf-8"))
    canon = [(b["slug"], b["verses"]) for b in books]
    slugs = [b["slug"] for b in books]
    for mod, (name, subdir, size4) in MODULES.items():
        data = read_module(module_dir(name, subdir), canon, size4)
        d = OUT / mod
        d.mkdir(parents=True, exist_ok=True)
        total = 0
        for slug, counts in canon:
            entries, index, maps = [], {}, []
            for c, n in enumerate(counts, 1):
                row = []
                for v in range(1, n + 1):
                    e = data.get((slug, c, v))
                    if not e:
                        row.append(-1); continue
                    key, osis = e
                    if key not in index:
                        h = to_html(osis, slugs)
                        if not re.sub(r"<[^>]+>|\s", "", h):
                            row.append(-1); continue
                        index[key] = len(entries); entries.append(h)
                    row.append(index[key])
                maps.append(row)
            total += len(entries)
            (d / f"{slug}.json").write_text(json.dumps({"e": entries, "m": maps}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"{name}: {total} entries")


if __name__ == "__main__":
    main()
