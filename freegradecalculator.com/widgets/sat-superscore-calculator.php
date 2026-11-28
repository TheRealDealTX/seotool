<form class="calc" data-tool="sat" novalidate>
  <?= w_head('SAT Superscore Calculator', 'star', 'Each section is scored 200–800.') ?>
  <div class="calc-body">
    <template data-row><div class="row row-sat"><span class="row-n">Test</span>
      <div><span class="row-lbl">Reading &amp; Writing</span><input class="input" name="rw" inputmode="numeric" placeholder="650"></div>
      <div><span class="row-lbl">Math</span><input class="input" name="m" inputmode="numeric" placeholder="620"></div>
      <?= w_rm() ?></div></template>
    <div class="rows" data-rows data-seed='[["620","680"],["670","640"]]'></div>
    <button type="button" class="add-row" data-add data-max="4"><?= icon('plus') ?> Add test date</button>
    <?= w_actions('Calculate superscore') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('ss', 'of 1600') ?><div><div class="result-label">Your SAT superscore</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="stats"><div class="stat"><span>Best R&amp;W</span><b data-out="rw">--</b></div><div class="stat"><span>Best Math</span><b data-out="m">--</b></div><div class="stat"><span>Best single sitting</span><b data-out="single">--</b></div></div>
    </div>
  </div>
</form>
