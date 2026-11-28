<form class="calc" data-tool="average" novalidate>
  <?= w_head('Average Calculator', 'sigma', 'Separate numbers with commas, spaces or new lines.') ?>
  <div class="calc-body">
    <div class="field"><label for="f-nums">Numbers</label><textarea class="input" id="f-nums" name="nums" rows="3">85, 92, 78, 92, 88, 95</textarea></div>
    <div class="result show" data-result>
      <div class="stats"><div class="stat"><span>Mean</span><b data-out="mean">--</b></div><div class="stat"><span>Median</span><b data-out="med">--</b></div><div class="stat"><span>Mode</span><b data-out="mode">--</b></div><div class="stat"><span>Range</span><b data-out="range">--</b></div><div class="stat"><span>Sum</span><b data-out="sum">--</b></div><div class="stat"><span>Count</span><b data-out="n">--</b></div></div>
    </div>
  </div>
</form>
