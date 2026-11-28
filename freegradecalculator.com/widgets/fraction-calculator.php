<form class="calc" data-tool="fraction" novalidate>
  <?= w_head('Fraction Calculator', 'divide', 'Use mixed numbers like 1 1/2, fractions like 3/4, or decimals.') ?>
  <div class="calc-body">
    <div class="grid-3" style="align-items:end">
      <?= w_field('a', 'First fraction', '1 1/2', '', 'text', '1 1/2') ?>
      <div class="field"><label for="f-op">Operation</label><select class="select" id="f-op" name="op"><option value="+">+ Add</option><option value="-">− Subtract</option><option value="*">× Multiply</option><option value="/">÷ Divide</option></select></div>
      <?= w_field('b', 'Second fraction', '2/3', '', 'text', '2/3') ?>
    </div>
    <?= w_actions() ?>
    <div class="result" data-result>
      <div class="result-label">Answer</div><div class="result-big"><span data-out="big">--</span></div>
      <div class="stats"><div class="stat"><span>Mixed number</span><b data-out="mixed">--</b></div><div class="stat"><span>Decimal</span><b data-out="dec">--</b></div></div>
      <ol class="note" data-out="steps" style="padding-left:1.2em"></ol>
    </div>
  </div>
</form>
