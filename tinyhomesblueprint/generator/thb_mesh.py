"""3D model of a plan: walls with real openings, roof, floor, porch, lofts and fixtures.

Output groups ('structure', 'roof', 'interior') of triangles per material. The site's
three.js viewer loads the JSON form; buyers get the same mesh as Wavefront OBJ/MTL.
Axes: x = W, y = D (front at y = 0), z = up, feet.
"""
from __future__ import annotations

import math

import thb_model as M

MATERIALS = {
    "siding": "#d9cbb4", "trim": "#f4f1ea", "roof": "#3d4a52", "glass": "#8fc9d9", "door": "#8a5a3b",
    "foundation": "#9a9a94", "floor": "#c8a97e", "porch": "#a07a52", "steel": "#5f7f86", "interior": "#efe9df",
    "fixture": "#ffffff", "counter": "#7a8f8a", "bed": "#b9c7d6", "tile": "#dfe7ea", "trailer": "#2c2c2c", "loft": "#b98f61",
}
ROOM_FLOOR = {"bath": "tile", "laundry": "tile", "utility": "tile", "mud": "tile"}


class Mesh:
    def __init__(self):
        self.g = {}

    def tri(self, group, mat, a, b, c):
        self.g.setdefault(group, {}).setdefault(mat, []).append((a, b, c))

    def quad(self, group, mat, a, b, c, d):
        self.tri(group, mat, a, b, c)
        self.tri(group, mat, a, c, d)

    def hexa(self, group, mat, base, top):
        """Prism from a 4-point footprint (counter-clockwise from above) with per-corner bottom/top z.
        base: [(x, y, z0)...], top: [z1...]"""
        b = [(x, y, z) for x, y, z in base]
        t = [(x, y, z1) for (x, y, _), z1 in zip(base, top)]
        self.quad(group, mat, b[3], b[2], b[1], b[0])
        self.quad(group, mat, t[0], t[1], t[2], t[3])
        for i in range(4):
            j = (i + 1) % 4
            self.quad(group, mat, b[i], b[j], t[j], t[i])

    def box(self, group, mat, x, y, z, w, d, h):
        self.hexa(group, mat, [(x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z)], [z + h] * 4)

    def slab(self, group, mat, pts, thick):
        """Roof plane given by 4 corners (CCW from outside/above) extruded downward by thick."""
        lo = [(x, y, z - thick) for x, y, z in pts]
        self.quad(group, mat, *pts)
        self.quad(group, mat, lo[3], lo[2], lo[1], lo[0])
        for i in range(4):
            j = (i + 1) % 4
            self.quad(group, mat, lo[i], lo[j], pts[j], pts[i])

    def cylinder(self, group, mat, cx, cz, y0, y1, r, n=10):
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            p0 = (cx + r * math.cos(a0), cz + r * math.sin(a0))
            p1 = (cx + r * math.cos(a1), cz + r * math.sin(a1))
            self.quad(group, mat, (p0[0], y0, p0[1]), (p1[0], y0, p1[1]), (p1[0], y1, p1[1]), (p0[0], y1, p0[1]))
            self.tri(group, mat, (cx, y0, cz), (p1[0], y0, p1[1]), (p0[0], y0, p0[1]))
            self.tri(group, mat, (cx, y1, cz), (p0[0], y1, p0[1]), (p1[0], y1, p1[1]))


