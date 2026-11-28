<form class="calc" data-tool="attend" novalidate>
  <?= w_head('Attendance Percentage Calculator', 'user-check', 'Know exactly where you stand.') ?>
  <div class="calc-body">
    <div class="grid-3">
      <?= w_field('h', 'Classes held', '60', '', 'numeric', '60') ?>
      <?= w_field('a', 'Classes attended', '47', '', 'numeric', '47') ?>
      <?= w_field('req', 'Required', '75', '%', 'decimal', '75') ?>
    </div>
    <?= w_actions('Check attendance') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('pct', 'attendance') ?><div><div class="result-label">Current attendance</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
    </div>
  </div>
</form>
