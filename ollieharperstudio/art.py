"""Original SVG artwork for ollieharperstudio.com.

Every illustration on the site is drawn here as flat vector shapes, so the
build has no stock photography and no third-party image licensing. build.py
writes each entry of ART to assets/img/<name>.svg.
"""

INK = "#1d1a24"
CREAM = "#f6efe6"
TOMATO = "#ef5b3c"
BLUSH = "#f4a7b9"
MUSTARD = "#f2b134"
SAGE = "#8fb39a"
COBALT = "#3550d6"
PLUM = "#6b2d5c"


def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}">{body}</svg>\n')


def leaf(x, y, r, rot, fill):
    return (f'<g transform="translate({x} {y}) rotate({rot})">'
            f'<path d="M0 0 C {r*.45} {-r*.35} {r*.75} {-r*.2} {r} 0 C {r*.75} {r*.2} {r*.45} {r*.35} 0 0Z" fill="{fill}"/>'
            f'<path d="M0 0 L {r*.9} 0" stroke="{INK}" stroke-width="2" opacity=".35"/></g>')


def cup(x, y, s, body, sleeve):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-50 -60 L50 -60 L40 70 Q0 82 -40 70Z" fill="{body}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="-56" y="-78" width="112" height="22" rx="8" fill="{INK}"/>'
            f'<path d="M-46 -10 L46 -10 L42 34 L-42 34Z" fill="{sleeve}" stroke="{INK}" stroke-width="4"/>'
            f'<path class="steam" d="M-14 -96 q-12 -18 0 -34 q12 -16 0 -32" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            f'<path class="steam" d="M16 -96 q-12 -18 0 -34 q12 -16 0 -32" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>'
            '</g>')


