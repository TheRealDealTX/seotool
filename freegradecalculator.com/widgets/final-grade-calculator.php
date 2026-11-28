<?php $tag = $tag ?? 'h2'; ?>
<form class="calc" data-tool="final" novalidate>
  <?= w_head('Final Grade Calculator', 'flag', 'What do I need on my final exam?', true, $tag) ?>
  <div class="calc-body">
    <div class="grid-3">
      <?= w_field('cur', 'Current grade', '84 or B', '', 'text', '84') ?>
      <?= w_field('want', 'Grade you want', '85 or B', '', 'text', '85') ?>
      <?= w_field('w', 'Final is worth', '20', '%', 'decimal', '20') ?>
    </div>
    <?= w_actions('Find my required score') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('need', 'needed') ?><div><div class="result-label">You need on the final</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="scroll-x"><table class="mini-table"><thead><tr><th>To finish with</th><th>You need on the final</th></tr></thead><tbody data-out="table"></tbody></table></div>
    </div>
  </div>
</form>
