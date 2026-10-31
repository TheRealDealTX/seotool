"""Copy and form markup for each tool page. The logic lives in assets/js/tools/<slug>.js."""


def seg(name, options, checked):
    return '<div class="seg">' + "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}> {t}</label>'
        for v, t in options) + "</div>"


def checks(name, options):
    return '<div class="seg">' + "".join(
        f'<label><input type="checkbox" name="{name}" value="{v}"> {t}</label>' for v, t in options) + "</div>"


PLACE_FIELD = ('<div class="field"><label for="place">Trailhead, park or town</label>'
               '<input type="search" id="place" placeholder="e.g. Estes Park, Zion, Mount Rainier">'
               '<div class="hint">Type at least 2 letters and pick from the list.</div></div>')

TOOLS = {}

TOOLS["packing-list"] = dict(
    title="Camping Packing List Generator (Printable Checklist)",
    description="Build a camping, backpacking or day-hike packing checklist for your trip type, season, nights and group size. Check items off, print it, or share it.",
    h1="Camping & Backpacking Packing List Generator",
    intro="Pick your trip and get a checklist that scales with your nights, group size and season — with the Ten Essentials built in. Your ticks are saved on this device, and the link remembers your settings.",
    form=f"""<form id="packform" class="panel no-print" onsubmit="return false">
<h2>Your trip</h2>
<div class="field"><span class="label">Trip type</span>{seg("trip", [("car", "Car camping"), ("backpack", "Backpacking"), ("day", "Day hike")], "car")}</div>
<div class="field"><span class="label">Season</span>{seg("season", [("warm", "Summer / warm"), ("shoulder", "Spring & fall"), ("cold", "Winter / cold")], "warm")}</div>
<div class="row"><div class="field" id="nights-row"><label for="nights">Nights</label><input type="number" id="nights" min="0" max="30" value="2"></div>
<div class="field"><label for="people">People</label><input type="number" id="people" min="1" max="20" value="2"></div></div>
<div class="field"><span class="label">Extras</span>{checks("extra", [("bear", "Bear country"), ("kids", "Kids"), ("dog", "Dog"), ("rain", "Rain likely"), ("desert", "Desert / hot"), ("photo", "Photography"), ("fish", "Fishing")])}</div>
<div class="btns"><button type="button" class="btn primary sm" id="print">Print checklist</button><button type="button" class="btn outline sm" id="share">Share link</button><button type="button" class="btn outline sm" id="reset">Uncheck all</button></div>
</form>""",
    explain="""<h2 id="how-it-works">How the list is built</h2>
<p>Every list starts from the <strong>Ten Essentials</strong> — navigation, headlamp, sun protection, first aid, knife, fire, shelter, extra food, extra water and extra clothes — then adds what your trip type actually needs. Car campers get the cooler, chairs and a two-burner stove; backpackers get the lightest version of each system plus water treatment and food storage; day hikers get a compact kit with an emergency bivy.</p>
<p>Quantities scale with your inputs: food is planned at roughly 1.5–2 lb per person per day for backpacking, socks and underwear cap at four pairs (wash and rotate on longer trips), and stove fuel scales with group size. Season changes the clothing and sleep system — cold trips add a second pad, insulated layers, traction and hand warmers; hot trips add sun protection, shade and a tent fan.</p>
<h2 id="before-you-go">Before you go</h2>
<ul><li>Check fire restrictions and campground rules — many parks ban fires in dry months.</li>
<li>Check the forecast with the <a href="/tools/trail-weather/">trail weather tool</a> and adjust layers.</li>
<li>Leave your trip plan (route, campsites, return time) with someone at home.</li>
<li>New to this? Read <a href="/blogs/the-outdoor-traveler/camping-101-a-guide-for-the-first-time-camper/">Camping 101</a> and the <a href="/car-camping-essentials/">car camping essentials</a> guide.</li></ul>""",
    faq=[("What are the Ten Essentials for hiking?", "Navigation (map, compass, phone), a headlamp, sun protection, first aid, a knife or multi-tool, fire starter, emergency shelter, and extra food, water and clothing. They are built into every list this tool makes."),
         ("How much food should I pack per day for backpacking?", "Plan on about 1.5 to 2 pounds of food per person per day, or roughly 2,500 to 3,500 calories depending on effort. The camp meal planner can size it for your group."),
         ("Is my checklist saved?", "Yes. Ticks are saved in your browser on this device, and the page link stores your trip settings so you can bookmark or share it.")],
)

