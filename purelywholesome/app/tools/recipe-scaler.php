<?php $slug = 'recipe-scaler'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body">
    <form class="tool__form" onsubmit="return false">
      <div class="field">
        <label for="rs-list">Ingredients, one per line</label>
        <textarea id="rs-list" name="list" rows="8">2 cups pumpkin puree
3/4 cup brown sugar
1 1/2 tsp pumpkin pie spice
1/2 tsp fine salt
3 large eggs
1 cup evaporated milk
1 unbaked 9-inch pie crust</textarea>
      </div>
      <div class="field field--split">
        <label>Servings</label>
        <div class="field__row">
          <input name="from" type="number" min="1" value="8" aria-label="Original servings" inputmode="numeric">
          <span class="field__unit">→</span>
          <input name="to" type="number" min="1" value="16" aria-label="New servings" inputmode="numeric">
        </div>
      </div>
      <div class="quick"><button type="button" data-factor="0.5">½×</button><button type="button" data-factor="1.5">1½×</button><button type="button" data-factor="2">2×</button><button type="button" data-factor="3">3×</button></div>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="scaled-head"><strong data-out="factor">2×</strong><button type="button" class="btn btn--ghost btn--sm" data-copy><?= icon('link') ?> Copy list</button></div>
      <ul class="scaled" data-out="list"></ul>
    </div>
  </div>
</section>
