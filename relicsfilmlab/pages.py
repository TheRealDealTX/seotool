"""Hand-written pages for Relics Film Lab: home, film-lab/service products, info & legal pages."""
import html, os, re
import content as C

STATIC_REDIRECTS = {
    "/404": "/",
    "/relics-film-lab/p/develop-only": "/products/develop-only",
    "/relics-film-lab/p/group-35mm-film-photography-workshops": "/collections/workshops",
    "/collections/polaroid-cameraspolaroid-600-sun-lms-instant-camera": "/products/polaroid-600-sun-lms-instant-camera",
    "/collections/polaroid-cameraspolaroid-600-silver-express-instant-camera": "/products/polaroid-600-silver-express-instant-camera",
    "/collections/allolympus-stylus-35-mm-black": "/products/olympus-stylus-35-mm-black",
    "/collections/all-film-camerasolympus-superzoom-760": "/products/olympus-superzoom-760",
    "/collections/all-film-cameraspetri-flex-7": "/products/petri-flex-7",
    "/pages/film-lab-technician": "/pages/careers",
    "/products": "/collections/all", "/collections": "/collections/all", "/blogs": "/blogs/guides", "/blogs/news": "/blogs/guides",
    "/cart": "/pages/wishlist", "/account": "/", "/account/login": "/", "/search": "/collections/all",
    "/policies/privacy-policy": "/pages/privacy-policy", "/policies/refund-policy": "/pages/returns-exchanges",
    "/policies/shipping-policy": "/pages/store-help", "/policies/terms-of-service": "/pages/terms-of-service",
    "/point-shoot-cameras": "/collections/point-shoot-cameras", "/about": "/pages/about-us", "/contact": "/pages/contact",
    "/gift-cards": "/collections/gift-guide", "/collections/gift-cards": "/collections/gift-guide", "/collections/frontpage": "/collections/all",
    "/collections/ready-to-hang-prints": "/collections/prints", "/collections/camera-repair": "/camera-repairs",
    "/pages/camera-repair": "/camera-repairs", "/pages/film-lab": "/collections/film-lab", "/pages/why-relics": "/pages/the-relics-standard",
}

GIFT_PICKS = ["olympus-trip-35", "olympus-stylus", "canon-ae-1", "minolta-x-700-mps-with-50mm-lens", "polaroid-one-step-land-camera", "polaroid-600-sun-lms-instant-camera",
              "fujifilm-instax-wide-300-instant-film-camera-black-silver", "yashica-mat-124-g", "color-film", "analogue-photography-reference-manual-for-shooting-film",
              "the-ansel-adams-basic-techniques-of-photography", "vintage-kodak-leather-camera-bag", "autumn-vintage-strap", "35mm-film-canister-keychains",
              "michael-jordan-print", "2002-porsche-911-turbo"]

def _kit(items):
    return items