TOOLS["trail-weather"] = dict(
    title="Trail Weather Forecast & Hike Score for Any Trailhead",
    description="Free 7-day hiking forecast for any trailhead or park with a daily hike score and warnings for thunderstorms, heat, wind, snow and freezing nights.",
    h1="Trail Weather Forecast & Hike Score",
    intro="Search any trailhead, park or mountain town for a 7-day forecast scored for hiking. Each day gets a 0–100 hike score, and the warnings call out thunderstorms, dangerous heat, strong gusts, snow and freezing overnight lows.",
    form=f"""<div class="panel no-print">
<h2>Where are you hiking?</h2>
{PLACE_FIELD}
<div class="btns"><button type="button" class="btn outline sm" id="locate">Use my location</button></div>
<p class="status" id="status"></p>
<div class="field"><span class="label">Popular parks</span><div class="chips">{{QUICK_PLACES}}</div></div>
</div>""",
    result_title='<h2 style="margin-top:0">Forecast: <span id="place-name">pick a place</span></h2>',
    explain="""<h2 id="hike-score">How the hike score works</h2>
<p>The score starts at 100 and subtracts for the conditions that make hiking less pleasant or less safe: highs below 50°F or a feels-like temperature above 78°F, chance and amount of precipitation, gusts above 25 mph, thunderstorms (a big deduction — lightning is the main summer hazard in the mountains) and snow. <strong>80+ is great, 65–79 good, 50–64 fair, under 50 poor.</strong></p>
<p>It's a quick comparison between days, not a safety guarantee. Mountain weather changes fast, and the forecast is for the point you picked — conditions on a summit 3,000 ft higher can be very different. Use the freezing-level line to judge whether high terrain will have snow and ice, and check the <a href="https://www.weather.gov/">National Weather Service</a> forecast and any park alerts before you go.</p>
<h2 id="mountain-weather">Reading a mountain forecast</h2>
<ul><li><strong>Afternoon thunderstorms:</strong> in summer, plan to be off summits and exposed ridges by early afternoon when storms are in the forecast.</li>
<li><strong>Elevation:</strong> temperatures typically drop 3–5°F for every 1,000 ft you climb, and wind increases on ridgelines.</li>
<li><strong>Heat:</strong> above about 88°F feels-like, start at dawn and carry more water — see the <a href="/tools/water-calculator/">water calculator</a>.</li>
<li><strong>Cold nights:</strong> a freezing low changes your sleep system; size it with the <a href="/tools/sleeping-bag-temperature/">sleeping bag guide</a>.</li></ul>
<p>Planning further ahead? Our <a href="/destinations/">destination guides</a> show 10-year monthly averages for popular parks, and the <a href="/weather/">where-to-go-by-month</a> guide ranks them for every month.</p>""",
    faq=[("Where does the forecast come from?", "Forecasts come from Open-Meteo, which blends national weather models such as NOAA's GFS and HRRR. Always cross-check with the National Weather Service for your area before a big day."),
         ("What is a good hike score?", "80 or higher is a great hiking day, 65 to 79 is good, 50 to 64 is fair, and below 50 means poor or risky conditions such as storms, extreme heat or strong winds."),
         ("What does freezing level mean?", "It's the elevation where the air temperature hits 32°F. Above it, precipitation falls as snow and wet rock can ice up, so trails above the freezing level need winter gear and judgment.")],
)

