<?php defined('BO') || exit;
// Homepage. Primary keywords: better outdoors, better outdoors archery, its better outdoors.

$GLOBALS['FAQS'] = [];
$homeFaqs = [
    'What is Better Outdoors?' => 'Better Outdoors is a free archery and outdoor resource. We publish in-depth compound bow reviews, step-by-step bow tuning guides such as the 2016 PSE draw length adjustment, and interactive calculators that help hunters set up their gear with confidence.',
    'Is Better Outdoors an archery pro shop?' => 'No. Better Outdoors is an independent publication, not a retail archery pro shop. We do not sell bows directly. We explain specs, setup and tuning so you walk into your local pro shop, or shop online, knowing exactly what you need.',
    'Are the Better Outdoors tools really free?' => 'Yes. Every Better Outdoors calculator, including the draw length calculator, arrow speed calculator, kinetic energy calculator, bow finder quiz and bowhunting checklist, is free with no sign-up required.',
    'How does Better Outdoors make money?' => 'Better Outdoors is reader-supported. Some links go to Amazon, and as an Amazon Associate we earn from qualifying purchases at no extra cost to you. Affiliate relationships never change our verdicts.',
    'Which bow brands does Better Outdoors cover?' => 'Right now Better Outdoors covers Mathews, Bear Archery and PSE compound bows, including the Mathews Lift 29.5, Mathews Prima, Bear Alaskan XT, Bear Persist, Bear Whitetail Maxx and PSE Evolve 28, with more brands on the way.',
];
ob_start();
echo faq_block($homeFaqs, 'faq', 'Better Outdoors FAQ');
$faqHtml = ob_get_clean();
$qa = [];
foreach ($homeFaqs as $q => $a) $qa[] = ['@type' => 'Question', 'name' => $q, 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $a]];

page_head([
    'title' => 'Better Outdoors | Archery Guides, Bow Reviews & Free Bowhunting Tools',
    'desc'  => 'Better Outdoors: honest compound bow reviews, draw length and bow tuning guides, and free bowhunting calculators. Go outside. Do it better.',
    'path'  => '/',
    'preload' => img_url('Better-Outdoors-BG.webp'),
    'schema' => [
        ['@type' => 'WebPage', '@id' => SITE_URL . '/#webpage', 'url' => SITE_URL . '/', 'name' => 'Better Outdoors', 'isPartOf' => ['@id' => SITE_URL . '/#website'], 'about' => ['@id' => SITE_URL . '/#organization']],
        ['@type' => 'FAQPage', 'mainEntity' => $qa],
    ],
    'body_class' => 'is-home',
]);
$featured = '2016-pse-draw-length-adjustment';
?>
<section class="hero">
  <div class="hero-bg" style="background-image:url('<?= img_url('Better-Outdoors-BG.webp') ?>')" aria-hidden="true"></div>
  <canvas class="hero-canvas" aria-hidden="true"></canvas>
  <div class="wrap hero-inner">
    <div>
      <span class="eyebrow"><i class="fa-solid fa-mountain" aria-hidden="true"></i> Better Outdoors Archery &amp; Bowhunting</span>
      <h1>Better Outdoors: <span class="accent">Go Outside. Do It Better.</span></h1>
      <p class="hero-lead">Better Outdoors helps archers and bowhunters make smarter decisions with honest compound bow reviews, step-by-step tuning guides and free interactive tools, so you spend less time guessing and more time shooting tight groups in the field.</p>
      <div class="btn-row">
        <a class="btn btn-orange" href="/blog/">Explore Guides <i class="fa-regular fa-circle-right" aria-hidden="true"></i></a>
        <a class="btn btn-ghost" href="/tools/draw-length-calculator/"><i class="fa-solid fa-ruler-horizontal" aria-hidden="true"></i> Find My Draw Length</a>
      </div>
      <div class="hero-stats">
        <div><b data-count="9">9</b><span>In-depth bow guides</span></div>
        <div><b data-count="5">5</b><span>Free archery tools</span></div>
        <div><b data-count="100" data-suffix="%">100%</b><span>Free, no paywalls</span></div>
      </div>
    </div>
    <div class="target-stage" aria-label="Interactive archery target">
      <span class="hit-count">Hits: <b>0</b></span>
      <div class="target"></div>
      <span class="ripple"></span><span class="ripple r2"></span>
      <div class="arrow"><span class="arrow-shaft"></span><span class="arrow-tip"></span><span class="arrow-fletch f1"></span><span class="arrow-fletch f2"></span></div>
      <button class="btn btn-orange shoot-btn" type="button"><i class="fa-solid fa-bullseye" aria-hidden="true"></i> Take a Shot</button>
    </div>
  </div>
  <div class="ridges" aria-hidden="true">
    <svg viewBox="0 0 1440 260" preserveAspectRatio="none"><path class="ridge-1" d="M0 260V150l90-60 70 40 110-95 90 70 80-35 120 90 100-110 110 85 90-40 120 75 110-90 110 60 90-30 150 80v70z"/></svg>
    <svg viewBox="0 0 1440 260" preserveAspectRatio="none"><path class="ridge-2" d="M0 260V190l120-70 90 45 130-80 100 75 120-50 110 70 140-95 100 80 130-55 110 60 120-40 170 70v50z"/></svg>
    <svg viewBox="0 0 1440 260" preserveAspectRatio="none"><path class="ridge-3" d="M0 260V230l160-40 120 25 160-45 140 40 150-30 140 35 170-40 130 30 170-25 100 15v95z"/></svg>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
