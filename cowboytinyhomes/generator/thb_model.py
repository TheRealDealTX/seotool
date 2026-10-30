"""Plan detailing: turns a plan's room rectangles (inc/plans.php) into a buildable model.

From the rooms alone it derives walls, doors, windows, kitchen/bath/laundry fixtures,
electrical devices and circuits, and plumbing fixtures and pipe runs. Every drawing,
the materials takeoff, the cost estimate and the 3D model are produced from this model.

Coordinates are feet. x runs along W (left to right on the front elevation), y runs
from the front wall (y = 0) to the rear wall (y = D). Plans are drawn with the front at
the bottom of the sheet, so y increases up the page.
"""
from __future__ import annotations

import json
import math
import os
import re
from dataclasses import dataclass, field

EPS = 1e-6

# Site-specific settings (brand, climate, structure, notes). Each site keeps its own
# generator/profile.json; every .py file is shared verbatim between the sites.
PROFILE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile.json"), encoding="utf-8"))

# ---------------------------------------------------------------------------------------
# Rooms
# ---------------------------------------------------------------------------------------

PUBLIC = {"living", "kitchen", "entry", "studio", "dining", "hall", "stair"}
WET = {"bath", "kitchen", "laundry", "utility"}
UPPER_PLATE = 8.0       # second-floor wall height
FLOOR_DEPTH = 1.0       # second-floor framing + subfloor (11-7/8" I-joists, 3/4" deck)


def room_kind(label: str) -> str:
    L = label.upper()
    if L in ("PORCH", "BREEZEWAY", "DOGTROT", "DOGTROT BREEZEWAY"):
        return "porch"
    if "STAIR" in L:
        return "stair"
    if "BATH" in L or "POWDER" in L:
        return "bath"
    if ("CLOSET" in L or L.startswith("WIC") or "PANTRY" in L) and "W/D" not in L and "LAUNDRY" not in L:
        return "closet"
    if "HALL" in L or "LANDING" in L:
        return "hall"
    if "GREAT ROOM + KITCHEN" in L or "KITCHEN / DINING" in L or "KITCHEN" in L:
        return "kitchen" if "GREAT ROOM" not in L else "living"
    if "STUDIO" in L or "SLEEP / LIVING" in L:
        return "studio"
    if "BED" in L or "PRIMARY" in L or "BUNK" in L:
        return "bed"
    if "UTILITY" in L:
        return "utility"
    if "LAUNDRY" in L or "W/D" in L:
        return "mud" if "MUD" in L else "laundry"
    if "MUD" in L:
        return "mud"
    if "OFFICE" in L or "FLEX" in L or "STUDY" in L:
        return "office"
    if "ENTRY" in L:
        return "entry"
    if "LIVING" in L or "GREAT" in L:
        return "living"
    return "living"


@dataclass
class Room:
    label: str
    x: float
    y: float
    w: float
    d: float
    kind: str = ""
    has_kitchen: bool = False   # combined great room + kitchen
    has_laundry: bool = False   # bath or mudroom with a washer/dryer
    loft: bool = False

    def __post_init__(self):
        self.kind = self.kind or room_kind(self.label)
        L = self.label.upper()
        self.has_kitchen = self.kind == "kitchen" or "KITCHEN" in L
        self.has_laundry = self.kind in ("laundry", "utility") or "W/D" in L or "LAUNDRY" in L

    @property
    def x2(self): return self.x + self.w

    @property
    def y2(self): return self.y + self.d

    @property
    def area(self): return self.w * self.d

    @property
    def cx(self): return self.x + self.w / 2

    @property
    def cy(self): return self.y + self.d / 2

    def edges(self):
        """The four edges as Seg objects, each tagged with which side of the room it is."""
        return [Seg("h", self.y, self.x, self.x2, "S"), Seg("h", self.y2, self.x, self.x2, "N"),
                Seg("v", self.x, self.y, self.y2, "W"), Seg("v", self.x2, self.y, self.y2, "E")]

    def contains(self, px, py):
        return self.x - EPS <= px <= self.x2 + EPS and self.y - EPS <= py <= self.y2 + EPS

    @property
    def title(self):
        return " ".join(w.capitalize() if not w.startswith("W/D") else w for w in self.label.split())


@dataclass
class Seg:
    """Axis-aligned segment. 'h' lies along x at y = c; 'v' lies along y at x = c."""
    o: str
    c: float
    a: float
    b: float
    side: str = ""

    @property
    def length(self): return self.b - self.a

    def point(self, t):
        """Point at distance t along the segment from a."""
        return (self.a + t, self.c) if self.o == "h" else (self.c, self.a + t)

    def at(self, s):
        """Point at axis coordinate s."""
        return (s, self.c) if self.o == "h" else (self.c, s)

    @property
    def p1(self): return self.at(self.a)

    @property
    def p2(self): return self.at(self.b)


def subtract(a: float, b: float, cuts):
    """Return the parts of [a, b] not covered by the (lo, hi) intervals in cuts."""
    parts = [(a, b)]
    for lo, hi in sorted(cuts):
        nxt = []
        for p, q in parts:
            if hi <= p + EPS or lo >= q - EPS:
                nxt.append((p, q))
                continue
            if lo > p + EPS:
                nxt.append((p, lo))
            if hi < q - EPS:
                nxt.append((hi, q))
        parts = nxt
    return [(p, q) for p, q in parts if q - p > 0.05]


# ---------------------------------------------------------------------------------------
# Walls and openings
# ---------------------------------------------------------------------------------------

@dataclass
class Wall:
    seg: Seg
    exterior: bool
    rooms: tuple            # (room,) for exterior, (a, b) for interior
    open: bool = False      # interior boundary left open (open-plan)
    facade: str = ""        # exterior: front | rear | left | right

    @property
    def length(self): return self.seg.length


@dataclass
class Opening:
    kind: str               # door | slider | window | pocket
    wall: Wall
    s: float                # axis coordinate of the opening center
    width: float
    height: float
    sill: float = 0.0
    room: Room | None = None    # the room the door swings into / the window serves
    tag: str = ""
    egress: bool = False
    label: str = ""
    main: bool = False      # the main entry door

    @property
    def a(self): return self.s - self.width / 2

    @property
    def b(self): return self.s + self.width / 2

    @property
    def exterior(self): return self.wall.exterior

    @property
    def center(self): return self.wall.seg.at(self.s)


@dataclass
class Fixture:
    kind: str               # sink, range, fridge, dw, lav, toilet, shower, tub, washer, dryer, stack_wd, wh, counter, bed, island
    x: float
    y: float
    w: float
    d: float
    room: Room | None = None
    rot: int = 0            # side of the room the fixture backs onto: S, N, W or E

    @property
    def cx(self): return self.x + self.w / 2

    @property
    def cy(self): return self.y + self.d / 2

    def back_point(self):
        """Center of the fixture's back edge (where supply and drain lines enter)."""
        return {"S": (self.cx, self.y), "N": (self.cx, self.y + self.d),
                "W": (self.x, self.cy), "E": (self.x + self.w, self.cy)}.get(self.rot, (self.cx, self.cy))


@dataclass
class Device:
    kind: str               # rec, gfci, rec20, rec240, wp, sw, sw3, light, can, fan, cfan, sconce, pendant, smoke, co, panel, minisplit, condenser, data, inlet
    x: float
    y: float
    room: Room | None = None
    circuit: int = 0
    note: str = ""
    loft: bool = False
    level: int = 0          # 0 = main floor, 1 = second floor


@dataclass
class Circuit:
    no: int
    name: str
    amps: int
    volts: int
    va: int
    breaker: str = ""
    wire: str = ""


@dataclass
class Pipe:
    kind: str               # cold | hot | waste | vent
    pts: list
    size: str = ""


# ---------------------------------------------------------------------------------------
# The model
# ---------------------------------------------------------------------------------------

ROOF_PITCH = {"gable": 6, "gable-steep": 12, "thow": 4, "gooseneck": 4, "shed": 2.5, "shed-thow": 1.5,
              "container": 0, "container-double": 1, "aframe": 0, "gambrel": 0}