TOOLS["hiking-time-calculator"] = dict(
    title="Hiking Time Calculator: How Long Will My Hike Take?",
    description="Estimate how long a hike will take from distance, elevation gain and pace, with breaks, finish time, turnaround time and latest start before sunset.",
    h1="Hiking Time Calculator",
    intro="Enter the distance and elevation gain to estimate how long a hike will take — including breaks — and when you need to start to finish before dark.",
    form=f"""<form id="hikeform" class="panel no-print" onsubmit="return false">
<h2>Your hike</h2>
<div class="row"><div class="field"><label for="dist">Distance (miles, round trip)</label><input type="number" id="dist" min="0" step="0.1" value="8"></div>
<div class="field"><label for="gain">Elevation gain (ft)</label><input type="number" id="gain" min="0" step="50" value="2000"></div></div>
<div class="field"><label for="loss">Elevation loss (ft)</label><input type="number" id="loss" min="0" step="50" value="2000"><div class="hint">For a loop or out-and-back this usually equals the gain.</div></div>
<div class="field"><span class="label">Pace</span>{seg("pace", [("easy", "Relaxed"), ("moderate", "Steady"), ("fast", "Fast")], "moderate")}</div>
<div class="field"><span class="label">Pack</span>{seg("pack", [("1", "Daypack"), ("1.1", "Overnight pack"), ("1.2", "Heavy pack")], "1")}</div>
<div class="field"><label for="breaks">Breaks: minutes per hour of walking</label><input type="number" id="breaks" min="0" max="30" value="10"></div>
<h2>Timing (optional)</h2>
<div class="row"><div class="field"><label for="start">Start time</label><input type="text" id="start" placeholder="07:30" value="08:00"></div>
<div class="field"><label for="date">Date</label><input type="date" id="date"></div></div>
{PLACE_FIELD}
</form>""",
    explain="""<h2 id="formula">The formula</h2>
<p>The calculator uses a version of <strong>Naismith's rule</strong>, the classic hiking time estimate: time on the flat at your walking speed, plus extra time for every foot you climb. A steady hiker averages about 2.5 mph on the flat and adds an hour for every 1,500 ft of gain; relaxed hikers are closer to 2 mph and 1,000 ft per hour, and fit, fast hikers 3 mph and 2,000 ft per hour (Naismith's original). Long, steep descents add a little time too — they're hard on knees and slower than people expect.</p>
<p>Heavier packs slow everyone down, so overnight and heavy loads add 10–20%. Breaks are added on top of moving time: 10 minutes per hour is realistic for most groups once you count photos, snacks and layer changes.</p>
<h2 id="turnaround">Set a turnaround time</h2>
<p>On an out-and-back hike, the turnaround time is the halfway point of your total time. Decide it before you start and stick to it — summit fever is how hikers end up descending in the dark or in an afternoon storm. Pair this with the <a href="/tools/sunrise-sunset/">sunrise and sunset calculator</a> and the <a href="/tools/trail-weather/">trail forecast</a>, and always carry a headlamp.</p>
<p>Scrambling terrain is much slower than trail. On class 3 and 4 ground, budget extra time per mile — see our guides to <a href="/class-3-scramble/">class 3</a> and <a href="/class-4-scramble/">class 4 scrambles</a>.</p>""",
    faq=[("How long does it take to hike 10 miles?", "On a mostly flat trail, a steady hiker covers 10 miles in about 4 to 5 hours including breaks. Add roughly an hour for every 1,500 feet of elevation gain."),
         ("What is Naismith's rule?", "A rule of thumb from 1892: allow one hour for every 3 miles walked plus one hour for every 2,000 feet of ascent. Most hikers today use slower values, which is why this calculator offers three paces."),
         ("How fast does the average person hike?", "About 2 to 3 miles per hour on flat, well-maintained trail, slowing considerably on steep climbs, rough terrain or at high altitude.")],
)

TOOLS["water-calculator"] = dict(
    title="Hiking Water Calculator: How Much Water to Bring",
    description="Calculate how much water to carry on a hike from duration, temperature, effort and body weight, with water weight and refill planning.",
    h1="How Much Water Should I Bring Hiking?",
    intro="A quick estimate of how much water to carry for your hike, based on how long you'll be out, how hot it is, how hard you're working and your body weight.",
    form=f"""<form id="waterform" class="panel no-print" onsubmit="return false">
<h2>Your hike</h2>
<div class="row"><div class="field"><label for="hours">Hours on trail</label><input type="number" id="hours" min="0.5" step="0.5" value="5"></div>
<div class="field"><label for="temp">Expected high (°F)</label><input type="number" id="temp" value="80"></div></div>
<div class="field"><span class="label">Effort</span>{seg("effort", [("easy", "Easy"), ("moderate", "Moderate"), ("hard", "Strenuous")], "moderate")}</div>
<div class="row"><div class="field"><label for="weight">Body weight (lb)</label><input type="number" id="weight" value="160"></div>
<div class="field"><label for="sources">Reliable water sources on route</label><input type="number" id="sources" min="0" value="0"></div></div>
<div class="field"><div class="seg"><label><input type="checkbox" id="humid"> Humid</label><label><input type="checkbox" id="alt"> Above 8,000 ft</label></div></div>
</form>""",
    explain="""<h2 id="rule-of-thumb">The rule of thumb</h2>
<p>A common starting point is <strong>about half a liter (17 oz) per hour</strong> of moderate hiking in mild temperatures. That rises quickly with heat and effort — in desert summer heat, hikers can lose a liter or more per hour. The calculator scales a moderate-effort baseline for temperature (about 3% more per degree above 70°F), body size, humidity and altitude.</p>
<h2 id="carry-or-filter">Carry it or filter it?</h2>
<p>Water weighs 2.2 lb per liter, so on long days it's often smarter to carry enough to reach the next reliable source and treat water there. Only count sources you can confirm are flowing this season, and carry a filter or purifier — see our <a href="/sawyer-squeeze-gravity-setup/">Sawyer Squeeze gravity setup guide</a>. In the desert, assume there's no water.</p>
<div class="callout warn"><strong>Safety:</strong> heat exhaustion signs include heavy sweating, cold clammy skin, nausea, headache, dizziness and weakness. Stop, get into shade, sip water and cool down. Confusion, hot skin or fainting can mean heat stroke — a medical emergency. Call 911. (Source: <a href="https://www.cdc.gov/heat-health/">CDC</a>.)</div>""",
    faq=[("How much water should I bring on a 5-mile hike?", "For a 5-mile hike of about 2.5 to 3 hours in mild weather, 1.5 to 2 liters is typical. In hot weather or with lots of climbing, bring 2.5 to 3 liters or more."),
         ("Can you drink too much water while hiking?", "Yes. Drinking large amounts of plain water without salt over many hours can cause hyponatremia. On long, hot hikes, eat salty snacks or use electrolytes and drink to thirst, steadily."),
         ("How much does a liter of water weigh?", "About 2.2 pounds (1 kilogram). Three liters adds 6.6 pounds to your pack.")],
)

