"""Markup for the interactive tools (logic lives in assets/js/tools.js) and the tool page copy."""
from icons import icon

SIZE_OPTS = [("studio", "Studio"), ("1br", "1 BR"), ("2br", "2 BR"), ("3br", "3 BR"), ("4br", "4+ BR")]


def seg(name, opts, checked):
    return '<div class="seg" role="radiogroup">' + "".join(
        f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == checked else ""}><span>{l}</span></label>'
        for v, l in opts) + "</div>"


def field(label, inner, out=None, hint=None, lbl_for=None):
    o = f' <output data-out="{out}"></output>' if out else ""
    h = f'<span class="hint">{hint}</span>' if hint else ""
    tag = f'<label for="{lbl_for}">' if lbl_for else '<span class="lbl">'
    end = "</label>" if lbl_for else "</span>"
    return f'<div class="field">{tag}{label}{o}{end}{inner}{h}</div>'


def chk(name, label, checked=False):
    return f'<label class="check"><input type="checkbox" name="{name}"{" checked" if checked else ""}> {label}</label>'


def rows(pairs):
    return '<div class="result-rows">' + "".join(f'<div><span>{a}</span><b data-out="{b}">—</b></div>' for a, b in pairs) + "</div>"


def shell(key, ic, title, sub, inp, outp, full=False, uid=""):
    return (f'<form class="tool{" full" if full else ""}" data-tool="{key}" id="tool-{key}{uid}" novalidate>'
            f'<div class="tool-head"><span class="ico">{icon(ic)}</span><div><h3>{title}</h3><small>{sub}</small></div></div>'
            f'<div class="tool-body"><div class="tool-in">{inp}</div><div class="tool-out" aria-live="polite">{outp}</div></div></form>')


def t_affordability(u):
    inp = (field("Annual gross income", f'<div class="money"><input id="inc{u}" type="number" name="income" value="60000" min="0" step="1000" inputmode="numeric"></div>', lbl_for=f"inc{u}", hint="Before taxes, all earners on the lease")
           + field("Monthly debt payments", f'<div class="money"><input id="debt{u}" type="number" name="debt" value="350" min="0" step="25" inputmode="numeric"></div>', lbl_for=f"debt{u}", hint="Car, student loans, card minimums")
           + field("Test a rent amount", f'<input id="rent{u}" type="range" name="rent" min="300" max="6000" step="25" value="1450">', out="rentv", lbl_for=f"rent{u}"))
    outp = ('<div class="result-label">Recommended max rent</div><div class="result-big" data-out="max">—</div>'
            '<div class="meter"><i></i></div><div>That rent is <b data-out="pct">—</b> of gross monthly income.</div>'
            '<div class="verdict"></div>'
            + rows([("30% of gross income", "r30"), ("40× rule (income ÷ 40)", "r40"), ("36% debt-to-income room", "dti"), ("Gross monthly income", "mo"), ("Passes landlords' 3× income test?", "qual")])
            + '<p class="tool-note">Recommended max is the lowest of the three rules. Guidelines only — not financial advice.</p>')
    return shell("affordability", "calculator", "Rent Affordability Calculator", "Four rules, one answer", inp, outp, uid=u)


def t_moving_cost(u):
    inp = (field("Home size", seg("size", SIZE_OPTS, "2br"))
           + field("Distance", f'<input id="mi{u}" type="range" name="miles" min="5" max="3000" step="5" value="25">', out="milesv", lbl_for=f"mi{u}")
           + field("How are you moving?", seg("method", [("diy", "DIY truck"), ("movers", "Movers"), ("container", "Container")], "movers"))
           + '<div class="checks">' + chk("pack", "Professional packing") + chk("stairs", "Stairs / no elevator") + chk("heavy", "Piano, safe or very heavy items") + chk("storage", "One month of storage") + chk("peak", "Peak season (May–Sept) or month-end", True) + "</div>")
    outp = ('<div class="result-label" data-out="dist">Estimated cost</div><div class="result-big"><span data-out="low">—</span>–<span data-out="high">—</span></div>'
            '<p class="note">Estimated range for your selected method.</p>'
            '<div class="bars">'
            + "".join(f'<div class="bar-row"><span>{l}</span><div class="track"><i data-bar="{k}"></i></div><b data-out="{k}">—</b></div>' for k, l in [("diy", "DIY truck"), ("movers", "Movers"), ("container", "Container")])
            + '</div><p class="tool-note">Planning estimates based on typical U.S. pricing, including basic supplies. Always get at least three written quotes.</p>')
    return shell("moving-cost", "truck", "Moving Cost Calculator", "Compare DIY, movers and containers", inp, outp, uid=u)


