"""Page copy for rjbledlcdtvservicecentre.com.

Everything here is data: build.py turns it into HTML. Slugs match the URLs the
old WordPress site used (they still carry rankings and backlinks), so do not
rename them.
"""

BIZ = {
    "name": "RJB LED LCD TV Service Centre",
    "short": "RJB TV Service",
    "email": "info@rjbledlcdtvservicecentre.com",
    "city": "Kolkata",
    "region": "West Bengal",
    "country": "IN",
    "domain": "rjbledlcdtvservicecentre.com",
}

DISCLAIMER = (
    "RJB LED LCD TV Service Centre is an independent, multi-brand TV repair service. "
    "We are not an authorised service centre of, or affiliated with, Samsung, Sony, LG, Videocon "
    "or any other manufacturer. Brand names are used only to describe the televisions we repair."
)

# Wordmarks shown in the scrolling brand strip (plain text, no logos).
MARQUEE = ["Samsung", "Sony", "LG", "Videocon", "Panasonic", "Philips", "Onida", "TCL",
           "Mi", "OnePlus", "Haier", "Micromax", "Hisense", "Toshiba", "Sharp", "Vu"]

# ---------------------------------------------------------------- services
SERVICES = [
    ("backlight", "LED Backlight Repair",
     "Dark screen with sound? Failed LED strips are the most common fault in modern TVs. We replace "
     "complete strip sets, not just the one dead LED, so the repair lasts."),
    ("power", "Power Supply Board",
     "No standby light, clicking on and off, or a dead set after a voltage spike. We trace the fault "
     "to the failed capacitor, MOSFET or IC and repair the board."),
    ("board", "Mainboard &amp; T-Con",
     "Logo loops, frozen menus, ghosting or a picture split into halves. Board-level diagnosis on the "
     "bench with proper tools, firmware and replacement chips."),
    ("panel", "Panel &amp; Display Faults",
     "Vertical or horizontal lines, half-screen, colour bands. We check the panel, flex cables and "
     "COF bonding and tell you honestly whether it is worth fixing."),
    ("sound", "Sound &amp; Ports",
     "No audio, crackling speakers, dead HDMI or USB ports, ARC that won't talk to your soundbar. "
     "Port replacement and audio amplifier repair."),
    ("smart", "Smart TV &amp; Software",
     "Apps crashing, Wi-Fi dropping, endless reboots or a forgotten lock. Software reloads, eMMC "
     "repair and setup for Tizen, webOS, Android TV and Google TV."),
]

# ---------------------------------------------------------------- symptom checker
SYMPTOMS = [
    ("nopicture", "Sound but no picture",
     "Most often the LED backlight. Shine a torch at the screen: if you can faintly see the picture, "
     "the panel is working and only the lighting has failed.",
     "LED backlight strips, backlight driver on the power board, or (less often) the T-con board.",
     "Usually repairable. Backlight strip replacement is our most common job."),
    ("lines", "Lines on the screen",
     "Vertical lines that are always in the same place usually point to the panel's COF (chip-on-film) "
     "bonding. Lines that change with the picture often come from the T-con board or its ribbon cable.",
     "Panel COF/bonding, T-con board, LVDS/V-by-One ribbon cables.",
     "Board and cable faults are repairable; panel bonding faults need assessment first."),
    ("nopower", "TV won't turn on",
     "No standby light at all suggests the power supply. A standby light that blinks in a pattern is "
     "the TV reporting an error code, which tells us where to look.",
     "Power supply board (capacitors, MOSFETs, PWM IC), standby circuit, mainboard short.",
     "Power supply faults are among the most reliably repairable."),
    ("dim", "Dark patches or uneven light",
     "Dark corners, a dim band or 'cloudy' patches usually mean one or more LEDs in the backlight "
     "array have failed or the diffuser sheets have shifted.",
     "Individual LED failure, lens caps fallen off, diffuser or reflector sheet damage.",
     "Repairable. We replace the strips and re-seat the optical sheets."),
    ("flicker", "Flickering or restarting",
     "A picture that flickers, or a TV that restarts by itself, often has a weak power rail or "
     "corrupted firmware.",
     "Dried-out capacitors, backlight driver, firmware/eMMC corruption.",
     "Usually repairable at board level or with a software reload."),
    ("sound", "Picture but no sound",
     "Check the TV is not set to an external speaker or ARC output first. If it is, the audio "
     "amplifier or speakers may have failed.",
     "Audio amplifier IC, speaker coils, mainboard audio section, settings.",
     "Repairable, often the same day once diagnosed."),
    ("smart", "Smart features not working",
     "Apps that crash, Wi-Fi that drops, or a TV stuck on the logo are usually software or storage "
     "(eMMC) problems rather than hardware damage.",
     "Firmware, eMMC storage chip, Wi-Fi module, mainboard.",
     "Often fixed with a software reload; eMMC replacement when storage has failed."),
]

