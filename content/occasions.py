"""Occasion pages under /custom-banners/ - one per banner type.

Each entry: slug, label, nav_label, keyword, title, description, h1, intro,
sections (list of (heading, paragraphs)), ideas (list of wording ideas),
faqs, gallery (creation slugs to feature), icon (emoji used as a decorative
glyph in the cards).
"""

from siteconfig import BIZ

P = BIZ["phone_display"]

OCCASIONS = [
    {
        "slug": "birthday-banners",
        "label": "Birthday Banners",
        "nav_label": "Birthday",
        "icon": "🎂",
        "keyword": "custom birthday banner",
        "title": "Custom Hand-Painted Birthday Banners | Belton Banners",
        "description": "Custom hand-painted birthday banners from Belton, TX. Names, ages, hobbies and themes painted by hand on kraft paper. Kids', milestone and 21st birthdays.",
        "h1": "Custom Birthday Banners, Painted by Hand",
        "intro": "A birthday banner should look like the person it is for. Christina Dittman Creations paints birthday banners from scratch: the name, the age and the things they love, lettered and illustrated by hand on kraft paper. These are the Belton banners that end up framed after the party instead of in the recycling.",
        "sections": [
            ("Kids' birthday banners", [
                "First birthdays, second birthdays, turning five. A kids' banner carries the theme of the party: construction trucks and a road-striped number for a dig-site party, ladybugs and gingham for a garden tea, planets and shooting stars for a space theme. The wording stays short so it reads from across the room and photographs well behind the cake.",
            ]),
            ("Milestone birthdays", [
                "Eighteenth, twenty-first, thirtieth, fortieth, fiftieth. Milestone banners lean into personality: a camo border with boots and a cowboy hat, a pair of clinking cans, a cowgirl portrait, a favorite drink. Tell us about the person and the details take care of themselves.",
            ]),
            ("What goes on a birthday banner", [
                "Most birthday banners start with the greeting and the name, then build out with three to six illustrations of hobbies, pets, sports, favorite foods or an inside joke. Colors are matched to the party palette or chosen to pop against the kraft background. If the party has a theme, the banner follows it.",
            ]),
        ],
        "ideas": ["Happy Birthday + first name in script", "Name + 'turning 5' with a themed number", "Happy 21st Birthday + name", "Cheers to 30 / 40 / 50 years", "One in a melon / Two sweet / Wild one", "Hobby collage around the greeting"],
        "faqs": [
            ("How far ahead should I order a birthday banner?", "Two to three weeks ahead is comfortable. Shorter timelines are often possible depending on the current queue, so ask - call or text " + P + "."),
            ("Can you match my party colors?", "Yes. Send a photo of the invitation, the cake or the decorations and the palette is matched to it."),
            ("What size is a typical birthday banner?", "Most birthday banners are 36\" x 30\" or 48\" x 30\" and hang behind the cake or gift table. Larger 60\" x 30\" and 36\" x 60\" sizes work for photo backdrops."),
        ],
        "gallery": ["custom-hand-painted-birthday-banner", "custom-hand-painted-birthday-banner-2", "custom-hand-painted-birthday-banner-4", "custom-hand-painted-birthday-banner-5", "custom-hand-painted-birthday-banner-6", "custom-hand-painted-birthday-banner-3"],
    },
    {
        "slug": "wedding-banners",
        "label": "Wedding Banners",
        "nav_label": "Wedding",
        "icon": "💍",
        "keyword": "hand painted wedding banner",
        "title": "Hand-Painted Wedding Banners & Welcome Signs | Belton Banners",
        "description": "Hand-painted wedding banners, welcome signs and sweetheart-table backdrops from Christina Dittman Creations in Belton, TX. Names, dates and vows by hand.",
        "h1": "Hand-Painted Wedding Banners & Welcome Signs",
        "intro": "A wedding banner does three jobs at once: it welcomes guests, it anchors the photos and it becomes the keepsake you hang at home afterward. Christina Dittman Creations hand-letters wedding banners for ceremonies, receptions, rehearsal dinners, engagement parties and bridal showers across Belton and Central Texas.",
        "sections": [
            ("Welcome signs and ceremony backdrops", [
                "A welcome banner with your names and the date sets the tone at the entrance. For the ceremony itself, a wide banner behind the altar or arbor carries a verse, a line from your vows or simply your names and the date in flowing script.",
            ]),
            ("Sweetheart table and reception banners", [
                "Behind the sweetheart table is where the banner gets photographed most. Keep the wording short - 'The Smiths', 'Better Together', 'Welcome to Our Forever' - and let the florals, greenery or a monogram do the decorating.",
            ]),
            ("Engagement parties and bridal showers", [
                "Engagement and shower banners are a little more playful: 'She said yes', 'From Miss to Mrs', the couple's names with the proposal date, or a motif tied to the shower theme.",
            ]),
        ],
        "ideas": ["Welcome to Our Forever", "The + last name + wedding date", "Better Together", "She said yes!", "From Miss to Mrs", "A verse or a line from the vows"],
        "faqs": [
            ("Can the banner be painted on white or cream instead of kraft paper?", "Yes. Kraft paper is the signature look, but white, cream and other paper colors are available for weddings and showers."),
            ("Will the banner survive an outdoor ceremony?", "A banner is fine under a tent or on a covered porch. For open-air ceremonies, plan to hang it just before and take it down after; heavy wind and rain are the only real enemies."),
            ("Can I keep it after the wedding?", "That is the idea. Roll it (never fold it) and store it dry, or frame it as wall art."),
        ],
        "gallery": ["custom-painted-verse-banner", "custom-painted-verse-banner-5", "hand-painted-over-then-moon-banner"],
    },
    {
        "slug": "baby-shower-banners",
        "label": "Baby Shower Banners",
        "nav_label": "Baby Shower",
        "icon": "🌙",
        "keyword": "baby shower banner",
        "title": "Custom Baby Shower & Gender Reveal Banners | Belton Banners",
        "description": "Hand-painted baby shower, gender reveal and welcome-baby banners from Belton, TX. Over the Moon, woodland, floral and more by Christina Dittman Creations.",
        "h1": "Baby Shower & Gender Reveal Banners",
        "intro": "Baby showers are made for hand-painted banners: soft colors, a name or a theme, and something the parents can hang in the nursery afterward. Christina Dittman Creations paints shower, sprinkle, gender-reveal and welcome-home banners for families in Belton and the surrounding area.",
        "sections": [
            ("Popular baby shower themes", [
                "'Over the Moon' with planets and shooting stars, 'Twinkle Twinkle Little Star', woodland animals, wildflowers, bees and honey, 'A little pumpkin is on the way' for fall showers. If the nursery has a theme, the banner can match it so it moves straight from the party to the wall.",
            ]),
            ("Gender reveals", [
                "A reveal banner can keep the secret - 'He or She? Come See!' - or announce it in pink or blue script once the moment has passed. Some families order a two-part banner: the question for the party and the answer for the photos.",
            ]),
            ("Name banners for the nursery", [
                "A name banner painted for the shower doubles as nursery art. Soft neutral lettering with a small illustration keeps it calm enough for a bedroom wall.",
            ]),
        ],
        "ideas": ["Over the Moon for Baby + name", "Oh baby!", "Twinkle twinkle little star", "He or She? Come see!", "Welcome home + name", "A little pumpkin is on the way"],
        "faqs": [
            ("Can you keep the baby's name a secret until the shower?", "Yes. Share the name privately and it stays between you and the artist until the banner is unveiled."),
            ("What colors work for a gender-neutral shower?", "Sage, mustard, terracotta, cream and soft blue all read beautifully on kraft paper and keep the banner neutral."),
            ("Can the banner be used again for a first birthday?", "Name banners and theme banners without a date often come back out for the first birthday. Store it rolled and dry in between."),
        ],
        "gallery": ["hand-painted-over-then-moon-banner", "custom-hand-painted-birthday-banner-2"],
    },
    {
        "slug": "church-banners",
        "label": "Church & Scripture Banners",
        "nav_label": "Church",
        "icon": "✝️",
        "keyword": "church banners",
        "title": "Hand-Painted Church Banners & Scripture Banners | Belton Banners",
        "description": "Hand-painted church banners and scripture verse banners for children's church, Easter, Christmas, VBS and sermon series. Painted in Belton, TX.",
        "h1": "Church Banners & Scripture Verse Banners",
        "intro": "Scripture banners are a large part of what Christina Dittman Creations paints. Children's church lessons, Easter and Christmas services, Thanksgiving, Valentine's lessons, VBS weeks and sermon series all get a hand-lettered verse with illustrations that help kids remember it. Churches in Belton, Temple, Killeen and across Bell County hang these banners on classroom walls, stages and fellowship halls.",
        "sections": [
            ("Children's church banners", [
                "A children's church banner carries the week's verse in large, readable lettering with a scene that tells the story: the empty tomb with butterflies for 'He is risen', a mailbox full of painted envelopes for 'God's love letters to you', a praying cowboy and a cornucopia for a Thanksgiving psalm. Portrait banners suit classroom walls; wide banners suit a stage.",
            ]),
            ("Seasonal services", [
                "Easter, Christmas, Thanksgiving and Valentine's lessons each get their own look. A Christmas banner might carry Luke 2:11 over a nativity silhouette, or Isaiah 9:6 with the letters of CHRISTMAS picked out in gold as an acrostic. Fall banners pair a verse with sunflowers, pumpkins and a rope frame.",
            ]),
            ("Verse banners for home", [
                "Not every scripture banner is for a church. Families order verse banners for a living room, a nursery, a graduation party or a baptism, and they are painted with the same care.",
            ]),
        ],
        "ideas": ["Rejoice, for He is risen - Matthew 28:6", "God's love letters to you", "Love the Lord your God - Mark 12:30", "Seasons change but Jesus Christ remains the same - Hebrews 13:8", "For unto you is born this day - Luke 2:11", "With all my heart I will thank the Lord - Psalm 111:1"],
        "faqs": [
            ("Can you paint a banner for a whole sermon series?", "Yes. A series banner usually carries the series title with room for the week's verse, or a set of smaller banners painted in one style."),
            ("Do you paint banners for VBS?", "Yes. Send the VBS theme artwork and the banner is painted to match it, with the theme verse front and center."),
            ("How big can a church banner be?", "Standard sizes run up to 60\" x 30\" and 36\" x 60\". Larger stage banners are possible on request."),
        ],
        "gallery": ["childrens-church-hand-painted-banner", "childrens-church-hand-painted-banner-2", "custom-painted-verse-banner-4", "custom-painted-verse-banner", "custom-painted-verse-banner-2", "custom-painted-verse-banner-3"],
    },
    {
        "slug": "graduation-banners",
        "label": "Graduation Banners",
        "nav_label": "Graduation",
        "icon": "🎓",
        "keyword": "graduation banner",
        "title": "Custom Graduation Banners, Hand-Painted | Belton Banners",
        "description": "Hand-painted graduation banners for high school, college and kindergarten grads in Belton, Temple and Killeen, TX. School colors, names and class years.",
        "h1": "Custom Graduation Banners in School Colors",
        "intro": "A graduation banner says the name, the school and the year, in the school's colors, with whatever the graduate is proudest of painted around it. Christina Dittman Creations paints graduation banners for Belton, Temple, Killeen and Central Texas grads, from kindergarten send-offs to college commencements.",
        "sections": [
            ("High school and college graduates", [
                "School colors and a mascot, the class year, the graduate's name and the next step: a college logo, a branch of service, a trade. Senior-night and graduation-party banners hang behind the dessert table and come home afterward.",
            ]),
            ("Little graduates", [
                "Kindergarten and pre-K graduations get a banner too - a cap, a diploma, the child's name and 'Off to first grade'.",
            ]),
            ("Wording that works", [
                "'Congrats Grad', 'Class of 2026', 'She did it', 'The tassel was worth the hassle', or a verse or quote the graduate has chosen. Short wording reads better from across a gym or a backyard.",
            ]),
        ],
        "ideas": ["Congrats + name, Class of 2026", "The tassel was worth the hassle", "Off to + college name", "She did it / He did it", "Kindergarten graduate!", "Proverbs 3:5-6 or Jeremiah 29:11"],
        "faqs": [
            ("Can you match our school colors exactly?", "Send the school's colors or a photo of a jersey and the paint is mixed to match."),
            ("We have several graduation parties in May - can you handle a group order?", "Yes. Group orders from a church, a team or a group of families are welcome; ask early because May books up."),
            ("Can the banner include a photo?", "Painted portraits and illustrations are possible; printed photos are not glued onto banners."),
        ],
        "gallery": ["custom-hand-painted-birthday-banner-5", "custom-hand-painted-birthday-banner-3", "custom-painted-verse-banner"],
    },
    {
        "slug": "holiday-seasonal-banners",
        "label": "Holiday & Seasonal Banners",
        "nav_label": "Seasonal",
        "icon": "🍂",
        "keyword": "seasonal banners",
        "title": "Hand-Painted Holiday & Seasonal Banners | Belton Banners",
        "description": "Hand-painted fall, Christmas, Easter, Thanksgiving and Valentine's banners from Belton, TX. Porch, classroom and church banners by Christina Dittman Creations.",
        "h1": "Holiday & Seasonal Banners, Painted for the Season",
        "intro": "Some banners come out every year. A 'Happy Fall' banner for the porch, a Christmas verse for the entryway, an Easter banner for the classroom. Christina Dittman Creations paints seasonal banners that are decorative enough for a home and durable enough to reuse season after season.",
        "sections": [
            ("Fall and Thanksgiving", [
                "Pumpkins, sunflowers, acorns, falling leaves, cornucopias, a rope frame and a cowboy hat. Fall banners pair naturally with a verse about gratitude or simply 'Happy Fall, Y'all'.",
            ]),
            ("Christmas", [
                "Nativity silhouettes, pine branches with red berries, holly, a star, and a verse from Luke 2 or Isaiah 9 in script. Christmas banners work for a mantel, a church lobby or a classroom door.",
            ]),
            ("Easter, Valentine's and spring", [
                "Butterflies, wildflowers, the empty tomb, hearts and love letters. Spring banners are bright and soft at the same time, and they photograph well in natural light.",
            ]),
        ],
        "ideas": ["Happy Fall, Y'all", "Give thanks", "Seasons change but Jesus Christ remains the same", "Joy to the world", "He is risen", "Love one another"],
        "faqs": [
            ("Can I use a seasonal banner outdoors on the porch?", "On a covered porch, yes. Bring it in for rain and heavy wind, and it will last for years."),
            ("Can you paint on something other than kraft paper?", "Grey, white and cream paper are available. Ask about canvas for a banner that will be hung outside more often."),
            ("How do I store it between seasons?", "Roll it around a cardboard tube with the painted side out, wrap it loosely, and keep it somewhere dry."),
        ],
        "gallery": ["custom-painted-fall-banner", "custom-painted-verse-banner-5", "custom-painted-verse-banner-2", "custom-painted-verse-banner-3", "childrens-church-hand-painted-banner"],
    },
]

BY_SLUG = {o["slug"]: o for o in OCCASIONS}