def profile(m: M.Model):
    """Heights for drawing and modelling: base, plates, ridge, and the roof line across D."""
    B = m.base
    rt = m.roof_type
    p = m.pitch / 12
    if rt.startswith("container"):
        P = 9.5
    elif rt == "aframe":
        P = 0.0
    else:
        P = m.plate
    info = {"B": B, "P": P, "pitch": p, "ov": 1.0 if not m.mobile else 0.5}
    if rt in ("gable", "gable-steep", "thow", "gooseneck"):
        R = m.D / 2 * p
        info.update(kind="gable", ridge=B + P + R, front=B + P, rear=B + P)
        info["line"] = [(0, B + P), (m.D / 2, B + P + R), (m.D, B + P)]
    elif rt in ("shed", "shed-thow"):
        R = m.D * p
        info.update(kind="shed", front=B + P, rear=B + P - R, ridge=B + P)
        info["line"] = [(0, B + P), (m.D, B + P - R)]
    elif rt == "container":
        info.update(kind="flat", front=B + P, rear=B + P, ridge=B + P)
        info["line"] = [(0, B + P), (m.D, B + P)]
    elif rt == "container-double":
        R = m.D * max(p, 1 / 12)
        info.update(kind="shedover", front=B + P, rear=B + P, ridge=B + P + 0.4 + R, roof_front=B + P + 0.4 + R, roof_rear=B + P + 0.4)
        info["line"] = [(0, B + P), (m.D, B + P)]
    elif rt == "aframe":
        H = M.aframe_height(m)
        info.update(kind="aframe", front=B, rear=B, ridge=B + H, H=H)
        info["line"] = [(0, B), (m.D / 2, B + H), (m.D, B)]
    elif rt == "gambrel":
        R = m.D * 0.62
        Pg = 6.5
        info.update(kind="gambrel", P=Pg, front=B + Pg, rear=B + Pg, ridge=B + Pg + R)
        info["line"] = [(0, B + Pg), (m.D * 0.16, B + Pg + R * 0.55), (m.D / 2, B + Pg + R), (m.D * 0.84, B + Pg + R * 0.55), (m.D, B + Pg)]
    return info


def roof_z(info, y):
    """Height of the wall top / roof underside at depth y (wall tops on the gable ends)."""
    pts = info["line"]
    for (y0, z0), (y1, z1) in zip(pts, pts[1:]):
        if y0 - 1e-9 <= y <= y1 + 1e-9:
            return z0 + (z1 - z0) * ((y - y0) / (y1 - y0) if y1 > y0 else 0)
    return pts[-1][1]


def wall_top(m, info, wall, s):
    """Top of an exterior wall at axis coordinate s. Long walls (h) stop at the plate; gable walls follow the roof."""
    if wall.seg.o == "h":
        y = wall.seg.c
        if info["kind"] in ("shed",):
            return roof_z(info, y)
        if info["kind"] == "aframe":
            return info["B"]
        return info["front"] if info["kind"] != "gambrel" else info["B"] + info["P"]
    return roof_z(info, s)


