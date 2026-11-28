<?php
return [
  'h1'          => 'Points Grade Calculator',
  'meta_title'  => 'Points Grade Calculator – Total Points to Percentage',
  'description' => 'Free points grade calculator: add assignments with points earned and points possible to get your total points, overall percentage and letter grade in seconds.',
  'lead'        => 'Add each assignment\'s points earned and points possible to see your total points, class percentage, and letter grade.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the points grade calculator</h2>
<p>Many classes use a total-points system: every assignment is worth a set number of points, and your grade is everything you've earned divided by everything that was possible. This points grade calculator adds it all up for you.</p>
<ol class="steps">
  <li><strong>Add a row for each assignment.</strong> Homework, quizzes, tests, projects: each one gets its own row.</li>
  <li><strong>Enter points earned.</strong> The points you received, such as 45.</li>
  <li><strong>Enter points possible.</strong> The maximum for that assignment, such as 50.</li>
  <li><strong>Read the totals.</strong> The calculator shows total points earned, total points possible, your percentage, and the letter grade.</li>
</ol>

<h2 id="formula">The points grade formula</h2>
<div class="formula">Grade % = Σ points earned ÷ Σ points possible × 100</div>
<p>Notice that you add the points first and divide once. You don't average the percentages of each assignment. That's what makes a points system different: bigger assignments automatically count more.</p>

<div class="example-box"><h4>Worked example</h4>
<p>You have four graded assignments:</p>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Assignment</th><th>Earned</th><th>Possible</th></tr></thead><tbody>
<tr><td>Homework set</td><td>45</td><td>50</td></tr>
<tr><td>Quiz</td><td>18</td><td>20</td></tr>
<tr><td>Unit test</td><td>82</td><td>100</td></tr>
<tr><td>Project</td><td>47</td><td>50</td></tr>
<tr><td><strong>Total</strong></td><td><strong>192</strong></td><td><strong>220</strong></td></tr>
</tbody></table></div>
<p>192 ÷ 220 = 0.8727, so your grade is <strong>87.3%</strong>, a <strong>B+</strong> (87–89).</p>
<p>If you had averaged the four percentages instead (90, 90, 82, 94), you'd get 89.0%, which overstates the grade because the 100-point test, your lowest score, carries the most points.</p>
</div>

<h2 id="one-assignment">How one big assignment changes your grade</h2>
<p>Because every point counts equally, a large assignment can move your grade a lot, especially early in the term when few points have been graded. It's worth checking before a big test so there are no surprises.</p>
<div class="example-box"><h4>Example: adding a 100-point test</h4>
<p>Continuing the example above, you take a second 100-point test and score 70.</p>
<p>New totals: 192 + 70 = 262 earned, 220 + 100 = 320 possible.<br>262 ÷ 320 = 0.8188 → <strong>81.9%</strong>, a <strong>B-</strong>.</p>
<p>One test dropped the grade by more than five points, from a B+ to a B-. If that test had been a 95 instead, the grade would be 287 ÷ 320 = 89.7%, which rounds to an A- at many schools.</p>
</div>
<p>To find your numbers, open your school portal and look for columns labeled "score" and "out of," or "points earned" and "points possible." Some portals also show a running total at the bottom of the class page, which you can use to double-check the calculator.</p>

<h2 id="points-vs-weighted">Points system vs. weighted categories</h2>
<div class="compare">
  <div class="compare-col"><h4>Total points</h4><ul><li>Every point counts equally</li><li>Big assignments matter most</li><li>Grade = earned ÷ possible</li></ul></div>
  <div class="compare-col"><h4>Weighted categories</h4><ul><li>Each category has a % weight</li><li>A small quiz category can still matter a lot</li><li>Grade = Σ (score × weight)</li></ul></div>
</div>
<p>If your syllabus lists percentages like "Tests 50%," you're in a weighted class. Use the <a href="/weighted-grade-calculator">weighted grade calculator</a> instead, because a points total will give the wrong answer.</p>

<h2 id="common-mistakes">Common mistakes</h2>
<ul>
  <li><strong>Averaging percentages.</strong> As the example shows, averaging assignment percentages ignores point values and can be off by a couple of points.</li>
  <li><strong>Leaving out zeros.</strong> A missing assignment still counts in points possible. Enter it as 0 earned so your total is accurate.</li>
  <li><strong>Counting extra credit as possible points.</strong> Extra credit usually adds to points earned only. Add it to an existing row's earned points, or as its own row with 0 possible, depending on how your teacher records it.</li>
  <li><strong>Using ungraded work.</strong> Only include assignments that have been scored. Future work belongs in a "what do I need" calculation.</li>
</ul>

<h2 id="planning-ahead">Planning for the rest of the term</h2>
<p>Once you know your current points, you can figure out what you need on upcoming work. The <a href="/raise-my-grade-calculator">raise my grade calculator</a> takes your points so far and the points still to come and tells you the average you need to hit a target percentage.</p>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Look at which assignments have the most points left in the term. In a points system, a single 200-point final project can swing your grade more than ten 10-point homework sets combined.</p></div>
HTML,
  'faqs'        => [
    ["How do I calculate my grade with points?", "Add up all the points you earned, add up all the points possible, divide the first total by the second, and multiply by 100. For 192 out of 220 points, that's 87.3%."],
    ["Should I average my assignment percentages?", "Not in a points-based class. Averaging percentages treats a 20-point quiz the same as a 100-point test. Adding points first gives the correct grade."],
    ["How do I enter a missing assignment?", "Enter 0 for points earned and the full value for points possible. Missing work still counts against your total."],
    ["What letter grade scale does it use?", "The common US scale: A 93–96, A- 90–92, B+ 87–89, B 83–86, and so on down to F below 60. Your school may use different cutoffs."],
    ["Is a points grade the same as a weighted grade?", "No. In a points system, every point is equal. In a weighted system, each category has a percentage weight regardless of its points. Check your syllabus to see which your class uses."],
  ],
];
