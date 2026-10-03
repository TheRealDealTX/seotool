<?php
/** Insurance Claim Settlement Calculator. */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
?>
<section class="section section-alt" aria-labelledby="calc-h">
  <div class="container">
    <div class="tool-layout" data-calculator>
      <form class="tool-panel" data-calc-form novalidate onsubmit="return false">
        <h2 id="calc-h">Your claim numbers</h2>
        <p class="small muted">Enter what you know. Results update instantly and stay on your device&mdash;nothing is sent to us.</p>
        <div class="form-grid">
          <div class="field field-full"><label for="c-rcv">Estimated replacement cost (RCV) of the damage</label><div class="input-money"><input id="c-rcv" name="rcv" type="text" inputmode="decimal" placeholder="24,000" autocomplete="off"></div><span class="field-hint">Total cost to repair or replace with like kind and quality, from the insurer's or your contractor's estimate.</span></div>
          <div class="field field-full"><label for="c-dep">Depreciation</label>
            <div class="input-group"><div class="input-money" data-dep-money><input id="c-dep" name="dep" type="text" inputmode="decimal" placeholder="7,200" autocomplete="off"></div>
              <div class="seg" role="radiogroup" aria-label="Depreciation entered as"><label><input type="radio" name="depmode" value="amt" checked><span>$</span></label><label><input type="radio" name="depmode" value="pct"><span>%</span></label></div></div>
            <span class="field-hint">Dollar amount from the estimate, or a percentage of the covered replacement cost.</span></div>
          <div class="field"><label for="c-ded">Deductible</label><div class="input-money"><input id="c-ded" name="ded" type="text" inputmode="decimal" placeholder="5,000" autocomplete="off"></div><span class="field-hint">Check the declarations page; wind/hail deductibles are often a % of the dwelling limit.</span></div>
          <div class="field"><label for="c-prev">Payments already received</label><div class="input-money"><input id="c-prev" name="prev" type="text" inputmode="decimal" placeholder="0" autocomplete="off"></div><span class="field-hint">Total of checks already issued on this claim.</span></div>
          <div class="field"><label for="c-nc">Non-covered costs</label><div class="input-money"><input id="c-nc" name="noncov" type="text" inputmode="decimal" placeholder="0" autocomplete="off"></div><span class="field-hint">Parts of the project the policy does not cover (upgrades, excluded items, pre-existing issues).</span></div>
          <div class="field"><label for="c-lim">Applicable policy limit <span class="opt">(optional)</span></label><div class="input-money"><input id="c-lim" name="limit" type="text" inputmode="decimal" placeholder="Leave blank if unknown" autocomplete="off"></div><span class="field-hint">e.g. Coverage A (dwelling) limit.</span></div>
          <div class="field field-full field-check"><input id="c-rc" name="rcpolicy" type="checkbox" checked><label for="c-rc"><strong>Replacement cost policy</strong> &mdash; depreciation is recoverable after repairs are completed. Uncheck for an actual cash value (ACV) policy or ACV roof coverage.</label></div>
        </div>
        <div class="tool-actions no-print">
          <button class="btn btn-ghost btn-sm" type="button" data-example>Load example</button>
          <button class="btn btn-ghost btn-sm" type="reset" data-reset><?= icon('refresh', 'icon icon-sm') ?> Reset</button>
        </div>
      </form>
      <div class="tool-panel results" aria-live="polite">
        <h2>Estimated results</h2>
        <p class="print-only">McAllen Public Adjuster &middot; Claim Settlement Estimate &middot; <span data-print-date></span></p>
        <dl class="result-rows">
          <div class="result-row"><dt>Replacement cost value (RCV)<small>Covered portion after non-covered costs</small></dt><dd data-out="rcv">$0</dd></div>
          <div class="result-row"><dt>Less depreciation</dt><dd data-out="dep">$0</dd></div>
          <div class="result-row"><dt>Actual cash value (ACV)<small>RCV minus depreciation</small></dt><dd data-out="acv">$0</dd></div>
          <div class="result-row"><dt>Estimated initial (ACV) payment<small>ACV minus deductible, within limits, less prior payments</small></dt><dd data-out="initial">$0</dd></div>
          <div class="result-row"><dt>Potential recoverable depreciation<small>Typically released after repairs are completed</small></dt><dd data-out="recoverable">$0</dd></div>
          <div class="result-row"><dt>Estimated remaining payment<small>Total estimated proceeds minus payments received</small></dt><dd data-out="remaining">$0</dd></div>
          <div class="result-row is-total"><dt>Total estimated insurance proceeds</dt><dd data-out="total">$0</dd></div>
          <div class="result-row is-oop"><dt>Estimated out-of-pocket cost<small>Project cost not paid by insurance</small></dt><dd data-out="oop">$0</dd></div>
        </dl>
        <div class="result-bar" aria-hidden="true"><span data-bar="ins" style="background:var(--gold)"></span><span data-bar="dep" style="background:#7fa7c9"></span><span data-bar="oop" style="background:#e07a5f"></span></div>
        <ul class="legend"><li><i style="background:var(--gold)"></i>Paid now (est.)</li><li><i style="background:#7fa7c9"></i>Recoverable later</li><li><i style="background:#e07a5f"></i>Your cost</li></ul>
        <p class="warn-text" data-warn hidden></p>
        <div class="tool-actions no-print">
          <button class="btn btn-gold btn-sm" type="button" data-print><?= icon('printer', 'icon icon-sm') ?> Print summary</button>
          <button class="btn btn-ghost btn-sm" type="button" data-download><?= icon('download', 'icon icon-sm') ?> Download report</button>
        </div>
      </div>
    </div>
    <div class="tool-panel explain" style="margin-top:28px">
      <h2>How these numbers are calculated</h2>
      <ol>
        <li><strong>Covered RCV</strong> = replacement cost &minus; non-covered costs.</li>
        <li><strong>Depreciation</strong> = the dollar amount you enter, or the percentage &times; covered RCV (never more than covered RCV).</li>
        <li><strong>ACV</strong> = covered RCV &minus; depreciation.</li>
        <li><strong>Maximum claim payment</strong> = covered RCV &minus; deductible, capped at the policy limit (if entered). On an ACV policy, ACV is used instead of RCV.</li>
        <li><strong>Initial payment</strong> = ACV &minus; deductible, capped at the policy limit, minus payments already received (not below $0).</li>
        <li><strong>Recoverable depreciation</strong> = maximum claim payment &minus; (ACV &minus; deductible, capped at the limit). Zero on an ACV policy.</li>
        <li><strong>Remaining payment</strong> = maximum claim payment &minus; payments already received.</li>
        <li><strong>Out-of-pocket</strong> = full replacement cost &minus; total estimated proceeds (deductible + non-covered costs + any amount over the limit + non-recoverable depreciation).</li>
      </ol>
      <p class="disclaimer-box mb-0"><strong>Educational estimate only.</strong> Results are not an offer, a coverage decision, or a guarantee. Actual settlements depend on your policy language, endorsements, limits, deductibles, sublimits, depreciation methods, repair deadlines, and the facts of your claim. Some policies settle roofs on an actual cash value or payment-schedule basis, and recoverable depreciation usually requires completing repairs within a time limit. Ask your insurer for the estimate and policy forms, or request a <a href="/free-claim-review/">Free Claim Review</a>.</p>
    </div>
    <?php component('cta-band', ['heading' => 'Do these numbers look lower than your repair costs?']); ?>
  </div>
</section>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
    </article>
    <aside class="sidebar"><?php include MPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
