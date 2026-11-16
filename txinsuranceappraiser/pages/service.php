<?php
/** /services/{slug}/ — five service pages sharing the long-form template. */
$S = [];

/* ------------------------------------------------------------------ APPRAISAL */
ob_start(); ?>
<p class="lead">TX Insurance Appraiser provides insurance appraisal services for Texas homeowners and businesses whose carriers accept a claim but underpay it. We serve as your appraiser under the policy’s appraisal clause — inspecting the damage, writing a line-item estimate, and negotiating a fair, binding award with the insurer’s appraiser or an umpire.</p>
<h2 id="what-we-do">What our insurance appraisal service includes</h2>
<p>When you appoint TX Insurance Appraiser, you get a complete, evidence-driven appraisal file — not just a signature on an award form. Every assignment includes:</p>
<ul>
  <li><strong>Policy and claim review</strong> — we read the appraisal clause, the carrier’s estimate and correspondence to define exactly what is in dispute.</li>
  <li><strong>Detailed property inspection</strong> — roof, exterior envelope, interior, attic and mechanical components, with measurements and photo documentation.</li>
  <li><strong>3D documentation</strong> with <a href="/services/matterport/">Matterport</a> on qualifying interior losses, so every room is preserved before repairs.</li>
  <li><strong>Line-item estimate</strong> in <a href="/services/xactimate-estimate/">Xactimate</a> or <a href="/services/symbility-estimate/">Symbility</a>, priced for your ZIP code and the date of loss.</li>
  <li><strong>Negotiation with the carrier’s appraiser</strong>, item by item, with supporting evidence for every disputed line.</li>
  <li><strong>Umpire presentation</strong> if the appraisers reach an impasse, including a written position and site walk-through.</li>
  <li><strong>Award review</strong> so you understand the replacement cost, actual cash value and depreciation figures in the final award.</li>
</ul>
<h2 id="property-damage-appraisers">Property damage appraisers for every type of Texas loss</h2>
<p>Our property damage appraisers handle the claims Texas weather and accidents create most often:</p>
<table>
  <thead><tr><th>Loss type</th><th>Typical disputes we resolve</th></tr></thead>
  <tbody>
    <tr><td>Hail</td><td>Repair vs. replacement, functional vs. “cosmetic” damage, soft-metal and siding damage, matching</td></tr>
    <tr><td>Wind &amp; tornado</td><td>Creased or lifted shingles, structural framing, fences, debris impact</td></tr>
    <tr><td>Hurricane</td><td>Hurricane/named-storm deductibles, wind-driven rain, envelope damage</td></tr>
    <tr><td>Water &amp; freeze</td><td>Hidden moisture, cabinets and flooring replacement, drying scope</td></tr>
    <tr><td>Fire &amp; smoke</td><td>Structural repair scope, soot cleaning vs. replacement, contents</td></tr>
  </tbody>
</table>
<p>We appraise single-family homes, <a href="/apartment-complex-insurance-appraisal/">apartment complexes</a>, <a href="/hoa-insurance-appraisal-process/">HOAs</a>, <a href="/church-insurance-appraisal-texas/">churches</a>, <a href="/commercial-property-insurance-appraisal-texas/">commercial buildings</a>, hotels, retail centers and industrial facilities.</p>
<h2 id="when-to-hire">When to hire an insurance claim appraiser</h2>
<p>Appraisal is designed for one problem: <strong>disagreement over the amount of a covered loss</strong>. It is usually the right move when:</p>
<ul>
  <li>The carrier approved the claim but its estimate is far below a qualified contractor’s bid.</li>
  <li>Your roof was paid as a spot repair when the damage supports full replacement.</li>
  <li>The estimate leaves out code items, flashing, waste, overhead and profit, or matching.</li>
  <li>Negotiation with the adjuster has stalled and you want a decision without filing suit.</li>
