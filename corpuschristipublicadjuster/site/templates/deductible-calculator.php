<?php
defined('CCPA_ROOT') || exit;
/** Hurricane / named-storm / wind-hail deductible calculator. */
$toc = [];
$body = prepared_body($page, $toc);
component('page-hero', ['page' => $page]);
?>
<section class="section section-alt" aria-labelledby="ded-h">
  <div class="container">
    <div class="tool-layout" data-ded-calc>
      <form class="tool-panel" novalidate onsubmit="return false">
        <h2 id="ded-h">Your policy numbers</h2>
        <p class="small muted">Find these on your declarations page (homeowners or TWIA). Everything runs in your browser&mdash;nothing is sent to us.</p>
        <div class="form-grid">
          <div class="field field-full"><label for="d-limit">Dwelling (Coverage A) limit</label><div class="input-money"><input id="d-limit" name="limit" type="text" inputmode="decimal" placeholder="300,000" autocomplete="off"></div><span class="field-hint">Percentage deductibles are calculated on this limit, not on the damage.</span></div>
          <div class="field field-full"><label for="d-type">Deductible on your policy</label>
            <select id="d-type" name="type">
              <option value="0.01">1% of Coverage A</option>
              <option value="0.02" selected>2% of Coverage A</option>
              <option value="0.03">3% of Coverage A</option>
              <option value="0.05">5% of Coverage A</option>
              <option value="0.10">10% of Coverage A</option>
              <option value="flat">Flat dollar amount</option>
            </select></div>
          <div class="field field-full" data-flat hidden><label for="d-flat">Flat deductible</label><div class="input-money"><input id="d-flat" name="flat" type="text" inputmode="decimal" placeholder="2,500" autocomplete="off"></div></div>
          <div class="field field-full"><label for="d-damage">Estimated covered storm damage</label><div class="input-money"><input id="d-damage" name="damage" type="text" inputmode="decimal" placeholder="18,000" autocomplete="off"></div><span class="field-hint">Replacement cost of covered wind or hail damage to the dwelling. Flood damage is a separate policy.</span></div>
        </div>
        <div class="tool-actions no-print">
          <button class="btn btn-ghost btn-sm" type="button" data-example>Load example</button>
          <button class="btn btn-ghost btn-sm" type="reset"><?= icon('refresh', 'icon icon-sm') ?> Reset</button>
        </div>
      </form>
      <div class="tool-panel results" aria-live="polite">
        <h2>What the deductible means</h2>
        <p class="mb-0" style="color:#b9c6d3">Your deductible</p>
        <p class="calc-big" data-o="ded">$0</p>
        <div class="gauge" aria-hidden="true"><span data-o-gauge style="width:0%"></span></div>
        <p class="small" style="color:#b9c6d3" data-o="share">Enter your numbers to see how much of the damage you would pay.</p>
        <dl class="result-rows">
          <div class="result-row"><dt>Covered damage entered</dt><dd data-o="damage">$0</dd></div>
          <div class="result-row"><dt>You pay (deductible portion)<small>Never more than the damage</small></dt><dd data-o="you">$0</dd></div>
          <div class="result-row is-total"><dt>Policy could pay before depreciation<small>Damage minus deductible, up to the limit</small></dt><dd data-o="ins">$0</dd></div>
        </dl>
        <h3 style="color:#fff;margin-top:22px;font-size:1.05rem">Same home, different deductibles</h3>
        <div class="table-wrap" style="border-color:rgba(255,255,255,.12)"><table data-nowrap style="background:transparent;min-width:0">
          <thead><tr><th>Deductible</th><th>You pay first</th><th>Insurer pays*</th></tr></thead>
          <tbody data-o-table style="color:#d8e1ea"></tbody>
        </table></div>
        <p class="small" style="color:#9fb2c4">*Before depreciation, sublimits, and other policy terms.</p>
        <div class="tool-actions no-print"><button class="btn btn-gold btn-sm" type="button" onclick="window.print()"><?= icon('printer', 'icon icon-sm') ?> Print</button></div>
      </div>
    </div>
    <div class="tool-panel explain" style="margin-top:28px">
      <h2>How it works</h2>
      <ol>
        <li><strong>Percentage deductible</strong> = Coverage A limit &times; the percentage. A 2% deductible on a $300,000 home is $6,000, no matter how small the damage.</li>
        <li><strong>You pay</strong> the lesser of the deductible or the damage.</li>
        <li><strong>The policy could pay</strong> the damage minus the deductible, capped at the limit. Depreciation, roof schedules, and sublimits can reduce that further.</li>
      </ol>
      <p class="disclaimer-box mb-0"><strong>Educational estimate only.</strong> Policies define hurricane, named-storm, and wind/hail deductibles differently, and some apply per occurrence or per season. TWIA and private carriers use their own forms. Read your declarations page and endorsements, or request a <a href="/free-claim-review/">Free Claim Review</a>.</p>
    </div>
    <?php component('cta-band', ['heading' => 'Storm damage above your deductible?']); ?>
  </div>
</section>
<section class="section section-article">
  <div class="container with-sidebar">
    <article class="prose">
      <?= $body ?>
      <?php component('faq', ['faqs' => $page['faqs'] ?? []]); ?>
    </article>
    <aside class="sidebar"><?php include CCPA_ROOT . '/templates/sidebar.php'; ?></aside>
  </div>
</section>
