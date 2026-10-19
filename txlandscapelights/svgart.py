"""Inline SVG artwork: the lit-house scene (visualizer), the Texas map and the logo. Photos live in photos.py."""
import math
import random


def _stars(rng, n, w, h, maxy):
    out = []
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(0, maxy)
        r = rng.choice((0.6, 0.8, 1.0, 1.3))
        out.append(f'<circle class="twinkle" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity="{rng.uniform(.35, .9):.2f}"/>')
    return "".join(out)


def _defs(p):
    return f"""<defs>
<linearGradient id="{p}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b13"/><stop offset=".6" stop-color="#121a27"/><stop offset="1" stop-color="#262733"/></linearGradient>
<radialGradient id="{p}-g"><stop offset="0" stop-color="currentColor" stop-opacity=".95"/><stop offset=".45" stop-color="currentColor" stop-opacity=".35"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></radialGradient>
<linearGradient id="{p}-up" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="currentColor" stop-opacity=".85"/><stop offset=".55" stop-color="currentColor" stop-opacity=".28"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient>
<linearGradient id="{p}-dn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity=".7"/><stop offset="1" stop-color="currentColor" stop-opacity="0"/></linearGradient>
<linearGradient id="{p}-lawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151b14"/><stop offset="1" stop-color="#0a0d0a"/></linearGradient>
<pattern id="{p}-stone" width="40" height="18" patternUnits="userSpaceOnUse"><rect width="40" height="18" fill="#34322e"/><path d="M0 17.5h40M20 0v9M0 9h40M8 9v9M32 9v9" stroke="#26241f" stroke-width="1.2"/></pattern>
<filter id="{p}-blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>"""


