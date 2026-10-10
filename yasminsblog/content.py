"""Page copy for the yasminsblog.com rebuild.

Every post keeps the exact URL the old Squarespace site used, because those are
the URLs that earned rankings (Semrush organic positions) and backlinks. The
copy is new: written as editorial guides, with no quotes or first-person
experiences attributed to anyone.
"""

SITE = {
    "name": "Yasmin's Blog",
    "host": "https://www.yasminsblog.com",
    "tagline": "New York food, culture & photography",
    "description": (
        "Yasmin's Blog is an independent New York journal about food, "
        "neighborhood institutions, culture and street photography."
    ),
    "email": "hello@yasminsblog.com",
    "updated": "2026-10-10",
}

CATEGORIES = {
    "Food": "Delis, noodle shops, coffee roasters, candy stores and the dollar slice: the places that make New York taste like New York.",
    "Culture": "Spirituality, tattoos, movement, zines and the communities that make the city more than its skyline.",
    "Photography": "Photo essays and notes on looking: subway portraits, storefronts and small details.",
    "Travel": "Short trips out of the city, from a day in New Orleans to the Italian coast.",
}

# Tag pages that ranked in search. Each lists the posts carrying the tag.
TAGS = {
    "porto+rico+importing+co": {
        "label": "Porto Rico Importing Co",
        "intro": "Everything we've written about Porto Rico Importing Co., the Greenwich Village coffee and tea merchant that has been roasting and selling beans since 1907.",
    },
    "jaden+smith": {
        "label": "Jaden Smith",
        "intro": "Posts touching on celebrity-led spirituality and the new wave of self-styled wellness, a conversation that public figures like Jaden Smith helped bring into the mainstream.",
    },
    "human.nyc": {
        "label": "human.nyc",
        "intro": "Portraits and people: posts about the New Yorkers you pass every day, on the subway, behind counters and in the studio.",
    },
    "new+york": {
        "label": "New York",
        "intro": "The full New York archive: food institutions, neighborhood shops, culture and street photography from all five boroughs.",
    },
}

