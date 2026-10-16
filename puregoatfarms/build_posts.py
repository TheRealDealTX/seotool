#!/usr/bin/env python3
"""Build the publish payload for puregoatfarms.com.

Writes payload.json containing:
  posts  - three new Milking & Dairy articles as Gutenberg block HTML
           (title, slug, excerpt, meta description, focus keyword, categories)
  edits  - contextual internal links to splice into the two existing posts
           (exact search string -> replacement; applied only when the search
           string occurs exactly once, see publish.php)

Why these three articles: the Search Console export (2026-07-16 to 2026-10-16)
shows the site earning impressions, but no clicks, for three query clusters
that the existing "how much milk can a goat give at once" post only half
answers:

  per-day yield / by breed   how much milk does a goat produce (a day),
                             goat milk production (per day), saanen / alpine /
                             nubian goat milk production per day
  lactation / "all the time" do goats produce milk all the time, ... without
                             being pregnant, do all goats produce milk,
                             do goats make milk, how long do goats produce milk
  milking frequency          how often do you milk a goat, how often can you /
                             do you need to milk a goat

Each cluster gets its own article with the query phrasing in the title, H1,
first paragraph, an H2 and the FAQ, and every article links to the others and
to the two existing posts so the five pages form one Milking & Dairy cluster.
"""

import json
import os
import re

ORIGIN = "https://puregoatfarms.com"

# Existing content
MILK_AT_ONCE = f"{ORIGIN}/how-much-milk-can-a-goat-really-give-at-once/"
CHEESE = f"{ORIGIN}/how-many-goats-do-you-need-to-make-cheese/"
CAT_BREEDS = f"{ORIGIN}/category/goat-breeds/"
CAT_HEALTH = f"{ORIGIN}/category/health-care/"
MILK_AT_ONCE_ID = 60
CHEESE_ID = 134

# New content
PER_DAY_SLUG = "how-much-milk-does-a-goat-produce-per-day"
ALL_TIME_SLUG = "do-goats-produce-milk-all-the-time"
HOW_OFTEN_SLUG = "how-often-do-you-milk-a-goat"
PER_DAY = f"{ORIGIN}/{PER_DAY_SLUG}/"
ALL_TIME = f"{ORIGIN}/{ALL_TIME_SLUG}/"
HOW_OFTEN = f"{ORIGIN}/{HOW_OFTEN_SLUG}/"

# WordPress category IDs on the live site
CAT_ID = {"milking-dairy": 6, "farm-life": 5, "goat-breeds": 8, "health-care": 7}


# --------------------------------------------------------------------------
# Block helpers. Output is the same markup the block editor saves, so the
# posts stay editable in wp-admin.
# --------------------------------------------------------------------------

def p(html):
    return f"<!-- wp:paragraph -->\n<p>{html}</p>\n<!-- /wp:paragraph -->"


def h2(text, anchor=None):
    a = f' id="{anchor}"' if anchor else ""
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading"{a}>{text}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{text}</h3>\n<!-- /wp:heading -->'


def ul(items):
    lis = "\n".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items)
    return f"<!-- wp:list -->\n<ul class=\"wp-block-list\">\n{lis}\n</ul>\n<!-- /wp:list -->"


def ol(items):
    lis = "\n".join(f"<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->" for i in items)
    return f"<!-- wp:list {{\"ordered\":true}} -->\n<ol class=\"wp-block-list\">\n{lis}\n</ol>\n<!-- /wp:list -->"


def table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = "\n".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (
        '<!-- wp:table {"hasFixedLayout":true} -->\n'
        f'<figure class="wp-block-table"><table class="has-fixed-layout"><thead><tr>{th}</tr></thead>'
        f"<tbody>\n{body}\n</tbody></table></figure>\n<!-- /wp:table -->"
    )


def a(href, text):
    return f'<a href="{href}">{text}</a>'


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def faq(items, base_id):
    """Yoast FAQ block. The block attributes carry the questions, which is
    what Yoast reads to emit FAQPage schema; the HTML is the saved output."""
    questions = []
    html = []
    for i, (q, ans) in enumerate(items, 1):
        qid = f"faq-question-{base_id}{i:02d}"
        questions.append(
            {
                "id": qid,
                "question": [q],
                "answer": [ans],
                "jsonQuestion": strip_tags(q),
                "jsonAnswer": ans,
            }
        )
        html.append(
            f'<div class="schema-faq-section" id="{qid}"><strong class="schema-faq-question">{q}</strong> '
            f'<p class="schema-faq-answer">{ans}</p> </div>'
        )
    attrs = json.dumps({"questions": questions}, ensure_ascii=False)
    # Yoast's own save() puts everything on one line inside the wrapper div.
    return (
        f"<!-- wp:yoast/faq-block {attrs} -->\n"
        f'<div class="schema-faq wp-block-yoast-faq-block">{" ".join(html)} </div>\n'
        "<!-- /wp:yoast/faq-block -->"
    )


def related(links):
    return h2("Keep Reading") + "\n\n" + ul([a(href, text) for href, text in links])


def join(*blocks):
    return "\n\n".join(blocks)


# --------------------------------------------------------------------------
# Article 1 - per-day yield by breed
# --------------------------------------------------------------------------

