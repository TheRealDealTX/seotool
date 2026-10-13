<?php
return [
    'title'       => 'Home Insurance Claim Settlement Calculator (Texas)',
    'description' => 'Estimate your property claim payout: replacement cost, depreciation, deductible, ACV vs. RCV policies, holdback and what a public adjuster fee means for your net.',
    'h1'          => 'Claim settlement calculator',
    'lead'        => 'Enter the numbers from your insurer\'s estimate to see what you\'re paid now, what\'s held back until repairs, and what you keep. You can also check whether hiring a public adjuster would pay for itself.',
    'updated'     => '2026-10-13',
    'script'      => '/assets/js/tools/settlement.js',
    'app'         => <<<'HTML'
<div class="tcols" data-calc>
  <div>
    <fieldset class="tgroup">
      <legend>1. Your policy</legend>
      <div class="seg" data-seg="policy">
        <button type="button" class="is-on" data-v="rcv">Replacement cost (RCV)</button>
        <button type="button" data-v="acv">Actual cash value (ACV)</button>
      </div>
      <p class="muted" style="margin-top:-.4rem">Not sure? Check your declarations page or roof endorsement. ACV roof schedules are common on older Texas roofs.</p>
      <div class="seg" data-seg="dedtype">
        <button type="button" class="is-on" data-v="flat">Flat deductible</button>
        <button type="button" data-v="pct">% of dwelling coverage</button>
      </div>
      <div class="tf-row">
        <label class="tf" data-show="flat">Deductible<span class="tf-money"><input type="number" min="0" step="100" value="2500" data-in="ded"></span></label>
        <label class="tf" data-show="pct" hidden>Deductible %<input type="number" min="0" max="10" step="0.5" value="2" data-in="dedpct"></label>
        <label class="tf" data-show="pct" hidden>Dwelling coverage (Coverage A)<span class="tf-money"><input type="number" min="0" step="1000" value="350000" data-in="covA"></span></label>
      </div>
    </fieldset>
    <fieldset class="tgroup">
      <legend>2. The estimate</legend>
      <label class="tf">Replacement cost value (RCV) of the damage<small>The "RCV" total on the insurer's estimate (or your contractor's)</small><span class="tf-money"><input type="number" min="0" step="500" value="24000" data-in="rcv"></span></label>
      <label class="tf">Depreciation<small>The insurer's depreciation total, or use the roof-age helper below</small><span class="tf-money"><input type="number" min="0" step="100" value="7000" data-in="dep"></span></label>
      <details class="faq" style="margin-bottom:1rem">
        <summary>Roof-age depreciation helper</summary>
        <div class="faq__a">
          <div class="tf-row">
            <label class="tf">Roof age (years)<input type="number" min="0" max="60" value="9" data-in="age"></label>
            <label class="tf">Expected life (years)<select data-in="life"><option value="20">20 (3-tab shingle)</option><option value="25" selected>25 (architectural shingle)</option><option value="40">40 (metal / standing seam)</option><option value="50">50 (tile)</option></select></label>
          </div>
          <button type="button" class="btn btn--ghost btn--sm" data-act="applydep">Use straight-line estimate</button>
          <p class="muted" style="margin:.6rem 0 0">Insurers apply their own depreciation tables, often to materials only. This is a rough straight-line estimate.</p>
        </div>
      </details>
      <label class="tf">Payments already received<span class="tf-money"><input type="number" min="0" step="100" value="0" data-in="paid"></span></label>
    </fieldset>
    <fieldset class="tgroup">
      <legend>3. Would a public adjuster pay for itself?</legend>
      <label class="tf">Public adjuster fee: <span class="range-val" data-out="feeLbl">10%</span><input type="range" min="0" max="10" step="0.5" value="10" data-in="fee"><small>Texas caps public adjuster fees at 10% of the settlement (Ins. Code §4102.104).</small></label>
      <label class="tf">A higher, documented RCV you believe is correct (optional)<small>For example, your contractor's full scope or a public adjuster's estimate</small><span class="tf-money"><input type="number" min="0" step="500" value="" placeholder="e.g. 31000" data-in="rcv2"></span></label>
    </fieldset>
  </div>
  <div class="tresult" aria-live="polite">
    <p class="tlabel">Paid to you now</p>
    <p class="tbig" data-out="now">$0</p>
    <div class="bar" aria-hidden="true"><span class="c-pay" data-bar="pay"></span><span class="c-hold" data-bar="hold"></span><span class="c-ded" data-bar="ded"></span><span class="c-fee" data-bar="lost"></span></div>
    <div class="legend"><span><i class="c-pay"></i>Paid now</span><span><i class="c-hold"></i>Held back until repairs</span><span><i class="c-ded"></i>Deductible</span><span><i class="c-fee"></i>Non-recoverable depreciation</span></div>
    <ul class="tlines">
      <li><span>Replacement cost (RCV)</span><strong data-out="rcvOut"></strong></li>
      <li class="is-neg"><span>Depreciation withheld</span><strong data-out="depOut"></strong></li>
      <li class="is-neg"><span>Deductible</span><strong data-out="dedOut"></strong></li>
      <li><span>Actual cash value payment</span><strong data-out="acvOut"></strong></li>
      <li><span>Recoverable after repairs</span><strong data-out="holdOut"></strong></li>
      <li class="is-neg"><span>Less payments received</span><strong data-out="paidOut"></strong></li>
      <li class="is-total"><span>Total claim value to you</span><strong data-out="total"></strong></li>
    </ul>
    <div data-pa hidden>
      <p class="tlabel" style="margin-top:1.4rem">With a public adjuster</p>
      <ul class="tlines">
        <li><span>Total at the higher RCV</span><strong data-out="t2"></strong></li>
        <li class="is-neg"><span>Fee (<span data-out="feeLbl2"></span>)</span><strong data-out="feeAmt"></strong></li>
        <li class="is-total"><span>Net to you</span><strong data-out="net2"></strong></li>
        <li><span>Difference vs. settling yourself</span><strong data-out="diff"></strong></li>
      </ul>
    </div>
    <p class="tnote" data-out="breakeven"></p>
    <div class="tbtns"><button type="button" class="btn btn--light btn--sm" data-act="print">Print results</button><a class="btn btn--primary btn--sm" href="/contact-us/">Have us check the estimate</a></div>
  </div>
