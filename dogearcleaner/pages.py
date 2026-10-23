"""Homepage for dogearcleaner.com.

Brief: the site name "Dog Ear Cleaner" must appear at least 14 times in the
homepage's visible copy (validate.py counts it). The page targets the
queries Search Console shows the homepage earning impressions for:
dog ear cleaner, ear cleanser for dogs, dog ear care, ear cleaner for dog,
dog ear cleaner infection, dog ear rinse, dog ear cleaning, vet dog ear cleaning.
"""

from products import PRODUCTS
import tools as T

HOME_FAQ = [
    ("What is the best dog ear cleaner?",
     "For most dogs, Dog Ear Cleaner recommends starting with a gentle, alcohol-free cleaner such as Virbac Epi-Otic "
     "Advanced, the cleaner many vet clinics hand out. Dogs with sensitive or sore ears often do better with a no-sting "
     "rinse like Vetericyn Plus, and smelly, waxy ears with an enzymatic cleaner like Zymox."),
    ("How often should I clean my dog's ears?",
     "Most healthy dogs need their ears cleaned every 2 to 4 weeks, or when you see wax. Floppy-eared dogs, swimmers and "
     "dogs with allergies often need weekly cleaning. Our free schedule calculator gives a personal answer in 30 seconds."),
    ("Can a dog ear cleaner treat an ear infection?",
     "No. A dog ear cleaner removes wax, debris and moisture, which helps prevent infections, but it does not cure an "
     "active bacterial or yeast infection. Those need a vet's diagnosis and usually medicated drops."),
    ("Can I use homemade ear cleaner on my dog?",
     "It's not a good idea. Vinegar, hydrogen peroxide and rubbing alcohol can sting, dry out and irritate the ear canal, "
     "and can be harmful if the eardrum is damaged. A purpose-made, pH-balanced ear cleanser for dogs is safer."),
    ("Should I use cotton swabs to clean my dog's ears?",
     "Not inside the canal. Cotton swabs push wax deeper and can injure the ear. Use cotton balls, cotton rounds or gauze "
     "on the ear flap and the opening of the canal only."),
    ("Is Dog Ear Cleaner run by veterinarians?",
     "No. Dog Ear Cleaner is written by dog owners who research ear-care products and veterinary guidance carefully. "
     "We tell you when to call a vet, and our tools are triage aids, not a diagnosis."),
]