def article_per_day():
    title = "How Much Milk Does a Goat Produce Per Day? Real Numbers by Breed"
    content = join(
        p(
            "If you are asking <strong>how much milk does a goat produce</strong> in a day, the short answer "
            "is that a standard-size dairy goat in good condition gives about 6 to 8 pounds of milk per day, "
            "which is roughly three quarters of a gallon to one gallon. Small breeds give less, top-producing "
            "does give more, and every goat gives more in week six of lactation than she does in month eight."
        ),
        p(
            "That one-line answer hides a lot of variation, so this guide lays out the real numbers: daily "
            "goat milk production by breed, how the amount changes across a lactation, what you actually get "
            "in the bucket once kids take their share, and what a single goat adds up to over a year."
        ),
        p(
            f"If you want to know how much comes out in one milking session rather than a full day, we cover "
            f"that separately in {a(MILK_AT_ONCE, 'how much milk a goat can really give at once')}."
        ),
        h2("Quick Answer: How Much Milk Does a Goat Produce a Day?"),
        p(
            "Most full-size dairy goats produce 6 to 8 pounds of milk per day across a lactation, with peaks of "
            "10 to 12 pounds or more in a strong doe. Nigerian Dwarf goats produce about 2 to 4 pounds per day. "
            "One gallon of goat milk weighs about 8.6 pounds, so an average dairy doe gives close to a gallon a "
            "day at her best and closer to half a gallon late in lactation."
        ),
        table(
            ["Type of goat", "Typical daily yield", "In gallons", "In liters"],
            [
                ["Nigerian Dwarf or other miniature breed", "2 to 4 pounds", "1 to 2 quarts", "1 to 2 liters"],
                ["Average full-size dairy doe", "6 to 8 pounds", "0.7 to 0.9 gallon", "2.7 to 3.6 liters"],
                ["Strong producer at peak", "10 to 12 pounds", "1.2 to 1.4 gallons", "4.5 to 5.4 liters"],
                ["Exceptional doe, proven dairy lines", "14 to 20+ pounds", "1.6 to 2.3+ gallons", "6 to 9+ liters"],
                ["Meat or fiber breed (Boer, Kiko, Angora)", "1 to 3 pounds", "Up to about 1.5 quarts", "Up to about 1.4 liters"],
            ],
        ),
        p(
            "These are planning ranges, not promises. Breed sets the ceiling, and genetics, feed, water, milking "
            "schedule, health, and stage of lactation decide how close a goat gets to it."
        ),
        h2("Goat Milk Production by Breed", "by-breed"),
        p(
            "The breed question is the one we hear most, so here are the daily ranges we would plan around for "
            "each of the common dairy breeds. The numbers describe a healthy doe in her second lactation or "
            "later, milked twice a day with no kids nursing. First fresheners usually land near the bottom of "
            "each range."
        ),
        table(
            ["Breed", "Typical daily yield", "Peak daily yield", "Butterfat", "Best known for"],
            [
                ["Saanen", "8 to 11 pounds (1 to 1.3 gallons)", "12 to 18+ pounds", "3 to 3.5%", "Highest volume of any breed"],
                ["Alpine", "7 to 10 pounds (0.8 to 1.2 gallons)", "12 to 16 pounds", "3.5%", "Steady volume over a long lactation"],
                ["LaMancha", "7 to 9 pounds (0.8 to 1 gallon)", "10 to 14 pounds", "4%", "Good volume with richer milk"],
                ["Toggenburg", "7 to 9 pounds (0.8 to 1 gallon)", "10 to 14 pounds", "3.5%", "Persistent, long lactations"],
                ["Oberhasli", "6 to 8 pounds (0.7 to 0.9 gallon)", "9 to 12 pounds", "3.5 to 4%", "Sweet, mild milk"],
                ["Nubian", "5 to 8 pounds (0.6 to 0.9 gallon)", "8 to 12 pounds", "4.5 to 5%", "Rich milk for cheese and soap"],
                ["Nigerian Dwarf", "2 to 4 pounds (1 to 2 quarts)", "4 to 6 pounds", "6 to 7%", "Highest butterfat, small size"],
                ["Mini breeds (Mini Nubian, Mini Alpine)", "4 to 6 pounds (0.5 to 0.7 gallon)", "6 to 8 pounds", "4.5 to 6%", "Middle ground on size and volume"],
            ],
        ),
        h3("Saanen goat milk production per day"),
        p(
            "Saanens are the volume breed. A good Saanen doe gives 8 to 11 pounds a day for most of her "
            "lactation, which is a gallon or more, and proven does at peak can top 2 gallons. Their milk runs "
            "lower in butterfat, around 3 to 3.5 percent, so it drinks light and makes a softer, higher-yield "
            "fresh cheese. If the goal is the most milk per goat, this is the breed to start with."
        ),
        h3("Alpine goat milk production per day"),
        p(
            "Alpines sit just behind Saanens on volume, usually 7 to 10 pounds a day, and they are known for "
            "holding production late into lactation. Many Alpines will still give half a gallon a day at month "
            "nine when other breeds have tapered off. Butterfat is around 3.5 percent."
        ),
        h3("How much milk do Nubian goats produce?"),
        p(
            "A Nubian doe typically gives 5 to 8 pounds a day, so a bit less than the Swiss breeds, but her milk "
            "is noticeably richer at 4.5 to 5 percent butterfat. That matters if cheese, yogurt, or soap is the "
            f"goal, because richer milk yields more finished cheese per gallon. Our note on "
            f"{a(CHEESE, 'how many goats you need to make cheese')} walks through those yields."
        ),
        h3("How much milk does a Nigerian Dwarf goat produce?"),
        p(
            "Nigerian Dwarfs give 2 to 4 pounds a day, call it a quart to half a gallon, with exceptional does "
            "reaching 6 pounds at peak. The trade-off is butterfat of 6 percent or more, the highest of any "
            "breed, which is why so many small homesteads keep two or three Nigerians instead of one full-size "
            "doe. They also breed year-round, so staggered kiddings can keep milk in the fridge all year."
        ),
        h3("LaMancha, Toggenburg, and Oberhasli"),
        p(
            "The three remaining standard breeds all land in the 6 to 9 pound range. LaManchas pair solid "
            "volume with 4 percent butterfat and a calm temperament. Toggenburgs are famous for persistence, "
            "meaning they decline slowly after peak. Oberhaslis give a little less volume but very mild-tasting "
            f"milk. For a fuller picture of build and temperament, browse our {a(CAT_BREEDS, 'goat breed notes')}."
        ),
        h2("Daily Yield vs. Per Milking vs. Per Lactation"),
        p(
            "People mix up three different measurements when they talk about goat milk production. A goat that "
            "gives 8 pounds a day, milked twice a day, gives about 4 pounds per milking, and over a 10-month "
            "lactation she adds up to roughly 2,400 pounds, or about 280 gallons."
        ),
        table(
            ["Measurement", "What it means", "Example for an average doe"],
            [
                ["Per milking", "Milk collected in one session", "3 to 4 pounds (about 1.5 to 2 quarts)"],
                ["Per day", "Total over 24 hours, usually two milkings", "6 to 8 pounds (about 0.75 to 1 gallon)"],
                ["Per week", "Seven days of production", "42 to 56 pounds (about 5 to 6.5 gallons)"],
                ["Per lactation", "Total over about 10 months (305 days)", "1,800 to 2,500 pounds (about 210 to 290 gallons)"],
            ],
        ),
        p(
            "Handy conversions: 1 gallon of goat milk is about 8.6 pounds, 3.8 liters, or 16 cups. One quart is "
            "about 2.15 pounds. When a breeder quotes production in pounds, divide by 8.6 to get gallons."
        ),
        h2("How Production Changes Across a Lactation"),
        p(
            "A goat does not give the same amount every day. Production climbs for the first several weeks "
            "after kidding, peaks somewhere between week four and week eight, holds for a while, and then "
            "declines gradually until the doe is dried off about two months before her next kidding."
        ),
        table(
            ["Stage", "Weeks after kidding", "Share of peak yield", "Average doe (8 lb peak)"],
            [
                ["Colostrum and early rise", "Weeks 1 to 3", "60 to 85%", "5 to 7 pounds"],
                ["Peak", "Weeks 4 to 8", "100%", "8 pounds"],
                ["Mid lactation", "Weeks 9 to 24", "75 to 90%", "6 to 7 pounds"],
                ["Late lactation", "Weeks 25 to 40", "40 to 65%", "3 to 5 pounds"],
                ["Drying off", "Weeks 41 to 44", "Tapering to zero", "0 to 2 pounds"],
            ],
        ),
        p(
            f"A goat is a seasonal producer, not a tap. We explain the whole cycle, including the dry period "
            f"and milking through without rebreeding, in {a(ALL_TIME, 'do goats produce milk all the time?')}"
        ),
        h2("What Changes How Much Milk a Goat Gives"),
        h3("Age and lactation number"),
        p(
            "First fresheners give the least. Production typically rises through the second and third "
            "lactation and peaks around the third to fifth, then holds or declines slowly. A two-year-old "
            "Nubian giving 5 pounds a day may well give 7 or 8 as a four-year-old."
        ),
        h3("Genetics"),
        p(
            "Two does of the same breed can differ by half. A doe from a line with milk records behind her "
            "will nearly always outperform a doe bought on looks. If you buy for milk, ask to see the dam "
            "milked or ask for test-day records."
        ),
        h3("Feed and water"),
        p(
            "Milk is mostly water, so a doe without clean water in front of her all day drops quickly. After "
            "that, good hay or browse plus a dairy ration fed on the stand sets the ceiling. A rule of thumb "
            "many herds use is about 1 pound of grain for every 3 pounds of milk, adjusted to body condition."
        ),
        h3("Milking schedule"),
        p(
            f"Milking twice a day about 12 hours apart gets the most out of a goat. Once-a-day milking is "
            f"workable but usually costs 15 to 30 percent of the volume. We compare the options in "
            f"{a(HOW_OFTEN, 'how often do you milk a goat?')}"
        ),
        h3("Kids on the doe"),
        p(
            "If kids are nursing, they take their share first. A doe raising twins may be producing a gallon "
            "and leaving you with a quart. Separating kids overnight and milking in the morning is the usual "
            "compromise."
        ),
        h3("Health"),
        p(
            f"Parasites, mastitis, mineral shortfalls, and heat stress all show up in the bucket before they "
            f"show up anywhere else. A sudden drop in one doe is a reason to check her, not the feed bin. Our "
            f"{a(CAT_HEALTH, 'health and care notes')} cover what to look for."
        ),
        h2("How Much Milk Does One Goat Produce in a Year?"),
        p(
            "Because a doe milks for about 10 months and then rests for two, a year of production is really a "
            "lactation of production. Multiply the average daily yield by roughly 300 days."
        ),
        table(
            ["Goat", "Average daily yield", "Milk per lactation (about 300 days)"],
            [
                ["Nigerian Dwarf", "3 pounds", "About 900 pounds, or 105 gallons"],
                ["Nubian", "6.5 pounds", "About 1,950 pounds, or 225 gallons"],
                ["LaMancha, Toggenburg, Oberhasli", "7.5 pounds", "About 2,250 pounds, or 260 gallons"],
                ["Alpine", "8.5 pounds", "About 2,550 pounds, or 295 gallons"],
                ["Saanen", "9.5 pounds", "About 2,850 pounds, or 330 gallons"],
            ],
        ),
        p(
            "National top producers in the dairy breeds record 4,000 to 6,000 pounds in a lactation, but those "
            "are show-ring outliers with intensive feeding. Plan around the table, and be pleased if a doe "
            "beats it."
        ),
        h2("What You Actually Get in the Bucket"),
        p(
            "Daily production and usable milk are not the same number. Subtract what the kids drink, the "
            "first squirts you strip to check for mastitis, and any milk you discard during a medication "
            "withdrawal. A realistic household plan looks like this:"
        ),
        table(
            ["Situation", "Doe produces", "You collect"],
            [
                ["Kids weaned, milked twice daily", "8 pounds", "About 8 pounds (just under 1 gallon)"],
                ["Kids separated at night, milked once in the morning", "8 pounds", "About 3 to 4 pounds (about 2 quarts)"],
                ["Kids on the doe full time, no separation", "8 pounds", "Often under 1 pound"],
            ],
        ),
        p(
            "For a family of four that drinks milk daily and makes a little cheese or yogurt, one strong "
            "full-size doe or two to three Nigerians in milk is usually enough. For regular cheesemaking, see "
            f"{a(CHEESE, 'how many goats you need to make cheese')} for the herd math."
        ),
        h2("What We See on Our Own Stand"),
        p(
            "Our dairy line is Nubian and Nigerian Dwarf, so we live at the rich-milk end of these tables. A "
            "Nubian doe in her second or third lactation settles in around 6 to 7 pounds a day for us at peak, "
            "then eases to about 4 pounds by late summer. Our Nigerians give a quart to three pints a day at "
            "their best. On paper that is far less than a Saanen, but the butterfat means a gallon of Nubian "
            "milk turns into noticeably more chevre than a gallon of Saanen milk, and it is the milk our kids "
            "will actually drink."
        ),
        p(
            "The single biggest difference we have measured is water. The summer we moved to a float-fed trough "
            "in the milking paddock, our does held peak production about three weeks longer than the year "
            "before with the same hay and grain."
        ),
        h2("FAQs"),
        faq(
            [
                ("How much milk does a goat produce a day?",
                 "A full-size dairy goat produces about 6 to 8 pounds of milk per day on average, which is roughly three quarters of a gallon to one gallon. Strong does reach 10 to 12 pounds at peak lactation, and Nigerian Dwarf goats give about 2 to 4 pounds per day."),
                ("How much milk does a goat produce per year?",
                 "Because a doe milks for about 10 months and rests for two, one goat gives roughly 1,800 to 2,500 pounds of milk per year, or about 210 to 290 gallons. A Nigerian Dwarf gives closer to 900 pounds, and a top Saanen can exceed 3,000 pounds."),
                ("Which goat breed produces the most milk?",
                 "Saanens produce the most milk by volume, typically 8 to 11 pounds per day with peaks above 2 gallons. Alpines are close behind. Nigerian Dwarfs produce the least volume but the richest milk, at 6 percent butterfat or more."),
                ("How much milk does a Saanen goat produce per day?",
                 "A good Saanen doe produces 8 to 11 pounds of milk per day, about 1 to 1.3 gallons, and proven does can exceed 16 pounds at peak lactation."),
                ("How much milk does a Nubian goat produce per day?",
                 "Nubian goats produce about 5 to 8 pounds of milk per day, a little less than the Swiss breeds, with butterfat around 4.5 to 5 percent that makes the milk excellent for cheese and soap."),
                ("Is one goat enough milk for a family?",
                 "Usually yes. One full-size dairy doe in milk gives about a gallon a day at peak and half a gallon late in lactation, enough for drinking and some cheese or yogurt. Two does with staggered kiddings keep milk coming year-round."),
                ("Do goats produce milk every day?",
                 "A goat in milk produces every day and should be milked every day, but she does not produce year-round. Lactation lasts about 10 months after kidding, followed by a two-month dry period before the next kidding."),
            ],
            base_id="2026101601",
        ),
        related(
            [
                (MILK_AT_ONCE, "How Much Milk Can a Goat Really Give at Once?"),
                (HOW_OFTEN, "How Often Do You Milk a Goat? Once a Day vs. Twice a Day"),
                (ALL_TIME, "Do Goats Produce Milk All the Time?"),
                (CHEESE, "How Many Goats Do You Need to Make Cheese?"),
            ]
        ),
    )
    return {
        "slug": PER_DAY_SLUG,
        "title": title,
        "excerpt": "How much milk does a goat produce per day? Real daily yields by breed, from Saanen to Nigerian Dwarf, plus what changes across a lactation and what you actually get in the bucket.",
        "metadesc": "How much milk does a goat produce a day? Daily yields by breed (Saanen, Alpine, Nubian, Nigerian Dwarf), production across a lactation, and what you really get in the bucket.",
        "focuskw": "how much milk does a goat produce",
        "categories": [CAT_ID["milking-dairy"], CAT_ID["goat-breeds"]],
        "primary_category": CAT_ID["milking-dairy"],
        "image_title": "How Much Milk Does a Goat Produce Per Day?",
        "image_kicker": "Real numbers by breed",
        "content": content,
    }


