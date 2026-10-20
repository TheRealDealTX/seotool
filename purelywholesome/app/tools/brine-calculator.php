<?php $slug = 'brine-calculator'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body">
    <form class="tool__form" onsubmit="return false">
      <div class="field field--split">
        <label for="bc-water">Water</label>
        <div class="field__row">
          <input id="bc-water" name="water" type="number" min="0.25" step="0.25" value="1" inputmode="decimal">
          <select name="unit" aria-label="Water unit">
            <option value="3785.41">gallons</option><option value="946.353">quarts</option><option value="1000">liters</option><option value="236.588">cups</option>
          </select>
        </div>
      </div>
      <div class="field">
        <label for="bc-salt">Salt you have</label>
        <select id="bc-salt" name="salt">
          <option value="diamond">Diamond Crystal kosher</option>
          <option value="morton">Morton kosher</option>
          <option value="table">Table salt (fine)</option>
          <option value="sea">Fine sea salt</option>
          <option value="coarse">Coarse sea salt</option>
        </select>
      </div>
      <div class="field">
        <label for="bc-strength">Brine strength <output name="strengthOut">5%</output></label>
        <input id="bc-strength" name="strength" type="range" min="2" max="8" step="0.5" value="5">
        <div class="range-labels"><span>Gentle</span><span>Classic</span><span>Quick</span></div>
      </div>
      <div class="field">
        <label for="bc-cut">What are you brining?</label>
        <select id="bc-cut" name="cut">
          <option value="breast">Boneless chicken breasts or thighs</option>
          <option value="pieces">Bone-in chicken pieces</option>
          <option value="whole" selected>Whole chicken (3-5 lb)</option>
          <option value="spatch">Spatchcocked chicken</option>
          <option value="turkeybreast">Turkey breast</option>
          <option value="turkey">Whole turkey (12-16 lb)</option>
          <option value="chops">Pork chops</option>
          <option value="shoulder">Pork shoulder</option>
          <option value="brisket">Brisket (flavor brine)</option>
        </select>
      </div>
      <label class="toggle"><input type="checkbox" name="sugar" checked><span></span> Add sugar for browning</label>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="result-grid">
        <div class="result result--big"><span class="result__label">Salt</span><strong data-out="salt">—</strong><small data-out="saltg"></small></div>
        <div class="result"><span class="result__label">Sugar</span><strong data-out="sugar">—</strong><small data-out="sugarg"></small></div>
        <div class="result"><span class="result__label">Brine time</span><strong data-out="time">—</strong><small data-out="timenote"></small></div>
      </div>
      <div class="gauge" aria-hidden="true"><span class="gauge__fill" data-out="gauge"></span><span class="gauge__marks"><i>2%</i><i>5%</i><i>8%</i></span></div>
      <p class="tool__note" data-out="note"></p>
      <ol class="steps">
        <li>Dissolve the salt (and sugar) in a quarter of the water, warmed, then add the rest cold.</li>
        <li>Brine fully submerged in the fridge (below 40°F) in a food-safe container.</li>
        <li>Rinse, pat very dry and rest uncovered in the fridge if you can, then cook to 165°F for poultry.</li>
      </ol>
    </div>
  </div>
</section>
