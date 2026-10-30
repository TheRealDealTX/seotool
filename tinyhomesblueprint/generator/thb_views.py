"""Drawing views. Each view draws one plan, elevation or section of the model onto any
canvas backend (thb_draw). Coordinates are model feet; the caller sets the view origin
and scale. Text sizes are paper inches.
"""
from __future__ import annotations

import math

import thb_model as M
from thb_mesh import profile, roof_z
from thb_qty import header_for

TXT = {"room": 0.115, "dims": 0.08, "tag": 0.072, "note": 0.08, "small": 0.065, "label": 0.09}


def ft_in(v, zero_inches=True):
    v = round(v * 12) / 12
    f = int(math.floor(v + 1e-9))
    i = int(round((v - f) * 12))
    if i == 12:
        f, i = f + 1, 0
    return f"{f}'-{i}\"" if (i or zero_inches) else f"{f}'"


# ---------------------------------------------------------------------------------------
# Plan views
# ---------------------------------------------------------------------------------------

def _inside_heated(m, x, y):
    return any(r.contains(x, y) and r.x + 1e-3 < x < r.x2 - 1e-3 and r.y + 1e-3 < y < r.y2 - 1e-3 for r in m.heated)


def wall_rects(m: M.Model):
    """Solid wall rectangles (x, y, w, h) with door and window openings removed."""
    out = []
    t_e, t_i = m.ext_t, m.int_t
    for w in m.walls:
        if w.open:
            continue
        s = w.seg
        cuts = [(o.a, o.b) for o in m.openings_on(w)]
        a0, b0 = s.a, s.b
        if w.exterior:
            nx, ny = m.inward(w, w.rooms[0])
            # Extend into concave corners so the poche closes.
            for end, sign in ((a0, -1), (b0, 1)):
                px, py = s.at(end + sign * 0.02)
                px += nx * t_e / 2
                py += ny * t_e / 2
                if _inside_heated(m, px, py):
                    if sign < 0:
                        a0 -= t_e
                    else:
                        b0 += t_e
            for a, b in M.subtract(a0, b0, cuts):
                if s.o == "h":
                    y0 = s.c if ny > 0 else s.c - t_e
                    out.append((a, y0, b - a, t_e))
                else:
                    x0 = s.c if nx > 0 else s.c - t_e
                    out.append((x0, a, t_e, b - a))
        else:
            for a, b in M.subtract(a0 - t_i / 2, b0 + t_i / 2, cuts):
                if s.o == "h":
                    out.append((a, s.c - t_i / 2, b - a, t_i))
                else:
                    out.append((s.c - t_i / 2, a, t_i, b - a))
    return out


def opening_geom(m, o):
    """Inner/outer face offsets of the wall at an opening, and the inward normal."""
    w = o.wall
    s = w.seg
    if w.exterior:
        nx, ny = m.inward(w, w.rooms[0])
        f0, f1 = 0.0, m.ext_t
    else:
        r = o.room or w.rooms[0]
        nx, ny = m.inward(w, r)
        f0, f1 = -m.int_t / 2, m.int_t / 2
    return s, nx, ny, f0, f1


def draw_openings(cv, m, light=False):
    st_d = "door" if not light else "fixture_lt"
    st_w = "window" if not light else "fixture_lt"
    for o in m.openings:
        s, nx, ny, f0, f1 = opening_geom(m, o)

        def P(sv, off):
            x, y = s.at(sv)
            return x + nx * off, y + ny * off
        if o.kind == "window":
            for off in (f0, f1, (f0 + f1) / 2):
                cv.line(*P(o.a, off), *P(o.b, off), st_w)
            cv.line(*P(o.a, f0), *P(o.a, f1), st_w)
            cv.line(*P(o.b, f0), *P(o.b, f1), st_w)
            continue
        cv.line(*P(o.a, f0), *P(o.a, f1), st_d)
        cv.line(*P(o.b, f0), *P(o.b, f1), st_d)
        if o.kind == "slider":
            mid = (f0 + f1) / 2
            half = o.width / 2
            cv.line(*P(o.a, mid - 0.06), *P(o.s + 0.15, mid - 0.06), st_d)
            cv.line(*P(o.s - 0.15, mid + 0.06), *P(o.b, mid + 0.06), st_d)
            continue
        if o.kind == "pocket":
            ext = o.width / 2 if o.width >= 5 else o.width
            mid = (f0 + f1) / 2
            for side in ((o.a - ext, o.a), (o.b, o.b + ext)) if o.width >= 5 else ((o.b, o.b + ext),):
                cv.poly([P(side[0], mid - 0.08), P(side[1], mid - 0.08), P(side[1], mid + 0.08), P(side[0], mid + 0.08)], "hidden", closed=True)
            continue
        if o.width >= 5:     # double doors
            hinges = [(o.a, o.s), (o.b, o.s)]
        else:
            seg_mid = (s.a + s.b) / 2
            hinge = o.a if (o.a - s.a) < (s.b - o.b) else o.b
            hinges = [(hinge, o.b if hinge == o.a else o.a)]
        face = f1 if (nx, ny) != (0, 0) else f0
        for h, latch in hinges:
            leaf = abs(latch - h)
            hx, hy = P(h, f1)
            ex, ey = hx + nx * leaf, hy + ny * leaf
            cv.line(hx, hy, ex, ey, st_d)
            lx, ly = P(latch, f1)
            a_leaf = math.degrees(math.atan2(ey - hy, ex - hx))
            a_close = math.degrees(math.atan2(ly - hy, lx - hx))
            d = (a_close - a_leaf + 540) % 360 - 180
            cv.arc(hx, hy, leaf, a_leaf, a_leaf + d, "swing" if not light else "fixture_lt")


