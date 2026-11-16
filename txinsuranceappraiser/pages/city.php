<?php
/** /areas/{city}-insurance-appraiser/ — unique, locally specific city landing page. */
require_once ROOT . '/inc/regions.php';

$c  = $city;
$N  = $c['name'];
$K  = $N . ' Insurance Appraiser';
$s  = $c['slug'];
$L  = $c['local'];
$R  = REGIONS[$c['region']];
$C  = cities();
$path = city_url($s);
$img  = city_image($c);
$county = $c['county'] . ' County';
$near = array_values(array_filter(array_map(fn($n) => $C[$n] ?? null, $c['nearby'])));
$hoods = $L['neighborhoods'] ?? [];
$marks = $L['landmarks'] ?? [];
$zips  = $L['zip_codes'] ?? [];
$hubLine = $c['hub_miles'] < 25
    ? "We work out of our {$c['hub']} hub, so {$N} is right in our backyard."
    : "Our nearest hub is in {$c['hub']}, roughly {$c['hub_miles']} miles away, and we travel to {$N} for every inspection.";

$title = pick([
    "{$K} | Property Claim Appraisals in {$N}, TX",
    "{$K} — Underpaid Claim Help in {$N}, TX",
    "{$K} for Hail, Wind & Water Claims | {$N}, TX",
], $s);
if (mb_strlen($title) > 64) {
    $title = "{$K} | {$N}, TX Claim Appraisals";
}
if (mb_strlen($title) > 64) {
    $title = "{$K} | TX Insurance Appraiser";
}
$desc = pick([
    "Looking for a {$K}? TX Insurance Appraiser helps {$county} homeowners and businesses resolve underpaid property claims through appraisal. Free review.",
    "Hire a trusted {$K} for underpaid hail, wind, water and fire claims. Policyholder-side appraisal in {$N}, TX. Free claim review: (254) 421-5412.",
    "{$K} services for {$N}, TX property owners: appraisal, umpire, Xactimate and Matterport. Get a fair, documented amount of loss. Free review.",
], $s, 1);
if (mb_strlen($desc) > 160) {
    $desc = "{$K} for underpaid property claims in {$N}, TX. Policyholder-side appraisal, estimates and 3D documentation. Free claim review.";
}
if (mb_strlen($desc) > 160) {
    $desc = "{$K} for underpaid hail, wind & water claims in {$N}, TX. Policyholder-side appraisal. Free review.";
}

$intro2 = pick([
    "As a {$K}, our job is simple to describe and hard to do well: prove the true cost of your covered loss and negotiate a fair award when your carrier’s estimate falls short.",
    "Hiring a {$K} gives you a professional who speaks the carrier’s language — line-item estimates, pricing databases and policy terms — and who works for you, not the insurer.",
    "A {$K} levels the playing field. Insurers rely on trained adjusters and estimating software; when you invoke appraisal, you deserve the same expertise on your side.",
], $s, 2);

$when = pick([
    ['Your carrier accepted the claim but its estimate is thousands below your contractor’s bid.', 'A storm-damaged roof was approved for spot repairs instead of full replacement.', 'The estimate leaves out flashing, drip edge, code items, waste or overhead and profit.', 'Interior water or fire damage was scoped as “clean and paint.”', 'Negotiations with the adjuster have stalled and you want a binding decision without a lawsuit.'],
    ['The insurer agrees the damage is covered but not on how much it costs to fix.', 'Your roof, siding or windows were labeled “cosmetic” despite functional damage.', 'Pricing in the carrier’s estimate doesn’t reflect current local labor and material costs.', 'Matching issues leave you with mismatched shingles, siding or flooring.', 'Supplements have been denied and you’ve run out of room to negotiate.'],
], $s, 3);

