"""Turns the content modules into pages.

build.py calls build_all() with its own globals so this module can use the
shared chrome without a circular import.
"""

from siteconfig import BIZ, STATUTE, FOOTER_SERVING, TODAY

from content.industries import INDUSTRIES
from content.services import SERVICES
from content.tools import TOOLS
from content.areas import AREAS
from content.blog import POSTS
from content import pages as sp


def _rotate(seq, start, count):
    """Deterministic slice with wraparound, so related-links blocks differ
    from page to page instead of repeating the same three items site-wide."""
    n = len(seq)
    return [seq[(start + i) % n] for i in range(count)]


def build_all(B):
    write = B["write"]
    standard_page = B["standard_page"]
    article_page = B["article_page"]
    build_hub = B["build_hub"]
    render_blocks = B["render_blocks"]
    service_schema = B["service_schema"]
    tool_schema = B["tool_schema"]
    article_schema = B["article_schema"]
    itemlist_schema = B["itemlist_schema"]
    all_pages = B["all_pages"]

    # ------------------------------------------------------------ industries
    write("/who-we-serve/", build_hub(
        path="/who-we-serve/",
        eyebrow="Who we serve",
        h1="Nine kinds of building,<br>nine different <em>problems</em>",
        lede=("We work institutional and large commercial property only. The pages below set out "
              "what changes when the owner is a congregation rather than a corporation, a school "
              "board rather than a landlord, a city rather than a chain &mdash; whichever party "
              "has retained us."),
        items=INDUSTRIES,
        intro_sections=sp.INDUSTRY_HUB_INTRO,
        trail=[("Home", "/"), ("Who we serve", None)],
        title="Who We Serve | Churches, Schools, Cities &amp; Commercial",
        description=("Independent claims consultants for Texas churches, school districts, "
                     "municipalities, universities, hospitals, multifamily, hotels, industrial "
                     "and retail property."),
        card_mode="cards",
        schema=[itemlist_schema("/who-we-serve/", "Property types served",
                                [(i["nav_label"], i["path"]) for i in INDUSTRIES])],
    ))

    for idx, ind in enumerate(INDUSTRIES):
        rel_services = _rotate(SERVICES, idx * 2, 3)
        rel_posts = _rotate(POSTS, idx, 2)
        page = dict(ind)
        page["trail"] = [("Home", "/"), ("Who we serve", "/who-we-serve/"),
                         (ind["nav_label"], None)]
        page["schema"] = [service_schema(
            "%s insurance claim representation" % ind["nav_label"],
            ind["card_blurb"], ind["path"], "Public Insurance Adjusting")]
        page["sections"] = list(ind["sections"]) + [
            {
                "band": "paper2",
                "eyebrow": "Related services",
                "h2": "How these claims get worked.",
                "blocks": [
                    ("cards", [(s["card_title"], s["card_blurb"], s["path"]) for s in rel_services]),
                    ("html", '<div class="mt-l"><a class="tlink" href="/services/">'
                             'All claim services <span class="arw">&rarr;</span></a></div>'),
                ],
            },
            {
                "eyebrow": "Further reading",
                "h2": "From the claims desk.",
                "blocks": [
                    ("links", [(p["h1_plain"], p["blurb"], p["path"]) for p in rel_posts]),
                    ("html", '<div class="mt-l"><p class="kicker" style="margin-bottom:14px;">'
                             'Where we work</p><div class="tagrow">'
                             + "".join('<a class="tag" href="%s">%s</a>' % (a["path"], a["nav_label"])
                                       for a in AREAS)
                             + '<a class="tag" href="/service-areas/">All of Texas &rarr;</a></div></div>'),
                ],
            },
        ]
        write(ind["path"], standard_page(page))

    # -------------------------------------------------------------- services
    write("/services/", build_hub(
        path="/services/",
        eyebrow="Claim services",
        h1="From first notice<br>to final <em>number</em>",
        lede=("Five of these are organized by what happened to the building. Three are for "
              "matters that are already stuck. One works best before there is a claim at all."),
        items=SERVICES,
        intro_sections=sp.SERVICE_HUB_INTRO,
        trail=[("Home", "/"), ("Services", None)],
        title="Commercial Claim Services | Texas Claims Consultants",
        description=("Claims consulting services for Texas commercial property: hurricane, "
                     "hail, fire, water and freeze, business interruption, appraisal, denied "
                     "claims and policy review."),
        card_mode="links",
        schema=[itemlist_schema("/services/", "Claim services",
                                [(s["nav_label"], s["path"]) for s in SERVICES])],
    ))

    for idx, svc in enumerate(SERVICES):
        rel_inds = _rotate(INDUSTRIES, idx * 3, 3)
        rel_tools = _rotate(TOOLS, idx, 2)
        page = dict(svc)
        page["trail"] = [("Home", "/"), ("Services", "/services/"), (svc["nav_label"], None)]
        page["schema"] = [service_schema(svc["h1_plain"], svc["card_blurb"], svc["path"])]
        page["sections"] = list(svc["sections"]) + [
            {
                "band": "paper2",
                "eyebrow": "Who this is for",
                "h2": "Property types we take these claims for.",
                "blocks": [
                    ("cards", [(i["card_title"], i["card_blurb"], i["path"]) for i in rel_inds]),
                    ("html", '<div class="mt-l"><a class="tlink" href="/who-we-serve/">'
                             'Everyone we serve <span class="arw">&rarr;</span></a></div>'),
                ],
            },
            {
                "eyebrow": "Run the numbers",
                "h2": "Tools that apply to this kind of claim.",
                "blocks": [
                    ("links", [(t["card_title"], t["card_blurb"], t["path"]) for t in rel_tools]),
                ],
            },
        ]
        write(svc["path"], standard_page(page))

    # ----------------------------------------------------------------- tools
    write("/tools/", build_hub(
        path="/tools/",
        eyebrow="Tools &amp; calculators",
        h1="Seven calculators<br>we use on <em>live files</em>",
        lede=("Built for commercial numbers rather than householder ones. Everything runs in your "
              "browser &mdash; no form to fill in, nothing stored, nothing sent."),
        items=TOOLS,
        intro_sections=sp.TOOL_HUB_INTRO,
        trail=[("Home", "/"), ("Tools", None)],
        title="Commercial Claim Calculators | Free Tools",
        description=("Seven free commercial claim calculators: claim value, business "
                     "interruption, coinsurance, depreciation, Texas deadlines, roof cost "
                     "and adjuster fees."),
        card_mode="cards",
        schema=[itemlist_schema("/tools/", "Claim calculators",
                                [(t["nav_label"], t["path"]) for t in TOOLS])],
    ))

    for idx, tool in enumerate(TOOLS):
        others = [t for t in TOOLS if t["slug"] != tool["slug"]]
        rel_tools = _rotate(others, idx, 3)
        rel_svc = _rotate(SERVICES, idx * 2 + 1, 2)
        page = dict(tool)
        page["trail"] = [("Home", "/"), ("Tools", "/tools/"), (tool["nav_label"], None)]
        page["schema"] = [tool_schema(tool)]
        page["page_type"] = "WebApplication"
        page["sections"] = [
            {"tight": True, "flush": True, "blocks": [("html", tool["calc"])]},
        ] + list(tool["sections"]) + [
            {
                "band": "paper2",
                "eyebrow": "Other tools",
                "h2": "The rest of the toolkit.",
                "blocks": [
                    ("links", [(t["card_title"], t["card_blurb"], t["path"]) for t in rel_tools]),
                ],
            },
            {
                "eyebrow": "Related services",
                "h2": "When the number matters enough to argue about.",
                "blocks": [
                    ("cards", [(s["card_title"], s["card_blurb"], s["path"]) for s in rel_svc]),
                ],
            },
        ]
        write(tool["path"], standard_page(page))

    # ---------------------------------------------------------- service areas
    write("/service-areas/", build_hub(
        path="/service-areas/",
        eyebrow="Service areas",
        h1="Statewide Texas,<br>six metros <em>constantly</em>",
        lede=("A hail file in Tarrant County and a surge file in Nueces County are different "
              "arguments, not the same page with the city name swapped. Each of these is written "
              "from what actually damages buildings there."),
        items=AREAS,
        intro_sections=sp.AREA_HUB_INTRO,
        trail=[("Home", "/"), ("Service areas", None)],
        title="Texas Service Areas | Commercial Public Adjusters Statewide",
        description=("Commercial and institutional claims consulting across Texas: Austin, "
                     "Houston, Dallas-Fort Worth, San Antonio, Corpus Christi and the Rio Grande "
                     "Valley."),
        card_mode="cards",
        schema=[itemlist_schema("/service-areas/", "Service areas",
                                [(a["nav_label"], a["path"]) for a in AREAS])],
    ))

    for idx, area in enumerate(AREAS):
        rel_inds = _rotate(INDUSTRIES, idx * 3 + 1, 3)
        rel_svc = _rotate(SERVICES, idx * 2, 4)
        perils = [(t, d) for t, d in area["perils"]]
        page = {
            "path": area["path"],
            "title": area["title"],
            "description": area["description"],
            "eyebrow": area["eyebrow"],
            "h1": area["h1"],
            "h1_plain": area["h1_plain"],
            "lede": area["lede"],
            "trail": [("Home", "/"), ("Service areas", "/service-areas/"),
                      (area["nav_label"], None)],
            "head_meta": ["Serving " + area["counties"], "Retained by either party",
                          "Statewide Texas response"],
            "schema": [service_schema(
                "Public insurance adjusting in %s" % area["city"],
                area["card_blurb"], area["path"], "Public Insurance Adjusting")],
            "faqs": area["faqs"],
            "sections": [
                {
                    "eyebrow": "What damages buildings here",
                    "h2": "The local perils, and what each one turns on.",
                    "blocks": [("steps", [(t, "<p>%s</p>" % d) for t, d in perils])],
                },
                {
                    "band": "paper2",
                    "eyebrow": "On the ground",
                    "h2": "What we see on %s files." % area["city"],
                    "blocks": list(area["local"]),
                    "aside": [
                        ("ledger", "Coverage", [
                            ("Metro", area["nav_label"]),
                            ("Counties", "See below"),
                            ("Property types", "Institutional"),
                            ("Response", "Same or next day"),
                            ("Fee", "Contingent"),
                            ("Licensing", "Tex. ch. 4102"),
                        ], "Serving " + area["counties"] + "."),
                    ],
                },
                {
                    "eyebrow": "Who we serve here",
                    "h2": "Institutional owners across the metro.",
                    "blocks": [
                        ("cards", [(i["card_title"], i["card_blurb"], i["path"]) for i in rel_inds]),
                    ],
                },
                {
                    "band": "ink",
                    "eyebrow": "Services",
                    "h2": "What we handle in %s." % area["city"],
                    "blocks": [
                        ("checks", ["<strong>%s</strong> &mdash; %s" % (s["nav_label"], s["card_blurb"])
                                    for s in rel_svc]),
                        ("html", '<div class="btn-row"><a class="btn btn--brass" href="/contact/">'
                                 'Discuss a matter <span class="arw">&rarr;</span></a>'
                                 '<a class="btn btn--ghost" href="/services/">All services</a></div>'),
                    ],
                },
            ],
        }
        write(area["path"], standard_page(page))

    # ------------------------------------------------------------------ blog
    postlist = "".join(
        '<a class="postitem" href="%s"><div class="pmeta"><b>%s</b>%s &middot; %s min</div>'
        '<div><h3>%s</h3><p>%s</p></div></a>'
        % (p["path"], p.get("category", "Claim strategy"),
           _month(p["published"]), p.get("read", "9"), p["h1_plain"], p["blurb"])
        for p in POSTS)

    blog_index = {
        "path": "/blog/",
        "title": "Insights | Texas Commercial Property Claims",
        "description": ("Articles on Texas commercial property insurance claims: statutory "
                        "deadlines, coinsurance, ordinance and law, business interruption, "
                        "appraisal and claim documentation."),
        "eyebrow": "Insights",
        "h1": "Notes from the<br><em>claims desk</em>",
        "h1_plain": "Insights",
        "lede": ("Policy wording, Texas statute and the arguments that move money on institutional "
                 "files. Written for the person who has to explain the claim to a board."),
        "trail": [("Home", "/"), ("Insights", None)],
        "page_type": "CollectionPage",
        "schema": [itemlist_schema("/blog/", "Articles",
                                   [(p["h1_plain"], p["path"]) for p in POSTS])],
        "sections": [
            {"blocks": [("html", '<div class="postlist">%s</div>' % postlist)]},
        ] + sp.BLOG_INTRO,
    }
    write("/blog/", standard_page(blog_index))

    for idx, post in enumerate(POSTS):
        related = _rotate([p for p in POSTS if p["slug"] != post["slug"]], idx, 3)
        page = dict(post)
        page["trail"] = [("Home", "/"), ("Insights", "/blog/"), (post["h1_plain"], None)]
        page["schema"] = [article_schema(post)]
        write(post["path"], article_page(page, related))

    # --------------------------------------------------------- static pages
    for page in (sp.ABOUT, sp.CLIENTS, sp.HOW_WE_WORK, sp.FEES_PAGE, sp.FAQ_PAGE,
                 sp.GLOSSARY, sp.CONTACT):
        write(page["path"], standard_page(page))

    for page in sp.LEGAL:
        p = dict(page)
        p["cta"] = {"heading": "Questions about any of this?",
                    "dek": "Call and ask. We would rather answer a question early than correct an "
                           "assumption late.",
                    "primary": ("Contact us", "/contact/"),
                    "secondary": ("About the firm", "/about/")}
        write(page["path"], standard_page(p))

    # -------------------------------------------------------------- sitemap
    write("/sitemap/", standard_page(_sitemap_page(render_blocks)))