# ---------------------------------------------------------------- process
PROCESS = [
    ("Tell us the fault", "Email or use the form with your TV brand, model number and what it is doing. "
     "A photo of the screen helps a lot."),
    ("Diagnosis", "We test the set on the bench, find the failed part and explain the fault in plain language."),
    ("Your go-ahead", "You get a clear quote before any work starts. No approval, no charge for parts."),
    ("Repair &amp; test", "We repair, then burn-in test the TV for hours so the fault does not come straight back."),
]

# ---------------------------------------------------------------- home FAQ
HOME_FAQ = [
    ("Do you repair all TV brands?",
     "Yes. We specialise in Samsung, Sony, LG and Videocon LED and LCD televisions, and we also repair "
     "Panasonic, Philips, Onida, TCL, Mi, OnePlus, Haier, Vu, Hisense and most other brands sold in India."),
    ("Is it worth repairing an LED TV or should I buy a new one?",
     "Most common faults (backlight strips, power supply, mainboard, ports and software) cost a fraction "
     "of a new TV to fix. The exception is a cracked or physically damaged panel, where a replacement "
     "panel can approach the price of a new set. We tell you honestly which side of that line your TV is on."),
    ("Can you repair a TV with a broken screen?",
     "A physically cracked panel cannot be repaired, only replaced. Lines, colour bands and half-screen "
     "faults are different: they are often caused by boards or cables and can usually be fixed."),
    ("Which areas do you cover?",
     "Kolkata and the surrounding districts: Howrah, Hooghly, North 24 Parganas and South 24 Parganas, "
     "including Bally, Uttarpara, Chandannagar, Barrackpore, Naihati, Budge Budge and many more. See our "
     "service areas page for the full list."),
    ("How do I book a repair?",
     "Email info@rjbledlcdtvservicecentre.com or use the contact form with your TV brand, model number "
     "and a short description of the fault. We reply with the next steps."),
]