CHECKLIST = [
    (-56, "8 weeks before", [("Set your moving budget", "/tools/moving-cost-calculator/"), ("Start decluttering: sell, donate, toss", None), ("Research movers or truck rentals", "/moving-resources/movers/"), ("Give notice to your current landlord (check lease)", None)]),
    (-42, "6 weeks before", [("Book movers, truck or container", "/moving-resources/moving-truck-rentals/"), ("Order boxes and packing supplies", "/tools/packing-calculator/"), ("Request school and medical records", None)]),
    (-28, "4 weeks before", [("Set up internet installation", "/moving-resources/utility-connections/"), ("Buy or update renters insurance", "/moving-resources/rental-insurance/"), ("Start packing rooms you use least", None), ("Book move-out cleaning", "/moving-resources/maid-services/")]),
    (-14, "2 weeks before", [("Schedule electricity, gas and water start/stop", "/moving-resources/electricity/"), ("Forward mail with USPS", None), ("Update address with bank, employer and subscriptions", None), ("Reserve elevator / loading zone", None)]),
    (-7, "1 week before", [("Confirm movers or truck pickup", None), ("Pack an 'open first' essentials box", None), ("Refill prescriptions", None), ("Defrost freezer and use up food", None)]),
    (-2, "2–3 days before", [("Finish packing, label every box", None), ("Withdraw cash for tips", None), ("Charge devices, gather chargers", None)]),
    (0, "Moving day", [("Do a final walkthrough with photos", "/tools/move-in-inspection-checklist/"), ("Hand in keys and leave forwarding address", None), ("Inspect and record the new place before unloading", None)]),
    (7, "First week after", [("Unpack kitchen and bedrooms first", None), ("Update driver's license and voter registration", None), ("Set up rent reporting to build credit", "/moving-resources/credit-rent-boost/"), ("Follow up on your security deposit", "/blog/how-to-get-your-security-deposit-back/")]),
]


def t_checklist(u):
    groups = ""
    n = 0
    for off, label, items in CHECKLIST:
        lis = ""
        for text, link in items:
            n += 1
            extra = f' <a href="{link}">Guide</a>' if link else ""
            lis += f'<label class="tl-item"><input type="checkbox" value="t{n}"><span>{text}{extra}</span></label>'
        groups += f'<div class="tl-group" data-offset="{off}"><h4>{label} <span class="when"></span></h4>{lis}</div>'
    inp = (field("Your moving date", f'<input id="md{u}" type="date" name="movedate">', lbl_for=f"md{u}")
           + '<div><div class="result-label">Progress</div><div class="result-big" data-out="done">—</div><div class="meter"><i></i></div><b data-out="days"></b></div>'
           + '<div class="tool-actions"><button type="button" class="btn sm" data-act="print">' + icon("printer") + ' Print</button><button type="button" class="btn sm ghost" data-act="reset">' + icon("refresh") + ' Reset</button></div>'
           + '<p class="tool-note">Your checks are saved in this browser only.</p>')
    outp = f'<div class="timeline">{groups}</div>'
    return shell("checklist", "clipboard", "Interactive Moving Checklist", "Dated to your move — progress saves automatically", inp, outp, uid=u)