@dataclass
class Model:
    slug: str
    p: dict
    W: float
    D: float
    rooms: list
    lofts: list
    porch: tuple | None
    roof_type: str
    walls: list = field(default_factory=list)
    openings: list = field(default_factory=list)
    fixtures: list = field(default_factory=list)
    devices: list = field(default_factory=list)
    circuits: list = field(default_factory=list)
    pipes: list = field(default_factory=list)
    notes: dict = field(default_factory=dict)
    level: int = 0              # 0 = main floor model, 1 = second-floor model
    upper: "Model | None" = None
    z0: float | None = None     # finished-floor height of a second-floor model

    # --- basic properties -------------------------------------------------------------
    @property
    def heated(self):
        return [r for r in self.rooms if r.kind != "porch"]

    @property
    def storeys(self):
        """The main-floor model plus the second-floor model, if any."""
        return [self] + ([self.upper] if self.upper else [])

    def all(self, attr):
        """A list attribute (openings, fixtures, pipes, walls, heated) across every storey."""
        out = []
        for s in self.storeys:
            out += getattr(s, attr)
        return out

    @property
    def upper_base(self):
        """Finished-floor height of the second floor above grade."""
        return self.base + self.plate + FLOOR_DEPTH

    @property
    def wall_h(self):
        """Exterior wall height from the main floor to the top plate under the roof."""
        return self.plate + (FLOOR_DEPTH + UPPER_PLATE if self.upper else 0)

    @property
    def overhang(self):
        if self.mobile:
            return 0.5
        return float(self.p.get("overhang", PROFILE.get("overhang", 1.0)))

    @property
    def mobile(self):
        return self.roof_type in ("thow", "shed-thow", "gooseneck")

    @property
    def container(self):
        return self.roof_type.startswith("container")

    @property
    def stud(self):
        """Exterior stud size: '2x6' or '2x4' (containers: furred 2x3 at 24 in.)."""
        if self.container:
            return "2x3"
        m = re.search(r"2x(\d)", self.p.get("walls", ""))
        return f"2x{m.group(1)}" if m else "2x6"

    @property
    def ext_t(self):
        return {"2x6": 0.55, "2x4": 0.40, "2x3": 0.30}[self.stud]

    @property
    def int_t(self):
        return 0.375

    @property
    def base(self):
        """Finished floor height above grade."""
        if self.z0 is not None:
            return self.z0
        if self.mobile:
            return 2.2
        if self.container:
            return 1.0
        if self.foundation == "chassis":
            return 2.5
        return 0.67 if "slab" in self.p.get("foundation", "").lower() and "crawl" not in self.p.get("foundation", "").lower() else 1.5

    @property
    def plate(self):
        """Wall plate height (floor to top of wall framing)."""
        if self.level:
            return UPPER_PLATE
        if "plate" in self.p:
            return float(self.p["plate"])
        return {"thow": 9.0, "gooseneck": 9.0, "shed-thow": 10.0, "container": 9.0, "container-double": 9.0,
                "shed": 10.0, "aframe": 0.0, "gambrel": 6.5}.get(self.roof_type, 9.0 if "9'" in self.p.get("ceiling", "") or True else 8.0)

    @property
    def pitch(self):
        m = re.search(r"(\d+(?:\.\d+)?):12", self.p.get("roof", ""))
        if m and self.roof_type in ("gable", "gable-steep", "shed", "thow"):
            return float(m.group(1))
        return ROOF_PITCH.get(self.roof_type, 6)

    @property
    def foundation(self):
        f = self.p.get("foundation", "").lower()
        if self.mobile:
            return "trailer"
        if "chassis" in f:
            return "chassis"             # park model: steel chassis set on piers
        if "pier" in f and "slab" not in f:
            return "piers"
        if "pier" in f or "footing" in f:
            return "piers" if self.container else "slab"
        if "crawl" in f and "slab" not in f:
            return "crawl"
        return "slab"

    def room_by_kind(self, *kinds):
        return [r for r in self.heated if r.kind in kinds]

    # --- facade naming ----------------------------------------------------------------
    def facade_of(self, seg: Seg) -> str:
        if seg.o == "h":
            return "front" if abs(seg.c) < EPS else "rear" if abs(seg.c - self.D) < EPS else ""
        return "left" if abs(seg.c) < EPS else "right" if abs(seg.c - self.W) < EPS else ""

    def walls_of(self, room: Room, exterior=None):
        out = []
        for w in self.walls:
            if room in w.rooms and (exterior is None or w.exterior == exterior):
                out.append(w)
        return out

    def openings_on(self, wall: Wall):
        return [o for o in self.openings if o.wall is wall]

    def free_spans(self, wall: Wall, pad=0.3, kinds=("door", "slider", "pocket", "window")):
        cuts = [(o.a - pad, o.b + pad) for o in self.openings_on(wall) if o.kind in kinds]
        return subtract(wall.seg.a, wall.seg.b, cuts)

    def inward(self, wall: Wall, room: Room):
        """Unit normal pointing from the wall into the room."""
        s = wall.seg
        if s.o == "h":
            return (0, 1) if room.cy > s.c else (0, -1)
        return (1, 0) if room.cx > s.c else (-1, 0)

    def wall_side(self, wall: Wall, room: Room) -> str:
        nx, ny = self.inward(wall, room)
        return {(0, 1): "S", (0, -1): "N", (1, 0): "W", (-1, 0): "E"}[(nx, ny)]

    def exterior_kind(self, wall):
        """Can this exterior wall take windows and doors at a normal height?"""
        if self.roof_type == "aframe":
            return wall.seg.o == "v"     # only gable ends are walls; the long sides are roof
        return True


# ---------------------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------------------