def draw_fixture(cv, f, light=False):
    st = "fixture" if not light else "fixture_lt"
    x, y, w, d = f.x, f.y, f.w, f.d
    k = f.kind
    cx, cy = f.cx, f.cy
    # unit vector pointing from the back of the fixture to its front
    fx, fy = {"S": (0, 1), "N": (0, -1), "W": (1, 0), "E": (-1, 0)}.get(f.rot, (0, 1))
    if k in ("counter", "island"):
        cv.rect(x, y, w, d, st)
        return
    if k == "bed":
        cv.rect(x, y, w, d, "furn")
        bx, by = f.back_point()
        along = (abs(fy), abs(fx))
        pw = (w if f.rot in "SN" else d)
        for i in (0.27, 0.73):
            px = (x + w * i) if f.rot in "SN" else (bx + fx * 0.45)
            py = (by + fy * 0.45) if f.rot in "SN" else (y + d * i)
            cv.rect(px - (pw * 0.18 if f.rot in "SN" else 0.3), py - (0.3 if f.rot in "SN" else pw * 0.18), pw * 0.36 if f.rot in "SN" else 0.6, 0.6 if f.rot in "SN" else pw * 0.36, "furn")
        lx, ly = bx + fx * (2.2), by + fy * (2.2)
        if f.rot in "SN":
            cv.line(x, ly, x + w, ly, "furn")
        else:
            cv.line(lx, y, lx, y + d, "furn")
        return
    cv.rect(x, y, w, d, st)
    if k == "sink":
        inset = 0.25
        if w >= 2.5 and f.rot in "SN" or d >= 2.5 and f.rot in "WE":
            if f.rot in "SN":
                cv.rect(x + inset, y + inset, w / 2 - inset * 1.5, d - 2 * inset, st)
                cv.rect(x + w / 2 + inset / 2, y + inset, w / 2 - inset * 1.5, d - 2 * inset, st)
            else:
                cv.rect(x + inset, y + inset, w - 2 * inset, d / 2 - inset * 1.5, st)
                cv.rect(x + inset, y + d / 2 + inset / 2, w - 2 * inset, d / 2 - inset * 1.5, st)
        else:
            cv.rect(x + inset, y + inset, w - 2 * inset, d - 2 * inset, st)
        cv.circle(cx, cy, 0.08, st)
    elif k == "range":
        for i in (0.28, 0.72):
            for j in (0.3, 0.7):
                cv.circle(x + w * i, y + d * j, min(w, d) * 0.15, st)
    elif k == "fridge":
        cv.text(cx, cy - 0.04, "REF", TXT["small"], "text_lt" if light else "text")
        bx, by = f.back_point()
        cv.line(x, y, x + w, y + d, st) if False else None
    elif k == "dw":
        cv.text(cx, cy - 0.04, "DW", TXT["small"], "text_lt" if light else "text")
    elif k in ("washer", "dryer", "stack_wd"):
        cv.text(cx, cy - 0.04, {"washer": "W", "dryer": "D", "stack_wd": "W/D"}[k], TXT["small"], "text_lt" if light else "text")
        cv.circle(cx, cy, min(w, d) * 0.36, st)
    elif k in ("wh", "tankless"):
        if k == "wh":
            cv.circle(cx, cy, min(w, d) * 0.42, st)
        cv.text(cx, cy - 0.04, "WH" if k == "wh" else "TWH", TXT["small"], "text_lt" if light else "text")
    elif k == "lav":
        rx, ry = (w * 0.3, d * 0.28) if f.rot in "SN" else (w * 0.28, d * 0.3)
        _ellipse(cv, cx + fx * 0.05, cy + fy * 0.05, rx, ry, st)
    elif k == "toilet":
        # tank against the wall, bowl toward the room
        bx, by = f.back_point()
        if f.rot in "SN":
            cv.rect(cx - w * 0.36, by if f.rot == "S" else by - 0.6, w * 0.72, 0.6, st)
            _ellipse(cv, cx, by + fy * 1.45, w * 0.3, 0.75, st)
        else:
            cv.rect(bx if f.rot == "W" else bx - 0.6, cy - d * 0.36, 0.6, d * 0.72, st)
            _ellipse(cv, bx + fx * 1.45, cy, 0.75, d * 0.3, st)
        # bowl drawn over the (rectangular) clearance box: draw box lightly
    elif k == "shower":
        cv.line(x, y, x + w, y + d, st)
        cv.line(x, y + d, x + w, y, st)
        cv.circle(cx, cy, 0.12, st)
    elif k == "tub":
        cv.rect(x + 0.2, y + 0.2, w - 0.4, d - 0.4, st)
        bx, by = f.back_point()
        drain = (x + 0.5, cy) if f.rot in "SN" else (cx, y + 0.5)
        cv.circle(*drain, 0.1, st)


def _ellipse(cv, cx, cy, rx, ry, st):
    pts = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in (2 * math.pi * i / 28 for i in range(29))]
    cv.poly(pts, st)


def dim_line(cv, p1, p2, off, label, o="h", st="dim", size=None):
    """Dimension between two model points with the line offset perpendicular by off."""
    size = size or TXT["dims"]
    (x1, y1), (x2, y2) = p1, p2
    tk = 0.22
    if o == "h":
        y = y1 + off
        cv.line(x1, y1 + (0.3 if off > 0 else -0.3), x1, y + (0.25 if off > 0 else -0.25), st)
        cv.line(x2, y2 + (0.3 if off > 0 else -0.3), x2, y + (0.25 if off > 0 else -0.25), st)
        cv.line(x1 - 0.2, y, x2 + 0.2, y, st)
        for x in (x1, x2):
            cv.line(x - tk, y - tk, x + tk, y + tk, st)
        cv.text((x1 + x2) / 2, y + 0.12, label, size, st)
    else:
        x = x1 + off
        cv.line(x1 + (0.3 if off > 0 else -0.3), y1, x + (0.25 if off > 0 else -0.25), y1, st)
        cv.line(x2 + (0.3 if off > 0 else -0.3), y2, x + (0.25 if off > 0 else -0.25), y2, st)
        cv.line(x, y1 - 0.2, x, y2 + 0.2, st)
        for y in (y1, y2):
            cv.line(x - tk, y - tk, x + tk, y + tk, st)
        cv.text(x - 0.12, (y1 + y2) / 2, label, size, st, rot=90)


def porch_rect(m):
    pr = next((r for r in m.rooms if r.kind == "porch"), None)
    if pr:
        return (pr.x, pr.y, pr.w, pr.d), True
    if m.porch:
        return tuple(m.porch), False
    return None, False


def draw_plan(cv, m: M.Model, mode="floor", labels=True):
    """mode: floor | electrical | plumbing | foundation | framing | loft"""
    light = mode in ("electrical", "plumbing", "loft", "framing", "foundation")
    pr, inset = porch_rect(m)
    if pr and mode not in ("foundation", "framing"):
        px, py, pw, pd = pr
        cv.rect(px, py, pw, pd, "hidden")
        lbl = "DECK" if m.roof_type == "aframe" else "COVERED PORCH"
        if labels:
            cv.text(px + pw / 2, py + pd / 2 - 0.05, lbl, TXT["label"], "text_lt" if light else "text", bold=True)
            cv.text(px + pw / 2, py + pd / 2 - 0.55, f"{ft_in(pw)} x {ft_in(pd)}", TXT["small"], "text_lt")
        if not inset and m.roof_type != "aframe":
            for qx, qy in ((px, py), (px + pw - 0.45, py), (px, py + pd - 0.45), (px + pw - 0.45, py + pd - 0.45)):
                if (qy < 0 and qy + 0.45 <= 0.01) or (qx >= m.W - 0.01) or (pd <= 0.5):
                    pass
            for qx, qy in _porch_posts(m, pr):
                cv.rect(qx, qy, 0.45, 0.45, "door" if not light else "fixture_lt")
        elif inset:
            for qx, qy in _porch_posts(m, pr):
                cv.rect(qx, qy, 0.45, 0.45, "door" if not light else "fixture_lt")
    if mode in ("foundation", "framing"):
        return
    # Walls
    fill = "wallfill" if not light else "wallfill_lt"
    for x, y, w, h in wall_rects(m):
        cv.rect(x, y, w, h, "wall" if not light else "wall_lt", fill=fill)
    draw_openings(cv, m, light=light)
    # A-frame knee walls (5 ft headroom line)
    off = M.knee_offset(m)
    if off:
        for yy in (off, m.D - off):
            cv.line(0.3, yy, m.W - 0.3, yy, "hidden")
        if labels:
            cv.text(m.W / 2, off - 0.45, "LINE OF 5'-0\" HEADROOM / KNEE WALL", TXT["small"], "text_lt")
    # Fixtures
    for f in m.fixtures:
        if f.room and f.room.loft:
            continue
        draw_fixture(cv, f, light=light)
    # Loft outline (dashed) on the main plan
    if mode == "floor":
        for lr in m.lofts:
            cv.rect(lr.x + 0.15, lr.y + 0.15, lr.w - 0.3, lr.d - 0.3, "hidden")
    # Room labels
    if labels:
        for r in m.heated:
            name = r.label
            fixtures_here = [f for f in m.fixtures if f.room is r and f.kind not in ("bed",)]
            lx, ly = r.cx, r.cy
            # nudge the label away from fixtures
            for f in fixtures_here:
                if f.x - 0.3 <= lx <= f.x + f.w + 0.3 and f.y - 0.6 <= ly <= f.y + f.d + 0.6:
                    ly = f.y + f.d + 0.9 if f.cy < r.cy else f.y - 0.9
            ly = min(max(ly, r.y + 0.9), r.y2 - 0.5)
            size = TXT["room"] if not light else TXT["room"] * 0.8
            words = [name]
            fit = cv.text_width(name, size, True) / max(cv.s, 1e-6) if hasattr(cv, "text_width") else len(name) * 0.3
            if fit > r.w - 0.6 and " " in name:
                words = name.rsplit(" ", 1) if "/" not in name and "+" not in name else [p.strip() for p in name.replace("+", "+|").replace("/", "/|").split("|")]
            yy = ly + (len(words) - 1) * 0.28
            for wd in words:
                cv.text(lx, yy, wd, size, "text" if not light else "text_lt", bold=True)
                yy -= 0.5 * size / 0.115
            if mode == "floor":
                cv.text(lx, yy - 0.0, f"{ft_in(r.w, False)} x {ft_in(r.d, False)}", TXT["small"], "text_lt")
    if mode == "floor" and labels:
        for lr in m.lofts:
            cv.text(lr.cx, lr.y2 - 0.75, f"{lr.label} ABOVE", TXT["small"], "text_lt", bold=True)
        tag_openings(cv, m)