def t_renters_insurance(u):
    cats = [("electronics", "Electronics & computers", 20000), ("furniture", "Furniture & décor", 30000), ("clothing", "Clothing, shoes & bags", 20000), ("kitchen", "Kitchen & appliances", 10000), ("jewelry", "Jewelry & valuables", 15000), ("other", "Sports, hobby & everything else", 15000)]
    sl = "".join(field(l, f'<input id="{k}{u}" type="range" name="{k}" min="0" max="{m}" step="250" value="1000">', out=k, lbl_for=f"{k}{u}") for k, l, m in cats)
    inp = (field("Home size (sets typical values)", seg("size", SIZE_OPTS, "1br")) + sl
           + field("Deductible", seg("ded", [("500", "$500"), ("1000", "$1,000")], "500"))
           + '<div class="checks">' + chk("rc", "Replacement-cost coverage (recommended)", True) + chk("risk", "I have a dog, host often or have significant savings") + "</div>")
    outp = ('<div class="result-label">Suggested personal property coverage</div><div class="result-big" data-out="cover">—</div>'
            + rows([("Estimated value of belongings", "total"), ("Suggested liability coverage", "liab"), ("Estimated premium", "prem")])
            + '<div class="callout" style="margin-top:18px">' + icon("info") + '<p data-out="jnote"></p></div>'
            + '<p class="tool-note">Premiums vary widely by state, insurer and claims history. Get quotes from several insurers.</p>')
    return shell("renters-insurance", "shield", "Renters Insurance Coverage Calculator", "How much coverage do you need?", inp, outp, uid=u)


def t_rent_split(u):
    tpl = ('<template><div class="rm-row"><input data-f="name" aria-label="Name"><input data-f="size" type="number" min="0" aria-label="Bedroom size in square feet">'
           '<input data-f="inc" type="number" min="0" step="1000" aria-label="Annual income"><button type="button" aria-label="Remove roommate">' + icon("x") + '</button></div></template>')
    inp = (f'<div class="form-grid">' + field("Monthly rent", f'<div class="money"><input id="sr{u}" type="number" name="rent" value="2400" min="0" step="25"></div>', lbl_for=f"sr{u}")
           + field("Shared utilities / mo", f'<div class="money"><input id="su{u}" type="number" name="util" value="220" min="0" step="10"></div>', lbl_for=f"su{u}") + "</div>"
           + field("Split method", seg("method", [("equal", "Equal"), ("size", "Room size"), ("income", "Income")], "size"))
           + field("Common-area share (room-size method)", f'<input id="cs{u}" type="range" name="common" min="0" max="80" step="5" value="40">', out="commonv", lbl_for=f"cs{u}")
           + '<div class="rm-head"><span>Name</span><span>Room sq ft</span><span>Income/yr</span><span></span></div><div class="roommates"></div>' + tpl
           + '<button type="button" class="btn sm ghost" data-act="add">' + icon("plus") + ' Add roommate</button>')
    outp = ('<div class="result-label">Total monthly housing cost</div><div class="result-big" data-out="total">—</div>'
            '<p class="note">An equal split would be <b data-out="each">—</b> each.</p><div class="bars"></div>'
            '<p class="tool-note">Utilities are split equally; rent is split by the method you choose.</p>')
    return shell("rent-split", "split", "Rent Split Calculator", "Fair splits for roommates", inp, outp, uid=u)


def t_packing(u):
    inp = (field("Home size", seg("size", SIZE_OPTS, "2br"))
           + field("How much stuff?", seg("style", [("light", "Minimalist"), ("avg", "Average"), ("heavy", "Lots of stuff")], "avg"))
           + field("People in the home", f'<input id="pp{u}" type="range" name="people" min="1" max="6" step="1" value="2">', out="peoplev", lbl_for=f"pp{u}"))
    outp = ('<div class="result-label">Boxes you\'ll need</div><div class="result-big" data-out="total">—</div>'
            + rows([("Small boxes (books, tools, pantry)", "bS"), ("Medium boxes (kitchen, décor, toys)", "bM"), ("Large boxes (linens, pillows, lampshades)", "bL"), ("Wardrobe boxes", "bW"), ("Dish packs", "bD"), ("Packing tape", "tape"), ("Packing paper", "paper"), ("Bubble wrap", "wrap"), ("Estimated supply cost", "cost")])
            + '<p class="tool-note">Free boxes from liquor and grocery stores can cut the cost a lot.</p>')
    return shell("packing", "box", "Packing Supplies Calculator", "Boxes, tape and paper — sorted", inp, outp, uid=u)