SPECIAL_PRODUCTS = {
    "develop-only": dict(
        q="film developing kit black and white", btn="Shop developing kits on Amazon",
        intro="Develop only means processing your film into negatives without scans or prints. You can send rolls to a lab — or do it yourself at home with a tank, a changing bag and a few bottles of chemistry. Here is how, including 110 and 127 film.",
        body="""<h2>Develop-only at a lab</h2><p>Most labs offer a develop-only price for C-41 colour, black &amp; white and E-6 slide film. You get your negatives back to scan yourself or print in a darkroom. It is the cheapest option if you own a scanner.</p>
<h2>Develop at home in 7 steps</h2><ol><li>Load the film onto a reel inside a changing bag.</li><li>Pour in developer at the right temperature (20 °C for most B&amp;W developers).</li><li>Agitate as the developer's chart says.</li><li>Stop bath (or a water rinse).</li><li>Fixer — after this step the film is safe in light.</li><li>Wash, then a drop of wetting agent.</li><li>Hang to dry in a dust-free room.</li></ol>
<p>Colour (C-41) is just as doable with a kit — it simply needs warmer, carefully held temperatures. See our full guide: <a href="/blogs/guides/how-to-develop-film-at-home">how to develop film at home</a>.</p>
<h2>110, 127 and odd formats</h2><p>Can you develop 110 film or 127 film? Yes. 127 loads on adjustable reels set to its width, and 110 fits the 16mm setting on many reels. If you would rather a lab handle it, read <a href="/blogs/guides/where-to-develop-110-127-and-old-film">where to develop 110, 127 and old film</a>.</p>""",
        kit=[("Paterson developing tank & reels", "Paterson universal developing tank"), ("Changing bag", "film changing bag"), ("Ilford ID-11 / D-76 developer", "Kodak D-76 developer"),
             ("Ilford Rapid Fixer", "Ilford rapid fixer"), ("C-41 colour kit", "C-41 color developing kit"), ("Film clips for drying", "film drying clips")],
        faq=[("What does develop only mean?", "The lab processes your film into negatives but does not scan or print them. You get the negatives back."),
             ("Where can you develop 110 film?", "Many mail-in labs still process 110 C-41 film; ask whether they can scan it, as 110 needs special holders. You can also develop it yourself on an adjustable reel."),
             ("Can I develop 127 film at home?", "Yes — 127 film fits adjustable plastic reels and develops exactly like 120 black & white or C-41."),
             ("Is developing film at home cheaper?", "For black & white, very much so: a starter kit pays for itself in roughly 10 rolls.")]),
    "scan-only": dict(
        q="35mm film scanner", btn="Shop film scanners on Amazon",
        intro="Already have negatives? Scanning them yourself gives you full control of colour and sharpness. These are the scanners and DIY camera-scanning setups we recommend for 35mm and 120.",
        body="""<h2>Three ways to scan film</h2><ol><li><strong>Dedicated film scanner</strong> — simple, consistent and great for 35mm.</li><li><strong>Flatbed with film holders</strong> — the most affordable way to scan 120 medium format.</li><li><strong>Camera scanning</strong> — a digital camera, a macro lens, a light panel and a film holder. Fastest and highest quality once set up.</li></ol>
<h2>Tips for better scans</h2><ul><li>Clean negatives with a blower before scanning — never wipe them dry.</li><li>Use a high-CRI light source for accurate colour.</li><li>Scan in RAW or 16-bit TIFF and invert with dedicated software for the best colour negatives.</li></ul>""",
        kit=[("Dedicated 35mm film scanner", "35mm film scanner"), ("Epson flatbed photo scanner", "Epson Perfection photo scanner film"), ("LED light panel (high CRI)", "high CRI LED light pad film"),
             ("35mm film holder for camera scanning", "35mm negative film holder digitizing"), ("Anti-static gloves & blower", "anti static film cleaning gloves")]),
    "black-white-film-processing": dict(
        q="black and white film developing kit", btn="Shop B&W developing kits",
        intro="Black & white film is the easiest film to process yourself — no strict temperatures, cheap chemistry and wonderful results. Here is everything you need for black & white film processing at home.",
        body="""<h2>What you need</h2><ul><li>A daylight developing tank with reels</li><li>A changing bag (or a truly dark room)</li><li>Developer (Ilford ID-11, Kodak D-76 or HC-110), stop bath, fixer</li><li>A thermometer, measuring jugs and film clips</li></ul><h2>Classic developer times at 20 °C</h2>
<table><tr><th>Film</th><th>Developer</th><th>Time</th></tr><tr><td>Ilford HP5 Plus 400</td><td>ID-11 stock</td><td>7.5 min</td></tr><tr><td>Kodak Tri-X 400</td><td>D-76 stock</td><td>6.75 min</td></tr><tr><td>Ilford FP4 Plus 125</td><td>ID-11 stock</td><td>8.5 min</td></tr></table>
<p class="note">Always confirm times against the manufacturer's current data sheet.</p><p>Step-by-step instructions are in our <a href="/blogs/guides/how-to-develop-film-at-home">home developing guide</a>.</p>""",
        kit=[("Paterson tank & 2 reels", "Paterson super system 4 tank"), ("Kodak D-76 developer", "Kodak D-76 developer"), ("Ilford ID-11 developer", "Ilford ID-11"), ("Ilford Rapid Fixer", "Ilford rapid fixer"), ("Ilford HP5 Plus 35mm", "Ilford HP5 Plus 35mm film")]),
    "develop-scan-ecn-2-motion-picture-film": dict(
        q="Kodak Vision3 35mm film", btn="Shop cinema film on Amazon",
        intro="ECN-2 is the process for Kodak Vision3 motion-picture film — the stock behind most film-shot movies. Shooting it in a still camera gives a gorgeous cinematic look. Here is what ECN-2 means and how to develop it.",
        body="""<h2>What is ECN-2?</h2><p>ECN-2 is the colour negative process used for motion-picture stocks such as Kodak Vision3 50D, 250D and 500T. Vision3 has a carbon <em>remjet</em> backing that must be removed during processing.</p>
<h2>Your options</h2><ul><li><strong>A lab that runs ECN-2</strong> — the best results with proper remjet removal.</li><li><strong>At home</strong> — ECN-2 kits are available; a pre-bath in a borax solution softens remjet so it can be wiped away.</li><li><strong>C-41 cross-processing</strong> — possible but gives colour shifts and risks contaminating a lab's machine; only do it at home with remjet removed first.</li></ul>""",
        kit=[("Kodak Vision3 250D 35mm", "Kodak Vision3 250D 35mm film"), ("Kodak Vision3 500T 35mm", "Kodak Vision3 500T 35mm film"), ("ECN-2 developing kit", "ECN-2 developing kit"), ("Developing tank & reels", "Paterson developing tank")],
        faq=[("What is ECN-2 film?", "Motion-picture colour negative film, such as Kodak Vision3, developed in the ECN-2 process."), ("Can I develop ECN-2 film in C-41?", "It can be done at home after removing the remjet layer, but colours shift and most labs won't accept it in their C-41 machines.")]),
    "4x6-prints-individual": dict(
        q="photo printer 4x6", btn="Shop 4x6 photo printers",
        intro="4×6 prints are the classic photo-album size. Here is how to get great prints from your film scans — at home, or from a print service — plus frames and albums to put them in.",
        body="""<h2>Printing film scans</h2><ul><li>Export at 1800 × 1200 pixels or more (300 dpi at 6 × 4 inches).</li><li>Match the 3:2 ratio of 35mm so nothing gets cropped.</li><li>Calibrate your screen, or print a test sheet first.</li></ul><h2>Home printing</h2><p>Compact dye-sublimation printers make durable 4×6 prints in about a minute and are perfect for parties and travel.</p>""",
        kit=[("4×6 photo printer", "4x6 photo printer dye sublimation"), ("4×6 photo paper", "4x6 glossy photo paper"), ("Photo album for 4×6", "photo album 4x6 600 photos"), ("4×6 picture frames", "4x6 picture frames set")]),
    "camera-repair-diagnostic": dict(
        q="camera repair tool kit", btn="Shop camera repair tools",
        intro="Not sure what is wrong with your film camera? Work through our diagnostic checklist before paying for a repair — many faults are dead batteries, dirty contacts or tired light seals.",
        body="""<h2>Five-minute camera diagnostic</h2><ol><li><strong>Fresh battery</strong> — and clean the contacts with a pencil eraser or isopropyl alcohol.</li><li><strong>Shutter</strong> — open the back, fire at 1 second and 1/500: you should see a clear difference.</li><li><strong>Light seals</strong> — sticky black foam around the door means light leaks; replacement kits are cheap.</li><li><strong>Lens</strong> — shine a torch through it to spot haze or fungus.</li><li><strong>Meter</strong> — compare readings with a phone light-meter app.</li></ol><p>For anything beyond that, read our <a href="/camera-repairs">camera repair guide</a>.</p>""",
        kit=[("Precision screwdriver set", "precision screwdriver set camera"), ("Light seal replacement kit", "camera light seal foam kit"), ("Lens spanner wrench", "lens spanner wrench"), ("Isopropyl alcohol 99%", "99% isopropyl alcohol"), ("Lens cleaning kit", "camera lens cleaning kit")]),
    "color-film": dict(
        q="35mm color film", btn="Shop 35mm colour film",
        intro="Colour negative film is the place to start: it is forgiving, widely available and developed by every lab. These are the 35mm colour films we load most often, from budget to professional.",
        body="""<h2>Which colour film should I buy?</h2><table><tr><th>Film</th><th>Speed</th><th>Best for</th></tr><tr><td>Kodak Gold 200</td><td>200</td><td>Sunny days, warm nostalgic colour</td></tr><tr><td>Kodak UltraMax 400</td><td>400</td><td>All-round, point-and-shoots</td></tr><tr><td>Fujifilm 400</td><td>400</td><td>Cooler greens and blues</td></tr><tr><td>Kodak Portra 400</td><td>400</td><td>Skin tones, weddings, portraits</td></tr><tr><td>Kodak Ektar 100</td><td>100</td><td>Landscapes, saturated colour</td></tr><tr><td>CineStill 800T</td><td>800</td><td>Night, neon, tungsten light</td></tr></table>
<p>Store film in the fridge and let it warm to room temperature before loading.</p>""",
        kit=[("Kodak Gold 200 (3-pack)", "Kodak Gold 200 35mm 3 pack"), ("Kodak UltraMax 400", "Kodak UltraMax 400 35mm"), ("Kodak Portra 400", "Kodak Portra 400 35mm film"), ("Kodak Ektar 100", "Kodak Ektar 100 35mm"), ("CineStill 800T", "CineStill 800T 35mm")],
        faq=[("What is the best 35mm colour film for beginners?", "Kodak Gold 200 in good light or Kodak UltraMax 400 for everything else — both are affordable and forgiving."), ("Does film expire?", "Yes. Keep it cool; expired film still works but needs extra exposure — roughly one stop per decade.")]),
    "black-and-white-film-developing-workshop": dict(
        q="black and white film developing kit", btn="Get the workshop kit",
        intro="Our Black &amp; White Film Developing Workshop, as a self-guided lesson. In one evening you will learn to load a reel in the dark, mix chemistry and develop your first roll at home.",
        body="""<h2>The lesson plan</h2><ol><li>Practise loading a reel in daylight with a sacrificial roll, then with your eyes closed.</li><li>Load your real film in a changing bag.</li><li>Mix developer, stop and fixer; bring everything to 20 °C.</li><li>Develop, stop, fix, wash and hang to dry.</li><li>Scan or contact-print your negatives.</li></ol><p>Full instructions: <a href="/blogs/guides/how-to-develop-film-at-home">how to develop film at home</a>.</p>""",
        kit=[("Paterson tank & reels", "Paterson developing tank"), ("Changing bag", "film changing bag"), ("Kodak D-76", "Kodak D-76 developer"), ("Ilford Rapid Fixer", "Ilford rapid fixer"), ("Ilford HP5 Plus", "Ilford HP5 Plus 35mm film"), ("Darkroom thermometer", "darkroom thermometer")]),
    "camera-basics-workshop": dict(
        q="beginner film camera kit", btn="Shop beginner kits",
        intro="The Camera Basics Workshop, self-guided: how to load film, read a light meter and understand aperture, shutter speed and ISO — the foundation of every great photograph.",
        body="""<h2>The exposure triangle in five minutes</h2><ul><li><strong>Aperture</strong> (f-number) controls how much is in focus.</li><li><strong>Shutter speed</strong> controls motion blur.</li><li><strong>Film speed</strong> (ISO) is fixed by the roll you load.</li></ul><p>Start with the <strong>Sunny 16 rule</strong>: in bright sun, at f/16, use a shutter speed of 1/ISO.</p><h2>Practice assignment</h2><ol><li>Load a 36-exposure roll of 400-speed film.</li><li>Shoot the same scene at three apertures.</li><li>Shoot a moving subject at 1/30, 1/125 and 1/500.</li><li>Note every setting, then compare when your scans come back.</li></ol>""",
        kit=[("Pentax K1000 or similar 35mm SLR", "Pentax K1000 film camera"), ("Handheld light meter", "handheld light meter photography"), ("Ilford HP5 Plus 400", "Ilford HP5 Plus 35mm film"), ("Kodak's beginner books", "Kodak photography book beginner")]),
    "private-film-photography-group-workshop-with-drake-founder-of-relics": dict(
        q="film photography book beginners", btn="Shop learning resources",
        intro="Our founder Drake's private group workshops were where many Long Beach photographers shot their first roll. They have moved online as free guides — here is the curriculum and the gear we used.",
        body="""<h2>The curriculum</h2><ol><li><a href="/products/camera-basics-workshop">Camera basics</a>: loading, metering, exposure.</li><li>Composition walk: shoot a full roll with one rule each frame.</li><li><a href="/products/black-and-white-film-developing-workshop">Developing your roll</a> at home.</li><li>Scanning and editing: <a href="/products/scan-only">our scanning guide</a>.</li></ol><p>Questions about a private session? Email <a href="mailto:info@relicsfilmlab.com">info@relicsfilmlab.com</a>.</p>""",
        kit=[("Analogue Photography reference manual", "Analogue Photography reference manual shooting film"), ("Ilford HP5 Plus", "Ilford HP5 Plus 35mm film"), ("Developing starter kit", "black and white film developing kit")]),
}

