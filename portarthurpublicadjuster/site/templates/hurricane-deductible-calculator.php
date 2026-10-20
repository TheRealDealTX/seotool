<?php
/** Hurricane / wind & hail percentage deductible calculator (runs in the browser). */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
?>
<section class="section section-alt" aria-labelledby="ded-h">
  <div class="container">
    <div class="tool-layout" data-deductible>
      <form class="tool-panel" data-ded-form novalidate onsubmit="return false">
        <h2 id="ded-h">Your policy</h2>
        <p class="small muted">Use the numbers on your declarations page. Everything is calculated on your device&mdash;nothing is sent to us.</p>
        <div class="form-grid">
          <div class="field field-full"><label for="d-cova">Dwelling limit (Coverage A)</label><div class="input-money"><input id="d-cova" name="cova" type="text" inputmode="decimal" placeholder="250,000" autocomplete="off"></div><span class="field-hint">Percentage deductibles are usually figured on Coverage A, not on the amount of damage.</span></div>
          <div class="field field-full"><label for="d-pct">Wind / hail or named-storm deductible</label>
            <div class="seg seg-wide" role="radiogroup" aria-label="Deductible percentage">
              <?php foreach (['1', '2', '3', '5', '10'] as $p): ?><label><input type="radio" name="pct" value="<?= $p ?>"<?= $p === '2' ? ' checked' : '' ?>><span><?= $p ?>%</span></label><?php endforeach; ?>
              <label><input type="radio" name="pct" value="custom"><span>Other</span></label>
            </div>
            <div class="input-group" data-custom hidden style="margin-top:10px"><input id="d-custom" name="custom" type="text" inputmode="decimal" placeholder="e.g. 1.5" aria-label="Custom percentage"><span class="input-suffix">%</span></div>
          </div>
          <div class="field"><label for="d-flat">All-other-perils deductible <span class="opt">(optional)</span></label><div class="input-money"><input id="d-flat" name="flat" type="text" inputmode="decimal" placeholder="1,000" autocomplete="off"></div><span class="field-hint">Shown for comparison; applies to non-wind losses such as fire or plumbing leaks.</span></div>
          <div class="field"><label for="d-loss">Estimated wind damage <span class="opt">(optional)</span></label><div class="input-money"><input id="d-loss" name="loss" type="text" inputmode="decimal" placeholder="18,000" autocomplete="off"></div><span class="field-hint">Repair estimate for the covered wind or hail damage.</span></div>
        </div>
        <div class="tool-actions no-print">
          <button class="btn btn-ghost btn-sm" type="button" data-example>Load example</button>
          <button class="btn btn-ghost btn-sm" type="reset" data-reset><?= icon('refresh', 'icon icon-sm') ?> Reset</button>
        </div>
      </form>
      <div class="tool-panel results" aria-live="polite">
        <h2>What you would pay first</h2>
        <p class="print-only">Port Arthur Public Adjuster &middot; Hurricane Deductible Estimate &middot; <span data-print-date></span></p>
        <div class="ded-hero">
          <span class="ded-hero-label">Your wind/hail deductible</span>
          <strong class="ded-hero-num" data-out="ded">$0</strong>
          <span class="small muted" data-out="ded-note">Enter your dwelling limit</span>
        </div>
        <dl class="result-rows">
          <div class="result-row"><dt>All-other-perils deductible<small>For comparison</small></dt><dd data-out="flat">&mdash;</dd></div>
          <div class="result-row"><dt>Wind deductible vs. flat deductible<small>How much more a wind loss costs you up front</small></dt><dd data-out="diff">&mdash;</dd></div>
          <div class="result-row"><dt>Estimated claim payment for this damage<small>Damage minus deductible, before depreciation and limits</small></dt><dd data-out="pay">&mdash;</dd></div>
          <div class="result-row is-oop"><dt>Damage you would absorb<small>The deductible portion of this loss</small></dt><dd data-out="absorb">&mdash;</dd></div>
        </dl>
        <div class="result-bar" aria-hidden="true"><span data-bar="pay" style="background:var(--gold)"></span><span data-bar="absorb" style="background:#e07a5f"></span></div>
        <ul class="legend"><li><i style="background:var(--gold)"></i>Insurance pays (est.)</li><li><i style="background:#e07a5f"></i>You pay</li></ul>
        <p class="warn-text" data-warn hidden></p>
        <h3 style="margin-top:22px">Compare common percentages</h3>
        <div class="table-wrap"><table class="ded-table"><thead><tr><th scope="col">Deductible</th><th scope="col">You pay first</th><th scope="col">Claim payment*</th></tr></thead><tbody data-compare><tr><td colspan="3" class="muted">Enter a dwelling limit to compare.</td></tr></tbody></table></div>
        <p class="small muted">*For the damage amount entered, before depreciation, sublimits, and other policy terms.</p>
        <div class="tool-actions no-print">
          <button class="btn btn-gold btn-sm" type="button" data-print><?= icon('printer', 'icon icon-sm') ?> Print summary</button>
        </div>
      </div>
    </div>
    <div class="tool-panel explain" style="margin-top:28px">
      <h2>How it works</h2>
      <ol>
        <li><strong>Percentage deductible</strong> = Coverage A dwelling limit &times; the percentage on your declarations page (for example, 2% of $250,000 = $5,000).</li>
        <li><strong>Estimated claim payment</strong> = covered wind damage &minus; that deductible (never below $0). Depreciation, policy limits, and sublimits can lower the actual payment.</li>
        <li>If your home carries <strong>two wind-related policies</strong>&mdash;for example a homeowners policy that excludes wind and a separate TWIA windstorm policy&mdash;the wind deductible that applies is the one on the policy that covers wind.</li>
      </ol>
      <p class="disclaimer-box mb-0"><strong>Educational estimate only.</strong> Deductible wording varies. Some policies apply a named-storm or hurricane deductible only when the National Weather Service names a storm; others apply a wind/hail deductible to any wind or hail loss. Flood insurance has its own separate deductibles. Check your declarations page and endorsements, or request a <a href="/free-claim-review/">Free Claim Review</a>.</p>
    </div>
    <?php component('cta-band', ['heading' => 'Not sure which deductible applies to your claim?']); ?>
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