def render_home(*, layout, posts, helpers):
    h = helpers
    esc = h["esc"]
    card = h["product_card"]
    img = h["img_tag"]
    by = {p["slug"]: p for p in posts.values()}

    def plink(slug, text):
        return f'<a href="/{slug}/">{text}</a>' if slug in by else text

    review_cards = "".join(h["post_card"](p) for p in posts.values() if p["category"] == "reviews")
    guide_cards = "".join(h["post_card"](p) for p in posts.values() if p["category"] != "reviews")
    epi = PRODUCTS["epi-otic"]

    body = f'''
<section class="home-hero"><div class="wrap hero-grid">
<div class="hero-copy">
<p class="eyebrow">Dog ear care, made simple</p>
<h1>Dog Ear Cleaner: Find the Best Dog Ear Cleaner &amp; Clean Your Dog's Ears Safely</h1>
<p class="hero-lead">Dog Ear Cleaner helps you choose the right ear cleanser for your dog, use it the right way, and know when it's time for the vet instead. Honest reviews, step-by-step guides and free interactive tools, all in plain English.</p>
<div class="hero-ctas"><a class="btn-primary" href="/best-dog-ear-cleaner/">See the best dog ear cleaners</a><a class="btn-ghost" href="/tools/ear-cleaner-finder/">Take the 30-second quiz</a></div>
<ul class="hero-proof"><li><strong>16</strong> ear cleaners compared</li><li><strong>4</strong> free ear-care tools</li><li><strong>0</strong> paid placements</li></ul>
</div>
<figure class="hero-media">{img("Dog-Ear-Cleaner-Hero-Image.webp", "Yorkshire Terrier having its ear examined and cleaned by a veterinary professional", eager=True)}
<figcaption>Leave swabs inside the ear to your vet. At home, a dog ear cleaner and cotton rounds do the job.</figcaption></figure>
</div></section>

<section class="picks"><div class="wrap">
<div class="section-head"><p class="eyebrow">Dog Ear Cleaner top picks</p><h2>The best dog ear cleaners at a glance</h2>
<p>Short on time? These are the three cleaners Dog Ear Cleaner recommends most often. Each links to Amazon so you can check today's price, and to our full review.</p></div>
<div class="pick-grid">
<div class="pick"><span class="pick-label">Best overall</span>{card("epi-otic")}</div>
<div class="pick"><span class="pick-label">Best for smelly, waxy ears</span>{card("zymox-cleanser")}</div>
<div class="pick"><span class="pick-label">Best for sensitive ears</span>{card("vetericyn-plus")}</div>
</div>
<p class="center"><a class="text-link" href="/best-dog-ear-cleaner/">Compare all 10 picks in our best dog ear cleaner guide &rarr;</a></p>
</div></section>

<section class="home-tool"><div class="wrap home-tool-grid">
<div class="home-tool-copy"><p class="eyebrow">Free quiz</p><h2>Not sure which dog ear cleaner your dog needs?</h2>
<p>A dog with itchy, allergy-prone ears needs something different from a Labrador that swims every weekend. Answer five questions and the Dog Ear Cleaner finder matches your dog to two cleaners, with links to buy and to read the full review.</p>
<p>Prefer to compare yourself? The table below lines up the ear cleansers for dogs we've researched.</p></div>
{T.render("finder")}
</div></section>

<section class="home-steps"><div class="wrap">
<div class="section-head"><p class="eyebrow">Dog ear cleaning in 6 steps</p><h2>How to clean your dog's ears (the quick version)</h2>
<p>Here's the routine Dog Ear Cleaner recommends for healthy ears. For photos-free detail, mistakes to avoid and how to handle a dog that hates it, read the full guide to {plink("how-to-clean-dog-earss-matters", "how to clean dog ears")}.</p></div>
<ol class="step-grid">
<li><strong>Check first.</strong> Pale pink skin and a little light wax is normal. Redness, pain, discharge or a bad smell means vet first, cleaner later.</li>
<li><strong>Get set up.</strong> Ear cleaner, cotton rounds or gauze, a towel and treats. No cotton swabs inside the canal.</li>
<li><strong>Fill the canal.</strong> Lift the ear flap and squeeze in enough dog ear cleaner to fill the canal. Most people use too little.</li>
<li><strong>Massage 20-30 seconds.</strong> Rub the base of the ear until you hear a squish. That's the cleaner breaking up wax.</li>
<li><strong>Let them shake.</strong> Step back. The head shake brings loosened debris up and out.</li>
<li><strong>Wipe and reward.</strong> Wipe the flap and the opening, never deeper than your finger reaches, then praise and treat.</li>
</ol>
<div class="center"><a class="btn-primary" href="/how-to-clean-dog-earss-matters/">Read the full ear cleaning guide</a> <a class="btn-ghost" href="/tools/ear-cleaning-schedule/">How often should I clean?</a></div>
</div></section>

<section class="home-compare"><div class="wrap">
<div class="section-head"><p class="eyebrow">Side by side</p><h2>Dog ear cleaner comparison</h2>
<p>The ear cleanser for dogs that's right for you depends on what's going on in the ear. Here's how the most popular options compare on the features that matter.</p></div>
{h["compare_table"](["epi-otic", "zymox-cleanser", "vetericyn-plus", "petmd-tris-flush", "epiklean", "petmd-wipes"])}
</div></section>

<section class="home-vet"><div class="wrap vet-grid">
<div><p class="eyebrow">Dog ear cleaner vs. infection</p><h2>Clean at home, or call the vet?</h2>
<p>A dog ear cleaner is for maintenance: it lifts wax, rinses away debris and dries out moisture so yeast and bacteria have less to work with. It isn't a treatment for an infection that's already there. If your dog's ear smells bad, looks red or swollen, has yellow, green or dark discharge, or your dog cries when you touch it, use the symptom checker or book a vet visit before you clean.</p>
<p>Red flags that need a vet <em>today</em>: head tilt, loss of balance, flicking eyes, a drooping face, bleeding, or a puffy, fluid-filled ear flap. More in our guide to {plink("ear-infection-signs", "dog ear infection signs")}.</p>
<a class="btn-primary" href="/tools/ear-symptom-checker/">Use the ear symptom checker</a></div>
<div class="vet-tools"><p class="tool-title">Free Dog Ear Cleaner tools</p>{T.tool_grid()}</div>
</div></section>

<section class="home-posts"><div class="wrap">
<div class="section-head"><p class="eyebrow">Honest reviews</p><h2>Dog ear cleaner reviews</h2>
<p>Each Dog Ear Cleaner review digs into the ingredient list, the label directions, the dogs it suits and the downsides most reviews skip.</p></div>
<div class="card-grid">{review_cards}</div>
<div class="section-head spaced"><p class="eyebrow">Dog ear care guides</p><h2>Guides to keep your dog's ears healthy</h2>
<p>From floppy-ear breeds to after-bath drying, these Dog Ear Cleaner guides cover the habits that prevent most ear problems.</p></div>
<div class="card-grid">{guide_cards}</div>
<p class="center"><a class="text-link" href="/resources/">Browse all dog ear care resources &rarr;</a></p>
</div></section>

<section class="home-trust"><div class="wrap trust-grid">
<div><p class="eyebrow">Why trust Dog Ear Cleaner</p><h2>Research you can check, advice you can actually follow</h2>
<p>Dog Ear Cleaner is a small, independent site run by dog owners. We don't do sponsored reviews and no brand can pay for a spot on our lists. When you buy through our Amazon links we may earn a small commission, which keeps the site free, and it never changes what we recommend.</p>
<p>Every recommendation on Dog Ear Cleaner starts with the full ingredient list and the manufacturer's directions, gets checked against published veterinary guidance on ear care, and is weighed against patterns in owner feedback. We're upfront that we're not vets, and we tell you plainly when a problem needs one. <a href="/about-us/">How Dog Ear Cleaner researches products</a>.</p></div>
<ul class="trust-list">
<li><strong>Ingredient-first reviews.</strong> We explain what each active ingredient does, so you can judge for yourself.</li>
<li><strong>Vet-first safety.</strong> Every guide says when to stop and call the vet.</li>
<li><strong>No fake testing claims.</strong> We tell you exactly how we reached each verdict.</li>
<li><strong>Kept current.</strong> Product formulas change, so we re-check our picks regularly.</li>
</ul>
</div></section>

<section class="home-faq"><div class="wrap narrow">
{h["faq_html"](HOME_FAQ, "Dog ear cleaner FAQs")}
</div></section>

<section class="home-final"><div class="wrap final-cta">
<div><h2>Ready to clean your dog's ears?</h2><p>Start with the cleaner most vets reach for. It's gentle, alcohol-free and suits most dogs.</p></div>
<a class="btn-amazon" href="{epi["url"]}" rel="nofollow sponsored noopener" target="_blank">Shop Epi-Otic on Amazon</a>
</div></section>
'''
    origin = h["ORIGIN"]
    schema = [h["faq_schema"](HOME_FAQ, origin + "/"),
              {"@type": "WebPage", "@id": origin + "/#webpage", "url": origin + "/",
               "name": "Dog Ear Cleaner: Best Dog Ear Cleaners, Guides & Free Tools",
               "isPartOf": {"@id": origin + "/#website"}, "about": {"@id": origin + "/#org"},
               "primaryImageOfPage": origin + "/assets/img/Dog-Ear-Cleaner-Hero-Image.webp"}]
    return layout(
        path="/", title="Dog Ear Cleaner: Best Dog Ear Cleaners, Guides & Free Tools",
        description=("Dog Ear Cleaner helps you pick the best dog ear cleaner and clean your dog's ears safely: "
                     "honest reviews, step-by-step guides and free ear-care tools."),
        body=body, schema=schema, extra_head=T.data_script(), body_class="home")