# --------------------------------------------------------------------------
# Article 2 - lactation cycle / "all the time"
# --------------------------------------------------------------------------

def article_all_time():
    title = "Do Goats Produce Milk All the Time? Lactation, Dry Periods, and Milking Without Breeding"
    content = join(
        p(
            "<strong>Do goats produce milk all the time?</strong> No. A doe only makes milk after she has given "
            "birth, she produces for about 10 months, and then she needs a rest of around two months before her "
            "next kidding. Bucks and wethers never produce milk, and a doe that has never kidded almost never "
            "does. So a goat is not a year-round tap, but with a little planning a small herd can keep milk in "
            "the fridge every month of the year."
        ),
        p(
            "This guide covers the questions behind the question: whether goats make milk without being "
            "pregnant, whether all goats produce milk, how long a lactation lasts, when goats stop, and how "
            "to stagger a herd so you never run dry."
        ),
        h2("Quick Answer"),
        table(
            ["Question", "Short answer"],
            [
                ["Do goats produce milk all the time?", "No. About 10 months of milk after kidding, then a 2-month dry period."],
                ["Do goats produce milk without being pregnant?", "Yes, once they have kidded. Pregnancy is not what makes milk; giving birth is. A doe can be milked for a year or more without being bred again."],
                ["Do all goats produce milk?", "No. Only does that have kidded. Bucks and wethers never do, and meat breeds produce only enough for their kids."],
                ["How long do goats produce milk?", "About 8 to 10 months per lactation, and 7 to 10 productive years in a lifetime."],
                ["Do goats make milk every day?", "Yes, while in milk. A doe in lactation needs milking every day, once or twice."],
            ],
        ),
        h2("Do Goats Produce Milk Without Being Pregnant?"),
        p(
            "This is the part that confuses most new owners, so it is worth being precise. A goat does not need "
            "to be pregnant to produce milk. She needs to have <em>kidded</em>. The hormonal shift at birth is "
            "what switches the udder on. After that, milk production continues as long as milk keeps being "
            "removed, whether by kids or by you, and tapers off when it is not."
        ),
        p(
            "So a doe that kidded in March and was never bred again will still be giving milk in November, "
            "without being pregnant. Many home dairies rely on exactly that."
        ),
        h3("Milking through: skipping a breeding season"),
        p(
            "If you keep milking a doe instead of drying her off and rebreeding, she will often keep producing "
            "well past the usual 10 months. This is called milking through. Production drops to maybe half of "
            "her peak and stays there, but a persistent doe can milk for 18 to 24 months, and some go longer. "
            "Swiss breeds (Saanen, Alpine, Toggenburg) tend to milk through better than Nubians or Nigerian "
            "Dwarfs, though individual does vary."
        ),
        p(
            "Milking through means fewer kids to sell or raise, fewer kidding risks, and no two-month gap. The "
            "trade-off is lower daily volume and a doe who never gets a full reset, so most herds milk a doe "
            "through for one extra year at most before breeding her again."
        ),
        h3("Precocious udders"),
        p(
            "Occasionally a doe that has never been bred develops an udder and produces a little milk on her "
            "own. This is called a precocious udder and it is most common in Nigerian Dwarfs and heavy dairy "
            "lines. It can be milked, but the amounts are small and the udder should be watched for mastitis. "
            "It is the exception that proves the rule: a goat can technically make milk without ever being "
            "pregnant, but you cannot plan a milk supply around it."
        ),
        h3("Bucks and wethers"),
        p(
            "Male goats do not produce milk. Bucks have rudimentary teats and no functioning mammary tissue, "
            "and wethers (castrated males) are the same. If someone sells you a milk goat, it is a doe."
        ),
        h2("Do All Goats Produce Milk?"),
        p(
            "Every doe that kids produces milk, because her kids need it. But not every goat produces enough "
            "milk to be worth milking. The difference between a dairy goat and a meat goat is mostly how much "
            "milk is left after the kids are fed, and for how long."
        ),
        table(
            ["Goat", "Produces milk?", "Worth milking?"],
            [
                ["Dairy doe that has kidded (Saanen, Alpine, Nubian, LaMancha, Nigerian Dwarf, etc.)", "Yes, for 8 to 10 months", "Yes, 2 to 12 pounds a day depending on breed"],
                ["Meat-breed doe that has kidded (Boer, Kiko, Spanish)", "Yes, for 3 to 5 months", "Rarely. Usually 1 to 3 pounds a day and a short lactation"],
                ["Fiber-breed doe (Angora, Cashmere)", "Yes, for a few months", "Rarely. Low volume"],
                ["Doe that has never kidded", "No, apart from a rare precocious udder", "No"],
                ["Buck or wether", "Never", "No"],
            ],
        ),
        p(
            f"For how the dairy breeds compare on daily volume and butterfat, see "
            f"{a(PER_DAY, 'how much milk a goat produces per day, by breed')}."
        ),
        h2("How the Goat Lactation Cycle Works"),
        p(
            "A dairy goat runs on roughly a one-year cycle. Here is what a conventional year looks like for a "
            "doe bred in the fall, which is when most standard breeds come into heat."
        ),
        table(
            ["Stage", "When", "What is happening"],
            [
                ["Breeding", "Late summer to winter (Swiss breeds and Nubians); any month for Nigerian Dwarfs", "Doe is bred. She may still be milking from her previous kidding."],
                ["Pregnancy", "About 150 days (5 months)", "Milk from the previous lactation continues for the first 3 months."],
                ["Dry period", "The last 60 days of pregnancy", "Milking stops so the udder rests and rebuilds. No milk."],
                ["Kidding", "Day 0", "Birth switches milk production on. First 3 to 5 days are colostrum, which the kids need."],
                ["Rising production", "Weeks 1 to 4", "Volume climbs quickly. Many owners start taking milk at about 2 weeks."],
                ["Peak", "Weeks 4 to 8", "Highest daily yield of the whole lactation."],
                ["Mid lactation", "Months 3 to 6", "Slow, steady decline. Still 75 to 90 percent of peak."],
                ["Late lactation", "Months 7 to 10", "Yield falls to 40 to 65 percent of peak. Milk gets richer."],
                ["Drying off", "About month 10", "Milking is tapered off over 1 to 2 weeks. The cycle restarts at the next kidding."],
            ],
        ),
        p(
            f"If you are deciding how many times a day to milk through that cycle, read "
            f"{a(HOW_OFTEN, 'how often do you milk a goat?')} It also covers the right way to dry a doe off."
        ),
        h2("How Long Do Goats Produce Milk?"),
        h3("Per lactation"),
        p(
            "Most dairy does produce for 8 to 10 months after kidding. The dairy industry standardizes "
            "records on a 305-day lactation, which is just over 10 months. Persistent does, especially "
            "Alpines and Toggenburgs, will go 12 months or more if you let them. Meat-breed does usually "
            "dry up on their own at 3 to 5 months once the kids are weaned."
        ),
        h3("Per lifetime"),
        p(
            "A doe usually freshens for the first time at one to two years old, hits her best lactations in "
            "years three through five, and can milk productively until she is 8 to 10 years old. Some does "
            "milk well past 10. A good dairy doe can give you 7 to 9 lactations over her life."
        ),
        h2("How Often Do Goats Produce Milk Without Being Pregnant?"),
        p(
            "People usually mean one of two things by this. If the question is how often a goat comes into "
            "milk, the answer is once per kidding, which under conventional management is once a year. If "
            "the question is how long she keeps producing after kidding while not pregnant, the answer is the "
            "whole lactation, 8 to 10 months, or 18 to 24 months if you milk her through."
        ),
        table(
            ["Management", "Breedings", "Months in milk", "Months dry"],
            [
                ["Conventional, bred every year", "1 per year", "About 10 of every 12", "About 2 of every 12"],
                ["Milking through, bred every other year", "1 per 2 years", "About 22 of every 24", "About 2 of every 24"],
                ["Extended milking through", "1 per 3 years", "Up to 34 of every 36", "About 2 of every 36"],
            ],
        ),
        h2("When Do Goats Stop Producing Milk?"),
        p("A doe stops producing milk for one of three reasons."),
        ul(
            [
                "<strong>You dry her off.</strong> About two months before her due date you taper milking, cut the grain, and let the udder go slack. This is the normal end of a lactation.",
                "<strong>She dries herself off.</strong> If milk is not removed regularly, production shuts down within a week or two. Skipped milkings late in lactation will end it early.",
                "<strong>She ages out.</strong> Production declines after about age 8 and most does are retired from the milk stand by 10 to 12, though plenty of healthy does milk longer.",
            ]
        ),
        p(
            f"Stopping abruptly is the one thing not to do with a doe in full milk. It is painful and invites "
            f"mastitis. The gradual approach is covered in {a(HOW_OFTEN, 'our milking schedule guide')}."
        ),
        h2("How to Have Goat Milk Year-Round"),
        p(
            "Since one doe cannot produce all the time, the answer is more than one doe on different "
            "schedules. Three ways to do it:"
        ),
        ol(
            [
                "<strong>Stagger your breedings.</strong> Breed one doe in September and another in December. When the first dries off in July, the second is still in full milk, and the first is back in milk by February.",
                "<strong>Milk one doe through.</strong> Breed one doe every year and milk the other through. Swap which doe gets bred each year.",
                "<strong>Keep a Nigerian Dwarf in the mix.</strong> Nigerians cycle year-round, so one can be bred for a spring kidding to cover the gap the fall-bred standard does leave.",
            ]
        ),
        p(
            f"Two to three does with staggered kiddings will keep a family in milk every month. If cheese is "
            f"the goal, {a(CHEESE, 'how many goats you need to make cheese')} walks through the batch math, "
            f"and {a(MILK_AT_ONCE, 'how much milk a goat gives at once')} covers what to expect per milking."
        ),
        h2("What It Looks Like on Our Farm"),
        p(
            "We run two kidding windows. Our Nubians are bred in October for March kids, and we hold one or "
            "two Nigerian Dwarf does back to breed in February for July kids. That puts the Nubians at peak "
            "when the Nigerians are dry, and the Nigerians at peak in late summer when the Nubians are "
            "tapering. The one year we bred everyone in the fall, we had six weeks in January with no milk at "
            "all and bought cartons at the store like everyone else. We have not repeated that."
        ),
        p(
            "We have also milked one Alpine-cross doe through for 19 months. She held a steady 4 pounds a day "
            "for the second year, about half her peak, and came back strong after she was finally bred."
        ),
        h2("FAQs"),
        faq(
            [
                ("Do goats produce milk all the time?",
                 "No. A doe produces milk for about 10 months after giving birth, then needs a dry period of about two months before her next kidding. With two or more does on staggered schedules, a herd can supply milk every month of the year."),
                ("Do goats produce milk without being pregnant?",
                 "Yes. Pregnancy is not what triggers milk; giving birth is. Once a doe has kidded she keeps producing as long as she is milked, whether or not she is bred again. Does can be milked through for 18 to 24 months without being pregnant."),
                ("Do all goats produce milk?",
                 "Only does that have given birth produce milk. Bucks and wethers never do. Meat and fiber breeds produce enough for their kids but rarely enough to be worth milking; dairy breeds produce a surplus for 8 to 10 months."),
                ("How long do goats produce milk after giving birth?",
                 "Most dairy goats produce for 8 to 10 months after kidding. Persistent does can go 12 months or longer, and a doe that is not rebred can be milked through for up to two years."),
                ("Do goats make milk every day?",
                 "Yes. A goat in milk produces continuously and should be milked every day, usually twice. Skipping milkings signals her body to slow down and can lead to mastitis."),
                ("At what age do goats stop producing milk?",
                 "Production usually peaks between ages three and five and declines after about age eight. Most does are retired from milking around 10 to 12 years old, though healthy does can milk longer."),
                ("Can a goat produce milk without having a baby?",
                 "Rarely. Some does, especially Nigerian Dwarfs, develop a precocious udder and produce a small amount of milk without kidding. It is not something you can plan a milk supply around."),
            ],
            base_id="2026101602",
        ),
        related(
            [
                (PER_DAY, "How Much Milk Does a Goat Produce Per Day? Real Numbers by Breed"),
                (HOW_OFTEN, "How Often Do You Milk a Goat? Once a Day vs. Twice a Day"),
                (MILK_AT_ONCE, "How Much Milk Can a Goat Really Give at Once?"),
                (CHEESE, "How Many Goats Do You Need to Make Cheese?"),
            ]
        ),
    )
    return {
        "slug": ALL_TIME_SLUG,
        "title": title,
        "excerpt": "Do goats produce milk all the time? No. Here is how the lactation cycle works, whether goats make milk without being pregnant, how long they produce, and how to keep milk year-round.",
        "metadesc": "Do goats produce milk all the time, or without being pregnant? How goat lactation works, how long does produce milk, when they stop, and how to stagger a herd for year-round milk.",
        "focuskw": "do goats produce milk all the time",
        "categories": [CAT_ID["milking-dairy"]],
        "primary_category": CAT_ID["milking-dairy"],
        "image_title": "Do Goats Produce Milk All the Time?",
        "image_kicker": "Lactation, dry periods, and milking through",
        "content": content,
    }