$faqs = [
    ['q' => "How do I hire a {$K}?",
     'a' => "Call TX Insurance Appraiser at " . SITE['phone'] . " or send your carrier’s estimate through our contact form. We review your claim free, explain our fee in writing, and if appraisal makes sense, you appoint us as your appraiser in your written demand or response to the carrier."],
    ['q' => "How much does a {$K} cost?",
     'a' => "Each side pays its own appraiser and shares the umpire’s fee if one is needed. Our fee depends on the size and complexity of the {$N} claim and is set out in writing before you sign. Use our free Appraisal Cost Calculator to estimate your net recovery first."],
    ['q' => "How long does an appraisal take in {$N}?",
     'a' => "Many residential appraisals in the {$N} area resolve within roughly one to three months after both appraisers are named. Timing depends on inspection scheduling, the size of the gap, and whether an umpire is required. Large commercial claims can take longer."],
    ['q' => "Does TX Insurance Appraiser serve all of {$county}?",
     'a' => "Yes. Along with {$N}, we serve communities throughout {$county} and the surrounding area" . ($near ? ", including " . implode(', ', array_map(fn($x) => $x['name'], array_slice($near, 0, 3))) : '') . ". " . $hubLine],
];
if (!empty($L['faq_local']['q'])) {
    array_splice($faqs, 2, 0, [$L['faq_local']]);
}

ob_start(); ?>
<section class="hero hero-split">
  <div class="hero-bg" style="background-image:url(<?= e($img) ?>)"></div>
  <div class="orb orb-1"></div><div class="orb orb-2"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim"><?= e($county) ?> · <?= e($c['region']) ?></span>
      <h1 class="anim"><?= e($K) ?></h1>
      <p class="lead anim">TX Insurance Appraiser is the <?= e($K) ?> property owners across <?= e($county) ?> call when an insurance company accepts a claim but underpays it. We inspect, estimate and negotiate a fair, binding award under your policy’s appraisal clause.</p>
      <div class="hero-actions anim">
        <a class="btn btn-gold btn-lg" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 20) ?> <?= e(SITE['phone_short']) ?></a>
        <a class="btn btn-ghost-light btn-lg" href="#contact">Free claim review <?= icon('arrow', 18) ?></a>
      </div>
      <div class="trust-row anim">
        <span><?= icon('shield', 18) ?> Policyholder-side appraisal</span>
        <span><?= icon('pin', 18) ?> Serving <?= e($N) ?> &amp; <?= e($county) ?></span>
      </div>
    </div>
    <div class="glass hero-card anim">
      <h2 style="font-size:1.15rem;margin-bottom:14px"><?= e($K) ?> at a glance</h2>
      <ul class="facts">
        <li><b>County</b><?= e($county) ?></li>
        <li><b>Region</b><?= e($c['region']) ?></li>
        <li><b>Nearest hub</b><?= e($c['hub']) ?><?= $c['hub_miles'] >= 25 ? ' (~' . $c['hub_miles'] . ' mi)' : '' ?></li>
        <li><b>Free review</b>Within 1 business day</li>
        <?php if ($zips): ?><li style="grid-column:1/-1"><b>ZIP codes served</b><?= e(implode(', ', $zips)) ?> &amp; surrounding</li><?php endif; ?>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split-60">
    <div class="reveal-l">
      <span class="eyebrow">Local appraisal advocacy</span>
      <h2>Your <?= e($K) ?> for Disputed Property Claims</h2>
      <?php if (!empty($L['local_intro'])): ?><p><?= e($L['local_intro']) ?></p><?php endif; ?>
      <p><?= e($intro2) ?></p>
      <p>Whether it’s a hail-battered roof, a burst pipe, a wind-damaged storefront or a fire loss, TX Insurance Appraiser documents every line item, prices it for the <?= e($N) ?> market, and presents it to the carrier’s appraiser — or to a neutral umpire if needed.</p>
    </div>
    <div class="reveal-r frame-deco">
      <div class="frame"><img src="<?= e($img) ?>" alt="<?= e($K) ?> — <?= e($N) ?>, Texas" width="800" height="420" loading="lazy"></div>
      <div class="float-badge"><span class="ic-badge ic-gold" style="width:44px;height:44px;margin:0"><?= icon('pin', 22) ?></span><div><b><?= e($N) ?>, TX</b><?= e($county) ?></div></div>
    </div>
  </div>