def lipstick(x, y, s, shade, case=INK, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<path d="M-18 -70 L18 -86 L18 -30 L-18 -30Z" fill="{shade}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="-24" y="-32" width="48" height="34" rx="4" fill="{MUSTARD}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="-30" y="0" width="60" height="92" rx="6" fill="{case}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="-20" y="12" width="8" height="66" rx="4" fill="#fff" opacity=".25"/></g>')


def lemon(x, y, s):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<ellipse rx="62" ry="46" fill="{MUSTARD}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M58 -8 q16 8 4 18" fill="{MUSTARD}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="-22" cy="-14" r="5" fill="#fff" opacity=".6"/>{leaf(-50, -36, 46, -140, SAGE)}</g>')


def croissant(x, y, s):
    segs = ''.join(
        f'<path d="M{a} 0 q{12} -48 {34} 0 q-17 18 -34 0Z" fill="#e9a35b" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        for a in (-68, -34, 0, 34))
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-96 8 Q0 -70 96 8 Q60 36 0 30 Q-60 36 -96 8Z" fill="#f0b46d" stroke="{INK}" stroke-width="4"/>{segs}</g>')


def pizza(x, y, s):
    dots = ''.join(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{TOMATO}" stroke="{INK}" stroke-width="3"/>'
                   for cx, cy in ((-20, -40), (14, -6), (-6, 30), (28, -52)))
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-60 -86 Q0 -110 60 -86 L0 90Z" fill="{MUSTARD}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-64 -88 Q0 -116 64 -88 L58 -74 Q0 -96 -58 -74Z" fill="#d9893d" stroke="{INK}" stroke-width="4"/>{dots}</g>')


def sunglasses(x, y, s, lens=COBALT):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-96 -20 L-10 -20 Q-14 34 -54 34 Q-94 34 -96 -20Z" fill="{lens}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M96 -20 L10 -20 Q14 34 54 34 Q94 34 96 -20Z" fill="{lens}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-10 -14 Q0 -24 10 -14" fill="none" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M-80 -8 L-64 -8 M60 -8 L76 -8" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"/></g>')


def heel(x, y, s, color=TOMATO):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-80 30 Q-84 -10 -60 -10 Q-20 -10 20 30 L70 30 Q86 30 84 46 L-70 46 Q-82 46 -80 30Z" fill="{color}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-74 46 L-70 96 L-58 96 L-56 46Z" fill="{INK}"/></g>')


def plant(x, y, s):
    leaves = ''.join(leaf(0, -60, 70 + (i % 2) * 18, -160 + i * 28, SAGE if i % 2 else "#5e8f6d") for i in range(6))
    return (f'<g transform="translate({x} {y}) scale({s})">{leaves}'
            f'<path d="M-46 -60 L46 -60 L36 40 L-36 40Z" fill="{TOMATO}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="-52" y="-72" width="104" height="16" rx="6" fill="{INK}"/></g>')


def chair(x, y, s, color=MUSTARD):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-70 -110 Q0 -150 70 -110 L64 10 L-64 10Z" fill="{color}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="-84" y="0" width="168" height="34" rx="14" fill="{color}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M-66 34 L-76 100 M66 34 L76 100" stroke="{INK}" stroke-width="7" stroke-linecap="round"/></g>')


def lamp(x, y, s):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-50 -40 L50 -40 L30 -110 L-30 -110Z" fill="{BLUSH}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M0 -40 L0 80" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="84" rx="40" ry="10" fill="{INK}"/></g>')


def pencil(x, y, s, rot, color=COBALT):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<rect x="-100" y="-12" width="160" height="24" fill="{color}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M60 -12 L100 0 L60 12Z" fill="#f3d3a4" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M88 -4 L100 0 L88 4Z" fill="{INK}"/>'
            f'<rect x="-118" y="-12" width="20" height="24" rx="4" fill="{BLUSH}" stroke="{INK}" stroke-width="4"/></g>')


def blob(x, y, r, fill, cls="blob"):
    return (f'<path class="{cls}" transform="translate({x} {y}) scale({r/100})" '
            f'd="M70 -20 C88 30 50 86 -6 88 C-62 90 -98 46 -92 -6 C-86 -60 -40 -96 8 -92 C52 -88 58 -54 70 -20Z" fill="{fill}"/>')


def sparkle(x, y, s, fill=INK):
    return (f'<path class="twinkle" transform="translate({x} {y}) scale({s})" '
            f'd="M0 -20 Q3 -3 20 0 Q3 3 0 20 Q-3 3 -20 0 Q-3 -3 0 -20Z" fill="{fill}"/>')


HERO = svg(640, 560, (
    blob(330, 290, 230, BLUSH) + blob(470, 150, 110, MUSTARD, "blob blob-b") + blob(150, 430, 90, SAGE, "blob blob-c")
    + f'<g class="float-a">{cup(220, 270, 1.25, CREAM, TOMATO)}</g>'
    + f'<g class="float-b">{lipstick(460, 330, 1.05, TOMATO, INK, 14)}</g>'
    + f'<g class="float-c">{lemon(470, 120, .95)}</g>'
    + f'<g class="float-b">{croissant(250, 470, .95)}</g>'
    + f'<g class="float-a">{pencil(500, 480, .9, -30)}</g>'
    + leaf(80, 170, 110, -30, SAGE) + leaf(70, 210, 90, -70, "#5e8f6d")
    + sparkle(110, 80, 1.2) + sparkle(590, 270, .9) + sparkle(380, 60, .7, TOMATO)
), "Illustrated still life: a coffee cup, a red lipstick, a lemon, a croissant and a pencil")

CULINARY = svg(640, 480, (
    blob(320, 240, 210, "#ffe1c4") + blob(520, 120, 80, SAGE, "blob blob-b")
    + f'<g class="float-a">{pizza(170, 230, 1.1)}</g>' + f'<g class="float-b">{cup(340, 260, 1, "#fff", COBALT)}</g>'
    + f'<g class="float-c">{lemon(500, 330, .9)}</g>' + f'<g class="float-a">{croissant(470, 140, .8)}</g>'
    + sparkle(80, 80, 1) + sparkle(600, 420, .8, TOMATO)
), "Illustrated food spread: a pizza slice, a latte, a lemon and a croissant")

FASHION = svg(640, 480, (
    blob(320, 250, 210, "#ffd9e2") + blob(120, 120, 70, MUSTARD, "blob blob-b")
    + f'<g class="float-a">{sunglasses(330, 130, 1.1, TOMATO)}</g>'
    + f'<g class="float-b">{heel(210, 300, 1.25, COBALT)}</g>'
    + f'<g class="float-c">{lipstick(470, 300, 1, PLUM, INK, -12)}</g>'
    + sparkle(560, 90, 1) + sparkle(90, 400, .8, TOMATO)
), "Illustrated fashion accessories: sunglasses, a heeled shoe and a lipstick")

STYLING = svg(640, 480, (
    blob(320, 260, 220, "#dfeee2") + blob(520, 110, 80, BLUSH, "blob blob-b")
    + f'<g class="float-a">{chair(300, 300, 1.05, MUSTARD)}</g>'
    + f'<g class="float-b">{plant(500, 330, .95)}</g>'
    + f'<g class="float-c">{lamp(120, 300, 1)}</g>'
    + sparkle(560, 60, 1) + sparkle(80, 80, .8, TOMATO)
), "Illustrated set: a mustard armchair, a potted plant and a pink lamp")

PROJECTS = svg(640, 480, (
    blob(320, 240, 220, "#e3e7ff") + blob(110, 380, 70, MUSTARD, "blob blob-b")
    + f'<g class="float-a"><rect x="150" y="90" width="300" height="220" rx="18" fill="#fff" stroke="{INK}" stroke-width="5"/>'
    + f'<rect x="176" y="118" width="120" height="90" rx="10" fill="{BLUSH}"/><rect x="310" y="118" width="114" height="14" rx="7" fill="{INK}"/>'
    + f'<rect x="310" y="144" width="90" height="10" rx="5" fill="{INK}" opacity=".4"/><rect x="176" y="226" width="248" height="60" rx="10" fill="{SAGE}"/></g>'
    + f'<g class="float-b">{pencil(430, 370, 1, -20, TOMATO)}</g>' + f'<g class="float-c">{cup(520, 220, .7, CREAM, MUSTARD)}</g>'
    + sparkle(100, 100, 1) + sparkle(570, 420, .8, COBALT)
), "Illustrated design desk: a project board, a pencil and a coffee")

THOUGHTS = svg(640, 480, (
    blob(320, 240, 220, "#fff0c9") + blob(520, 380, 80, BLUSH, "blob blob-b")
    + f'<g class="float-a"><path d="M150 120 L320 100 L320 380 L150 400Z" fill="#fff" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    + f'<path d="M320 100 L490 120 L490 400 L320 380Z" fill="#fff" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    + ''.join(f'<path d="M180 {160+i*36} L292 {148+i*36}" stroke="{INK}" stroke-width="4" opacity=".35" stroke-linecap="round"/>' for i in range(6))
    + f'<circle cx="405" cy="200" r="46" fill="{TOMATO}"/>{leaf(370, 300, 80, -10, SAGE)}</g>'
    + f'<g class="float-b">{pencil(470, 420, .9, -35)}</g>' + sparkle(100, 90, 1) + sparkle(560, 80, .8, COBALT)
), "Illustrated open sketchbook with a drawn sun, a leaf and a pencil")

CONTACT = svg(640, 420, (
    blob(320, 210, 200, "#ffe1c4") + blob(530, 100, 70, SAGE, "blob blob-b")
    + f'<g class="float-a"><rect x="170" y="110" width="300" height="200" rx="14" fill="#fff" stroke="{INK}" stroke-width="5"/>'
    + f'<path d="M170 124 L320 230 L470 124" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    + f'<circle cx="430" cy="150" r="22" fill="{TOMATO}" stroke="{INK}" stroke-width="4"/></g>'
    + f'<g class="float-b">{lipstick(120, 290, .7, BLUSH, INK, -20)}</g>' + sparkle(560, 330, 1) + sparkle(90, 80, .8, COBALT)
), "Illustrated envelope with a red seal")

# Lipstick Theory: one tube per personality shade.
SHADES = [
    ("Classic Red", "#c8102e"), ("Coral", "#ff6f61"), ("Berry", "#8e1b4f"), ("Nude", "#c99383"),
    ("Plum", "#5b1f4a"), ("Fuchsia", "#e0218a"), ("Brick", "#9c3b25"), ("Mauve", "#b0717f"),
]
LIPSTICKS = svg(720, 260, ''.join(
    f'<g class="float-{"abc"[i % 3]}">{lipstick(60 + i * 86, 130, .95, c, INK, (-1) ** i * 6)}</g>'
    for i, (_, c) in enumerate(SHADES)), "Eight illustrated lipstick tubes in red, coral, berry, nude, plum, fuchsia, brick and mauve")


def neighborhood_map():
    blocks = []
    for r in range(4):
        for c in range(5):
            fill = [CREAM, "#ffe1c4", "#dfeee2", "#ffd9e2"][(r + c) % 4]
            blocks.append(f'<rect x="{40 + c*124}" y="{40 + r*100}" width="104" height="80" rx="10" fill="{fill}" stroke="{INK}" stroke-width="3"/>')
    pins = ''.join(
        f'<g class="pin" style="--d:{i*.15}s" transform="translate({x} {y})"><path d="M0 0 C-18 -22 -18 -46 0 -46 C18 -46 18 -22 0 0Z" fill="{col}" stroke="{INK}" stroke-width="3"/>'
        f'<circle cy="-30" r="6" fill="#fff"/></g>'
        for i, (x, y, col) in enumerate(((150, 110, TOMATO), (290, 210, MUSTARD), (420, 120, COBALT), (520, 300, TOMATO),
                                          (170, 330, SAGE), (380, 400, PLUM), (600, 160, MUSTARD), (260, 420, COBALT))))
    return svg(680, 480, '<rect width="680" height="480" rx="24" fill="#fff"/>' + ''.join(blocks) + pins,
               "Illustrated neighborhood map with eight colorful pins marking places to eat")


# Coloring page: every region carries data-fill so the page script can paint it.
def coloring_room():
    def r(d, extra=""):
        return f'<path class="cz" d="{d}" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round" {extra}/>'
    parts = [
        r("M0 0 H720 V330 H0Z"),                                   # wall
        r("M0 330 H720 V480 H0Z"),                                 # floor
        r("M60 60 H260 V250 H60Z"),                                # window
        r("M66 66 H156 V150 H66Z"), r("M164 66 H254 V150 H164Z"),
        r("M66 158 H156 V244 H66Z"), r("M164 158 H254 V244 H164Z"),
        r("M40 60 Q30 160 50 300 L70 300 Q56 160 60 60Z"),          # curtain L
        r("M280 60 Q290 160 270 300 L250 300 Q264 160 260 60Z"),    # curtain R
        r("M330 210 Q470 160 610 210 L600 330 L340 330Z"),          # sofa back
        r("M310 300 H630 V360 H310Z"),                              # seat
        r("M300 250 Q290 250 290 270 V370 H330 V260Z"),             # arm L
        r("M640 250 Q650 250 650 270 V370 H610 V260Z"),             # arm R
        r("M380 230 Q420 214 450 236 L440 290 Q408 294 384 286Z"),  # cushion
        r("M490 236 Q520 214 560 230 L556 286 Q532 294 500 290Z"),  # cushion
        r("M180 420 m-110 0 a110 34 0 1 0 220 0 a110 34 0 1 0 -220 0"),  # rug
        r("M150 418 m-60 0 a60 18 0 1 0 120 0 a60 18 0 1 0 -120 0"),     # rug inner
        r("M670 330 L700 330 L690 410 L680 410Z"),                  # vase
        r("M660 220 Q690 150 720 220 Q690 250 660 220Z"),           # leaf
        r("M645 260 Q610 200 650 170 Q670 230 645 260Z"),
        r("M520 60 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0"),          # wall clock / art
        r("M360 60 H470 V150 H360Z"), r("M374 74 H456 V136 H374Z"),  # frame
        r("M460 400 H580 V420 H460Z"), r("M470 420 H482 V470 H470Z"), r("M558 420 H570 V470 H558Z"),  # coffee table
    ]
    return svg(720, 480, ''.join(parts) +
               f'<path d="M560 60 L560 40 M560 60 L580 66" stroke="{INK}" stroke-width="3" stroke-linecap="round" pointer-events="none"/>',
               "Line-art living room to color in: a window with curtains, a sofa with cushions, a rug, a plant, framed art and a coffee table")


ART = {
    "hero": HERO, "culinary": CULINARY, "fashion": FASHION, "styling": STYLING,
    "projects": PROJECTS, "thoughts": THOUGHTS, "contact": CONTACT,
    "lipsticks": LIPSTICKS, "map": neighborhood_map(), "coloring-room": coloring_room(),
}

# Small single-object tiles used in gallery grids: (file, label, svg body).
TILES = {
    "tile-latte": ("A latte with a cobalt sleeve", cup(100, 120, .8, "#fff", COBALT)),
    "tile-pizza": ("A pizza slice", pizza(100, 110, .8)),
    "tile-lemon": ("A lemon with a leaf", lemon(100, 100, 1)),
    "tile-croissant": ("A croissant", croissant(100, 100, .85)),
    "tile-sunglasses": ("Tomato-red sunglasses", sunglasses(100, 100, .85, TOMATO)),
    "tile-heel": ("A cobalt heeled shoe", heel(110, 90, .9, COBALT)),
    "tile-lipstick": ("A plum lipstick", lipstick(100, 105, .85, PLUM)),
    "tile-chair": ("A mustard armchair", chair(100, 120, .7)),
    "tile-plant": ("A potted plant", plant(100, 140, .7)),
    "tile-lamp": ("A pink lamp", lamp(100, 110, .9)),
    "tile-pencil": ("A blue pencil", pencil(100, 100, .8, -35)),
}
for name, (label, body) in TILES.items():
    ART[name] = svg(200, 200, body, label)

FAVICON = svg(64, 64, f'<rect width="64" height="64" rx="16" fill="{TOMATO}"/>'
              f'<circle cx="24" cy="32" r="12" fill="none" stroke="{CREAM}" stroke-width="6"/>'
              f'<path d="M40 18 V46 M52 18 V46 M40 32 H52" stroke="{CREAM}" stroke-width="6" stroke-linecap="round"/>',
              "Ollie Harper Studio")
