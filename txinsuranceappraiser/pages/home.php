<?php
$title = 'TX Insurance Appraiser | Insurance Appraiser in Texas';
$desc  = 'TX Insurance Appraiser provides policyholder-side insurance appraisal for hail, wind, hurricane, water and fire claims in Texas. Free review.';
$C = cities();
$latest = array_slice(posts(), 0, 6, true);

$faqs = [
    ['q' => 'What does TX Insurance Appraiser do?',
     'a' => 'TX Insurance Appraiser serves as the policyholder’s appraiser when a property owner and their insurance company agree a loss is covered but disagree on the amount. We inspect the damage, build a line-item estimate in Xactimate or Symbility, document the property, and negotiate the amount of loss with the carrier’s appraiser or an umpire under your policy’s appraisal clause.'],
    ['q' => 'When should I hire an insurance appraiser instead of continuing to negotiate?',
     'a' => 'Consider appraisal when your carrier accepts that the damage is covered but its estimate is well below what a qualified contractor says the repair will cost, and further negotiation has stalled. Common examples are hail claims paid as repairs instead of replacements, missing line items, low pricing, or disputes over matching and code upgrades.'],
    ['q' => 'How much does an insurance appraiser cost in Texas?',
     'a' => 'Each side normally pays its own appraiser and splits the umpire’s fee if one is needed. Appraiser fees in Texas are commonly a percentage of the award or a flat or hourly fee depending on claim size. TX Insurance Appraiser explains its fee in writing before you sign anything, and our free Appraisal Cost Calculator helps you estimate whether appraisal is worth it.'],
    ['q' => 'How long does the insurance appraisal process take?',
     'a' => 'Many Texas residential appraisals resolve in roughly 30 to 90 days after both appraisers are named, depending on how quickly inspections are scheduled, how large the gap is, and whether an umpire is needed. Large commercial losses can take longer. Having complete documentation ready usually shortens the process.'],
    ['q' => 'Is an insurance appraiser the same as a public adjuster?',
     'a' => 'No. A public adjuster manages and negotiates the whole claim on your behalf. An appraiser is appointed under the policy’s appraisal clause to determine only the amount of loss. Our lead appraiser, Joseph Dittman, is a Texas-licensed public adjuster by background, but on an appraisal assignment he acts strictly as your appraiser.'],
    ['q' => 'Does TX Insurance Appraiser work outside major cities?',
     'a' => 'Yes. TX Insurance Appraiser works from Austin, Waco, Dallas and Houston and serves property owners in 288 Texas cities and the rural areas between them, from the Panhandle and Permian Basin to the Rio Grande Valley, East Texas and the Gulf Coast.'],
];

$featured = ['houston', 'dallas', 'san-antonio', 'austin', 'fort-worth', 'el-paso', 'corpus-christi', 'waco'];
$pins = [ // approx positions on the Texas-Map.webp graphic (percent)
    ['Dallas', 71.8, 9.4], ['Waco', 69.7, 41.7], ['Austin', 65.9, 75.6], ['Houston', 83.6, 86],
];

ob_start(); ?>
<section class="hero">
  <div class="hero-bg" style="background-image:url(/assets/img/site/TX-Insurance-Appraiser-Hero-BG.webp)"></div>
  <div class="orb orb-1"></div><div class="orb orb-2"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">TX Insurance Appraiser</span>
      <h1 class="anim">Texas Insurance Appraiser for <span class="text-gold"><span class="typed" data-words="Hail|Wind|Hurricane|Water|Fire|Freeze">Hail</span> Claims</span></h1>
      <p class="lead anim">When your insurance company agrees the damage is covered but lowballs the amount, TX Insurance Appraiser steps in as your policyholder-side appraiser — inspecting every line item, documenting the loss in 3D, and negotiating a fair award under your policy’s appraisal clause.</p>
      <div class="hero-actions anim">
        <a class="btn btn-gold btn-lg" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 20) ?> Call <?= e(SITE['phone_short']) ?></a>
        <a class="btn btn-ghost-light btn-lg" href="#how-it-works">How appraisal works <?= icon('arrow', 18) ?></a>
      </div>
      <div class="trust-row anim">
        <span><?= icon('shield', 18) ?> Texas-licensed adjuster background</span>
        <span><?= icon('map', 18) ?> 288 Texas cities served</span>
        <span><?= icon('cube', 18) ?> Xactimate · Symbility · Matterport</span>
      </div>
    </div>
    <div class="glass hero-card anim">
      <h2>Get a free claim review</h2>
      <p style="color:#cfe0ee;font-size:.95rem;margin-bottom:16px">Tell us about your claim. A TX Insurance Appraiser specialist will tell you honestly whether appraisal makes sense.</p>
      <?= lead_form('compact', 'home-hero') ?>
    </div>
  </div>
  <div class="hero-wave"><svg viewBox="0 0 1440 60" preserveAspectRatio="none"><path fill="#fff" d="M0 40c240 25 480 25 720 5s480-25 720 0v15H0z"/></svg></div>
