<?php $slug = 'lamb-sides-builder'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body">
    <form class="tool__form" onsubmit="return false">
      <fieldset class="field pills">
        <legend>Season</legend>
        <label><input type="radio" name="season" value="spring" checked><span>Spring</span></label>
        <label><input type="radio" name="season" value="summer"><span>Summer</span></label>
        <label><input type="radio" name="season" value="fall"><span>Fall</span></label>
        <label><input type="radio" name="season" value="winter"><span>Winter</span></label>
      </fieldset>
      <fieldset class="field pills">
        <legend>Kind of dinner</legend>
        <label><input type="radio" name="style" value="weeknight" checked><span>Easy weeknight</span></label>
        <label><input type="radio" name="style" value="party"><span>Dinner party</span></label>
        <label><input type="radio" name="style" value="grill"><span>Off the grill</span></label>
        <label><input type="radio" name="style" value="holiday"><span>Holiday table</span></label>
      </fieldset>
      <button type="button" class="btn btn--ghost" data-shuffle><?= icon('sparkle') ?> Shuffle the menu</button>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="plate" data-out="plate"></div>
      <p class="tool__note">Want the details? See <a href="/sides-for-lamb-chops/">sides for lamb chops</a> and <a href="/best-sauce-for-lamb-chops/">the best sauce for lamb chops</a>.</p>
    </div>
  </div>
</section>
