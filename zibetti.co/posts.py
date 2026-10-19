"""Journal posts for zibetti.co. Each body is trusted HTML; headings carry the ids used in `toc`."""


def fig(name, alt, caption=""):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return (f'<figure class="reveal"><img src="/assets/img/{name}.webp" srcset="/assets/img/{name}-sm.webp 900w, /assets/img/{name}.webp 1800w" '
            f'sizes="(max-width: 1020px) 100vw, 760px" alt="{alt}" loading="lazy" decoding="async" width="1800" height="1200">{cap}</figure>')


POSTS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "how-to-elope-in-utah",
        "title": "How to Elope in Utah: The Complete Step-by-Step Guide",
        "short": "How to elope in Utah",
        "seo_title": "How to Elope in Utah: License, Permits & Locations",
        "description": "Everything you need to elope in Utah: marriage license rules, witnesses, national and state park permits, the best seasons and a sample elopement timeline.",
        "excerpt": "Marriage licenses, witnesses, permits, seasons and the exact order to plan it all — from a Utah-based elopement team.",
        "category": "Elopement guide",
        "minutes": 9,
        "date": "2026-10-02",
        "image": "mountain-elopement-couple",
        "image_alt": "Couple walking hand in hand through a golden mountain meadow",
        "toc": [("why-utah", "Why elope in Utah"), ("license", "Get your marriage license"), ("permits", "Permits by land type"),
                ("seasons", "Pick your season"), ("steps", "The planning order"), ("day-of", "A sample elopement day"), ("faq", "Quick answers")],
        "faq": [
            ("Do you need witnesses to elope in Utah?", "Yes. Utah requires two witnesses who are at least 18 years old, in addition to an authorized officiant. Your photographer can often serve as one witness."),
            ("How long is a Utah marriage license valid?", "A Utah marriage license is valid for 32 days from the date it is issued and can be used anywhere in the state."),
            ("Do you need a permit to elope in a Utah national park?", "Yes. Ceremonies in national parks such as Arches, Zion, Bryce Canyon, Canyonlands and Capitol Reef require a special use permit from the park."),
        ],
        "body": """
<p class="lead">Utah might be the best state in the country to elope. Five national parks, alpine lakes, salt flats and slot canyons sit within a day’s drive of each other, and the marriage license process is refreshingly simple. Here is exactly how to do it, in the order we walk our own couples through it.</p>

<h2 id="why-utah">Why elope in Utah?</h2>
<p>Variety is the short answer. In a single weekend you could say your vows on a red-rock rim at sunrise and toast under pine trees at an alpine lake by sunset. Utah also has big, open skies — which means long, gorgeous golden hours — and enough public land that you can find solitude even in peak season if you plan around the crowds.</p>
<ul>
  <li><strong>Desert and red rock:</strong> Arches, Canyonlands, Capitol Reef, Goblin Valley, the San Rafael Swell.</li>
  <li><strong>Canyons and hoodoos:</strong> Zion and Bryce Canyon.</li>
  <li><strong>Mountains and lakes:</strong> the Uinta Mountains, the Alpine Loop, Sundance and Park City.</li>
  <li><strong>Something totally different:</strong> the Bonneville Salt Flats and Antelope Island.</li>
</ul>
""" + fig("red-rock-desert-road", "Road winding into Utah red rock country", "Southern Utah’s red-rock country is a three to four hour drive from the Wasatch Front.") + """
<h2 id="license">Step 1: Get your Utah marriage license</h2>
<p>Utah marriage licenses are issued by county clerks, and a license from any Utah county works anywhere in the state. Several counties (including Utah County and Salt Lake County) let you apply online and complete the process by video call, which is a lifesaver for out-of-state couples.</p>
<div class="callout"><strong>The essentials</strong>
<ul>
  <li>No waiting period — you can marry the same day the license is issued.</li>
  <li>The license is valid for <b>32 days</b>, so don’t apply too early.</li>
  <li>You need an authorized <b>officiant</b> and <b>two witnesses aged 18+</b>.</li>
  <li>Both partners need valid photo ID. Fees vary by county, so check your clerk’s website.</li>
</ul></div>
<p>Plenty of elopement officiants in Utah will travel to a trailhead or overlook with you. If you’re bringing zero guests, ask your officiant whether they can bring a second witness. Your photographer can usually sign as the other.</p>

<h2 id="permits">Step 2: Understand permits by land type</h2>
<p>This is where most couples get stuck, so here is the simple version. Who manages the land decides what you need.</p>
<div class="table-scroll"><table>
  <thead><tr><th>Land type</th><th>Examples</th><th>What to expect</th></tr></thead>
  <tbody>
    <tr><td>National parks</td><td>Arches, Zion, Bryce Canyon, Canyonlands, Capitol Reef</td><td>Special use permit required. Group-size limits and approved ceremony sites. Apply weeks to months ahead.</td></tr>
    <tr><td>State parks</td><td>Dead Horse Point, Goblin Valley, Snow Canyon, Antelope Island</td><td>Special use or event permit from the park. Often more flexible on group size.</td></tr>
    <tr><td>National forest</td><td>Uinta-Wasatch-Cache (Alpine Loop, Mirror Lake Highway)</td><td>Small, low-impact ceremonies are often simpler; larger gatherings may need a permit. Call the ranger district.</td></tr>
    <tr><td>BLM land</td><td>San Rafael Swell, Factory Butte, the Salt Flats</td><td>Often the most flexible, but rules vary by field office. Always confirm.</td></tr>
    <tr><td>Private venues</td><td>Sundance, lodges, ranches</td><td>Book directly. No public-land permit, plus bathrooms and shelter.</td></tr>
  </tbody>
</table></div>
<p>Permits and rules change, so treat this as a map, not the final word. When you book an elopement with us we help you choose a location that fits your group and then confirm the current permit requirements together.</p>

<h2 id="seasons">Step 3: Pick your season</h2>
<p><strong>Spring (March–May)</strong> is prime time for the desert parks: mild temperatures and long days, but also spring break crowds and wind. <strong>Summer (June–August)</strong> belongs to the mountains; the Uintas and Alpine Loop are green and full of wildflowers while southern Utah bakes. <strong>Fall (September–November)</strong> is our favorite — golden aspens up north in late September and perfect red-rock weather down south in October. <strong>Winter</strong> brings snow-dusted hoodoos at Bryce and almost-empty trails, as long as you dress for it.</p>
<p>Not sure where your season points you? Our <a href="/tools/utah-elopement-location-finder/">Utah elopement location finder</a> filters 20 spots by season, scenery and drive time.</p>

<h2 id="steps">Step 4: Plan in this order</h2>
<ol>
  <li><strong>Pick a rough season and vibe</strong> (desert, alpine, water, snow).</li>
  <li><strong>Book your photographer</strong> early — they’ll help you choose a location that photographs well at the time of day you want.</li>
  <li><strong>Choose your exact location</strong> and confirm the permit and group limits.</li>
  <li><strong>Apply for the permit</strong>, then book lodging nearby (Moab, Springdale and Park City fill up fast).</li>
  <li><strong>Book your officiant</strong> and line up witnesses.</li>
  <li><strong>Apply for your license</strong> within 32 days of the date.</li>
  <li><strong>Plan your timeline around sunset</strong> using our <a href="/tools/golden-hour-calculator/">golden hour calculator</a>.</li>
</ol>

<h2 id="day-of">A sample Utah elopement day</h2>
<p>Here is how a relaxed, four-hour sunset elopement in Moab might look in October (sunset around 6:40 pm):</p>
<ul>
  <li><b>2:30 pm</b> — Getting ready and details at your rental.</li>
  <li><b>3:30 pm</b> — First look in a quiet spot near your lodging.</li>
  <li><b>4:15 pm</b> — Drive and short walk to the ceremony site.</li>
  <li><b>5:00 pm</b> — Vows, rings and signing the license.</li>
  <li><b>5:30 pm</b> — Champagne, picnic and adventure portraits.</li>
  <li><b>6:00 pm</b> — Golden hour portraits on the rim.</li>
  <li><b>6:45 pm</b> — Blue hour and stars, then dinner.</li>
</ul>
<p>Build your own version with the <a href="/tools/wedding-day-timeline-builder/">timeline builder</a> — set the type to “Elopement” and pick your location.</p>
""" + fig("alpenglow-mountain-peak", "Mountain peaks glowing pink at sunset", "Alpenglow lasts only minutes — worth planning your whole day around.") + """
<h2 id="faq">Quick answers</h2>
<p><strong>Do we need witnesses?</strong> Yes — two, aged 18 or older. <strong>Can we marry in a national park?</strong> Yes, with a special use permit. <strong>How far ahead should we plan?</strong> Four to eight months is comfortable for peak-season dates; less is possible for weekdays and winter.</p>
<p>Ready to start? <a href="/contact-us/">Tell us your season and dream spot</a> and we’ll send our full elopement guide.</p>
""",
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "best-places-to-elope-in-utah",
        "title": "The 15 Best Places to Elope in Utah (By Season and Scenery)",
        "short": "Best places to elope in Utah",
        "seo_title": "15 Best Places to Elope in Utah (Red Rock to Alpine)",
        "description": "The best places to elope in Utah by scenery: national and state parks, alpine lakes, slot canyons and the Bonneville Salt Flats, with seasons and permits.",
        "excerpt": "Red-rock rims, alpine lakes, hoodoos and salt flats — our favorite Utah elopement locations, with the best season for each.",
        "category": "Locations",
        "minutes": 10,
        "date": "2026-09-24",
        "image": "desert-river-canyon",
        "image_alt": "River curving through a deep red sandstone canyon",
        "toc": [("red-rock", "Red rock & desert"), ("canyons", "Canyons & hoodoos"), ("alpine", "Alpine & lakes"), ("unexpected", "The unexpected"), ("choose", "How to choose")],
        "tools_js": False,
        "body": """
<p class="lead">We could fill a book with Utah locations. Instead, here are fifteen we come back to again and again — grouped by the kind of scenery you’re dreaming about, with the season we’d pick for each.</p>
<div class="callout"><strong>Interactive</strong>Want to narrow this list down fast? The <a href="/tools/utah-elopement-location-finder/">Utah elopement location finder</a> filters these spots (plus a few more) by season, scenery, hiking and drive time.</div>

<h2 id="red-rock">Red rock &amp; desert</h2>
<h3>1. Arches National Park</h3>
<p>Sandstone arches, balanced rocks and fins glowing orange at sunrise. Arches is iconic for a reason, which also means crowds — choose a weekday sunrise and a less famous viewpoint. <em>Best: March–May, late September–November. Permit: national park special use permit.</em></p>
<h3>2. Dead Horse Point State Park</h3>
<p>A rim-top overlook above a gooseneck bend of the Colorado River. Massive views with nearly zero hiking — perfect for grandparents or a small group. <em>Best: spring and fall; winter is quiet and beautiful. Permit: state park.</em></p>
<h3>3. Canyonlands — Island in the Sky</h3>
<p>Layer upon layer of canyons stretching to the horizon. Grand View Point at sunset feels like standing on the edge of the world. <em>Best: spring and fall.</em></p>
<h3>4. Capitol Reef National Park</h3>
<p>White domes, red cliffs, historic orchards and far fewer visitors than the “Mighty Five” neighbors. Great for couples who want quiet. <em>Best: April–May and October.</em></p>
<h3>5. Goblin Valley State Park</h3>
<p>Hundreds of mushroom-shaped hoodoos that look like another planet. Playful, surreal and endlessly photogenic. <em>Best: spring and fall.</em></p>
""" + fig("red-rock-desert-road", "Road leading into red rock desert") + """
<h2 id="canyons">Canyons &amp; hoodoos</h2>
<h3>6. Zion National Park</h3>
<p>Thousand-foot cliffs, the Virgin River and cottonwoods that turn gold in early November. Canyon walls block the sun early, so plan for open light rather than a horizon sunset. <em>Best: spring, late fall and winter.</em></p>
<h3>7. Bryce Canyon National Park</h3>
<p>An amphitheater of orange hoodoos at around 8,000 feet. Cool in summer and unforgettable with fresh snow. Sunrise at the rim is the move. <em>Best: any season — winter is magic.</em></p>
<h3>8. The San Rafael Swell slot canyons</h3>
<p>Narrow, glowing slot canyons for adventurous couples who don’t mind a little scrambling. Never enter a slot canyon with rain anywhere in the forecast. <em>Best: spring and fall.</em></p>

<h2 id="alpine">Alpine &amp; lakes</h2>
<h3>9. Mirror Lake Highway &amp; the Uinta Mountains</h3>
<p>High alpine lakes, pine forests and summer wildflowers about two hours from Salt Lake City. The highway closes in winter. <em>Best: July–September.</em></p>
<h3>10. The Alpine Loop &amp; Mount Timpanogos</h3>
<p>Our backyard. Aspen groves, meadows and big granite peaks minutes from Provo. Peak fall color usually lands in the last week or two of September. <em>Best: summer and late September.</em></p>
""" + fig("fall-lake-wedding-portrait", "Couple at an autumn lake surrounded by fall color", "Late September in the Wasatch is short, golden and worth chasing.") + """
<h3>11. Tibble Fork Reservoir</h3>
<p>A calm mountain reservoir in American Fork Canyon with easy access — ideal when you have family who can’t hike. <em>Best: June–October.</em></p>
<h3>12. Sundance Mountain Resort</h3>
<p>Rustic-luxe lodging, dining and ceremony sites at the base of Timpanogos. A great pick for intimate weddings with a few dozen guests. <em>Best: year-round.</em></p>
<h3>13. Guardsman Pass, Park City</h3>
<p>Rolling ridgelines and aspen groves with roadside access — plus all of Park City’s restaurants for your dinner afterward. <em>Best: summer and fall.</em></p>

<h2 id="unexpected">The unexpected</h2>
<h3>14. Bonneville Salt Flats</h3>
<p>A blindingly white, perfectly flat horizon. Minimal and modern, and after a rain it becomes a mirror. Bring sunglasses and be ready for heat. <em>Best: late summer and fall when the flats are dry.</em></p>
<h3>15. Antelope Island State Park</h3>
<p>Golden grasslands, the Great Salt Lake shoreline and free-roaming bison, about an hour from Salt Lake City. Bugs can be intense in late spring. <em>Best: April and September–October.</em></p>

<h2 id="choose">How to choose your spot</h2>
<ul>
  <li><strong>Start with the season.</strong> Desert in spring and fall, mountains in summer and early fall.</li>
  <li><strong>Be honest about hiking.</strong> A mile in wedding shoes feels like three.</li>
  <li><strong>Count your guests.</strong> National parks have group limits; private venues and state parks are more flexible.</li>
  <li><strong>Check the light.</strong> Use the <a href="/tools/golden-hour-calculator/">golden hour calculator</a> — canyon locations lose the sun early.</li>
</ul>
<p>Then read our <a href="/blog/how-to-elope-in-utah/">step-by-step guide to eloping in Utah</a> for licenses and permits.</p>
""",
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "how-to-travel-with-a-wedding-dress",
        "title": "How to Travel With a Wedding Dress (Without Wrinkles or Panic)",
        "short": "How to travel with a wedding dress",
        "seo_title": "How to Travel With a Wedding Dress on a Plane: 11 Tips",
        "description": "How to travel with a wedding dress for a destination wedding or elopement: carry-on vs. checked, packing, garment bags, steaming, suits and formalwear tips.",
        "excerpt": "Carry-on or check it? How to pack, protect and steam your dress (and suit) for a destination wedding or elopement.",
        "category": "Destination tips",
        "minutes": 7,
        "date": "2026-09-12",
        "image": "wedding-dress-hanging",
        "image_alt": "Wedding gown hanging on a dress form by a sunny window",
        "toc": [("before", "Before you fly"), ("pack", "How to pack it"), ("airport", "At the airport"), ("arrive", "When you arrive"), ("suits", "Suits & formalwear")],
        "body": """
<p class="lead">As destination photographers, we’ve seen dresses arrive perfect and dresses arrive… less perfect. Here’s everything we tell our couples about traveling with a wedding dress and formal attire.</p>

<h2 id="before">Before you fly</h2>
<ol>
  <li><strong>Call your airline.</strong> Ask how they handle wedding dresses. Many airlines will let you hang a gown in a crew closet on larger aircraft if space allows, but nothing is guaranteed — plan to carry it on.</li>
  <li><strong>Ask your boutique to pack it.</strong> Bridal shops fold dresses for shipping all the time. Ask for acid-free tissue paper between every fold.</li>
  <li><strong>Schedule your final fitting early.</strong> Leave a buffer so you’re not picking the dress up the day before your flight.</li>
  <li><strong>Consider shipping.</strong> For big ball gowns going abroad, a tracked, insured courier shipment to your venue can be less stressful than an overhead bin. Confirm the venue can receive and store it.</li>
</ol>

<h2 id="pack">How to pack it</h2>
<p>For most dresses, a <strong>breathable garment bag</strong> (not plastic, which traps moisture) folded into thirds fits in an overhead bin. For voluminous gowns, a <strong>dedicated wedding dress travel box</strong> or a large carry-on with the dress rolled in tissue works better.</p>
<ul>
  <li>Turn the dress inside out to protect beading and lace.</li>
  <li>Stuff the bodice with tissue to keep its shape.</li>
  <li>Fold along existing seams, never across structured bodices.</li>
  <li>Pack your veil separately, rolled loosely around a towel or cardboard tube.</li>
</ul>
""" + fig("airplane-wing-travel", "View from an airplane window above the clouds", "Carry it on. Always carry it on.") + """
<h2 id="airport">At the airport</h2>
<ol start="5">
  <li><strong>Board early.</strong> Pay for priority boarding so overhead space isn’t gone when you get on.</li>
  <li><strong>Tell the crew.</strong> A friendly “I’m flying with my wedding dress” often earns a closet spot or a careful hand.</li>
  <li><strong>Never check it.</strong> Lost luggage is a nightmare on any trip; on this trip it’s not an option.</li>
  <li><strong>Keep the essentials with you:</strong> rings, vows, marriage paperwork, shoes and any jewelry go in your personal item.</li>
</ol>

<h2 id="arrive">When you arrive</h2>
<ol start="9">
  <li><strong>Unpack immediately</strong> and hang the dress somewhere high so the train hangs free.</li>
  <li><strong>Steam, don’t iron.</strong> Bring a travel steamer or ask your hotel. A steamy bathroom works in a pinch for light fabrics. Test on an inside seam first.</li>
  <li><strong>Find a local pro.</strong> For destination weddings, ask your planner or venue for a local seamstress or steaming service on standby.</li>
</ol>
<div class="callout"><strong>Photographer tip</strong>Leave the dress on its prettiest hanger. We photograph it during the details portion of getting ready — hanging in a window, it’s often one of the most-loved images in the gallery.</div>

<h2 id="suits">Suits &amp; other formalwear</h2>
<p>Suits and tuxedos travel well in a carry-on garment bag. Roll shirts instead of folding them, pack ties flat inside a book, and stuff dress shoes with socks to keep their shape. If you’re renting, check whether the rental company has a location near your destination — it’s often easier to pick up there.</p>
<p>Bridesmaids and groomsmen should follow the same rule: carry it on, unpack on arrival, steam the day before. Planning a destination wedding? See our <a href="/blog/how-much-does-a-destination-wedding-photographer-cost/">guide to destination photography costs</a>, or <a href="/contact-us/">send us your date</a>.</p>
""",
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "wedding-day-timeline-for-photos",
        "title": "The Perfect Wedding Day Timeline for Photos (With Examples)",
        "short": "Wedding day timeline for photos",
        "seo_title": "Wedding Day Timeline for Photos: Samples & Tips",
        "description": "How to build a wedding day timeline for photos: first look or not, family formals, golden hour portraits and two complete sample schedules.",
        "excerpt": "First look or not, how long family photos really take, and two sample timelines built around sunset.",
        "category": "Planning",
        "minutes": 8,
        "date": "2026-08-28",
        "image": "reception-table-setting",
        "image_alt": "Reception table set with wildflowers and glassware",
        "toc": [("rules", "Three rules"), ("first-look", "First look or not"), ("family", "Family formals"), ("sample-a", "Sample: first look"), ("sample-b", "Sample: no first look"), ("tool", "Build yours")],
        "body": """
<p class="lead">A good timeline is the difference between a relaxed day and a rushed one — and it shows in your photos. Here is how we build them.</p>

<h2 id="rules">Three rules we never break</h2>
<ol>
  <li><strong>Anchor to sunset.</strong> Portraits in the last hour before sunset are the warmest, softest and most flattering of the day. Check your date with our <a href="/tools/golden-hour-calculator/">golden hour calculator</a>.</li>
  <li><strong>Pad everything by 10–15%.</strong> Hair runs late. Shuttles get lost. Buffers keep the day calm.</li>
  <li><strong>Family photos right after the ceremony.</strong> Everyone is in one place and still looks perfect.</li>
</ol>

<h2 id="first-look">First look or not?</h2>
<p>A first look is a private moment where you see each other before the ceremony. It lets us do most portraits and wedding party photos early, so you can actually attend your cocktail hour. Skipping it is totally valid — you get that walk-down-the-aisle reveal — but plan for a busier hour after the ceremony.</p>
<div class="table-scroll"><table>
  <thead><tr><th></th><th>First look</th><th>No first look</th></tr></thead>
  <tbody>
    <tr><td>Photo time before ceremony</td><td>~1.5–2 hours</td><td>~1 hour</td></tr>
    <tr><td>Cocktail hour</td><td>You get to enjoy it</td><td>Mostly portraits</td></tr>
    <tr><td>Nerves</td><td>Usually calmer</td><td>Big emotional reveal</td></tr>
  </tbody>
</table></div>

<h2 id="family">How long family formals really take</h2>
<p>Plan about <strong>two minutes per grouping</strong>. Ten groupings is twenty minutes, plus wrangling. Write a list, assign a loud cousin to round people up, and tell everyone in advance to stay after the ceremony.</p>
""" + fig("bride-groom-bouquet", "Bride and groom holding a bouquet together") + """
<h2 id="sample-a">Sample timeline: first look, 5:00 pm ceremony</h2>
<p>For a September wedding with sunset around 7:30 pm and eight hours of coverage:</p>
<ul>
  <li><b>12:30</b> Details and getting ready</li>
  <li><b>1:45</b> Getting into the dress and suit</li>
  <li><b>2:30</b> First look</li>
  <li><b>2:50</b> Couple portraits</li>
  <li><b>3:30</b> Wedding party photos</li>
  <li><b>4:15</b> Tuck away, touch-ups</li>
  <li><b>5:00</b> Ceremony</li>
  <li><b>5:30</b> Family formals</li>
  <li><b>6:00</b> Join cocktail hour</li>
  <li><b>6:30</b> Entrance, dinner, toasts</li>
  <li><b>7:05</b> Sunset portraits (15 minutes)</li>
  <li><b>7:30</b> First dance, cake, open dancing</li>
  <li><b>8:15</b> Send-off</li>
</ul>

<h2 id="sample-b">Sample timeline: no first look, 4:00 pm ceremony</h2>
<ul>
  <li><b>12:00</b> Details and getting ready</li>
  <li><b>1:30</b> Dress and suit, portraits of each of you separately</li>
  <li><b>2:30</b> Separate wedding party photos</li>
  <li><b>3:30</b> Hide away before guests arrive</li>
  <li><b>4:00</b> Ceremony</li>
  <li><b>4:30</b> Family formals</li>
  <li><b>5:00</b> Full wedding party, then couple portraits</li>
  <li><b>6:00</b> Entrance, dinner, toasts</li>
  <li><b>7:00</b> Sunset portraits</li>
  <li><b>7:20</b> Dances and party</li>
  <li><b>8:00</b> Send-off</li>
</ul>

<h2 id="tool">Build your own in two minutes</h2>
<p>Our free <a href="/tools/wedding-day-timeline-builder/">wedding day timeline builder</a> uses your real date and location to find sunset, then lays out a full schedule — and it can pick the best ceremony time for you. Print it, tweak it and send it to your planner.</p>
""",
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "golden-hour-wedding-photos",
        "title": "Golden Hour Wedding Photos: How to Plan Your Day Around the Light",
        "short": "Golden hour wedding photos",
        "seo_title": "Golden Hour Wedding Photos: When It Is & How to Plan",
        "description": "What golden hour and blue hour are, when they happen on your wedding date, and how to plan ceremony, portraits and sunset photos around the best light.",
        "excerpt": "What golden hour actually is, why it changes with the seasons, and how to sneak away for the best photos of your day.",
        "category": "Photography",
        "minutes": 6,
        "date": "2026-08-14",
        "image": "sunset-sky",
        "image_alt": "Red and orange sunset sky over the horizon",
        "toc": [("what", "What is golden hour"), ("when", "When it happens"), ("terrain", "Mountains & canyons"), ("plan", "Planning tips"), ("blue", "Don’t skip blue hour")],
        "body": """
<p class="lead">Ask any photographer for one piece of timeline advice and you’ll hear the same thing: plan for golden hour. Here’s why, and how.</p>

<h2 id="what">What is golden hour?</h2>
<p>Golden hour is the window just after sunrise and just before sunset when the sun is low — roughly from 6° above the horizon to a few degrees below it. Low sunlight passes through more atmosphere, which scatters blue light and leaves warm, soft, directional light behind. It flatters skin, glows through hair and veils, and makes landscapes look painted.</p>
<p><strong>Blue hour</strong> follows sunset (and precedes sunrise): the sun is 4–6° below the horizon and the sky turns an even, cool blue. It’s ideal for moody portraits, city lights and sparkler exits.</p>

<h2 id="when">When does it happen on your date?</h2>
<p>It changes every day. In Utah, an evening golden hour can start before 4:00 pm in December and after 8:00 pm in late June. It also lasts longer in summer and at higher latitudes. The quickest way to know is our <a href="/tools/golden-hour-calculator/">golden hour calculator</a> — pick a location and your date.</p>
""" + fig("mountains-above-clouds", "Mountains rising above a sea of clouds at golden hour") + """
<h2 id="terrain">Mountains and canyons change the math</h2>
<p>The calculator assumes a flat horizon. Real places aren’t flat. In Zion’s main canyon, direct sun can leave the canyon floor an hour or more before official sunset. On the Wasatch Front, the light drops behind western ridges early in some neighborhoods. Overlooks and salt flats, on the other hand, keep the light until the very last minute.</p>
<p>That’s why we scout. We check sun angles on satellite maps and, for local weddings, visit at the same time of day when we can.</p>

<h2 id="plan">Planning tips</h2>
<ul>
  <li><strong>Sunset portraits in the middle of the reception.</strong> Fifteen to twenty minutes is plenty. Your guests will be eating dessert.</li>
  <li><strong>Elopements: vows an hour before sunset.</strong> You get the ceremony in warm light and portraits right after.</li>
  <li><strong>Morning people:</strong> sunrise elopements mean empty trails and golden light on red rock.</li>
  <li><strong>Overcast? Don’t panic.</strong> Clouds act like a giant softbox, and a break at the horizon can produce the most dramatic sunsets.</li>
</ul>

<h2 id="blue">Don’t skip blue hour</h2>
<p>After the sun sets, stay ten more minutes. Blue hour is short, but the moody, cinematic frames from it are often couples’ favorites. Pair it with sparklers, a lantern or simply a quiet slow dance.</p>
<p>Want this built into a schedule automatically? The <a href="/tools/wedding-day-timeline-builder/">timeline builder</a> places your sunset portraits for you.</p>
""",
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "photo-and-video-should-you-hire-both",
        "title": "Wedding Photo and Video: Should You Hire Both?",
        "short": "Photo and video: hire both?",
        "seo_title": "Wedding Photographer and Videographer: Should You Hire Both?",
        "description": "Should you hire a wedding photographer and a videographer? The pros, costs and benefits of booking a single photo + film team, and when photo-only makes sense.",
        "excerpt": "What film captures that photos can’t, what it costs, and why one coordinated team beats two strangers.",
        "category": "Planning",
        "minutes": 6,
        "date": "2026-07-30",
        "image": "black-white-first-dance",
        "image_alt": "Black and white photo of a couple's first dance",
        "toc": [("why-film", "What film captures"), ("one-team", "Why one team"), ("cost", "What it costs"), ("skip", "When to skip film"), ("decide", "How to decide")],
        "body": """
<p class="lead">It’s one of the most common budget questions we hear. And the most common regret we hear from married couples? “I wish we’d gotten video.”</p>

<h2 id="why-film">What film captures that photos can’t</h2>
<ul>
  <li><strong>Voices.</strong> Your vows in your own words. Your grandmother’s toast.</li>
  <li><strong>Movement.</strong> The way the veil caught the wind, the spin on the dance floor.</li>
  <li><strong>Sound and music.</strong> The song you walked in to, the laughter, the cheering.</li>
</ul>
<p>Photographs are what you’ll hang on the wall and print in albums. Film is what you’ll watch on anniversaries and show your kids. They do different jobs.</p>

<h2 id="one-team">Why one team works better than two</h2>
<p>When a photographer and videographer have never met, they compete for the same angles, step into each other’s shots and plan two separate timelines. A single photo + film team plans one schedule, knows where the other will stand and moves as one quiet crew. You get better coverage with fewer people in your space.</p>
""" + fig("film-clapperboard", "Clapperboard held up in the desert") + """
<h2 id="cost">What it costs</h2>
<p>Nationally, wedding videography often costs about as much as photography. Booking both from one studio usually saves money because travel, planning and coordination are shared. At Zibetti, adding film to any photo collection is a $2,000 add-on that covers the same hours as your photos, and film-only collections start at $3,200. You can try combinations in our <a href="/pricing/#estimator">pricing estimator</a>.</p>

<h2 id="skip">When photo-only makes sense</h2>
<ul>
  <li>Very short elopements where it’s just the two of you and an officiant.</li>
  <li>Couples who genuinely never re-watch videos.</li>
  <li>A tight budget where the choice is film vs. a great photographer. Choose the great photographer.</li>
</ul>

<h2 id="decide">How to decide</h2>
<p>Ask yourself: twenty years from now, would you rather hear your vows or not? If the answer is “hear them,” at least add a short highlight film or a ceremony-only edit. Learn more on our <a href="/video/">wedding film page</a>.</p>
""",
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "how-much-does-a-destination-wedding-photographer-cost",
        "title": "How Much Does a Destination Wedding Photographer Cost?",
        "short": "Destination photographer cost",
        "seo_title": "Destination Wedding Photographer Cost (2026 Guide)",
        "description": "What a destination wedding photographer costs in 2026, what drives the price (travel, hours, film, albums) and how to compare quotes fairly.",
        "excerpt": "Typical price ranges, what’s usually included in travel pricing, and the hidden costs to ask about before you sign.",
        "category": "Destination tips",
        "minutes": 7,
        "date": "2026-07-16",
        "image": "beach-wedding-veil",
        "image_alt": "Bride and groom on a beach with a long veil",
        "toc": [("ranges", "Typical price ranges"), ("drives", "What drives the price"), ("included", "What should be included"), ("compare", "Comparing quotes"), ("save", "Ways to save")],
        "body": """
<p class="lead">Destination pricing can feel like a black box. Here’s how it actually works, from a team that prices it every week.</p>

<h2 id="ranges">Typical price ranges</h2>
<p>Every market is different, but for experienced photographers you’ll commonly see:</p>
<div class="table-scroll"><table>
  <thead><tr><th>Type of day</th><th>Common range</th><th>Zibetti starts at</th></tr></thead>
  <tbody>
    <tr><td>Local elopement (up to 4 hrs)</td><td>$1,800–$4,000</td><td>$2,400</td></tr>
    <tr><td>Local full wedding (8 hrs)</td><td>$3,000–$6,000</td><td>$3,600</td></tr>
    <tr><td>Stateside destination</td><td>$4,500–$9,000</td><td>$5,200</td></tr>
    <tr><td>International destination</td><td>$6,000–$12,000+</td><td>$6,500</td></tr>
  </tbody>
</table></div>
<p>Ranges are general market observations, not quotes. Build your own estimate in our <a href="/pricing/#estimator">pricing estimator</a>.</p>

<h2 id="drives">What drives the price</h2>
<ul>
  <li><strong>Travel days.</strong> A destination wedding often means two or three days away from home, not one.</li>
  <li><strong>Flights, lodging and rental cars.</strong> Some photographers bill these separately; others (like us) include them.</li>
  <li><strong>Hours of coverage</strong> and whether a second photographer is needed.</li>
  <li><strong>Film</strong>, which can be bundled at a discount with a single team.</li>
  <li><strong>Albums and prints.</strong></li>
</ul>
""" + fig("travel-planning-map", "Travel planning flat lay with a map, notebook and camera") + """
<h2 id="included">What should be included</h2>
<p>Ask every photographer for a written list. A good destination collection should include coverage hours, edited image count (we guarantee 300+ for short days and 500+ for full days), an online gallery, travel and lodging (or a clear estimate), and a turnaround time.</p>

<h2 id="compare">Comparing quotes fairly</h2>
<ol>
  <li>Convert every quote to an all-in number, including travel.</li>
  <li>Compare hours and image counts side by side.</li>
  <li>Ask about overtime rates — ours is $200/hour beyond the first hour of grace.</li>
  <li>Check the retainer and payment schedule (we take 50% to book, the rest a month before).</li>
  <li>Look at full galleries, not just highlights.</li>
</ol>

<h2 id="save">Ways to save</h2>
<ul>
  <li>Choose an off-peak month or a weekday.</li>
  <li>Combine your welcome party and wedding into fewer coverage hours.</li>
  <li>Book photo and film from the same studio.</li>
  <li>Skip the second shooter for guest counts under about 75.</li>
</ul>
<p>Planning a trip? Don’t miss <a href="/blog/how-to-travel-with-a-wedding-dress/">how to travel with a wedding dress</a>.</p>
""",
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "what-to-wear-for-engagement-photos",
        "title": "What to Wear for Engagement Photos: A Photographer’s Guide",
        "short": "What to wear for engagement photos",
        "seo_title": "What to Wear for Engagement Photos: Outfit Ideas",
        "description": "Engagement photo outfit ideas from a photographer: colors that work, what to avoid, and how to dress for mountains, deserts, cities and the beach.",
        "excerpt": "Colors that photograph beautifully, fabrics that move, and outfit ideas for mountain, desert and city sessions.",
        "category": "Sessions",
        "minutes": 6,
        "date": "2026-07-02",
        "image": "couple-holding-hands",
        "image_alt": "Bride and groom holding hands",
        "toc": [("rules", "Basic rules"), ("colors", "Colors that work"), ("location", "Dress for the location"), ("avoid", "What to avoid"), ("checklist", "Packing checklist")],
        "body": """
<p class="lead">Your engagement session is the warm-up for your wedding: a chance to get comfortable on camera and get images you’ll actually frame. What you wear matters more than you think.</p>

<h2 id="rules">The basic rules</h2>
<ul>
  <li><strong>Coordinate, don’t match.</strong> Pick a palette of two or three colors and each wear pieces from it.</li>
  <li><strong>Choose movement.</strong> Flowy dresses, long skirts, open jackets and scarves catch the wind and make photos feel alive.</li>
  <li><strong>Texture beats pattern.</strong> Knits, linen, suede and denim add depth without distracting.</li>
  <li><strong>Wear what you love.</strong> If you feel like yourself, it shows.</li>
</ul>

<h2 id="colors">Colors that photograph beautifully</h2>
<p>Earth tones (rust, olive, cream, camel, dusty blue) look great almost everywhere. Deep jewel tones are stunning in fall and winter. Soft neutrals feel timeless. Bright white can blow out in harsh sun; cream or ivory is more forgiving.</p>
""" + fig("fall-lake-wedding-portrait", "Couple in coordinated autumn tones beside a lake") + """
<h2 id="location">Dress for the location</h2>
<h3>Mountains &amp; forests</h3>
<p>Rich greens, cream knits, rust and burgundy. Boots with a heel for the walk in, and a blanket for cool evenings.</p>
<h3>Red rock &amp; desert</h3>
<p>Contrast with the orange: dusty blue, sage, cream, black or a bold emerald. Long flowing dresses look incredible in desert wind.</p>
<h3>Salt flats &amp; beaches</h3>
<p>Go bold — saturated colors pop against white salt or sand. Pack sunglasses for between shots.</p>
<h3>City</h3>
<p>Elevated and tailored: a sharp suit, a slip dress, a trench coat. Black and white is a classic for a reason.</p>

<h2 id="avoid">What to avoid</h2>
<ul>
  <li>Large logos and busy small patterns.</li>
  <li>Neon colors that cast color onto skin.</li>
  <li>Brand-new shoes you haven’t walked in.</li>
  <li>Everyone in head-to-toe denim.</li>
</ul>

<h2 id="checklist">Packing checklist</h2>
<ul>
  <li>Two outfits (one casual, one dressy)</li>
  <li>Comfortable shoes for walking and nicer shoes for photos</li>
  <li>Lint roller, bobby pins, lip color, water</li>
  <li>A blanket, a hat or a bottle of champagne as fun props</li>
</ul>
<p>Sessions start at $750 — see <a href="/pricing/">pricing</a> or check sunset for your date with the <a href="/tools/golden-hour-calculator/">golden hour calculator</a>.</p>
""",
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "utah-fall-wedding-photos",
        "title": "Fall Wedding Photos in Utah: When and Where to Find Peak Color",
        "short": "Utah fall wedding photos",
        "seo_title": "Utah Fall Wedding Photos: Peak Color Dates & Locations",
        "description": "When fall colors peak in Utah and where to take fall wedding, bridal and engagement photos — from Wasatch aspen groves to Zion cottonwoods.",
        "excerpt": "When the aspens turn, where to find them, and how to plan a fall bridal or engagement session in the Wasatch.",
        "category": "Locations",
        "minutes": 5,
        "date": "2026-06-18",
        "image": "bride-in-meadow",
        "image_alt": "Bride holding her bouquet in a golden meadow",
        "toc": [("when", "When color peaks"), ("where", "Where to go"), ("bridals", "Fall bridal sessions"), ("tips", "Fall planning tips")],
        "body": """
<p class="lead">Fall in Utah is short and spectacular. Mountains turn gold, red and orange, then winter arrives almost overnight. If you want fall color in your photos, timing is everything.</p>

<h2 id="when">When does fall color peak in Utah?</h2>
<p>Color moves downhill as the weeks go by. In a typical year:</p>
<ul>
  <li><strong>High elevations (Uintas, upper Alpine Loop):</strong> mid to late September.</li>
  <li><strong>Wasatch canyons near Provo, Salt Lake and Park City:</strong> late September to early October.</li>
  <li><strong>Valley floors:</strong> mid to late October.</li>
  <li><strong>Zion’s cottonwoods:</strong> late October to mid-November.</li>
</ul>
<p>Every year shifts by a week or more depending on temperature and moisture, so build flexibility into session dates.</p>

<h2 id="where">Where to go</h2>
<ul>
  <li><strong>The Alpine Loop</strong> between American Fork and Provo canyons — famous aspen groves.</li>
  <li><strong>Guardsman Pass</strong> above Park City.</li>
  <li><strong>Mirror Lake Highway</strong> for early-season color at the lakes.</li>
  <li><strong>Sundance</strong> for an intimate fall wedding with lodging.</li>
  <li><strong>Zion</strong> for late-season gold against red cliffs.</li>
</ul>
""" + fig("mountain-river-forest", "River running through a mountain forest") + """
<h2 id="bridals">Fall bridal and engagement sessions</h2>
<p>A bridal session — wearing your dress before the wedding — is a Utah favorite, and fall is the perfect time for it. Warm colors in the mountains and your bouquet can look like they were made for each other. Choose florals in burgundy, rust and cream, and plan the session for golden hour so the backlit leaves glow.</p>

<h2 id="tips">Fall planning tips</h2>
<ul>
  <li>Golden hour arrives earlier every week — check your date with the <a href="/tools/golden-hour-calculator/">golden hour calculator</a>.</li>
  <li>Mountain evenings get cold fast. Bring a coat for between shots.</li>
  <li>Weekends in peak color are busy; weekday sessions are calmer.</li>
  <li>Some mountain roads close for the season, typically in late fall. Check before you go.</li>
</ul>
<p>Looking for the right spot? Try the <a href="/tools/utah-elopement-location-finder/">location finder</a> with the season set to “Fall”.</p>
""",
    },
]