def _porch_posts(m, pr):
    px, py, pw, pd = pr
    posts = []
    if py < 0:                       # front porch outside the footprint
        posts = [(px, py), (px + pw - 0.45, py)]
        if pw > 16:
            posts.append((px + pw / 2 - 0.22, py))
    elif px >= m.W - 0.01:           # side porch
        posts = [(px + pw - 0.45, py), (px + pw - 0.45, py + pd - 0.45)]
    else:                            # inset porch: posts at the open corner
        cx = px + pw - 0.45 if px == 0 else px
        cy = py if py == 0 else py + pd - 0.45
        posts = [(px if px > 0 else px, cy), (cx, cy)] if px == 0 else [(px, cy), (px + pw - 0.45, cy)]
        posts = [(px + 0.02, py + 0.02)] if px == 0 and py == 0 else posts
    return posts


def tag_openings(cv, m):
    for o in m.openings:
        s, nx, ny, f0, f1 = opening_geom(m, o)
        x, y = s.at(o.s)
        if o.kind == "window":
            d = -0.55 if o.exterior else 0.6
            tx, ty = x + nx * d, y + ny * d
            cv.text(tx, ty - 0.12, o.tag, TXT["tag"], "accent", bold=True)
        else:
            d = f1 + 0.6
            tx, ty = x + nx * d, y + ny * d
            cv.circle(tx, ty, 0.32, "accent")
            cv.text(tx, ty - 0.1, o.tag.replace("D", ""), TXT["small"], "accent", bold=True)


def plan_dims(cv, m):
    """Overall and opening-location dimension strings on all four sides."""
    W, D = m.W, m.D
    pr, inset = porch_rect(m)
    y_front = min(0, pr[1]) if pr and not inset else 0
    x_right = max(W, pr[0] + pr[2]) if pr and not inset else W
    for fac in ("front", "rear", "left", "right"):
        if fac in ("front", "rear"):
            line_c = 0.0 if fac == "front" else D
            pts = {0.0, W}
            for o in m.openings:
                if o.exterior and o.wall.seg.o == "h" and abs(o.wall.seg.c - line_c) < 1e-6:
                    pts.add(round(o.s, 3))
            for w in m.walls:
                if w.exterior and w.seg.o == "h" and abs(w.seg.c - line_c) < 1e-6:
                    pts.update({round(w.seg.a, 3), round(w.seg.b, 3)})
            pts = sorted(pts)
            base = (y_front - 2.2) if fac == "front" else D + 2.2
            sign = -1 if fac == "front" else 1
            if len(pts) > 2:
                for a, b in zip(pts, pts[1:]):
                    if b - a > 0.6:
                        dim_line(cv, (a, line_c), (b, line_c), base - line_c, ft_in(b - a), "h")
            dim_line(cv, (0, line_c), (W, line_c), base - line_c + sign * 1.6, ft_in(W), "h")
        else:
            line_c = 0.0 if fac == "left" else W
            pts = {0.0, D}
            for o in m.openings:
                if o.exterior and o.wall.seg.o == "v" and abs(o.wall.seg.c - line_c) < 1e-6:
                    pts.add(round(o.s, 3))
            for w in m.walls:
                if w.exterior and w.seg.o == "v" and abs(w.seg.c - line_c) < 1e-6:
                    pts.update({round(w.seg.a, 3), round(w.seg.b, 3)})
            pts = sorted(pts)
            base = -2.2 if fac == "left" else (x_right + 2.2)
            sign = -1 if fac == "left" else 1
            if len(pts) > 2:
                for a, b in zip(pts, pts[1:]):
                    if b - a > 0.6:
                        dim_line(cv, (line_c, a), (line_c, b), base - line_c, ft_in(b - a), "v")
            dim_line(cv, (line_c, 0), (line_c, D), base - line_c + sign * 1.6, ft_in(D), "v")


# ---------------------------------------------------------------------------------------
# Electrical and plumbing overlays
# ---------------------------------------------------------------------------------------

def draw_device(cv, d, num=True):
    k = d.kind
    x, y = d.x, d.y
    st = "elec"
    r = 0.24
    if k in ("rec", "gfci", "rec20", "rec240", "wp"):
        cv.circle(x, y, r, st)
        cv.line(x - r * 0.55, y - r * 0.35, x - r * 0.55, y + r * 0.35, st)
        cv.line(x + r * 0.55, y - r * 0.35, x + r * 0.55, y + r * 0.35, st)
        tag = {"gfci": "GFI", "rec20": "20A", "rec240": "240", "wp": "WP"}.get(k)
        if k == "rec240":
            cv.line(x, y - r * 0.6, x, y + r * 0.6, st)
        if tag:
            cv.text(x, y + r + 0.12, tag, TXT["small"] * 0.85, "elec_text", bold=True)
    elif k in ("sw", "sw3"):
        cv.text(x, y - 0.1, "S" + ("3" if k == "sw3" else ""), TXT["tag"], "elec_text", bold=True)
    elif k == "light":
        cv.circle(x, y, 0.36, st)
        cv.line(x - 0.25, y - 0.25, x + 0.25, y + 0.25, st)
        cv.line(x - 0.25, y + 0.25, x + 0.25, y - 0.25, st)
    elif k == "can":
        cv.circle(x, y, 0.22, st)
        cv.circle(x, y, 0.1, st)
    elif k == "fan":
        cv.rect(x - 0.35, y - 0.35, 0.7, 0.7, st)
        cv.line(x - 0.35, y - 0.35, x + 0.35, y + 0.35, st)
        cv.line(x - 0.35, y + 0.35, x + 0.35, y - 0.35, st)
    elif k == "sconce":
        cv.circle(x, y, 0.2, st, fill="elec")
    elif k in ("smoke", "smokeco"):
        cv.circle(x, y, 0.3, st)
        cv.text(x, y - 0.07, "SD" if k == "smoke" else "S/C", TXT["small"] * 0.8, "elec_text", bold=True)
    elif k == "panel":
        cv.rect(x - 0.6, y - 0.18, 1.2, 0.36, st, fill="elec")
    elif k == "minisplit":
        cv.rect(x - 1.1, y - 0.25, 2.2, 0.5, st)
        cv.text(x, y - 0.07, "HP", TXT["small"] * 0.85, "elec_text", bold=True)
    elif k == "condenser":
        cv.rect(x - 1.2, y - 0.6, 2.4, 1.2, st)
        cv.text(x, y - 0.07, "CU", TXT["small"], "elec_text", bold=True)
    elif k == "disconnect":
        cv.rect(x - 0.2, y - 0.2, 0.4, 0.4, st, fill="elec")
    elif k == "jbox":
        cv.circle(x, y, 0.2, st)
        cv.text(x, y - 0.06, "J", TXT["small"] * 0.8, "elec_text", bold=True)
    elif k == "inlet":
        cv.rect(x - 0.35, y - 0.25, 0.7, 0.5, st)
        cv.text(x, y - 0.07, "RV", TXT["small"] * 0.8, "elec_text", bold=True)
    if num and d.circuit and k not in ("sw", "sw3"):
        cv.text(x + 0.42, y - 0.42, str(d.circuit), TXT["small"] * 0.8, "elec_text")