COLLECTION_EXTRA = {
    "point-shoot-cameras": dict(body="""<h2>How to choose a point and shoot film camera</h2><ul><li><strong>Fixed lens or zoom?</strong> Fixed-lens compacts like the Olympus Stylus Epic or Nikon L35AF usually have faster, sharper lenses. Zooms are more flexible but darker.</li><li><strong>Batteries:</strong> most 90s compacts use CR123A or CR2 lithium cells — easy to find.</li><li><strong>Flash override:</strong> look for a flash-off mode if you shoot at night.</li></ul><p>See our full ranking: <a href="/blogs/guides/best-point-and-shoot-film-cameras">the best point and shoot film cameras</a>.</p>""",
        faq=[("What makes a great point and shoot film camera?", "A sharp lens, reliable autofocus, a flash you can switch off and common batteries."), ("Are point and shoot film cameras worth it?", "Yes — they are the easiest way to shoot film, and the best ones produce results to rival SLRs.")]),
    "slr-cameras": dict(body="""<h2>Picking your first 35mm SLR</h2><p>For learning, we recommend a mechanical or semi-automatic body with a 50mm lens: the <a href="/products/pentax-k-1000-with-50mm-lens-1">Pentax K1000</a>, <a href="/products/canon-ae-1">Canon AE-1</a>, <a href="/products/minolta-x-700-mps-with-50mm-lens">Minolta X-700</a> or <a href="/products/olympus-om-10">Olympus OM-10</a>. All have huge, affordable lens ecosystems.</p>""",
        faq=[("What is the best 35mm SLR for beginners?", "The Pentax K1000, Canon AE-1 Program and Minolta X-700 are the classic choices: simple, robust and well supported."), ("Do vintage SLRs need batteries?", "Most need a small battery for the light meter; fully mechanical cameras like the K1000 and Nikon FM still fire without one.")]),
    "polaroid-cameras": dict(body="""<h2>Which film does my Polaroid take?</h2><table><tr><th>Camera type</th><th>Film</th></tr><tr><td>600 cameras (Sun 600, Spirit, Impulse, OneStep 600)</td><td>Polaroid 600</td></tr><tr><td>SX-70 type (OneStep Land Camera, Pronto)</td><td>Polaroid SX-70 (or 600 with ND filter)</td></tr><tr><td>Fujifilm Instax Wide</td><td>Instax Wide</td></tr></table>""",
        faq=[("Do they still make Polaroid cameras?", "Yes — Polaroid makes new cameras and fresh film for both vintage 600 and SX-70 cameras."), ("Where can I buy Polaroid camera film?", "Polaroid 600, SX-70 and i-Type film are sold on Amazon and in camera stores; check which type your camera takes first.")]),
    "medium-format-cameras": dict(body="""<h2>Cheap medium format film cameras</h2><p>The most affordable route into 120 film is a twin-lens reflex such as the <a href="/products/yashica-mat-124-g">Yashica Mat-124 G</a>, or a Soviet SLR like the <a href="/products/kiev-6c-with-65mm-lens">Kiev 6C</a>. Studio favourites like the <a href="/products/mamiya-rb67-pro-sd">Mamiya RB67</a> and <a href="/products/hasselblad-500cm">Hasselblad 500C/M</a> cost more but are fully modular.</p><h3>Negative sizes</h3><ul><li>6×4.5 — 15–16 frames per roll</li><li>6×6 — 12 frames</li><li>6×7 — 10 frames</li></ul>""",
        faq=[("What film does a medium format camera use?", "120 roll film (some older cameras use 220 or 620)."), ("Is medium format better than 35mm?", "The larger negative gives more detail and smoother tones, at the cost of fewer frames per roll and bigger cameras.")]),
    "super-8-collections": dict(body="""<h2>What to look for in a Super 8 camera</h2><ul><li>An <strong>XL</strong> (existing light) lens and shutter for low light.</li><li>Reliable <strong>auto exposure</strong> — many cameras read the cartridge's notch for film speed.</li><li>24 fps for a smoother, more cinematic look; 18 fps to stretch a cartridge.</li></ul><p>Planning a wedding film? Read <a href="/blogs/guides/the-ultimate-guide-to-shooting-super-8-for-weddings-a-relics-film-lab-manual">our Super 8 wedding guide</a>.</p>""",
        faq=[("Is Super 8 film still made?", "Yes. Kodak manufactures Vision3 50D, 200T and 500T colour negative and Tri-X black & white Super 8 cartridges."), ("How long is a Super 8 cartridge?", "50 feet — about 3 minutes 20 seconds at 18 fps or 2 minutes 30 seconds at 24 fps.")]),
    "all-film-cameras": dict(body="""<h2>Old cameras worth buying today</h2><p>Some old film cameras are collectors' pieces; most are excellent working tools. If it can still take a film that is made today — 35mm, 120, Polaroid, Instax, Super 8 or 110 — it can still make beautiful pictures. Old movie cameras and reel cameras are covered in our <a href="/collections/super-8-collections">Super 8 collection</a>.</p>""",
        faq=[("Can old film cameras still be used?", "Yes, as long as film for their format is still made. 35mm, 120, Polaroid and Super 8 film are all in production."), ("What is a CLA?", "A clean, lube and adjust — a service that restores an old camera's shutter, meter and controls.")]),
    "film-lab": dict(top="", body="""<h2>From the Long Beach film lab</h2><p>For years Relics ran a professional film lab in Long Beach, developing and scanning rolls from across the US. Our <a href="/film-services">film services guide</a> shares what we learned — how to send film to a lab, what to ask for, and how to get lab-quality results at home.</p>""",
        faq=[("Is Relics still a film store in Long Beach?", "Relics began as a Long Beach film lab and camera shop. Today Relics Film Lab is an online guide and curated shop: we recommend gear and link to Amazon, and we no longer process film in person."), ("Where can I develop film?", 'See <a href="/order-now">where to develop film</a> for mail-in and local options.')]),
}