</ul>
<p>Run your numbers with our <a href="/tools/appraisal-cost-calculator/">Is Appraisal Worth It? calculator</a> before you decide.</p>
<h2 id="process">Our appraisal process</h2>
<ol>
  <li><strong>Free review.</strong> Send the carrier estimate, photos and policy. We tell you whether the gap is worth pursuing.</li>
  <li><strong>Engagement.</strong> Written fee agreement and appointment as your appraiser.</li>
  <li><strong>Inspection and estimate.</strong> We document the loss and build our line-item estimate.</li>
  <li><strong>Negotiation.</strong> We meet the opposing appraiser and work through every difference.</li>
  <li><strong>Umpire if needed.</strong> We present the evidence to the neutral umpire.</li>
  <li><strong>Award.</strong> A signed award sets the amount of loss; the carrier pays per the policy.</li>
</ol>
<h2 id="why-us">Why choose TX Insurance Appraiser</h2>
<p>Our lead appraiser, <a href="/about-us/">Joseph Dittman</a>, is a Texas-licensed public adjuster who has spent his career on the policyholder side of hail, wind, water and fire claims. He knows how carrier estimates are built and where they fall short — the exact knowledge an appraisal demands. With hubs in Austin, Waco, Dallas and Houston, we serve <a href="/areas/">288 Texas cities</a>, including <a href="/areas/houston-insurance-appraiser/">Houston</a>, <a href="/areas/dallas-insurance-appraiser/">Dallas</a>, <a href="/areas/san-antonio-insurance-appraiser/">San Antonio</a> and <a href="/areas/fort-worth-insurance-appraiser/">Fort Worth</a>.</p>
<div class="callout"><strong>Good to know:</strong> Appraisal decides the amount of loss, not coverage. TX Insurance Appraiser is not a law firm. If your carrier denied coverage, you may also want to consult a Texas attorney.</div>
<h2 id="costs">What does an insurance appraiser cost?</h2>
<p>Each side pays its own appraiser and shares the umpire’s fee. Our fee structure — percentage, flat or hourly depending on the claim — is explained in writing before you sign. We’ll also tell you plainly if we don’t think appraisal will produce a meaningful increase.</p>
<div class="callout callout-cta"><strong>Ready to close the gap?</strong> Call <?= e(SITE['phone']) ?> or <a href="/contact-us/">request a free claim review</a>.</div>
<?php
$S['appraisal'] = [
    'title' => 'Insurance Appraisal Services in Texas | TX Insurance Appraiser',
    'description' => 'Policyholder-side insurance appraisal services in Texas for underpaid hail, wind, hurricane, water and fire claims. Experienced property damage appraisers.',
    'h1' => 'Insurance Appraisal Services in Texas', 'eyebrow' => 'Insurance appraisal',
    'lead' => 'Experienced property damage appraisers who prove the true amount of your loss — and negotiate a fair, binding award when your carrier’s number falls short.',
    'image' => '/assets/img/site/TX-Insurance-Appraiser-Appraisals.webp', 'body' => (string) ob_get_clean(),
    'faqs' => [
        ['q' => 'What does an insurance appraiser do?', 'a' => 'An insurance appraiser determines the amount of a covered loss under the appraisal clause. They inspect the property, prepare or review line-item estimates, negotiate with the other side’s appraiser and, if needed, present the dispute to an umpire. An award signed by two of the three sets the amount owed.'],
        ['q' => 'Do I need an insurance appraiser near me?', 'a' => 'A local appraiser helps because pricing, building codes and weather patterns vary by region. TX Insurance Appraiser works from Austin, Waco, Dallas and Houston and travels throughout Texas, so you get regional knowledge wherever your property is.'],
        ['q' => 'Can appraisal be used for roof claims?', 'a' => 'Yes. Roof disputes are among the most common appraisals in Texas, especially repair-versus-replacement disagreements after hail and wind. Appraisers can weigh storm damage versus wear and tear when setting the amount of loss.'],
        ['q' => 'Does appraisal increase settlement amounts?', 'a' => 'It often does when the carrier’s estimate missed damage or underpriced repairs, but there is no guaranteed result. The award reflects the evidence, which is why a thorough inspection and estimate matter so much.'],
        ['q' => 'How quickly can TX Insurance Appraiser start?', 'a' => 'We typically review a new claim within one business day and can be appointed as your appraiser as soon as the fee agreement is signed, well within common 20-day policy deadlines.'],
    ],
];

