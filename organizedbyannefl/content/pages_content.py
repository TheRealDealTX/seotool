"""Copy and data for the hand-built pages: home, about, services hub, contact,
service area, tools and legal. Templates are str.format()-ed by build.py, so
literal braces must be doubled.
"""

HOME_TITLE = "Professional Organizer in Fort Lauderdale | Organized by Anne"
HOME_DESC = ("Organized by Anne is a professional organizer in Fort Lauderdale bringing calm, beautiful order to "
             "closets, kitchens, pantries and whole homes across Broward County.")

ROTATE = ["closets", "pantries", "home offices", "kitchens", "whole homes"]
MARQUEE = ["Closets", "Pantries", "Kitchens", "Home offices", "Move-ins", "Bathrooms", "Laundry rooms", "Kids' rooms",
           "Downsizing", "Garages"]

# icon, color, messy-left %, messy-top %, messy-rotation
CALM_ITEMS = [
    ("shirt", "#c4785a", 58, 52, -24), ("utensils", "#7d917b", 6, 62, 18), ("box", "#b99a66", 36, 8, 32),
    ("lamp", "#4d614f", 72, 14, -12), ("sofa", "#c4785a", 22, 38, 40), ("laptop", "#2a2724", 48, 30, -38),
    ("gift", "#b99a66", 78, 62, 22), ("tag", "#7d917b", 10, 10, -30), ("washing-machine", "#4d614f", 40, 60, 12),
    ("armchair", "#c4785a", 64, 36, 55), ("calendar", "#2a2724", 18, 70, -48), ("heart", "#7d917b", 82, 40, -16),
]

PICKER = {
    "closet": {"label": "The closet", "img": "closet-rail", "alt": "Organized clothing rail",
               "title": "Closet organization", "tip": "Turn every hanger backwards today. In three months, anything still backwards is a strong candidate to let go — and you'll have data instead of guilt.",
               "href": "/services/closet-organization", "cta": "Explore closet organization"},
    "kitchen": {"label": "Kitchen & pantry", "img": "kitchen-open-shelves", "alt": "Organized kitchen shelves",
                "title": "Kitchen & pantry organization", "tip": "Store things where you use them: mugs by the coffee maker, oils by the stove, lunch gear near the fridge. Zones beat pretty containers every time.",
                "href": "/services/kitchen-pantry-organization", "cta": "Explore pantry organization"},
    "office": {"label": "Home office", "img": "green-home-office", "alt": "Calm home office",
               "title": "Home office organization", "tip": "Give paper exactly three homes: to-do, to-file and to-shred. Anything else on the desk is decor or a decision you haven't made yet.",
               "href": "/services/home-office-organization", "cta": "Explore home office help"},
    "move": {"label": "A move", "img": "bright-empty-living", "alt": "Bright, freshly unpacked living room",
             "title": "Move-in & unpacking", "tip": "Unpack the kitchen and one bathroom first, then beds. A home that can feed you and rest you buys you patience for everything else.",
             "href": "/services/move-in-unpacking", "cta": "Explore unpacking services"},
    "everything": {"label": "Honestly? Everything", "img": "minimal-living", "alt": "Clutter-free living room",
                   "title": "Decluttering & whole-home organizing", "tip": "Start with the space you see first every morning. A small, visible win changes how the whole house feels — and fuels the next room.",
                   "href": "/services/decluttering-downsizing", "cta": "Explore decluttering services"},
    "laundry": {"label": "Laundry & bath", "img": "laundry-baskets", "alt": "Laundry shelves with woven baskets",
                "title": "Laundry & bathroom organization", "tip": "One basket per person in the laundry room means clean clothes travel straight back to the right bedroom — no more mystery pile on the couch.",
                "href": "/services/laundry-bathroom-organization", "cta": "Explore laundry & bath"},
}

PROCESS = [
    ("clipboard-list", "Consult", "We walk the space with you, in person or by video, and listen to what's not working."),
    ("palette", "Plan", "A custom plan using what you already own, plus a curated product list and layout ideas."),
    ("layers", "Sort &amp; edit", "We sort, categorize and edit together — judgment-free, at a pace that feels right."),
    ("sparkles", "Style", "Containers, labels and a touch of decor so the space is as beautiful as it is functional."),
    ("refresh-cw", "Maintain", "Simple routines and a reset guide so the system keeps working long after we leave."),
]

TOOLS = [
    ("organizing-time-estimator", "calculator", "Organizing time estimator",
     "Pick your rooms and clutter level to see roughly how many organizer hours your project needs."),
    ("declutter-decision-helper", "circle-help", "Keep or let go? Decision helper",
     "Stuck on an item? Answer a few quick questions and get a clear keep, donate, sell or toss verdict."),
    ("30-day-declutter-challenge", "list-checks", "30-day declutter challenge",
     "One small task a day for a month. Your progress saves in your browser so you can pick up anytime."),
    ("closet-rod-calculator", "ruler", "Closet rod calculator",
     "Count your hanging clothes and find out how many feet of rod you need — and whether double-hang works."),
]

HOME_FAQS = [
    ("What does a professional organizer do?", "We help you edit what you own, design a system that fits your routines, and set up containers and labels so everything has a home. We work side by side with you or take the lead, whichever you prefer."),
    ("Do I need to declutter before you arrive?", "No. Please don't clean or tidy first — seeing the space as it really is helps us design a system that works for the way you actually live."),
    ("What areas do you serve?", "We're based in Fort Lauderdale and work throughout Broward County, including Wilton Manors, Oakland Park, Plantation, Weston, Coral Springs, Hollywood and Pompano Beach. Virtual consultations are available anywhere."),
    ("Will you make me throw things away?", "Never. Every keep-or-let-go decision is yours. We ask helpful questions, offer options like donating or selling, and handle the drop-offs if you'd like."),
    ("Do you shop for organizing products?", "Yes. We start with what you already have, then share a curated product list or shop for you from local stores so everything fits your space and style."),
    ("How do I get started?", "Send us a note through the contact form or email info@organizedbyannefl.com. We'll set up a consultation to talk through your space, goals and timeline."),
]

