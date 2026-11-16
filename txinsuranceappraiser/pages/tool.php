<?php
/** /tools/{slug}/ — individual calculator pages. Logic lives in /assets/js/tools.js. */
$t = TOOLS[$tool_slug];
$path = '/tools/' . $tool_slug . '/';
$D = [];

/* ---------------------------------------------------------- depreciation */
$D['recoverable-depreciation-calculator'] = [
    'title' => 'Recoverable Depreciation Calculator (RCV vs ACV) | Free',
    'description' => 'Free recoverable depreciation calculator: enter RCV, depreciation and deductible to see your ACV check now and the depreciation holdback you can recover.',
    'h1' => 'Recoverable Depreciation Calculator',
    'lead' => 'See what your insurance company should pay now (actual cash value) and how much recoverable depreciation you can collect after repairs.',
    'form' => <<<HTML
<div class="tool" data-tool="depreciation"><div class="tool-grid">
  <div class="tool-in">
    <label>Replacement cost value (RCV) <span class="hint">Total from your carrier’s estimate</span><input type="number" min="0" step="100" name="rcv" value="24000" inputmode="decimal"></label>
    <label>How is depreciation shown?
      <select name="mode"><option value="amount">Dollar amount from my estimate</option><option value="age">Estimate it from age &amp; lifespan</option></select></label>
    <div data-show="amount"><label>Total depreciation <span class="hint">Sum of depreciation on the estimate</span><input type="number" min="0" step="50" name="dep" value="7200"></label></div>
    <div data-show="age" hidden><div class="row2">
      <label>Item age (years)<input type="number" min="0" step="1" name="age" value="8"></label>
      <label>Expected life (years)<input type="number" min="1" step="1" name="life" value="25"></label></div></div>
    <label>Non-recoverable portion of depreciation (%) <span class="hint">0% for most RCV policies; 100% if paid at ACV only (e.g. some roof schedules)</span><input type="number" min="0" max="100" step="5" name="nonrec" value="0"></label>
    <div class="row2">
      <label>Deductible ($)<input type="number" min="0" step="100" name="ded" value="2500"></label>
      <label>Prior payments ($)<input type="number" min="0" step="100" name="prior" value="0"></label>
    </div>
  </div>
  <div class="tool-out" aria-live="polite">
    <h2 style="font-size:1.1rem">Initial ACV payment</h2>
    <div class="big-num" data-out="acv">$0</div>
    <p style="margin:0;color:#cfe0ee">Paid after the deductible and prior payments.</p>
    <div class="bar"><i data-out="bar"></i></div>
    <ul class="out-rows">
      <li><span>Actual cash value (RCV − depreciation)</span><b data-out="acvgross">$0</b></li>
      <li><span>Recoverable depreciation (holdback)</span><b data-out="rec">$0</b></li>
      <li><span>Non-recoverable depreciation</span><b data-out="nonrecamt">$0</b></li>
      <li><span>Total you can receive after repairs</span><b data-out="total">$0</b></li>
    </ul>
    <p class="verdict" data-out="note">Complete repairs and submit invoices to recover the holdback.</p>
  </div>
</div></div>
HTML,
    'body' => '<h2 id="how-it-works">How recoverable depreciation works</h2><p>Most Texas homeowners policies pay replacement cost in two steps. First, the carrier pays the <strong>actual cash value (ACV)</strong> — the replacement cost minus depreciation, less your deductible. After you complete repairs and submit proof, it releases the <strong>recoverable depreciation</strong> it held back, up to what you actually spent.</p><table><thead><tr><th>Term</th><th>Meaning</th></tr></thead><tbody><tr><td>RCV</td><td>Cost to repair or replace with like kind and quality today</td></tr><tr><td>Depreciation</td><td>Reduction for age, wear and condition</td></tr><tr><td>ACV</td><td>RCV minus depreciation</td></tr><tr><td>Recoverable depreciation</td><td>Holdback you can collect after repairs</td></tr><tr><td>Non-recoverable depreciation</td><td>Depreciation you can’t recover (ACV-only coverage or schedules)</td></tr></tbody></table><h2 id="tips">Tips to recover your full depreciation</h2><ul><li>Check your policy for the deadline to complete repairs and claim the holdback.</li><li>Keep invoices, contracts and proof of payment.</li><li>Challenge excessive depreciation — labor generally shouldn’t be depreciated on many estimates, and age-based schedules can be applied too aggressively.</li><li>If the replacement cost itself is too low, depreciation math won’t fix it — consider <a href="/services/appraisal/">appraisal</a>.</li></ul><p>Read the full guide: <a href="/recoverable-depreciation-explained/">recoverable depreciation explained</a>.</p>',
    'faqs' => [
        ['q' => 'What is recoverable depreciation?', 'a' => 'Recoverable depreciation is the portion of depreciation an insurer holds back from the first payment on a replacement cost policy and pays after you complete repairs and document the cost. It closes the gap between actual cash value and replacement cost.'],
        ['q' => 'How do I get my depreciation back from insurance?', 'a' => 'Complete the repairs, then send the insurer the final invoice, contract and proof of payment within the policy’s time limit. The carrier then releases the recoverable depreciation up to the amount actually spent, subject to the policy terms.'],
        ['q' => 'What is non-recoverable depreciation?', 'a' => 'It is depreciation you cannot collect even after repairs — for example on actual cash value policies or roof payment schedules that pay ACV only. Your declarations page and endorsements show whether it applies.'],
    ],
];

