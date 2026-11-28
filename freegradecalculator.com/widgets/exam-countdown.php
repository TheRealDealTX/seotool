<div class="calc" data-tool="countdown">
  <?= w_head('Exam Countdown', 'hourglass', 'Saved on this device.', false) ?>
  <div class="calc-body">
    <div class="grid-2"><?= w_field('name', 'Exam name', 'Calculus final', '', 'text', 'Final exams') ?><div class="field"><label for="f-dt">Exam date &amp; time</label><input class="input" id="f-dt" type="datetime-local" name="dt"></div></div>
    <?= w_field('hrs', 'Total study hours you need (optional)', '30', 'hours', 'decimal', '30') ?>
    <div class="result show" data-result>
      <div class="result-label" data-out="label">Time left</div>
      <div class="countdown"><div><b data-out="d">0</b><span>Days</span></div><div><b data-out="h">0</b><span>Hours</span></div><div><b data-out="m">0</b><span>Min</span></div><div><b data-out="s">0</b><span>Sec</span></div></div>
      <p class="result-msg" data-out="msg"></p>
    </div>
  </div>
</div>
