<?php
// Interactive widgets shared by several pages. The markup works on its own;
// assets/js/site.js wires up the behavior through the data-widget attributes.

function widget_bah() {
    ob_start(); ?>
<section class="widget card" data-widget="bah" aria-labelledby="bah-title">
  <div class="widget-head">
    <span class="widget-icon"><?= icon('calc') ?></span>
    <div>
      <h3 id="bah-title">BAH Budget Calculator</h3>
      <p class="muted">See how a rental fits inside your housing allowance.</p>
    </div>
  </div>
  <div class="calc-grid">
    <label>Monthly BAH <span class="field-money"><input type="number" inputmode="decimal" min="0" step="10" value="2100" data-bah-in="bah"></span></label>
    <label>Rent <span class="field-money"><input type="number" inputmode="decimal" min="0" step="10" value="1650" data-bah-in="rent"></span></label>
    <label>Utilities <span class="field-money"><input type="number" inputmode="decimal" min="0" step="10" value="220" data-bah-in="util"></span></label>
    <label>Renters insurance &amp; extras <span class="field-money"><input type="number" inputmode="decimal" min="0" step="5" value="25" data-bah-in="extra"></span></label>
  </div>
  <div class="meter" role="img" data-bah-meter aria-label="Share of BAH used">
    <span class="meter-fill" data-bah-fill></span>
  </div>
  <div class="calc-result">
    <div><span class="muted">Total housing cost</span><strong data-bah-out="total">$1,895</strong></div>
    <div><span class="muted">Left over each month</span><strong data-bah-out="left">$205</strong></div>
    <div><span class="muted">Left over each year</span><strong data-bah-out="year">$2,460</strong></div>
  </div>
  <p class="calc-msg" data-bah-out="msg"></p>
  <p class="fineprint">Look up your official rate with the <a href="https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/BAH-Rate-Lookup/" target="_blank" rel="noopener">DoD BAH calculator</a>. In privatized on-base housing, rent is usually set to your BAH. <a href="/bah-explained-military-housing-allowance/">How BAH works &rarr;</a></p>
</section>
<?php
    return ob_get_clean();
}

function widget_pcs() {
    ob_start(); ?>
<section class="widget card" data-widget="pcs" aria-labelledby="pcs-title">
  <div class="widget-head">
    <span class="widget-icon"><?= icon('calendar') ?></span>
    <div>
      <h3 id="pcs-title">PCS Countdown &amp; Timeline</h3>
      <p class="muted">Enter your report date to get a personal move timeline.</p>
    </div>
  </div>
  <label class="pcs-date">Report no later than (RNLT) date <input type="date" data-pcs-date></label>
  <div class="pcs-count" data-pcs-count hidden>
    <strong data-pcs-days>0</strong><span data-pcs-label>days until you report</span>
  </div>
  <ol class="timeline" data-pcs-timeline>
    <li data-offset="-60"><b>Book your move</b> on Move.mil and contact the gaining housing office</li>
    <li data-offset="-45"><b>Declutter</b> and photograph your belongings</li>
    <li data-offset="-30"><b>Give notice</b> on your lease, using the SCRA if you need it</li>
    <li data-offset="-21"><b>Book lodging</b>, pet travel and utility transfers</li>
    <li data-offset="-14"><b>Pack the do-not-pack zone</b> and your first-night box</li>
    <li data-offset="-7"><b>Pack-out and load</b>, then clear quarters</li>
    <li data-offset="0"><b>Report</b> and sign in at your new duty station</li>
    <li data-offset="7"><b>Move-in inspection</b>: document everything before you unpack</li>
  </ol>
  <p class="fineprint">Want the full list? <a href="/pcs-moving-checklist/">PCS moving checklist &rarr;</a></p>
</section>
<?php
    return ob_get_clean();
}

function cta_band() {
    ob_start(); ?>
<section class="cta-band">
  <div class="wrap cta-inner">
    <div>
      <h2>Own a rental near a base?</h2>
      <p>List it where military families are already looking. We review every submission and help you put together a complete listing.</p>
    </div>
    <div class="cta-actions">
      <a class="btn btn-accent btn-lg" href="/submit-property/">Submit your property <?= icon('arrow') ?></a>
      <a class="btn btn-ghost-light btn-lg" href="<?= e(cfg('phone_href')) ?>"><?= icon('phone') ?> <?= e(cfg('phone')) ?></a>
    </div>
  </div>
</section>
<?php
    return ob_get_clean();
}

function sidebar_listings() {
    ob_start(); ?>
<aside class="sidebar">
  <div class="card side-card">
    <h3>Recently Listed</h3>
    <ul class="mini-list">
    <?php foreach (newest_listings(5) as $l): $img = listing_image($l); ?>
      <li><a href="/properties/<?= e($l['slug']) ?>/"><img src="<?= e($img['src']) ?>" alt="" width="64" height="64" loading="lazy"><span><strong><?= e($l['title']) ?></strong><small><?= e(city_state($l)) ?></small></span></a></li>
    <?php endforeach; ?>
    </ul>
    <a class="btn btn-outline btn-block" href="/properties/">Browse all listings</a>
  </div>
</aside>
<?php
    return ob_get_clean();
}
