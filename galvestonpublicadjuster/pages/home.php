<?php
$meta['title'] = 'Galveston Public Adjuster | TWIA Claims Expert | (832) 503-5866';
$meta['description'] = 'Galveston public adjuster for TWIA windstorm, hurricane, fire and flood claims. Denied or underpaid? Free expert claim review — no recovery, no fee. Call (832) 503-5866.';
$meta['schema'][] = ['@type' => 'Service', 'name' => 'Public adjusting services in Galveston, TX', 'serviceType' => 'Public insurance adjuster',
    'provider' => ['@id' => SITE_URL . '/#business'], 'areaServed' => 'Galveston County, TX'];
$faqs = [
    ['What does a Galveston public adjuster do?', '<p>A public adjuster is a licensed professional who represents <strong>you</strong>, the policyholder — not the insurance company. We inspect the damage, read your policy, build a complete estimate, document the loss, file and negotiate the claim with your carrier or TWIA, and push back on denials and lowball offers until the claim is paid correctly.</p>'],
    ['How much does a public adjuster cost in Texas?', '<p>Nothing up front. We work on a contingency fee that is a percentage of the claim payment, and Texas law caps public adjuster fees. If we do not recover money for you, you owe us nothing. Use our <a href="/calculators/">claim payout calculator</a> to see what you would net after the fee.</p>'],
    ['Can you help if TWIA already denied or underpaid my claim?', '<p>Yes. Many of our files start after a denial or a low offer. We can reopen the claim, supplement it with new documentation, and use the appraisal or dispute process when needed. Deadlines apply, so call as soon as possible.</p>'],
    ['How long do I have to file a TWIA windstorm claim?', '<p>TWIA requires that a claim be reported within <strong>one year</strong> of the date of loss (with limited good-cause extensions). See our <a href="/texas-windstorm-rules/">Texas windstorm rules</a> page for every deadline in the process.</p>'],
    ['Do I need a public adjuster for a small claim?', '<p>Not always. If the damage is minor and the offer is fair, you may not need us — and we will tell you so honestly during the free review. Public adjusters add the most value on large, complex, denied or underpaid claims.</p>'],
];
$posts = array_slice(blog_posts(), 0, 3);
?>
<section class="hero to-sand">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="eyebrow"><?= icon('shield', 18) ?> Licensed Texas public adjusters · Galveston County</span>
      <h1>Galveston Public Adjuster: Get Paid What Your Claim Is Really Worth</h1>
      <p class="lede">Hurricane, windstorm, fire or flood — your insurance company has an adjuster working for them. As your Galveston public adjuster, we work only for you: we document every inch of damage, handle TWIA and private carriers, and fight denied and underpaid claims.</p>
      <div class="hero-actions">
        <?= phone_link('btn btn-cta btn-lg', icon('phone', 20) . ' Call ' . PHONE) ?>
        <a class="btn btn-ghost btn-lg" href="#review" data-open-popup>Free Claim Review</a>
      </div>
      <ul class="hero-trust">
        <li><?= icon('check', 18) ?> No recovery, no fee</li>
        <li><?= icon('check', 18) ?> TWIA expert on every windstorm file</li>
        <li><?= icon('check', 18) ?> Free, no-obligation review</li>
      </ul>
    </div>
    <div class="hero-art"><?= art_hero_house() ?></div>
  </div>
  <?= wave_divider() ?>
</section>

<section class="section alt" style="padding-top:40px">
  <div class="wrap">
    <div class="stats reveal" style="--x:0">
      <div class="stat" style="background:#0b2540"><b>$0</b><span>Up front — we're paid only if you are</span></div>
      <div class="stat" style="background:#0f3358"><b>1 <em>yr</em></b><span>Deadline to report a TWIA windstorm claim</span></div>
      <div class="stat" style="background:#0e4a73"><b>10<em>%</em></b><span>Maximum public adjuster fee under Texas law</span></div>
      <div class="stat" style="background:#1f6f99"><b>14</b><span>Galveston County communities served</span></div>
    </div>
  </div>
</section>

