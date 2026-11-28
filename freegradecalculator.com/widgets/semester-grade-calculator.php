<form class="calc" data-tool="semester" novalidate>
  <?= w_head('Semester Grade Calculator', 'calendar', 'Quarter grades + final exam = semester grade.') ?>
  <div class="calc-body">
    <div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="true" data-mode="grade">Semester grade</button><button type="button" role="tab" aria-selected="false" data-mode="need">Final needed</button></div>
    <div class="grid-2">
      <?= w_field('q1', 'Quarter 1 grade', '88', '%', 'decimal', '88') ?>
      <?= w_field('q1w', 'Q1 weight', '40', '%', 'decimal', '40') ?>
      <?= w_field('q2', 'Quarter 2 grade', '84', '%', 'decimal', '84') ?>
      <?= w_field('q2w', 'Q2 weight', '40', '%', 'decimal', '40') ?>
      <div data-show="grade"><?= w_field('fe', 'Final exam grade', '90', '%', 'decimal', '90') ?></div>
      <div data-show="need" hidden><?= w_field('target', 'Target semester grade', '90', '%', 'decimal', '90') ?></div>
      <?= w_field('few', 'Final exam weight', '20', '%', 'decimal', '20') ?>
    </div>
    <?= w_actions() ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('pct') ?><div><div class="result-label" data-out="label">Semester grade</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
    </div>
  </div>
</form>