def build_mesh(m: M.Model) -> Mesh:
    me = Mesh()
    info = profile(m)
    B = info["B"]
    W, D = m.W, m.D
    gn = m.roof_type == "gooseneck"
    raise_at = W - 8 if gn else None

    def zbase(x):
        return B + (3.2 if gn and x >= raise_at - 1e-6 else 0)

    # Foundation / trailer / platform
    if m.mobile:
        me.box("structure", "trailer", -0.2, 0.15, B - 0.55, W + 0.4, D - 0.3, 0.5)
        axle = W * 0.58 if not gn else (W - 8) * 0.55
        for ax in (axle - 1.6, axle + 1.6):
            for yy in (-0.2, D - 0.6):
                me.cylinder("structure", "trailer", ax, 1.15, yy, yy + 0.8, 1.15)
        if gn:
            me.box("structure", "trailer", raise_at, 0.3, B, 8, D - 0.6, 3.2)
        else:
            me.hexa("structure", "trailer", [(-4, D / 2 - 0.2, 1.2), (0, D / 2 - 2.5, 1.2), (0, D / 2 + 2.5, 1.2), (-4, D / 2 + 0.2, 1.2)], [1.6] * 4)
    elif m.container:
        for px in ([0, W - 2] if W <= 21 else [0, W / 2 - 1, W - 2]):
            for py in (0, D - 2):
                me.box("structure", "foundation", px, py, 0, 2, 2, B)
    else:
        for r in m.heated:
            me.box("structure", "foundation", r.x, r.y, 0, r.w, r.d, B - 0.05)

    # Floors by room (cutaway view)
    for r in m.heated:
        mat = ROOM_FLOOR.get(r.kind, "floor")
        me.box("interior", mat, r.x, r.y, zbase(r.x) - 0.05, r.w, r.d, 0.06)

    # Exterior walls with openings
    T = m.ext_t
    wall_mat = "steel" if m.container else "siding"
    for w in m.walls:
        if not w.exterior:
            continue
        r = w.rooms[0]
        nx, ny = m.inward(w, r)
        ops = sorted(m.openings_on(w), key=lambda o: o.s)
        s0, s1 = w.seg.a, w.seg.b
        cuts = [s0, s1]
        for o in ops:
            cuts += [o.a, o.b]
        if w.seg.o == "v":
            for y0, _ in info["line"][1:-1]:
                if s0 < y0 < s1:
                    cuts.append(y0)
        if gn and w.seg.o == "h" and s0 < raise_at < s1:
            cuts.append(raise_at)
        cuts = sorted(set(round(c, 4) for c in cuts))

        def corner(s, z, inner):
            x, y = w.seg.at(s)
            off = T if inner else 0
            return (x + nx * off, y + ny * off, z)

        def piece(sa, sb, za, zb_a, zb_b, mat=wall_mat):
            if sb - sa < 1e-4:
                return
            zat = za if not callable(za) else None
            base = [corner(sa, za, False), corner(sb, za, False), corner(sb, za, True), corner(sa, za, True)]
            top = [zb_a, zb_b, zb_b, zb_a]
            # keep CCW from above
            ax, ay = base[1][0] - base[0][0], base[1][1] - base[0][1]
            bx, by = base[2][0] - base[0][0], base[2][1] - base[0][1]
            if ax * by - ay * bx < 0:
                base = [base[0], base[3], base[2], base[1]]
                top = [top[0], top[3], top[2], top[1]]
            me.hexa("structure", mat, base, top)

        for sa, sb in zip(cuts, cuts[1:]):
            mid = (sa + sb) / 2
            x_mid = w.seg.at(mid)[0]
            zb = zbase(x_mid)
            ta, tb = wall_top(m, info, w, sa), wall_top(m, info, w, sb)
            if info["kind"] == "aframe" and w.seg.o == "h":
                continue
            o = next((o for o in ops if o.a - 1e-4 <= mid <= o.b + 1e-4), None)
            if not o:
                piece(sa, sb, zb, ta, tb)
                continue
            z_lo = zb + o.sill
            z_hi = zb + o.sill + o.height
            if o.sill > 0:
                piece(sa, sb, zb, z_lo, z_lo)
            if min(ta, tb) > z_hi + 0.01:
                # lintel: bottom at z_hi, top follows the wall top
                base = [corner(sa, z_hi, False), corner(sb, z_hi, False), corner(sb, z_hi, True), corner(sa, z_hi, True)]
                piece(sa, sb, z_hi, ta, tb)
            # glass or door panel in the middle of the wall
            g0 = corner(sa, z_lo, False)
            g1 = corner(sb, z_lo, False)
            off = T / 2
            gp = [(g0[0] + nx * off, g0[1] + ny * off), (g1[0] + nx * off, g1[1] + ny * off)]
            mat = "glass" if o.kind in ("window", "slider") else "door"
            me.quad("structure", mat, (gp[0][0], gp[0][1], z_lo), (gp[1][0], gp[1][1], z_lo), (gp[1][0], gp[1][1], z_hi), (gp[0][0], gp[0][1], z_hi))
            me.quad("structure", mat, (gp[0][0], gp[0][1], z_hi), (gp[1][0], gp[1][1], z_hi), (gp[1][0], gp[1][1], z_lo), (gp[0][0], gp[0][1], z_lo))
            # trim frame around the opening on the outside face
            t = 0.25
            for (a, b, z0, z1) in ((sa - t, sa, z_lo - (t if o.sill else 0), z_hi + t), (sb, sb + t, z_lo - (t if o.sill else 0), z_hi + t),
                                   (sa - t, sb + t, z_hi, z_hi + t)) + (((sa - t, sb + t, z_lo - t, z_lo),) if o.sill else ()):
                p0, p1 = w.seg.at(a), w.seg.at(b)
                bx_ = [(p0[0] - nx * 0.06, p0[1] - ny * 0.06, z0), (p1[0] - nx * 0.06, p1[1] - ny * 0.06, z0),
                       (p1[0] + nx * 0.02, p1[1] + ny * 0.02, z0), (p0[0] + nx * 0.02, p0[1] + ny * 0.02, z0)]
                ax, ay = bx_[1][0] - bx_[0][0], bx_[1][1] - bx_[0][1]
                cx, cy = bx_[2][0] - bx_[0][0], bx_[2][1] - bx_[0][1]
                if ax * cy - ay * cx < 0:
                    bx_ = [bx_[0], bx_[3], bx_[2], bx_[1]]
                me.hexa("structure", "trim", bx_, [z1] * 4)

    # Container double: shed roof over boxes; plain container: roof deck
    ov = info["ov"]
    k = info["kind"]
    if k == "gable":
        R = info["ridge"]
        e = info["front"]
        drop = ov * info["pitch"]
        me.slab("roof", "roof", [(-ov, -ov, e - drop), (W + ov, -ov, e - drop), (W + ov, D / 2, R), (-ov, D / 2, R)], 0.5)
        me.slab("roof", "roof", [(W + ov, D + ov, e - drop), (-ov, D + ov, e - drop), (-ov, D / 2, R), (W + ov, D / 2, R)], 0.5)
    elif k == "shed":
        p = info["pitch"]
        me.slab("roof", "roof", [(-ov, -ov, info["front"] + ov * p), (W + ov, -ov, info["front"] + ov * p),
                                 (W + ov, D + ov, info["rear"] - ov * p), (-ov, D + ov, info["rear"] - ov * p)], 0.5)
    elif k == "flat":
        me.box("roof", "steel", 0, 0, info["front"], W, D, 0.15)
    elif k == "shedover":
        me.box("roof", "steel", 0, 0, info["front"], W, D, 0.15)
        me.slab("roof", "roof", [(-ov, -ov, info["roof_front"]), (W + ov, -ov, info["roof_front"]),
                                 (W + ov, D + ov, info["roof_rear"]), (-ov, D + ov, info["roof_rear"])], 0.35)
        for xx in (0.2, W / 2, W - 0.5):
            for yy, zz in ((0.0, info["roof_front"]), (D - 0.3, info["roof_rear"])):
                me.box("roof", "steel", xx, yy, info["front"], 0.3, 0.3, zz - info["front"] - 0.35)
    elif k == "aframe":
        H = info["ridge"]
        ext = 0.8
        me.slab("roof", "roof", [(-ov, -ext * 0.5, B - ext), (W + ov, -ext * 0.5, B - ext), (W + ov, D / 2, H + 0.4), (-ov, D / 2, H + 0.4)], 0.7)
        me.slab("roof", "roof", [(W + ov, D + ext * 0.5, B - ext), (-ov, D + ext * 0.5, B - ext), (-ov, D / 2, H + 0.4), (W + ov, D / 2, H + 0.4)], 0.7)
    elif k == "gambrel":
        L = info["line"]
        pts = [(L[0][0] - 0.6, L[0][1] - 0.4)] + L[1:-1] + [(L[-1][0] + 0.6, L[-1][1] - 0.4)]
        for (y0, z0), (y1, z1) in zip(pts, pts[1:]):
            if y1 <= D / 2 + 1e-6:
                me.slab("roof", "roof", [(-ov, y0, z0 + 0.4), (W + ov, y0, z0 + 0.4), (W + ov, y1, z1 + 0.4), (-ov, y1, z1 + 0.4)], 0.45)
            else:
                me.slab("roof", "roof", [(W + ov, y0, z0 + 0.4), (-ov, y0, z0 + 0.4), (-ov, y1, z1 + 0.4), (W + ov, y1, z1 + 0.4)], 0.45)
        # long-side walls under the lower slope
    # Porch outside the footprint: deck, posts and a shed roof
    if m.porch:
        px, py, pw, pd = m.porch
        me.box("structure", "porch", px, py, B - 0.45, pw, pd, 0.4)
        if k == "aframe":
            pass
        else:
            ph = B + 8.2
            for qx, qy in ((px + 0.2, py + 0.2 if py < 0 else py + pd - 0.6), (px + pw - 0.6, py + 0.2 if py < 0 else py + pd - 0.6)):
                if py >= 0 and px >= W:
                    qx, qy = (px + pw - 0.6, py + 0.2) if qx < px + pw / 2 else (px + pw - 0.6, py + pd - 0.6)
                me.box("structure", "trim", qx, qy, B, 0.4, 0.4, ph - B)
            if py < 0:
                me.slab("roof", "roof", [(px - 0.6, py - 0.6, ph), (px + pw + 0.6, py - 0.6, ph), (px + pw + 0.6, 0, ph + 1.1), (px - 0.6, 0, ph + 1.1)], 0.35)
            elif px >= W - 1e-6:
                me.slab("roof", "roof", [(px + pw + 0.6, py - 0.6, ph), (px + pw + 0.6, py + pd + 0.6, ph), (W, py + pd + 0.6, ph + 1.1), (W, py - 0.6, ph + 1.1)], 0.35)
    for r in m.rooms:
        if r.kind == "porch":
            me.box("structure", "foundation", r.x, r.y, 0, r.w, r.d, B - 0.6)
            me.box("structure", "porch", r.x, r.y, B - 0.6, r.w, r.d, 0.25)
            for qx, qy in ((r.x, r.y), (r.x2 - 0.45, r.y) if r.y == 0 else (r.x, r.y2 - 0.45)):
                me.box("structure", "trim", qx + 0.02, qy + 0.02, B, 0.42, 0.42, info["front"] - B)

    # Interior walls (cutaway)
    ti = m.int_t
    for w in m.walls:
        if w.exterior or w.open:
            continue
        ops = sorted(m.openings_on(w), key=lambda o: o.s)
        cuts = sorted({w.seg.a, w.seg.b, *[o.a for o in ops], *[o.b for o in ops]})
        if w.seg.o == "v":
            cuts = sorted(set(cuts) | {y for y, _ in info["line"][1:-1] if w.seg.a < y < w.seg.b})

        def top(x, y):
            # 8 ft partition, never above the roof underside
            return min(zbase(x) + 8.0, roof_z(info, y) - 0.3 if k not in ("flat", "shedover") else info["front"])
        for sa, sb in zip(cuts, cuts[1:]):
            mid = (sa + sb) / 2
            x0, y0 = w.seg.at(sa)
            x1, y1 = w.seg.at(sb)
            zb = zbase((x0 + x1) / 2)
            o = next((o for o in ops if o.a - 1e-4 <= mid <= o.b + 1e-4), None)
            z0 = zb if not o else zb + 6.83
            t0, t1 = top(x0, y0), top(x1, y1)
            if min(t0, t1) - z0 <= 0.05:
                continue
            if w.seg.o == "h":
                me.hexa("interior", "interior", [(x0, y0 - ti / 2, z0), (x1, y0 - ti / 2, z0), (x1, y0 + ti / 2, z0), (x0, y0 + ti / 2, z0)], [t0, t1, t1, t0])
            else:
                me.hexa("interior", "interior", [(x0 - ti / 2, y0, z0), (x0 + ti / 2, y0, z0), (x0 + ti / 2, y1, z0), (x0 - ti / 2, y1, z0)], [t0, t0, t1, t1])

    # Lofts
    for lr in m.lofts:
        z = B + 7.0
        y0, y1 = lr.y + 0.05, lr.y2 - 0.05
        if k in ("aframe", "gambrel", "gable"):
            # keep the loft deck under the roof
            while y0 < y1 and roof_z(info, y0) < z + 0.9:
                y0 += 0.1
            while y1 > y0 and roof_z(info, y1) < z + 0.9:
                y1 -= 0.1
        me.box("interior", "loft", lr.x + 0.05, y0, z, lr.w - 0.1, y1 - y0, 0.6)

    # Fixtures (cutaway)
    H = {"counter": (3.0, "counter"), "island": (3.0, "counter"), "sink": (3.05, "fixture"), "range": (3.05, "trim"), "fridge": (6.0, "fixture"),
         "dw": (2.9, "trim"), "lav": (2.8, "fixture"), "toilet": (1.4, "fixture"), "tub": (1.7, "fixture"), "shower": (0.3, "fixture"),
         "washer": (3.0, "fixture"), "dryer": (3.0, "fixture"), "stack_wd": (6.0, "fixture"), "wh": (4.6, "fixture"), "tankless": (2.0, "fixture"),
         "bed": (1.8, "bed")}
    for f in m.fixtures:
        if f.kind not in H:
            continue
        h, mat = H[f.kind]
        z = (B + 7.6) if (f.room and f.room.loft) else zbase(f.cx)
        if f.kind == "tankless":
            z += 4
        # never taller than the roof above it (A-frame knee walls, gooseneck)
        if k in ("aframe", "gambrel", "shed", "gable"):
            h = max(0.1, min(h, roof_z(info, f.y) - z - 0.15, roof_z(info, f.y + f.d) - z - 0.15))
        me.box("interior", mat, f.x + 0.03, f.y + 0.03, z, f.w - 0.06, f.d - 0.06, h if f.kind not in ("sink",) else 0.08)
    return me


