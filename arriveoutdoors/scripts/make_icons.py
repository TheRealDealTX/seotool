"""Render the logo mark to favicon.ico and PNG app icons (PIL only, supersampled)."""
import os
from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "assets", "icons")
NIGHT, MOSS, EMBER, WHITE = (7, 19, 15), (134, 168, 107), (255, 106, 43), (255, 255, 255)
# Logo paths from the SVG (viewBox 38x30)
MOUNTAIN = [(2, 28), (14, 6), (20, 16), (24, 10), (36, 28)]
FRONT = [(10, 28), (18, 19), (23, 24), (27, 21), (36, 28)]
SNOW = [[(14, 6), (17.4, 12.2), (15.2, 10.8), (12.8, 13.4), (11.2, 11.8)], [(24, 10), (26.6, 13.9), (25, 13.1), (23.4, 14.7), (22.2, 13.5)]]


def render(size, pad, radius, bg=NIGHT):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius), fill=bg)
    inner = S * (1 - 2 * pad)
    k = inner / 38
    ox = (S - 38 * k) / 2
    oy = (S - 30 * k) / 2 - S * 0.01
    t = lambda pts: [(ox + x * k, oy + y * k) for x, y in pts]
    d.polygon(t(MOUNTAIN), fill=MOSS)
    for s in SNOW:
        d.polygon(t(s), fill=WHITE)
    d.polygon(t(FRONT), fill=EMBER)
    return im.resize((size, size), Image.LANCZOS)


os.makedirs(OUT, exist_ok=True)
render(512, 0.12, 0.22).save(os.path.join(OUT, "icon-512.png"))
render(192, 0.12, 0.22).save(os.path.join(OUT, "icon-192.png"))
render(180, 0.12, 0.0).convert("RGB").save(os.path.join(OUT, "apple-touch-icon.png"))  # iOS rounds corners itself
render(512, 0.22, 0.0).save(os.path.join(OUT, "maskable-512.png"))                      # content inside the 80% safe zone
render(32, 0.06, 0.2).save(os.path.join(OUT, "favicon-32.png"))
ico = render(256, 0.06, 0.2)
ico.save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
print("icons written")