/* --------------------------------------------------------------------- UMPIRE */
ob_start(); ?>
<p class="lead">An insurance umpire is the neutral third party who decides the disputed items when the two appraisers in a property insurance appraisal can’t agree. TX Insurance Appraiser provides umpire services across Texas — reviewing both appraisers’ positions, inspecting when needed, and signing a reasoned award on the amount of loss.</p>
<h2 id="what-umpire-does">What does an insurance umpire do?</h2>
<p>Most Texas appraisal clauses provide that the two appraisers select a competent, impartial umpire. The umpire only steps in on the items the appraisers cannot resolve. An award signed by the umpire and either appraiser becomes binding as to the amount of loss. Read more in <a href="/what-does-an-insurance-umpire-do/">what does an insurance umpire do?</a></p>
<ul>
  <li>Reviews each appraiser’s estimate, photos, measurements and reports</li>
  <li>Holds a conference or hearing with both appraisers</li>
  <li>Inspects the property when the evidence calls for it</li>
  <li>Decides each disputed line item and signs the award with one appraiser</li>
</ul>
<h2 id="how-umpires-are-chosen">How umpires are chosen in Texas</h2>
<p>The appraisers usually agree on an umpire within a set period — often 15 days. If they can’t, either party may ask a court of record in the county where the property is located to appoint one. Our guide on <a href="/how-insurance-umpires-are-chosen-in-texas/">how insurance umpires are chosen in Texas</a> covers the process in detail.</p>
<h2 id="qualities">What makes a good appraisal umpire?</h2>
<table>
  <thead><tr><th>Quality</th><th>Why it matters</th></tr></thead>
  <tbody>
    <tr><td>Impartiality</td><td>No financial interest in the outcome and no disqualifying relationship with either side.</td></tr>
    <tr><td>Construction knowledge</td><td>Able to evaluate roofing, framing, finishes and code requirements on the merits.</td></tr>
    <tr><td>Estimating fluency</td><td>Comfortable reading Xactimate and Symbility line items and pricing.</td></tr>
    <tr><td>Clear communication</td><td>Explains decisions so both sides understand the award.</td></tr>
  </tbody>