<?php for ($i = 0; $i < 2; $i++): foreach (['Mathews', 'Bear Archery', 'PSE', 'Draw Length', 'Bow Tuning', 'Ready-to-Hunt Packages', 'Treestand Setups', 'Arrow Speed', 'Kinetic Energy', 'Whitetail Season'] as $w): ?>
    <span><i class="fa-solid fa-bullseye"></i> <?= e($w) ?></span>
<?php endforeach; endfor; ?>
  </div>
</div>

<section class="section">
  <div class="topo" aria-hidden="true"></div>
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">Why we exist</span>
      <h2>It&rsquo;s Better Outdoors When Your Gear Fits You</h2>
      <p>Better Outdoors is a free online resource built for archers, bowhunters and anyone who loves time outside but wants clear, trustworthy information before spending money or heading into the woods. Most bow problems are not shooting problems. They are fit and setup problems: the wrong draw length, a mismatched package, a grip that torques the riser.</p>
      <p>That is why Better Outdoors focuses on practical setup, honest specs and recommendations that actually help in real conditions. No hype. No gatekeeping. Just straightforward guidance from people who shoot.</p>
      <ul class="checks">
        <li>Specs checked against manufacturer and retailer data</li>
        <li>Step-by-step tuning you can do at home</li>
        <li>Calculators that turn numbers into decisions</li>
      </ul>
      <a class="btn btn-teal" href="/about-us/">Learn More About Better Outdoors</a>
    </div>
    <div class="img-stack reveal reveal-d2">
      <img src="<?= img_url('Better-Outdoors-Site-Image.webp') ?>" alt="Better Outdoors archery and outdoor adventure guides" width="1200" height="720" loading="lazy">
      <div class="float-badge"><i class="fa-solid fa-bullseye" aria-hidden="true"></i><div><b>Built for real hunts</b><span>Not just headlines</span></div></div>
    </div>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">Explore</span>
      <h2>What You&rsquo;ll Find on Better Outdoors</h2>
      <p>Whether you are buying your first compound bow or tuning a bow you have owned for a decade, Better Outdoors content is designed to help you prepare with confidence.</p>
    </div>
    <div class="features">
      <a class="feature reveal" href="/blog/"><div class="ico"><i class="fa-solid fa-bullseye" aria-hidden="true"></i></div><h3>Compound Bow Reviews</h3><p>Full specs, real-world speed and who each Mathews, Bear and PSE bow actually suits.</p></a>
      <a class="feature reveal reveal-d1" href="/2016-pse-draw-length-adjustment/"><div class="ico"><i class="fa-solid fa-screwdriver-wrench" aria-hidden="true"></i></div><h3>Bow Tuning Guides</h3><p>Draw length adjustment, module settings and when you need a bow press.</p></a>
      <a class="feature reveal reveal-d2" href="/tools/"><div class="ico"><i class="fa-solid fa-calculator" aria-hidden="true"></i></div><h3>Interactive Tools</h3><p>Draw length, arrow speed and kinetic energy calculators plus a bow finder quiz.</p></a>
      <a class="feature reveal reveal-d3" href="/understanding-mathews-compound-bow-packages/"><div class="ico"><i class="fa-solid fa-box-open" aria-hidden="true"></i></div><h3>Bow Package Advice</h3><p>What comes in an RTH package and when a bare bow is the better buy.</p></a>
      <a class="feature reveal reveal-d4" href="/tools/bowhunting-checklist/"><div class="ico"><i class="fa-solid fa-mountain" aria-hidden="true"></i></div><h3>Outdoor &amp; Hunting Tips</h3><p>Pack lists and small details that make every trip smoother.</p></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">Fresh from the blog</span>
      <h2>Latest Better Outdoors Guides &amp; Bow Reviews</h2>
      <p>Our most-read archery guides, updated for <?= date('Y') ?>.</p>
    </div>
    <div class="post-grid">