TOOLS["sleeping-bag-temperature"] = dict(
    title="Sleeping Bag Temperature Rating Calculator + Pad R-Value",
    description="Find the sleeping bag comfort rating and sleeping pad R-value you need for your expected overnight low, sleeping style and shelter.",
    h1="Sleeping Bag & Pad Temperature Guide",
    intro="Enter the coldest overnight low you expect and how you sleep. You'll get the bag rating to shop for and the pad R-value that keeps the ground from stealing your heat.",
    form=f"""<form id="bagform" class="panel no-print" onsubmit="return false">
<h2>Your night</h2>
<div class="field"><label for="low">Expected overnight low (°F)</label><input type="number" id="low" value="35"><div class="hint">Check the forecast for your campsite's elevation — lows drop about 3–5°F per 1,000 ft.</div></div>
<div class="field"><span class="label">You usually sleep…</span>{seg("sleeper", [("warm", "Warm"), ("average", "Average"), ("cold", "Cold")], "average")}</div>
<div class="field"><span class="label">Shelter</span>{seg("shelter", [("tent", "Tent"), ("hammock", "Hammock"), ("car", "Car / SUV")], "tent")}</div>
<div class="field"><div class="seg"><label><input type="checkbox" id="wind"> Windy / exposed site</label><label><input type="checkbox" id="damp"> Damp or humid</label></div></div>
</form>""",
    explain="""<h2 id="ratings">Comfort vs limit ratings</h2>
<p>Most bags are tested to the ISO 23537 standard (which replaced EN 13537) and carry two key numbers. The <strong>comfort</strong> rating is the temperature at which a typical cold sleeper stays comfortable in a relaxed position. The <strong>limit</strong> (or lower-limit) rating is the lowest temperature at which a typical warm sleeper stays comfortable curled up — and it's often the number in the product name. The gap is usually around 10°F.</p>
<p>That's why this tool shops by the comfort rating and adds a margin if you sleep cold, camp somewhere windy or damp.</p>
<h2 id="r-value">Why the pad matters as much as the bag</h2>
<p>Your bag's insulation is crushed flat under your body, so the ground pulls heat out of you through the pad. The pad's R-value measures that resistance (ASTM F3340 standard). R-values are additive — stack a foam pad under an inflatable to go colder. As a guide: R 2+ for summer, R 3–4 for spring and fall, R 5+ for camping on snow or frozen ground.</p>
<p>Heading out in the cold? Read our <a href="/cold-weather-camping/">cold weather camping guide</a>, and check what the wind will feel like with the <a href="/tools/feels-like/">wind chill calculator</a>.</p>""",
    faq=[("What temperature sleeping bag do I need?", "Choose a bag whose comfort rating is at or below the coldest low you expect, or about 10°F below it if you sleep cold. A 20°F limit-rated bag usually has a comfort rating near 30°F."),
         ("What R-value do I need for camping?", "About R 2 for warm summer nights, R 3 to 4 for three-season camping with nights near freezing, and R 5 or more for winter and snow camping."),
         ("Is a 30 degree sleeping bag warm enough?", "A bag with a 30°F limit rating is usually comfortable down to about 40°F for average sleepers. For nights near freezing, look for a 30°F comfort rating instead.")],
)

