<?php
defined('GAP') || exit;
/** @var string $slug */
[$name, $blurb, $kind, $kinds] = TOOLS[$slug];
$trail = [['Tools', '/tools/'], [$name, "/tools/$slug/"]];

// Products the tool can recommend, embedded for the script.
$byKind = [];
$kitCats = ['/climbing/', '/rope/climbing-rope/', '/cutting-and-pruning/hand-saws-and-scabbards/'];
foreach ($CAT['products'] as $p) if ($slug === 'climbing-kit-builder' ? array_filter($kitCats, fn($k) => str_starts_with($p['category'], $k)) : in_array($p['kind'], $kinds, true)) $byKind[] = ['p' => $p['path'], 'n' => $p['name'], 'pr' => $p['price'], 'k' => $p['kind'], 'c' => $p['category'], 'l' => $p['level'] ?? 'all', 'bn' => $p['brand_name'] ?? ''];

$copy = [
 'climbing-kit-builder' => ['Tree Climbing Kit Builder', 'Build a complete tree climbing gear kit for moving rope (MRS/DdRT), stationary rope (SRS/SRT) or spur removals, sized to your budget, then add it to your cart.',
   [['How the kit builder chooses gear', ['Every climbing system needs the same backbone: a saddle, a life-support rope, a way to ascend and descend on it, a secondary attachment (lanyard), connectors and a helmet. What changes between systems is the device in the middle. Moving rope (MRS, also called DdRT) runs a friction hitch or mechanical device on a doubled line over a branch union. Stationary rope (SRS, or SRT) anchors one end and climbs or descends a single line with a rope wrench or mechanical device, which usually means ascenders too.', 'The builder fills each slot from the store, picking budget, mid-range or pro options depending on where you set the slider, and keeps a running total against your budget so you can see where the money goes.']],
    ['Before you climb on any of it', ['Life-support gear has to be compatible: rope diameter must suit the hitch cord or device, connectors must be rated and auto-locking, and everything must be inspected before each climb. Get trained by a qualified climber, read the manufacturer instructions for every component and work to ANSI Z133. The kit builder is a shopping aid, not a substitute for that training.']]],
   [['What is the difference between MRS and SRS climbing?', 'MRS (moving rope system, or DdRT) runs the rope over a branch and back to the climber, so you pull yourself up on a doubled line with roughly 2:1 advantage. SRS (stationary rope system, or SRT) anchors the rope and the climber moves along a single fixed line, which is faster for ascending but needs different devices.'], ['Do I need spurs for pruning?', 'No. Climbing spurs are for removals only. Spiking a tree you intend to keep wounds it, and ANSI Z133 and good practice both say to climb pruning jobs on rope.']]],
 'rigging-load-calculator' => ['Rigging Load Calculator', 'Estimate a log’s weight from species, diameter and length, see how a drop multiplies the load, and get a minimum rope and sling strength with a working-load margin.',
   [['How the numbers are worked out', ['Log weight is the volume of a cylinder (π × radius² × length) multiplied by the green weight of the species per cubic foot. Green wood is heavy: a 20-inch red oak round 4 feet long weighs roughly 550 pounds before it ever moves.', 'When a piece is allowed to free-fall before the rope catches it, the force on the system can be several times the static weight. The calculator uses a simple fall-factor based multiplier to show how quickly that adds up, then applies a 10:1 design factor, which is the margin commonly used for arborist rigging rope working load limits.']],
    ['Use it as a sanity check, not a certificate', ['Real shock loads depend on rope stretch, friction on the lowering device, how the piece swings and the rigging point itself, which is often the weakest link. Treat the result as a starting point for a conversation with your crew, keep drops short, let the rope run, and when the numbers look big, take smaller pieces.']]],
   [['How much does green oak weigh?', 'Red oak runs around 63 pounds per cubic foot green and white oak is about the same. Our calculator uses typical green weights for each species and shows the figure it used.'], ['What is a 10:1 design factor?', 'It means the working load you plan to put on rope is no more than a tenth of its rated breaking strength, to allow for wear, knots, bends and shock loading.']]],
 'rope-length-calculator' => ['Tree Height & Climbing Rope Length Calculator', 'Measure tree height from the ground with a distance and angle, then find how much climbing rope you need for a doubled (MRS) or single-line (SRS) climb.',
   [['Measuring a tree from the ground', ['Pace or tape a distance from the trunk on level ground, then sight the top of the tree with a clinometer or phone level app. Height is your distance multiplied by the tangent of the angle, plus your eye height. If you have no clinometer, the stick method works: hold a stick at arm’s length so its length above your hand equals your arm length, then back up until it covers the tree from base to top. Your distance from the trunk then roughly equals tree height.']],
    ['How much rope do I need?', ['A doubled moving-rope climb needs at least twice the height of your tie-in point plus enough tail to tie off and work, while a stationary rope needs the height plus the tail. The calculator adds a working margin and suggests the next common rope length up, because running out of rope on the way down is not an option. Always tie a stopper knot in the tail.']]],
   [['How long should an arborist climbing rope be?', '150 feet covers most moving-rope climbs to about 60 feet. Taller trees or SRS work from a basal anchor often call for 200 feet or more.'], ['Is the stick method accurate?', 'It is usually within 10 to 15 percent on level ground, which is good enough for choosing rope length, but not for felling distances, where you should add a generous safety margin.']]],
 'fuel-mix-calculator' => ['2-Stroke Fuel Mix Calculator (50:1 and more)', 'Work out exactly how much 2-stroke oil to add to any amount of gas for 50:1, 40:1, 32:1 or a custom ratio, in ounces and milliliters.',
   [['Getting the mix right', ['Most modern professional chainsaws, including Husqvarna’s, are designed to run a 50:1 mix with a quality 2-stroke oil. That is 2.6 US fluid ounces of oil per gallon of gas. Older saws and some other brands specify 40:1 or 32:1, so always check the operator’s manual for your machine.', 'Mix in a clean, approved fuel can: add the oil first, then the fuel, cap it and shake. Use fresh gasoline with the octane rating the manufacturer specifies, and avoid fuel with more than 10 percent ethanol. Premixed canned fuel is the easy way to avoid both problems.']]],
   [['How much oil for 1 gallon at 50:1?', '2.56 US fluid ounces, usually rounded to 2.6 oz (about 76 ml).'], ['Can I run 40:1 in a saw that calls for 50:1?', 'A slightly richer oil mix will not usually harm a saw, but it smokes more and can foul plugs and spark arrestor screens. Stick with the manufacturer’s ratio.']]],
 'spark-plug-decoder' => ['NGK Spark Plug Decoder & Plug Reading Guide', 'Decode an NGK small-engine spark plug number such as BPMR7A or CMR6H, and diagnose your chainsaw from the color of the plug tip.',
   [['Reading an NGK part number', ['NGK numbers are a code. The first letter is the thread diameter, the next letters describe the construction, the number is the heat range and the trailing letters cover reach and special features. On NGK plugs a lower heat number means a hotter plug. Two plugs that only differ by a letter can still be different lengths, so when replacing a plug, use the exact number listed in your saw’s operator’s manual.']],
    ['What a plug tells you', ['Pull the plug after a run and look at the insulator tip. Light tan to gray means the engine is running right. Black and sooty points to a rich mixture or a clogged air filter, wet and oily points to too much oil or a flooded engine, and white or blistered can mean a lean, hot-running engine that needs attention before it seizes.']]],
   [['What does the R mean in BPMR7A?', 'R means the plug has a built-in resistor, which suppresses radio-frequency interference.'], ['How often should I replace a chainsaw spark plug?', 'Many manufacturers suggest checking the plug every season or every 100 hours or so, and replacing it when the electrode is worn, the insulator is cracked, or the saw is hard to start.']]],
 'chain-file-finder' => ['Chainsaw Chain & File Size Finder', 'Find the right round file size for your chain pitch, decode the pitch, gauge and drive-link numbers stamped on your bar, and estimate the chain loop for a bar length.',
   [['Pitch, gauge and drive links', ['Every chain is described by three numbers. Pitch is the size of the chain (the distance between any three rivets divided by two), gauge is the thickness of the drive links that ride in the bar groove, and the drive link count sets the loop length. All three must match your bar and sprocket. They are stamped on the bar tail, and most chain boxes print them too.', 'File size follows pitch: the wrong file either fails to sharpen the full cutter or changes the hook of the tooth. Use a file guide to hold the right depth and angle.']]],
   [['What file size for 3/8 chain?', 'Standard 3/8" pitch chain is usually sharpened with a 7/32" (5.5 mm) file. 3/8" low-profile chain uses 5/32" (4.0 mm), and .325" chain uses 3/16" (4.8 mm). Check the chain maker’s chart for your exact chain.'], ['How do I count drive links?', 'Lay the chain flat and count the tangs that point inward, the parts that ride in the bar groove. Mark your starting link with a marker so you do not lose count.']]],
];
[$h1, $desc, $explain, $faq] = $copy[$slug];
$faqArr = array_map(fn($f) => ['q' => $f[0], 'a' => $f[1]], $faq);
$meta = [
    'title' => $name, 'desc' => $desc, 'canonical' => "/tools/$slug/",
    'jsonld' => array_filter([['@type' => 'WebApplication', 'name' => $h1, 'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any', 'url' => abs_url("/tools/$slug/"), 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD']], crumbs_ld($trail), faq_ld($faqArr)]),
    'scripts' => ['/assets/js/tools.js'],
    'body_class' => 'is-tool',
];
?>
<section class="cat-hero tool-hero"><div class="wrap">
  <?= crumbs($trail) ?>
  <div class="cat-hero-row"><div><p class="eyebrow">Free tool</p><h1><?= e($h1) ?></h1><p class="lede"><?= e($desc) ?></p></div>
  <img class="tool-hero-art" src="<?= kind_img($kind) ?>" alt="" width="140" height="140"></div>
</div></section>

<section class="wrap tool-app" data-tool="<?= e($slug) ?>">
<script type="application/json" id="tool-products"><?= json_encode($byKind, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
<?php include __DIR__ . "/tools/$slug.php"; ?>
</section>

<section class="section"><div class="wrap guide-layout">
  <div class="prose reveal">
<?php foreach ($explain as [$h, $ps]): ?>
    <h2><?= e($h) ?></h2>
<?php foreach ($ps as $para): ?>    <p><?= e($para) ?></p>
<?php endforeach; endforeach; ?>
  </div>
  <div class="guide-side"><?= faq_block($faqArr) ?>
    <div class="aside-box"><h2>More free tools</h2><ul class="aside-links"><?php foreach (TOOLS as $s => $t) if ($s !== $slug): ?><li><a href="/tools/<?= $s ?>/"><?= e($t[0]) ?></a></li><?php endif; ?></ul></div>
  </div>
</div></section>
