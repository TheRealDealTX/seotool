"""Interactive tools: server-rendered form markup + page copy.

The behavior lives in src/js/site.js (one handler per data-tool value). Each
tool works as a plain HTML form, so it renders fine before JS loads.
"""

import html
import json

from products import PRODUCTS

esc = html.escape


def _radios(name, legend, options, checked=0):
    opts = "".join(
        f'<label class="chip"><input type="radio" name="{name}" value="{v}"{" checked" if i == checked else ""}><span>{esc(t)}</span></label>'
        for i, (v, t) in enumerate(options))
    return f'<fieldset><legend>{esc(legend)}</legend><div class="chips">{opts}</div></fieldset>'


def _checks(name, legend, options):
    opts = "".join(
        f'<label class="check"><input type="checkbox" name="{name}" value="{v}"><span>{esc(t)}</span></label>'
        for v, t in options)
    return f'<fieldset><legend>{esc(legend)}</legend><div class="checks">{opts}</div></fieldset>'


FORMS = {
    "schedule": lambda: "".join([
        _radios("ears", "1. What are your dog's ears like?", [
            ("upright", "Upright / pricked"), ("semi", "Semi-folded"), ("floppy", "Floppy / long"),
            ("hairy", "Hairy ear canals (Poodle, Shih Tzu)")]),
        _radios("water", "2. How often does your dog swim or get bathed?", [
            ("rare", "Rarely"), ("monthly", "About monthly"), ("weekly", "Weekly or more")]),
        _radios("allergy", "3. Does your dog have allergies (itchy paws, skin, seasonal flare-ups)?", [
            ("none", "No"), ("seasonal", "Seasonal"), ("chronic", "Year-round")]),
        _radios("wax", "4. What do the ears look like right now?", [
            ("clean", "Pale pink, little wax"), ("some", "Some brown wax"), ("heavy", "Lots of wax or a smell"),
            ("sore", "Red, sore or discharge")]),
        _radios("history", "5. Ear infections in the last year?", [
            ("0", "None"), ("1", "One"), ("2", "Two or more")]),
    ]),
    "symptoms": lambda: "".join([
        _checks("s", "Tick everything you have noticed in the last few days:", [
            ("scratch", "Scratching at the ear or rubbing it on the floor"),
            ("shake", "Frequent head shaking"),
            ("wax", "Light brown wax, no smell"),
            ("odor", "Bad, yeasty or sour smell"),
            ("dark", "Dark brown or black discharge"),
            ("coffee", "Dry, crumbly 'coffee grounds' debris"),
            ("pus", "Yellow or green discharge (pus)"),
            ("red", "Redness inside the ear flap or canal"),
            ("swelcanal", "Swollen, narrowed ear canal"),
            ("pain", "Yelps, flinches or won't let you touch the ear"),
            ("flap", "Puffy, fluid-filled ear flap (like a pillow)"),
            ("blood", "Bleeding from the ear"),
            ("tilt", "Head tilt, circling or loss of balance"),
            ("eyes", "Flicking eyes, drooping face or eyelid on one side"),
            ("deaf", "Sudden hearing loss / not responding"),
            ("swim", "Symptoms started after swimming or a bath"),
            ("outdoor", "Recent walk through tall grass or foxtails"),
        ]),
    ]),
    "finder": lambda: "".join([
        _radios("goal", "1. What do you mainly need the cleaner for?", [
            ("routine", "Routine cleaning"), ("smelly", "Smelly, waxy ears"), ("itchy", "Itchy, allergy-prone ears"),
            ("sensitive", "Sensitive or sore ears"), ("swim", "Drying after swims and baths")]),
        _radios("format", "2. Liquid flush or wipes?", [
            ("liquid", "Liquid flush"), ("wipes", "Wipes"), ("either", "Either")]),
        _radios("budget", "3. Budget?", [("value", "Best value"), ("mid", "Middle"), ("any", "Whatever works best")], 2),
        _radios("natural", "4. Prefer plant-based or non-medicated?", [("no", "No preference"), ("yes", "Yes, keep it gentle/natural")]),
        _radios("size", "5. Dog size?", [("small", "Under 25 lb"), ("medium", "25-60 lb"), ("large", "Over 60 lb / several dogs")], 1),
    ]),
    "bottle": lambda: (
        '<fieldset><legend>1. Your dog\'s weight</legend><div class="range-row"><input type="range" name="weight" min="3" max="180" value="40" aria-label="Dog weight in pounds"><output class="range-out">40 lb</output></div></fieldset>'
        + _radios("freq", "2. How often you clean", [
            ("0.5", "Every 2 weeks"), ("1", "Weekly"), ("2", "Twice a week"), ("3.5", "Every other day"), ("0.25", "Monthly")], 1)
        + _radios("ears", "3. Ears cleaned each time", [("2", "Both ears"), ("1", "One ear")])
        + _radios("bottle", "4. Bottle size", [("118", "4 oz (118 mL)"), ("237", "8 oz (237 mL)"), ("355", "12 oz (355 mL)"), ("473", "16 oz (473 mL)")], 1)
    ),
}

