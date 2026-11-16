<?php
$title = 'About Us: Joseph Dittman, Texas Insurance Appraiser';
$desc  = 'Meet Joseph Dittman, lead appraiser at TX Insurance Appraiser — a Texas-licensed public adjuster who inspects, estimates and negotiates property claims statewide.';
$A = SITE['appraiser'];
$faqs = [
    ['q' => 'Who is the appraiser at TX Insurance Appraiser?',
     'a' => 'Joseph Dittman is the lead appraiser at TX Insurance Appraiser. He is a Texas-licensed public adjuster who has spent his career on the policyholder side of property claims, inspecting hail, wind, water and fire losses, writing line-item estimates and negotiating with carrier adjusters across Texas.'],
    ['q' => 'How can I verify Joseph Dittman’s license?',
     'a' => 'Rise Public Adjusting LLC, Joseph’s firm, holds Texas Department of Insurance public adjuster license #3356839. You can confirm it on the TDI agent and adjuster license lookup at tdi.texas.gov by searching the license number or the firm name.'],
    ['q' => 'Will Joseph act as my public adjuster or my appraiser?',
     'a' => 'On an appraisal assignment through TX Insurance Appraiser, Joseph serves as your appraiser under the policy’s appraisal clause, focused on the amount of loss. He does not act as your public adjuster or attorney on that claim, and TX Insurance Appraiser does not provide legal advice.'],
    ['q' => 'What types of properties does TX Insurance Appraiser handle?',
     'a' => 'TX Insurance Appraiser handles single-family homes, multi-family and apartment properties, HOAs, churches, retail, office, hotel and industrial buildings. Typical losses include hail, wind, tornado, hurricane, water, freeze, fire and smoke damage anywhere in Texas.'],
];
ob_start(); ?>
<section class="hero hero-split">
  <div class="hero-bg" style="background-image:url(/assets/img/site/TX-Insurance-Appraiser-Mission.webp)"></div>
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">About TX Insurance Appraiser</span>
      <h1 class="anim">Your trusted partner in Texas insurance appraisal</h1>
      <p class="lead anim">TX Insurance Appraiser exists for one reason: to make sure Texas property owners have a qualified, experienced professional on their side when the amount of a covered loss is in dispute.</p>
      <div class="hero-actions anim">
        <a class="btn btn-gold btn-lg" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone', 20) ?> Call us</a>
        <a class="btn btn-ghost-light btn-lg" href="/contact-us/">Send us a message</a>
      </div>
    </div>
    <div class="glass hero-card anim">
      <ul class="facts">
        <li><b>Lead appraiser</b>Joseph Dittman</li>
        <li><b>TDI license</b>#<?= e($A['license']) ?></li>
        <li><b>Hubs</b>Austin · Waco · Dallas · Houston</li>
        <li><b>Coverage</b>All of Texas</li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="joseph-dittman">
  <div class="wrap person">
    <div class="person-photo reveal-l"><span class="init">JD</span></div>
    <div class="reveal-r">
      <span class="eyebrow">Meet the appraiser</span>
      <h2>Joseph Dittman — Lead Insurance Appraiser</h2>
      <div class="badge-row">
        <span class="badge"><?= icon('shield', 16) ?> Texas-licensed public adjuster</span>
        <span class="badge"><?= icon('doc', 16) ?> TDI license #<?= e($A['license']) ?></span>
        <span class="badge"><?= icon('hail', 16) ?> Hail · Wind · Water · Fire</span>
        <span class="badge"><?= icon('calc', 16) ?> Xactimate &amp; Symbility</span>
      </div>
      <p>Joseph Dittman is a Texas-licensed public adjuster who has spent his career on the policyholder side of property claims. He has inspected hail, wind, water and fire losses, written line-item estimates, and negotiated with carrier adjusters in every region of the state — from Panhandle hailstorms to Gulf Coast hurricanes.</p>
      <p>That background is exactly what an appraisal demands. As the lead appraiser at TX Insurance Appraiser, Joseph knows how carrier estimates are assembled, where scopes typically come up short, and how to present a documented, defensible amount of loss to the opposing appraiser or an umpire.</p>
      <p>His firm, Rise Public Adjusting LLC, holds Texas Department of Insurance public adjuster license <strong>#<?= e($A['license']) ?></strong>, which you can verify on the <a href="<?= e($A['tdi_url']) ?>" target="_blank" rel="noopener">TDI license lookup</a>. On an appraisal assignment, Joseph acts as your appraiser under the policy’s appraisal clause — not as your public adjuster or attorney on that claim.</p>
    </div>
  </div>