POSTS = [
    # ------------------------------------------------------------------ 2020
    {
        "path": "/mamablog/2020/5/5/turkish-immigrant-restaurant-owners-in-new-york-amp-london",
        "title": "Turkish Immigrant Restaurant Owners in New York & London",
        "h1": "Turkish Immigrant Restaurant Owners in New York & London",
        "description": "How Turkish immigrant families built restaurant communities in New York and London, from ocakbaşı grills to bakeries, often to fund their children's future.",
        "keyword": "turkish immigrant restaurant owners",
        "category": "Food",
        "tags": ["new+york"],
        "dek": "Two cities, one story told thousands of times: a family opens a restaurant so the next generation doesn't have to.",
        "read": 7,
        "body": """
<p>Walk down Green Lanes in north London or Skillman Avenue in Sunnyside, Queens, and you'll see the same signs: <em>kebap</em>, <em>pide</em>, <em>lahmacun</em>, <em>ocakbaşı</em>. Behind most of them is a family that crossed a border, opened a kitchen and worked very long hours. This piece looks at what Turkish immigrant restaurant owners in New York and London have in common and where their stories split.</p>

<h2>Why restaurants?</h2>
<p>For many first-generation immigrants, a restaurant is the business that takes skills they already have. It doesn't need a recognized degree or perfect English to start. A family recipe, a few relatives who will work the counter and a lease are enough. In both cities, the Turkish restaurant became a way to earn money and also a way to keep a community together: a place to hear your own language, read a Turkish newspaper and find out who is hiring.</p>
<p>A theme comes up again and again in these family histories: the restaurant was never meant to be the children's future. It was there to pay for it. Parents worked double shifts at the grill so their kids could study law, medicine or engineering. In many of these families, the restaurant works as a tuition fund, and the long hours are spent for the sake of the kids' education.</p>

<h2>London: Green Lanes, Dalston and the ocakbaşı</h2>
<p>London's Turkish and Turkish-Cypriot community grew from the 1950s on, and later arrivals from mainland Turkey and Kurdish regions added to it. North and east London became the center: Harringay's Green Lanes, Stoke Newington and Dalston. The grill restaurant, or <strong>ocakbaşı</strong>, defines these streets. Diners sit around a charcoal grill hood while the <em>usta</em> (master griller) works skewers of lamb, chicken wings and adana kebab over open coals.</p>
<p>London's Turkish restaurants also shaped the city's late-night food culture. The neighborhood kebab shop is now so normal in Britain that people forget it was an immigrant business model. Families built it shop by shop, with long opening hours, small margins and a lot of loyalty from regulars.</p>

<h2>New York: Sunnyside, Bay Ridge and Paterson's "Little Istanbul"</h2>
<p>The Turkish community in the New York area is smaller and more spread out. Restaurants cluster in Sunnyside and Astoria in Queens, around Bay Ridge in Brooklyn, and across the river in Paterson, New Jersey, whose Main Street area is often called "Little Istanbul." Manhattan has its own mix, from casual pide and döner counters in Midtown to sit-down meyhane-style dining rooms.</p>
<p>New York's restaurant economy is brutal in its own way. Rents are high, competition is constant and the clientele changes from block to block. Turkish owners here often lean on what sets them apart. They bake their own bread, or they run a <strong>pide</strong> oven or a real <strong>baklava</strong> counter. Some sell to the wider Mediterranean market and some to fellow Turks who want breakfast the way it's served at home: olives, white cheese, tomatoes, cucumbers, simit and endless tea.</p>

<h2>What the two cities share</h2>
<ul>
  <li><strong>Family labor.</strong> Spouses, siblings and teenage children cover shifts. The business works because labor costs are absorbed by the family.</li>
  <li><strong>Hospitality as identity.</strong> A free glass of tea or a plate of fruit at the end of the meal isn't a promotion. It comes from the culture of <em>misafirperverlik</em>, taking care of the guest.</li>
  <li><strong>Education as the goal.</strong> The restaurant pays for school. Many owners hope it closes with them rather than passing down.</li>
  <li><strong>A community hub.</strong> Restaurants double as informal job boards, translation services and places to celebrate.</li>
</ul>

<h2>Where they differ</h2>
<p>London's scene is denser and older, so it has more specialization. You'll find dedicated ocakbaşı grills, Cypriot meze houses and Kurdish-run cafés. New York's is younger and more mixed. One restaurant may serve as bakery, grill and café at once, and owners often market themselves as "Mediterranean" to reach a wider audience. In London, being Turkish is the draw. In New York, it's sometimes something you explain on the menu.</p>

<h2>The pandemic test</h2>
<p>When dining rooms closed in spring 2020, family-run immigrant restaurants were among the most exposed businesses in both cities. They had thin cash reserves and landlords who still expected rent. Many of them were also slow to get onto delivery platforms. The ones that survived usually did it the way they had always worked: family members took unpaid shifts, menus got shorter and regulars kept ordering. More on the city's food institutions is in our <a href="/mamablog/category/Food">Food</a> archive.</p>

<h2>How to support them</h2>
<p>Order directly from the restaurant rather than through a high-commission app. Tip properly, and go back. Ask what's good today. In most Turkish kitchens the answer is whatever came out of the oven an hour ago.</p>
""",
    },
    {
        "path": "/mamablog/2020/6/26/4-photos-from-salerno",
        "title": "4 Photos from Salerno: Light, Lemons and the Amalfi Coast",
        "h1": "4 Photos from Salerno",
        "description": "A four-frame photo essay from Salerno, the port city at the edge of Italy's Amalfi Coast: lemon stalls, the lungomare promenade, steep alleys and evening light.",
        "keyword": "4 photos from salerno",
        "category": "Photography",
        "tags": ["human.nyc"],
        "dek": "The \"4 Photos\" series takes four frames and nothing else. This time it's the Italian port city most travelers rush past on the way to Positano.",
        "read": 3,
        "photos": [
            ("The lungomare", "Salerno's seafront promenade runs for more than a kilometer under palm and holm-oak trees. At dusk the whole city seems to come out to walk it."),
            ("Lemon stalls", "The Amalfi Coast's sfusato lemons are huge, knobbly and fragrant. Market stalls stack them next to bottles of limoncello."),
            ("Up the steps", "The centro storico climbs the hill in narrow staircases and arches. Look up and you'll see laundry lines and the castle on the ridge."),
            ("Duomo bells", "The cathedral of San Matteo, consecrated in the 11th century, has a Romanesque bell tower that still marks the hours over the old town."),
        ],
        "body": """
<p>Salerno is where the Amalfi Coast road starts. Ferries run from its harbor to Amalfi and Positano, and most visitors only see it from the dock. That's a shame. The city has a long seafront promenade, a medieval old town and a cathedral with more than 900 years of history.</p>
<p>The "4 Photos" format is simple: four frames that together give you the feel of a place. Here they are below as illustrated plates, each with a caption.</p>
""",
        "after": """
<h2>If you go</h2>
<ul>
  <li><strong>Getting there:</strong> Salerno is on Italy's main high-speed rail line, a short ride south of Naples.</li>
  <li><strong>Base yourself here:</strong> Hotels cost less than on the coast, and ferries leave from the harbor for Amalfi, Positano and beyond.</li>
  <li><strong>Walk the lungomare at sunset.</strong> It's what everyone in town does.</li>
  <li><strong>Visit the Duomo of San Matteo</strong> and its crypt, then get lost in the alleys of the centro storico.</li>
</ul>
<p>More from the series: <a href="/mamablog/2020/6/13/4-photos-from-economy-candy">4 Photos from Economy Candy</a>.</p>
""",
    },
    {
        "path": "/mamablog/2020/6/13/4-photos-from-economy-candy",
        "title": "4 Photos from Economy Candy, NYC's Lower East Side Candy Store",
        "h1": "4 Photos from Economy Candy",
        "description": "Inside Economy Candy, the Lower East Side candy store on Rivington Street selling old-fashioned sweets since 1937. A four-photo essay plus a visitor's guide.",
        "keyword": "economy candy store nyc",
        "category": "Photography",
        "tags": ["new+york", "human.nyc"],
        "dek": "Floor-to-ceiling bins, retro wrappers and halvah by the slab: a Lower East Side institution in four frames.",
        "read": 4,
        "photos": [
            ("The wall of bins", "Clear bins run floor to ceiling, holding jelly beans, gummies, malt balls and more licorice than you knew existed."),
            ("Retro wrappers", "Economy Candy is known for nostalgia candy: brands you remember from childhood and some you thought had been discontinued."),
            ("Halvah & dried fruit", "Some of its Lower East Side roots show at the counter: halvah, nuts and dried fruit sold by weight."),
            ("Rivington Street", "The storefront at 108 Rivington Street has been selling sweets to the neighborhood since 1937."),
        ],
        "body": """
<p><strong>Economy Candy</strong> has been on the Lower East Side since 1937, which makes it one of the oldest candy stores in New York City. It started as a neighborhood shop selling sweets to a working-class, largely immigrant population. It has since become a destination, packed with tourists, kids and adults hunting for a candy bar they haven't seen in thirty years.</p>
<p>The "4 Photos" series takes four frames that together give you the feel of a place. Here they are below as illustrated plates, each with a caption.</p>
""",
        "after": """
<h2>Visiting Economy Candy</h2>
<ul>
  <li><strong>Where:</strong> 108 Rivington Street, between Essex and Ludlow, on the Lower East Side.</li>
  <li><strong>What to buy:</strong> Nostalgia candy, international sweets, halvah, chocolate-covered everything, and bulk bins priced by the pound.</li>
  <li><strong>When:</strong> Weekday mornings are calmer. Weekend afternoons get crowded. Check current hours before you go.</li>
  <li><strong>Make a day of it:</strong> It's a short walk to <a href="/mamablog/2018/1/20/katz-deli-some-delicious-pastrami">Katz's Delicatessen</a> and the <a href="/mamablog/2018/10/30/its-more-than-just-a-slice-to-end-the-night">late-night dollar slice</a> spots on the Lower East Side.</li>
</ul>
<p>Next in the series: <a href="/mamablog/2020/6/26/4-photos-from-salerno">4 Photos from Salerno</a>.</p>
""",
    },
    {
        "path": "/mamablog/2020/3/28/24-hours-in-new-orleans-a-mini-mardi-gras-bender",
        "title": "24 Hours in New Orleans: A Mini Mardi Gras Bender",
        "h1": "24 Hours in New Orleans: A Mini Mardi Gras Bender",
        "description": "How to spend 24 hours in New Orleans during Carnival season: beignets, parades, the St. Charles streetcar, king cake and live music on Frenchmen Street.",
        "keyword": "24 hours in new orleans",
        "category": "Travel",
        "tags": [],
        "dek": "One day, one city, one very full itinerary for Carnival season. Wear comfortable shoes.",
        "read": 6,
        "body": """
<p>New Orleans rewards a short trip better than almost any American city. Everything you came for is close together: food, music, architecture and a culture of celebration that peaks during <strong>Mardi Gras</strong>. You can't see it all in 24 hours, but you can get a good taste. Here's a one-day plan for Carnival season.</p>

<h2>Morning: beignets and the French Quarter</h2>
<p>Start the classic way: beignets under a snowdrift of powdered sugar and a café au lait at <strong>Café du Monde</strong> on Decatur Street, which has been serving them since 1862. Go early because the line builds fast. Then walk it off through the French Quarter. Jackson Square, St. Louis Cathedral and the cast-iron balconies of Royal Street look their best before the crowds arrive.</p>

<h2>Midday: the St. Charles streetcar</h2>
<p>Catch the <strong>St. Charles Avenue streetcar</strong>, which has been running for well over a century. Ride it through the Garden District under live oaks, past grand mansions. During Carnival, the oaks along the parade route are draped in beads thrown from earlier floats. Hop off for lunch. A po'boy (roast beef "debris" or fried shrimp) or a bowl of gumbo is the right call.</p>

<h2>Afternoon: parade time</h2>
<p>In the weeks before Fat Tuesday, krewes roll almost every day. Check the parade schedule and stake out a spot along St. Charles or Napoleon Avenue. Bring a bag for throws, stand behind any barricades and don't step between floats. Families set up ladders along the route for kids to sit in, and that's part of the scene.</p>
<p>Snack on <strong>king cake</strong> while you wait. It's a ring of sweet dough in purple, green and gold sugar, sold all Carnival season. Whoever finds the tiny plastic baby inside traditionally buys the next one.</p>

<h2>Evening: dinner and Frenchmen Street</h2>
<p>For dinner, choose between Creole fine dining in an old-line dining room and a casual plate of red beans and rice or boiled crawfish if they're in season. Then head to <strong>Frenchmen Street</strong> in the Marigny. Its clubs and bars have live jazz, brass bands and blues every night. It's where locals go to hear music without the chaos of Bourbon Street.</p>

<h2>Late night</h2>
<p>New Orleans doesn't really close. If you have energy left, grab a late bite, wander the quieter blocks of the Quarter and finish the loop with a second round of beignets.</p>

<h2>Quick tips</h2>
<ul>
  <li><strong>Book early.</strong> Hotels fill up and prices climb for Carnival weekends.</li>
  <li><strong>Walk or take the streetcar.</strong> Parade routes close streets, and driving is a headache.</li>
  <li><strong>Carry cash</strong> for small vendors, and keep your phone charged for the parade-tracking apps.</li>
  <li><strong>Respect the neighborhoods.</strong> People live here year-round.</li>
</ul>
""",
    },
    # ------------------------------------------------------------------ 2019
    {
        "path": "/mamablog/2019/11/2/young-women-come-together-at-photoville-for-this-is-18-a-zine-by-the-nytimes",
        "title": "Photoville and \"This Is 18\", a New York Times Zine",
        "h1": "Young Women Come Together at Photoville for \"This Is 18\"",
        "description": "The New York Times' \"This Is 18\" project showed what life looks like for 18-year-old girls around the world, photographed by women. Here's why it resonated at Photoville.",
        "keyword": "this is 18 new york times photoville",
        "category": "Culture",
        "tags": ["new+york", "human.nyc"],
        "dek": "A global portrait of being eighteen, made by women photographers, and a reminder of why print zines still matter.",
        "read": 5,
        "body": """
<p>In 2018, <strong>The New York Times</strong> published <em>"This Is 18,"</em> an ambitious visual project about what it means to be an 18-year-old girl in different parts of the world. The project paired young women with women photographers across many countries. The result was a mosaic of school, work, faith, love, ambition and ordinary days. Editors including <strong>Jessica Bennett</strong> and <strong>Anya Strzemien</strong> were among the people behind it.</p>

<h2>Why the project mattered</h2>
<p>Most images of teenage girls are made by someone else: advertisers, news photographers, social feeds. <em>This Is 18</em> turned that around. It commissioned women photographers, many of them from the regions they were documenting. It also built the stories around the girls' own words about their lives, worries and hopes. The project treated eighteen as what it is: the edge of adulthood, with very different stakes depending on where you happen to be born.</p>

<h2>From screen to zine</h2>
<p>The project also lived on paper. A printed zine and in-person events took it beyond the website. That's where <strong>Photoville</strong> comes in. The free outdoor photography festival, best known for exhibitions in repurposed shipping containers around Brooklyn Bridge Park, is a natural home for this kind of work. People walk in off the street, families wander through, and teenagers see faces that look like theirs on the walls.</p>
<p>A zine invites a different kind of attention than a scrolling feed. You hold it, flip back, linger on a portrait and pass it to a friend. Young women at gatherings like this tend to do just that: they compare the pictures to their own lives and talk about the ones that stuck with them.</p>

<h2>Why it still resonates</h2>
<ul>
  <li><strong>Representation by women, of women.</strong> Who holds the camera changes the picture.</li>
  <li><strong>Global, but personal.</strong> Each image is specific. Together they show a shared stage of life.</li>
  <li><strong>Print as community.</strong> Zines and festivals turn a media project into something people gather around.</li>
</ul>

<h2>See for yourself</h2>
<p>Look for the original <em>This Is 18</em> feature in The New York Times archive, and check Photoville's site for current festival dates. It returns to New York regularly and is free to attend. For more photography, see our <a href="/mamablog/category/Photography">Photography</a> archive.</p>
""",
    },
    {
        "path": "/mamablog/2019/5/12/on-pole-dancing-with-shawanda-davis",
        "title": "On Pole Dancing: Strength, Artistry and Community in New York",
        "h1": "On Pole Dancing: Strength, Artistry and Community",
        "description": "Pole dancing has moved from the club to the studio and the competition stage. A look at pole fitness in New York: its history, the strength it takes and how to start.",
        "keyword": "pole dancing new york",
        "category": "Culture",
        "tags": ["new+york", "human.nyc"],
        "dek": "It's a sport, an art form and a community. It's also some of the hardest strength training you'll ever do.",
        "read": 6,
        "body": """
<p>Ask anyone who has taken a pole class what surprised them most and the answer is almost always the same: <strong>how hard it is</strong>. Pole dancing asks for grip strength, core control, flexibility and a lot of nerve. In New York, it has grown from a niche into a big network of studios, instructors and performers who take it seriously as both art and athletics.</p>

<h2>A short history</h2>
<p>Dancing on a pole has roots in very different traditions. Indian <em>mallakhamb</em> uses a wooden pole for gymnastic feats, and Chinese pole acrobatics is a circus discipline. The modern form people recognize grew up in clubs in North America. From the 2000s on, fitness studios reclaimed it as a workout. Today there are international competitions, scoring codes and a push by athletes to have <strong>pole sports</strong> recognized alongside gymnastics.</p>

<h2>What it takes</h2>
<ul>
  <li><strong>Strength:</strong> Climbs, holds and inversions build serious upper-body and core strength.</li>
  <li><strong>Flexibility:</strong> Advanced shapes need open shoulders, hips and backs, built gradually.</li>
  <li><strong>Skin grip:</strong> Bare skin holds the pole, which is why dancers wear shorts. It isn't about costume.</li>
  <li><strong>Patience:</strong> Bruises and slow progress come with the territory. Everyone starts with spins and walks.</li>
</ul>

<h2>The community</h2>
<p>Pole studios often say they're built on body positivity and on people supporting each other. Classes mix ages, body types, genders and backgrounds. A beginner's first climb gets the same cheering as an advanced dancer's new combo. For many people, the studio becomes the place they built confidence as well as muscle.</p>
<p>New York has studios across the boroughs, from fitness-focused gyms to spaces centered on performance, choreography and "exotic" styles that celebrate pole's club heritage. Instructors here usually have backgrounds in dance, gymnastics, circus or competition, and many run showcases where students perform.</p>

<h2>How to start</h2>
<ol>
  <li><strong>Book an intro class.</strong> Most studios offer beginner sessions with no experience needed.</li>
  <li><strong>Wear shorts and a tank top</strong>, and skip lotion that day: it makes the pole slippery.</li>
  <li><strong>Expect to feel it the next day</strong>, especially in your forearms and shoulders.</li>
  <li><strong>Go regularly.</strong> Strength builds fast with consistency.</li>
</ol>
<p>Pole is part of a bigger story about New Yorkers redefining what movement and self-expression look like. Read more in our <a href="/mamablog/category/Culture">Culture</a> archive.</p>
""",
    },
    {
        "path": "/mamablog/2019/5/9/more-than-skin-deep-with-byron-kim",
        "title": "More Than Skin Deep: Stick and Poke Tattoos and the Hand-Poke Revival",
        "h1": "More Than Skin Deep: The Hand-Poke Tattoo Revival",
        "description": "Stick and poke tattoos have moved from DIY to fine-art studios in New York and Tokyo. What hand-poking is, how it differs from machine work and how to find an artist.",
        "keyword": "stick and poke tattoo",
        "category": "Culture",
        "tags": ["new+york", "human.nyc"],
        "dek": "No machine, no buzz: just a needle, ink and a lot of patience. Why hand-poked tattoos are having a moment.",
        "read": 6,
        "body": """
<p>Tattooing started as a hand craft. Long before electric machines, people around the world put ink into skin by hand, with tapping, poking and stitching techniques. Today <strong>hand-poked tattoos</strong> (often called "stick and poke") are having a real revival, especially in New York, Tokyo and other cities with strong tattoo cultures.</p>

<h2>What is a hand-poked tattoo?</h2>
<p>A hand-poked tattoo is made by pushing a single needle (or a small grouping) into the skin by hand, one dot at a time. There's no motor and no buzzing. The artist builds lines and shading from many tiny points. Done professionally, with sterile, single-use needles and quality tattoo ink, the results can be crisp, delicate and very detailed.</p>

<h2>Hand-poke vs. machine</h2>
<ul>
  <li><strong>Feel:</strong> Many clients find hand-poking gentler and quieter, though it takes longer.</li>
  <li><strong>Look:</strong> Hand-poked work often has a soft, textured, dotted quality that suits fine line, minimal and illustrative designs.</li>
  <li><strong>Healing:</strong> It can be less traumatic to the skin, so some people heal faster. Aftercare still matters just as much.</li>
  <li><strong>Time:</strong> Expect longer sessions for the same size piece.</li>
</ul>

<h2>From DIY to the studio</h2>
<p>"Stick and poke" used to mean a sewing needle, thread and pen ink in someone's bedroom, and that carries real infection and blowout risks. The revival is different. Professional hand-poke artists work in licensed studios or private appointment-only spaces. They use proper sterilization and treat the technique as a deliberate artistic choice.</p>
<p>In <strong>Tokyo</strong>, hand techniques have deep roots: traditional Japanese <em>tebori</em> uses a hand tool to create the large bodysuits associated with Japanese tattooing. A newer generation of artists in Tokyo and New York uses hand-poking for small, personal, fine-art pieces, and many travel between the two cities doing guest spots.</p>

<h2>How to find a good artist</h2>
<ol>
  <li><strong>Study portfolios</strong> and look for healed photos, not just fresh ones.</li>
  <li><strong>Ask about hygiene:</strong> single-use needles, gloves, barrier film and a clean workspace are non-negotiable.</li>
  <li><strong>Check licensing</strong> where it's required. In New York City, tattoo artists need a license from the city's health department.</li>
  <li><strong>Book a consultation</strong> to talk about placement, size and how your design will age.</li>
</ol>

<h2>Why it matters</h2>
<p>For many people, a hand-poked tattoo is about the process as much as the result. It's slow and quiet, and you have to trust the artist. It's a reminder that a tattoo is more than skin deep. More stories about the city's makers are in our <a href="/mamablog/tag/human.nyc">human.nyc</a> archive.</p>
""",
    },
    {
        "path": "/mamablog/2019/1/2/pies-thighs-and-all-things-nice",
        "title": "Pies 'n' Thighs and All Things Nice: Brooklyn's Fried Chicken & Biscuits",
        "h1": "Pies 'n' Thighs and All Things Nice",
        "description": "Pies 'n' Thighs in Williamsburg serves Southern comfort food: fried chicken, biscuits, donuts and pie. What to order for brunch and how to plan your visit.",
        "keyword": "pies n thighs brunch",
        "category": "Food",
        "tags": ["new+york"],
        "dek": "Fried chicken, warm biscuits and a slice of pie: Brooklyn's favorite Southern-style brunch, explained.",
        "read": 5,
        "body": """
<p>Few New York restaurants have a name that tells you so exactly what you'll eat. <strong>Pies 'n' Thighs</strong> is a Williamsburg, Brooklyn favorite for Southern-style comfort food. Think crisp fried chicken, tall biscuits, donuts and a rotating case of pies. It has been a neighborhood fixture since the mid-2000s, and at brunch the line is part of the experience.</p>

<h2>What to order</h2>
<ul>
  <li><strong>The fried chicken.</strong> Crunchy, well-seasoned and juicy, with thighs as the namesake for good reason. Get the box with a biscuit and a side.</li>
  <li><strong>Chicken biscuit.</strong> Fried chicken on a flaky biscuit, often with hot sauce and honey butter. It's the brunch move.</li>
  <li><strong>Donuts.</strong> Yeasted, glazed and filled varieties that sell out.</li>
  <li><strong>Pie.</strong> The other half of the name: seasonal fruit pies, cream pies and Southern classics. Take a slice to go even if you're full.</li>
  <li><strong>Sides.</strong> Mac and cheese, collard greens, grits and the like. Choose comfort over restraint.</li>
</ul>

<h2>Brunch tips</h2>
<ol>
  <li><strong>Go early or late.</strong> Weekend brunch peaks late morning, so arrive near opening or mid-afternoon.</li>
  <li><strong>Bring a friend</strong> so you can split a chicken plate and a sweet.</li>
  <li><strong>Check the hours and menu</strong> before you go. They change, and some items are only made in limited batches.</li>
</ol>

<h2>Make a day of it</h2>
<p>Williamsburg is easy to walk. After brunch, head to the waterfront for Manhattan skyline views or browse the shops along Bedford Avenue. Coffee nerds can keep going with our guides to <a href="/mamablog/2018/2/17/mountain-province">Mountain Province</a> and <a href="/mamablog/2018/10/20/porto-rico-importing-co">Porto Rico Importing Co.</a></p>
""",
    },
    # ------------------------------------------------------------------ 2018
    {
        "path": "/mamablog/2018/12/17/defining-your-own-rules-welcome-to-the-new-age-of-spirituality",
        "title": "Defining Your Own Rules: Welcome to the New Age of Spirituality",
        "h1": "Defining Your Own Rules: Welcome to the New Age of Spirituality",
        "description": "Tarot, crystals, witchcraft and shops like Catland Books in Brooklyn: how a generation builds a DIY spirituality, plus what eggshells mean in witchcraft.",
        "keyword": "new age spirituality",
        "category": "Culture",
        "tags": ["new+york", "jaden+smith"],
        "dek": "Tarot apps, moon circles and occult bookstores: why so many young New Yorkers are writing their own spiritual rulebook.",
        "read": 7,
        "body": """
<p>Fewer young Americans identify with organized religion than any generation before them. But that doesn't mean they've stopped looking for meaning. Many are putting together a personal, mix-and-match spirituality from tarot, astrology, crystals, meditation, herbalism and modern witchcraft. The rules are theirs to write.</p>

<h2>A spirituality without gatekeepers</h2>
<p>The appeal is easy to see. Personal practice doesn't need a congregation, a dogma or permission. You can pull a tarot card in the morning, track the moon's phases, set intentions and still feel free to drop what doesn't work. Social media sped it all up: witchy creators on TikTok and Instagram, astrology apps and celebrities who talk openly about energy, manifestation and alternative belief. Public figures such as Jaden Smith, with his openly philosophical and unconventional takes on life, helped make this kind of exploration feel mainstream for a younger audience.</p>

<h2>The shops: Catland and the occult bookstore</h2>
<p>New York has a long line of metaphysical shops, and a new generation has given it fresh energy. <strong>Catland Books</strong> in Bushwick, Brooklyn, is one of the best known. It's an occult bookstore and community space selling books, candles, herbs and tools, and it hosts classes and workshops on tarot, witchcraft, astrology and more. Spaces like this work as gathering places. People go to learn and meet others, not only to shop.</p>

<h2>Eggshells in witchcraft</h2>
<p>One small, practical example of how folk traditions get passed along: <strong>eggshells</strong>. In many folk-magic and modern witchcraft practices, eggs and eggshells stand for protection, fertility and new beginnings. The best-known use is <strong>cascarilla</strong>, a fine white powder made from ground eggshells, which comes from Afro-Caribbean and Latin American traditions. Practitioners use it for:</p>
<ul>
  <li><strong>Protection:</strong> drawing lines or symbols at doorways and windows.</li>
  <li><strong>Cleansing:</strong> adding it to spiritual baths or sprinkling it in a space.</li>
  <li><strong>Ritual markings:</strong> drawing sigils or circles on altars and candles.</li>
</ul>
<p>If you're curious about traditions with specific cultural roots, learn where they come from and who keeps them alive. Shops and teachers who credit those origins are a good sign.</p>

<h2>Defining your own rules, responsibly</h2>
<ol>
  <li><strong>Start with curiosity, not purchases.</strong> Books, classes and conversation come before an expensive crystal haul.</li>
  <li><strong>Respect closed practices.</strong> Some traditions are meant to be learned within a community.</li>
  <li><strong>Keep your judgment.</strong> Spiritual practice can support mental health but shouldn't replace medical care.</li>
  <li><strong>Find your people.</strong> Workshops and moon circles are where practice turns into community.</li>
</ol>
<p>More from New York's culture scene: <a href="/mamablog/2019/5/9/more-than-skin-deep-with-byron-kim">the hand-poke tattoo revival</a> and <a href="/mamablog/2019/5/12/on-pole-dancing-with-shawanda-davis">pole dancing as art and sport</a>.</p>
""",
    },
    {
        "path": "/mamablog/2018/10/30/its-more-than-just-a-slice-to-end-the-night",
        "title": "It's More Than Just a Slice to End the Night: NYC's Dollar Pizza",
        "h1": "It's More Than Just a Slice to End the Night",
        "description": "The cheap slice is a New York institution. A guide to dollar pizza on the Lower East Side: its history, why prices crept up and where to get a late-night slice.",
        "keyword": "dollar pizza lower east side",
        "category": "Food",
        "tags": ["new+york"],
        "dek": "Cheap, hot and open late: the New York dollar slice is street food, a social equalizer and the city's unofficial nightcap.",
        "read": 5,
        "body": """
<p>Two a.m. on the Lower East Side. The bars are letting out and the subway is a gamble, and there's one bright window still open: the cheap-slice joint. A thin, foldable, slightly greasy slice of cheese pizza handed over on a paper plate is one of New York's great equalizers. Students, bartenders, line cooks, bankers and tourists all eat the same thing standing at the same counter.</p>

<h2>A brief history of the dollar slice</h2>
<p>The <strong>dollar slice</strong> took off in New York in the 2000s, when a handful of shops, with <strong>2 Bros. Pizza</strong> the best known, made a business of selling cheese slices for a single dollar. The model ran on volume, a simple menu and fast ovens. Competitors such as 99 Cent Fresh Pizza followed, and the cheap slice became a fixture near transit hubs, campuses and nightlife strips like the Lower East Side.</p>

<h2>Why it isn't always a dollar anymore</h2>
<p>Rising rent, wages, flour and cheese prices have pushed many shops to $1.50 or more, and the true one-dollar slice is getting harder to find. The spirit hasn't changed, though. The cheap slice is still the city's most affordable hot meal, and it's still the default way to end a night out.</p>

<h2>How to eat it like a New Yorker</h2>
<ul>
  <li><strong>Fold it.</strong> The lengthwise fold keeps the tip from flopping and the oil off your shirt.</li>
  <li><strong>Add the shakers.</strong> Garlic powder, red pepper flakes, oregano and Parmesan are free and essential.</li>
  <li><strong>Eat it standing up</strong>, ideally on the sidewalk.</li>
  <li><strong>Don't expect artisanal.</strong> That isn't the point.</li>
</ul>

<h2>The Lower East Side late-night circuit</h2>
<p>The LES is one of the best neighborhoods in the city for after-hours food. Cheap slice shops sit a few blocks from <a href="/mamablog/2018/1/20/katz-deli-some-delicious-pastrami">Katz's Delicatessen</a>, where pastrami is a different kind of late-night indulgence, and the sweets at <a href="/mamablog/2020/6/13/4-photos-from-economy-candy">Economy Candy</a> on Rivington Street. Check current hours, since late-night schedules change often.</p>

<h2>More than a slice</h2>
<p>Pizza snobs can argue about coal ovens and sourdough crusts. The cheap slice keeps going because it does one thing perfectly: it feeds anyone, at any hour, for almost nothing. That's a very New York kind of hospitality.</p>
""",
    },
    {
        "path": "/mamablog/2018/10/20/porto-rico-importing-co",
        "title": "Porto Rico Importing Co.: Greenwich Village's Coffee Institution Since 1907",
        "h1": "Porto Rico Importing Co.",
        "description": "Porto Rico Importing Co. has sold coffee and tea on Bleecker Street since 1907. A guide to the NYC coffee shop: what to buy, the bean bins and wholesale coffee.",
        "keyword": "porto rico coffee nyc",
        "category": "Food",
        "tags": ["porto+rico+importing+co", "new+york"],
        "dek": "Burlap sacks, wooden bins and the smell of roasting beans: a Greenwich Village coffee merchant that has outlasted every trend.",
        "read": 6,
        "body": """
<p>Long before third-wave coffee and latte art, <strong>Porto Rico Importing Co.</strong> was selling coffee by the pound in Greenwich Village. Founded in <strong>1907</strong>, the shop on <strong>Bleecker Street</strong> is one of New York's oldest coffee merchants. It has been family-run for decades and is beloved for its huge selection, fair prices and old-world feel.</p>

<h2>What makes it special</h2>
<ul>
  <li><strong>The selection.</strong> Dozens of single-origin coffees, blends, flavored coffees and decafs, plus loose-leaf teas, scooped from bins and sacks.</li>
  <li><strong>The prices.</strong> Porto Rico has long been known as one of the better values for whole-bean coffee in Manhattan.</li>
  <li><strong>The atmosphere.</strong> Burlap, wood, hand-written labels and staff who will happily talk roast levels and brewing methods.</li>
  <li><strong>The history.</strong> More than a century in the same neighborhood, through every change Greenwich Village has seen.</li>
</ul>

<h2>How to shop like a regular</h2>
<ol>
  <li><strong>Know your brew method.</strong> Tell staff whether you use espresso, drip, French press or pour-over, and they'll grind to match. Or buy whole bean and grind at home.</li>
  <li><strong>Try a house blend.</strong> House blends are a good way into the selection.</li>
  <li><strong>Buy small and often.</strong> Coffee tastes best within a few weeks of roasting.</li>
  <li><strong>Don't skip the tea wall.</strong> The loose-leaf selection rivals the coffee.</li>
</ol>

<h2>Porto Rico coffee wholesale</h2>
<p>Porto Rico also supplies coffee <strong>wholesale</strong> to cafés, restaurants and offices. If you run a business and want a long-established New York roaster behind your coffee program, contact the company directly for current wholesale pricing and minimums.</p>

<h2>Visiting</h2>
<p>The flagship is at <strong>201 Bleecker Street</strong> in Greenwich Village. Over the years the company has run other New York locations as well, so check its website for current shops and hours before you go.</p>
<p>See all of our posts tagged <a href="/mamablog/tag/porto+rico+importing+co">Porto Rico Importing Co</a>, or keep the coffee crawl going at <a href="/mamablog/2018/2/17/mountain-province">Mountain Province</a>.</p>
""",
        "faq": [
            ("When was Porto Rico Importing Co. founded?", "Porto Rico Importing Co. was founded in 1907 in Greenwich Village, making it one of New York City's oldest coffee merchants."),
            ("Where is Porto Rico Importing Co.?", "The flagship store is at 201 Bleecker Street in Greenwich Village, Manhattan. Check the company's website for its other current locations and hours."),
            ("Does Porto Rico sell coffee wholesale?", "Yes. Porto Rico Importing Co. supplies coffee wholesale to cafés, restaurants and offices. Contact the company for current pricing."),
        ],
    },
    {
        "path": "/mamablog/2018/9/11/journalistic-inquiry-notes-quotes-and-details",
        "title": "Journalistic Inquiry: Notes, Quotes and Details from a NYC Ramen Festival",
        "h1": "Journalistic Inquiry: Notes, Quotes and Details",
        "description": "What reporting on a New York ramen festival teaches about food journalism: how to take notes, gather quotes and catch details. Plus our favorite ramen quotes.",
        "keyword": "ramen quotes",
        "category": "Food",
        "tags": ["new+york"],
        "dek": "A food festival is a crash course in reporting: noisy, crowded and full of small details worth writing down.",
        "read": 6,
        "body": """
<p>New York's ramen festivals bring dozens of shops, some local and some flown in from Japan, under one roof or tent for a day of slurping. They're also an excellent place to practice <strong>journalistic inquiry</strong>. There are long lines to watch, chefs to talk to, ingredients to identify and a thousand small details to notice. Here's how to cover a food event and come home with a story, not just a full stomach.</p>

<h2>Notes: write down everything, then a bit more</h2>
<ul>
  <li><strong>Who:</strong> Shop names, chef names (spelled correctly), and where each shop is from.</li>
  <li><strong>What:</strong> Broth style (tonkotsu, shoyu, shio, miso), noodle thickness, toppings, portion size and price.</li>
  <li><strong>Sensory details:</strong> The fog over a pot of pork bone broth, the sound of a crowd slurping, the color of a tare.</li>
  <li><strong>Numbers:</strong> Wait times, bowls served, how long a broth simmers. Numbers make a story concrete.</li>
</ul>

<h2>Quotes: ask open questions</h2>
<p>The best quotes come from questions that can't be answered with yes or no. "What's the hardest part of this bowl?" gets more than "Is this hard to make?" Ask chefs about their first bowl of ramen, ask festival-goers why they waited 40 minutes, and record (with permission) so you can quote people exactly. Never tidy up a quote into something the person didn't say.</p>

<h2>Details: the story is in the small things</h2>
<p>Anyone can write "the ramen was delicious." A reporter notices the chef tasting the broth between every batch, the hand-written sign apologizing that the chashu sold out, or the line of regulars in matching T-shirts. Specific, verifiable details are what make readers trust you.</p>

<h2>Ramen quotes we love</h2>
<p>Ramen has inspired plenty of thoughts worth quoting. Some favorites:</p>
<blockquote>"Peace will come to the world when the people have enough to eat." <cite>— attributed to Momofuku Ando, inventor of instant ramen</cite></blockquote>
<blockquote>"A bowl of ramen is a whole universe in a bowl." <cite>— a common saying among ramen lovers</cite></blockquote>
<p>Ando created instant noodles in Japan in 1958, and the Cup Noodles Museum in Yokohama tells his story. Japanese film has its own ramen classic: Juzo Itami's 1985 comedy <em>Tampopo</em>, a "ramen western" full of memorable lines about how to properly appreciate a bowl.</p>

<h2>Writing it up</h2>
<ol>
  <li><strong>Lead with a scene,</strong> not a summary.</li>
  <li><strong>Pick three or four standout bowls</strong> instead of listing every vendor.</li>
  <li><strong>Fact-check names, prices and quotes</strong> before you publish.</li>
  <li><strong>End with something the reader can do:</strong> where to find the shop year-round, or when the festival returns.</li>
</ol>
<p>Looking for noodles right now? Read about <a href="/mamablog/2018/4/17/little-tong-noodle-shop">Little Tong Noodle Shop</a>, the East Village spot that brought Yunnan mixian to New York.</p>
""",
    },
    {
        "path": "/mamablog/2018/4/24/subway-photos-trial-no1",
        "title": "Subway Photos, Trial No. 1: Learning from Walker Evans",
        "h1": "Subway Photos, Trial No. 1",
        "description": "A first attempt at New York subway portraits, inspired by Walker Evans' hidden-camera subway photography from 1938 to 1941. Notes on candid street photography and ethics.",
        "keyword": "walker evans subway photography",
        "category": "Photography",
        "tags": ["new+york", "human.nyc"],
        "dek": "The subway car is the most democratic portrait studio in the world. Walker Evans knew it eighty years ago.",
        "read": 5,
        "body": """
<p>Between <strong>1938 and 1941</strong>, photographer <strong>Walker Evans</strong> rode the New York City subway with a 35mm camera hidden in his coat, the lens peeking out between buttons and a shutter release running down his sleeve. Sitting across from riders who had no idea they were being photographed, he made hundreds of candid portraits of New Yorkers lost in thought, tired, bored and unguarded.</p>
<p>Evans waited decades to publish them. The work finally appeared in 1966 as the book <em>Many Are Called</em>, with an introduction by James Agee, and it's now considered one of the landmark bodies of American street photography.</p>

<h2>Why subway portraits work</h2>
<ul>
  <li><strong>Everyone is there.</strong> Every age, class and background shares the same bench.</li>
  <li><strong>Stillness.</strong> Riders sit for minutes at a time, which makes it ideal for portraits.</li>
  <li><strong>The unposed face.</strong> In transit, people drop the expression they wear for the world.</li>
</ul>

<h2>Trial no. 1: lessons from a first attempt</h2>
<ol>
  <li><strong>Light is the enemy and the friend.</strong> Subway light is flat and green-tinted, so shoot raw and fix the white balance later.</li>
  <li><strong>Use a fast prime lens</strong> and a high ISO. Grain suits this kind of picture.</li>
  <li><strong>Sit, don't stand.</strong> Evans shot at eye level from a seated position, and it changes everything.</li>
  <li><strong>Be patient.</strong> The best frame usually comes after the train pulls out and everyone settles.</li>
</ol>

<h2>The ethics question</h2>
<p>Evans' hidden camera raises questions that matter even more today. Photographing people in public is generally legal in the US. But doing it ethically means not exploiting people at vulnerable moments, deleting images when someone asks, and thinking hard before publishing photos of identifiable strangers. Many modern subway photographers shoot openly and talk with their subjects afterward.</p>

<h2>Keep going</h2>
<p>A first trial is just that: a start. Go back to the same line, at the same hour, until the car feels like a studio. See more of our photo essays in the <a href="/mamablog/category/Photography">Photography</a> archive.</p>
""",
    },
    {
        "path": "/mamablog/2018/4/17/little-tong-noodle-shop",
        "title": "Little Tong Noodle Shop: Yunnan Mixian Comes to New York",
        "h1": "Little Tong Noodle Shop",
        "description": "Little Tong Noodle Shop introduced many New Yorkers to Yunnan-style mixian rice noodles. The story of chef Simone Tong's East Village restaurant and what made it special.",
        "keyword": "little tong noodle shop",
        "category": "Food",
        "tags": ["new+york"],
        "dek": "Slippery rice noodles, Grandma Chicken broth and a chef who put Yunnan on New York's noodle map.",
        "read": 5,
        "body": """
<p>When <strong>Little Tong Noodle Shop</strong> opened in the East Village in <strong>March 2017</strong>, at First Avenue and 11th Street, it introduced many New Yorkers to a noodle they had never tried: <strong>mixian</strong>, the round rice noodles of China's Yunnan province. Chef-owner <strong>Simone Tong</strong> built the menu around them, and the small restaurant quickly became one of the neighborhood's most talked-about noodle spots.</p>

<h2>What is mixian?</h2>
<p>Mixian are rice noodles, slippery and springy, served in Yunnan in endless variations. Some come in rich broths, some dressed and cold, some loaded with pickles, herbs, chili and fermented flavors. Yunnan sits at a crossroads near Southeast Asia, Tibet and Sichuan, and its food shows it: sour, spicy, funky and fresh at once.</p>

<h2>What people ordered</h2>
<ul>
  <li><strong>Grandma Chicken mixian.</strong> The signature bowl: a deeply savory chicken broth with tender chicken and rice noodles, the dish most diners came back for.</li>
  <li><strong>Spicy and tingly bowls</strong> with chili oil and Sichuan peppercorn for heat seekers.</li>
  <li><strong>Small plates</strong> of pickles, salads and snacks inspired by Yunnan street food.</li>
</ul>

<h2>What happened to Little Tong?</h2>
<p>The East Village location <strong>closed in March 2020</strong>, as the pandemic hit New York's restaurants. A Midtown outpost closed later when office workers stopped coming in. Simone Tong went on to open new projects, including <strong>Silver Apricot</strong> in the West Village. Little Tong's influence lasted: it showed that New York diners were hungry for regional Chinese cooking beyond the familiar takeout menu.</p>

<h2>Where to find mixian now</h2>
<p>Yunnan noodle shops have popped up across New York since then, from Manhattan's Chinatown to Flushing, Queens. Look for menus listing "crossing-the-bridge" noodles (<em>guoqiao mixian</em>), Yunnan's most famous dish. It's served as a scalding broth with raw ingredients and noodles on the side, which you add and cook at the table.</p>
<p>More noodles: our notes from a <a href="/mamablog/2018/9/11/journalistic-inquiry-notes-quotes-and-details">New York ramen festival</a>.</p>
""",
    },
    {
        "path": "/mamablog/2018/2/17/mountain-province",
        "title": "Mountain Province: Filipino Coffee and a Lola's Kitchen in Williamsburg",
        "h1": "Mountain Province",
        "description": "Mountain Province Espresso Bar in East Williamsburg served single-origin coffee from the Philippine highlands, plus Filipino baked goods. A Brooklyn café story.",
        "keyword": "mountain province coffee",
        "category": "Food",
        "tags": ["new+york"],
        "dek": "Coffee from the highlands of the Philippines, pineapple scones and a café built as a love letter to a grandmother.",
        "read": 4,
        "body": """
<p><strong>Mountain Province Espresso Bar</strong> in East Williamsburg, Brooklyn, built its identity on a region most New York coffee drinkers had never heard of. Its beans came from the <strong>mountain regions of the Philippines</strong>, including the highlands of the Cordillera, where the province that gave the café its name is found. The space was designed as an homage to the owner's <em>lola</em>, the Filipino word for grandmother.</p>

<h2>Filipino coffee, explained</h2>
<p>The Philippines is one of the few countries that grows all four major commercial coffee species: <strong>Arabica, Robusta, Liberica</strong> (locally known as <em>barako</em>) and <strong>Excelsa</strong>. Highland Arabica from the Cordillera, including Benguet and Mountain Province, has drawn growing attention from specialty roasters for its sweetness and body. Farms there are often small and family-run.</p>

<h2>What made the café special</h2>
<ul>
  <li><strong>Sourcing with a story:</strong> fair-trade, single-origin beans tied to a specific place and its farmers.</li>
  <li><strong>Filipino baking:</strong> regulars praised the pineapple scones, coconut muffins and picadillo buns.</li>
  <li><strong>A homey room:</strong> a neighborhood café that felt like someone's grandmother's kitchen, and a favorite place to work.</li>
</ul>

<h2>The legacy</h2>
<p>Mountain Province has since closed, but it was part of a wave of Filipino-American cafés and bakeries in New York that put ube, calamansi, pandesal and Philippine-grown coffee on the city's radar. If you love Filipino flavors, look for those ingredients on menus around Queens' Woodside ("Little Manila") and in Brooklyn and Manhattan cafés.</p>
<p>Want a coffee institution that's still roasting after more than a century? Read about <a href="/mamablog/2018/10/20/porto-rico-importing-co">Porto Rico Importing Co.</a></p>
""",
    },
    {
        "path": "/mamablog/2018/1/20/katz-deli-some-delicious-pastrami",
        "title": "Katz's Deli: Some Delicious Pastrami (and Why It Costs What It Does)",
        "h1": "Katz's Deli: Some Delicious Pastrami",
        "description": "A guide to Katz's Delicatessen on the Lower East Side: how the ticket system works, what to order, why the pastrami is so expensive and whether cats can eat pastrami.",
        "keyword": "katz deli pastrami",
        "category": "Food",
        "tags": ["new+york"],
        "dek": "Hand-carved pastrami piled impossibly high, a paper ticket you must not lose and more than a century of Lower East Side history.",
        "read": 6,
        "body": """
<p><strong>Katz's Delicatessen</strong> has stood on the corner of East Houston and Ludlow Streets since <strong>1888</strong>. It's one of the last great Jewish delis of the Lower East Side, and its pastrami on rye is about as close as New York gets to a sacred food. It's also famous from the movies: the "I'll have what she's having" scene in <em>When Harry Met Sally</em> (1989) was filmed here, and a sign hangs over the table.</p>

<h2>How the ticket system works</h2>
<ol>
  <li><strong>Take a ticket</strong> at the door. Every person gets one.</li>
  <li><strong>Choose:</strong> order at the counter yourself, or sit in the waiter-service section along the wall.</li>
  <li><strong>At the counter,</strong> a cutter hand-carves your meat and usually hands you a taste. Tipping your cutter is customary.</li>
  <li><strong>Each counter marks your ticket</strong> with what you ordered.</li>
  <li><strong>Pay on the way out.</strong> Don't lose the ticket: there's a fee if you do.</li>
</ol>

<h2>What to order</h2>
<ul>
  <li><strong>Pastrami on rye</strong> with mustard. No mayo, no lettuce, no arguments.</li>
  <li><strong>Corned beef</strong>, or get a combo if you can't decide.</li>
  <li><strong>Matzo ball soup</strong> and a <strong>knish</strong> to round things out.</li>
  <li><strong>Pickles</strong>, both full and half sours, which come with the meal.</li>
  <li>A <strong>Dr. Brown's</strong> soda (Cel-Ray, if you're brave) or an egg cream.</li>
</ul>

<h2>Why is Katz's so expensive?</h2>
<p>A pastrami sandwich at Katz's costs more than most sandwiches in New York, and people ask why. The short answer is labor, time and quantity:</p>
<ul>
  <li><strong>The cure takes weeks.</strong> The brisket is cured, then rubbed with spices, smoked and steamed. It's a multi-day process.</li>
  <li><strong>It's carved by hand,</strong> to order, by skilled cutters, not run through a slicer.</li>
  <li><strong>The portion is enormous.</strong> One sandwich is easily enough for two people, and splitting is common.</li>
  <li><strong>Prime Manhattan real estate</strong> and a huge, busy operation open long hours.</li>
</ul>

<h2>Can cats have pastrami?</h2>
<p>Since people really do search it: <strong>no, you shouldn't feed your cat pastrami.</strong> It's very high in salt, and its spice rub often contains garlic and onion, which are toxic to cats. A tiny accidental nibble is unlikely to be an emergency. Call your vet if your cat eats more than that or seems unwell. Save the pastrami for yourself.</p>

<h2>Tips for visiting</h2>
<ul>
  <li><strong>Go off-peak:</strong> weekday mid-afternoon is calmest. Weekend lunch is a scrum.</li>
  <li><strong>Split a sandwich</strong> and add sides.</li>
  <li><strong>Make a Lower East Side day of it</strong> with <a href="/mamablog/2020/6/13/4-photos-from-economy-candy">Economy Candy</a> and a <a href="/mamablog/2018/10/30/its-more-than-just-a-slice-to-end-the-night">late-night slice</a>.</li>
</ul>
""",
        "faq": [
            ("Why is Katz's Deli so expensive?", "Katz's pastrami is cured for weeks, spice-rubbed, smoked and steamed, then hand-carved to order. The sandwiches are huge, often enough for two people, and the deli runs a large operation in prime Manhattan real estate."),
            ("Can cats have pastrami?", "No. Pastrami is very high in sodium and its spice rub often includes garlic and onion, which are toxic to cats. Call a vet if your cat eats a meaningful amount."),
            ("How does the Katz's ticket system work?", "Everyone takes a ticket at the door. Counter staff mark it with what you order, and you pay on the way out. Losing the ticket incurs a fee."),
        ],
    },
]
