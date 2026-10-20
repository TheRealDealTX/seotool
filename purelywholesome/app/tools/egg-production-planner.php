<?php $slug = 'egg-production-planner'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body">
    <form class="tool__form" onsubmit="return false">
      <div class="field">
        <label for="ep-eggs">Eggs your household uses per week <output name="eggsOut">18</output></label>
        <input id="ep-eggs" name="eggs" type="range" min="3" max="72" step="1" value="18">
      </div>
      <div class="field">
        <label for="ep-breed">Breed</label>
        <select id="ep-breed" name="breed">
          <option value="290">White Leghorn (~290 eggs/yr)</option>
          <option value="290">ISA Brown / Red Sex-Link (~290)</option>
          <option value="250" selected>Australorp (~250)</option>
          <option value="250">Rhode Island Red (~250)</option>
          <option value="220">Easter Egger (~220)</option>
          <option value="220">Barred Plymouth Rock (~220)</option>
          <option value="190">Buff Orpington (~190)</option>
          <option value="190">Wyandotte (~190)</option>
          <option value="120">Silkie (~120)</option>
        </select>
      </div>
      <label class="toggle"><input type="checkbox" name="winter" checked><span></span> Plan for winter (shorter days, fewer eggs)</label>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="hens" data-out="hens" aria-hidden="true"></div>
      <div class="result-grid result-grid--4">
        <div class="result result--big"><span class="result__label">Hens needed</span><strong data-out="count">—</strong></div>
        <div class="result"><span class="result__label">Coop floor</span><strong data-out="coop">—</strong></div>
        <div class="result"><span class="result__label">Run space</span><strong data-out="run">—</strong></div>
        <div class="result"><span class="result__label">Nest boxes</span><strong data-out="nests">—</strong></div>
        <div class="result"><span class="result__label">Roost bar</span><strong data-out="roost">—</strong></div>
        <div class="result"><span class="result__label">Feed / week</span><strong data-out="feed">—</strong></div>
        <div class="result"><span class="result__label">Water / day</span><strong data-out="water">—</strong></div>
        <div class="result"><span class="result__label">Eggs / week (peak)</span><strong data-out="peak">—</strong></div>
      </div>
      <p class="tool__note">Check local rules before you buy chicks: many towns cap backyard flocks or ban roosters.</p>
    </div>
  </div>
</section>