TOOL_META = {
    "schedule": ("How often should you clean your dog's ears?", "Answer five quick questions to get a personal ear-cleaning schedule, plus a calendar file you can save.", "Get my schedule"),
    "symptoms": ("Dog ear symptom checker", "Tick what you've noticed. You'll see whether it sounds like home care, a vet visit this week, or a vet today.", "Check symptoms"),
    "finder": ("Which ear cleaner is right for my dog?", "Five questions, two matched picks from the cleaners Dog Ear Cleaner has researched.", "Show my matches"),
    "bottle": ("How much ear cleaner should I use?", "Estimate how much cleaner to use per ear and how long a bottle will last.", "Calculate"),
}


def render(kind, standalone=False):
    if kind not in FORMS:
        raise SystemExit(f"unknown tool {kind}")
    title, sub, button = TOOL_META[kind]
    head = "" if standalone else (f'<div class="tool-head"><span class="tool-badge">Free tool</span>'
                                   f'<p class="tool-title">{esc(title)}</p><p class="tool-sub">{esc(sub)}</p></div>')
    link = "" if standalone else (f'<p class="tool-link"><a href="{TOOLS[kind]["path"]}">Open the full {esc(TOOLS[kind]["name"].lower())}</a></p>')
    return (f'<div class="tool{" standalone" if standalone else ""}" data-tool="{kind}">{head}'
            f'<form class="tool-form" novalidate>{FORMS[kind]()}'
            f'<button class="btn-primary" type="submit">{button}</button></form>'
            f'<div class="tool-result" aria-live="polite" hidden></div>{link}</div>')


def data_script():
    """Product facts the finder/schedule tools need, embedded once per page."""
    data = {k: {"name": p["name"], "url": p["url"], "review": p["review"], "best": p["best_for"], "tags": p["tags"]}
            for k, p in PRODUCTS.items()}
    return f'<script type="application/json" id="dec-products">{json.dumps(data, separators=(",", ":"))}</script>\n'


def tool_grid(exclude=None, large=False):
    cards = []
    for k, t in TOOLS.items():
        if k == exclude:
            continue
        cards.append(f'<a class="tool-card" href="{t["path"]}"><span class="tool-icon" aria-hidden="true">{t["icon"]}</span>'
                     f'<span class="tool-card-name">{esc(t["name"])}</span><span class="tool-card-sub">{esc(t["short"])}</span></a>')
    return f'<div class="tool-grid{" large" if large else ""}">' + "".join(cards) + "</div>"


