"""Sheet compositions for the 24 x 36 in. (ARCH D) construction drawing set, plus the
website previews (SVG) and the CAD export (DXF).
"""
from __future__ import annotations

import datetime as dt
import math

import thb_model as M
import thb_qty as Q
import thb_views as V
from thb_draw import DxfCanvas, PdfCanvas, SvgCanvas
from thb_mesh import profile

SHEET_W, SHEET_H = 36.0, 24.0
TB_X = 32.4              # title block left edge
AREA = (0.75, 0.75, TB_X - 0.35, SHEET_H - 0.75)   # drawing area x0, y0, x1, y1
SCALE = 0.25             # 1/4" = 1'-0"
SITE = "tinyhomesblueprint.com"
DISCLAIMER = [
    "PLANNING & PERMIT-DEVELOPMENT SET. THESE DRAWINGS ARE",
    "GENERATED FROM THE PLAN DESIGN AND ARE INTENDED FOR",
    "PRICING, PLANNING AND PERMIT PREPARATION. VERIFY ALL",
    "DIMENSIONS ON SITE. STRUCTURAL, ELECTRICAL AND PLUMBING",
    "DESIGN MUST BE REVIEWED AND, WHERE YOUR JURISDICTION",
    "REQUIRES IT, STAMPED BY A LICENSED ENGINEER OR ARCHITECT",
    "AND INSTALLED BY LICENSED TRADES TO LOCAL CODE.",
]


def money(v):
    return f"${v:,.0f}"


