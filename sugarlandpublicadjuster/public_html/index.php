<?php
/**
 * Front controller for "/" (the homepage). Unknown URLs are routed to 404.php
 * by .htaccess, so this file only ever renders the homepage.
 */
require __DIR__ . '/inc/layout.php';

$faqs = [
    ['What does a Sugar Land public adjuster do?',
     '<p>A Sugar Land public adjuster is a licensed insurance professional who works for you, the policyholder. We inspect and document the damage, read your policy for every applicable coverage, build a detailed estimate, file or supplement the claim, and negotiate with your insurance company until the claim is resolved. The insurance company’s adjuster works for the carrier; a public adjuster in Sugar Land works only for you.</p>'],
    ['How much does a public adjuster in Sugar Land cost?',
     '<p>There are no upfront fees. We are paid a percentage of the settlement we help recover, and Texas law caps a public adjuster’s fee at 10% of the insurance settlement. Use our <a href="/tools/public-adjuster-fee-calculator/">public adjuster fee calculator</a> to see the math on your own claim.</p>'],
    ['When should I call a public adjuster after storm damage in Sugar Land?',
     '<p>As early as possible—ideally before the insurer’s inspection—but we can step in at almost any stage: after a denial, after a low offer, or even after a claim was closed if new damage is found. Early involvement prevents the most common mistakes, like recorded statements that narrow your claim or accepting a scope that misses hidden damage.</p>'],
    ['Can Sugar Land public adjusters help with a denied or underpaid claim?',
     '<p>Yes. Denied, delayed and underpaid claims are a large share of our work. We review the denial letter and the carrier’s estimate against your policy, document what was missed, and present a supplemented claim. When a dispute is over the amount of loss, many Texas policies also allow appraisal.</p>'],
    ['Do you handle commercial claims as well as homes?',
     '<p>Yes. We represent homeowners, landlords, HOAs and business owners—retail centers, offices, warehouses, churches and multi-family properties—across Sugar Land and Fort Bend County, including business interruption and contents losses.</p>'],
    ['Is a public adjuster the same as an attorney?',
     '<p>No. A public adjuster prepares, documents and negotiates the insurance claim. An attorney handles litigation and legal disputes. Most claims are resolved without a lawsuit; if yours needs legal action, we will tell you plainly.</p>'],
];

page_start([
    'title' => 'Sugar Land Public Adjuster | Free Claim Review | +1 (832) 503-5866',
    'og_title' => 'Sugar Land Public Adjuster — We Work for You, Not the Insurance Company',
    'description' => 'Sugar Land Public Adjuster represents policyholders, not insurers. Licensed public adjuster in Sugar Land, TX for hurricane, hail, water & fire claims.',
    'path' => '/',
    'page_type' => 'WebPage',
    'preload' => '/assets/img/hero-1600.webp',
    'schema' => [faq_schema($faqs, '/')],
    'body_class' => 'home',
]);
?>
<section class="hero">
  <img class="hero-bg" src="/assets/img/hero-1600.webp" alt="" width="1600" height="1067" fetchpriority="high">
  <div class="container hero-inner">
    <div>
      <p class="eyebrow">Licensed public adjusters · Sugar Land, Texas</p>
      <h1>Sugar Land Public Adjuster Fighting for Your Full Insurance Settlement</h1>
      <p class="lead"><strong>We work for you—not the insurance company.</strong> As your Sugar Land public adjuster, our licensed team handles the inspection, documentation and negotiation to help you pursue the full value of your hurricane, hail, water, fire or commercial property claim.</p>
      <ul class="hero-badges">
        <li>No upfront fees</li>
        <li>Fees capped by Texas law</li>
        <li>Denied &amp; underpaid claims</li>
        <li>Homes &amp; businesses</li>
      </ul>
      <div class="btn-row">
        <a class="btn btn-light" href="tel:<?= SITE['phone_href'] ?>">Call Us Today: <?= e(SITE['phone_display']) ?></a>
        <a class="btn btn-outline-light" href="sms:<?= SITE['phone_href'] ?>">Text a Photo of the Damage</a>
      </div>
    </div>
    <div class="hero-card" id="free-review">
      <h2>Get a free claim review</h2>
      <p>Tell a licensed public adjuster in Sugar Land what happened. We’ll call you back quickly to talk through your options.</p>
      <?php lead_form('hero', 'Homepage hero'); ?>
    </div>
  </div>