# --------------------------------------------------------------------------
# Article 3 - milking frequency
# --------------------------------------------------------------------------

def article_how_often():
    title = "How Often Do You Milk a Goat? Once a Day vs. Twice a Day"
    content = join(
        p(
            "<strong>How often do you milk a goat?</strong> The standard answer is twice a day, about 12 hours "
            "apart, every day she is in milk. That schedule gets the most milk out of a doe and keeps her "
            "udder comfortable. Once-a-day milking is a real option too, especially if kids are nursing or the "
            "doe is late in lactation, and it is how a lot of busy homesteads run. Three times a day is for "
            "commercial dairies and heavy producers at peak."
        ),
        p(
            "Below we lay out each schedule, what it costs you in milk, when to start milking after kidding, "
            "how to switch from twice to once, what happens if you skip, and how to stop milking properly when "
            "the lactation ends."
        ),
        h2("Quick Answer: How Often Should You Milk a Goat?"),
        table(
            ["Schedule", "Interval", "Milk you get", "Best for"],
            [
                ["Twice a day", "Every 12 hours (for example 6 am and 6 pm)", "100% of what she can give", "Maximum production, bottle-raised kids, high producers"],
                ["Once a day, kids separated overnight", "Milk in the morning after 10 to 12 hours apart from kids", "About a third to a half of daily production", "Dam-raised kids in the first 2 to 3 months"],
                ["Once a day, no kids", "Every 24 hours", "About 70 to 85% of twice-a-day volume", "Late lactation, low producers, owners who travel"],
                ["Three times a day", "Every 8 hours", "5 to 15% more than twice a day", "Commercial herds and very heavy does at peak"],
            ],
        ),
        p(
            "Whatever you choose, keep it consistent. A goat milked at 6 and 6 one day and 9 and 4 the next "
            "will give less than a goat milked at the same times every day."
        ),
        h2("Why Twice a Day, 12 Hours Apart, Is the Standard"),
        p(
            "An udder is a storage tank with a feedback loop. As it fills, pressure rises and a protein in the "
            "milk signals the doe to slow production. Empty the udder regularly and the signal stays off, so "
            "she keeps producing at full rate. Leave her full for too long and production ratchets down."
        ),
        p(
            "For most does the udder is comfortably full at around 12 hours. Milking at 12-hour intervals "
            "keeps pressure low, keeps the production signal on, and splits the day into two equal "
            "milkings so each one yields about the same. An uneven split, say 8 hours and 16 hours, works, "
            "but the long gap costs a little volume and leaves her uncomfortable."
        ),
        p(
            f"For what to expect out of each of those two milkings in pounds and quarts, see "
            f"{a(MILK_AT_ONCE, 'how much milk a goat can really give at once')}."
        ),
        h2("How Often Can You Milk a Goat?"),
        p(
            "You can milk a goat up to three times a day, and commercial dairies do, because a heavy producer "
            "at peak fills her udder faster than every 12 hours. The gain is usually 5 to 15 percent more "
            "milk. Beyond three times there is nothing left to gain; the udder is being emptied before it has "
            "refilled, and you are just spending time on the stand."
        ),
        p(
            "For a home herd of average does, twice a day is the practical ceiling. Three milkings only pay "
            "off on a doe giving 12 pounds or more a day, and even then only for the first few months."
        ),
        h2("How Often Do You Need to Milk a Goat?"),
        p(
            "The minimum is once a day, every day, for as long as she is in milk and you want her to stay in "
            "milk. A doe can go 24 hours between milkings and stay productive, at a reduced level. Stretch "
            "that to 36 or 48 hours and she starts drying off and runs a real risk of mastitis."
        ),
        p(
            "If kids are on her, she still needs to be managed daily, but the kids do the emptying. You can "
            "leave a dam-raising doe unmilked entirely for the first two weeks while the kids take everything."
        ),
        h2("When to Start Milking After Kidding"),
        p("This depends on who is feeding the kids."),
        table(
            ["Approach", "Days 1 to 3", "Days 4 to 14", "Week 3 onward"],
            [
                ["Kids bottle-raised", "Milk colostrum twice a day and feed it to kids", "Milk twice a day, feed kids from the bucket", "Milk twice a day, kids on bottles until weaning"],
                ["Kids dam-raised, milk shared", "Leave kids on the doe", "Leave kids on the doe, check udder daily", "Separate kids overnight, milk once in the morning, kids back on by day"],
                ["Kids dam-raised, no milking", "Leave kids on the doe", "Leave kids on the doe", "Start milking only after kids are weaned at 8 to 12 weeks"],
            ],
        ),
        p(
            "The first three to five days the doe is producing colostrum, which kids need and which you should "
            "not drink or make cheese with. After that it is ordinary milk. Many owners strip a few squirts "
            "from each side even on dam-raised does to make sure both halves are flowing and to spot mastitis."
        ),
        h2("Once-a-Day Milking: How It Works"),
        p(
            "Once-a-day milking is the most common compromise on small farms, and there are two versions."
        ),
        h3("With kids separated overnight"),
        p(
            "Put the kids in a pen next to the doe at night, about 10 to 12 hours before you plan to milk. In "
            "the morning, milk the doe out, then let the kids back with her for the day. You get the overnight "
            "milk, the kids get the daytime milk, and the doe is emptied regularly either way. This is the "
            "easiest schedule there is for the first two or three months, and it works from about two weeks "
            "of age."
        ),
        h3("Without kids"),
        p(
            "Once the kids are weaned or sold, once-a-day milking means a 24-hour interval. Most does adjust, "
            "but production settles 15 to 30 percent below what twice-a-day would give, and heavy producers "
            "may be uncomfortable or leaky by hour 20. It suits does in mid to late lactation, low producers, "
            "and Nigerian Dwarfs, which are small enough that the udder tolerates a long interval."
        ),
        h3("How to switch from twice a day to once a day"),
        ol(
            [
                "Pick the milking you will keep, usually morning, and keep its time fixed.",
                "Push the other milking later by about an hour every two days so the gap grows gradually.",
                "Once the second milking is 6 to 8 hours after the first and yields very little, drop it.",
                "Reduce the grain ration a little to match her lower output.",
                "Watch the udder for heat, lumps, or an uneven side for the first two weeks.",
            ]
        ),
        p(
            f"Where that leaves you on total milk per day is covered in "
            f"{a(PER_DAY, 'how much milk a goat produces per day')}, including the breed-by-breed numbers."
        ),
        h2("What Happens If You Skip a Milking?"),
        ul(
            [
                "<strong>One missed milking:</strong> a full, uncomfortable udder and a slightly lower yield the next day or two. Milk her as soon as you can and carry on. Not a disaster.",
                "<strong>Two or three missed milkings in a row:</strong> production drops noticeably and may not fully recover this lactation. The risk of mastitis rises as milk sits in a warm udder.",
                "<strong>Several days:</strong> she begins drying off. In early lactation this can mean a painfully engorged udder and a doe who is miserable; in late lactation she may simply dry up early.",
            ]
        ),
        p(
            "If you have to be away, the options are a neighbor who can milk, a once-a-day schedule for the "
            "trip with kids left on the doe, or drying her off ahead of time if she is late in lactation anyway."
        ),
        h2("How Long Does Milking a Goat Take?"),
        table(
            ["Method", "Per goat", "Notes"],
            [
                ["By hand, experienced", "5 to 8 minutes", "Plus a minute or two to clean teats and strip"],
                ["By hand, learning", "15 to 20 minutes", "Expect sore forearms the first two weeks"],
                ["Small milking machine", "3 to 5 minutes", "Plus 10 to 15 minutes of equipment washing per session"],
            ],
        ),
        p(
            "For two or three goats, hand milking twice a day is around 30 to 40 minutes of your day including "
            "setup and straining. A machine starts to make sense at four or five does."
        ),
        h2("How to Stop Milking: Drying a Goat Off"),
        p(
            "About two months before her next kidding, or when her yield has fallen to a pint or so a day, "
            "it is time to dry a doe off. Do it gradually over one to two weeks, not all at once."
        ),
        ol(
            [
                "Drop to once a day for about a week.",
                "Cut the grain on the stand so her body gets the signal to slow down. Keep hay and water free choice.",
                "Go to every other day for a few days, then every third day, milking out only enough to relieve pressure.",
                "Stop. The udder will stay firm for a week or so and then soften as the milk is reabsorbed.",
                "Check the udder daily for heat or hard spots for two weeks after the last milking.",
            ]
        ),
        p(
            f"Why the rest matters, and what the whole year looks like for a dairy doe, is in "
            f"{a(ALL_TIME, 'do goats produce milk all the time?')}"
        ),
        h2("A Sample Milking Routine"),
        table(
            ["Time", "Task"],
            [
                ["6:00 am", "Grain on the stand, wash and dry teats, strip the first squirts into a cup and check them, milk out, dip teats"],
                ["6:20 am", "Strain milk, chill immediately in ice water or the coldest part of the fridge"],
                ["During the day", "Kids with the doe if dam-raising; hay, browse, and water for everyone"],
                ["6:00 pm", "Repeat the morning milking (twice-a-day) or pen kids separately for the night (once-a-day)"],
            ],
        ),
        p(
            f"Planning to turn that milk into cheese? {a(CHEESE, 'How many goats you need to make cheese')} "
            f"covers how a milking schedule affects the batch you can make."
        ),
        h2("How We Run It Here"),
        p(
            "Our Nubians are milked twice a day at 6 and 6 from about two weeks after kidding until midsummer, "
            "then once a day in the morning once they drop under about 4 pounds. Our Nigerian Dwarf does are "
            "once-a-day milkers almost from the start; we pen the kids next to their dams at 7 pm, milk at "
            "6:30 am, and let everyone back together. It costs us some volume, but it means one person can do "
            "chores in forty minutes and nobody dreads a late evening."
        ),
        p(
            "The one rule we do not bend is time. When we let the evening milking drift by two or three hours "
            "during a busy week in June, the whole string dropped close to a pound a day apiece and took "
            "most of a month to recover."
        ),
        h2("FAQs"),
        faq(
            [
                ("How often do you milk a goat?",
                 "Most dairy goats are milked twice a day, about 12 hours apart, for the 8 to 10 months they are in milk. Once a day works when kids are nursing or in late lactation, at the cost of 15 to 30 percent of the milk. Three times a day is only worthwhile for very heavy producers."),
                ("Can you milk a goat once a day?",
                 "Yes. Once-a-day milking is common on small farms. With kids on the doe, separate them overnight and milk in the morning. Without kids, expect 15 to 30 percent less milk than twice-a-day milking and watch heavy producers for discomfort."),
                ("How often can you milk a goat?",
                 "Up to three times a day. Commercial dairies milk heavy producers every 8 hours for 5 to 15 percent more milk. More often than that gives no extra milk because the udder has not refilled."),
                ("How often do you need to milk a goat?",
                 "At least once every 24 hours while she is in milk. Going 36 to 48 hours between milkings starts the drying-off process and raises the risk of mastitis."),
                ("What happens if you do not milk a goat?",
                 "If kids are nursing, nothing; they empty the udder. If not, a doe in milk becomes engorged and uncomfortable within a day, production drops within two or three days, mastitis risk rises, and she dries off within a week or two."),
                ("When should you start milking a goat after she gives birth?",
                 "If you are bottle-raising the kids, milk from day one and feed the colostrum to the kids. If the kids are nursing, let them have everything for about two weeks, then separate them overnight and start milking in the morning."),
                ("How long does it take to milk a goat?",
                 "An experienced hand milker takes 5 to 8 minutes per goat, plus cleanup. Beginners should expect 15 to 20 minutes. A small milking machine takes 3 to 5 minutes per goat but adds equipment washing time."),
            ],
            base_id="2026101603",
        ),
        related(
            [
                (MILK_AT_ONCE, "How Much Milk Can a Goat Really Give at Once?"),
                (PER_DAY, "How Much Milk Does a Goat Produce Per Day? Real Numbers by Breed"),
                (ALL_TIME, "Do Goats Produce Milk All the Time?"),
                (CHEESE, "How Many Goats Do You Need to Make Cheese?"),
            ]
        ),
    )
    return {
        "slug": HOW_OFTEN_SLUG,
        "title": title,
        "excerpt": "How often do you milk a goat? Twice a day, 12 hours apart, is the standard. Here is when once a day works, what skipping costs you, when to start after kidding, and how to dry a doe off.",
        "metadesc": "How often do you milk a goat? Twice a day 12 hours apart is standard. When once-a-day works, how often you can milk, what happens if you skip, when to start after kidding, and how to dry off.",
        "focuskw": "how often do you milk a goat",
        "categories": [CAT_ID["milking-dairy"], CAT_ID["farm-life"]],
        "primary_category": CAT_ID["milking-dairy"],
        "image_title": "How Often Do You Milk a Goat?",
        "image_kicker": "Once a day vs. twice a day",
        "content": content,
    }