TOOLS["backpack-size"] = dict(
    title="Backpack Size Calculator: Torso Length & Liters",
    description="Find your backpack size from torso length and hip measurement, plus the right pack capacity in liters for day hikes, overnights and long trips.",
    h1="Backpack Size & Torso Fit Calculator",
    intro="Backpacks are sized by torso length, not height. Enter your measurements and trip to get your pack size, hipbelt size and the capacity in liters you actually need.",
    form=f"""<form id="packsizeform" class="panel no-print" onsubmit="return false">
<h2>Your measurements</h2>
<div class="row"><div class="field"><label for="torso">Torso length (in)</label><input type="number" id="torso" min="12" max="26" step="0.5" value="18.5"></div>
<div class="field"><label for="hips">Hip circumference (in)</label><input type="number" id="hips" min="20" max="60" step="0.5" placeholder="optional"></div></div>
<p class="small"><a href="/how-to-measure-torso-length-for-backpack/">How to measure your torso length →</a></p>
<h2>Your trip</h2>
<div class="field"><span class="label">Trip</span>{seg("trip", [("day", "Day hikes"), ("overnight", "Overnights")], "overnight")}</div>
<div class="field" id="nights-row"><label for="nights">Typical nights out</label><input type="number" id="nights" min="1" max="14" value="2"></div>
<div class="field"><span class="label">Gear style</span>{seg("style", [("ul", "Ultralight"), ("std", "Typical"), ("bulky", "Bulky / winter")], "std")}</div>
</form>""",
    explain="""<h2 id="measure">Measuring your torso</h2>
<p>Torso length runs from the bony bump at the base of your neck (the C7 vertebra — tilt your head forward to find it) down to the imaginary line between the tops of your hip bones (iliac crest). Have a friend measure along your spine with a soft tape while you stand straight. Most adults fall between 15 and 22 inches. Our <a href="/how-to-measure-torso-length-for-backpack/">step-by-step torso guide</a> covers it in detail.</p>
<h2 id="sizes">Typical size ranges</h2>
<div class="table-wrap"><table><thead><tr><th>Size</th><th>Torso length</th></tr></thead><tbody>
<tr><td>Extra small</td><td>Under ~15–16 in</td></tr><tr><td>Small</td><td>~16–18 in</td></tr><tr><td>Medium</td><td>~18–20 in</td></tr><tr><td>Large</td><td>~20–22 in</td></tr><tr><td>Extra large</td><td>22 in and up</td></tr></tbody></table></div>
<p>Ranges overlap and differ between brands, which is why many packs have adjustable harnesses. Capacity matters as much as fit: a bigger pack tempts you to carry more. For most people with modern gear, 40–55 liters covers weekend trips. Want to rent before you commit? See <a href="/rent-camping-gear/">where to rent camping gear</a>.</p>""",
    faq=[("What size backpack do I need for a 3 day hike?", "For a 2 to 3 night backpacking trip, most people need 40 to 55 liters with typical modern gear, or 35 to 45 liters with ultralight gear."),
         ("Is backpack size based on height?", "No. Backpacks are sized by torso length, from the C7 vertebra at the base of your neck to the top of your hip bones. Two people of the same height can need different sizes."),
         ("What size daypack do I need?", "18 to 30 liters fits water, layers, food, and the Ten Essentials for a full day hike. Go toward 30 liters for winter or if you carry gear for kids.")],
)

TOOLS["sunrise-sunset"] = dict(
    title="Sunrise & Sunset Calculator for Hikers (Golden Hour)",
    description="Sunrise, sunset, golden hour, civil twilight and daylight hours for any trailhead or park on any date, plus a month-by-month daylight table.",
    h1="Sunrise, Sunset & Daylight Calculator",
    intro="Look up sunrise, sunset, golden hour and usable daylight for any trailhead, park or town on any date — and see how daylight changes month by month when you're planning a trip.",
    form=f"""<div class="panel no-print">
<h2>Place and date</h2>
{PLACE_FIELD}
<div class="btns"><button type="button" class="btn outline sm" id="locate">Use my location</button></div>
<p class="status" id="status"></p>
<div class="field"><label for="date">Date</label><input type="date" id="date"></div>
</div>""",
    explain="""<h2 id="terms">What the times mean</h2>
<ul><li><strong>Civil dawn / dusk:</strong> the sun is 6° below the horizon. There's enough light to hike without a headlamp on open trail — but not in a forest or canyon.</li>
<li><strong>Golden hour:</strong> when the sun is less than 6° above the horizon. Warm, low light — the best time for landscape and portrait photos (see <a href="/how-to-pose-for-hiking-pictures/">how to pose for hiking pictures</a>).</li>
<li><strong>Solar noon:</strong> the sun's highest point, when shade is scarcest and UV is strongest.</li></ul>
<h2 id="planning">Planning with daylight</h2>
<p>Short winter days catch hikers out more than anything else. Work backward from sunset with the <a href="/tools/hiking-time-calculator/">hiking time calculator</a>, and keep a headlamp in your pack year-round. For sunrise summits, plan to reach the top at civil dawn — the sky is often most colorful 20–30 minutes before the sun appears.</p>""",
    faq=[("What time is golden hour?", "Golden hour runs from sunrise until the sun is about 6 degrees high in the morning, and from when the sun drops to about 6 degrees until sunset in the evening. That's often 30 to 60 minutes, longer in winter and at high latitudes."),
         ("How long after sunset is it dark?", "Civil twilight, when you can still see on open ground, lasts about 25 to 40 minutes after sunset in most of the US. Under trees or in canyons it gets dark much sooner."),
         ("Why does the sun set earlier in canyons?", "Official sunset assumes a flat horizon. Canyon walls, mountains and ridges block the sun earlier, so in places like Zion or the Grand Canyon's inner trails you lose direct light well before the listed time.")],
)

