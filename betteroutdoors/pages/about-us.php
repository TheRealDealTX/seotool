<?php defined('BO') || exit;
// About page.
$crumbs = [['Home', '/'], ['About Us', '/about-us/']];
page_head([
    'title' => 'About Better Outdoors: Who We Are & How We Review Archery Gear',
    'desc'  => 'Better Outdoors is an independent archery and bowhunting resource. Learn who we are, how we research bows and how we handle affiliate links.',
    'path'  => '/about-us/',
    'schema' => [breadcrumb_schema($crumbs), ['@type' => 'AboutPage', 'name' => 'About Better Outdoors', 'url' => SITE_URL . '/about-us/', 'about' => ['@id' => SITE_URL . '/#organization']]],
]);
?>
<section class="page-hero">
  <div class="wrap">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>About Better Outdoors</h1>
    <p>Better Outdoors was created for people who love getting outside but don&rsquo;t want confusion, hype or guesswork getting in the way of a good hunt.</p>
  </div>
</section>
<section class="section">
  <div class="topo" aria-hidden="true"></div>
  <div class="wrap split">
    <div class="prose reveal">
      <h2 id="h-why-better-outdoors-exists">Why Better Outdoors Exists</h2>
      <p>Archery information is everywhere. Unfortunately, much of it is outdated, overly technical, or written to sell you something before it helps you. Spec sheets are copied without context, reviews are rushed, and tuning advice assumes you already own a bow press and a decade of experience.</p>
      <p>We saw a gap, and Better Outdoors was built to fill it. We focus on:</p>
      <ul class="checks">
        <li>Practical advice over perfection</li>
        <li>Clear explanations instead of jargon</li>
        <li>Specs checked against manufacturer and retailer listings</li>
        <li>Useful recommendations instead of sales pressure</li>
      </ul>
    </div>
    <div class="img-stack reveal reveal-d2">
      <img src="<?= img_url('Better-Outdoors-Site-Image.webp') ?>" alt="The Better Outdoors team's approach to outdoor and archery guides" width="1200" height="720" loading="lazy">
      <div class="float-badge"><i class="fa-solid fa-mountain" aria-hidden="true"></i><div><b>Est. 2026</b><span>Free for every reader</span></div></div>
    </div>
  </div>
</section>
<section class="section section-mist">
  <div class="wrap">
    <div class="section-head reveal">
      <h2 id="h-who-better-outdoors-is-for">Who Better Outdoors Is For</h2>
      <p>You don&rsquo;t need to be an expert. You just need curiosity and a desire to shoot better.</p>
    </div>
    <div class="features">
      <div class="feature reveal"><div class="ico"><i class="fa-solid fa-seedling" aria-hidden="true"></i></div><h3>New archers</h3><p>Buying a first compound bow or ready-to-hunt package and wanting to get it right the first time.</p></div>
      <div class="feature reveal reveal-d1"><div class="ico"><i class="fa-solid fa-tree" aria-hidden="true"></i></div><h3>Whitetail hunters</h3><p>Preparing for the season with a bow that fits and a setup they trust.</p></div>
      <div class="feature reveal reveal-d2"><div class="ico"><i class="fa-solid fa-screwdriver-wrench" aria-hidden="true"></i></div><h3>DIY tuners</h3><p>Adjusting draw length, modules and accessories at home.</p></div>
      <div class="feature reveal reveal-d3"><div class="ico"><i class="fa-solid fa-recycle" aria-hidden="true"></i></div><h3>Used-bow buyers</h3><p>Weighing a proven older bow against a brand-new model.</p></div>
      <div class="feature reveal reveal-d4"><div class="ico"><i class="fa-solid fa-person-hiking" aria-hidden="true"></i></div><h3>Outdoor families</h3><p>Planning trips and hunts that actually run smoothly.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap prose" style="max-width:860px">
    <h2 id="h-what-you-ll-find-on-better-outdoors">What You&rsquo;ll Find on Better Outdoors</h2>
    <h3 id="h-core-content-areas">Core Content Areas</h3>
    <ul>
      <li><strong>Compound bow reviews</strong> for Mathews, Bear Archery and PSE, with verified specs, strengths, trade-offs and who each bow suits. Start with the <?= post_link('bear-archery-alaskan-xt-rth-compound-bow', 'Bear Alaskan XT') ?> or <?= post_link('mathews-lift-29-5', 'Mathews Lift 29.5') ?>.</li>
      <li><strong>Bow tuning guides</strong> such as our <?= post_link('2016-pse-draw-length-adjustment', '2016 PSE draw length adjustment guide') ?>.</li>
      <li><strong>Buying advice</strong> on <?= post_link('understanding-mathews-compound-bow-packages', 'bow packages') ?>, grips and accessories.</li>
      <li><strong>Interactive tools</strong>: draw length, arrow speed and kinetic energy calculators, a bow finder quiz and a bowhunting checklist. <a href="/tools/">See all tools</a>.</li>
    </ul>
    <h2 id="h-our-approach-to-content">Our Approach to Content</h2>
    <p>Every Better Outdoors guide starts with the questions real archers type into Google, then answers them plainly. Specifications come from manufacturer pages and major archery retailers; where sources disagree, we say so rather than picking the most flattering number. We update posts when models change and show the &ldquo;updated&rdquo; date on every article.</p>
    <h3 id="h-what-our-reviews-focus-on">What Our Reviews Focus On</h3>
    <ul class="checks">
      <li>Fit: draw length range, draw weight options and axle-to-axle length</li>
      <li>Shootability: brace height, let-off and how forgiving the bow is</li>
      <li>Real-world speed, not just the IBO number</li>
      <li>Who the bow is best for, and who should skip it</li>
    </ul>
    <h2 id="h-how-we-handle-gear-recommendations">How We Handle Gear Recommendations</h2>
    <p>Better Outdoors is reader-supported. Some links go to Amazon, and as an Amazon Associate we earn from qualifying purchases at no extra cost to you. That income keeps every guide and tool free. It never decides what we recommend: if a product isn&rsquo;t a good fit for most readers, we say so. Full details are in our <a href="/privacy-policy/#affiliate-disclosure">affiliate disclosure</a>.</p>
    <h2 id="h-our-philosophy-on-outdoor-travel">Our Philosophy on the Outdoors</h2>
    <p>Hunting and outdoor travel should feel freeing, not overwhelming. We believe in ethical shot placement, respecting landowners and wildlife agencies, and leaving places better than we found them.</p>
    <h2 id="h-free-resources-always">Free Resources, Always</h2>
    <p>No paywalls, no forced sign-ups. Everything on Better Outdoors is free to read and use.</p>
    <h2 id="h-looking-ahead">Looking Ahead</h2>
    <p>We are expanding into more bow brands, arrow and broadhead guides, and new calculators. Have a bow you want reviewed? <a href="/contact-us/">Tell us</a>.</p>
    <h2 id="h-join-the-better-outdoors-journey">Join the Better Outdoors Journey</h2>
    <p>Bookmark the <a href="/blog/">Better Outdoors blog</a>, try a <a href="/tools/">free tool</a>, and get outside. Go outside. Do it better.</p>
  </div>
</section>
<?php page_foot(); ?>