# --------------------------------------------------------------------------
# Contextual links spliced into the two existing posts.
#
# Each search string is a full sentence that appears exactly once in the live
# post and contains no apostrophes, quotes or dashes (wptexturize can change
# those between the stored and rendered text). publish.php refuses an edit
# whose search string is not found exactly once, and skips one whose
# replacement is already present, so this list is safe to re-run.
# --------------------------------------------------------------------------

def edits():
    e = []

    def add(post_id, search, extra):
        e.append({"post_id": post_id, "search": search, "replace": search + " " + extra})

    # --- "How Much Milk Can a Goat Really Give at Once?" (post 60)
    add(
        MILK_AT_ONCE_ID,
        "The exact amount depends on management and genetics.",
        f"For breed-by-breed daily numbers, see our guide to {a(PER_DAY, 'how much milk a goat produces per day')}.",
    )
    add(
        MILK_AT_ONCE_ID,
        "Goats naturally produce smaller amounts of milk compared with cows because they have smaller udders and different body structures.",
        f"If you are deciding between one and two milkings a day, {a(HOW_OFTEN, 'how often do you milk a goat?')} walks through the trade-offs.",
    )
    add(
        MILK_AT_ONCE_ID,
        "Proper nutrition, good genetics, and careful management can help extend productive years.",
        f"For the full picture of lactation length, dry periods, and milking through without rebreeding, read {a(ALL_TIME, 'do goats produce milk all the time?')}",
    )
    add(
        MILK_AT_ONCE_ID,
        "Families estimating how much milk is available for drinking, cooking, or cheese-making",
        f"(see {a(CHEESE, 'how many goats you need to make cheese')})",
    )

    # --- "How Many Goats Do You Need to Make Cheese?" (post 134)
    add(
        CHEESE_ID,
        "However, for planning purposes, you can use a simple range.",
        f"For breed-specific daily numbers, see {a(PER_DAY, 'how much milk a goat produces per day')}.",
    )
    add(
        CHEESE_ID,
        "For beginners, a two- or three-day collection window is often more realistic than trying to make a large batch from one day of milk.",
        f"To see what a single milking actually yields, read {a(MILK_AT_ONCE, 'how much milk a goat can give at once')}.",
    )
    add(
        CHEESE_ID,
        "Milk must be filtered, chilled quickly, stored cold, and used while still fresh.",
        f"Your milking routine matters here too; see {a(HOW_OFTEN, 'how often you should milk a goat')}.",
    )
    add(
        CHEESE_ID,
        "Aged cheese also ties up your milk because you are making food for later, not just for this week.",
        f"Remember too that does do not milk year-round; {a(ALL_TIME, 'do goats produce milk all the time?')} explains the dry period and how to stagger breedings so the cheese shelf never runs empty.",
    )
    return e


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    posts = [article_per_day(), article_all_time(), article_how_often()]
    payload = {"posts": posts, "edits": edits()}
    out = os.path.join(here, "payload.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    for post in posts:
        words = len(re.sub(r"<[^>]+>", " ", post["content"]).split())
        links = len(re.findall(r'href="https://puregoatfarms\.com/', post["content"]))
        print(f"{post['slug']}: {words} words, {links} internal links")
    print(f"{len(payload['edits'])} edits to existing posts -> {out}")


if __name__ == "__main__":
    main()
