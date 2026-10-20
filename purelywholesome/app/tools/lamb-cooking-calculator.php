<?php $slug = 'lamb-cooking-calculator'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body">
    <form class="tool__form" onsubmit="return false">
      <div class="field">
        <label for="lc-cut">Cut</label>
        <select id="lc-cut" name="cut">
          <option value="chops">Loin or rib chops, 1 inch (pan-seared)</option>
          <option value="thick">Thick chops, 1½ inch (sear + oven)</option>
          <option value="lollipops">Frenched lollipops (pan-seared)</option>
          <option value="rack">Rack of lamb (sear + 425°F oven)</option>
          <option value="legbone">Leg of lamb, bone-in (325°F)</option>
          <option value="legboneless">Leg of lamb, boneless (325°F)</option>
          <option value="shoulder">Shoulder, slow-roasted (300°F)</option>
        </select>
      </div>
      <div class="field" data-weight>
        <label for="lc-weight">Weight <output name="weightOut">5 lb</output></label>
        <input id="lc-weight" name="weight" type="range" min="2" max="10" step="0.5" value="5">
      </div>
      <fieldset class="field pills" data-doneness>
        <legend>Doneness</legend>
        <label><input type="radio" name="done" value="rare"><span>Rare</span></label>
        <label><input type="radio" name="done" value="mr" checked><span>Medium-rare</span></label>
        <label><input type="radio" name="done" value="m"><span>Medium</span></label>
        <label><input type="radio" name="done" value="mw"><span>Medium-well</span></label>
        <label><input type="radio" name="done" value="w"><span>Well</span></label>
      </fieldset>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="thermo-viz" aria-hidden="true"><div class="thermo-viz__tube"><span data-out="mercury"></span></div><div class="thermo-viz__bulb"></div></div>
      <div class="result-grid">
        <div class="result result--big"><span class="result__label">Pull at</span><strong data-out="pull">—</strong><small data-out="pullc"></small></div>
        <div class="result"><span class="result__label">After resting</span><strong data-out="final">—</strong><small data-out="rest"></small></div>
        <div class="result"><span class="result__label">Cook time</span><strong data-out="time">—</strong><small data-out="timenote"></small></div>
      </div>
      <p class="tool__note" data-out="note"></p>
    </div>
  </div>
</section>
