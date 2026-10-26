"""Generate branded featured images for posts whose 'image' lives in /assets/img/posts/.
Run from anywhere: python3 scripts/post_images.py (needs Pillow + php). Re-renders all of them."""
import sys, textwrap, re
sys.path.insert(0, '')
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import subprocess, json
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
U = ROOT + '/wp-content/uploads/2026/01/'
posts = json.loads(subprocess.check_output(['php', '-r', 'define("BO",1); putenv("BO_SHOW_SCHEDULED=1"); require "inc/config.php"; echo json_encode($POSTS);'], cwd=ROOT))
bgs = [U+'Better-Outdoors-BG.webp', U+'Better-Outdoors-BG-1.webp', U+'Better-Outdoors-Site-Image.webp']
icons = {'Bow Tuning': 'TUNING', 'Bow Guides': 'GUIDE', 'Bow Reviews': 'REVIEW', 'Hunting Tips': 'HUNTING', 'Outdoor Tips': 'OUTDOORS'}
H = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', 64)
S = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
logo = Image.open(U + 'Better-Outdoors-Logo-White.webp').convert('RGBA'); logo = logo.resize((300, int(300 * logo.height / logo.width)))
i = 0
for slug, p in posts.items():
    if not p['image'].startswith('/assets/img/posts/'): continue
    src = Image.open(bgs[i % 2]).convert('RGB')
    if (i // 2) % 2: src = src.transpose(Image.FLIP_LEFT_RIGHT)
    W, Hh = 1200, 800
    # varied crop per post
    sc = max(W / src.width, Hh / src.height) * (1.15 + 0.1 * (i % 3))
    src = src.resize((int(src.width * sc), int(src.height * sc)))
    ox = int((src.width - W) * ((i * 37) % 100) / 100); oy = int((src.height - Hh) * ((i * 53) % 100) / 100)
    im = src.crop((ox, oy, ox + W, oy + Hh)).filter(ImageFilter.GaussianBlur(1.5))
    im = ImageEnhance.Brightness(im).enhance(0.75)
    ov = Image.new('RGBA', (W, Hh)); d = ImageDraw.Draw(ov)
    for x in range(W):  # left-to-right navy gradient
        a = int(235 - 170 * x / W); d.line([(x, 0), (x, Hh)], fill=(6, 30, 41, a))
    im = Image.alpha_composite(im.convert('RGBA'), ov)
    d = ImageDraw.Draw(im)
    # target rings on the right
    cx, cy, R = [1010, 1040, 1000][i % 3], [400, 360, 440][i % 3], [190, 210, 175][i % 3]
    cols = [(232, 238, 240, 230), (6, 30, 41, 235), (6, 30, 41, 235), (29, 84, 109, 240), (29, 84, 109, 240), (255, 105, 48, 245), (255, 105, 48, 245)]
    for k, c in enumerate(cols):
        r = R * (1 - k / len(cols)); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c, outline=(255, 255, 255, 200), width=3)
    # arrow stuck in target
    d.line([(cx - 10, cy + 8), (cx + 260, cy - 150)], fill=(40, 40, 40, 255), width=7)
    d.polygon([(cx + 230, cy - 150), (cx + 280, cy - 170), (cx + 262, cy - 125)], fill=(255, 105, 48, 255))
    # chip
    chip = icons.get(p['cat'], 'GUIDE'); tw = d.textlength(chip, font=S)
    d.rounded_rectangle([70, 90, 70 + tw + 40, 136], radius=23, fill=(255, 105, 48, 255)); d.text((90, 99), chip, font=S, fill='white')
    # title
    for size in (64, 58, 52, 46):
        F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', size)
        words, lines, cur = p['h1'].split(), [], ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=F) <= 640: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) <= 4: break
    y = 170
    for ln in lines:
        d.text((70, y), ln, font=F, fill='white'); y += int(size * 1.25)
    d.rectangle([70, y + 18, 150, y + 24], fill=(255, 105, 48, 255))
    im.alpha_composite(logo, (70, Hh - logo.height - 60))
    out = ROOT + p['image']; im.convert('RGB').save(out, 'WEBP', quality=82)
    im.convert('RGB').resize((768, 512), Image.LANCZOS).save(ROOT + p['thumb'], 'WEBP', quality=80)
    i += 1
    print(slug)