def scene(p="hero", title="A Texas Hill Country home lit at night"):
    """The main house scene. Light layers: .lt-arch .lt-path .lt-tree .lt-patio; windows .win."""
    rng = random.Random(7)
    W, H = 800, 520
    canopy = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#0e1710"/>'
        for cx, cy, rx, ry in [(70, 250, 70, 42), (130, 220, 90, 55), (200, 248, 72, 40), (40, 290, 50, 30), (150, 280, 110, 38), (230, 290, 46, 26)]
    )
    canopy_lit = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{p}-g)" opacity=".55"/>'
        for cx, cy, rx, ry in [(110, 245, 95, 60), (185, 262, 70, 42), (60, 278, 55, 34)]
    )
    path_pts = [(452, 430), (430, 452), (404, 476), (382, 505)]
    path_l = "".join(
        f'<ellipse cx="{x}" cy="{y + 4}" rx="{30 + i * 6}" ry="{8 + i * 2}" fill="url(#{p}-g)" opacity=".8"/>'
        f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 16 - i * 3}" stroke="#55534d" stroke-width="{1.6 + i * .4}"/>'
        f'<ellipse cx="{x}" cy="{y - 17 - i * 3}" rx="{5 + i}" ry="{2 + i * .4}" fill="#3a3833"/>'
        f'<ellipse cx="{x}" cy="{y - 14 - i * 3}" rx="{4 + i}" ry="2" fill="currentColor"/>'
        for i, (x, y) in enumerate(path_pts)
    ) + "".join(
        f'<ellipse cx="{x}" cy="{y + 4}" rx="{26 + i * 6}" ry="{7 + i * 2}" fill="url(#{p}-g)" opacity=".7"/>'
        f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y - 15 - i * 3}" stroke="#55534d" stroke-width="{1.6 + i * .4}"/>'
        f'<ellipse cx="{x}" cy="{y - 14 - i * 3}" rx="{4 + i}" ry="2" fill="currentColor"/>'
        for i, (x, y) in enumerate([(492, 432), (478, 456), (466, 482), (458, 510)])
    )
    ups = [(268, 262), (370, 262), (512, 262), (612, 262)]
    arch = "".join(
        f'<polygon points="{x - 5},412 {x - 34},{t} {x + 34},{t} {x + 5},412" fill="url(#{p}-up)" opacity=".75"/>'
        f'<ellipse cx="{x}" cy="412" rx="16" ry="5" fill="url(#{p}-g)"/><rect x="{x - 3}" y="406" width="6" height="7" rx="1" fill="#222"/>'
        for x, t in ups
    ) + (f'<polygon points="436,412 404,212 476,212 444,412" fill="url(#{p}-up)" opacity=".85"/>'
         f'<ellipse cx="440" cy="300" rx="44" ry="70" fill="url(#{p}-g)" opacity=".25"/>'
         f'<polygon points="560,262 552,196 588,196 580,262" fill="url(#{p}-up)" opacity=".6"/>')
    tree = "".join(
        f'<polygon points="{x - 4},428 {x - 40},{t} {x + 40},{t} {x + 4},428" fill="url(#{p}-up)" opacity=".7"/>'
        f'<ellipse cx="{x}" cy="428" rx="14" ry="4" fill="url(#{p}-g)"/>'
        for x, t in [(96, 220), (150, 200), (196, 236)]
    ) + canopy_lit
    # patio string lights: catenary from house corner to post
    bulbs, seg = [], []
    x0, y0, x1, y1 = 640, 316, 778, 330
    for i in range(12):
        t = i / 11
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t + math.sin(math.pi * t) * 22
        bulbs.append(f'<circle cx="{x:.0f}" cy="{y + 4:.0f}" r="9" fill="url(#{p}-g)"/><circle cx="{x:.0f}" cy="{y + 4:.0f}" r="2.3" fill="currentColor"/>')
        seg.append(f"{x:.1f},{y:.1f}")
    patio = (f'<ellipse cx="712" cy="432" rx="96" ry="20" fill="url(#{p}-g)" opacity=".55"/>'
             f'<polyline points="{" ".join(seg)}" fill="none" stroke="#5d584f" stroke-width="1.2"/>' + "".join(bulbs))
    stone = f"url(#{p}-stone)"
    return f"""<svg class="scene" id="{p}-scene" viewBox="0 0 {W} {H}" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg">{_defs(p)}
<rect width="{W}" height="{H}" fill="url(#{p}-sky)"/>
<g>{_stars(rng, 70, W, H, 230)}</g>
<circle cx="700" cy="78" r="46" fill="#f5efdf" opacity=".08"/><circle cx="700" cy="78" r="24" fill="#efe8d6" opacity=".9"/><circle cx="709" cy="72" r="21" fill="#121a27" opacity=".55"/>
<path d="M0 360 C120 330 220 345 330 336 S560 318 640 330 S760 338 800 330 V420 H0Z" fill="#0d1219"/>
<rect y="408" width="{W}" height="{H - 408}" fill="url(#{p}-lawn)"/>
<path d="M96 430 C100 380 112 330 120 290 M120 300 C100 280 80 265 60 262 M122 296 C150 270 180 262 205 255 M118 330 C135 310 160 300 190 295" stroke="#18130f" stroke-width="12" fill="none" stroke-linecap="round"/>
<path d="M118 430 L124 300" stroke="#18130f" stroke-width="18"/>
{canopy}
<rect x="552" y="196" width="36" height="70" fill="#2a2825"/><rect x="548" y="190" width="44" height="8" fill="#1d1c1a"/>
<polygon points="226,264 440,168 654,264" fill="#17191c"/>
<g stroke="#24272b" stroke-width="1.2">{"".join(f'<line x1="{x}" y1="{168 + abs(x - 440) * 96 / 214:.0f}" x2="{x}" y2="264"/>' for x in range(250, 640, 16))}</g>
<rect x="250" y="262" width="380" height="150" fill="{stone}"/>
<rect x="250" y="262" width="380" height="150" fill="#000" opacity=".25"/>
<polygon points="378,264 440,204 502,264" fill="#1c1e22"/>
<rect x="388" y="262" width="104" height="150" fill="{stone}"/>
<rect x="250" y="404" width="380" height="8" fill="#1d1c19"/>
<circle class="win" cx="440" cy="240" r="11"/>
<rect class="win" x="276" y="296" width="38" height="56" rx="2"/><rect class="win" x="328" y="296" width="38" height="56" rx="2"/>
<rect class="win" x="516" y="296" width="38" height="56" rx="2"/><rect class="win" x="568" y="296" width="38" height="56" rx="2"/>
<g stroke="#1a1a1a" stroke-width="2.5">{"".join(f'<line x1="{x + 19}" y1="296" x2="{x + 19}" y2="352"/><line x1="{x}" y1="324" x2="{x + 38}" y2="324"/>' for x in (276, 328, 516, 568))}</g>
<rect x="420" y="330" width="40" height="78" rx="18" fill="#3b2a1d"/><rect x="420" y="330" width="40" height="78" rx="18" fill="none" stroke="#1c140d" stroke-width="3"/>
<path d="M452 412 C440 440 410 470 380 520 H470 C478 480 488 448 498 412Z" fill="#2b2925"/>
<g transform="translate(700 300)"><path d="M0 130 C-2 80 2 40 6 0" stroke="#1b1712" stroke-width="7" fill="none"/>{"".join(f'<path d="M6 0 Q{dx * .55:.0f} {dy * .5 - 14:.0f} {dx} {dy}" stroke="#0f1810" stroke-width="5" fill="none" stroke-linecap="round"/>' for dx, dy in [(-58, 18), (-46, -24), (-6, -50), (40, -30), (60, 12), (-26, 34), (30, 36)])}</g>
<rect x="768" y="326" width="6" height="88" fill="#2a2724"/>
<rect x="676" y="400" width="74" height="6" rx="2" fill="#2f2c28"/><rect x="684" y="406" width="4" height="14" fill="#2f2c28"/><rect x="738" y="406" width="4" height="14" fill="#2f2c28"/>
<g class="lights glow">
<g class="lt lt-tree">{tree}</g>
<g class="lt lt-arch">{arch}</g>
<g class="lt lt-path">{path_l}</g>
<g class="lt lt-patio">{patio}</g>
<g class="lt lt-arch"><ellipse cx="440" cy="330" rx="16" ry="10" fill="url(#{p}-g)"/><rect x="436" y="322" width="8" height="12" rx="2" fill="currentColor" opacity=".9"/></g>
</g>
</svg>"""