</section>

<section class="section bg-mist">
  <div class="wrap split">
    <div class="reveal-l">
      <span class="eyebrow">Is appraisal right for you?</span>
      <h2>When Should You Hire a <?= e($K) ?>?</h2>
      <p>Appraisal is built for one specific problem — a disagreement about the <strong>amount</strong> of a covered loss. Consider calling a <?= e($K) ?> when:</p>
      <ul class="checks"><?php foreach ($when as $w): ?><li><?= e($w) ?></li><?php endforeach; ?></ul>
      <p>Appraisal doesn’t decide coverage questions or legal claims. If your claim was denied outright, read <a href="/can-you-invoke-appraisal-after-a-denied-claim/">can you invoke appraisal after a denied claim?</a></p>
    </div>
    <div class="reveal-r">
      <div class="tool" style="padding:28px">
        <h3><?= icon('calc', 22) ?> Run the numbers first</h3>
        <p style="color:var(--ink-2)">Our free calculators show whether appraisal is likely worth it for your <?= e($N) ?> claim — before you spend a dollar.</p>
        <ul class="checks" style="margin-bottom:18px">
          <li><a href="/tools/appraisal-cost-calculator/">Is Appraisal Worth It? Calculator</a></li>
          <li><a href="/tools/recoverable-depreciation-calculator/">Recoverable Depreciation Calculator</a></li>
          <li><a href="/tools/texas-claim-deadline-calculator/">Texas Claim Deadline Calculator</a></li>
        </ul>
        <a class="btn btn-navy btn-block" href="/tools/">See all free tools</a>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Local storm &amp; property risks</span>
      <h2><?= e($N) ?> Storm Risks Every Property Owner Should Know</h2>
      <p><?= e($L['weather'] ?? $R['season']) ?></p>
    </div>
    <div class="peril-grid">
      <?php $i = 0; foreach ($R['perils'] as $ic => $label): ?>
      <div class="peril reveal d<?= $i++ % 3 + 1 ?>"><span class="ic-badge"><?= icon($ic, 22) ?></span><div><h3><?= e($label) ?></h3><p><?= e(PERIL_TEXT[$ic]) ?></p></div></div>
      <?php endforeach; ?>
    </div>
    <p class="reveal" style="margin-top:30px;max-width:900px">In <?= e($c['region']) ?>, the disputes our <?= e($K) ?> team sees most often involve <?= e($R['focus']) ?>. <?= e($R['season']) ?></p>
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">What we do</span>
      <h2>Services From Your <?= e($K) ?></h2>
      <p>Every service is available to <?= e($N) ?> residential and commercial property owners.</p>
    </div>
    <div class="grid g3">
      <?php foreach ([
          ['scale', 'Insurance Appraisal', '/services/appraisal/', "Your {$K} under the policy’s appraisal clause — inspection, estimate, negotiation and award."],
          ['gavel', 'Umpire Services', '/services/umpire/', "Neutral umpire services for {$N} appraisals that reach an impasse between the two appraisers."],
          ['cube', 'Matterport 3D Scans', '/services/matterport/', 'Measurable 3D documentation that preserves interior damage before repairs begin.'],
          ['calc', 'Xactimate Estimates', '/services/xactimate-estimate/', "Line-item estimates priced for {$N}-area ZIP codes in the format carriers use."],
          ['doc', 'Symbility Estimates', '/services/symbility-estimate/', 'Estimates that match carriers using the Symbility platform for direct comparison.'],
          ['search', 'Free Claim Review', '#contact', 'Send your carrier estimate — we’ll tell you honestly whether appraisal can close the gap.'],
      ] as $i => [$ic, $t, $u, $d]): ?>
      <a class="glass hero-card reveal d<?= $i % 3 + 1 ?>" href="<?= $u ?>" style="text-decoration:none;padding:26px">
        <div class="ic-badge ic-gold"><?= icon($ic, 24) ?></div>
        <h3><?= e($t) ?></h3><p style="color:#cfe0ee;margin:0"><?= e($d) ?></p>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Step by step</span>
      <h2>How the Appraisal Process Works in <?= e($N) ?></h2>
    </div>
    <ol class="timeline">
      <li class="reveal"><h3>Free claim review</h3><p>Share your carrier estimate, photos and policy. Your <?= e($K) ?> compares the scope to the real damage and tells you whether appraisal is worth it.</p></li>
      <li class="reveal"><h3>Written demand for appraisal</h3><p>A written demand invokes the appraisal clause. Most policies give each side a short window — often 20 days — to name an appraiser.</p></li>
      <li class="reveal"><h3>Inspection &amp; documentation</h3><p>We inspect your <?= e($N) ?> property with the carrier’s appraiser, capture measurements and Matterport scans, and build a line-item estimate.</p></li>
      <li class="reveal"><h3>Negotiation</h3><p>The two appraisers compare estimates line by line. Most disputes resolve here with a signed award.</p></li>
      <li class="reveal"><h3>Umpire if needed</h3><p>If the appraisers can’t agree, a neutral umpire — chosen by the appraisers or appointed by a court in <?= e($county) ?> — decides the disputed items.</p></li>
      <li class="reveal"><h3>Award &amp; payment</h3><p>An award signed by two of the three sets the amount of loss. Under Texas law, carriers generally must pay within five business days after agreeing to pay.</p></li>
    </ol>
  </div>
