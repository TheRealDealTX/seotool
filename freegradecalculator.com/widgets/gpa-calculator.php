<form class="calc" data-tool="gpa" novalidate>
  <?= w_head('College GPA Calculator', 'cap', '4.0 scale with plus/minus grades.') ?>
  <div class="calc-body">
    <template data-row><div class="row row-course">
      <div class="c-name"><span class="row-lbl">Course</span><input class="input" name="name" placeholder="e.g. Biology 101" autocomplete="off"></div>
      <div><span class="row-lbl">Grade</span><?= w_letter_select('g') ?></div>
      <div><span class="row-lbl">Credits</span><input class="input" name="c" inputmode="decimal" placeholder="3"></div>
      <?= w_rm() ?></div></template>
    <div class="rows" data-rows data-seed='[["English Composition","A","3"],["Calculus I","B+","4"],["Intro to Psychology","A-","3"],["Chemistry Lab","B","1"]]'></div>
    <button type="button" class="add-row" data-add><?= icon('plus') ?> Add course</button>
    <details style="margin-top:14px"><summary style="font-weight:700;cursor:pointer">Include previous semesters (cumulative GPA)</summary>
      <div class="grid-2" style="margin-top:12px"><?= w_field('pg', 'Current cumulative GPA', '3.20', '', 'decimal') ?><?= w_field('pc', 'Credits already earned', '30', '', 'decimal') ?></div>
    </details>
    <?= w_actions('Calculate GPA') ?>
    <div class="result" data-result>
      <div class="result-main"><?= w_ring('gpa', 'GPA') ?><div><div class="result-label">Semester GPA</div><div class="result-big"><span data-out="big">--</span></div><p class="result-msg" data-out="msg"></p></div></div>
      <div class="stats"><div class="stat"><span>Credits</span><b data-out="cr">--</b></div><div class="stat"><span>Quality points</span><b data-out="qp">--</b></div><div class="stat" data-cum hidden><span>New cumulative</span><b data-out="cum">--</b></div></div>
    </div>
  </div>
</form>