</section>

<div class="wx-strip" id="wx-strip">
  <div class="container wx-strip-inner">
    <span data-wx><span class="wx-pill">Live Sugar Land weather &amp; NWS alerts</span></span>
    <span><a href="/sugar-land-weather/">Open the storm center &rarr;</a></span>
  </div>
</div>

<section class="section">
  <div class="container">
    <h2 class="section-title">Insurance Companies Have Adjusters. You Should Too.</h2>
    <p class="section-intro">Insurance carriers rely on experienced professionals to control payouts. Most policyholders face the process alone—often for the first time. Sugar Land Public Adjuster steps in to level the playing field. We manage the technical work, challenge unfair assessments, and protect your rights from start to finish.</p>
    <p class="center"><strong>Property damage doesn’t discriminate, and neither do we. As a Sugar Land public adjuster, we represent:</strong></p>
    <div class="grid-4">
      <div class="card card-lav"><div class="icon" aria-hidden="true">🏠</div><p>Homeowners with storm, fire, or water damage.</p></div>
      <div class="card card-lav"><div class="icon" aria-hidden="true">🏢</div><p>Business owners facing property loss or interruptions.</p></div>
      <div class="card card-lav"><div class="icon" aria-hidden="true">🔑</div><p>Landlords and property managers with complex claims.</p></div>
      <div class="card card-lav"><div class="icon" aria-hidden="true">📄</div><p>Policyholders with denied, delayed, or underpaid settlements.</p></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">Property Insurance Claims We Handle</h2>
    <p class="section-intro">We provide hands-on representation for a wide range of property losses—residential and commercial, first-time and reopened. From first inspection to final settlement, your public adjuster in Sugar Land stays involved every step of the way.</p>
    <div class="grid-3">
      <div class="card linked"><div class="icon" aria-hidden="true">🌀</div><h3><a href="/services/hurricane-wind-damage-claims/">Hurricane &amp; Wind Damage</a></h3><p>Roof, siding, fence, tree-impact and wind-driven-rain claims after Gulf storms like Beryl and Ike—including hurricane-deductible disputes.</p><span class="card-more">Learn more &rarr;</span></div>
      <div class="card linked"><div class="icon" aria-hidden="true">🧊</div><h3><a href="/services/hail-damage-claims/">Hail Damage</a></h3><p>Bruised shingles, dented soft metals, cracked skylights and HVAC fins—documented properly so a “repair” doesn’t replace a needed replacement.</p><span class="card-more">Learn more &rarr;</span></div>
      <div class="card linked"><div class="icon" aria-hidden="true">💧</div><h3><a href="/services/water-damage-claims/">Water Damage &amp; Burst Pipes</a></h3><p>Slab leaks, burst pipes, appliance failures, roof leaks and mold-related secondary damage—one of the most underpaid claim types.</p><span class="card-more">Learn more &rarr;</span></div>
      <div class="card linked"><div class="icon" aria-hidden="true">🔥</div><h3><a href="/services/fire-smoke-damage-claims/">Fire &amp; Smoke Damage</a></h3><p>Structure, contents, smoke and soot contamination, odor remediation and additional living expenses after a fire.</p><span class="card-more">Learn more &rarr;</span></div>
      <div class="card linked"><div class="icon" aria-hidden="true">🌊</div><h3><a href="/services/flood-damage-claims/">Flood Claims</a></h3><p>NFIP and private flood claims for Brazos River and Oyster Creek–area flooding, with strict proof-of-loss deadlines.</p><span class="card-more">Learn more &rarr;</span></div>
      <div class="card linked"><div class="icon" aria-hidden="true">🏬</div><h3><a href="/services/commercial-property-claims/">Commercial Property</a></h3><p>Retail, office, industrial, multi-family and church properties, plus business interruption and equipment losses.</p><span class="card-more">Learn more &rarr;</span></div>
    </div>
    <p class="center mt-2"><a class="btn btn-outline" href="/services/denied-underpaid-claims/">Claim denied or underpaid? See how we reopen it</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">How the Process Works</h2>
    <p class="section-intro">We keep the process transparent and straightforward. Here is what working with a Sugar Land public adjuster looks like, from the first call to the final check.</p>
    <div class="process">
      <div class="step"><img src="/wp-content/uploads/2026/02/Initial-Consultation.webp" alt="Initial consultation with a Sugar Land public adjuster" width="640" height="427" loading="lazy"><div class="step-body"><h3>Initial Consultation</h3><p>We review your situation and explain your options—free, with no obligation.</p></div></div>
      <div class="step"><img src="/wp-content/uploads/2026/02/Property-Inspection.webp" alt="Property inspection of storm damage in Sugar Land" width="640" height="427" loading="lazy"><div class="step-body"><h3>Property Inspection</h3><p>A detailed assessment of damage and affected areas—visible and hidden.</p></div></div>
      <div class="step"><img src="/wp-content/uploads/2026/02/Policy-Analysis.webp" alt="Insurance policy analysis" width="640" height="360" loading="lazy"><div class="step-body"><h3>Policy Analysis</h3><p>Identification of applicable coverages, limits, endorsements and exclusions.</p></div></div>
      <div class="step"><img src="/wp-content/uploads/2026/02/Claim-Preparation.webp" alt="Insurance claim preparation and estimate" width="640" height="427" loading="lazy"><div class="step-body"><h3>Claim Preparation</h3><p>Accurate documentation, photos, measurements and line-item valuation.</p></div></div>
      <div class="step"><img src="/wp-content/uploads/2026/02/Negotiation.webp" alt="Negotiating with the insurance company" width="640" height="427" loading="lazy"><div class="step-body"><h3>Negotiation</h3><p>Direct communication with the insurance company—backed by evidence, not emotion.</p></div></div>
      <div class="step"><img src="/wp-content/uploads/2026/02/Resolution.webp" alt="Insurance claim resolution" width="640" height="427" loading="lazy"><div class="step-body"><h3>Resolution</h3><p>Support through settlement, recoverable depreciation and final claim closure.</p></div></div>
    </div>
    <p class="center mt-2">We stay involved from start to finish. You’re never left guessing what happens next.</p>
  </div>
