"""Drawing backends. Views draw in model feet inside a view transform; sheet furniture
(title blocks, tables) draws in paper inches. Line styles are named, and each backend maps
a name to color, weight, dash pattern and CAD layer.

  PdfCanvas  - ARCH D / tabloid sheets through reportlab (the printed plan set)
  SvgCanvas  - web previews in the site's blueprint colors
  DxfCanvas  - AutoCAD R12 DXF at full scale, inches, one layer per style
"""
from __future__ import annotations

import math
from xml.sax.saxutils import escape

from thb_model import PROFILE

# name: (print color, blueprint color, weight in pt, dash, layer)
STYLES = {
    "wall":      ("#1f2a30", "#e8f2f2", 0.6, None, "A-WALL"),
    "wallfill":  ("#3b474d", "#e8f2f2", 0.0, None, "A-WALL-PATT"),
    "wall_lt":   ("#9aa6ab", "#5d8a92", 0.4, None, "A-WALL"),
    "wallfill_lt": ("#c9d1d4", "#3f6d75", 0.0, None, "A-WALL-PATT"),
    "door":      ("#1f2a30", "#f2c58d", 0.5, None, "A-DOOR"),
    "swing":     ("#5b6b72", "#f2c58d", 0.3, None, "A-DOOR"),
    "window":    ("#1f2a30", "#9fe0dc", 0.45, None, "A-GLAZ"),
    "fixture":   ("#36444b", "#cfe3e3", 0.4, None, "A-FLOR-FIXT"),
    "fixture_lt": ("#a8b3b7", "#55808a", 0.3, None, "A-FLOR-FIXT"),
    "furn":      ("#a5b0b5", "#5d8a92", 0.3, None, "A-FURN"),
    "hidden":    ("#5b6b72", "#9fe0dc", 0.4, (4, 3), "A-HIDD"),
    "dim":       ("#33505a", "#9fe0dc", 0.3, None, "A-ANNO-DIMS"),
    "text":      ("#1f2a30", "#cfe3e3", 0.3, None, "A-ANNO-TEXT"),
    "text_lt":   ("#7d8a90", "#7fb3b8", 0.3, None, "A-ANNO-TEXT"),
    "title":     ("#0f5f66", "#f2c58d", 0.3, None, "A-ANNO-TTLB"),
    "accent":    ("#b8742a", "#f2c58d", 0.5, None, "A-ANNO-NOTE"),
    "border":    ("#1f2a30", "#e8f2f2", 1.2, None, "A-ANNO-TTLB"),
    "thin":      ("#1f2a30", "#cfe3e3", 0.35, None, "A-ANNO-TTLB"),
    "grid":      ("#d5dcdf", "#28545c", 0.25, None, "A-ANNO-TTLB"),
    "elec":      ("#c0392b", "#ffb36b", 0.5, None, "E-POWR"),
    "elec_lt":   ("#c0392b", "#ffb36b", 0.35, (3, 2), "E-LITE-CIRC"),
    "elec_text": ("#9a2a1f", "#ffcf99", 0.3, None, "E-ANNO-TEXT"),
    "cold":      ("#1f6fd1", "#6fb6ff", 0.8, None, "P-DOMW-CWTR"),
    "hot":       ("#d1361f", "#ff7a6b", 0.8, (5, 2.5), "P-DOMW-HOTW"),
    "waste":     ("#1d8a4a", "#7be3a0", 1.4, None, "P-SANR-PIPE"),
    "vent":      ("#1d8a4a", "#7be3a0", 0.6, (2, 2), "P-SANR-VENT"),
    "plumb_text": ("#145f34", "#a6f0c2", 0.3, None, "P-ANNO-TEXT"),
    "struct":    ("#1f2a30", "#e8f2f2", 0.5, None, "S-FRAM"),
    "struct_lt": ("#7d8a90", "#7fb3b8", 0.3, None, "S-FRAM"),
    "concrete":  ("#1f2a30", "#e8f2f2", 0.6, None, "S-FNDN"),
    "earth":     ("#7d6a50", "#9fe0dc", 0.5, None, "A-ANNO-GRAD"),
    "watermark": ("#0f5f66", "#f2c58d", 0.3, None, "A-ANNO-WMRK"),
}


def _rgb(hexcolor):
    h = hexcolor.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


