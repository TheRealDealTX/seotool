<?php $slug = 'pumpkin-pie-troubleshooter'; ?>
<section class="tool tool--<?= $tool['color'] ?>" data-tool="<?= $slug ?>" id="<?= $slug ?>">
  <?php include __DIR__ . '/_head.php' ?>
  <div class="tool__body tool__body--stack">
    <form class="tool__form" onsubmit="return false">
      <fieldset class="field symptoms">
        <legend>What went wrong? Pick all that apply.</legend>
        <label><input type="checkbox" name="s" value="watery"><span>💧 Watery or runny center</span></label>
        <label><input type="checkbox" name="s" value="cracked"><span>⚡ Cracked top</span></label>
        <label><input type="checkbox" name="s" value="soggy"><span>🥧 Soggy bottom crust</span></label>
        <label><input type="checkbox" name="s" value="weeping"><span>💦 Liquid pooling after cooling</span></label>
        <label><input type="checkbox" name="s" value="grainy"><span>🌾 Grainy or curdled texture</span></label>
        <label><input type="checkbox" name="s" value="sunken"><span>⬇️ Puffed up, then sank</span></label>
        <label><input type="checkbox" name="s" value="edges"><span>🔥 Crust edges burnt</span></label>
        <label><input type="checkbox" name="s" value="bland"><span>😐 Bland flavor</span></label>
      </fieldset>
    </form>
    <div class="tool__out" aria-live="polite">
      <div class="diagnosis" data-out="diagnosis"><p class="diagnosis__empty">Pick a problem above to see what caused it and how to fix it.</p></div>
    </div>
  </div>
</section>