/* ------------------------------------------------------------- appraisal */
$D['appraisal-cost-calculator'] = [
    'title' => 'Is Insurance Appraisal Worth It? Free Cost Calculator',
    'description' => 'Estimate whether insurance appraisal is worth it. Compare the carrier estimate to yours, factor in appraiser and umpire fees, and see your likely net gain.',
    'h1' => 'Is Appraisal Worth It? Cost vs. Recovery Calculator',
    'lead' => 'Compare your insurer’s number to your estimate, factor in appraisal costs, and see a realistic range for what appraisal could put in your pocket.',
    'form' => <<<HTML
<div class="tool" data-tool="appraisal"><div class="tool-grid">
  <div class="tool-in">
    <div class="row2">
      <label>Carrier’s estimate (RCV $)<input type="number" min="0" step="500" name="carrier" value="18000"></label>
      <label>Your / contractor estimate (RCV $)<input type="number" min="0" step="500" name="mine" value="42000"></label>
    </div>
    <label>Share of the gap you expect to recover: <b data-out="pctlabel">60%</b> <span class="hint">Conservative: 40–60%. Strong documentation: 60–85%.</span><input type="range" min="10" max="100" step="5" name="pct" value="60"></label>
    <label>Appraiser fee structure
      <select name="feetype"><option value="pct_increase">% of the increase</option><option value="pct_award">% of the total award</option><option value="flat">Flat fee</option></select></label>
    <label>Appraiser fee (% or $)<input type="number" min="0" step="1" name="fee" value="15"></label>
    <label>Estimated total umpire fee (you pay half) <span class="hint">Only if an umpire is needed</span><input type="number" min="0" step="250" name="umpire" value="3000"></label>
  </div>
  <div class="tool-out" aria-live="polite">
    <h2 style="font-size:1.1rem">Estimated net gain from appraisal</h2>
    <div class="big-num" data-out="net">$0</div>
    <div class="bar"><i data-out="bar"></i></div>
    <ul class="out-rows">
      <li><span>Gap between estimates</span><b data-out="gap">$0</b></li>
      <li><span>Expected award</span><b data-out="award">$0</b></li>
      <li><span>Expected increase</span><b data-out="inc">$0</b></li>
      <li><span>Your appraisal costs</span><b data-out="cost">$0</b></li>
    </ul>
    <p class="verdict" data-out="verdict"></p>
  </div>
</div></div>
HTML,
    'body' => '<h2 id="how-to-use">How to use this calculator</h2><p>Enter the replacement cost total from your carrier’s estimate and from a qualified contractor or independent estimate. The slider represents how much of the difference you expect the appraisal panel to award. Appraisal costs come out of the increase, so the calculator shows your estimated <strong>net</strong> gain.</p><h2 id="when-worth-it">When is appraisal usually worth it?</h2><ul><li>The gap is large relative to costs — many owners use several thousand dollars as a practical minimum.</li><li>The dispute is about amount, scope or pricing — not coverage.</li><li>You have documentation: photos, measurements, an itemized estimate.</li></ul><p>Learn more: <a href="/does-insurance-appraisal-increase-settlement-amounts/">does insurance appraisal increase settlement amounts?</a> and <a href="/how-long-does-an-insurance-appraisal-take/">how long appraisal takes</a>.</p><div class="callout"><strong>Note:</strong> Results are estimates only. Actual awards depend on the evidence, policy terms and the appraisal panel.</div>',
    'faqs' => [
        ['q' => 'Who pays for an insurance appraisal?', 'a' => 'Under most Texas appraisal clauses, each side pays its own appraiser and the two sides split the umpire’s fees and expenses equally. Your own appraiser’s fee structure is set by your agreement with them.'],
        ['q' => 'Is appraisal cheaper than a lawsuit?', 'a' => 'Usually, yes. Appraisal is typically faster and less expensive than litigation for disputes limited to the amount of loss, because it avoids court filings, discovery and trial.'],
        ['q' => 'What if appraisal awards less than I expected?', 'a' => 'The award reflects the evidence presented. That is why a thorough inspection and line-item estimate matter. A free review from TX Insurance Appraiser can tell you before you invoke whether your gap is well supported.'],
    ],
];