class Canvas:
    """Base class: view transform from model feet to paper inches."""
    theme = "print"

    def __init__(self):
        self.ox = self.oy = 0.0
        self.s = 1.0           # paper inches per model foot (1.0 = paper space)
        self.in_view = False

    # --- transforms -------------------------------------------------------------------
    def view(self, ox, oy, s):
        self.ox, self.oy, self.s, self.in_view = ox, oy, s, True

    def paper(self):
        self.ox, self.oy, self.s, self.in_view = 0.0, 0.0, 1.0, False

    def P(self, x, y):
        return self.ox + x * self.s, self.oy + y * self.s

    def color(self, st):
        c = STYLES[st]
        return c[0] if self.theme == "print" else c[1]

    # --- primitives, all in current coordinates -----------------------------------------
    def line(self, x1, y1, x2, y2, st="thin"):
        self.poly([(x1, y1), (x2, y2)], st)

    def rect(self, x, y, w, h, st="thin", fill=None):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], st, closed=True, fill=fill)

    def arc(self, cx, cy, r, a0, a1, st="thin"):
        n = max(6, int(abs(a1 - a0) / 6))
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        self.poly(pts, st)

    def curve(self, p0, p1, bulge, st):
        """Quadratic arc between two points, bowed sideways by bulge (model units)."""
        (x0, y0), (x1, y1) = p0, p1
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1
        cx, cy = mx - dy / L * bulge, my + dx / L * bulge
        pts = []
        for i in range(13):
            t = i / 12
            pts.append(((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1))
        self.poly(pts, st)

    def poly(self, pts, st="thin", closed=False, fill=None):
        raise NotImplementedError

    def shape(self, pts, fill_hex, stroke_hex=None, lw=0.15):
        """Filled polygon in a literal color (used for shaded 3D renders)."""
        raise NotImplementedError

    def circle(self, cx, cy, r, st="thin", fill=None):
        raise NotImplementedError

    def text(self, x, y, t, size=0.1, st="text", anchor="middle", bold=False, rot=0):
        """size is the cap height in paper inches regardless of the view scale."""
        raise NotImplementedError


# ---------------------------------------------------------------------------------------

class PdfCanvas(Canvas):
    def __init__(self, path, width_in, height_in, title=""):
        super().__init__()
        from reportlab.pdfgen import canvas as rl
        self.W, self.H = width_in, height_in
        self.c = rl.Canvas(path, pagesize=(width_in * 72, height_in * 72))
        self.c.setTitle(title)
        self.c.setAuthor(PROFILE["brand_name"])
        self.c.setCreator(PROFILE["brand_name"] + " plan generator")

    def _pt(self, x, y):
        px, py = self.P(x, y)
        return px * 72, py * 72

    def _style(self, st):
        _, _, w, dash, _ = STYLES[st]
        self.c.setStrokeColorRGB(*_rgb(self.color(st)))
        self.c.setLineWidth(w)
        self.c.setDash(dash or [])
        self.c.setLineJoin(1)
        self.c.setLineCap(1 if not dash else 0)

    def poly(self, pts, st="thin", closed=False, fill=None):
        self._style(st)
        p = self.c.beginPath()
        x, y = self._pt(*pts[0])
        p.moveTo(x, y)
        for q in pts[1:]:
            p.lineTo(*self._pt(*q))
        if closed:
            p.close()
        stroke = STYLES[st][2] > 0
        if fill:
            self.c.setFillColorRGB(*_rgb(self.color(fill) if fill in STYLES else fill))
        self.c.drawPath(p, stroke=1 if stroke else 0, fill=1 if fill else 0)

    def shape(self, pts, fill_hex, stroke_hex=None, lw=0.15):
        p = self.c.beginPath()
        p.moveTo(*self._pt(*pts[0]))
        for q in pts[1:]:
            p.lineTo(*self._pt(*q))
        p.close()
        self.c.setDash([])
        self.c.setLineJoin(1)
        self.c.setFillColorRGB(*_rgb(fill_hex))
        self.c.setStrokeColorRGB(*_rgb(stroke_hex or fill_hex))
        self.c.setLineWidth(lw)
        self.c.drawPath(p, stroke=1, fill=1)

    def circle(self, cx, cy, r, st="thin", fill=None):
        self._style(st)
        x, y = self._pt(cx, cy)
        if fill:
            self.c.setFillColorRGB(*_rgb(self.color(fill) if fill in STYLES else fill))
        self.c.circle(x, y, r * self.s * 72, stroke=1, fill=1 if fill else 0)

    def text(self, x, y, t, size=0.1, st="text", anchor="middle", bold=False, rot=0):
        px, py = self._pt(x, y)
        fs = size * 72 / 0.72          # cap height -> font size
        self.c.saveState()
        self.c.setFillColorRGB(*_rgb(self.color(st)))
        self.c.setFont("Helvetica-Bold" if bold else "Helvetica", fs)
        self.c.translate(px, py)
        if rot:
            self.c.rotate(rot)
        if anchor == "middle":
            self.c.drawCentredString(0, 0, t)
        elif anchor == "end":
            self.c.drawRightString(0, 0, t)
        else:
            self.c.drawString(0, 0, t)
        self.c.restoreState()

    def text_width(self, t, size, bold=False):
        from reportlab.pdfbase.pdfmetrics import stringWidth
        return stringWidth(t, "Helvetica-Bold" if bold else "Helvetica", size * 72 / 0.72) / 72

    def page(self):
        self.c.showPage()

    def save(self):
        self.c.save()


# ---------------------------------------------------------------------------------------

class SvgCanvas(Canvas):
    """Web preview. Paper inches map to 96 px; y is flipped so the plan front is at the bottom."""
    theme = "blueprint"
    PX = 96

    def __init__(self, width_in, height_in, title="", theme="blueprint", bg=True):
        super().__init__()
        self.theme = theme
        self.W, self.H = width_in, height_in
        self.title = title
        self.out = []
        self.bg = bg

    def _xy(self, x, y):
        px, py = self.P(x, y)
        return px * self.PX, (self.H - py) * self.PX

    def _attrs(self, st, fill=None):
        _, _, w, dash, _ = STYLES[st]
        col = self.color(st)
        a = f'stroke="{col}" stroke-width="{max(w, 0.0) * self.PX / 72 * 1.6:.2f}"' if w > 0 else 'stroke="none"'
        if dash:
            a += f' stroke-dasharray="{" ".join(f"{d * self.PX / 72 * 1.4:.1f}" for d in dash)}"'
        if fill:
            fc = self.color(fill) if fill in STYLES else fill
            op = ' fill-opacity=".9"' if fill in ("wallfill", "wallfill_lt") else ""
            a += f' fill="{fc}"{op}'
        else:
            a += ' fill="none"'
        return a

    def poly(self, pts, st="thin", closed=False, fill=None):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in (self._xy(*p) for p in pts))
        tag = "polygon" if closed else "polyline"
        self.out.append(f'<{tag} points="{d}" {self._attrs(st, fill)} stroke-linejoin="round" stroke-linecap="round"/>')

    def shape(self, pts, fill_hex, stroke_hex=None, lw=0.15):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in (self._xy(*p) for p in pts))
        self.out.append(f'<polygon points="{d}" fill="{fill_hex}" stroke="{stroke_hex or fill_hex}" stroke-width="{lw * 1.3:.2f}" stroke-linejoin="round"/>')

    def circle(self, cx, cy, r, st="thin", fill=None):
        x, y = self._xy(cx, cy)
        self.out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * self.s * self.PX:.1f}" {self._attrs(st, fill)}/>')

    def text(self, x, y, t, size=0.1, st="text", anchor="middle", bold=False, rot=0):
        px, py = self._xy(x, y)
        fs = size * self.PX / 0.72
        tr = f' transform="rotate({-rot} {px:.1f} {py:.1f})"' if rot else ""
        w = ' font-weight="600"' if bold else ""
        self.out.append(f'<text x="{px:.1f}" y="{py:.1f}" font-size="{fs:.1f}" fill="{self.color(st)}" text-anchor="{anchor}"{w}{tr}>{escape(t)}</text>')

    def text_width(self, t, size, bold=False):
        return len(t) * size / 0.72 * 0.55

    def svg(self):
        w, h = self.W * self.PX, self.H * self.PX
        bg = ""
        if self.bg:
            col = "#0d3c48" if self.theme == "blueprint" else "#ffffff"
            bg = (f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity=".05"/></pattern></defs>'
                  f'<rect width="{w:.0f}" height="{h:.0f}" fill="{col}"/>' + (f'<rect width="{w:.0f}" height="{h:.0f}" fill="url(#g)"/>' if self.theme == "blueprint" else ""))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" '
                f'aria-label="{escape(self.title)}" font-family="Inter, Helvetica, Arial, sans-serif"><title>{escape(self.title)}</title>'
                + bg + "".join(self.out) + "</svg>")