def t_truck(u):
    inp = (field("Home size", seg("size", SIZE_OPTS, "2br"))
           + '<div class="checks">' + chk("appl", "Moving a washer, dryer or fridge") + chk("garage", "Garage, patio or storage unit too") + chk("lots", "More stuff than average") + chk("minimal", "Minimalist / partly furnished") + "</div>")
    vis = "".join(f'<div style="height:{h}%">{l}</div>' for l, h in [("Van", 30), ("10'", 45), ("15'", 62), ("20'", 78), ("26'", 100)])
    outp = ('<div class="result-label">Recommended</div><div class="result-big" data-out="truck">—</div>'
            f'<div class="truck-vis" aria-hidden="true">{vis}</div>'
            + rows([("Estimated load", "cu"), ("Trips", "trips")])
            + '<p class="tool-note">Includes about 10% extra room for awkward items. Capacities vary by rental company.</p>')
    return shell("truck-size", "truck", "Moving Truck Size Calculator", "Van, 10, 15, 20 or 26 ft?", inp, outp, uid=u)


ROOMS = [
    ("Living room", ["Walls & paint", "Flooring / carpet", "Windows & blinds", "Doors & locks", "Light fixtures & outlets", "Smoke detector"]),
    ("Kitchen", ["Countertops", "Cabinets & drawers", "Sink & faucet", "Stove / oven", "Refrigerator", "Dishwasher", "Microwave", "Flooring"]),
    ("Bedroom(s)", ["Walls & paint", "Flooring / carpet", "Closet & doors", "Windows & blinds", "Outlets & lights"]),
    ("Bathroom(s)", ["Toilet", "Tub / shower & grout", "Sink & vanity", "Mirror & cabinet", "Exhaust fan", "Flooring"]),
    ("Entry, halls & laundry", ["Front door & lock", "Washer / dryer hookups", "HVAC & thermostat", "Water heater area"]),
    ("Exterior & patio", ["Patio / balcony", "Screens", "Parking / garage"]),
]


def t_inspection(u):
    rooms = ""
    for ri, (room, items) in enumerate(ROOMS):
        rws = ""
        for ii, it in enumerate(items):
            k = f"r{ri}i{ii}"
            opts = "".join(f'<label><input type="radio" name="{k}{u}" value="{v}" data-k="{k}"><span>{l}</span></label>' for v, l in [("good", "Good"), ("fair", "Fair"), ("damaged", "Damaged")])
            rws += f'<div class="inspect-row"><span class="lbl-t">{it}</span><div class="seg">{opts}</div><input type="text" placeholder="Notes (e.g. scratch near window)" data-k="{k}n" aria-label="{it} notes"></div>'
        rooms += f'<details class="inspect-room"{" open" if ri == 0 else ""}><summary><b>{room}</b><span class="cnt note"></span></summary><div class="items">{rws}</div></details>'
    inp = ('<div class="form-grid">' + field("Property address", f'<input id="ad{u}" type="text" name="addr" placeholder="123 Main St, Apt 4">', lbl_for=f"ad{u}")
           + field("Inspection date", f'<input id="id{u}" type="date" name="idate">', lbl_for=f"id{u}") + "</div>"
           + '<div class="result-rows"><div><span>Items checked</span><b data-out="rated">—</b></div><div><span>Fair condition</span><b data-out="fair">—</b></div><div><span>Damaged</span><b data-out="issues">—</b></div></div>'
           + '<div class="tool-actions"><button type="button" class="btn sm" data-act="copy">' + icon("copy") + ' Copy report</button><button type="button" class="btn sm ghost" data-act="print">' + icon("printer") + ' Print</button><button type="button" class="btn sm ghost" data-act="reset">' + icon("refresh") + ' Reset</button></div>'
           + '<p class="tool-note">Saved in this browser only. Pair it with dated photos and email the report to your landlord.</p>')
    return shell("inspection", "clipboard", "Move-In / Move-Out Inspection Checklist", "Protect your security deposit", inp, rooms, uid=u)