def to_json(m: M.Model, me: Mesh):
    info = profile(m)
    groups = {}
    for gname, mats in me.g.items():
        groups[gname] = {mat: [round(v, 2) for t in tris for p in t for v in p] for mat, tris in mats.items()}
    return {"W": m.W, "D": m.D, "H": round(info["ridge"], 2), "materials": {k: v for k, v in MATERIALS.items()}, "groups": groups,
            "rooms": [[r.title, round(r.cx, 2), round(r.cy, 2), round(info["B"], 2)] for r in m.heated]}


def to_obj(m: M.Model, me: Mesh, name: str):
    """Wavefront OBJ (y up, units feet) with an MTL library."""
    lines = [f"# {name} - Tiny Homes Blueprint 3D model (units: feet, Y up)", f"mtllib {name}.mtl"]
    vi = 1
    for gname, mats in me.g.items():
        lines.append(f"g {gname}")
        for mat, tris in mats.items():
            lines.append(f"usemtl {mat}")
            for a, b, c in tris:
                for x, y, z in (a, b, c):
                    lines.append(f"v {x:.3f} {z:.3f} {-y:.3f}")
                lines.append(f"f {vi} {vi + 1} {vi + 2}")
                vi += 3
    mtl = []
    for k, v in MATERIALS.items():
        r, g, b = (int(v[i:i + 2], 16) / 255 for i in (1, 3, 5))
        mtl += [f"newmtl {k}", f"Kd {r:.3f} {g:.3f} {b:.3f}", "Ka 0.1 0.1 0.1", f"d {0.45 if k == 'glass' else 1.0}", "illum 2", ""]
    return "\n".join(lines) + "\n", "\n".join(mtl)