<section class="section" id="claims">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Claims we handle</span>
      <h2>One Galveston public adjuster for every kind of property loss</h2>
      <p>On the island and across Galveston County, we handle residential and commercial claims from the first photo to the final check.</p>
    </div>
    <div class="grid g4">
      <article class="card hot reveal"><div class="badge-ico"><?= icon('wind', 30) ?></div><h3><a href="/twia-claims-expert/">TWIA Windstorm Claims</a></h3><p>Roof, siding, windows and wind-driven rain. We know the association's rules, deadlines and WPI-8 requirements.</p><a class="more" href="/twia-claims-expert/">TWIA claims help <?= icon('arrow', 16) ?></a></article>
      <article class="card reveal"><div class="badge-ico"><?= icon('hurricane', 30) ?></div><h3>Hurricane Damage</h3><p>Named-storm deductibles, wind vs. flood disputes, ALE and contents. We separate and prove every cause of loss.</p><a class="more" href="/galveston-storm-history/">Storm history <?= icon('arrow', 16) ?></a></article>
      <article class="card hot reveal"><div class="badge-ico"><?= icon('fire', 30) ?></div><h3><a href="/galveston-fire-claims/">Fire &amp; Smoke Claims</a></h3><p>Structure, contents, smoke and soot migration, HVAC contamination and living expenses — the items insurers most often leave out.</p><a class="more" href="/galveston-fire-claims/">Galveston fire claims <?= icon('arrow', 16) ?></a></article>
      <article class="card reveal"><div class="badge-ico"><?= icon('water', 30) ?></div><h3>Flood &amp; Water Damage</h3><p>NFIP and private flood policies, burst pipes, slab leaks and mold. We make sure the right policy pays for the right damage.</p><a class="more" href="/contact/">Get a review <?= icon('arrow', 16) ?></a></article>
      <article class="card reveal"><div class="badge-ico"><?= icon('home', 30) ?></div><h3>Roof &amp; Hail Claims</h3><p>Creased, lifted and missing shingles, matching, code upgrades and decking. See what wind does to shingles in our calculator.</p><a class="more" href="/calculators/">Wind calculator <?= icon('arrow', 16) ?></a></article>
      <article class="card hot reveal"><div class="badge-ico"><?= icon('alert', 30) ?></div><h3>Denied &amp; Underpaid</h3><p>"Wear and tear," "pre-existing," "flood not wind" — we challenge the reason with evidence, supplements and appraisal.</p><a class="more" href="/blog/">Claim guides <?= icon('arrow', 16) ?></a></article>
      <article class="card reveal"><div class="badge-ico"><?= icon('building', 30) ?></div><h3>Commercial Property</h3><p>Hotels, rentals, restaurants and shops on the Strand and Seawall — building, inventory and business interruption.</p><a class="more" href="/contact/">Talk to us <?= icon('arrow', 16) ?></a></article>
      <article class="card reveal"><div class="badge-ico"><?= icon('file', 30) ?></div><h3>Reopened Claims</h3><p>Already settled but found more damage? Many policies allow supplements. We review old files for missed items.</p><a class="more" href="/contact/">Check my claim <?= icon('arrow', 16) ?></a></article>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap split">
    <div class="reveal"><?= art_adjuster() ?></div>
    <div class="reveal">
      <span class="kicker">Why hire a public adjuster</span>
      <h2>Their adjuster protects their money. Your Galveston public adjuster protects yours.</h2>
      <p>The adjuster your insurance company sends is paid by the insurance company. Their estimate is a starting point — and it routinely leaves out creased shingles, code-required upgrades, matching, overhead and profit, contents and hidden water damage.</p>
      <ul class="checks">
        <li>We read your entire policy — endorsements, exclusions and deductibles</li>
        <li>We build a line-by-line estimate in the same software the carriers use</li>
        <li>We photograph, measure and moisture-map the damage before repairs</li>
        <li>We handle every call, email and re-inspection so you don't have to</li>
        <li>We push back on denials and lowball offers with evidence, not arguments</li>
      </ul>
      <?= phone_link('btn btn-cta btn-lg', icon('phone', 20) . ' Call for an expert consultation') ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">The difference</span><h2>Insurance company adjuster vs. your public adjuster</h2></div>
    <div class="compare reveal">
      <div class="them"><h3>Carrier / TWIA field adjuster</h3>
        <ul class="checks xs"><li>Hired and paid by the insurance company</li><li>Handles dozens of claims after a storm</li><li>Quick inspection, often ground-level only</li><li>Estimate written to the carrier's guidelines</li><li>Won't point out coverage you didn't claim</li></ul></div>
      <div class="us"><h3>Galveston Public Adjuster</h3>
        <ul class="checks"><li>Hired by you, paid only if you're paid</li><li>A licensed Texas adjuster who lives the coast</li><li>Full roof-to-slab inspection with documentation</li><li>Complete estimate: code, matching, O&amp;P, contents</li><li>TWIA expert handling deadlines and disputes</li></ul></div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="section-head"><span class="kicker">How it works</span><h2>From storm damage to settlement check in four steps</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Free claim review</h3><p>Call or send the form. We review your policy, photos and any offer or denial letter — free, with no obligation.</p></div>
      <div class="step reveal"><h3>Inspect &amp; document</h3><p>We inspect the property top to bottom, photograph and measure everything, and identify all covered damage.</p></div>
      <div class="step reveal"><h3>Estimate &amp; file</h3><p>We prepare a detailed estimate and proof of loss and present the claim to your carrier or TWIA.</p></div>
      <div class="step reveal"><h3>Negotiate &amp; recover</h3><p>We negotiate, attend re-inspections and escalate to appraisal when needed until the claim is paid.</p></div>
    </div>
    <?= banner('Hurricane or fire claim underpaid? Call for an expert consultation.', 'Talk directly with ' . AUTHOR . ' — free, no obligation.') ?>
  </div>
</section>