def t_electricity(u):
    inp = (field("Home size", seg("size", SIZE_OPTS, "1br"))
           + field("People", f'<input id="ep{u}" type="range" name="people" min="1" max="6" value="2">', out="peoplev", lbl_for=f"ep{u}")
           + field("Season", seg("season", [("mild", "Spring / fall"), ("summer", "Summer"), ("winter", "Winter")], "summer"))
           + field("Energy rate (¢ per kWh, all-in)", f'<input id="er{u}" type="range" name="rate" min="8" max="30" step="0.5" value="15">', out="ratev", lbl_for=f"er{u}")
           + field("Monthly base / customer charge", f'<input id="eb{u}" type="range" name="base" min="0" max="15" step="0.5" value="4.95">', out="basev", lbl_for=f"eb{u}")
           + '<div class="checks">' + chk("wfh", "Someone works from home") + chk("ev", "I charge an electric vehicle at home") + "</div>")
    outp = ('<div class="result-label">Estimated monthly bill</div><div class="result-big" data-out="bill">—</div>'
            + rows([("Estimated usage", "kwh"), ("Estimated yearly cost", "year")])
            + '<div class="result-label" style="margin-top:20px">Compare rates</div><div class="bars">'
            + "".join(f'<div class="bar-row"><span data-out="{k}r">—</span><div class="track"><i data-bar="{k}"></i></div><b data-out="{k}">—</b></div>' for k in ("lo", "mid", "hi"))
            + '</div><p class="tool-note">Usage estimates are typical averages; your unit\'s insulation, appliances and thermostat settings matter most.</p>')
    return shell("electricity", "zap", "Electricity Bill Estimator", "Estimate usage and compare rates", inp, outp, uid=u)


RENDER = {
    "affordability": t_affordability, "moving-cost": t_moving_cost, "checklist": t_checklist,
    "renters-insurance": t_renters_insurance, "rent-split": t_rent_split, "packing": t_packing,
    "truck-size": t_truck, "inspection": t_inspection, "electricity": t_electricity,
}


def render(key, uid=""):
    return RENDER[key](uid)


