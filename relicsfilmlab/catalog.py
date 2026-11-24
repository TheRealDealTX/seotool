"""Relics Film Lab product catalog.

One line per product:  slug | Name | category | year | spec | blurb
  * slug      — kept exactly as the old Shopify /products/<slug> URL
  * category  — key from CATEGORIES below
  * year      — launch year (approximate is fine, blank if unknown)
  * spec      — short spec line shown under the title ("35mm · 38mm f/2.8 · autofocus")
  * blurb     — optional hand-written intro; when blank the generator writes one
Old URLs that should 301 to another product live in PRODUCT_REDIRECTS.
"""

CATEGORIES = {
    # key: (label, collection slug, format, film search, film label)
    "ps":      ("Point & Shoot", "point-shoot-cameras", "35mm", "Kodak Gold 200 35mm film", "35mm colour negative film"),
    "slr":     ("SLR Camera", "slr-cameras", "35mm", "Kodak Portra 400 35mm film", "35mm colour negative film"),
    "instant": ("Instant Camera", "polaroid-cameras", "instant", "Polaroid 600 film", "Polaroid 600 film"),
    "mf":      ("Medium Format", "medium-format-cameras", "120", "Kodak Portra 400 120 film", "120 roll film"),
    "movie":   ("Super 8 & Movie", "super-8-collections", "super8", "Kodak Super 8 film cartridge", "Super 8 film cartridges"),
    "pocket":  ("110 Pocket Camera", "point-shoot-cameras", "110", "Lomography 110 film", "110 cartridge film"),
    "digital": ("Vintage Digital", "all-film-cameras", "digital", "SD memory card 8GB", "SD memory cards"),
    "lens":    ("Lens", "accessories", "", "", ""),
    "bag":     ("Camera Bag", "accessories", "", "", ""),
    "strap":   ("Camera Strap", "accessories", "", "", ""),
    "film":    ("Film & Supplies", "film-lab", "", "", ""),
    "book":    ("Photo Book", "books", "", "", ""),
    "print":   ("Photo Print", "prints", "", "", ""),
    "carprint": ("Car Print", "car-collection", "", "", ""),
    "tote":    ("Tote Bag", "prints", "", "", ""),
    "service": ("Film Lab Guide", "film-lab", "", "", ""),
    "workshop": ("Workshop & Learning", "workshops", "", "", ""),
    "collect": ("Collectible", "accessories", "", "", ""),
}