def draw_electrical(cv, m: M.Model, loft=False):
    devs = [d for d in m.devices if d.loft == loft]
    for d in devs:
        draw_device(cv, d)
    # Switch legs: dashed arcs from each switch to the lights it controls.
    lights = [d for d in devs if d.kind in ("light", "can", "fan", "sconce", "pendant")]
    for sw in [d for d in devs if d.kind in ("sw", "sw3")]:
        if sw.note == "fan":
            targets = [l for l in lights if l.room is sw.room and l.kind == "fan"]
        else:
            targets = [l for l in lights if l.room is sw.room and l.kind != "fan"]
            if sw.note.startswith("exterior"):
                targets += [l for l in lights if l.room is None and l.note == "exterior" and math.dist((l.x, l.y), (sw.x, sw.y)) < 8]
                targets += [l for l in lights if l.note == "porch"]
        if not targets:
            continue
        chain = [(sw.x, sw.y)]
        rest = targets[:]
        cur = (sw.x, sw.y)
        while rest:
            nxt = min(rest, key=lambda l: math.dist(cur, (l.x, l.y)))
            rest.remove(nxt)
            cv.curve(cur, (nxt.x, nxt.y), 0.18 * math.dist(cur, (nxt.x, nxt.y)) ** 0.5, "elec_lt")
            cur = (nxt.x, nxt.y)


def draw_plumbing(cv, m: M.Model):
    order = {"waste": 0, "vent": 1, "cold": 2, "hot": 3}
    for p in sorted(m.pipes, key=lambda p: order[p.kind]):
        cv.poly(p.pts, p.kind)
    # Size labels on the longer runs
    for p in m.pipes:
        L = sum(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(p.pts, p.pts[1:]))
        if L < 3 or p.kind not in ("waste", "cold"):
            continue
        (x1, y1), (x2, y2) = max(zip(p.pts, p.pts[1:]), key=lambda s: abs(s[0][0] - s[1][0]) + abs(s[0][1] - s[1][1]))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        lbl = (p.size + (" PVC" if p.kind == "waste" else " PEX"))
        if abs(y1 - y2) < 1e-6:
            cv.text(mx, my + (0.22 if p.kind == "waste" else -0.42), lbl, TXT["small"] * 0.85, "plumb_text" if p.kind == "waste" else "text_lt")
        else:
            cv.text(mx + (0.25 if p.kind == "waste" else -0.25), my, lbl, TXT["small"] * 0.85, "plumb_text" if p.kind == "waste" else "text_lt", rot=90)
    st = m.notes.get("stack")
    if st:
        cv.circle(*st, 0.32, "waste")
        cv.text(st[0] + 0.55, st[1] + 0.25, '3" VTR', TXT["small"], "plumb_text", anchor="start", bold=True)
    ex = m.notes.get("sewer_exit")
    if ex:
        cv.rect(ex[0] - 0.25, ex[1] - 0.25, 0.5, 0.5, "waste")
        lbl = "CO / TO SEWER OR SEPTIC" if not m.mobile else "SEWER OUTLET (RV)"
        dx = -0.6 if ex[0] <= 0.01 else 0.6 if ex[0] >= m.W - 0.01 else 0
        dy = -0.6 if ex[1] <= 0.01 else 0.6 if ex[1] >= m.D - 0.01 else 0
        cv.text(ex[0] + dx, ex[1] + dy - (0.15 if dy <= 0 else -0.05), lbl, TXT["small"], "plumb_text", anchor="end" if dx < 0 else "start" if dx > 0 else "middle", bold=True)
    we = m.notes.get("water_entry")
    if we:
        cv.circle(we[0], we[1], 0.28, "cold")
        cv.line(we[0] - 0.2, we[1] - 0.2, we[0] + 0.2, we[1] + 0.2, "cold")
        lbl = "WATER SERVICE + MAIN SHUTOFF" if not m.mobile else "FRESH WATER INLET + PRV"
        dy = -0.7 if we[1] <= 0.01 else 0.5
        dx = -0.6 if we[0] <= 0.01 else 0.6 if we[0] >= m.W - 0.01 else 0
        cv.text(we[0] + dx, we[1] + dy, lbl, TXT["small"], "text", anchor="end" if dx < 0 else "start" if dx > 0 else "middle", bold=True)
    # Hose bibbs on the front and rear walls
    for fac, yy in (("front", -0.35), ("rear", m.D + 0.35)):
        ws = [w for w in m.walls if w.exterior and w.facade == fac and abs(w.seg.c - (0 if fac == "front" else m.D)) < 1e-6]
        if ws:
            w = max(ws, key=lambda w: w.length)
            spans = m.free_spans(w, 0.3)
            if spans:
                a, b = max(spans, key=lambda t: t[1] - t[0])
                hx = b - 0.8
                cv.circle(hx, yy, 0.2, "cold")
                cv.text(hx, yy + (-0.55 if fac == "front" else 0.3), "HB", TXT["small"], "text", bold=True)
    # Fixture tags
    for f in m.fixtures:
        if f.kind in M.DFU and f.kind != "dw":
            pass


# ---------------------------------------------------------------------------------------
# Foundation, framing and loft plans
# ---------------------------------------------------------------------------------------

