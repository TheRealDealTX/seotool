"""Generate the favicon set (site root) from the logo's diamond mark. Run once; output is committed in public/."""

from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / "public"
INK, COPPER, PAPER = (25, 21, 18, 255), (172, 95, 64, 255), (250, 247, 242, 255)
INNER = 0.64  # copper diamond as a share of the dark diamond (measured from the original icon)


def mark(size, fill=0.96, bg=None):
    s = size * 8  # supersample, then downscale for clean edges
    im = Image.new("RGBA", (s, s), bg or (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c, r = s / 2, s / 2 * fill
    d.polygon([(c, c - r), (c + r, c), (c, c + r), (c - r, c)], fill=INK)
    ri = r * INNER
    d.polygon([(c, c - ri), (c + ri, c), (c, c + ri), (c - ri, c)], fill=COPPER)
    return im.resize((size, size), Image.LANCZOS)


def main():
    mark(48).save(OUT / "favicon-48x48.png")
    mark(96).save(OUT / "favicon-96x96.png")
    mark(256).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    mark(180, fill=0.78, bg=PAPER).convert("RGB").save(OUT / "apple-touch-icon.png")
    for n in (192, 512):
        mark(n, fill=0.7, bg=PAPER).convert("RGB").save(OUT / f"web-app-manifest-{n}x{n}.png")
    r, ri = 48, 48 * INNER
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        f'<path fill="#191512" d="M50 {50 - r}L{50 + r} 50 50 {50 + r} {50 - r} 50z"/>'
        f'<path fill="#ac5f40" d="M50 {50 - ri:.2f}L{50 + ri:.2f} 50 50 {50 + ri:.2f} {50 - ri:.2f} 50z"/></svg>\n')
    (OUT / "site.webmanifest").write_text("""{
  "name": "Stone Coated Roofs",
  "short_name": "Stone Coated Roofs",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#faf7f2",
  "theme_color": "#12100e",
  "icons": [
    {"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
    {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
  ]
}
""")
    print("icons written")


if __name__ == "__main__":
    main()