# ---------------------------------------------------------------- brands
BRANDS = {
    "samsung": {
        "slug": "samsung-led-lcd-tv-service-centre-kolkata",
        "name": "Samsung",
        "title": "Samsung LED LCD TV Service Centre Kolkata | TV Repair",
        "h1": "Samsung LED LCD TV Service Centre in Kolkata",
        "desc": "Samsung TV repair in Kolkata: LED backlight, power supply, mainboard, lines on screen and "
                "Smart TV faults on Crystal UHD, QLED and LCD models.",
        "img": "living-room-led-tv", "img_alt": "Samsung-style flat screen LED TV in a Kolkata living room",
        "card": "Crystal UHD, QLED and older LCD/LED Samsung sets: backlight strips, power boards, One Connect and Tizen faults.",
        "intro": [
            "Samsung is the TV brand we see most often on our bench. "
            "From older LCD and Full HD LED sets to today's Crystal UHD, QLED and The Frame models, we "
            "repair Samsung televisions at component level across Kolkata.",
            "Whether you searched for a Samsung TV repair center near you because the screen went dark, "
            "the TV keeps restarting, or there are lines across the picture, the cause is usually one of "
            "a handful of well-known faults, and most of them are repairable.",
        ],
        "faults": [
            ("Backlight failure (sound, no picture)", "Samsung's direct-lit LED models are known for LED strip failures. We replace the full strip set so one weak strip doesn't take the rest down months later."),
            ("Red standby light blinking", "A blinking standby LED is the power board or mainboard reporting a fault. We read the pattern and test the rails to find it."),
            ("Vertical lines or half screen", "Often the T-con board or the panel's ribbon cables; sometimes the panel bonding. We test each before quoting."),
            ("Stuck on Samsung logo / boot loop", "Corrupted firmware or a failing eMMC chip. A software reload or storage replacement brings Tizen back."),
            ("One Connect box faults", "On models with a separate One Connect box, a bad cable or box looks like a dead TV. We test both ends."),
            ("No sound or HDMI not detected", "Audio amplifier and HDMI port faults are repaired on the mainboard, including ARC/eARC issues with soundbars."),
        ],
        "series": "Crystal UHD, QLED, Neo QLED, The Frame, Full HD and HD Ready LED, and older Samsung LCD (CCFL) televisions.",
        "faq": [
            ("Why does my Samsung TV have sound but no picture?",
             "In most cases the LED backlight has failed while the rest of the TV still works. Shine a torch close to the screen: if you can see a faint picture, it is almost certainly the backlight, which we repair by replacing the LED strips."),
            ("Can you repair Samsung QLED TVs?",
             "Yes. QLED sets are LED-backlit LCD TVs with a quantum-dot layer, so they share most of the faults (and repairs) of other Samsung LED TVs: backlight, power supply, mainboard and T-con."),
            ("Are you the official Samsung service centre?",
             "No. We are an independent multi-brand repair centre. For a TV still under Samsung's warranty, contact Samsung first; once it is out of warranty, independent repair is usually faster and cheaper."),
        ],
    },
    "sony": {
        "slug": "sony-led-lcd-tv-service-centre-kolkata",
        "name": "Sony",
        "title": "Sony LED LCD TV Service Centre Kolkata | Bravia Repair",
        "h1": "Sony LED LCD TV Service Centre in Kolkata",
        "desc": "Sony Bravia TV repair in Kolkata: no picture, blinking red light, backlight, power board, "
                "Android TV and Google TV faults. Independent service.",
        "img": "living-room-wall-tv", "img_alt": "Wall-mounted Sony Bravia style television in a bright living room",
        "card": "Bravia LED, LCD and Android/Google TV models: blinking red light codes, backlights and software faults.",
        "intro": [
            "Sony Bravia televisions are built to last, which is exactly why they are worth repairing when "
            "something does go wrong. We repair Sony LED and LCD TVs across Kolkata, from older Bravia "
            "LCD models to current Android TV and Google TV sets.",
            "A Sony that shows a blinking red light, switches itself off, or plays sound with a black "
            "screen is telling us something specific. We use that diagnostic information to go straight "
            "to the fault instead of swapping parts until something works.",
        ],
        "faults": [
            ("Red light blinking (error code)", "Bravia sets count out error codes by blinking the standby light. The number of blinks points us to the power supply, backlight or mainboard."),
            ("Sound but no picture", "Usually the backlight LEDs or the backlight driver. We confirm with a torch test and current measurements, then replace the strips."),
            ("Switching on and off by itself", "A protection shutdown, often from a backlight short or a weak power rail. Repairable once the cause is found."),
            ("Android TV / Google TV stuck or slow", "Boot loops, apps crashing and endless updates are mostly software or eMMC storage faults."),
            ("Lines, colour bands or ghosting", "We test the T-con board and ribbon cables before suspecting the panel itself."),
            ("No sound or distorted audio", "Speaker and amplifier faults, plus HDMI ARC problems with home theatres and soundbars."),
        ],
        "series": "Bravia LED (X, W and A series), Android TV and Google TV models, and older Bravia LCD televisions.",
        "faq": [
            ("What does it mean when my Sony TV's red light blinks?",
             "The TV has detected a fault and shut itself down to protect itself. The number of blinks between pauses is an error code. Note the count and tell us when you get in touch; it helps us diagnose before we even see the TV."),
            ("Is it worth repairing an older Sony Bravia?",
             "Usually, yes. Backlight, power supply and board faults on Bravia sets are repairable for much less than a comparable new TV, and the panels themselves tend to hold up well."),
            ("Are you an authorised Sony service centre?",
             "No. We are an independent repair service. For in-warranty sets, contact Sony first; for out-of-warranty repairs we are a practical alternative."),
        ],
    },
    "lg": {
        "slug": "lg-led-lcd-tv-service-centre-kolkata",
        "name": "LG",
        "title": "LG LED LCD TV Service Centre in Kolkata | LG TV Repair",
        "h1": "LG LED LCD TV Service Centre in Kolkata",
        "desc": "LG TV repair in Kolkata: LED backlight strips, no picture, power supply, webOS and Magic "
                "Remote faults on LG LED, NanoCell and LCD TVs.",
        "img": "modern-living-tv", "img_alt": "LG style LED TV mounted in a modern white living room",
        "card": "LED, NanoCell and LCD sets: the well-known LG backlight strip fault, power boards and webOS issues.",
        "intro": [
            "LG makes some of the most popular televisions in Kolkata homes, and a few of its LED models "
            "share one very well-known weakness: the backlight. If your LG TV has sound but a black "
            "screen, you are in good company, and it is very repairable.",
            "We repair LG LED, NanoCell and LCD televisions across the city, from the backlight and power "
            "supply to the mainboard, T-con and webOS software.",
        ],
        "faults": [
            ("Black screen with sound", "The classic LG LED fault. LEDs in the strips burn out, often one after another. We replace the full set with quality strips."),
            ("Screen goes dark after a few seconds", "Picture appears then disappears: the backlight is shutting down to protect itself from a failed LED. Same repair, same result."),
            ("TV won't power on", "Power supply board faults, from blown fuses and capacitors to failed regulators. Repaired at component level."),
            ("webOS slow, apps not loading", "Corrupted software or worn storage. We reload the system and repair the eMMC where needed."),
            ("Magic Remote not pairing", "Pairing, IR and Bluetooth module faults, plus the settings that often cause the problem in the first place."),
            ("Lines or half-screen", "T-con board and ribbon cable faults are repairable; panel faults are assessed honestly before any spend."),
        ],
        "series": "LG UHD and Full HD LED, NanoCell, older LG LCD televisions, and board-level work on LG OLED models.",
        "faq": [
            ("Why does my LG TV have sound but no picture?",
             "On LG LED televisions this is almost always the backlight. One or more LEDs in the strips have failed, which breaks the whole chain. Replacing all the strips is the reliable fix."),
            ("Can you repair LG OLED TVs?",
             "We handle power, mainboard, sound and software faults on LG OLED sets. OLED panels have no backlight, so 'no picture' faults on an OLED have different causes, which we diagnose on the bench."),
            ("Are you LG's official service centre?",
             "No, we are an independent multi-brand repair centre and not affiliated with LG. For in-warranty sets, contact LG first."),
        ],
    },
    "videocon": {
        "slug": "videocon-led-lcd-tv-service-centre-kolkata",
        "name": "Videocon",
        "title": "Videocon LED LCD TV Service Centre Kolkata | TV Repair",
        "h1": "Videocon LED LCD TV Service Centre in Kolkata",
        "desc": "Videocon TV repair in Kolkata: LED and LCD Videocon TVs repaired at board level, even when "
                "spare parts are scarce. Backlight, power and mainboard faults.",
        "img": "minimal-tv-room", "img_alt": "Flat screen Videocon style LED TV on a wooden console",
        "card": "Videocon LED and LCD TVs kept running with board-level repair, even where official spares are scarce.",
        "intro": [
            "Videocon televisions are still in thousands of Kolkata homes, but with the company's "
            "consumer-electronics business no longer active, finding service and genuine spare parts has "
            "become difficult. That is where board-level repair comes in.",
            "Instead of replacing whole boards that are no longer made, we repair the board you already "
            "have: the failed capacitor, regulator, LED or IC. That keeps a working Videocon LED or LCD TV "
            "out of the scrap heap.",
        ],
        "faults": [
            ("No power / dead set", "Power supply faults are the most common Videocon repair and almost always fixable at component level."),
            ("Sound but no picture", "On LED models, the backlight strips; on older LCD models, the CCFL lamps or inverter board."),
            ("Picture colours wrong or washed out", "Mainboard, T-con or panel settings. We test signal path end to end."),
            ("Remote not working", "IR receiver and remote faults, plus universal remote setup when original remotes are unavailable."),
            ("USB or HDMI ports not working", "Port and mainboard repair so you can connect set-top boxes and streaming sticks."),
            ("Lines on screen", "Board and cable faults are repaired; panel faults are assessed honestly before any spend."),
        ],
        "series": "Videocon LED TVs (HD Ready, Full HD), older Videocon LCD and CCFL-backlit sets.",
        "faq": [
            ("Can you still get parts for Videocon TVs?",
             "Complete replacement boards are increasingly rare, which is why we repair boards at component level. Most failed components are standard parts that are still available."),
            ("Is it worth repairing a Videocon LED TV?",
             "If the panel is undamaged, usually yes. Power supply and backlight repairs cost far less than a new TV and keep a working set in use."),
            ("Which is better, LED or LCD TV?",
             "LED TVs are LCD TVs with an LED backlight instead of fluorescent tubes, so they are thinner, brighter and use less power. See our LED vs LCD guide for the full comparison."),
        ],
    },
}
BRAND_ORDER = ["samsung", "sony", "lg", "videocon"]