def build_model(slug: str, p: dict) -> Model:
    rooms = [Room(r[0], *map(float, r[1:5])) for r in p["rooms"]]
    lofts = [Room(r[0], *map(float, r[1:5]), kind="loft", loft=True) for r in p.get("loft", [])]
    m = Model(slug, p, float(p["W"]), float(p["D"]), rooms, lofts, tuple(p["porch"]) if p.get("porch") else None,
              p.get("roof_type", "gable"))
    _walls(m)
    _doors(m)
    _windows(m)
    _fixtures(m)
    living, panel_room = _electrical(m)
    if p.get("upper"):
        # Second floor: same footprint, its own walls, doors, windows, fixtures and devices.
        # Tags continue the main-floor numbering; devices join the main panel.
        up = Model(slug, p, m.W, m.D, [Room(r[0], *map(float, r[1:5])) for r in p["upper"]], [], None, m.roof_type,
                   level=1, z0=m.upper_base)
        m.upper = up
        m.notes["stair_rise"] = up.notes["stair_rise"] = m.plate + FLOOR_DEPTH
        _walls(up)
        _doors(up)
        _windows(up, start=(sum(o.kind != "window" for o in m.openings), sum(o.kind == "window" for o in m.openings)))
        _fixtures(up)
        _electrical(up)
        for d in up.devices:
            d.level = 1
        m.devices += up.devices
    _circuits(m, living, panel_room)
    _plumbing(m)
    if m.upper:
        _plumbing(m.upper, below=m)
    if m.roof_type in ("shed", "shed-thow"):
        # Clerestory band high on the tall front wall: (x center, width) pairs.
        n = max(1, int((m.W - 2) // 4))
        m.notes["clerestory"] = [(1 + (m.W - 2) * (i + 0.5) / n, 2.5) for i in range(n)]
    return m


def plan_type(m: Model) -> str:
    """house | adu | studio | park-model | thow (selects the code notes on the cover)."""
    return m.p.get("type") or ("thow" if m.mobile else "house")


def aframe_height(m: Model) -> float:
    """A-frame apex height above the floor."""
    return m.D * 1.15


def _walls(m: Model):
    heated = m.heated
    # Interior walls: shared edges between heated rooms.
    for i, a in enumerate(heated):
        for b in heated[i + 1:]:
            for ea in a.edges():
                for eb in b.edges():
                    if ea.o != eb.o or abs(ea.c - eb.c) > EPS or {ea.side, eb.side} not in ({"N", "S"}, {"E", "W"}):
                        continue
                    lo, hi = max(ea.a, eb.a), min(ea.b, eb.b)
                    if hi - lo > 0.5:
                        opn = a.kind in PUBLIC and b.kind in PUBLIC
                        m.walls.append(Wall(Seg(ea.o, ea.c, lo, hi), False, (a, b), open=opn))
    # Exterior walls: room edges not shared with another heated room (porch rooms count as outside).
    for r in heated:
        for e in r.edges():
            cuts = []
            for o in heated:
                if o is r:
                    continue
                for eo in o.edges():
                    if eo.o == e.o and abs(eo.c - e.c) < EPS and {e.side, eo.side} in ({"N", "S"}, {"E", "W"}):
                        cuts.append((eo.a, eo.b))
            for lo, hi in subtract(e.a, e.b, cuts):
                seg = Seg(e.o, e.c, lo, hi, e.side)
                fac = {"S": "front", "N": "rear", "W": "left", "E": "right"}[e.side]
                if _faces_court(m, seg, r):
                    fac = "court"      # faces a breezeway between two wings: hidden on the elevations
                m.walls.append(Wall(seg, True, (r,), facade=fac))


def _faces_court(m: Model, seg: Seg, r: Room) -> bool:
    """True when the wall looks across an open breezeway at another heated room."""
    mid = (seg.a + seg.b) / 2
    if seg.o == "v":
        if abs(seg.c) < EPS or abs(seg.c - m.W) < EPS:
            return False
        d = 1 if seg.c >= r.x2 - EPS else -1
        return any(o is not r and o.y < mid < o.y2 and (o.x >= seg.c - EPS if d > 0 else o.x2 <= seg.c + EPS) for o in m.heated)
    if abs(seg.c) < EPS or abs(seg.c - m.D) < EPS:
        return False
    d = 1 if seg.c >= r.y2 - EPS else -1
    return any(o is not r and o.x < mid < o.x2 and (o.y >= seg.c - EPS if d > 0 else o.y2 <= seg.c + EPS) for o in m.heated)


def _place_on(m: Model, wall: Wall, width: float, prefer: str = "center", pad: float = 0.4, near=None):
    """Find an axis coordinate for an opening of the given width on a wall, avoiding other openings."""
    spans = [(a, b) for a, b in m.free_spans(wall, pad=0.25) if b - a >= width + 2 * pad - EPS]
    if not spans:
        return None
    if near is not None:
        best = None
        for a, b in spans:
            s = min(max(near, a + pad + width / 2), b - pad - width / 2)
            if best is None or abs(s - near) < abs(best - near):
                best = s
        return best
    a, b = max(spans, key=lambda t: t[1] - t[0])
    if prefer == "center":
        return (a + b) / 2
    if prefer == "start":
        return a + pad + width / 2
    return b - pad - width / 2


def _on_rect_edge(seg: Seg, r: Room) -> bool:
    if seg.o == "h":
        return (abs(seg.c - r.y) < EPS or abs(seg.c - r.y2) < EPS) and min(seg.b, r.x2) - max(seg.a, r.x) > 1
    return (abs(seg.c - r.x) < EPS or abs(seg.c - r.x2) < EPS) and min(seg.b, r.y2) - max(seg.a, r.y) > 1


def _touches_exterior_at(m, wall: Wall, end: str) -> bool:
    s = wall.seg
    px, py = s.p1 if end == "a" else s.p2
    return px < EPS or py < EPS or px > m.W - EPS or py > m.D - EPS


def _doors(m: Model):
    heated = m.heated
    interior = [w for w in m.walls if not w.exterior and not w.open]
    # ---- main entry ------------------------------------------------------------------
    entry_wall = None
    entry_s = None
    entry_fac = m.p.get("entry")
    if m.level:
        pass                                 # second floor: reached by the stair, no exterior door
    elif entry_fac:
        # Forced entry facade (e.g. a front door with the porch at the rear).
        cands = [w for w in m.walls if w.exterior and w.facade == entry_fac]
        cands.sort(key=lambda w: ({"entry": -1, "living": 0, "hall": 0.2, "studio": 0, "dining": 1, "kitchen": 1.5, "mud": 0.5}.get(w.rooms[0].kind, 5), -w.length))
        if cands:
            entry_wall = cands[0]
            entry_s = (entry_wall.seg.a + entry_wall.seg.b) / 2
    elif m.roof_type in ("aframe", "gambrel"):
        cands = [w for w in m.walls if w.exterior and w.facade == "left"]
        cands.sort(key=lambda w: (w.rooms[0].kind not in PUBLIC, -w.length))
        entry_wall = cands[0] if cands else None
        if entry_wall:
            entry_s = (entry_wall.seg.a + entry_wall.seg.b) / 2
    else:
        porch_rooms = [r for r in m.rooms if r.kind == "porch"]
        porch_rect = None
        if porch_rooms:
            pr = porch_rooms[0]
            porch_rect = (pr.x, pr.y, pr.w, pr.d)
        elif m.porch:
            porch_rect = m.porch
        cands = []
        for w in m.walls:
            if not w.exterior:
                continue
            r = w.rooms[0]
            score = {"living": 0, "entry": -1, "mud": 0.5, "studio": 0, "kitchen": 1.5, "dining": 1}.get(r.kind, 5)
            if porch_rect:
                px, py, pw, pd = porch_rect
                s = w.seg
                # wall must lie on the porch boundary
                if s.o == "h" and (abs(s.c - py) < EPS or abs(s.c - (py + pd)) < EPS):
                    lo, hi = max(s.a, px), min(s.b, px + pw)
                elif s.o == "v" and (abs(s.c - px) < EPS or abs(s.c - (px + pw)) < EPS):
                    lo, hi = max(s.a, py), min(s.b, py + pd)
                else:
                    continue
                if hi - lo < 3.8:
                    continue
                cands.append((score, -(hi - lo), w, (lo + hi) / 2))
            else:
                if m.container and w.facade in ("left", "right") and r.kind in ("living", "studio"):
                    cands.append((score - 2, -w.length, w, (w.seg.a + w.seg.b) / 2))
                elif w.facade == "front":
                    cands.append((score, -w.length, w, (w.seg.a + w.seg.b) / 2))
        cands.sort(key=lambda t: (t[0], t[1]))
        if not cands or cands[0][0] >= 5:
            # The porch only touches private rooms: enter through the front wall of a public room instead.
            cands = [(0, -w.length, w, (w.seg.a + w.seg.b) / 2) for w in m.walls
                     if w.exterior and w.facade == "front" and w.rooms[0].kind in PUBLIC] or cands
        if cands:
            _, _, entry_wall, entry_s = cands[0]
    if entry_wall:
        glass = m.container and entry_wall.facade in ("left", "right")
        width = min(6.0, entry_wall.length - 1) if glass else 3.0
        if m.roof_type == "aframe":
            glass, width = True, min(6.0, entry_wall.length - 2)
        if m.roof_type == "gambrel":
            width = 5.0
        s = _place_on(m, entry_wall, width, near=entry_s, pad=0.3)
        if s is not None:
            m.openings.append(Opening("slider" if glass else "door", entry_wall, s, width, 6.67 if not glass else 6.83,
                                      room=entry_wall.rooms[0], label="Entry", tag="ENTRY", main=True))
    m.notes["entry"] = entry_wall

    # ---- interior doors: connect every enclosed room back to the public rooms ----------
    reach = {id(r) for r in heated if r.kind in PUBLIC}
    if not reach and heated:
        reach = {id(max(heated, key=lambda r: r.area))}
    pending = [r for r in heated if id(r) not in reach]
    rank_via = {"living": 0, "kitchen": 0.3, "entry": 0, "studio": 0, "dining": 0, "hall": 0.1, "mud": 0.5, "laundry": 1.2,
                "utility": 1.4, "office": 1.6, "bed": 2.0, "closet": 2.2, "bath": 2.5, "stair": 3.5}
    if not m.level and len(heated) > 1 and any(w.facade == "court" for w in m.walls):
        # Public rooms count as reached only when the entry connects to them through open
        # walls; a wing across a breezeway starts unreached and gets its own door.
        start = entry_wall.rooms[0] if entry_wall else max(heated, key=lambda r: r.area)
        reach = {id(start)}
        grow = True
        while grow:
            grow = False
            for w in m.walls:
                if w.open and any(id(r) in reach for r in w.rooms) and not all(id(r) in reach for r in w.rooms):
                    reach.update(id(r) for r in w.rooms)
                    grow = True
        pending = [r for r in heated if id(r) not in reach]
    guard = 0
    while pending and guard < 50:
        guard += 1
        best = None
        for r in pending:
            for w in interior:
                if r not in w.rooms:
                    continue
                other = w.rooms[0] if w.rooms[1] is r else w.rooms[1]
                if id(other) not in reach:
                    continue
                width = 2.5 if r.kind in ("bath", "laundry", "utility") else 2.67
                if r.kind == "office" and "FLEX" in r.label:
                    width = 6.0
                if w.length < width + 0.6:
                    continue
                score = rank_via.get(other.kind, 3) - min(w.length, 10) * 0.01
                if r.kind == "closet" and other.kind == "bed":
                    score -= 3                     # walk-in closets open off the bedroom
                if best is None or score < best[0]:
                    best = (score, r, w, width)
        if not best and not m.level:
            # Nothing reachable from inside: a separate wing. Give its most public room an
            # exterior door on the breezeway (or porch) side, then keep connecting from there.
            porch_rooms = [q for q in m.rooms if q.kind == "porch"]
            opts = []
            for r in pending:
                for w in m.walls_of(r, exterior=True):
                    if w.length < 3.8:
                        continue
                    on_porch = w.facade == "court" or any(_on_rect_edge(w.seg, q) for q in porch_rooms)
                    opts.append((rank_via.get(r.kind, 3) - (2 if on_porch else 0) + (0.5 if r.kind == "bath" else 0), -w.length, r, w))
            if not opts:
                break
            opts.sort(key=lambda t: (t[0], t[1]))
            _, _, r, w = opts[0]
            s = _place_on(m, w, 3.0, prefer="center")
            if s is not None:
                m.openings.append(Opening("door", w, s, 3.0, 6.67, room=r, label="Breezeway entry", tag="ENTRY2"))
            reach.add(id(r))
            pending.remove(r)
            grow = True
            while grow:
                grow = False
                for w2 in m.walls:
                    if w2.open and any(id(q) in reach for q in w2.rooms) and not all(id(q) in reach for q in w2.rooms):
                        for q in w2.rooms:
                            if id(q) not in reach:
                                reach.add(id(q))
                                pending.remove(q)
                        grow = True
            continue
        if not best:
            break
        _, r, w, width = best
        # Push the door toward the interior end of the wall (away from exterior corners).
        ea, eb = _touches_exterior_at(m, w, "a"), _touches_exterior_at(m, w, "b")
        prefer = "start" if eb and not ea else "end" if ea and not eb else "center"
        s = _place_on(m, w, width, prefer=prefer, pad=0.35)
        if s is not None:
            kind = "pocket" if width >= 5 else "door"
            m.openings.append(Opening(kind, w, s, width, 6.67, room=r, label=r.title))
        reach.add(id(r))
        pending.remove(r)
    # Open-plan boundaries become cased openings (drawn without a wall).

    # ---- secondary exterior door from a mudroom, laundry or utility room ------------------
    for r in heated:
        if m.level:
            break
        if r.kind not in ("mud",) and not (r.kind in ("laundry", "utility") and r.area >= 30 and not m.mobile and not m.container):
            continue
        if any(o.exterior and o.kind in ("door", "slider") and o.room is r for o in m.openings):
            continue
        ws = [w for w in m.walls_of(r, exterior=True) if m.exterior_kind(w) and w.length >= 3.8]
        ws.sort(key=lambda w: (w.facade != "rear", w.facade != "left", -w.length))
        for w in ws:
            s = _place_on(m, w, 3.0, prefer="center")
            if s is not None:
                m.openings.append(Opening("door", w, s, 3.0, 6.67, room=r, label="Rear entry" if w.facade == "rear" else "Side entry", tag="REAR"))
                break
            break
    # Code: a house needs a second way out from bedrooms - egress windows handle that.


WIN = {  # kind: (width, height, sill)
    "bed": (3.0, 4.0, 2.0), "living": (3.0, 5.0, 1.5), "studio": (3.0, 5.0, 1.5), "dining": (3.0, 5.0, 1.5),
    "office": (3.0, 4.0, 2.5), "kitchen": (3.0, 3.0, 3.5), "bath": (2.0, 2.0, 5.0), "laundry": (2.0, 3.0, 4.0),
    "utility": (2.0, 2.0, 5.0), "mud": (2.0, 3.0, 4.0), "entry": (2.0, 5.0, 1.5),
}


def _windows(m: Model, start=(0, 0)):
    for r in m.heated:
        if r.kind not in WIN:
            continue
        ww, wh, sill = WIN[r.kind]
        if m.container:
            wh = min(wh, 4.0)
        if m.mobile and r.kind in ("living", "studio"):
            wh = 4.5
        if m.roof_type == "gooseneck" and r.x >= m.W - 8 - EPS:
            # Raised gooseneck floor (3'-2" up): lower sill and shorter sash so the window stays under the eave.
            sill = min(sill, 1.5)
            wh = min(wh, math.floor((m.plate - 3.2 - sill - 0.5) * 2) / 2)
        walls = [w for w in m.walls_of(r, exterior=True) if m.exterior_kind(w)]
        walls.sort(key=lambda w: -w.length)
        if not walls:
            continue
        if r.kind == "bed":
            placed = 0
            for w in walls[:2]:
                if w.length < ww + 1:
                    continue
                s = _place_on(m, w, ww, prefer="center", pad=0.6)
                if s is not None:
                    m.openings.append(Opening("window", w, s, ww, wh, sill, room=r, egress=placed == 0))
                    placed += 1
        elif r.kind in ("living", "studio", "dining", "entry") or (r.kind == "kitchen" and r.has_kitchen and r.area > 150) or (r.kind == "office" and r.area >= 120):
            for w in walls:
                n = int(w.length // 6.5)
                if n == 0 and w.length >= ww + 1.6:
                    n = 1
                for i in range(n):
                    target = w.seg.a + w.length * (i + 0.5) / n
                    s = _place_on(m, w, ww, near=target, pad=0.5)
                    if s is not None:
                        m.openings.append(Opening("window", w, s, ww, wh, sill, room=r,
                                                  egress=r.kind == "studio" and not any(o.egress and o.room is r for o in m.openings)))
        else:
            for w in walls:
                if w.length < ww + 1.2:
                    continue
                s = _place_on(m, w, ww, prefer="center", pad=0.5)
                if s is not None:
                    m.openings.append(Opening("window", w, s, ww, wh, sill, room=r))
                    break
    # A-frame gable ends: windows must sit under the roof slope.
    if m.roof_type == "aframe":
        H = m.D * 1.15
        keep = []
        for o in m.openings:
            if o.exterior and o.wall.seg.o == "v":
                edge = min(o.a, m.D - o.b)
                room_h = edge * 2 * H / m.D - 0.5
                if o.sill + o.height > room_h:
                    if o.kind == "window" and room_h - o.sill >= 2:
                        o.height = math.floor((room_h - o.sill) * 2) / 2
                    elif o.kind != "window":
                        o.height = min(o.height, max(6.67, room_h))
                    else:
                        continue
            keep.append(o)
        m.openings[:] = keep
    # Tags: doors D1.., windows W1.. in a stable order (front, right, rear, left, interior).
    order = {"front": 0, "right": 1, "rear": 2, "left": 3, "porch": 4, "": 5}
    m.openings.sort(key=lambda o: (o.kind == "window", order.get(o.wall.facade, 5), o.wall.seg.o, o.wall.seg.c, o.s))
    di, wi = start
    for o in m.openings:
        if o.kind == "window":
            wi += 1
            o.tag = f"W{wi}"
        else:
            di += 1
            o.tag = f"D{di}"


# ---------------------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------------------

def _wall_runs(m: Model, r: Room, avoid_doors=True):
    """Usable straight runs along each side of a room, inside the room, as (side, a, b)."""
    out = []
    for e in r.edges():
        cuts = []
        for o in m.openings:
            s = o.wall.seg
            if s.o != e.o or abs(s.c - e.c) > EPS:
                continue
            if o.kind == "window":
                continue
            if avoid_doors:
                cuts.append((o.a - 0.25, o.b + 0.25))
        # open sides (no wall) cannot take counters
        for w in m.walls:
            if w.open and r in w.rooms and w.seg.o == e.o and abs(w.seg.c - e.c) < EPS:
                cuts.append((w.seg.a, w.seg.b))
        for a, b in subtract(e.a, e.b, cuts):
            out.append((e.side, a, b))
    return out


def _windows_on_side(m, r, side):
    e = {e.side: e for e in r.edges()}[side]
    return [o for o in m.openings if o.kind == "window" and o.wall.seg.o == e.o and abs(o.wall.seg.c - e.c) < EPS
            and e.a - EPS <= o.s <= e.b + EPS]


def _rect_on_side(r: Room, side: str, s0: float, length: float, depth: float):
    """Rectangle (x, y, w, d) backed against a room side, starting at axis coordinate s0."""
    if side == "S":
        return (s0, r.y, length, depth)
    if side == "N":
        return (s0, r.y2 - depth, length, depth)
    if side == "W":
        return (r.x, s0, depth, length)
    return (r.x2 - depth, s0, depth, length)


def _add(m, kind, rect, r, side):
    x, y, w, d = rect
    f = Fixture(kind, x, y, w, d, r, side)
    m.fixtures.append(f)
    return f


def _fixtures(m: Model):
    wh_room = None
    for kinds in (("utility",), ("laundry",), ("mud",), ("bath",), ("kitchen",)):
        if m.level:
            break                            # the water heater stays on the main floor
        rs = [r for r in m.heated if r.kind in kinds and (kinds != ("mud",) or r.has_laundry) and not _half_bath(r)]
        if rs:
            wh_room = max(rs, key=lambda r: r.area)
            break
    m.notes["wh_room"] = wh_room
    for r in m.heated:
        rr = _headroom_proxy(m, r)
        n0 = len(m.fixtures)
        if r.has_kitchen:
            _kitchen(m, rr)
        if r.kind == "bath":
            _bath(m, rr, wh=(r is wh_room))
        if r.kind in ("laundry", "utility") or (r.kind == "mud" and r.has_laundry):
            _laundry(m, rr, wh=(r is wh_room))
        if r.kind == "bed" or (r.kind == "studio"):
            _bed(m, rr)
        for f in m.fixtures[n0:]:
            f.room = r
        if r.kind == "kitchen" and r is wh_room and not any(f.kind == "wh" for f in m.fixtures):
            pass
    if not m.level and not any(f.kind in ("wh", "tankless") for f in m.fixtures):
        # No room took the heater: mount a tankless unit on the kitchen wall.
        k = next((f for f in m.fixtures if f.kind == "sink"), None) or next((f for f in m.fixtures if f.kind == "lav"), None)
        if k:
            _add(m, "tankless", (k.x, k.y, 1.2, 0.6) if k.rot in ("S", "N") else (k.x, k.y, 0.6, 1.2), k.room, k.rot)
    for lr in m.lofts:
        if "STORAGE" not in lr.label.upper():
            _bed(m, lr)


def knee_offset(m: Model) -> float:
    """A-frame: distance in from each long side to where the roof is 5 ft above the floor (knee wall)."""
    return 5 * m.D / (2 * aframe_height(m)) if m.roof_type == "aframe" else 0.0


def _headroom_proxy(m: Model, r: Room) -> Room:
    """In an A-frame, fixtures stand against knee walls at 5 ft headroom, not the sloped roof."""
    off = knee_offset(m)
    if not off:
        return r
    y0, y1 = max(r.y, off), min(r.y2, m.D - off)
    if y1 - y0 < 3:
        return r
    return Room(r.label, r.x, y0, r.w, y1 - y0)


def _kitchen(m: Model, r: Room):
    small = r.kind != "kitchen" or "KITCHENETTE" in r.label.upper() or r.area < 45
    runs = _wall_runs(m, r)
    if not runs:
        return
    # Prefer a run on an exterior wall with a window, then the longest.
    def score(run):
        side, a, b = run
        ext = any(w.exterior and w.seg.o == ("h" if side in "SN" else "v") and abs(w.seg.c - (r.y if side == "S" else r.y2 if side == "N" else r.x if side == "W" else r.x2)) < EPS
                  for w in m.walls_of(r))
        win = bool(_windows_on_side(m, r, side))
        return (b - a) + (3 if win else 0) + (1 if ext else 0)
    if r.has_kitchen and r.kind != "kitchen":
        # Great room with a kitchen: use the run farthest from the entry door.
        entry = next((o for o in m.openings if o.main), None)
        ex, ey = entry.center if entry else (0, 0)
        runs.sort(key=lambda run: -((b := run[2]) - run[1]) * 0.2 - math.dist((ex, ey), _run_mid(r, run)))
        main = runs[0]
        main = (main[0], main[1], min(main[2], main[1] + 12))
    else:
        runs.sort(key=lambda run: -score(run))
        main = runs[0]
    side, a, b = main
    L = b - a
    if L < 4:
        return
    depth = 2.0
    _add(m, "counter", _rect_on_side(r, side, a, L, depth), r, side)
    wins = _windows_on_side(m, r, side)
    sink_s = wins[0].s if wins else a + L * 0.5
    sw = 2.0 if small else 2.75
    sink_s = min(max(sink_s, a + sw / 2 + (2.6 if L > 8 else 0.2)), b - sw / 2 - (2.6 if L > 8 else 0.2))
    _add(m, "sink", _rect_on_side(r, side, sink_s - sw / 2, sw, depth), r, side)
    # Fridge at the end farthest from the sink, range between with landing space.
    fw = 2.0 if small else 2.75
    rw = 2.0 if small else 2.5
    left_room, right_room = sink_s - sw / 2 - a, b - (sink_s + sw / 2)
    if right_room >= left_room:
        f0 = b - fw
        r0 = max(sink_s + sw / 2 + 1.25, (sink_s + sw / 2 + f0) / 2 - rw / 2)
        if r0 + rw > f0 - 0.1:
            r0 = None
    else:
        f0 = a
        r0 = min(sink_s - sw / 2 - 1.25 - rw, (f0 + fw + sink_s - sw / 2) / 2 - rw / 2)
        if r0 < f0 + fw + 0.1:
            r0 = None
    galley_other = None
    if r0 is None:
        # Not enough room on one run: put the range across a galley, or beside the sink.
        others = [run for run in runs if run is not main and run[2] - run[1] >= rw + 1]
        opp = {"S": "N", "N": "S", "W": "E", "E": "W"}[side]
        others.sort(key=lambda run: (run[0] != opp, -(run[2] - run[1])))
        if others and min(r.w, r.d) <= 10:
            galley_other = others[0]
    _add(m, "fridge", _rect_on_side(r, side, f0, fw, 2.5), r, side)
    island = r.kind == "kitchen" and min(r.w, r.d) >= 12 and r.area >= 140
    if r0 is None and not galley_other and not island:
        others = [run for run in runs if run is not main and run[2] - run[1] >= rw + 1]
        if others:
            galley_other = max(others, key=lambda run: run[2] - run[1])
    if r0 is not None:
        _add(m, "range", _rect_on_side(r, side, r0, rw, depth), r, side)
    elif galley_other:
        gs, ga, gb = galley_other
        gl = min(gb - ga, 8)
        _add(m, "counter", _rect_on_side(r, gs, ga, gl, depth), r, gs)
        _add(m, "range", _rect_on_side(r, gs, ga + (gl - rw) / 2, rw, depth), r, gs)
    if not small and L >= 10:
        ds = sink_s + sw / 2 if right_room >= left_room else sink_s - sw / 2 - 2
        _add(m, "dw", _rect_on_side(r, side, ds, 2.0, depth), r, side)
    # Island in a deep kitchen.
    if r.kind == "kitchen" and min(r.w, r.d) >= 12 and r.area >= 140:
        iw, idp = min(6, r.w - 7), 3
        if side in "SN":
            iy = r.cy - idp / 2
            m.fixtures.append(Fixture("island", r.cx - iw / 2, iy, iw, idp, r, side))
        else:
            ix = r.cx - idp / 2
            m.fixtures.append(Fixture("island", ix, r.cy - iw / 2, idp, iw, r, side))
        if r0 is None and not galley_other:
            isl = m.fixtures[-1]
            cw = 2.5
            if side in "SN":
                m.fixtures.append(Fixture("range", isl.cx - cw / 2, isl.y, cw, 2.0, r, "S" if side == "N" else "N"))
            else:
                m.fixtures.append(Fixture("range", isl.x, isl.cy - cw / 2, 2.0, cw, r, "W" if side == "E" else "E"))


def _run_mid(r, run):
    side, a, b = run
    s = (a + b) / 2
    return {"S": (s, r.y), "N": (s, r.y2), "W": (r.x, s), "E": (r.x2, s)}[side]


def _bath(m: Model, r: Room, wh=False):
    door = next((o for o in m.openings if o.room is r and o.kind != "window"), None)
    door_side = None
    if door:
        s = door.wall.seg
        for e in r.edges():
            if e.o == s.o and abs(e.c - s.c) < EPS:
                door_side = e.side
    runs = [run for run in _wall_runs(m, r) if run[0] != door_side] or _wall_runs(m, r)
    runs.sort(key=lambda run: -(run[2] - run[1]))
    side, a, b = runs[0]
    L = b - a
    long_dim, short_dim = max(r.w, r.d), min(r.w, r.d)
    accessible = "ROLL-IN" in r.label.upper() or "ACCESSIBLE" in r.label.upper()
    tub = short_dim >= 5 and long_dim >= 8 and L >= 5 and not m.mobile and not m.container and "SHOWER" not in r.label.upper() and not accessible
    items = []
    if _half_bath(r):
        pass                                 # powder room: toilet and lavatory only
    elif tub:
        items.append(("tub", 5.0, 2.5))
    else:
        sw_ = 3.0 if L >= 6.5 else 2.67
        if accessible:
            sw_ = 5.0                        # curbless 60 x 36 in. roll-in shower
        items.append(("shower", sw_, 3.0 if L >= 6.5 else 2.67))
    items.append(("toilet", 2.5, 2.4))
    lav_w = 3.0 if L >= 9 else 2.0 if L >= 7 else 1.6
    items.append(("lav", lav_w, 1.75))
    if r.has_laundry:
        items.append(("stack_wd", 2.5, 2.5))
    if wh and not r.has_laundry:
        items.append(("wh", 2.0, 2.0))
    total = sum(w for _, w, _ in items)
    if total > L + EPS:
        # Tight wall: drop to a 32 in. shower and an 18 in. lavatory before spilling over.
        items = [(k, 2.67 if k == "shower" and w == 3.0 else 1.6 if k == "lav" else w, 2.67 if k == "shower" and d == 3.0 else d) for k, w, d in items]
        total = sum(w for _, w, _ in items)
    # Shower or tub goes at the end farthest from the door.
    far_end_b = True
    if door:
        dpos = door.s
        far_end_b = abs(b - (dpos if (side in "SN") == (door.wall.seg.o == "h") else (a + b) / 2)) >= abs(a - (dpos if (side in "SN") == (door.wall.seg.o == "h") else (a + b) / 2))
        # door on a perpendicular wall: compare distances from the door wall
        if door_side and door_side not in (side, {"S": "N", "N": "S", "W": "E", "E": "W"}[side]):
            dw = {"W": r.x, "E": r.x2, "S": r.y, "N": r.y2}[door_side]
            far_end_b = abs(b - dw) > abs(a - dw)
    seq = items if not far_end_b else list(reversed(items))
    if tub and r.d <= 5.5 and side in "SN" and False:
        pass
    pos = a if total > L else a + (L - total) / 2 if not far_end_b else b - total
    if far_end_b:
        pos = max(a, b - total)
    else:
        pos = a
    for kind, w, d in seq:
        if pos + w > b + 0.6:
            # Out of wall: put the remainder on the opposite side of the room.
            opp = {"S": "N", "N": "S", "W": "E", "E": "W"}[side]
            oe = {e.side: e for e in r.edges()}[opp]
            _add(m, kind, _rect_on_side(r, opp, oe.a + 0.2, w, d), r, opp)
            continue
        _add(m, kind, _rect_on_side(r, side, pos, w, d), r, side)
        pos += w


def _half_bath(r: Room) -> bool:
    L = r.label.upper()
    return r.kind == "bath" and ("POWDER" in L or "HALF" in L)


def _laundry(m: Model, r: Room, wh=False):
    runs = _wall_runs(m, r)
    runs.sort(key=lambda run: -(run[2] - run[1]))
    if not runs:
        return
    side, a, b = runs[0]
    L = b - a
    if L >= 5.2:
        _add(m, "washer", _rect_on_side(r, side, a + 0.1, 2.5, 2.5), r, side)
        _add(m, "dryer", _rect_on_side(r, side, a + 2.6, 2.5, 2.5), r, side)
        used = 5.2
    else:
        _add(m, "stack_wd", _rect_on_side(r, side, a + 0.1, 2.5, 2.5), r, side)
        used = 2.7
    if wh:
        if L - used >= 2.1:
            _add(m, "wh", _rect_on_side(r, side, a + used + 0.1, 2.0, 2.0), r, side)
        elif len(runs) > 1:
            s2, a2, b2 = runs[1]
            _add(m, "wh", _rect_on_side(r, s2, b2 - 2.1, 2.0, 2.0), r, s2)
        else:
            _add(m, "tankless", _rect_on_side(r, side, a + used + 0.1, 1.2, 0.6), r, side)


def _bed(m: Model, r: Room):
    # queen 5 x 6.67, full 4.5 x 6.25, twin 3.25 x 6.25
    for bw, bl in ((5.0, 6.67), (4.5, 6.25), (3.25, 6.25)):
        if r.loft:
            if r.w >= bl and r.d >= bw:
                m.fixtures.append(Fixture("bed", r.cx - bl / 2, r.cy - bw / 2, bl, bw, r, "W"))
                return
            if r.d >= bl and r.w >= bw:
                m.fixtures.append(Fixture("bed", r.cx - bw / 2, r.cy - bl / 2, bw, bl, r, "S"))
                return
            continue
        # Headboard against the longest wall without a door, centered, with walk space.
        runs = _wall_runs(m, r)
        runs.sort(key=lambda run: -(run[2] - run[1]))
        for side, a, b in runs:
            depth_avail = r.d if side in "SN" else r.w
            if b - a >= bw + 1 and depth_avail >= bl + 2:
                s = (a + b) / 2 - bw / 2
                x, y, w, d = _rect_on_side(r, side, s, bw, bl)
                m.fixtures.append(Fixture("bed", x, y, w, d, r, side))
                return
        if r.kind == "studio":
            return


# ---------------------------------------------------------------------------------------
# Electrical
# ---------------------------------------------------------------------------------------

def _inset(x, y, nx, ny, d=0.35):
    return (x + nx * d, y + ny * d)


def _electrical(m: Model):
    dev = m.devices
    heated = m.heated
    counters = [f for f in m.fixtures if f.kind in ("counter",)]

    # Receptacles along walls: no point on a usable wall more than 6 ft from an outlet (12 ft spacing).
    sub = bool(m.level)
    for r in heated:
        if r.kind in ("bath", "stair", "closet"):
            continue
        for side, a, b in _wall_runs(m, r):
            if r.has_kitchen and any(f.room is r and f.rot == side and f.kind == "counter" for f in counters):
                continue
            L = b - a
            if L < 2:
                continue
            n = max(1, math.ceil(L / 12))
            for i in range(n):
                s = a + L * (i + 0.5) / n
                x, y = {"S": (s, r.y), "N": (s, r.y2), "W": (r.x, s), "E": (r.x2, s)}[side]
                nx, ny = {"S": (0, 1), "N": (0, -1), "W": (1, 0), "E": (-1, 0)}[side]
                kind = "gfci" if r.kind in ("laundry", "utility", "mud") else "rec"
                dev.append(Device(kind, *_inset(x, y, nx, ny), r))
    # Kitchen countertop receptacles every 4 ft (GFCI), plus dedicated appliance outlets.
    for f in m.fixtures:
        r = f.room
        nx, ny = {"S": (0, 1), "N": (0, -1), "W": (1, 0), "E": (-1, 0)}.get(f.rot, (0, 0))
        if f.kind == "counter":
            L = f.w if f.rot in "SN" else f.d
            n = max(1, math.ceil(L / 4))
            for i in range(n):
                t = L * (i + 0.5) / n
                x = f.x + t if f.rot in "SN" else (f.x if f.rot == "W" else f.x + f.w)
                y = f.y + t if f.rot in "WE" else (f.y if f.rot == "S" else f.y + f.d)
                if any(g.kind in ("fridge", "range", "sink") and g.x - 0.1 <= x <= g.x + g.w + 0.1 and g.y - 0.1 <= y <= g.y + g.d + 0.1 for g in m.fixtures):
                    continue
                dev.append(Device("gfci", *_inset(x, y, nx, ny, 0.25), r, note="counter"))
        elif f.kind == "fridge":
            x, y = f.back_point()
            dev.append(Device("rec20", *_inset(x, y, nx, ny, 0.25), r, note="fridge"))
        elif f.kind == "range":
            x, y = f.back_point()
            dev.append(Device("rec240", *_inset(x, y, nx, ny, 0.25), r, note="range"))
        elif f.kind in ("washer", "stack_wd"):
            x, y = f.back_point()
            dev.append(Device("rec20", *_inset(x, y, nx, ny, 0.25), r, note="washer"))
            dev.append(Device("rec240", *_inset(x + (0.0 if f.rot in "WE" else 1.0), y + (1.0 if f.rot in "WE" else 0), nx, ny, 0.25), r, note="dryer"))
        elif f.kind == "lav":
            x, y = f.back_point()
            dev.append(Device("gfci", *_inset(x + (0.9 if f.rot in "SN" else 0), y + (0.9 if f.rot in "WE" else 0), nx, ny, 0.25), r, note="bath"))
        elif f.kind in ("wh",):
            x, y = f.back_point()
            dev.append(Device("jbox", *_inset(x, y, nx, ny, 0.25), r, note="water heater"))
        elif f.kind == "tankless":
            x, y = f.back_point()
            dev.append(Device("jbox", *_inset(x, y, nx, ny, 0.25), r, note="tankless heater"))
        elif f.kind == "dw":
            x, y = f.back_point()
            dev.append(Device("jbox", *_inset(x, y, nx, ny, 0.4), r, note="dishwasher"))

    # Lighting.
    for r in heated:
        if r.kind in ("living", "studio", "kitchen", "dining", "entry") and r.area >= 60:
            nx_ = max(1, round(r.w / 6)); ny_ = max(1, round(r.d / 6))
            for i in range(nx_):
                for j in range(ny_):
                    dev.append(Device("can", r.x + r.w * (i + 0.5) / nx_, r.y + r.d * (j + 0.5) / ny_, r))
        elif r.kind == "bath":
            lav = next((f for f in m.fixtures if f.kind == "lav" and f.room is r), None)
            if lav:
                nx, ny = {"S": (0, 1), "N": (0, -1), "W": (1, 0), "E": (-1, 0)}[lav.rot]
                bx, by = lav.back_point()
                dev.append(Device("sconce", bx + nx * 0.15, by + ny * 0.15, r, note="vanity"))
            dev.append(Device("fan", r.cx, r.cy, r, note="exhaust fan / light, 80 CFM"))
        else:
            dev.append(Device("light", r.cx, r.cy, r))
    if PROFILE.get("ceiling_fans"):
        # Hot-climate spec: a ceiling fan with light in the living area and every bedroom.
        for r in heated:
            if r.kind in ("bed", "studio") or (r.kind == "office" and r.area >= 80):
                for d in [d for d in dev if d.room is r and d.kind == "light"]:
                    d.kind, d.note = "cfan", "ceiling fan / light"
            elif r.kind in ("living", "dining") and r.area >= 100:
                cans = [d for d in dev if d.room is r and d.kind == "can"]
                if cans:
                    c = min(cans, key=lambda d: math.dist((d.x, d.y), (r.cx, r.cy)))
                    c.kind, c.note, c.x, c.y = "cfan", "ceiling fan / light", r.cx, r.cy
    for lr in m.lofts:
        dev.append(Device("light", lr.cx, lr.cy, lr, loft=True))
        dev.append(Device("smoke", lr.cx + min(1.5, lr.w / 4), lr.cy, lr, loft=True))
        dev.append(Device("rec", lr.x + 0.35, lr.cy, lr, loft=True))
        dev.append(Device("rec", lr.x2 - 0.35, lr.cy, lr, loft=True))
    # Exterior: light at every exterior door, GFCI weatherproof receptacles front and rear.
    for o in m.openings:
        if o.exterior and o.kind != "window":
            x, y = o.center
            nx, ny = m.inward(o.wall, o.room)
            ox, oy = -nx * 0.4, -ny * 0.4
            ax = (o.width / 2 + 0.6)
            if o.wall.seg.o == "h":
                dev.append(Device("sconce", x + ax + ox, y + oy, None, note="exterior"))
            else:
                dev.append(Device("sconce", x + ox, y + ax + oy, None, note="exterior"))
    for porch_room in [r for r in m.rooms if r.kind == "porch"]:
        dev.append(Device("light", porch_room.cx, porch_room.cy, porch_room, note="porch"))
    if m.porch:
        px, py, pw, pd = m.porch
        dev.append(Device("light", px + pw / 2, py + pd / 2, None, note="porch"))
        if PROFILE.get("ceiling_fans") and pw * pd >= 80:
            dev.append(Device("cfan", px + pw / 2 + (3 if pw >= pd else 0), py + pd / 2 + (0 if pw >= pd else 3), None, note="porch fan, damp-rated"))
    for fac in ("front", "rear"):
        if sub:
            break
        ws = [w for w in m.walls if w.exterior and w.facade == fac and m.exterior_kind(w)]
        if not ws:
            ws = [w for w in m.walls if w.exterior and w.facade == fac]
        if ws:
            w = max(ws, key=lambda w: w.length)
            spans = m.free_spans(w, 0.4)
            if spans:
                a, b = max(spans, key=lambda t: t[1] - t[0])
                x, y = w.seg.at(a + 0.6)
                ny = -0.4 if fac == "front" else 0.4
                dev.append(Device("wp", x, y + ny, None, note="exterior GFCI"))

    # Switches: one at each door into a room, on the latch side; exterior lights at the entry.
    for r in heated + [r for r in m.rooms if r.kind == "porch"]:
        doors = [o for o in m.openings if o.kind != "window" and (o.room is r)]
        if r.kind == "porch":
            continue
        if not doors:
            # Open-plan rooms: switch at the edge of the opening nearest the entry.
            ent = next((o for o in m.openings if o.main), None)
            opens = [w for w in m.walls if w.open and r in w.rooms]
            if opens:
                w = opens[0]
                nx, ny = m.inward(w, r)
                px, py = w.seg.at(w.seg.a + 0.4) if not ent else min((w.seg.p1, w.seg.p2), key=lambda q: math.dist(q, ent.center))
                if w.seg.o == "h":
                    px += 0.4 if abs(px - w.seg.a) < 0.1 else -0.4
                else:
                    py += 0.4 if abs(py - w.seg.a) < 0.1 else -0.4
                dev.append(Device("sw", px + nx * 0.3, py + ny * 0.3, r))
            continue
        for k, o in enumerate(doors):
            nx, ny = m.inward(o.wall, r)
            if o.wall.seg.o == "h":
                px, py = o.b + 0.4, o.wall.seg.c
                if px > min(r.x2, o.wall.seg.b) - 0.2:
                    px = o.a - 0.4
            else:
                px, py = o.wall.seg.c, o.b + 0.4
                if py > min(r.y2, o.wall.seg.b) - 0.2:
                    py = o.a - 0.4
            dev.append(Device("sw3" if len(doors) > 1 else "sw", px + nx * 0.3, py + ny * 0.3, r,
                              note="exterior + interior" if o.exterior else ""))
            if r.kind == "bath":
                dev.append(Device("sw", px + nx * 0.3 + (0.35 if o.wall.seg.o == "h" else 0), py + ny * 0.3 + (0.35 if o.wall.seg.o == "v" else 0), r, note="fan"))

    # Smoke alarms in every sleeping room and outside sleeping areas; CO alarm in the living area.
    beds = [r for r in heated if r.kind in ("bed", "studio")]
    for r in beds:
        dev.append(Device("smoke", r.cx + min(1.2, r.w / 4), r.cy + min(1.2, r.d / 4), r))
    if sub:
        # Second floor: smoke alarm in the hall outside the bedrooms; heads in the bedrooms and study.
        hall = max([r for r in heated if r.kind in ("hall", "stair", "living")] or heated, key=lambda r: (r.kind != "stair", r.area))
        dev.append(Device("smoke", hall.cx, hall.cy + min(0.8, hall.d / 4), hall))
        for r in [r for r in heated if r.kind in ("bed", "studio", "office", "living") and r.area >= 70]:
            _minisplit_head(m, r)
        return None, None
    living = max([r for r in heated if r.kind in ("living", "studio", "kitchen", "dining", "entry")] or heated, key=lambda r: r.area)
    dev.append(Device("smokeco", living.cx - min(1.5, living.w / 4), living.cy + min(1.2, living.d / 4), living, note="smoke / CO"))

    # Panel, mini-split, data.
    panel_room = None
    for kinds in (("utility",), ("laundry",), ("mud",), ("kitchen",), ("living",), ("studio",), ("office",), ("hall",)):
        rs = [r for r in heated if r.kind in kinds]
        if rs:
            panel_room = max(rs, key=lambda r: r.area)
            break
    pw = None
    for w in m.walls_of(panel_room):
        spans = m.free_spans(w, 0.5)
        fx_block = [f for f in m.fixtures if f.room is panel_room and f.kind in ("washer", "dryer", "stack_wd", "wh", "counter", "fridge", "range", "sink")]
        for a, b in spans:
            if b - a < 2:
                continue
            s = (a + b) / 2
            px, py = w.seg.at(s)
            if any(f.x - 0.5 <= px <= f.x + f.w + 0.5 and f.y - 0.5 <= py <= f.y + f.d + 0.5 for f in fx_block):
                continue
            pw = (w, s)
            break
        if pw:
            break
    if pw:
        w, s = pw
        px, py = w.seg.at(s)
        nx, ny = m.inward(w, panel_room)
        dev.append(Device("panel", px + nx * 0.25, py + ny * 0.25, panel_room, note="load center"))
    m.notes["panel_room"] = panel_room
    # Mini-split heads: living area plus each bedroom over 100 sq ft (multi-zone above 600 sq ft).
    zones = [living] + ([r for r in beds if r.area >= 100 and r is not living] if m.p["sqft"] >= 600 else [])
    # Every wing across a breezeway gets its own head, in its largest habitable room.
    for r in sorted(heated, key=lambda q: -q.area):
        if r.kind in ("bed", "office", "living", "studio") and not any(_same_wing(m, z, r) for z in zones):
            zones.append(r)
    for r in zones:
        _minisplit_head(m, r)
    ext_rear = [w for w in m.walls if w.exterior and w.facade in ("rear", "right")]
    if ext_rear:
        w = max(ext_rear, key=lambda w: w.length)
        px, py = w.seg.at(w.seg.a + w.length * 0.7)
        nx, ny = m.inward(w, w.rooms[0])
        dev.append(Device("condenser", px - nx * 1.3, py - ny * 1.3, None, note="heat pump condenser"))
        dev.append(Device("disconnect", px - nx * 0.4 + (0.9 if w.seg.o == "h" else 0), py - ny * 0.4 + (0.9 if w.seg.o == "v" else 0), None, note="A/C disconnect"))
    if m.mobile:
        ws = [w for w in m.walls if w.exterior and w.facade == "rear"]
        if ws:
            px, py = ws[0].seg.at(ws[0].seg.a + 0.8)
            dev.append(Device("inlet", px, py + 0.4, None, note="50A RV inlet"))
    return living, panel_room


def _same_wing(m: Model, a: Room, b: Room) -> bool:
    """Rooms joined by interior walls (not split by a breezeway)."""
    seen, todo = {id(a)}, [a]
    while todo:
        r = todo.pop()
        if r is b:
            return True
        for w in m.walls:
            if not w.exterior and r in w.rooms:
                o = w.rooms[0] if w.rooms[1] is r else w.rooms[1]
                if id(o) not in seen:
                    seen.add(id(o))
                    todo.append(o)
    return False


def _minisplit_head(m: Model, r: Room):
    ws = [w for w in m.walls_of(r, exterior=True)]
    if not ws:
        return
    w = max(ws, key=lambda w: w.length)
    spans = m.free_spans(w, 0.3, kinds=("door", "slider", "pocket"))
    if not spans:
        return
    a, b = max(spans, key=lambda t: t[1] - t[0])
    px, py = w.seg.at((a + b) / 2)
    nx, ny = m.inward(w, r)
    m.devices.append(Device("minisplit", px + nx * 0.4, py + ny * 0.4, r, note="ductless head"))


HEAD_SIZES = (6000, 9000, 12000, 15000, 18000, 24000)
OUTDOOR_SIZES = (9000, 12000, 18000, 24000, 30000, 36000, 42000, 48000)


def _size_hvac(m: Model, heads):
    """Right-size each ductless head from the floor area it serves (profile BTU per sq ft),
    and the outdoor unit from the sum. Rooms without a head count toward the largest head in
    the same wing on the same floor."""
    f = PROFILE.get("cooling_btu_per_sqft", 20)
    served = {id(d): d.room.area for d in heads}
    for s in m.storeys:
        hs = [d for d in heads if d.level == s.level]
        own = {id(d.room) for d in hs}
        for r in s.heated:
            if id(r) in own:
                continue
            cands = [d for d in hs if _same_wing(s, d.room, r)]
            if cands:
                d = max(cands, key=lambda d: d.room.area)
                served[id(d)] += r.area
    rows = []
    for d in heads:
        need = served[id(d)] * f
        size = next((h for h in HEAD_SIZES if h >= need * 0.95), HEAD_SIZES[-1])
        rows.append((d.room.title, round(served[id(d)]), size))
        d.note = f"ductless head, {size // 1000}k BTU"
    total = sum(r[2] for r in rows)
    need = sum(r[1] for r in rows) * f
    cap = next((o for o in OUTDOOR_SIZES if o >= need * 0.95), OUTDOOR_SIZES[-1]) if rows else 0
    if len(rows) == 1:
        cap = rows[0][2]                     # single-zone system: matched head and condenser
    elif rows:
        cap = max(cap, 18000)                # smallest common multi-zone outdoor unit
    m.notes["hvac"] = {"heads": rows, "outdoor_btu": cap, "connected_btu": total, "btu_per_sqft": f}
    return m.notes["hvac"]


def _circuits(m: Model, living, panel_room):
    """Assign devices to circuits and build the panel schedule and service load calculation."""
    sq = m.p["sqft"]
    circuits = []

    def add(name, amps, volts, va, wire=None):
        c = Circuit(len(circuits) + 1, name, amps, volts, va, f"{amps}A {'2P' if volts == 240 else '1P'}",
                    wire or {15: "14/2 NM-B", 20: "12/2 NM-B", 30: "10/2 NM-B", 40: "8/2 NM-B", 50: "6/3 NM-B"}[amps] + (" (w/ gnd, 240V)" if volts == 240 and amps < 50 else ""))
        circuits.append(c)
        return c.no

    fx = {f.kind for f in m.all("fixtures")}
    has_k = any(r.has_kitchen for r in m.heated)
    sabc = []
    if has_k:
        sabc.append(add("Kitchen small appliance 1 (GFCI)", 20, 120, 1500))
        if sq > 300:
            sabc.append(add("Kitchen small appliance 2 (GFCI)", 20, 120, 1500))
    fridge_c = add("Refrigerator", 20, 120, 700) if "fridge" in fx else 0
    range_c = 0
    if "range" in fx:
        small = sq < 350
        range_c = add("Range" if not small else "Cooktop / range (2-burner induction)", 40 if not small else 30, 240, 8000 if not small else 3600)
    dw_c = add("Dishwasher", 20, 120, 1200) if "dw" in fx else 0
    bath_c = add("Bathroom receptacles (GFCI)", 20, 120, 1500) if any(r.kind == "bath" for r in m.all("heated")) else 0
    laundry_c = add("Laundry receptacle", 20, 120, 1500) if fx & {"washer", "stack_wd"} else 0
    dryer_c = add("Dryer", 30, 240, 5000) if fx & {"dryer", "stack_wd"} else 0
    wh_c = 0
    if "wh" in fx:
        wh_c = add("Water heater (40 gal or heat-pump)", 30, 240, 4500)
    elif "tankless" in fx:
        wh_c = add("Tankless water heater (point-of-use)", 40, 240, 7200, "8/2 NM-B (w/ gnd, 240V)")
    hp = [d for d in m.devices if d.kind == "minisplit"]
    hvac = _size_hvac(m, hp)
    cap = hvac["outdoor_btu"]
    hp_c = (add(f"Heat pump (mini-split, {cap:,} BTU outdoor unit)", 20 if cap <= 12000 else 30 if cap <= 30000 else 40, 240,
                2400 if cap <= 12000 else 4800 if cap <= 30000 else 6800) if hp else 0)
    # General lighting and receptacles: 3 VA per sq ft, 1,800 VA per 15A circuit (NEC 220.12).
    gen_va = sq * 3
    n_gen = max(2, math.ceil(gen_va / 1800) + 1)
    gen = [add(f"Lighting & receptacles {i + 1}", 15, 120, int(gen_va / n_gen)) for i in range(n_gen)]
    ext_c = add("Exterior receptacles & lighting (GFCI)", 20, 120, 360)
    smoke_c = gen[0]

    # Assign devices.
    rooms_sorted = sorted(m.all("heated") + m.lofts, key=lambda r: (r.x, r.y))
    room_c = {id(r): gen[i % len(gen)] for i, r in enumerate(rooms_sorted)}
    for d in m.devices:
        if d.note == "counter":
            d.circuit = sabc[0] if not sabc[1:] else sabc[int(d.x * 7) % 2]
        elif d.note == "fridge":
            d.circuit = fridge_c
        elif d.note == "range":
            d.circuit = range_c
        elif d.note == "dishwasher":
            d.circuit = dw_c
        elif d.note == "bath" or (d.kind == "gfci" and d.room and d.room.kind == "bath"):
            d.circuit = bath_c
        elif d.note == "washer":
            d.circuit = laundry_c
        elif d.note == "dryer":
            d.circuit = dryer_c
        elif d.note in ("water heater", "tankless heater"):
            d.circuit = wh_c
        elif d.kind in ("minisplit", "condenser", "disconnect"):
            d.circuit = hp_c
        elif d.kind in ("smoke", "smokeco"):
            d.circuit = smoke_c
        elif d.room is None or (d.room and d.room.kind == "porch") or d.kind == "wp":
            d.circuit = ext_c
        elif d.kind in ("panel", "inlet"):
            d.circuit = 0
        else:
            d.circuit = room_c.get(id(d.room), gen[0])

    # Standard method service load (NEC 220.82 optional method, dwelling).
    other = gen_va + 1500 * len(sabc) + 1500 * bool(laundry_c) + sum(c.va for c in circuits if c.no in (fridge_c, range_c, dw_c, dryer_c, wh_c, bath_c))
    hp_va = sum(c.va for c in circuits if c.no == hp_c)
    demand = min(other, 10000) + max(0, other - 10000) * 0.4 + hp_va
    amps = demand / 240
    if m.mobile:
        service = "50A, 120/240V via RV inlet to a 100A main-lug panel"
    elif m.foundation == "chassis":
        service = "50A, 120/240V feeder from the RV-park pedestal (NEC 552) to a 100A panel"
    else:
        service = "100A, 120/240V single phase" if amps <= 80 else "125A" if amps <= 100 else "200A, 120/240V single phase"
    m.circuits = circuits
    m.notes["load"] = {"general_va": gen_va, "other_va": int(other), "hp_va": hp_va, "demand_va": int(demand),
                       "amps": round(amps, 1), "service": service}


# ---------------------------------------------------------------------------------------
# Plumbing
# ---------------------------------------------------------------------------------------

DFU = {"toilet": 3, "shower": 2, "tub": 2, "lav": 1, "sink": 2, "dw": 2, "washer": 2, "stack_wd": 2}
TRAP = {"toilet": '3"', "shower": '2"', "tub": '1-1/2"', "lav": '1-1/4"', "sink": '1-1/2"', "dw": "(via sink)", "washer": '2"', "stack_wd": '2"'}
HOT = {"shower", "tub", "lav", "sink", "dw", "washer", "stack_wd"}
COLD = {"shower", "tub", "lav", "sink", "dw", "washer", "stack_wd", "toilet", "fridge"}


def _route(a, b, first="x"):
    (x1, y1), (x2, y2) = a, b
    if abs(x1 - x2) < EPS or abs(y1 - y2) < EPS:
        return [a, b]
    return [a, (x2, y1), b] if first == "x" else [a, (x1, y2), b]


def _plumbing(m: Model, below: Model | None = None):
    """Supply and DWV for one floor. A second floor (below = the main-floor model) is fed by
    a riser at the water heater and drains through a stack to the main building drain."""
    fixtures = [f for f in m.fixtures if f.kind in COLD | {"wh", "tankless"}]
    wh = next((f for f in (below or m).fixtures if f.kind in ("wh", "tankless")), None)
    users = [f for f in fixtures if f.kind in COLD]
    if not users:
        return
    # Water service enters on the rear (or nearest) wall near the water heater.
    if wh:
        whp = (wh.cx, wh.cy)
    else:
        whp = (users[0].cx, users[0].cy)
    if below:
        m.notes["riser"] = whp
    else:
        entry = min([(whp[0], 0.0), (whp[0], m.D), (0.0, whp[1]), (m.W, whp[1])], key=lambda q: math.dist(q, whp))
        m.notes["water_entry"] = entry
        # Supply: trunk from the service to the water heater, then a branch to each fixture.
        m.pipes.append(Pipe("cold", _route(entry, whp, "y" if entry[1] in (0.0, m.D) else "x"), '3/4"'))
    off = 0.22
    for f in users:
        bx, by = f.back_point()
        if f.kind == "fridge":
            m.pipes.append(Pipe("cold", _route(whp, (bx, by)), '1/4" ice maker'))
            continue
        m.pipes.append(Pipe("cold", _route(whp, (bx - off * (f.rot in "SN"), by - off * (f.rot in "WE"))), '1/2"'))
        if f.kind in HOT:
            m.pipes.append(Pipe("hot", _route((whp[0] + off, whp[1] + off), (bx + off * (f.rot in "SN"), by + off * (f.rot in "WE")), "y"), '1/2"'))
    # Drain-waste-vent: fixtures drain to a building drain that leaves the house toward the sewer or septic.
    drains = [f for f in users if f.kind in DFU]
    if not drains:
        return
    toilet = next((f for f in drains if f.kind == "toilet"), None)
    ys = [f.back_point()[1] for f in drains]
    xs = [f.back_point()[0] for f in drains]
    horizontal = (max(xs) - min(xs)) >= (max(ys) - min(ys))
    if horizontal:
        yd = toilet.cy if toilet else sum(ys) / len(ys)
        out_x = 0.0 if (min(xs) + max(xs)) / 2 < m.W / 2 else m.W
        if below:
            out_x = toilet.back_point()[0] if toilet else min(xs)
        x_lo, x_hi = min(min(xs), out_x), max(max(xs), out_x)
        main = [(x_lo, yd), (x_hi, yd)]
        exit_pt = (out_x, yd)
    else:
        xd = toilet.cx if toilet else sum(xs) / len(xs)
        out_y = m.D if (min(ys) + max(ys)) / 2 > m.D / 2 else 0.0
        if below:
            out_y = toilet.back_point()[1] if toilet else min(ys)
        y_lo, y_hi = min(min(ys), out_y), max(max(ys), out_y)
        main = [(xd, y_lo), (xd, y_hi)]
        exit_pt = (xd, out_y)
    total_dfu = sum(DFU[f.kind] for f in drains)
    main_size = '3"' if toilet or total_dfu > 6 else '2"'
    m.pipes.append(Pipe("waste", main, main_size))
    for f in drains:
        if f.kind == "dw":
            continue
        cx, cy = (f.cx, f.cy) if f.kind in ("toilet", "shower", "tub") else f.back_point()
        tgt = (cx, main[0][1]) if horizontal else (main[0][0], cy)
        m.pipes.append(Pipe("waste", [(cx, cy), tgt], TRAP[f.kind]))
    stack = (toilet.cx, toilet.back_point()[1]) if toilet else drains[0].back_point()
    if toilet:
        bx, by = toilet.back_point()
        stack = (bx, by)
    m.notes["stack"] = stack
    m.notes["dfu"] = total_dfu
    m.notes["main_drain"] = main_size
    if not below:
        m.notes["sewer_exit"] = exit_pt
        return
    # Second floor: the stack drops to the main floor and ties into the building drain under the slab.
    m.notes["stack_down"] = exit_pt
    below.notes["stack_from_above"] = exit_pt
    bmain = next((p for p in below.pipes if p.kind == "waste" and p.size == '3"' and len(p.pts) == 2), None) \
        or next((p for p in below.pipes if p.kind == "waste"), None)
    if bmain:
        (x1, y1), (x2, y2) = bmain.pts[0], bmain.pts[-1]
        if abs(y1 - y2) < EPS:
            tie = (min(max(exit_pt[0], min(x1, x2)), max(x1, x2)), y1)
        else:
            tie = (x1, min(max(exit_pt[1], min(y1, y2)), max(y1, y2)))
        below.pipes.append(Pipe("waste", _route(exit_pt, tie), '3"'))
        bmain.size = '3"'
        below.notes["main_drain"] = '3"'
    below.notes["dfu"] = below.notes.get("dfu", 0) + total_dfu
