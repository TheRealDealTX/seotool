<form class="calc" data-tool="ezgrader" novalidate>
  <?= w_head('EZ Grader', 'table', 'Instant grading chart for any test.') ?>
  <div class="calc-body">
    <div class="grid-2">
      <?= w_field('n', 'Number of questions / points', '20', '', 'numeric', '20') ?>
      <div class="field"><label for="f-step">Step</label><select class="select" id="f-step" name="step"><option value="1">Whole points</option><option value="0.5">Half points</option></select></div>
    </div>
    <div class="calc-actions"><button type="submit" class="btn btn-primary"><?= icon('zap') ?> Build chart</button><button type="button" class="btn btn-ghost" data-print><?= icon('print') ?> Print</button></div>
    <div class="result" data-result>
      <div class="scroll-x" style="max-height:520px;overflow:auto"><table class="mini-table" style="margin:0"><thead><tr><th>Wrong</th><th>Right</th><th>Score</th><th>Grade</th></tr></thead><tbody data-out="chart"></tbody></table></div>
    </div>
  </div>
</form>