TOOLS["camp-meal-planner"] = dict(
    title="Backpacking Food Calculator: Calories & Food Weight",
    description="Plan camping and backpacking food: calories per day, food weight per person and for the group, and a daily meal plan you can adjust.",
    h1="Camp Meal & Food Weight Planner",
    intro="How much food do you really need? Set your group, days and trip style to get daily calories, total food weight and a simple meal plan.",
    form=f"""<form id="mealform" class="panel no-print" onsubmit="return false">
<h2>Your trip</h2>
<div class="row"><div class="field"><label for="people">People</label><input type="number" id="people" min="1" value="2"></div>
<div class="field"><label for="days">Days of food</label><input type="number" id="days" min="1" value="3"></div></div>
<div class="field"><span class="label">Trip style</span>{seg("style", [("car", "Car camping"), ("backpack", "Backpacking"), ("hard", "Big-mileage / mountains")], "backpack")}</div>
<div class="field"><label for="size">Average body size</label><select id="size"><option value="0.85">Smaller</option><option value="1" selected>Average</option><option value="1.2">Larger</option></select></div>
<div class="field"><div class="seg"><label><input type="checkbox" id="cold"> Cold weather (adds ~15%)</label></div></div>
</form>""",
    explain="""<h2 id="calories">How many calories on the trail?</h2>
<p>Hiking with a pack burns a lot more than a normal day. Most backpackers need roughly <strong>2,500–3,500 calories a day</strong>, and big mileage in the mountains or cold weather can push that past 4,000. Few people can eat that much on the trail, so the goal is to carry dense food you'll actually want to eat.</p>
<h2 id="density">Calorie density is the key</h2>
<p>Aim for <strong>100–125 calories per ounce</strong> across your food bag. Nuts, nut butter, olive oil, chocolate, cheese and dried meats are dense; fresh fruit and canned food are not. At 110 cal/oz, a 3,000-calorie day weighs about 1.7 lb.</p>
<p>Biking instead of hiking? See <a href="/bikepacking-food/">bikepacking food</a>. Store food properly in bear country — in many parks a bear canister or locker is required.</p>""",
    faq=[("How many calories do you burn backpacking?", "Roughly 400 to 600 calories per hour of hiking with a pack, depending on body weight, pack weight and terrain. Over a full day that often adds up to 3,000 to 4,500 calories."),
         ("How many pounds of food per day for backpacking?", "Plan about 1.5 to 2 pounds per person per day. Dense foods at 120+ calories per ounce let you carry 3,000 calories in under 1.6 pounds."),
         ("What foods have the most calories per ounce?", "Olive oil (about 240), macadamia nuts and pecans (about 200), most nuts and nut butters (160 to 190), and chocolate (about 150).")],
)