HOME_TEMPLATE = """
<section class="hero">
  <div class="blob blob-1" aria-hidden="true"></div><div class="blob blob-2" aria-hidden="true"></div><div class="blob blob-3" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="reveal">
      <h1><span class="h1-kicker">Professional organizer in Fort Lauderdale</span>Organizing with a touch of design for <span class="rotator">{rot}</span></h1>
      <p class="lead">Organized by Anne is a professional organizer in Fort Lauderdale helping you create order in the chaos of life. We pair practical systems with thoughtful styling, because a sorted space can be a work of art.</p>
      <div class="hero-actions">
        <a class="btn btn-terra" href="/contact">Book a consultation {arrow}</a>
        <a class="btn btn-ghost" href="/services">Explore services</a>
      </div>
      <ul class="hero-points">
        <li>{check} In-home &amp; virtual consults</li>
        <li>{check} Judgment-free, always</li>
        <li>{check} Broward County</li>
      </ul>
    </div>
    <div class="hero-art reveal" data-reveal>
      <svg class="spin-badge" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="circ" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs><circle cx="60" cy="60" r="58" fill="#fffdf9"/><text><textPath href="#circ">a sorted space · a work of art · </textPath></text><path d="M50 66 60 44 70 66M54 59h12" fill="none" stroke="#c4785a" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="main" data-depth="-14">{hero_img}</div>
      <div class="float-card fc-1" data-depth="26">{fc1}</div>
      <div class="float-card fc-2" data-depth="34">{fc2}</div>
      <div class="hero-badge" data-depth="18"><span class="bi">{sparkles}</span><span>Calm, styled spaces<small>Systems that stay organized</small></span></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">{marquee}</div></div>

<section class="section">
  <div class="wrap calm-grid">
    <div class="reveal">
      <span class="eyebrow">See the difference</span>
      <h2>From clutter to <em class="accent">calm</em> — in one tap</h2>
      <p class="lead">Life can be stressful, cluttered and busy, but your home doesn't have to be. Every item gets a home, every home gets a label, and the whole space finally exhales.</p>
      <div class="toggle-wrap" role="group" aria-label="Show before or after">
        <button type="button" data-calm="0" aria-pressed="true">Before</button>
        <button type="button" data-calm="1" aria-pressed="false">After</button>
      </div>
      <ul class="calm-list">
        <li>{check}<span><strong>Edit first, buy second.</strong> We work with what you own before suggesting a single bin.</span></li>
        <li>{check}<span><strong>Zones that match your routines.</strong> Things live where you actually use them.</span></li>
        <li>{check}<span><strong>A finishing touch of design.</strong> Containers, labels and styling that look as good as they work.</span></li>
      </ul>
    </div>
    <div class="calm-stage reveal" aria-label="Animation of scattered household items snapping into a tidy grid">{calm}<span class="calm-label">Before: clutter</span></div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="section-head center reveal"><span class="eyebrow">Services</span><h2>Every space, thoughtfully organized</h2>
      <p class="lead">Do-it-all service or a custom plan you carry out yourself — your trusted partner either way.</p></div>
    <div class="card-grid">{svc_cards}</div>
  </div>
</section>

<section class="section" id="about">
  <div class="wrap split">
    <div class="img-stack reveal-img"><div class="a">{about_a}</div><div class="b">{about_b}</div></div>
    <div class="reveal">
      <span class="eyebrow">Let's meet</span>
      <h2>Order for real life, with an eye for <em class="accent">design</em></h2>
      <p>Organized by Anne brings the same attention to detail you'd expect from a luxury event planner to the spaces you live in every day. From planning to execution, every detail is taken care of — in your home, office or studio.</p>
      <p>We can do it all for you, or work alongside you to build the perfect customized solution for your space. Either way, the goal is the same: a little more peace at home, finished with a touch of decor.</p>
      <ul class="feature-list">
        <li><span class="fi">{leaf}</span><div><strong>Sustainable by default</strong><span>We reuse what you have and route donations to local organizations.</span></div></li>
        <li><span class="fi">{palette}</span><div><strong>Designed, not just tidied</strong><span>Color, texture and proportion matter — a sorted space can be a work of art.</span></div></li>
        <li><span class="fi">{heart}</span><div><strong>Judgment-free</strong><span>Every home has a hot spot. We're here to help, never to critique.</span></div></li>
      </ul>
      <a class="btn" href="/about">More about us {arrow}</a>
    </div>
  </div>
</section>

<section class="section section-ink">
  <div class="wrap">
    <div class="section-head center reveal"><span class="eyebrow" style="color:#e7a98d">How it works</span><h2>A calm, five-step process</h2></div>
    {process}
  </div>
</section>

<section class="section">
  <div class="wrap" data-picker>
    <script type="application/json">{picker_json}</script>
    <div class="section-head reveal"><span class="eyebrow">Quick pick</span><h2>Which space is stressing you out?</h2><p class="lead">Tap one for a pro tip you can try tonight — and the service that fixes it for good.</p></div>
    <div class="picker">
      <div class="picker-chips reveal" role="group" aria-label="Choose a space">{chips}</div>
      <div class="picker-out reveal" aria-live="polite">
        <div class="po-img">{p_img}</div>
        <div class="po-body fade"><span class="eyebrow">Pro tip</span><h3>{p_title}</h3><p>{p_tip}</p><a class="btn btn-sm" href="{p_href}">{p_cta} {arrow}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="section section-paper">
  <div class="wrap">
    <div class="section-head center reveal"><span class="eyebrow">Free tools</span><h2>Plan your project in minutes</h2><p class="lead">Interactive helpers to estimate time, make decisions faster and build habits that stick.</p></div>
    <div class="card-grid">{tools}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="area-band reveal">{area_img}
      <div class="inner">
        <span class="eyebrow" style="color:#f3d6c8">Where we work</span>
        <h2>Fort Lauderdale &amp; Broward County</h2>
        <p>From Las Olas high-rises to family homes in Plantation and Weston, we know South Florida living — humidity, hurricane season, seasonal moves and all.</p>
        <div class="area-tags">{tags}</div>
        <a class="btn btn-light" href="/service-area">See our service area {arrow}</a>
      </div>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="section-head reveal" style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;max-width:none">
      <div><span class="eyebrow">From the blog</span><h2>Life-changing tips for your space</h2></div>
      <a class="btn btn-ghost" href="/blog">All articles {arrow}</a>
    </div>
    <div class="card-grid posts">{posts}</div>
  </div>
</section>

<section class="section">
  <div class="narrow reveal">{faq}</div>
</section>

<section class="section-tight"><div class="wrap">
  <div class="cta-band reveal">
    <div class="blob blob-1" aria-hidden="true"></div>
    <div style="position:relative"><h2>For life-changing tips for your space</h2><p>Join our list for seasonal organizing ideas, Florida-specific checklists and new free tools. No spam, unsubscribe anytime.</p></div>
    <form class="actions" action="/contact-submit" method="post" data-ajax data-ok="You're on the list — thank you!">
      <input type="hidden" name="type" value="tips"><input type="hidden" name="ts" value="">
      <label class="hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
      <div class="newsletter"><label class="sr-only" for="nl-email">Email address</label><input id="nl-email" type="email" name="email" placeholder="you@email.com" required autocomplete="email"><button class="btn btn-light btn-sm" type="submit">Subscribe {send}</button></div>
      <div class="form-status" role="status"></div>
    </form>
  </div>
</div></section>
"""

