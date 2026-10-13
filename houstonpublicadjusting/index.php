<?php
require __DIR__ . '/inc/layout.php';

$faqs = [
    ['What do Houston public adjusters do?', 'Houston public adjusters are licensed insurance professionals who represent the policyholder, not the insurance company. We inspect and document the damage, read your policy for every coverage that applies, build a line-item estimate, submit the claim and negotiate with the carrier until it is resolved.'],
    ['How much does a public adjuster in Houston, TX cost?', 'There is no upfront fee. A public adjuster in Houston, TX is paid a percentage of the claim money recovered, agreed in writing before any work starts. Texas law caps public adjuster fees at 10% of the claim settlement amount (Texas Insurance Code §4102.104). If we do not recover anything, you owe nothing. Use our <a href="/tools/public-adjuster-fee-calculator/">fee calculator</a> to see what you would net.'],
    ['When should I call a public adjuster in Houston?', 'As early as possible — ideally before the insurance company inspects. You should also call if your claim was denied, underpaid, delayed, or if the carrier keeps changing adjusters or asking for more paperwork. We can step in at almost any stage, including reopening a claim that was already paid.'],
    ['Are public adjusters in Houston licensed?', 'They must be. Every public adjuster in Texas has to hold a license from the Texas Department of Insurance (TDI). Our team works under Rise Public Adjusting LLC, Texas public adjuster license #3356839. You can verify any adjuster on the TDI license lookup before you sign.'],
    ['What is the difference between Houston public insurance adjusters and the insurance company adjuster?', 'The carrier’s staff or independent adjuster is hired by the insurance company and works to resolve the claim on the insurer’s terms. Houston public insurance adjusters are hired by you, owe their duty to you, and are paid only when you are. That difference shapes everything from the inspection to the final number.'],
    ['Do you handle hurricane, flood and commercial claims?', 'Yes. We handle hurricane and wind claims, hail and roof claims, water and burst-pipe losses, fire and smoke claims, freeze damage, and commercial property claims for offices, retail, apartments, warehouses and churches. For flood losses we help wherever coverage applies, including NFIP and private flood policies.'],
];

$hero = '
<section class="hero">
  <div class="wrap hero-in">
    <div>
      <p class="eyebrow">Licensed Texas public adjusters &middot; Greater Houston</p>
      <h1>Houston Public Adjusters <span>Fighting for Your Full Insurance Settlement</span></h1>
      <p class="lede">We work for you &mdash; not the insurance company. Our licensed Houston public adjusters handle the inspection, documentation and negotiation on hurricane, hail, water, fire and commercial property claims so you can pursue every dollar your policy allows.</p>
      <div class="hero-actions">
        <a class="btn btn-accent" href="tel:' . PHONE_E164 . '">Call ' . PHONE_DISPLAY . '</a>
        <a class="btn btn-ghost-light" href="sms:' . PHONE_E164 . '">Text ' . PHONE_DISPLAY . '</a>
      </div>
      <ul class="trust-row">
        <li>No upfront fees</li><li>TDI license #' . LICENSE_NO . '</li><li>Denied &amp; underpaid claims</li><li>Residential &amp; commercial</li>
      </ul>
    </div>
    <div class="hero-card">' . lead_form('lead-hero', 'Free Claim Review', 'Tell us what happened. A licensed public adjuster in Houston will call you back &mdash; no pressure, no obligation.', true) . '</div>
  </div>
</section>';

