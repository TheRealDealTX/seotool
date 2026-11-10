<div class="narrow-lg rent">
  <a class="backlink" href="/tools"><?= icon('back') ?> Tools</a>
  <h1>Rent split calculator</h1>
  <p class="muted">Bigger room, private bath or a parking spot? Split it fairly. Everything updates as you type.</p>
  <div class="layout-2">
    <section class="card form">
      <div class="row-2">
        <label>Monthly rent<div class="input-prefix"><span>$</span><input type="number" id="rs-rent" value="2000" min="0" step="25"></div></label>
        <label>Utilities &amp; internet<div class="input-prefix"><span>$</span><input type="number" id="rs-util" value="180" min="0" step="5"></div></label>
      </div>
      <label>How to split utilities<select id="rs-utilmode"><option value="even">Evenly</option><option value="rent">Same ratio as rent</option></select></label>
      <label>Shared-space weighting <output id="rs-common-out" class="range-out">50% split evenly</output>
        <input type="range" id="rs-common" min="0" max="100" value="50"></label>
      <p class="small muted" style="margin-top:-8px">The share of rent that covers kitchen, living room etc. is split evenly; the rest is split by bedroom size.</p>
      <div id="rs-people"></div>
      <button type="button" class="btn btn-outline btn-sm" id="rs-add"><?= icon('plus') ?> Add roommate</button>
    </section>
    <section>
      <div class="card rs-result">
        <h3 class="card-title">Fair split</h3>
        <div id="rs-bars"></div>
        <div class="rs-total muted small" id="rs-total"></div>
        <div class="btn-row" style="margin-top:14px">
          <button type="button" class="btn btn-outline btn-sm" id="rs-copy"><?= icon('link') ?> Copy summary</button>
          <?php if ($friends): ?>
          <select id="rs-friend" class="select-sm"><option value="">Send to a friend…</option><?php foreach ($friends as $f): ?><option value="<?= e($f['username']) ?>"><?= e($f['name']) ?></option><?php endforeach; ?></select>
          <?php endif; ?>
        </div>
      </div>
      <div class="card small muted">💡 Premiums: a private bathroom adds about 8% to a room's weight, a parking spot is billed at its own price, and you can nudge any room with the adjustment.</div>
    </section>
  </div>
</div>
<template id="rs-person-tpl">
  <div class="rs-person">
    <div class="rs-person-head"><input type="text" class="rs-name" maxlength="30"><button type="button" class="iconbtn rs-del" aria-label="Remove"><?= icon('x') ?></button></div>
    <div class="row-3">
      <label>Bedroom (sq ft)<input type="number" class="rs-size" min="40" step="5"></label>
      <label>Parking ($)<input type="number" class="rs-park" min="0" step="5" value="0"></label>
      <label>Adjust ($)<input type="number" class="rs-adj" step="5" value="0"></label>
    </div>
    <label class="check"><input type="checkbox" class="rs-bath"> Private bathroom</label>
  </div>
</template>
