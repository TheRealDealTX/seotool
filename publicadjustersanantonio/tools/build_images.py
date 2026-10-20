#!/usr/bin/env python3
"""Build featured images (16:9 crops) and responsive variants for the site.

Usage: python3 tools/build_images.py
Requires Pillow. Sources are the site's own photos under wp-content/uploads.
Outputs:
  site/assets/img/featured/<name>.webp   (1200x675 or smaller when the source is small)
  site/assets/img/media/<base>-<w>.webp  (480/960/1440 variants) + manifest.json
"""
import json, os
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
UP = os.path.join(ROOT, 'wp-content', 'uploads', '2026')
S = {
 'A': '02/Claim-Preparation.webp', 'B': '02/Initial-Consultation.webp', 'C': '02/League-City-Public-Adjuster-BG.webp',
 'D': '02/Negotiation.webp', 'E': '02/Policy-Analysis.webp', 'F': '02/Property-Inspection.webp',
 'G': '02/Public-Adjuster-Pros-and-Cons.webp', 'H': '02/When-Is-It-Too-Late-to-Hire-a-Public-Adjuster.webp',
 'I': '03/Do-I-Need-A-Public-Adjuster.webp', 'J': '03/Fire-Insurance-Adjuster-1.webp', 'K': '03/How-to-Find-a-Public-Adjuster.webp',
 'L': '03/Property-Damage-Adjuster.webp',
 'M': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-Xactimate-Insights-1.webp',
 'N': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-Xactimate-Insights-2.webp',
 'O': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-Xactimate-Insights-3.webp',
 'P': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-Xactimate-Insights-4.webp',
 'Q': '04/Hail-Damage-Roof-Insurance-Claim-How-to-Protect-Your-Roof-1.webp', 'R': '04/Hail-Damage-Roof-Insurance-Claim-How-to-Protect-Your-Roof-2.webp',
 'S': '04/Hail-Damage-Roof-Insurance-Claim-How-to-Protect-Your-Roof-4.webp', 'T': '04/Hail-Damage-Roof-Insurance-Claim-How-to-Protect-Your-Roof-5.webp',
 'U': '04/How-to-Document-Hail-Damage-for-an-Insurance-Claim-1.webp', 'V': '04/How-to-Document-Hail-Damage-for-an-Insurance-Claim-2.webp',
 'W': '04/How-to-Document-Hail-Damage-for-an-Insurance-Claim-3.webp', 'X': '04/How-to-Document-Hail-Damage-for-an-Insurance-Claim-4.webp',
 'Y': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-1.webp', 'Z': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-2.webp',
 'AA': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-3.webp', 'AB': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-4.webp',
 'AC': '04/What-to-Do-If-Your-Hail-Claim-Was-Denied-in-Texas-1.webp', 'AD': '04/What-to-Do-If-Your-Hail-Claim-Was-Denied-in-Texas-2.webp',
 'AE': '04/What-to-Do-If-Your-Hail-Claim-Was-Denied-in-Texas-3.webp', 'AF': '02/Resolution.webp',
}
FULL = (0, 0, 1, 1); LEFT = (0, 0, .5, 1); RIGHT = (.5, 0, 1, 1); MID = (.15, .1, .85, .9)
TL = (0, 0, .5, .5); TR = (.5, 0, 1, .5); BL = (0, .5, .5, 1); BR = (.5, .5, 1, 1)
# name: (source, crop box as fractions, focus y 0..1 for the 16:9 cut)
FEATURED = {
 'san-antonio-hail-season-storm-data': ('Y', FULL, .5),
 'wind-damage-insurance-claims-san-antonio-tx': ('L', FULL, .4),
 'flash-flood-damage-insurance-san-antonio': ('I', FULL, .45),
 'freeze-damage-burst-pipe-claims-san-antonio': ('G', FULL, .45),
 'replacement-cost-vs-actual-cash-value-texas': ('M', FULL, .55),
 'how-to-review-underpaid-roof-insurance-estimate': ('P', FULL, .45),
 'building-codes-insurance-repairs-san-antonio': ('T', FULL, .45),
 'service-hail-damage-claims': ('AC', FULL, .5), 'service-roof-damage-insurance-claims': ('R', FULL, .5),
 'service-wind-damage-claims': ('L', MID, .4), 'service-storm-damage-claims': ('Q', FULL, .5),
 'service-flood-damage-claims': ('I', MID, .5), 'service-freeze-damage-claims': ('K', FULL, .45),
 'service-fire-damage-claims': ('J', FULL, .45), 'service-smoke-damage-claims': ('J', LEFT, .4),
 'service-water-damage-claims': ('H', FULL, .5), 'service-residential-property-claims': ('G', MID, .45),
 'service-commercial-property-claims': ('D', FULL, .5), 'service-denied-insurance-claims': ('AD', FULL, .5),
 'service-underpaid-insurance-claims': ('X', FULL, .5), 'service-delayed-insurance-claims': ('B', FULL, .5),
 'service-insurance-claim-supplements': ('O', FULL, .45), 'service-insurance-appraisal': ('AF', FULL, .5),
 'service-insurance-estimate-review': ('P', MID, .45),
 'page-about-us': ('N', FULL, .45), 'page-services': ('M', MID, .5), 'page-service-areas': ('Y', MID, .5),
 'page-privacy-policy': ('E', FULL, .5), 'page-terms-of-use': ('A', FULL, .5), 'page-local-building-codes': ('F', FULL, .4),
 'page-free-claim-review': ('K', MID, .45), 'page-contact': ('B', FULL, .5), 'page-author-joseph-dittman': ('AE', FULL, .5),
 'page-weather': ('V', FULL, .4), 'page-weather-events': ('Z', FULL, .3), 'page-storm-history': ('U', FULL, .5),
 'page-storm-lookup': ('W', FULL, .5), 'page-claim-calculator': ('M', FULL, .3), 'page-claim-documentation-checklist': ('U', MID, .5),
 'page-claim-tools': ('AA', FULL, .5), 'page-sitemap': ('C', FULL, .5), 'page-blog': ('S', FULL, .4), 'page-faq': ('G', FULL, .3),
 'page-area-alamo-heights': ('AB', FULL, .5), 'page-area-boerne': ('Y', MID, .4), 'page-area-converse': ('AC', MID, .5),
 'page-area-helotes': ('AD', MID, .5), 'page-area-leon-valley': ('Z', MID, .5), 'page-area-live-oak': ('T', MID, .5),
 'page-area-new-braunfels': ('Q', MID, .5), 'page-area-schertz': ('R', MID, .5), 'page-area-universal-city': ('X', MID, .5),
}