# ------------------------------------------------------------------ simple info pages
def info_pages(ctx):
    site_img, amz_link, ICON = ctx["site_img"], ctx["amz_link"], ctx["ICON"]
    P = {}
    P["/pages/about-us"] = ("About Relics Film Lab — Long Beach Film Lab & Camera Shop", "About <em>Relics</em>",
        "Relics Film Lab began as a film lab and vintage camera shop in Long Beach, California. Here is our story and what we do today.", "darkroom",
        """<h2>Long Beach born</h2><p>Relics started as a small film lab and camera shop in Long Beach, California, run by people who simply loved film. We developed rolls on Noritsu processors, scanned them on Fujifilm Frontier scanners, refurbished vintage cameras by hand and taught workshops to anyone who wanted to learn.</p>
<p>Somewhere along the way thousands of photographers bought their first camera from us, sent us their first roll or sat in on a Saturday developing class.</p>
<h2>What Relics Film Lab is today</h2><p>Relics Film Lab is now an online film photography shop and guide. We still choose every camera and product ourselves and write about it honestly — what it does well, what to check and which film to load — but instead of holding stock, we link to the best current listings on Amazon. You get Amazon's checkout, delivery and returns; we keep doing the part we love: helping people shoot film.</p>
<h2>Our promise</h2><ul><li>We only feature gear we would use ourselves.</li><li>We tell you what can go wrong with a used camera, not just what goes right.</li><li>Recommendations are never paid for by brands. As an Amazon Associate we earn from qualifying purchases, which keeps the guides free.</li></ul>
<p>Say hello any time: <a href="mailto:info@relicsfilmlab.com">info@relicsfilmlab.com</a>.</p>""")
    P["/pages/the-relics-standard"] = ("The Relics Standard — Why Shop With Relics?", "The Relics <em>standard</em>",
        "Why Relics? How we choose film cameras, what we check, and why we send you to Amazon to buy.", "photographer",
        """<h2>Every recommendation earns its place</h2><p>When we ran our shop, every camera went through a bench test before it went on sale. The same thinking guides what we feature now.</p>
<div class="steps"><div class="step"><h3>Proven designs</h3><p>We feature cameras with a track record: sharp lenses, reliable shutters and parts or repairers still available.</p></div>
<div class="step"><h3>Film you can buy</h3><p>Every camera we list takes a film that is in production today — no dead formats sold as working cameras.</p></div>
<div class="step"><h3>Honest checklists</h3><p>Each product page tells you what to inspect when your camera arrives, so you can return a dud quickly.</p></div>
<div class="step"><h3>Protected checkout</h3><p>You buy on Amazon, covered by its A-to-z Guarantee and return policy.</p></div></div>
<h2>Why Amazon?</h2><p>Vintage cameras are one-of-a-kind items. Rather than keep a small shelf of stock, we link to Amazon's live marketplace so you can compare condition, price and seller ratings across many listings at once — and get fast shipping and simple returns.</p>""")
    P["/pages/contact"] = ("Contact Relics Film Lab", "Get in <em>touch</em>",
        "Contact Relics Film Lab: questions about film cameras, film, developing or a product guide. Email info@relicsfilmlab.com.", "film-rolls",
        f"""<p class="lede">Questions about a camera, a roll of film or one of our guides? We read every email.</p>
<p><a class="btn" href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
<h2>Before you write</h2><ul><li><strong>Order questions</strong> — orders are placed on Amazon, so shipping, returns and refunds are handled through <a href="https://www.amazon.com/gp/css/order-history" rel="nofollow noopener" target="_blank">your Amazon orders page</a>.</li>
<li><strong>Camera help</strong> — tell us the make and model and what it is doing (or not doing). Our <a href="/products/camera-repair-diagnostic">diagnostic checklist</a> solves many issues.</li>
<li><strong>Press &amp; partnerships</strong> — we are happy to hear from labs, repairers and makers.</li></ul>""")
    P["/pages/faqs"] = ("Relics Film Lab FAQs", "Frequently asked <em>questions</em>",
        "Answers about Relics Film Lab: how ordering through Amazon works, returns, Long Beach, film developing and choosing a camera.", "negatives", "")
    P["/pages/returns-exchanges"] = ("Returns & Exchanges", "Returns &amp; <em>exchanges</em>",
        "How returns work for products bought through Relics Film Lab links on Amazon.", "film-rolls",
        """<p class="lede">Everything you buy through Relics Film Lab is sold and shipped by Amazon or independent sellers on Amazon, so returns are handled there.</p>
<ol><li>Go to <a href="https://www.amazon.com/gp/css/order-history" rel="nofollow noopener" target="_blank">Your Orders</a> on Amazon.</li><li>Select the item and choose <em>Return or replace items</em>.</li><li>Follow the instructions for the seller's return policy.</li></ol>
<p>Most items can be returned within 30 days. Third-party sellers set their own policies but are covered by Amazon's <strong>A-to-z Guarantee</strong> if an item doesn't arrive or isn't as described.</p>
<h2>Test your camera straight away</h2><p>Use the checklist on each product page the day your camera arrives, and shoot a test roll quickly so you are within the return window.</p>""")
    P["/pages/store-help"] = ("Store Help — Ordering, Shipping & Amazon", "Store <em>help</em>",
        "How shopping with Relics Film Lab works: browsing, ordering on Amazon, shipping, returns and wishlists.", "point-shoot",
        """<h2>How ordering works</h2><div class="steps"><div class="step"><h3>Browse</h3><p>Explore our collections and guides to find the right camera or film.</p></div><div class="step"><h3>Shop on Amazon</h3><p>Tap “Shop on Amazon” to see live listings, prices and conditions.</p></div><div class="step"><h3>Checkout</h3><p>Amazon (or its seller) handles payment, shipping, tracking and returns.</p></div></div>
<h2>Shipping</h2><p>Delivery speed and cost depend on the seller and your Amazon account (Prime items ship fastest).</p><h2>Wishlist</h2><p>Tap the heart on any product to save it to your <a href="/pages/wishlist">wishlist</a> — it's stored in your browser.</p><h2>Prices</h2><p>We don't show prices because vintage listings change constantly; Amazon always shows the current price.</p>""")
    P["/pages/careers"] = ("Careers at Relics Film Lab", "Work with <em>Relics</em>",
        "Careers at Relics Film Lab: writers, photographers and camera technicians who love film.", "workshop",
        f"""<p class="lede">We are a small team, but we're always glad to hear from people who love film.</p><h2>Who we'd like to hear from</h2><ul><li><strong>Writers &amp; reviewers</strong> who shoot film and can explain gear clearly.</li><li><strong>Photographers</strong> with film work we could feature in guides.</li><li><strong>Camera technicians</strong> who might contribute repair guides.</li></ul><p>Send a short note and links to your work to <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.</p>""")
    P["/pages/basic-camera-cleaning"] = ("Basic Camera Cleaning: How to Clean a Film Camera", "Basic camera <em>cleaning</em>",
        "How to clean a film camera safely: lenses, viewfinders, film chambers, battery contacts and light seals — with the tools we use.", "repair",
        f"""<p class="lede">A gentle clean makes a used camera look, feel and work better. Here is the routine we used on every camera at the Relics bench.</p>
<h2>What you need</h2><ul><li>A rocket air blower (never canned air inside a camera)</li><li>A soft lens brush and microfibre cloth</li><li>Lens cleaning fluid and tissue</li><li>Cotton swabs and 99% isopropyl alcohol</li><li>A pencil eraser for battery contacts</li></ul>
<h2>Step by step</h2><ol><li><strong>Outside:</strong> wipe the body with a barely damp cloth; use a swab in the crevices.</li><li><strong>Film chamber:</strong> blow out dust and film chips. Don't touch the shutter curtains.</li><li><strong>Lens:</strong> blow, brush, then a drop of fluid on tissue — wipe in circles from the centre out.</li><li><strong>Viewfinder:</strong> clean the eyepiece only; leave the mirror and focusing screen to a pro.</li><li><strong>Battery contacts:</strong> rub with an eraser, then alcohol on a swab.</li><li><strong>Light seals:</strong> if the foam is sticky or crumbly, replace it with a seal kit.</li></ol>
<div class="kit" style="max-width:520px">{amz_link("Rocket air blower <span>Amazon →</span>", "Giottos rocket air blower", "")}{amz_link("Lens cleaning kit <span>Amazon →</span>", "camera lens cleaning kit", "")}{amz_link("Light seal replacement kit <span>Amazon →</span>", "camera light seal foam kit", "")}{amz_link("99% isopropyl alcohol <span>Amazon →</span>", "99% isopropyl alcohol", "")}</div>""")
    P["/pages/affiliate-disclosure"] = ("Affiliate Disclosure", "Affiliate <em>disclosure</em>", "Relics Film Lab affiliate disclosure for the Amazon Associates program.", "film-rolls",
        """<p>Relics Film Lab is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com.</p><p>As an Amazon Associate we earn from qualifying purchases. When you click a “Shop on Amazon” button or another product link and make a purchase, we may receive a commission at no additional cost to you.</p><p>Prices and availability are accurate as of the time displayed on Amazon and are subject to change. Any price and availability information displayed on Amazon at the time of purchase will apply. Our recommendations are our own and are not paid for by manufacturers.</p>""")
    P["/pages/privacy-policy"] = ("Privacy Policy", "Privacy <em>policy</em>", "Relics Film Lab privacy policy: what we collect (very little), how wishlists stay in your browser and how Amazon affiliate links work.", "film-rolls",
        f"""<p>Last updated {ctx['TODAY']}.</p><p>Relics Film Lab (“we”) respects your privacy. This site does not require an account and we do not sell personal information.</p><h2>What we collect</h2><ul><li><strong>Wishlist:</strong> saved in your own browser (localStorage); it never reaches our servers.</li><li><strong>Email:</strong> if you email us, we use your address only to reply.</li><li><strong>Server logs:</strong> our host keeps standard access logs for security.</li></ul><h2>Amazon and third parties</h2><p>When you follow a link to Amazon, Amazon may set cookies to attribute purchases to our affiliate tag. Amazon's privacy notice applies on its site. Fonts are served by Google Fonts.</p><h2>Contact</h2><p><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>""")
    P["/pages/terms-of-service"] = ("Terms of Service", "Terms of <em>service</em>", "Relics Film Lab terms of service covering use of our guides, photo licences and purchases made from sellers on Amazon.", "film-rolls",
        f"""<p>Last updated {ctx['TODAY']}.</p><p>By using relicsfilmlab.com you agree to these terms. Content is provided for general information; we work to keep it accurate but can't guarantee it. Products are sold by Amazon and third-party sellers, whose terms govern your purchase. Photos are used under the licences listed on our <a href="/pages/photo-credits">photo credits</a> page. All other content © Relics Film Lab. Questions: <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.</p>""")
    return P