page_start([
    'title' => 'Houston Public Adjusters | Licensed Public Adjuster Houston TX',
    'desc' => 'Houston Public Adjusters represent policyholders, not insurance companies. Licensed public adjusters in Houston, TX for hurricane, hail, water, fire & denied claims. Free review: (832) 503-5866.',
    'path' => '/',
    'hero' => $hero,
    'schema' => [faq_schema($faqs)],
    'body_class' => 'home',
]);
?>
<section class="section tight">
  <div class="wrap">
    <div class="wx-mini" id="wx-mini" data-lat="<?= GEO_LAT ?>" data-lng="<?= GEO_LNG ?>">
      <div><p class="eyebrow" style="margin:0">Houston storm watch &middot; live</p><div class="wx-temp" data-wx="temp">--&deg;</div></div>
      <div><p class="wx-cond" data-wx="cond">Loading current conditions&hellip;</p><span class="skel" data-wx="station"></span></div>
      <div class="wx-status" data-wx="alerts"><span class="pill">Checking National Weather Service alerts&hellip;</span></div>
      <a class="btn btn-dark" href="/houston-weather/">Open live weather tracker</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap two-col center">
    <div>
      <p class="eyebrow">Why hire Houston public adjusters</p>
      <h2>Insurance Companies Have Adjusters. You Should Too.</h2>
      <p>Insurance carriers rely on experienced professionals to control payouts. Most policyholders face the process alone &mdash; often for the first time, and usually while they are still cleaning up after a storm. Houston Public Adjusters step in to level the playing field. We manage the technical work, challenge unfair assessments and protect your rights from the first inspection to the final check.</p>
      <p>Property damage doesn&rsquo;t discriminate, and neither do we. Houston Public Adjusters represent:</p>
      <ul class="checklist">
        <li>Homeowners with hurricane, storm, hail, fire or water damage</li>
        <li>Business owners facing property loss or business interruption</li>
        <li>Landlords and property managers with complex, multi-unit claims</li>
        <li>Policyholders with denied, delayed or underpaid settlements</li>
      </ul>
      <p><a class="btn btn-outline" href="/about-us/">Meet the team</a></p>
    </div>
    <div>
      <div class="table-wrap">
        <table class="compare">
          <thead><tr><th></th><th>Insurance company adjuster</th><th>Houston Public Adjusters</th></tr></thead>
          <tbody>
            <tr><td>Who they work for</td><td>The insurance carrier</td><td>You, the policyholder</td></tr>
            <tr><td>Goal</td><td>Close the file within the carrier&rsquo;s guidelines</td><td>Recover the full value your policy allows</td></tr>
            <tr><td>Caseload</td><td>Dozens of files after a big storm</td><td>Your claim gets dedicated attention</td></tr>
            <tr><td>Policy reading</td><td>Conservative, carrier-first</td><td>Every coverage that applies to you</td></tr>
            <tr><td>Estimate</td><td>Carrier&rsquo;s scope and pricing</td><td>Independent Xactimate line-item estimate</td></tr>
            <tr><td>Cost to you</td><td>&mdash;</td><td>$0 upfront; paid only from what we recover</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<section class="section alt" id="claims">
  <div class="wrap">
    <p class="eyebrow" style="text-align:center">Property insurance claims we handle</p>
    <h2 class="section-title">What Houston Public Adjusters Can Help You Recover</h2>
    <p class="section-lede">From Gulf hurricanes to spring hail and summer derechos, Houston property takes a beating. We provide hands-on representation for every major type of property loss.</p>
    <div class="card-grid">
      <div class="card icon-card"><div class="ic" aria-hidden="true">&#127744;</div><h3>Hurricane &amp; Wind Damage</h3><p>Roof, envelope and interior damage from hurricanes, tropical storms and straight-line winds &mdash; including percentage-deductible disputes.</p><a class="more" href="/services/#hurricane">Hurricane claims &rarr;</a></div>
      <div class="card icon-card"><div class="ic" aria-hidden="true">&#127784;</div><h3>Hail &amp; Roof Claims</h3><p>Bruised shingles, damaged soft metals, gutters, siding and skylights. We document what the first inspection missed.</p><a class="more" href="/services/#hail">Hail &amp; roof claims &rarr;</a></div>
      <div class="card icon-card"><div class="ic" aria-hidden="true">&#128167;</div><h3>Water &amp; Flood Losses</h3><p>Burst pipes, roof leaks, storm-driven rain, slab leaks and flood losses where coverage applies, plus mold as a secondary loss.</p><a class="more" href="/services/#water">Water claims &rarr;</a></div>
      <div class="card icon-card"><div class="ic" aria-hidden="true">&#128293;</div><h3>Fire &amp; Smoke Damage</h3><p>Structure, contents, smoke and soot contamination, firefighting water damage and additional living expenses.</p><a class="more" href="/services/#fire">Fire claims &rarr;</a></div>
      <div class="card icon-card"><div class="ic" aria-hidden="true">&#127970;</div><h3>Commercial Property</h3><p>Offices, retail, apartments, warehouses, churches and mixed-use buildings &mdash; including business interruption.</p><a class="more" href="/services/#commercial">Commercial claims &rarr;</a></div>
      <div class="card icon-card"><div class="ic" aria-hidden="true">&#9878;</div><h3>Denied, Delayed &amp; Reopened</h3><p>Denied or lowball claims, stalled files and previously settled claims that can still be supplemented or reopened.</p><a class="more" href="/services/#reopen">Claim disputes &rarr;</a></div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <h2 class="section-title">Why Property Owners Choose Our Houston Public Adjusters</h2>
    <p class="section-lede">A licensed public adjuster in Houston, TX who treats your claim like the financial recovery it is.</p>
    <div class="stats">
      <div class="stat"><b>$0</b><span>Upfront cost. Houston Public Adjusters are paid only from money we recover.</span></div>
      <div class="stat"><b>#<?= LICENSE_NO ?></b><span>Texas Department of Insurance public adjuster license (Rise Public Adjusting LLC).</span></div>
      <div class="stat"><b>1,400+</b><span>Claim files reviewed each year across our Texas public adjusting firm.</span></div>
      <div class="stat"><b>10% max</b><span>Texas law caps public adjuster fees at 10% of the settlement (Ins. Code &sect;4102.104).</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow" style="text-align:center">How it works</p>
    <h2 class="section-title">How Houston Public Adjusters Handle Your Claim</h2>
    <p class="section-lede">We keep the process transparent and straightforward. You are never left guessing what happens next.</p>
    <ol class="steps">
      <li><h3>Initial Consultation</h3><p>We review your situation, your policy and the carrier&rsquo;s position, then explain your options in plain English.</p></li>
      <li><h3>Property Inspection</h3><p>A detailed assessment of visible and hidden damage &mdash; photos, measurements, moisture readings and 3D documentation.</p></li>
      <li><h3>Policy Analysis</h3><p>We identify every applicable coverage, limit, deductible and endorsement, including code upgrade and ALE coverage.</p></li>
      <li><h3>Claim Preparation</h3><p>Accurate documentation and valuation built on industry-standard Xactimate pricing for the Houston market.</p></li>
      <li><h3>Negotiation</h3><p>Direct communication with the insurance company. We push back on low scopes, missing items and improper depreciation.</p></li>
      <li><h3>Resolution</h3><p>Support through settlement, supplements and final claim closure &mdash; and we stay available after the check arrives.</p></li>
    </ol>
    <p style="text-align:center;margin-top:28px"><a class="btn btn-accent" href="tel:<?= PHONE_E164 ?>">Talk to a Houston public adjuster: <?= PHONE_DISPLAY ?></a></p>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <p class="eyebrow" style="text-align:center">Free claim tools</p>
    <h2 class="section-title">Calculators From Houston Public Adjusters</h2>
    <p class="section-lede">Run the numbers on your own claim before you talk to anyone. Every tool runs in your browser &mdash; nothing is saved or sent.</p>
    <div class="card-grid">
      <a class="card tool-card" href="/tools/claim-settlement-calculator/"><span class="ic" aria-hidden="true">&#129518;</span><h3>Claim Settlement Calculator</h3><p>Estimate your check from RCV, depreciation and deductible.</p><span class="go">Open tool &rarr;</span></a>
      <a class="card tool-card" href="/tools/public-adjuster-fee-calculator/"><span class="ic" aria-hidden="true">&#128181;</span><h3>Public Adjuster Fee Calculator</h3><p>See what you net with and without representation.</p><span class="go">Open tool &rarr;</span></a>
      <a class="card tool-card" href="/tools/hurricane-deductible-calculator/"><span class="ic" aria-hidden="true">&#127744;</span><h3>Hurricane Deductible Calculator</h3><p>Turn a 1%&ndash;5% windstorm deductible into dollars.</p><span class="go">Open tool &rarr;</span></a>
      <a class="card tool-card" href="/tools/claim-deadline-calculator/"><span class="ic" aria-hidden="true">&#128197;</span><h3>Texas Claim Deadline Calculator</h3><p>Map the Texas Prompt Payment Act timeline for your claim.</p><span class="go">Open tool &rarr;</span></a>
    </div>
    <p style="text-align:center;margin-top:24px"><a href="/tools/">See all claim tools &rarr;</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">Local knowledge matters</p>
      <h2>Houston Public Adjusters Who Know Gulf Coast Claims</h2>
      <p>Houston&rsquo;s weather patterns, construction styles and insurance market create challenges that require local understanding. From Hurricane Ike and Harvey to Winter Storm Uri, the May 2024 derecho and Hurricane Beryl, we&rsquo;ve seen how insurers handle Houston-area claims &mdash; and where policyholders lose ground.</p>
      <p>That local experience lets our Houston public adjusters anticipate insurer tactics: blaming wind damage on &ldquo;wear and tear,&rdquo; calling water damage &ldquo;long-term seepage,&rdquo; or pricing a roof below what Houston contractors actually charge after a storm.</p>
      <p>If you have been searching for <strong>public adjusters Houston</strong> homeowners and business owners can trust, start with three checks: a Texas license, a written fee agreement and real local claim experience. Any <strong>public adjuster Houston, TX</strong> policyholders hire should be licensed by the Texas Department of Insurance (ours is #<?= LICENSE_NO ?>) and should explain the fee before you sign anything.</p>
      <p><a class="btn btn-outline" href="/houston-storm-history/">Explore Houston storm history</a></p>
    </div>
    <div>
      <h3>Areas we serve</h3>
      <p class="kw-note">Our public adjusters serve Houston and the surrounding communities across Harris, Fort Bend, Montgomery, Brazoria and Galveston counties:</p>
      <div class="area-grid">
<?php foreach (array_slice(AREAS, 0, 12) as $a): ?>
        <div class="area"><h3><?= e($a[0]) ?></h3><p><?= e($a[3]) ?> County</p></div>
<?php endforeach; ?>
      </div>
      <p style="margin-top:16px"><a href="/service-areas/">All service areas &rarr;</a></p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap two-col center">
    <div style="text-align:center">
      <img src="<?= AUTHOR['photo'] ?>" alt="Joseph Dittman, licensed Texas public adjuster with Houston Public Adjusters" width="340" height="340" loading="lazy" style="margin:0 auto;border-radius:50%">
    </div>
    <div>
      <p class="eyebrow">Meet your public adjuster</p>
      <h2>Joseph Dittman, Licensed Texas Public Adjuster</h2>
      <p>Joseph Dittman is the licensed public adjuster behind Houston Public Adjusters and its sister firm, TX Public Adjusting. He is licensed through Rise Public Adjusting LLC (Texas license #<?= LICENSE_NO ?>) and represents policyholders only &mdash; never insurance companies.</p>
      <p>Joseph documents every loss with Matterport 3D imaging and builds estimates in Xactimate and Symbility, the same software carriers use, so there is nothing for the insurer to dismiss as guesswork. He writes every guide on this site.</p>
      <p><a class="btn btn-dark" href="<?= AUTHOR['url'] ?>">Read Joseph&rsquo;s bio</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">Questions</p>
      <h2>Houston Public Adjusters FAQ</h2>
      <p>Straight answers about hiring a public adjuster in Houston. Have a question that isn&rsquo;t here? <a href="/faq/">See the full FAQ</a> or call <?= PHONE_DISPLAY ?>.</p>
      <?= faq_html($faqs) ?>
    </div>
    <div>
      <div class="side-card sticky" id="free-review">
        <h2 style="font-size:1.5rem">Start With a Free Claim Review</h2>
        <p>If your property has been damaged or your insurance claim doesn&rsquo;t feel right, don&rsquo;t guess. Houston Public Adjusters will review your situation, explain your options and help you decide the best next step &mdash; without pressure or obligation.</p>
        <?= lead_form('lead-home', '', '') ?>
      </div>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <h2 class="section-title">Latest Claim Guides From Houston Public Adjusters</h2>
    <p class="section-lede">Practical advice from Joseph Dittman on hail, fire, denied claims and when to bring in a public adjuster.</p>
    <?= post_cards(array_slice(array_keys(POSTS), 0, 6)) ?>
    <p style="text-align:center;margin-top:24px"><a class="btn btn-outline" href="/blog/">View all articles</a></p>
  </div>
</section>
<?php
$PAGE['scripts'] = ['/assets/js/weather.js'];
page_end();
