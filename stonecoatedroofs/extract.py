"""One-off: turn the WordPress REST export in backup/ into clean content/wp.json.

Run once after a fresh backup; build.py reads content/wp.json and never touches
the backup. Bodies are sanitised to a small tag allowlist, site-absolute links
become root-relative, and media URLs point at the mirrored /wp-content/uploads/.
"""

import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API = ROOT / "backup" / "wordpress-2026-10-06" / "api"
OUT = ROOT / "content" / "wp.json"
ORIGIN = "https://stonecoatedroofs.com"

ALLOWED = {
    "h2": (), "h3": (), "h4": (), "p": (), "ul": (), "ol": (), "li": (),
    "strong": (), "em": (), "b": (), "i": (), "br": (), "blockquote": (),
    "table": (), "thead": (), "tbody": (), "tr": (), "th": ("colspan", "rowspan"),
    "td": ("colspan", "rowspan"), "a": ("href",), "figure": (), "figcaption": (),
    "img": ("src", "width", "height", "alt"),
}
VOID = {"br", "img"}
DROP_WITH_CONTENT = {"style", "script", "svg", "noscript", "form", "iframe"}


def clean_alt(alt):
    alt = re.sub(r"\s*\(\d+\)\s*$", "", alt or "").strip()
    return alt[:1].upper() + alt[1:] if alt else alt


def local(url):
    if url.startswith(ORIGIN):
        url = url[len(ORIGIN):] or "/"
    return url


class Sanitiser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out, self.drop, self.stack = [], 0, []

    def handle_starttag(self, tag, attrs):
        if tag in DROP_WITH_CONTENT:
            self.drop += 1
            return
        if self.drop or tag not in ALLOWED:
            return
        a = dict(attrs)
        keep = []
        for k in ALLOWED[tag]:
            v = a.get(k)
            if v is None:
                continue
            if k in ("href", "src"):
                v = local(v)
            if k == "alt":
                v = clean_alt(v)
            keep.append(f'{k}="{html.escape(v, quote=True)}"')
        if tag == "img":
            if not a.get("alt"):
                keep.append(f'alt="{html.escape(clean_alt(re.sub(r"[-_]", " ", a.get("src", "").rsplit("/", 1)[-1].rsplit(".", 1)[0])), quote=True)}"')
            keep.append('loading="lazy" decoding="async"')
        self.out.append(f"<{tag}{(' ' + ' '.join(keep)) if keep else ''}>")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.drop -= 1
            return
        if self.drop or tag not in ALLOWED or tag in VOID:
            return
        if tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.out.append(f"</{t}>")
                if t == tag:
                    break

    def handle_data(self, d):
        if not self.drop:
            self.out.append(d)

    def handle_entityref(self, name):
        if not self.drop:
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self.drop:
            self.out.append(f"&#{name};")


def sanitise(raw):
    s = Sanitiser()
    s.feed(raw)
    body = "".join(s.out)
    # headings never need <strong>; WordPress wraps nearly all of them
    body = re.sub(r"<(h[2-4])>\s*<strong>(.*?)</strong>\s*</\1>", r"<\1>\2</\1>", body, flags=re.S)
    body = re.sub(r"<(h[2-4])>\s*<b>(.*?)</b>\s*</\1>", r"<\1>\2</\1>", body, flags=re.S)
    body = re.sub(r"<p>(\s|&nbsp;|<br>)*</p>", "", body)
    body = re.sub(r"<figure>\s*(<table>.*?</table>)\s*</figure>", r'<div class="table-wrap">\1</div>', body, flags=re.S)
    # tables whose first row is bold labels -> make it a real header row
    def thead(m):
        t = m.group(0)
        first = re.search(r"<tbody>\s*<tr>(.*?)</tr>", t, flags=re.S)
        if first and "<th" not in t and all(
                re.fullmatch(r"\s*<strong>.*?</strong>\s*", c, flags=re.S)
                for c in re.findall(r"<td[^>]*>(.*?)</td>", first.group(1), flags=re.S)):
            cells = re.sub(r"<td([^>]*)>\s*<strong>(.*?)</strong>\s*</td>", r"<th\1>\2</th>", first.group(1), flags=re.S)
            t = t.replace(first.group(0), f"<thead><tr>{cells}</tr></thead><tbody>", 1)
        return t
    body = re.sub(r"<table>.*?</table>", thead, body, flags=re.S)
    # Gutenberg posts jump h2 -> h4; close the gap so the outline is h2 -> h3
    if "<h3>" not in body:
        body = body.replace("<h4>", "<h3>").replace("</h4>", "</h3>")
    body = re.sub(r"\n\s*\n+", "\n", body).strip()
    body = re.sub(r"\?utm_source=[^\"&]*", "", body)
    # runs of adjacent links to the same URL (an editor artefact) -> one link
    body = re.sub(r'(?:(?:<strong>)?<a href="([^"]+)">(?:<strong>)?[^<]*(?:</strong>)?</a>(?:</strong>)?){2,}',
                  lambda m: '<a href="%s"><strong>%s</strong></a>' % (m.group(1), re.sub(r"<[^>]+>", "", m.group(0)))
                  if len(set(re.findall(r'href="([^"]+)"', m.group(0)))) == 1 else m.group(0), body)
    body = re.sub(r"(\w)<a href", r"\1 <a href", body)
    for old, new in FIXES:
        body = body.replace(old, new)
    return body


# Stray editorial text found in the WordPress copy
FIXES = [
    (" The site design and positioning for your new brand already reinforce durability, premium aesthetics, and Texas-specific performance expectations.", ""),
]


def unent(s):
    return html.unescape(s or "").strip()


def seo_title(y, fallback):
    t = unent(y.get("title")) or fallback
    return re.sub(r"\s+[—–-]\s+Stone Coated Roofs$", "", t)


def entry(item, kind):
    y = item.get("yoast_head_json") or {}
    og = (y.get("og_image") or [{}])[0]
    link = item["link"]
    return {
        "id": item["id"],
        "kind": kind,
        "slug": item["slug"],
        "path": local(link),
        "title": unent(item["title"]["rendered"]),
        "seo_title": seo_title(y, unent(item["title"]["rendered"])),
        "description": unent(y.get("description")),
        "date": item["date"][:10],
        "modified": item["modified"][:10],
        "categories": item.get("categories", []),
        "image": {"src": local(og["url"]), "width": og.get("width"), "height": og.get("height")} if og.get("url") else None,
        "excerpt": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", unent(item["excerpt"]["rendered"]))).replace(" [&hellip;]", "").replace("[…]", "").strip(),
        "body": sanitise(item["content"]["rendered"]),
    }


def main():
    pages = json.loads((API / "pages.json").read_text())
    posts = json.loads((API / "posts.json").read_text())
    cats = json.loads((API / "cats.json").read_text())
    out = {"pages": [], "posts": [], "categories": []}
    for p in pages:
        kind = "area" if p["parent"] == 23 else "page"
        out["pages"].append(entry(p, kind))
    for p in posts:
        out["posts"].append(entry(p, "post"))
    for c in cats:
        out["categories"].append({"id": c["id"], "slug": c["slug"], "name": c["name"],
                                  "path": local(c["link"]), "description": unent(c.get("description"))})
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"pages={len(out['pages'])} posts={len(out['posts'])} categories={len(out['categories'])} -> {OUT}")


if __name__ == "__main__":
    main()