</section>

<section class="section-sm" style="padding-top:20px">
  <div class="wrap">
    <div class="counters">
      <div class="counter reveal"><b><span data-count="288">288</span></b><span>Texas cities served</span></div>
      <div class="counter reveal d1"><b><span data-count="4">4</span></b><span>Regional hubs: Austin, Waco, Dallas &amp; Houston</span></div>
      <div class="counter reveal d2"><b><span data-count="5">5</span></b><span>Specialized appraisal &amp; estimating services</span></div>
      <div class="counter reveal d3"><b>24<span class="plus">/7</span></b><span>Reach us any time — fast call-backs</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal-l">
      <span class="eyebrow">Your premier insurance appraiser in Texas</span>
      <h2>A fair, documented number for your property damage claim</h2>
      <p>At TX Insurance Appraiser, we bring construction knowledge and years of claim experience to one job: proving the true amount of your loss. Insurance carriers employ trained adjusters and estimators. When you invoke appraisal, you deserve an equally qualified professional on your side of the table.</p>
      <p>Our insurance appraisers inspect the property from the roof deck to the drywall, write a detailed line-item estimate using the same software insurers use, and meet with the carrier’s appraiser to resolve the difference. If the two appraisers can’t agree, a neutral umpire decides — and an award signed by any two of the three sets the amount of loss.</p>
      <ul class="checks">
        <li>Residential, multi-family, commercial, church and HOA property claims</li>
        <li>Hail, wind, tornado, hurricane, water, freeze, fire and smoke losses</li>
        <li>Clear written fee terms before you commit — no surprises</li>
      </ul>
      <div class="hero-actions" style="margin:22px 0 0"><a class="btn btn-navy" href="/services/appraisal/">Explore appraisal services</a><a class="btn btn-ghost" href="/about-us/">Meet your appraiser</a></div>
    </div>
    <div class="reveal-r frame-deco">
      <div class="frame">
        <img src="/assets/img/site/TX-Insurance-Appraiser-Trusted-Partner.webp" alt="Hurricane and fire damaged homes — the kinds of property losses TX Insurance Appraiser appraises" width="800" height="420" loading="lazy">
      </div>
      <div class="float-badge"><span class="ic-badge ic-gold" style="width:44px;height:44px;margin:0"><?= icon('award', 22) ?></span><div><b>Policyholder-side</b>Independent appraisal advocacy</div></div>
    </div>
  </div>
</section>

