<?php
$index = posts_index();
$pick = fn(array $slugs) => array_values(array_filter(array_map(fn($s) => ($index[$s] ?? null) && $index[$s]['indexable'] ? $index[$s] : null, $slugs)));

$popular = $pick(array_slice(POPULAR, 0, 7));
$latest = array_slice(array_values(array_filter(live_posts(), fn($p) => !$p['sponsored'] && !in_array($p['slug'], POPULAR, true))), 0, 6);

// What's happening on the farm this month.
$seasons = [
    1 => ['Deep winter', 'Keeping water open, the coop dry and the soup pot full.', ['how-to-keep-livestock-water-from-freezing', 'heated-poultry-waterer', 'homemade-potato-soup', 'sourdough-storage']],
    2 => ['Kidding prep', 'Due dates are close: time to set up the kidding pen and kit.', ['preparing-for-kidding-season', 'goat-pregnancy', 'goat-birthing-kit', 'easy-rustic-artisan-bread']],
    3 => ['Kidding season', 'New kids in the barn and colostrum on the stove.', ['goat-kidding', 'goat-colostrum', 'scours-in-goats', 'postpartum-goat-care-after-birth']],
    4 => ['Spring lamb', 'Easter tables, tender chops and the first chicks under the lamp.', ['roast-lamb', 'sides-for-lamb-chops', 'best-sauce-for-lamb-chops', 'chick-temperature']],
    5 => ['Chicks & seedlings', 'Brooders, garden beds and dandelions everywhere.', ['chick-temperature', 'raising-layer-hens-for-eggs', 'golden-beet-seeds', 'the-many-uses-for-dandelion']],
    6 => ['Grilling season', 'Fresh mint, marinades and keeping the coop cool.', ['summer-lamb-recipes-with-fresh-mint', 'grilled-chicken-brine', 'lamb-chops-marinade', 'chicken-coop-ventilation']],
    7 => ['Canning begins', 'Cucumbers and zucchini faster than anyone can eat them.', ['how-to-water-bath-can', 'sweet-pickle-recipe', 'homemade-zucchini-bread', 'how-to-sterilize-mason-jars-for-canning']],
    8 => ['Peak canning', 'Tomatoes, peaches and salsa on every counter.', ['homemade-salsa-canning-recipe', 'canning-peaches', 'homemade-canned-tomato-sauce', 'citric-acid-for-canning']],
    9 => ['Harvest time', 'Apples, beets and getting the coop ready for cold.', ['homemade-applesauce', 'golden-beet-recipes', 'how-to-winterize-a-chicken-coop', 'homemade-chai-tea-recipe']],
    10 => ['Pumpkin season', 'Sugar pumpkins, silky pies and winterizing the coop.', ['pumpkin-pie-filling', 'sugar-pumpkin-vs-carving-pumpkin', 'how-to-make-pumpkin-puree', 'how-to-winterize-a-chicken-coop']],
    11 => ['Thanksgiving', 'The bird, the brine and every pie on the table.', ['how-to-brine-a-chicken', 'best-brining-container', 'thanksgiving-desserts', 'pumpkin-pie-filling']],
    12 => ['Holidays on the farm', 'Edible gifts, a festive roast and frost-free water troughs.', ['edible-gifts', 'holiday-snacks', 'roasted-lamb-leg', 'how-to-keep-livestock-water-from-freezing']],
];
$month = (int)date('n');
[$seasonLabel, $seasonBlurb, $seasonSlugs] = $seasons[$month];
$season = $pick($seasonSlugs);

$counts = array_count_values(array_column(live_posts(), 'topic'));
$homeFaq = [
    ['What is Purely Wholesome Farm?', 'Purely Wholesome Farm is a farm kitchen and homestead journal. We publish scratch recipes, practical livestock and garden guides, and free interactive tools for people who cook from scratch and keep animals, whether on acreage or a backyard.'],
    ['Are the Purely Wholesome Farm tools free?', 'Yes. Every calculator on Purely Wholesome Farm is free, works on your phone, and needs no sign-up: the brine calculator, lamb cooking calculator, goat due date calculator, canning altitude adjuster, egg planner and more.'],
    ['Where should I start on Purely Wholesome Farm?', 'Most readers find us through our lamb and brining guides. Start with what to serve with lamb chops, how to brine a chicken, or our pumpkin pie fixes, then explore the topic hubs for goats, chickens, canning and baking.'],
    ['Does Purely Wholesome Farm give veterinary advice?', 'No. Our livestock guides share hands-on homestead experience and cite veterinary and extension sources, but they are not a substitute for your veterinarian, especially for a sick or kidding animal.'],
    ['Does Purely Wholesome Farm accept guest posts?', 'We no longer publish paid guest posts. Everything on Purely Wholesome Farm is written for home cooks and homesteaders. If you have a question, a correction or a story to share, we would love to hear from you.'],
];
render('home', compact('popular', 'latest', 'season', 'seasonLabel', 'seasonBlurb', 'counts', 'homeFaq', 'index'), [
    'title' => 'Purely Wholesome Farm | Farm Kitchen Recipes, Homestead Guides & Tools',
    'desc' => 'Purely Wholesome Farm shares scratch recipes, practical goat and chicken care, canning guides and free farm tools like a brine calculator and goat due date calculator.',
    'path' => '/',
    'preload' => $popular[0]['image'] ?? null,
    'body_class' => 'is-home',
    'schema' => [['@type' => 'FAQPage', '@id' => SITE_ORIGIN . '/#faq', 'mainEntity' => array_map(fn($f) => ['@type' => 'Question', 'name' => $f[0], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f[1]]], $homeFaq)]],
]);
