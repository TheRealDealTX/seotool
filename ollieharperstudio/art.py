"""SVG artwork that stays vector on ollieharperstudio.com.

Page imagery is royalty-free photography (assets/photos/). What remains here is
the interactive coloring page, which has to be line art, the favicon and the
Lipstick Theory shade list.
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


# Lipstick Theory: one tube per personality shade.
SHADES = [
    ("Classic Red", "#c8102e"), ("Coral", "#ff6f61"), ("Berry", "#8e1b4f"), ("Nude", "#c99383"),
    ("Plum", "#5b1f4a"), ("Fuchsia", "#e0218a"), ("Brick", "#9c3b25"), ("Mauve", "#b0717f"),
]
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


ART = {"coloring-room": coloring_room()}

FAVICON = svg(64, 64, f'<rect width="64" height="64" rx="16" fill="{TOMATO}"/>'
              f'<circle cx="24" cy="32" r="12" fill="none" stroke="{CREAM}" stroke-width="6"/>'
              f'<path d="M40 18 V46 M52 18 V46 M40 32 H52" stroke="{CREAM}" stroke-width="6" stroke-linecap="round"/>',
              "Ollie Harper Studio")
