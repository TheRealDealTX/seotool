<form class="calc" data-tool="hsgpa" novalidate>
  <?= w_head('High School GPA Calculator', 'school', 'Weighted & unweighted, with Honors and AP/IB.') ?>
  <div class="calc-body">
    <template data-row><div class="row row-hs">
      <div class="c-name"><span class="row-lbl">Class</span><input class="input" name="name" placeholder="e.g. AP Biology" autocomplete="off"></div>
      <div><span class="row-lbl">Grade</span><?= w_letter_select('g') ?></div>
      <div><span class="row-lbl">Credits</span><input class="input" name="c" inputmode="decimal" placeholder="1" value="1"></div>
      <div><span class="row-lbl">Type</span><select class="select" name="t"><option value="0">Regular</option><option value="0.5">Honors</option><option value="1">AP / IB</option></select></div>
      <?= w_rm() ?></div></template>
    <div class="rows" data-rows data-seed='[["English 11","A-","1","0.5"],["AP US History","B+","1","1"],["Algebra II","A","1","0"],["Chemistry","B","1","0"],["Spanish III","A","1","0"],["AP Biology","B+","1","1"]]'></div>
    <button type="button" class="add-row" data-add><?= icon('plus') ?> Add class</button>
    <?= w_actions('Calculate GPA') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('w', 'weighted') ?><div><div class="result-label">Weighted GPA</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="stats"><div class="stat"><span>Unweighted GPA</span><b data-out="uw">--</b></div><div class="stat"><span>Weighted GPA</span><b data-out="wt">--</b></div><div class="stat"><span>Credits</span><b data-out="cr">--</b></div></div>
    </div>
  </div>
</form>
