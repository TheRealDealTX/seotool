#!/usr/bin/env python3
"""Build featured images (16:9 crops) and responsive variants for the site.

Usage: python3 tools/build_images.py
Requires Pillow. Sources: site/assets/img/photos/*.webp and the original
WordPress uploads under site/wp-content/uploads/2026/02/.

Every '/assets/img/featured/<name>.webp' referenced by a content file is built.
Names listed in PICK use the chosen photo; anything else gets a photo by keyword,
falling back to a stable rotation so no reference is ever left broken.

Outputs:
  site/assets/img/featured/<name>.webp   (1200x675)
  site/assets/img/media/<base>-<w>.webp  (480/960/1440 variants) + manifest.json
"""
import glob, hashlib, json, os, re
from PIL import Image, ImageEnhance

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
PH = os.path.join(ROOT, 'assets', 'img', 'photos')
UP = os.path.join(ROOT, 'wp-content', 'uploads', '2026', '02')

# name -> (photo basename without .webp, focus y 0..1)
PICK = {
    'page-hurricane-tracker': ('radar-weather-data-review', .45),
    'page-hurricane-deductible-calculator': ('homeowners-reviewing-settlement-with-adjuster', .45),
    'page-weather': ('radar-weather-data-review', .3),
    'page-weather-events': ('storm-damaged-neighborhood-roofs', .4),
    'page-storm-history': ('storm-damaged-neighborhood-roofs', .6),
    'page-storm-lookup': ('storm-damage-documentation-collage', .5),
    'page-claim-calculator': ('xactimate-estimate-review', .4),
    'page-claim-documentation-checklist': ('claim-file-photos-and-estimates', .5),
    'page-claim-tools': ('estimate-review-laptop-roof-photos', .4),
    'page-about-us': ('adjuster-inspecting-ceiling-damage-with-homeowners', .35),
    'page-services': ('public-adjuster-roof-inspection-tarp', .4),
    'page-service-areas': ('storm-damaged-neighborhood-roofs', .5),
    'page-contact': ('adjuster-explaining-claim-to-couple', .4),
    'page-free-claim-review': ('homeowner-reviewing-claim-letter', .45),
    'page-faq': ('adjuster-explaining-claim-to-couple', .55),
    'page-author-joseph-dittman': ('adjuster-measuring-roof-damage', .4),
    'page-local-building-codes': ('roof-inspection-brick-home', .5),
    'page-privacy-policy': ('claim-file-photos-and-estimates', .3),
    'page-terms-of-use': ('xactimate-estimate-review', .6),
    'page-sitemap': ('storm-damaged-neighborhood-roofs', .2),
    'page-blog': ('estimate-review-laptop-roof-photos', .6),
    'page-category-general': ('estimate-review-laptop-roof-photos', .3),
    'service-hurricane-damage-claims': ('adjuster-and-homeowner-roof-tarp', .4),
    'service-twia-windstorm-claims': ('public-adjuster-roof-inspection-tarp', .5),
    'service-wind-damage-claims': ('metal-roof-storm-damage', .5),
    'service-flood-damage-claims': ('flooded-living-room-homeowners-adjuster', .45),
    'service-storm-damage-claims': ('storm-damaged-neighborhood-roofs', .45),
    'service-roof-damage-insurance-claims': ('adjuster-measuring-roof-damage', .45),
    'service-hail-damage-claims': ('damaged-shingles-roof-diagram', .5),
    'service-water-damage-claims': ('adjuster-reviewing-ceiling-water-damage', .4),
    'service-mold-damage-claims': ('storm-damaged-interior-adjuster', .4),
    'service-fire-damage-claims': ('house-fire-damage-claim', .45),
    'service-smoke-damage-claims': ('smoke-damage-living-room-inspection', .45),
    'service-residential-property-claims': ('adjuster-inspecting-ceiling-damage-with-homeowners', .4),
    'service-commercial-property-claims': ('estimate-review-laptop-roof-photos', .5),
    'service-denied-insurance-claims': ('denied-claim-vs-approved-claim', .5),
    'service-underpaid-insurance-claims': ('homeowners-reviewing-settlement-with-adjuster', .5),
    'service-delayed-insurance-claims': ('homeowner-reviewing-claim-letter', .5),
    'service-insurance-claim-supplements': ('xactimate-estimate-review', .5),
    'service-insurance-appraisal': ('insurance-dispute-appraisal', .5),
    'service-insurance-estimate-review': ('claim-file-photos-and-estimates', .45),
    'twia-windstorm-claim-guide-port-arthur': ('public-adjuster-roof-inspection-tarp', .35),
    'hurricane-damage-insurance-claim-port-arthur': ('adjuster-and-homeowner-roof-tarp', .55),
    'wind-vs-flood-damage-port-arthur-insurance': ('flooded-living-room-homeowners-adjuster', .3),
    'hurricane-deductible-texas-explained': ('homeowners-reviewing-settlement-with-adjuster', .35),
    'port-arthur-hurricane-history-insurance-lessons': ('radar-weather-data-review', .55),
    'how-to-document-storm-damage-port-arthur': ('photographing-roof-damage', .5),
    'denied-insurance-claim-port-arthur': ('denied-claim-vs-approved-claim', .4),
}
KEYWORDS = [('hurricane', 'adjuster-and-homeowner-roof-tarp'), ('flood', 'flooded-living-room-homeowners-adjuster'),
            ('wind', 'metal-roof-storm-damage'), ('roof', 'adjuster-measuring-roof-damage'), ('fire', 'house-fire-damage-claim'),
            ('water', 'adjuster-reviewing-ceiling-water-damage'), ('area', 'storm-damaged-neighborhood-roofs')]