RAW = r"""
polaroid-one-step-land-camera|Polaroid OneStep Land Camera|instant|1977|SX-70 film · fixed-focus 103mm lens · folding-free body|The rainbow-stripe Polaroid OneStep Land Camera is the camera most people picture when they hear the word Polaroid. Introduced in 1977, it made instant photography a one-button affair: point, press the red shutter and a print slides out the front.
minolta-x-700-mps-with-50mm-lens|Minolta X-700 MPS with 50mm Lens|slr|1981|35mm SLR · Minolta MD mount · Program, Aperture-priority & Manual|The Minolta X-700 was European Camera of the Year in 1981 and stayed in production for almost twenty years. It pairs a bright viewfinder and a full Program mode with genuine manual control, which is why it is still one of the best first SLRs you can buy.
olympus-trip-35|Olympus Trip 35|ps|1967|35mm · Zuiko 40mm f/2.8 · selenium meter, no batteries|The Olympus Trip 35 sold more than ten million copies between 1967 and 1984. Its selenium cell powers the auto-exposure from light alone, so there is no battery to die, and the four-element 40mm Zuiko lens is sharp enough to embarrass far newer cameras.
canon-eos-rebel-xs|Canon EOS Rebel XS (35mm)|slr|1993|35mm autofocus SLR · Canon EF mount · Program & creative modes|The 35mm Canon EOS Rebel XS (sold as the EOS 500 in Europe and the EOS Kiss in Japan) is a light, quiet autofocus film SLR that takes every Canon EF lens ever made. Not to be confused with the later digital Rebel XS, it shoots real 35mm film. It is an easy, affordable way to get modern autofocus and auto-exposure on real film.
canon-eos-rebel|Canon EOS Rebel 35mm Film Camera|slr|1990|35mm autofocus SLR · Canon EF mount · built-in flash|The original Canon EOS Rebel brought Canon's EF autofocus system to beginners in 1990. It is a lightweight film SLR with full program automation, a pop-up flash and access to Canon's huge EF lens catalogue.
canon-ae-1|Canon AE-1|slr|1976|35mm SLR · Canon FD mount · shutter-priority auto exposure|The Canon AE-1 was the first SLR with a microprocessor and one of the best-selling film cameras of all time. Shutter-priority auto exposure, a crisp split-image focusing screen and Canon's superb FD lenses make it a classic first film SLR.
canon-ae-1-program|Canon AE-1 Program|slr|1981|35mm SLR · Canon FD mount · Program & shutter-priority modes|The Canon AE-1 Program added a full Program mode and a brighter focusing screen to the legendary AE-1. It is one of the most popular 35mm SLRs to learn on because it can be fully automatic or fully manual.
canon-sure-shot-z-115|Canon Sure Shot Z115|ps|1993|35mm · 38–115mm zoom · autofocus · built-in flash|The Canon Sure Shot Z115 (Prima Super 115 / Autoboy S) is a compact 35mm zoom camera with a long 38–115mm lens, dependable autofocus and an automatic flash — a fuss-free travel camera.
olympus-stylus-35-mm-black|Olympus Stylus (Infinity Stylus) 35mm|ps|1991|35mm · 35mm f/3.5 · autofocus · clamshell|The original Olympus Stylus — sold in the US as the Infinity Stylus and as the mju in Europe — introduced the pebble-shaped clamshell design that made it one of the most popular compact 35mm cameras ever.
olympus-stylus-epic-zoom-80|Olympus Stylus Epic Zoom 80|ps|1998|35mm · 38–80mm zoom · weatherproof · autofocus|The Olympus Stylus Epic Zoom 80 (mju-II Zoom 80) packs a 38–80mm zoom into the same splash-proof pocket body as the famous Stylus Epic.
olympus-quick-shooter|Olympus Quick Shooter Zoom|ps|1990|35mm · zoom lens · autofocus · built-in flash|The Olympus Quick Shooter is a simple, rugged 35mm point-and-shoot built for snapshots — load the film, close the back and shoot.
pentax-iqzoom-160|Pentax IQZoom 160|ps|1997|35mm · 38–160mm zoom · autofocus|The Pentax IQZoom 160 (Espio 160) was one of the longest-reaching compact zooms of the nineties, with a 38–160mm lens that goes from group shots to tight portraits.
olympus-superzoom-760|Olympus Superzoom 760|ps|1996|35mm · 38–76mm zoom · autofocus|The Olympus Superzoom 760 is a slim 35mm zoom compact with a 38–76mm lens and an automatic flash — a reliable everyday film camera.
olympus-stylus|Olympus Stylus Epic|ps|1997|35mm · 35mm f/2.8 · weatherproof · autofocus|The Olympus Stylus Epic (mju-II) is a cult classic: a fast, sharp 35mm f/2.8 lens in a splash-proof body small enough to disappear in a pocket.
canon-514xl-super-8-camera|Canon 514XL Super 8 Camera|movie|1975|Super 8 · 9–45mm f/1.4 zoom · 18/24 fps|The Canon 514XL is a compact Super 8 movie camera with a fast f/1.4 zoom lens and Canon's "XL" low-light design, which makes it a favourite for weddings and home movies.
nikon-nikomat|Nikon Nikkormat (Nikomat)|slr|1965|35mm SLR · Nikon F mount (non-AI) · mechanical shutter|The Nikkormat — sold as the Nikomat in Japan — is Nikon's all-mechanical workhorse from the 1960s and 70s. It takes Nikon F-mount lenses and needs a battery only for the light meter.
olympus-stylus-zoom-35-70mm|Olympus Stylus Zoom 35–70mm|ps|1993|35mm · 35–70mm zoom · autofocus · clamshell|The Olympus Stylus Zoom adds a 35–70mm zoom lens to the clamshell Stylus design — a pocketable Olympus film camera with a little extra reach.
olympus-infinity-zoom-200|Olympus Infinity Zoom 200|ps|1990|35mm · 38–80mm zoom · autofocus|The Olympus Infinity Zoom 200 is a capable 35mm zoom point-and-shoot from Olympus's Infinity line, with autofocus and a built-in flash.
nikon-tele-touch|Nikon Tele Touch|ps|1987|35mm · dual 35/70mm lens · autofocus|The Nikon Tele Touch (TW2 / Tele AF) flips between a 35mm wide and 70mm tele lens at the push of a button.
canon-sure-shot-owl-date|Canon Sure Shot Owl Date|ps|1988|35mm · 35mm f/2.8 · autofocus · date back|The Canon Sure Shot Owl earned its nickname from the large viewfinder window above its lens — giving it its owl-like face and one of the brightest finders on any compact.
ds-max-hc-2000|DS-Max HC-2000|ps||35mm compact · fixed-focus lens · built-in flash|
kodak-cameo-motor-ex|Kodak Cameo Motor EX|ps|1990|35mm · fixed-focus 35mm lens · motorised advance|The Kodak Cameo Motor EX is a tiny motorised 35mm camera made for no-thought snapshots.
minolta-xg-1|Minolta XG-1|slr|1979|35mm SLR · Minolta MD mount · aperture-priority|The Minolta XG-1 is a compact, aperture-priority 35mm SLR that takes Minolta's excellent MC and MD Rokkor lenses.
fuji-discovery-1000-zoom|Fuji Discovery 1000 Zoom|ps|1993|35mm · 38–105mm zoom · autofocus|The Fuji Discovery 1000 Zoom is a 35mm zoom compact from Fujifilm's Discovery series, with a Fujinon zoom lens.
pentax-espio-738|Pentax Espio 738|ps|2000|35mm · 38–70mm zoom · autofocus|The Pentax Espio 738 (IQZoom 738) is a compact 35mm zoom with a 38–70mm lens and Pentax's dependable autofocus.
pentax-zoom-70-r|Pentax Zoom 70-R|ps|1988|35mm · 35–70mm zoom · autofocus|The Pentax Zoom 70-R is a chunky late-80s autofocus zoom compact with a 35–70mm lens.
olympus-stylus-epic-dlx-w-panoramic|Olympus Stylus Epic DLX with Panoramic|ps|1997|35mm · 35mm f/2.8 · weatherproof · panorama mode|The Olympus Stylus Epic DLX is the deluxe version of the cult Stylus Epic, adding a date/panorama function to the same sharp 35mm f/2.8 lens.
canon-sureshot-65-zoom|Canon Sure Shot 65 Zoom|ps|1994|35mm · 38–65mm zoom · autofocus|The Canon Sure Shot 65 Zoom is a compact Canon 35mm camera with a modest 38–65mm zoom.
canon-sure-shot-105-zoom-s|Canon Sure Shot 105 Zoom S|ps|1997|35mm · 38–105mm zoom · autofocus|The Canon Sure Shot 105 Zoom S is a slim 35mm Canon Sure Shot with a 38–105mm zoom lens.
kodak-fisher-price|Kodak × Fisher-Price 110 Camera|pocket|1984|110 film · fixed-focus lens|The Fisher-Price 110 camera is a rugged, kid-proof 110 film camera with oversized controls.
nikon-f-photomic|Nikon F Photomic|slr|1965|35mm SLR · Nikon F mount · Photomic metering prism|The Nikon F was the camera that made the 35mm SLR the professional standard. The Photomic version adds a metering prism to the indestructible F body.
olympus-35-rc|Olympus 35 RC|ps|1970|35mm rangefinder · 42mm f/2.8 · shutter-priority|The Olympus 35 RC is one of the smallest full-featured rangefinders ever made, with a sharp 42mm f/2.8 lens and both auto and manual exposure.
canon-t50-with-35-70mm-zoom-lens|Canon T50 with 35–70mm Zoom Lens|slr|1983|35mm SLR · Canon FD mount · program auto|The Canon T50 is a fully programmed 35mm SLR with a built-in motor winder — Canon's first step towards the modern automatic SLR.
canon-tx|Canon TX|slr|1975|35mm SLR · Canon FD mount · manual|The Canon TX is a simple, all-manual FD-mount SLR — a great camera for learning exposure.
nikon-one-touch|Nikon One Touch|ps|1987|35mm · 35mm f/3.5 · autofocus|The Nikon One Touch (L35AF3) is a straightforward Nikon point-and-shoot film camera with a sharp 35mm lens.
olympus-om-10|Olympus OM-10|slr|1979|35mm SLR · Olympus OM mount · aperture-priority|The Olympus OM-10 is a small, light aperture-priority SLR that takes Olympus's renowned Zuiko OM lenses.
polaroid-600-one-step-spirit-instant-camera|Polaroid 600 OneStep Spirit|instant|1990s|Polaroid 600 film · fixed focus · built-in flash|The Polaroid Spirit 600 is a classic box-style Polaroid 600 camera.
polaroid-600-onestep-close-up-instant-camera|Polaroid 600 OneStep Close-Up|instant|1990s|Polaroid 600 film · close-up lens switch|The Polaroid OneStep Close Up adds a close-up lens setting to the classic 600 OneStep.
minolta-x-370|Minolta X-370|slr|1984|35mm SLR · Minolta MD mount · aperture-priority & manual|The Minolta X-370 (X-300) is a simple, light Minolta SLR with aperture-priority auto exposure.
nikon-one-touch-zoom-90s|Nikon One Touch Zoom 90s|ps|1998|35mm · 38–90mm zoom · autofocus|A compact 90s Nikon zoom camera with a 38–90mm lens.
kiev-6c-with-65mm-lens|Kiev 6C with 65mm Lens|mf|1971|6×6 medium format SLR · Pentacon Six mount|The Kiev 6C is a Soviet-made 6×6 medium-format SLR shaped like a giant 35mm camera.
olympus-stylus-120|Olympus Stylus 120|ps|2003|35mm · 38–120mm zoom · weatherproof|The Olympus Stylus 120 is a splash-proof 35mm zoom compact.
yashica-electro-35-gsn|Yashica Electro 35 GSN|ps|1973|35mm rangefinder · Yashinon 45mm f/1.7 · aperture-priority|The Yashica Electro 35 GSN pairs a fast 45mm f/1.7 lens with stepless aperture-priority auto exposure.
olympus-stylus-infinity-mju-35mm-black-amp-silver|Olympus Stylus Infinity (mju)|ps|1991|35mm · 35mm f/3.5 · autofocus|The Olympus Infinity Stylus is the original clamshell compact.
fujica-dl-100|Fujica DL-100|ps|1984|35mm · 38mm f/2.8 · auto load|The Fujica DL-100 introduced Fuji's "drop-in loading" for effortless 35mm film loading.
yashica-mat-124-g|Yashica Mat-124 G|mf|1970|6×6 TLR · Yashinon 80mm f/3.5|The Yashica Mat-124 G is the classic affordable twin-lens reflex.
chinon-20-p-xl-direct-sound-super-8-camera|Chinon 20P XL Direct Sound Super 8 Camera|movie|1978|Super 8 sound · XL low-light zoom|The Chinon 20P XL Direct Sound records sound on Super 8 sound cartridges.
minolta-srt-101-with-50mm-lens-1966|Minolta SRT 101 with 50mm Lens (1966)|slr|1966|35mm SLR · Minolta MC mount · match-needle meter|The Minolta SRT 101 is a heavy, all-mechanical SLR.
contax-t3-like-new|Contax T3|ps|2001|35mm · Carl Zeiss Sonnar 35mm f/2.8 · titanium body|The Contax T3 is the last and best of Contax's titanium premium compacts.
olympus-om-2n|Olympus OM-2N|slr|1979|35mm SLR · Olympus OM mount · off-the-film metering|The Olympus OM-2N is a pro-level compact SLR.
canon-af-35-ml|Canon AF35ML|ps|1981|35mm · 40mm f/1.9 · autofocus|The Canon AF35ML (Super Sure Shot) has an unusually fast 40mm f/1.9 lens.
samsung-maxima-zoom-70-xl|Samsung Maxima Zoom 70 XL|ps|1990s|35mm · 35–70mm zoom · autofocus|A compact Samsung 35mm zoom.
canon-sureshot-80u|Canon Sure Shot 80u|ps|1999|35mm · 38–80mm zoom · autofocus|The Canon Sure Shot 80u is a compact 35mm zoom.
konica-autoreflex-t3|Konica Autoreflex T3|slr|1973|35mm SLR · Konica AR mount · shutter-priority|The Konica Autoreflex T3 is a robust shutter-priority SLR.
polaroid-sun-660|Polaroid Sun 660|instant|1981|Polaroid 600 film · sonar autofocus|The Polaroid Sun 660 adds sonar autofocus to the 600 platform.
olympus-om-g|Olympus OM-G (OM-20)|slr|1983|35mm SLR · Olympus OM mount · aperture-priority|The Olympus OM-G (OM-20) is an easy aperture-priority SLR.
polaroid-job-pro-2|Polaroid Job Pro II|instant|1990s|Polaroid 600 film · professional documentation camera|The Polaroid Job Pro II was built for insurance, police and construction documentation.
polaroid-600-cool-cam-instant-camera|Polaroid 600 Cool Cam|instant|1988|Polaroid 600 film · fixed focus|The red Polaroid Cool Cam is a fun, colourful 600 instant camera.
fujifilm-instax-wide-300-instant-film-camera-black-silver|Fujifilm Instax Wide 300|instant|2014|Instax Wide film · two-zone focus|The Fujifilm Instax Wide 300 makes credit-card-wide instant prints.
canon-at-1|Canon AT-1|slr|1976|35mm SLR · Canon FD mount · match-needle manual|The Canon AT-1 is the manual sibling of the AE-1.
olympus-trip-md3|Olympus Trip MD3|ps|1990s|35mm · 35mm f/4.5 · motorised|The Olympus Trip MD3 is a simple motorised Olympus compact.
minolta-af-tel|Minolta AF-Tele|ps|1987|35mm · dual 38/60mm lens · autofocus|The Minolta AF-Tele switches between 38mm and 60mm focal lengths.
polaroid-pronto-land-camera|Polaroid Pronto Land Camera|instant|1976|SX-70 film · manual focus|The Polaroid Pronto is a simpler, non-folding SX-70 camera.
vivitar-lc-600-focus-free|Vivitar LC600 Focus Free|ps|1990s|35mm · fixed-focus lens · flash|The Vivitar LC600 is a basic focus-free 35mm camera.
minolta-freedom-zoom-supreme-ex|Minolta Freedom Zoom Supreme EX|ps|1990s|35mm · zoom · autofocus|A long-zoom Minolta Freedom compact.
minolta-xg-m|Minolta XG-M|slr|1981|35mm SLR · Minolta MD mount · aperture-priority & manual|The Minolta XG-M is the last and most refined XG model.
canon-snappy-lx|Canon Snappy LX|ps|1989|35mm · 35mm f/3.5 · autofocus|The Canon Snappy LX is a colourful, easy-to-use Canon compact.
canon-elph-sport|Canon Elph Sport (APS)|ps|1998|APS film · weatherproof|The Canon Elph Sport is a weather-resistant APS film camera.
minolta-110-zoom-date|Minolta 110 Zoom SLR|pocket|1976|110 film SLR · 25–50mm zoom|The Minolta 110 Zoom is one of the only true SLRs ever made for 110 film.
pentax-iqzoom-900|Pentax IQZoom 900|ps|1993|35mm · 38–90mm zoom · autofocus|The Pentax IQZoom 900 is a capable 35mm zoom compact.
polaroid-600-sun-lms-instant-camera|Polaroid Sun 600 LMS|instant|1983|Polaroid 600 film · light management system|The Polaroid Sun 600 LMS has Polaroid's light management system.
pentax-auto-110-film-camera|Pentax Auto 110|pocket|1978|110 film SLR · interchangeable lenses|The Pentax Auto 110 is the smallest interchangeable-lens SLR system ever.
minolta-xe-7-with-50mm-lens|Minolta XE-7 with 50mm Lens|slr|1975|35mm SLR · Minolta MC/MD mount · aperture-priority|The Minolta XE-7 (XE-1) has a smooth Leitz-designed shutter.
olympus-infinity-superzoom-330|Olympus Infinity Superzoom 330|ps|1990s|35mm · 38–105mm zoom · autofocus|
minolta-hi-matic-af2-md|Minolta Hi-Matic AF2-MD|ps|1983|35mm · 38mm f/2.8 · autofocus · motor drive|
nikon-nikonos-iv-a|Nikon Nikonos IV-A|ps|1980|35mm underwater camera · Nikkor 35mm f/2.5|The Nikonos IV-A is an amphibious 35mm camera rated for diving.
fuji-fujica-st-605|Fujica ST605|slr|1976|35mm SLR · M42 screw mount · match-needle|The Fujica ST605 takes M42 screw-mount lenses.
michael-jordan-standing|Michael Jordan Standing Print|print||Ready-to-hang basketball photo print|
olympus-infinity-zoom-211|Olympus Infinity Zoom 211|ps|1990s|35mm · zoom · autofocus|
olympus-stylus-epic-zoom-115-deluxe-1|Olympus Stylus Epic Zoom 115 Deluxe|ps|1999|35mm · 38–115mm zoom · weatherproof|
keystone-easy-shot-500|Keystone Easy Shot 500|ps|1990s|35mm · fixed focus · flash|
canon-310xl-super-8-camera|Canon 310XL Super 8 Camera|movie|1976|Super 8 · 8.5–25.5mm f/1.0 zoom|The Canon 310XL has an ultra-fast f/1.0 lens for shooting in low light.
nikon-fg-20|Nikon FG-20|slr|1984|35mm SLR · Nikon F mount · aperture-priority|
fuji-discovery|Fuji Discovery|ps|1990s|35mm · autofocus · flash|
pentax-pc-35-afm|Pentax PC35AF-M|ps|1985|35mm · 35mm f/2.8 · autofocus|
ricoh-shotmaster-zoom|Ricoh Shotmaster Zoom|ps|1990s|35mm · zoom · autofocus|
28mm-lens|28mm f/2.8 Wide-Angle Lens|lens||Wide-angle prime lens for 35mm SLRs|
vivitar-series-1-460pz|Vivitar Series 1 460PZ|ps|1990s|35mm · zoom · autofocus|
sony-handycam-ccd-sc5|Sony Handycam CCD-SC5|digital|1995|Hi8/8mm camcorder · compact palm design|
nikon-l35-af|Nikon L35AF|ps|1983|35mm · Nikon 35mm f/2.8 · autofocus|The Nikon L35AF (Pikaichi) has one of the best lenses of any 80s point-and-shoot.
samsung-evoca-140s-quartz-date|Samsung Evoca 140S Quartz Date|ps|1990s|35mm · 38–140mm zoom · autofocus|
minolta-srt-200|Minolta SRT 200 / 201 / 202|slr|1975|35mm SLR · Minolta MC/MD mount · match-needle|
canon-t70-1|Canon T70|slr|1984|35mm SLR · Canon FD mount · multi-program|
fuji-gs645-s|Fuji GS645S Professional|mf|1984|6×4.5 medium format rangefinder · 60mm f/4|The Fuji GS645S is a folding-free 6×4.5 rangefinder with a wide 60mm lens.
minolta-hi-matic-af-2|Minolta Hi-Matic AF2|ps|1981|35mm · 38mm f/2.8 · autofocus|
yashica-35-me-1973|Yashica 35-ME|ps|1979|35mm · Yashinon 38mm f/2.8 · auto exposure|
minolta-freedom-dual|Minolta Freedom Dual|ps|1990s|35mm · dual focal length · autofocus|
minolta-freedom-action-zoom|Minolta Freedom Action Zoom|ps|1990s|35mm · zoom · autofocus|
ricoh-ff-3-af-super|Ricoh FF-3 AF Super|ps|1983|35mm · 35mm f/3.2 · autofocus|
mamiya-c330-with-80mm-lens|Mamiya C330 with 80mm Lens|mf|1969|6×6 TLR · interchangeable lenses|The Mamiya C330 is the only major TLR system with interchangeable lenses.
yashica-a|Yashica-A|mf|1959|6×6 TLR · Yashikor 80mm f/3.5|
pentax-iqzoom-115v|Pentax IQZoom 115V|ps|2000|35mm · 38–115mm zoom · autofocus|
samsung-maxima-zoom-105-xl|Samsung Maxima Zoom 105 XL|ps|1990s|35mm · 38–105mm zoom · autofocus|
olympus-pen-ee-1961|Olympus Pen EE (1961)|ps|1961|35mm half-frame · 28mm f/3.5 · selenium meter|The Olympus Pen EE is a half-frame camera: you get 72 pictures on a 36-exposure roll.
minolta-hi-matic-af2-m|Minolta Hi-Matic AF2-M|ps|1982|35mm · 38mm f/2.8 · autofocus · motor|
canon-sure-shot-telemax-date|Canon Sure Shot Telemax Date|ps|1988|35mm · dual 38/70mm lens · autofocus|
zeiss-ikon-contaflex-with-original-leather-case1953|Zeiss Ikon Contaflex with Leather Case (1953)|slr|1953|35mm leaf-shutter SLR · Tessar 45mm f/2.8|The Zeiss Ikon Contaflex was one of the first 35mm SLRs with a leaf shutter.
olympus-infinity-76|Olympus Infinity 76|ps|1990s|35mm · autofocus|
yashica-electro-35-gt|Yashica Electro 35 GT|ps|1970|35mm rangefinder · 45mm f/1.7|
olympus-xa2-2|Olympus XA2|ps|1980|35mm · 35mm f/3.5 · zone focus · clamshell|The Olympus XA2 is a tiny clamshell zone-focus camera.
canon-tl|Canon TL QL|slr|1968|35mm SLR · Canon FL/FD mount · match-needle|
vivitar-v3000s|Vivitar V3000S|slr|1990s|35mm SLR · K-mount · manual|
canon-ftb|Canon FTb|slr|1971|35mm SLR · Canon FD mount · match-needle|The Canon FTb is a rugged, all-mechanical FD-mount SLR.
zeiss-ikon-contessa-lk-1963|Zeiss Ikon Contessa LK (1963)|ps|1963|35mm viewfinder · Tessar 50mm f/2.8|
olympus-trip-af-50|Olympus Trip AF 50|ps|1990s|35mm · fixed focus · motor|
nikon-zoom-touch-400|Nikon Zoom Touch 400|ps|1990|35mm · zoom · autofocus|
konica-autoreflex-tc|Konica Autoreflex TC|slr|1976|35mm SLR · Konica AR mount · shutter-priority|
nikon-lite-touch-zoom-110|Nikon Lite Touch Zoom 110|ps|1999|35mm · 38–110mm zoom · autofocus|
canon-sureshot-telemax|Canon Sure Shot Telemax|ps|1988|35mm · dual 38/70mm lens · autofocus|
minolta-freedom-zoom-90|Minolta Freedom Zoom 90|ps|1990s|35mm · 38–90mm zoom · autofocus|
nishika-n8000-3d-35mm-film-camera|Nishika N8000 3D Camera|ps|1989|35mm · four-lens 3D lenticular camera|The Nishika N8000 has four lenses side by side to make lenticular 3D prints.
pentax-mg-with-50mm-lens|Pentax MG with 50mm Lens|slr|1981|35mm SLR · Pentax K mount · aperture-priority|
minolta-camera-bag-with-strap|Minolta Camera Bag with Strap|bag||Vintage Minolta-branded shoulder camera bag|
vivitar-pn2011|Vivitar PN2011|ps|1990s|35mm · focus free · flash|
canon-af35m-ii|Canon AF35M II|ps|1983|35mm · 38mm f/2.8 · autofocus|
nikon-one-touch-200|Nikon One Touch 200|ps|1990s|35mm · autofocus|
minolta-xg-9|Minolta XG-9|slr|1979|35mm SLR · Minolta MD mount · aperture-priority|
canon-sure-shot-zoom-s|Canon Sure Shot Zoom S|ps|1990|35mm · 38–60mm zoom · autofocus|
canon-sure-shot-tele|Canon Sure Shot Tele|ps|1990|35mm · dual 40/70mm lens · autofocus|
vintage-kodak-leather-camera-bag|Vintage Kodak Leather Camera Bag|bag||Vintage leather camera case|
the-mural-projejct|The Mural Project Print|print||Ready-to-hang photo print|
pentax-iq-zoom-120|Pentax IQZoom 120|ps|1990s|35mm · 38–120mm zoom · autofocus|
point-and-shoot-a-m-minolta-hi-matic-s|Minolta Hi-Matic S|ps|1975|35mm · Rokkor 38mm f/2.7 · auto exposure|
minolta-freedom-zoom-105i|Minolta Freedom Zoom 105i|ps|1990s|35mm · 38–105mm zoom · autofocus|
kodak-cameo-zoom-plus|Kodak Cameo Zoom Plus|ps|1990s|35mm · zoom · autofocus|
kodak-cameo-focus-free|Kodak Cameo Focus Free|ps|1990s|35mm · fixed focus|
canon-a-1-black-1|Canon A-1 (Black)|slr|1978|35mm SLR · Canon FD mount · five auto modes|The Canon A-1 was the first SLR with a full Program mode plus aperture- and shutter-priority.
canon-sure-shot-85-zoom|Canon Sure Shot 85 Zoom|ps|1997|35mm · 38–85mm zoom · autofocus|
minolta-freedom-af-35r|Minolta Freedom AF 35R|ps|1990s|35mm · autofocus|
polaroid-600-silver-express-instant-camera|Polaroid 600 Silver Express|instant|1990s|Polaroid 600 film · fixed focus|
minolta-freedom-sightseer-zoom|Minolta Freedom Sightseer Zoom|ps|1990s|35mm · zoom · autofocus|
bolex-580-super-8-camera|Bolex 580 Super 8 Camera|movie|1970s|Super 8 · macro zoom|
polaroid-impulse-se|Polaroid Impulse SE|instant|1988|Polaroid 600 film · fixed focus|
kyocera-samurai-x3-0-red-35mm-half-frame-film-camera|Kyocera Samurai ×3.0 Half-Frame (Red)|ps|1987|35mm half-frame SLR · 25–75mm zoom|The Kyocera (Yashica) Samurai ×3.0 is a half-frame SLR shaped like a camcorder.
minolta-af101r-date|Minolta AF101R Date|ps|1990s|35mm · autofocus|
canon-canonet-ql-17-n|Canon Canonet QL17 (New)|ps|1969|35mm rangefinder · 40mm f/1.7|
35mm-film-canister-keychains|35mm Film Canister Keychains|collect||Film canister keychain|
35mm-film-canister-c|35mm Film Canister (C)|collect||Empty 35mm film canister|
canon-av-1|Canon AV-1|slr|1979|35mm SLR · Canon FD mount · aperture-priority|
canon|Canon FD Lenses|lens||Canon FD-mount lenses incl. fisheye|
pentax-iqzoom-ezy-80|Pentax IQZoom EZY-80|ps|1997|35mm · 38–80mm zoom · autofocus|
pentax-iq-zoom-80-e|Pentax IQZoom 80-E|ps|1990s|35mm · 38–80mm zoom · autofocus|
4x6-prints-individual|4×6 Photo Prints|service||Prints from film scans|
olympus-xa2-original-case-a11-electronic-flash|Olympus XA2 with A11 Flash and Case|ps|1980|35mm · zone focus · A11 flash|
polaroid-600-one-step-rainbow-instant-camera|Polaroid 600 OneStep Rainbow|instant|1990s|Polaroid 600 film · fixed focus|
petri-7s|Petri 7S|ps|1963|35mm rangefinder · 45mm f/2.8|
pentax-k-1000-with-50mm-lens-1|Pentax K1000 with 50mm Lens|slr|1976|35mm SLR · Pentax K mount · fully mechanical|The Pentax K1000 is the camera generations of photography students learned on: fully mechanical, built like a tank and simple enough to master in an afternoon.
develop-scan-ecn-2-motion-picture-film|Develop & Scan ECN-2 Motion Picture Film|service||ECN-2 cinema film guide|
nikon-fe2|Nikon FE2|slr|1983|35mm SLR · Nikon F mount (AI) · 1/4000s shutter|
vivitar-big-view-bv35|Vivitar Big View BV35|ps|1990s|35mm · large viewfinder|
canon-canonet-ql-17-giii-1|Canon Canonet QL17 GIII|ps|1972|35mm rangefinder · 40mm f/1.7|The Canonet QL17 GIII is the classic compact rangefinder with a fast 40mm f/1.7 lens.
hasselblad-503cx|Hasselblad 503CX with Distagon 60mm|mf|1988|6×6 medium format SLR · V-system|
canon-powershot-a550|Canon PowerShot A550|digital|2007|7.1MP digital compact · 4× zoom|
nikon-fg-1982|Nikon FG (1982)|slr|1982|35mm SLR · Nikon F mount · program|
nikon-em|Nikon EM|slr|1979|35mm SLR · Nikon F mount · aperture-priority|
polaroid-600-impulse-instant-camera|Polaroid 600 Impulse|instant|1988|Polaroid 600 film · fixed focus|
mamiyasekor-msx-500|Mamiya/Sekor MSX 500|slr|1974|35mm SLR · M42 mount|
canon-canonet-28|Canon Canonet 28|ps|1971|35mm rangefinder · 40mm f/2.8|
olympus-om-10-with-50mm-lens-black|Olympus OM-10 with 50mm Lens (Black)|slr|1979|35mm SLR · OM mount|
canon-af-35m|Canon AF35M (Sure Shot)|ps|1979|35mm · 38mm f/2.8 · first autofocus Canon compact|
fuji-blimp-inflated|Fujifilm Blimp (Inflatable Collectible)|collect||Inflatable Fujifilm blimp|
nikon-f-with-lens|Nikon F with Lens|slr|1959|35mm SLR · Nikon F mount|
autumn-vintage-strap|Autumn Vintage Camera Strap|strap||Vintage-style camera strap|
quantaray-dakota-rz-2000|Quantaray Dakota RZ 2000|ps|1990s|35mm · zoom · autofocus|
canon-canonet-ql-25|Canon Canonet QL25|ps|1965|35mm rangefinder · 45mm f/2.5|
yashica-zoom-image-70|Yashica Microtec Zoom 70|ps|1990s|35mm · zoom · autofocus|
mamiya-rb67-pro-sd|Mamiya RB67 Pro SD|mf|1990|6×7 medium format SLR · revolving back|
ricoh-kr-10m|Ricoh KR-10M|slr|1984|35mm SLR · Pentax K mount|
nikon-one-touch-zoom|Nikon One Touch Zoom|ps|1990s|35mm · zoom · autofocus|
canon-a35-f-40mm-lens|Canon A35F (Datelux)|ps|1978|35mm rangefinder · 40mm f/2.8 · flash|
minolta-freedom-zoom-160-date|Minolta Freedom Zoom 160 Date|ps|1990s|35mm · 38–160mm zoom · autofocus|
olympus-infinity-super-zoom-300|Olympus Infinity Superzoom 300|ps|1990s|35mm · zoom · autofocus|
joy-of-photography|The Joy of Photography (Kodak)|book|1979|Kodak photography book|
minolta-minoltina-p|Minolta Minoltina-P|ps|1961|35mm viewfinder · Rokkor 45mm f/2.8|
minolta-freedom-zoom-70-ex|Minolta Freedom Zoom 70 EX|ps|1990s|35mm · zoom · autofocus|
minolta-weathermatic-dual-35|Minolta Weathermatic Dual 35|ps|1987|35mm waterproof · dual focal length|
polaroid-photo-magic-system|Polaroid Photo Magic System 2|instant|1990s|Polaroid 600 instant kit|
samsung-maxima-zoom-105|Samsung Maxima Zoom 105|ps|1990s|35mm · 38–105mm zoom · autofocus|
canon-z-135-caption|Canon Sure Shot Z135 Caption|ps|1994|35mm · 38–135mm zoom · caption feature|
nikon-fun-touch-6|Nikon Fun Touch 6|ps|1990s|35mm · focus free|
yashica-j-3|Yashica J-3|slr|1962|35mm SLR · M42 mount|
pentax-iq-zoom-700|Pentax IQZoom 700|ps|1990s|35mm · zoom · autofocus|
canon-lens-fd-50mm-118-chrome-nose|Canon FD 50mm f/1.8 Lens (Chrome Nose)|lens|1971|Canon FD-mount standard lens|
minolta-freedom-gt|Minolta Freedom GT|ps|1990s|35mm · autofocus|
fuji-discovery-800-zoom|Fuji Discovery 800 Zoom|ps|1990s|35mm · zoom · autofocus|
vivitar-357pz-quartz-date|Vivitar 357PZ Quartz Date|ps|1990s|35mm · zoom · autofocus|
contax-t2|Contax T2|ps|1990|35mm · Carl Zeiss Sonnar 38mm f/2.8 · titanium|The Contax T2 is the luxury compact that kicked off the premium point-and-shoot craze.
leather-camera-bag-with-red-stripe|Leather Camera Bag with Red Stripe|bag||Leather camera shoulder bag|
minolta-freedom-zoom-130|Minolta Freedom Zoom 130|ps|1990s|35mm · zoom · autofocus|
mike-tyson-bobby-brown-tote-bag|Mike Tyson & Bobby Brown Tote Bag|tote||Photo-print canvas tote|
canon-snappy-20|Canon Snappy 20|ps|1980s|35mm · fixed focus · flash|
hasselblad-500cm|Hasselblad 500C/M with Distagon 80mm f/2.8|mf|1970|6×6 medium format SLR · V-system|The Hasselblad 500C/M is the definitive modular medium-format camera.
olympus-trip-af-60|Olympus Trip AF 60|ps|1990s|35mm · fixed focus · motor|
35mm-film-canister-b|35mm Film Canister (B)|collect||Empty 35mm film canister|
35mm-film-canister-d|35mm Film Canister Keychain (D)|collect||Film canister keychain|
pentax-me-super-with-50mm-lens|Pentax ME Super with 50mm Lens|slr|1979|35mm SLR · Pentax K mount · aperture-priority & manual|
fuji-discovery-1000-zoom-panorama|Fuji Discovery 1000 Zoom Panorama|ps|1990s|35mm · zoom · panorama|
pentax-me|Pentax ME|slr|1976|35mm SLR · Pentax K mount · aperture-priority|
polaroid-252-bv|Polaroid 252 BV|instant|1990s|Polaroid instant camera|
2002-porsche-911-turbo|2002 Porsche 911 Turbo Print|carprint|2002|Automotive photo print|
kodak-kb-28|Kodak KB 28|ps|1990s|35mm · fixed focus · flash|
nikon-f2-with-50mm-lens|Nikon F2 with 50mm Lens|slr|1971|35mm SLR · Nikon F mount|The Nikon F2 is a fully mechanical professional SLR.
nikon-fe-black|Nikon FE (Black)|slr|1978|35mm SLR · Nikon F mount · aperture-priority|
olympus-stylus-zoom-115|Olympus Stylus Zoom 115|ps|1990s|35mm · 38–115mm zoom · autofocus|
petri-flex-7|Petri Flex 7|slr|1964|35mm SLR · Petri breech-lock mount|
vivitar-ic-100|Vivitar IC 100|ps|1990s|35mm · focus free|
28-85mm-lens|28–85mm Zoom Lens|lens||Standard zoom lens for 35mm SLRs|
agfa-optima-500|Agfa Optima 500|ps|1970s|35mm · auto exposure|
analogue-photography-reference-manual-for-shooting-film|Analogue Photography: Reference Manual for Shooting Film|book|2017|Reference handbook for film photographers|
camera-repair-diagnostic|Camera Repair Diagnostic|service||Camera troubleshooting guide|
canon-af-10|Canon AF-10|ps|1980s|35mm · autofocus|
canon-snappy-lx-ii|Canon Snappy LX II|ps|1990s|35mm · autofocus|
color-film|35mm Colour Film|film||Colour negative film for 35mm cameras|
edward-weston-aperture-masters-of-photography|Edward Weston (Aperture Masters of Photography)|book||Aperture monograph|
gray-cross-body-camera-bag|Gray Cross-Body Camera Bag|bag||Cross-body camera bag|
joel-meyerowitz-red-heads|Joel Meyerowitz: Redheads|book|1991|Photo book|
kareem-abdul-jabbar-rebound|Kareem Abdul-Jabbar Rebound Print|print||Basketball photo print|
kareem-abdul-jabbar-tote-bag|Kareem Abdul-Jabbar Tote Bag|tote||Photo-print canvas tote|
kinon-5050|Kinon 5050|ps|1990s|35mm compact|
kodaks-most-basic-book-of-35mm-photography|Kodak's Most Basic Book of 35mm Photography|book||Beginner photography book|
michael-jordan-breakaway-print|Michael Jordan Breakaway Print|print||Basketball photo print|
michael-jordan-print|Michael Jordan Print|print||Basketball photo print|
nba-tote-bag|NBA Photo Tote Bag|tote||Photo-print canvas tote|
petri-flex-v|Petri Flex V|slr|1960s|35mm SLR · Petri mount|
the-ansel-adams-basic-techniques-of-photography|Ansel Adams: Basic Techniques of Photography|book||Photography technique book|
the-complete-kodak-book-of-photography|The Complete Kodak Book of Photography|book||Photography book|
the-disappearance-of-photography-photography-at-the-end-of-the-analog-era|The Disappearance of Darkness: Photography at the End of the Analog Era|book|2012|Robert Burley photo book|
vivitar-ez-motor|Vivitar EZ Motor|ps|1990s|35mm · motorised|
vivitar-spree-plus|Vivitar Spree Plus|ps|1990s|35mm · focus free|
konica-hi-precision-zoom-compact|Konica Hi-Precision Zoom Compact|ps|1990s|35mm · zoom · autofocus|
nikon-lite-touch-zoom-110-panorama|Nikon Lite Touch Zoom 110 Panorama|ps|1999|35mm · zoom · panorama|
nikon-zoom-touch-600|Nikon Zoom Touch 600|ps|1990s|35mm · zoom · autofocus|
olympus-quick-shooter-tele|Olympus Quick Shooter Tele|ps|1990s|35mm · dual lens|
porsche-progression|Porsche Progression Print|carprint||Automotive photo print|
nikon-nikkormat-black-with-24mm-wide-angle-lens|Nikon Nikkormat (Black) with 24mm Lens|slr|1965|35mm SLR · Nikon F mount|
agfa-silette-sl|Agfa Silette SL|ps|1960s|35mm viewfinder|
black-and-white-film-developing-workshop|Black & White Film Developing Workshop|workshop||Learn to develop B&W film at home|
black-white-film-processing|Black & White Film Processing|service||B&W developing guide|
camera-basics-workshop|Camera Basics Workshop|workshop||Learn film camera basics|
canon-a1-sureshot-panorama|Canon Sure Shot A1 Panorama|ps|1990s|35mm · waterproof|
kareem-abdul-jabbar-post-up|Kareem Abdul-Jabbar Post-Up Print|print||Basketball photo print|
kareem-abdul-jabbar-postup-tote-bag|Kareem Abdul-Jabbar Post-Up Tote Bag|tote||Photo-print canvas tote|
kodak-pocket-guide-to-point-amp-shoot-photography|Kodak Pocket Guide to Point & Shoot Photography|book||Pocket photography guide|
kodak-pocket-guide-to-travel-photography|Kodak Pocket Guide to Travel Photography|book||Pocket photography guide|
kodak-s300md|Kodak S300MD|ps|1980s|35mm · motor drive|
konica-z-up-140-super|Konica Z-Up 140 Super|ps|1990s|35mm · 38–140mm zoom|
lancia-delta|Lancia Delta Print|carprint||Automotive photo print|
linda-mccartney-sun-prints|Linda McCartney: Sun Prints|book|1989|Photo book|
mercedes-500sl|Mercedes-Benz 500SL Print|carprint||Automotive photo print|
michael-jordan-pose-tote-bag|Michael Jordan Pose Tote Bag|tote||Photo-print canvas tote|
minolta-freedom-tele|Minolta Freedom Tele|ps|1990s|35mm · dual lens|
minolta-hi-matic-s2|Minolta Hi-Matic S2|ps|1978|35mm · Rokkor 38mm f/2.8|
minolta-silver-streak-zoom|Minolta Silver Streak Zoom|ps|1990s|35mm · zoom|
more-joy-of-photography-hard-cover-1|More Joy of Photography (Hardcover)|book|1981|Kodak photography book|
nan-goldin-55s|Nan Goldin (Photofile / 55s)|book||Photo book|
nikon-fg-black-with-50mm-lens|Nikon FG (Black) with 50mm Lens|slr|1982|35mm SLR · Nikon F mount|
nikon-fm-with-50mm-lens|Nikon FM with 50mm Lens|slr|1977|35mm SLR · Nikon F mount · fully mechanical|
paris-dakar-rally|Paris–Dakar Rally Print|carprint||Motorsport photo print|
porsche-carerra|Porsche Carrera Print|carprint||Automotive photo print|
private-film-photography-group-workshop-with-drake-founder-of-relics|Private Film Photography Group Workshop|workshop||Film photography workshop|
robert-capa|Robert Capa (Photo Book)|book||Photo book|
samsung-maxima-1450af|Samsung Maxima 1450AF|ps|1990s|35mm · zoom|
samsung-maxima-60xl|Samsung Maxima 60XL|ps|1990s|35mm · zoom|
shaquille-oneal-overhead|Shaquille O'Neal Overhead Print|print||Basketball photo print|
the-darkroom-book|The Darkroom Book|book||Darkroom technique book|
the-kodak-workshop-series-lenses-for-35mm-photography|Kodak Workshop Series: Lenses for 35mm Photography|book||Photography book|
the-kodak-workshop-series-using-filters|Kodak Workshop Series: Using Filters|book||Photography book|
the-morgan-amp-morgan-darkroom-book|The Morgan & Morgan Darkroom Book|book||Darkroom technique book|
the-practical-zone-system|The Practical Zone System|book||Exposure technique book|
vivitar-pz-3090|Vivitar PZ 3090|ps|1990s|35mm · zoom|
mamiya-c220-professional|Mamiya C220 Professional|mf|1968|6×6 TLR · interchangeable lenses|The Mamiya C220 is the lighter sibling of the C330 — a twin-lens reflex with interchangeable lenses and bellows focusing for close-ups.
joel-meyerowitz-tuscany|Joel Meyerowitz: Tuscany|book|2003|Photo book|
wind-and-water-van-der-wal|Wind and Water (Van der Wal)|book||Photo book|
scan-only|Scan Only (Film Scanning)|service||Film scanning guide|
develop-only|Develop Only (Film Developing)|service||Film developing guide|
mamiya-7-with-80mm-lens|Mamiya 7 with 80mm Lens|mf|1995|6×7 medium format rangefinder · Mamiya N 80mm f/4 · interchangeable lenses|The Mamiya 7 is the lightest 6×7 rangefinder ever made — a big-negative camera you can carry all day. With the sharp N 80mm f/4 lens it produces some of the most detailed images any film camera can make, which is why the Mamiya 7 is a favourite of landscape and travel photographers.
polaroid-pz2001|Polaroid PZ2001|instant|2000|Polaroid 600 film · autofocus · built-in zoom flash|The Polaroid PZ2001 is a late 600-series autofocus instant camera with a zoom lens-style flash, made for crisp, well-exposed Polaroid 600 prints.
premier-pc-80-with-50mm-lens|Premier PC-80 with 50mm Lens|slr|1980s|35mm SLR · K mount · manual focus|The Premier PC-80 is a simple, affordable manual 35mm SLR from the 1980s with a K-mount 50mm lens — a budget-friendly way to learn film photography.
bell-amp-howell-bf-705-big-finder-motor|Bell & Howell BF-705 Big Finder Motor|ps|1980s|35mm · fixed focus · large viewfinder · motor advance|The Bell & Howell BF-705 Big Finder Motor is a motorised 35mm compact with an oversized viewfinder — a fun, simple snapshot camera.
pentax-km-35mm-film-camera-with-50mm-lens|Pentax KM with 50mm Lens|slr|1975|35mm SLR · Pentax K mount · fully mechanical · match-needle|The Pentax KM is the better-equipped sibling of the K1000, with a self-timer and depth-of-field preview in the same mechanical, battery-optional body.
nikon-f-black-35mm-film-camera-with-35-70mm-lens|Nikon F (Black) with 35–70mm Lens|slr|1960s|35mm SLR · Nikon F mount · fully mechanical|A black Nikon F — the professional SLR that defined the genre — paired with a versatile 35–70mm zoom.
werra|Carl Zeiss Jena Werra|ps|1955|35mm viewfinder · Tessar 50mm f/2.8 · leaf shutter|The Werra is an elegant East German 35mm camera from Carl Zeiss Jena with a sharp Tessar lens and a distinctive minimalist body.
olympus-infinity-zoom-2000|Olympus Infinity Zoom 2000|ps|1990s|35mm · zoom · autofocus · built-in flash|The Olympus Infinity Zoom 2000 is a capable autofocus zoom compact from Olympus's Infinity line — easy to use and great for everyday 35mm film.
olympus-stylus-epic-zoom-170|Olympus Stylus Epic Zoom 170|ps|2003|35mm · 38–170mm zoom · weatherproof · autofocus|The Olympus Stylus Epic Zoom 170 packs a long 38–170mm zoom into a splash-proof pocket body — the longest-reaching Stylus Epic.
kodak-pocket-guide-to-35mm-photography|Kodak Pocket Guide to 35mm Photography|book||Pocket photography guide|
kodak-guide-to-35mm-photography|Kodak Guide to 35mm Photography|book||Classic Kodak photography handbook|
the-kodak-workshop-series-the-art-of-seeing|Kodak Workshop Series: The Art of Seeing|book||Photography composition book|
sony-cyber-shot-dsc-wx350-white|Sony Cyber-shot DSC-WX350 (White)|digital|2014|18MP digital compact · 20× zoom|
black-white-film|35mm Black & White Film|film||Black & white film for 35mm cameras|
35mm-film-canisters-tri-x|35mm Film Canisters (Tri-X)|collect||Kodak Tri-X film canister collectible|
andre-agassi-kissing-net|Andre Agassi Kissing the Net Print|print||Tennis photo print|
michael-jordan-breakaway-tote-bag|Michael Jordan Breakaway Tote Bag|tote||Photo-print canvas tote|
1997-911-carrera-4s|1997 Porsche 911 Carrera 4S Print|carprint|1997|Automotive photo print|
rally-racer-helmet-mud|Rally Racer Helmet (Mud) Print|print||Motorsport photo print|
1997-911-carrera-cabriolet|1997 Porsche 911 Carrera Cabriolet Print|carprint|1997|Automotive photo print|
1997-911-carrera-targa|1997 Porsche 911 Carrera Targa Print|carprint|1997|Automotive photo print|
"""