TOOLS = {
    "symptoms": dict(
        key="symptoms", icon="&#x1FA7A;", path="/tools/ear-symptom-checker/", name="Ear Symptom Checker",
        short="Clean at home, or call the vet?",
        title="Dog Ear Symptom Checker: Home Care or Vet Visit?",
        h1="Dog Ear Symptom Checker",
        description=("Free dog ear symptom checker from Dog Ear Cleaner. Tick your dog's ear symptoms to see "
                     "if it sounds like routine cleaning, a vet visit this week, or an emergency."),
        intro=("Scratching, head shaking, a funny smell? Tick what you've noticed and the Dog Ear Cleaner symptom "
               "checker sorts it into home care, a vet visit in the next few days, or a same-day vet visit."),
        body="""<h2>How to use the dog ear symptom checker</h2>
<p>Look at both ears in good light before you start. Lift each ear flap, sniff, and gently press around the base of the ear to see whether your dog flinches. Then tick every box that applies. The checker weighs red-flag signs (balance problems, facial drooping, bleeding, a swollen ear flap) far above everyday signs like light wax, so a single serious symptom is enough to recommend a same-day vet visit.</p>
<h2>What the results mean</h2>
<ul><li><strong>Home care:</strong> normal-looking wax with no pain or smell usually just needs a gentle cleaning. Follow our <a href="/how-to-clean-dog-earss-matters/">step-by-step guide to cleaning dog ears</a>.</li>
<li><strong>Vet visit this week:</strong> odor, discharge, redness or constant scratching suggest otitis externa (an outer ear infection). A vet needs to look down the canal and check a swab under the microscope to tell yeast from bacteria. Don't flush the ear right before the appointment, as it can wash away the evidence.</li>
<li><strong>Vet today:</strong> head tilt, circling, flicking eyes, facial drooping, bleeding, severe pain or a pillow-like ear flap can mean a middle or inner ear problem, a ruptured eardrum or an aural hematoma. These are not home-care problems.</li></ul>
<h2>Why you shouldn't pour cleaner into a painful ear</h2>
<p>If the eardrum is damaged, some cleaner ingredients can reach the middle ear and cause harm. That's why every reputable ear cleaner label says to ask a vet first if the ear is inflamed or painful. For a full rundown of warning signs, read <a href="/ear-infection-signs/">ear infection signs every dog owner should know</a>.</p>
<p>Once your vet has cleared the ear, a gentle maintenance cleaner such as [[amazon:epi-otic|Virbac Epi-Otic Advanced]] or [[amazon:vetericyn-plus|Vetericyn Plus Ear Rinse]] helps keep it that way.</p>""",
        faq=[
            ("Can I tell if my dog has an ear infection at home?", "You can spot the warning signs at home: odor, discharge, redness, swelling, head shaking and scratching. But only a vet can confirm an infection and tell yeast from bacteria or mites, because that needs an otoscope exam and a look at a swab under the microscope."),
            ("Should I clean my dog's ears if I think they're infected?", "Not before a vet has examined them. Cleaning can sting an inflamed ear, can be risky if the eardrum is damaged, and can wash away the debris the vet needs to sample."),
            ("Is a dog ear infection an emergency?", "Most outer ear infections are not emergencies but should be seen within a few days. Head tilt, loss of balance, flicking eyes, facial drooping, bleeding or severe pain should be seen the same day."),
            ("What does a yeast ear infection smell like?", "Owners often describe yeast as a musty, sweet or bread-like smell with brown, greasy wax. Bacterial infections more often smell foul and produce yellow or green discharge. These are clues, not a diagnosis."),
            ("Does this symptom checker replace a vet?", "No. It is a free triage aid from Dog Ear Cleaner that helps you decide how quickly to act. When in doubt, call your vet."),
        ]),
    "schedule": dict(
        key="schedule", icon="&#x1F4C5;", path="/tools/ear-cleaning-schedule/", name="Ear Cleaning Schedule Calculator",
        short="How often should you clean?",
        title="How Often to Clean Dog Ears: Free Schedule Calculator",
        h1="How Often Should You Clean Your Dog's Ears? (Schedule Calculator)",
        description=("How often should you clean your dog's ears? Answer 5 questions in this free Dog Ear Cleaner "
                     "calculator for a schedule based on ear type, swimming and allergies."),
        intro=("Every dog is different. A Basset Hound that swims needs a very different routine to a German Shepherd "
               "that hates water. Answer five questions to get your dog's ear-cleaning schedule and save the dates to your calendar."),
        body="""<h2>How often should you clean your dog's ears?</h2>
<p>Most dogs with healthy, upright ears only need their ears checked weekly and cleaned every few weeks, or when they look dirty. Dogs with floppy ears, hairy ear canals, allergies or a swimming habit build up moisture and wax faster, so they usually do better with weekly cleaning, plus a drying clean after every swim or bath.</p>
<p>Cleaning too often is a real problem too: it can irritate the canal and strip away its natural protection. The calculator above balances those risks using the factors that matter most.</p>
<h2>What the calculator considers</h2>
<ul><li><strong>Ear shape:</strong> floppy and hairy ears trap warmth and moisture. See our guide to <a href="/floppy-ear-breeds/">floppy-ear breeds</a>.</li>
<li><strong>Water exposure:</strong> water left in the canal after swims and baths is a classic trigger. Our <a href="/after-bath-care/">after-bath care guide</a> covers drying.</li>
<li><strong>Allergies:</strong> allergic dogs make up a large share of recurring ear infections, and cleaning is part of managing them.</li>
<li><strong>Current state and history:</strong> a dog that has had repeated infections needs a tighter routine (and a vet's plan).</li></ul>
<h2>Turn the schedule into a routine</h2>
<p>Pair the schedule with our <a href="/cleaning-routines/">dog ear cleaning routines</a> and the right cleaner. For most routine schedules, Dog Ear Cleaner recommends a gentle, drying, alcohol-free cleaner such as [[amazon:epi-otic|Virbac Epi-Otic Advanced]]; for very sensitive ears, [[amazon:vetericyn-plus|Vetericyn Plus Ear Rinse]].</p>""",
        faq=[
            ("How often should I clean my dog's ears?", "For most healthy dogs, every 2 to 4 weeks or when the ears look dirty. Floppy-eared dogs, swimmers and allergic dogs often need weekly cleaning, plus a drying clean after swimming or bathing."),
            ("Can you clean a dog's ears too much?", "Yes. Over-cleaning can irritate the ear canal and disrupt its natural balance. Unless a vet tells you otherwise, more than two or three times a week is usually too often for a healthy ear."),
            ("Should I clean my dog's ears after every bath?", "If water gets into the ears, yes: a drying ear cleaner after the bath helps remove trapped moisture. Placing cotton balls loosely in the ear openings during the bath helps keep water out in the first place."),
            ("Do puppies need their ears cleaned?", "Puppies need weekly ear checks, mainly to get them used to having their ears handled. Clean only when you see wax or dirt, using a gentle cleaner."),
            ("Do dogs with upright ears need ear cleaning?", "Less often. Many dogs with upright ears only need a weekly look and an occasional clean. Clean when you see wax build-up or after swimming."),
        ]),
    "finder": dict(
        key="finder", icon="&#x1F50D;", path="/tools/ear-cleaner-finder/", name="Ear Cleaner Finder Quiz",
        short="Match your dog to a cleaner",
        title="Which Dog Ear Cleaner Is Best for My Dog? Free Quiz",
        h1="Ear Cleaner Finder: Which Dog Ear Cleaner Is Best for Your Dog?",
        description=("Not sure which dog ear cleaner to buy? Take the free 30-second Dog Ear Cleaner quiz and get "
                     "two matched picks for smelly, itchy, sensitive or swimmer's ears."),
        intro=("There is no single best dog ear cleaner for every dog. Answer five questions and the Dog Ear Cleaner "
               "finder matches your dog's ears, your budget and your preferences to the cleaners we've researched."),
        body="""<h2>How the ear cleaner finder picks products</h2>
<p>Each cleaner in the quiz is tagged by what it actually contains and does: drying agents, enzymes, Tris-EDTA, hypochlorous acid, aloe, hydrocortisone, scent and format. Your answers weight those tags. A swimmer gets drying agents, a sore ear gets a no-sting formula, an itchy dog gets soothing ingredients, and a "natural" preference steers away from medicated products.</p>
<h2>Ingredients to look for (and avoid)</h2>
<ul><li><strong>Look for:</strong> alcohol-free formulas, gentle surfactants, drying agents for swimmers, and pH-balanced solutions.</li>
<li><strong>Use with care:</strong> hydrocortisone products (best for short-term itch relief, ideally with a vet's okay).</li>
<li><strong>Avoid:</strong> rubbing alcohol, hydrogen peroxide and undiluted vinegar. They sting, dry the canal and can damage irritated skin.</li></ul>
<p>Want the full comparison? Read our roundup of <a href="/best-dog-ear-cleaner/">the best dog ear cleaners</a>, or go straight to the <a href="/virbac-epi-otic-flush-review/">Epi-Otic review</a> and <a href="/zymox-ear-cleanser-review/">Zymox review</a>.</p>""",
        faq=[
            ("What is the best dog ear cleaner?", "For most dogs, a gentle, alcohol-free cleaner such as Virbac Epi-Otic Advanced is a safe starting point. Sensitive ears often do better with a no-sting rinse like Vetericyn Plus, and smelly, waxy ears with an enzymatic cleaner like Zymox."),
            ("Are ear wipes as good as liquid ear cleaner?", "Wipes are handy for cleaning the ear flap and the opening of the canal, but they can't flush debris out of the canal. Use a liquid cleaner for real cleaning and wipes for quick touch-ups."),
            ("Can I use a natural ear cleaner on my dog?", "Some plant-based cleaners are gentle and fine for routine cleaning. Avoid homemade mixes with vinegar, alcohol, peroxide or essential oils, which can irritate or harm the ear."),
            ("Do I need a prescription ear cleaner?", "Not for routine cleaning. Prescription cleaners and medicated drops are for diagnosed infections, so follow your vet's instructions for those."),
            ("Is the same ear cleaner safe for cats?", "Several cleaners, including Epi-Otic and Zymox, are labeled for both dogs and cats, but always check the label. Never use a product containing essential oils on a cat without veterinary advice."),
        ]),
    "bottle": dict(
        key="bottle", icon="&#x1F9EA;", path="/tools/ear-cleaner-dose-calculator/", name="Ear Cleaner Dose Calculator",
        short="How much to use, how long it lasts",
        title="How Much Ear Cleaner to Use on a Dog: Dose Calculator",
        h1="How Much Ear Cleaner Should You Use? (Dose & Bottle Calculator)",
        description=("How much ear cleaner should you use on your dog? The free Dog Ear Cleaner calculator estimates "
                     "the dose per ear and how long a bottle will last."),
        intro=("Most owners use far too little ear cleaner. Enter your dog's weight and routine to estimate how much to use "
               "per ear, and how many weeks a bottle will last before you need to reorder."),
        body="""<h2>How much ear cleaner should you use?</h2>
<p>Most dog ear cleaner labels tell you to fill the ear canal until the solution is visible at the opening, then massage the base of the ear. In practice that is roughly 1 to 2 mL per ear for a toy breed and 5 to 10 mL per ear for a giant breed. Using too little is the most common mistake: a few drops just sits on top of the wax instead of loosening it.</p>
<p>These are estimates. Always follow your product's label or your vet's directions, which take priority over any calculator.</p>
<h2>Which bottle size makes sense?</h2>
<p>Small dogs on a monthly routine can make a 4 oz bottle last a year or more, but ear cleaner doesn't last forever once opened, so check the expiry date. Large dogs, weekly cleaners and multi-dog homes usually save money with the bigger sizes, such as [[amazon:epi-otic-8oz|Epi-Otic Advanced 8 oz]] or [[amazon:petmd-tris-flush|Pet MD Tris Flush 12 oz]].</p>
<p>For technique, see <a href="/how-to-clean-dog-earss-matters/">how to clean dog ears</a>. For product picks, see <a href="/best-dog-ear-cleaner/">the best dog ear cleaners</a>.</p>""",
        faq=[
            ("How much ear cleaner do I put in my dog's ear?", "Fill the canal until you can see the liquid at the opening. That is roughly 1 to 2 mL per ear for toy breeds, 2 to 4 mL for small dogs, 4 to 6 mL for medium dogs and 6 to 10 mL for large and giant breeds. Follow your product label first."),
            ("Can you use too much ear cleaner on a dog?", "The extra simply runs out when your dog shakes, so overfilling one session isn't dangerous for a healthy ear. Cleaning too often is a bigger problem than using too much at once."),
            ("Should the bottle tip touch my dog's ear?", "No. Keep the nozzle just above the canal opening so it doesn't contaminate the bottle or poke the ear. Wipe the tip if it touches anything."),
            ("How long does a bottle of dog ear cleaner last?", "It depends on your dog's size and how often you clean. A 4 oz bottle used weekly on a 40 lb dog lasts roughly 3 months; the calculator gives an estimate for your dog."),
            ("Does ear cleaner expire?", "Yes. Check the expiry date printed on the bottle and replace it if the liquid changes color, smell or texture."),
        ]),
}