TOOLS["rent-vs-buy"] = dict(
    title="Rent vs Buy Camping Gear Calculator (Break-Even)",
    description="Should you rent or buy camping gear? Compare costs for a tent, sleeping bag, pad and pack and find the break-even number of trips.",
    h1="Rent vs Buy Camping Gear Calculator",
    intro="Rental prices add up fast — but so does a garage full of gear you use once a year. Enter your trips and prices to see the break-even point for each item.",
    form="""<form id="rentform" class="panel no-print" onsubmit="return false">
<h2>How often you camp</h2>
<div class="row"><div class="field"><label for="trips">Trips per year</label><input type="number" id="trips" min="0" value="3"></div>
<div class="field"><label for="years">Years you'd keep the gear</label><input type="number" id="years" min="1" value="3"></div></div>
<div class="field"><label for="resale">Resale value when you're done (%)</label><input type="number" id="resale" min="0" max="80" value="25"></div>
<h2>Gear (edit prices to match real quotes)</h2>
<div class="table-wrap"><table id="items"><thead><tr><th></th><th>Item</th><th>Buy $</th><th>Rent $/trip</th><th>Break-even</th></tr></thead><tbody>
<tr data-name="Tent"><td><input type="checkbox" checked></td><td>Tent (2–3 person)</td><td><input class="buy" type="number" value="250"></td><td><input class="rent" type="number" value="45"></td><td class="be"></td></tr>
<tr data-name="Sleeping bag"><td><input type="checkbox" checked></td><td>Sleeping bag</td><td><input class="buy" type="number" value="180"></td><td><input class="rent" type="number" value="30"></td><td class="be"></td></tr>
<tr data-name="Sleeping pad"><td><input type="checkbox" checked></td><td>Sleeping pad</td><td><input class="buy" type="number" value="110"></td><td><input class="rent" type="number" value="20"></td><td class="be"></td></tr>
<tr data-name="Backpack"><td><input type="checkbox" checked></td><td>Backpacking pack</td><td><input class="buy" type="number" value="230"></td><td><input class="rent" type="number" value="35"></td><td class="be"></td></tr>
<tr data-name="Stove & cook kit"><td><input type="checkbox" checked></td><td>Stove + cook kit</td><td><input class="buy" type="number" value="90"></td><td><input class="rent" type="number" value="20"></td><td class="be"></td></tr>
<tr data-name="Bear canister"><td><input type="checkbox"></td><td>Bear canister</td><td><input class="buy" type="number" value="85"></td><td><input class="rent" type="number" value="10"></td><td class="be"></td></tr>
</tbody></table></div>
<p class="small muted">Default prices are illustrative mid-range figures, not quotes. Rental pricing varies a lot by shop and trip length.</p>
</form>""",
    explain="""<h2 id="rule">The short answer</h2>
<p>If you'll camp <strong>more than four or five times</strong> over the life of the gear, buying usually wins for the core items — tent, bag, pad and pack. Renting wins for your first few trips, for specialized gear you'll use once (bear canisters, snowshoes, winter tents), and when flying to a trip where hauling gear costs more than renting at the destination.</p>
<p>Renting first also lets you try gear before spending hundreds on it. Read <a href="/best-camping-gear-to-rent-vs-buy/">what to rent vs buy</a> item by item, and <a href="/rent-camping-gear/">where to rent camping gear</a>.</p>""",
    faq=[("Is it cheaper to rent or buy camping gear?", "Renting is cheaper for one to three trips. For core gear like a tent and sleeping bag, buying usually becomes cheaper after about four to six trips, especially if you resell it later."),
         ("How much does it cost to rent camping gear?", "Prices vary by shop and region. A tent rental commonly runs tens of dollars for a weekend, and complete kits for two cost more. Get quotes from a couple of shops and plug them in above."),
         ("What camping gear should you buy first?", "Buy items that need a personal fit or that you'd rather not share: hiking boots, a sleeping pad and a sleeping bag or liner. Rent the big, expensive items like tents and packs until you know what you like.")],
)

TOOLS["feels-like"] = dict(
    title="Wind Chill & Heat Index Calculator for Hikers",
    description="Calculate wind chill and heat index with the National Weather Service formulas, with frostbite timing and heat illness risk levels for hiking.",
    h1="Wind Chill & Heat Index Calculator",
    intro="Air temperature alone doesn't tell you how dangerous it is out there. Enter temperature, humidity and wind to see what it really feels like — and the risk level for hiking.",
    form="""<form id="feelform" class="panel no-print" onsubmit="return false">
<h2>Conditions</h2>
<div class="field"><label for="t">Air temperature (°F)</label><input type="number" id="t" value="95"></div>
<div class="row"><div class="field"><label for="rh">Relative humidity (%)</label><input type="number" id="rh" min="0" max="100" value="40"></div>
<div class="field"><label for="v">Wind speed (mph)</label><input type="number" id="v" min="0" value="5"></div></div>
<p class="small muted">Humidity is used for heat index (80°F and up); wind for wind chill (50°F and below).</p>
</form>""",
    explain="""<h2 id="formulas">The formulas</h2>
<p>Both numbers use the official <a href="https://www.weather.gov/">National Weather Service</a> equations. <strong>Heat index</strong> combines temperature and humidity to estimate how hot it feels in the shade — sweat evaporates less in humid air, so your body can't cool itself. Direct sun can add up to 15°F more. <strong>Wind chill</strong> estimates how cold exposed skin feels as wind strips away body heat, and how fast frostbite can set in.</p>
<h2 id="trail">On the trail</h2>
<ul><li>In heat, start at first light, rest in shade and size your water with the <a href="/tools/water-calculator/">water calculator</a>. See also <a href="/cool-a-tent-without-electricity/">how to stay cool at camp</a>.</li>
<li>In cold wind, a windproof shell does more than another fleece. Size your sleep system with the <a href="/tools/sleeping-bag-temperature/">sleeping bag guide</a> and read <a href="/cold-weather-camping/">cold weather camping</a>.</li></ul>""",
    faq=[("What heat index is too hot to hike?", "The National Weather Service treats a heat index of 103°F and above as dangerous, with heat exhaustion and heat stroke likely during prolonged exertion. Many hikers avoid strenuous hiking when it's above 90°F."),
         ("At what wind chill does frostbite occur?", "At a wind chill around -18°F, frostbite can develop on exposed skin in about 30 minutes. At about -32°F it can take 10 minutes, and at -48°F five minutes or less."),
         ("Does wind chill affect water bottles or tents?", "No. Wind chill describes heat loss from skin. Objects only cool to the actual air temperature, though wind makes them get there faster.")],
)