# Old Shopify slugs that 301 to a better / de-duplicated product URL.
PRODUCT_REDIRECTS = {
    "canon-ae-1-program-2-5p8r3": "canon-ae-1-program",
    "canonn-ae-1-4-2yww6": "canon-ae-1",
    "canon-514xl-super-8-camera-with-original-leather-case-front-and-back-lens-cap": "canon-514xl-super-8-camera",
    "hasselblad-500cm-film-camera-with-carl-zeiss-distagon-t-80mm-f2-8-lens-kit": "hasselblad-500cm",
    "hasselblad-503cx-with-carl-zeiss-distagon-t-60mm-f35-cf-lens-kit": "hasselblad-503cx",
    "polaroid-photo-magic-system-2-instant-film-camera-with-case-and-accessories": "polaroid-photo-magic-system",
    "b656e39woy3lulm7msfl7u7qt2i35w": "vivitar-v3000s",
    "b656e39woy3lulm7msfl7u7qt2i35w-1": "vivitar-v3000s",
    "av092feu5nrxdtgd77c0c9i2yi2ofo": "canon-ftb",
    "fw5exyfck4r7uyp96h5uya7puv3u20": "canon-snappy-20",
    # exact duplicates of another listing
    "minolta-freedom-zoom-105i-1": "minolta-freedom-zoom-105i",
    "nikon-zoom-touch-400-1": "nikon-zoom-touch-400",
    "minolta-freedom-dual-1": "minolta-freedom-dual",
    "pentax-iq-zoom-900": "pentax-iqzoom-900",
    "minolta-hi-matic-af2-2": "minolta-hi-matic-af-2",
    "canon-t50": "canon-t50-with-35-70mm-zoom-lens",
    "canon-snappy-lx-silver": "canon-snappy-lx",
    "canon-sureshot-owl": "canon-sure-shot-owl-date",
    "konica-autoreflex-t3-black": "konica-autoreflex-t3",
    "petri-flex-7-24fte": "petri-flex-7",
    # store-only items with no Amazon equivalent
    "gift-card-50-00": "/collections/gift-guide",
    "gift-card-100-00": "/collections/gift-guide",
    "gift-card-250-00": "/collections/gift-guide",
    "relics-gift-card-1": "/collections/gift-guide",
    "relics-box-logo-sticker": "/collections/accessories",
    "relics-box-logo-tee-white": "/collections/accessories",
    "relics-serif-font-sticker": "/collections/accessories",
    "relics-water-bottle": "/collections/accessories",
    "5kxb28ggrul56uexfcuk9ybe58qt30": "/collections/all-film-cameras",
    "wmq5ptkr88ldtwycgfqgbr88frhiw9": "/collections/all-film-cameras",
    # GSC 404s (Nov 2026 audit)
    "av092feu5nrxdtgd77c0c9i2yi2ofo-35gn4": "canon-ftb", "michael-olympus-stylus-epic-35mm-film-camera": "olympus-stylus",
    "olympus-infinity-zoom-2000-35mm-film-camera": "olympus-infinity-zoom-2000", "olympus-om-10-35mm-film-camera-with-50mm-lens": "olympus-om-10",
    "minolta-x-370-35mm-film-camera-with-50mm-lens-1984": "minolta-x-370", "mamiya-7-with-80mm_lens": "mamiya-7-with-80mm-lens",
    "infinity-superzoom-330": "olympus-infinity-superzoom-330", "konica-autoreflex-t3-silver-35mm-film-camera-with-50mm-1-7-lens": "konica-autoreflex-t3",
    "minolta-freedom-zoom-160": "minolta-freedom-zoom-160-date", "minolta-freedom-zoom-90-35mm-film-camera": "minolta-freedom-zoom-90",
    "olympus-infinity-super-zoom-35mm-film-camera": "olympus-infinity-super-zoom-300", "olympus-infinity-superzoom-300": "olympus-infinity-super-zoom-300",
    "olympus-infinity-super-zoom-300-35mm-film-camera": "olympus-infinity-super-zoom-300", "olympus-stylus-120-35mm-film-camera": "olympus-stylus-120",
    "olympus-stylus-epic-35mm-film-camera": "olympus-stylus", "one-touch-200": "nikon-one-touch-200", "pentax-iqzoom-700": "pentax-iq-zoom-700",
    "polaroid-600-sun-lms-instant-film-camera": "polaroid-600-sun-lms-instant-camera", "polaroid-sun-600-instant-camera": "polaroid-600-sun-lms-instant-camera",
    "polaroid-sun-600-sun-lms-instant-camera": "polaroid-600-sun-lms-instant-camera", "polaroid-one-step-spirit-instant-camera": "polaroid-600-one-step-spirit-instant-camera",
    "powershot-a550": "canon-powershot-a550", "ricoh-kr-10-m": "ricoh-kr-10m", "canon-310xl": "canon-310xl-super-8-camera",
    "polaroid-600-onestep-close-up": "polaroid-600-onestep-close-up-instant-camera", "canon-canonet-ql17-g-iii": "canon-canonet-ql-17-giii-1",
    "ompus-om-10-with-50mm-lens-black": "olympus-om-10-with-50mm-lens-black",
    "basic-camera-cleaning": "/pages/basic-camera-cleaning", "private-1-1-session": "private-film-photography-group-workshop-with-drake-founder-of-relics",
    "most-popular": "/collections/staff-picks", "amlyq0w49uhjzuqp871chowzm29rak": "/collections/all-film-cameras",
    "relics-film-lab-gift-card": "/collections/gift-guide", "gift-card-25-00": "/collections/gift-guide", "gift-card-250-1": "/collections/gift-guide",
    "relics-serif-tee-white": "/collections/accessories", "relics-serif-tee-black": "/collections/accessories", "relics-serif-tee-white-film-camera-t-shirt": "/collections/accessories",
    "relics-serif-tee-black-film-camera-t-shirt": "/collections/accessories", "relics-box-logo-tee-black": "/collections/accessories",
    "relics-box-logo-tee-black-film-camera-t-shirt": "/collections/accessories", "relics-box-logo-tee-white-film-camera-t-shirt": "/collections/accessories",
}


def products():
    out = []
    for line in RAW.strip().splitlines():
        parts = [p.strip() for p in line.split("|")]
        while len(parts) < 6:
            parts.append("")
        slug, name, cat, year, spec, blurb = parts[:6]
        if name == "x":
            continue
        assert cat in CATEGORIES, (slug, cat)
        out.append(dict(slug=slug, name=name, cat=cat, year=year, spec=spec, blurb=blurb))
    slugs = [p["slug"] for p in out]
    assert len(slugs) == len(set(slugs)), "duplicate slug"
    return out
