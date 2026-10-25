# Nine-domain content network: plan, keywords and link flow

Prepared 2026-10-25. Companion files in this folder:

- `content_calendar_q1.csv` — 108 posts: one per site per week for 12 weeks, each with target keyword, US monthly volume, keyword difficulty (DataForSEO), working title and the network link that post carries.
- `link_schedule_q1.csv` — which site links to which, month by month, for the first quarter.

## 1. What each domain was, and what it becomes

Topic continuity is the whole game. Google's March 2024 expired-domain abuse policy targets domains repurposed into unrelated content. Every site below keeps its original subject and only widens it toward home and property where that is natural.

| Domain | Historical topic (from anchor text and real linkers) | New editorial focus | Tier |
| --- | --- | --- | --- |
| hatetolovethesplit.com | US split-level home renovation blog (Ikea Akurum cabinet review, renovation checklists) | Home renovation, kitchen remodels, budgets, roof and attic basics | 1 |
| agadecor.com | Home decor | Room-by-room decor ideas, exterior curb appeal | 1 |
| ohmtoherminediy.com | DIY crafts and home projects | DIY home maintenance, upcycling, gutters and attic jobs | 1 |
| fraserandmorris.com | UK interiors brand (109 article links from thedahliapapers.com, House and Garden mention) | Interior design styles, wallpaper, renovation planning | 1 |
| rjbledlcdtvservicecentre.com | Kolkata LED/LCD TV service centre | Home electronics repair and troubleshooting, storm-damage claims for electronics | 1b |
| asmith.photography | Fashion and editorial photographer (eye-forward.com, fashiongonerogue.com, ladygunn.com) | Fashion, portrait and location photography | 2 |
| michellewhitephoto.com | Wedding photographer (weddingsparrow.com, brideandbreakfast.hk) | Wedding and engagement photography, wedding planning | 2 |
| comeicavoliamerenda.com | Florence food blog by Chiara Francioli ("Cavoli a merenda") | Tuscan and Italian cooking, Florence travel | 2 |
| findsforfitness.com | Fitness gear reviews (best shoes for flat feet) | Flat-feet footwear, home gym setup | 2 |

Tier 1 sites are the only ones that link to the money sites. Tier 2 sites link only into Tier 1. The TV repair site sits between: it is thin, so it links into Tier 1 and sends exactly one money-site link per quarter, from its insurance-claim post.

Two cautions on the heritage:

- Do not present the photography and food sites as the original people. Aaron Smith, Michelle White and Chiara Francioli are real. Keep the domain as the brand name, add an "under new ownership" about page with a new editorial persona, and never reuse their names, bios or images.
- comeicavoliamerenda.com carries a stray "California Insurance Law" anchor from a previous repurposing. That is a prior abuse signal on this domain. Stay strictly on food.

## 2. Keyword approach

Every target in the calendar came from DataForSEO Labs filtered to: informational intent, keyword difficulty 30 or lower, US volume between 150 and 3,000 a month. Volumes shown are the current month. A handful of strong targets had no difficulty score in the dataset and are marked n/a; treat those as unverified and check them in Semrush before writing.

Rules for every post:

- One primary keyword per post, no two posts in the network on the same primary keyword.
- 1,200 to 2,000 words, original photos or properly licensed images, author byline that is consistent within a site and different across sites.
- Two to four internal links to the site's own posts.
- One outbound link to a non-network authority source on every post (manufacturer, .gov, university, trade body). This is what makes the network link look normal.
- At most one network link per post, and roughly half of posts carry none.

## 3. Link flow

The pattern is a funnel, not a ring.

```
Tier 2 (photo, wedding, food, fitness)  -->  Tier 1 (renovation, decor, DIY, interiors)  -->  money sites
                                             Tier 1b (TV repair) ---------------------------^ (one link per quarter)
```

Rules:

- Money-site links come only from Tier 1. Each Tier 1 site sends two per month, each to a different roofing domain, rotating so every roofing site receives links from every Tier 1 site over the quarter.
- Money-site links point at deep pages (a service page or a blog post), never only the homepage. Anchors rotate: brand name, bare URL, a partial phrase ("the roof repair guide"), and a generic ("this explainer"). Never an exact-match commercial anchor.
- Tier 1 sites link laterally to one other Tier 1 site per month, in a one-way ring that reverses direction next quarter. No reciprocal pair inside any 90-day window.
- Tier 2 sites send one link per month into Tier 1, rotating target each month. Tier 2 sites never link to money sites and never link to each other more than once a quarter.
- Nothing in the network links to rjbledlcdtvservicecentre.com except the home renovation site, once, in month 3. It is the weakest domain and receiving links from it is worth more than sending them.

The month-by-month assignments are in `link_schedule_q1.csv`. The per-post assignment is the last column of the content calendar.

## 4. Footprint hygiene

The network is nine same-owner sites that link toward four same-owner roofing sites. These are the things that make that visible:

- Hosting: different providers or at least different IP ranges per tier. Not all on the Hostinger account that runs huttoroofs.com.
- Nameservers and registrars: varied. Whois privacy on all.
- Platforms and themes: mix static builds, WordPress and one or two other stacks. No shared theme, favicon style or footer text.
- Analytics: separate Google Analytics properties and Search Console verifications. No shared Tag Manager container, AdSense ID or affiliate IDs.
- Publishing cadence: different weekdays per site, published times varied, not nine posts at 9 a.m. Monday.
- Authors: one named persona per site with a consistent voice and a real-looking about page. No persona appears on two sites.
- Outbound profile: every site links out to real third-party sources far more than it links into the network.

## 5. Clean-up before launch

All nine domains were hit by the same link-spam network during the last few months: roughly 2,600 referring domains each, from auto-generated "Domain Report" and "URL Shared" pages on a single IP block plus .shop/.store/.site throwaways, with anchors like "Premium Link Building Experts for Better Rankings". That is why every one of these domains shows a spam score around 53.

Before publishing:

1. Upload a disavow file per domain listing those referring domains. I can generate it from the DataForSEO exports.
2. Rebuild the old high-value URLs where real links still point (the fraserandmorris.com pages that thedahliapapers.com links to, the asmith.photography pages eye-forward.com links to). A 301 to a relevant new page is fine, a 404 wastes the link.
3. Set up Search Console on each domain on day one to catch any manual action from the previous owner's history.

## 6. Build sequence

1. Week 0: disavow files, hosting split, Search Console, one persona per site, about and contact pages, 301 map for legacy URLs.
2. Weeks 1 to 4: publish from the calendar with no network links at all. Let each site index on its own content first.
3. Weeks 5 to 12: introduce the links on the schedule. Start with Tier 2 into Tier 1, add money-site links from week 7.
4. End of quarter: pull ranked keywords for each site, drop any keyword cluster that has not moved, and run the next quarter's keyword pass with the same filters.
