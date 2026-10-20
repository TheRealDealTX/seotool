<?php $slug = 'goat-gestation-calculator'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body">
    <form class="tool__form" onsubmit="return false">
      <div class="field">
        <label for="gg-date">Breeding date</label>
        <input id="gg-date" name="bred" type="date">
      </div>
      <fieldset class="field pills">
        <legend>Breed size</legend>
        <label><input type="radio" name="breed" value="150" checked><span>Standard (Nubian, Alpine, Boer…)</span></label>
        <label><input type="radio" name="breed" value="145"><span>Miniature (Nigerian Dwarf, Pygmy)</span></label>
      </fieldset>
      <div class="field">
        <label for="gg-name">Doe’s name <small>(optional)</small></label>
        <input id="gg-name" name="doe" type="text" maxlength="40" placeholder="e.g. Clover">
      </div>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="result-grid">
        <div class="result result--big"><span class="result__label">Expected kidding</span><strong data-out="due">—</strong><small data-out="window"></small></div>
        <div class="result"><span class="result__label">Countdown</span><strong data-out="count">—</strong><small data-out="countnote"></small></div>
      </div>
      <div class="preg-bar" aria-hidden="true"><span data-out="bar"></span><i data-out="barlabel"></i></div>
      <ol class="timeline" data-out="timeline"></ol>
      <button type="button" class="btn btn--ghost" data-ics><?= icon('calendar') ?> Add due date to my calendar</button>
    </div>
  </div>
</section>