<section class="section dark">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">TWIA claims help</span>
      <h2>A TWIA expert in your corner</h2>
      <p>The Texas Windstorm Insurance Association insures most homes on Galveston Island, and its claims process has rules and deadlines private carriers don't. Reporting windows, WPI-8 certificates, "wind vs. water" disputes and TWIA's own appraisal and notice requirements can decide whether a claim is paid in full.</p>
      <p>With the right representation, your windstorm claim is filed right the first time — and challenged correctly if TWIA gets it wrong.</p>
      <ul class="checks"><li>TWIA-specific claim filing and deadline tracking</li><li>Wind-driven rain vs. flood damage separation</li><li>Supplements, re-inspections and appraisal</li></ul>
      <a class="btn btn-cta btn-lg" href="/twia-claims-expert/">Talk to a TWIA expert <?= icon('arrow', 18) ?></a>
    </div>
    <div class="reveal"><?= art_twia() ?></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Free tools &amp; local knowledge</span><h2>Resources for Galveston property owners</h2><p>Everything we use on real claims, published for you.</p></div>
    <div class="grid g3">
      <a class="card reveal" href="/calculators/" style="text-decoration:none"><div class="badge-ico"><?= icon('calc', 30) ?></div><h3>Shingle Wind Damage Calculator</h3><p>See what 60 to 180 mph winds do to shingles rated for different speeds — plus wind ratings for 10 top manufacturers.</p></a>
      <a class="card reveal" href="/calculators/#claim-calc" style="text-decoration:none"><div class="badge-ico"><?= icon('dollar', 30) ?></div><h3>Claim Payout Calculator</h3><p>Compare your insurer's offer with what you'd net after your deductible and our fee.</p></a>
      <a class="card reveal" href="/texas-windstorm-rules/" style="text-decoration:none"><div class="badge-ico"><?= icon('scale', 30) ?></div><h3>Texas Windstorm Rules</h3><p>TWIA eligibility, WPI-8 certificates, claim deadlines and dispute steps in plain English.</p></a>
      <a class="card reveal" href="/galveston-local-code/" style="text-decoration:none"><div class="badge-ico"><?= icon('building', 30) ?></div><h3>Galveston Local Code</h3><p>Wind design speeds, roofing and floodplain rules that decide what your claim should include.</p></a>
      <a class="card reveal" href="/galveston-storm-history/" style="text-decoration:none"><div class="badge-ico"><?= icon('hurricane', 30) ?></div><h3>Galveston Storm History</h3><p>From the 1900 Storm to Ike and Beryl — how the island's storms shaped today's insurance.</p></a>
      <a class="card reveal" href="/weather-events/" style="text-decoration:none"><div class="badge-ico"><?= icon('wind', 30) ?></div><h3>Weather Events: 70+ mph Winds</h3><p>Updated weekly: every day Galveston winds reached 70 mph or more — the level where roof damage begins.</p></a>
    </div>
  </div>
</section>

<section class="section alt" id="review">
  <div class="wrap split">
    <div class="reveal">
      <span class="kicker">Meet your adjuster</span>
      <h2>Local, licensed and personally involved</h2>
      <p><?= AUTHOR ?> is a licensed Texas public adjuster who works claims across Galveston Island, Bolivar, Tiki Island, Jamaica Beach and the mainland. Every file gets his personal attention — no call centers, no hand-offs.</p>
      <p>When you call a Galveston public adjuster from our office, you get straight answers: whether your claim is worth pursuing, what's missing, and what it realistically should pay. If you don't need us, we'll tell you.</p>
      <p><a class="btn btn-outline" href="/about/">About <?= AUTHOR ?> <?= icon('arrow', 16) ?></a></p>
    </div>
    <div class="hero-card reveal">
      <h2>Get a free claim review</h2>
      <p class="muted">Tell us what happened. A Galveston public adjuster will call you back — usually the same day.</p>
      <?= lead_form('home') ?>
    </div>
  </div>
</section>

<?php if ($posts): ?>
<section class="section">
  <div class="wrap">
    <div class="section-head"><span class="kicker">Claim guides</span><h2>Latest from the blog</h2><p>New, practical guides every week from <?= AUTHOR ?>.</p></div>
    <div class="grid g3"><?php foreach ($posts as $i => $p) echo post_card($p, $i); ?></div>
  </div>
</section>
<?php endif ?>

<section class="section alt">
  <div class="wrap layout-side">
    <div>
      <span class="kicker">Questions</span>
      <h2>Galveston public adjuster FAQ</h2>
      <?= faq_block($faqs, $meta['schema']) ?>
    </div>
    <aside class="sidebar">
      <div class="side-card dark"><h3>Serving all of Galveston County</h3><p><?= e(implode(' · ', AREAS)) ?></p><?= phone_link('btn btn-cta btn-block', icon('phone', 18) . ' ' . PHONE) ?></div>
      <div class="side-card"><h3>Before you sign an insurer's release</h3><p>Once you accept a final payment and sign a release, reopening the claim gets much harder. Get a second opinion from a Galveston public adjuster first.</p></div>
    </aside>
  </div>
</section>