# ---------------------------------------------------------------- service areas
# district -> description. Every area page links back to its district group.
DISTRICTS = {
    "kolkata": "Kolkata",
    "howrah": "Howrah district",
    "hooghly": "Hooghly district",
    "n24": "North 24 Parganas",
    "s24": "South 24 Parganas",
    "greater": "Greater Kolkata",
}

# slug, brand key (or None for multi-brand), service phrase, place, district, intro, local notes
AREAS = [
    {
        "slug": "samsung-led-tv-service-centre-in-bally", "brand": "samsung", "kind": "LED TV Service Centre",
        "place": "Bally", "district": "howrah", "nearby": ["Belur", "Liluah", "Uttarpara", "Howrah"],
        "intro": "Bally sits on the west bank of the Hooghly at the Howrah end of Vivekananda Setu and Nivedita Setu, "
                 "so it is one of the easiest places for us to reach from Kolkata. We repair Samsung LED televisions "
                 "for homes across Bally, Belur and Liluah.",
        "local": "Many of the Samsung sets we see from Bally are Full HD and Crystal UHD models a few years old, "
                 "and the most common fault is the backlight: sound is fine, the screen is dark.",
    },
    {
        "slug": "samsung-lcd-tv-service-centre-in-howrah", "brand": "samsung", "kind": "LCD TV Service Centre",
        "place": "Howrah", "district": "howrah", "nearby": ["Shibpur", "Santragachi", "Bally", "Salkia"],
        "intro": "Howrah, Kolkata's twin city across the river, has a huge number of older Samsung LCD and early LED "
                 "televisions still in daily use. We repair them, from Shibpur and Santragachi to Salkia and the "
                 "streets around Howrah Station.",
        "local": "Older Samsung LCD sets use fluorescent (CCFL) backlights and an inverter board instead of LED strips. "
                 "We still repair both, which matters when a newer replacement part simply does not fit.",
    },
    {
        "slug": "samsung-led-tv-service-centre-in-chandan-nagar", "brand": "samsung", "kind": "LED TV Service Centre",
        "place": "Chandannagar", "district": "hooghly", "nearby": ["Bhadreshwar", "Chinsurah", "Mankundu", "Baidyabati"],
        "intro": "Chandannagar, the old French settlement on the Hooghly famous for its Jagaddhatri Puja lights, is a "
                 "town that knows its electronics. We provide Samsung LED TV repair for Chandannagar, Mankundu and "
                 "the neighbouring Hooghly towns.",
        "local": "Power surges during the monsoon are a frequent cause of dead TVs in the Hooghly belt. A Samsung that "
                 "will not turn on after a storm usually has a power supply fault, which is very repairable.",
    },
    {
        "slug": "samsung-led-tv-service-centre-in-uttarpara", "brand": "samsung", "kind": "LED TV Service Centre",
        "place": "Uttarpara", "district": "hooghly", "nearby": ["Konnagar", "Hindmotor", "Bally", "Kotrung"],
        "intro": "Uttarpara is the first town of Hooghly district coming up the river from Bally, and our Samsung LED TV "
                 "service covers it along with Kotrung, Hindmotor and Konnagar.",
        "local": "From Uttarpara we see a lot of Samsung Smart TVs with software trouble: stuck on the logo, apps that "
                 "will not open, Wi-Fi that drops. Most are fixed with a firmware reload rather than new parts.",
    },
    {
        "slug": "samsung-led-tv-service-centre-in-baidyabati", "brand": "samsung", "kind": "LED TV Service Centre",
        "place": "Baidyabati", "district": "hooghly", "nearby": ["Sheoraphuli", "Serampore", "Champdani", "Chandannagar"],
        "intro": "Baidyabati and its twin Sheoraphuli sit on the Howrah–Bardhaman main line in Hooghly district. We repair "
                 "Samsung LED televisions for homes across Baidyabati, Sheoraphuli, Serampore and Champdani.",
        "local": "Common Samsung jobs from this area are backlight strips, power boards and HDMI ports damaged by "
                 "set-top box cables pulled at an angle.",
    },
    {
        "slug": "samsung-led-tv-service-centre-in-bhadreshwar", "brand": "samsung", "kind": "LED TV Service Centre",
        "place": "Bhadreshwar", "district": "hooghly", "nearby": ["Chandannagar", "Champdani", "Mankundu", "Baidyabati"],
        "intro": "Bhadreshwar lies between Champdani and Chandannagar on the Hooghly's west bank. Our Samsung LED TV "
                 "service covers Bhadreshwar and the surrounding mill towns.",
        "local": "If your Samsung has a blinking red standby light, count the blinks before you get in touch. The pattern "
                 "helps us narrow the fault down to the power supply, backlight or mainboard.",
    },
    {
        "slug": "samsung-led-tv-service-centre-in-naihati", "brand": "samsung", "kind": "LED TV Service Centre",
        "place": "Naihati", "district": "n24", "nearby": ["Halisahar", "Garifa", "Shyamnagar", "Bandel"],
        "intro": "Naihati is a busy junction on the Sealdah main line in North 24 Parganas. We repair Samsung LED and "
                 "Smart TVs for Naihati, Garifa, Halisahar and the nearby towns.",
        "local": "Samsung sets from the Naihati area most often come to us with dark screens (backlight) and "
                 "no-power faults after voltage fluctuations.",
    },
    {
        "slug": "samsung-led-tv-service-centre-in-barrackpore", "brand": "samsung", "kind": "LED TV Service Centre",
        "place": "Barrackpore", "district": "n24", "nearby": ["Palta", "Titagarh", "Ichapur", "Khardah"],
        "intro": "Barrackpore, with its cantonment and riverside Gandhi Ghat, is one of the main towns of North 24 "
                 "Parganas. Our Samsung LED TV service covers Barrackpore, Titagarh, Palta and Ichapur.",
        "local": "We repair everything from older Samsung Full HD LED sets to current Crystal UHD models, including "
                 "lines on screen, half-screen faults and boot loops.",
    },
    {
        "slug": "sony-led-tv-service-centre-in-phool-bagan", "brand": "sony", "kind": "LED TV Service Centre",
        "place": "Phoolbagan", "district": "kolkata", "nearby": ["Kankurgachi", "Beleghata", "Narkeldanga", "Sealdah"],
        "intro": "Phoolbagan in central-east Kolkata, between Kankurgachi, Beleghata and Narkeldanga, is right in the "
                 "middle of our coverage. We repair Sony Bravia LED televisions across the neighbourhood.",
        "local": "Sony sets from Phoolbagan typically come in with a blinking red light or sound with no picture. "
                 "Both are diagnostic signals we can work with straight away.",
    },
    {
        "slug": "sony-led-tv-service-centre-in-ghshpara", "brand": "sony", "kind": "LED TV Service Centre",
        "place": "Ghoshpara", "district": "n24", "nearby": ["Shyamnagar", "Jagaddal", "Kankinara", "Naihati"],
        "intro": "Ghoshpara Road runs through the industrial towns of North 24 Parganas, and our Sony LED TV service "
                 "covers homes along it, from Shyamnagar and Jagaddal to Kankinara.",
        "local": "We repair Sony Bravia LED, LCD and Android TV models: backlight, power supply, software and "
                 "audio faults.",
    },
    {
        "slug": "lg-led-tv-service-centre-in-kakurgachi", "brand": "lg", "kind": "LED TV Service Centre",
        "place": "Kankurgachi", "district": "kolkata", "nearby": ["Phoolbagan", "Ultadanga", "Bagmari", "Salt Lake"],
        "intro": "Kankurgachi, between Ultadanga and Phoolbagan near the CIT Road crossing, is one of the central "
                 "Kolkata neighbourhoods we serve most. We repair LG LED televisions for homes across the area.",
        "local": "The most common LG fault from Kankurgachi is the well-known backlight failure: sound plays, the "
                 "screen stays black or goes dark after a few seconds.",
    },
    {
        "slug": "lg-led-tv-service-centre-in-palta", "brand": "lg", "kind": "LED TV Service Centre",
        "place": "Palta", "district": "n24", "nearby": ["Barrackpore", "Ichapur", "Shyamnagar", "Titagarh"],
        "intro": "Palta, just north of Barrackpore and home to the waterworks that supply much of Kolkata, is covered by "
                 "our LG LED TV service along with Ichapur and Shyamnagar.",
        "local": "We repair LG LED and NanoCell sets here: backlight strips, power supply boards, webOS faults and "
                 "Magic Remote pairing problems.",
    },
    {
        "slug": "lcd-tv-repairing-centre-in-akra", "brand": None, "kind": "LCD TV Repairing Centre",
        "place": "Akra", "district": "s24", "nearby": ["Maheshtala", "Santoshpur", "Budge Budge", "Behala"],
        "intro": "Akra, on the Budge Budge line in South 24 Parganas, is covered by our multi-brand LCD and LED TV "
                 "repairing service along with Maheshtala and the surrounding area.",
        "local": "We repair LCD and LED TVs of every major brand from Akra: no power, no picture, lines on screen, "
                 "sound faults and broken ports.",
    },
    {
        "slug": "lcd-tv-repairing-centre-in-bamangachi", "brand": None, "kind": "LCD TV Repairing Centre",
        "place": "Bamangachi", "district": "greater", "nearby": [],
        "intro": "Our multi-brand LCD and LED TV repairing service covers Bamangachi and its surrounding "
                 "neighbourhoods, with the same bench diagnosis and clear quotes we offer across Kolkata.",
        "local": "Older LCD televisions with CCFL backlights are still common here. We repair their inverter boards "
                 "and lamps as well as modern LED backlights.",
    },
    {
        "slug": "lcd-tv-repairing-centre-in-santoshpur", "brand": None, "kind": "LCD TV Repairing Centre",
        "place": "Santoshpur", "district": "kolkata", "nearby": ["Jadavpur", "Survey Park", "Kasba", "Mukundapur"],
        "intro": "Santoshpur in south Kolkata, between Jadavpur, Survey Park and the EM Bypass, is well within our "
                 "coverage. We repair LCD and LED TVs of all brands for homes across the area.",
        "local": "Typical jobs from Santoshpur are backlight repairs on Samsung and LG LED sets and Smart TV "
                 "software faults on newer Android TV models.",
    },
    {
        "slug": "lcd-tv-repairing-centre-in-budge-budge", "brand": None, "kind": "LCD TV Repairing Centre",
        "place": "Budge Budge", "district": "s24", "nearby": ["Pujali", "Maheshtala", "Akra", "Bawali"],
        "intro": "Budge Budge, the riverside town at the end of the Budge Budge line in South 24 Parganas, is covered by "
                 "our multi-brand LCD and LED TV repairing service along with Pujali and Maheshtala.",
        "local": "Humidity near the river is hard on electronics. Corroded connectors and swollen capacitors on the "
                 "power board are common causes of TVs that will not switch on, and both are repairable.",
    },
    {
        "slug": "lcd-tv-repairing-centre-in-gangpur", "brand": None, "kind": "LCD TV Repairing Centre",
        "place": "Gangpur", "district": "greater", "nearby": [],
        "intro": "Our LCD and LED TV repairing service covers Gangpur and the neighbouring localities, with "
                 "board-level diagnosis rather than guesswork part-swapping.",
        "local": "We repair every major brand here, from older LCD sets to current 4K LED Smart TVs, with board-level "
                 "diagnosis and a clear quote before work begins.",
    },
    {
        "slug": "led-tv-service-center-in-ruby", "brand": None, "kind": "LED TV Service Center",
        "place": "Ruby", "district": "kolkata", "nearby": ["Kasba", "Anandapur", "Mukundapur", "Santoshpur"],
        "intro": "The Ruby crossing on the EM Bypass connects Kasba, Anandapur and Mukundapur, some of the fastest-"
                 "growing parts of south-east Kolkata. Our LED TV service covers all of them.",
        "local": "Newer flats around Ruby mean a lot of large wall-mounted 4K LED and Smart TVs. We repair backlight, "
                 "power, mainboard and software faults on all major brands.",
    },
]

