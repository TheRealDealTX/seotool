"""Inline SVG artwork: the lit-house scene, page vignettes, post covers and the Texas map."""
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


# ---------- vignettes ----------

def _frame(p, inner, label, w=600, h=400, horizon=300, seed=3):
    rng = random.Random(seed)
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg" style="color:#ffd394">{_defs(p)}'
            f'<rect width="{w}" height="{h}" fill="url(#{p}-sky)"/>{_stars(rng, 40, w, h, horizon - 80)}'
            f'<rect y="{horizon}" width="{w}" height="{h - horizon}" fill="url(#{p}-lawn)"/>{inner}</svg>')


def _oak(x, y, s=1.0, fill="#0e1710"):
    blobs = [(-70, -150, 70, 44), (0, -180, 95, 58), (75, -150, 72, 44), (-30, -120, 90, 34), (50, -118, 70, 30)]
    c = "".join(f'<ellipse cx="{x + dx * s:.0f}" cy="{y + dy * s:.0f}" rx="{rx * s:.0f}" ry="{ry * s:.0f}" fill="{fill}"/>' for dx, dy, rx, ry in blobs)
    return f'<path d="M{x - 8 * s} {y} L{x - 4 * s} {y - 110 * s} L{x + 6 * s} {y - 110 * s} L{x + 10 * s} {y}Z" fill="#18130f"/>' + c


def _cone(p, x, y, top, spread=36, op=.75):
    return (f'<polygon points="{x - 4},{y} {x - spread},{top} {x + spread},{top} {x + 4},{y}" fill="url(#{p}-up)" opacity="{op}"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="14" ry="4" fill="url(#{p}-g)"/>')


