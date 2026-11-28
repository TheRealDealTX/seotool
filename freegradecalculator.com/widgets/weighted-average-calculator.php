<form class="calc" data-tool="wavg" novalidate>
  <?= w_head('Weighted Average Calculator', 'scale', 'Enter each value and its weight.') ?>
  <div class="calc-body">
    <template data-row><div class="row row-2">
      <div><span class="row-lbl">Value</span><input class="input" name="v" inputmode="decimal" placeholder="90"></div>
      <div><span class="row-lbl">Weight</span><input class="input" name="w" inputmode="decimal" placeholder="2"></div>
      <?= w_rm() ?></div></template>
    <div class="rows" data-rows data-seed='[["90","3"],["75","1"],["84","2"]]'></div>
    <button type="button" class="add-row" data-add><?= icon('plus') ?> Add value</button>
    <?= w_actions() ?>
    <div class="result" data-result>
      <div class="result-label">Weighted average</div><div class="result-big"><span data-out="big">--</span></div>
      <div class="stats"><div class="stat"><span>Sum of weights</span><b data-out="sw">--</b></div><div class="stat"><span>Simple average</span><b data-out="sa">--</b></div></div>
    </div>
  </div>
</form>
