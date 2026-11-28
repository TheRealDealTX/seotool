<?php
return [
  'h1'          => 'Rubric Grade Calculator',
  'meta_title'  => 'Rubric Grade Calculator – Rubric Score to Percentage',
  'description' => 'Free rubric grade calculator: convert rubric points (like 18/24 or 3.25/4) to a percentage and letter grade, with a chart for every whole and half score.',
  'lead'        => 'Convert a rubric score into a percentage and letter grade, and see a full conversion chart for every whole and half point.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the rubric grade calculator</h2>
<p>Rubrics are great for feedback, but report cards need percentages. This rubric grade calculator converts a rubric score into a percentage and a letter grade, whether your rubric totals 24 points or uses a 4-point scale.</p>
<ol class="steps">
  <li><strong>Enter the rubric points earned.</strong> Add up the scores across every criterion, such as 18. For a 4-point rubric, you can enter an average like 3.25.</li>
  <li><strong>Enter the total rubric points.</strong> The maximum possible, such as 24 (six criteria × 4 points) or 4.</li>
  <li><strong>Read the result.</strong> You'll see the percentage and its letter grade.</li>
  <li><strong>Use the chart.</strong> A conversion chart lists the percentage and letter for every whole and half score on that rubric, which is handy when grading a full class set.</li>
</ol>

<h2 id="formula">The rubric to percentage formula</h2>
<div class="formula">Rubric % = Points earned ÷ Total rubric points × 100</div>
<p>This is a straight proportion, the same math as a test score. The letter grade then comes from the standard US scale (A 93–96, B 83–86, C 73–76, and so on).</p>

<div class="example-box"><h4>Worked example: a 24-point rubric</h4>
<p>An essay rubric has six criteria scored 1–4, for 24 points total. A student earns 18.</p>
<p>18 ÷ 24 = 0.75 → <strong>75%</strong>, a <strong>C</strong>.</p>
</div>

<div class="example-box"><h4>Worked example: a 4-point rubric</h4>
<p>A student averages 3.25 on a 4-point rubric.</p>
<p>3.25 ÷ 4 = 0.8125 → <strong>81.25%</strong>, a <strong>B-</strong>.</p>
</div>

<h2 id="four-point-chart">4-point rubric conversion chart</h2>
<p>Here's how a 4-point rubric converts with straight percentages:</p>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Rubric score</th><th>Percentage</th><th>Letter</th></tr></thead><tbody>
<tr><td>4</td><td>100%</td><td>A+</td></tr>
<tr><td>3.5</td><td>87.5%</td><td>B+</td></tr>
<tr><td>3</td><td>75%</td><td>C</td></tr>
<tr><td>2.5</td><td>62.5%</td><td>D- or D, depending on rounding</td></tr>
<tr><td>2</td><td>50%</td><td>F</td></tr>
<tr><td>1</td><td>25%</td><td>F</td></tr>
</tbody></table></div>

<h2 id="twenty-four-point-chart">24-point rubric conversion chart</h2>
<p>A longer rubric gives much finer steps. Here are the top whole scores on a 24-point rubric (six criteria × 4 points):</p>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Rubric score</th><th>Percentage</th><th>Letter</th></tr></thead><tbody>
<tr><td>24 / 24</td><td>100%</td><td>A+</td></tr>
<tr><td>23 / 24</td><td>95.8%</td><td>A</td></tr>
<tr><td>22 / 24</td><td>91.7%</td><td>A-</td></tr>
<tr><td>21 / 24</td><td>87.5%</td><td>B+</td></tr>
<tr><td>20 / 24</td><td>83.3%</td><td>B</td></tr>
<tr><td>19 / 24</td><td>79.2%</td><td>C+</td></tr>
<tr><td>18 / 24</td><td>75%</td><td>C</td></tr>
<tr><td>17 / 24</td><td>70.8%</td><td>C-</td></tr>
</tbody></table></div>
<p>Each rubric point here is worth about 4.2 percentage points, so one point usually moves a grade by a single plus or minus step rather than a full letter.</p>

<h2 id="the-catch">The catch with converting rubrics to percentages</h2>
<p>Look at the chart again. A 3 out of 4 usually means "proficient" or "meets the standard," yet a straight conversion turns it into a C. A 2, often described as "approaching the standard," becomes an F.</p>
<p>That's a known problem with converting short rubric scales directly. Because a 4-point rubric has so few steps, each point is worth 25 percentage points. For that reason, some schools and teachers use their own conversion tables that map rubric levels to percentages (for example, treating a 3 as a B). Others use standards-based report cards that avoid percentages altogether.</p>
<p>This calculator shows the straight mathematical conversion. If your school publishes its own rubric conversion table, that table takes priority. Our article on <a href="/blog/standards-based-grading">standards-based grading</a> explains the reasoning behind those alternatives.</p>

<h2 id="tips">Tips for teachers</h2>
<ul>
  <li><strong>Use more points for finer grades.</strong> A rubric with 6 criteria worth 4 points each (24 total) gives 4.2-point steps instead of 25-point steps.</li>
  <li><strong>Weight important criteria.</strong> If "thesis" matters more than "formatting," make it worth more points on the rubric.</li>
  <li><strong>Share the conversion upfront.</strong> Tell students how rubric scores become grades before the assignment, not after.</li>
  <li><strong>Be consistent across sections.</strong> If you teach several class periods, use the same rubric total and conversion for each so grades stay comparable.</li>
  <li><strong>Put rubric grades in context.</strong> Once you have the percentage, enter it as a category score in the <a href="/weighted-grade-calculator">weighted grade calculator</a> to see its effect on the overall grade.</li>
</ul>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Print or screenshot the conversion chart for your rubric's total. Grading a stack of 30 essays goes much faster when every possible score is already converted.</p></div>
HTML,
  'faqs'        => [
    ["How do I convert a rubric score to a percentage?", "Divide the points earned by the total rubric points and multiply by 100. For example, 18 out of 24 is 75%."],
    ["What is a 3 out of 4 on a rubric as a percentage?", "A straight conversion gives 3 ÷ 4 = 75%, a C on the standard scale. Many schools use their own table that treats a 3 as higher, so check your school's policy."],
    ["What grade is 3.5 out of 4?", "3.5 ÷ 4 = 87.5%, a B+ on the standard US scale."],
    ["Can I enter decimal rubric scores?", "Yes. You can enter averages like 3.25 out of 4, and the chart includes every whole and half score."],
    ["Why do rubric grades seem low as percentages?", "On short rubric scales, each point is a big share of the total. On a 4-point rubric, one point is 25 percentage points, so a small drop looks like a big grade change."],
  ],
];
