<form class="calc" data-tool="letter" novalidate>
  <?= w_head('Letter Grade Calculator', 'letter', 'Type a percentage — the letter updates instantly.') ?>
  <div class="calc-body">
    <?= w_field('pct', 'Percentage', '87.5', '%', 'decimal', '87.5') ?>
    <div class="result show" data-result>
      <div class="result-main"><span class="grade-pill" data-out="letter-pill" style="min-width:84px;height:84px;font-size:2.4rem">B+</span><div><div class="result-label">Letter grade</div><div class="result-big"><span data-out="big">B+</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="scroll-x"><table class="mini-table"><thead><tr><th>Letter</th><th>Percent</th><th>GPA</th></tr></thead><tbody data-out="scale"></tbody></table></div>
    </div>
  </div>
</form>
