<form class="calc" data-tool="classavg" novalidate>
  <?= w_head('Class Average Calculator', 'chart', 'Paste every student’s score.') ?>
  <div class="calc-body">
    <div class="field"><label for="f-sc">Scores</label><textarea class="input" id="f-sc" name="scores" rows="4">92 85 78 88 95 67 73 81 90 84 76 59 98 87 82</textarea></div>
    <?= w_actions('Analyze class') ?>
    <div class="result" data-result>
      <div class="stats"><div class="stat"><span>Mean</span><b data-out="mean">--</b></div><div class="stat"><span>Median</span><b data-out="med">--</b></div><div class="stat"><span>Mode</span><b data-out="mode">--</b></div><div class="stat"><span>Std. dev.</span><b data-out="sd">--</b></div><div class="stat"><span>Range</span><b data-out="range">--</b></div><div class="stat"><span>Min / Max</span><b data-out="mm">--</b></div><div class="stat"><span>Count</span><b data-out="n">--</b></div></div>
      <p class="lbl" style="margin:16px 0 0">Grade distribution</p>
      <div class="bars" data-out="dist"></div>
    </div>
  </div>
</form>