MONTH_OPTS = "".join(f'<option value="{i}">{m}</option>' for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]))

TOOLS["trip-finder"] = dict(
    title="Trip Finder: Best National Parks Near Me This Month",
    description="Find the best parks near you for any month: share your location or enter an address, and we rank parks by drive time and 10 years of hiking and camping weather.",
    h1="Trip Finder: Best Parks Near You This Month",
    intro="Share your location — or type any address, town or ZIP code — and we'll rank parks within driving distance by how good their hiking and camping weather is in the month you want to go.",
    form=f"""<div class="panel no-print">
<h2>1. Where are you starting from?</h2>
<button type="button" class="btn primary" id="use-loc" style="width:100%;justify-content:center">📍 Use my location</button>
<p class="small muted" style="margin:8px 0 14px">Your location stays in your browser. We don't store it.</p>
<form id="addr-form" class="field"><label for="addr">Or enter an address, town or ZIP code</label>
<div style="display:flex;gap:8px"><input type="search" id="addr" placeholder="e.g. 80302, Asheville NC, or a street address" autocomplete="off"><button class="btn outline sm" type="submit">Find</button></div>
<div class="hint">Address lookup by <a href="https://www.openstreetmap.org/copyright" rel="nofollow noopener">© OpenStreetMap</a> contributors.</div></form>
<p class="status" id="loc-status" aria-live="polite"></p>
<div id="origin-box" class="callout tip" hidden><strong>Starting from:</strong> <span id="origin-label"></span> <button type="button" class="chip" id="change-loc" style="cursor:pointer;margin-left:6px">Change</button></div>
<form id="tf-opts" onsubmit="return false">
<h2 style="margin-top:22px">2. When and how far?</h2>
<div class="field"><label for="month">Month</label><select id="month">{MONTH_OPTS}</select></div>
<div class="field"><span class="label">Max drive</span>{seg("drive", [("3", "3 hrs"), ("6", "6 hrs"), ("8", "8 hrs"), ("12", "12 hrs"), ("99", "Any (I'll fly)")], "8")}</div>
<div class="field"><span class="label">Prioritize</span>{seg("pref", [("weather", "Best weather"), ("balanced", "Balanced"), ("close", "Closest")], "balanced")}</div>
</form>
</div>""",
    explain="""<h2 id="how-it-works">How Trip Finder ranks parks</h2>
<p>Every park on Arrive Outdoors has a <strong>monthly weather score</strong> built from 10 years of daily weather (2015–2024) at its main visitor area: comfortable highs, mild nights, few rain or snow days and little extreme heat score best. Trip Finder combines that score with an estimated drive time from your starting point, then drops anything beyond your maximum drive.</p>
<ul><li><strong>Best weather</strong> leans hard toward the score — worth it for a long-weekend road trip.</li>
<li><strong>Balanced</strong> trades a little weather for a shorter drive.</li>
<li><strong>Closest</strong> favors whatever's near you, as long as the weather isn't poor that month.</li></ul>
<p>Drive times are estimates from straight-line distance (roads typically add about a quarter) at highway speeds, so use the Directions link for a real route. Weather scores don't account for crowds, road closures or permits — each <a href="/destinations/">destination guide</a> covers those, and the <a href="/tools/trail-weather/">trail forecast</a> shows the next 7 days.</p>
<h2 id="privacy">Your location and privacy</h2>
<p>"Use my location" asks your browser for permission; the coordinates are used on this page to calculate distances and are saved only in your browser so the tool remembers you next time. If you type an address, it's sent to OpenStreetMap's geocoding service to find its coordinates. See our <a href="/privacy-policy/">privacy policy</a>.</p>
<p>Want a month-wide view instead? See <a href="/weather/">where to go hiking this month</a>.</p>""",
    faq=[("How do I find national parks near me?", "Use Trip Finder: allow location access or type your town or ZIP code, choose how far you're willing to drive, and it lists the parks in range ranked by that month's weather."),
         ("What is the best national park to visit this month?", "It depends on where you are. Trip Finder ranks parks by weather for the month you pick and by distance from you; the where-to-go-by-month guide ranks all parks on weather alone."),
         ("Does Trip Finder store my location?", "No. Your coordinates are used in your browser and saved only on your device. Typed addresses are looked up through OpenStreetMap's geocoder to get coordinates.")],
)
