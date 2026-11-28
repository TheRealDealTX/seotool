<?php $tag = $tag ?? 'h2'; ?>
<form class="calc" data-tool="weighted" novalidate>
  <?= w_head('Weighted Grade Calculator', 'scale', 'Scores can be percentages (92) or letters (A-).', true, $tag) ?>
  <div class="calc-body">
    <template data-row><div class="row row-cat">
      <div class="c-name"><span class="row-lbl">Category</span><input class="input" name="name" placeholder="e.g. Tests" autocomplete="off"></div>
      <div><span class="row-lbl">Weight %</span><input class="input" name="w" inputmode="decimal" placeholder="40" autocomplete="off"></div>
      <div><span class="row-lbl">Score</span><input class="input" name="s" placeholder="92 or A-" autocomplete="off"></div>
      <?= w_rm() ?></div></template>
    <div class="rows" data-rows data-seed='[["Tests","40","88"],["Quizzes","20","92"],["Homework","25","A-"],["Participation","15","100"]]'></div>
    <button type="button" class="add-row" data-add><?= icon('plus') ?> Add category</button>
    <?= w_actions('Calculate my grade') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('pct', 'overall') ?><div><div class="result-label">Your weighted grade</div><div class="result-big"><span data-out="big">--</span></div><span class="grade-pill" data-out="letter-pill">--</span></div></div>
      <div class="stats"><div class="stat"><span>Letter</span><b data-out="letter">--</b></div><div class="stat"><span>GPA points</span><b data-out="gpa">--</b></div><div class="stat"><span>Total weight</span><b data-out="tw">--</b></div></div>
      <div class="bars" data-out="bars"></div>
      <p class="note" data-out="note"></p>
    </div>
  </div>
</form>