ABOUT_BODY = """
<section class="section">
  <div class="wrap split">
    <div class="img-stack reveal-img"><div class="a">{a}</div><div class="b">{b}</div></div>
    <div class="reveal">
      <span class="eyebrow">Our story</span>
      <h2>Create order in the chaos of life</h2>
      <p>Organized by Anne began with a simple idea: life can be stressful, cluttered and busy — but your home doesn't have to be. The same planning mindset that keeps a high-end event running smoothly, where every detail is considered from start to finish, works beautifully at home.</p>
      <p>That's why our projects feel a little different. We don't just tidy. We study how you move through your day, edit what no longer serves you, and design systems that are easy to keep up. Then we finish with a touch of decor — matching hangers, a pretty basket, a label in a font you love — because a sorted space can be a work of art.</p>
      <p>As your trusted partner, we can do it all, or work alongside you to create the perfect customized solution for your home, office or studio.</p>
      <p class="sig">— Organized by Anne</p>
    </div>
  </div>
</section>

<section class="section section-sand">
  <div class="wrap">
    <div class="section-head center reveal"><span class="eyebrow">What we believe</span><h2>Three promises on every project</h2></div>
    <div class="values">
      <div class="value reveal"><span class="vi">{heart}</span><h3>No judgment, ever</h3><p>Clutter is a normal side effect of a full life — new babies, moves, careers, caregiving, grief. We show up to help, not to critique.</p></div>
      <div class="value reveal" style="--d:.1s"><span class="vi">{leaf}</span><h3>Use what you have</h3><p>Before we suggest a single purchase we repurpose the bins, baskets and furniture you already own. Donations go to local Broward County organizations whenever possible.</p></div>
      <div class="value reveal" style="--d:.2s"><span class="vi">{palette}</span><h3>Beautiful and practical</h3><p>A system only works if you enjoy using it. We pay attention to color, texture and proportion so the finished space feels like you.</p></div>
    </div>
  </div>
</section>

<section class="section section-ink">
  <div class="wrap">
    <div class="section-head center reveal"><span class="eyebrow" style="color:#e7a98d">Our process</span><h2>How a project comes together</h2></div>
    {process}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Popular services</span><h2>Where we can help</h2></div>
    <div class="card-grid">{svc_cards}</div>
    <p style="margin-top:28px"><a class="btn btn-ghost" href="/services">See all services {arrow}</a></p>
  </div>
</section>

<section class="section-tight"><div class="narrow reveal">{faq}</div></section>
"""

ABOUT_FAQS = [
    ("Who is Organized by Anne for?", "Busy families, professionals, seasonal residents, people preparing to move or downsize, and anyone who wants their home to feel calmer and work better."),
    ("Do you work in condos and high-rises?", "Yes. Much of Fort Lauderdale lives vertically, and we're used to working around elevator reservations, loading docks and compact storage."),
    ("Is everything confidential?", "Absolutely. What we see in your home stays between us, and we never post photos of your space without your written permission."),
    ("Can you work with my designer or contractor?", "Yes. We happily coordinate with interior designers, closet installers, movers and contractors so the organizing plan fits the bigger picture."),
]

SERVICES_BODY = """
<section class="section section-ink">
  <div class="wrap">
    <div class="section-head center reveal"><span class="eyebrow" style="color:#e7a98d">Every project</span><h2>How we work</h2></div>
    {process}
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Two ways to work together</span>
      <h2>Do-it-all or do-it-together</h2>
      <p>Some clients want to hand over the keys and come home to a finished space. Others want a clear plan and a guide by their side. Both are welcome.</p>
      <ul class="calm-list">
        <li>{check}<span><strong>Full-service organizing.</strong> In-home consultation, a curated plan, hands-on sorting, product sourcing, installation, labels and donation drop-off.</span></li>
        <li>{check}<span><strong>Plan &amp; guide.</strong> We review areas of opportunity and concern, build your organizational plan around existing systems, and coach you as you implement it.</span></li>
        <li>{check}<span><strong>Virtual consultation.</strong> A one-hour video session with help taking measurements, a curated product list and a mock diagram of your space.</span></li>
      </ul>
      <p style="margin-top:26px"><a class="btn btn-terra" href="/contact">Book a consultation {arrow}</a></p>
    </div>
    <div class="reveal tool-shell" style="--d:.1s">
      <span class="eyebrow">Not sure where to start?</span>
      <h3>Estimate your project in two minutes</h3>
      <p>Our free organizing time estimator turns your rooms and clutter level into a ballpark of organizer hours and sessions.</p>
      <a class="btn" href="/tools/organizing-time-estimator">Open the estimator {arrow}</a>
    </div>
  </div>
</section>
<section class="section-tight"><div class="narrow reveal">{faq}</div></section>
"""

