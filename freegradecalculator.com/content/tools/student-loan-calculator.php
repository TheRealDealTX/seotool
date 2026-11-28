<?php
return [
  'h1'          => 'Student Loan Calculator',
  'meta_title'  => 'Student Loan Calculator – Monthly Payment & Interest',
  'description' => 'Free student loan calculator: enter loan amount, interest rate, and term to see your monthly payment, total interest, total paid, and yearly balance chart.',
  'lead'        => 'Enter your student loan amount, interest rate, and repayment term to see your monthly payment, total interest, total cost, and how your balance drops each year.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the student loan calculator</h2>
<ol class="steps">
  <li><strong>Enter the loan amount.</strong> The total you borrowed or expect to borrow for college. If you have several loans with the same rate, you can add them together.</li>
  <li><strong>Enter the interest rate (APR %).</strong> Find it on your loan documents or your loan servicer's website.</li>
  <li><strong>Enter the term in years.</strong> The classic standard plan for federal student loans is 10 years, though federal rules for newer loans can set longer standard terms for larger balances. Private loans often offer 5 to 20 years.</li>
  <li><strong>Read your results.</strong> You see your monthly payment, the total interest you will pay, the total amount paid, and a chart of your remaining balance at the end of each year.</li>
</ol>

<h2 id="formula">Student loan payment formula</h2>
<p>The calculator uses the standard amortization formula for a fixed-rate loan with equal monthly payments:</p>
<div class="formula">M = P · r ÷ (1 − (1 + r)<sup>−n</sup>)</div>
<ul>
  <li><strong>M</strong> = monthly payment</li>
  <li><strong>P</strong> = loan amount (principal)</li>
  <li><strong>r</strong> = monthly interest rate = APR ÷ 100 ÷ 12</li>
  <li><strong>n</strong> = number of monthly payments = years × 12</li>
</ul>
<div class="formula">Total paid = M × n &nbsp;&nbsp;·&nbsp;&nbsp; Total interest = Total paid − P</div>

<div class="example-box"><h4>Worked example</h4>
<p>You borrow <strong>$30,000</strong> at <strong>6.5% APR</strong> on a <strong>10-year</strong> standard plan.</p>
<p>r = 0.065 ÷ 12 ≈ 0.0054167, and n = 10 × 12 = 120.</p>
<p>M = 30,000 × 0.0054167 ÷ (1 − 1.0054167<sup>−120</sup>) ≈ <strong>$340.64 per month</strong>.</p>
<p>Total paid = $340.64 × 120 ≈ <strong>$40,877</strong>. Total interest ≈ <strong>$10,877</strong>.</p>
<p>After 5 years, the balance is still about <strong>$17,410</strong>, because early payments go mostly to interest.</p>
</div>

<h2 id="term-comparison">How the repayment term changes the cost</h2>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>$30,000 at 6.5%</th><th>Monthly payment</th><th>Total interest</th></tr></thead>
<tbody>
<tr><td>10-year term</td><td>$340.64</td><td>$10,877</td></tr>
<tr><td>20-year term</td><td>$223.67</td><td>$23,681</td></tr>
</tbody></table></div>
<p>Stretching the loan to 20 years lowers the monthly payment by about $117, but more than doubles the interest. A shorter term costs more each month and much less overall. Try different terms in the calculator to find a payment that fits your budget.</p>

<h2 id="what-it-includes">What this calculator does and does not include</h2>
<p>The results assume a fixed interest rate, equal monthly payments, and that repayment starts on the full amount you enter. Real loans can differ:</p>
<ul>
  <li><strong>Interest while in school.</strong> Unsubsidized federal loans and most private loans build interest while you are in school and during any grace period. If unpaid interest is added to your balance, enter the higher amount.</li>
  <li><strong>Other repayment plans.</strong> Federal loans offer plans such as graduated, extended, and income-driven repayment, which work differently from the standard plan. Check studentaid.gov for current options.</li>
  <li><strong>Variable rates.</strong> Some private loans have rates that change over time, so your actual payment may go up or down.</li>
  <li><strong>Fees.</strong> Federal loans charge an origination fee that is taken out of each disbursement, so you receive slightly less than you borrow.</li>
</ul>

<h2 id="balance-chart">Reading the yearly balance chart</h2>
<p>The chart shows what you still owe at the end of each year. In the $30,000 example, the balance falls to about $27,797 after year one, $17,410 after year five, and $3,947 after year nine before reaching zero. The line curves downward faster over time because, as the balance shrinks, less of each payment goes to interest and more goes to principal.</p>

<h2 id="tips">Tips for borrowing less and paying less</h2>
<ul>
  <li><strong>Borrow only what you need.</strong> Every $1,000 you skip borrowing at 6.5% over 10 years saves about $363 in interest.</li>
  <li><strong>Pay interest while in school if you can.</strong> Even small payments keep interest from piling onto your balance.</li>
  <li><strong>Pay extra toward principal.</strong> Extra payments shorten the loan and cut total interest. Ask your servicer to apply them to principal.</li>
  <li><strong>Compare the payment with your expected salary.</strong> A common rule of thumb is to keep total student debt below your expected first-year salary.</li>
  <li><strong>Keep your grades up for scholarships.</strong> Many merit scholarships require a minimum GPA to renew, and every renewed scholarship means less to borrow. Track yours with the <a href="/gpa-calculator">GPA calculator</a>.</li>
</ul>
HTML,
  'faqs'        => [
    ['How is a student loan monthly payment calculated?', 'It uses the amortization formula M = P × r ÷ (1 − (1 + r)^−n), where P is the loan amount, r is the monthly interest rate, and n is the number of monthly payments.'],
    ['What is the monthly payment on a $30,000 student loan?', 'At 6.5% APR over 10 years, the payment is about $340.64 a month, with roughly $10,877 in total interest. Your rate and term will change the result.'],
    ['What is the standard repayment plan for student loans?', 'The classic federal standard plan has fixed monthly payments over 10 years, and it usually costs the least interest among federal plans. Rules for newer federal loans can allow longer standard terms for larger balances, so check studentaid.gov for the plan that applies to your loans.'],
    ['Does this calculator include interest that builds up in school?', 'No. It assumes repayment starts on the amount you enter. If interest accrued during school was added to your balance, enter that higher amount.'],
    ['Does a longer loan term save money?', 'No. A longer term lowers the monthly payment but increases total interest. For $30,000 at 6.5%, a 20-year term costs about $23,681 in interest versus $10,877 over 10 years.'],
  ],
];
