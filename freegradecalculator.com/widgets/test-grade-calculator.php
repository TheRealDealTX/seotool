<form class="calc" data-tool="test" novalidate>
  <?= w_head('Test Grade Calculator', 'check', 'Enter the number of questions and how many you missed.') ?>
  <div class="calc-body">
    <div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="true" data-mode="wrong">Number wrong</button><button type="button" role="tab" aria-selected="false" data-mode="right">Number right</button></div>
    <div class="grid-2">
      <?= w_field('total', 'Total questions / points', '25', '', 'decimal', '25') ?>
      <?= w_field('n', 'Number wrong', '3', '', 'decimal', '3') ?>
    </div>
    <?= w_actions('Grade this test') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('pct', 'score') ?><div><div class="result-label">Test score</div><div class="result-big"><span data-out="big">--</span></div><span class="grade-pill" data-out="letter-pill">--</span></div></div>
      <div class="scroll-x" style="max-height:340px;overflow:auto;margin-top:14px"><table class="mini-table" style="margin:0"><thead><tr><th>Wrong</th><th>Right</th><th>Score</th><th>Grade</th></tr></thead><tbody data-out="chart"></tbody></table></div>
    </div>
  </div>
</form>
