<form class="calc" data-tool="points" novalidate>
  <?= w_head('Points Grade Calculator', 'plus', 'Add each assignment’s points earned and points possible.') ?>
  <div class="calc-body">
    <template data-row><div class="row row-pts">
      <div class="c-name"><span class="row-lbl">Assignment</span><input class="input" name="name" placeholder="e.g. Lab report" autocomplete="off"></div>
      <div><span class="row-lbl">Earned</span><input class="input" name="e" inputmode="decimal" placeholder="18"></div>
      <div><span class="row-lbl">Possible</span><input class="input" name="p" inputmode="decimal" placeholder="20"></div>
      <?= w_rm() ?></div></template>
    <div class="rows" data-rows data-seed='[["Homework 1","18","20"],["Quiz 1","42","50"],["Project","88","100"]]'></div>
    <button type="button" class="add-row" data-add><?= icon('plus') ?> Add assignment</button>
    <?= w_actions('Total my points') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('pct', 'grade') ?><div><div class="result-label">Your grade</div><div class="result-big"><span data-out="big">--</span></div><span class="grade-pill" data-out="letter-pill">--</span></div></div>
      <div class="stats"><div class="stat"><span>Points earned</span><b data-out="e">--</b></div><div class="stat"><span>Points possible</span><b data-out="p">--</b></div><div class="stat"><span>Points missed</span><b data-out="m">--</b></div></div>
    </div>
  </div>
</form>
