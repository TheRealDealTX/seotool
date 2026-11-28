<form class="calc" data-tool="cumgpa" novalidate>
  <?= w_head('Cumulative GPA Calculator', 'layers', 'Combine your current GPA with new terms.') ?>
  <div class="calc-body">
    <div class="grid-2"><?= w_field('g0', 'Current cumulative GPA', '3.25', '', 'decimal', '3.25') ?><?= w_field('c0', 'Credits earned so far', '45', '', 'decimal', '45') ?></div>
    <p class="lbl" style="margin:6px 0 8px">New terms</p>
    <template data-row><div class="row row-2">
      <div><span class="row-lbl">Term GPA</span><input class="input" name="g" inputmode="decimal" placeholder="3.6"></div>
      <div><span class="row-lbl">Credits</span><input class="input" name="c" inputmode="decimal" placeholder="15"></div>
      <?= w_rm() ?></div></template>
    <div class="rows" data-rows data-seed='[["3.6","15"]]'></div>
    <button type="button" class="add-row" data-add><?= icon('plus') ?> Add term</button>
    <?= w_actions('Calculate cumulative GPA') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('gpa', 'GPA') ?><div><div class="result-label">New cumulative GPA</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="stats"><div class="stat"><span>Total credits</span><b data-out="cr">--</b></div><div class="stat"><span>Quality points</span><b data-out="qp">--</b></div><div class="stat"><span>Change</span><b data-out="chg">--</b></div></div>
    </div>
  </div>
</form>