</section>

<section class="section section-dark">
  <div class="container">
    <div class="split">
      <div>
        <p class="eyebrow" style="color:var(--lavender)">Why hire a public adjuster in Sugar Land</p>
        <h2>The insurer’s first offer is rarely the full value of the claim</h2>
        <p>Underpayment usually isn’t dramatic. It’s a missed line item, outdated pricing, depreciation applied too aggressively, or hidden damage that never made it into the scope. A Sugar Land public adjuster finds those gaps before you sign off.</p>
        <ul class="checklist">
          <li>Line-by-line policy review, including endorsements most people never read</li>
          <li>Detailed estimates in the same software insurers use, priced for the Houston market</li>
          <li>Moisture mapping, roof measurements and photo documentation</li>
          <li>Recoverable depreciation, code upgrades and additional living expenses tracked to the end</li>
        </ul>
      </div>
      <div class="mini-calc tool" id="mini-calc">
        <h3>Quick check: how big is your claim gap?</h3>
        <div class="tool-grid">
          <label>Insurer’s offer <span class="money"><input type="number" min="0" step="100" id="mc-offer" value="12000" inputmode="decimal"></span></label>
          <label>Contractor’s estimate <span class="money"><input type="number" min="0" step="100" id="mc-est" value="27500" inputmode="decimal"></span></label>
        </div>
        <div class="tool-results">
          <div class="result-grid">
            <div class="result bad"><span>Gap</span><strong id="mc-gap">$15,500</strong></div>
            <div class="result"><span>Offer covers</span><strong id="mc-pct">44%</strong></div>
          </div>
          <div class="bar"><i id="mc-bar" style="width:44%"></i></div>
          <p class="small mb-0">Big gap? <a href="/tools/insurance-claim-settlement-calculator/">Run the full settlement calculator</a> or ask a Sugar Land public adjuster to review it free.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="team-card">
      <img src="<?= e(AUTHOR['image']) ?>" alt="Joseph Dittman, licensed public adjuster serving Sugar Land, TX" width="240" height="240" loading="lazy">
      <div>
        <p class="eyebrow">Meet your public adjuster</p>
        <h2>Joseph Dittman, Licensed Texas Public Adjuster</h2>
        <p>Joseph Dittman leads claims for Sugar Land Public Adjuster through <?= e(SITE['firm']) ?> (Texas license #<?= e(SITE['firm_license']) ?>), the firm behind TX Public Adjusting. His team documents losses with tools like Matterport 3D imaging and builds estimates in Xactimate and Symbility—the same platforms insurance carriers use—so every line item can be defended.</p>
        <p>Joseph writes every guide on this site, from <a href="/why-use-a-public-adjuster/">why use a public adjuster</a> to <a href="/fire-insurance-adjuster-secrets/">fire claim strategy</a>. When you call Sugar Land Public Adjuster, you get a licensed professional who takes your loss personally—not a call center.</p>
        <div class="btn-row"><a class="btn btn-primary" href="<?= e(AUTHOR['url']) ?>">Read Joseph’s profile</a><a class="btn btn-outline" href="tel:<?= SITE['phone_href'] ?>">Call <?= e(SITE['phone_display']) ?></a></div>
      </div>
    </div>
  </div>
</section>

<section class="section section-lav">
  <div class="container split split-60">
    <div>
      <h2>Local Knowledge Matters</h2>
      <p>Sugar Land’s weather patterns, construction styles, and insurance market create challenges that require local understanding. From Gulf hurricanes and spring hail to Brazos River flooding and the 2021 freeze, we’ve seen how insurers handle Sugar Land-area claims—and where policyholders often lose ground.</p>
      <p>That local experience allows us to anticipate insurer tactics and protect your interests more effectively. A Sugar Land public adjuster knows that Fort Bend County sits outside the Texas Windstorm Insurance Association’s coastal territory, so wind coverage usually comes through your standard homeowners policy—often with a separate named-storm or wind/hail deductible that deserves a close read.</p>
      <p>Our Sugar Land public adjusters serve every neighborhood in the city and the surrounding Fort Bend communities, including:</p>
      <ul class="chips">
        <li>First Colony</li><li>Telfair</li><li>Riverstone</li><li>Greatwood</li><li>New Territory</li><li>Sugar Creek</li><li>Avalon</li><li>Commonwealth</li><li>Imperial</li><li>Sugar Lakes</li><li>Settlers Park</li><li>Lake Pointe</li><li>Missouri City</li><li>Stafford</li><li>Richmond</li><li>Rosenberg</li><li>Fulshear</li>
      </ul>
      <p class="mt-2"><a href="/service-areas/">See all service areas &rarr;</a></p>
    </div>
    <div class="card">
      <h3>Sugar Land storm record at a glance</h3>
      <ul class="checklist purple">
        <li><strong>Hurricane Harvey (2017):</strong> the Brazos River at Richmond crested at a record 55.19 ft.</li>
        <li><strong>Winter Storm Uri (2021):</strong> days of hard freeze and burst pipes across Fort Bend County.</li>
        <li><strong>Hurricane Beryl (2024):</strong> wind damage, falling trees and multi-day outages.</li>
        <li><strong>Every spring:</strong> severe thunderstorms with hail and damaging straight-line winds.</li>
      </ul>
      <a class="btn btn-primary btn-block" href="/sugar-land-storm-history/">Explore Sugar Land storm history</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">Free Claim Tools &amp; Calculators</h2>
    <p class="section-intro">Built by a Sugar Land public adjuster to help you understand your claim before you talk to anyone—free, private, and nothing to download.</p>
    <div class="grid-3">
      <div class="card linked"><div class="icon" aria-hidden="true">🧮</div><h3><a href="/tools/insurance-claim-settlement-calculator/">Claim Settlement Calculator</a></h3><p>Compare the insurer’s payment to your real repair cost after deductible and depreciation.</p></div>
      <div class="card linked"><div class="icon" aria-hidden="true">📉</div><h3><a href="/tools/depreciation-calculator/">Depreciation (ACV) Calculator</a></h3><p>Estimate actual cash value and how much recoverable depreciation you can still collect.</p></div>
      <div class="card linked"><div class="icon" aria-hidden="true">💲</div><h3><a href="/tools/public-adjuster-fee-calculator/">Public Adjuster Fee Calculator</a></h3><p>See your net recovery with and without representation under the Texas fee cap.</p></div>
      <div class="card linked"><div class="icon" aria-hidden="true">🌀</div><h3><a href="/tools/hurricane-deductible-calculator/">Hurricane Deductible Calculator</a></h3><p>Turn a percentage deductible into dollars before the next storm hits.</p></div>
      <div class="card linked"><div class="icon" aria-hidden="true">📅</div><h3><a href="/tools/claim-deadline-calculator/">Texas Claim Deadline Calculator</a></h3><p>Map the insurer’s Texas Prompt Payment deadlines from the day you file.</p></div>
      <div class="card linked"><div class="icon" aria-hidden="true">📋</div><h3><a href="/tools/home-inventory-checklist/">Home Inventory Builder</a></h3><p>List your belongings room by room and export a spreadsheet for your contents claim.</p></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container narrow">
    <h2 class="section-title">Sugar Land Public Adjuster FAQ</h2>
    <p class="section-intro">Looking for a public adjuster Sugar Land homeowners and business owners can trust? Here are straight answers to the questions we hear most across Fort Bend County.</p>
    <?php faq_list($faqs, true); ?>
    <p class="center"><a href="/faq/">More questions answered &rarr;</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">Latest Articles</h2>
    <p class="section-intro">Claim guides written by Joseph Dittman, Sugar Land public adjuster.</p>
    <div class="post-grid">
<?php foreach (array_slice(POSTS, 0, 3) as $p) post_card($p); ?>
    </div>
    <p class="center mt-2"><a class="btn btn-outline" href="/blog/">View all articles</a></p>
  </div>
</section>

<section class="section section-lav">
  <div class="container split">
    <div>
      <h2>Start With a Free Claim Review</h2>
      <p>If your property has been damaged or your insurance claim doesn’t feel right, don’t guess. Start with a conversation.</p>
      <p>We’ll review your situation, explain your options, and help you decide the best next step—without pressure or obligation. Call or text <?= tel_link() ?>, email <a href="mailto:<?= e(SITE['email']) ?>"><?= e(SITE['email']) ?></a>, or use the form.</p>
      <p><strong>Sugar Land Public Adjuster is here to protect your claim, your property, and your peace of mind.</strong></p>
    </div>
    <div class="form-card"><?php lead_form('bottom', 'Homepage bottom', true); ?></div>
  </div>
</section>
<?php
$mini = <<<'JS'
<script>
(function(){var o=document.getElementById('mc-offer'),s=document.getElementById('mc-est');if(!o)return;
function f(n){return '$'+Math.round(n).toLocaleString('en-US');}
function u(){var a=+o.value||0,b=+s.value||0,g=Math.max(0,b-a),p=b>0?Math.min(100,a/b*100):0;
document.getElementById('mc-gap').textContent=f(g);document.getElementById('mc-pct').textContent=Math.round(p)+'%';document.getElementById('mc-bar').style.width=p+'%';}
o.addEventListener('input',u);s.addEventListener('input',u);u();})();
</script>
JS;
page_end(['scripts' => $mini]);