SERVICES_FAQS = [
    ("How much do your organizing services cost?", "Every project is quoted individually after a consultation, because scope, team size and products vary widely. Our guide to professional organizer costs explains the factors involved."),
    ("How long does a typical project take?", "A single closet or pantry is often finished in one session, while a whole home may take several days spread across a few weeks. Try our time estimator for a ballpark."),
    ("Do I have to be home while you organize?", "For editing decisions we'll need you nearby, at least at first. Once decisions are made, many clients run errands or work while we set up the space."),
    ("Do you take donations away?", "Yes. We bag, label and drop off donations to local charities, and can point you toward consignment for higher-value pieces."),
]

CONTACT_BODY = """
<section class="section-tight">
  <div class="wrap contact-grid">
    <div class="reveal">
      <h2>Let's talk about it</h2>
      <p>Not sure which service you need? That's what the consultation is for. Share what's on your mind and we'll suggest a plan — no pressure, no judgment.</p>
      <ul class="contact-points">
        <li><span class="ci">{mail}</span><div><small>Email</small><a href="mailto:{email}">{email}</a></div></li>
        <li><span class="ci">{pin}</span><div><small>Based in</small><span>Fort Lauderdale, FL · Broward County</span></div></li>
        <li><span class="ci">{clock}</span><div><small>Response time</small><span>Within one business day</span></div></li>
        <li><span class="ci">{video}</span><div><small>Outside South Florida?</small><a href="/services/virtual-organizing">Book a virtual consultation</a></div></li>
      </ul>
      <div class="hero-media reveal-img" style="aspect-ratio:4/3">{img}</div>
    </div>
    <div class="form-card reveal" style="--d:.1s">
      <form action="/contact-submit" method="post" data-ajax data-ok="Thank you! Your message is on its way. We'll reply within one business day.">
        <input type="hidden" name="type" value="contact"><input type="hidden" name="ts" value="">
        <label class="hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
        <div class="field-row">
          <div class="field"><label for="c-name">Your name</label><input id="c-name" name="name" required autocomplete="name"></div>
          <div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required autocomplete="email"></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="c-phone">Phone (optional)</label><input id="c-phone" type="tel" name="phone" autocomplete="tel"></div>
          <div class="field"><label for="c-city">Neighborhood or city</label><input id="c-city" name="city" placeholder="e.g. Victoria Park" autocomplete="address-level2"></div>
        </div>
        <fieldset class="field" style="border:0;padding:0;margin:0 0 18px"><legend class="lbl" style="margin-bottom:8px">Which spaces need help?</legend><div class="chip-group">{spaces}</div></fieldset>
        <div class="field"><label for="c-type">Consultation type</label>
          <select id="c-type" name="consult"><option>In-home (Broward County)</option><option>Virtual (video)</option><option>Not sure yet</option></select></div>
        <div class="field"><label for="c-msg">Tell us about your space</label><textarea id="c-msg" name="message" required placeholder="What's working, what isn't, and your ideal timeline."></textarea></div>
        <button class="btn btn-terra" type="submit">Send message {send}</button>
        <div class="form-status" role="status" aria-live="polite"></div>
        <p class="form-note" style="color:var(--muted)">We'll only use your details to reply to your request. See our <a href="/privacy-policy">privacy policy</a>.</p>
      </form>
    </div>
  </div>
</section>
<section class="section-tight"><div class="narrow reveal">{faq}</div></section>
"""

CONTACT_FAQS = [
    ("What happens after I send a message?", "We'll reply within one business day to learn a bit more and schedule your consultation, either at your home or by video."),
    ("Should I send photos?", "Photos are helpful but optional. If you'd like, reply to our email with a few pictures of the space so we can come prepared."),
    ("Do you offer gift certificates?", "Yes — organizing makes a thoughtful gift for new parents, newlyweds and anyone who just moved. Mention it in your message and we'll set one up."),
]

AREA_BODY = """
<section class="section-tight">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">Neighborhoods &amp; cities</span><h2>Where we organize</h2>
      <p class="lead">If you don't see your neighborhood, just ask — we travel throughout Broward County and can often reach nearby Palm Beach and Miami-Dade communities.</p></div>
    <div class="chip-group reveal">{tags}</div>
  </div>
</section>
<section class="section">
  <div class="wrap split flip">
    <div class="hero-media reveal-img" style="margin-top:0;aspect-ratio:4/3.2">{img}</div>
    <div class="reveal">
      <span class="eyebrow">Local know-how</span>
      <h2>Organizing for South Florida living</h2>
      <p>Organizing a home in Fort Lauderdale comes with its own checklist. We plan for it from the first consultation.</p>
      <ul class="calm-list">
        <li>{check}<span><strong>Humidity-smart storage.</strong> Breathable bins, airflow in closets and moisture absorbers to protect clothing, leather and paper. <a href="/blog/closet-organization-humid-climate">Read our humid-climate closet guide</a>.</span></li>
        <li>{check}<span><strong>Hurricane-season ready.</strong> A grab-and-go document system and labeled supply bins that are easy to reach from June through November. <a href="/blog/hurricane-season-home-organization-florida">See the checklist</a>.</span></li>
        <li>{check}<span><strong>Condo &amp; high-rise logistics.</strong> Elevator reservations, loading docks and compact storage are part of the plan, not a surprise.</span></li>
        <li>{check}<span><strong>Seasonal residents.</strong> Open-up and close-down routines for snowbirds and second homes. <a href="/blog/seasonal-home-organization-snowbirds">Get the seasonal guide</a>.</span></li>
      </ul>
      <p style="margin-top:24px"><a class="btn btn-terra" href="/contact">Check availability {arrow}</a></p>
    </div>
  </div>
</section>
<section class="section-tight"><div class="narrow reveal">{faq}</div></section>
"""