</section>

<section class="section bg-mist">
  <div class="wrap split">
    <div class="reveal-l">
      <span class="eyebrow">Who we are</span>
      <h2>The impartial, construction-savvy voice in appraisal</h2>
      <p>At TX Insurance Appraiser, we position ourselves as a fair and knowledgeable voice in appraisal matters, bringing construction expertise and extensive claim experience to every file. We proudly serve as the policyholder’s appraiser, committed to accuracy and objectivity in every assessment.</p>
      <p>Our understanding of construction methods, material pricing and Texas building codes lets us produce evaluations that hold up to scrutiny. That matters, because umpires side with the better-documented number — not the bigger one.</p>
      <p>Whether you are navigating an active dispute or simply want a second opinion on a carrier estimate, TX Insurance Appraiser gives you a clear, honest assessment of where you stand.</p>
    </div>
    <div class="reveal-r frame-deco"><div class="frame"><img src="/assets/img/site/TX-Insurance-Appraiser-Approach.webp" alt="TX Insurance Appraiser team member reviewing an insurance appraisal with a property owner" width="800" height="420" loading="lazy"></div></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head reveal">
      <span class="eyebrow">Mission, approach &amp; values</span>
      <h2>What guides every TX Insurance Appraiser assignment</h2>
    </div>
    <div class="grid g3">
      <div class="card reveal"><div class="ic-badge"><?= icon('award', 26) ?></div><h3>Our mission</h3><p>To stand as a reliable source of fairness in the complicated world of property insurance appraisals — giving Texas policyholders an appraiser whose estimate is rooted in real construction knowledge.</p></div>
      <div class="card reveal d1"><div class="ic-badge"><?= icon('search', 26) ?></div><h3>Our approach</h3><p>Inspect thoroughly, document everything, estimate line by line, and negotiate on evidence. We prepare every file as if it will go to an umpire.</p></div>
      <div class="card reveal d2"><div class="ic-badge ic-gold"><?= icon('scale', 26) ?></div><h3>Our values</h3><p><strong>Fairness</strong> in every number. <strong>Objectivity</strong> rooted in construction facts. <strong>Knowledge</strong> that helps clients make informed decisions.</p></div>
    </div>
  </div>
</section>

<section class="section bg-navy">
  <div class="wrap">
    <div class="sec-head reveal"><span class="eyebrow">Why choose TX Insurance Appraiser?</span><h2>Experience you can see in the estimate</h2></div>
    <div class="grid g4">
      <?php foreach ([
          ['award', 'Expertise', 'Years on the policyholder side of Texas property claims.'],
          ['cube', 'Technology', 'Matterport, Xactimate and Symbility on every qualifying file.'],
          ['map', 'Regional coverage', 'Austin, Waco, Dallas and Houston hubs serving all of Texas.'],
          ['chat', 'Communication', 'Real updates by phone, text and email throughout the appraisal.'],
      ] as $i => [$ic, $t, $d]): ?>
      <div class="glass hero-card reveal d<?= $i + 1 ?>"><div class="ic-badge ic-gold"><?= icon($ic, 24) ?></div><h3><?= e($t) ?></h3><p style="color:#cfe0ee;margin:0"><?= e($d) ?></p></div>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<?= faq_html($faqs, 'About TX Insurance Appraiser: FAQs') ?>
<?= cta_band('Work with TX Insurance Appraiser', 'Make a quick call or send your carrier estimate. Joseph will review it and tell you whether appraisal makes sense.') ?>
<?php
$content = (string) ob_get_clean();
$person = schema_webpage('AboutPage', $title, $desc, '/about-us/');
$person['mainEntity'] = ['@id' => SITE['origin'] . '/#joseph-dittman'];
render_page([
    'title' => $title, 'description' => $desc, 'path' => '/about-us/',
    'crumbs' => [['Home', '/'], ['About Us', '/about-us/']],
    'schema' => [$person, schema_faq($faqs)],
], $content);
