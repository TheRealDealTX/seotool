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
 'CP': '02/Claim-Preparation.webp', 'IC': '02/Initial-Consultation.webp', 'LC': '02/League-City-Public-Adjuster-BG.webp',
 'NG': '02/Negotiation.webp', 'PA': '02/Policy-Analysis.webp', 'PI': '02/Property-Inspection.webp',
 'PC': '02/Public-Adjuster-Pros-and-Cons.webp', 'RS': '02/Resolution.webp', 'TQ': '02/Top-Questions-About-Public-Adjusters.webp',
 'TL': '02/When-Is-It-Too-Late-to-Hire-a-Public-Adjuster.webp',
 'DH1': '04/Document-Hail-Damage-for-an-Insurance-Claim-1.webp', 'DH2': '04/Document-Hail-Damage-for-an-Insurance-Claim-2.webp',
 'DH3': '04/Document-Hail-Damage-for-an-Insurance-Claim-3.webp', 'DH4': '04/Document-Hail-Damage-for-an-Insurance-Claim-4.webp',
 'DN1': '04/Hail-Claim-Was-Denied-in-Texas-1.webp', 'DN2': '04/Hail-Claim-Was-Denied-in-Texas-2.webp',
 'DN3': '04/Hail-Claim-Was-Denied-in-Texas-3.webp', 'DN4': '04/Hail-Claim-Was-Denied-in-Texas-4.webp',
 'SU11': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-1-1.webp',
 'SU1': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-1.webp',
 'SU2': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-2.webp',
 'SU31': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-3-1.webp',
 'SU3': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-3.webp',
 'SU41': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-4-1.webp',
 'SU4': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-4.webp',
 'SU5': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-5.webp',
 'SU6': '04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-6.webp',
 'RF1': '04/Hail-Damage-Roof-Insurance-Claim-1.webp', 'RF2': '04/Hail-Damage-Roof-Insurance-Claim-2.webp',
 'RF3': '04/Hail-Damage-Roof-Insurance-Claim-3.webp', 'RF6': '04/Hail-Damage-Roof-Insurance-Claim-6.webp',
 'PV1': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-1.webp',
 'PV3': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-3.webp',
 'PV4': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-4.webp',
 'PV6': '04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-in-Texas-6.webp',
 'FI1': '06/Fire-Insurance-Adjuster-1.webp', 'FI2': '06/Fire-Insurance-Adjuster-2.webp',
 'FI4': '06/Fire-Insurance-Adjuster-4.webp', 'FI6': '06/Fire-Insurance-Adjuster-6.webp',
}
FULL = (0, 0, 1, 1); LEFT = (0, 0, .5, 1); RIGHT = (.5, 0, 1, 1)
TOPL = (0, 0, .5, .5); TOPR = (.5, 0, 1, .5); BOTL = (0, .5, .5, 1); BOTR = (.5, .5, 1, 1)
# name: (source, crop box as fractions, focus y 0..1 for the 16:9 cut)
FEATURED = {
 # new articles
 'hurricane-damage-claims-corpus-christi-guide': ('TQ', FULL, .45),
 'twia-claim-process-corpus-christi': ('SU2', FULL, .4),
 'wind-vs-storm-surge-damage-claims-texas-coast': ('SU3', FULL, .5),
 'named-storm-hurricane-deductibles-texas': ('TL', FULL, .5),
 'windstorm-certificate-wpi-8-insurance-claims': ('PI', FULL, .5),
 'wind-damage-insurance-claims-corpus-christi-tx': ('SU4', FULL, .45),
 'water-damage-vs-flood-damage-corpus-christi': ('SU5', FULL, .5),
 'replacement-cost-vs-actual-cash-value-texas': ('PV6', FULL, .5),
 'why-property-insurance-claims-are-delayed-texas': ('DN2', FULL, .45),
 'how-to-review-underpaid-roof-insurance-estimate': ('RF2', FULL, .5),
 'document-commercial-property-damage-after-storm': ('SU31', FULL, .5),
 'freeze-damage-burst-pipe-claims-corpus-christi': ('CP', FULL, .5),
 'noaa-weather-records-document-property-damage-corpus-christi': ('DH2', FULL, .45),
 'corpus-christi-storm-history-hail-wind-hurricanes': ('DH3', FULL, .5),
 # services
 'service-hurricane-damage-claims': ('TQ', FULL, .3),
 'service-twia-windstorm-claims': ('SU41', FULL, .45),
 'service-wind-damage-claims': ('SU11', FULL, .5),
 'service-hail-damage-claims': ('SU1', FULL, .5),
 'service-roof-damage-insurance-claims': ('DN4', FULL, .5),
 'service-storm-damage-claims': ('DH1', FULL, .5),
 'service-flood-damage-claims': ('SU5', FULL, .3),
 'service-water-damage-claims': ('TL', FULL, .3),
 'service-mold-damage-claims': ('RS', FULL, .5),
 'service-fire-damage-claims': ('FI1', FULL, .45),
 'service-smoke-damage-claims': ('FI2', FULL, .45),
 'service-residential-property-claims': ('PC', FULL, .4),
 'service-commercial-property-claims': ('NG', FULL, .5),
 'service-denied-insurance-claims': ('DN1', FULL, .5),
 'service-underpaid-insurance-claims': ('RF6', FULL, .5),
 'service-delayed-insurance-claims': ('DN3', FULL, .5),
 'service-insurance-claim-supplements': ('SU6', FULL, .5),
 'service-insurance-appraisal': ('PA', FULL, .5),
 'service-insurance-estimate-review': ('RF1', FULL, .5),
 # pages
 'page-about-us': ('PV1', FULL, .45), 'page-services': ('SU3', FULL, .3), 'page-service-areas': ('SU3', RIGHT, .5),
 'page-privacy-policy': ('PA', FULL, .4), 'page-terms-of-use': ('RS', FULL, .4), 'page-local-building-codes': ('PI', FULL, .3),
 'page-free-claim-review': ('PC', FULL, .3), 'page-contact': ('IC', FULL, .5), 'page-author-joseph-dittman': ('PV3', FULL, .5),
 'page-weather': ('SU5', FULL, .2), 'page-weather-events': ('DH3', FULL, .2), 'page-storm-history': ('SU3', FULL, .65),
 'page-storm-lookup': ('DH4', FULL, .5), 'page-claim-calculator': ('PV6', FULL, .3), 'page-claim-documentation-checklist': ('DH4', TOPL, .5),
 'page-claim-tools': ('RF3', FULL, .5), 'page-sitemap': ('LC', FULL, .5), 'page-faq': ('TQ', FULL, .6),
 'page-hurricane-season-guide': ('SU3', LEFT, .5), 'page-hurricane-deductible-calculator': ('PV4', FULL, .5),
 'page-claim-deadline-calculator': ('DN2', FULL, .3), 'page-blog': ('SU31', FULL, .3),
 # service-area pages
 'page-area-portland-tx': ('SU2', RIGHT, .5), 'page-area-rockport-tx': ('SU3', LEFT, .4), 'page-area-port-aransas-tx': ('SU3', RIGHT, .4),
 'page-area-aransas-pass-tx': ('SU5', LEFT, .5), 'page-area-ingleside-tx': ('SU4', RIGHT, .5), 'page-area-padre-island-tx': ('SU6', FULL, .4),
 'page-area-robstown-tx': ('DH3', FULL, .65), 'page-area-kingsville-tx': ('PV1', RIGHT, .5),
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
