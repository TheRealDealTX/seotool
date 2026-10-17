"""Copy for the hub pages (/weddings/, /portraits/, /lifestyle/), About and Privacy."""

ABOUT = {
    "h1": 'A journal about love, <em class="accent">light</em> &amp; home',
    "sub": "Weddings, portraits, the desert Southwest and the small projects that make a house feel like yours.",
    "html": """
<p class="lead">Jaz &amp; Theo began years ago as a husband-and-wife photographers&rsquo; blog: wedding days in the Sonoran desert, engagement sessions under El Paso&rsquo;s holiday lights, road trips north to the Badlands, and the house projects that filled the weekends in between.</p>
<p>Today Jaz &amp; Theo is an independent journal that carries those same subjects forward. A small editorial team writes and updates every guide, and the people behind the original blog are not involved. We don&rsquo;t photograph weddings or take bookings, and nothing here is a sponsored post.</p>
<h2>What you&rsquo;ll find here</h2>
<ul>
<li><strong>Venue and location guides</strong> for weddings, engagements and senior portraits across West Texas, southern New Mexico, Arizona, Austin and beyond.</li>
<li><strong>Planning help</strong> written in plain language: what photography costs, how to build a timeline, when golden hour starts, what to wear.</li>
<li><strong>Home projects</strong> you can finish in a weekend: peg rails, shiplap, hanging lights, gallery walls, and a kitchen with fewer paper towels.</li>
<li><strong>Free tools</strong> — calculators and planners that run in your browser and never ask for an email address.</li>
</ul>
<h2>How we write</h2>
<p>We would rather tell you to call the venue than guess at a fee. Permit rules, prices and hours change, so our guides point you to whoever has the final word, and we label price figures as typical ranges rather than quotes. Older stories from the original blog have been rewritten from scratch and dated so you know when they were last checked.</p>
<p>Found something out of date, or know a place we should write about? Email <a href="mailto:info@jazandtheo.com">info@jazandtheo.com</a> or use the <a href="/contact/">contact form</a>.</p>
""",
}

PRIVACY = """
<p>This policy explains what happens to information on jazandtheo.com. The short version: we collect very little, and we never sell it.</p>
<h2>Contact form</h2>
<p>When you use the contact form, we receive your name, email address, topic and message by email at info@jazandtheo.com so we can reply. We keep those emails only as long as needed to answer and follow up, and we don&rsquo;t add you to any mailing list.</p>
<h2>Tools and checklists</h2>
<p>The calculators, quiz and checklists run entirely in your browser. Checklist ticks are saved in your browser&rsquo;s local storage so they are still there when you come back; they never reach our server, and you can clear them with the Reset button or by clearing your browser data. If you choose &ldquo;Use my location&rdquo; in the golden hour calculator, your browser shares your coordinates with the page only to do the calculation; they are not sent to us.</p>
<h2>Server logs</h2>
<p>Like most websites, our host records standard request logs (IP address, browser type, pages requested and time) for security and troubleshooting.</p>
<h2>Third parties</h2>
<p>Fonts are loaded from Google Fonts, which receives your IP address when the font files are requested. Share buttons link to Pinterest and Facebook; nothing is sent to them unless you click. We don&rsquo;t run advertising trackers.</p>
<h2>Children</h2>
<p>This site is intended for adults and is not directed at children under 13.</p>
<h2>Changes and contact</h2>
<p>If this policy changes, we will update the date at the top of the page. Questions? Email <a href="mailto:info@jazandtheo.com">info@jazandtheo.com</a>.</p>
"""

