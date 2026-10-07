"""Tiny Markdown subset renderer for content/posts/*.md (see CONTENT_GUIDE.md)."""
import html
import re

WIDGET_RE = re.compile(r"^\{\{widget:([a-z0-9-]+)\}\}$")


def parse_front(text):
    if not text.startswith("---"):
        raise ValueError("missing front matter")
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body.strip()


def slugify(s):
    s = re.sub(r"<[^>]+>", "", s).lower()
    s = re.sub(r"&[a-z]+;", "", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60]


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _link, s)
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def _link(m):
    text, url = m.group(1), m.group(2)
    if url.startswith("http") and "cebudavao.com" not in url:
        return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'
    url = re.sub(r"^https?://(www\.)?cebudavao\.com", "", url)
    return f'<a href="{url}">{text}</a>'


def render(body, widget_fn):
    """Return (html, headings[(id,text)], faqs[(q,a)], sections{name: [lines]})."""
    lines = body.splitlines()
    out, headings, faqs = [], [], []
    i, in_faq = 0, False
    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        st = line.strip()
        if not st:
            flush(); i += 1; continue
        w = WIDGET_RE.match(st)
        if w:
            flush(); out.append(widget_fn(w.group(1))); i += 1; continue
        if st.startswith("## "):
            flush()
            text = st[3:].strip()
            hid = slugify(text)
            in_faq = "frequently asked" in text.lower() or text.lower() in ("faq", "faqs")
            headings.append((hid, text))
            out.append(f'<h2 id="{hid}">{inline(text)}</h2>')
            if in_faq:
                out[-1] = f'<h2 id="{hid}" class="faq-title">{inline(text)}</h2>'
            i += 1; continue
        if st.startswith("### "):
            flush()
            text = st[4:].strip()
            if in_faq:
                # collect answer paragraphs until next heading
                j, ans = i + 1, []
                while j < len(lines) and not lines[j].strip().startswith("#"):
                    ans.append(lines[j].strip()); j += 1
                answer = " ".join(a for a in ans if a)
                faqs.append((text, answer))
                out.append(f'<details class="faq"><summary>{inline(text)}</summary><p>{inline(answer)}</p></details>')
                i = j; continue
            out.append(f'<h3 id="{slugify(text)}">{inline(text)}</h3>')
            i += 1; continue
        if re.match(r"^[-*] ", st):
            flush(); items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                items.append(lines[i].strip()[2:]); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\d+[.)] ", st):
            flush(); items = []
            while i < len(lines) and re.match(r"^\s*\d+[.)] ", lines[i]):
                items.append(re.sub(r"^\s*\d+[.)] ", "", lines[i])); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        if st.startswith(">"):
            flush(); q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip().lstrip(">").strip()); i += 1
            out.append('<aside class="callout"><p>' + inline(" ".join(q)) + "</p></aside>")
            continue
        if st.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            out.append(_table(rows))
            continue
        para.append(st); i += 1
    flush()
    return "\n".join(out), headings, faqs


def _table(rows):
    cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
    head = cells[0]
    body = [r for r in cells[1:] if not all(re.fullmatch(r":?-{2,}:?", c or "--") for c in r)]
    h = "".join(f"<th scope=\"col\">{inline(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="table-wrap"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def section_items(body, name):
    """Return list items under '## name' (used for recipe ingredients/instructions)."""
    m = re.search(r"^##\s+" + name + r"[^\n]*\n(.*?)(?=^##\s|\Z)", body, re.M | re.S | re.I)
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        s = line.strip()
        if re.match(r"^([-*]|\d+[.)]) ", s):
            items.append(re.sub(r"\*\*|\*|\[([^\]]+)\]\([^)]+\)", lambda x: x.group(1) or "", re.sub(r"^([-*]|\d+[.)]) ", "", s)))
    return items
