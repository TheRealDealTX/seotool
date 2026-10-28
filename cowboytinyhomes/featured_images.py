import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
S, IMG = sys.argv[1], sys.argv[2]
F = S + '/fonts/'
INK, INK3, GOLD, GOLD2, CREAM = (40,42,57), (29,31,43), (198,151,73), (224,182,99), (230,230,238)
posts = [
  ('blog-western-tiny-homes.webp', 'Park-Model-Homes.webp', 'DESIGN & STYLE', 'Western Tiny Homes: Texas Ranch Style, Built Small'),
  ('blog-backyard-casita-ideas.webp', 'Accessory-Dwelling-Units.webp', 'ADUs & CASITAS', '9 Backyard Casita Ideas Texans Love'),
  ('blog-gooseneck-vs-bumper-pull.webp', 'Tiny-Homes-On-Wheels.webp', 'TINY HOMES ON WHEELS', 'Gooseneck vs Bumper Pull: Which Tiny House Trailer?'),
  ('blog-tiny-home-texas-heat.webp', '3.webp', 'BUILDING SMART', 'Designing a Tiny Home for Texas Heat'),
  ('blog-tiny-house-communities-texas.webp', 'Custom-Tiny-Homes.webp', 'TINY LIVING', 'Tiny House Communities in Texas: What to Know'),
]
W, H = 1200, 675
bp = Image.open(IMG + '/Cowboy-Tiny-Homes-Home-BG.webp').convert('L').resize((W, int(W*1357/1920)))
logo = Image.open(IMG + '/Cowboy-Tiny-Homes-Footer-Image.webp').convert('RGBA')
def wrap(d, text, font, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines
for out, photo, kicker, title in posts:
    im = Image.new('RGB', (W, H), INK3)
    tex = ImageEnhance.Brightness(bp.crop((0, 0, W, H)).convert('RGB')).enhance(0.18)
    im = Image.blend(im, tex, 0.5)
    d = ImageDraw.Draw(im)
    # right-hand photo, rounded, with gold rule
    ph = Image.open(IMG + '/' + photo).convert('RGB')
    pw, phh = 560, 560
    r = max(pw/ph.width, phh/ph.height); ph = ph.resize((int(ph.width*r)+1, int(ph.height*r)+1), Image.LANCZOS)
    ph = ph.crop(((ph.width-pw)//2, (ph.height-phh)//2, (ph.width-pw)//2+pw, (ph.height-phh)//2+phh))
    mask = Image.new('L', (pw, phh), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, phh), 28, fill=255)
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle((598, 70, 598+pw, 70+phh), 28, fill=150)
    im.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
    im.paste(ph, (590, 58), mask)
    d.rounded_rectangle((590, 58+phh-8, 590+pw, 58+phh+4), 4, fill=GOLD)
    # text
    fk = ImageFont.truetype(F + 'M-600.ttf', 22); ft = ImageFont.truetype(F + 'M-800.ttf', 54)
    d.rectangle((64, 160, 92, 165), fill=GOLD2); d.text((104, 148), kicker, font=fk, fill=GOLD2)
    y = 196
    for ln in wrap(d, title, ft, 480):
        d.text((64, y), ln, font=ft, fill=(255, 255, 255)); y += 66
    d.rectangle((64, y + 18, 148, y + 23), fill=GOLD)
    lg = logo.copy(); lg.thumbnail((230, 80)); im.paste(lg, (52, H - 118), lg)
    im.save(IMG + '/' + out, 'WEBP', quality=86)
    print(out, im.size)