HUB_COPY = {
    "weddings": {
        "crumb": "Weddings", "cats": ["wedding"], "eyebrow": "Wedding guides",
        "h1": 'Wedding guides for the <em class="accent">desert Southwest</em> &amp; beyond',
        "sub": "Venue guides from El Paso to Lake Powell, honest photography budgets, timelines that actually work, and every little decision in between.",
        "hero": "weddings-hero", "hero_alt": "A bride and groom embracing outdoors in warm evening light",
        "title": "Wedding Photography Guides: El Paso, Arizona & Austin",
        "desc": "Wedding photography guides and venue spotlights for El Paso, Tucson, Phoenix, the Gila Valley, Lake Powell and Austin, plus timeline and budget tools.",
        "intro_h2": "Plan the photos you&rsquo;ll keep forever",
        "intro": """<p>Most couples spend more time choosing a photographer than any other vendor, and for good reason: the pictures are what&rsquo;s left when the flowers wilt. These guides cover the whole arc — finding and budgeting for a photographer, building a day that leaves time for portraits, and choosing places that look beautiful in the light you&rsquo;ll actually have.</p>
<p>Planning an El Paso wedding, a Tucson garden ceremony or a Lake Powell elopement? Each venue guide covers the best photo spots, the light at different times of day, the season to aim for and what to confirm with the venue before you sign.</p>""",
        "checklist": ["Set a photography budget line", "Shortlist three photographers whose full galleries you love", "Choose first look or aisle reveal", "Check sunset time for your date", "Draft a family formals list", "Decide on your exit and ask the venue"],
        "start": ["/2026/10/how-much-does-wedding-photography-cost/", "/2018/06/how-to-find-your-wedding-photographer/", "/2026/10/wedding-day-photography-timeline/", "/2018/04/wedding-exits-different-types/", "/2017/03/what-the-maid-of-honor-is-in-charge-of/"],
        "blocks": [
            {"eyebrow": "Venue spotlights", "h2": "Arizona gardens, desert museums and a lake in the canyon", "img": "gather-estate", "alt": "Outdoor wedding reception with string lights",
             "img2": "sonoran-cactus", "alt2": "Saguaro cactus in the Sonoran desert",
             "html": """<p>From the farm-estate charm of <a href="/2018/03/gather-estate-wedding-arizona-mikayla-shung/">the Gather Estate in Mesa</a> to cactus-lined paths at <a href="/2018/04/arizona-sonoran-desert-museum-cactus-wedding-erin-ricky/">the Arizona-Sonora Desert Museum</a>, our Arizona guides cover where to stand, when to shoot and what to ask.</p>
<p>Further afield, <a href="/2020/08/lake-powell-desitination-wedding-mikay-ryker/">Lake Powell</a> pairs red rock with blue water for one of the most dramatic destination weddings in the West, and the green fields around <a href="/2018/05/lush-gila-valley-temple-wedding-tia-marco/">the Gila Valley</a> surprise everyone who expects only desert.</p>"""},
            {"eyebrow": "West Texas", "h2": "El Paso weddings: dunes, mountains and city lights", "img": "red-sands", "alt": "Sand dunes glowing at sunset", "reverse": True, "sand": True,
             "img2": "el-paso-winter", "alt2": "Holiday lights downtown on a winter evening",
             "html": """<p>El Paso wedding photography has a range few cities can match: rippled sand at <a href="/2018/11/red-sands-el-paso-tx-yasmin-jared/">Red Sands</a>, the Franklin Mountains at golden hour, historic downtown streets and, every December, <a href="/2019/01/downtown-el-paso-winter-engagement-jordanne-aidan/">downtown&rsquo;s holiday lights</a>.</p>
<p>Our <a href="/2026/09/el-paso-engagement-photo-locations/">El Paso photo locations guide</a> rounds up the best spots for engagement and wedding portraits, with notes on access and the best time of day.</p>"""},
        ],
        "tools": ["budget", "timeline", "golden-hour", "exit-quiz"],
        "tools_h2": "Calculators for the big day",
        "list_h2": "Every wedding guide",
        "faq": [
            ("How far in advance should we book a wedding photographer?", "Popular photographers often book 9 to 15 months ahead for spring and fall Saturdays. If your date is flexible, a Friday, Sunday or off-season date widens your options."),
            ("What's the best time of day for wedding photos in the desert?", "The hour before sunset. Midday desert sun is harsh and hot; plan portraits for golden hour and use open shade or a first look for anything earlier."),
            ("Do we need a permit for photos at a park or national recreation area?", "Often, yes — especially for weddings and commercial photography on public land. Check with the park, city or land manager well before your date."),
        ],
    },
    "portraits": {
        "crumb": "Portraits", "cats": ["portraits"], "eyebrow": "Portrait guides",
        "h1": 'Engagement, senior &amp; <em class="accent">anniversary</em> sessions',
        "sub": "Where to go, what to wear and how to relax in front of the camera — from Tucson's desert to downtown Los Angeles.",
        "hero": "portraits-hero", "hero_alt": "A couple laughing together during an outdoor portrait session",
        "title": "Engagement & Senior Photo Locations and Ideas",
        "desc": "Engagement, senior and anniversary photo guides: the best locations in El Paso, Tucson, Phoenix, Los Angeles and Austin, plus outfit palettes and checklists.",
        "intro_h2": "Portrait sessions that feel like you",
        "intro": """<p>A good portrait session is part location, part light and part comfort. The guides here help with all three: the best spots for engagement photos and senior pictures in cities across the Southwest, what to wear for each setting, and simple ways to loosen up so the photos look like you on a good day.</p>
<p>Every location guide includes the best time of day, what to bring and what to check before you go — parking, permits and the occasional rattlesnake warning.</p>""",
        "checklist": ["Pick a location that means something to you", "Check golden hour for your date", "Plan two outfits from one palette", "Pack water, a brush and comfortable shoes", "Bring one prop or activity (optional)", "Confirm any permit or fee"],
        "start": ["/2026/08/what-to-wear-for-engagement-photos/", "/2026/09/el-paso-engagement-photo-locations/", "/2026/08/senior-portrait-session-checklist/", "/2019/05/tucson-downtown-and-desert-senior-session/", "/2018/03/phoenix-papago-desert-engagement-mikayla-shung/"],
        "blocks": [
            {"eyebrow": "Engagements", "h2": "Desert trails, canyon walls and city lights", "img": "papago", "alt": "Red desert buttes at golden hour", "img2": "sabino-canyon", "alt2": "A canyon trail in the Sonoran desert",
             "html": """<p>Arizona offers some of the most photogenic engagement settings anywhere: the red buttes of <a href="/2018/03/phoenix-papago-desert-engagement-mikayla-shung/">Papago Park in Phoenix</a>, the creek and saguaros of <a href="/2017/06/hannah-caleb-sabino-canyon-anniversary-session/">Sabino Canyon</a> and the green farmland of <a href="/2017/04/becca-tanner-lush-gila-valley-engagement/">the Gila Valley</a>.</p>
<p>In West Texas, winter brings one of our favorite sessions of the year: <a href="/2019/01/downtown-el-paso-winter-engagement-jordanne-aidan/">downtown El Paso under the holiday lights</a>.</p>"""},
            {"eyebrow": "Seniors", "h2": "Senior pictures with personality", "img": "tucson-senior", "alt": "A senior portrait in the desert", "reverse": True, "sand": True, "img2": "la-senior", "alt2": "A city street downtown",
             "html": """<p>Senior pictures should look like the person in them. Our guides to <a href="/2019/05/tucson-downtown-and-desert-senior-session/">senior pictures in Tucson</a> and <a href="/2019/01/downtown-los-angeles-senior-session/">downtown Los Angeles</a> pair city backdrops with natural ones, so one session gives you variety.</p>
<p>Before you go, run through the <a href="/2026/08/senior-portrait-session-checklist/">senior portrait checklist</a> — outfits, a few meaningful props and a plan for the light.</p>"""},
        ],
        "tools": ["outfit", "golden-hour", "timeline", "budget"],
        "tools_h2": "Plan your session",
        "list_h2": "Every portrait guide",
        "faq": [
            ("How long is a typical engagement session?", "Most run 60 to 90 minutes, often with one outfit change and one or two nearby locations."),
            ("When should seniors take their pictures?", "Many schedule them in late summer or early fall of senior year so photos are ready for announcements and yearbook deadlines. Check your school's deadline first."),
            ("What if we're awkward in front of the camera?", "Almost everyone is for the first ten minutes. Walk, talk and do something together; a good photographer will give you prompts rather than stiff poses."),
        ],
    },
    "lifestyle": {
        "crumb": "Lifestyle", "cats": ["home", "travel", "photography"], "eyebrow": "Home & lifestyle",
        "h1": 'Home projects, road trips &amp; the <em class="accent">in-between</em>',
        "sub": "Peg rails and shiplap, better lighting, a kitchen without paper towels, and the open road from the Badlands to Yellowstone.",
        "hero": "lifestyle-hero", "hero_alt": "A bright, simply styled living room with natural light",
        "title": "Lifestyle: DIY Home Projects, Decor & Road Trips",
        "desc": "DIY home projects and lifestyle ideas from Jaz & Theo: peg rail shelves, shiplap, light fixtures, gallery walls, cloth napkins, windows and road trips.",
        "intro_h2": "Small projects, big difference",
        "intro": """<p>Some of the most-read stories on Jaz &amp; Theo were never about weddings at all. Readers still search for the <a href="/2019/12/our-entry-peg-rail-shelf-and-shiplap-for-christmas/">entry peg rail shelf and shiplap wall</a>, how high to hang a dining light, and how to make a gallery wall with objects instead of frames.</p>
<p>This is the home-and-life side of the journal: weekend projects with real measurements, simple swaps for a calmer kitchen, and road-trip notes for when you need to get out of the house entirely.</p>""",
        "checklist": ["Measure twice: wall width, stud locations, ceiling height", "Size the dining light before you buy it", "Pick one wall for objects, not frames", "Swap paper towels for a stack of cloth", "Label the pantry (and be kind with the rest)", "Plan a weekend road trip"],
        "start": ["/2019/12/our-entry-peg-rail-shelf-and-shiplap-for-christmas/", "/2018/06/guide-to-buying-and-hanging-lights/", "/2018/03/display-objects-on-walls/", "/2018/04/go-cloth-napkins-towels/", "/2018/05/south-dakota-yellowstone-trip/"],
        "blocks": [
            {"eyebrow": "Around the house", "h2": "Peg rails, lighting and walls worth looking at", "img": "peg-rail", "alt": "An entryway with a wooden peg rail shelf", "img2": "lights", "alt2": "Pendant lights over a dining table",
             "html": """<p>Start with the entry: a <a href="/2019/12/our-entry-peg-rail-shelf-and-shiplap-for-christmas/">Shaker-style peg rail</a> gives every coat and bag a place and takes an afternoon to build. Then fix the lighting with our <a href="/2018/06/guide-to-buying-and-hanging-lights/">guide to buying and hanging lights</a>, and give a blank wall some character with <a href="/2018/03/display-objects-on-walls/">objects instead of art</a>.</p>
<p>Thinking bigger? Our notes on <a href="/2018/08/all-about-windows/">choosing windows</a> cover efficiency, light and the treatments that suit each room.</p>"""},
            {"eyebrow": "On the road", "h2": "Badlands, geysers and the long way home", "img": "south-dakota", "alt": "Layered badlands formations at dusk", "reverse": True, "sand": True, "img2": "lake-powell", "alt2": "Red cliffs above blue water",
             "html": """<p>Our <a href="/2018/05/south-dakota-yellowstone-trip/">South Dakota to Yellowstone road trip</a> covers the drive from Rapid City through the Badlands and the Black Hills to the geysers, with the stops worth a detour and the best light at each.</p>
<p>Closer to home, <a href="/2020/08/lake-powell-desitination-wedding-mikay-ryker/">Lake Powell</a> and <a href="/2018/11/red-sands-el-paso-tx-yasmin-jared/">Red Sands</a> make easy weekend escapes with a camera.</p>"""},
        ],
        "tools": ["pegrail", "chandelier", "napkins", "golden-hour"],
        "tools_h2": "Tools for the house",
        "list_h2": "Home, travel &amp; photography stories",
        "faq": [
            ("What's the easiest DIY project for a beginner?", "A peg rail. It's a single board, a row of drilled holes and a few screws into studs — and it solves the pile of coats by the door."),
            ("How do I find studs before hanging a shelf?", "Use a stud finder, then confirm with a small nail or a magnet that finds the drywall screws. In most US homes studs sit 16 inches apart on center."),
            ("Is shiplap still in style?", "Painted horizontal boards in an entry or mudroom remain a durable, practical choice. Narrow boards, a matte finish and restrained use keep it from feeling dated."),
        ],
    },
}