# slug, key, name, icon, short, seo title, description, intro, how-to (HTML), faqs
TOOLS = [
("rent-affordability-calculator", "affordability", "Rent Affordability Calculator", "calculator",
 "See how much rent you can afford using the 30%, 3×, 40× and debt-to-income rules.",
 "Rent Affordability Calculator: How Much Rent Can I Afford?",
 "Free rent affordability calculator. Enter your income and debts to see how much rent you can afford using the 30% rule, 40× rule, 3× income test and debt-to-income.",
 "Enter your income and debts to see a recommended maximum rent — then test any rent to see if it's comfortable, a stretch or rent-burdened.",
 "<p>The calculator checks three common guidelines and recommends the <strong>lowest</strong> of them so you have breathing room: 30% of gross monthly income, annual income divided by 40, and the room left under a 36% debt-to-income ceiling after your monthly debt payments. It also tells you whether you pass the 3× income test many landlords use.</p><p>Read more in <a href=\"/blog/how-much-rent-can-i-afford/\">How much rent can I afford?</a></p>",
 [("Is the 30% rule realistic?", "It's a guideline. In high-cost cities many renters spend more; if you do, keep other fixed costs and debt low and build an emergency fund."),
  ("Should I use gross or net income?", "Landlords and the 30% rule use gross (pre-tax) income. For your personal budget, also check rent against take-home pay using the 50/30/20 rule.")]),
("moving-cost-calculator", "moving-cost", "Moving Cost Calculator", "truck",
 "Estimate and compare the cost of a DIY truck, professional movers or a moving container.",
 "Moving Cost Calculator: Compare DIY, Movers & Containers",
 "Free moving cost calculator for renters. Estimate a local or long-distance move and compare DIY truck rental, professional movers and moving containers side by side.",
 "Pick your home size, distance and extras to see an estimated range — and how DIY, movers and containers compare for your move.",
 "<p>Local moves (under about 50 miles) are estimated by crew hours or truck mileage; long-distance moves by weight and distance. Packing, stairs, heavy items, storage and peak-season timing are added on top. For real numbers, get at least three written quotes — see our <a href=\"/moving-resources/movers/\">guide to hiring movers</a>.</p>",
 [("What's the cheapest way to move?", "Usually a DIY truck rental for local moves. For long distances, a moving container can be competitive once you include fuel, lodging and time."),
  ("When is moving cheapest?", "Mid-month, mid-week, and outside the May–September peak season.")]),
("moving-checklist", "checklist", "Interactive Moving Checklist", "clipboard",
 "A dated, printable moving timeline that saves your progress as you check off tasks.",
 "Interactive Moving Checklist & Timeline (Free, Printable)",
 "Free interactive moving checklist. Enter your moving date to get a dated timeline from 8 weeks before to the week after — progress saves in your browser.",
 "Enter your moving date and every task gets a due date. Check things off as you go — your progress is saved in this browser.",
 "<p>Overdue groups turn red so you know what to catch up on. Each task links to the matching Connected Renter guide. Use <strong>Print</strong> for a paper copy for the fridge.</p>",
 [("How early should I start planning a move?", "About eight weeks ahead for most moves; earlier for long-distance or summer moves."),
  ("Is my checklist saved?", "Yes, in your browser's local storage on this device. Clearing browser data will reset it.")]),
("renters-insurance-calculator", "renters-insurance", "Renters Insurance Calculator", "shield",
 "Estimate how much personal property and liability coverage you need — and the premium.",
 "Renters Insurance Calculator: How Much Coverage Do I Need?",
 "Free renters insurance calculator. Estimate the value of your belongings by category, get a suggested coverage amount, liability limit and premium range.",
 "Adjust the value of your belongings by category to see a suggested coverage amount, liability limit and estimated monthly premium.",
 "<p>Start with your home size to load typical values, then adjust each category. Coverage is rounded up to the next $5,000. Learn what's covered in our <a href=\"/moving-resources/rental-insurance/\">rental insurance guide</a>.</p>",
 [("How much renters insurance do I need?", "Enough personal property coverage to replace everything you own, plus at least $100,000 of liability. Many 1–2 bedroom renters land around $20,000–$30,000 of property coverage."),
  ("Is replacement cost worth it?", "Usually. It pays to replace items new, while actual cash value subtracts depreciation, which can leave you far short after a loss.")]),
("rent-split-calculator", "rent-split", "Rent Split Calculator", "split",
 "Split rent fairly between roommates by room size, income or evenly.",
 "Rent Split Calculator: Split Rent Fairly With Roommates",
 "Free rent split calculator for roommates. Split rent equally, by bedroom size with shared common areas, or by income — plus utilities.",
 "Add each roommate's bedroom size and income, then compare an equal split, a room-size split and an income-based split.",
 "<p>The room-size method shares the common-area portion of rent equally and splits the rest by private square footage — adjust the common-area share with the slider. Read <a href=\"/blog/renting-with-roommates-guide/\">renting with roommates</a> for tips on writing a roommate agreement.</p>",
 [("What's the fairest way to split rent?", "When rooms differ, splitting by room size (with common space shared equally) is usually seen as fairest. Couples often prefer splitting by income."),
  ("Should a private bathroom cost more?", "Commonly, yes. Add its square footage to that roommate's room size.")]),
("packing-calculator", "packing", "Packing Calculator", "box",
 "Find out how many boxes, rolls of tape and packing paper you need.",
 "Packing Calculator: How Many Moving Boxes Do I Need?",
 "Free packing calculator. Find out how many small, medium, large, wardrobe and dish-pack boxes you need, plus tape, paper and bubble wrap.",
 "Choose your home size and how much stuff you have to get a full packing-supply list and cost estimate.",
 "<p>Estimates assume average household contents. Buy a few extra small boxes — they're the ones everyone runs out of. Ready to go? Follow our <a href=\"/10-steps-for-a-successful-diy-move/\">10 steps for a successful DIY move</a>.</p>",
 [("How many boxes for a 1-bedroom apartment?", "Typically around 25–35 boxes in mixed sizes, depending on how much you own."),
  ("Where can I get free moving boxes?", "Grocery and liquor stores, office recycling, local buy-nothing groups and online marketplaces.")]),
("moving-truck-size-calculator", "truck-size", "Moving Truck Size Calculator", "truck",
 "Find the right rental truck size for your home — van, 10, 15, 20 or 26 ft.",
 "Moving Truck Size Calculator: What Size Truck Do I Need?",
 "Free moving truck size calculator. Find out whether you need a cargo van or a 10, 15, 20 or 26 ft truck for your apartment or house.",
 "Select your home size and extras to see which truck fits — with room to spare.",
 "<p>The estimate converts your home into an approximate load in cubic feet and picks the smallest truck with about 10% to spare. See costs and driving tips in <a href=\"/moving-resources/moving-truck-rentals/\">moving truck rentals</a>.</p>",
 [("Is it better to rent a bigger truck?", "If you're between sizes, yes. A second trip costs more time, fuel and mileage than the difference in rental price."),
  ("How much fits in a 15 ft truck?", "Roughly a one- to two-bedroom apartment.")]),
("move-in-inspection-checklist", "inspection", "Move-In Inspection Checklist", "clipboard",
 "Room-by-room condition report you can save, print and send to your landlord.",
 "Move-In Inspection Checklist: Protect Your Security Deposit",
 "Free interactive move-in / move-out inspection checklist. Rate every room, add notes, then print or copy a report to send your landlord.",
 "Walk through each room, rate the condition and add notes. Copy or print the report and email it to your landlord with photos.",
 "<p>Use it at move-in to record existing damage, and again at move-out to show the unit's condition. Learn more in <a href=\"/blog/how-to-get-your-security-deposit-back/\">how to get your security deposit back</a>.</p>",
 [("When should I do a move-in inspection?", "Before you move furniture in — ideally on the day you get the keys."),
  ("Should I send the report to my landlord?", "Yes. Email it with your photos so there's a dated record, and keep a copy until your deposit is returned.")]),
("electricity-bill-calculator", "electricity", "Electricity Bill Calculator", "zap",
 "Estimate your apartment's electric usage and compare rates before you choose a plan.",
 "Electricity Bill Calculator for Apartments (kWh & Rate Compare)",
 "Free electricity bill calculator for renters. Estimate monthly kWh for your apartment size and season, then compare what different rates would cost.",
 "Estimate your monthly usage by home size, household and season, then see what different all-in rates would cost.",
 "<p>Use an all-in rate (energy plus delivery charges) for the most realistic estimate. In deregulated areas like most of Texas, compare plans using the Electricity Facts Label at your expected usage. See our <a href=\"/moving-resources/electricity/\">electricity guide</a>.</p>",
 [("How much electricity does an apartment use?", "Many one-bedroom apartments use roughly 500–900 kWh a month, more in hot summers with heavy A/C use."),
  ("What's an all-in rate?", "The total cost per kWh including energy, delivery and fees — divide a bill's total by its kWh to find yours.")]),
]