<section class="section bg-mist" id="services">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Insurance appraisal services</span>
      <h2>Everything you need to win the amount-of-loss dispute</h2>
      <p>TX Insurance Appraiser combines appraisal advocacy with professional estimating and 3D documentation, so the carrier sees a complete, defensible picture of your damage.</p>
    </div>
    <div class="grid g3">
      <?php
      $svc = [
          ['scale', 'Insurance Appraisal', '/services/appraisal/', 'We serve as your appraiser under the appraisal clause — scoping the damage, building the estimate and negotiating the award with the carrier’s appraiser.'],
          ['gavel', 'Umpire Services', '/services/umpire/', 'Neutral umpire services for Texas appraisals when the two appraisers reach an impasse on the amount of loss.'],
          ['cube', 'Matterport 3D Scans', '/services/matterport/', 'Immersive, measurable 3D scans that preserve every room and every damaged surface before repairs begin.'],
          ['calc', 'Xactimate Estimates', '/services/xactimate-estimate/', 'Line-item Xactimate estimates priced for your ZIP code — the same platform most Texas carriers use.'],
          ['doc', 'Symbility Estimates', '/services/symbility-estimate/', 'Symbility estimates for carriers and claims that run on the CoreLogic platform, built to match their format.'],
          ['search', 'Free Claim Review', '/contact-us/', 'Not sure appraisal is right? Send us your carrier estimate and we’ll give you a straight answer at no cost.'],
      ];
      foreach ($svc as $i => [$ic, $t, $u, $d]): ?>
      <article class="card tilt reveal d<?= $i % 3 + 1 ?>">
        <div class="ic-badge<?= $i === 5 ? ' ic-gold' : '' ?>"><?= icon($ic, 28) ?></div>
        <h3><a href="<?= $u ?>" style="text-decoration:none;color:inherit"><?= e($t) ?></a></h3>
        <p><?= e($d) ?></p>
        <a class="link-arrow" href="<?= $u ?>">Learn more <?= icon('arrow', 16) ?></a>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Why choose TX Insurance Appraiser?</span>
      <h2>Property damage appraisers who know how carriers build their numbers</h2>
      <p>Most underpaid claims aren’t a single big mistake — they’re dozens of small omissions. TX Insurance Appraiser finds them.</p>
    </div>
    <div class="grid g3">
      <?php
      $why = [
          ['award', 'Adjuster-level expertise', 'Our lead appraiser spent his career on the policyholder side of Texas property claims, so he knows where carrier estimates typically fall short.'],
          ['calc', 'Line-item precision', 'Waste factors, flashing, drip edge, ridge vents, code upgrades, matching, overhead and profit — we account for what is commonly left out.'],
          ['cube', 'Cutting-edge technology', 'Matterport, Xactimate and Symbility give the umpire and the carrier a clear, measurable record of the loss.'],
          ['map', 'Statewide coverage', 'With hubs in Austin, Waco, Dallas and Houston, we reach homes and businesses in 288 Texas cities quickly.'],
          ['scale', 'Fair and objective', 'Appraisal works because both sides present evidence. We build a defensible number, not an inflated one — which is what persuades umpires.'],
          ['chat', 'Straight communication', 'You’ll know where your appraisal stands at every step, by phone, text or email.'],
      ];
      foreach ($why as $i => [$ic, $t, $d]): ?>
      <div class="glass hero-card reveal d<?= $i % 3 + 1 ?>" style="padding:26px">
        <div class="ic-badge ic-gold"><?= icon($ic, 26) ?></div>
        <h3><?= e($t) ?></h3>
        <p style="color:#cfe0ee;margin:0"><?= e($d) ?></p>
      </div>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap person">
    <div class="person-photo reveal-l"><img src="<?= SITE['photo'] ?>" alt="Joseph Dittman, Texas insurance appraiser" width="500" height="500" loading="lazy"></div>
    <div class="reveal-r">
      <span class="eyebrow">Meet your appraiser</span>
      <h2>Joseph Dittman, Lead Appraiser at TX Insurance Appraiser</h2>
      <div class="badge-row">
        <span class="badge"><?= icon('shield', 16) ?> Texas-licensed public adjuster</span>
        <span class="badge"><?= icon('doc', 16) ?> TDI license #<?= SITE['appraiser']['license'] ?></span>
        <span class="badge"><?= icon('calc', 16) ?> Xactimate &amp; Symbility</span>
      </div>
      <p>Joseph Dittman has spent his career on the policyholder side of Texas property claims — inspecting hail, wind, water and fire losses, writing line-item estimates, and negotiating with carrier adjusters across the state. As the lead appraiser at TX Insurance Appraiser, he brings that same field experience to the appraisal table.</p>
      <p>His firm, Rise Public Adjusting LLC, holds Texas Department of Insurance public adjuster license #<?= SITE['appraiser']['license'] ?>, which you can verify on the <a href="<?= SITE['appraiser']['tdi_url'] ?>" target="_blank" rel="noopener">TDI license lookup</a>.</p>
      <a class="link-arrow" href="/about-us/">Read Joseph’s full background <?= icon('arrow', 16) ?></a>
    </div>
  </div>