def art(name, p=None):
    p = p or f"a-{name}"
    g = f"url(#{p}-g)"
    if name == "facade":
        inner = (f'<polygon points="90,200 300,110 510,200" fill="#17191c"/><rect x="110" y="198" width="380" height="104" fill="url(#{p}-stone)"/><rect x="110" y="198" width="380" height="104" fill="#000" opacity=".3"/>'
                 f'<rect x="270" y="236" width="60" height="66" rx="26" fill="#3b2a1d"/>' + "".join(f'<rect x="{x}" y="226" width="36" height="46" fill="#f6c66f" opacity=".85"/>' for x in (140, 200, 366, 426))
                 + '<g class="glow" style="mix-blend-mode:screen">' + "".join(_cone(p, x, 302, 150, 34) for x in (128, 250, 350, 472)) + f'<polygon points="296,302 262,120 338,120 304,302" fill="url(#{p}-up)" opacity=".8"/></g>')
        return _frame(p, inner, "Architectural uplighting on a stone facade", horizon=300)
    if name == "path":
        inner = '<path d="M250 400 C270 350 330 320 300 300 L330 300 C370 330 330 360 380 400Z" fill="#2b2925"/>'
        pts = [(286, 312, .6), (342, 312, .6), (268, 340, .8), (360, 342, .8), (246, 376, 1.1), (392, 378, 1.1)]
        inner += '<g style="mix-blend-mode:screen">' + "".join(
            f'<ellipse cx="{x}" cy="{y + 4}" rx="{44 * s:.0f}" ry="{11 * s:.0f}" fill="{g}"/><line x1="{x}" y1="{y}" x2="{x}" y2="{y - 26 * s:.0f}" stroke="#5a574f" stroke-width="{2 * s:.1f}"/><ellipse cx="{x}" cy="{y - 27 * s:.0f}" rx="{8 * s:.0f}" ry="{3 * s:.0f}" fill="#3a3833"/><ellipse cx="{x}" cy="{y - 24 * s:.0f}" rx="{6 * s:.0f}" ry="2.5" fill="currentColor"/>'
            for x, y, s in pts) + '</g>'
        inner += _oak(110, 300, .8) + _oak(500, 300, .7)
        return _frame(p, inner, "Path lights along a curving walkway", horizon=300)
    if name == "tree":
        inner = _oak(300, 330, 1.45) + '<g style="mix-blend-mode:screen">' + "".join(_cone(p, x, 332, 90, 52, .7) for x in (250, 300, 352)) + f'<ellipse cx="300" cy="120" rx="150" ry="70" fill="{g}" opacity=".45"/></g>'
        return _frame(p, inner, "Uplit live oak tree at night", horizon=330)
    if name == "patio":
        bul, seg = [], []
        for i in range(14):
            t = i / 13
            x, y = 60 + 480 * t, 120 + math.sin(math.pi * t) * 46
            seg.append(f"{x:.0f},{y:.0f}")
            bul.append(f'<circle cx="{x:.0f}" cy="{y + 5:.0f}" r="12" fill="{g}"/><circle cx="{x:.0f}" cy="{y + 5:.0f}" r="3" fill="currentColor"/>')
        inner = (f'<rect x="56" y="110" width="8" height="200" fill="#2a2724"/><rect x="536" y="110" width="8" height="200" fill="#2a2724"/><rect x="40" y="290" width="520" height="16" fill="#2f2d29"/>'
                 f'<rect x="200" y="250" width="200" height="10" rx="3" fill="#3a352f"/><rect x="215" y="260" width="6" height="34" fill="#3a352f"/><rect x="380" y="260" width="6" height="34" fill="#3a352f"/>'
                 f'<polyline points="{" ".join(seg)}" fill="none" stroke="#5d584f" stroke-width="1.4"/><g style="mix-blend-mode:screen">{"".join(bul)}<ellipse cx="300" cy="300" rx="240" ry="30" fill="{g}" opacity=".5"/></g>')
        return _frame(p, inner, "Patio with bistro string lights", horizon=300)
    if name == "pool":
        inner = (f'<defs><linearGradient id="{p}-w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2fc0d8"/><stop offset="1" stop-color="#0c5a7a"/></linearGradient></defs>'
                 f'<rect x="90" y="300" width="420" height="80" rx="6" fill="#1d2a2c"/><rect x="104" y="308" width="392" height="64" rx="4" fill="url(#{p}-w)"/>'
                 '<path d="M110 330 q20 -6 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0" stroke="#bff3ff" stroke-opacity=".4" fill="none"/>'
                 '<g transform="translate(470 300)"><path d="M0 0 C-4 -60 4 -120 10 -170" stroke="#1b1712" stroke-width="8" fill="none"/>'
                 + "".join(f'<path d="M10 -170 Q{dx * .5:.0f} {dy * .5 - 190:.0f} {dx} {dy - 170}" stroke="#0f1810" stroke-width="6" fill="none" stroke-linecap="round"/>' for dx, dy in [(-70, 20), (-50, -30), (0, -55), (50, -30), (70, 22), (-30, 40), (34, 40)])
                 + f'</g><g style="mix-blend-mode:screen">{_cone(p, 470, 300, 110, 46)}<ellipse cx="300" cy="340" rx="230" ry="40" fill="#5fe0f2" opacity=".18"/></g>')
        return _frame(p, inner, "Pool and palm lit at night", horizon=300)
    if name == "controls":
        inner = (f'<g transform="translate(330 60)"><rect width="170" height="300" rx="26" fill="#14161a" stroke="#3a3f45" stroke-width="3"/><rect x="12" y="34" width="146" height="230" rx="10" fill="#1f2226"/>'
                 '<text x="85" y="62" text-anchor="middle" fill="#f4b13e" font-family="sans-serif" font-size="13" font-weight="700">ZONES</text>'
                 + "".join(f'<text x="24" y="{96 + i * 44}" fill="#d9d7d2" font-family="sans-serif" font-size="12">{z}</text><rect x="24" y="{104 + i * 44}" width="120" height="6" rx="3" fill="#3a3f45"/><rect x="24" y="{104 + i * 44}" width="{v}" height="6" rx="3" fill="#f4b13e"/><circle cx="{24 + v}" cy="{107 + i * 44}" r="7" fill="#fff"/>' for i, (z, v) in enumerate([("Facade", 96), ("Trees", 80), ("Paths", 60), ("Patio", 104)]))
                 + '<text x="85" y="250" text-anchor="middle" fill="#9db394" font-family="sans-serif" font-size="11">ON AT SUNSET</text></g>'
                 f'<polygon points="40,240 150,180 260,240" fill="#17191c"/><rect x="56" y="238" width="188" height="64" fill="url(#{p}-stone)"/><g style="mix-blend-mode:screen">{_cone(p, 90, 302, 190, 28)}{_cone(p, 210, 302, 190, 28)}</g>')
        return _frame(p, inner, "Smart lighting app controlling zones", horizon=300)
    if name == "repair":
        inner = (f'<rect x="80" y="150" width="120" height="150" rx="10" fill="#2b2e33" stroke="#4a4f56" stroke-width="2"/><rect x="96" y="170" width="88" height="20" rx="3" fill="#15171a"/><text x="140" y="185" text-anchor="middle" fill="#9db394" font-family="monospace" font-size="12">12.6V</text>'
                 '<circle cx="118" cy="230" r="12" fill="#1b1d20" stroke="#f4b13e"/><circle cx="162" cy="230" r="12" fill="#1b1d20" stroke="#f4b13e"/>'
                 '<path d="M200 280 C260 300 300 330 360 320 S460 300 500 330" stroke="#111" stroke-width="7" fill="none"/><path d="M200 280 C260 300 300 330 360 320 S460 300 500 330" stroke="#3b3b3b" stroke-width="3" fill="none"/>'
                 '<g transform="translate(500 330) rotate(-12)"><rect x="-6" y="-60" width="12" height="60" fill="#5a574f"/><path d="M-26 -60 h52 l-10 -16 h-32z" fill="#3a3833"/></g>'
                 f'<g style="mix-blend-mode:screen"><ellipse cx="488" cy="276" rx="60" ry="18" fill="{g}"/><circle cx="330" cy="326" r="26" fill="#f4b13e" opacity=".25"/></g>'
                 '<g transform="translate(330 326)"><rect x="-14" y="-9" width="28" height="18" rx="5" fill="#f4b13e"/></g>')
        return _frame(p, inner, "Transformer, wire splice and path light being repaired", horizon=300)
    if name == "commercial":
        inner = (f'<rect x="150" y="200" width="300" height="100" fill="url(#{p}-stone)"/><rect x="130" y="290" width="340" height="14" fill="#262420"/>'
                 '<text x="300" y="262" text-anchor="middle" fill="#e9e1cf" font-family="Barlow Condensed, sans-serif" font-size="40" font-weight="800" letter-spacing="6">WELCOME</text>'
                 '<path d="M300 205 l7 14 15 1-11 10 4 15-15-8-15 8 4-15-11-10 15-1z" fill="#d0663d" transform="translate(0 -8) scale(1) "/>'
                 f'<g style="mix-blend-mode:screen"><polygon points="190,300 150,190 260,190 200,300" fill="url(#{p}-up)" opacity=".7"/><polygon points="410,300 340,190 450,190 400,300" fill="url(#{p}-up)" opacity=".7"/></g>'
                 + _oak(70, 300, .7) + _oak(530, 300, .7))
        return _frame(p, inner, "Lit monument sign at a neighborhood entrance", horizon=300)
    # city
    rng = random.Random(11)
    bldg = []
    x = 0
    while x < 600:
        w_, h_ = rng.randint(26, 60), rng.randint(60, 190)
        bldg.append(f'<rect x="{x}" y="{240 - h_}" width="{w_}" height="{h_}" fill="#151a22"/>')
        for wy in range(240 - h_ + 10, 232, 14):
            for wx in range(x + 5, x + w_ - 6, 10):
                if rng.random() < .28:
                    bldg.append(f'<rect x="{wx}" y="{wy}" width="4" height="6" fill="#f6c66f" opacity="{rng.uniform(.4, .9):.2f}"/>')
        x += w_ + rng.randint(2, 8)
    houses = "".join(
        f'<polygon points="{hx - 50},262 {hx},228 {hx + 50},262" fill="#17191c"/><rect x="{hx - 42}" y="260" width="84" height="40" fill="url(#{p}-stone)"/><rect x="{hx - 10}" y="272" width="20" height="28" fill="#3b2a1d"/>'
        f'<g style="mix-blend-mode:screen">{_cone(p, hx - 30, 300, 236, 16, .8)}{_cone(p, hx + 30, 300, 236, 16, .8)}</g>'
        for hx in (90, 300, 510))
    return _frame(p, f'<g opacity=".9">{"".join(bldg)}</g><rect y="240" width="600" height="60" fill="#0d1219"/>{houses}', "Texas city skyline with lit homes in front", horizon=300)


POST_ART = {
    "landscape-lighting-cost-texas": "facade", "best-landscape-lighting-for-texas-heat": "repair",
    "landscape-lighting-techniques": "tree", "warm-white-vs-cool-white-landscape-lighting": "patio",
    "path-light-spacing": "path", "tree-uplighting-guide": "tree",
    "landscape-lighting-transformer-sizing": "repair", "halogen-to-led-landscape-lighting": "controls",
    "protecting-landscape-lighting-from-texas-storms": "pool", "landscape-lighting-for-home-security": "facade",
    "landscape-lighting-maintenance-checklist": "path", "how-much-electricity-does-landscape-lighting-use": "controls",
}


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
