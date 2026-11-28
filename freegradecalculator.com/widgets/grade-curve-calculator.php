<form class="calc" data-tool="curve" novalidate>
  <?= w_head('Grade Curve Calculator', 'bell', 'Paste scores separated by commas, spaces or new lines.') ?>
  <div class="calc-body">
    <div class="field"><label for="f-scores">Raw scores</label><textarea class="input" id="f-scores" name="scores" rows="4">62, 71, 75, 78, 80, 83, 85, 88, 64, 70, 91, 58</textarea></div>
    <div class="grid-2">
      <div class="field"><label for="f-method">Curve method</label><select class="select" id="f-method" name="method">
        <option value="flat">Flat — top score becomes 100</option><option value="add">Add points to everyone</option><option value="sqrt">Square root (10 × √score)</option><option value="mean">Shift to a target average</option><option value="bell">Bell curve (target mean &amp; SD)</option></select></div>
      <div data-m="add mean bell"><?= w_field('p1', 'Points / target mean', '75', '', 'decimal', '75') ?></div>
      <div data-m="bell"><?= w_field('p2', 'Target standard deviation', '10', '', 'decimal', '10') ?></div>
    </div>
    <label class="switch" style="margin-top:6px"><input type="checkbox" name="cap" checked> Cap curved scores at 100</label>
    <?= w_actions('Curve scores') ?>
    <div class="result" data-result>
      <div class="stats"><div class="stat"><span>Old average</span><b data-out="m0">--</b></div><div class="stat"><span>New average</span><b data-out="m1">--</b></div><div class="stat"><span>Students</span><b data-out="n">--</b></div></div>
      <div class="scroll-x" style="max-height:380px;overflow:auto;margin-top:14px"><table class="mini-table" style="margin:0"><thead><tr><th>#</th><th>Original</th><th>Curved</th><th>Grade</th></tr></thead><tbody data-out="table"></tbody></table></div>
    </div>
  </div>
</form>