</section>

<section class="section bg-mist">
  <div class="wrap split">
    <div class="reveal-l">
      <span class="eyebrow">Homes &amp; businesses</span>
      <h2>Residential &amp; Commercial Claims in <?= e($N) ?></h2>
      <?php if (!empty($L['property_mix'])): ?><p><?= e($L['property_mix']) ?></p><?php endif; ?>
      <p>Our <?= e($K) ?> services cover single-family homes, townhomes, <a href="/apartment-complex-insurance-appraisal/">apartment complexes</a>, <a href="/hoa-insurance-appraisal-process/">HOAs</a>, <a href="/church-insurance-appraisal-texas/">churches</a>, <a href="/retail-property-damage-appraisal/">retail centers</a> and <a href="/commercial-property-insurance-appraisal-texas/">commercial buildings</a>. Each estimate reflects the actual materials on your property — not a generic template.</p>
    </div>
    <div class="reveal-r">
      <div class="person" style="grid-template-columns:120px 1fr;gap:22px">
        <div class="person-photo" style="border-radius:20px"><span class="init" style="font-size:2.2rem">JD</span></div>
        <div>
          <h3 style="margin-bottom:.2em">Meet Your <?= e($K) ?>: Joseph Dittman</h3>
          <p style="color:var(--ink-2);margin:0">Joseph is a Texas-licensed public adjuster who has spent his career on the policyholder side of hail, wind, water and fire claims. His firm, Rise Public Adjusting LLC, holds TDI license #<?= SITE['appraiser']['license'] ?>. On your appraisal, he serves as your appraiser. <a href="/about-us/">Read his background</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Neighborhoods &amp; nearby cities</span>
      <h2>Areas Our <?= e($K) ?> Team Serves</h2>
      <p><?= e($hubLine) ?> We serve every part of <?= e($N) ?> and the surrounding <?= e($county) ?> communities.</p>
    </div>
    <?php if ($hoods): ?>
    <ul class="chips reveal" style="justify-content:center;margin-bottom:18px">
      <?php foreach ($hoods as $h): ?><li><?= icon('home', 15) ?> <?= e($h) ?></li><?php endforeach; ?>
      <?php foreach ($marks as $m): ?><li><?= icon('pin', 15) ?> <?= e($m) ?></li><?php endforeach; ?>
    </ul>
    <?php endif; ?>
    <?php if ($near): ?>
    <p class="center reveal" style="font-weight:600;color:var(--navy-3);margin:26px 0 12px">Nearby cities we also serve:</p>
    <ul class="chips reveal" style="justify-content:center">
      <?php foreach ($near as $n): ?><li class="chip-link"><a href="<?= city_url($n['slug']) ?>"><?= e($n['name']) ?> Insurance Appraiser</a></li><?php endforeach; ?>
    </ul>
    <?php endif; ?>
  </div>