<?php
echo post_card($featured, $POSTS[$featured], false);
foreach ($POSTS as $s => $p) if ($s !== $featured) echo post_card($s, $p);
?>
    </div>
    <p style="text-align:center;margin-top:36px"><a class="btn btn-outline" href="/blog/">See All Articles <i class="fa-regular fa-circle-right" aria-hidden="true"></i></a></p>
  </div>
</section>

<section class="section section-mist">
  <div class="topo" aria-hidden="true"></div>
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">Try it now</span>
      <h2>Find Your Draw Length in 10 Seconds</h2>
      <p>Draw length is the single biggest factor in how a compound bow feels. Slide to your wingspan (fingertip to fingertip, in inches) and Better Outdoors will estimate your starting draw length using the wingspan &divide; 2.5 method archery pro shops use.</p>
      <p>Want a deeper check? The full calculator also works from height and walks you through the signs of a correct fit.</p>
      <a class="btn btn-teal" href="/tools/draw-length-calculator/">Open the Full Calculator</a>
    </div>
    <div class="mini-tool reveal reveal-d2">
      <svg class="bow-visual" viewBox="-40 0 160 120" aria-hidden="true">
        <path d="M60 10 Q118 60 60 110" fill="none" stroke="#1D546D" stroke-width="6" stroke-linecap="round"/>
        <rect x="70" y="50" width="12" height="20" rx="4" fill="#061E29"/>
        <path id="bow-string" d="M60 10 L30 60 L60 110" fill="none" stroke="#5F9598" stroke-width="1.6"/>
        <g id="bow-arrow"><line x1="30" y1="60" x2="118" y2="60" stroke="#2D2D2D" stroke-width="2.2"/><path d="M118 55 L128 60 L118 65 Z" fill="#FF6930"/><path d="M30 60 L40 54 L44 54 L36 60 L44 66 L40 66 Z" fill="#FF6930"/></g>
      </svg>
      <div class="field">
        <label for="mini-wingspan">Your wingspan <output id="mini-in">70"</output></label>
        <input type="range" id="mini-wingspan" min="56" max="80" step="0.5" value="70">
      </div>
      <p style="margin:0;color:var(--muted)">Estimated draw length</p>
      <div class="mini-out"><b id="mini-out">28.0</b><span>inches</span></div>
      <p class="hint" style="font-size:.85rem;color:var(--muted);margin:0">A starting point. Confirm at full draw with a pro shop or the signs in our <a href="/2016-pse-draw-length-adjustment/#h-how-to-find-your-correct-draw-length">draw length guide</a>.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">Free tools</span>
      <h2>Interactive Better Outdoors Archery Tools</h2>
      <p>Numbers are easier to trust when you can play with them. Every Better Outdoors tool runs right in your browser, no sign-up needed.</p>
    </div>
    <div class="tools-grid">