def draw_foundation(cv, m: M.Model):
    W, D = m.W, m.D
    fnd = m.foundation
    pr, inset = porch_rect(m)
    if fnd == "slab":
        outline = [(0, 0, W, D)] if not inset else [(r.x, r.y, r.w, r.d) for r in m.heated]
        for x, y, w, d in outline:
            pass
        cv.rect(0, 0, W, D, "concrete") if not inset else _outline_heated(cv, m, "concrete")
        _outline_heated(cv, m, "hidden", inset_by=1.0)
        cv.text(W / 2, D / 2 + 0.6, "4\" CONCRETE SLAB ON 10 MIL VAPOR RETARDER", TXT["note"], "text", bold=True)
        cv.text(W / 2, D / 2 + 0.05, "OVER 4\" COMPACTED CRUSHED STONE; #4 BARS @ 18\" O.C. E.W.", TXT["small"], "text")
        cv.text(W / 2, D / 2 - 0.5, "12\" x 12\" THICKENED EDGE W/ (2) #4 CONT. (DASHED)", TXT["small"], "text")
        _anchor_bolts(cv, m)
    elif fnd == "crawl":
        _outline_heated(cv, m, "concrete")
        _outline_heated(cv, m, "concrete", inset_by=0.67)
        _outline_heated(cv, m, "hidden", inset_by=-0.33)
        _outline_heated(cv, m, "hidden", inset_by=1.0)
        cv.line(0.67, D / 2, W - 0.67, D / 2, "hidden")
        n = max(2, math.ceil((W - 1.34) / 6))
        for i in range(1, n):
            px = 0.67 + (W - 1.34) * i / n
            cv.rect(px - 0.8, D / 2 - 0.8, 1.6, 1.6, "concrete")
            cv.rect(px - 0.33, D / 2 - 0.33, 0.67, 0.67, "concrete")
        cv.text(W / 2, D / 2 + 1.1, "BUILT-UP 3-2x10 GIRDER ON 16\" CMU PIERS / 24\" x 24\" x 10\" FTGS", TXT["small"], "text", bold=True)
        cv.text(W / 2, D * 0.25, "2x10 FLOOR JOISTS @ 16\" O.C. (TYP.)  -  8\" CMU STEM WALL ON 16\" x 8\" CONT. FOOTING", TXT["small"], "text")
        cv.rect(W - 4, 0.0, 2.5, 0.67, "concrete", fill="wallfill_lt")
        cv.text(W - 2.75, 0.95, "CRAWL ACCESS", TXT["small"], "text_lt")
        for i in range(1, max(2, int(W // 10))):
            vx = W * i / max(2, int(W // 10))
            for yy in (0.0, D - 0.67):
                cv.rect(vx - 0.6, yy, 1.2, 0.67, "hidden")
        _anchor_bolts(cv, m)
    elif fnd == "piers":
        cv.rect(0, 0, W, D, "hidden")
        xs = [0, W] if W <= 21 else [0, W / 2, W]
        for px in xs:
            for py in (0, D):
                qx = min(max(px - 1, 0), W - 2)
                qy = min(max(py - 1, 0), D - 2)
                cv.rect(qx, qy, 2, 2, "concrete", fill="wallfill_lt")
                cv.rect(qx + 0.5, qy + 0.5, 1, 1, "concrete")
        cv.text(W / 2, D / 2 + 0.25, "24\" x 24\" x 36\" CONCRETE PIERS W/ 3/8\" x 8\" x 8\" EMBEDDED WELD PLATES", TXT["small"], "text", bold=True)
        cv.text(W / 2, D / 2 - 0.35, "WELD CONTAINER CORNER CASTINGS TO PLATES (OR TWIST-LOCK BRACKETS)", TXT["small"], "text")
    else:  # trailer
        cv.rect(-0.2, 0.15, W + 0.4, D - 0.3, "concrete")
        for yy in (0.6, D - 0.6):
            cv.line(0, yy, W, yy, "struct_lt")
        axle = W * 0.58 if m.roof_type != "gooseneck" else (W - 8) * 0.55
        for ax in (axle - 1.6, axle + 1.6):
            cv.line(ax, -0.4, ax, D + 0.4, "struct")
            for yy in (-0.6, D - 0.2):
                cv.rect(ax - 1.1, yy, 2.2, 0.8, "struct")
        if m.roof_type == "gooseneck":
            cv.rect(W - 8, 0.15, 8, D - 0.3, "hidden")
            cv.text(W - 4, D / 2 - 0.1, "GOOSENECK DECK (RAISED 3'-2\")", TXT["small"], "text", bold=True)
        else:
            cv.poly([(0, D / 2 - 2.6), (-4.5, D / 2), (0, D / 2 + 2.6)], "struct")
            cv.circle(-4.6, D / 2, 0.3, "struct")
            cv.text(-4.6, D / 2 + 0.6, "2-5/16\" COUPLER", TXT["small"], "text_lt")
        cv.text(axle, D / 2 + 0.2, f"TANDEM 7,000 LB AXLES W/ ELECTRIC BRAKES", TXT["small"], "text", bold=True)
        cv.text(W * 0.3, D / 2 - 0.4, "WELDED-ON TIE-DOWN PLATES @ 4'-0\" O.C. - FASTEN BOTTOM PLATE W/ 1/2\" BOLTS", TXT["small"], "text")
    # Under-slab / underfloor plumbing rough-in
    for f in m.fixtures:
        if f.kind in ("toilet", "shower", "tub", "lav", "sink", "washer", "stack_wd"):
            x, y = (f.cx, f.cy) if f.kind in ("toilet", "shower", "tub") else f.back_point()
            cv.circle(x, y, 0.22, "waste")
    ex = m.notes.get("sewer_exit")
    if ex:
        cv.rect(ex[0] - 0.25, ex[1] - 0.25, 0.5, 0.5, "waste")


def _outline_heated(cv, m, st, inset_by=0.0):
    """Outline of the heated footprint (handles an inset porch notch), optionally offset inward."""
    pr, inset = porch_rect(m)
    W, D, k = m.W, m.D, inset_by
    if not inset:
        cv.rect(k, k, W - 2 * k, D - 2 * k, st)
        return
    px, py, pw, pd = pr
    # porch in a corner of the footprint at (0, 0)
    if px == 0 and py == 0:
        pts = [(pw + k, k), (W - k, k), (W - k, D - k), (k, D - k), (k, pd + k), (pw + k, pd + k)]
    else:
        pts = [(k, k), (W - k, k), (W - k, D - k), (k, D - k)]
    cv.poly(pts, st, closed=True)


def _anchor_bolts(cv, m):
    W, D = m.W, m.D
    t = 0.3
    for x in [0.9 + i * 6 for i in range(int((W - 1.8) // 6) + 1)] + [W - 0.9]:
        for y in (t, D - t):
            if _inside_or_wall(m, x, y):
                cv.circle(x, y, 0.1, "concrete", fill="concrete")
    for y in [0.9 + i * 6 for i in range(int((D - 1.8) // 6) + 1)] + [D - 0.9]:
        for x in (t, W - t):
            if _inside_or_wall(m, x, y):
                cv.circle(x, y, 0.1, "concrete", fill="concrete")


def _inside_or_wall(m, x, y):
    return any(r.x - 0.01 <= x <= r.x2 + 0.01 and r.y - 0.01 <= y <= r.y2 + 0.01 for r in m.heated)


def draw_framing(cv, m: M.Model):
    W, D = m.W, m.D
    info = profile(m)
    ov = info["ov"]
    _outline_heated(cv, m, "hidden")
    rt = m.roof_type
    if rt in ("container",):
        cv.rect(0, 0, W, D, "struct")
        cv.text(W / 2, D / 2, "CORRUGATED CONTAINER ROOF - SLOPE 1/4\" PER FT MIN. TO DRIP EDGE; ELASTOMERIC COATING", TXT["small"], "text", bold=True)
        return
    cv.rect(-ov, -ov, W + 2 * ov, D + 2 * ov, "struct")
    n = int(W // 2) + 1
    for i in range(n + 1):
        x = min(i * 2.0, W)
        cv.line(x, -ov, x, D + ov, "struct_lt")
    if info["kind"] in ("gable", "aframe", "gambrel"):
        cv.line(-ov, D / 2, W + ov, D / 2, "struct")
        cv.text(W / 2, D / 2 + 0.25, "RIDGE", TXT["small"], "text", bold=True)
    if info["kind"] == "gambrel":
        for yy in (D * 0.16, D * 0.84):
            cv.line(-ov, yy, W + ov, yy, "hidden")
    pitch = m.pitch
    labels = {
        "gable": f"PRE-ENGINEERED TRUSSES @ 24\" O.C., {pitch:g}:12 PITCH, {ft_in(D)} SPAN - BY TRUSS MFR.",
        "shed": f"2x RAFTERS @ 24\" O.C. ({'2x6' if D + 2 * ov <= 9.5 else '2x8' if D + 2 * ov <= 13 else '2x10'}), {pitch:g}:12 SLOPE TO REAR",
        "shedover": "2x6 RAFTERS @ 24\" O.C. ON STEEL POSTS / BEAM OVER CONTAINERS",
        "aframe": "2x10 RAFTER PAIRS @ 24\" O.C. W/ 2x6 COLLAR TIES; 2x12 RIDGE BOARD",
        "gambrel": "2x6 GAMBREL RAFTERS @ 24\" O.C. W/ 1/2\" PLYWOOD GUSSETS",
    }
    if rt in ("thow", "gooseneck"):
        lbl = f"2x6 RAFTERS @ 24\" O.C., {pitch:g}:12, 2x8 RIDGE; SIMPSON H2.5A @ EA. RAFTER"
    else:
        lbl = labels.get(info["kind"], "")
    cv.text(W / 2, D * 0.27, lbl, TXT["small"], "text", bold=True)
    cv.text(W / 2, D * 0.27 - 0.5, f"{'1/2\" CDX' if True else ''} ROOF SHEATHING; {ft_in(ov)} OVERHANG AT EAVES AND RAKES", TXT["small"], "text")
    # Header callouts at exterior openings
    for o in m.openings:
        if not o.exterior:
            continue
        s, nx, ny, f0, f1 = opening_geom(m, o)
        x, y = s.at(o.s)
        cv.text(x - nx * 0.6, y - ny * 0.6 - 0.1, f"{o.tag}: {header_for(o.width)}", TXT["small"] * 0.9, "accent", bold=True,
                rot=90 if s.o == "v" else 0)


def draw_loft(cv, m: M.Model):
    _outline_heated(cv, m, "wall_lt")
    for x, y, w, h in wall_rects(m):
        cv.rect(x, y, w, h, "wall_lt", fill="wallfill_lt")
    for lr in m.lofts:
        cv.rect(lr.x, lr.y, lr.w, lr.d, "wall")
        cv.text(lr.cx, lr.cy + 1.4 if lr.d > 5 else lr.cy + 0.3, lr.label, TXT["room"], "text", bold=True)
        cv.text(lr.cx, lr.cy + 0.9 if lr.d > 5 else lr.cy - 0.2, f"{ft_in(lr.w, False)} x {ft_in(lr.d, False)}  ({round(lr.area)} SQ FT)", TXT["small"], "text_lt")
        # guardrail on edges not against an exterior wall
        for e in lr.edges():
            on_ext = (e.o == "h" and (abs(e.c) < 1e-6 or abs(e.c - m.D) < 1e-6)) or (e.o == "v" and (abs(e.c) < 1e-6 or abs(e.c - m.W) < 1e-6))
            if not on_ext:
                p1, p2 = e.p1, e.p2
                cv.line(*p1, *p2, "door")
                mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
                cv.text(mx + (0.4 if e.o == "v" else 0), my + (0.3 if e.o == "h" else 0), "GUARD 36\" MIN.", TXT["small"] * 0.85, "accent", rot=90 if e.o == "v" else 0)
                # ladder / stair just outside the open edge
                if e.o == "v":
                    lx = e.c + (0.2 if e.side == "E" else -1.9)
                    ly = (e.a + e.b) / 2 - 0.9
                    cv.rect(lx, ly, 1.7, 1.8, "fixture")
                    for k in range(1, 5):
                        cv.line(lx + 1.7 * k / 5, ly, lx + 1.7 * k / 5, ly + 1.8, "fixture")
                    cv.text(lx + 0.85, ly - 0.35, "LADDER / SHIP STAIR", TXT["small"] * 0.85, "text_lt")
                    break
        for f in m.fixtures:
            if f.room is lr:
                draw_fixture(cv, f)
    draw_electrical(cv, m, loft=True)


# ---------------------------------------------------------------------------------------
# Elevations and section
# ---------------------------------------------------------------------------------------

def facade_len(m, fac):
    return m.W if fac in ("front", "rear") else m.D


def to_u(m, fac, s):
    return {"front": s, "rear": m.W - s, "right": s, "left": m.D - s}[fac]


def draw_elevation(cv, m: M.Model, fac: str):
    info = profile(m)
    B, ov, p = info["B"], info["ov"], info["pitch"]
    L = facade_len(m, fac)
    k = info["kind"]
    eave_side = fac in ("front", "rear")
    gn = m.roof_type == "gooseneck"
    mobile = m.mobile

    def raised(u):
        if not gn or not eave_side:
            return 0
        x = u if fac == "front" else m.W - u
        return 3.2 if x >= m.W - 8 - 1e-6 else 0

    cv.line(-6, 0, L + 6, 0, "earth")
    # foundation / trailer
    if mobile:
        cv.rect(-0.2, B - 0.55, L + 0.4, 0.5, "struct")
        if eave_side:
            axle = m.W * 0.58 if not gn else (m.W - 8) * 0.55
            for ax in (axle - 1.6, axle + 1.6):
                u = ax if fac == "front" else m.W - ax
                cv.circle(u, 1.15, 1.15, "struct")
                cv.circle(u, 1.15, 0.5, "struct_lt")
            if not gn:
                u0 = 0 if fac == "front" else L
                d = -1 if fac == "front" else 1
                cv.line(u0, B - 0.4, u0 + d * 4.2, 1.3, "struct")
            else:
                u0 = L - 8 if fac == "front" else 0
                cv.rect(u0, B, 8, 3.2, "struct_lt")
    elif m.container:
        xs = [0, L - 2] if L <= 21 else [0, L / 2 - 1, L - 2]
        for px in xs:
            cv.rect(px, 0, 2, B, "concrete")
    else:
        cv.rect(-0.1, 0, L + 0.2, B, "concrete")
    # walls + roof by type
    front, rear = info["front"], info["rear"]
    if k == "gable":
        R = info["ridge"]
        if eave_side:
            if gn:
                pts = [(0, B + raised(0.1)), (L, B + raised(L - 0.1))]
                xg = (m.W - 8) if fac == "front" else 8
                if fac == "front":
                    cv.poly([(0, B), (xg, B), (xg, B + 3.2), (L, B + 3.2), (L, front), (0, front)], "wall", closed=True)
                else:
                    cv.poly([(0, B + 3.2), (xg, B + 3.2), (xg, B), (L, B), (L, front), (0, front)], "wall", closed=True)
            else:
                cv.rect(0, B, L, front - B, "wall")
            e = front - ov * p
            cv.poly([(-ov, e), (L + ov, e), (L + ov, R), (-ov, R)], "wall", closed=True)
            cv.line(-ov, e + 0.35, L + ov, e + 0.35, "thin")
            for i in range(1, 6):
                z = e + (R - e) * i / 6
                cv.line(-ov, z, L + ov, z, "grid")
        else:
            cv.poly([(0, B), (L, B), (L, front), (L / 2, R), (0, front)], "wall", closed=True)
            dz = ov * p
            cv.poly([(-ov, front - dz), (L / 2, R + 0.05), (L + ov, front - dz)], "wall")
            cv.poly([(-ov, front - dz + 0.45), (L / 2, R + 0.5), (L + ov, front - dz + 0.45)], "wall")
            cv.circle(L / 2, front + (R - front) * 0.45, 0.5, "thin")    # gable vent
    elif k == "shed":
        if fac == "front":
            cv.rect(0, B, L, front - B, "wall")
            cv.rect(-ov, front + ov * p - 0.1, L + 2 * ov, 0.6, "wall")
            for cx, cw in m.notes.get("clerestory", []):
                cv.rect(cx - cw / 2, front - 1.7, cw, 1.15, "window")
        elif fac == "rear":
            cv.rect(0, B, L, rear - B, "wall")
            cv.rect(-ov, rear - ov * p - 0.5, L + 2 * ov, 0.6, "wall")
        else:
            hl, hr = (front, rear) if fac == "right" else (rear, front)
            cv.poly([(0, B), (L, B), (L, hr), (0, hl)], "wall", closed=True)
            dl = ov * p
            zl = hl + (dl if hl > hr else -dl)
            zr = hr + (-dl if hl > hr else dl)
            cv.poly([(-ov, zl), (L + ov, zr), (L + ov, zr + 0.55), (-ov, zl + 0.55)], "wall", closed=True)
    elif k in ("flat", "shedover"):
        cv.rect(0, B, L, front - B, "wall")
        cv.rect(0, front - 0.35, L, 0.35, "thin")
        cv.rect(0, B, L, 0.35, "thin")
        for i in range(1, int(L / 0.5)):
            cv.line(i * 0.5, B + 0.45, i * 0.5, front - 0.45, "grid")
        if k == "shedover":
            rf, rr = info["roof_front"], info["roof_rear"]
            if fac == "front":
                cv.rect(-ov, rf - 0.35, L + 2 * ov, 0.35, "wall")
            elif fac == "rear":
                cv.rect(-ov, rr - 0.35, L + 2 * ov, 0.35, "wall")
            else:
                hl, hr = (rf, rr) if fac == "right" else (rr, rf)
                cv.poly([(-ov, hl), (L + ov, hr), (L + ov, hr - 0.35), (-ov, hl - 0.35)], "wall", closed=True)
            for xx in ([0.2, L / 2, L - 0.5] if eave_side else [0.0, L - 0.3]):
                top = (rf if fac == "front" else rr) if eave_side else (rf + (rr - rf) * (xx / L) if fac == "right" else rr + (rf - rr) * (xx / L))
                cv.rect(xx, front, 0.3, top - front - 0.35, "thin")
    elif k == "aframe":
        H = info["ridge"]
        if eave_side:
            cv.poly([(-ov, B - 0.8), (L + ov, B - 0.8), (L + ov, H + 0.4), (-ov, H + 0.4)], "wall", closed=True)
            for i in range(1, int((L + 2 * ov) / 1.5)):
                cv.line(-ov + i * 1.5, B - 0.8, -ov + i * 1.5, H + 0.4, "grid")
        else:
            cv.poly([(0, B), (L / 2, H), (L, B)], "wall", closed=True)
            cv.poly([(-0.5, B - 0.8), (L / 2, H + 1.1), (L + 0.5, B - 0.8)], "wall")
            cv.poly([(-0.1, B - 0.25), (L / 2, H + 0.45), (L + 0.1, B - 0.25)], "wall")
            if fac == "left":   # glass gable over the entry
                z0 = B + 7.6
                hw = (H - z0) * (L / 2) / (H - B)
                cv.poly([(L / 2 - hw + 0.6, z0), (L / 2, H - 1.2), (L / 2 + hw - 0.6, z0)], "window", closed=True)
                cv.line(L / 2, z0, L / 2, H - 1.2, "window")
    elif k == "gambrel":
        Ln = info["line"]
        if eave_side:
            Pg = B + info["P"]
            cv.rect(0, B, L, info["P"], "wall")
            knee = Ln[1][1]
            cv.poly([(-ov, Pg - 0.4), (L + ov, Pg - 0.4), (L + ov, knee), (-ov, knee)], "wall", closed=True)
            cv.poly([(-ov, knee), (L + ov, knee), (L + ov, info["ridge"]), (-ov, info["ridge"])], "wall", closed=True)
            for i in range(1, 4):
                z = knee + (info["ridge"] - knee) * i / 4
                cv.line(-ov, z, L + ov, z, "grid")
        else:
            cv.poly([(0, B)] + [(u, z) for u, z in Ln] + [(L, B)], "wall", closed=True)
            cv.poly([(Ln[0][0] - 0.6, Ln[0][1] - 0.4)] + [(u, z + 0.45) for u, z in Ln[1:-1]] + [(Ln[-1][0] + 0.6, Ln[-1][1] - 0.4)], "wall")
    # Outside porch
    pr, inset = porch_rect(m)
    if pr and not inset and k != "aframe":
        px, py, pw, pd = pr
        ph = B + 8.2
        if py < 0:   # front porch
            if eave_side:
                u0, u1 = (px, px + pw) if fac == "front" else (m.W - px - pw, m.W - px)
                if fac == "front":
                    cv.poly([(u0 - 0.6, ph), (u1 + 0.6, ph), (u1 + 0.6, ph + 1.1), (u0 - 0.6, ph + 1.1)], "accent", closed=True)
                    for qx, _ in _porch_posts(m, pr):
                        cv.rect(qx, B, 0.45, ph - B, "accent")
                    cv.rect(u0, B - 0.45, pw, 0.4, "accent")
            else:
                u0, u1 = (-pd, 0) if fac == "right" else (L, L + pd)
                cv.rect(u0, B - 0.45, pd, 0.4, "accent")
                post = u0 + 0.05 if fac == "right" else u1 - 0.5
                cv.rect(post, B, 0.45, ph - B, "accent")
                hi_u = 0 if fac == "right" else L
                lo_u = u0 - 0.6 if fac == "right" else u1 + 0.6
                cv.poly([(lo_u, ph), (hi_u, ph + 1.1)], "accent")
        elif px >= m.W - 0.01:   # side porch
            if fac == "front":
                cv.rect(L, B - 0.45, pw, 0.4, "accent")
                cv.rect(L + pw - 0.5, B, 0.45, ph - B, "accent")
                cv.poly([(L, ph + 1.1), (L + pw + 0.6, ph)], "accent")
            elif fac == "rear":
                cv.rect(-pw, B - 0.45, pw, 0.4, "accent")
                cv.rect(-pw + 0.05, B, 0.45, ph - B, "accent")
                cv.poly([(0, ph + 1.1), (-pw - 0.6, ph)], "accent")
    if pr and inset and fac == "front":
        for qx, _ in _porch_posts(m, pr):
            cv.rect(qx, B, 0.45, front - B, "accent")
    # Openings on this facade
    for o in m.openings:
        if not o.exterior or o.wall.facade != fac:
            continue
        u0, u1 = sorted((to_u(m, fac, o.a), to_u(m, fac, o.b)))
        xm = o.wall.seg.at(o.s)[0]
        zb = B + (3.2 if gn and xm >= m.W - 8 - 1e-6 else 0)
        z0, z1 = zb + o.sill, zb + o.sill + o.height
        setback = o.wall.seg.c not in (0.0, m.W, m.D)
        if o.kind == "window":
            cv.rect(u0 - 0.2, z0 - 0.2, u1 - u0 + 0.4, z1 - z0 + 0.4, "thin")
            cv.rect(u0, z0, u1 - u0, z1 - z0, "window")
            if o.egress:
                cv.line((u0 + u1) / 2, z0, (u0 + u1) / 2, z1, "window")
            else:
                cv.line(u0, (z0 + z1) / 2, u1, (z0 + z1) / 2, "window")
            cv.text((u0 + u1) / 2, z0 - 0.75, o.tag, TXT["tag"], "accent", bold=True)
        else:
            cv.rect(u0 - 0.25, z0, u1 - u0 + 0.5, z1 - z0 + 0.25, "thin")
            cv.rect(u0, z0, u1 - u0, z1 - z0, "door")
            if o.kind == "slider" or o.width >= 5:
                cv.line((u0 + u1) / 2, z0, (u0 + u1) / 2, z1, "door")
                if o.kind == "slider":
                    cv.rect(u0 + 0.25, z0 + 0.25, (u1 - u0) / 2 - 0.5, z1 - z0 - 0.5, "window")
                    cv.rect((u0 + u1) / 2 + 0.25, z0 + 0.25, (u1 - u0) / 2 - 0.5, z1 - z0 - 0.5, "window")
                else:
                    for a, b in ((u0, (u0 + u1) / 2), ((u0 + u1) / 2, u1)):
                        cv.line(a, z0, b, z1, "thin")
                        cv.line(a, z1, b, z0, "thin")
            else:
                cv.rect(u0 + 0.4, z0 + (z1 - z0) * 0.5, u1 - u0 - 0.8, (z1 - z0) * 0.4, "window")
                cv.circle(u1 - 0.35, z0 + 3.0, 0.08, "door")
            cv.text((u0 + u1) / 2, z1 + 0.45, o.tag, TXT["tag"], "accent", bold=True)
    # Height dimensions on the right
    xr = L + (ov + 1.6 if k != "aframe" else 2.4) + (pr[3] if pr and not inset and pr[1] < 0 and fac == "left" else 0)
    levels = [(0, "GRADE"), (B, "FIN. FLOOR")]
    if k == "aframe":
        levels.append((info["ridge"], "RIDGE"))
    elif k == "gambrel":
        levels += [(B + info["P"], "T.O. WALL"), (info["ridge"], "RIDGE")]
    elif k == "shed":
        top = front if fac in ("front", "right") else rear
        levels += [(top if eave_side else max(front, rear), "T.O. PLATE (HIGH)")]
    elif k in ("flat",):
        levels.append((front, "T.O. CONTAINER"))
    elif k == "shedover":
        levels += [(front, "T.O. CONTAINER"), (info["roof_front"], "T.O. ROOF")]
    else:
        levels += [(front, "T.O. PLATE"), (info["ridge"], "RIDGE")]
    for z, lbl in levels:
        cv.line(xr - 0.4, z, xr + 0.4, z, "dim")
        cv.text(xr + 0.6, z - 0.1, f"{lbl}  {ft_in(z)}", TXT["small"], "dim", anchor="start")
    cv.line(xr, 0, xr, levels[-1][0], "dim")


def draw_section(cv, m: M.Model):
    """Transverse building section cut through the loft (or the middle of the house), looking left."""
    info = profile(m)
    B, ov, p = info["B"], info["ov"], info["pitch"]
    D = m.D
    k = info["kind"]
    xc = m.lofts[0].cx if m.lofts else m.W / 2
    cv.line(-5, 0, D + 5, 0, "earth")
    t = m.ext_t
    fnd = m.foundation
    # foundation / floor structure
    if fnd == "slab":
        cv.poly([(0, B), (D, B), (D, -0.5), (D - 1, -0.5), (D - 1, B - 0.33), (1, B - 0.33), (1, -0.5), (0, -0.5)], "concrete", closed=True)
    elif fnd == "crawl":
        for u in (0, D - 0.67):
            cv.rect(u, -1.0, 0.67, B - 0.9 + 1.0, "concrete")
            cv.rect(u - 0.33, -1.67, 1.33, 0.67, "concrete")
        cv.rect(0, B - 0.9, D, 0.9, "struct")
        cv.rect(D / 2 - 0.4, -1.0, 0.8, B - 0.9 + 1.0, "concrete")
    elif fnd == "trailer":
        cv.rect(0, B - 0.55, D, 0.5, "struct")
        cv.circle(D / 2, 1.15, 1.15, "struct_lt")
        cv.rect(0, B - 0.05 - 0.5, D, 0.5, "struct_lt")
    else:
        cv.rect(0, 0, 2, B, "concrete")
        cv.rect(D - 2, 0, 2, B, "concrete")
        cv.rect(0, B - 0.3, D, 0.3, "struct")
    cv.line(0, B, D, B, "wall")
    # walls and roof
    line = info["line"]
    if k != "aframe":
        for u0 in (0, D - t):
            top = roof_z(info, u0 + t / 2)
            cv.rect(u0, B, t, top - B, "wall", fill="wallfill")
    outer = [(u, z) for u, z in line]
    # roof structure: outer line extended by the overhang, inner line offset down
    th = 0.8 if k != "flat" else 0.3
    if k == "gable":
        dz = ov * p
        cv.poly([(-ov, line[0][1] - dz), (D / 2, info["ridge"] + 0.1), (D + ov, line[-1][1] - dz)], "wall")
        cv.poly([(-ov, line[0][1] - dz + th), (D / 2, info["ridge"] + th + 0.1), (D + ov, line[-1][1] - dz + th)], "wall")
        if m.roof_type in ("gable", "gable-steep"):
            cv.line(t, info["front"], D - t, info["front"], "struct")     # bottom chord / ceiling
            for frac in (0.25, 0.5, 0.75):
                u = D * frac
                cv.line(u, info["front"], u, roof_z(info, u), "struct_lt")
            cv.line(D * 0.25, info["front"], D * 0.5, info["ridge"], "struct_lt")
            cv.line(D * 0.75, info["front"], D * 0.5, info["ridge"], "struct_lt")
    elif k == "shed":
        cv.poly([(-ov, info["front"] + ov * p), (D + ov, info["rear"] - ov * p)], "wall")
        cv.poly([(-ov, info["front"] + ov * p + th), (D + ov, info["rear"] - ov * p + th)], "wall")
    elif k in ("flat", "shedover"):
        cv.rect(0, info["front"] - 0.3, D, 0.3, "struct")
        if k == "shedover":
            cv.poly([(-ov, info["roof_front"]), (D + ov, info["roof_rear"])], "wall")
            cv.poly([(-ov, info["roof_front"] - 0.35), (D + ov, info["roof_rear"] - 0.35)], "wall")
    elif k == "aframe":
        H = info["ridge"]
        cv.poly([(-0.5, B - 0.8), (D / 2, H + 1.1), (D + 0.5, B - 0.8)], "wall")
        cv.poly([(0.1, B), (D / 2, H + 0.3), (D - 0.1, B)], "wall")
        cv.line(D * 0.25, B + (H - B) * 0.5 + 0.4, D * 0.75, B + (H - B) * 0.5 + 0.4, "struct_lt")
    elif k == "gambrel":
        cv.poly(outer, "wall")
        cv.poly([(u, z + th) for u, z in outer], "wall")
    # loft
    for lr in m.lofts:
        if lr.x <= xc <= lr.x2:
            z = B + 7.0
            y0, y1 = lr.y, lr.y2
            while y0 < y1 and roof_z(info, y0) < z + 0.9:
                y0 += 0.1
            while y1 > y0 and roof_z(info, y1) < z + 0.9:
                y1 -= 0.1
            cv.rect(y0, z, y1 - y0, 0.65, "struct", fill="wallfill_lt")
            cv.text((y0 + y1) / 2, z + 1.4, lr.label, TXT["label"], "text", bold=True)
            open_edge = y1 if y1 < D - 0.5 else y0 if y0 > 0.5 else None
            if open_edge is not None:
                cv.line(open_edge, z + 0.65, open_edge, z + 0.65 + 3.0, "door")
                cv.text(open_edge, z + 3.9, "36\" GUARD", TXT["small"], "accent")
            cv.line(D + ov + 0.8, z, D + ov + 1.3, z, "dim")
            cv.text(D + ov + 1.5, z - 0.1, f"LOFT FLOOR {ft_in(z)}", TXT["small"], "dim", anchor="start")
    # interior partitions crossed by the cut, and room names
    for w in m.walls:
        if not w.exterior and not w.open and w.seg.o == "h" and w.seg.a <= xc <= w.seg.b:
            top = min(B + 8, roof_z(info, w.seg.c) - 0.3)
            cv.rect(w.seg.c - m.int_t / 2, B, m.int_t, top - B, "wall", fill="wallfill")
    for r in m.heated:
        if r.x <= xc <= r.x2:
            cv.text(r.cy, B + 3.2, r.label, TXT["label"], "text", bold=True)
            ceil = min(roof_z(info, r.cy), info["front"] if m.roof_type in ("gable", "gable-steep", "container", "container-double") else 99) - B
            cv.text(r.cy, B + 2.5, f"CLG {ft_in(ceil)}", TXT["small"], "text_lt")


# ---------------------------------------------------------------------------------------
# Shaded axonometric render (cover sheet, previews)
# ---------------------------------------------------------------------------------------

def render_axo(cv, me, m: M.Model, ox, oy, width, height, groups=("structure", "roof"), az=-38, el=28):
    """Painter's-algorithm render of the mesh into a box (paper inches)."""
    import thb_mesh
    a = math.radians(az)
    e = math.radians(el)
    ca, sa, ce, se = math.cos(a), math.sin(a), math.cos(e), math.sin(e)
    light = (-0.45, -0.6, 0.66)
    L = math.sqrt(sum(c * c for c in light))
    light = tuple(c / L for c in light)
    polys = []
    for g in groups:
        for mat, tris in me.g.get(g, {}).items():
            base = thb_mesh.MATERIALS.get(mat, "#cccccc")
            rgb = [int(base[i:i + 2], 16) for i in (1, 3, 5)]
            for t in tris:
                pts = []
                for x, y, z in t:
                    x -= m.W / 2
                    y -= m.D / 2
                    xr = x * ca - y * sa
                    yr = x * sa + y * ca
                    u = xr
                    v = z * ce + yr * se
                    depth = yr * ce - z * se
                    pts.append((u, v, depth))
                (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = t
                nx = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
                ny = (z2 - z1) * (x3 - x1) - (x2 - x1) * (z3 - z1)
                nz = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
                nl = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
                nx, ny, nz = nx / nl, ny / nl, nz / nl
                # flip normals that face away from the camera (double-sided)
                vx, vy, vz = math.sin(a) * ce * 0 + (-sa * ce), (-ca * ce), se
                facing = nx * (sa * ce) + ny * (-ca * ce) + nz * se
                if facing < 0:
                    nx, ny, nz = -nx, -ny, -nz
                lam = max(0.0, nx * light[0] + ny * light[1] + nz * light[2])
                shade = 0.55 + 0.45 * lam
                col = "#%02x%02x%02x" % tuple(min(255, int(c * shade)) for c in rgb)
                depth = max(p_[2] for p_ in pts) * 0.7 + sum(p_[2] for p_ in pts) / 3 * 0.3
                polys.append((depth, [(p_[0], p_[1]) for p_ in pts], col))
    if not polys:
        return
    us = [q[0] for _, pts, _ in polys for q in pts]
    vs = [q[1] for _, pts, _ in polys for q in pts]
    w, h = max(us) - min(us), max(vs) - min(vs)
    s = min(width / w, height / h)
    cx, cy = ox + (width - w * s) / 2 - min(us) * s, oy + (height - h * s) / 2 - min(vs) * s
    polys.sort(key=lambda q: -q[0])
    prev = (cv.ox, cv.oy, cv.s, cv.in_view)
    cv.paper()
    for _, pts, col in polys:
        cv.shape([(cx + u * s, cy + v * s) for u, v in pts], col, lw=0.12)
    cv.ox, cv.oy, cv.s, cv.in_view = prev
