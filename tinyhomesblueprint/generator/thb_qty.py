"""Materials takeoff and cost estimate, computed from the detailed model.

Quantities include typical waste factors. Unit prices are 2026 US national-average
retail prices for builder-grade materials; labor is a ratio of material cost per trade,
calibrated so a contractor-built total lands inside typical 2026 cost-per-square-foot
ranges. The site's cost tool applies region and finish multipliers to these numbers.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import thb_model as M

CATEGORIES = [
    "Site & foundation", "Trailer / shell", "Framing & sheathing", "Roofing", "Windows & doors", "Exterior finish",
    "Insulation", "Drywall & paint", "Flooring & trim", "Cabinets & counters", "Electrical", "Plumbing",
    "HVAC & ventilation", "Appliances", "Fasteners & misc.",
]
# Contractor labor as a share of material cost, by category.
LABOR = {
    "Site & foundation": 0.85, "Trailer / shell": 0.15, "Framing & sheathing": 1.05, "Roofing": 0.75, "Windows & doors": 0.35,
    "Exterior finish": 0.95, "Insulation": 0.55, "Drywall & paint": 1.6, "Flooring & trim": 0.85, "Cabinets & counters": 0.30,
    "Electrical": 1.5, "Plumbing": 1.35, "HVAC & ventilation": 0.55, "Appliances": 0.05, "Fasteners & misc.": 0.0,
}
FINISH_SENSITIVE = {"Windows & doors", "Exterior finish", "Flooring & trim", "Cabinets & counters", "Appliances", "Drywall & paint", "Plumbing"}


@dataclass
class Item:
    cat: str
    name: str
    qty: float
    unit: str
    price: float
    note: str = ""

    @property
    def total(self):
        return self.qty * self.price


def ceil(x):
    return int(math.ceil(x - 1e-9))


def geometry(m: M.Model):
    """Areas and lengths shared by the takeoff, the sheets and the site."""
    ext = [w for w in m.walls if w.exterior]
    inner = [w for w in m.walls if not w.exterior and not w.open]
    perim = sum(w.length for w in ext)
    int_lf = sum(w.length for w in inner)
    floor = sum(r.area for r in m.heated)
    loft = sum(r.area for r in m.lofts)
    P = m.plate if m.roof_type != "aframe" else 0
    pitch = m.pitch / 12
    ov = 1.0 if not m.mobile else 0.5
    rt = m.roof_type
    if rt in ("gable", "gable-steep", "thow", "gooseneck"):
        rise = m.D / 2 * pitch
        slope = math.hypot(m.D / 2 + ov, rise + ov * pitch)
        roof = 2 * slope * (m.W + 2 * ov)
        gable = m.D * rise          # both gable triangles
        ridge = m.W + 2 * ov
    elif rt in ("shed", "shed-thow", "container-double"):
        rise = m.D * pitch
        slope = math.hypot(m.D + 2 * ov, rise)
        roof = slope * (m.W + 2 * ov)
        gable = m.D * rise          # two trapezoid tops
        ridge = 0
    elif rt == "aframe":
        H = m.D * 1.15
        rise = H
        slope = math.hypot(m.D / 2, H) + ov
        roof = 2 * slope * (m.W + 2 * ov)
        gable = m.D * H            # both triangular gable walls
        ridge = m.W + 2 * ov
    elif rt == "gambrel":
        rise = m.D * 0.62
        low = math.hypot(m.D * 0.16, rise * 0.55)
        up = math.hypot(m.D * 0.34, rise * 0.45)
        slope = low + up + ov
        roof = 2 * slope * (m.W + 2 * ov)
        gable = 2 * (m.D * rise * 0.55 * 0.84 + m.D * 0.68 * rise * 0.45 / 2)
        ridge = m.W + 2 * ov
    else:   # container
        rise, slope, roof, gable, ridge = 0, 0, 0, 0, 0
    wall_gross = perim * P + gable
    openings = sum(o.width * o.height for o in m.openings if o.exterior)
    porch = 0.0
    porch_room = next((r for r in m.rooms if r.kind == "porch"), None)
    if porch_room:
        porch = porch_room.area
    elif m.porch:
        porch = m.porch[2] * m.porch[3]
    return {"perim": perim, "int_lf": int_lf, "floor": floor, "loft": loft, "plate": P, "rise": rise, "roof": roof,
            "roof_slope_len": slope, "gable": gable, "ridge": ridge, "wall_gross": wall_gross, "wall_net": wall_gross - openings,
            "openings": openings, "porch": porch, "overhang": ov, "corners": len(ext)}


def header_for(width):
    if width <= 3.1:
        return "2-2x6"
    if width <= 4.1:
        return "2-2x8"
    if width <= 6.1:
        return "2-2x10"
    return "2-2x12"


def window_size(o):
    def ft_in(v):
        f = int(v); i = round((v - f) * 12)
        return f"{f}'{i}\"" if i else f"{f}'0\""
    return f"{ft_in(o.width)} x {ft_in(o.height)}"


def wire_runs(m: M.Model):
    """Estimate cable length per circuit: home run from the panel plus device-to-device hops, routed orthogonally."""
    panel = next((d for d in m.devices if d.kind == "panel"), None)
    px, py = (panel.x, panel.y) if panel else (0, 0)
    by = {}
    for d in m.devices:
        if d.circuit:
            by.setdefault(d.circuit, []).append(d)
    out = {}
    for c in m.circuits:
        devs = by.get(c.no, [])
        if not devs:
            out[c.no] = 0
            continue
        pts = [(d.x, d.y) for d in devs]
        cur = min(pts, key=lambda q: abs(q[0] - px) + abs(q[1] - py))
        L = abs(cur[0] - px) + abs(cur[1] - py) + 2 * m.plate * 0.5
        rest = [q for q in pts if q is not cur]
        while rest:
            nxt = min(rest, key=lambda q: abs(q[0] - cur[0]) + abs(q[1] - cur[1]))
            L += abs(nxt[0] - cur[0]) + abs(nxt[1] - cur[1]) + 3.0   # drops to boxes
            rest.remove(nxt)
            cur = nxt
        out[c.no] = L * 1.15 + 6
    return out


def pipe_lengths(m: M.Model):
    out = {}
    for p in m.pipes:
        L = sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(p.pts, p.pts[1:]))
        key = (p.kind, p.size)
        out[key] = out.get(key, 0) + L
    return out


def takeoff(m: M.Model):
    g = geometry(m)
    items: list[Item] = []
    add = lambda *a, **k: items.append(Item(*a, **k))
    sq = m.p["sqft"]
    fnd = m.foundation
    wood = not m.container
    ext_stud = m.stud
    stud_len = 10 if g["plate"] >= 9.9 else 9 if g["plate"] >= 8.9 else 8
    spacing = 24 if m.container else 16

    # ---- Site & foundation -------------------------------------------------------------
    A = m.W * m.D
    if fnd == "slab":
        slab = A * (4 / 12) / 27
        edge = g["perim"] * 1.0 * 1.0 / 27
        add("Site & foundation", "Ready-mix concrete, 3,000 psi (4 in. slab + 12 x 12 in. thickened edge)", round((slab + edge) * 1.08, 1), "cu yd", 175)
        add("Site & foundation", "Crushed stone base, 4 in.", round(A * (4 / 12) / 27 * 1.1, 1), "cu yd", 55)
        add("Site & foundation", "Vapor retarder, 10 mil poly", ceil(A * 1.15), "sq ft", 0.12)
        add("Site & foundation", "#4 rebar, 20 ft (18 in. grid + 2 bars in edge)", ceil((A / 1.5 * 2 + g["perim"] * 2) * 1.1 / 20), "ea", 13.50)
        add("Site & foundation", "Anchor bolts, 1/2 x 10 in. with washers", ceil(g["perim"] / 6) + 2 * 4, "ea", 2.25)
        add("Site & foundation", "Rigid foam slab-edge insulation, 2 in. XPS, 2 x 8 ft", ceil(g["perim"] / 8), "sheet", 38)
        add("Site & foundation", "Forms, stakes and pump/finishing supplies (allowance)", 1, "lot", 350 + A * 0.9)
    elif fnd == "crawl":
        add("Site & foundation", "Ready-mix concrete, footings 16 x 8 in. + interior piers", round((g["perim"] * (16 / 12) * (8 / 12) / 27 + (ceil(m.W / 6) + 1) * 0.15) * 1.1, 1), "cu yd", 175)
        add("Site & foundation", "CMU block 8 x 8 x 16 in. (3 courses stem wall)", ceil(g["perim"] / (16 / 12) * 3 * 1.05), "ea", 2.60)
        add("Site & foundation", "Mortar mix, 80 lb", ceil(g["perim"] / 8), "bag", 9.50)
        add("Site & foundation", "Crawlspace vapor barrier, 10 mil", ceil(A * 1.2), "sq ft", 0.14)
        add("Site & foundation", "Foundation vents / access door", ceil(g["perim"] / 10) + 1, "ea", 22)
        add("Site & foundation", "Anchor bolts, 1/2 x 10 in.", ceil(g["perim"] / 6) + 8, "ea", 2.25)
    elif fnd == "piers":
        n = 6 if m.W <= 20 else 8 if m.D <= 8.5 else 12
        add("Site & foundation", "Concrete piers 24 x 24 x 36 in. with weld plates", n, "ea", 210)
        add("Site & foundation", "Gravel pad under unit, 4 in.", round(A * 1.3 * (4 / 12) / 27, 1), "cu yd", 55)
    else:  # trailer
        add("Site & foundation", "Leveling jacks / stabilizers and cribbing", 4 if m.W <= 24 else 6, "ea", 85)
        add("Site & foundation", "Hurricane / ground anchors with straps", 4 if m.W <= 24 else 6, "ea", 45)
    add("Site & foundation", "Excavation, grading and haul-off (allowance)", 1, "lot", 600 if fnd == "trailer" else 1800 + A * 2)

    # ---- Trailer or container shell ------------------------------------------------------
    if m.mobile:
        length = int(round(m.W))
        price = {20: 7500, 24: 8800, 28: 9800, 32: 12500}.get(length, 9000 + (length - 24) * 400)
        if m.roof_type == "gooseneck":
            price += 2500
        add("Trailer / shell", f"{length} ft tiny house trailer, {'gooseneck, ' if m.roof_type == 'gooseneck' else ''}flat deck, 10k-14k lb GVWR, brakes", 1, "ea", price)
        add("Trailer / shell", "Trailer flashing / metal underbelly and sill seal", ceil(m.W * 8.5 * 1.1), "sq ft", 1.10)
    if m.container:
        n = 2 if m.roof_type == "container-double" else 1
        size = "40 ft" if m.W >= 39 else "20 ft"
        add("Trailer / shell", f"{size} high-cube shipping container, one-trip", n, "ea", 6200 if size == "40 ft" else 4200)
        add("Trailer / shell", "Steel tube framing for cut openings (3x3 / 2x4 HSS)", ceil(sum(2 * (o.width + o.height) for o in m.openings if o.exterior) + (m.W * 2 if n == 2 else 0)), "lin ft", 9.50)
        add("Trailer / shell", "Cutting, welding and rust treatment (allowance)", 1, "lot", 900 * n + 120 * len([o for o in m.openings if o.exterior]))
        add("Trailer / shell", "Container delivery and crane set", n, "ea", 1100)

    # ---- Framing & sheathing --------------------------------------------------------------
    ext_open = [o for o in m.openings if o.exterior]
    int_open = [o for o in m.openings if not o.exterior]
    if wood:
        ext_studs = ceil(g["perim"] * 12 / spacing) + len([w for w in m.walls if w.exterior]) + 3 * g["corners"] // 2 + 4 * len(ext_open)
        add("Framing & sheathing", f"{ext_stud} studs, {stud_len} ft (precut), exterior walls @ {spacing} in. o.c.", ceil(ext_studs * 1.1), "ea", 9.80 if ext_stud == "2x6" else 5.40)
        add("Framing & sheathing", f"{ext_stud} plates, 16 ft (1 bottom PT + 2 top), exterior", ceil(g["perim"] * 3 / 16 * 1.08), "ea", 17.50 if ext_stud == "2x6" else 10.50)
        if g["gable"]:
            add("Framing & sheathing", f"{ext_stud} gable / rake wall studs, 10 ft", ceil(g["gable"] / 2 / (spacing / 12) / 4 * 1.15) + 2, "ea", 12.50 if ext_stud == "2x6" else 7.20)
    else:
        add("Framing & sheathing", "2x3 furring studs, 8 ft @ 24 in. o.c. (container walls)", ceil(g["perim"] * 12 / 24 * 1.15), "ea", 4.10)
    if g["int_lf"]:
        int_studs = ceil(g["int_lf"] * 12 / 16) + 2 * len([w for w in m.walls if not w.exterior and not w.open]) + 2 * len(int_open)
        add("Framing & sheathing", f"2x4 studs, {min(stud_len, 9)} ft (precut), interior walls @ 16 in. o.c.", ceil(int_studs * 1.1), "ea", 5.40)
        add("Framing & sheathing", "2x4 plates, 16 ft, interior walls", ceil(g["int_lf"] * 3 / 16 * 1.08), "ea", 10.50)
    hdr = {}
    for o in m.openings:
        if o.exterior or o.width >= 4:
            k = header_for(o.width)
            hdr[k] = hdr.get(k, 0) + o.width + 0.5
    for k, lf in sorted(hdr.items()):
        size = k.split("-")[1]
        add("Framing & sheathing", f"Header stock {size} (doubled, with 1/2 in. spacer), 12 ft", ceil(lf * 2 / 12 * 1.1), "ea", {"2x6": 12, "2x8": 14.5, "2x10": 19.5, "2x12": 26}[size])
    rt = m.roof_type
    nr = ceil(m.W / 2) + 1
    if rt in ("gable", "gable-steep"):
        add("Framing & sheathing", f"Pre-engineered roof trusses, {M.Model.pitch.fget(m):g}:12, {m.D:g} ft span, @ 24 in. o.c. (incl. 2 gable-end trusses)", nr, "ea", 95 + m.D * 6.5 * (1.3 if rt == "gable-steep" else 1))
        add("Framing & sheathing", "Truss hurricane ties (H2.5A) and blocking", nr * 2, "ea", 1.60)
    elif rt in ("thow", "gooseneck"):
        add("Framing & sheathing", f"2x6 rafters, 6 ft @ 24 in. o.c. + 2x8 ridge", nr * 2 + ceil(m.W / 12), "ea", 9)
        add("Framing & sheathing", "Rafter ties / hurricane straps", nr * 2, "ea", 1.60)
    elif rt in ("shed", "shed-thow", "container-double"):
        span = m.D + 2 * g["overhang"]
        size = "2x6" if span <= 9.5 else "2x8" if span <= 13 else "2x10"
        add("Framing & sheathing", f"{size} shed-roof rafters, {ceil(span)} ft @ 24 in. o.c.", nr, "ea", {"2x6": 1.0, "2x8": 1.25, "2x10": 1.65}[size] * ceil(span))
        add("Framing & sheathing", "Rafter hurricane ties", nr * 2, "ea", 1.60)
    elif rt == "aframe":
        L = ceil(g["roof_slope_len"])
        add("Framing & sheathing", f"2x10 A-frame rafters, {L} ft, paired @ 24 in. o.c.", nr * 2, "ea", 2.0 * L)
        add("Framing & sheathing", "2x6 collar ties / loft floor ties", nr, "ea", 1.0 * m.D)
        add("Framing & sheathing", "Ridge board 2x12 and steel ridge straps", ceil(m.W / 12) + 1, "ea", 32)
    elif rt == "gambrel":
        add("Framing & sheathing", "2x6 gambrel rafters (4 members per pair) @ 24 in. o.c.", nr * 4, "ea", 11)
        add("Framing & sheathing", "Plywood gusset plates, 1/2 in.", nr * 3, "ea", 4)
    if fnd == "crawl":
        add("Framing & sheathing", "2x10 floor joists, 12 ft @ 16 in. o.c. (two bays)", ceil(m.W * 12 / 16 + 1) * 2, "ea", 22)
        add("Framing & sheathing", "Built-up beam 3-2x10, 16 ft (center girder)", ceil(m.W / 16) * 3, "ea", 30)
        add("Framing & sheathing", "PT sill plate 2x6, 16 ft + sill seal", ceil(g["perim"] / 16 * 1.1), "ea", 19)
        add("Framing & sheathing", "Joist hangers", ceil(m.W * 12 / 16 + 1) * 2, "ea", 1.40)
    if fnd in ("crawl", "trailer"):
        if fnd == "trailer":
            add("Framing & sheathing", "2x6 floor joists, 8 ft @ 16 in. o.c. (trailer deck)", ceil(m.W * 12 / 16) + 1, "ea", 8.80)
        add("Framing & sheathing", "Subfloor 3/4 in. T&G OSB/ply, 4 x 8", ceil(m.W * m.D / 32 * 1.08), "sheet", 44)
    if g["loft"]:
        add("Framing & sheathing", "2x8 loft joists @ 16 in. o.c. + rim", ceil(sum(r.w for r in m.lofts) * 12 / 16 + 2), "ea", 14)
        add("Framing & sheathing", "Loft subfloor 3/4 in. T&G, 4 x 8", ceil(g["loft"] / 32 * 1.1), "sheet", 44)
        add("Framing & sheathing", "Loft guardrail (36-42 in.) and ladder / ship stair", len(m.lofts), "ea", 420)
    if wood:
        add("Framing & sheathing", "Wall sheathing 7/16 in. OSB, 4 x 8 (9 ft: 4 x 9)", ceil(g["wall_gross"] / 32 * 1.1), "sheet", 21)
        add("Framing & sheathing", "House wrap 9 x 150 ft + seam tape", ceil(g["wall_gross"] * 1.15 / 1350) or 1, "roll", 185)
    if g["roof"]:
        add("Framing & sheathing", "Roof sheathing 1/2 in. CDX plywood, 4 x 8", ceil(g["roof"] / 32 * 1.1), "sheet", 38)
    if g["porch"]:
        add("Framing & sheathing", "Porch: 6x6 PT posts, beams, joists and roof framing (allowance per sq ft)", ceil(g["porch"]), "sq ft", 9.5)
        add("Framing & sheathing", "Porch decking, 5/4 x 6 composite or PT", ceil(g["porch"] * 1.1), "sq ft", 6.5)

    # ---- Roofing ------------------------------------------------------------------------
    roof_all = g["roof"] + (g["porch"] * 1.15 if g["porch"] and next((r for r in m.rooms if r.kind == "porch"), None) is None else 0)
    if roof_all:
        squares = roof_all * 1.12 / 100
        metal = "metal" in m.p.get("roof", "").lower() or m.mobile or rt in ("shed", "container-double")
        if metal:
            add("Roofing", "Standing-seam / exposed-fastener metal roofing panels with trim", round(squares, 1), "square", 520)
            add("Roofing", "Metal ridge cap, closures and fasteners", ceil(max(g["ridge"], m.W) / 10) + 1, "piece", 32)
        else:
            add("Roofing", "Architectural asphalt shingles (3 bundles / square)", ceil(squares * 3), "bundle", 42)
            add("Roofing", "Ridge cap shingles", ceil(g["ridge"] / 20) + 1, "bundle", 65)
            add("Roofing", "Starter strip shingles", ceil((m.W + 2) * 2 / 100) + 1, "bundle", 48)
            add("Roofing", "Roofing nails, 1-1/4 in. coil, 7,200 ct", ceil(squares / 15) + 1, "box", 48)
        add("Roofing", "Synthetic underlayment, 10 square roll", ceil(squares / 10) + 0, "roll", 130)
        add("Roofing", "Ice & water shield at eaves and valleys, 2 square roll", ceil((m.W + 2) * 2 * 3 / 200) + 1, "roll", 120)
        add("Roofing", "Drip edge, 10 ft", ceil(((m.W + 2) * 2 + g["roof_slope_len"] * 4) / 10), "piece", 9.50)
        if g["ridge"] and rt not in ("aframe",):
            add("Roofing", "Ridge vent, 4 ft", ceil(g["ridge"] / 4), "piece", 16)
        add("Roofing", "Gutters 5 in. K-style with downspouts (lin ft)", ceil((m.W + 2) * (2 if rt not in ("shed", "shed-thow", "container-double") else 1)), "lin ft", 7.5)
    if m.container and rt == "container":
        add("Roofing", "Elastomeric roof coating (container roof), 5 gal", ceil(m.W * m.D / 100) + 1, "pail", 165)

    # ---- Windows & doors ------------------------------------------------------------------
    sizes = {}
    for o in m.openings:
        if o.kind == "window":
            key = (window_size(o), o.egress)
            sizes[key] = sizes.get(key, 0) + 1
    for (sz, egr), n in sorted(sizes.items()):
        w, h = [float(v.split("'")[0]) + float(v.split("'")[1].rstrip('"') or 0) / 12 for v in sz.split(" x ")]
        area = w * h
        add("Windows & doors", f"Vinyl {'casement (egress)' if egr else 'single-hung / slider'} window, low-E, {sz}", n, "ea", 180 + area * 22 + (60 if egr else 0))
    clere = m.notes.get("clerestory", [])
    if clere:
        add("Windows & doors", "Fixed clerestory window, low-E, 2'6\" x 1'2\"", len(clere), "ea", 175)
    for o in m.openings:
        if o.kind == "window":
            continue
        if o.exterior:
            if o.kind == "slider":
                add("Windows & doors", f"Exterior sliding glass door, {window_size(o).split(' x ')[0]} wide, low-E", 1, "ea", 1450 if o.width <= 6 else 1900)
            elif o.width >= 5:
                add("Windows & doors", f"Exterior double / barn-style door pair, {window_size(o).split(' x ')[0]}", 1, "ea", 1650)
            else:
                add("Windows & doors", "Exterior prehung door 36 x 80 in., fiberglass, half-lite, with lockset & deadbolt", 1, "ea", 620)
        else:
            if o.kind == "pocket":
                add("Windows & doors", f"Pocket / sliding door kit + slab, {window_size(o).split(' x ')[0]} opening", 1, "ea", 520)
            else:
                add("Windows & doors", f"Interior prehung door {int(round(o.width * 12))} x 80 in., hollow-core, with {'privacy' if o.room and o.room.kind in ('bath', 'bed') else 'passage'} set", 1, "ea", 165)
    add("Windows & doors", "Window & door flashing tape, sill pans and low-expansion foam", 1, "lot", 25 * len(ext_open) + 40)
    if any(r.kind == "bed" for r in m.heated) or m.lofts:
        add("Windows & doors", "Closet doors / shelving kits", len([r for r in m.heated if r.kind == "bed"]), "ea", 210)

    # ---- Exterior finish --------------------------------------------------------------------
    if wood:
        siding = "fiber-cement lap" if "fiber" in m.p.get("walls", "").lower() else "engineered wood / lap" if "lap" in m.p.get("walls", "").lower() else "vertical board-and-batten" if "vertical" in m.p.get("walls", "").lower() else "siding"
        add("Exterior finish", f"Exterior {siding} siding (installed area)", ceil(g["wall_net"] * 1.12), "sq ft", 3.40)
        add("Exterior finish", "Corner boards, window/door trim 1x4 / 1x6 (lin ft)", ceil(g["corners"] * 2 * g["plate"] + sum(2 * (o.width + o.height) for o in ext_open)), "lin ft", 2.10)
        add("Exterior finish", "Soffit & fascia, vented (lin ft)", ceil((m.W + 2) * 2 + (g["roof_slope_len"] * 4 if rt not in ("aframe",) else 0)), "lin ft", 6.2)
        if "stone" in m.p.get("walls", "").lower():
            add("Exterior finish", "Manufactured stone veneer wainscot, 3 ft high, front", ceil(m.W * 3), "sq ft", 11)
        add("Exterior finish", "Exterior paint / stain, primer + 2 coats", ceil(g["wall_net"] * 2 / 350) + 1, "gal", 52)
    else:
        add("Exterior finish", "Direct-to-metal primer + exterior paint for container", ceil(g["perim"] * 9.5 * 2 / 350) + 2, "gal", 68)
    add("Exterior finish", "Caulk, sealants and exterior trim fasteners", 1, "lot", 120 + sq * 0.15)

    # ---- Insulation --------------------------------------------------------------------------
    ceiling = g["floor"] * (1.0 if rt not in ("aframe", "gambrel", "shed", "shed-thow") else 1.25)
    if m.container:
        bf = (g["perim"] * 8.8 + g["floor"]) * 2.0
        add("Insulation", "Closed-cell spray foam, 2 in. walls & ceiling (board feet)", ceil(bf * 1.05), "board ft", 1.25)
        add("Insulation", "Subfloor foam board over container floor, 1 in. XPS", ceil(g["floor"] / 32 * 1.08), "sheet", 26)
    else:
        rv = "R-21 (2x6)" if ext_stud == "2x6" else "R-15 (2x4)"
        add("Insulation", f"Wall insulation {rv} batts or mineral wool", ceil(g["wall_net"] * 1.05), "sq ft", 1.05 if ext_stud == "2x6" else 0.85)
        if rt in ("aframe", "gambrel", "shed", "shed-thow", "thow", "gooseneck"):
            add("Insulation", "Cathedral roof insulation R-30 closed-cell + batt (or rigid above deck)", ceil(g["roof"] * 0.95), "sq ft", 2.40)
        else:
            add("Insulation", "Attic insulation R-38 blown cellulose / fiberglass", ceil(ceiling * 1.05), "sq ft", 1.05)
            add("Insulation", "Attic baffles and air sealing kit", ceil(m.W / 2) * 2 + 1, "ea", 3)
        if fnd in ("crawl", "trailer"):
            add("Insulation", "Floor insulation R-19 / R-21 (or rigid foam under trailer deck)", ceil(m.W * m.D * 1.05), "sq ft", 1.10)
    add("Insulation", "Acoustic batts at bedroom and bath walls", ceil(sum(w.length for w in m.walls if not w.exterior and not w.open and any(r.kind in ('bed', 'bath') for r in w.rooms)) * g["plate"] * 1.05) or 0, "sq ft", 0.95)

    # ---- Drywall & paint ------------------------------------------------------------------------
    walls_in = g["perim"] * (g["plate"] or 8) + g["int_lf"] * 2 * (g["plate"] or 8) + g["gable"] * (1 if rt in ("aframe", "gambrel", "shed", "shed-thow") else 0)
    if rt == "aframe":
        walls_in = g["roof"] * 0.9 + g["gable"]
    ceil_area = ceiling if rt != "aframe" else 0
    dry = walls_in + ceil_area + g["loft"]
    finish_board = "1/4 in. plywood / T&G pine" if m.mobile else "1/2 in. drywall"
    if m.mobile:
        add("Drywall & paint", "Interior wall & ceiling paneling: T&G pine or 1/4 in. plywood (lightweight)", ceil(dry * 1.1), "sq ft", 2.10)
    else:
        add("Drywall & paint", f"Drywall {finish_board}, 4 x 8 (moisture-resistant in baths)", ceil(dry * 1.12 / 32), "sheet", 16.50)
        add("Drywall & paint", "Joint compound, tape, corner bead and screws", ceil(dry / 300) + 1, "kit", 46)
    add("Drywall & paint", "Interior primer + 2 coats paint (walls & ceilings)", ceil(dry * 3 / 400) + 1, "gal", 42)
    add("Drywall & paint", "Paint sundries (rollers, brushes, tape, caulk)", 1, "lot", 90 + sq * 0.1)

    # ---- Flooring & trim -----------------------------------------------------------------------------
    bath_area = sum(r.area for r in m.heated if r.kind == "bath")
    add("Flooring & trim", "Luxury vinyl plank flooring, waterproof, 20 mil", ceil((g["floor"] - bath_area + g["loft"]) * 1.1), "sq ft", 3.20)
    if bath_area:
        add("Flooring & trim", "Porcelain tile floor + shower walls, thinset, grout, backer board", ceil(bath_area * 1.1 + 70 * len([f for f in m.fixtures if f.kind in ('shower', 'tub')])), "sq ft", 6.8)
        add("Flooring & trim", "Shower pan / tub surround kit & waterproofing membrane", len([f for f in m.fixtures if f.kind in ("shower", "tub")]), "ea", 340)
    base = sum(2 * (r.w + r.d) for r in m.heated) - sum(o.width for o in m.openings if o.kind != "window")
    add("Flooring & trim", "Baseboard, primed MDF 3-1/4 in. (lin ft)", ceil(base * 1.1), "lin ft", 1.35)
    add("Flooring & trim", "Door & window casing / stool (lin ft)", ceil(sum(2 * (o.width + o.height) + (o.width if o.kind == "window" else 0) for o in m.openings) * 1.1), "lin ft", 1.45)
    add("Flooring & trim", "Bath accessories (mirror, towel bars, TP holder, shower rod/door)", len([r for r in m.heated if r.kind == "bath"]), "set", 260)

    # ---- Cabinets & counters ------------------------------------------------------------------------
    counter_lf = sum((f.w if f.rot in "SN" else f.d) for f in m.fixtures if f.kind == "counter")
    appl_lf = sum((f.w if f.rot in "SN" else f.d) for f in m.fixtures if f.kind in ("fridge",))
    island = [f for f in m.fixtures if f.kind == "island"]
    base_lf = max(0, counter_lf - appl_lf)
    add("Cabinets & counters", "Base cabinets, shaker, RTA/stock (lin ft)", round(base_lf + sum(max(f.w, f.d) for f in island), 1), "lin ft", 165)
    win_k = sum(o.width for o in m.openings if o.kind == "window" and o.room and o.room.has_kitchen and o.wall.seg.o in "hv")
    add("Cabinets & counters", "Wall cabinets 30-36 in. (lin ft)", round(max(2, base_lf - win_k - 2.5), 1), "lin ft", 120)
    add("Cabinets & counters", "Countertop, quartz or butcher block (sq ft)", ceil((base_lf * 2.1 + sum(f.w * f.d for f in island)) * 1.1), "sq ft", 48)
    lavs = [f for f in m.fixtures if f.kind == "lav"]
    if lavs:
        add("Cabinets & counters", "Bathroom vanity with top", len(lavs), "ea", 340)
    add("Cabinets & counters", "Cabinet hardware, fillers and toe kick", 1, "lot", 60 + base_lf * 9)

    # ---- Electrical -----------------------------------------------------------------------------------
    runs = wire_runs(m)
    cable = {}
    for c in m.circuits:
        cable[c.wire] = cable.get(c.wire, 0) + runs.get(c.no, 0)
    cable_price = {"14/2 NM-B": 0.62, "12/2 NM-B": 0.92, "10/2 NM-B (w/ gnd, 240V)": 1.65, "8/2 NM-B (w/ gnd, 240V)": 2.90,
                   "12/2 NM-B (w/ gnd, 240V)": 0.92, "6/3 NM-B": 5.20, "14/2 NM-B (w/ gnd, 240V)": 0.62}
    for wire, L in sorted(cable.items()):
        rolls = ceil(L / 250) if L > 0 else 0
        add("Electrical", f"Cable {wire}", ceil(L / 25) * 25, "lin ft", cable_price.get(wire, 1.2))
    kinds = {}
    for d in m.devices:
        kinds[d.kind] = kinds.get(d.kind, 0) + 1
    dev_price = {"rec": ("Duplex receptacle 15A, tamper-resistant + plate", 3.5), "gfci": ("GFCI receptacle 20A, TR, WR + plate", 24),
                 "rec20": ("Single receptacle 20A dedicated + plate", 6), "rec240": ("240V receptacle (range/dryer) + plate", 22),
                 "wp": ("Weatherproof GFCI receptacle with in-use cover", 38), "sw": ("Single-pole switch + plate", 4),
                 "sw3": ("3-way switch + plate", 7.5), "light": ("Ceiling light fixture, LED (allowance)", 55),
                 "can": ("LED wafer recessed light, 4 in.", 16), "fan": ("Bath exhaust fan / light, 80 CFM, Energy Star", 120),
                 "sconce": ("Wall sconce / vanity light, LED (allowance)", 65), "smoke": ("Smoke alarm, hardwired, interconnected", 32),
                 "smokeco": ("Smoke / CO combination alarm, hardwired", 52), "jbox": ("Appliance junction box / whip", 14),
                 "inlet": ("50A RV power inlet + cord", 260), "disconnect": ("A/C disconnect, 60A non-fused", 28)}
    for k, n in sorted(kinds.items()):
        if k in dev_price:
            nm, pr = dev_price[k]
            add("Electrical", nm, n, "ea", pr)
    boxes = sum(n for k, n in kinds.items() if k in ("rec", "gfci", "rec20", "rec240", "wp", "sw", "sw3", "light", "sconce", "smoke", "smokeco", "jbox"))
    add("Electrical", "Device / ceiling boxes (new-work)", ceil(boxes * 1.05), "ea", 1.80)
    nbreak = sum(2 if c.volts == 240 else 1 for c in m.circuits)
    spaces = 20 if nbreak <= 18 else 30 if nbreak <= 28 else 40
    add("Electrical", f"Load center {'100A main-lug' if m.mobile else '100A main breaker' if 'A,' in m.notes['load']['service'] and m.notes['load']['service'].startswith('100') else '125-200A main breaker'}, {spaces} spaces", 1, "ea", 240 if spaces <= 20 else 320)
    afci = sum(1 for c in m.circuits if c.volts == 120)
    add("Electrical", "Breakers: combination AFCI / dual-function (120V)", afci, "ea", 48)
    add("Electrical", "Breakers: 2-pole (240V)", sum(1 for c in m.circuits if c.volts == 240), "ea", 22)
    if not m.mobile:
        add("Electrical", "Meter base, service entrance cable, ground rods & bonding", 1, "lot", 650)
    add("Electrical", "Staples, wire nuts, connectors, nail plates", 1, "lot", 80 + sq * 0.12)

    # ---- Plumbing -----------------------------------------------------------------------------------
    pl = pipe_lengths(m)
    pex34 = sum(L for (k, s), L in pl.items() if k == "cold" and s == '3/4"')
    pex12 = sum(L for (k, s), L in pl.items() if k in ("cold", "hot") and s == '1/2"')
    add("Plumbing", "PEX-A 3/4 in. (service + trunk), with fittings allowance", ceil((pex34 + m.plate) * 1.25 / 10) * 10 + 10, "lin ft", 1.35)
    add("Plumbing", "PEX-A 1/2 in. red/blue (branches), with fittings allowance", ceil((pex12 + 3 * len([p for p in m.pipes if p.kind in ('cold', 'hot')])) * 1.25 / 10) * 10, "lin ft", 0.78)
    users = [f for f in m.fixtures if f.kind in M.COLD and f.kind != "fridge"]
    supplies = sum(2 if f.kind in M.HOT else 1 for f in users)
    add("Plumbing", "Quarter-turn angle stops, supply lines, stub-outs", supplies, "ea", 14)
    for size in ('3"', '2"', '1-1/2"', '1-1/4"'):
        L = sum(Lp for (k, s), Lp in pl.items() if k == "waste" and s == size)
        if size == '3"':
            L += (m.plate + geometry(m)["rise"] + 2) if any(f.kind == "toilet" for f in m.fixtures) else 0
        if L:
            add("Plumbing", f"PVC DWV pipe {size} schedule 40, with fittings allowance", ceil(L * 1.3 / 10) * 10, "lin ft", {'3"': 3.4, '2"': 2.1, '1-1/2"': 1.6, '1-1/4"': 1.4}[size])
    add("Plumbing", "DWV fittings, cleanouts, primer & cement (allowance)", 1, "lot", 120 + 35 * len(users))
    if m.mobile:
        add("Plumbing", "RV fresh-water inlet, pressure regulator, sewer outlet & valve", 1, "lot", 240)
    fixture_price = {"toilet": ("Toilet, 1.28 gpf, elongated (or composting toilet on wheels)", 260 if not m.mobile else 1050),
                     "lav": ("Bathroom faucet + drain", 110), "shower": ("Shower valve, trim & drain; 32-36 in. shower base", 420),
                     "tub": ("Bathtub 60 in. alcove + valve/trim", 520), "sink": ("Kitchen sink, stainless + faucet + disposal", 480),
                     "wh": ("Water heater, 40-50 gal electric or heat-pump", 1250), "tankless": ("Tankless electric water heater, point-of-use", 620),
                     "washer": ("Washer box with valves & hammer arrestors", 85), "stack_wd": ("Washer box with valves & hammer arrestors", 85)}
    fk = {}
    for f in m.fixtures:
        if f.kind in fixture_price:
            fk[f.kind] = fk.get(f.kind, 0) + 1
    for k, n in sorted(fk.items()):
        nm, pr = fixture_price[k]
        add("Plumbing", nm, n, "ea", pr)
    add("Plumbing", "Frost-free hose bibbs", 2, "ea", 38)
    add("Plumbing", "Main shutoff, expansion tank, pressure-reducing valve", 1, "lot", 185)

    # ---- HVAC & ventilation ----------------------------------------------------------------------------
    heads = len([d for d in m.devices if d.kind == "minisplit"])
    if heads:
        if heads == 1:
            add("HVAC & ventilation", f"Ductless mini-split heat pump, {'9,000' if sq < 350 else '12,000' if sq < 650 else '18,000'} BTU, single zone, with line set", 1, "ea", 1650 if sq < 350 else 2100)
        else:
            add("HVAC & ventilation", f"Multi-zone ductless heat pump, {heads} heads, {'18,000' if sq < 700 else '24,000'} BTU, with line sets", 1, "ea", 2400 + 750 * heads)
        add("HVAC & ventilation", "Condenser pad / wall bracket, condensate pump and disconnect whip", 1, "lot", 210)
    add("HVAC & ventilation", "Range hood, ducted to exterior, with wall cap", 1, "ea", 240)
    add("HVAC & ventilation", "Exhaust duct, caps and dryer vent kit", 1, "lot", 95 + 45 * len([r for r in m.heated if r.kind == "bath"]))
    if sq >= 400 and not m.mobile:
        add("HVAC & ventilation", "Spot ERV / balanced ventilation (tight-house fresh air)", 1, "ea", 780)

    # ---- Appliances ------------------------------------------------------------------------------------
    appl = {"fridge": ("Refrigerator", 1100 if sq >= 400 else 650), "range": ("Range / induction cooktop", 900 if sq >= 400 else 420),
            "dw": ("Dishwasher, 18-24 in.", 650), "washer": ("Washer", 800), "dryer": ("Dryer (heat-pump or electric)", 850),
            "stack_wd": ("Compact stackable / combo washer-dryer", 1350)}
    for f in m.fixtures:
        if f.kind in appl:
            nm, pr = appl[f.kind]
            add("Appliances", nm, 1, "ea", pr)
    add("Appliances", "Microwave (over-range or countertop)", 1, "ea", 260)

    # ---- Fasteners & misc. ------------------------------------------------------------------------------
    add("Fasteners & misc.", "Framing nails, structural screws, connectors, construction adhesive", 1, "lot", 280 + sq * 0.55)
    add("Fasteners & misc.", "Dumpster / waste haul-off", 1 if sq < 500 else 2, "ea", 520)
    add("Fasteners & misc.", "Temporary power, portable toilet and tool rental (allowance)", 1, "lot", 650 if not m.mobile else 300)

    # Merge duplicate lines (same name and price).
    merged = {}
    for it in items:
        if it.qty <= 0:
            continue
        k = (it.cat, it.name, it.unit, round(it.price, 2))
        if k in merged:
            merged[k].qty += it.qty
        else:
            merged[k] = it
    out = list(merged.values())
    out.sort(key=lambda it: (CATEGORIES.index(it.cat), -it.total))
    return out, g


def estimate(m: M.Model, items):
    sq = m.p["sqft"]
    by = {c: 0.0 for c in CATEGORIES}
    for it in items:
        by[it.cat] += it.total
    cats = []
    for c in CATEGORIES:
        mat = by[c]
        if mat <= 0:
            continue
        cats.append({"name": c, "materials": round(mat), "labor": round(mat * LABOR[c]), "finish": c in FINISH_SENSITIVE})
    materials = sum(c["materials"] for c in cats)
    labor = sum(c["labor"] for c in cats)
    permits = round(800 + sq * 3.2 if not m.mobile else 450 + sq * 1.2, -1)
    design = 0
    overhead = round((materials + labor) * 0.18)
    contingency_diy = round(materials * 0.12)
    contingency_gc = round((materials + labor + overhead) * 0.10)
    diy_help = round(sum(c["labor"] for c in cats if c["name"] in ("Electrical", "Plumbing", "HVAC & ventilation")) * 0.55)
    diy = materials + permits + contingency_diy + diy_help
    gc = materials + labor + overhead + permits + contingency_gc
    return {
        "categories": cats, "materials": materials, "labor": labor, "permits": permits, "overhead": overhead,
        "contingency_diy": contingency_diy, "contingency_gc": contingency_gc, "diy_trade_help": diy_help,
        "diy_total": diy, "gc_total": gc, "diy_psf": round(diy / sq), "gc_psf": round(gc / sq), "sqft": sq,
        "excludes": ["Land", "Utility connections (well/septic or water/sewer taps, power service drop)",
                     "Driveway and landscaping", "Engineering or stamped drawings required by your jurisdiction",
                     "Furniture and window coverings"] + (["Tow vehicle and transport"] if m.mobile else []),
    }
