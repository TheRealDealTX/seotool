<form class="calc" data-tool="cgpa" novalidate>
  <?= w_head('CGPA to Percentage Calculator', 'percent', '10-point CGPA ⇄ percentage.') ?>
  <div class="calc-body">
    <div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="true" data-mode="c2p">CGPA → %</button><button type="button" role="tab" aria-selected="false" data-mode="p2c">% → CGPA</button></div>
    <div class="grid-2">
      <div data-show="c2p"><?= w_field('cg', 'CGPA (out of 10)', '8.4', '', 'decimal', '8.4') ?></div>
      <div data-show="p2c" hidden><?= w_field('pc', 'Percentage', '79.8', '%', 'decimal', '79.8') ?></div>
      <?= w_field('mult', 'Multiplier', '9.5', '×', 'decimal', '9.5') ?>
    </div>
    <div class="result show" data-result>
      <div class="result-main"><?= w_ring('ring') ?><div><div class="result-label" data-out="label">Percentage</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <p class="note">9.5 is the CBSE convention. Many universities publish their own formula — check your marksheet or registrar.</p>
    </div>
  </div>
</form>
