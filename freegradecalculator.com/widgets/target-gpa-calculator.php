<form class="calc" data-tool="target" novalidate>
  <?= w_head('Target GPA Calculator', 'target', 'Plan the GPA you need to reach your goal.') ?>
  <div class="calc-body">
    <div class="grid-2">
      <?= w_field('g', 'Current GPA', '3.1', '', 'decimal', '3.1') ?>
      <?= w_field('c', 'Credits completed', '60', '', 'decimal', '60') ?>
      <?= w_field('t', 'Target GPA', '3.3', '', 'decimal', '3.3') ?>
      <?= w_field('r', 'Credits remaining', '30', '', 'decimal', '30') ?>
    </div>
    <?= w_actions('What GPA do I need?') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('need', 'needed') ?><div><div class="result-label">GPA needed on remaining credits</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
    </div>
  </div>
</form>