AREA_FAQS = [
    ("Do you charge for travel?", "Projects in Fort Lauderdale and nearby cities don't carry a travel fee. For locations farther out we'll mention any travel considerations when we quote your project."),
    ("Can you organize a home I'm not living in yet?", "Yes. We regularly unpack and set up homes for clients who are still relocating, and we can coordinate with your movers and building management."),
    ("What if I live outside Florida?", "Our virtual organizing consultation works anywhere. We'll review your space by video and send a custom plan, product list and layout diagram."),
]

# ------------------------------------------------------------------ tools

DECISION = {
    "nodes": {
        "start": {"q": "When did you last use (or wear) this item?", "a": [["Within the past year", "love"], ["One to two years ago", "season"], ["Honestly, I can't remember", "dup"]]},
        "love": {"q": "Do you love it, or does it genuinely make life easier?", "a": [["Yes, absolutely", "home"], ["Not really — it's just there", "dup"]]},
        "home": {"q": "Does it have a dedicated home where you can find it quickly?", "a": [["Yes", "v_keep"], ["Not yet", "v_home"]]},
        "season": {"q": "Is it seasonal or for a specific occasion (holidays, travel, hurricane kit, guests)?", "a": [["Yes", "v_store"], ["No", "dup"]]},
        "dup": {"q": "Do you own something else that does the same job?", "a": [["Yes, I have a duplicate", "cond"], ["No, it's the only one", "senti"]]},
        "senti": {"q": "Is it sentimental — a gift, heirloom or memory?", "a": [["Yes", "space"], ["No", "replace"]]},
        "space": {"q": "Would a photo of it hold the memory just as well?", "a": [["Maybe, yes", "cond"], ["No, I want the real thing", "v_memory"]]},
        "replace": {"q": "If you let it go and needed it later, could you borrow or replace it easily (for under about $20)?", "a": [["Yes, easily", "cond"], ["No, it would be hard to replace", "v_store"]]},
        "cond": {"q": "What condition is it in?", "a": [["Like new or valuable", "v_sell"], ["Good and usable", "v_donate"], ["Worn out, stained or broken", "recy"]]},
        "recy": {"q": "Is it made of something recyclable (paper, metal, electronics, textiles)?", "a": [["Yes", "v_recycle"], ["No / not sure", "v_toss"]]},
        "v_keep": {"verdict": "keep", "why": "You use it, you love it, and it already has a home."},
        "v_home": {"verdict": "home", "why": "It earns its place — it just needs an address."},
        "v_store": {"verdict": "store", "why": "It's useful, just not every day."},
        "v_memory": {"verdict": "memory", "why": "Some things matter because of the story they hold."},
        "v_sell": {"verdict": "sell", "why": "It still has real value, and someone else will love it."},
        "v_donate": {"verdict": "donate", "why": "It's in good shape but isn't serving you anymore."},
        "v_recycle": {"verdict": "recycle", "why": "It's past its useful life, but the materials aren't."},
        "v_toss": {"verdict": "toss", "why": "It's done its job and can't be reused by someone else."},
    },
    "verdicts": {
        "keep": {"title": "Keep it", "icon": "heart", "color": "#7d917b", "next": "Put it back in its home and enjoy it."},
        "home": {"title": "Keep it — and give it a home", "icon": "house", "color": "#c4785a", "next": "Store it near where you use it, and label the spot so it always finds its way back."},
        "store": {"title": "Keep it — store it smartly", "icon": "box", "color": "#b99a66", "next": "Move it to a labeled bin up high or in deep storage so it isn't taking prime real estate."},
        "memory": {"title": "Keep it as a treasure", "icon": "hand-heart", "color": "#a85f43", "next": "Display it or give it a special memory box. Limiting the box size keeps memories meaningful, not overwhelming."},
        "sell": {"title": "Sell or consign it", "icon": "tag", "color": "#b99a66", "next": "Give yourself a deadline — two weeks is plenty. If it hasn't sold by then, donate it."},
        "donate": {"title": "Donate it", "icon": "gift", "color": "#4d614f", "next": "Bag it today and put the bag in your car so it actually leaves the house."},
        "recycle": {"title": "Recycle it", "icon": "recycle", "color": "#7d917b", "next": "Check your city's recycling guidelines or a local e-waste or textile drop-off."},
        "toss": {"title": "Let it go", "icon": "trash-2", "color": "#2a2724", "next": "Thank it for its service and toss it. Every exit makes room for what matters."},
    },
}


def estimator_rooms(icon):
    rooms = [("closet", "shirt", "Closets"), ("kitchen", "utensils", "Kitchen"), ("pantry", "box", "Pantry"),
             ("bedroom", "lamp", "Bedrooms"), ("bath", "sparkles", "Bathrooms"), ("office", "laptop", "Home office"),
             ("kids", "heart", "Kids' rooms / playroom"), ("living", "sofa", "Living / family room"),
             ("laundry", "washing-machine", "Laundry room"), ("garage", "package-open", "Garage")]
    return "".join(
        '<div class="room-row" data-room="%s"><label>%s %s</label><div class="stepper">'
        '<button type="button" data-step="-1" aria-label="Fewer %s">&minus;</button><output aria-live="polite">0</output>'
        '<button type="button" data-step="1" aria-label="More %s">+</button></div></div>' % (k, icon(i), n, n, n) for k, i, n in rooms)