FAQ_MAIN = [
    ("What is Relics Film Lab?", "Relics Film Lab is a film photography shop and guide that started as a film lab and camera store in Long Beach, California. We curate film cameras, film and lab gear and link you to the best current listings on Amazon."),
    ("Do you sell cameras directly?", "No. Every “Shop on Amazon” button takes you to Amazon, where you buy from Amazon or an independent seller with Amazon's checkout, shipping and returns."),
    ("Are you still a film lab or camera store in Long Beach?", "Relics was born in Long Beach and ran a film lab and camera shop there. Today we operate online and no longer process film or take walk-ins; our film services guide points you to great labs and home-developing kits."),
    ("How do returns work?", 'Returns go through your Amazon account. See <a href="/pages/returns-exchanges">returns &amp; exchanges</a>.'),
    ("Why don't you show prices?", "Vintage camera listings change daily, so we let Amazon show the live price, condition and seller rating."),
    ("Where should I develop my film?", 'Read <a href="/order-now">where to develop film</a> or learn to <a href="/blogs/guides/how-to-develop-film-at-home">develop film at home</a>.'),
    ("What camera should I buy first?", 'For fully automatic, try an <a href="/products/olympus-stylus">Olympus Stylus Epic</a> or <a href="/products/olympus-trip-35">Olympus Trip 35</a>. To learn manual exposure, a <a href="/products/pentax-k-1000-with-50mm-lens-1">Pentax K1000</a> or <a href="/products/canon-ae-1">Canon AE-1</a>.'),
    ("How can I contact you?", f'Email <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>.'),
]