</section>

<section class="section bg-mist" id="how-it-works">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">How the appraisal process works</span>
      <h2>Six steps from a lowball estimate to a binding award</h2>
      <p>Texas policies with an appraisal clause give both sides a faster, less expensive alternative to litigation for disputes about the amount of loss.</p>
    </div>
    <ol class="timeline">
      <li class="reveal"><h3>Free claim review</h3><p>Send us your carrier estimate, photos and policy. We compare the scope to the actual damage and tell you whether the gap justifies appraisal.</p></li>
      <li class="reveal"><h3>Demand estimate &amp; written appraisal demand</h3><p>A detailed estimate documents the true cost of repair. If the carrier still disagrees, a written demand invokes the appraisal clause in your policy.</p></li>
      <li class="reveal"><h3>Appraisers are named</h3><p>You appoint TX Insurance Appraiser; the carrier appoints its own appraiser. Most policies set a short deadline (often 20 days) for each side to name one.</p></li>
      <li class="reveal"><h3>Joint inspection &amp; documentation</h3><p>We inspect the property with the other appraiser, capture Matterport scans and measurements, and build or refine the line-item estimate.</p></li>
      <li class="reveal"><h3>Negotiation of the amount of loss</h3><p>The appraisers compare estimates line by line. Most disputes resolve here with an agreed award.</p></li>
      <li class="reveal"><h3>Umpire &amp; signed award</h3><p>If the appraisers can’t agree, a neutral umpire reviews both positions. An award signed by any two of the three sets the amount of loss.</p></li>
    </ol>
    <p class="center reveal"><a class="btn btn-navy" href="/what-is-an-appraisal/">What is an insurance appraisal? Read the full guide</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Claims we appraise</span>
      <h2>Texas weather is hard on property — and on claims</h2>
      <p>From Panhandle hail to Gulf Coast hurricanes, TX Insurance Appraiser handles the losses Texans actually face.</p>
    </div>
    <div class="peril-grid">
      <?php foreach ([
          ['hail', 'Hail damage', 'Roof, siding, gutter, window and HVAC damage that carriers often call “cosmetic” or repairable.', '/insurance-appraisal-for-hail-damage-claims/'],
          ['wind', 'Wind & tornado', 'Lifted shingles, creased tabs, structural damage and debris impact after straight-line winds.', '/tornado-damage-insurance/'],
          ['storm', 'Hurricane & tropical storm', 'Wind-driven rain, roof and envelope damage, and hurricane deductible disputes on the coast.', '/hurricane-damage-insurance/'],
          ['drop', 'Water & plumbing', 'Sudden pipe bursts, appliance leaks and hidden moisture damage behind walls and floors.', '/what-evidence-helps-during-insurance-appraisal/'],
          ['flame', 'Fire & smoke', 'Structural fire, soot and smoke contamination, and contents disputes after residential or commercial fires.', '/fire-damage/'],
          ['snow', 'Winter freeze', 'Freeze-related pipe failures and resulting water damage like the losses after Winter Storm Uri.', '/signs-your-insurance-claim-was-underpaid/'],
      ] as $i => [$ic, $t, $d, $u]): ?>
      <a class="peril reveal d<?= $i % 3 + 1 ?>" href="<?= $u ?>" style="text-decoration:none">
        <span class="ic-badge"><?= icon($ic, 22) ?></span>
        <div><h3><?= e($t) ?></h3><p><?= e($d) ?></p></div>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section bg-navy" style="padding-bottom:0">
  <div class="wrap split">
    <div class="reveal-l">
      <span class="eyebrow">Statewide insurance appraisers</span>
      <h2>Serving every corner of Texas</h2>
      <p style="color:#cfe0ee">With regional hubs in Austin, Waco, Dallas and Houston, TX Insurance Appraiser covers 288 cities — from Amarillo to Brownsville and El Paso to Beaumont. Looking for an insurance appraiser near you? Find your city below.</p>
      <div class="hero-actions"><a class="btn btn-gold" href="/areas/">View all service areas</a></div>
    </div>
    <div class="reveal-r map-wrap">
      <img src="/assets/img/site/Texas-Map.webp" alt="Map of Texas showing TX Insurance Appraiser hubs in Dallas, Waco, Austin and Houston" width="1600" height="532" loading="lazy">
      <?php foreach ($pins as [$n, $x, $y]): ?><span class="map-pin" style="left:<?= $x ?>%;top:<?= $y ?>%"><i></i><span><?= e($n) ?></span></span><?php endforeach; ?>
    </div>
  </div>
  <div class="wrap" style="padding-top:56px;padding-bottom:56px">
    <div class="featured-cities">
      <?php foreach ($featured as $i => $s): $c = $C[$s]; ?>
      <a class="fc reveal d<?= $i % 4 + 1 ?>" href="<?= city_url($s) ?>">
        <img src="<?= city_image($c) ?>" alt="<?= e($c['name']) ?> Insurance Appraiser service area" width="800" height="420" loading="lazy">
        <span><small><?= e($c['county']) ?> County</small><?= e($c['name']) ?> Insurance Appraiser</span>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
  <div class="marquee" aria-label="More Texas cities">
    <div class="marquee-track">
      <?php $list = array_slice(array_values($C), 230); for ($k = 0; $k < 2; $k++): foreach ($list as $c): ?>
      <a href="<?= city_url($c['slug']) ?>"<?= $k ? ' tabindex="-1" aria-hidden="true"' : '' ?>><?= icon('pin', 14) ?> <?= e($c['name']) ?></a>
      <?php endforeach; endfor; ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Free claim tools</span>
      <h2>Check your settlement before you sign</h2>
      <p>Built by TX Insurance Appraiser to help Texas property owners understand their numbers — free, private and instant.</p>
    </div>
    <div class="grid g3">
      <?php $i = 0; foreach (TOOLS as $slug => $t): if ($i++ > 2) break; ?>
      <a class="card tilt reveal" href="/tools/<?= $slug ?>/" style="text-decoration:none">
        <div class="ic-badge ic-gold"><?= icon($t['icon'], 26) ?></div>
        <h3><?= e($t['title']) ?></h3>
        <p><?= e($t['short']) ?></p>
        <span class="link-arrow">Open the tool <?= icon('arrow', 16) ?></span>
      </a>
      <?php endforeach; ?>
    </div>
    <p class="center reveal" style="margin-top:28px"><a class="btn btn-ghost" href="/tools/">See all free tools</a></p>
  </div>
