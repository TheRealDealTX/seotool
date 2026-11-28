<?php
return [
  'h1'          => 'Test Grade Calculator',
  'meta_title'  => 'Test Grade Calculator – Score by Number Wrong',
  'description' => 'Free test grade calculator: enter total questions or points and the number wrong (or right) to get your test score percentage, letter grade and a full chart.',
  'lead'        => 'Enter how many questions were on the test and how many you missed to get your percentage, letter grade, and a full score chart.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the test grade calculator</h2>
<p>A test grade calculator turns "I missed 6 out of 40" into a percentage and a letter grade in one step. It's handy for students checking a returned test and for teachers grading a stack of quizzes.</p>
<ol class="steps">
  <li><strong>Enter the total.</strong> Type the number of questions on the test, or the total points if questions are worth different amounts.</li>
  <li><strong>Enter the number wrong.</strong> Type how many questions (or points) were missed. Prefer counting correct answers? Use the toggle to switch to number right.</li>
  <li><strong>Read your score.</strong> You'll see the percentage and the matching letter grade.</li>
  <li><strong>Check the chart.</strong> Below the result, a full chart lists every possible number wrong with its percentage, so you can see the whole grading scale for that test at a glance.</li>
</ol>

<h2 id="formula">The test score formula</h2>
<p>Your test percentage is the share of questions (or points) you earned.</p>
<div class="formula">Test score % = (Total − Number wrong) ÷ Total × 100</div>
<p>If you count correct answers instead, it's simply Number right ÷ Total × 100. Each question you miss costs you 100 ÷ Total percentage points, which is why a single miss hurts more on a short quiz than on a long exam.</p>

<div class="example-box"><h4>Worked example</h4>
<p>A test has 40 questions and you missed 6.</p>
<p>40 − 6 = 34 correct<br>34 ÷ 40 = 0.85<br>0.85 × 100 = <strong>85%</strong></p>
<p>On the standard US scale, 85% is a <strong>B</strong> (83–86). Each question on this test is worth 100 ÷ 40 = 2.5 percentage points.</p>
</div>

<div class="example-box"><h4>Example: a short quiz</h4>
<p>A 25-question quiz with 3 wrong: 22 ÷ 25 × 100 = <strong>88%</strong>, a <strong>B+</strong>. Here each question is worth 4 points, so one more miss would drop the score to 84%.</p>
</div>

<h2 id="how-many-can-i-miss">How many questions can I miss?</h2>
<p>Students often ask the question the other way around: how many can I get wrong and still get an A or a B? The chart answers it at a glance, but the math is quick too. Multiply the total by the share you're allowed to lose, then round down.</p>
<div class="example-box"><h4>Example: a 30-question test</h4>
<p>To score at least 90%, you can lose 10% of 30 = 3 questions (27 ÷ 30 = 90%).<br>To score at least 80%, you can lose 20% of 30 = 6 questions (24 ÷ 30 = 80%).<br>To pass with at least 60%, you can lose 40% of 30 = 12 questions (18 ÷ 30 = 60%).</p>
<p>Miss a 4th question and you drop to 26 ÷ 30 = 86.7%, a B. That's why short tests feel so unforgiving.</p>
</div>

<h2 id="points-tests">Tests with different point values</h2>
<p>If some questions are worth more than others, enter total points instead of total questions, and points lost instead of questions wrong. A test with 20 multiple-choice questions worth 2 points each and 4 short answers worth 5 points each has 60 total points. Losing 9 points gives 51 ÷ 60 = 85%.</p>

<h2 id="letter-scale">Letter grade scale used</h2>
<p>The letter grade follows the common US scale. Your teacher's cutoffs may differ, so check your syllabus.</p>
<div class="table-wrap"><table class="data-table"><thead><tr><th>Letter</th><th>Percentage</th></tr></thead><tbody>
<tr><td>A+ / A / A-</td><td>97–100 / 93–96 / 90–92</td></tr>
<tr><td>B+ / B / B-</td><td>87–89 / 83–86 / 80–82</td></tr>
<tr><td>C+ / C / C-</td><td>77–79 / 73–76 / 70–72</td></tr>
<tr><td>D+ / D / D-</td><td>67–69 / 63–66 / 60–62</td></tr>
<tr><td>F</td><td>Below 60</td></tr>
</tbody></table></div>

<h2 id="tips">Tips for students and teachers</h2>
<ul>
  <li><strong>Check partial credit.</strong> If you earned half credit on a question, enter the test's total points and the points you lost instead of whole questions, so the half point counts.</li>
  <li><strong>Know what one question is worth.</strong> On a 10-question quiz, every miss is 10 points. That's a full letter grade per question.</li>
  <li><strong>Teachers: print the chart.</strong> The number-wrong chart doubles as a quick answer key for grading. For a dedicated printable chart with half-point steps, try the <a href="/easy-grader">EZ grader</a>.</li>
  <li><strong>See the bigger picture.</strong> One test is only part of your class grade. Plug your test average into the <a href="/weighted-grade-calculator">weighted grade calculator</a> to see how it affects your overall grade.</li>
</ul>
<div class="callout callout-info"><strong>Good to know</strong><p>Some teachers round scores (84.5 up to 85, for example) and some don't. If your percentage lands right on a cutoff, ask how your teacher rounds.</p></div>
HTML,
  'faqs'        => [
    ["How do I calculate my test grade?", "Subtract the number wrong from the total, divide by the total, and multiply by 100. Missing 6 out of 40 gives 34 ÷ 40 × 100 = 85%."],
    ["What is 17 out of 20 as a grade?", "17 ÷ 20 × 100 = 85%, which is a B on the standard US scale."],
    ["How much is each question worth?", "Divide 100 by the number of questions. On a 25-question test, each question is worth 4 percentage points; on a 50-question test, each is worth 2."],
    ["Can I enter the number right instead of the number wrong?", "Yes. Use the toggle to switch from number wrong to number right. The percentage and chart update either way."],
    ["What if questions are worth different points?", "Enter total points instead of total questions and points missed instead of questions wrong. The math is the same."],
  ],
];
