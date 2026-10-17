# Live-Style rebuild — content brief for writers

Site: live-style.co.uk — a UK (London-based) interiors, design & lifestyle magazine/blog.
It ran 2013–2016. We are rebuilding it with fresh, original writing at the SAME URLs.
Voice: warm, curious, design-literate British editorial voice ("we" / "us" = the Live-Style
editors). British spelling (colour, favourite, neighbourhood). Do NOT write as a named real
person and never claim to be "Anna" or any real blogger. No fake quotes from real people,
no invented prices, opening hours, addresses, statistics or awards. If you aren't sure a fact
is true, verify it with WebSearch or leave it out. Shops/brands that have since closed or changed:
check and, where relevant, mention it in a light "Looking back" note rather than presenting
stale info as current.

## Output format (Python module, must import cleanly)

Write a file at the path you are given, containing exactly:

```python
POSTS = [
    {
        "path": "/2013/06/30/open-shelving-in-kitchens/",   # exactly as given
        "date": "2013-06-30",                                # from the URL; for non-dated paths use the date given
        "title": "Open Shelving in Kitchens",               # H1. Must naturally contain the primary keyword
        "seo_title": "Open Shelving in Kitchens: Ideas & Styling Tips",   # <= 55 chars, contains keyword; " | Live-Style" is appended automatically
        "description": "...",                               # 140-158 chars, contains keyword
        "category": "Interiors",                            # one of the categories listed below
        "tags": ["Kitchens", "Shelving"],                   # 2-5 human-readable tag names
        "image": "open-shelving-kitchen.jpg",               # exactly the filename given to you
        "image_alt": "...",                                  # describe what the given photo shows (described below), relevant to topic
        "excerpt": "...",                                    # 1-2 sentences, <= 200 chars
        "body": """<p>...</p>...""",                         # HTML, see rules
        "faq": [("Question?", "Answer.")],                   # 2-4 Q&As targeting the keywords; plain text answers
    },
]
```

Body HTML rules: 650-950 words. Allowed tags only: p, h2, h3, ul, ol, li, strong, em, blockquote, a.
Start with 1-2 paragraphs (no heading first). Use 3-5 h2 sections. Use ONE `<blockquote>` as a pull-quote
(our own words, not a quote attributed to a real person). Add 2-3 internal links using
`<a href="/path/">anchor</a>` to OTHER paths from the master list below (use natural anchors).
No external links. No images. No inline styles. Use the primary + secondary keywords naturally
(primary in the first 100 words and in at least one h2), no stuffing. Escape `&` as `&amp;`.
Use straight double quotes only inside HTML attributes; avoid using `"""` inside the body.

Categories (use exactly): Interiors, Design & Makers, Art & Prints, Food & Drink, Places,
Renovation Diary, Shopping, January Cure, Lifestyle

## Master list of every article path on the site (for internal linking)
/2013/06/30/open-shelving-in-kitchens/  (open shelving in kitchens)
/2013/07/14/my-live-style-challenge-favourite-restaurants/  (favourite London restaurants)
/2013/08/25/swedish-charms/  (Swedish / Scandinavian style)
/2013/08/28/stunning-lighting-by-bocci-exclusively-for-heals/  (Bocci lighting at Heal's)
/2013/08/29/101-things-i-learned-in-architecture-school/  (book)
/2013/09/27/eleanor-pritchard-textiles/  (blankets)
/2013/09/28/introducing-made-by-jason/  (furniture maker)
/2013/10/20/house-of-twenty/
/2013/11/10/outline-editions/  (Noma Bar prints)
/2013/11/18/cubit-shelving/
/2013/11/26/carine-roitfeld-irreverent/  (book)
/2013/11/28/open-studio-and-christmas-fair-in-london/
/2014/01/02/west-elm-london/
/2014/01/03/apartment-therapy-january-cure/
/2014/01/26/home-with-house-of-fraser/  (Christiane Lemieux / Pied-à-terre)
/2014/02/02/two-east-london-hotspots/  (Sushisamba / Shoreditch)
/2014/02/16/apartment-therapys-january-cure-better-late-than-never/
/2014/03/28/comic-art-ltd-by-john-patrick-reynolds/
/2014/06/06/the-weekly-crave-heavenly-hammocks/
/2014/07/04/nigella-lawson-almond-cake-recipe/
/2014/09/19/alberto-alessi-living-on-the-line/
/2014/10/18/back-online-with-kakkoii-pantone-speakers/
/2015/07/16/final-paint-selections/  (Little Greene paints)
/2016/01/07/a-p-c-in-the-house/
/2016/01/08/aram-store/
/2016/01/15/one-partially-failed-diy-and-one-gorgeous-runner/  (Roger Oates runner)
/2016/01/22/end-of-sale-edit/
/2016/01/22/end-of-sale-edit/christine-lemieux/
/2016/01/31/why-its-important-to-take-your-pleasure-seriously/
/2016/02/02/bbc2-great-interior-design-challenge-tennis-racket-upcycle/
/2016/04/08/pick-me-up-graphic-arts-festival/
