<?php
return [
  'h1'          => 'Percentage Calculator',
  'meta_title'  => 'Percentage Calculator – Percent Of, Percent & % Change',
  'description' => 'Free percentage calculator: find X% of Y, what percent X is of Y, or the percent change from X to Y. Simple formulas and examples for grades and homework.',
  'lead'        => 'Find a percentage of a number, what percent one number is of another, or the percent change between two numbers, with the formula shown for each.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the percentage calculator</h2>
<p>The percentage calculator has three modes. Pick the one that matches your question, type two numbers, and the answer appears instantly.</p>
<ol class="steps">
  <li><strong>What is X% of Y?</strong> Use this to find a portion of a total, such as 15% of 80.</li>
  <li><strong>X is what percent of Y?</strong> Use this to turn a score into a percentage, such as 42 out of 56.</li>
  <li><strong>Percent change from X to Y.</strong> Use this to see how much something went up or down, such as a test score that rose from 40 to 52.</li>
</ol>

<h2 id="formulas">Percentage formulas</h2>
<h3>X% of Y</h3>
<div class="formula">Result = X ÷ 100 × Y</div>
<h3>X is what percent of Y</h3>
<div class="formula">Percent = X ÷ Y × 100</div>
<h3>Percent change from X to Y</h3>
<div class="formula">Percent change = (Y − X) ÷ X × 100</div>
<p>A positive percent change is an increase, and a negative one is a decrease. The starting value always goes in the denominator.</p>

<div class="example-box"><h4>Worked examples</h4>
<p><strong>15% of 80:</strong> 15 ÷ 100 × 80 = <strong>12</strong>. If a homework category is worth 15% of an 80-point project, it is worth 12 points.</p>
<p><strong>42 is what percent of 56:</strong> 42 ÷ 56 × 100 = <strong>75%</strong>. Getting 42 of 56 points right on a test is a 75%.</p>
<p><strong>Percent change from 40 to 52:</strong> (52 − 40) ÷ 40 × 100 = <strong>+30%</strong>. Going the other way, from 52 to 40, is (40 − 52) ÷ 52 × 100 = <strong>−23.1%</strong>.</p>
</div>
<p>Notice in the last example that a 30% increase and the matching decrease are not the same size. Percent change always depends on where you start.</p>

<h2 id="grades">Using percentages for grades</h2>
<p>Most school grades are percentages underneath the letters. To figure out your grade on a test, use the "X is what percent of Y" mode with your points earned and points possible. A score of 18 out of 24 is 75%, and 47 out of 50 is 94%.</p>
<p>For a whole class grade built from several categories with different weights, a single percentage is not enough, because each category counts differently. In that case, use the <a href="/weighted-grade-calculator">weighted grade calculator</a>. If you are working out exactly how teachers combine assignment percentages, our guide on <a href="/blog/how-to-calculate-your-final-grade">how to calculate your final grade</a> walks through the math.</p>

<h2 id="everyday-uses">Other everyday uses for students</h2>
<div class="table-wrap"><table class="data-table">
<thead><tr><th>Situation</th><th>Mode</th><th>Example</th></tr></thead>
<tbody>
<tr><td>Sale price on a textbook</td><td>X% of Y</td><td>20% off $60 saves $12</td></tr>
<tr><td>Tip at a restaurant</td><td>X% of Y</td><td>18% of $25 is $4.50</td></tr>
<tr><td>Quiz score</td><td>X is what % of Y</td><td>9 of 12 is 75%</td></tr>
<tr><td>Reading progress</td><td>X is what % of Y</td><td>150 of 400 pages is 37.5%</td></tr>
<tr><td>Grade improvement</td><td>% change</td><td>70 to 84 is +20%</td></tr>
</tbody></table></div>

<h2 id="mental-math">Quick mental math for percentages</h2>
<p>You do not always need a calculator. These shortcuts help you check answers fast:</p>
<ul>
  <li><strong>10%:</strong> move the decimal one place left. 10% of 85 is 8.5.</li>
  <li><strong>5%:</strong> half of 10%. 5% of 85 is 4.25.</li>
  <li><strong>25%:</strong> divide by 4. 25% of 60 is 15.</li>
  <li><strong>Swap trick:</strong> X% of Y equals Y% of X. 8% of 50 is the same as 50% of 8, which is 4.</li>
</ul>

<h2 id="tips">Tips and common mistakes</h2>
<ul>
  <li><strong>Percent change vs. percentage points.</strong> Going from an 80% to a 90% is a gain of 10 percentage points, but a 12.5% increase. Teachers and report cards usually talk in percentage points.</li>
  <li><strong>Put the original value first.</strong> In percent change, divide by the starting number, not the ending one.</li>
  <li><strong>Convert percents to decimals.</strong> 15% = 0.15. Multiplying by the decimal is the same as dividing by 100 first.</li>
  <li><strong>Check that the answer makes sense.</strong> A part should be smaller than the whole unless the percent is over 100.</li>
  <li><strong>Reverse a discount carefully.</strong> If a price dropped 20% to $48, the original was $48 ÷ 0.80 = $60, not $48 + 20%.</li>
</ul>
HTML,
  'faqs'        => [
    ['How do I calculate a percentage of a number?', 'Divide the percent by 100 and multiply by the number. For example, 15% of 80 is 0.15 × 80 = 12.'],
    ['How do I find what percent one number is of another?', 'Divide the part by the whole and multiply by 100. For example, 42 out of 56 is 42 ÷ 56 × 100 = 75%.'],
    ['How do you calculate percent change?', 'Subtract the old value from the new value, divide by the old value, and multiply by 100. A change from 40 to 52 is a 30% increase.'],
    ['How do I turn my test score into a percentage?', 'Use the "X is what percent of Y" mode with your points earned as X and the points possible as Y. 47 out of 50 is 94%.'],
    ['What is the difference between percent and percentage points?', 'Percentage points are the simple difference between two percentages, such as 80% to 90% (10 points). Percent change compares that difference to the starting value (12.5%).'],
  ],
];