CHALLENGE = [
    "Clear your kitchen counters", "Purge expired pantry items", "Sort the junk drawer", "Toss old receipts and mail",
    "Edit your sock and underwear drawer", "Match food storage lids and containers", "Clear out the bathroom cabinet",
    "Delete 100 photos from your phone", "Donate five pieces of clothing", "Empty and wipe the fridge",
    "Tidy your entryway and shoes", "Recycle old magazines and catalogs", "Edit your coffee mug collection",
    "Clear the nightstand", "Sort cleaning supplies under the sink", "Unsubscribe from ten email lists",
    "Edit linens and towels", "Clean out your purse or work bag", "Declutter the car", "Sort cords and chargers",
    "Edit books and keep your favorites", "Purge old makeup and skincare", "Organize your desk drawer",
    "Edit kids' toys or art (or your hobby supplies)", "Check your hurricane kit and documents", "Clear one shelf in the garage",
    "Sort spices and toss the stale ones", "Edit shoes you never wear", "Drop off every donation bag", "Reset one room and celebrate",
]


def challenge_days():
    return "".join(
        '<div class="day"><input type="checkbox" id="d%d"><label for="d%d"><span class="dn">%d</span><span class="tx">%s</span></label></div>' % (
            i + 1, i + 1, i + 1, t) for i, t in enumerate(CHALLENGE))