<?php $d = 0; foreach ($TOOLS as $ts => $t): ?>
      <a class="tool-card reveal reveal-d<?= $d++ % 4 ?>" href="/tools/<?= e($ts) ?>/"><div class="ico"><i class="fa-solid <?= e($t['icon']) ?>" aria-hidden="true"></i></div><h3><?= e($t['h1']) ?></h3><p><?= e($t['short']) ?></p><span class="go">Open tool <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span></a>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section-navy">
  <div class="wrap">
    <div class="stats reveal" style="margin-bottom:70px">
      <div><b data-count="18000" data-suffix="+">18,000+</b><span>Words of bow guides</span></div>
      <div><b data-count="80" data-suffix="+">80+</b><span>Archery questions answered</span></div>
      <div><b data-count="3">3</b><span>Major bow brands covered</span></div>
      <div><b>$0</b><span>Cost to readers</span></div>
    </div>
    <div class="section-head reveal">
      <span class="kicker">Why choose us</span>
      <h2>Why Choose Better Outdoors</h2>
      <p>There is no shortage of archery content online. What makes Better Outdoors different is how we approach it.</p>
    </div>
    <div class="why-grid">
      <div class="why reveal"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><h3>Practical over flashy</h3><p>Advice that works outside of perfect range conditions.</p></div>
      <div class="why reveal reveal-d1"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><h3>Honest gear recommendations</h3><p>Pros and cons included, every time.</p></div>
      <div class="why reveal reveal-d2"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><h3>Beginner-friendly</h3><p>No jargon or assumptions about what you know.</p></div>
      <div class="why reveal reveal-d3"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><h3>Free resources</h3><p>No paywalls or forced sign-ups at Better Outdoors.</p></div>
      <div class="why reveal reveal-d4"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><h3>Evergreen content</h3><p>Useful today and years from now, updated as models change.</p></div>
    </div>
    <p class="reveal" style="text-align:center;margin-top:40px;font-family:var(--head);font-size:1.2rem;color:#fff">We don&rsquo;t tell you how to hunt &ldquo;the right way.&rdquo; Better Outdoors helps you find your better way.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="kicker">Gear we trust</span>
      <h2>Better Outdoors Essential Archery Gear Picks</h2>
      <p>The accessories that make the biggest difference for most bowhunters, whatever bow you shoot.</p>
    </div>
    <?= product_grid([
        ['name' => 'Bow Release Aid', 'q' => 'index finger bow release aid', 'icon' => 'fa-hand-pointer', 'badge' => 'Top pick', 'blurb' => 'A quality wrist-strap release is the cheapest accuracy upgrade in archery.', 'pros' => ['Cleaner, repeatable shots', 'Adjustable length and trigger']],
        ['name' => 'Archery Rangefinder', 'q' => 'archery rangefinder angle compensation', 'icon' => 'fa-binoculars', 'blurb' => 'Angle-compensated yardage removes the biggest source of misses from a treestand.', 'pros' => ['Angle compensation', 'Fast scan mode']],
        ['name' => 'Portable Bow Press', 'q' => 'portable bow press compound', 'icon' => 'fa-screwdriver-wrench', 'blurb' => 'For module swaps, peep installs and string changes at home.', 'pros' => ['Saves pro shop trips', 'Protects cams and limbs']],
        ['name' => 'Bag or Foam Block Target', 'q' => 'archery bag target compound bow', 'icon' => 'fa-bullseye', 'blurb' => 'Shoot more arrows at home, which is the real secret to tighter groups.', 'pros' => ['Stops field points and broadheads', 'Easy arrow removal']],
    ], 'Recommended on Amazon') ?>
  </div>
</section>

<section class="section section-mist">
  <div class="wrap" style="max-width:860px">
    <div class="prose reveal"><?= $faqHtml ?></div>
  </div>
</section>
<?php page_foot(); ?>