</div>
HTML,
    'body'        => <<<'HTML'
<h2>How a property claim payment is calculated</h2>
<p>Most Texas homeowners policies pay a claim in two stages. First, the insurer pays the <strong>actual cash value (ACV)</strong>: the replacement cost minus depreciation and your deductible. Then, if your policy is a <strong>replacement cost (RCV)</strong> policy, it releases the withheld depreciation (the "holdback" or "recoverable depreciation") once the repairs are done and you send proof.</p>
<div class="table-wrap"><table>
<thead><tr><th>Term</th><th>What it means</th></tr></thead>
<tbody>
<tr><td>RCV</td><td>What it costs today to repair or replace the damage with like kind and quality.</td></tr>
<tr><td>Depreciation</td><td>The reduction for age and wear. On RCV policies it's usually recoverable; on ACV policies or ACV roof endorsements it isn't.</td></tr>
<tr><td>ACV</td><td>RCV minus depreciation. This is the first check, less your deductible.</td></tr>
<tr><td>Deductible</td><td>Your share. Wind and hail deductibles in Texas are often a percentage of your dwelling coverage, not a flat amount.</td></tr>
</tbody></table></div>

<h2>Where the real money is: the scope, not the math</h2>
<p>The calculator is only as good as the RCV you put in. In our experience, the biggest gap between a low payment and a fair one isn't depreciation. It's the scope: a slope left off, missing drip edge or starter course, no line for code-required items, interior drywall patched when it should be replaced, or general contractor overhead and profit omitted. Our guide to <a href="/post/underpaid-hail-damage-insurance-claim/">underpaid hail claims</a> lists the items we see missed most often.</p>

<h2>Does a public adjuster pay for itself?</h2>
<p>The math is simple. With a 10% fee, the settlement has to rise by at least about 11.1% over what you would get on your own before you come out ahead. On a claim the insurer has scoped correctly, it won't, and we'll tell you so in the free review. On claims with missing slopes, interior damage or contents, the difference is often much larger than the fee. See <a href="/post/the-truth-about-public-adjuster-fees/">how public adjuster fees work in Texas</a>.</p>
<div class="callout callout--law"><p><strong>Texas law:</strong> a public adjuster's total commission may not exceed 10% of the settlement, and your name must be on every claim check (Tex. Ins. Code §4102.104).</p></div>
HTML,
    'faqs' => [
        ['q' => 'What is recoverable depreciation?', 'a' => 'On a replacement cost policy, the insurer withholds depreciation from the first payment and releases it once you complete the repairs and send proof, such as a final invoice. Check your policy for any deadline to complete repairs and claim it.'],
        ['q' => 'Why is my first check so much lower than the estimate?', 'a' => 'Because the first check is the actual cash value: replacement cost minus depreciation minus your deductible. The calculator shows each piece.'],
        ['q' => 'Does a percentage deductible apply to the whole claim?', 'a' => 'A wind and hail percentage deductible is calculated on your dwelling (Coverage A) limit, not on the size of the claim. A 2% deductible on a $350,000 home is $7,000.'],
        ['q' => 'Is the public adjuster fee charged on money already paid?', 'a' => 'That depends on the contract you sign, so ask before you sign. Get it in writing whether the percentage applies only to new money recovered or to the whole claim.'],
    ],
    'related' => ['/post/the-truth-about-public-adjuster-fees/', '/post/underpaid-hail-damage-insurance-claim/', '/post/hail-damage-supplement-claim/'],
];
