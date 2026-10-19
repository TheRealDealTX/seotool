<?php
// Blog post registry. Bodies live in app/posts/<slug>.php; URLs stay at the
// root (/<slug>/) exactly as WordPress published them.
defined('PGF') || exit;

const POSTS = [
    'how-to-increase-goat-milk-production' => [
        'title'    => 'How to Increase Goat Milk Production: 12 Field-Tested Fixes',
        'seo'      => 'How to Increase Goat Milk Production (12 Field-Tested Fixes)',
        'desc'     => 'Low milk? Here is how to increase goat milk production with better forage, protein, water, minerals, milking routine and health checks — tested on our own herd.',
        'date'     => '2026-10-06',
        'modified' => '2026-10-06',
        'cats'     => ['health-care', 'milking-dairy'],
        'image'    => ['/assets/img/blog/how-to-increase-goat-milk-production.webp', 1200, 675],
        'alt'      => 'Dairy goat being hand-milked into a stainless pail on the milking stand',
        'excerpt'  => 'Twelve practical changes — from forage quality to milking rhythm — that reliably lift a dairy doe\'s daily yield.',
        'tool'     => 'goat-feed-calculator',
        'faq' => [
            ['What is the fastest way to increase goat milk production?', 'The fastest gains usually come from fixing water and forage first: unlimited clean, lukewarm water and better-quality hay (alfalfa or a leafy grass-alfalfa mix). Many does respond within 5 to 10 days. Adding a properly balanced dairy ration on the stand and keeping a steady twice-a-day milking schedule usually adds more over the following weeks.'],
            ['Does alfalfa increase goat milk?', 'Alfalfa is one of the most useful feeds for dairy goats because it is high in protein and calcium, both of which milk production depends on. Feeding part of the forage ration as alfalfa hay or pellets commonly lifts yield in does that were on grass hay alone.'],
            ['Why did my goat\'s milk production suddenly drop?', 'A sudden drop usually points to stress, a change in feed, heat, an empty water bucket, mastitis, a parasite load, or the doe coming into heat. Check her temperature, run a CMT on each half of the udder, check FAMACHA eye color and look at what changed in the last two or three days.'],
            ['Does milking three times a day increase goat milk?', 'For high-producing does in early lactation, three milkings a day can raise total daily yield because the udder is emptied more often. For most home herds the extra labor is not worth it; consistent twice-a-day milking 12 hours apart captures most of the benefit.'],
            ['Can herbs or supplements increase goat milk supply?', 'Some keepers use galactagogue herbs such as fenugreek or fennel, but evidence in goats is limited. Correcting a protein, energy, water or mineral shortfall will almost always do far more than any single supplement.'],
        ],
    ],
    'best-dairy-goat-breeds-for-milk' => [
        'title'    => 'Best Dairy Goat Breeds for Milk: Saanen vs Alpine vs Nubian (and More)',
        'seo'      => 'Best Dairy Goat Breeds for Milk: Saanen vs Alpine vs Nubian',
        'desc'     => 'Compare the best dairy goat breeds for milk — Saanen, Alpine, Nubian, LaMancha, Oberhasli, Toggenburg and Nigerian Dwarf — by daily yield, butterfat and temperament.',
        'date'     => '2026-09-17',
        'modified' => '2026-09-17',
        'cats'     => ['goat-breeds', 'milking-dairy'],
        'image'    => ['/assets/img/blog/best-dairy-goat-breeds-for-milk.webp', 1200, 675],
        'alt'      => 'Mixed herd of dairy goat breeds walking across green pasture',
        'excerpt'  => 'A side-by-side comparison of the seven main dairy breeds: how much milk each gives per day, how rich it is, and who each breed suits.',
        'tool'     => 'dairy-goat-breed-finder',
        'faq' => [
            ['Which goat breed produces the most milk?', 'Saanens are generally the highest-volume dairy goat breed, with good does averaging roughly 1 to 1.5 gallons (8 to 12 pounds) a day at peak. Alpines are a close second and are known for long, steady lactations.'],
            ['Which goat breed has the richest milk?', 'Nigerian Dwarfs have the richest milk of the common dairy breeds, typically around 6 to 7 percent butterfat. Nubians follow at roughly 4.5 to 5 percent, which is why both are popular for cheese, butter and soap.'],
            ['What is the best dairy goat for beginners?', 'Nigerian Dwarfs and LaManchas are often recommended for beginners. Nigerians are small, easy to handle and produce rich milk; LaManchas are calm, sturdy and produce a solid volume without the noise Nubians are known for.'],
            ['How much milk does a Saanen goat produce per day?', 'A typical Saanen doe produces about 6 to 10 pounds (roughly 0.75 to 1.2 gallons) of milk per day across her lactation, with top does exceeding 12 pounds a day at peak.'],
            ['How much milk does a Nubian goat produce?', 'Nubians usually produce around 4 to 7 pounds (about half a gallon to 0.8 gallon) per day. They give less volume than Saanens or Alpines, but their milk is higher in butterfat and protein.'],
        ],
    ],
    'do-goats-produce-milk-without-being-pregnant' => [
        'title'    => 'Do Goats Produce Milk Without Being Pregnant? What Every New Owner Should Know',
        'seo'      => 'Do Goats Produce Milk Without Being Pregnant? (Explained)',
        'desc'     => 'Do goats produce milk without being pregnant, and do they give milk all the time? How lactation starts, milking through, maiden milkers and dry periods explained.',
        'date'     => '2026-08-29',
        'modified' => '2026-08-29',
        'cats'     => ['health-care', 'milking-dairy'],
        'image'    => ['/assets/img/blog/do-goats-produce-milk-without-being-pregnant.webp', 1200, 675],
        'alt'      => 'Small herd of goats resting together in tall summer grass',
        'excerpt'  => 'Goats do not make milk all the time. Here is how lactation starts, how long it lasts, and the real exceptions — milking through and maiden milkers.',
        'tool'     => 'goat-gestation-calculator',
        'faq' => [
            ['Do goats produce milk without being pregnant?', 'Normally, no. A doe begins producing milk when she gives birth (freshens), so she must be bred and carry a pregnancy to term first. The exceptions are does that are "milked through" from a previous kidding and the occasional maiden doe that develops a precocious udder.'],
            ['Do goats give milk all the time?', 'No. A dairy goat produces milk for a lactation of roughly 10 months after kidding, then production declines. Most keepers dry the doe off about two months before her next kidding so her body can rest.'],
            ['Do all female goats produce milk?', 'Any healthy doe can produce milk after kidding, but only dairy breeds produce enough beyond what their kids need to make milking worthwhile. Meat and fiber breeds such as Boers and Angoras usually produce only enough for their kids.'],
            ['How long can a goat be milked without rebreeding?', 'Many dairy does can be "milked through" for 18 months to two years or more without rebreeding, as long as they are milked consistently. Daily yield is lower in the second year, but it saves the doe a pregnancy.'],
            ['Can a male goat produce milk?', 'Very rarely. Bucks occasionally develop small udders (gynecomastia) and may even produce a little fluid, but this is a hormonal oddity, not a source of milk, and should be checked by a vet.'],
        ],
    ],
    'how-often-do-you-milk-a-goat' => [
        'title'    => 'How Often Do You Milk a Goat? Once vs Twice a Day Explained',
        'seo'      => 'How Often Do You Milk a Goat? Once vs Twice a Day',
        'desc'     => 'How often do you milk a goat? Most dairy goats are milked twice a day, 12 hours apart. Learn when once-a-day works, how kids change the schedule and how long milking takes.',
        'date'     => '2026-08-12',
        'modified' => '2026-08-12',
        'cats'     => ['milking-dairy', 'farm-life'],
        'image'    => ['/assets/img/blog/how-often-do-you-milk-a-goat.webp', 1200, 675],
        'alt'      => 'Fresh goat milk in a stainless pail next to a dairy doe on the milking stand',
        'excerpt'  => 'Twice a day, 12 hours apart, is the standard. But once-a-day milking, kid-sharing and milking through all have their place — here is how to choose.',
        'tool'     => 'goat-milk-yield-calculator',
        'faq' => [
            ['How often do you need to milk a goat?', 'Most dairy goats are milked twice a day, about 12 hours apart, for the whole lactation. Once-a-day milking also works, especially for lower-producing does or when kids are left on the doe part-time, but total yield is usually lower.'],
            ['What happens if you only milk a goat once a day?', 'The doe adjusts her production down to match. Expect roughly 15 to 25 percent less milk per day than twice-a-day milking. Switch gradually over a week or two rather than overnight to avoid discomfort and mastitis risk.'],
            ['Can you skip a milking?', 'Skipping one milking occasionally will not ruin a lactation, but the doe will be uncomfortable and repeated skips signal her body to reduce production. Skips also raise mastitis risk in heavy milkers.'],
            ['How long does it take to milk a goat?', 'By hand, an experienced milker takes about 5 to 10 minutes per doe. Beginners often take 15 to 20 minutes until their grip and rhythm build up.'],
            ['How soon after kidding can you milk a goat?', 'You can milk out a little colostrum right after kidding to make sure kids get enough and the udder is comfortable. Most keepers start keeping milk for the house after about two weeks, once colostrum has cleared.'],
        ],
    ],
    'how-much-milk-does-a-goat-produce-per-day' => [
        'title'    => 'How Much Milk Does a Goat Produce Per Day? Breed-by-Breed Chart',
        'seo'      => 'How Much Milk Does a Goat Produce Per Day? (Breed Chart)',
        'desc'     => 'How much milk does a goat produce per day? Most dairy goats give 0.5–1.5 gallons (4–12 lb) a day. See the breed chart for Saanen, Alpine, Nubian and Nigerian Dwarf.',
        'date'     => '2026-07-24',
        'modified' => '2026-10-14',
        'cats'     => ['milking-dairy'],
        'image'    => ['/assets/img/blog/how-much-milk-does-a-goat-produce-per-day.webp', 1200, 675],
        'alt'      => 'Dairy goats grazing a green pasture at Pure Goat Farms',
        'excerpt'  => 'The real numbers: daily milk by breed, how production changes across the lactation, and what a whole season adds up to.',
        'tool'     => 'goat-milk-production-estimator',
        'faq' => [
            ['How much milk does a goat produce per day?', 'A typical full-size dairy goat produces about 0.5 to 1.5 gallons (roughly 4 to 12 pounds, or 2 to 5.5 liters) of milk per day. Miniature breeds such as Nigerian Dwarfs give about 1 to 2 quarts a day.'],
            ['How much milk does a goat produce in a year?', 'Over a standard 305-day lactation, a good full-size dairy doe produces roughly 1,800 to 2,800 pounds of milk — about 210 to 325 gallons. Nigerian Dwarfs average closer to 700 to 800 pounds.'],
            ['How much milk does one goat give per day in liters?', 'Most dairy goats give about 2 to 5 liters per day. High producers can exceed 6 liters a day at peak lactation.'],
            ['When do goats produce the most milk?', 'Production peaks about 6 to 8 weeks after kidding, then slowly declines through the rest of the lactation.'],
            ['Is one goat enough milk for a family?', 'One good full-size dairy doe giving a gallon a day is usually plenty for a family\'s drinking milk with some left for yogurt or soft cheese. Goats are herd animals, though, so plan on keeping at least two.'],
        ],
    ],
    'how-many-goats-do-you-need-to-make-cheese' => [
        'title'    => 'How Many Goats Do You Need to Make Cheese?',
        'seo'      => 'How Many Goats Do You Need to Make Cheese? (Calculator)',
        'desc'     => 'How many goats do you need to make cheese? Learn milk yields, cheese types, and herd planning for better homemade goat cheese — with a free herd calculator.',
        'date'     => '2026-07-09',
        'modified' => '2026-10-14',
        'cats'     => ['milking-dairy'],
        'image'    => [UPLOADS . 'How-Many-Goats-Do-You-Need-to-Make-Cheese.webp', 1000, 563],
        'alt'      => 'Fresh goat cheese and a pail of milk on a farm table with dairy goats behind',
        'excerpt'  => 'Start with the cheese, then the milk, then the goats. A practical herd-planning guide with a built-in calculator.',
        'tool'     => 'goat-cheese-herd-calculator',
        'faq' => [
            ['How many goats do you need to make cheese at home?', 'One productive dairy doe is enough to make small batches of fresh chevre at home. Two does make regular weekly cheese-making much easier and give you company for each goat, since goats should not be kept alone.'],
            ['How much goat milk does it take to make a pound of cheese?', 'Roughly 1 gallon of goat milk makes about 1 pound of fresh chevre, while firm or aged cheeses need more — often 1.5 to 2 gallons per finished pound, depending on butterfat and recipe.'],
            ['Which goat breed is best for making cheese?', 'Breeds with higher butterfat and protein — Nigerian Dwarf, Nubian and LaMancha — give a higher cheese yield per gallon. Saanens and Alpines give more total milk with a slightly lower yield per gallon.'],
        ],
    ],
    'how-much-milk-can-a-goat-really-give-at-once' => [
        'title'    => 'How Much Milk Can a Goat Really Give at Once?',
        'seo'      => 'How Much Milk Can a Goat Give at Once? Per Milking & Per Day',
        'desc'     => 'How much milk can a goat give at once? Most dairy goats give 2–4 lb per milking and 4–8 lb a day. See breed differences, what affects yield, and a free calculator.',
        'date'     => '2026-07-08',
        'modified' => '2026-10-14',
        'cats'     => ['farm-life', 'milking-dairy'],
        'image'    => [UPLOADS . 'How-Much-Milk-Can-a-Goat-Really-Give-at-Once.webp', 1536, 1024],
        'alt'      => 'Dairy goat being hand-milked into a stainless steel pail',
        'excerpt'  => 'Per milking, per day and at peak: realistic milk numbers by breed, plus the factors that change them.',
        'tool'     => 'goat-milk-yield-calculator',
        'faq' => [
            ['How much milk can a goat give in one milking session?', 'A typical dairy goat can provide around 2–4 pounds of milk per milking, while high-producing goats may give 4–6 or more pounds.'],
            ['How much milk does a goat produce per day?', 'Most dairy goats produce about 4–8 pounds of milk daily, while excellent producers may reach 8–12+ pounds during peak lactation.'],
            ['Which goat breed produces the most milk?', 'Saanen goats are among the highest milk-producing breeds, followed by Alpine goats, which are also known for strong and consistent production.'],
            ['Can one goat provide enough milk for a family?', 'Yes, a productive dairy goat can supply enough milk for drinking, cooking, cheese-making, and other household uses when properly managed.'],
            ['Do bigger goats always produce more milk?', 'Not always. Milk production depends more on genetics, breed, health, nutrition, and lactation stage than body size alone.'],
            ['How can I increase my goat’s milk production?', 'Providing quality feed, fresh water, proper minerals, a consistent milking schedule, and good health care can help improve milk output.'],
            ['How long does a goat produce milk after giving birth?', 'Most dairy goats produce milk for about 8–10 months after kidding, although some may continue producing longer with proper care.'],
            ['Why is my goat producing less milk than expected?', 'Low milk production may result from poor nutrition, stress, illness, parasites, inconsistent milking routines, or the natural decline during late lactation.'],
            ['How often should a dairy goat be milked?', 'Most dairy goats are milked twice daily, although some lower-producing goats may be managed with once-a-day milking.'],
            ['Are Nigerian Dwarf goats good milk producers?', 'Nigerian Dwarf goats produce less milk than larger dairy breeds but provide rich milk with higher butterfat, making them popular for small farms.'],
        ],
    ],
];

// Posts newest first (the array above is already ordered, but sort defensively).
function posts_sorted(): array
{
    $p = POSTS;
    uasort($p, fn($a, $b) => strcmp($b['date'], $a['date']));
    return $p;
}

function posts_in(string $cat): array
{
    return array_filter(posts_sorted(), fn($p) => in_array($cat, $p['cats'], true));
}