def cut(im, box, fy):
    W, H = im.size
    im = im.crop((int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)))
    w, h = im.size
    th = int(w * 9 / 16)
    if th <= h:
        top = int((h - th) * fy)
        return im.crop((0, top, w, top + th))
    tw = int(h * 16 / 9)
    left = (w - tw) // 2
    return im.crop((left, 0, left + tw, h))

def main():
    fdir = os.path.join(ROOT, 'assets', 'img', 'featured'); os.makedirs(fdir, exist_ok=True)
    for name, (src, box, fy) in FEATURED.items():
        im = Image.open(os.path.join(UP, S[src])).convert('RGB')
        im = cut(im, box, fy)
        if im.width > 1200:
            im = im.resize((1200, 675), Image.LANCZOS)
        im.save(os.path.join(fdir, name + '.webp'), 'WEBP', quality=80, method=6)
    # Responsive variants for every image referenced by pages (featured + uploads originals).
    mdir = os.path.join(ROOT, 'assets', 'img', 'media'); os.makedirs(mdir, exist_ok=True)
    manifest = {}
    sources = [os.path.join(fdir, f) for f in os.listdir(fdir)] + [os.path.join(UP, p) for p in S.values()]
    for path in sources:
        im = Image.open(path).convert('RGB')
        base = os.path.splitext(os.path.basename(path))[0]
        variants = {}
        for w in (480, 960, 1440):
            if w >= im.width and w != 480:
                continue
            if w > im.width:
                continue
            h = round(im.height * w / im.width)
            out = os.path.join(mdir, f'{base}-{w}.webp')
            im.resize((w, h), Image.LANCZOS).save(out, 'WEBP', quality=78, method=6)
            variants[w] = f'/assets/img/media/{base}-{w}.webp'
        # Always include the original as the largest candidate.
        rel = '/' + os.path.relpath(path, ROOT).replace(os.sep, '/')
        variants[im.width] = rel
        manifest[os.path.basename(path)] = {'w': im.width, 'h': im.height, 'variants': dict(sorted(variants.items()))}
    with open(os.path.join(mdir, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=1)
    print(len(FEATURED), 'featured;', len(manifest), 'images with variants')

if __name__ == '__main__':
    main()