# Area pages get distinct photos, in this order.
AREA_PHOTOS = ['storm-damaged-neighborhood-roofs', 'roof-inspection-brick-home', 'public-adjuster-roof-inspection-tarp',
               'photographing-roof-damage', 'adjuster-and-homeowner-roof-tarp', 'adjuster-measuring-roof-damage', 'metal-roof-storm-damage']


def referenced_featured():
    names = set()
    for f in glob.glob(os.path.join(ROOT, 'content', '**', '*.php'), recursive=True) + glob.glob(os.path.join(ROOT, 'templates', '**', '*.php'), recursive=True):
        names.update(re.findall(r'/assets/img/featured/([a-z0-9-]+)\.webp', open(f, encoding='utf-8').read()))
    return sorted(names)


def choose(name, area_i):
    if name in PICK:
        return PICK[name]
    if name.startswith('page-service-areas-'):
        return AREA_PHOTOS[area_i % len(AREA_PHOTOS)], .5
    for kw, photo in KEYWORDS:
        if kw in name:
            return photo, .5
    photos = sorted(os.path.splitext(p)[0] for p in os.listdir(PH))
    return photos[int(hashlib.md5(name.encode()).hexdigest(), 16) % len(photos)], .5


def cut(im, fy):
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
    area_i = 0
    built = 0
    for name in referenced_featured():
        photo, fy = choose(name, area_i)
        if name.startswith('page-service-areas-') and name not in PICK:
            area_i += 1
        im = Image.open(os.path.join(PH, photo + '.webp')).convert('RGB')
        im = cut(im, fy)
        im = im.resize((1200, 675), Image.LANCZOS) if im.width >= 1200 else im
        im = ImageEnhance.Color(im).enhance(.95)
        im.save(os.path.join(fdir, name + '.webp'), 'WEBP', quality=80, method=6)
        built += 1
    mdir = os.path.join(ROOT, 'assets', 'img', 'media'); os.makedirs(mdir, exist_ok=True)
    for old in glob.glob(os.path.join(mdir, '*')):
        os.remove(old)
    manifest = {}
    sources = sorted(glob.glob(os.path.join(fdir, '*.webp'))) + sorted(glob.glob(os.path.join(PH, '*.webp')))
    sources += [os.path.join(UP, n) for n in ('Are-Insurance-Adjusters-Honest.webp', 'Public-Adjuster-Pros-and-Cons.webp',
                                              'When-Is-It-Too-Late-to-Hire-a-Public-Adjuster.webp', 'League-City-Public-Adjuster-BG.webp')]
    for path in sources:
        im = Image.open(path).convert('RGB')
        base = os.path.splitext(os.path.basename(path))[0]
        variants = {}
        for w in (480, 960, 1440):
            if w >= im.width:
                continue
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(os.path.join(mdir, f'{base}-{w}.webp'), 'WEBP', quality=78, method=6)
            variants[w] = f'/assets/img/media/{base}-{w}.webp'
        variants[im.width] = '/' + os.path.relpath(path, ROOT).replace(os.sep, '/')
        manifest[os.path.basename(path)] = {'w': im.width, 'h': im.height, 'variants': dict(sorted(variants.items()))}
    with open(os.path.join(mdir, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=1)
    print(built, 'featured;', len(manifest), 'images with variants')


if __name__ == '__main__':
    main()
