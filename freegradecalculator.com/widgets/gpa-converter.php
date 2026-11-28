<form class="calc" data-tool="gpaconv" novalidate>
  <?= w_head('GPA Converter', 'swap', 'Percent or letter to the 4.0 scale — and back.') ?>
  <div class="calc-body">
    <div class="tabs" role="tablist"><button type="button" role="tab" aria-selected="true" data-mode="pct">Percentage → GPA</button><button type="button" role="tab" aria-selected="false" data-mode="letter">Letter → GPA</button><button type="button" role="tab" aria-selected="false" data-mode="gpa">GPA → Letter</button></div>
    <div data-show="pct"><?= w_field('pct', 'Percentage', '88', '%', 'decimal', '88') ?></div>
    <div data-show="letter" hidden><div class="field"><label>Letter grade</label><?= w_letter_select('lt', 'B+') ?></div></div>
    <div data-show="gpa" hidden><?= w_field('gpa', 'GPA (0–4.0)', '3.5', '', 'decimal', '3.5') ?></div>
    <div class="result show" data-result>
      <div class="result-main"><?= w_ring('ring') ?><div><div class="result-label" data-out="label">4.0 GPA</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="scroll-x"><table class="mini-table"><thead><tr><th>Letter</th><th>Percent</th><th>4.0 GPA</th></tr></thead><tbody data-out="scale"></tbody></table></div>
    </div>
  </div>
</form>