</section>

<?php if ($latest): ?>
<section class="section bg-mist">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Latest articles</span>
      <h2>Insurance claim guides from TX Insurance Appraiser</h2>
    </div>
    <div class="grid g3">
      <?php foreach ($latest as $p): ?>
      <article class="card card-img reveal">
        <a class="ci-media" href="/<?= $p['slug'] ?>/"><img src="<?= post_image($p) ?>" alt="<?= e($p['h1']) ?>" width="700" height="394" loading="lazy"></a>
        <div class="ci-body">
          <span class="pill"><?= e($p['category'] ?? 'Guides') ?></span>
          <h3><a href="/<?= $p['slug'] ?>/" style="text-decoration:none;color:inherit"><?= e($p['h1']) ?></a></h3>
          <p><?= e($p['excerpt'] ?? '') ?></p>
          <a class="link-arrow" href="/<?= $p['slug'] ?>/">Read article <?= icon('arrow', 16) ?></a>
        </div>
      </article>
      <?php endforeach; ?>
    </div>
    <p class="center" style="margin-top:28px"><a class="btn btn-ghost" href="/blog/">Browse all articles</a></p>
  </div>
</section>
<?php endif; ?>

<?= faq_html($faqs, 'TX Insurance Appraiser FAQs') ?>
<?= cta_band('Experience the TX Insurance Appraiser difference', 'Make a quick call or send your carrier estimate. We’ll review it free and tell you honestly whether appraisal can close the gap.') ?>
<?php
$content = (string) ob_get_clean();
render_page([
    'title' => $title, 'description' => $desc, 'path' => '/',
    'preload' => '/assets/img/site/TX-Insurance-Appraiser-Hero-BG.webp',
    'schema' => [schema_webpage('WebPage', $title, $desc, '/'), schema_faq($faqs)],
], $content);
