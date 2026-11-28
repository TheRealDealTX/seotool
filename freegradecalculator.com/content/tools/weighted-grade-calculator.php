<?php
return [
  'h1'          => 'Weighted Grade Calculator',
  'meta_title'  => 'Weighted Grade Calculator – Grade by Category Weight',
  'description' => 'Free weighted grade calculator: enter each category weight and score (as a % or letter) to get your weighted average, letter grade and 4.0 GPA points.',
  'lead'        => 'Enter each grading category, its weight, and your score to see your weighted class grade, letter grade, and GPA points instantly.',
  'body'        => <<<'HTML'
<h2 id="how-to-use">How to use the weighted grade calculator</h2>
<p>Most teachers don't average every assignment equally. Tests might be worth half your grade while homework is worth a fifth. A weighted grade calculator does that math for you, category by category.</p>
<ol class="steps">
  <li><strong>Find your syllabus weights.</strong> Look for a breakdown like "Homework 20%, Quizzes 30%, Tests 50%." Each category becomes one row.</li>
  <li><strong>Enter a name and weight for each row.</strong> The name is just a label (Labs, Essays, Participation). The weight is the percentage your teacher assigns to it.</li>
  <li><strong>Enter your score for each category.</strong> Type a percentage like 88, or a letter like A- or B+. Use your current average in that category from your gradebook or school portal.</li>
  <li><strong>Add or remove rows as needed.</strong> Classes with five or six categories work the same way as classes with two.</li>
  <li><strong>Read your results.</strong> You get your weighted percentage, the matching letter grade, and the 4.0 GPA points for that letter.</li>
</ol>

<h2 id="formula">The weighted grade formula</h2>
<p>Each score is multiplied by its weight, the products are added together, and the total is divided by the sum of the weights.</p>
<div class="formula">Weighted grade = Σ (score × weight) ÷ Σ weights</div>
<p>When your weights add up to 100, dividing by the total weight changes nothing. When they don't (for example, your teacher hasn't entered the final exam yet), the calculator normalizes by the total weight you entered and tells you it did so. That gives you your grade based only on the work that has been graded so far.</p>

<div class="example-box"><h4>Worked example</h4>
<p>Your class counts Homework 20%, Quizzes 30%, and Tests 50%. Your averages are 92, 85, and 80.</p>
<p>Homework: 92 × 0.20 = 18.4<br>Quizzes: 85 × 0.30 = 25.5<br>Tests: 80 × 0.50 = 40.0</p>
<p>18.4 + 25.5 + 40.0 = <strong>83.9%</strong>, which is a <strong>B</strong> on the standard scale (83–86) and worth <strong>3.0</strong> GPA points.</p>
</div>

<div class="example-box"><h4>Example: weights that don't add to 100</h4>
<p>Same class, but a 10% project hasn't been graded yet, so you enter Homework 20, Quizzes 30, Tests 40 (total 90) with the same scores.</p>
<p>(92 × 20 + 85 × 30 + 80 × 40) ÷ 90 = (1,840 + 2,550 + 3,200) ÷ 90 = 7,590 ÷ 90 = <strong>84.3%</strong>.</p>
<p>That's your current grade on the 90% of the class that has been graded.</p>
</div>

<h2 id="weighted-vs-points">Weighted grades vs. total points</h2>
<p>Some teachers use a points system instead: every assignment is worth a set number of points and your grade is total earned divided by total possible. If your syllabus lists point values instead of percentages, use the <a href="/points-grade-calculator">points grade calculator</a> instead.</p>
<p>The difference matters. In a weighted class, a 10-question quiz can count as much as a 100-point test if both categories carry the same weight. In a points class, the bigger assignment always counts more.</p>

<h2 id="common-mistakes">Common mistakes to avoid</h2>
<ul>
  <li><strong>Averaging categories without weights.</strong> A simple average of 92, 85, and 80 is 85.7, which overstates the grade in the example above by almost two points because tests count most.</li>
  <li><strong>Entering individual assignments as categories.</strong> Each row should be a category average, not a single quiz, unless your teacher weights each assignment separately.</li>
  <li><strong>Forgetting dropped scores.</strong> If your teacher drops the lowest quiz, recalculate the category average without it before entering it.</li>
  <li><strong>Assuming every school uses the same letter cutoffs.</strong> This calculator uses the common US scale (A 93–96, A- 90–92, and so on). Your school's scale may differ, so check your handbook.</li>
</ul>

<h2 id="what-if">Use it for "what if" planning</h2>
<p>Change one category score to see how much it moves your overall grade. Because tests carry the most weight in many classes, raising a test average by 5 points usually moves your grade more than raising homework by 10.</p>
<p>If you want to know exactly what you need on a final exam, the <a href="/final-grade-calculator">final grade calculator</a> solves for it directly. For a deeper walkthrough of the math, read our guide on <a href="/blog/how-to-calculate-weighted-grades">how to calculate weighted grades</a>.</p>
<div class="callout callout-tip"><strong>Pro tip</strong><p>Check your school portal's category averages, not just the overall grade. Portals sometimes show unweighted totals until the end of a grading period, and entering the categories here gives you the real weighted picture.</p></div>
HTML,
  'faqs'        => [
    ["How do I calculate my weighted grade?", "Multiply each category average by its weight, add the results, and divide by the total of the weights. For Homework 20% at 92, Quizzes 30% at 85, and Tests 50% at 80, the weighted grade is 18.4 + 25.5 + 40 = 83.9%."],
    ["What if my category weights don't add up to 100%?", "The calculator divides by the total weight you entered, so you see your grade based on the categories graded so far. It shows a note whenever it normalizes this way."],
    ["Can I enter letter grades instead of percentages?", "Yes. Each score can be a percentage like 87 or a letter like A- or B+. You can mix both in the same calculation."],
    ["What GPA points does my weighted grade equal?", "The calculator converts your weighted percentage to a letter on the standard US scale, then to 4.0 GPA points (for example, B = 3.0, B+ = 3.3, A- = 3.7)."],
    ["Is a weighted grade the same as a weighted GPA?", "No. A weighted grade combines categories within one class. A weighted GPA adds extra points for Honors or AP courses across all your classes. For that, use the high school GPA calculator."],
  ],
];