/* ------------------------------------------------------------------ roof */
$D['roof-square-calculator'] = [
    'title' => 'Roof Square Calculator with Pitch & Waste Factor | Free',
    'description' => 'Free roof square calculator: convert footprint and pitch to true roof area and squares, add a waste factor, and compare against your insurance estimate.',
    'h1' => 'Roof Square, Pitch & Waste Factor Calculator',
    'lead' => 'Turn a building footprint and roof pitch into true roof squares, apply a waste factor, and check the quantities on your insurance estimate.',
    'form' => <<<HTML
<div class="tool" data-tool="roof"><div class="tool-grid">
  <div class="tool-in">
    <label>Footprint area under the roof (sq ft) <span class="hint">Include eaves/overhangs. Or use length × width below.</span><input type="number" min="0" step="10" name="area" value="2400"></label>
    <div class="row2">
      <label>…or length (ft)<input type="number" min="0" step="1" name="len" placeholder="e.g. 60"></label>
      <label>width (ft)<input type="number" min="0" step="1" name="wid" placeholder="e.g. 40"></label>
    </div>
    <label>Roof pitch (rise per 12" run)
      <select name="pitch">
        <option value="2">2/12</option><option value="3">3/12</option><option value="4">4/12</option><option value="5">5/12</option><option value="6" selected>6/12</option><option value="7">7/12</option><option value="8">8/12</option><option value="9">9/12</option><option value="10">10/12</option><option value="12">12/12</option>
      </select></label>
    <label>Roof style (sets a typical waste factor)
      <select name="style"><option value="10">Simple gable — ~10%</option><option value="15" selected>Hip roof — ~15%</option><option value="18">Cut-up / complex — ~18%+</option><option value="custom">Custom</option></select></label>
    <label>Waste factor (%)<input type="number" min="0" max="40" step="1" name="waste" value="15"></label>
    <label>Squares on your insurance estimate (optional)<input type="number" min="0" step="0.1" name="carrier" placeholder="e.g. 28.5"></label>
  </div>
  <div class="tool-out" aria-live="polite">
    <h2 style="font-size:1.1rem">Squares to order (with waste)</h2>
    <div class="big-num" data-out="sqw">0</div>
    <ul class="out-rows">
      <li><span>Pitch multiplier</span><b data-out="mult">0</b></li>
      <li><span>True roof surface area</span><b data-out="surf">0 sq ft</b></li>
      <li><span>Measured squares (no waste)</span><b data-out="sq">0</b></li>
      <li><span>Shingle bundles (3 per square)</span><b data-out="bundles">0</b></li>
    </ul>
    <p class="verdict" data-out="cmp">Enter the squares from your estimate to compare.</p>
  </div>
</div></div>
HTML,
    'body' => '<h2 id="what-is-a-square">What is a roofing square?</h2><p>One roofing square equals <strong>100 square feet</strong> of roof surface. Because roofs are sloped, the surface area is larger than the footprint — the pitch multiplier accounts for that. A 6/12 roof, for example, has about 12% more surface than its footprint.</p><table><thead><tr><th>Pitch</th><th>Multiplier</th></tr></thead><tbody><tr><td>4/12</td><td>1.054</td></tr><tr><td>6/12</td><td>1.118</td></tr><tr><td>8/12</td><td>1.202</td></tr><tr><td>10/12</td><td>1.302</td></tr><tr><td>12/12</td><td>1.414</td></tr></tbody></table><h2 id="waste">Why waste factor matters on insurance estimates</h2><p>Shingles must be cut at hips, valleys, rakes and penetrations. Estimates that apply too little waste leave you short of material. Learn more in <a href="/how-roof-waste-factors-affect-insurance-estimates/">how roof waste factors affect insurance estimates</a> and <a href="/roof-measurements-for-insurance-claims/">roof measurements for insurance claims</a>.</p><div class="callout"><strong>Note:</strong> This tool gives planning estimates. Aerial reports or field measurements are needed for an accurate claim estimate.</div>',
    'faqs' => [
        ['q' => 'How many squares is my roof?', 'a' => 'Multiply the footprint area (including overhangs) by the pitch multiplier to get the true surface area, then divide by 100. Add the waste factor to get the number of squares to order.'],
        ['q' => 'What waste factor do insurance companies use?', 'a' => 'It varies by roof complexity. Simple gable roofs are often figured around 10%, hip roofs around 15%, and cut-up roofs higher. Estimates that use a flat low figure on complex roofs often come up short.'],
        ['q' => 'Do steep roofs cost more on an insurance estimate?', 'a' => 'Often, yes. Estimating platforms commonly add steep and high-roof labor charges for steeper pitches and multi-story roofs. Check your estimate for these line items.'],
    ],
];

/* -------------------------------------------------------------- deadlines */
$D['texas-claim-deadline-calculator'] = [
    'title' => 'Texas Insurance Claim Deadline Calculator (Ch. 542)',
    'description' => 'Free Texas insurance claim deadline calculator. Map prompt-payment deadlines under Texas Insurance Code Chapter 542 from your claim dates, plus appraisal timelines.',
    'h1' => 'Texas Insurance Claim Deadline Calculator',
    'lead' => 'Enter your claim dates to map the key deadlines Texas Insurance Code Chapter 542 generally sets for insurers — plus common appraisal-clause timelines.',
    'form' => <<<HTML
<div class="tool" data-tool="deadlines"><div class="tool-grid">
  <div class="tool-in">
    <label>Date you gave notice of the claim<input type="date" name="notice"></label>
    <label>Date the insurer received all requested items <span class="hint">Leave blank if not yet</span><input type="date" name="items"></label>
    <label>Date the insurer notified you it will pay <span class="hint">Optional</span><input type="date" name="accept"></label>
    <label>Date of written appraisal demand <span class="hint">Optional</span><input type="date" name="demand"></label>
    <label style="flex-direction:row;display:flex;gap:10px;align-items:center"><input type="checkbox" name="cat" style="width:auto"> Weather catastrophe or major disaster declared (adds 15 days)</label>
  </div>
  <div class="tool-out" aria-live="polite">
    <h2 style="font-size:1.1rem">Your key dates</h2>
    <table class="dl-table" data-out="table"><tr><td>Enter the date you reported the claim to begin.</td><td></td></tr></table>
    <p class="verdict" style="font-size:.85rem;font-weight:500">General information only — not legal advice. Deadlines can vary (for example, surplus lines insurers, policy terms, or extensions the insurer properly invokes). Confirm with your policy or a Texas attorney.</p>
  </div>
</div></div>
HTML,
    'body' => '<h2 id="chapter-542">Texas prompt-payment deadlines (Chapter 542)</h2><p>The Texas Prompt Payment of Claims Act generally requires insurers to move claims forward on a set schedule. Key steps include:</p><table><thead><tr><th>Step</th><th>General deadline</th></tr></thead><tbody><tr><td>Acknowledge the claim, begin investigation, request items</td><td>15 days after notice of claim</td></tr><tr><td>Accept or reject the claim</td><td>15 business days after receiving all requested items (may extend up to 45 days with notice)</td></tr><tr><td>Pay after agreeing to pay</td><td>5 business days</td></tr><tr><td>Weather catastrophe extension</td><td>Additional 15 days</td></tr></tbody></table><p>Read the statute at <a href="https://statutes.capitol.texas.gov/Docs/IN/htm/IN.542.htm" target="_blank" rel="noopener">statutes.capitol.texas.gov</a>.</p><h2 id="appraisal-timelines">Common appraisal-clause timelines</h2><p>Many Texas policies give each side about 20 days after a written appraisal demand to name an appraiser, and the appraisers about 15 days to agree on an umpire. Your policy controls — read <a href="/what-happens-after-invoking-the-appraisal-clause-in-texas/">what happens after invoking the appraisal clause in Texas</a>.</p><h2 id="542a">Chapter 542A pre-suit notice</h2><p>For many weather-related claims, Chapter 542A requires written notice at least 61 days before filing suit. Talk to a Texas attorney about legal deadlines.</p>',
    'faqs' => [
        ['q' => 'How long does an insurance company have to pay a claim in Texas?', 'a' => 'Under Chapter 542, after an insurer notifies you it will pay all or part of a claim, it generally must pay within five business days. Before that, it generally has 15 business days after receiving all requested items to accept or reject, with a possible extension up to 45 days.'],
        ['q' => 'What happens if my insurer misses a deadline?', 'a' => 'Chapter 542 provides for statutory interest and attorney’s fees in some circumstances when insurers violate prompt-payment requirements. Whether that applies depends on the facts; consult a Texas attorney.'],
        ['q' => 'Do deadlines change after a hurricane or major storm?', 'a' => 'Yes. When the governor declares a weather-related catastrophe or major natural disaster, the insurer’s Chapter 542 deadlines are generally extended by an additional 15 days.'],
    ],
];

/* --------------------------------------------------------------- checklist */
$groups = [
    'Policy & claim paperwork' => ['Full certified copy of the policy, declarations page and endorsements', 'Claim number and adjuster contact information', 'Every letter, email and text from the insurer', 'Carrier estimate(s) and any revised estimates', 'Proof of loss form (if requested) and the date submitted'],
    'Damage evidence' => ['Date-stamped photos and video of all damage, inside and out', 'Wide shots plus close-ups with a scale reference (coin, tape)', 'Matterport scan or room-by-room walkthrough video', 'Weather data for the date of loss (hail size, wind speeds)', 'Damaged material samples kept (shingles, siding pieces) where safe'],
    'Estimates & experts' => ['Itemized contractor or independent Xactimate/Symbility estimate', 'Roof measurements or aerial report', 'Engineer or specialist reports, if any', 'Code requirements / permit notes from your city', 'Matching evidence: discontinued product or color mismatch'],
    'Costs & mitigation' => ['Receipts for emergency repairs, tarps and board-up', 'Water mitigation / drying logs and invoices', 'Additional living expense receipts (hotel, meals, mileage)', 'Contents inventory with ages and replacement prices', 'Payments received from the insurer and dates'],
    'Timeline & deadlines' => ['Date of loss and date you reported the claim', 'Dates you sent requested items to the insurer', 'Policy deadline for repairs to recover depreciation', 'Appraisal demand date and appraiser deadlines', 'Log of every call: date, who you spoke with, what was said'],
];
$chk = '<div class="tool" data-tool="checklist" style="padding:28px"><div class="progress-ring" style="margin-bottom:20px"><div style="flex:1"><b data-out="count">0</b> of <span data-out="total">0</span> items complete<div class="bar" style="background:var(--line)"><i data-out="bar"></i></div></div><button class="btn btn-navy" type="button" onclick="window.print()">Print checklist</button><button class="btn btn-ghost" type="button" data-reset>Reset</button></div><div class="check-groups">';
$n = 0;
foreach ($groups as $g => $items) {
    $chk .= '<div class="check-group"><h3>' . e($g) . ' <small></small></h3>';
    foreach ($items as $it) {
        $chk .= '<label><input type="checkbox" data-k="c' . ($n++) . '"><span>' . e($it) . '</span></label>';
    }
    $chk .= '</div>';
}
$chk .= '</div><p style="font-size:.85rem;color:var(--ink-2);margin:18px 0 0">Your progress is saved privately in this browser only.</p></div>';
$D['claim-documentation-checklist'] = [
    'title' => 'Insurance Claim Documentation Checklist (Printable)',
    'description' => 'Free interactive insurance claim documentation checklist for Texas property owners. Track the evidence that wins appraisal disputes and print it anytime.',
    'h1' => 'Insurance Claim Documentation Checklist',
    'lead' => 'The evidence that wins appraisal disputes, in one interactive checklist. Tick items off as you go — your progress saves in your browser — and print it anytime.',
    'form' => $chk,
    'body' => '<h2 id="why-documentation">Why documentation decides appraisals</h2><p>Appraisers and umpires decide on evidence. A claim with clear photos, measurements, an itemized estimate and a paper trail is far easier to prove than one built on recollection. See <a href="/what-evidence-helps-during-insurance-appraisal/">what evidence helps during insurance appraisal</a> and <a href="/common-mistakes-during-insurance-appraisal/">common mistakes during insurance appraisal</a>.</p><h2 id="next">What to do next</h2><ul><li>Check your deadlines with the <a href="/tools/texas-claim-deadline-calculator/">Texas claim deadline calculator</a>.</li><li>Estimate your recovery with the <a href="/tools/appraisal-cost-calculator/">appraisal cost calculator</a>.</li><li>Get a <a href="/contact-us/">free claim review</a> from TX Insurance Appraiser.</li></ul>',
    'faqs' => [
        ['q' => 'What documents do I need for an insurance claim?', 'a' => 'At minimum: your full policy, the claim number, all insurer correspondence and estimates, dated photos and video of the damage, receipts for emergency repairs, and an itemized repair estimate. For appraisal, measurements and expert reports strengthen your position.'],
        ['q' => 'How should I photograph storm damage?', 'a' => 'Take wide shots to show location, then close-ups with a scale reference such as a coin or tape measure. Photograph every elevation, the roof if safe, and interior damage, before any repairs. Keep the original files with their date stamps.'],
    ],
];

$d = $D[$tool_slug];
ob_start(); ?>
<section class="hero hero-sm">
  <div class="orb orb-1"></div><div class="orb orb-2"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">Free tool</span>
      <h1 class="anim"><?= e($d['h1']) ?></h1>
      <p class="lead anim"><?= e($d['lead']) ?></p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:56px">
  <div class="wrap"><?= $d['form'] ?></div>
</section>
<section class="section bg-mist" style="padding-top:60px">
  <div class="wrap narrow"><article class="prose"><?= $d['body'] ?></article></div>
</section>
<section class="section-sm">
  <div class="wrap">
    <h2 class="sec-title reveal">More free tools</h2>
    <div class="grid g4">
      <?php foreach (TOOLS as $slug => $o): if ($slug === $tool_slug) continue; ?>
      <a class="card reveal" href="/tools/<?= $slug ?>/" style="text-decoration:none"><div class="ic-badge ic-gold"><?= icon($o['icon'], 24) ?></div><h3 style="font-size:1.05rem"><?= e($o['title']) ?></h3><span class="link-arrow">Open <?= icon('arrow', 16) ?></span></a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?= faq_html($d['faqs'], $t['title'] . ' FAQs') ?>
<?= cta_band('Numbers don’t add up?', 'TX Insurance Appraiser will review your carrier’s estimate free and tell you whether appraisal can close the gap.') ?>
<?php
$content = (string) ob_get_clean();
$app = ['@type' => 'WebApplication', 'name' => $d['h1'], 'url' => abs_url($path), 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any', 'description' => $d['description'],
    'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'], 'provider' => ['@id' => SITE['origin'] . '/#business']];
render_page([
    'title' => $d['title'], 'description' => $d['description'], 'path' => $path,
    'crumbs' => [['Home', '/'], ['Free Tools', '/tools/'], [$t['title'], $path]],
    'schema' => [schema_webpage('WebPage', $d['title'], $d['description'], $path), $app, schema_faq($d['faqs'])],
    'scripts' => ['/assets/js/tools.js'],
], $content);
