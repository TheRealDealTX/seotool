<?php $slug = 'canning-altitude-adjuster'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body">
    <form class="tool__form" onsubmit="return false">
      <fieldset class="field pills">
        <legend>Method</legend>
        <label><input type="radio" name="method" value="bath" checked><span>Water bath</span></label>
        <label><input type="radio" name="method" value="weighted"><span>Pressure (weighted gauge)</span></label>
        <label><input type="radio" name="method" value="dial"><span>Pressure (dial gauge)</span></label>
      </fieldset>
      <div class="field field--split">
        <label for="ca-alt">Your elevation</label>
        <div class="field__row">
          <input id="ca-alt" name="alt" type="number" min="0" max="12000" step="50" value="1500" inputmode="numeric">
          <select name="altunit" aria-label="Elevation unit"><option value="ft">feet</option><option value="m">meters</option></select>
        </div>
      </div>
      <div class="field">
        <label for="ca-time">Recipe processing time (sea level)</label>
        <div class="field__row"><input id="ca-time" name="time" type="number" min="1" max="200" value="10" inputmode="numeric"><span class="field__unit">minutes</span></div>
      </div>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="mountain" aria-hidden="true"><svg viewBox="0 0 300 90" preserveAspectRatio="none"><path d="M0 90 70 40l30 18 60-52 50 38 30-16 60 62Z" fill="currentColor" opacity=".25"/><path d="M0 90 90 55l40 15 70-40 100 60Z" fill="currentColor" opacity=".45"/></svg><span class="mountain__jar" data-out="jar"><?= icon('jar') ?></span></div>
      <div class="result-grid">
        <div class="result result--big"><span class="result__label" data-out="biglabel">Process for</span><strong data-out="big">—</strong><small data-out="bignote"></small></div>
        <div class="result"><span class="result__label">Altitude band</span><strong data-out="band">—</strong></div>
      </div>
      <p class="tool__note">Always start from a tested recipe (USDA, NCHFP or a current Ball guide). If your recipe gives its own altitude chart, follow it instead.</p>
    </div>
  </div>
</section>
