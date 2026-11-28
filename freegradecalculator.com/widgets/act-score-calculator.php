<form class="calc" data-tool="act" novalidate>
  <?= w_head('ACT Score Calculator', 'award', 'Section scores 1–36.') ?>
  <div class="calc-body">
    <div class="grid-4">
      <?= w_field('en', 'English', '28', '', 'numeric', '28') ?>
      <?= w_field('ma', 'Math', '26', '', 'numeric', '26') ?>
      <?= w_field('rd', 'Reading', '30', '', 'numeric', '30') ?>
      <?= w_field('sc', 'Science (optional)', '25', '', 'numeric', '25') ?>
    </div>
    <label class="switch" style="margin-top:12px"><input type="checkbox" name="legacy"> Include Science in composite (legacy ACT)</label>
    <?= w_actions('Calculate composite') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('comp', 'of 36') ?><div><div class="result-label">ACT composite</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="stats"><div class="stat"><span>Exact average</span><b data-out="avg">--</b></div><div class="stat"><span>STEM score</span><b data-out="stem">--</b></div></div>
    </div>
  </div>
</form>
