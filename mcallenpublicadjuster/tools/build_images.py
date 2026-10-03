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
 'A': '02/Are-Public-Adjusters-Worth-It.webp', 'B': '02/Claim-Preparation.webp', 'C': '02/Fire-Insurance-Public-Adjuster.webp',
 'D': '02/How-to-Find-a-Public-Adjuster.webp', 'E': '02/Initial-Consultation.webp', 'F': '02/League-City-Public-Adjuster-BG.webp',
 'G': '02/Negotiation.webp', 'H': '02/Policy-Analysis.webp', 'I': '02/Property-Inspection.webp', 'J': '02/Resolution.webp',
 'K': '02/What-Is-a-Public-Adjuster-and-How-to-Hire-One.webp', 'L': '02/What-Is-a-Public-Claims-Adjuster.webp',
 'M': '02/When-Is-It-Too-Late-to-Hire-a-Public-Adjuster.webp', 'N': '03/Fire-Insurance-Adjuster-1.webp', 'O': '03/Fire-Insurance-Adjuster-2.webp',
 'P': '03/Fire-Insurance-Adjuster-3.webp', 'Q': '03/Fire-Insurance-Adjuster.webp', 'R': '03/Situations-Where-You-Should-Consider-Hiring-a-Public-Adjuster.webp',
 'S': '03/The-Moment-a-Claim-Changes-Knowing-When-to-Hire-a-Public-Adjuster.webp', 'T': '03/Understanding-the-Cost-of-Hiring-a-Public-Adjuster.webp',
 'U': '04/Document-Hail-Damage-for-an-Insurance-Claim-1.webp', 'V': '04/Document-Hail-Damage-for-an-Insurance-Claim-2.webp',
 'W': '04/Document-Hail-Damage-for-an-Insurance-Claim-3.webp', 'X': '04/Document-Hail-Damage-for-an-Insurance-Claim-4.webp',
 'Y': '04/Document-Hail-Damage-for-an-Insurance-Claim-5.webp', 'Z': '04/Document-Hail-Damage-for-an-Insurance-Claim-6.webp',
 'AA': '04/Hail-Damage-Claim-Supplements-1.webp', 'AB': '04/Hail-Damage-Claim-Supplements-2.webp', 'AC': '04/Hail-Damage-Claim-Supplements-4.webp',
 'AD': '04/Hail-Damage-Claim-Supplements-5.webp', 'AE': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-1.webp',
 'AF': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-2.webp', 'AG': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-3.webp',
 'AH': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-4.webp', 'AI': '04/Roof-Hail-Damage-Insurance-Claim-McAllen-1.webp',
 'AJ': '04/Roof-Hail-Damage-Insurance-Claim-McAllen-2.webp', 'AK': '04/Roof-Hail-Damage-Insurance-Claim-McAllen-3.webp',
 'AL': '04/Roof-Hail-Damage-Insurance-Claim-McAllen-4.webp', 'AM': '04/What-to-Do-If-Your-Hail-Claim-Was-Denied-3.webp',
 'AN': '04/What-to-Do-If-Your-Hail-Claim-Was-Denied-4.webp', 'AO': '04/What-to-Do-If-Your-Hail-Claim-Was-Denied-6.webp',
 'AP': '04/What-to-Do-If-Your-Hail-Claim-Was-Denied-7.webp',
}
FULL = (0, 0, 1, 1); LEFT = (0, 0, .5, 1); RIGHT = (.5, 0, 1, 1)
TL = (0, 0, .5, .5); TR = (.5, 0, 1, .5); BL = (0, .5, .5, 1); BR = (.5, .5, 1, 1)
# name: (source, crop box as fractions, focus y 0..1 for the 16:9 cut)
FEATURED = {
 'wind-damage-insurance-claims-mcallen-tx': ('K', FULL, .45),
 'hurricane-damage-mcallen-homeowners-guide': ('AI', FULL, .4),
 'building-codes-insurance-repairs-mcallen': ('I', FULL, .5),
 'how-to-review-underpaid-roof-insurance-estimate': ('AB', FULL, .5),
 'why-property-insurance-claims-are-delayed-texas': ('AH', FULL, .4),
 'water-damage-vs-flood-damage-mcallen': ('S', FULL, .45),
 'document-commercial-property-damage-after-storm': ('AD', LEFT, .5),
 'replacement-cost-vs-actual-cash-value-texas': ('T', FULL, .55),
 'insurance-company-disputes-storm-damage': ('AO', FULL, .45),
 'noaa-weather-records-document-property-damage-mcallen': ('AP', FULL, .5),
 'freeze-damage-burst-pipe-claims-rio-grande-valley': ('R', FULL, .4),
 'mcallen-hail-season-storm-data': ('V', FULL, .5),
 'service-hail-damage-claims': ('AA', FULL, .5),
 'service-roof-damage-insurance-claims': ('AF', FULL, .45),
 'service-wind-damage-claims': ('L', FULL, .5),
 'service-storm-damage-claims': ('AD', RIGHT, .5),
 'service-hurricane-damage-claims': ('AJ', FULL, .5),
 'service-fire-damage-claims': ('N', FULL, .45),
 'service-smoke-damage-claims': ('P', FULL, .45),
 'service-water-damage-claims': ('D', FULL, .4),
 'service-residential-property-claims': ('A', FULL, .4),
 'service-commercial-property-claims': ('G', FULL, .5),
 'service-denied-insurance-claims': ('AM', FULL, .5),
 'service-underpaid-insurance-claims': ('X', FULL, .5),
 'service-delayed-insurance-claims': ('M', FULL, .5),
 'service-insurance-claim-supplements': ('AG', FULL, .5),
 'service-insurance-appraisal': ('J', FULL, .5),
 'service-insurance-estimate-review': ('Z', FULL, .5),
 'page-about-us': ('AK', FULL, .45), 'page-services': ('AA', FULL, .15), 'page-service-areas': ('AL', LEFT, .5),
 'page-privacy-policy': ('H', FULL, .5), 'page-terms-of-use': ('B', FULL, .5), 'page-local-building-codes': ('AL', RIGHT, .5),
 'page-free-claim-review': ('O', FULL, .45), 'page-contact': ('E', FULL, .5), 'page-author-joseph-dittman': ('Y', FULL, .5),
 'page-weather': ('AP', FULL, .3), 'page-weather-events': ('AI', FULL, .2), 'page-storm-history': ('U', FULL, .5),
 'page-storm-lookup': ('W', TL, .5), 'page-claim-calculator': ('T', FULL, .3), 'page-claim-documentation-checklist': ('Y', FULL, .4),
 'page-claim-tools': ('Z', FULL, .3), 'page-sitemap': ('F', FULL, .5),
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