def build_pages(ctx):
    write, crumbs, phero, site_img, faq_html, esc, amz_link, ICON, grid, BY = (ctx[k] for k in ("write", "crumbs", "phero", "site_img", "faq_html", "esc", "amz_link", "ICON", "grid", "BY_SLUG"))
    for path, (title, h1, desc, img, body) in info_pages(ctx).items():
        plain = re.sub("<.*?>", "", html.unescape(h1))
        cr_h, cr_ld = crumbs([(None, esc(plain))])
        schema = [cr_ld]
        if path == "/pages/faqs":
            fh, fld = faq_html(FAQ_MAIN)
            body = fh; schema.append(fld)
        write(path, title, desc, phero(h1, "", cr_h, site_img(img)) + f'<section class="section" style="padding-top:48px"><div class="wrap prose">{body}</div></section>', schema=schema, preload=site_img(img))

    # wishlist (noindex)
    cr_h, cr_ld = crumbs([(None, "Wishlist")])
    write("/pages/wishlist", "Your Wishlist", "Cameras and gear you've saved at Relics Film Lab.",
          phero("Your <em>wishlist</em>", "Saved in this browser only.", cr_h) + '<section class="section" style="padding-top:40px"><div class="wrap" id="wishlist-grid"></div></section>', robots="noindex,follow")

    # photo credits
    rows = []
    for k, c in sorted(ctx["CRED"].items()):
        label = ("Site image: " + k[5:]) if k.startswith("site:") else (BY[k]["name"] if k in BY else k)
        link = ("/products/" + k) if k in BY else None
        rows.append(f'<tr><td>{f"<a href={link!r}>{esc(label)}</a>" if link else esc(label)}</td><td><a href="{esc(c["page"])}" rel="nofollow noopener" target="_blank">{esc(c["title"][:70])}</a></td><td>{esc(c["artist"])}</td><td>{esc(c["license"])}</td></tr>')
    cr_h, cr_ld = crumbs([(None, "Photo Credits")])
    write("/pages/photo-credits", "Photo Credits", "Credits and licences for the photographs used on Relics Film Lab.",
          phero("Photo <em>credits</em>", "Our product photos are real photographs of each camera, shared by photographers under open licences (Creative Commons and public domain) via Wikimedia Commons and Openverse. Thank you to every photographer below.", cr_h)
          + f'<section class="section" style="padding-top:40px"><div class="wrap prose" style="max-width:none"><table><tr><th>Used on</th><th>Photo</th><th>Author</th><th>Licence</th></tr>{"".join(rows)}</table></div></section>', schema=[cr_ld])

    # top-level service pages (old URLs)
    lab = BY.get
    cr_h, cr_ld = crumbs([(None, "Camera Repairs")])
    fh, fld = faq_html([("Is it worth repairing a vintage film camera?", "Usually, yes — a CLA (clean, lube, adjust) on a quality SLR or rangefinder costs less than replacing it and can add decades of life."),
                        ("What is a film camera CLA?", "A clean, lube and adjust: the technician cleans the shutter and mechanism, lubricates where needed and calibrates shutter speeds and meter."),
                        ("Can I fix light leaks myself?", "Yes. Replacing sticky light-seal foam is an easy DIY job with a seal kit, a toothpick and some isopropyl alcohol."),
                        ("Does Relics still repair cameras?", "Our Long Beach repair bench has closed, but this guide shares the diagnostics we used and how to find a good repairer.")])
    write("/camera-repairs", "Vintage Camera Repair Guide — Film Camera CLA & Fixes", "Vintage camera repair: diagnose common film camera faults, DIY fixes like light seals and batteries, and when to send a camera for a CLA.",
          phero("Vintage camera <em>repair</em>", "Most film camera problems are simpler than they look. Here is the restoration know-how from the Relics repair bench — what you can fix yourself and when to call a pro.", cr_h, site_img("repair"))
          + f"""<section class="section" style="padding-top:48px"><div class="wrap prose">
<h2>Common film camera faults</h2><table><tr><th>Symptom</th><th>Likely cause</th><th>Fix</th></tr>
<tr><td>Dead — nothing works</td><td>Battery or corroded contacts</td><td>New battery, clean contacts</td></tr>
<tr><td>Orange or red streaks on photos</td><td>Light leaks from old foam seals</td><td>DIY light-seal replacement</td></tr>
<tr><td>Shutter stuck or slow</td><td>Dried lubricant</td><td>Professional CLA</td></tr>
<tr><td>Hazy, low-contrast images</td><td>Lens haze or fungus</td><td>Lens cleaning by a technician</td></tr>
<tr><td>Wrong exposures</td><td>Meter drift, wrong battery voltage</td><td>Correct battery or meter calibration</td></tr>
<tr><td>Sticky aperture blades</td><td>Oil on the blades</td><td>Lens service</td></tr></table>
<h2>Start with a diagnostic</h2><p>Run our five-minute <a href="/products/camera-repair-diagnostic">camera repair diagnostic</a> before booking a repair. Then try <a href="/pages/basic-camera-cleaning">basic camera cleaning</a>.</p>
<h2>Finding a repairer</h2><p>Look for a technician who specialises in your brand, publishes turnaround times and offers a warranty on work. Ask for a quote first: if a repair costs more than a replacement body, buying another may make more sense.</p>
<div class="kit" style="max-width:520px">{amz_link("Precision screwdriver set <span>Amazon →</span>", "precision screwdriver set camera", "")}{amz_link("Light seal foam kit <span>Amazon →</span>", "camera light seal foam kit", "")}{amz_link("Lens spanner wrench <span>Amazon →</span>", "lens spanner wrench", "")}</div>
<h2>FAQ</h2>{fh}</div></section>""", schema=[cr_ld, fld], preload=site_img("repair"))

    cr_h, cr_ld = crumbs([(None, "Film Services")])
    fh, fld = faq_html([("What film services does Relics offer?", "Relics ran a professional film lab in Long Beach. Today we publish free guides to developing, scanning and printing film, and recommend the kits to do it at home."),
                        ("What is the difference between C-41, E-6 and B&W?", "C-41 is the process for colour negative film, E-6 for colour slide film, and black & white film uses its own developers. ECN-2 is for motion-picture film."),
                        ("What scanner did the Relics lab use?", "A Fujifilm Frontier SP3000, famous for its warm skin tones, paired with Noritsu processing.")])
    write("/film-services", "Film Services — Developing, Scanning & Printing Guide", "Film developing, scanning and printing explained by the team behind the Relics Long Beach film lab: C-41, black & white, ECN-2 and how to do it at home.",
          phero("Film <em>services</em>", "We spent years developing and scanning film for photographers across the US. Here's the whole process — and how to get lab-quality results yourself.", cr_h, site_img("negatives"))
          + f"""<section class="section" style="padding-top:48px"><div class="wrap">
<div class="steps"><div class="step"><h3><a href="/products/develop-only">Develop only</a></h3><p>Negatives only — at a lab or with a home kit. Includes 110 &amp; 127.</p></div>
<div class="step"><h3><a href="/products/black-white-film-processing">Black &amp; white</a></h3><p>The easiest film to process at home, with developer times.</p></div>
<div class="step"><h3><a href="/products/develop-scan-ecn-2-motion-picture-film">ECN-2 cinema film</a></h3><p>Kodak Vision3 stills with remjet removal.</p></div>
<div class="step"><h3><a href="/products/scan-only">Scanning</a></h3><p>Dedicated, flatbed and camera scanning setups.</p></div>
<div class="step"><h3><a href="/products/4x6-prints-individual">4×6 prints</a></h3><p>Printing your scans at home or through a print service.</p></div></div>
<div class="prose mt"><h2>The Relics signal chain</h2><p>Our lab paired Noritsu processors — consistent temperature and agitation — with a Fujifilm Frontier SP3000 scanner, loved for its golden skin tones and vivid greens. If you send film to a lab, ask which processor and scanner they use and what scan resolution you'll get.</p>
<h2>FAQ</h2>{fh}</div></div></section>""", schema=[cr_ld, fld], preload=site_img("negatives"))

    cr_h, cr_ld = crumbs([(None, "Where to Develop Film")])
    fh, fld = faq_html([("Where can I get film developed near me?", "Search for independent film labs in your area, or use a mail-in lab: pack the rolls in a padded envelope with your order number and ship them."),
                        ("How much does film developing cost?", "Typically $10–$20 per roll for develop and scan in the US, depending on scan resolution."),
                        ("Can I still get disposable cameras developed?", "Yes — any C-41 lab can process disposable cameras; some ask you to send the whole camera."),
                        ("Can I drop off film at Relics?", "Not any more. Relics' Long Beach lab and drop boxes have closed; use a mail-in lab or develop at home.")])
    write("/order-now", "Where to Develop Film: Labs, Mail-In & Home Developing", "Where to develop film in 2026: how mail-in film labs work, what to ask for, costs, and how to develop 35mm, 120 and disposable cameras at home.",
          phero("Where to <em>develop</em> film", "The Relics lab no longer takes orders — but here's exactly how to get your film developed and scanned well, wherever you are.", cr_h, site_img("film-rolls"))
          + f"""<section class="section" style="padding-top:48px"><div class="wrap prose">
<h2>Option 1: a mail-in film lab</h2><ol><li>Place an order on the lab's website and choose develop-only, develop + scan, or prints.</li><li>Put your rolls in a zip bag with the order number, then a padded envelope.</li><li>Ship with tracking. Scans usually arrive by download link within a week.</li></ol>
<h2>Option 2: a local lab</h2><p>Independent labs and camera stores often offer drop-off. Ask which processes they run in-house (C-41, B&amp;W, E-6) and what scanner they use.</p>
<h2>Option 3: develop at home</h2><p>Black &amp; white is cheap and easy; colour is doable with a kit. Follow our <a href="/blogs/guides/how-to-develop-film-at-home">home developing guide</a>.</p>
<div class="kit" style="max-width:520px">{amz_link("Film developing starter kit <span>Amazon →</span>", "film developing kit", "")}{amz_link("C-41 colour kit <span>Amazon →</span>", "C-41 color developing kit", "")}{amz_link("Film scanner <span>Amazon →</span>", "35mm film scanner", "")}</div>
<h2>What to ask a lab</h2><ul><li>Scan resolution and file format (JPEG vs TIFF)</li><li>Whether negatives are returned</li><li>Push/pull processing for over- or under-exposed film</li><li>Turnaround time</li></ul>
<h2>FAQ</h2>{fh}</div></section>""", schema=[cr_ld, fld], preload=site_img("film-rolls"))

