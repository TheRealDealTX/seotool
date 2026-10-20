<?php $slug = 'goat-temperature-checker'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body">
    <form class="tool__form" onsubmit="return false">
      <div class="field field--split">
        <label for="gt-temp">Rectal temperature</label>
        <div class="field__row">
          <input id="gt-temp" name="temp" type="number" step="0.1" value="102.3" inputmode="decimal">
          <select name="unit" aria-label="Unit"><option value="F">°F</option><option value="C">°C</option></select>
        </div>
      </div>
      <fieldset class="field pills">
        <legend>Age</legend>
        <label><input type="radio" name="age" value="adult" checked><span>Adult</span></label>
        <label><input type="radio" name="age" value="kid"><span>Kid (under 6 months)</span></label>
      </fieldset>
      <label class="toggle"><input type="checkbox" name="hot"><span></span> It’s a hot day or the goat was just active</label>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="temp-scale" aria-hidden="true">
        <div class="temp-scale__band"><i class="z-cold"></i><i class="z-low"></i><i class="z-ok"></i><i class="z-warm"></i><i class="z-fever"></i></div>
        <span class="temp-scale__pin" data-out="pin"></span>
        <div class="temp-scale__labels"><span>98°F</span><span>101.5</span><span>103.5</span><span>106°F</span></div>
      </div>
      <div class="status" data-out="status"><strong data-out="headline">—</strong><p data-out="advice"></p></div>
    </div>
  </div>
</section>