# ---------------------------------------------------------------------------------------

class DxfCanvas(Canvas):
    """AutoCAD R12 ASCII DXF. Views are placed in model space at full scale (inches)."""
    PLOT = 48     # text sizes are specified as if plotted at 1/4" = 1'-0"

    ACI = {"A-WALL": 7, "A-WALL-PATT": 8, "A-DOOR": 30, "A-GLAZ": 4, "A-FLOR-FIXT": 9, "A-FURN": 8, "A-HIDD": 8,
           "A-ANNO-DIMS": 3, "A-ANNO-TEXT": 7, "A-ANNO-TTLB": 7, "A-ANNO-NOTE": 30, "A-ANNO-GRAD": 32, "A-ANNO-WMRK": 8,
           "E-POWR": 1, "E-LITE-CIRC": 1, "E-ANNO-TEXT": 1, "P-DOMW-CWTR": 5, "P-DOMW-HOTW": 1, "P-SANR-PIPE": 3,
           "P-SANR-VENT": 3, "P-ANNO-TEXT": 3, "S-FRAM": 7, "S-FNDN": 7}

    def __init__(self):
        super().__init__()
        self.ents = []
        self.layers = set()

    def view(self, ox, oy, s=12.0):
        # ox/oy are model-space inches; s is fixed at 12 (inches per foot)
        super().view(ox, oy, 12.0)

    def _layer(self, st):
        lay = STYLES[st][4]
        self.layers.add(lay)
        return lay

    def poly(self, pts, st="thin", closed=False, fill=None):
        lay = self._layer(st)
        pp = [self.P(*p) for p in pts]
        if closed:
            pp.append(pp[0])
        for (x1, y1), (x2, y2) in zip(pp, pp[1:]):
            self.ents.append(f"0\nLINE\n8\n{lay}\n10\n{x1:.3f}\n20\n{y1:.3f}\n30\n0.0\n11\n{x2:.3f}\n21\n{y2:.3f}\n31\n0.0")

    def circle(self, cx, cy, r, st="thin", fill=None):
        lay = self._layer(st)
        x, y = self.P(cx, cy)
        self.ents.append(f"0\nCIRCLE\n8\n{lay}\n10\n{x:.3f}\n20\n{y:.3f}\n30\n0.0\n40\n{r * self.s:.3f}")

    def arc(self, cx, cy, r, a0, a1, st="thin"):
        lay = self._layer(st)
        x, y = self.P(cx, cy)
        if a1 < a0:
            a0, a1 = a1, a0
        self.ents.append(f"0\nARC\n8\n{lay}\n10\n{x:.3f}\n20\n{y:.3f}\n30\n0.0\n40\n{r * self.s:.3f}\n50\n{a0 % 360:.3f}\n51\n{a1 % 360:.3f}")

    def text(self, x, y, t, size=0.1, st="text", anchor="middle", bold=False, rot=0):
        lay = self._layer(st)
        px, py = self.P(x, y)
        h = size * self.PLOT
        just = {"start": 0, "middle": 1, "end": 2}[anchor]
        t = t.replace("\n", " ")
        e = f"0\nTEXT\n8\n{lay}\n10\n{px:.3f}\n20\n{py:.3f}\n30\n0.0\n40\n{h:.3f}\n1\n{t}"
        if rot:
            e += f"\n50\n{rot:.1f}"
        if just:
            e += f"\n72\n{just}\n11\n{px:.3f}\n21\n{py:.3f}\n31\n0.0"
        self.ents.append(e)

    def text_width(self, t, size, bold=False):
        return len(t) * size * 0.75

    def dxf(self):
        layers = "\n".join(f"0\nLAYER\n2\n{l}\n70\n0\n62\n{self.ACI.get(l, 7)}\n6\nCONTINUOUS" for l in sorted(self.layers))
        return ("0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n9\n$INSUNITS\n70\n1\n0\nENDSEC\n"
                "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLTYPE\n70\n1\n0\nLTYPE\n2\nCONTINUOUS\n70\n0\n3\nSolid line\n72\n65\n73\n0\n40\n0.0\n0\nENDTAB\n"
                f"0\nTABLE\n2\nLAYER\n70\n{len(self.layers)}\n{layers}\n0\nENDTAB\n0\nENDSEC\n"
                "0\nSECTION\n2\nENTITIES\n" + "\n".join(self.ents) + "\n0\nENDSEC\n0\nEOF\n")