</table>
<h2 id="statewide">Umpire services throughout Texas</h2>
<p>We accept umpire appointments for residential and commercial appraisals in <a href="/areas/houston-insurance-appraiser/">Houston</a>, <a href="/areas/dallas-insurance-appraiser/">Dallas</a>, <a href="/areas/austin-insurance-appraiser/">Austin</a>, <a href="/areas/san-antonio-insurance-appraiser/">San Antonio</a>, <a href="/areas/fort-worth-insurance-appraiser/">Fort Worth</a> and <a href="/areas/">cities statewide</a>. To preserve impartiality, we do not serve as umpire on any claim where we have represented either party.</p>
<h2 id="impasse">When appraisers reach an impasse</h2>
<p>An impasse isn’t a failure — it’s exactly what the umpire provision is for. Understanding <a href="/what-is-an-impasse-in-insurance-appraisal/">what an impasse means</a> and <a href="/what-happens-if-appraisers-disagree/">what happens if appraisers disagree</a> helps both sides prepare clear, well-supported submissions.</p>
<div class="callout callout-cta"><strong>Need an umpire for a Texas appraisal?</strong> Call <?= e(SITE['phone']) ?> or <a href="/contact-us/">contact us</a> with the claim details and both appraisers’ information.</div>
<?php
$S['umpire'] = [
    'title' => 'Insurance Umpire Services in Texas | Appraisal Umpire',
    'description' => 'Neutral insurance umpire services for Texas property appraisals in Houston, Dallas, Austin, San Antonio, Fort Worth and statewide. Fair, reasoned awards.',
    'h1' => 'Insurance Umpire Services in Texas', 'eyebrow' => 'Appraisal umpire services',
    'lead' => 'A neutral, construction-savvy umpire for Texas appraisals that reach an impasse — fair decisions grounded in the evidence.',
    'image' => '/assets/img/site/TX-Insurance-Appraiser-Offers.webp', 'body' => (string) ob_get_clean(),
    'faqs' => [
        ['q' => 'Who pays the insurance umpire?', 'a' => 'Under most Texas appraisal clauses, the policyholder and the insurer split the umpire’s fee equally, while each side pays its own appraiser. Check your policy for the exact cost-sharing language.'],
        ['q' => 'Can a court appoint an umpire?', 'a' => 'Yes. If the two appraisers cannot agree on an umpire within the time set by the policy, either party may ask a court of record in the county where the property is located to appoint one.'],
        ['q' => 'Is the umpire’s decision binding?', 'a' => 'An award signed by the umpire and one appraiser is generally binding as to the amount of loss. Texas courts set awards aside only in narrow situations such as fraud, accident or mistake, or an award made without authority.'],
        ['q' => 'Does the umpire inspect the property?', 'a' => 'Often, yes. Many umpires inspect when the dispute involves the extent or cause of damage, such as hail versus wear on a roof. Others decide on the submitted estimates and photos when the dispute is purely about pricing.'],
    ],
];

/* ----------------------------------------------------------------- MATTERPORT */
ob_start(); ?>
<p class="lead">Matterport is a 3D capture technology that creates a measurable, walk-through digital twin of a property. TX Insurance Appraiser uses Matterport scans to document storm, water and fire damage room by room — preserving evidence before repairs begin and giving adjusters, appraisers and umpires an accurate view of the loss.</p>
<h2 id="why-matterport">Why Matterport matters for insurance claims</h2>
<p>Photos show fragments. A Matterport scan shows the whole property in context, with measurements you can take after the fact. That makes it powerful in appraisal, where the burden is on each side to prove the scope of damage.</p>
<ul>
  <li><strong>Preserve the scene</strong> before mitigation and repairs remove the evidence.</li>
  <li><strong>Measure accurately</strong> — room dimensions, wall areas and openings for precise estimates.</li>
  <li><strong>Share instantly</strong> with carriers, appraisers and umpires anywhere.</li>
  <li><strong>Reduce disputes</strong> about what was damaged and where.</li>
</ul>
<h2 id="what-we-capture">What we capture</h2>
<table>
  <thead><tr><th>Deliverable</th><th>How it helps your claim</th></tr></thead>
  <tbody>
    <tr><td>Interactive 3D tour</td><td>Lets reviewers “walk” the property and see damage in context.</td></tr>
    <tr><td>Measurements &amp; floor plans</td><td>Supports accurate quantities for flooring, drywall, paint and trim.</td></tr>
    <tr><td>High-resolution stills</td><td>Clear images of staining, charring, cracking and moisture damage.</td></tr>
    <tr><td>Tagged damage notes</td><td>Points out specific damage locations for the estimate and award.</td></tr>
  </tbody>
