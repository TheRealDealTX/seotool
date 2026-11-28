<form class="calc" data-tool="loan" novalidate>
  <?= w_head('Student Loan Calculator', 'dollar', 'Standard fixed-rate repayment.') ?>
  <div class="calc-body">
    <div class="grid-3">
      <?= w_field('p', 'Loan amount', '30000', '$', 'decimal', '30000') ?>
      <?= w_field('r', 'Interest rate (APR)', '6.5', '%', 'decimal', '6.5') ?>
      <?= w_field('y', 'Term', '10', 'yrs', 'decimal', '10') ?>
    </div>
    <?= w_actions() ?>
    <div class="result" data-result>
      <div class="result-label">Monthly payment</div><div class="result-big"><span data-out="big">--</span></div>
      <div class="stats"><div class="stat"><span>Total interest</span><b data-out="ti">--</b></div><div class="stat"><span>Total paid</span><b data-out="tp">--</b></div><div class="stat"><span>Payments</span><b data-out="n">--</b></div></div>
      <p class="lbl" style="margin:16px 0 0">Remaining balance by year</p><div class="bars" data-out="bars"></div>
    </div>
  </div>
</form>