def _month(iso):
    import datetime
    return datetime.date.fromisoformat(iso).strftime("%b %Y")


def _sitemap_page(render_blocks):
    def links(items, label_key="nav_label", desc_key="card_blurb"):
        return ("links", [(i[label_key], i[desc_key], i["path"]) for i in items])

    return {
        "path": "/sitemap/",
        "title": "Sitemap | %s" % BIZ["name"],
        "description": ("Every page on claimsconsultant.com in one place: property types, claim "
                        "services, calculators, service areas, articles and firm information."),
        "eyebrow": "Index",
        "h1": "Everything<br>on this <em>site</em>",
        "h1_plain": "Sitemap",
        "lede": "Fifty-odd pages, organised the way the practice is.",
        "trail": [("Home", "/"), ("Sitemap", None)],
        "page_type": "CollectionPage",
        "sections": [
            {"eyebrow": "Who we serve", "h2": "Property types",
             "blocks": [links(INDUSTRIES)]},
            {"band": "paper2", "eyebrow": "Services", "h2": "Claim services",
             "blocks": [links(SERVICES)]},
            {"eyebrow": "Tools", "h2": "Calculators",
             "blocks": [links(TOOLS)]},
            {"band": "paper2", "eyebrow": "Service areas", "h2": "Where we work",
             "blocks": [links(AREAS)]},
            {"eyebrow": "Insights", "h2": "Articles",
             "blocks": [("links", [(p["h1_plain"], p["blurb"], p["path"]) for p in POSTS])]},
            {"band": "paper2", "eyebrow": "The firm", "h2": "About, terms and reference",
             "blocks": [("links", [
                 ("About the firm", "Who we are, what we will not do, and how to check our license.", "/about/"),
                 ("How we work", "The method, stage by stage, with a typical timeline.", "/how-we-work/"),
                 ("Fees &amp; engagement", "Hourly and fixed fees, conflict checks and third-party costs.", "/fees/"),
                 ("Frequently asked questions", "What boards and councils ask in the first call.", "/faq/"),
                 ("Claims glossary", "Thirty terms that decide Texas commercial claims.", "/glossary/"),
                 ("Contact", "Run a conflict check, or just ask a question.", "/contact/"),
                 ("Privacy policy", "What this site collects, which is very little.", "/privacy-policy/"),
                 ("Terms of use", "The terms on which this site is published.", "/terms/"),
                 ("Disclaimer", "Licensing, scope of services and the limits of what is here.", "/disclaimer/"),
                 ("Accessibility", "Our approach, known limitations, and how to report a problem.", "/accessibility/"),
             ])]},
        ],
    }
