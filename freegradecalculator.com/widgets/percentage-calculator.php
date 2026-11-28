<form class="calc" data-tool="percent" novalidate>
  <?= w_head('Percentage Calculator', 'percent', 'Results update as you type.') ?>
  <div class="calc-body">
    <div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="true" data-mode="of">X% of Y</button><button type="button" role="tab" aria-selected="false" data-mode="what">X is what % of Y</button><button type="button" role="tab" aria-selected="false" data-mode="chg">% change</button></div>
    <div class="grid-2">
      <?= w_field('x', 'X', '15', '', 'decimal', '15') ?>
      <?= w_field('y', 'Y', '80', '', 'decimal', '80') ?>
    </div>
    <div class="result show" data-result>
      <div class="result-label" data-out="label">Result</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p>
    </div>
  </div>
</form>