# Extra localities listed (without their own page) on the service-areas hub.
EXTRA_LOCALITIES = {
    "kolkata": ["Salt Lake", "Dum Dum", "Behala", "Tollygunge", "Garia", "Park Circus", "Shyambazar", "Ultadanga"],
    "howrah": ["Shibpur", "Santragachi", "Liluah", "Belur"],
    "hooghly": ["Serampore", "Konnagar", "Rishra", "Chinsurah"],
    "n24": ["Titagarh", "Khardah", "Sodepur", "Barasat"],
    "s24": ["Maheshtala", "Pujali", "Sonarpur", "Baruipur"],
    "greater": [],
}

# Legacy WordPress tag archives -> where they live now (301 in index.php).
TAG_REDIRECTS = {
    "lg-led-tv-service-centre-in-kolkata": "lg-led-lcd-tv-service-centre-kolkata",
    "sony-led-tv-service-centre-in-kolkata": "sony-led-lcd-tv-service-centre-kolkata",
    "samsung-led-tv-service-centre-in-kolkata": "samsung-led-lcd-tv-service-centre-kolkata",
    "led-tv-repairing-service-centre-in-kolkata": "led-lcd-tv-repairing-in-kolkata",
    "samsung-led-tv-service-centre-in-bhadreshwar": "samsung-led-tv-service-centre-in-bhadreshwar",
    "lcd-tv-repairing-centre-in-budge-budge": "lcd-tv-repairing-centre-in-budge-budge",
    "samsung-led-tv-service-centre-in-naihati": "samsung-led-tv-service-centre-in-naihati",
    "samsung-led-tv-service-centre-in-barrackpore": "samsung-led-tv-service-centre-in-barrackpore",
    "lcd-tv-repairing-centre-in-gangpur": "lcd-tv-repairing-centre-in-gangpur",
    "lg-led-tv-service-centre-in-kakurgachi": "lg-led-tv-service-centre-in-kakurgachi",
    "lg-led-tv-service-centre-in-palta": "lg-led-tv-service-centre-in-palta",
}
