<form class="calc" data-tool="raise" novalidate>
  <?= w_head('Raise My Grade Calculator', 'trend', 'Works for points-based classes.') ?>
  <div class="calc-body">
    <div class="grid-2">
      <?= w_field('e', 'Points earned so far', '410', '', 'decimal', '410') ?>
      <?= w_field('p', 'Points possible so far', '500', '', 'decimal', '500') ?>
      <?= w_field('r', 'Points still to come', '300', '', 'decimal', '300') ?>
      <?= w_field('t', 'Target grade', '85', '%', 'decimal', '85') ?>
    </div>
    <?= w_actions('Show what I need') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('need', 'needed') ?><div><div class="result-label">Average needed on remaining work</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="stats"><div class="stat"><span>Current grade</span><b data-out="cur">--</b></div><div class="stat"><span>Best possible</span><b data-out="max">--</b></div><div class="stat"><span>Lowest possible</span><b data-out="min">--</b></div></div>
    </div>
  </div>
</form>