</table>
<h2 id="uses">Best uses for Matterport scans</h2>
<p>Matterport is most valuable on interior-heavy losses: <a href="/fire-damage/">fire and smoke damage</a>, water and freeze losses, <a href="/hotel-property-insurance-claims/">hotels</a>, <a href="/multi-family-insurance-claim-disputes/">multi-family buildings</a> and commercial spaces. For roofs, we pair it with field measurements and roof reports — see <a href="/eagleview-vs-matterport-for-insurance-claims/">EagleView vs. Matterport</a> for when each tool fits.</p>
<h2 id="learn-more">Learn more about Matterport</h2>
<p>New to the technology? Read <a href="/what-is-matterport/">what is Matterport?</a> and <a href="/power-of-matterport/">the power of Matterport in insurance documentation</a>.</p>
<div class="callout callout-cta"><strong>Document your loss before it’s gone.</strong> Call <?= e(SITE['phone']) ?> to schedule a Matterport scan anywhere in Texas.</div>
<?php
$S['matterport'] = [
    'title' => 'Matterport 3D Scanning for Insurance Claims in Texas',
    'description' => 'Matterport 3D scanning services for insurance claims in Texas. Measurable, shareable documentation of storm, water and fire damage for appraisal and claims.',
    'h1' => 'Matterport 3D Scanning for Insurance Claims', 'eyebrow' => 'Matterport services',
    'lead' => 'Immersive, measurable 3D scans that preserve every room and every damaged surface — evidence that holds up in appraisal.',
    'image' => '/assets/img/site/TX-Insurance-Appraiser-Matterport.webp', 'body' => (string) ob_get_clean(),
    'faqs' => [
        ['q' => 'How long does a Matterport scan take?', 'a' => 'A typical single-family home can usually be scanned in one to three hours depending on size and how many rooms are affected. Large commercial properties take longer and may be scheduled in phases.'],
        ['q' => 'Will my insurance company accept a Matterport scan?', 'a' => 'Matterport scans are widely used in the insurance and restoration industries. They don’t replace an estimate, but they give adjusters, appraisers and umpires a clear, measurable record of the damage to support one.'],
        ['q' => 'Do you offer Matterport scanning in Austin and San Antonio?', 'a' => 'Yes. TX Insurance Appraiser offers Matterport scanning throughout Texas, including Austin, San Antonio, Houston, Dallas, Fort Worth and Waco, as part of an appraisal or as a standalone documentation service.'],
        ['q' => 'Should I scan before or after mitigation?', 'a' => 'Ideally before demolition or major mitigation, so the original condition is preserved. Never delay necessary steps to prevent further damage; if mitigation must start immediately, scan as early as possible.'],
    ],
];

/* ------------------------------------------------------------------ XACTIMATE */
ob_start(); ?>
<p class="lead">An Xactimate estimate is a line-item repair estimate built in the Xactimate software that most U.S. insurance carriers use to price property claims. TX Insurance Appraiser writes detailed Xactimate estimates priced for your ZIP code, so your claim is presented in the same format and pricing database your insurer uses.</p>
<h2 id="why-xactimate">Why an independent Xactimate estimate matters</h2>
<p>When the carrier’s adjuster writes the only Xactimate estimate, small omissions add up quickly. An independent estimate lets you compare line by line and make the case for what was missed.</p>
<ul>
  <li>Same software and price lists the carrier uses — fewer arguments about format</li>
  <li>Regional pricing tied to your ZIP code and the date of loss</li>
  <li>Complete scopes including tear-off, disposal, permits and code items</li>
  <li>Clear notes and photos supporting every line</li>
</ul>
<h2 id="commonly-missed">Line items commonly missing from carrier estimates</h2>
<table>
  <thead><tr><th>Category</th><th>Often missed or underpaid</th></tr></thead>
  <tbody>
    <tr><td>Roofing</td><td>Starter course, drip edge, step and counter flashing, ridge vent, ice-and-water shield, steep and high charges</td></tr>
    <tr><td>Waste</td><td>Realistic waste factors for hips, valleys and cut-up roofs</td></tr>
    <tr><td>Exterior</td><td>Gutters and downspouts, window screens and wraps, paint on soft metals</td></tr>
    <tr><td>Interior</td><td>Matching flooring, full-wall paint, baseboard detach-and-reset, content manipulation</td></tr>
    <tr><td>General</td><td>Permits, code upgrades, dumpsters, overhead and profit</td></tr>
  </tbody>
