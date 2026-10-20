"""Moving Resources pages — the eleven guides from the original site's menu.

URLs match the original WordPress site (/moving-resources/<slug>/). The original
copy could not be recovered, so each guide is written fresh.
Body HTML: every <h2> needs an id (the build turns them into the page's table of contents).
"""

RESOURCES = [
# ---------------------------------------------------------------- apartment locator
{
"slug": "apartment-locator",
"name": "Apartment Locator",
"icon": "map-pin",
"short": "Free help finding apartments that fit your budget, area and move date.",
"seo_title": "Apartment Locator: How Free Apartment Locating Works",
"desc": "How free apartment locator services work, what they cost (usually nothing), what to ask, and how to use one to find the right apartment faster.",
"h1": "Apartment Locator: Find Your Next Place Without the Legwork",
"lead": "An apartment locator does the searching, calling and comparing for you, and in most cities the service is free to renters. Here's how locating works and how to get the most out of it.",
"tool": "affordability",
"body": """
<h2 id="what-is">What an apartment locator actually does</h2>
<p>An apartment locator (sometimes called an apartment finder or rental agent) is a licensed real-estate professional who matches renters with apartment communities. You share your budget, preferred neighborhoods, move-in date, must-haves and deal-breakers. The locator then pulls current availability, specials and pricing from dozens of properties, narrows the list, and often schedules tours or sends video walkthroughs.</p>
<p>Because locators talk to leasing offices every day, they tend to know things a listing site won't show you: which communities are running look-and-lease specials, which ones are strict about credit or rental history, and where the "available now" units actually are.</p>

<h2 id="cost">Is an apartment locator free?</h2>
<p>For renters, usually yes. In large rental markets — Dallas–Fort Worth, Houston, Austin, San Antonio, Atlanta, Phoenix and many others — apartment communities pay the locator a referral commission when you sign a lease. That fee is typically a percentage of one month's rent and is built into the property's marketing budget, not added to your rent.</p>
<div class="callout">__ICON_info__<div><p><strong>Important:</strong> list the locator on your rental application (most applications have a "referred by" or "locator" field). If you tour a property on your own first and then use a locator, the property may not honor the referral.</p></div></div>
<p>In some markets (parts of New York City and Boston, for example) renters may be asked to pay a broker fee. Always ask up front: "Will I owe you anything, now or at signing?"</p>

<h2 id="how-it-works">How the process works, step by step</h2>
<ol class="steps">
<li><strong>Set your budget.</strong> Decide on a total monthly number that includes rent, utilities, parking and pet rent. Use the affordability calculator below if you're not sure.</li>
<li><strong>Share your criteria.</strong> Bedrooms, move-in date, commute, school zone, pets, in-unit laundry, garage, credit or rental-history concerns.</li>
<li><strong>Get a shortlist.</strong> A good locator sends 5–10 options with current prices, specials and floor plans rather than a list of 40.</li>
<li><strong>Tour.</strong> In person or by video. Ask the leasing agent about total monthly cost, not just base rent.</li>
<li><strong>Apply and name your locator.</strong> Submit one application at a time when you can — each one usually carries a non-refundable fee.</li>
<li><strong>Sign and plan the move.</strong> Lock in your move-in date, then set up <a href="/moving-resources/utility-connections/">utilities</a>, <a href="/moving-resources/rental-insurance/">renters insurance</a> and <a href="/moving-resources/movers/">movers</a>.</li>
</ol>

<h2 id="questions">Questions to ask any locator</h2>
<ul>
<li>Are you licensed, and in which state? (In Texas, locators must hold a real-estate license through TREC.)</li>
<li>Do I pay anything — now, at signing, or if I break the lease?</li>
<li>Which properties do you <em>not</em> work with, and why?</li>
<li>Can you work with my credit score, past eviction or broken lease?</li>
<li>Do you offer a rebate or move-in gift? (Some locators share part of their commission where state rules allow.)</li>
</ul>

<h2 id="pros-cons">Locator vs. searching on your own</h2>
<div class="table-scroll"><table>
<tr><th></th><th>Apartment locator</th><th>DIY search</th></tr>
<tr><td>Cost to renter</td><td>Usually free</td><td>Free</td></tr>
<tr><td>Time spent</td><td>A few hours</td><td>Days to weeks</td></tr>
<tr><td>Access to specials</td><td>Strong — they hear about them first</td><td>Only what's advertised</td></tr>
<tr><td>Help with credit issues</td><td>Knows which properties are flexible</td><td>Trial and error (and application fees)</td></tr>
<tr><td>Best for</td><td>Relocating, tight timelines, credit challenges</td><td>Small towns, private landlords, very specific buildings</td></tr>
</table></div>

<h2 id="red-flags">Red flags to avoid</h2>
<div class="callout warn">__ICON_alert__<div><p>Walk away from anyone who asks you to wire a deposit before you've seen the unit, pressures you to sign the same day, or can't show a license number. Rental scams often copy real listings and undercut the price to rush you.</p></div></div>
<p>Once you've found the place, our <a href="/5-easy-steps-to-find-your-perfect-apartment/">5 easy steps to find your perfect apartment</a> walk through the touring and application stage in more detail.</p>
""",
"faqs": [
("Do apartment locators cost money?", "In most U.S. rental markets, no. The apartment community pays the locator a referral fee when you sign a lease. Some high-cost cities use renter-paid broker fees instead, so always ask before you start."),
("Will using a locator raise my rent?", "No. The referral fee comes from the property's marketing budget and the rent is the same whether you use a locator or walk in yourself."),
("Can an apartment locator help with bad credit or an eviction?", "Often, yes. Locators know which properties use more flexible screening, accept guarantors or offer second-chance leasing, which can save you from paying application fees at places that will decline you."),
("Do I need to name the locator on my application?", "Yes. If the locator isn't listed on your application or guest card, the property may not pay them — and some locators can't help you with that property afterward."),
],
},
# ---------------------------------------------------------------- maid services
{
"slug": "maid-services",
"name": "Maid Services",
"icon": "sparkles",
"short": "Move-out and move-in cleaning that protects your security deposit.",
"seo_title": "Move-Out Cleaning & Maid Services for Renters",
"desc": "Hire the right maid service for your move-out or move-in clean: what it costs, what's included, and a room-by-room checklist that helps you get your deposit back.",
"h1": "Maid Services for Renters: Move-Out & Move-In Cleaning",
"lead": "A professional move-out clean is one of the cheapest ways to protect a security deposit worth hundreds — or thousands — of dollars. Here's what to book, what it costs and what landlords actually inspect.",
"tool": "inspection",
"body": """
<h2 id="why">Why a move-out clean pays for itself</h2>
<p>Most leases require you to return the unit "in the same condition as move-in, less normal wear and tear." Landlords can deduct reasonable cleaning costs from your deposit if the unit is left dirty — and their rates are often higher than what you'd pay a cleaner yourself. A $200–$400 professional clean can protect a deposit of $500 to a full month's rent.</p>

<h2 id="types">Types of cleaning (and what each includes)</h2>
<div class="compare">
<div class="card"><h3>Standard clean</h3><ul><li>Dusting and wiping surfaces</li><li>Kitchen counters, sink, stovetop exterior</li><li>Bathrooms, floors, vacuuming</li></ul></div>
<div class="card"><h3>Deep clean</h3><ul><li>Everything in standard</li><li>Baseboards, door frames, switch plates</li><li>Inside microwave, grout scrubbing, blinds</li></ul></div>
<div class="card"><h3>Move-out / move-in</h3><ul><li>Everything in deep clean</li><li>Inside oven, fridge, cabinets and drawers</li><li>Closets, windowsills, tracks, vents</li></ul></div>
</div>

<h2 id="cost">What maid services cost</h2>
<div class="table-scroll"><table>
<tr><th>Home size</th><th>Standard clean</th><th>Move-out clean</th></tr>
<tr><td>Studio / 1 bedroom</td><td>$100–$170</td><td>$180–$300</td></tr>
<tr><td>2 bedrooms</td><td>$140–$220</td><td>$250–$400</td></tr>
<tr><td>3 bedrooms</td><td>$180–$280</td><td>$320–$500</td></tr>
</table></div>
<p class="note">Typical ranges for planning only; prices vary by city, condition and add-ons such as carpet shampooing or wall washing.</p>

<h2 id="checklist">Move-out cleaning checklist</h2>
<h3 id="kitchen">Kitchen</h3>
<ul><li>Inside and outside of oven, stovetop, drip pans and range hood filter</li><li>Inside fridge and freezer (unplug only if the lease allows; leave doors ajar)</li><li>Cabinets and drawers inside and out, sink and faucet, dishwasher seal</li></ul>
<h3 id="bathrooms">Bathrooms</h3>
<ul><li>Toilet including base and behind, tub/shower and grout, glass doors</li><li>Mirror, vanity, inside drawers, exhaust fan cover</li></ul>
<h3 id="living">Living areas and bedrooms</h3>
<ul><li>Baseboards, doors, light switches, outlet covers, ceiling fans</li><li>Blinds, windowsills and tracks, closet shelves and floors</li><li>Vacuum and mop; spot-clean carpet stains or book a carpet clean if your lease requires it</li></ul>
<div class="callout">__ICON_bulb__<div><p><strong>Take dated photos and video</strong> of every room after the clean, and keep the cleaner's receipt. If your landlord deducts cleaning fees, that's your evidence. Our inspection checklist below creates a room-by-room record you can print or copy.</p></div></div>

<h2 id="hiring">How to choose a cleaning service</h2>
<ul>
<li>Confirm they're <strong>insured and bonded</strong> and run background checks on staff.</li>
<li>Ask for a written list of what "move-out clean" includes — inside appliances is often an add-on.</li>
<li>Look for a re-clean guarantee if the landlord flags anything within 24–48 hours.</li>
<li>Book 1–2 weeks ahead; month-end dates fill up fast because that's when most leases end.</li>
<li>Schedule the clean <em>after</em> the movers are done so the cleaner can reach every corner.</li>
</ul>

<h2 id="move-in">Don't skip the move-in clean</h2>
<p>Turnover cleans between tenants are sometimes rushed. A move-in clean before your furniture arrives is easier than cleaning around boxes — and it's the moment to document any existing damage so you're not charged for it later. Pair it with our <a href="/tools/move-in-inspection-checklist/">move-in inspection checklist</a>.</p>
""",
"faqs": [
("How much does a move-out cleaning cost?", "Most renters pay roughly $180–$500 depending on the size and condition of the home and whether inside-appliance cleaning or carpet shampooing is included."),
("Can a landlord charge me for cleaning?", "Landlords can generally deduct reasonable cleaning costs if the unit is left dirtier than normal wear and tear. They usually can't charge you for routine turnover tasks like repainting after a normal tenancy. Rules vary by state."),
("When should I schedule the move-out clean?", "After everything is out of the unit and before your final walkthrough — ideally the day after the movers, leaving time for touch-ups."),
("Is a move-in clean worth it?", "Yes if the unit wasn't cleaned well between tenants. It's also the best time to photograph and record existing damage."),
],
},
# ---------------------------------------------------------------- movers
{
"slug": "movers",
"name": "Movers",
"icon": "box",
"short": "How to compare moving companies, read quotes and avoid scams.",
"seo_title": "How to Hire Movers: Costs, Quotes & Avoiding Moving Scams",
"desc": "Compare local and long-distance movers, understand binding vs. non-binding estimates, check USDOT numbers and estimate your moving cost with our free calculator.",
"h1": "Hiring Movers: Compare Quotes, Costs & Red Flags",
"lead": "Good movers make moving day almost easy. The wrong ones hold your belongings hostage. Here's how to compare quotes, check credentials and figure out what your move should cost.",
"tool": "moving-cost",
"body": """
<h2 id="options">Your moving options</h2>
<div class="compare">
<div class="card"><h3>Full-service movers</h3><ul><li>They pack, load, drive and unload</li><li>Highest cost, least effort</li><li>Best for busy schedules or long moves</li></ul></div>
<div class="card"><h3>Labor-only movers</h3><ul><li>You rent the truck; they load/unload</li><li>Hourly, often 2-hour minimum</li><li>Great middle ground for local moves</li></ul></div>
<div class="card"><h3>Moving containers</h3><ul><li>A pod is dropped off; you pack it</li><li>Flexible timing and storage</li><li>Good for long distance on a budget</li></ul></div>
</div>
<p>Doing it yourself? Read <a href="/10-steps-for-a-successful-diy-move/">10 steps for a successful DIY move</a> and compare <a href="/moving-resources/moving-truck-rentals/">moving truck rentals</a>.</p>

<h2 id="costs">What movers cost</h2>
<p>Local moves (generally under 50 miles) are usually billed <strong>by the hour</strong> for a crew and truck — commonly $100–$200 per hour for two or three movers, plus a travel fee. Long-distance moves are priced mainly by <strong>weight (or volume) and distance</strong>, with extra charges for stairs, long carries, bulky items, packing and storage.</p>
<div class="table-scroll"><table>
<tr><th>Home size</th><th>Local (typical)</th><th>~1,000 miles (typical)</th></tr>
<tr><td>Studio / 1 bedroom</td><td>$400–$900</td><td>$2,000–$4,000</td></tr>
<tr><td>2 bedrooms</td><td>$800–$1,500</td><td>$3,500–$6,500</td></tr>
<tr><td>3 bedrooms</td><td>$1,200–$2,400</td><td>$5,000–$9,000</td></tr>
</table></div>
<p class="note">Planning ranges only. Use the estimator below for your own numbers, then get at least three written quotes.</p>

<h2 id="estimates">Binding vs. non-binding estimates</h2>
<ul>
<li><strong>Binding estimate:</strong> the price is fixed for the items listed. Add items and the price changes.</li>
<li><strong>Binding not-to-exceed:</strong> you pay the lower of the estimate or the actual weight — the renter-friendliest option.</li>
<li><strong>Non-binding estimate:</strong> the final bill depends on actual weight/time. For interstate moves, federal rules generally limit what the mover can demand at delivery to the estimate plus 10%, with the rest billed later.</li>
</ul>
<div class="callout">__ICON_info__<div><p>Insist on an in-home or live video survey. A quote given over the phone without seeing your stuff is the number-one source of moving-day surprises.</p></div></div>

<h2 id="vetting">How to check a moving company</h2>
<ol class="steps">
<li><strong>Interstate movers</strong> must have a USDOT number — look it up on the FMCSA's site and check their complaint history.</li>
<li><strong>Intrastate movers</strong> may need a state license. In Texas, household-goods movers register with TxDMV.</li>
<li>Read recent reviews on more than one platform, looking for patterns (late arrivals, damage claims, price hikes).</li>
<li>Confirm the company — not a broker — will do the move, or ask who the carrier is.</li>
<li>Get everything in writing: estimate, inventory, pickup/delivery windows and valuation coverage.</li>
</ol>

<h2 id="red-flags">Moving scam red flags</h2>
<div class="callout warn">__ICON_alert__<div><ul style="margin:0"><li>A large cash deposit before the move</li><li>A quote far below everyone else's</li><li>No physical address, license or USDOT number</li><li>The truck shows up unmarked or with a rental logo</li><li>They ask you to sign blank or incomplete paperwork</li></ul></div></div>

<h2 id="protection">Protecting your belongings</h2>
<p>By default, interstate movers' liability is often limited to about 60 cents per pound per item (released value) — a 10 lb laptop would be "worth" $6. Full-value protection costs extra. Check whether your <a href="/moving-resources/rental-insurance/">renters insurance</a> covers belongings in transit, and keep valuables, documents and medications with you.</p>

<h2 id="tips">Tips to lower the bill</h2>
<ul>
<li>Move mid-month and mid-week; avoid the end of the month and summer weekends when you can.</li>
<li>Declutter first — every box you sell or donate is one you don't pay to move.</li>
<li>Pack yourself (see our <a href="/tools/packing-calculator/">packing calculator</a>) and have everything ready when the crew arrives.</li>
<li>Reserve elevator time and close-in parking so the crew isn't paid to walk.</li>
</ul>
""",
"faqs": [
("How far in advance should I book movers?", "Four to eight weeks ahead for most moves, and earlier for summer or end-of-month dates. Long-distance moves benefit from even more lead time."),
("How much should I tip movers?", "A common guideline is $20–$40 per mover for a half-day local move and $40–$60+ each for a full day or a difficult move, plus cold drinks. Tipping is optional and should reflect the service."),
("What's the difference between a moving broker and a carrier?", "A carrier owns the trucks and employs the crew. A broker sells your move to a carrier. Brokers are legal but you should know who will actually show up and who is liable for damage."),
("Do movers move plants, paint or propane?", "Most won't. Hazardous items (paint, propane, fuel, cleaning chemicals) and often live plants are excluded. Ask for the mover's non-allowable list."),
],
},
# ---------------------------------------------------------------- truck rentals
{
"slug": "moving-truck-rentals",
"name": "Moving Truck Rentals",
"icon": "truck",
"short": "Pick the right truck size, compare rental costs and drive it safely.",
"seo_title": "Moving Truck Rentals: What Size Truck Do I Need?",
"desc": "Choose the right moving truck size with our calculator, compare one-way and local rental costs, and learn the fees, insurance and driving tips that matter.",
"h1": "Moving Truck Rentals: Size, Cost & Booking Tips",
"lead": "Renting a truck is usually the cheapest way to move — if you pick the right size and know the fees. Use the truck size finder, then compare the real cost before you book.",
"tool": "truck-size",
"body": """
<h2 id="sizes">Truck sizes at a glance</h2>
<div class="table-scroll"><table>
<tr><th>Truck</th><th>Approx. capacity</th><th>Typically fits</th></tr>
<tr><td>Cargo van</td><td>~250 cu ft</td><td>Dorm or small studio, a few large items</td></tr>
<tr><td>10 ft truck</td><td>~400 cu ft</td><td>Studio or small 1-bedroom</td></tr>
<tr><td>15 ft truck</td><td>~760 cu ft</td><td>1–2 bedrooms</td></tr>
<tr><td>20 ft truck</td><td>~1,000 cu ft</td><td>2–3 bedrooms</td></tr>
<tr><td>26 ft truck</td><td>~1,700 cu ft</td><td>3–5 bedrooms</td></tr>
</table></div>
<p class="note">Capacities vary by rental company and model. When in doubt, size up — a second trip costs more than a bigger truck.</p>

<h2 id="cost">What a rental really costs</h2>
<p><strong>Local (in-town) rentals</strong> usually have a low daily rate — often $20–$60 for smaller trucks — plus a <strong>per-mile charge</strong> (commonly around $0.80–$1.30 per mile). <strong>One-way rentals</strong> are quoted as a package with a set number of days and miles included, and prices swing a lot by route and season.</p>
<p>Budget for the extras:</p>
<ul>
<li><strong>Fuel:</strong> large trucks often get roughly 8–12 mpg. Return it with the same fuel level or pay a premium.</li>
<li><strong>Damage protection:</strong> your personal auto policy and credit card often <em>don't</em> cover large rental trucks. Check before declining the rental company's coverage.</li>
<li><strong>Equipment:</strong> furniture pads, a utility dolly and an appliance dolly are worth the few dollars each.</li>
<li><strong>Taxes, environmental fees and late returns.</strong></li>
</ul>

<h2 id="compare">Truck vs. container vs. movers</h2>
<p>A truck is cheapest when you have friends to help and a short distance. For long moves, a <a href="/moving-resources/movers/">moving container</a> can be close in price once you add fuel, lodging and time off work. Run your numbers in the <a href="/tools/moving-cost-calculator/">moving cost calculator</a>.</p>

<h2 id="booking">Booking tips</h2>
<ol class="steps">
<li>Book 2–4 weeks out (6+ in summer). End-of-month weekends sell out first.</li>
<li>Confirm the exact pickup location — reservations at busy times are sometimes moved to another branch.</li>
<li>Ask about deck height, loading ramp and whether a tow dolly or car trailer fits your vehicle.</li>
<li>Photograph the truck inside and out at pickup, including the fuel gauge and odometer.</li>
</ol>

<h2 id="driving">Driving a moving truck safely</h2>
<ul>
<li>Know your clearance height — drive-throughs, parking garages and low bridges are the classic mistakes.</li>
<li>Leave double the stopping distance; a loaded truck takes much longer to stop.</li>
<li>Use mirrors constantly and make wide right turns.</li>
<li>Load heavy items first, against the cab, and distribute weight evenly side to side.</li>
<li>Back up with a spotter, and avoid backing up at all when you can.</li>
</ul>
""",
"faqs": [
("What size moving truck do I need for a 2-bedroom apartment?", "Most 2-bedroom apartments fit in a 15 ft truck; a 20 ft truck is safer if you have large furniture, a home office or a lot of boxes."),
("Do I need a special license to drive a moving truck?", "Not for standard consumer rental trucks up to 26 ft in the U.S.; a regular driver's license is enough. Check the rental company's minimum age requirement."),
("Does my car insurance cover a rental moving truck?", "Often not. Many personal auto policies and credit cards exclude trucks above a certain size. Call your insurer before you decline the rental company's protection."),
("Is a one-way truck rental cheaper than movers?", "Usually, yes, especially for smaller homes. Factor in fuel, lodging, time off work and help with loading before you decide."),
],
},
# ---------------------------------------------------------------- credit rent boost
{
"slug": "credit-rent-boost",
"name": "Credit Rent Boost",
"icon": "trending-up",
"short": "Turn on-time rent payments into credit history with rent reporting.",
"seo_title": "Credit Rent Boost: Build Credit With Your Rent",
"desc": "How rent reporting services like Credit Rent Boost work, which credit bureaus see your rent, what it costs, and who benefits most from reporting rent payments.",
"h1": "Credit Rent Boost: Build Credit With the Rent You Already Pay",
"lead": "Rent is probably your biggest monthly bill, yet it usually never shows up on your credit report. Rent reporting changes that — here's how it works and whether it's worth it for you.",
"tool": None,
"body": """
<h2 id="what">What rent reporting is</h2>
<p>Rent reporting services verify your monthly rent payments and send them to one or more of the three major credit bureaus (Equifax, Experian and TransUnion) as a tradeline. Once it appears on your report, every on-time payment can help build your credit history — the same way a car loan or credit card would.</p>
<p><strong>Credit Rent Boost</strong> is one of the services that does this; others include programs run by property-management software, banks and fintech apps. Some landlords report rent automatically, so ask your leasing office first.</p>

<h2 id="how">How it works</h2>
<ol class="steps">
<li><strong>Enroll</strong> with a reporting service and share your lease details.</li>
<li><strong>Verify payments</strong> — through your landlord, bank-account connection or payment history.</li>
<li><strong>Optional back-reporting:</strong> many services can report up to 24 months of past on-time rent for a one-time fee.</li>
<li><strong>Monthly reporting</strong> continues as long as you're enrolled and paying on time.</li>
</ol>

<h2 id="who">Who benefits most</h2>
<ul>
<li><strong>Thin or no credit file:</strong> students, young renters and new arrivals to the U.S. can establish a score.</li>
<li><strong>Rebuilding credit:</strong> a steady stream of positive payments helps offset older negatives over time.</li>
<li><strong>Planning a big purchase:</strong> a car loan or mortgage in the next year or two.</li>
</ul>
<p>If you already have a long, healthy credit history, the effect is usually smaller.</p>

<h2 id="scores">Will rent reporting raise my score?</h2>
<p>It can, but it depends on the scoring model. Newer models such as FICO 9, FICO 10 and VantageScore 3.0 and 4.0 include rental history when it's reported. Older FICO versions still widely used for mortgages may ignore it. Rent reporting also only helps if you pay on time — some services report late payments too, so read the terms.</p>
<div class="callout">__ICON_info__<div><p>Experian Boost and similar tools can also count rent paid from a linked bank account, often for free. Compare what's free before paying for a service.</p></div></div>

<h2 id="costs">Typical costs</h2>
<div class="table-scroll"><table>
<tr><th>Item</th><th>Typical range</th></tr>
<tr><td>Enrollment / setup fee</td><td>$0–$50</td></tr>
<tr><td>Monthly fee</td><td>$0–$10</td></tr>
<tr><td>Back-reporting (past 12–24 months)</td><td>$0–$100 one time</td></tr>
<tr><td>Roommate / co-tenant add-on</td><td>Often discounted</td></tr>
</table></div>

<h2 id="choose">How to choose a service</h2>
<ul>
<li>Which bureaus does it report to — one, two or all three?</li>
<li>Does it report late payments, or only positive history?</li>
<li>What happens to the tradeline if you cancel?</li>
<li>Does it need landlord verification, or can it verify from your bank?</li>
<li>Is back-reporting included or extra?</li>
</ul>
<p>Pair rent reporting with the habits in our <a href="/moving-resources/credit-repair/">credit repair guide</a> and our post on <a href="/blog/how-to-build-credit-as-a-renter/">building credit as a renter</a>.</p>
""",
"faqs": [
("Does paying rent build credit?", "Not automatically. Rent only affects your credit if it's reported to a credit bureau — through your landlord, a rent reporting service or a tool like Experian Boost."),
("How fast can rent reporting improve my credit?", "A new tradeline usually appears within 30–60 days. Renters with thin files sometimes see a score generated or a noticeable bump within a couple of months; established files change more slowly."),
("Is Credit Rent Boost legitimate?", "Rent reporting is a legitimate, widely used way to add rent payments to your credit file. As with any service, review the fees, which bureaus it reports to and its cancellation terms before you enroll."),
("Can rent reporting hurt my credit?", "It can if the service reports late or missed payments. Choose a service with positive-only reporting if you're worried, and set up autopay."),
],
},
# ---------------------------------------------------------------- furniture
{
"slug": "furniture",
"name": "Furniture",
"icon": "sofa",
"short": "Furnish your rental on any budget — buy, rent or rent-to-own.",
"seo_title": "Furniture for Renters: Buy, Rent or Rent-to-Own?",
"desc": "How to furnish an apartment on a budget: when to buy new or used, when furniture rental makes sense, rent-to-own pitfalls and how to measure before you move.",
"h1": "Furniture for Renters: Furnish Your Place on Any Budget",
"lead": "You don't need to fill a whole apartment on day one. Start with the essentials, measure everything, and pick the right mix of new, used and rented pieces for how long you plan to stay.",
"tool": None,
"body": """
<h2 id="essentials">Start with the essentials</h2>
<p>Day-one furniture is about sleeping, sitting and eating. Everything else can wait for a sale.</p>
<ul>
<li><strong>Bedroom:</strong> mattress and frame, blackout curtains, a lamp</li>
<li><strong>Living:</strong> a sofa or two chairs, a small table, lighting</li>
<li><strong>Kitchen:</strong> a small dining set or counter stools, basic cookware</li>
<li><strong>Storage:</strong> a dresser or closet organizers, a shoe rack</li>
</ul>

<h2 id="options">Buy, rent or rent-to-own?</h2>
<div class="compare">
<div class="card"><h3>Buy (new or used)</h3><ul><li>Cheapest over 1+ years</li><li>Used marketplaces save 50–80%</li><li>You have to move it next time</li></ul></div>
<div class="card"><h3>Furniture rental</h3><ul><li>Monthly fee, delivery and pickup</li><li>Ideal for 3–12 month stays or relocations</li><li>Costs add up on longer stays</li></ul></div>
<div class="card"><h3>Rent-to-own</h3><ul><li>No credit check, small weekly payments</li><li>Total cost often 2–3× retail</li><li>Use only as a last resort</li></ul></div>
</div>
<div class="callout warn">__ICON_alert__<div><p>Before signing a rent-to-own agreement, add up every payment until you own the item and compare it with the retail price. A $600 sofa can easily cost $1,500+ this way.</p></div></div>

<h2 id="measure">Measure before you buy</h2>
<ol class="steps">
<li>Measure doorways, hallways, stairwells and elevator depth — not just the room.</li>
<li>Map the floor plan with painter's tape to see real walking space.</li>
<li>Note outlet, vent and window locations before placing beds and TVs.</li>
<li>Check the lease for restrictions (waterbeds, wall mounting, heavy items on balconies).</li>
</ol>

<h2 id="budget">Budget-friendly tips</h2>
<ul>
<li>Buy the mattress and sofa new (comfort and hygiene); go used for tables, dressers and shelving.</li>
<li>Shop holiday-weekend sales and floor-model clearances.</li>
<li>Check for bed bugs on any used upholstered item — look in seams, under cushions and on frames.</li>
<li>Choose modular or flat-pack pieces that are easier to move next time.</li>
<li>Add the value of new furniture to your <a href="/tools/renters-insurance-calculator/">renters insurance coverage</a>.</li>
</ul>

<h2 id="small-spaces">Making small apartments work</h2>
<p>Go vertical with tall shelving, use under-bed storage, pick furniture with legs to make rooms feel bigger, and use mirrors to bounce light. Removable wallpaper, plug-in sconces and command hooks let you personalize without risking your deposit.</p>
""",
"faqs": [
("Is renting furniture worth it?", "Usually only for short stays (under about 12 months), corporate relocations or when you need a fully furnished place quickly. For longer stays, buying new or used is almost always cheaper."),
("What furniture should I buy first for my first apartment?", "A bed, a place to sit, lighting and basic storage. Add a dining set, desk and decor once you know how you use the space."),
("How do I avoid bed bugs with used furniture?", "Inspect seams, joints and undersides with a flashlight, avoid used mattresses and upholstered pieces from unknown sources, and heat-treat or vacuum items before bringing them inside."),
],
},
# ---------------------------------------------------------------- electricity
{
"slug": "electricity",
"name": "Electricity",
"icon": "zap",
"short": "Set up power, compare plans and estimate your monthly electric bill.",
"seo_title": "Electricity for Renters: Setup & Plans (Texas Guide)",
"desc": "How to set up electricity in a new apartment, compare plans in deregulated markets like Texas, read an electricity facts label and estimate your monthly bill.",
"h1": "Electricity for Renters: Set Up Power & Pick the Right Plan",
"lead": "Nobody wants to arrive at a new apartment with the lights off. Here's how to set up electricity, compare plans if you live in a deregulated area like most of Texas, and estimate your bill before you sign.",
"tool": "electricity",
"body": """
<h2 id="who">Who provides your electricity?</h2>
<p>In most of the U.S., one regulated utility serves your address and you simply open an account with it. In <strong>deregulated markets</strong> — including most of Texas, plus parts of states like Pennsylvania, Ohio, Illinois and New York — you choose a <strong>retail electricity provider</strong> while the local utility still maintains the poles and wires.</p>
<p>In Texas, the Public Utility Commission runs <strong>PowerToChoose.org</strong>, the official site for comparing plans in deregulated areas. Some Texas cities (Austin, San Antonio and others served by municipal utilities or co-ops) are not deregulated, so you'll set up service with the city utility instead.</p>

<h2 id="setup">How to set up electricity</h2>
<ol class="steps">
<li>Confirm with your leasing office whether electricity is in your name or included in rent.</li>
<li>Find your provider (or compare providers in a deregulated area) using your exact address — some buildings have their own meter IDs (ESI ID in Texas).</li>
<li>Schedule start of service for your move-in date — 1–2 weeks ahead is ideal.</li>
<li>Be ready for a deposit if you have limited credit history; a letter of good payment history from a previous utility can sometimes waive it.</li>
<li>Schedule shut-off at your old address for the day after you move out.</li>
</ol>

<h2 id="plans">Understanding plan types</h2>
<div class="compare">
<div class="card"><h3>Fixed rate</h3><ul><li>Same energy rate for the whole term</li><li>Predictable bills</li><li>Early-termination fees apply</li></ul></div>
<div class="card"><h3>Variable rate</h3><ul><li>Rate can change monthly</li><li>No long commitment</li><li>Risky during heat waves or cold snaps</li></ul></div>
<div class="card"><h3>Prepaid</h3><ul><li>Pay ahead, usually no deposit or credit check</li><li>Good for credit challenges</li><li>Watch daily balance alerts</li></ul></div>
</div>

<h2 id="efl">Read the Electricity Facts Label (EFL)</h2>
<p>Advertised rates are often shown at exactly 1,000 kWh. Plans with bill credits can look cheap at 1,000 kWh but cost much more at 900 or 1,100 kWh. The EFL shows the average price at 500, 1,000 and 2,000 kWh, plus base charges, the delivery (TDU) charges and the contract length. Compare plans at <em>your</em> usage, not the headline number.</p>
<div class="callout">__ICON_bulb__<div><p>Ask your leasing office or the previous tenant for the unit's average monthly usage, or use the estimator below to get a realistic kWh figure for your size of home.</p></div></div>

<h2 id="save">Ways renters can lower the bill</h2>
<ul>
<li>Set the thermostat to 78°F in summer when home and higher when away; use ceiling fans.</li>
<li>Close blinds on sun-facing windows in the afternoon.</li>
<li>Replace the HVAC filter monthly in summer (ask maintenance if you're not allowed to).</li>
<li>Switch to LED bulbs and use smart plugs on entertainment centers.</li>
<li>Wash clothes in cold water and run full loads.</li>
</ul>
<p>Setting up internet, water and gas too? See our <a href="/moving-resources/utility-connections/">utility connections checklist</a>.</p>
""",
"faqs": [
("How long does it take to set up electricity?", "Often same day or next day for an existing meter, but schedule 1–2 weeks before move-in to be safe, especially at month-end."),
("Why do I need a deposit for electricity?", "Providers may require a deposit when you have little or no credit history or a past unpaid utility balance. Prepaid plans and letters of credit from a previous utility can help you avoid it."),
("What's a good electricity rate in Texas?", "It changes with the market. Compare the average price per kWh on the Electricity Facts Label at your expected usage, and include delivery charges — not just the advertised energy charge."),
("Can my landlord include electricity in my rent?", "Yes. Some properties bill a flat utility fee or use sub-metering. Ask how it's calculated and whether there's a cap."),
],
},
# ---------------------------------------------------------------- credit repair
{
"slug": "credit-repair",
"name": "Credit Repair",
"icon": "wrench",
"short": "Fix report errors and rebuild credit to qualify for better rentals.",
"seo_title": "Credit Repair for Renters: Fix Errors & Get Approved",
"desc": "A renter's guide to credit repair: get your free reports, dispute errors under the FCRA, rebuild your score and spot credit repair scams before you pay.",
"h1": "Credit Repair for Renters: Rebuild Your Credit & Get Approved",
"lead": "A low score can mean denied applications, bigger deposits or a co-signer requirement. The good news: much of credit repair is something you can do yourself, for free.",
"tool": None,
"body": """
<h2 id="why">Why your credit matters when you rent</h2>
<p>Most landlords run a credit check or a tenant-screening report. Many look for a score in the 600s or higher, no recent evictions, and no unpaid balances owed to previous landlords or utilities. A weaker report doesn't automatically mean a denial, but it can mean a larger deposit, a guarantor requirement or fewer options.</p>

<h2 id="reports">Step 1: Get your free credit reports</h2>
<p>You're entitled to free reports from Equifax, Experian and TransUnion at <strong>AnnualCreditReport.com</strong> — the only official site — and free weekly access is now permanent. Review all three: they don't always match. Also request your tenant-screening reports from screening companies, which you can get free once a year or after a denial.</p>

<h2 id="dispute">Step 2: Dispute errors</h2>
<p>Under the Fair Credit Reporting Act (FCRA) you can dispute inaccurate or unverifiable information, and the bureau generally has 30 days to investigate.</p>
<ol class="steps">
<li>List each error: wrong balances, accounts that aren't yours, duplicate collections, late payments you can prove were on time.</li>
<li>Dispute online with each bureau reporting it, and attach documentation.</li>
<li>Dispute directly with the creditor or collector as well.</li>
<li>Keep copies and dates. If an error isn't corrected, you can file a complaint with the CFPB.</li>
</ol>
<div class="callout">__ICON_info__<div><p>Accurate negative information can't be removed just because it hurts — most negatives stay up to seven years. Focus disputes on genuine errors, and focus your energy on adding positive history.</p></div></div>

<h2 id="rebuild">Step 3: Rebuild with positive history</h2>
<ul>
<li><strong>Pay every bill on time</strong> — payment history is the biggest factor in most scores. Autopay the minimums.</li>
<li><strong>Lower utilization:</strong> keep card balances under about 30% of limits, ideally under 10%.</li>
<li><strong>Add a tradeline:</strong> a secured card, credit-builder loan or <a href="/moving-resources/credit-rent-boost/">rent reporting</a>.</li>
<li><strong>Don't close old cards</strong> without a reason; age of credit helps.</li>
<li><strong>Handle collections strategically:</strong> ask for "pay for delete" in writing, and know that newer scoring models ignore paid collections.</li>
</ul>

<h2 id="companies">Should you hire a credit repair company?</h2>
<p>Legitimate credit repair companies can save you time on disputes, but they can't do anything you can't do yourself. Under the Credit Repair Organizations Act they <strong>cannot charge before services are performed</strong>, must give you a written contract and a three-day cancellation right, and can't promise to remove accurate information.</p>
<div class="callout warn">__ICON_alert__<div><p>Red flags: upfront fees, guarantees to remove "all negatives," advice to dispute accurate items or to create a "new credit identity" with an EIN — that last one is illegal.</p></div></div>

<h2 id="meanwhile">Renting while you rebuild</h2>
<ul>
<li>Offer a larger deposit or prepaid rent where state law allows.</li>
<li>Use a guarantor, co-signer or an institutional guarantor service.</li>
<li>Look for "second-chance" communities — an <a href="/moving-resources/apartment-locator/">apartment locator</a> knows which ones.</li>
<li>Bring proof of income, reference letters and a short explanation of past issues.</li>
</ul>
""",
"faqs": [
("What credit score do I need to rent an apartment?", "There's no single number, but many professionally managed properties look for 600–650 or higher. Lower scores may still be approved with a larger deposit or a guarantor."),
("How long does credit repair take?", "Disputes usually resolve in 30–45 days. Rebuilding a score through positive history typically shows results in 3–12 months."),
("Can I repair my credit myself?", "Yes. Getting your reports, disputing errors and building positive history are all free and something you can do on your own."),
("Do evictions show on credit reports?", "Eviction judgments generally no longer appear on the big three credit reports, but they can show up on tenant-screening reports, and unpaid rent sent to collections can appear on your credit report."),
],
},
# ---------------------------------------------------------------- rental insurance
{
"slug": "rental-insurance",
"name": "Rental Insurance",
"icon": "shield",
"short": "Renters insurance explained — what it covers and how much you need.",
"seo_title": "Renters Insurance Explained: Coverage & Cost",
"desc": "What renters insurance covers, what it doesn't, how much personal property and liability coverage you need, and what it costs — plus a free coverage calculator.",
"h1": "Rental Insurance: What It Covers & How Much You Need",
"lead": "Your landlord's insurance covers the building — not your stuff, and not your liability. Renters insurance usually costs less than a streaming bundle and protects both.",
"tool": "renters-insurance",
"body": """
<h2 id="what">What renters insurance covers</h2>
<div class="compare">
<div class="card"><h3>Personal property</h3><ul><li>Furniture, electronics, clothes</li><li>Covered for fire, theft, smoke, certain water damage and more</li><li>Often covered away from home too</li></ul></div>
<div class="card"><h3>Personal liability</h3><ul><li>Injuries to guests in your home</li><li>Damage you accidentally cause to others' property</li><li>Legal defense costs</li></ul></div>
<div class="card"><h3>Loss of use</h3><ul><li>Hotel and extra living costs</li><li>When a covered loss makes your home unlivable</li></ul></div>
</div>

<h2 id="not-covered">What it usually doesn't cover</h2>
<ul>
<li><strong>Floods</strong> (rising water) — that needs separate flood insurance, which is worth considering in flood-prone areas.</li>
<li><strong>Earthquakes</strong> — a separate endorsement or policy.</li>
<li><strong>Pest damage</strong> such as bed bugs or rodents.</li>
<li><strong>Your roommate's belongings</strong> unless they're named on the policy.</li>
<li><strong>High-value items above sub-limits</strong> — jewelry, watches and collectibles often have a theft limit around $1,500 unless scheduled.</li>
</ul>

<h2 id="how-much">How much coverage do you need?</h2>
<p>Add up what it would cost to replace everything you own — most renters underestimate by thousands. The calculator below helps you estimate it room by room. A few rules of thumb:</p>
<ul>
<li><strong>Personal property:</strong> $20,000–$30,000 is common for a 1–2 bedroom apartment.</li>
<li><strong>Liability:</strong> $100,000 is the typical minimum; $300,000 is inexpensive peace of mind if you have a dog, host often or have savings to protect.</li>
<li><strong>Replacement cost vs. actual cash value:</strong> replacement cost pays to buy new; actual cash value subtracts depreciation. Replacement cost costs a little more and is usually worth it.</li>
</ul>

<h2 id="cost">What renters insurance costs</h2>
<p>National averages typically run around $15–$25 per month, depending on your location, coverage amount, deductible, claims history and (in many states) credit-based insurance score. Bundling with auto insurance often brings a discount.</p>

<h2 id="landlord">When your landlord requires it</h2>
<p>Many leases require proof of renters insurance with a minimum liability amount (often $100,000) and the property listed as an "interested party" so they're notified if the policy lapses. Some properties offer a built-in plan — compare its price and coverage with buying your own.</p>

<h2 id="claim">How to make a claim go smoothly</h2>
<ol class="steps">
<li>Keep a home inventory: a video walkthrough of every room and closet, saved to the cloud.</li>
<li>Save receipts for big purchases (email receipts count).</li>
<li>After a loss, document damage before cleaning up and file a police report for theft.</li>
<li>Contact your insurer promptly and keep a log of every conversation.</li>
</ol>
""",
"faqs": [
("Is renters insurance required by law?", "No state requires it by law, but landlords can require it in the lease — and many do."),
("Does renters insurance cover my roommate?", "Not automatically. Some insurers let you add a roommate to the policy; otherwise each roommate should carry their own."),
("Does renters insurance cover my car?", "It doesn't cover the car itself, but it often covers personal belongings stolen from your car."),
("Does renters insurance cover water damage?", "It usually covers sudden and accidental water damage, such as a burst pipe or an overflowing upstairs washer, but not flooding from rising water or damage from long-term leaks."),
],
},
# ---------------------------------------------------------------- ESA letters
{
"slug": "esa-letters",
"name": "ESA Letters",
"icon": "paw",
"short": "Emotional support animal letters and your rights under fair housing law.",
"seo_title": "ESA Letters for Housing: Rules, Rights & Scams",
"desc": "What a legitimate ESA letter for housing must include, your rights under the Fair Housing Act, what landlords can and can't ask, and how to spot ESA letter scams.",
"h1": "ESA Letters: Emotional Support Animals & Your Housing Rights",
"lead": "If you have a disability and an emotional support animal helps with it, fair housing law generally lets you live with that animal — even in a no-pet building, and without pet fees. Here's how ESA letters work and how to get a legitimate one.",
"tool": None,
"body": """
<h2 id="what">What is an emotional support animal?</h2>
<p>An emotional support animal (ESA) is an animal that provides therapeutic support for a person with a mental or emotional disability. Unlike service dogs, ESAs don't need specific task training, and they aren't limited to dogs. Under the federal <strong>Fair Housing Act (FHA)</strong>, an ESA is treated as a "reasonable accommodation," not a pet.</p>

<h2 id="rights">Your housing rights</h2>
<ul>
<li>Housing providers generally must allow an ESA even with a no-pet policy.</li>
<li>They generally can't charge pet rent, pet deposits or pet fees for an ESA (you can still be charged for actual damage).</li>
<li>Breed and weight restrictions generally don't apply to ESAs.</li>
<li>A request can be denied if the specific animal poses a direct threat or would cause substantial damage, or if it creates an undue burden.</li>
</ul>
<p>Some small properties (for example, owner-occupied buildings with four or fewer units) may be exempt from the FHA. State and local laws can add protections. HUD's 2020 guidance on assistance animals is the key federal reference.</p>

<h2 id="letter">What a legitimate ESA letter includes</h2>
<p>When the disability or need isn't obvious, a housing provider may ask for reliable documentation. A strong letter:</p>
<ul>
<li>Is written by a licensed health care professional (such as a therapist, psychologist, physician or licensed clinical social worker) who has personal knowledge of your condition.</li>
<li>Is on letterhead with the provider's license type, number, state and contact information, and is dated and signed.</li>
<li>States that you have a disability and that the animal helps with symptoms or effects of it — it does <strong>not</strong> need to name your diagnosis.</li>
</ul>
<div class="callout warn">__ICON_alert__<div><p><strong>ESA "registrations," ID cards and vests have no legal standing.</strong> HUD has specifically said certificates sold online without a genuine therapeutic relationship are not, by themselves, reliable documentation. A growing number of states also penalize misrepresenting an animal as an assistance animal.</p></div></div>

<h2 id="how">How to get an ESA letter the right way</h2>
<ol class="steps">
<li>Talk to a licensed provider you already see, or establish care with one (in person or via a reputable telehealth practice licensed in your state).</li>
<li>Expect a real evaluation, not an instant approval after a quiz.</li>
<li>Submit the letter to your housing provider with a written reasonable-accommodation request. Keep copies.</li>
<li>Renew if your provider or landlord asks for current documentation (many letters are updated annually).</li>
</ol>

<h2 id="landlord">What landlords can and can't ask</h2>
<div class="table-scroll"><table>
<tr><th>Landlords may</th><th>Landlords generally may not</th></tr>
<tr><td>Ask for reliable documentation when the disability isn't obvious</td><td>Ask for your diagnosis or medical records</td></tr>
<tr><td>Hold you responsible for damage the animal causes</td><td>Charge pet deposits, pet rent or pet fees for an ESA</td></tr>
<tr><td>Require the animal to be housebroken and under control</td><td>Require a specific registration or certificate</td></tr>
<tr><td>Deny a specific animal that's a direct threat</td><td>Apply breed or weight limits by default</td></tr>
</table></div>

<h2 id="responsible">Being a responsible ESA owner</h2>
<p>Keep vaccinations and local licensing current, clean up after your animal, and address noise complaints quickly. ESAs don't have public-access rights the way trained service dogs do, so they generally aren't allowed in restaurants or stores. For pets that aren't ESAs, read our guide to <a href="/blog/moving-with-pets-renter-guide/">moving with pets</a>.</p>
""",
"faqs": [
("Can a landlord deny an emotional support animal?", "Yes, in limited cases: if the specific animal poses a direct threat or would cause substantial damage that can't be reduced, if the request is an undue burden, or if the property is exempt from the Fair Housing Act."),
("Do I have to pay a pet deposit for an ESA?", "Generally no. Landlords covered by the Fair Housing Act generally can't charge pet deposits, fees or pet rent for an assistance animal, but you can be charged for actual damage."),
("Are online ESA letters legitimate?", "Some are, if they come from a licensed professional in your state after a genuine evaluation. Instant letters, registrations and ID cards sold online are not reliable documentation on their own."),
("Does an ESA letter expire?", "There's no federal expiration, but many landlords ask for documentation that's reasonably current, and many providers re-evaluate annually."),
],
},
# ---------------------------------------------------------------- utility connections
{
"slug": "utility-connections",
"name": "Utility Connections",
"icon": "plug",
"short": "Your checklist for setting up power, water, gas, internet and more.",
"seo_title": "Utility Connections Checklist for Renters",
"desc": "A step-by-step checklist for setting up electricity, water, gas, internet, trash and mail when you move into a rental — with timelines and money-saving tips.",
"h1": "Utility Connections: Set Up Every Service Before You Move",
"lead": "Arriving to working lights, water and Wi-Fi is the difference between a stressful first night and a good one. Use this checklist to get every utility connected on time.",
"tool": "checklist",
"body": """
<h2 id="which">Which utilities are you responsible for?</h2>
<p>Check your lease. Many apartments include water, sewer and trash in rent or bill them as a flat fee, while you set up electricity and internet yourself. Houses usually put everything in the tenant's name. Ask the leasing office for a list of providers for your address.</p>

<h2 id="checklist">The utility setup checklist</h2>
<div class="table-scroll"><table>
<tr><th>Utility</th><th>When to set up</th><th>Notes</th></tr>
<tr><td>Electricity</td><td>1–2 weeks before</td><td>Compare plans in deregulated areas. See <a href="/moving-resources/electricity/">electricity</a>.</td></tr>
<tr><td>Internet / Wi-Fi</td><td>2–3 weeks before</td><td>Installation slots fill quickly; ask about self-install kits.</td></tr>
<tr><td>Gas</td><td>1–2 weeks before</td><td>May need someone home to relight pilot lights.</td></tr>
<tr><td>Water / sewer</td><td>1–2 weeks before</td><td>Often city-run; a deposit may apply.</td></tr>
<tr><td>Trash / recycling</td><td>1 week before</td><td>Learn pickup days and bulk-item rules.</td></tr>
<tr><td>Renters insurance</td><td>Before move-in</td><td>Many leases require proof at signing. See <a href="/moving-resources/rental-insurance/">rental insurance</a>.</td></tr>
<tr><td>Mail forwarding</td><td>2 weeks before</td><td>USPS change of address online.</td></tr>
</table></div>

<h2 id="internet">Choosing internet</h2>
<ul>
<li><strong>Fiber</strong> gives the fastest, most reliable speeds where available.</li>
<li><strong>Cable</strong> is widely available and fast, though upload speeds are lower.</li>
<li><strong>5G home internet</strong> needs no installation and often has no contract — good for renters who move often.</li>
<li>Most households are fine with 100–300 Mbps; heavy streaming, gaming or working from home may justify more.</li>
<li>Buying your own compatible modem/router can save a monthly rental fee.</li>
</ul>

<h2 id="deposits">Avoiding utility deposits</h2>
<p>Utilities often ask for a deposit when you have a thin credit file. Ask your current provider for a letter of credit showing on-time payments, choose a prepaid plan, or ask about autopay waivers. Deposits are generally refunded after a period of on-time payments or when you close the account.</p>

<h2 id="moving-out">Don't forget your old address</h2>
<ul>
<li>Schedule shut-off for the day <em>after</em> you move out so you have power for cleaning.</li>
<li>Return internet equipment to avoid fees, and take photos of the return receipt.</li>
<li>Give each provider your forwarding address for final bills and deposit refunds.</li>
</ul>
<p>Use the interactive timeline below to schedule utilities alongside every other moving task.</p>
""",
"faqs": [
("How far in advance should I set up utilities?", "About two to three weeks before move-in for internet and one to two weeks for electricity, gas and water."),
("What utilities do renters usually pay?", "Most renters pay electricity and internet; many also pay gas, water, sewer and trash depending on the lease. Check the lease's utility section."),
("Can I set up utilities before I sign a lease?", "Usually you need the exact unit address and move-in date, so set them up right after signing."),
],
},
]