TOOL_PAGES = [
    {
        "slug": "organizing-time-estimator", "name": "Organizing Time Estimator", "img": "planner-board",
        "title": "Organizing Time Estimator: How Long Will It Take?",
        "description": "Free organizing time estimator: choose your rooms, home size and clutter level to see roughly how many professional organizer hours your project needs.",
        "h1": "How long will it take to organize your home?",
        "lead": "Add the rooms on your list, set your clutter level and see a ballpark of organizer hours and sessions. It's a planning estimate, not a quote — every home is different.",
        "widget": """<div class="tool-shell reveal" data-tool="estimator"><div class="tool-grid">
  <div>
    <h2 style="font-size:1.5rem">1. Which spaces are on your list?</h2>
    <div class="room-rows">{rooms}</div>
    <h2 style="font-size:1.5rem;margin-top:30px">2. How full are they?</h2>
    <div class="seg" role="group" aria-label="Clutter level">
      <button type="button" data-level="1" aria-pressed="false">Light<small>Mostly tidy, needs systems</small></button>
      <button type="button" data-level="2" aria-pressed="true">Moderate<small>Full, some piles</small></button>
      <button type="button" data-level="3" aria-pressed="false">Heavy<small>Hard to use the space</small></button>
    </div>
    <h2 style="font-size:1.5rem;margin-top:30px">3. Home size</h2>
    <label class="sr-only" for="home-size">Home size</label>
    <input class="range" type="range" id="home-size" min="1" max="3" step="1" value="2">
    <div class="range-row"><span>Compact</span><strong id="size-name">Average</strong><span>Spacious</span></div>
    <h2 style="font-size:1.5rem;margin-top:30px">4. Team size</h2>
    <div class="seg" role="group" aria-label="Number of organizers">
      <button type="button" data-team="1" aria-pressed="true">1 organizer<small>Steady pace</small></button>
      <button type="button" data-team="2" aria-pressed="false">2 organizers<small>Faster finish</small></button>
      <button type="button" data-team="3" aria-pressed="false">3 organizers<small>Move-in speed</small></button>
    </div>
  </div>
  <div class="result-card" aria-live="polite">
    <span class="eyebrow" style="color:#e7a98d">Your estimate</span>
    <div class="big">0 <small>hrs</small></div>
    <p id="sessions" class="muted">Add a room or two to see your estimate.</p>
    <div class="bars"></div>
    <p class="muted" style="margin-top:18px">Planning estimate only. Your actual time depends on decision speed, product installation and the space itself.</p>
    <a class="btn btn-terra" href="/contact">Get a real quote {arrow}</a>
  </div>
</div></div>""",
        "body": """<h2>How the estimate works</h2>
<p>Each space starts from a typical number of hands-on hours for one organizer working through an average-sized room with a moderate amount of stuff. A walk-in closet, for example, usually takes longer than a linen closet, and a garage takes longer than either. The calculator then adjusts for clutter level, overall home size and the number of organizers on site.</p>
<p>The result shows <strong>total organizer hours</strong> (the labor involved) and <strong>hours on site</strong> (how long your home is busy). Two organizers working for four hours is eight organizer hours but only four hours of your day.</p>
<h2>What makes projects faster or slower</h2>
<ul><li><strong>Decision speed.</strong> The biggest variable is how quickly keep-or-let-go decisions get made. Our <a href="/tools/declutter-decision-helper">decision helper</a> can help you practice.</li>
<li><strong>Pre-sorting.</strong> Gathering like items together before your session can save time — but please don't stress-clean first.</li>
<li><strong>Product installation.</strong> Closet systems, drawer inserts and shelving add setup time.</li>
<li><strong>Donation logistics.</strong> Hauling donations or consignment pieces adds a short trip at the end.</li></ul>
<p>Ready for a real plan? See our <a href="/services">organizing services</a> or read <a href="/blog/how-much-does-a-professional-organizer-cost">how professional organizer costs work</a>.</p>""",
        "faqs": [("Is this estimate a quote?", "No. It's a planning tool. We quote every project individually after a consultation because each home, and each person's pace, is different."),
                 ("Why does clutter level matter so much?", "Most organizing time is spent sorting and deciding, not arranging. A heavily filled space simply has more decisions to make."),
                 ("Does it save my answers?", "Yes, your selections are stored only in your own browser so you can come back to them later.")],
    },
    {
        "slug": "declutter-decision-helper", "name": "Declutter Decision Helper", "img": "minimal-living",
        "title": "Keep or Let Go? Free Declutter Decision Helper",
        "description": "Stuck on an item while decluttering? Answer a few quick questions in our free decision helper and get a clear keep, store, donate, sell, recycle or toss verdict.",
        "h1": "Keep it or let it go? Ask the decision helper",
        "lead": "Hold the item in your hand, answer a few quick questions and get a clear, guilt-free verdict. Repeat for the next item — momentum is everything.",
        "widget": """<div class="tool-shell reveal" data-tool="decision">
  <script type="application/json">{json}</script>
  <div class="quiz">
    <div class="quiz-progress" aria-hidden="true"><span></span></div>
    <div class="quiz-stage" aria-live="polite"></div>
    <div style="margin-top:34px;padding-top:20px;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;font-size:.88rem;color:var(--ink-2)">
      <strong>Your session:</strong>
      <span>Keep <b data-tally="keep">0</b></span><span>Home <b data-tally="home">0</b></span><span>Store <b data-tally="store">0</b></span>
      <span>Treasure <b data-tally="memory">0</b></span><span>Sell <b data-tally="sell">0</b></span><span>Donate <b data-tally="donate">0</b></span>
      <span>Recycle <b data-tally="recycle">0</b></span><span>Toss <b data-tally="toss">0</b></span>
      <button type="button" class="link-btn" data-reset-tally>{rotate} Reset</button>
    </div>
  </div>
</div>""",
        "body": """<h2>Why a decision tree helps</h2>
<p>Decluttering is rarely hard because of the stuff. It's hard because of the decisions — dozens of them, back to back, each with a little emotion attached. A short, consistent set of questions takes the guesswork out and helps you move faster without second-guessing.</p>
<h2>Tips for a faster session</h2>
<ul><li>Set up four bags or boxes before you start: keep, donate, sell and recycle/toss.</li>
<li>Work one small category at a time, like mugs or T-shirts, rather than a whole room.</li>
<li>Set a timer for 20 minutes and stop while you still have energy.</li>
<li>Take donations to the car the same day so they actually leave.</li></ul>
<p>Want to build the habit? Try our <a href="/tools/30-day-declutter-challenge">30-day declutter challenge</a> or download ideas from our <a href="/blog/room-by-room-decluttering-checklist">room-by-room decluttering checklist</a>. If it all feels like too much, our <a href="/services/decluttering-downsizing">decluttering services</a> are judgment-free.</p>""",
        "faqs": [("What if I still can't decide?", "Put the item in a dated 'maybe' box. If you haven't opened the box in six months, donate it without looking inside."),
                 ("What about sentimental items?", "Keep the pieces that tell the story best and give them a place of honor. A photo can preserve the memory of the rest."),
                 ("Where can I donate in Fort Lauderdale?", "Many local thrift stores, shelters and charities accept household goods. Call ahead for what they currently need, or let us handle the drop-off during a session.")],
    },
    {
        "slug": "30-day-declutter-challenge", "name": "30-Day Declutter Challenge", "img": "cozy-living",
        "title": "30-Day Declutter Challenge: Free Interactive Checklist",
        "description": "Take the free 30-day declutter challenge: one small task a day with an interactive checklist that saves your progress in your browser. Printable, too.",
        "h1": "The 30-day declutter challenge",
        "lead": "One small task a day, about 15 minutes each. Check off days as you go — your progress saves in this browser, so you can come back anytime.",
        "widget": """<div class="tool-shell reveal" data-tool="challenge"><div class="tool-grid">
  <div class="days">{days}</div>
  <div class="result-card">
    <span class="eyebrow" style="color:#e7a98d">Your progress</span>
    <div class="ring-wrap">
      <svg class="ring" viewBox="0 0 120 120" aria-hidden="true"><circle class="bg" cx="60" cy="60" r="52"/><circle class="fg" cx="60" cy="60" r="52"/><text x="60" y="68" text-anchor="middle">0/30</text></svg>
      <p id="challenge-msg" aria-live="polite" style="margin:0">Pick a day and start small — fifteen minutes counts.</p>
    </div>
    <p class="muted" style="margin-top:18px">Do the days in any order. Skipped one? No problem — just pick up where you are.</p>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <button type="button" class="btn btn-light btn-sm" data-print>Print checklist</button>
      <button type="button" class="btn btn-sm" style="--bg:transparent;border-color:rgba(255,255,255,.3)" data-reset>{rotate} Reset</button>
    </div>
  </div>
</div></div>""",
        "body": """<h2>How to do the challenge</h2>
<p>Every task is designed to take about fifteen minutes. Small wins build momentum, and momentum is what turns decluttering from a dreaded weekend project into an easy habit. You don't need to go in order, and you don't need to be perfect.</p>
<ul><li><strong>Keep a donation bag in your car.</strong> Drop items in as you go and make one trip at the end of each week.</li>
<li><strong>Use the decision helper</strong> when you get stuck: our <a href="/tools/declutter-decision-helper">keep-or-let-go tool</a> keeps things moving.</li>
<li><strong>Celebrate milestones.</strong> Days 10, 20 and 30 deserve a little reward.</li></ul>
<h2>After the 30 days</h2>
<p>Once the backlog is gone, maintenance is simple: a ten-minute reset each evening and a quick monthly edit of hot spots like the <a href="/blog/junk-drawer-organization-tips">junk drawer</a>. If you'd like a pro to tackle the bigger rooms, explore our <a href="/services/home-organizing">home organizing services</a>.</p>""",
        "faqs": [("Do I need to finish in exactly 30 days?", "Not at all. Go at your own pace — the checklist saves your progress so you can take breaks."),
                 ("Is my progress private?", "Yes. Your checkmarks are saved only in your own browser and are never sent to us."),
                 ("Can I print it?", "Yes. Use the Print checklist button to print the list and stick it on the fridge.")],
    },
    {
        "slug": "closet-rod-calculator", "name": "Closet Rod Calculator", "img": "closet-rail",
        "title": "Closet Rod Calculator: How Much Hanging Space?",
        "description": "Free closet rod calculator: count shirts, pants, dresses and coats to see how many feet of hanging rod you need and whether double-hang will work.",
        "h1": "Closet rod calculator: how much hanging space do you need?",
        "lead": "Count what you hang, pick your hanger style and see how many feet of rod your wardrobe needs — plus whether a double-hang section could double your space.",
        "widget": """<div class="tool-shell reveal" data-tool="rod"><div class="tool-grid">
  <div>
    <div class="field-row">
      <div class="field"><label for="r-shirts">Shirts &amp; blouses</label><input id="r-shirts" type="number" name="shirts" min="0" max="400" value="30" inputmode="numeric"></div>
      <div class="field"><label for="r-pants">Pants &amp; skirts</label><input id="r-pants" type="number" name="pants" min="0" max="400" value="12" inputmode="numeric"></div>
      <div class="field"><label for="r-dresses">Dresses</label><input id="r-dresses" type="number" name="dresses" min="0" max="400" value="6" inputmode="numeric"></div>
      <div class="field"><label for="r-jackets">Blazers &amp; light jackets</label><input id="r-jackets" type="number" name="jackets" min="0" max="400" value="4" inputmode="numeric"></div>
      <div class="field"><label for="r-suits">Suits</label><input id="r-suits" type="number" name="suits" min="0" max="400" value="0" inputmode="numeric"></div>
      <div class="field"><label for="r-coats">Heavy coats</label><input id="r-coats" type="number" name="coats" min="0" max="400" value="1" inputmode="numeric"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="hanger">Hanger style</label><select id="hanger"><option value="slim">Slim velvet hangers</option><option value="standard">Standard plastic hangers</option><option value="wood">Wooden hangers</option></select></div>
      <div class="field"><label for="existing">Current rod length (feet)</label><input id="existing" type="number" min="0" max="60" step="0.5" value="" placeholder="e.g. 6" inputmode="decimal"></div>
    </div>
    <p class="lbl" style="font-weight:700;margin:6px 0 0">Your rod, visualized</p>
    <div class="rod-viz" aria-hidden="true"></div>
  </div>
  <div class="result-card" aria-live="polite">
    <span class="eyebrow" style="color:#e7a98d">You need about</span>
    <div class="big">0 <small>feet of rod</small></div>
    <p id="rod-gap" class="muted"></p>
    <p id="rod-drop" class="muted"></p>
    <p class="muted">Includes about 15% breathing room so hangers slide easily — important for airflow in humid Florida closets.</p>
    <a class="btn btn-terra" href="/services/closet-organization">Plan my closet {arrow}</a>
  </div>
</div></div>""",
        "body": """<h2>How we calculate rod space</h2>
<p>Every garment takes up a predictable slice of rod. On slim velvet hangers, most shirts use about an inch each, pants and skirts a little more, and bulky coats several inches. Standard plastic and wooden hangers are thicker, so the calculator scales up for them. We then add about 15% breathing room so clothes aren't crushed and air can circulate.</p>
<h2>Double-hang vs. long-hang</h2>
<p>Shirts, folded pants and skirts hang in roughly 40 inches or less, which means two rods can stack in a standard-height closet — instantly doubling capacity. Dresses, long coats and suits need a long-hang section. Most closets work best with a mix.</p>
<div class="tip"><strong>Pro tip</strong><p>Switching to matching slim hangers is one of the fastest, most affordable ways to gain rod space and make a closet look instantly calmer.</p></div>
<p>Keeping clothes fresh in a Florida closet takes more than space — read our guide to <a href="/blog/closet-organization-humid-climate">closet organization in humid climates</a>, or let us design it with you through our <a href="/services/closet-organization">closet organization service</a>.</p>""",
        "faqs": [("How much closet rod does one person need?", "It varies widely, but many people need somewhere between four and eight feet of hanging space. Count your own wardrobe with the calculator for a personal answer."),
                 ("What height should a double-hang rod be?", "A common setup places the upper rod around 80 to 84 inches from the floor and the lower rod around 40 to 42 inches, but measure your longest double-hang items first."),
                 ("Should I fold or hang sweaters?", "Fold knits and sweaters to prevent stretched shoulders. That can free up a lot of rod space, too.")],
    },
]