</table>
<p>Dig deeper in <a href="/common-xactimate-line-items-missing-from-roof-claims/">common Xactimate line items missing from roof claims</a>, <a href="/how-roof-waste-factors-affect-insurance-estimates/">how roof waste factors affect estimates</a> and <a href="/why-flashing-is-commonly-missed-in-claims/">why flashing is commonly missed</a>.</p>
<h2 id="pricing">How Xactimate pricing works in Texas</h2>
<p>Xactimate price lists are updated regularly by region, which is why the same repair can price differently in Houston and Amarillo. Learn why in <a href="/how-xactimate-pricing-works-in-texas/">how Xactimate pricing works in Texas</a> and <a href="/why-xactimate-estimates-differ-by-zip-code/">why Xactimate estimates differ by ZIP code</a>. Comparing to a contractor bid? See <a href="/xactimate-vs-contractor-estimates/">Xactimate vs. contractor estimates</a>.</p>
<h2 id="tools">Check the math yourself</h2>
<p>Use our <a href="/tools/roof-square-calculator/">roof square &amp; waste calculator</a> to sanity-check roof quantities, and the <a href="/tools/recoverable-depreciation-calculator/">recoverable depreciation calculator</a> to understand RCV, ACV and holdback on your estimate.</p>
<div class="callout callout-cta"><strong>Need an Xactimate estimate?</strong> Call <?= e(SITE['phone']) ?> or <a href="/contact-us/">send us your carrier estimate</a> for a free comparison.</div>
<?php
$S['xactimate-estimate'] = [
    'title' => 'Xactimate Estimates for Insurance Claims in Texas',
    'description' => 'Independent Xactimate estimates for Texas insurance claims, priced by ZIP code. Find missing line items, waste and code upgrades in your carrier’s estimate.',
    'h1' => 'Xactimate Estimates for Texas Insurance Claims', 'eyebrow' => 'Xactimate estimating',
    'lead' => 'Line-item Xactimate estimates in the carriers’ own format — complete, ZIP-priced, and built to stand up in appraisal.',
    'image' => '/assets/img/site/TX-Insurance-Appraiser-Matterport-Xactimate.webp', 'body' => (string) ob_get_clean(),
    'faqs' => [
        ['q' => 'What is an Xactimate estimate?', 'a' => 'It is a repair or replacement estimate created in Xactimate, a widely used insurance estimating platform. It lists each task and material as a line item with regional unit pricing, so carriers and policyholders can compare scopes directly.'],
        ['q' => 'Why is my Xactimate estimate lower than my contractor’s bid?', 'a' => 'Carrier estimates often omit items, use low waste factors, or exclude overhead and profit, while contractor bids reflect real-world costs. An independent Xactimate estimate helps bridge the two in the carrier’s own format.'],
        ['q' => 'Can I use your Xactimate estimate without appraisal?', 'a' => 'Yes. Many clients use our estimate to support a supplement or reopen negotiations with the adjuster. If negotiation fails, the same estimate becomes the foundation of an appraisal.'],
        ['q' => 'Do Xactimate prices change by location?', 'a' => 'Yes. Price lists are set by region and updated over time, so labor and material costs can differ between Texas markets and between dates of loss.'],
    ],
];

/* ------------------------------------------------------------------ SYMBILITY */
ob_start(); ?>
<p class="lead">A Symbility estimate is a property claim estimate built in CoreLogic’s Symbility platform, used by a number of insurance carriers in place of Xactimate. TX Insurance Appraiser prepares accurate Symbility estimates so your claim can be compared line by line with carriers that run on this system.</p>
<h2 id="what-is-symbility">What is Symbility estimating software?</h2>
<p>Symbility is a cloud-based claims and estimating platform. Like Xactimate, it uses regional pricing and line-item scopes, but its structure, codes and terminology differ. When your carrier’s estimate comes from Symbility, presenting your position in the same format avoids translation arguments and speeds up negotiation.</p>
<h2 id="benefits">Benefits of a Symbility estimate from TX Insurance Appraiser</h2>
<ul>
  <li>Format that matches your carrier’s estimate for direct comparison</li>
  <li>Detailed scopes for roofing, exterior, interior and contents-related work</li>
  <li>Supporting photos, measurements and notes for each disputed item</li>
  <li>Ready for supplements, negotiation or a formal appraisal</li>
