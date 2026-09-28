"""Markdown-lite renderer for SmokeDamage.com content files.

Supports the syntax documented in CONTENT-SPEC.md: front matter, H2/H3,
paragraphs, lists, pipe tables, inline bold/italic/links, {{tokens}} and the
:::block components (cta, note, faq, cards, steps, checklist, sources, figure).

The renderer returns HTML plus the structured data the page layout needs
(FAQ pairs for schema, H2 list for the table of contents, word count).
"""

import html
import re

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text):
    return SLUG_RE.sub("-", text.lower()).strip("-")


def parse_front_matter(raw):
    """Split `---` front matter from the body. Returns (meta, body)."""
    meta = {}
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            block = raw[3:end].strip("\n")
            body = raw[end + 4:]
            for line in block.splitlines():
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                if ":" in line:
                    k, v = line.split(":", 1)
                    v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                        v = v[1:-1]
                    meta[k.strip()] = v
            return meta, body.lstrip("\n")
    return meta, raw


class Renderer:
    """Converts one content body to HTML. `ctx` provides tokens and helpers."""

    def __init__(self, ctx):
        self.ctx = ctx
        self.faqs = []
        self.toc = []
        self.ids = set()

    # ---------------------------------------------------------------- inline
    def inline(self, text):
        text = html.escape(text, quote=False)
        # tokens
        text = text.replace("{{phone}}", self.ctx["phone_link"])
        text = text.replace("{{email}}", self.ctx["email_link"])
        text = text.replace("{{review}}", self.ctx["review_link"])
        # links [text](url)
        def link(m):
            label, href = m.group(1), m.group(2).strip()
            href_attr = href.replace('"', "%22")
            if href.startswith("http") and "smokedamage.com" not in href:
                return f'<a href="{href_attr}" rel="noopener" target="_blank">{label}</a>'
            if href.startswith("tel:"):
                return f'<a href="{href_attr}" data-track="phone">{label}</a>'
            if href.startswith("mailto:"):
                return f'<a href="{href_attr}" data-track="email">{label}</a>'
            return f'<a href="{href_attr}">{label}</a>'
        text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        # restore any raw HTML the tokens injected (they were inserted after escaping)
        return text

    def heading_id(self, text):
        base = slugify(re.sub(r"<[^>]+>", "", text))[:60] or "section"
        hid, n = base, 2
        while hid in self.ids:
            hid, n = f"{base}-{n}", n + 1
        self.ids.add(hid)
        return hid

    # ---------------------------------------------------------------- blocks
    def render(self, body):
        lines = body.replace("\r\n", "\n").split("\n")
        return self.render_lines(lines, top=True)

    def render_lines(self, lines, top=False):
        out = []
        i = 0
        n = len(lines)
        while i < n:
            line = lines[i]
            s = line.strip()
            if not s:
                i += 1
                continue
            if s.startswith(":::") and len(s) > 3:
                name, _, arg = s[3:].partition(" ")
                j = i + 1
                depth = 1
                while j < n:
                    t = lines[j].strip()
                    if t == ":::":
                        depth -= 1
                        if depth == 0:
                            break
                    elif t.startswith(":::") and len(t) > 3:
                        depth += 1
                    j += 1
                out.append(self.block(name.strip(), arg.strip(), lines[i + 1:j]))
                i = j + 1
                continue
            if s.startswith("<") and not s.startswith("<http"):
                # raw HTML passthrough (single paragraph)
                buf = []
                while i < n and lines[i].strip():
                    buf.append(lines[i])
                    i += 1
                out.append("\n".join(buf))
                continue
            m = re.match(r"^(#{2,4})\s+(.*)$", s)
            if m:
                level = len(m.group(1))
                text = self.inline(m.group(2).strip())
                hid = self.heading_id(text)
                if level == 2 and top:
                    self.toc.append((hid, re.sub(r"<[^>]+>", "", text)))
                out.append(f'<h{level} id="{hid}">{text}</h{level}>')
                i += 1
                continue
            if s.startswith("|"):
                buf = []
                while i < n and lines[i].strip().startswith("|"):
                    buf.append(lines[i].strip())
                    i += 1
                out.append(self.table(buf))
                continue
            if re.match(r"^[-*]\s+", s):
                buf = []
                while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                    buf.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                    i += 1
                    while i < n and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^\s*[-*]\s+", lines[i]):
                        buf[-1] += " " + lines[i].strip()
                        i += 1
                out.append("<ul>" + "".join(f"<li>{self.inline(x)}</li>" for x in buf) + "</ul>")
                continue
            if re.match(r"^\d+[.)]\s+", s):
                buf = []
                while i < n and re.match(r"^\s*\d+[.)]\s+", lines[i]):
                    buf.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i]))
                    i += 1
                    while i < n and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^\s*\d+[.)]\s+", lines[i]):
                        buf[-1] += " " + lines[i].strip()
                        i += 1
                out.append("<ol>" + "".join(f"<li>{self.inline(x)}</li>" for x in buf) + "</ol>")
                continue
            if s.startswith(">"):
                buf = []
                while i < n and lines[i].strip().startswith(">"):
                    buf.append(lines[i].strip().lstrip(">").strip())
                    i += 1
                out.append(f'<blockquote><p>{self.inline(" ".join(buf))}</p></blockquote>')
                continue
            # paragraph
            buf = []
            while i < n:
                t = lines[i].strip()
                if (not t or t.startswith(":::") or re.match(r"^#{2,4}\s", t) or t.startswith("|")
                        or re.match(r"^[-*]\s+", t) or re.match(r"^\d+[.)]\s+", t) or t.startswith(">")):
                    break
                buf.append(t)
                i += 1
            out.append(f"<p>{self.inline(' '.join(buf))}</p>")
        return "\n".join(out)

    def table(self, rows):
        def cells(r):
            r = r.strip()
            if r.startswith("|"):
                r = r[1:]
            if r.endswith("|"):
                r = r[:-1]
            return [c.strip() for c in r.split("|")]
        rows = [r for r in rows]
        head = cells(rows[0])
        body = [cells(r) for r in rows[1:] if not re.match(r"^\|?\s*:?-{2,}", r.strip().lstrip("|").strip())]
        h = "".join(f'<th scope="col">{self.inline(c)}</th>' for c in head)
        b = "".join("<tr>" + "".join(f"<td>{self.inline(c)}</td>" for c in r) + "</tr>" for r in body)
        return f'<div class="table-wrap"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'

    def split_items(self, lines):
        """Split block content on ### headings → [(title, [lines])]."""
        items, cur = [], None
        for line in lines:
            m = re.match(r"^\s*###\s+(.*)$", line)
            if m:
                cur = [m.group(1).strip(), []]
                items.append(cur)
            elif cur is not None:
                cur[1].append(line)
        return items

    def block(self, name, arg, lines):
        ctx = self.ctx
        if name == "cta":
            title = arg or "Request a closer review of your smoke or fire claim"
            body = self.render_lines(lines) if any(l.strip() for l in lines) else \
                "<p>Tell us what happened and where the claim stands. A licensed Texas public adjuster can review the situation with you.</p>"
            return ctx["cta_banner"](self.inline(title), body)
        if name == "note":
            title = f"<p class=\"note-title\">{self.inline(arg)}</p>" if arg else ""
            return f'<aside class="note">{title}{self.render_lines(lines)}</aside>'
        if name == "faq":
            items = self.split_items(lines)
            parts = []
            for q, a in items:
                ans_html = self.render_lines(a)
                self.faqs.append((re.sub(r"<[^>]+>", "", self.inline(q)), ans_html))
                parts.append(f'<details class="faq-item"><summary><span>{self.inline(q)}</span></summary>'
                             f'<div class="faq-answer">{ans_html}</div></details>')
            return '<div class="faq-list">' + "".join(parts) + "</div>"
        if name == "cards":
            items = self.split_items(lines)
            cards = []
            for title, body in items:
                href = None
                clean = []
                for l in body:
                    m = re.match(r"^\s*->\s*(\S+)\s*$", l)
                    if m:
                        href = m.group(1)
                    else:
                        clean.append(l)
                inner = f"<h3>{self.inline(title)}</h3>{self.render_lines(clean)}"
                if href:
                    cards.append(f'<a class="card card-link" href="{href}">{inner}<span class="card-more" aria-hidden="true">Learn more →</span></a>')
                else:
                    cards.append(f'<div class="card">{inner}</div>')
            return '<div class="card-grid">' + "".join(cards) + "</div>"
        if name == "steps":
            items = self.split_items(lines)
            li = "".join(f'<li><div class="step-num" aria-hidden="true">{k:02d}</div><div><h3>{self.inline(t)}</h3>{self.render_lines(b)}</div></li>'
                         for k, (t, b) in enumerate(items, 1))
            return f'<ol class="steps">{li}</ol>'
        if name == "checklist":
            title = f'<p class="note-title">{self.inline(arg)}</p>' if arg else ""
            return f'<div class="checklist">{title}{self.render_lines(lines)}</div>'
        if name == "sources":
            return f'<aside class="sources"><p class="note-title">Sources</p>{self.render_lines(lines)}</aside>'
        if name == "figure":
            cap = " ".join(l.strip() for l in lines if l.strip())
            return ctx["figure"](arg, self.inline(cap) if cap else "")
        # unknown block: render contents
        return self.render_lines(lines)


def word_count(html_text):
    text = re.sub(r"<[^>]+>", " ", html_text)
    return len(re.findall(r"[A-Za-z0-9’'-]+", text))