# ---------- Texas map ----------

TX_BORDER = [
    (36.5, -103.04), (36.5, -100.0), (34.56, -100.0), (34.42, -99.6), (34.38, -99.2), (34.2, -98.6), (34.12, -98.1),
    (33.85, -97.6), (33.73, -97.15), (33.88, -96.6), (33.73, -96.2), (33.84, -95.75), (33.64, -95.2), (33.9, -94.6),
    (33.55, -94.04), (33.0, -94.04), (32.0, -94.04), (31.7, -93.83), (31.3, -93.55), (30.9, -93.56), (30.4, -93.73),
    (30.05, -93.7), (29.7, -93.84), (29.55, -94.45), (29.3, -94.8), (29.05, -95.1), (28.75, -95.6), (28.5, -96.3),
    (28.2, -96.75), (27.85, -97.05), (27.4, -97.3), (26.9, -97.4), (26.4, -97.25), (26.0, -97.15), (25.96, -97.45),
    (26.1, -97.9), (26.2, -98.3), (26.4, -98.8), (26.8, -99.15), (27.3, -99.5), (27.75, -99.6), (28.2, -100.25),
    (28.65, -100.5), (29.1, -100.8), (29.45, -101.25), (29.77, -101.7), (29.75, -102.3), (29.55, -102.7), (29.15, -103.0),
    (28.98, -103.3), (29.2, -103.75), (29.55, -104.3), (29.9, -104.6), (30.4, -104.85), (30.85, -105.0), (31.2, -105.55),
    (31.55, -106.05), (31.78, -106.53), (32.0, -106.62), (32.0, -103.06),
]
LON0, LAT0, K = -106.8, 36.7, 62.0
COSL = math.cos(math.radians(31.2))


def proj(lat, lon):
    return ((lon - LON0) * K * COSL, (LAT0 - lat) * K)


def texas_map(cities, label_side=None):
    label_side = label_side or {}
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in (proj(a, b) for a, b in TX_BORDER))
    xs = [proj(a, b)[0] for a, b in TX_BORDER]
    ys = [proj(a, b)[1] for a, b in TX_BORDER]
    w, h = max(xs) + 12, max(ys) + 12
    dots = []
    for c in cities:
        x, y = proj(c["lat"], c["lon"])
        side = label_side.get(c["slug"], "r")
        dx, anchor = (10, "start") if side == "r" else (-10, "end")
        dy = {"r": 4, "l": 4}.get(side, 4) + c.get("dy", 0)
        dots.append(
            f'<g class="dot" data-city="{c["slug"]}" data-href="/service-areas/{c["slug"]}/" tabindex="0" role="link" aria-label="Landscape lighting in {c["name"]}">'
            f'<circle class="p" cx="{x:.1f}" cy="{y:.1f}" r="5"/><circle class="c" cx="{x:.1f}" cy="{y:.1f}" r="5"/>'
            f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}">{c["short"]}</text></g>')
    return (f'<svg viewBox="-6 -6 {w:.0f} {h:.0f}" role="img" aria-label="Map of Texas showing the cities Texas Landscape Lights serves" xmlns="http://www.w3.org/2000/svg">'
            f'<polygon class="state-glow" points="{pts}"/><polygon class="state" points="{pts}"/>'
            f'<g>{"".join(dots)}</g></svg>')


def logo_svg(cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 48 48" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
            '<defs><radialGradient id="lg-g" cx="50%" cy="60%"><stop offset="0" stop-color="#ffd88a"/><stop offset="1" stop-color="#f4b13e" stop-opacity="0"/></radialGradient></defs>'
            '<rect width="48" height="48" rx="12" fill="#2f3338"/><circle cx="24" cy="27" r="19" fill="url(#lg-g)" opacity=".35"/>'
            '<path d="M24 9.5l3.9 8.6 9.4.9-7.1 6.2 2.1 9.2L24 29.6l-8.3 4.8 2.1-9.2-7.1-6.2 9.4-.9z" fill="#f4b13e"/>'
            '<path d="M15 41h18" stroke="#d0663d" stroke-width="3" stroke-linecap="round"/></svg>')