</ul>
<h2 id="symbility-vs-xactimate">Symbility vs. Xactimate</h2>
<table>
  <thead><tr><th></th><th>Symbility</th><th>Xactimate</th></tr></thead>
  <tbody>
    <tr><td>Developer</td><td>CoreLogic</td><td>Verisk</td></tr>
    <tr><td>Used by</td><td>A subset of carriers and TPAs</td><td>Most U.S. carriers and contractors</td></tr>
    <tr><td>Pricing</td><td>Regional price data</td><td>Regional price lists by ZIP/market</td></tr>
    <tr><td>Our approach</td><td colspan="2">We estimate in whichever platform your carrier uses so the comparison is apples to apples.</td></tr>
  </tbody>
</table>
<h2 id="when">When you need a Symbility estimate</h2>
<p>If your carrier’s estimate header or line codes reference Symbility, or the adjuster tells you they use it, a matching estimate is the cleanest way to dispute scope and pricing. We also handle <a href="/supplemental-insurance-claims-explained/">supplemental claims</a> and help you <a href="/can-you-dispute-a-scope-of-loss/">dispute a scope of loss</a>.</p>
<div class="callout callout-cta"><strong>Carrier uses Symbility?</strong> Call <?= e(SITE['phone']) ?> or <a href="/contact-us/">send us the estimate</a> and we’ll show you what’s missing.</div>
<?php
$S['symbility-estimate'] = [
    'title' => 'Symbility Estimates for Insurance Claims in Texas',
    'description' => 'Symbility estimating services for Texas property insurance claims. Accurate line-item estimates that match carriers using the CoreLogic Symbility platform.',
    'h1' => 'Symbility Estimates for Insurance Claims', 'eyebrow' => 'Symbility estimating',
    'lead' => 'Precise Symbility estimates that match your carrier’s format — so the conversation is about the damage, not the software.',
    'image' => '/assets/img/site/TX-Insurance-Appraiser-Matterport-Symbility.webp', 'body' => (string) ob_get_clean(),
    'faqs' => [
        ['q' => 'What is Symbility used for?', 'a' => 'Symbility is a claims management and estimating platform used by some insurers and third-party administrators to scope and price property damage claims, much like Xactimate.'],
        ['q' => 'Is a Symbility estimate accepted in appraisal?', 'a' => 'Yes. Appraisers and umpires evaluate the scope and pricing, not the brand of software. A well-documented Symbility or Xactimate estimate can support your position in appraisal.'],
        ['q' => 'Can you convert a Xactimate estimate to Symbility?', 'a' => 'We rebuild the scope in the platform your carrier uses rather than converting files, which keeps line items and pricing consistent with the carrier’s own estimate.'],
    ],
];

$s = $S[$service_slug];
$path = '/services/' . $service_slug . '/';
$names = ['appraisal' => 'Insurance Appraisal', 'umpire' => 'Umpire Services', 'matterport' => 'Matterport', 'xactimate-estimate' => 'Xactimate Estimate', 'symbility-estimate' => 'Symbility Estimate'];
render_longform($s + [
    'path' => $path,
    'crumbs' => [['Home', '/'], ['Services', '/services/'], [$names[$service_slug], $path]],
    'schema' => [schema_webpage('WebPage', $s['title'], $s['description'], $path), schema_service($s['h1'], $s['description'], $path)],
    'faq_heading' => $names[$service_slug] . ' FAQs',
    'related' => services_strip($service_slug),
]);
