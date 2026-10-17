"""Blog posts for hatetolovethesplit.com.

Each post keeps the exact URL (date + slug) the original site used, so every
page that ranked or earned links answers at the same address. Posts marked
`new` cover tag pages that ranked but whose original post we never saw.

Body shorthand handled by build.py:
  [[fig name | alt text | caption]]   -> <figure> with /assets/img/name.webp
  [[tip Title | text]]                -> highlighted call-out box
"""

POSTS = [
# ---------------------------------------------------------------- 2014
{
"date": "2014-01-19", "slug": "crafty-great-grandmas-recipe",
"title": "Crafty: Framing Great Grandma's Recipe",
"seo_title": "Great Grandma Frame: How to Frame a Family Recipe Card",
"description": "A great grandma frame project: how we turned a stained, handwritten family recipe card into wall art for the kitchen in one afternoon.",
"category": "crafty", "tags": ["great-grandma-frame", "picture-frames", "kitchen-art", "diy"],
"image": "frames-brick", "image_alt": "Empty vintage picture frames leaning against a brick wall",
"body": """
<p class="lead">Somewhere in a recipe box that smells like cinnamon and 1962, my great grandma's handwriting is still telling people to "add flour until it feels right." This weekend that card finally got the respect it deserves: a frame, a mat, and a spot on our kitchen wall.</p>
<p>When you buy a split-level that's been beige since the Carter administration, the walls feel like a blank check. I didn't want generic "Live Laugh Love" art in the kitchen. I wanted something that actually belonged to us, and nothing belongs to us more than Great Grandma's sour cream coffee cake.</p>
<h2>Why a great grandma frame beats store-bought art</h2>
<p>Handwriting is the most personal thing you can hang. The loops, the crossed-out measurements, the grease spot over "bake 45 min" all tell a story. A framed recipe card is cheap, takes about an hour, and starts a conversation every time someone grabs a glass of water.</p>
[[fig gallery-frame | A simple black frame with a white mat leaning on a shelf | A thin black frame and an oversized mat make a 3x5 card look intentional.]]
<h2>What you need</h2>
<ul>
<li>The original card (or a high-resolution scan if the original is too fragile)</li>
<li>A frame at least two sizes larger than the card, we used an 8x10</li>
<li>An acid-free mat cut to the card's size, plus acid-free photo corners</li>
<li>A soft brush and a clean, dry work surface</li>
</ul>
<h2>How we framed it</h2>
<ol>
<li><strong>Scan first, always.</strong> Before anything touches tape, scan the card at 600 dpi. If the worst happens, you can print a copy on cardstock.</li>
<li><strong>Clean gently.</strong> A dry, soft brush removes crumbs (yes, actual crumbs). Don't use water or erasers on old ink.</li>
<li><strong>Use photo corners, not glue.</strong> The corners hold the card to the backing without damaging it, so the recipe can come out of the frame the next time someone actually wants to bake it.</li>
<li><strong>Float it on a big mat.</strong> A small card in a wide mat looks like a museum piece. Tight framing looks like a fridge magnet.</li>
<li><strong>Hang it away from the stove.</strong> Steam and direct sun fade ink fast. Ours lives on the wall opposite the window.</li>
</ol>
[[tip Make it a set | If your family has several recipe cards, frame three or five in matching frames and hang them as a row. Same frame and mat color keeps it from looking cluttered.]]
<p>Total cost: about $22 and an afternoon. Total number of times I've teared up looking at it: we're not counting. The split-level kitchen is still ugly, but now it's ugly with family history. That's progress.</p>
"""},

{
"date": "2014-01-21", "slug": "plumbing-nightmares-warning-nasty-rodent-pictures",
"title": "Plumbing Nightmares (Warning: Nasty Rodent Pictures)",
"seo_title": "Plumbing Nightmares: What We Found Under the Kitchen Sink",
"description": "Plumbing nightmares in a 1970s split-level: a slow drain, a smell, and the rodent nest we found under the kitchen sink. What we fixed and how to prevent it.",
"category": "kitchen", "tags": ["plumbing", "kitchen-sink", "pests", "home-repair"],
"image": "pipes", "image_alt": "A stack of plastic drain pipes",
"body": """
<p class="lead">Every old house has a moment where it tests whether you really love it. Ours arrived two days after we moved in, in the form of a slow kitchen drain and a smell I can only describe as "wet basement plus regret."</p>
<p>We promised nasty rodent pictures in the title, and honestly? We decided you're better off without them. Picture a nest of insulation, shredded paper towel and something that used to be a dish sponge, tucked behind the drain trap. Now un-picture it. You're welcome.</p>
<h2>How the plumbing nightmare started</h2>
<p>The kitchen sink drained, technically, but slowly enough that we'd do dishes in two shifts. We assumed grease. The plunger did nothing. When the Mister pulled the cabinet floor panel to reach the trap, the panel came up in soggy pieces, and that's when we met the nest.</p>
[[fig brass-faucet | Old brass faucet taps over a sink | Not our sink, but this is how we felt about the plumbing: charming from above, terrifying below.]]
<h2>What was actually wrong</h2>
<ul>
<li><strong>A leaky slip-nut</strong> on the P-trap had been dripping for who knows how long, rotting the cabinet floor.</li>
<li><strong>A gap around the drain pipe</strong> where it entered the wall gave mice a highway straight into the warm, damp cabinet.</li>
<li><strong>Old galvanized pipe</strong> inside the wall had narrowed with buildup, which explained the slow drain.</li>
</ul>
<h2>What we did</h2>
<ol>
<li>Cleaned and disinfected everything with gloves and a mask. Rodent droppings are no joke, so don't sweep them dry.</li>
<li>Replaced the P-trap and tailpiece with new PVC and fresh washers.</li>
<li>Had a plumber swap the galvanized section in the wall for PVC. Worth every penny.</li>
<li>Stuffed steel wool around every pipe penetration and sealed it with expanding foam.</li>
<li>Cut a new cabinet floor from 1/2" plywood and painted it with two coats of polyurethane.</li>
</ol>
[[tip Check yours today | Open the cabinet under your sink with a flashlight. Look for water stains, soft spots, droppings, or daylight around pipes. Five minutes now beats a weekend of plumbing nightmares later.]]
<p>The good news: the drain now runs like a river and the cabinet smells like nothing at all. The bad news: we've learned that the house has more surprises. Stay tuned.</p>
"""},

{
"date": "2014-01-24", "slug": "mindfulness",
"title": "Mindfulness (or: I'm Fifty! Days Into Homeownership)",
"seo_title": "Mindfulness for Renovators (and Molly Shannon's I'm Fifty)",
"description": "A little mindfulness for anyone drowning in a house project, plus why Molly Shannon's Sally O'Malley 'I'm fifty!' is our renovation mood.",
"category": "random-thoughts", "tags": ["mindfulness", "molly-shannon", "renovation-life"],
"image": "stones", "image_alt": "Balanced stacked stones by water",
"body": """
<p class="lead">The plumbing is fixed, the kitchen is still ugly, and I have a list of 147 projects on my phone. This week I tried something new: not doing all of them at once.</p>
<p>Mindfulness has become one of those words that's printed on mugs, but the core idea is simple and very useful for anyone living inside a renovation: pay attention to what's in front of you, right now, without immediately judging it.</p>
<h2>The renovation brain spiral</h2>
<p>You know the one. You go to hang a towel bar and notice the drywall is cracked. Then you notice the trim is chipped. Then you're on your phone pricing tile at 11 p.m. and wondering if you should have bought a condo. That spiral is where joy goes to die.</p>
[[fig coffee | A latte on a wooden table next to a laptop | Coffee first. Panic later. Possibly never.]]
<h2>What's actually helping</h2>
<ul>
<li><strong>One project at a time.</strong> It goes on the list, it gets a date, and I'm allowed to stop thinking about it until then.</li>
<li><strong>Five minutes of noticing.</strong> Each morning I sit with coffee and look at one room. Not to fix it, just to notice what I like. (Spoiler: the light in our living room is amazing.)</li>
<li><strong>Celebrate small wins.</strong> We fixed a drain! We hung a frame! Those count.</li>
</ul>
<h2>Our mascot: Sally O'Malley</h2>
<p>If you've never seen Molly Shannon's Sally O'Malley on SNL, go find it. "I'm fifty! I like to kick, stretch, and kick!" She's fifty, she's in red stretch pants, and she is having the time of her life. That's the energy we're bringing to this house. We're not perfect, the house isn't perfect, but we're going to kick, stretch, and kick anyway.</p>
<p>So here's to being present in a half-finished house. Breathe in. Breathe out. Ignore the cracked drywall for one more day.</p>
"""},

{
"date": "2014-02-07", "slug": "akurum-cabinets",
"title": "Our IKEA Akurum Cabinets: Base, Wall and Everything In Between",
"seo_title": "IKEA Akurum Cabinets: Base & Wall Cabinet Install Guide",
"description": "Installing IKEA Akurum cabinets: base cabinets, wall cabinets on the suspension rail, hardware tips, and what changed when Sektion replaced Akurum.",
"category": "kitchen", "tags": ["ikea-cabinets", "ikea-akurum", "kitchen-renovation", "suspension-rail"],
"image": "kitchen-cabinets", "image_alt": "Cream kitchen cabinets with under-cabinet lighting",
"body": """
<p class="lead">We did it. We ordered an IKEA kitchen. A truck showed up with roughly nine hundred flat boxes, and our split-level's upper level now looks like a cardboard fort. Here's everything we learned installing IKEA Akurum cabinets.</p>
<p>Akurum was IKEA's kitchen cabinet system for years. It's sturdy, affordable, and modular: one frame system, then you choose doors, drawers and hardware. (Heads up for anyone reading this later: IKEA replaced Akurum with the Sektion system in 2015, so Akurum parts are now mostly found secondhand. The install principles below still apply to Sektion.)</p>
<h2>Planning: measure three times</h2>
<p>We used IKEA's online kitchen planner, then printed it and taped the layout on the floor with painter's tape. Walking around the "kitchen" in tape caught two mistakes: a dishwasher door that would have hit the island, and a corner base cabinet that blocked a drawer.</p>
[[fig white-kitchen | A bright white kitchen with an island and pendant lights | Our inspiration board was mostly kitchens like this one.]]
<h2>Akurum base cabinets</h2>
<ul>
<li><strong>Find your high point.</strong> Floors in old houses are never level. Find the highest spot along the wall and set every base cabinet to that height with the adjustable legs.</li>
<li><strong>Connect cabinets to each other first</strong>, then to the wall. Clamping and screwing neighbors together keeps face frames flush.</li>
<li><strong>Cut sink cabinet backs before installing.</strong> It's much easier to trace pipe locations with the cabinet out.</li>
</ul>
<h2>Akurum wall cabinets and the suspension rail</h2>
<p>This is the clever part. Akurum wall cabinets hang on a metal suspension rail screwed into the studs. The cabinet hardware hooks over the rail, and two adjustment screws let you fine-tune height and depth after it's hung.</p>
<ol>
<li>Mark a level line for the top of the rail. Measure from the floor, not the countertop.</li>
<li>Screw the suspension rail hardware into every stud you can hit. Wall cabinets full of dishes are heavy.</li>
<li>Hang each cabinet, then adjust until the doors line up perfectly. Then adjust again.</li>
</ol>
[[tip Hardware for an IKEA Akurum wall cabinet | Lost the suspension rail hardware? Sektion's rail and fittings are compatible with most Akurum wall cabinets, so you can buy replacement hardware even though Akurum is discontinued.]]
<h2>Fridge drawers, wine fridge and fillers</h2>
<p>We left a 24" gap for an under-counter wine fridge and used IKEA filler panels around the full-size fridge. If you're thinking about fridge drawers in an IKEA kitchen, plan the panel and toe-kick details early. Appliance specs rarely match IKEA's standard heights.</p>
<h2>Was it worth it?</h2>
<p>Absolutely. Total cabinet cost was a fraction of custom, and the boxes feel solid. The trickiest part wasn't assembly, it was the house: out-of-square corners, wavy walls, and one mystery soffit. But that's a story for another post.</p>
"""},

{
"date": "2014-02-17", "slug": "diy-gallery-wall-shelves-pt-2",
"title": "DIY Gallery Wall Shelves, Pt. 2",
"seo_title": "Gallery Wall Shelves with IKEA Ribba Frames (DIY Pt. 2)",
"description": "Part 2 of our DIY gallery wall shelves: styling picture ledges with IKEA Ribba frames, plus Ribba frame instructions for swapping mats and photos.",
"category": "crafty", "tags": ["ribba-frames", "gallery-wall", "picture-ledges", "ikea"],
"image": "gallery-frame", "image_alt": "Framed art print leaning on a white shelf next to a plant",
"body": """
<p class="lead">In part one we built and hung three long picture ledges in the stairway between our split-level's upper and lower floors. Today: making them look good, with a stack of IKEA Ribba frames and zero new nail holes.</p>
<p>Gallery wall shelves are the commitment-phobe's gallery wall. Instead of hammering 18 holes and praying, you lean frames on narrow shelves and swap them whenever you want. Perfect for a stairway where every hole would be at a weird angle anyway.</p>
<h2>Why Ribba frames work so well</h2>
<ul>
<li>They're deep enough to stand up on their own on a ledge.</li>
<li>They come with mats, which makes even phone photos look intentional.</li>
<li>They're inexpensive, so mixing sizes doesn't break the bank.</li>
</ul>
[[fig bookshelf-wall | Dark wall shelves filled with books, records and objects | Layering frames with books and objects keeps ledges from feeling flat.]]
<h2>Ribba frame instructions (the parts nobody explains)</h2>
<ol>
<li><strong>Open the back:</strong> bend up the small metal tabs on the backing board. Go gently, they snap if you over-bend.</li>
<li><strong>Mat orientation:</strong> the mat's beveled edge faces out. Center your photo on the back of the mat with a strip of tape along the top edge only, so the photo can hang straight.</li>
<li><strong>Glass vs. plastic:</strong> newer Ribba frames ship with plastic glazing. Peel the protective film off both sides or everything looks foggy.</li>
<li><strong>Standing on a ledge:</strong> leave the hanging hardware off so frames sit flush against the wall.</li>
</ol>
<h2>How we styled the shelves</h2>
<ul>
<li>Start with the largest frame off-center on each shelf.</li>
<li>Overlap frames by an inch or two. Layering looks collected, not catalog.</li>
<li>Repeat colors across shelves, black frames on all three, plus one white accent per shelf.</li>
<li>Add one non-frame thing per ledge: a small plant, a book, a ceramic bird.</li>
</ul>
[[tip Mixing frame sizes | A good ratio on a 48" ledge: one large (50x70 cm), two medium (30x40 cm), and one small (13x18 cm). Adjust from there.]]
<p>The best part? When we get sick of the art, we'll swap it in five minutes. This is the first space in the house that feels finished, and it's the stairway. Split-level life, baby.</p>
"""},

{
"date": "2014-03-17", "slug": "carpet-countertop-beer",
"title": "Carpet, Countertops and Beer: Our Basement Bar Kegerator",
"seo_title": "Built-In Kegerator & Countertop Beer Tap: Our Basement Bar",
"description": "How we fit a built-in kegerator under IKEA cabinets with a countertop beer tap in our split-level basement bar, plus front-venting tips and brand notes.",
"category": "basement", "tags": ["kegerator", "built-in-kegerator", "beverage-factory", "ikea-cabinets"],
"image": "beer-taps", "image_alt": "A row of beer taps under a chalkboard beer menu",
"body": """
<p class="lead">The lower level of a split-level is basically designed for one thing: hanging out. Ours had wall-to-wall 1970s carpet and a sad wet bar. Now it has new carpet, a butcher-block countertop, and a kegerator with a beer tap right on the counter.</p>
<h2>Built-in kegerator vs. freestanding</h2>
<p>This is the single most important thing we learned: <strong>a built-in kegerator needs front ventilation.</strong> Most freestanding kegerators vent heat out the back or sides. Shove one under a countertop and it will overheat, run constantly, and die young. If you want an under-cabinet kegerator, buy one rated for built-in use.</p>
<ul>
<li><strong>Built-in (front-venting):</strong> designed to slide under a counter, zero-clearance on the sides.</li>
<li><strong>Freestanding:</strong> needs several inches of airflow around it. Fine at the end of a counter run.</li>
</ul>
[[fig bar-counter | A busy bar counter with taps and pendant lights | Our bar is smaller, but the vibe is the goal.]]
<h2>Choosing a kegerator</h2>
<p>We compared a few brands while shopping. Summit and Marvel both make built-in kegerators that fit standard 24" undercounter openings, and Beverage Factory sells a wide range of units, towers and conversion kits. We cared about three things: front venting, a stainless interior, and whether a full-size half-barrel would fit. Read the specs carefully; "fits a keg" sometimes means a sixtel.</p>
<h2>The countertop beer tap</h2>
<p>Most kegerators come with a tower that mounts on top of the unit. Under a counter, the tower has to go through the countertop instead. That means:</p>
<ol>
<li>Drilling a 3" hole through the countertop directly above the kegerator's tower opening.</li>
<li>Running the beer line up through an insulated column so the beer stays cold all the way to the faucet.</li>
<li>Using a tower cooling fan if the line is long, or your first pour will be all foam.</li>
</ol>
[[tip IKEA cabinets + kegerator | We built the bar from IKEA base cabinets with one 24" bay left open for the kegerator. A matching filler panel above and a continuous toe-kick make it look built-in.]]
<h2>And the carpet?</h2>
<p>Low-pile, stain-resistant, and a warm gray. Basements get cold in Minnesota, and bare floors down here would be miserable in January. Plus: it hides the occasional drip from the tap. Not that we'd know.</p>
"""},

{
"date": "2014-05-18", "slug": "ikea-pax-closet-makeover", "new": True,
"title": "Our IKEA Pax Closet Makeover (and a Hektar Lamp)",
"seo_title": "IKEA Pax Planner Tips: Closet Makeover + Hektar Lamp",
"description": "Using the IKEA Pax planner to design a bedroom wardrobe in an awkward split-level closet, plus why the industrial IKEA Hektar lamp ended up on our dresser.",
"category": "bedroom", "tags": ["ikea-pax", "ikea-hektar", "closet", "bedroom"],
"image": "tools-flatlay", "image_alt": "Hand tools laid out on a wooden table",
"body": """
<p class="lead">Split-levels have many talents. Generous closets are not one of them. Our bedroom closet was a 6-foot cave with a single wire shelf, so we tore it all out and replaced it with an IKEA Pax system.</p>
<h2>Start with the IKEA Pax planner</h2>
<p>The IKEA Pax planner lets you drop frames, doors and interior fittings into your exact dimensions. A few tips after many, many hours in it:</p>
<ul>
<li><strong>Measure ceiling height at the front and back</strong> of the closet. Old houses slope. Pax frames come in two heights, and you need clearance to tip the frame upright.</li>
<li><strong>Plan interiors before doors.</strong> Drawers behind hinged doors need extra clearance, and the planner flags it if you check.</li>
<li><strong>Print the parts list.</strong> The planner groups everything, which makes store pickup much faster.</li>
</ul>
<h2>The build</h2>
<p>We built the two frames on the bedroom floor, tipped them up, anchored them to the wall, and then filled them with drawers, double hanging rods and pull-out trays. Each frame took about an hour once we found our rhythm.</p>
[[fig level | Hands holding a red level on a surface | Level, anchor, repeat. Pax frames must be screwed to the wall.]]
<h2>The Hektar lamp</h2>
<p>While we were at IKEA (twice... three times), we grabbed a Hektar lamp. Hektar is IKEA's industrial-style line, and the oversized pendant and floor lamps look way more expensive than they are. Ours sits on the dresser next to the new wardrobe and makes the whole corner feel like a boutique hotel.</p>
[[tip Finish the gap | Pax frames rarely fill a closet wall perfectly. Cover the gaps with a strip of painted MDF scribed to the wall and nobody will know.]]
<p>Total time: one weekend. Total arguments: two. Total closet space gained: approximately infinity.</p>
"""},

{
"date": "2014-06-22", "slug": "installing-cement-pavers",
"title": "Installing Cement Pavers",
"seo_title": "Installing Cement Pavers: Our DIY Patio, Step by Step",
"description": "How to install cement pavers for a DIY patio: excavation, gravel base, sand, edging and polymeric sand, plus cement vs. rubber pavers.",
"category": "outsideyarddeck", "tags": ["cement-pavers", "patio", "diy-landscaping"],
"image": "patio", "image_alt": "Two Adirondack chairs on a concrete paver patio at sunset",
"body": """
<p class="lead">Our backyard came with a "patio" made of six cracked stepping stones and a lot of hope. This summer we pulled it out and laid a proper cement paver patio, by hand, in about four weekends.</p>
<h2>Cement pavers vs. rubber pavers</h2>
<p>We looked at rubber pavers at Home Depot because they're light and you can lay them on almost anything. They're great for playgrounds and around pools, but for a patio that would hold a grill, a table and a fire pit, we wanted cement pavers: heavier, more traditional looking, and they last decades.</p>
<h2>How to install cement pavers</h2>
<ol>
<li><strong>Plan the size and slope.</strong> Mark the outline with stakes and string, and plan for about 1/4" of slope per foot away from the house so water drains.</li>
<li><strong>Excavate.</strong> We dug down about 7": 4" for gravel, 1" for sand, and the paver's thickness. Rent a sod cutter for the grass. Trust us.</li>
<li><strong>Compact the base.</strong> Spread crushed gravel (Class 5 here in Minnesota) in 2" lifts and run a plate compactor over each lift.</li>
<li><strong>Screed the sand.</strong> Lay two 1" pipes on the base, pour sand between them, and drag a straight 2x4 across the top for a perfectly flat bed.</li>
<li><strong>Lay the pavers.</strong> Start in a corner against the house and work outward. Don't walk on the screeded sand.</li>
<li><strong>Edge it.</strong> Plastic or metal edge restraint spiked into the base keeps everything from creeping.</li>
<li><strong>Polymeric sand.</strong> Sweep it into the joints, compact again, then mist with water to set it. No weeds, no ants.</li>
</ol>
[[fig garden-trowel | A garden trowel in a pile of soil | Most of the work is dirt. The pavers are the fun part at the very end.]]
[[tip Cut pavers safely | Rent a wet saw or use a diamond blade on an angle grinder, outside, with eye, ear and dust protection. Cement dust is no joke.]]
<h2>Was it worth it?</h2>
<p>Every evening since it's been done. We've eaten dinner out there more in the last month than in the whole previous year. Next up: getting the lilacs under control.</p>
"""},

{
"date": "2014-07-07", "slug": "lilac-trimming",
"title": "Lilac Trimming: Taming Our Overgrown Lilacs",
"seo_title": "Trimming Lilacs: When & How to Prune an Overgrown Lilac",
"description": "Trimming lilacs the right way: prune right after bloom, how to cut back an overgrown lilac bush or lilac tree, and rejuvenating it over three years.",
"category": "outsideyarddeck", "tags": ["lilacs", "pruning", "gardening"],
"image": "lilac", "image_alt": "Close-up of purple lilac blossoms",
"body": """
<p class="lead">Our lilacs were planted by the original owners sometime around the moon landing. They're 14 feet tall, mostly bare at the bottom, and the flowers are all up where only birds can smell them. Time for some lilac trimming.</p>
<h2>When to trim lilacs</h2>
<p><strong>Right after they finish blooming.</strong> Lilacs set next year's flower buds on this summer's growth. If you prune in fall or early spring, you cut off next year's flowers. In Minnesota that means trimming lilacs in late May through June. We cut it close this year, but early July still works if you're quick.</p>
<h2>Three kinds of lilac trimming</h2>
<ul>
<li><strong>Deadheading:</strong> snip spent flower clusters just above the next set of leaves. Optional, but it keeps the shrub looking tidy.</li>
<li><strong>Maintenance pruning:</strong> remove dead, crossing or rubbing branches, and suckers coming up from the base.</li>
<li><strong>Rejuvenation pruning:</strong> for overgrown lilacs like ours. Remove about one-third of the oldest, thickest stems at ground level each year for three years.</li>
</ul>
[[fig lilac-branch | White and pale purple lilacs on a branch | Flowers form on this year's growth, so prune right after bloom.]]
<h2>How we cut back our overgrown lilac</h2>
<ol>
<li>Picked the oldest canes, the gray, thick ones with few leaves at the bottom.</li>
<li>Cut them flush at the ground with a pruning saw. Loppers couldn't handle the 3" stems.</li>
<li>Left the younger, more vigorous stems to carry flowers next spring.</li>
<li>Thinned suckers, keeping a few healthy ones to become future main stems.</li>
</ol>
[[tip Lilac tree trimming | Tree-form lilacs (like Japanese tree lilac) are different: keep a single trunk, remove suckers, and only lightly shape the canopy right after flowering.]]
<p>It looks a little sparse now, but in two years we should have a full, flowering lilac at nose height again. Patience is a gardening tool too.</p>
"""},

{
"date": "2014-08-10", "slug": "minnesota-ironman-bike-ride", "new": True,
"title": "Training for the Minnesota Ironman Bike Ride",
"seo_title": "Minnesota Ironman Bike Ride: Training on the Hiawatha Trail",
"description": "Training for the Minnesota Ironman bike ride: Hiawatha bike trail rides, spin class at Lakeville Lifetime Fitness and Stinger energy gel for fuel.",
"category": "random-thoughts", "tags": ["minnesota-ironman-bike-ride", "hiawatha-bike-trail", "stinger-energy-gel", "lifetime-fitness"],
"image": "cycling-road", "image_alt": "A cyclist riding down a road through rolling hills",
"body": """
<p class="lead">Not everything is about the house. (The house disagrees.) This year I signed up for the Minnesota Ironman bike ride, one of the oldest and largest one-day rides in the state, and I've been training whenever I'm not holding a paintbrush.</p>
<h2>What is the Minnesota Ironman bike ride?</h2>
<p>Despite the name, it's not a triathlon. The Minnesota Ironman is a recreational ride held each spring south of the Twin Cities, with route options from a short loop up to a full 100 miles. It's famous for unpredictable April weather. Some years it's sunny. Some years it snows. Everyone gets a story.</p>
<h2>Training on the Hiawatha bike trail</h2>
<p>Most of my weeknight miles happen on Minneapolis's Hiawatha trail, which runs along the light rail line toward Minnehaha Park. It's flat, paved and well lit, which makes it perfect for after-work intervals. On weekends I connect it to the river roads for longer rides.</p>
<p>(If you're searching for the famous Route of the Hiawatha rail trail with the long tunnels and trestles, that one is out west on the Idaho-Montana border. It's on our bucket list.)</p>
<h2>Spin class at Lifetime Fitness in Lakeville</h2>
<p>When the weather won't cooperate, I head to the Lakeville Lifetime Fitness for spin class. Forty-five minutes of hills with loud music is the closest thing to a Minnesota spring ride you can get indoors.</p>
<h2>Fuel: Stinger energy gel</h2>
<p>On anything longer than two hours, I bring Honey Stinger energy gel. It's honey-based, it doesn't taste like chemical candy, and it's easy on my stomach. One every 45 minutes or so keeps the bonk away.</p>
[[tip First long ride tips | Eat before you're hungry, drink before you're thirsty, and check the forecast twice. Then pack arm warmers anyway.]]
<p>Next spring: 100 miles. Probably. Ask me again after the bathroom is done.</p>
"""},

{
"date": "2014-09-27", "slug": "ceilings-on-the-brain",
"title": "Ceilings on the Brain",
"seo_title": "White Tongue and Groove Ceiling Ideas (Behr Whites Compared)",
"description": "White tongue and groove ceiling ideas and pictures, plus Behr Ceiling White vs. Behr Dolphin Fin for a split-level living room ceiling.",
"category": "living-room", "tags": ["tongue-and-groove", "behr-dolphin-fin", "ceilings", "paint"],
"image": "wood-ceiling", "image_alt": "A wooden tongue and groove ceiling",
"body": """
<p class="lead">Our living room ceiling has a texture that can only be described as "cottage cheese that gave up." We can't stop staring at it. And we can't stop staring at pictures of tongue and groove ceilings.</p>
<h2>Why tongue and groove?</h2>
<p>Split-levels have big, vaulted-ish living rooms on the upper level. That ceiling is the largest surface in the room, and right now it's the ugliest. Tongue and groove planks would cover the popcorn texture (after testing it for asbestos, which you must do on pre-1980 ceilings), add architectural detail, and make the room feel like a cabin in the best way.</p>
[[fig cabin-ceiling | Wood ceiling with tall windows looking onto a lake | The dream: warm wood, big views. Our reality: a cul-de-sac. Still.]]
<h2>Natural wood or a white tongue and groove ceiling?</h2>
<ul>
<li><strong>Natural pine</strong> is cozy and forgiving, but in a room with 8-foot side walls it can feel heavy.</li>
<li><strong>A white tongue and groove ceiling</strong> keeps the texture and shadow lines while bouncing light around. This is where we're leaning.</li>
<li><strong>Whitewash</strong> is the in-between: wood grain shows through a thin white stain.</li>
</ul>
<h2>Picking a ceiling white</h2>
<p>We painted sample boards with two Behr colors:</p>
<ul>
<li><strong>Behr Ceiling White:</strong> crisp, flat and bright. It reads a little blue in our north light.</li>
<li><strong>Behr Dolphin Fin:</strong> a soft off-white gray. On the walls it's lovely, and on a plank ceiling it gives just enough contrast with white trim.</li>
</ul>
[[fig paint-roller | A paint roller next to a freshly painted dark wall | Sample big. A 2x2 foot board tells you more than a chip ever will.]]
[[tip Paint before you install | Prime and paint planks before they go up, then do one final coat on the ceiling. You'll never see raw wood in the grooves when boards shrink in winter.]]
<p>Decision pending. Probably Dolphin Fin. Ask us again after we've stared at the ceiling for another month.</p>
"""},

{
"date": "2014-10-12", "slug": "front-stoop-refresh", "new": True,
"title": "Front Stoop Refresh: Paint, Planters and a Menards Wireless Doorbell",
"seo_title": "Front Stoop Refresh with a Menards Wireless Doorbell",
"description": "A one-weekend split-level front stoop refresh: painted door, house numbers, planters and installing a Menards wireless doorbell.",
"category": "outsideyarddeck", "tags": ["curb-appeal", "wireless-doorbell", "front-door"],
"image": "front-door", "image_alt": "A white front door with a wooden arched frame and a flower planter",
"body": """
<p class="lead">Split-levels have a signature look: the front door floats between two floors, halfway up a few concrete steps. Ours also had a doorbell that hadn't rung since roughly 1994. This weekend the stoop got a glow-up.</p>
<h2>The punch list</h2>
<ul>
<li>Paint the door (exterior enamel, two coats, one very nervous afternoon)</li>
<li>New modern house numbers mounted vertically next to the door</li>
<li>Two big planters with mums for fall</li>
<li>Replace the dead doorbell</li>
</ul>
<h2>Why a wireless doorbell</h2>
<p>The old wired doorbell had a broken transformer buried somewhere in a wall we'd rather not open. A wireless doorbell from Menards was the fix: a battery-powered button outside and a plug-in chime inside. Install time was about ten minutes.</p>
<ol>
<li>Remove the old button and cap the old wires with wire nuts.</li>
<li>Mount the new button with the included screws (or the adhesive strip on siding).</li>
<li>Plug the chime into an outlet on the middle level so it's heard upstairs and down.</li>
<li>Pair them and pick a chime that isn't "Westminster quarters." Please.</li>
</ol>
[[tip Split-level chime placement | Sound doesn't travel well between levels. Many wireless doorbells let you pair a second chime, so put one upstairs and one in the lower-level family room.]]
<p>It's amazing how much a painted door and a working doorbell change the way you feel walking up to your own house. Curb appeal: 1. Beige: 0.</p>
"""},

{
"date": "2014-11-16", "slug": "wallpaper-removal-and-gardz", "new": True,
"title": "Main Bathroom Demo: Wallpaper Removal and Zinsser Gardz",
"seo_title": "Wallpaper Removal & Zinsser Gardz: Fixing Torn Drywall",
"description": "Removing three layers of bathroom wallpaper, and how Zinsser Gardz from Home Depot sealed our torn drywall paper before skim coating.",
"category": "main-bathroom", "tags": ["zinsser-gardz", "wallpaper-removal", "bathroom-renovation"],
"image": "gutted-room", "image_alt": "A room mid-demolition with stripped walls and debris on the floor",
"body": """
<p class="lead">The main bathroom renovation is officially underway. Step one: remove the wallpaper. All three layers of it. The bottom layer was gold foil. We have questions for the previous owners.</p>
<h2>How we removed the wallpaper</h2>
<ol>
<li>Scored the surface lightly with a scoring tool so water could get behind the vinyl top layer.</li>
<li>Sprayed with hot water plus a splash of fabric softener and let it soak ten minutes.</li>
<li>Scraped with a wide plastic putty knife, then a steamer for the stubborn parts.</li>
</ol>
<p>It mostly worked. Mostly. In a few spots the paper came off along with the brown paper face of the drywall underneath. Torn drywall paper is a problem: if you skim coat or paint right over it, the moisture makes the paper bubble.</p>
<h2>Enter Zinsser Gardz</h2>
<p>Zinsser Gardz is a clear problem-surface sealer that soaks into torn drywall paper and wallpaper glue residue and hardens it into a paintable surface. We grabbed a gallon at Home Depot and rolled it on like water. It dries quickly, and the next day we skimmed joint compound right over it with no bubbles.</p>
[[fig paint-brushes | Worn paint brushes on a grid | Gardz goes on thin and watery. Use a roller with a short nap and protect the floor.]]
[[tip Glue residue check | Wipe a spot with warm water. If it feels slimy, wallpaper paste is still there. Wash it off or seal it with Gardz before painting, or the paint will crack.]]
<p>Next up: tile, a new vanity, and figuring out where that mysterious draft is coming from. The main bathroom is ugly-ugly now, which means it's about to get pretty.</p>
"""},

# ---------------------------------------------------------------- 2015
{
"date": "2015-02-22", "slug": "main-bathroom-reveal", "new": True,
"title": "Main Bathroom Reveal: Faux Wood Tiles, Mocha Grout and a Delta Faucet",
"seo_title": "Bathroom Reveal: Faux Wood Tile, Mocha Grout, Delta Faucet",
"description": "Our main bathroom reveal: faux wood tile floors with mocha grout, an oil rubbed bronze Delta faucet, and how to remove a Weslock door knob.",
"category": "main-bathroom", "tags": ["faux-wood-tiles", "mocha-grout", "delta-faucet", "door-hardware"],
"image": "bathroom-sink", "image_alt": "A dark tiled bathroom with a modern faucet and round sink",
"body": """
<p class="lead">Three months, one wallpaper battle, and approximately four hundred trips to the hardware store later, the main bathroom is done. Let's talk about the choices that made it.</p>
<h2>Faux wood tiles on the floor</h2>
<p>We love wood floors. We do not love wood floors in a bathroom. Porcelain faux wood tiles gave us the look of planks with none of the warping. A few tips:</p>
<ul>
<li>Use a 1/3 offset, not 1/2, on long plank tiles to avoid lippage from slight bowing.</li>
<li>Mix tiles from several boxes so the printed grain patterns don't repeat side by side.</li>
<li>Use tight grout joints (1/16" to 1/8") so it reads as wood, not tile.</li>
</ul>
[[fig tile-wall | Muted green and gray wall tiles | We tested a dozen tile and grout combos on scrap board before committing.]]
<h2>Why mocha grout</h2>
<p>White grout on a wood-look floor screams "tile!" and turns gray in a month. Mocha grout blends into the plank tones and hides dirt. Sanded grout for the floor, unsanded for the wall tile, and a penetrating sealer on both after 72 hours.</p>
<h2>The Delta faucet</h2>
<p>We picked a Delta faucet in oil rubbed bronze to warm up all the gray. Two things we liked: Delta's cartridge design makes repairs easy, and their lifetime warranty is real (we've already used it on a kitchen faucet). If you want a matching drinking water faucet in the kitchen, Delta makes those in the same finish too.</p>
[[fig clawfoot-bath | A vintage bathroom with a clawfoot tub and patterned floor | Inspiration for the someday-tub. This round, we kept the original tub and reglazed it.]]
<h2>Door hardware: removing a Weslock door knob</h2>
<p>The old brass Weslock knob had to go, and it didn't come off the way most knobs do. Here's the trick for Weslock door knob removal:</p>
<ol>
<li>Look for a tiny slot on the neck of the interior knob.</li>
<li>Push a small flat screwdriver or the tip of a paper clip into the slot to depress the spring catch.</li>
<li>Pull the knob off while holding the catch down. The rose (trim plate) then pops off to reveal the screws.</li>
<li>Remove the screws and slide out both halves and the latch.</li>
</ol>
<p>We replaced it with a simple oil-rubbed bronze lever to match the faucet. Small details, big difference.</p>
<p>The verdict: from our most hated room to one of our favorites. That's the whole point of this blog.</p>
"""},

{
"date": "2015-04-19", "slug": "a-weekend-in-nyc", "new": True,
"title": "A Weekend in NYC: Fig & Olive and Mung Bean Griddle Cakes",
"seo_title": "A Weekend in NYC: Fig & Olive and Mung Bean Griddle Cakes",
"description": "A weekend away from the house: brunch at Fig & Olive in NYC, Korean mung bean griddle cakes in Koreatown, and design ideas we brought home.",
"category": "random-thoughts", "tags": ["travel", "fig-and-olive", "mung-bean-griddle-cake", "food"],
"image": "restaurant-plate", "image_alt": "A plated dish on a busy restaurant table with wine glasses",
"body": """
<p class="lead">When the bathroom was finished, we gave ourselves a reward: three days in New York City, no paint, no tools, no Home Depot. We ate. A lot.</p>
<h2>Fig &amp; Olive</h2>
<p>Our first brunch was at Fig &amp; Olive, the Mediterranean spot known for olive oil tastings and crostini. The room is all white, warm wood and greenery, and we spent half of brunch taking notes on the light fixtures. Is it possible to eat avocado toast and plan a kitchen at the same time? Yes.</p>
<h2>Mung bean griddle cakes in Koreatown</h2>
<p>Our favorite bite of the trip was in Koreatown: bindaetteok, a crispy Korean mung bean griddle cake (also called a mung bean pancake). Soaked mung beans are ground with kimchi, bean sprouts and pork, then pan-fried until the edges shatter. Dipped in soy-vinegar sauce, it's perfect.</p>
[[tip Try it at home | Soak dried, split mung beans overnight, blend with a little water until thick, fold in chopped kimchi and green onions, and fry in a generous amount of oil. Crispy edges are the whole point.]]
<h2>What we brought home</h2>
<ul>
<li>A plan to use more plants and warm wood in the living room</li>
<li>A strong opinion about brass light fixtures</li>
<li>About four extra pounds</li>
</ul>
<p>Now back to Minneapolis, where the hallway is waiting.</p>
"""},

{
"date": "2015-06-14", "slug": "the-churchill-chair", "new": True,
"title": "The Churchill Chair (and a Little Jimmy Rig)",
"seo_title": "Restoration Hardware Churchill Chair: Our Library Chair",
"description": "We found a secondhand Restoration Hardware Churchill leather chair, fixed a wobbly leg with a little jimmy rig, and learned to care for it.",
"category": "living-room", "tags": ["restoration-hardware-churchill", "jimmy-rig", "furniture", "thrifting"],
"image": "wingback-chairs", "image_alt": "Two vintage wingback chairs against a stone wall",
"body": """
<p class="lead">The living room finally has a reading chair. Not just any chair: a secondhand Restoration Hardware Churchill leather chair we found online for a fraction of what it costs new.</p>
<h2>Why the Churchill?</h2>
<p>The Churchill is Restoration Hardware's take on a classic English library chair: rolled arms, a tight back, nailhead trim and leather that gets better as it gets beat up. It's compact enough for our split-level living room and looks like it has been reading books since 1940.</p>
<h2>The jimmy rig</h2>
<p>The chair had one problem: a back leg that wobbled. The previous owner's fix was a folded-up coaster. Ours was slightly better, but let's be honest, it's a jimmy rig (or jury rig, if you're picky):</p>
<ol>
<li>Flipped the chair and found the leg's corner block had come loose.</li>
<li>Scraped out old glue, re-glued the block with wood glue, and clamped it overnight.</li>
<li>Added two new screws through the block into the frame.</li>
</ol>
<p>No more wobble. The coaster has been retired with honors.</p>
[[tip Leather care | Dust weekly, condition twice a year with a leather conditioner, and keep the chair out of direct sun. Scratches on aniline leather often buff out with a warm finger.]]
<p>Now I just need to read more books. Which, conveniently, is next week's post.</p>
"""},

{
"date": "2015-08-09", "slug": "summer-reading-list", "new": True,
"title": "Summer Reading List: Stephanie Plum and The Fran Lebowitz Reader",
"seo_title": "Stephanie Plum Series & The Fran Lebowitz Reader: Our Picks",
"description": "What we read in the new reading chair: the Stephanie Plum series by Janet Evanovich in order, and why The Fran Lebowitz Reader is a must.",
"category": "random-thoughts", "tags": ["stephanie-plum-series", "the-fran-lebowitz-reader", "books"],
"image": "reading", "image_alt": "A person reading a book outside by the water",
"body": """
<p class="lead">The reading chair needed breaking in, so this summer I read. Two very different books (and one very long series) made the list.</p>
<h2>The Stephanie Plum series</h2>
<p>Janet Evanovich's Stephanie Plum series follows a bounty hunter from Trenton, New Jersey who is terrible at her job and somehow always catches her guy. Cars explode. Grandma Mazur steals every scene. It's pure fun, and the books are fast enough to finish on a weekend.</p>
<ul>
<li><strong>Start at the beginning:</strong> <em>One for the Money</em> introduces everyone, including the two men in Stephanie's life.</li>
<li><strong>Read in order:</strong> the numbered titles (<em>Two for the Dough</em>, <em>Three to Get Deadly</em>...) make it easy.</li>
<li><strong>Don't overthink it:</strong> these are beach books, and that's a compliment.</li>
</ul>
[[fig bookshelf | A wooden bookshelf filled with books | The to-read shelf keeps growing faster than the read shelf.]]
<h2>The Fran Lebowitz Reader</h2>
<p><em>The Fran Lebowitz Reader</em> collects her two essay books, <em>Metropolitan Life</em> and <em>Social Studies</em>. Lebowitz is dry, cranky and very funny about city life, manners and the general nonsense of modern living. It's the perfect book to read in five-minute bursts between coats of paint.</p>
[[tip Our reading rule | One chapter before screens at night. It's the best sleep we've had since we bought the house.]]
<p>What should we read next? Send your recommendations to info@hatetolovethesplit.com.</p>
"""},

{
"date": "2015-10-04", "slug": "vegas-baby", "new": True,
"title": "Vegas, Baby: The TaylorMade Golf Experience and a Zara Haul",
"seo_title": "TaylorMade Golf Experience & Zara Las Vegas: Our Vegas Trip",
"description": "A long weekend in Las Vegas: a club fitting at the TaylorMade Golf Experience, a Zara shopping haul on the Strip and casino design notes.",
"category": "random-thoughts", "tags": ["taylormade-golf-experience", "zara", "travel", "las-vegas"],
"image": "neon-open", "image_alt": "A glowing neon open sign in the dark",
"body": """
<p class="lead">A friend's birthday took us to Las Vegas, and we came home with a better golf swing (him), a suitcase of new clothes (me), and zero dollars of gambling winnings (us).</p>
<h2>The TaylorMade Golf Experience</h2>
<p>The Mister spent an entire morning at the TaylorMade Golf Experience, a fitting and practice facility in Las Vegas with outdoor bays, launch monitors and a short game area. A fitter watched his swing on a monitor, swapped heads and shafts, and showed him exactly why his drives slice. He's now unbearable about ball speed.</p>
[[fig golf-swing | A golfer mid swing on a green fairway | Somewhere between a lesson and therapy.]]
<h2>Zara in Vegas</h2>
<p>Meanwhile I went to Zara on the Strip. If you've only shopped Zara online, the Las Vegas stores are huge, with far more home pieces than we see in Minnesota. I came home with a wool coat (necessary), two sweaters (necessary), and a set of linen napkins (very necessary).</p>
<h2>Design notes from the casinos</h2>
<ul>
<li>Layered lighting is everything. No room in Vegas has just one overhead light.</li>
<li>Bold wallpaper works best in small spaces you pass through, like a powder room.</li>
<li>Brass and dark wood never stopped being a good idea.</li>
</ul>
<p>Back to reality: the hallway. Bring on the doors.</p>
"""},

{
"date": "2015-11-15", "slug": "hallway-part-1-doors-and-hinges", "new": True,
"title": "Hallway Part 1: New Doors and the Ryobi Hinge Template",
"seo_title": "Hanging Doors with a Ryobi Door Hinge Template (Hallway Pt. 1)",
"description": "Hallway part 1: replacing hollow-core doors, cutting hinge mortises with a Ryobi door hinge template, and picking new door hardware.",
"category": "hallway", "tags": ["door-hardware", "ryobi-door-hinge-template", "doors", "hallway"],
"image": "tool-wall", "image_alt": "A workshop wall full of hand tools",
"body": """
<p class="lead">Our upper-level hallway has five doors: three bedrooms, a bathroom and a linen closet. All five were flat, hollow, slightly warped and painted the color of a manila folder. They had to go.</p>
<h2>Slab doors vs. prehung</h2>
<p>Prehung doors come with a new frame and are easier to install in new construction. In an old house, keeping the existing jambs and buying slab doors saved us from tearing out trim and drywall. The catch: slab doors don't come with hinge mortises, so we had to cut them ourselves.</p>
<h2>Using the Ryobi door hinge template</h2>
<p>The Ryobi door hinge template is an adjustable jig that clamps to the edge of a door and guides a router to cut perfect hinge mortises. Here's how we used it:</p>
<ol>
<li>Lay the old door on top of the new slab and transfer the hinge locations.</li>
<li>Set the template for your hinge size (ours are 3-1/2") and corner radius.</li>
<li>Clamp it to the door edge, set the router bit depth to the hinge leaf thickness, and rout.</li>
<li>Repeat on the jamb if needed, then hang the door and check the gap all around.</li>
</ol>
[[fig level | Hands with a red level checking a surface | Check the reveal with a level before you drive the last screw.]]
[[tip Router depth test | Always test the depth on a scrap of wood first. A mortise that's too deep makes the door bind on the hinge side.]]
<h2>New door hardware</h2>
<p>We went with simple matte black levers on all five doors. Levers are easier to use with full hands (laundry baskets!), and black ties into the new picture ledges on the stairs. The old knobs are in a box in the garage, waiting for a craft project.</p>
<p>Next time: board and batten. The hallway is about to get some texture.</p>
"""},

# ---------------------------------------------------------------- 2016
{
"date": "2016-01-03", "slug": "hallway-part-2-board-and-batten",
"title": "Hallway Part 2: Board and Batten",
"seo_title": "Board and Batten Walls: Our DIY Hallway (Part 2)",
"description": "Hallway part 2: how we added board and batten walls to our split-level hallway, from spacing the battens to caulk and paint, in one long weekend.",
"category": "hallway", "tags": ["board-and-batten", "wainscoting", "hallway", "trim"],
"image": "bright-hallway", "image_alt": "A bright hallway with white walls and wood floors",
"body": """
<p class="lead">New doors are in. Now the hallway needed something to make it feel less like a tunnel and more like part of the house. The answer: board and batten.</p>
<h2>Why board and batten walls?</h2>
<p>Board and batten adds texture and shadow lines without the cost or fuss of real wainscoting. In a narrow hallway it also protects the lower wall from scuffs, bags and the vacuum. And it's very beginner friendly: if you can use a miter saw and a nail gun, you can do this.</p>
<h2>Materials</h2>
<ul>
<li>1x4 primed MDF for the vertical battens and the top rail</li>
<li>1x2 for a small cap ledge on top of the rail</li>
<li>Construction adhesive and 2" brad nails</li>
<li>Paintable caulk and wood filler</li>
<li>Semi-gloss paint (we used the same white as our trim)</li>
</ul>
<h2>How we did it</h2>
<ol>
<li><strong>Pick a height.</strong> About 2/3 of the wall height looked best in our hallway, roughly 60".</li>
<li><strong>Install the top rail</strong> level all the way around, nailed into studs.</li>
<li><strong>Space the battens evenly.</strong> We aimed for 16" to 18" between battens and adjusted so each wall ended with a full space.</li>
<li><strong>Glue and nail</strong> each batten, checking plumb with a level.</li>
<li><strong>Caulk every seam</strong> and fill nail holes. This is the step that makes it look built-in.</li>
<li><strong>Paint</strong> the battens and the wall between them the same color for a seamless look.</li>
</ol>
[[tip Outlets and switches | Plan batten spacing so battens don't land on an outlet. If you can't avoid it, add a box extender so the cover plate sits flush on top of the board.]]
<p>The hallway went from our most hated space to our most complimented. Every guest touches the walls. We're choosing to take that as a compliment.</p>
"""},

{
"date": "2016-02-07", "slug": "nordeast-night-out", "new": True,
"title": "A Night Out in Nordeast: The NE Minneapolis Bar Scene",
"seo_title": "NE Minneapolis Bar Scene: Our Nordeast Night Out",
"description": "How we celebrate a finished project: the NE Minneapolis bar scene, a Hammerheart Brewery day trip, Bistro Le Roux and El Jefe Guapo.",
"category": "random-thoughts", "tags": ["ne-minneapolis-bar-scene", "hammerheart-brewery", "el-jefe-guapo", "bistro-le-roux", "minneapolis-eats"],
"image": "bar-crowd", "image_alt": "A crowded neighborhood bar with chalkboard menus",
"body": """
<p class="lead">Every time we finish a big project, we celebrate the same way: dinner and drinks somewhere we didn't have to build. Lately that means Northeast Minneapolis, or as everyone here calls it, Nordeast.</p>
<h2>The NE Minneapolis bar scene</h2>
<p>Nordeast mixes old-school corner bars, polka-friendly dives and some of the best craft breweries in the state, all within a few blocks of each other. A typical night for us: a taproom flight, a dive bar for a game of pool, and late-night tacos.</p>
<ul>
<li><strong>Taprooms first.</strong> Minnesota's taproom law opened the floodgates, and NE has a brewery around nearly every corner.</li>
<li><strong>Dive bars second.</strong> Cheap beer, meat raffles, zero pretension.</li>
<li><strong>Walk or ride.</strong> Parking is easier than it used to be, but the neighborhood is best on foot.</li>
</ul>
<h2>Day trip: Hammerheart Brewery</h2>
<p>For a road trip, we drive north to Hammerheart Brewery in Lino Lakes. It's Viking-themed, smoky and dark, and the beers lean toward bold, smoked and barrel-aged styles. Grab a seat by the fire and you'll forget it's January.</p>
<h2>Meet El Jefe Guapo</h2>
<p>Readers keep asking about "El Jefe Guapo" (pronounced <em>el HEH-feh GWAH-po</em>: "the handsome boss"). He's the neighbor's very large orange cat who supervises every outdoor project from our front stoop. He doesn't help. He just judges. He is very handsome, and he is definitely the boss.</p>
<h2>Dinner at Bistro Le Roux</h2>
<p>For a quieter celebration we booked a cozy dinner at Bistro Le Roux. Candles, a small menu and a long conversation about which room is next. (The basement. It's always the basement.)</p>
[[tip Make it a ritual | Pick one celebration spot per finished project. It turns a punch list into something to look forward to.]]
"""},

{
"date": "2016-03-16", "slug": "say-it-dont-spray-it",
"title": "Say It, Don't Spray It",
"seo_title": "Say It, Don't Spray It: Spray Paint Lessons for DIYers",
"description": "Say it, don't spray it: hard lessons from spray painting light fixtures and hardware, plus when to grab a brush instead of a can for home projects.",
"category": "random-thoughts", "tags": ["spray-paint", "diy-fails", "hardware"],
"image": "paint-roller", "image_alt": "A paint roller next to a half-painted wall",
"body": """
<p class="lead">"Say it, don't spray it!" is what we yelled on the playground when someone talked too close. It's also my new rule for home projects, after a spray paint incident we will now describe in painful detail.</p>
<h2>The incident</h2>
<p>I spray painted the old brass hallway light fixture matte black. In the garage. In March. In Minnesota. It was 38 degrees, the paint went on thick, never really cured, and the first time we turned the light on, the fixture smelled like a burning tire. We repainted it. Outside. In May.</p>
<h2>When spray paint works</h2>
<ul>
<li>Small metal items with lots of detail: cabinet pulls, hinges, lamp bases</li>
<li>When it's 50 to 85 degrees with low humidity</li>
<li>With light coats, at least three, and a primer made for the surface</li>
</ul>
<h2>When to say it instead</h2>
<ul>
<li><strong>Anything that gets hot.</strong> Use high-heat paint, or don't.</li>
<li><strong>Large flat surfaces.</strong> A roller gives a smoother finish with less overspray.</li>
<li><strong>Indoors.</strong> Just don't. The overspray travels farther than you think.</li>
<li><strong>Things people touch a lot.</strong> Door levers and faucets wear through spray paint quickly. Replace them instead.</li>
</ul>
[[tip The cardboard box booth | Cut the top and one side off a big box, set it on a table outside, and spray inside it. Instant spray booth, much less overspray on the patio.]]
<p>Lesson learned. Now, who wants to talk about our new favorite arepa spot?</p>
"""},

{
"date": "2016-05-08", "slug": "hola-arepa-review",
"title": "Hola Arepa Review: From Food Truck to Our Favorite Minneapolis Restaurant",
"seo_title": "Hola Arepa Minneapolis Review: Food Truck to Restaurant",
"description": "Our Hola Arepa review: how the Minneapolis food truck became a restaurant on Nicollet, what to order, and why the arepas are worth the wait.",
"category": "random-thoughts", "tags": ["hola-arepa", "minneapolis-eats", "restaurant-review"],
"image": "street-sandwich", "image_alt": "A stuffed sandwich and juice on an outdoor table",
"body": """
<p class="lead">We first found Hola Arepa the way everyone did: chasing a food truck around downtown Minneapolis on a weekday lunch. Now it's a full restaurant on Nicollet Avenue, and it's our go-to whenever we need a night off from the house.</p>
<h2>From Hola Arepa food truck to restaurant</h2>
<p>The Hola Arepa food truck built a cult following for its arepas: griddled corn cakes split open and stuffed with fillings. The restaurant kept the truck's spirit, bright, loud and friendly, and added a full bar and a bigger menu. If you loved the truck, you'll love the restaurant.</p>
<h2>What to order</h2>
<ul>
<li><strong>Arepas, obviously.</strong> Crispy outside, soft inside, packed with braised meats, beans, cheese and slaw. Get two. Trust us.</li>
<li><strong>Something fried to share.</strong> Plantains or yuca are perfect with a group.</li>
<li><strong>A cocktail.</strong> The bar leans tropical and fresh, which helps in a Minnesota winter.</li>
</ul>
<h2>Tips for visiting</h2>
<ul>
<li>It gets busy on weekends. Go early or be ready to wait with a drink.</li>
<li>The patio is the move in summer.</li>
<li>Bring friends so you can try more of the menu.</li>
</ul>
[[tip Our order | Two arepas each, one side of plantains for the table, and one cocktail we always say we'll share and never do.]]
<p>The verdict: one of the best meals in Minneapolis, and proof that sometimes the best thing you can do for your house is leave it for a few hours.</p>
"""},
]