# ------------------------------------------------------------------ home
def build_home(ctx):
    write, site_img, img_path, esc, ICON, product_card, amz_link, faq_html, PRODUCTS, rank_of, SITE = (ctx[k] for k in
        ("write", "site_img", "img_path", "esc", "ICON", "product_card", "amz_link", "faq_html", "PRODUCTS", "rank_of", "SITE"))
    best = [p for p in sorted(PRODUCTS, key=rank_of) if img_path(p["slug"]) and p["cat"] in ("ps", "slr", "instant", "mf", "movie")][:8]
    strip_imgs = [img_path(p["slug"]) for p in sorted(PRODUCTS, key=rank_of) if img_path(p["slug"])][:16]
    strip = "".join(f'<img src="{u}" alt="" loading="lazy" width="255" height="170">' for u in strip_imgs * 2)
    tiles = [("point-shoot-cameras", "Point &amp; Shoot", "point-shoot", "Pocket 35mm"), ("slr-cameras", "SLR Cameras", "slr", "Learn properly"),
             ("polaroid-cameras", "Polaroid", "polaroids", "Instant joy"), ("medium-format-cameras", "Medium Format", "medium-format", "120 film"),
             ("super-8-collections", "Super 8", "super8", "Home movies"), ("collections/film", "Film &amp; Batteries", "film-rolls", "35mm · 120 · instant")]
    tiles_html = "".join(f'<a class="tile reveal reveal-d{i % 3}" href="/{s if s.startswith("collections/") else "collections/" + s}"><img src="{site_img(im)}" alt="" loading="lazy"><div><div class="mono">{sub}</div><h3>{t}</h3></div><span class="tile__arrow">{ICON["arrow"]}</span></a>'
                         for i, (s, t, im, sub) in enumerate(tiles))
    stocks = [("Portra 400", "Kodak Portra 400 35mm film"), ("HP5 Plus", "Ilford HP5 Plus 35mm film"), ("Gold 200", "Kodak Gold 200 35mm film"), ("Tri-X 400", "Kodak Tri-X 400 35mm film"),
              ("Ektar 100", "Kodak Ektar 100 35mm"), ("CineStill 800T", "CineStill 800T 35mm"), ("Polaroid 600", "Polaroid 600 film"), ("Vision3 Super 8", "Kodak Vision3 Super 8 film")]
    stock_html = "".join(f'<span>{amz_link(n, q, "")}</span>' for n, q in stocks * 2)
    posts = [("best-point-and-shoot-film-cameras", "The best point &amp; shoot film cameras", "point-shoot"), ("pentax-k1000-review-35mm-camera", "Pentax K1000 review", "slr"),
             ("how-to-develop-film-at-home", "How to develop film at home", "darkroom")]
    posts_html = "".join(f'<a class="post reveal reveal-d{i}" href="/blogs/guides/{s}"><img src="{site_img(im)}" alt="" loading="lazy"><div><div class="mono muted">Guide</div><h3>{t}</h3><p>Read the guide →</p></div></a>' for i, (s, t, im) in enumerate(posts))
    fh, fld = faq_html(FAQ_MAIN[:6])
    org = {"@context": "https://schema.org", "@type": "Organization", "name": "Relics Film Lab", "alternateName": "Relics", "url": SITE + "/",
           "logo": SITE + "/apple-touch-icon.png", "email": C.EMAIL, "foundingLocation": {"@type": "Place", "name": "Long Beach, California"}}
    web = {"@context": "https://schema.org", "@type": "WebSite", "name": "Relics Film Lab", "url": SITE + "/"}
    n_cams = sum(1 for p in PRODUCTS if p["cat"] in ("ps", "slr", "instant", "mf", "movie", "pocket"))
    body = f"""
<section class="hero"><div class="hero__bg"><img src="{site_img('hero')}" alt="Vintage 35mm film camera and film" fetchpriority="high"></div><span class="leak a"></span><span class="leak b"></span>
<div class="wrap hero__in">
<div class="eyebrow"><span class="rec">Relics Film Lab</span> · Long Beach born</div>
<h1><span class="line"><span>Film cameras,</span></span><span class="line"><span>chosen by a</span></span><span class="line"><span>real <em>film lab</em>.</span></span></h1>
<p class="hero__lead">Shop vintage film cameras, fresh film and the gear to go with them — curated by people who developed, scanned and repaired them for years. Honest buying advice on every model, then buy securely on Amazon.</p>
<div class="hero__cta"><a class="btn" href="/collections/all-film-cameras">Shop film cameras {ICON['arrow']}</a><a class="btn btn--ghost" href="/tools/camera-finder">Find your camera</a></div>
<div class="hero__meta"><div><b class="counter" data-to="{n_cams}" data-suffix="+">{n_cams}+</b>Film cameras covered</div><div><b>6</b>Film formats</div><div><b class="counter" data-to="{len(PRODUCTS)}">{len(PRODUCTS)}</b>Products &amp; guides</div><div><b>LBC</b>Long Beach, CA</div></div>
</div></section>
<div class="strip" aria-hidden="true"><div class="strip__track">{strip}</div></div>
<section class="section"><div class="wrap">
<div class="head-row reveal"><div><div class="eyebrow">Shop by format</div><h2>Find your <em>camera</em></h2></div><a class="btn btn--ghost btn--sm" href="/collections/all">Shop everything</a></div>
<div class="tiles">{tiles_html}</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
<div class="head-row reveal"><div><div class="eyebrow">Most loved</div><h2>The cameras people <em>search for</em></h2></div><a class="btn btn--ghost btn--sm" href="/collections/all-film-cameras">All film cameras</a></div>
<div class="grid">{"".join(product_card(p, i) for i, p in enumerate(best))}</div></div></section>
<div class="stocks"><div class="stocks__track">{stock_html}</div></div>
<section class="section"><div class="wrap split">
<figure class="split__media reveal"><img src="{site_img('darkroom')}" alt="Film being developed in a darkroom" loading="lazy"><figcaption>Fig 1.1 — The lab</figcaption></figure>
<div class="reveal reveal-d1"><div class="eyebrow">Why Relics</div><h2>A film lab's eye, <em>applied to every listing</em></h2>
<p class="lede">Relics started as a Long Beach film lab and camera store. We processed on Noritsu machines, scanned on a Fujifilm Frontier and bench-tested every camera we sold.</p>
<p>That experience is baked into every page: what each camera does brilliantly, which film to load, what tends to fail on a used copy and how to check it the day it arrives. Then we send you to Amazon, where you can compare live listings and buy with its checkout and returns.</p>
<a class="btn btn--ghost" href="/pages/the-relics-standard">The Relics standard</a></div></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
<div class="center reveal"><div class="eyebrow">How it works</div><h2>From <em>first roll</em> to final scan</h2></div>
<div class="steps"><div class="step reveal"><h3>Choose</h3><p>Browse by format or brand and read our honest take on every camera.</p></div>
<div class="step reveal reveal-d1"><h3>Shop on Amazon</h3><p>Compare live listings, condition and seller ratings — buy with Amazon's protection.</p></div>
<div class="step reveal reveal-d2"><h3>Load &amp; shoot</h3><p>Every page lists the film and batteries it needs, linked and ready.</p></div>
<div class="step reveal reveal-d3"><h3>Develop</h3><p>Send it to a lab or develop at home with our step-by-step guides.</p></div></div></div></section>

<section class="section" style="padding-top:0"><div class="wrap">
<div class="head-row reveal"><div><div class="eyebrow">Free tools</div><h2>Shop smarter with our <em>film tools</em></h2></div><a class="btn btn--ghost btn--sm" href="/tools">All tools</a></div>
<div class="toolgrid">
<a class="toolcard reveal" href="/tools/camera-finder"><span class="toolcard__ico">◎</span><h3>Camera finder</h3><p>Four questions, six cameras that suit you.</p><span class="card__cta">Find my camera →</span></a>
<a class="toolcard reveal reveal-d1" href="/tools/film-stock-finder"><span class="toolcard__ico">▤</span><h3>Film stock finder</h3><p>The right film for your camera, light and look.</p><span class="card__cta">Pick my film →</span></a>
<a class="toolcard reveal reveal-d2" href="/tools/battery-finder"><span class="toolcard__ico">⚡</span><h3>Battery finder</h3><p>Which battery does your camera take?</p><span class="card__cta">Look it up →</span></a>
<a class="toolcard reveal reveal-d3" href="/tools/exposure-calculator"><span class="toolcard__ico">☀</span><h3>Exposure calculator</h3><p>Sunny 16 made easy, for any light.</p><span class="card__cta">Calculate →</span></a>
</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap">
<div class="head-row reveal"><div><div class="eyebrow">Guides</div><h2>Learn from the <em>lab</em></h2></div><a class="btn btn--ghost btn--sm" href="/blogs/guides">All guides</a></div>
<div class="posts">{posts_html}</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap prose" style="max-width:860px"><div class="eyebrow">FAQ</div><h2>Questions, <em>answered</em></h2>{fh}</div></section>
<section class="section" style="padding-top:0"><div class="wrap split split--rev">
<figure class="split__media reveal"><img src="{site_img('long-beach', 'film-rolls')}" alt="Long Beach, California" loading="lazy"><figcaption>33.77° N / 118.19° W</figcaption></figure>
<div class="reveal reveal-d1"><div class="eyebrow">Long Beach roots</div><h2>Once the <em>film store</em> in Long Beach. Now everywhere.</h2>
<p>For years Relics was the camera store and film lab Long Beach photographers relied on — the place to buy a refurbished camera, drop off a roll or learn to develop. The storefront and drop boxes have closed, but the know-how moved online so film shooters anywhere can use it.</p>
<p>Looking for a film camera shop near Los Angeles? Start with our <a href="/collections/slr-cameras">SLR</a> and <a href="/collections/point-shoot-cameras">point-and-shoot</a> collections, or read <a href="/order-now">where to develop film</a>.</p></div></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><div class="band reveal"><div class="eyebrow">The Relics list</div><h2>New guides, film deals &amp; camera picks — <em>monthly</em>.</h2>
<form class="newsletter js-news"><input type="email" required placeholder="you@example.com" aria-label="Email address"><button class="btn" type="submit">Join the list</button></form></div></div></section>"""
    write("/", "Relics Film Lab — Shop Film Cameras, Film & Lab Gear", "Relics Film Lab: the Long Beach film lab turned online film photography shop. Shop film cameras, 35mm & 120 film and lab gear with honest buying guides.",
          body, schema=[org, web, fld], preload=site_img("hero"))

def build_sitemap_page(ctx, written):
    write, crumbs, phero, esc = ctx["write"], ctx["crumbs"], ctx["phero"], ctx["esc"]
    groups = {"Collections": [], "Products": [], "Guides": [], "Pages": []}
    for u, t in sorted(written.items()):
        g = "Collections" if u.startswith("/collections") else "Products" if u.startswith("/products") else "Guides" if u.startswith("/blogs") else "Pages"
        if u == "/pages/wishlist":
            continue
        groups[g].append((u, re.sub(r"\s*[—|].*$", "", t)))
    cr_h, cr_ld = crumbs([(None, "Sitemap")])
    body = phero("Site<em>map</em>", "", cr_h) + '<section class="section" style="padding-top:40px"><div class="wrap prose" style="max-width:none">' + "".join(
        f"<h2>{g}</h2><ul style='columns:3 260px'>" + "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in items) + "</ul>" for g, items in groups.items()) + "</div></section>"
    write("/sitemap", "Sitemap", "Every page on Relics Film Lab: film camera collections, product guides, film lab how-tos and store information.", body, schema=[cr_ld])