# ------------------------------------------------------------------ legal

LEGAL = [
    ("privacy-policy", "Privacy Policy", "How Organized by Anne collects, uses and protects the information you share through this website.", """
<p>This privacy policy explains how Organized by Anne ("we", "us") handles information collected through organizedbyannefl.com.</p>
<h2>Information we collect</h2>
<p>When you submit our contact or newsletter form, we collect the details you provide, such as your name, email address, phone number, neighborhood and message. We do not collect payment information through this website.</p>
<p>Our interactive tools (the time estimator, decision helper, 30-day challenge and closet rod calculator) store your selections only in your own browser using local storage. That information is never sent to us.</p>
<h2>How we use information</h2>
<ul><li>To respond to your inquiry and schedule consultations.</li><li>To send organizing tips if you subscribe — you can unsubscribe at any time.</li><li>To keep basic server logs for security and troubleshooting.</li></ul>
<p>We do not sell or rent your personal information.</p>
<h2>Photos of your home</h2>
<p>We never publish photos of a client's home without written permission.</p>
<h2>Third parties</h2>
<p>This website loads fonts from Google Fonts. Our hosting provider processes server logs on our behalf.</p>
<h2>Contact</h2>
<p>Questions about this policy? Email <a href="mailto:{email}">{email}</a>.</p>"""),
    ("terms", "Terms of Use", "The terms that apply when you use the Organized by Anne website, blog and free organizing tools.", """
<p>By using organizedbyannefl.com you agree to these terms.</p>
<h2>Content</h2>
<p>Articles and tools on this website are for general informational purposes. Estimates produced by our tools are planning guides, not quotes. Always follow manufacturer instructions and official guidance, including local emergency management advice during hurricane season.</p>
<h2>Services</h2>
<p>Organizing services are provided under a separate agreement or quote issued after a consultation.</p>
<h2>Intellectual property</h2>
<p>The text, design and tools on this website belong to Organized by Anne. You're welcome to share links to our pages and print checklists for personal use.</p>
<h2>Limitation of liability</h2>
<p>This website is provided "as is". We are not liable for decisions made based solely on its content.</p>
<h2>Contact</h2>
<p>Email <a href="mailto:{email}">{email}</a> with any questions.</p>"""),
]
