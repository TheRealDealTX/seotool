<form class="calc" data-tool="rubric" novalidate>
  <?= w_head('Rubric Grade Calculator', 'grid', 'Convert rubric points to a percentage.') ?>
  <div class="calc-body">
    <div class="grid-2">
      <?= w_field('e', 'Rubric points earned', '18', '', 'decimal', '18') ?>
      <?= w_field('t', 'Total rubric points', '24', '', 'decimal', '24') ?>
    </div>
    <?= w_actions('Convert') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('pct') ?><div><div class="result-label">Rubric percentage</div><div class="result-big"><span data-out="big">--</span></div><span class="grade-pill" data-out="letter-pill">--</span></div></div>
      <div class="scroll-x" style="max-height:320px;overflow:auto;margin-top:14px"><table class="mini-table" style="margin:0"><thead><tr><th>Score</th><th>Percent</th><th>Letter</th></tr></thead><tbody data-out="chart"></tbody></table></div>
    </div>
  </div>
</form>