class SetBuilder:
    def __init__(self, slug, p, m: M.Model, items, est, me, cover_img=None):
        self.cover_img = cover_img
        self.slug, self.p, self.m, self.items, self.est, self.me = slug, p, m, items, est, me
        self.g = Q.geometry(m)
        self.sheets = self._sheet_list()
        self.date = dt.date.today().strftime("%b %d, %Y").upper()

    def _sheet_list(self):
        s = [("A0.0", "COVER SHEET & PROJECT DATA", self.cover),
             ("A1.0", "FLOOR PLAN & SCHEDULES", self.floor)]
        if self.m.lofts:
            s.append(("A1.1", "LOFT PLAN", self.loft))
        s += [("A2.0", "EXTERIOR ELEVATIONS", self.elevations),
              ("A3.0", "BUILDING SECTION & ASSEMBLIES", self.section),
              ("S1.0", "FOUNDATION PLAN" if not self.m.mobile else "TRAILER & FLOOR FRAMING PLAN", self.foundation),
              ("S2.0", "ROOF FRAMING PLAN & HEADERS", self.framing),
              ("E1.0", "ELECTRICAL PLAN & PANEL SCHEDULE", self.electrical),
              ("P1.0", "PLUMBING PLAN & FIXTURE SCHEDULE", self.plumbing)]
        n_mat = max(1, math.ceil(len(self.items) / 220))
        for i in range(n_mat):
            s.append((f"G1.{i}", "MATERIALS LIST" + (f" ({i + 1} OF {n_mat})" if n_mat > 1 else ""), lambda cv, i=i, n=n_mat: self.materials(cv, i, n)))
        s.append(("G2.0", "COST ESTIMATE", self.cost))
        return s

    # ---------------------------------------------------------------------------------
    def pdf(self, path):
        cv = PdfCanvas(path, SHEET_W, SHEET_H, f"{self.p['name']} - {self.p['title']} - Construction Drawings")
        for i, (no, title, fn) in enumerate(self.sheets):
            cv.paper()
            self.frame(cv, no, title, i + 1)
            fn(cv)
            cv.paper()
            cv.page()
        cv.save()

    def frame(self, cv, no, title, idx):
        cv.rect(0.4, 0.4, SHEET_W - 0.8, SHEET_H - 0.8, "border")
        x = TB_X
        cv.line(x, 0.4, x, SHEET_H - 0.4, "border")
        y = SHEET_H - 0.9
        cv.text(x + 0.2, y, "TINY HOMES", 0.26, "title", anchor="start", bold=True)
        cv.text(x + 0.2, y - 0.42, "BLUEPRINT", 0.26, "title", anchor="start", bold=True)
        cv.text(x + 0.2, y - 0.75, SITE, 0.09, "text", anchor="start")
        cv.text(x + 0.2, y - 0.95, "210-903-9471  ·  contact@tinyhomesblueprint.com", 0.075, "text_lt", anchor="start")
        cv.line(x, y - 1.2, SHEET_W - 0.4, y - 1.2, "thin")
        cv.text(x + 0.2, y - 1.55, "PLAN", 0.07, "text_lt", anchor="start")
        cv.text(x + 0.2, y - 1.9, self.p["name"].upper(), 0.2, "text", anchor="start", bold=True)
        words, line, yy = self.p["title"].upper().split(), "", y - 2.25
        for wd in words:
            if len(line + " " + wd) > 30:
                cv.text(x + 0.2, yy, line.strip(), 0.085, "text", anchor="start")
                yy -= 0.19
                line = ""
            line += " " + wd
        cv.text(x + 0.2, yy, line.strip(), 0.085, "text", anchor="start")
        yy -= 0.35
        facts = [f"{self.p['sqft']:,} SQ FT", f"{self.p['beds']} BED / {self.p['baths']} BATH", f"{self.p['width']} x {self.p['depth']}"]
        cv.text(x + 0.2, yy, "  ·  ".join(facts), 0.075, "text_lt", anchor="start")
        cv.line(x, yy - 0.3, SHEET_W - 0.4, yy - 0.3, "thin")
        yy -= 0.65
        for line_ in DISCLAIMER:
            cv.text(x + 0.2, yy, line_, 0.058, "text_lt", anchor="start")
            yy -= 0.15
        cv.line(x, yy - 0.15, SHEET_W - 0.4, yy - 0.15, "thin")
        yy -= 0.5
        for k, v in (("DATE", self.date), ("SCALE", "AS NOTED (24 x 36)"), ("DRAWN", "THB PLAN GENERATOR"), ("CODES", "2021 IRC / 2023 NEC / 2021 IPC")):
            cv.text(x + 0.2, yy, k, 0.065, "text_lt", anchor="start")
            cv.text(x + 1.1, yy, v, 0.07, "text", anchor="start")
            yy -= 0.24
        cv.line(x, 3.4, SHEET_W - 0.4, 3.4, "thin")
        cv.text(x + 0.2, 3.05, "SHEET TITLE", 0.065, "text_lt", anchor="start")
        tw = title.split(" & ")
        cv.text(x + 0.2, 2.72, tw[0], 0.11, "text", anchor="start", bold=True)
        if len(tw) > 1:
            cv.text(x + 0.2, 2.47, "& " + tw[1], 0.11, "text", anchor="start", bold=True)
        cv.line(x, 2.15, SHEET_W - 0.4, 2.15, "thin")
        cv.text(x + 0.2, 1.8, "SHEET", 0.065, "text_lt", anchor="start")
        cv.text(x + 1.55, 0.85, no, 0.55, "title", bold=True)
        cv.text(SHEET_W - 0.6, 0.6, f"{idx} OF {len(self.sheets)}", 0.07, "text_lt", anchor="end")
        cv.text(x + 0.2, 0.6, f"© {dt.date.today().year} TINY HOMES BLUEPRINT", 0.055, "text_lt", anchor="start")

    def title(self, cv, x, y, label, scale="1/4\" = 1'-0\""):
        cv.paper()
        cv.circle(x + 0.25, y + 0.12, 0.25, "thin")
        cv.text(x + 0.62, y + 0.05, label, 0.14, "text", anchor="start", bold=True)
        cv.line(x + 0.6, y - 0.07, x + 0.6 + max(3.0, len(label) * 0.13), y - 0.07, "thin")
        if scale:
            cv.text(x + 0.62, y - 0.28, f"SCALE: {scale}", 0.075, "text_lt", anchor="start")

    def place(self, cv, w_ft, h_ft, x0, y0, x1, y1, scale=SCALE, pad=(0, 0, 0, 0), align="center"):
        """Set a view so a w x h ft drawing is centered in the paper box; pad is extra feet (l, b, r, t)."""
        l, b, r, t = pad
        total_w = (w_ft + l + r) * scale
        total_h = (h_ft + b + t) * scale
        ox = x0 + ((x1 - x0) - total_w) / 2 + l * scale if align == "center" else x0 + l * scale
        oy = y0 + ((y1 - y0) - total_h) / 2 + b * scale
        cv.view(ox, oy, scale)
        return ox, oy

    def fit_scale(self, w_ft, h_ft, box_w, box_h, prefer=0.5):
        for s in (0.5, 0.375, 0.25, 3 / 16, 1 / 8):
            if s > prefer:
                continue
            if w_ft * s <= box_w and h_ft * s <= box_h:
                return s
        return min(box_w / w_ft, box_h / h_ft)

    @staticmethod
    def scale_label(s):
        return {0.25: "1/4\" = 1'-0\"", 3 / 16: "3/16\" = 1'-0\"", 0.125: "1/8\" = 1'-0\"", 0.375: "3/8\" = 1'-0\"", 0.5: "1/2\" = 1'-0\""}.get(s, "NTS")

    def extents(self):
        pr, inset = V.porch_rect(self.m)
        x0, y0, x1, y1 = 0, 0, self.m.W, self.m.D
        if pr and not inset:
            x0, y0 = min(x0, pr[0]), min(y0, pr[1])
            x1, y1 = max(x1, pr[0] + pr[2]), max(y1, pr[1] + pr[3])
        if self.m.mobile and self.m.roof_type != "gooseneck":
            x0 = min(x0, -5)
        return x0, y0, x1, y1

    # ---------------------------------------------------------------------------------
    def table(self, cv, x, y, title, cols, rows, size=0.075, rh=0.22, header=True, max_y=None):
        """cols: [(header, width, align)]. Returns the y below the table."""
        cv.paper()
        if title:
            cv.text(x, y, title, 0.11, "text", anchor="start", bold=True)
            y -= 0.22
        tw = sum(c[1] for c in cols)
        if header:
            cv.rect(x, y - rh, tw, rh, "thin", fill="grid")
            cx = x
            for h, w, al in cols:
                tx = cx + 0.06 if al == "l" else cx + w - 0.06 if al == "r" else cx + w / 2
                cv.text(tx, y - rh + 0.065, h, size * 0.9, "text", anchor={"l": "start", "r": "end", "c": "middle"}[al], bold=True)
                cx += w
            y -= rh
        for row in rows:
            bold = isinstance(row, tuple) and len(row) and row[0] == "__bold__"
            vals = row[1:] if bold else row
            cx = x
            for (h, w, al), v in zip(cols, vals):
                tx = cx + 0.06 if al == "l" else cx + w - 0.06 if al == "r" else cx + w / 2
                txt = str(v)
                maxc = int(w / (size * 0.62))
                if len(txt) > maxc:
                    txt = txt[:maxc - 1] + "…"
                cv.text(tx, y - rh + 0.065, txt, size, "text", anchor={"l": "start", "r": "end", "c": "middle"}[al], bold=bold)
                cx += w
            cv.line(x, y - rh, x + tw, y - rh, "grid")
            y -= rh
        cv.rect(x, y, tw, (rh * (len(rows) + (1 if header else 0))), "thin")
        return y - 0.3

    def notes(self, cv, x, y, title, lines, size=0.075, width_chars=95, lh=0.16):
        cv.paper()
        cv.text(x, y, title, 0.11, "text", anchor="start", bold=True)
        y -= 0.25
        for i, ln in enumerate(lines):
            words = ln.split()
            cur = f"{i + 1}. " if not ln.startswith("-") else "   "
            first = True
            for wd in words:
                if len(cur) + len(wd) + 1 > width_chars:
                    cv.text(x, y, cur, size, "text", anchor="start")
                    y -= lh
                    cur = "    "
                cur += (wd if cur.endswith(" ") or not first and cur.strip() == "" else " " + wd) if not cur.endswith(". ") else wd
                first = False
            cv.text(x, y, cur, size, "text", anchor="start")
            y -= lh * 1.25
        return y - 0.1

    # ---------------------------------------------------------------------------------
    # Sheets
    # ---------------------------------------------------------------------------------
    def cover(self, cv):
        p, m, g = self.p, self.m, self.g
        cv.paper()
        cv.text(1.0, 22.3, p["name"].upper(), 0.42, "title", anchor="start", bold=True)
        cv.text(1.0, 21.6, p["title"], 0.22, "text", anchor="start")
        cv.text(1.0, 21.15, f"{p['sqft']:,} sq ft  ·  {p['beds']} bed  ·  {p['baths']} bath  ·  {p['width']} x {p['depth']}  ·  {p['foundation']}", 0.12, "text_lt", anchor="start")
        if self.cover_img:
            from reportlab.lib.utils import ImageReader
            img = ImageReader(self.cover_img)
            iw, ih = img.getSize()
            bw, bh = 18.5, 11.0
            sc = min(bw / iw, bh / ih)
            cv.c.drawImage(img, (1.0 + (bw - iw * sc) / 2) * 72, (9.6 + (bh - ih * sc) / 2) * 72, iw * sc * 72, ih * sc * 72)
        else:
            V.render_axo(cv, self.me, m, 1.0, 9.6, 18.5, 11.0)
        cv.text(10.25, 9.2, "3D VIEW - FRONT LEFT", 0.09, "text_lt")
        # project data
        info = profile(m)
        rows = [("Plan", p["name"]), ("Heated area", f"{p['sqft']:,} sq ft" + (f" ({p['main_sqft']:,} main + {p['loft_sqft']} loft)" if p.get("loft_sqft") else "")),
                ("Footprint", f"{p['width']} x {p['depth']}"), ("Bedrooms / baths", f"{p['beds']} / {p['baths']}"),
                ("Covered porch / deck", f"{g['porch']:.0f} sq ft" if g["porch"] else "None"),
                ("Overall height", p["height"]), ("Ceiling height", p["ceiling"]), ("Roof", p["roof"]), ("Exterior walls", p["walls"]),
                ("Foundation", p["foundation"]), ("Wall framing", f"{m.stud} @ {24 if m.container else 16}\" o.c."),
                ("Electrical service", m.notes["load"]["service"]), ("Heating & cooling", "Ductless mini-split heat pump"),
                ("Water heating", "Electric tank / heat-pump" if any(f.kind == "wh" for f in m.fixtures) else "Point-of-use tankless (electric)"),
                ("Est. build cost (DIY)", money(self.est["diy_total"])), ("Est. build cost (contractor)", money(self.est["gc_total"]))]
        self.table(cv, 20.3, 20.6, "PROJECT DATA", [("ITEM", 3.6, "l"), ("VALUE", 7.6, "l")], rows, size=0.085, rh=0.27)
        # sheet index
        y = self.table(cv, 20.3, 13.6, "SHEET INDEX", [("SHEET", 1.3, "l"), ("TITLE", 6.5, "l")], [(n, t) for n, t, _ in self.sheets], size=0.085, rh=0.25)
        gen = [
            "All work shall comply with the 2021 International Residential Code (IRC) including Appendix AQ (Tiny Houses) where adopted, the 2023 National Electrical Code (NEC) and the 2021 International Plumbing Code (IPC), as amended by the local jurisdiction.",
            "Design loads assumed: 40 psf floor live, 30 psf sleeping-loft live, 20 psf roof live / 30 psf ground snow, 115 mph ultimate wind (Exposure B), Seismic Design Category A-C. Verify for your site; higher loads require engineering.",
            "Contractor / owner-builder shall verify all dimensions, site conditions and utility locations before construction. Written dimensions govern; do not scale drawings.",
            "Smoke alarms in every sleeping room and outside sleeping areas, interconnected and hardwired with battery backup. CO alarm required where fuel-burning appliances or attached garages exist.",
            "Every sleeping room and loft requires an emergency escape opening: 5.7 sq ft net clear (5.0 at grade floor), 20 in. min. width, 24 in. min. height, sill 44 in. max. above floor.",
            "Provide whole-house mechanical ventilation per IRC M1505 and spot exhaust in bath (50 cfm) and kitchen (100 cfm). Continuous air barrier; blower-door test where required by energy code.",
            "Insulation and fenestration to meet the IECC prescriptive table for your climate zone; values shown are typical (Zones 3-5).",
            "Mobile units (on wheels): may be regulated as RVs (NFPA 1192 / ANSI A119.5) or as dwellings depending on jurisdiction. Confirm the applicable standard before starting.",
        ]
        if not m.mobile:
            gen = [x for x in gen if not x.startswith("Mobile")]
        self.notes(cv, 1.0, 8.4, "GENERAL NOTES", gen, size=0.08, width_chars=150, lh=0.17)

    def floor(self, cv):
        m = self.m
        x0, y0, x1, y1 = self.extents()
        w, h = x1 - x0, y1 - y0
        box = (AREA[0], 6.6, 21.0, AREA[3] - 0.6)
        s = self.fit_scale(w + 9, h + 9, box[2] - box[0], box[3] - box[1])
        self.place(cv, w, h, *box, scale=s, pad=(4.5 - x0, 4.5 - y0, 4.5 + x0, 4.5 + y0))
        cv.view(cv.ox - x0 * s, cv.oy - y0 * s, s) if False else None
        V.draw_plan(cv, m, "floor")
        V.plan_dims(cv, m)
        cv.text(m.W / 2, (min(0, y0)) - 6.0, "FRONT", 0.1, "text_lt", bold=True)
        self.title(cv, AREA[0] + 0.2, 6.0, "FLOOR PLAN", self.scale_label(s))
        # schedules
        doors = [o for o in m.openings if o.kind != "window"]
        wins = [o for o in m.openings if o.kind == "window"]
        drows = [(o.tag, (o.room.title if o.room else ""), {"door": "Ext. prehung, fiberglass half-lite" if o.exterior else "Int. prehung, hollow-core",
                                                            "slider": "Sliding glass door, low-E", "pocket": "Pocket / sliding panel"}[o.kind] if not (o.exterior and o.width >= 5 and o.kind == "door") else "Exterior double / barn doors",
                  f"{V.ft_in(o.width)} x {V.ft_in(o.height)}", Q.header_for(o.width) if (o.exterior or o.width >= 4) else "Flat 2x4", "Lockset + deadbolt" if o.exterior else ("Privacy" if o.room and o.room.kind in ("bed", "bath") else "Passage"))
                 for o in doors]
        y = self.table(cv, 21.6, AREA[3] - 0.3, "DOOR SCHEDULE", [("TAG", 0.55, "c"), ("ROOM", 2.0, "l"), ("TYPE", 3.3, "l"), ("SIZE (W x H)", 1.45, "c"), ("HEADER", 0.85, "c"), ("HARDWARE", 1.35, "l")], drows, size=0.072)
        wrows = [(o.tag, o.room.title if o.room else "", "Casement (egress)" if o.egress else ("Single-hung" if o.height > o.width else "Slider"),
                  f"{V.ft_in(o.width)} x {V.ft_in(o.height)}", V.ft_in(o.sill), Q.header_for(o.width), "Yes" if o.egress else "-", "Tempered" if (o.room and o.room.kind == "bath") or o.sill < 1.5 else "")
                 for o in wins]
        y = self.table(cv, 21.6, y, "WINDOW SCHEDULE", [("TAG", 0.55, "c"), ("ROOM", 2.0, "l"), ("TYPE", 1.7, "l"), ("SIZE (W x H)", 1.45, "c"), ("SILL", 0.8, "c"), ("HEADER", 0.85, "c"), ("EGRESS", 0.7, "c"), ("GLAZING", 1.45, "l")],
                       wrows, size=0.072)
        if m.notes.get("clerestory"):
            cv.text(21.6, y + 0.05, f"PLUS {len(m.notes['clerestory'])} FIXED CLERESTORY WINDOWS 2'-6\" x 1'-2\" HIGH ON THE FRONT WALL (SEE ELEVATIONS).", 0.07, "text", anchor="start")
            y -= 0.3
        rrows = []
        for r in m.heated + m.lofts:
            fl = "Porcelain tile" if r.kind in ("bath",) else "LVP (waterproof)"
            ceil = self.p["ceiling"] if not r.loft else "Sloped / 4'-0\" min."
            rrows.append((r.title, f"{r.area:.0f}", fl, "1/2\" gyp. bd., paint" if not m.mobile else "T&G / ply panel", ceil[:24]))
        y = self.table(cv, 21.6, y, "ROOM FINISH SCHEDULE", [("ROOM", 2.6, "l"), ("SQ FT", 0.8, "r"), ("FLOOR", 1.9, "l"), ("WALLS", 2.0, "l"), ("CEILING", 2.2, "l")], rrows, size=0.072)
        self.notes(cv, 21.6, max(y, 6.2), "FLOOR PLAN NOTES", [
            "Dimensions are to the outside face of exterior sheathing and the centerline of interior partitions.",
            f"Exterior walls {m.stud} @ {24 if m.container else 16}\" o.c.; interior partitions 2x4 @ 16\" o.c. unless noted.",
            "Window and door tags refer to the schedules above; egress windows marked in the window schedule.",
            "Provide solid blocking for cabinets, grab bars, towel bars, TV mounts and the mini-split head.",
            "Bath: moisture-resistant board; tile backer and waterproofing membrane at the shower / tub.",
        ], size=0.072, width_chars=100, lh=0.16)

    def loft(self, cv):
        m = self.m
        box = (AREA[0], 4.0, AREA[2], AREA[3] - 0.6)
        s = self.fit_scale(m.W + 8, m.D + 8, box[2] - box[0], box[3] - box[1], prefer=0.375 if m.W < 26 else SCALE)
        self.place(cv, m.W, m.D, *box, scale=s, pad=(4, 4, 4, 4))
        V.draw_loft(cv, m)
        self.title(cv, AREA[0] + 0.2, 3.4, "LOFT PLAN", self.scale_label(s))
        self.notes(cv, 12.0, 3.4, "LOFT NOTES", [
            "Habitable loft per IRC Appendix AQ: 35 sq ft min. floor area, 5 ft min. horizontal dimension, 3 ft min. clear height.",
            "Guards on open sides 36 in. min. (or half the clear height where under 6 ft); openings shall not pass a 4 in. sphere.",
            "Access by stair, alternating-tread device, ship's ladder or ladder per AQ104.4; provide handrails as required.",
            "Loft floor framing 2x8 @ 16\" o.c. designed for 30 psf live load; hang from rim with hangers.",
            "Emergency escape opening or skylight required in every sleeping loft (see window schedule / elevations).",
        ], size=0.075, width_chars=150)

    def elevations(self, cv):
        m = self.m
        info = profile(m)
        H = info["ridge"] + 2
        cells = [("front", AREA[0], 12.2), ("rear", 16.6, 12.2), ("left", AREA[0], 1.1), ("right", 16.6, 1.1)]
        maxL = max(m.W, m.D) + 12
        s = self.fit_scale(maxL, H + 3, 15.5, 9.8, prefer=0.375)
        for fac, x, y in cells:
            L = V.facade_len(m, fac)
            self.place(cv, L, H, x, y + 0.6, x + 15.5, y + 10.0, scale=s, pad=(5, 1.5, 8, 1))
            V.draw_elevation(cv, m, fac)
            self.title(cv, x + 0.2, y + 0.4, f"{fac.upper()} ELEVATION", self.scale_label(s))
        cv.paper()
        roofing = "STANDING-SEAM METAL" if "metal" in self.p["roof"].lower() or m.mobile else "ARCHITECTURAL ASPHALT SHINGLES"
        lines = [f"ROOF: {roofing} OVER SYNTHETIC UNDERLAYMENT", f"WALLS: {self.p['walls'].upper()}", "TRIM: 1x4 / 1x6 PRIMED, CORNER BOARDS", "WINDOWS: VINYL, LOW-E, U-0.30 MAX."]
        for i, ln in enumerate(lines):
            cv.text(AREA[0] + 0.3, 11.75 - i * 0.17, ln, 0.07, "text_lt", anchor="start")

    def section(self, cv):
        m = self.m
        info = profile(m)
        box = (AREA[0], 7.2, 20.5, AREA[3] - 0.6)
        s = self.fit_scale(m.D + 14, info["ridge"] + 6, box[2] - box[0], box[3] - box[1], prefer=0.5)
        self.place(cv, m.D, info["ridge"] + 3, *box, scale=s, pad=(5, 2.5, 9, 1))
        V.draw_section(cv, m)
        # height marks
        for z, lbl in ((info["B"], "FIN. FLOOR"), (info["front"], "T.O. PLATE" if info["kind"] != "aframe" else ""), (info["ridge"], "RIDGE")):
            if lbl:
                cv.line(m.D + info["ov"] + 0.8, z, m.D + info["ov"] + 1.3, z, "dim")
                cv.text(m.D + info["ov"] + 1.5, z - 0.1, f"{lbl} {V.ft_in(z)}", V.TXT["small"], "dim", anchor="start")
        self.title(cv, AREA[0] + 0.2, 6.6, "BUILDING SECTION A-A", self.scale_label(s))
        roofing = "metal roofing on 1x4 purlins or underlayment" if ("metal" in self.p["roof"].lower() or m.mobile) else "architectural shingles"
        rt = m.roof_type
        roof = [f"ROOF: {roofing}; synthetic underlayment; ice & water shield at eaves; 1/2\" CDX sheathing.",
                ("Pre-engineered trusses @ 24\" o.c.; R-38 blown insulation; vented attic with soffit + ridge vents; 1/2\" gypsum ceiling."
                 if rt in ("gable", "gable-steep") else
                 "Rafters @ 24\" o.c. (see S2.0); unvented cathedral assembly: 2\" closed-cell spray foam + batt to R-30 min.; interior finish.")]
        if m.container:
            roof = ["ROOF: container roof deck, elastomeric coating, slope to drip edge" + (" with 2x6 shed roof above" if rt == "container-double" else "") + ".",
                    "Ceiling: 2\" closed-cell spray foam (R-13) on steel + 1x3 furring and finish panel."]
        wall = ([f"WALL: {self.p['walls']}; house wrap (WRB); 7/16\" OSB sheathing; {m.stud} studs @ 16\" o.c.;",
                 f"{'R-21' if m.stud == '2x6' else 'R-15'} batts or mineral wool; 1/2\" gypsum board (or T&G / plywood on wheels). Flash all openings."]
                if not m.container else
                ["WALL: container steel; 2\" closed-cell spray foam (R-13) between 2x3 furring @ 24\" o.c.;", "1/2\" plywood or gypsum interior finish; thermal break at furring."])
        fnd = m.foundation
        floor = {"slab": ["FLOOR: LVP on 4\" concrete slab, 10 mil vapor retarder, 4\" crushed stone; 2\" XPS at slab edge.",
                          "Thickened edge 12\" x 12\" with (2) #4 cont.; 1/2\" anchor bolts @ 6'-0\" o.c., 12\" from corners."],
                 "crawl": ["FLOOR: LVP on 3/4\" T&G subfloor on 2x10 joists @ 16\" o.c.; R-19 insulation; 10 mil ground vapor barrier.",
                           "8\" CMU stem wall on 16\" x 8\" continuous footing below frost depth; PT 2x6 sill with anchor bolts @ 6'-0\"."],
                 "piers": ["FLOOR: container floor with 1\" XPS and 3/4\" plywood underlayment; LVP finish.", "Concrete piers 24\" x 24\" x 36\" with weld plates at corner castings."],
                 "trailer": ["FLOOR: LVP on 3/4\" T&G subfloor; 2x6 joists @ 16\" o.c. with rigid foam / R-19 between; metal flashing below.",
                             "Bottom plate bolted to trailer frame with 1/2\" bolts @ 4'-0\" o.c. and at each tie-down plate."]}[fnd]
        y = self.notes(cv, 21.0, AREA[3] - 0.3, "ROOF ASSEMBLY", roof, size=0.075, width_chars=100)
        y = self.notes(cv, 21.0, y, "WALL ASSEMBLY", wall, size=0.075, width_chars=100)
        y = self.notes(cv, 21.0, y, "FLOOR / FOUNDATION ASSEMBLY", floor, size=0.075, width_chars=100)
        y = self.notes(cv, 21.0, y, "CONNECTIONS", [
            "Rafter / truss to wall: Simpson H2.5A (or equal) at every rafter or truss.",
            "Wall sheathing nailing 8d @ 6\" edges / 12\" field; continuous sheathing as wall bracing per IRC R602.10.",
            "Headers per S2.0; jack and king studs each side of every opening.",
            "Loft or floor joists to rim with face-mount hangers; 3-16d at each bearing.",
        ], size=0.075, width_chars=100)

    def foundation(self, cv):
        m = self.m
        x0 = -6 if (m.mobile and m.roof_type != "gooseneck") else 0
        box = (AREA[0], 6.0, 21.0, AREA[3] - 0.6)
        s = self.fit_scale(m.W - x0 + 8, m.D + 8, box[2] - box[0], box[3] - box[1])
        self.place(cv, m.W - x0, m.D, *box, scale=s, pad=(4 - x0, 4, 4, 4))
        V.draw_foundation(cv, m)
        V.dim_line(cv, (0, 0), (m.W, 0), -2.2, V.ft_in(m.W), "h")
        V.dim_line(cv, (m.W, 0), (m.W, m.D), 2.2, V.ft_in(m.D), "v")
        self.title(cv, AREA[0] + 0.2, 5.4, "FOUNDATION PLAN" if not m.mobile else "TRAILER PLAN", self.scale_label(s))
        cv.text(AREA[0] + 0.85, 4.85, "CIRCLES = DRAIN / PLUMBING ROUGH-IN LOCATIONS (SEE P1.0)", 0.07, "text_lt", anchor="start")
        fnd = m.foundation
        notes = {
            "slab": ["Remove topsoil and organics; compact subgrade to 95% standard Proctor. Bottom of thickened edge below local frost depth or per local frost-protected shallow foundation (FPSF) rules.",
                     "Concrete 3,000 psi at 28 days, 4 in. slump +/- 1 in.; control joints at 10 ft max. each way within 24 hours.",
                     "Place under-slab plumbing and conduit before the pour; pressure-test DWV and water lines and get rough-in inspection.",
                     "Anchor bolts 1/2 in. x 10 in. at 6 ft o.c. max. and within 12 in. of each plate end, 7 in. embedment; 2 bolts min. per plate piece.",
                     "Termite protection per local requirements; radon-resistant construction (sub-slab vent stub) in Zone 1 radon areas."],
            "crawl": ["Footings 16 in. wide x 8 in. deep with (2) #4 continuous; bottom below frost depth on undisturbed soil (1,500 psf assumed bearing).",
                      "8 in. CMU stem wall, cells with anchor bolts grouted solid; 18 in. min. clearance from grade to bottom of joists.",
                      "Center girder 3-2x10 on CMU piers @ 6 ft o.c. max. with 24 x 24 x 10 in. footings.",
                      "Crawlspace: 10 mil vapor barrier lapped 6 in. and sealed; vents 1 sq ft per 150 sq ft or conditioned crawlspace per R408.3.",
                      "Access opening 18 x 24 in. min."],
            "piers": ["Piers 24 x 24 x 36 in. min. (below frost depth) with 3/8 x 8 x 8 in. weld plates; 3,000 psi concrete.",
                      "Container corner castings bear on piers; weld or bolt with twist-lock brackets. Intermediate piers at 20 ft where shown.",
                      "Level piers to 1/8 in. across the set; shim with steel plates only.",
                      "Engineer to review any cut in container side walls (see openings on A1.0)."],
            "trailer": ["Use a purpose-built tiny house trailer rated for the finished weight plus 15% margin (GVWR). Verify axle rating, brakes, lights and VIN/title.",
                        "Weld or bolt tie-down plates every 4 ft; fasten wall bottom plates through plates with 1/2 in. bolts.",
                        "Seal the underside with metal flashing; install rigid foam between floor joists.",
                        "Distribute weight 60/40 front-to-back of the axles with appliances and water tanks near the axles.",
                        "When parked long-term, set on leveling jacks and ground anchors; skirt with vented skirting."]}[fnd]
        self.notes(cv, 21.6, AREA[3] - 0.3, "FOUNDATION NOTES" if not m.mobile else "TRAILER NOTES", notes, size=0.075, width_chars=100)

    def framing(self, cv):
        m = self.m
        info = profile(m)
        box = (AREA[0], 6.0, 21.0, AREA[3] - 0.6)
        s = self.fit_scale(m.W + 9, m.D + 9, box[2] - box[0], box[3] - box[1])
        self.place(cv, m.W, m.D, *box, scale=s, pad=(4.5, 4.5, 4.5, 4.5))
        V.draw_framing(cv, m)
        self.title(cv, AREA[0] + 0.2, 5.4, "ROOF FRAMING PLAN", self.scale_label(s))
        rows = []
        seen = {}
        for o in m.openings:
            if o.exterior or o.width >= 4:
                key = Q.header_for(o.width)
                seen.setdefault(key, []).append(o.tag)
        span = {"2-2x6": "up to 3'-0\"", "2-2x8": "up to 4'-0\"", "2-2x10": "up to 6'-0\"", "2-2x12": "up to 8'-0\""}
        for k, tags in sorted(seen.items()):
            rows.append((k, span[k], ", ".join(tags), "1 jack + 1 king each side" if k in ("2-2x6", "2-2x8") else "2 jacks + 1 king each side"))
        y = self.table(cv, 21.6, AREA[3] - 0.3, "HEADER SCHEDULE (EXTERIOR BEARING WALLS)", [("HEADER", 1.1, "c"), ("CLEAR SPAN", 1.3, "c"), ("OPENINGS", 4.0, "l"), ("SUPPORT", 2.6, "l")], rows, size=0.072)
        self.notes(cv, 21.6, y, "FRAMING NOTES", [
            "Lumber: SPF or Hem-Fir No. 2 or better; PT lumber where in contact with concrete or within 8 in. of grade.",
            "Trusses (where used) designed by the truss manufacturer for the loads on A0.0; submit truss layout and bracing to the building department.",
            "Double top plates lapped 48 in. min. at splices; single top plate allowed with aligned framing and steel straps.",
            f"Ceiling / roof insulation and ventilation per A3.0. Overhang {V.ft_in(info['ov'])} at eaves and rakes.",
            "Non-bearing interior headers: flat 2x4. Provide fire blocking at soffits, chases and floor-ceiling lines.",
            "Gable-end walls: balloon-frame or brace at top plate per IRC R602.10 with continuous sheathing.",
        ], size=0.075, width_chars=100)

    def electrical(self, cv):
        m = self.m
        box = (AREA[0], 6.4, 19.5, AREA[3] - 0.6)
        s = self.fit_scale(m.W + 8, m.D + 8, box[2] - box[0], box[3] - box[1])
        self.place(cv, m.W, m.D, *box, scale=s, pad=(4, 4, 4, 4))
        V.draw_plan(cv, m, "electrical")
        V.draw_electrical(cv, m)
        self.title(cv, AREA[0] + 0.2, 5.8, "ELECTRICAL PLAN", self.scale_label(s))
        self.legend_elec(cv, AREA[0] + 0.3, 5.0)
        rows = [(c.no, c.name, c.breaker, c.wire, f"{c.va:,}") for c in m.circuits]
        y = self.table(cv, 20.0, AREA[3] - 0.3, "PANEL SCHEDULE", [("CCT", 0.5, "c"), ("DESCRIPTION", 4.6, "l"), ("BREAKER", 1.1, "c"), ("WIRE", 2.6, "l"), ("VA", 0.9, "r")], rows, size=0.072)
        ld = m.notes["load"]
        y = self.table(cv, 20.0, y, "SERVICE LOAD CALCULATION (NEC 220.82)", [("ITEM", 6.8, "l"), ("VA", 2.9, "r")], [
            ("General lighting & receptacles (3 VA/sq ft)", f"{ld['general_va']:,}"), ("Small appliance, laundry and fixed appliances", f"{ld['other_va'] - ld['general_va']:,}"),
            ("First 10,000 VA @ 100% + remainder @ 40%", f"{min(ld['other_va'], 10000) + int(max(0, ld['other_va'] - 10000) * 0.4):,}"),
            ("Heating / cooling (heat pump) @ 100%", f"{ld['hp_va']:,}"), ("__bold__", "Calculated demand", f"{ld['demand_va']:,} VA = {ld['amps']} A @ 240 V"),
            ("__bold__", "Recommended service", ld["service"])], size=0.072)
        self.notes(cv, 20.0, y, "ELECTRICAL NOTES", [
            "All work per NEC 2023 and local amendments; licensed electrician required where mandated. Obtain permits and inspections.",
            "AFCI protection for all 120 V 15/20 A branch circuits in dwelling units (210.12); GFCI for kitchen, bath, laundry, outdoor and within 6 ft of sinks (210.8).",
            "Tamper-resistant receptacles throughout (406.12). Receptacles so no point along a usable wall is more than 6 ft from an outlet (210.52).",
            "Two 20 A small-appliance circuits for kitchen counters; counter receptacles every 4 ft and within 2 ft of each counter end.",
            "Smoke alarms hardwired and interconnected with battery backup; CO alarm where required. Exterior lights at every exterior door.",
            "Cable sizes shown are copper NM-B; increase for runs over 75 ft. Circuit numbers next to devices match the panel schedule.",
        ] + (["Shore power: 50 A RV inlet feeding a 100 A main-lug panel; provide a bonded ground per NFPA 1192 / NEC 551 where the unit is an RV."] if m.mobile else []),
            size=0.072, width_chars=110, lh=0.155)

    def legend_elec(self, cv, x, y):
        items = [("rec", "Duplex receptacle"), ("gfci", "GFCI receptacle"), ("rec20", "Dedicated 20 A"), ("rec240", "240 V receptacle"), ("wp", "Weatherproof GFCI"),
                 ("sw", "Switch / 3-way"), ("light", "Ceiling light"), ("can", "Recessed LED"), ("fan", "Exhaust fan / light"), ("sconce", "Wall / vanity light"),
                 ("smoke", "Smoke alarm"), ("smokeco", "Smoke / CO alarm"), ("panel", "Panel"), ("minisplit", "Mini-split head"), ("jbox", "Junction box")]
        cv.paper()
        cv.text(x, y, "LEGEND", 0.1, "text", anchor="start", bold=True)
        cols = 3
        for i, (k, lbl) in enumerate(items):
            cx = x + (i % cols) * 4.6
            cy = y - 0.4 - (i // cols) * 0.42
            cv.view(cx + 0.25, cy, 0.25)
            V.draw_device(cv, M.Device(k, 0, 0), num=False)
            cv.paper()
            cv.text(cx + 0.65, cy - 0.04, lbl, 0.075, "text", anchor="start")
        cv.text(x, y - 0.4 - 5 * 0.42 - 0.05, "DASHED ARCS = SWITCH LEGS. SMALL NUMBERS = PANEL CIRCUIT.", 0.07, "text_lt", anchor="start")

    def plumbing(self, cv):
        m = self.m
        box = (AREA[0], 6.0, 19.5, AREA[3] - 0.6)
        s = self.fit_scale(m.W + 9, m.D + 9, box[2] - box[0], box[3] - box[1])
        self.place(cv, m.W, m.D, *box, scale=s, pad=(4.5, 4.5, 4.5, 4.5))
        V.draw_plan(cv, m, "plumbing")
        V.draw_plumbing(cv, m)
        self.title(cv, AREA[0] + 0.2, 5.4, "PLUMBING PLAN (SUPPLY & DWV)", self.scale_label(s))
        cv.paper()
        lx, ly = AREA[0] + 0.3, 4.7
        for i, (st, lbl) in enumerate((("cold", "Cold water (PEX)"), ("hot", "Hot water (PEX)"), ("waste", "Drain / waste (PVC DWV)"), ("vent", "Vent"))):
            cv.line(lx + i * 4.4, ly, lx + i * 4.4 + 0.9, ly, st)
            cv.text(lx + i * 4.4 + 1.05, ly - 0.04, lbl, 0.075, "text", anchor="start")
        counts = {}
        for f in m.fixtures:
            if f.kind in M.DFU or f.kind in ("wh", "tankless"):
                counts[f.kind] = counts.get(f.kind, 0) + 1
        names = {"toilet": "Water closet, 1.28 gpf", "lav": "Lavatory", "shower": "Shower", "tub": "Bathtub / shower", "sink": "Kitchen sink", "dw": "Dishwasher",
                 "washer": "Clothes washer", "stack_wd": "Washer (stacked W/D)", "wh": "Water heater", "tankless": "Tankless water heater"}
        sup = {"toilet": ('1/2"', "-"), "lav": ('1/2"', '1/2"'), "shower": ('1/2"', '1/2"'), "tub": ('1/2"', '1/2"'), "sink": ('1/2"', '1/2"'), "dw": ("-", '3/8"'),
               "washer": ('1/2"', '1/2"'), "stack_wd": ('1/2"', '1/2"'), "wh": ('3/4"', '3/4"'), "tankless": ('1/2"', '1/2"')}
        rows = [(names[k], n, M.DFU.get(k, "-"), M.TRAP.get(k, "-"), sup[k][0], sup[k][1]) for k, n in sorted(counts.items())]
        rows.append(("__bold__", "Total drainage fixture units", "", m.notes.get("dfu", 0), f"Bldg drain {m.notes.get('main_drain', '3\"')}", "", ""))
        y = self.table(cv, 20.0, AREA[3] - 0.3, "PLUMBING FIXTURE SCHEDULE", [("FIXTURE", 3.3, "l"), ("QTY", 0.6, "c"), ("DFU", 0.6, "c"), ("TRAP / DRAIN", 1.6, "c"), ("CW", 0.8, "c"), ("HW", 0.8, "c")], rows, size=0.072)
        self.notes(cv, 20.0, y, "PLUMBING NOTES", [
            "All work per IPC 2021 / local plumbing code; licensed plumber where required. Pressure-test supply (100 psi / 15 min) and DWV (water or air test) before cover.",
            "Supply: PEX-A with expansion fittings; 3/4\" service and trunk, 1/2\" branches (or home-run manifold). Quarter-turn stop at every fixture.",
            "Drain: PVC schedule 40 DWV; slope 1/4\" per ft for 3\" and smaller. Cleanouts at the building drain exit, each change of direction over 45 degrees and at the base of the stack.",
            "Vent: 3\" vent through roof at the stack; individual or wet vents per IPC 909/912; air admittance valves only where permitted.",
            "Water heater: T&P relief to the exterior or pan drain; expansion tank where a PRV or check valve is installed; seismic straps where required.",
            "Hose bibbs frost-free with vacuum breakers; insulate all lines in exterior walls or unconditioned space.",
        ] + (["On wheels: RV fresh-water inlet with PRV and backflow preventer; sewer outlet with 3\" knife valve. A composting toilet removes the black-water line."] if m.mobile else []),
            size=0.072, width_chars=110, lh=0.155)

    def materials(self, cv, page, pages):
        per = 220
        items = self.items[page * per:(page + 1) * per]
        cols = [("CATEGORY", 2.4, "l"), ("ITEM", 7.2, "l"), ("QTY", 0.9, "r"), ("UNIT", 0.9, "l"), ("UNIT $", 0.95, "r"), ("TOTAL", 1.1, "r")]
        half = (len(items) + 1) // 2
        for ci, chunk in enumerate((items[:half], items[half:])):
            rows = []
            for it in chunk:
                q = f"{it.qty:,.1f}".rstrip("0").rstrip(".") if isinstance(it.qty, float) else f"{it.qty:,}"
                rows.append((it.cat, it.name, q, it.unit, f"{it.price:,.2f}", money(it.total)))
            self.table(cv, AREA[0] + ci * 15.8, AREA[3] - 0.3, "MATERIALS LIST" if ci == 0 else "", cols, rows, size=0.068, rh=0.17)
        if page == pages - 1:
            cv.paper()
            cv.text(AREA[0], 0.95, f"MATERIALS SUBTOTAL: {money(self.est['materials'])}   ·   Quantities include typical waste. Prices are 2026 US national averages for builder-grade materials; check local suppliers.", 0.085, "text", anchor="start", bold=True)

    def cost(self, cv):
        e = self.est
        rows = [(c["name"], money(c["materials"]), money(c["labor"]), money(c["materials"] + c["labor"])) for c in e["categories"]]
        rows += [("__bold__", "Subtotal", money(e["materials"]), money(e["labor"]), money(e["materials"] + e["labor"])),
                 ("Contractor overhead & profit (18%)", "", money(e["overhead"]), money(e["overhead"])),
                 ("Permits & plan review (allowance)", money(e["permits"]), "", money(e["permits"])),
                 ("Contingency (10%)", "", "", money(e["contingency_gc"])),
                 ("__bold__", "TOTAL WITH A GENERAL CONTRACTOR", "", "", money(e["gc_total"]))]
        y = self.table(cv, AREA[0], AREA[3] - 0.3, "COST ESTIMATE - CONTRACTOR BUILD", [("CATEGORY", 5.6, "l"), ("MATERIALS", 2.0, "r"), ("LABOR", 2.0, "r"), ("TOTAL", 2.1, "r")], rows, size=0.09, rh=0.3)
        rows2 = [("Materials (all categories)", money(e["materials"])), ("Licensed trade help: electrical, plumbing & HVAC rough-in (55% of trade labor)", money(e["diy_trade_help"])),
                 ("Permits & plan review (allowance)", money(e["permits"])), ("Contingency (12% of materials)", money(e["contingency_diy"])),
                 ("__bold__", "TOTAL OWNER-BUILT (DIY)", money(e["diy_total"]))]
        self.table(cv, 13.6, AREA[3] - 0.3, "COST ESTIMATE - OWNER-BUILDER (DIY)", [("ITEM", 6.6, "l"), ("AMOUNT", 2.0, "r")], rows2, size=0.09, rh=0.3)
        cv.paper()
        sq = e["sqft"]
        yy = 15.0
        cv.text(13.6, yy, "COST PER SQUARE FOOT", 0.11, "text", anchor="start", bold=True)
        cv.text(13.6, yy - 0.45, f"Owner-built: {money(e['diy_psf'])} / sq ft      Contractor: {money(e['gc_psf'])} / sq ft      ({sq:,} sq ft heated)", 0.1, "text", anchor="start")
        # bar chart of category totals
        cats = e["categories"]
        mx = max(c["materials"] + c["labor"] for c in cats)
        by = yy - 1.2
        cv.text(13.6, by, "WHERE THE MONEY GOES (CONTRACTOR BUILD)", 0.1, "text", anchor="start", bold=True)
        for i, c in enumerate(sorted(cats, key=lambda c: -(c["materials"] + c["labor"]))):
            yb = by - 0.4 - i * 0.32
            cv.text(16.6, yb - 0.04, c["name"], 0.075, "text", anchor="end")
            wm = c["materials"] / mx * 9
            wl = c["labor"] / mx * 9
            cv.rect(16.8, yb - 0.1, wm, 0.2, "thin", fill="#0f5f66")
            cv.rect(16.8 + wm, yb - 0.1, wl, 0.2, "thin", fill="#f2c58d")
            cv.text(16.9 + wm + wl, yb - 0.04, money(c["materials"] + c["labor"]), 0.07, "text_lt", anchor="start")
        yl = by - 0.4 - len(cats) * 0.32 - 0.1
        cv.rect(16.8, yl - 0.1, 0.3, 0.2, "thin", fill="#0f5f66")
        cv.text(17.2, yl - 0.05, "Materials", 0.075, "text", anchor="start")
        cv.rect(18.6, yl - 0.1, 0.3, 0.2, "thin", fill="#f2c58d")
        cv.text(19.0, yl - 0.05, "Labor", 0.075, "text", anchor="start")
        self.notes(cv, AREA[0], 6.2, "WHAT THE ESTIMATE INCLUDES AND EXCLUDES", [
            "Includes every material in the materials list (G1.x) at 2026 US national-average prices, plus contractor labor by trade, overhead and profit, permits and contingency.",
            "Excludes: " + "; ".join(e["excludes"]) + ".",
            "Regional costs vary from about 15% below to 45% above these figures; finish choices (cabinets, flooring, windows, appliances) move the total most.",
            f"Use the cost tool at {SITE} to adjust for your region and finish level, then get at least three local bids before you build.",
        ], size=0.085, width_chars=170, lh=0.18)

    # ---------------------------------------------------------------------------------
    # Web previews (SVG, blueprint colors, watermarked)
    # ---------------------------------------------------------------------------------
    def preview(self, mode, watermark=True):
        m = self.m
        x0, y0, x1, y1 = self.extents() if mode == "floor" else (0, 0, m.W, m.D)
        if mode == "floor" and m.mobile and m.roof_type != "gooseneck":
            x0 = 0
        pad = 4.6 if mode == "floor" else 2.5
        s = min(0.36, 10.0 / (x1 - x0 + 2 * pad))
        Wp = (x1 - x0 + 2 * pad) * s
        Hp = (y1 - y0 + 2 * pad) * s + 0.35
        title = {"floor": "floor plan", "electrical": "electrical plan", "plumbing": "plumbing plan"}[mode]
        cv = SvgCanvas(Wp, Hp, f"{self.p['name']} {title} (preview)")
        cv.view((pad - x0) * s, (pad - y0) * s + 0.35, s)
        if mode == "floor":
            V.draw_plan(cv, m, "floor")
            V.plan_dims(cv, m)
        elif mode == "electrical":
            V.draw_plan(cv, m, "electrical")
            V.draw_electrical(cv, m)
        else:
            V.draw_plan(cv, m, "plumbing")
            V.draw_plumbing(cv, m)
        cv.paper()
        cv.text(Wp / 2, 0.14, f"{self.p['name'].upper()}  ·  {title.upper()}  ·  PREVIEW - FULL SET INCLUDES SCHEDULES, NOTES & DIMENSIONS", 0.07, "title", bold=True)
        svg = cv.svg()
        if watermark:
            w, h = Wp * 96, Hp * 96
            wm = (f'<g opacity=".07" fill="#ffffff" font-size="{w / 14:.0f}" font-weight="700" text-anchor="middle" transform="rotate(-24 {w / 2:.0f} {h / 2:.0f})">'
                  f'<text x="{w / 2:.0f}" y="{h / 2:.0f}">PREVIEW</text></g>')
            svg = svg.replace("</svg>", wm + "</svg>")
        return svg

    def preview_elevation(self, fac):
        m = self.m
        info = profile(m)
        L = V.facade_len(m, fac)
        H = info["ridge"] + 2
        s = min(0.3, 9.0 / (L + 14))
        Wp, Hp = (L + 14) * s, (H + 3) * s
        cv = SvgCanvas(Wp, Hp, f"{self.p['name']} {fac} elevation")
        cv.view(5 * s, 1.5 * s, s)
        V.draw_elevation(cv, m, fac)
        return cv.svg()

    # ---------------------------------------------------------------------------------
    # CAD export
    # ---------------------------------------------------------------------------------
    def dxf(self):
        m = self.m
        info = profile(m)
        cv = DxfCanvas()
        gap = (max(m.W, m.D) + 20) * 12
        views = [("FLOOR PLAN", lambda: (V.draw_plan(cv, m, "floor"), V.plan_dims(cv, m))),
                 ("ELECTRICAL PLAN", lambda: (V.draw_plan(cv, m, "electrical"), V.draw_electrical(cv, m))),
                 ("PLUMBING PLAN", lambda: (V.draw_plan(cv, m, "plumbing"), V.draw_plumbing(cv, m))),
                 ("FOUNDATION PLAN", lambda: V.draw_foundation(cv, m)),
                 ("ROOF FRAMING PLAN", lambda: V.draw_framing(cv, m))]
        if m.lofts:
            views.append(("LOFT PLAN", lambda: V.draw_loft(cv, m)))
        for i, (name, fn) in enumerate(views):
            cv.view((i % 3) * gap, -(i // 3) * (m.D + 22) * 12)
            fn()
            cv.text(m.W / 2, -6.5, name, 0.2, "title", bold=True)
        row = -((len(views) + 2) // 3) * (m.D + 22) * 12
        for i, fac in enumerate(("front", "rear", "left", "right")):
            cv.view(i * gap, row - (info["ridge"] + 10) * 12)
            V.draw_elevation(cv, m, fac)
            cv.text(V.facade_len(m, fac) / 2, -3.5, f"{fac.upper()} ELEVATION", 0.2, "title", bold=True)
        cv.view(4 * gap, row - (info["ridge"] + 10) * 12)
        V.draw_section(cv, m)
        cv.text(m.D / 2, -3.5, "BUILDING SECTION", 0.2, "title", bold=True)
        return cv.dxf()
