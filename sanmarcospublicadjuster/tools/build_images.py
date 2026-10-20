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
ST = os.path.join(ROOT, 'assets', 'img', 'stock')
# Original San Marcos photos (wp-content/uploads/2026/...) and shared stock photos (assets/img/stock/).
S = {
 'RD': UP + '/02/Roof-Damage-Public-Adjuster.webp', 'AF': UP + '/04/After-the-Flames-Insurance-Adjuster.webp',
 'CD': UP + '/03/The-Claim-Decision-That-Can-Cost-You-Thousands-Do-I-Need-a-Public-Adjuster_.webp',
 'SG': UP + '/03/7-Signs-You-Should-Hire-a-Public-Adjuster.webp', 'HC': UP + '/03/How-to-Choose-the-Right-Public-Adjuster-in-San-Marcos.webp',
 'WP': UP + '/02/What-Is-a-Public-Adjuster-and-How-to-Hire-One.webp', 'WC': UP + '/02/What-Is-a-Public-Claims-Adjuster.webp',
 'HF': UP + '/02/How-to-Find-a-Public-Adjuster.webp', 'WL': UP + '/02/When-Is-It-Too-Late-to-Hire-a-Public-Adjuster.webp',
 'AW': UP + '/02/Are-Public-Adjusters-Worth-It.webp', 'BG': UP + '/02/League-City-Public-Adjuster-BG.webp',
 'CP': UP + '/02/Claim-Preparation.webp', 'IC': UP + '/02/Initial-Consultation.webp', 'NG': UP + '/02/Negotiation.webp',
 'PA': UP + '/02/Policy-Analysis.webp', 'PI': UP + '/02/Property-Inspection.webp', 'RS': UP + '/02/Resolution.webp',
}
for _f in sorted(os.listdir(ST)) if os.path.isdir(ST) else []:
    S[_f[:-5]] = os.path.join(ST, _f)
FULL = (0, 0, 1, 1); LEFT = (0, 0, .5, 1); RIGHT = (.5, 0, 1, 1)
TL = (0, 0, .5, .5); TR = (.5, 0, 1, .5); BL = (0, .5, .5, 1); BR = (.5, .5, 1, 1)
# name: (source, crop box as fractions, focus y 0..1 for the 16:9 cut)
FEATURED = {
 # new articles
 'san-marcos-hail-season-storm-data': ('hail-covered-roof-after-storm', FULL, .5),
 'wind-damage-insurance-claims-san-marcos-tx': ('storm-damaged-roofs-neighborhood', FULL, .5),
 'flood-damage-insurance-claims-san-marcos': ('collapsed-ceiling-water-damage-adjuster', FULL, .45),
 'freeze-damage-burst-pipe-claims-san-marcos': ('water-damaged-ceiling-homeowners-meeting', FULL, .4),
 'building-codes-insurance-repairs-san-marcos': ('roof-inspection-damage-details', FULL, .5),
 'what-to-do-if-your-claim-was-denied-in-san-marcos': ('homeowner-reviewing-denial-letter', FULL, .5),
 'replacement-cost-vs-actual-cash-value-texas': ('homeowners-reviewing-claim-costs', FULL, .55),
 'how-to-review-underpaid-roof-insurance-estimate': ('xactimate-estimate-review-desk', FULL, .5),
 'why-property-insurance-claims-are-delayed-texas': ('claim-file-review-kitchen-table', FULL, .45),
 'hail-damage-claim-supplements': ('supplement-process-collage', FULL, .5),
 'public-adjuster-vs-insurance-adjuster': ('adjuster-roof-inspection-policyholder', FULL, .45),
 'commercial-property-insurance-claims-san-marcos': ('hail-dented-metal-roof', FULL, .5),
 # services
 'service-hail-damage-claims': ('hail-damaged-shingles-clipboard', FULL, .5),
 'service-roof-damage-insurance-claims': ('RD', FULL, .45),
 'service-wind-damage-claims': ('HF', FULL, .5),
 'service-storm-damage-claims': ('storm-damaged-roofs-neighborhood', RIGHT, .5),
 'service-flood-damage-claims': ('WC', FULL, .45),
 'service-freeze-damage-claims': ('collapsed-ceiling-water-damage-adjuster', FULL, .35),
 'service-fire-damage-claims': ('fire-damaged-room-inspection', FULL, .45),
 'service-smoke-damage-claims': ('fire-damaged-living-room-adjuster', FULL, .45),
 'service-water-damage-claims': ('WP', FULL, .45),
 'service-residential-property-claims': ('AW', FULL, .4),
 'service-commercial-property-claims': ('hail-dented-metal-roof', FULL, .3),
 'service-denied-insurance-claims': ('denied-vs-approved-claim', FULL, .5),
 'service-underpaid-insurance-claims': ('estimate-software-roof-diagram', FULL, .5),
 'service-delayed-insurance-claims': ('claim-evidence-organized-desk', FULL, .5),
 'service-insurance-claim-supplements': ('supplement-process-collage', FULL, .5),
 'service-insurance-appraisal': ('appraisal-dispute-review-table', FULL, .5),
 'service-insurance-estimate-review': ('xactimate-estimate-review-desk', FULL, .45),
 # pages
 'page-about-us': ('SG', FULL, .4), 'page-services': ('adjuster-marking-hail-hits-roof', FULL, .45),
 'page-service-areas': ('BG', FULL, .5), 'page-privacy-policy': ('PA', FULL, .5), 'page-terms-of-use': ('CP', FULL, .5),
 'page-local-building-codes': ('roof-inspection-damage-details', FULL, .35), 'page-free-claim-review': ('HC', FULL, .45),
 'page-contact': ('IC', FULL, .5), 'page-author-joseph-dittman': ('adjuster-roof-inspection-policyholder', FULL, .4),
 'page-weather': ('radar-storm-data-review', FULL, .5), 'page-weather-events': ('hail-covered-roof-after-storm', FULL, .2),
 'page-storm-history': ('hail-damage-documentation-collage', FULL, .5), 'page-storm-lookup': ('radar-storm-data-review', FULL, .3),
 'page-claim-calculator': ('homeowners-reviewing-claim-costs', FULL, .3), 'page-claim-documentation-checklist': ('organized-claim-documentation-folder', FULL, .4),
 'page-claim-tools': ('claim-photos-tablet-review', FULL, .4), 'page-sitemap': ('BG', FULL, .3), 'page-faq': ('CD', FULL, .45),
 'page-blog': ('WL', FULL, .45),
 'page-area-kyle': ('hail-damage-roof-photo-documentation', FULL, .5), 'page-area-buda': ('before-after-roof-documentation', FULL, .5),
 'page-area-wimberley': ('WL', FULL, .5), 'page-area-dripping-springs': ('hail-impact-shingle-closeup', FULL, .5),
 'page-area-new-braunfels': ('WC', FULL, .3), 'page-area-lockhart': ('PI', FULL, .5),
 'page-area-seguin': ('NG', FULL, .5), 'page-area-martindale': ('RS', FULL, .5),
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
        im = Image.open(S[src]).convert('RGB')
        im = cut(im, box, fy)
        if im.width > 1200:
            im = im.resize((1200, 675), Image.LANCZOS)
        im.save(os.path.join(fdir, name + '.webp'), 'WEBP', quality=80, method=6)
    # Responsive variants for every image referenced by pages (featured + uploads originals).
    mdir = os.path.join(ROOT, 'assets', 'img', 'media'); os.makedirs(mdir, exist_ok=True)
    manifest = {}
    sources = [os.path.join(fdir, f) for f in os.listdir(fdir)] + list(S.values())
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
