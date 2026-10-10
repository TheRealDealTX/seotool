# Post schema (one Python module per category: posts_<category_slug_with_underscores>.py)

```python
POSTS = [
    {
        "slug": "mason-jar-lanterns",            # lowercase-hyphen, keyword-led, unique site-wide
        "category": "diy-home-decor",            # one of the category slugs below
        "title": "DIY Mason Jar Lanterns for Cozy Evenings",   # <= 60 chars, contains the keyword
        "keyword": "mason jar lanterns",         # primary keyword (must appear in title, description, intro)
        "description": "...",                    # meta description, 140-160 chars
        "excerpt": "...",                        # 1-2 sentences for cards
        "date": "2026-08-14",                    # ISO date between 2026-06-01 and 2026-10-08
        "motif": "jar",                          # one of the MOTIFS below (drives the generated cover art)
        "difficulty": "Easy",                    # Easy | Moderate | Advanced
        "time": "45 minutes",
        "cost": "$10-$15",
        "intro": ["para", "para"],               # 2-3 paragraphs
        "materials": ["4 wide-mouth mason jars", "..."],
        "tools": ["Hot glue gun", "..."],
        "steps": [{"title": "Prep the jars", "body": "..."}],      # 5-8 steps, body 2-4 sentences
        "tips": ["...", "..."],                  # 3-5 tips
        "variations": [{"title": "...", "body": "..."}],           # 2-4
        "faq": [{"q": "...?", "a": "..."}],      # 3 questions
    },
]
```

Text fields are inserted as HTML: plain text, may use <em>, <strong>; escape & as &amp;.
Use straight ASCII quotes inside Python strings safely (prefer double-quoted Python strings and typographic apostrophes ’ in prose, or escape).

Categories: diy-home-decor, creative-crafts, christmas-crafts, halloween-crafts, thanksgiving-crafts, valentines-crafts, st-patricks-day-crafts

MOTIFS: frame, jar, plant, candle, pillow, flower, scissors, yarn, brush, ornament, tree, snowflake, wreath, gift, pumpkin, ghost, web, bat, leaf, acorn, heart, envelope, shamrock, rainbow, star