</section>

<section class="section bg-navy" id="contact">
  <div class="wrap split">
    <div class="reveal-l">
      <span class="eyebrow">Free claim review</span>
      <h2>Talk to a <?= e($K) ?> Today</h2>
      <p style="color:#cfe0ee">Tell us about your claim. We’ll review the carrier’s estimate at no cost and give you a straight answer about whether appraisal can close the gap.</p>
      <div class="contact-cards" style="margin-top:20px">
        <a class="contact-card" href="tel:<?= SITE['phone_href'] ?>"><span class="ic-badge ic-gold" style="margin:0;width:48px;height:48px"><?= icon('phone', 22) ?></span><span><b>Call</b><?= e(SITE['phone']) ?></span></a>
        <a class="contact-card" href="sms:<?= SITE['phone_href'] ?>"><span class="ic-badge" style="margin:0;width:48px;height:48px"><?= icon('chat', 22) ?></span><span><b>Text</b>Send us photos and questions</span></a>
      </div>
    </div>
    <div class="glass hero-card reveal-r"><?= lead_form('full', 'city-' . $s) ?></div>
  </div>
</section>

<?= faq_html($faqs, $K . ' FAQs') ?>

<?php
$rel = array_slice(array_values(array_filter(posts(), fn($p) => in_array($p['category'] ?? '', ['Appraisal Process', 'Roof Claims', 'Texas Weather & Claims'], true))), crc32($s) % 20, 3);
if ($rel): ?>
<section class="section-sm bg-mist">
  <div class="wrap">
    <h2 class="sec-title reveal">Helpful guides for <?= e($N) ?> property owners</h2>
    <div class="grid g3">
      <?php foreach ($rel as $p): ?>
      <a class="card reveal" href="/<?= $p['slug'] ?>/" style="text-decoration:none"><span class="pill"><?= e($p['category']) ?></span><h3><?= e($p['h1']) ?></h3><p><?= e($p['excerpt']) ?></p><span class="link-arrow">Read guide <?= icon('arrow', 16) ?></span></a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>
<?= cta_band("Underpaid claim in {$N}?", "Your {$K} is one call away. Free, no-pressure review from TX Insurance Appraiser.") ?>
<?php
$content = (string) ob_get_clean();
$area = ['@type' => 'City', 'name' => $N . ', TX', 'containedInPlace' => ['@type' => 'AdministrativeArea', 'name' => $county . ', Texas']];
$svc = schema_service($K, $desc, $path, $area);
$svc['serviceType'] = 'Insurance appraisal';
$geo = ['@type' => 'Place', 'name' => $N . ', Texas', 'geo' => ['@type' => 'GeoCoordinates', 'latitude' => $c['lat'], 'longitude' => $c['lon']]];
$svc['areaServed'] = [$area, $geo];
render_page([
    'title' => $title, 'description' => $desc, 'path' => $path, 'image' => $img, 'preload' => $img,
    'crumbs' => [['Home', '/'], ['Areas', '/areas/'], [$K, $path]],
    'schema' => [schema_webpage('WebPage', $title, $desc, $path), $svc, schema_faq($faqs)],
], $content);
